#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自动更新模块：对比MariaDB与本地SQLite版本，版本更高则更新"""
import os
import sys
import json
import sqlite3
import subprocess
from datetime import datetime
from mariadb import MariaDBManager
from util import CACHE_DB_PATH  # 复用缓存文件路径


class UpgradeManager:
    """版本更新管理器"""

    def __init__(self):
        self.mariadb_manager = MariaDBManager()
        self.mariadb_manager.connect()
        self.local_db_path = CACHE_DB_PATH  # 本地SQLite缓存文件（复用）
        self.app_name = "UOS应用商店"  # 要检查更新的软件名称

    def __del__(self):
        """析构函数：关闭数据库连接"""
        self.mariadb_manager.close()

    def _init_local_system_info(self):
        """初始化本地SQLite的system_info表（不存在则创建）"""
        conn = sqlite3.connect(self.local_db_path)
        cursor = conn.cursor()

        # 创建system_info表（与MariaDB结构一致）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (
            name TEXT NOT NULL PRIMARY KEY,
            version TEXT NOT NULL,
            author TEXT,
            created_time TIMESTAMP,
            update_time TIMESTAMP,
            deleted_time TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    def _get_local_version(self) -> str:
        """获取本地SQLite中的软件版本"""
        self._init_local_system_info()
        conn = sqlite3.connect(self.local_db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
            SELECT version FROM system_info 
            WHERE name = ? AND deleted_time IS NULL
            """, (self.app_name,))
            result = cursor.fetchone()
            # 本地无记录时返回默认版本
            return result[0] if result else "1.0.0"
        except Exception as e:
            print(f"读取本地版本失败：{e}")
            return "1.0.0"
        finally:
            conn.close()

    def _get_server_version(self) -> str:
        """获取MariaDB中的软件版本"""
        sql = """
        SELECT version FROM system_info 
        WHERE name = %s AND deleted_time IS NULL
        ORDER BY update_time DESC LIMIT 1
        """
        result = self.mariadb_manager.execute_query(sql, (self.app_name,))
        # 服务器无记录时返回本地版本（不更新）
        return result[0]["version"] if result else self._get_local_version()

    def _compare_version(self, local_ver: str, server_ver: str) -> int:
        """
        版本对比：返回1（服务器更高）、0（相同）、-1（本地更高）
        版本格式：x.y.z（如1.0.0、1.2.3）
        """
        try:
            # 拆分版本号为数字列表
            local_parts = [int(part) for part in local_ver.split(".")]
            server_parts = [int(part) for part in server_ver.split(".")]

            # 补齐长度（如1.0 vs 1.0.1 → 1.0.0 vs 1.0.1）
            max_len = max(len(local_parts), len(server_parts))
            local_parts += [0] * (max_len - len(local_parts))
            server_parts += [0] * (max_len - len(server_parts))

            # 逐位对比
            for l, s in zip(local_parts, server_parts):
                if s > l:
                    return 1
                elif s < l:
                    return -1
            return 0
        except Exception as e:
            print(f"版本对比失败：{e}")
            return 0

    def _update_local_version(self, new_version: str):
        """更新本地SQLite中的版本号"""
        self._init_local_system_info()
        conn = sqlite3.connect(self.local_db_path)
        cursor = conn.cursor()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # 插入/更新版本记录
            cursor.execute("""
            REPLACE INTO system_info (
                name, version, author, created_time, update_time, deleted_time
            ) VALUES (?, ?, ?, 
                (SELECT created_time FROM system_info WHERE name = ?) OR ?, 
                ?, NULL)
            """, (self.app_name, new_version, "Admin", self.app_name, now, now))
            conn.commit()
            print(f"本地版本已更新为：{new_version}")
        except Exception as e:
            print(f"更新本地版本失败：{e}")
        finally:
            conn.close()

    def _execute_update(self, update_script: str = None):
        """
        执行更新操作（可扩展：下载安装包、执行更新脚本等）
        此处为示例：打印更新日志 + 模拟更新
        """
        print("="*50)
        print(f"开始更新 {self.app_name} ...")
        print("模拟下载更新包...")
        # 实际场景可替换为：
        # 1. 下载最新安装包（如wget/curl）
        # 2. 执行安装脚本（如bash update.sh）
        # 3. 覆盖本地文件
        import time
        time.sleep(2)
        print("更新完成！")
        print("="*50)

    def check_and_upgrade(self) -> bool:
        """
        检查更新并执行升级
        :return: True=已更新，False=无需更新/更新失败
        """
        # 1. 获取本地和服务器版本
        local_ver = self._get_local_version()
        server_ver = self._get_server_version()
        print(f"本地版本：{local_ver} | 服务器版本：{server_ver}")

        # 2. 版本对比
        compare_result = self._compare_version(local_ver, server_ver)

        if compare_result == 1:
            # 服务器版本更高，执行更新
            print(f"发现新版本：{server_ver}，开始更新...")
            try:
                self._execute_update()
                self._update_local_version(server_ver)
                return True
            except Exception as e:
                print(f"更新失败：{e}")
                return False
        elif compare_result == 0:
            print("当前已是最新版本，无需更新")
            return False
        else:
            print("本地版本高于服务器版本，无需更新")
            return False

# ===================== 快捷调用函数 =====================


def check_app_upgrade() -> bool:
    """检查并执行应用更新（快捷函数）"""
    upgrade_manager = UpgradeManager()
    return upgrade_manager.check_and_upgrade()


# ===================== 测试入口 =====================
if __name__ == "__main__":
    # 测试更新逻辑
    check_app_upgrade()
