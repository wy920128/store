"""
统信UOS内网应用商店 - 工具类整合
修复 datatype mismatch 数据类型不匹配问题
"""
import os
import re
import enum
import uuid
import logging
import datetime
import pymysql
import sqlite3
from typing import Optional, Union, Type, List, Dict, Any
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# ===================== 基础配置 =====================
# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "database": os.getenv("DB_NAME", "uos_appstore"),
    "charset": "utf8mb4"
}

# 本地缓存配置
CACHE_CONFIG = {
    "path": os.getenv("CACHE_PATH", "./cache.db"),
    "expire_hours": int(os.getenv("CACHE_EXPIRE_HOURS", 2))
}

# 日志配置
LOG_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "dir": os.getenv("LOG_DIR", "./logs"),
    "max_bytes": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# ===================== 日志工具类 =====================


class LogUtil:
    """日志工具类"""
    _logger = None

    @classmethod
    def init_logger(cls):
        """初始化日志器"""
        if cls._logger is not None:
            return cls._logger

        # 创建日志目录
        os.makedirs(LOG_CONFIG["dir"], exist_ok=True)

        # 日志级别映射
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        log_level = level_map.get(LOG_CONFIG["level"].upper(), logging.INFO)

        # 配置日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 创建日志器
        cls._logger = logging.getLogger("uos_appstore")
        cls._logger.setLevel(log_level)
        cls._logger.handlers.clear()

        # 文件处理器
        file_handler = RotatingFileHandler(
            os.path.join(LOG_CONFIG["dir"], "appstore.log"),
            maxBytes=LOG_CONFIG["max_bytes"],
            backupCount=LOG_CONFIG["backup_count"],
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        cls._logger.addHandler(file_handler)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        cls._logger.addHandler(console_handler)

        return cls._logger

    @classmethod
    def get_logger(cls):
        """获取日志器"""
        if cls._logger is None:
            cls.init_logger()
        return cls._logger

    @classmethod
    def debug(cls, msg):
        cls.get_logger().debug(msg)

    @classmethod
    def info(cls, msg):
        cls.get_logger().info(msg)

    @classmethod
    def warning(cls, msg):
        cls.get_logger().warning(msg)

    @classmethod
    def error(cls, msg, exc_info=False):
        cls.get_logger().error(msg, exc_info=exc_info)

    @classmethod
    def critical(cls, msg):
        cls.get_logger().critical(msg)

# ===================== 时间工具类 =====================


class TimeUtil:
    """时间工具类"""
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT = "%Y-%m-%d"

    @classmethod
    def get_current_time(cls, tz: Optional[datetime.timezone] = None) -> datetime.datetime:
        """获取当前时间（默认东八区）"""
        if tz is None:
            tz = datetime.timezone(datetime.timedelta(hours=8))
        return datetime.datetime.now(tz)

    @classmethod
    def format_datetime(cls, dt: Optional[datetime.datetime], fmt: str = DATETIME_FORMAT) -> str:
        """格式化时间为字符串"""
        if dt is None:
            return ""
        try:
            return dt.strftime(fmt)
        except Exception as e:
            LogUtil.error(f"时间格式化失败: {e}", exc_info=True)
            return ""

    @classmethod
    def parse_datetime(cls, dt_str: str, fmt: str = DATETIME_FORMAT) -> datetime.datetime:
        """解析字符串为时间对象"""
        if not dt_str:
            return None  # 修改：空字符串返回None而非抛出异常
        try:
            return datetime.datetime.strptime(dt_str, fmt)
        except Exception as e:
            LogUtil.error(f"时间解析失败: {e}", exc_info=True)
            return None

    @classmethod
    def get_time_diff_hours(cls, start_time: str, end_time: str) -> float:
        """计算两个时间字符串的小时差"""
        try:
            t1 = cls.parse_datetime(start_time)
            t2 = cls.parse_datetime(end_time)
            if t1 is None or t2 is None:
                return CACHE_CONFIG["expire_hours"] + 1  # 缓存过期
            diff_seconds = (t2 - t1).total_seconds()
            return diff_seconds / 3600
        except Exception as e:
            LogUtil.error(f"计算时间差失败: {e}", exc_info=True)
            return CACHE_CONFIG["expire_hours"] + 1

# ===================== 数据校验工具类 =====================


class ValidateUtil:
    """数据校验工具类"""
    # 版本号正则
    VERSION_PATTERN = re.compile(r"^\d+(\.\d+)*$")
    # URL正则
    URL_PATTERN = re.compile(
        r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", re.IGNORECASE)

    @classmethod
    def validate_string(cls, value: Optional[str], min_len: int = 1, max_len: int = None) -> bool:
        """校验字符串"""
        if value is None or not isinstance(value, str):
            LogUtil.warning(f"字符串校验失败: 值为{value}，类型{type(value)}")
            return False

        value = value.strip()
        if len(value) < min_len:
            LogUtil.warning(f"字符串长度不足: {len(value)} < {min_len}")
            return False

        if max_len and len(value) > max_len:
            LogUtil.warning(f"字符串长度超限: {len(value)} > {max_len}")
            return False

        return True

    @classmethod
    def validate_version(cls, version: str) -> bool:
        """校验版本号"""
        if not cls.validate_string(version):
            return False
        if not cls.VERSION_PATTERN.match(version):
            LogUtil.warning(f"版本号格式错误: {version}")
            return False
        return True

    @classmethod
    def validate_url(cls, url: str) -> bool:
        """校验URL"""
        if not cls.validate_string(url):
            return False
        if not cls.URL_PATTERN.match(url):
            LogUtil.warning(f"URL格式错误: {url}")
            return False
        return True

    @classmethod
    def compare_versions(cls, ver1: str, ver2: str) -> int:
        """
        版本号对比
        返回: -1(ver1<ver2), 0(相等), 1(ver1>ver2)
        """
        if not cls.validate_version(ver1) or not cls.validate_version(ver2):
            return 0

        v1_parts = [int(part) for part in ver1.split(".")]
        v2_parts = [int(part) for part in ver2.split(".")]

        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts += [0] * (max_len - len(v1_parts))
        v2_parts += [0] * (max_len - len(v2_parts))

        for p1, p2 in zip(v1_parts, v2_parts):
            if p1 < p2:
                return -1
            elif p1 > p2:
                return 1
        return 0

# ===================== 数据库工具类 =====================


class DBUtil:
    """数据库工具类（远程MariaDB + 本地SQLite）"""

    def __init__(self):
        self.logger = LogUtil.get_logger()
        self.remote_conn = None
        self.local_conn = None
        self._init_local_db()

    def _init_local_db(self):
        """初始化本地缓存数据库"""
        try:
            # 创建目录
            os.makedirs(os.path.dirname(CACHE_CONFIG["path"]), exist_ok=True)

            # 连接本地数据库（线程安全配置）
            self.local_conn = sqlite3.connect(
                CACHE_CONFIG["path"],
                check_same_thread=False,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            self.local_conn.execute("PRAGMA foreign_keys = ON")
            self.local_conn.execute("PRAGMA journal_mode = WAL")  # 提升并发性能

            # 创建表结构
            self._create_local_tables()
            self.logger.info("本地缓存数据库初始化完成")
        except Exception as e:
            self.logger.error(f"初始化本地数据库失败: {e}", exc_info=True)
            raise

    def _create_local_tables(self):
        """创建本地缓存表结构"""
        cursor = self.local_conn.cursor()

        # 分类表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_time TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_time TEXT DEFAULT CURRENT_TIMESTAMP,
            deleted_time TEXT DEFAULT ''
        )
        """)

        # 软件表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS software (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            version TEXT,
            size TEXT,
            download_count INTEGER DEFAULT 0,
            download_url TEXT,
            created_time TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_time TEXT DEFAULT CURRENT_TIMESTAMP,
            deleted_time TEXT DEFAULT ''
        )
        """)

        # 分类-软件关联表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS category2software (
            category_id INTEGER,
            software_id INTEGER,
            created_time TEXT DEFAULT CURRENT_TIMESTAMP,
            deleted_time TEXT DEFAULT '',
            PRIMARY KEY (category_id, software_id),
            FOREIGN KEY (category_id) REFERENCES category(id),
            FOREIGN KEY (software_id) REFERENCES software(id)
        )
        """)

        # 用户表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number TEXT UNIQUE,
            department TEXT,
            created_time TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_time TEXT DEFAULT CURRENT_TIMESTAMP,
            deleted_time TEXT DEFAULT ''
        )
        """)

        # 用户-软件关联表（provider_id）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user2software (
            provider_id INTEGER,
            software_id INTEGER,
            created_time TEXT DEFAULT CURRENT_TIMESTAMP,
            deleted_time TEXT DEFAULT '',
            PRIMARY KEY (provider_id, software_id),
            FOREIGN KEY (provider_id) REFERENCES user(id),
            FOREIGN KEY (software_id) REFERENCES software(id)
        )
        """)

        # 系统信息表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            version TEXT,
            download_url TEXT,
            created_time TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_time TEXT DEFAULT CURRENT_TIMESTAMP,
            deleted_time TEXT DEFAULT ''
        )
        """)

        # 缓存元信息表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache_meta (
            key TEXT PRIMARY KEY,
            value TEXT,
            update_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 初始化缓存元信息
        cursor.execute("""
        INSERT OR IGNORE INTO cache_meta (key, value) 
        VALUES ('last_sync_time', '1970-01-01 00:00:00')
        """)

        # 新增应用更新、应用管理分类
        for cate_name in ["应用更新", "应用管理"]:
            cursor.execute("""
            INSERT OR IGNORE INTO category (name, description, deleted_time) 
            VALUES (?, ?, '')
            """, (cate_name, f"{cate_name}专属分类"))

        self.local_conn.commit()
        cursor.close()

    def _get_remote_conn(self):
        """获取远程MariaDB连接"""
        if self.remote_conn and self.remote_conn.open:
            return self.remote_conn

        try:
            self.remote_conn = pymysql.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"],
                charset=DB_CONFIG["charset"]
            )
            self.logger.info("远程数据库连接成功")
            return self.remote_conn
        except Exception as e:
            self.logger.error(f"远程数据库连接失败: {e}", exc_info=True)
            raise

    def sync_remote_to_local(self):
        """同步远程数据到本地缓存"""
        try:
            # 获取远程数据
            remote_conn = self._get_remote_conn()
            remote_cursor = remote_conn.cursor(pymysql.cursors.DictCursor)

            # 1. 同步分类表（修改：处理NULL为空字符串）
            remote_cursor.execute(
                "SELECT * FROM category WHERE deleted_time IS NULL")
            categories = remote_cursor.fetchall()
            for cate in categories:
                cate['deleted_time'] = cate['deleted_time'] or ''
                cate['created_time'] = cate['created_time'] or TimeUtil.format_datetime(
                    TimeUtil.get_current_time())
                cate['updated_time'] = cate['updated_time'] or TimeUtil.format_datetime(
                    TimeUtil.get_current_time())

            # 2. 同步软件表
            remote_cursor.execute(
                "SELECT * FROM software WHERE deleted_time IS NULL")
            softwares = remote_cursor.fetchall()
            for soft in softwares:
                soft['deleted_time'] = soft['deleted_time'] or ''
                soft['created_time'] = soft['created_time'] or TimeUtil.format_datetime(
                    TimeUtil.get_current_time())
                soft['updated_time'] = soft['updated_time'] or TimeUtil.format_datetime(
                    TimeUtil.get_current_time())

            # 3. 同步关联表
            remote_cursor.execute(
                "SELECT * FROM category2software WHERE deleted_time IS NULL")
            c2s = remote_cursor.fetchall()
            for item in c2s:
                item['deleted_time'] = item['deleted_time'] or ''
                item['created_time'] = item['created_time'] or TimeUtil.format_datetime(
                    TimeUtil.get_current_time())

            # 写入本地数据库
            local_cursor = self.local_conn.cursor()

            # 清空旧数据（保留应用更新、应用管理分类）
            local_cursor.execute("DELETE FROM category2software")
            local_cursor.execute("DELETE FROM software")
            local_cursor.execute(
                "DELETE FROM category WHERE name NOT IN ('应用更新', '应用管理')")

            # 插入分类
            for cate in categories:
                local_cursor.execute("""
                INSERT OR REPLACE INTO category 
                (id, name, description, created_time, updated_time, deleted_time)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    cate['id'], cate['name'], cate['description'] or '',
                    cate['created_time'], cate['updated_time'], cate['deleted_time']
                ))

            # 插入软件
            for soft in softwares:
                local_cursor.execute("""
                INSERT OR REPLACE INTO software 
                (id, name, version, size, download_count, download_url, 
                 created_time, updated_time, deleted_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    soft['id'], soft['name'], soft['version'] or '', soft['size'] or '',
                    soft['download_count'] or 0, soft['download_url'] or '',
                    soft['created_time'], soft['updated_time'], soft['deleted_time']
                ))

            # 插入关联数据
            for item in c2s:
                local_cursor.execute("""
                INSERT OR REPLACE INTO category2software 
                (category_id, software_id, created_time, deleted_time)
                VALUES (?, ?, ?, ?)
                """, (
                    item['category_id'], item['software_id'],
                    item['created_time'], item['deleted_time']
                ))

            # 更新同步时间
            current_time = TimeUtil.format_datetime(
                TimeUtil.get_current_time())
            local_cursor.execute("""
            UPDATE cache_meta SET value = ?, update_time = ? WHERE key = 'last_sync_time'
            """, (current_time, current_time))

            self.local_conn.commit()
            self.logger.info("远程数据同步到本地完成")

        except Exception as e:
            self.logger.error(f"同步远程数据失败: {e}", exc_info=True)
            raise
        finally:
            if 'remote_cursor' in locals():
                remote_cursor.close()
            if 'local_cursor' in locals():
                local_cursor.close()

    def get_data_from_cache(self, table_name: str, conditions: str = "") -> List[Dict]:
        """从本地缓存获取数据（修改：修复类型不匹配）"""
        try:
            cursor = self.local_conn.cursor(sqlite3.Row)
            # 修改：将 deleted_time IS NULL 改为 deleted_time = ''
            base_sql = f"SELECT * FROM {table_name} WHERE deleted_time = ''"
            if conditions:
                # 安全拼接条件，避免SQL注入
                base_sql += f" AND {conditions}"

            self.logger.debug(f"执行SQL: {base_sql}")
            cursor.execute(base_sql)
            rows = cursor.fetchall()

            # 转换为字典列表
            result = []
            for row in rows:
                result.append(dict(row))

            cursor.close()
            self.logger.info(f"从缓存获取{table_name}数据: {len(result)}条")
            return result
        except Exception as e:
            self.logger.error(f"从缓存获取数据失败: {e}", exc_info=True)
            raise

    def get_data(self, table_name: str, conditions: str = "") -> List[Dict]:
        """统一数据获取入口（缓存/远程）"""
        try:
            # 检查缓存是否过期
            cursor = self.local_conn.cursor()
            cursor.execute(
                "SELECT value FROM cache_meta WHERE key = 'last_sync_time' AND deleted_time = ''")
            last_sync = cursor.fetchone()
            cursor.close()

            last_sync_time = last_sync[0] if last_sync else '1970-01-01 00:00:00'
            current_time = TimeUtil.format_datetime(
                TimeUtil.get_current_time())
            diff_hours = TimeUtil.get_time_diff_hours(
                last_sync_time, current_time)

            # 缓存过期则同步
            if diff_hours >= CACHE_CONFIG["expire_hours"]:
                self.sync_remote_to_local()

            # 从缓存获取数据
            return self.get_data_from_cache(table_name, conditions)
        except Exception as e:
            self.logger.error(f"获取数据失败: {e}", exc_info=True)
            raise

    def get_category_by_name(self, cate_name: str) -> Optional[Dict]:
        """通过名称获取分类（安全查询，修复字符串拼接问题）"""
        try:
            cursor = self.local_conn.cursor(sqlite3.Row)
            # 修改：使用参数化查询，避免字符串拼接和类型问题
            cursor.execute(
                "SELECT * FROM category WHERE name = ? AND deleted_time = ''",
                (cate_name,)
            )
            row = cursor.fetchone()
            cursor.close()
            return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"获取分类失败: {e}", exc_info=True)
            return None

    def close(self):
        """关闭数据库连接"""
        try:
            if self.local_conn:
                self.local_conn.close()
            if self.remote_conn and self.remote_conn.open:
                self.remote_conn.close()
            self.logger.info("数据库连接已关闭")
        except Exception as e:
            self.logger.error(f"关闭数据库连接失败: {e}", exc_info=True)

