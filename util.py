"""
统信UOS内网应用商店 - 工具类（简化版）
移除本地缓存，所有数据直接从远程MariaDB服务器获取
"""
import os
import re
import json
import logging
import datetime
import pymysql
from typing import Optional, List, Dict, Any
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# ===================== SQL配置加载类 =====================


class SQLConfig:
    """SQL配置加载工具类"""
    _sql_config = None

    @classmethod
    def load_sql_config(cls, config_path: str = "./sql.json") -> Dict:
        """加载SQL配置文件"""
        if cls._sql_config is not None:
            return cls._sql_config

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"SQL配置文件不存在: {config_path}")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cls._sql_config = json.load(f)
            LogUtil.get_logger().info("SQL配置文件加载成功")
            return cls._sql_config
        except Exception as e:
            LogUtil.get_logger().error(f"加载SQL配置失败: {e}", exc_info=True)
            raise

    @classmethod
    def get_sql(cls, key_path: str) -> str:
        """
        获取指定SQL语句
        :param key_path: 层级路径，如"remote.select_category"
        :return: SQL语句字符串
        """
        config = cls.load_sql_config()
        keys = key_path.split(".")
        value = config
        for key in keys:
            if key not in value:
                raise KeyError(f"SQL配置中未找到键: {key_path}")
            value = value[key]
        return value


# ===================== 基础配置 =====================
# 加载环境变量
load_dotenv()

# 远程数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "database": os.getenv("DB_NAME", "uos_appstore"),
    "charset": "utf8mb4"
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
    def parse_datetime(cls, dt_str: str, fmt: str = DATETIME_FORMAT) -> Optional[datetime.datetime]:
        """解析字符串为时间对象"""
        if not dt_str:
            return None
        try:
            return datetime.datetime.strptime(dt_str, fmt)
        except Exception as e:
            LogUtil.error(f"时间解析失败: {e}", exc_info=True)
            return None

# ===================== 数据类型转换工具类 =====================


