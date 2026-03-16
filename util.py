import os
import re
import json
import logging
import datetime
import pymysql
import subprocess
import requests
import tempfile
from typing import Optional, List, Dict, Any, Tuple
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from contextlib import contextmanager

# ===================== SQL配置加载类 =====================
class SQLConfig:
    """SQL配置加载工具类（单例模式）"""
    _sql_config: Optional[Dict] = None

    @classmethod
    def load_sql_config(cls, config_path: str = "./sql.json") -> Dict:
        """加载SQL配置文件（带缓存）"""
        if cls._sql_config is not None:
            return cls._sql_config

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"SQL配置文件不存在: {config_path}")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cls._sql_config = json.load(f)
            LogUtil.get_logger().info(f"SQL配置文件加载成功: {config_path}")
            return cls._sql_config
        except json.JSONDecodeError as e:
            LogUtil.get_logger().error(f"SQL配置文件格式错误: {e}", exc_info=True)
            raise
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
        
        try:
            for key in keys:
                value = value[key]
            return str(value).strip()
        except KeyError:
            raise KeyError(f"SQL配置中未找到键路径: {key_path}")
        except Exception as e:
            LogUtil.get_logger().error(f"解析SQL配置键路径失败: {key_path}, 错误: {e}")
            raise

# ===================== 基础配置 =====================
# 加载环境变量（优先系统环境变量，其次.env文件）
load_dotenv(override=False)

# 远程数据库配置
DB_CONFIG: Dict[str, Any] = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "database": os.getenv("DB_NAME", "uos_appstore"),
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "read_timeout": 30,
    "write_timeout": 30
}

# 日志配置
LOG_CONFIG: Dict[str, Any] = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "dir": os.getenv("LOG_DIR", "./logs"),
    "max_bytes": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
    "fmt": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S"
}

# ===================== 日志工具类 =====================
class LogUtil:
    """日志工具类（单例模式）"""
    _logger: Optional[logging.Logger] = None

    @classmethod
    def init_logger(cls) -> logging.Logger:
        """初始化日志器（文件+控制台双输出）"""
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
            LOG_CONFIG["fmt"],
            datefmt=LOG_CONFIG["datefmt"]
        )

        # 创建日志器（避免重复添加处理器）
        cls._logger = logging.getLogger("uos_appstore")
        cls._logger.setLevel(log_level)
        cls._logger.propagate = False
        cls._logger.handlers.clear()

        # 文件处理器（按大小轮转）
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

        cls._logger.info("日志器初始化完成")
        return cls._logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """获取日志器（懒加载）"""
        if cls._logger is None:
            cls.init_logger()
        return cls._logger

    # 快捷日志方法
    @classmethod
    def debug(cls, msg: str) -> None:
        cls.get_logger().debug(msg)

    @classmethod
    def info(cls, msg: str) -> None:
        cls.get_logger().info(msg)

    @classmethod
    def warning(cls, msg: str) -> None:
        cls.get_logger().warning(msg)

    @classmethod
    def error(cls, msg: str, exc_info: bool = False) -> None:
        cls.get_logger().error(msg, exc_info=exc_info)

    @classmethod
    def critical(cls, msg: str) -> None:
        cls.get_logger().critical(msg)

# ===================== 时间工具类 =====================
class TimeUtil:
    """时间工具类（提供标准化的时间处理方法）"""
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    @classmethod
    def get_current_time(cls, tz: Optional[datetime.timezone] = None) -> datetime.datetime:
        """获取当前时间（默认东八区）"""
        if tz is None:
            tz = datetime.timezone(datetime.timedelta(hours=8))
        return datetime.datetime.now(tz)

    @classmethod
    def format_datetime(cls, dt: Optional[datetime.datetime], fmt: str = DATETIME_FORMAT) -> str:
        """格式化时间为字符串（空值安全）"""
        if dt is None:
            return ""
        try:
            return dt.strftime(fmt)
        except Exception as e:
            LogUtil.error(f"时间格式化失败: {dt} -> {fmt}, 错误: {e}", exc_info=True)
            return ""

    @classmethod
    def parse_datetime(cls, dt_str: str, fmt: str = DATETIME_FORMAT) -> Optional[datetime.datetime]:
        """解析字符串为时间对象（容错处理）"""
        if not isinstance(dt_str, str) or not dt_str.strip():
            return None
        try:
            return datetime.datetime.strptime(dt_str.strip(), fmt)
        except ValueError as e:
            LogUtil.warning(f"时间解析失败: {dt_str} -> {fmt}, 错误: {e}")
            return None
        except Exception as e:
            LogUtil.error(f"时间解析异常: {dt_str} -> {fmt}, 错误: {e}", exc_info=True)
            return None