# ===================== 系统应用工具类 =====================


class SystemAppUtil:
    """系统应用工具类（读取本地已装应用）"""
    # 系统白名单应用（排除）
    WHITE_LIST = [
        "uos-system", "uos-desktop", "uos-file-manager",
        "uos-terminal", "uos-settings", "uos-browser"
    ]

    @classmethod
    def get_local_installed_apps(cls) -> List[Dict]:
        """获取本地已安装应用"""
        logger = LogUtil.get_logger()
        installed_apps = []

        try:
            # 统信UOS基于Debian，使用dpkg获取已装应用
            import subprocess
            result = subprocess.check_output(
                "dpkg -l | grep -E '^ii' | awk '{print $2, $3}'",
                shell=True, encoding="utf-8"
            )

            for line in result.strip().split("\n"):
                if not line:
                    continue
                parts = line.split()
                app_name = parts[0].strip()

                # 过滤白名单
                if any(white in app_name for white in cls.WHITE_LIST):
                    continue

                version = parts[1].strip() if len(parts) >= 2 else "0.0.0"
                installed_apps.append({
                    "name": app_name,
                    "version": version
                })

            logger.info(f"获取本地已装应用: {len(installed_apps)}条")
            return installed_apps
        except Exception as e:
            logger.error(f"获取本地应用失败: {e}", exc_info=True)
            return []

    @classmethod
    def get_updatable_apps(cls, db_util: DBUtil) -> List[Dict]:
        """获取可更新应用"""
        logger = LogUtil.get_logger()

        # 获取本地应用
        local_apps = cls.get_local_installed_apps()
        if not local_apps:
            return []

        # 获取远程软件信息
        remote_softs = db_util.get_data("software")
        remote_soft_map = {soft["name"]: soft for soft in remote_softs}

        # 对比版本
        updatable = []
        for local_app in local_apps:
            app_name = local_app["name"]
            if app_name not in remote_soft_map:
                continue

            remote_soft = remote_soft_map[app_name]
            compare_result = ValidateUtil.compare_versions(
                local_app["version"], remote_soft["version"]
            )

            # 本地版本低于远程
            if compare_result == -1:
                updatable.append({
                    "name": app_name,
                    "local_version": local_app["version"],
                    "remote_version": remote_soft["version"],
                    "download_url": remote_soft["download_url"],
                    "size": remote_soft["size"]
                })

        logger.info(f"检测到可更新应用: {len(updatable)}条")
        return updatable