class DataTypeUtil:
    """数据类型转换工具类"""

    @classmethod
    def safe_int(cls, value: Any, default: int = 0) -> int:
        """安全转换为整数"""
        if value is None:
            return default
        try:
            if isinstance(value, (int, float)):
                return int(value)
            if isinstance(value, str):
                cleaned = ''.join(filter(str.isdigit, str(value)))
                if cleaned:
                    return int(cleaned)
        except Exception as e:
            LogUtil.warning(f"整数转换失败: {value} -> {e}")
        return default

    @classmethod
    def safe_str(cls, value: Any, default: str = "") -> str:
        """安全转换为字符串"""
        if value is None:
            return default
        try:
            return str(value).strip()
        except Exception as e:
            LogUtil.warning(f"字符串转换失败: {value} -> {e}")
            return default

    @classmethod
    def safe_bool(cls, value: Any, default: bool = False) -> bool:
        """安全转换为布尔值"""
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "y", "t")
        return default

    @classmethod
    def convert_remote_data(cls, remote_data: dict, field_types: dict) -> dict:
        """根据字段类型转换远程数据"""
        result = {}
        for field, value in remote_data.items():
            if field in field_types:
                target_type = field_types[field]
                if target_type == "int":
                    result[field] = cls.safe_int(value)
                elif target_type == "str":
                    result[field] = cls.safe_str(value)
                elif target_type == "bool":
                    result[field] = cls.safe_bool(value)
                else:
                    result[field] = value
            else:
                result[field] = value
        return result

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
    """数据库工具类（仅远程MariaDB交互）"""

    def __init__(self):
        self.logger = LogUtil.get_logger()
        self.remote_conn = None
        # 加载SQL配置
        self.sql_config = SQLConfig.load_sql_config()

    def _get_remote_conn(self) -> pymysql.connections.Connection:
        """获取远程MariaDB连接（自动重连）"""
        if self.remote_conn and self.remote_conn.open:
            return self.remote_conn

        try:
            self.remote_conn = pymysql.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"],
                charset=DB_CONFIG["charset"],
                cursorclass=pymysql.cursors.DictCursor  # 默认返回字典格式
            )
            self.logger.info("远程MariaDB数据库连接成功")
            return self.remote_conn
        except Exception as e:
            self.logger.error(f"远程数据库连接失败: {e}", exc_info=True)
            raise

    def close_remote_conn(self):
        """关闭远程数据库连接"""
        if self.remote_conn and self.remote_conn.open:
            self.remote_conn.close()
            self.logger.info("远程数据库连接已关闭")

    def get_data(self, sql_key: str, params: tuple = None) -> List[Dict]:
        """
        通用远程数据查询方法
        :param sql_key: SQL配置中的键路径，如"remote.select_category"
        :param params: SQL参数，元组格式
        :return: 字典列表格式的查询结果
        """
        conn = None
        cursor = None
        try:
            # 获取数据库连接
            conn = self._get_remote_conn()
            cursor = conn.cursor()

            # 获取SQL语句并执行
            sql = SQLConfig.get_sql(sql_key)
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            # 获取查询结果（字典格式）
            result = cursor.fetchall()
            self.logger.info(f"执行SQL[{sql_key}]成功，返回{len(result)}条数据")
            return result

        except Exception as e:
            self.logger.error(f"查询远程数据失败[{sql_key}]: {e}", exc_info=True)
            return []
        finally:
            # 关闭游标
            if cursor:
                cursor.close()

    def get_category_list(self) -> List[Dict]:
        """获取所有分类列表"""
        return self.get_data("remote.select_category")

    def get_category_by_name(self, cate_name: str) -> Optional[Dict]:
        """通过名称获取分类"""
        result = self.get_data("remote.select_category_by_name", (cate_name,))
        return result[0] if result else None

    def get_software_by_category(self, category_id: int) -> List[Dict]:
        """通过分类ID获取软件列表"""
        return self.get_data("remote.select_software_by_category", (category_id,))

    def get_software_list(self) -> List[Dict]:
        """获取所有软件列表"""
        return self.get_data("remote.select_software")

    def get_system_version(self, system_name: str = "UOS应用商店") -> Optional[Dict]:
        """获取系统版本信息"""
        result = self.get_data("remote.select_system_info", (system_name,))
        return result[0] if result else None

    def get_updatable_apps(self) -> List[Dict]:
        """获取可更新的应用列表（对比本地已装和远程最新版本）"""
        # 1. 获取本地已装应用
        local_apps = SystemAppUtil.get_local_installed_apps()
        if not local_apps:
            self.logger.warning("未检测到本地已安装应用")
            return []

        # 2. 获取远程所有软件
        remote_softs = self.get_software_list()
        remote_soft_map = {soft["name"]: soft for soft in remote_softs}

        # 3. 对比版本号，筛选可更新应用
        updatable = []
        for local_app in local_apps:
            app_name = local_app["name"]
            if app_name not in remote_soft_map:
                continue

            remote_soft = remote_soft_map[app_name]
            compare_result = ValidateUtil.compare_versions(
                local_app["version"], remote_soft["version"]
            )

            # 本地版本低于远程，标记为可更新
            if compare_result == -1:
                updatable.append({
                    "name": app_name,
                    "local_version": local_app["version"],
                    "remote_version": remote_soft["version"],
                    "download_url": remote_soft["download_url"],
                    "size": remote_soft["size"],
                    "provider": remote_soft["provider"]
                })

        self.logger.info(f"检测到{len(updatable)}个可更新应用")
        return updatable

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
        """获取本地已安装应用（仅UOS/Debian系统）"""
        logger = LogUtil.get_logger()
        installed_apps = []

        try:
            # 执行dpkg命令获取已安装包信息
            import subprocess
            result = subprocess.check_output(
                "dpkg -l | grep -E '^ii' | awk '{print $2, $3}'",
                shell=True,
                encoding="utf-8"
            )

            for line in result.strip().split("\n"):
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 2:
                    continue

                app_name = parts[0].strip()
                version = parts[1].strip()

                # 过滤白名单应用
                if any(white in app_name for white in cls.WHITE_LIST):
                    continue

                installed_apps.append({
                    "name": app_name,
                    "version": version
                })

            logger.info(f"获取本地已安装应用{len(installed_apps)}个")
            return installed_apps

        except Exception as e:
            logger.error(f"获取本地应用失败: {e}", exc_info=True)
            return []