# ===================== 数据类型转换工具类 =====================
class DataTypeUtil:
    """数据类型转换工具类（安全转换，避免类型错误）"""

    @classmethod
    def safe_int(cls, value: Any, default: int = 0) -> int:
        """安全转换为整数（支持数字/字符串类型）"""
        if value is None:
            return default
        try:
            if isinstance(value, (int, float)):
                return int(value)
            if isinstance(value, str):
                # 清理非数字字符（保留负号）
                cleaned = re.sub(r"[^\d-]", "", value.strip())
                return int(cleaned) if cleaned else default
            return default
        except Exception as e:
            LogUtil.warning(f"整数转换失败: {value} -> {default}, 错误: {e}")
            return default

    @classmethod
    def safe_str(cls, value: Any, default: str = "") -> str:
        """安全转换为字符串（空值安全）"""
        if value is None:
            return default
        try:
            return str(value).strip()
        except Exception as e:
            LogUtil.warning(f"字符串转换失败: {value} -> {default}, 错误: {e}")
            return default

    @classmethod
    def safe_bool(cls, value: Any, default: bool = False) -> bool:
        """安全转换为布尔值（支持多格式）"""
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            return value.strip().lower() in ("true", "1", "yes", "y", "t", "on")
        return default

    @classmethod
    def safe_float(cls, value: Any, default: float = 0.0) -> float:
        """安全转换为浮点数（新增）"""
        if value is None:
            return default
        try:
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                cleaned = re.sub(r"[^\d.-]", "", value.strip())
                return float(cleaned) if cleaned else default
            return default
        except Exception as e:
            LogUtil.warning(f"浮点数转换失败: {value} -> {default}, 错误: {e}")
            return default

    @classmethod
    def convert_remote_data(cls, remote_data: Dict[str, Any], field_types: Dict[str, str]) -> Dict[str, Any]:
        """根据字段类型映射转换远程数据"""
        if not isinstance(remote_data, dict) or not isinstance(field_types, dict):
            return remote_data
        
        result = {}
        for field, value in remote_data.items():
            target_type = field_types.get(field, "str")
            if target_type == "int":
                result[field] = cls.safe_int(value)
            elif target_type == "float":
                result[field] = cls.safe_float(value)
            elif target_type == "str":
                result[field] = cls.safe_str(value)
            elif target_type == "bool":
                result[field] = cls.safe_bool(value)
            else:
                result[field] = value
        return result

