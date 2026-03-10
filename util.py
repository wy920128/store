#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""缓存工具类（SQLite 本地缓存）"""
import os
import json
import sqlite3
import time
from datetime import datetime, timedelta
from mariadb import MariaDBManager

# 缓存文件路径
CACHE_DB_PATH = os.path.join(os.path.dirname(__file__), "app_cache.db")
# 缓存有效期（2小时）
CACHE_EXPIRE_HOURS = 2


class CacheManager:
    """SQLite 缓存管理类（单例）"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_cache_db()
            cls._instance.mariadb_manager = MariaDBManager()
        return cls._instance

    def _init_cache_db(self):
        """初始化SQLite缓存数据库"""
        # 创建缓存目录（如果不存在）
        os.makedirs(os.path.dirname(CACHE_DB_PATH), exist_ok=True)

        # 连接SQLite并创建缓存表
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()

        # 缓存表结构：key(唯一标识)、data(JSON数据)、create_time(缓存创建时间)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_cache (
            key TEXT PRIMARY KEY NOT NULL,
            data TEXT NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    def _get_cache_key(self, sql: str, params: tuple = None) -> str:
        """生成缓存KEY（SQL+参数拼接）"""
        param_str = json.dumps(params or ())
        return f"{sql}_{param_str}"

    def _is_cache_valid(self, create_time_str: str) -> bool:
        """判断缓存是否有效（小于2小时）"""
        try:
            create_time = datetime.strptime(
                create_time_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            delta = now - create_time
            return delta < timedelta(hours=CACHE_EXPIRE_HOURS)
        except Exception as e:
            print(f"判断缓存有效期失败：{e}")
            return False

    def get_data(self, sql: str, params: tuple = None) -> list:
        """
        获取数据（优先缓存，缓存失效则查MariaDB并更新缓存）
        :param sql: 查询SQL语句
        :param params: SQL参数
        :return: 查询结果列表
        """
        cache_key = self._get_cache_key(sql, params)

        # 1. 尝试从SQLite缓存读取
        conn = sqlite3.connect(CACHE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            # 查询缓存
            cursor.execute("""
            SELECT data, create_time FROM app_cache WHERE key = ?
            """, (cache_key,))
            cache_result = cursor.fetchone()

            if cache_result:
                # 缓存存在，判断是否有效
                if self._is_cache_valid(cache_result["create_time"]):
                    print(f"使用缓存：{cache_key}")
                    return json.loads(cache_result["data"])

            # 2. 缓存失效/不存在，查询MariaDB
            print(f"查询MariaDB：{cache_key}")
            mariadb_data = self.mariadb_manager.execute_query(sql, params)

            # 3. 更新缓存
            cursor.execute("""
            REPLACE INTO app_cache (key, data, create_time)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (cache_key, json.dumps(mariadb_data, ensure_ascii=False)))
            conn.commit()

            return mariadb_data

        except Exception as e:
            print(f"获取缓存/数据库数据失败：{e}")
            return []
        finally:
            conn.close()

    def clear_expired_cache(self):
        """清理过期缓存（大于2小时）"""
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()

        # 计算过期时间
        expire_time = datetime.now() - timedelta(hours=CACHE_EXPIRE_HOURS)
        expire_time_str = expire_time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor.execute("""
            DELETE FROM app_cache WHERE create_time < ?
            """, (expire_time_str,))
            deleted_count = cursor.rowcount
            conn.commit()
            print(f"清理过期缓存：{deleted_count} 条")
        except Exception as e:
            print(f"清理过期缓存失败：{e}")
        finally:
            conn.close()

    def clear_all_cache(self):
        """清空所有缓存"""
        conn = sqlite3.connect(CACHE_DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM app_cache")
            conn.commit()
            print("清空所有缓存成功")
        except Exception as e:
            print(f"清空缓存失败：{e}")
        finally:
            conn.close()


# 全局缓存实例
cache_manager = CacheManager()

# 快捷查询函数（供业务调用）


def query_with_cache(sql: str, params: tuple = None) -> list:
    """带缓存的查询函数（快捷调用）"""
    return cache_manager.get_data(sql, params)