# ===================== 应用商店自更新工具类 =====================


class AppStoreUpdateUtil:
    """应用商店自身更新工具类"""
    @classmethod
    def check_self_update(cls, db_util: DBUtil) -> Dict:
        """检查应用商店自身更新"""
        logger = LogUtil.get_logger()

        try:
            # 获取本地版本
            local_version = "1.0.0"  # 实际场景中可从配置文件/版本文件读取
            if os.path.exists("version.txt"):
                with open("version.txt", "r") as f:
                    local_version = f.read().strip()

            # 获取远程版本信息
            system_info = db_util.get_system_version()
            if not system_info:
                return {
                    "need_update": False,
                    "message": "未找到应用商店远程版本信息"
                }

            remote_version = f"{system_info['major']}.{system_info['minor']}.{system_info['patch']}"
            compare_result = ValidateUtil.compare_versions(
                local_version, remote_version
            )

            if compare_result == -1:
                return {
                    "need_update": True,
                    "local_version": local_version,
                    "remote_version": remote_version,
                    "changelog": system_info.get("update_log", ""),
                    "is_force": bool(system_info.get("is_force", 0)),
                    "message": f"发现新版本: {remote_version}"
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
            return {
                "need_update": False,
                "message": f"检查更新失败: {str(e)}"
            }

    @classmethod
    def do_self_update(cls, download_url: str) -> bool:
        """执行应用商店自身更新"""
        logger = LogUtil.get_logger()

        if not download_url:
            logger.error("更新失败: 下载链接为空")
            return False

        try:
            import requests
            import subprocess
            import tempfile
            import os

            # 下载更新包
            logger.info(f"开始下载更新包: {download_url}")
            resp = requests.get(download_url, timeout=30)
            resp.raise_for_status()

            # 保存到临时文件
            with tempfile.NamedTemporaryFile(suffix=".deb", delete=False) as f:
                f.write(resp.content)
                pkg_path = f.name

            # 执行安装（需root权限）
            logger.info(f"安装更新包: {pkg_path}")
            subprocess.run(
                ["sudo", "dpkg", "-i", pkg_path],
                check=True,
                capture_output=True,
                text=True
            )

            # 清理临时文件
            os.unlink(pkg_path)
            logger.info("应用商店更新完成")
            return True

        except Exception as e:
            logger.error(f"执行更新失败: {e}", exc_info=True)
            return False

# ===================== 测试函数 =====================


def test_db_util():
    """测试数据库工具类"""
    # 初始化日志
    LogUtil.init_logger()

    # 创建数据库工具实例
    db_util = DBUtil()

    try:
        # 测试获取分类列表
        categories = db_util.get_category_list()
        print(f"\n=== 分类列表（{len(categories)}条）===")
        for cate in categories:
            print(
                f"ID: {cate['id']}, 名称: {cate['name']}, 描述: {cate['description']}")

        # 测试获取可更新应用
        updatable_apps = db_util.get_updatable_apps()
        print(f"\n=== 可更新应用（{len(updatable_apps)}条）===")
        for app in updatable_apps:
            print(
                f"名称: {app['name']}, 本地版本: {app['local_version']}, 最新版本: {app['remote_version']}")

        # 测试检查自更新
        update_info = AppStoreUpdateUtil.check_self_update(db_util)
        print(f"\n=== 应用商店更新检查 ===")
        print(f"是否需要更新: {update_info['need_update']}")
        print(f"提示信息: {update_info['message']}")

    finally:
        # 关闭数据库连接
        db_util.close_remote_conn()


if __name__ == "__main__":
    # 运行测试
    test_db_util()