# ===================== 数据校验工具类 =====================
class ValidateUtil:
    """数据校验工具类（提供通用的校验规则）"""
    # 版本号正则（支持主版本.次版本.修订版格式）
    VERSION_PATTERN = re.compile(r"^\d+(\.\d+){0,2}$")
    # URL正则（支持http/https/ftp）
    URL_PATTERN = re.compile(
        r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", re.IGNORECASE)
    # 应用名称正则（仅字母、数字、下划线、中划线）
    APP_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_\-]+$")

    @classmethod
    def validate_string(cls, value: Any, min_len: int = 1, max_len: Optional[int] = None) -> bool:
        """校验字符串（非空、长度范围）"""
        if value is None or not isinstance(value, str):
            LogUtil.warning(f"字符串校验失败: 值为{value}（类型{type(value)}），要求字符串类型")
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
        """校验版本号格式（x.y.z 格式）"""
        if not cls.validate_string(version):
            return False
        if not cls.VERSION_PATTERN.match(version):
            LogUtil.warning(f"版本号格式错误: {version}（要求x.y.z格式）")
            return False
        return True

    @classmethod
    def validate_url(cls, url: str) -> bool:
        """校验URL格式"""
        if not cls.validate_string(url):
            return False
        if not cls.URL_PATTERN.match(url):
            LogUtil.warning(f"URL格式错误: {url}")
            return False
        return True

    @classmethod
    def validate_app_name(cls, name: str) -> bool:
        """校验应用名称格式（新增）"""
        if not cls.validate_string(name, min_len=1, max_len=100):
            return False
        if not cls.APP_NAME_PATTERN.match(name):
            LogUtil.warning(f"应用名称格式错误: {name}（仅支持字母、数字、下划线、中划线）")
            return False
        return True

    @classmethod
    def compare_versions(cls, ver1: str, ver2: str) -> int:
        """
        版本号对比
        返回: -1(ver1<ver2), 0(相等), 1(ver1>ver2)
        """
        if not cls.validate_version(ver1) or not cls.validate_version(ver2):
            LogUtil.warning(f"版本号对比失败: 无效版本号 {ver1} vs {ver2}")
            return 0

        # 拆分版本号并补零对齐
        v1_parts = [int(part) for part in ver1.split(".")]
        v2_parts = [int(part) for part in ver2.split(".")]
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts += [0] * (max_len - len(v1_parts))
        v2_parts += [0] * (max_len - len(v2_parts))

        # 逐段比较
        for p1, p2 in zip(v1_parts, v2_parts):
            if p1 < p2:
                return -1
            elif p1 > p2:
                return 1
        return 0

