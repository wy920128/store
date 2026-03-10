#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MariaDB 数据库操作封装"""
import os
import base64
import pymysql
from pymysql.err import OperationalError, ProgrammingError
from dotenv import load_dotenv


class MariaDBManager:
    """MariaDB 操作类（单例）"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = None
            cls._instance.cursor = None
            cls._instance._init_config()
        return cls._instance

    def _init_config(self):
        """初始化数据库配置"""
        load_dotenv()
        self.config = {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", 3306)),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", "123456"),
            "database": os.getenv("DB_DATABASE", "uos"),
            "charset": "utf8mb4"
        }

    def connect(self) -> bool:
        """连接数据库"""
        try:
            self.conn = pymysql.connect(**self.config)
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            return True
        except OperationalError as e:
            print(f"MariaDB 连接失败：{e}")
            return False
        except Exception as e:
            print(f"MariaDB 连接异常：{e}")
            return False

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, sql: str, params: tuple = None) -> list:
        """执行查询SQL（通用方法）"""
        if not self.conn:
            if not self.connect():
                return []
        try:
            self.cursor.execute(sql, params or ())
            return self.cursor.fetchall()
        except ProgrammingError as e:
            print(f"SQL 执行失败：{e} | SQL: {sql}")
            return []

    def execute_update(self, sql: str, params: tuple = None) -> bool:
        """执行更新/插入/删除SQL"""
        if not self.conn:
            if not self.connect():
                return False
        try:
            self.cursor.execute(sql, params or ())
            self.conn.commit()
            return True
        except Exception as e:
            print(f"SQL 更新失败：{e} | SQL: {sql}")
            self.conn.rollback()
            return False

    # ========== 业务相关查询（保留兼容） ==========
    def get_all_classifies(self) -> list:
        """获取所有分类"""
        sql = """
        SELECT id, name, description 
        FROM classify 
        WHERE deleted_time IS NULL 
        ORDER BY id ASC
        """
        return self.execute_query(sql)

    def get_softwares_by_classify(self, classify_id: int = None) -> list:
        """获取指定分类下的软件"""
        if classify_id is None:
            sql = """
            SELECT * FROM software 
            WHERE deleted_time IS NULL 
            ORDER BY name ASC
            """
            return self.execute_query(sql)
        else:
            sql = """
            SELECT s.* 
            FROM software s
            JOIN classify2software c2s ON s.id = c2s.software_id
            WHERE c2s.classify_id = %s 
            AND s.deleted_time IS NULL 
            AND c2s.deleted_time IS NULL
            ORDER BY s.name ASC
            """
            return self.execute_query(sql, (classify_id,))

    def insert_software_icon(self, software_id: str, icon_path: str) -> bool:
        """插入软件图标"""
        try:
            with open(icon_path, "rb") as f:
                icon_data = base64.b64encode(f.read()).decode("utf-8")
            sql = "UPDATE software SET icon = %s WHERE id = %s"
            return self.execute_update(sql, (icon_data, software_id))
        except Exception as e:
            print(f"插入图标失败：{e}")
            return False

    def get_software_icon(self, software_id: str):
        """获取软件图标"""
        sql = "SELECT icon FROM software WHERE id = %s AND deleted_time IS NULL"
        result = self.execute_query(sql, (software_id,))
        if not result or not result[0]["icon"]:
            return None
        try:
            from PyQt6.QtGui import QPixmap
            icon_bytes = base64.b64decode(result[0]["icon"])
            pixmap = QPixmap()
            pixmap.loadFromData(icon_bytes)
            return pixmap
        except Exception as e:
            print(f"解码图标失败：{e}")
            return None