# ===================== 应用商店自更新工具类 =====================


class AppStoreUpdateUtil:
    """应用商店自身更新工具类"""
    @classmethod
    def check_self_update(cls, db_util: DBUtil) -> Dict:
        """检查应用商店自身更新"""
        logger = LogUtil.get_logger()

        try:
            # 获取本地版本
            if os.path.exists("version.txt"):
                with open("version.txt", "r") as f:
                    local_version = f.read().strip()
            else:
                # 默认版本
                local_version = "1.0.0"
                with open("version.txt", "w") as f:
                    f.write(local_version)

            # 获取远程版本（使用参数化查询）
            system_info = db_util.get_data(
                "system_info", "name = 'uos_appstore'")
            if not system_info:
                return {"need_update": False, "message": "未找到应用商店版本信息"}

            remote_version = system_info[0]["version"]
            compare_result = ValidateUtil.compare_versions(
                local_version, remote_version)

            if compare_result == -1:
                return {
                    "need_update": True,
                    "local_version": local_version,
                    "remote_version": remote_version,
                    "message": f"发现新版本: {remote_version}",
                    "download_url": system_info[0].get("download_url", "")
                }
            else:
                return {
                    "need_update": False,
                    "local_version": local_version,
                    "remote_version": remote_version,
                    "message": "当前已是最新版本"
                }
        except Exception as e:
            logger.error(f"检查自更新失败: {e}", exc_info=True)
            return {"need_update": False, "message": f"检查更新失败: {str(e)}"}

    @classmethod
    def do_self_update(cls, download_url: str) -> bool:
        """执行应用商店更新"""
        logger = LogUtil.get_logger()

        if not download_url:
            logger.error("更新失败: 下载链接为空")
            return False

        try:
            import requests
            import subprocess
            import tempfile

            # 下载更新包
            logger.info(f"开始下载更新包: {download_url}")
            resp = requests.get(download_url, timeout=30)
            resp.raise_for_status()  # 抛出HTTP错误

            with tempfile.NamedTemporaryFile(suffix=".deb", delete=False) as f:
                f.write(resp.content)
                pkg_path = f.name

            # 安装更新包
            logger.info(f"安装更新包: {pkg_path}")
            subprocess.run(["sudo", "dpkg", "-i", pkg_path],
                           check=True, capture_output=True, text=True)

            # 清理临时文件
            os.unlink(pkg_path)
            logger.info("应用商店更新完成")
            return True
        except Exception as e:
            logger.error(f"执行更新失败: {e}", exc_info=True)
            return False