# ===================== 系统应用管理工具类 =====================
class SystemAppManager:
    """系统应用管理工具类（UOS/Debian专属，提供安装/更新/版本检查）"""
    
    @classmethod
    def is_package_installed(cls, package_name: str) -> bool:
        """
        检查软件包是否已安装
        :param package_name: 软件包名称（如：wps-office）
        :return: 是否安装
        """
        logger = LogUtil.get_logger()
        if not ValidateUtil.validate_app_name(package_name):
            logger.warning(f"检查安装状态失败: 无效的应用名称 {package_name}")
            return False
        
        try:
            result = subprocess.run(
                ["dpkg", "-s", package_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            installed = result.returncode == 0
            logger.debug(f"检查应用[{package_name}]安装状态: {installed}")
            return installed
        except Exception as e:
            logger.error(f"检查应用[{package_name}]安装状态失败: {e}", exc_info=True)
            return False

    @classmethod
    def get_installed_version(cls, package_name: str) -> str:
        """
        获取已安装软件包的版本号
        :param package_name: 软件包名称
        :return: 版本号字符串（空字符串表示未安装/获取失败）
        """
        logger = LogUtil.get_logger()
        if not cls.is_package_installed(package_name):
            return ""
        
        try:
            result = subprocess.run(
                ["dpkg", "-s", package_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                return ""
            
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    version = line.split("Version:")[1].strip()
                    logger.debug(f"获取应用[{package_name}]已安装版本: {version}")
                    return version
            return ""
        except Exception as e:
            logger.error(f"获取应用[{package_name}]版本号失败: {e}", exc_info=True)
            return ""

    @classmethod
    def install_package(cls, package_name: str, install_source: str = None) -> bool:
        """
        安装/更新软件包
        :param package_name: 软件包名称
        :param install_source: 安装源（可以是包名/本地路径/远程URL）
        :return: 是否安装成功
        """
        logger = LogUtil.get_logger()
        if not ValidateUtil.validate_app_name(package_name):
            logger.error(f"安装失败: 无效的应用名称 {package_name}")
            return False
        
        # 优先使用指定的安装源，否则使用包名
        install_target = install_source if install_source else package_name
        
        try:
            # 构建安装命令（自动确认、忽略交互式提示）
            cmd = ["sudo", "apt", "install", "-y", "-qq", install_target]
            logger.info(f"执行安装命令: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                logger.info(f"应用[{package_name}]安装/更新成功")
                return True
            else:
                logger.error(f"应用[{package_name}]安装失败: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error(f"应用[{package_name}]安装超时（5分钟）")
            return False
        except Exception as e:
            logger.error(f"应用[{package_name}]安装异常: {e}", exc_info=True)
            return False

    @classmethod
    def download_and_install_deb(cls, package_name: str, download_url: str) -> bool:
        """
        下载远程deb包并安装
        :param package_name: 软件包名称
        :param download_url: deb包下载链接
        :return: 是否安装成功
        """
        logger = LogUtil.get_logger()
        
        # 校验URL
        if not ValidateUtil.validate_url(download_url):
            logger.error(f"下载安装失败: 无效的URL {download_url}")
            return False
        
        try:
            # 下载deb包到临时文件
            logger.info(f"开始下载deb包: {download_url}")
            resp = requests.get(
                download_url,
                timeout=30,
                stream=True,
                headers={"User-Agent": "UOS-AppStore/1.0"}
            )
            resp.raise_for_status()
            
            # 保存到临时文件
            with tempfile.NamedTemporaryFile(suffix=".deb", delete=False) as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
                deb_path = f.name
            
            # 安装deb包
            logger.info(f"安装本地deb包: {deb_path}")
            result = subprocess.run(
                ["sudo", "dpkg", "-i", deb_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 修复依赖问题
            if result.returncode != 0:
                logger.warning(f"dpkg安装失败，尝试修复依赖: {result.stderr}")
                subprocess.run(
                    ["sudo", "apt", "install", "-f", "-y"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # 清理临时文件
            os.unlink(deb_path)
            logger.info(f"应用[{package_name}]通过deb包安装完成")
            return True
            
        except requests.RequestException as e:
            logger.error(f"下载deb包失败: {e}", exc_info=True)
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"安装deb包失败: {e.stderr}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"下载并安装deb包异常: {e}", exc_info=True)
            return False

    @classmethod
    def get_app_install_status(cls, package_name: str, server_version: str) -> Dict[str, Any]:
        """
        获取应用安装状态（整合版）
        :param package_name: 软件包名称
        :param server_version: 服务器最新版本
        :return: 状态字典 {installed: bool, version: str, need_update: bool, status: str}
        """
        installed = cls.is_package_installed(package_name)
        local_version = cls.get_installed_version(package_name) if installed else ""
        need_update = False
        status = "未安装"
        
        if installed:
            cmp_result = ValidateUtil.compare_versions(local_version, server_version)
            if cmp_result < 0:
                need_update = True
                status = "可更新"
            elif cmp_result == 0:
                status = "已安装（最新）"
            else:
                status = "已安装（本地版本更高）"
        
        return {
            "installed": installed,
            "local_version": local_version,
            "server_version": server_version,
            "need_update": need_update,
            "status": status
        }

# ===================== 系统应用工具类 =====================
class SystemAppUtil:
    """系统应用工具类（读取本地已装应用，仅支持UOS/Debian系统）"""
    # 系统白名单应用（排除系统核心应用）
    WHITE_LIST = [
        "uos-system", "uos-desktop", "uos-file-manager",
        "uos-terminal", "uos-settings", "uos-browser",
        "linux-libc-dev", "systemd", "kernel", "libc6"
    ]

    @classmethod
    def get_local_installed_apps(cls) -> List[Dict[str, str]]:
        """获取本地已安装应用（解析dpkg输出）"""
        logger = LogUtil.get_logger()
        installed_apps = []

        try:
            # 执行dpkg命令获取已安装包信息（过滤仅保留名称和版本）
            result = subprocess.check_output(
                "dpkg -l | grep -E '^ii' | awk '{print $2, $3}'",
                shell=True,
                encoding="utf-8",
                stderr=subprocess.DEVNULL
            )

            for line in result.strip().split("\n"):
                if not line:
                    continue
                parts = line.split(maxsplit=1)  # 处理版本号含空格的情况
                if len(parts) < 2:
                    continue

                app_name = parts[0].strip()
                version = parts[1].strip()

                # 过滤白名单应用
                if any(white in app_name for white in cls.WHITE_LIST):
                    continue

                # 校验应用名称格式
                if ValidateUtil.validate_app_name(app_name):
                    installed_apps.append({
                        "name": app_name,
                        "version": version
                    })

            logger.info(f"获取本地已安装应用{len(installed_apps)}个（已过滤系统应用）")
            return installed_apps

        except subprocess.CalledProcessError as e:
            logger.error(f"执行dpkg命令失败: {e}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"获取本地应用失败: {e}", exc_info=True)
            return []

# ===================== 数据库工具类 =====================
class DBUtil:
    """数据库工具类（远程MariaDB交互，带连接池和上下文管理器）"""

    def __init__(self):
        self.logger = LogUtil.get_logger()
        self.remote_conn: Optional[pymysql.connections.Connection] = None
        self.sql_config = SQLConfig.load_sql_config()

    def __del__(self):
        """析构函数：确保连接关闭"""
        self.close_remote_conn()

    def _get_remote_conn(self) -> pymysql.connections.Connection:
        """获取远程MariaDB连接（自动重连+超时配置）"""
        # 检查现有连接是否有效
        if self.remote_conn and self.remote_conn.open:
            try:
                # 测试连接可用性
                self.remote_conn.ping(reconnect=False)
                return self.remote_conn
            except Exception:
                self.logger.warning("现有数据库连接已失效，重新建立连接")
                self.close_remote_conn()

        # 建立新连接
        try:
            self.remote_conn = pymysql.connect(**DB_CONFIG)
            self.logger.info(f"远程MariaDB数据库连接成功: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
            return self.remote_conn
        except pymysql.MySQLError as e:
            self.logger.error(f"远程数据库连接失败: {e}", exc_info=True)
            raise ConnectionError(f"数据库连接失败: {e}")
        except Exception as e:
            self.logger.error(f"数据库连接异常: {e}", exc_info=True)
            raise

    @contextmanager
    def get_cursor(self, dict_cursor: bool = True) -> pymysql.cursors.Cursor:
        """
        数据库游标上下文管理器（自动提交/回滚）
        :param dict_cursor: 是否返回字典格式游标
        """
        conn = None
        cursor = None
        try:
            conn = self._get_remote_conn()
            cursor_class = pymysql.cursors.DictCursor if dict_cursor else pymysql.cursors.Cursor
            cursor = conn.cursor(cursor_class)
            yield cursor
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"数据库操作失败: {e}", exc_info=True)
            raise
        finally:
            if cursor:
                cursor.close()

    def close_remote_conn(self) -> None:
        """关闭远程数据库连接（安全关闭）"""
        if self.remote_conn and self.remote_conn.open:
            try:
                self.remote_conn.close()
                self.logger.info("远程数据库连接已关闭")
            except Exception as e:
                self.logger.error(f"关闭数据库连接失败: {e}", exc_info=True)
        self.remote_conn = None

    def get_data(self, sql_key: str, params: Tuple = None) -> List[Dict[str, Any]]:
        """
        通用远程数据查询方法
        :param sql_key: SQL配置中的键路径
        :param params: SQL参数（元组格式）
        :return: 字典列表格式的查询结果
        """
        try:
            sql = SQLConfig.get_sql(sql_key)
            with self.get_cursor(dict_cursor=True) as cursor:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                result = cursor.fetchall()
                self.logger.info(f"执行SQL[{sql_key}]成功，返回{len(result)}条数据")
                return result
        except Exception as e:
            self.logger.error(f"查询远程数据失败[{sql_key}]: {e}", exc_info=True)
            return []

    # ========== 业务方法 ==========
    def get_category_list(self) -> List[Dict[str, Any]]:
        """获取所有分类列表"""
        return self.get_data("remote.select_category")

    def get_category_by_name(self, cate_name: str) -> Optional[Dict[str, Any]]:
        """通过名称获取分类"""
        result = self.get_data("remote.select_category_by_name", (cate_name,))
        return result[0] if result else None

    def get_software_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        """通过分类ID获取软件列表"""
        return self.get_data("remote.select_software_by_category", (category_id,))

    def get_software_list(self) -> List[Dict[str, Any]]:
        """获取所有软件列表"""
        return self.get_data("remote.select_software")

    def get_system_version(self, system_name: str = "UOS应用商店") -> Optional[Dict[str, Any]]:
        """获取系统版本信息"""
        result = self.get_data("remote.select_system_info", (system_name,))
        return result[0] if result else None

    def get_updatable_apps(self) -> List[Dict[str, Any]]:
        """获取可更新的应用列表（对比本地已装和远程最新版本）"""
        try:
            # 1. 获取本地已装应用
            local_apps = SystemAppUtil.get_local_installed_apps()
            if not local_apps:
                self.logger.warning("未检测到本地已安装应用")
                return []

            # 2. 获取远程所有软件并构建映射
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
                        "download_url": remote_soft.get("download_url", ""),
                        "size": remote_soft.get("size", ""),
                        "provider": remote_soft.get("provider", "")
                    })

            self.logger.info(f"检测到{len(updatable)}个可更新应用")
            return updatable
        except Exception as e:
            self.logger.error(f"获取可更新应用失败: {e}", exc_info=True)
            return []

# ===================== 应用商店自更新工具类 =====================
class AppStoreUpdateUtil:
    """应用商店自身更新工具类"""
    @classmethod
    def check_self_update(cls, db_util: DBUtil) -> Dict[str, Any]:
        """检查应用商店自身更新"""
        logger = LogUtil.get_logger()

        try:
            # 1. 获取本地版本
            local_version = "1.0.0"
            if os.path.exists("version.txt"):
                with open("version.txt", "r", encoding="utf-8") as f:
                    local_version = f.read().strip() or local_version

            # 2. 获取远程版本信息
            system_info = db_util.get_system_version()
            if not system_info:
                return {
                    "need_update": False,
                    "local_version": local_version,
                    "remote_version": "",
                    "message": "未找到应用商店远程版本信息"
                }

            # 3. 构建远程版本号
            remote_version = f"{system_info.get('major', 1)}.{system_info.get('minor', 0)}.{system_info.get('patch', 0)}"
            
            # 4. 版本对比
            compare_result = ValidateUtil.compare_versions(local_version, remote_version)

            if compare_result == -1:
                return {
                    "need_update": True,
                    "local_version": local_version,
                    "remote_version": remote_version,
                    "changelog": system_info.get("update_log", ""),
                    "is_force": DataTypeUtil.safe_bool(system_info.get("is_force", 0)),
                    "download_url": system_info.get("download_url", ""),
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
                "local_version": "",
                "remote_version": "",
                "message": f"检查更新失败: {str(e)}"
            }

    @classmethod
    def do_self_update(cls, download_url: str) -> bool:
        """执行应用商店自身更新（复用SystemAppManager的下载安装方法）"""
        return SystemAppManager.download_and_install_deb("uos-appstore", download_url)

# ===================== 测试函数 =====================
def test_system_app_manager():
    """测试系统应用管理工具类"""
    # 初始化日志
    LogUtil.init_logger()
    logger = LogUtil.get_logger()

    # 测试1：检查应用安装状态
    test_app = "wget"
    status = SystemAppManager.get_app_install_status(test_app, "1.21.3")
    logger.info(f"\n=== 应用[{test_app}]状态 ===")
    logger.info(f"安装状态: {status['installed']}")
    logger.info(f"本地版本: {status['local_version']}")
    logger.info(f"服务器版本: {status['server_version']}")
    logger.info(f"是否需要更新: {status['need_update']}")
    logger.info(f"状态描述: {status['status']}")

    # 测试2：数据库工具类
    db_util = DBUtil()
    try:
        categories = db_util.get_category_list()
        logger.info(f"\n=== 分类列表（{len(categories)}条）===")
        for cate in categories[:3]:  # 只打印前3条
            logger.info(f"ID: {cate['id']}, 名称: {cate['name']}")
    finally:
        db_util.close_remote_conn()

if __name__ == "__main__":
    # 运行测试
    test_system_app_manager()