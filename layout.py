#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from typing import Dict, List, Any
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QMessageBox,
    QProgressBar, QDialog, QLabel, QScrollArea, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QColor, QPalette

# 导入工具类
try:
    from util import (
        LogUtil, DBUtil, SystemAppUtil, AppStoreUpdateUtil,
        SystemAppManager, ValidateUtil
    )
except ImportError as e:
    print(f"导入工具类失败: {e}")
    print("请确保util.py文件在当前目录下")
    sys.exit(1)

# ===================== 全局常量 =====================
CARD_LAYOUT_SWITCH_WIDTH = 1100
RIGHT_MIN_WIDTH = 700
FONT_TITLE = 16    # 左侧菜单 + 页面标题
FONT_BODY = 14     # 正文描述
FONT_SMALL = 12    # 统计信息小字
FONT_TINY = 10     # 辅助文字

# ===================== 下载进度对话框 =====================
class DownloadDialog(QDialog):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(400, 100)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e8e8e8;
                font-family: Noto Sans SC;
            }}
            QProgressBar {{
                border: none;
                border-radius: 10px;
                background-color: #f0f0f0;
                height: 20px;
                text-align: center;
                font-size: {FONT_TINY}px;
            }}
            QProgressBar::chunk {{
                background-color: #0078d7;
                border-radius: 10px;
            }}
            QLabel {{
                color: #333333;
                font-size: {FONT_SMALL}px;
                margin-top: 10px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("准备安装...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def update_progress(self, value: int, status: str) -> None:
        self.progress_bar.setValue(value)
        self.status_label.setText(status)
        if value >= 100:
            QTimer.singleShot(1000, self.close)

# ===================== 应用列表项（横条样式） =====================
class AppListItem(QWidget):
    download_clicked = pyqtSignal(str, str)  # (package_name, download_url)

    def __init__(self, app_info: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.app_info = app_info
        self.package_name = app_info.get("name", "")
        self.server_version = app_info.get("version", "")
        self.download_url = app_info.get("download_url", self.package_name)
        self.init_ui()
        self.update_button_state()

    def init_ui(self) -> None:
        self.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e8e8e8;
                margin: 5px 0;
                padding: 10px;
                font-family: Noto Sans SC;
            }}
            QWidget:hover {{
                border: 1px solid #d0d0d0;
                background-color: #fafafa;
            }}
            QLabel#name_label {{
                color: #333333;
                font-size: {FONT_TITLE}px;
                font-weight: bold;
                border: none;
            }}
            QLabel#version_label {{
                color: #666666;
                font-size: {FONT_TINY}px;
                border: none;
                margin-left: 10px;
            }}
            QLabel#desc_label {{
                color: #999999;
                font-size: {FONT_SMALL}px;
                border: none;
            }}
            QLabel#download_count_label {{
                color: #666666;
                font-size: {FONT_TINY}px;
                border: none;
                text-align: right;
            }}
            QPushButton {{
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 15px;
                font-size: {FONT_SMALL}px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: #005a9e;
            }}
            QPushButton:pressed {{
                background-color: #004a80;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #888888;
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)

        name_label = QLabel(self.package_name)
        name_label.setObjectName("name_label")
        top_layout.addWidget(name_label)

        version_label = QLabel(f"版本：{self.server_version}")
        version_label.setObjectName("version_label")
        top_layout.addWidget(version_label)

        top_layout.addStretch()

        self.download_btn = QPushButton()
        self.download_btn.clicked.connect(self.on_install_click)
        top_layout.addWidget(self.download_btn)

        main_layout.addLayout(top_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)

        desc = self.app_info.get("description", "暂无描述")
        if len(desc) > 100:
            desc = desc[:100] + "..."
        desc_label = QLabel(desc)
        desc_label.setObjectName("desc_label")
        desc_label.setWordWrap(False)
        desc_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        bottom_layout.addWidget(desc_label)

        download_count = self.app_info.get("download_count", 0)
        download_count_label = QLabel(f"下载量：{download_count} 次")
        download_count_label.setObjectName("download_count_label")
        download_count_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bottom_layout.addWidget(download_count_label)

        main_layout.addLayout(bottom_layout)

    def update_button_state(self):
        """根据安装状态更新按钮文字和状态"""
        status = SystemAppManager.get_app_install_status(self.package_name, self.server_version)
        if not status["installed"]:
            self.download_btn.setText("安装")
            self.download_btn.setEnabled(True)
        else:
            if status["need_update"]:
                self.download_btn.setText("更新")
                self.download_btn.setEnabled(True)
            else:
                self.download_btn.setText("已安装")
                self.download_btn.setEnabled(False)

    def on_install_click(self) -> None:
        self.download_clicked.emit(self.package_name, self.download_url)

# ===================== 左侧菜单 =====================
class LeftMenuList(QWidget):
    menu_clicked = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.logger = LogUtil.get_logger()
        self.db_util = DBUtil()
        self.init_ui()
        self.load_menu()

    def init_ui(self) -> None:
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #f8f8f8;
                border-radius: 12px;
                border: none;
                font-family: Noto Sans SC;
            }}
            QPushButton {{
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: {FONT_SMALL}px;
                margin: 0 10px 10px 10px;
            }}
            QPushButton:hover {{
                background-color: #005a9e;
            }}
            QPushButton:pressed {{
                background-color: #004a80;
            }}
            QLabel#title_label {{
                color: #333333;
                font-weight: bold;
                font-size: {FONT_TITLE}px;
                padding: 15px 0;
                text-align: center;
                margin: 0;
                border: none;
            }}
            QListWidget {{
                border: none;
                background-color: transparent;
                padding: 5px 0;
            }}
            QListWidget::item {{
                padding: 10px 15px;
                margin: 2px 10px;
                border-radius: 8px;
                color: #333333;
                font-size: {FONT_TITLE}px;
                font-weight: bold;
                border: none;
            }}
            QListWidget::item:selected {{
                background-color: #0078d7;
                color: white;
                border: none;
            }}
            QListWidget::item:hover:!selected {{
                background-color: #e8f4ff;
                color: #0078d7;
                border: none;
            }}
            QListWidget::item:disabled {{
                color: #999999;
                background-color: transparent;
                border: none;
            }}
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        title_label = QLabel("应用商店")
        title_label.setObjectName("title_label")
        self.layout.addWidget(title_label)

        self.menu_list = QListWidget()
        self.menu_list.setFocusPolicy(Qt.NoFocus)
        self.menu_list.itemClicked.connect(self.on_menu_click)
        self.layout.addWidget(self.menu_list)

        refresh_btn = QPushButton("刷新菜单")
        refresh_btn.clicked.connect(self.load_menu)
        self.layout.addWidget(refresh_btn)

    def load_menu(self) -> None:
        try:
            self.menu_list.clear()

            home_item = QListWidgetItem("首页")
            home_item.setData(Qt.UserRole, 0)
            home_item.setFont(QFont("Noto Sans SC", FONT_TITLE, QFont.Bold))
            self.menu_list.addItem(home_item)

            categories = self.db_util.get_category_list()
            if not categories:
                empty_item = QListWidgetItem("暂无分类数据")
                empty_item.setFlags(Qt.ItemIsEnabled)
                empty_item.setForeground(QColor("#999999"))
                empty_item.setFont(QFont("Noto Sans SC", FONT_TITLE, QFont.Bold))
                self.menu_list.addItem(empty_item)
            else:
                for cate in categories:
                    cate_item = QListWidgetItem(cate["name"])
                    cate_item.setData(Qt.UserRole, cate["id"])
                    cate_item.setFont(QFont("Noto Sans SC", FONT_TITLE, QFont.Bold))
                    self.menu_list.addItem(cate_item)

            update_item = QListWidgetItem("应用更新")
            update_item.setData(Qt.UserRole, 99)
            update_item.setFont(QFont("Noto Sans SC", FONT_TITLE, QFont.Bold))
            self.menu_list.addItem(update_item)

            manage_item = QListWidgetItem("应用管理")
            manage_item.setData(Qt.UserRole, 100)
            manage_item.setFont(QFont("Noto Sans SC", FONT_TITLE, QFont.Bold))
            self.menu_list.addItem(manage_item)

            self.logger.info(f"加载菜单完成：首页 + {len(categories)}个分类 + 应用更新 + 应用管理")
            self.menu_list.setCurrentItem(home_item)
            self.on_menu_click(home_item)

        except Exception as e:
            self.logger.error(f"加载菜单失败: {e}", exc_info=True)
            QMessageBox.warning(self, "错误", f"加载菜单失败: {str(e)}")

    def on_menu_click(self, item) -> None:
        menu_index = item.data(Qt.UserRole)
        if menu_index is None:
            return
        menu_name = item.text()
        self.logger.info(f"选中菜单: {menu_name} (index={menu_index})")
        self.menu_clicked.emit(menu_index)

# ===================== 右侧内容区 =====================
class RightContentArea(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = LogUtil.get_logger()
        self.db_util = DBUtil()
        self.current_menu_index = 0
        self.app_items: List[AppListItem] = []
        self.init_ui()

    def init_ui(self) -> None:
        self.setMinimumWidth(RIGHT_MIN_WIDTH)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #fafafa;
                border: none;
                font-family: Noto Sans SC;
            }}
            QLabel#title_label {{
                color: #333333;
                font-size: {FONT_TITLE}px;
                font-weight: bold;
                padding: 0 0 15px 0;
                border: none;
                margin: 0;
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QWidget#scroll_content {{
                background-color: transparent;
                padding: 10px;
            }}
            QLabel#home_desc {{
                color: #666666;
                font-size: {FONT_BODY}px;
                padding: 15px;
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e8e8e8;
            }}
            QFrame#stats_widget {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e8e8e8;
                padding: 8px 15px;
                margin: 10px 0;
            }}
            QLabel#stats_label {{
                font-size: {FONT_SMALL}px;
                color: #666666;
                border: none;
                padding: 0 20px 0 0;
                margin: 0;
            }}
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 30, 20)  # 修复滚动条遮挡
        self.layout.setSpacing(15)

        self.title_label = QLabel("统信UOS内网应用商店 - 首页")
        self.title_label.setObjectName("title_label")
        self.layout.addWidget(self.title_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scroll_content")
        self.list_layout = QVBoxLayout(self.scroll_content)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(0)
        self.scroll_area.setWidget(self.scroll_content)

        self.init_home_content()
        self.show_home_content()

    def clear_items(self) -> None:
        for item in self.app_items:
            try:
                item.setParent(None)
                item.deleteLater()
            except:
                pass
        self.app_items.clear()

    def init_home_content(self) -> None:
        self.home_widget = QWidget()
        home_layout = QVBoxLayout(self.home_widget)
        home_layout.setContentsMargins(0, 0, 0, 0)
        home_layout.setSpacing(15)

        home_desc = QLabel("""
统信UOS内网应用商店
====================
欢迎使用统信UOS内网应用商店！

本应用商店专为企业内网环境打造，提供安全、稳定的应用分发与管理服务：
• 丰富的应用分类：涵盖办公、开发、设计、工具等各类应用
• 一键安装更新：自动检测本地应用版本，便捷更新
• 本地应用管理：查看已安装应用，统一管理

使用说明：
• 左侧菜单选择「应用分类」浏览可用应用
• 「应用更新」查看可升级的本地应用
• 「应用管理」查看已安装的本地应用
        """)
        home_desc.setObjectName("home_desc")
        home_desc.setWordWrap(True)
        home_layout.addWidget(home_desc)

        stats_widget = QFrame()
        stats_widget.setObjectName("stats_widget")
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(30)

        cate_count = len(self.db_util.get_category_list())
        cate_label = QLabel(f"应用分类：{cate_count} 个")
        cate_label.setObjectName("stats_label")
        stats_layout.addWidget(cate_label)

        local_app_count = len(SystemAppUtil.get_local_installed_apps())
        local_label = QLabel(f"本地应用：{local_app_count} 个")
        local_label.setObjectName("stats_label")
        stats_layout.addWidget(local_label)

        home_layout.addWidget(stats_widget)

    def show_home_content(self) -> None:
        self.clear_items()
        self.title_label.setText("统信UOS内网应用商店 - 首页")
        self.scroll_area.takeWidget()
        self.scroll_area.setWidget(self.home_widget)

    def show_category_content(self, cate_id: int) -> None:
        self.scroll_area.takeWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.clear_items()

        cate_name = self.get_cate_name_by_id(cate_id)
        self.title_label.setText(f"应用分类 - {cate_name}")

        try:
            softs = self.db_util.get_software_by_category(cate_id)
            if not softs:
                QMessageBox.information(self, "提示", "该分类下暂无应用")
                return

            for soft in softs:
                if not soft.get("description"):
                    soft["description"] = f"{soft.get('name')} - 官方正版应用，安全可靠"
                if "download_count" not in soft:
                    soft["download_count"] = 0
                if "download_url" not in soft:
                    soft["download_url"] = soft["name"]  # 默认用包名作为安装名

                item = AppListItem(soft)
                item.download_clicked.connect(self.download_app)
                self.app_items.append(item)
                self.list_layout.addWidget(item)

            self.list_layout.addStretch()

        except Exception as e:
            self.logger.error(f"加载分类应用失败: {e}", exc_info=True)
            QMessageBox.warning(self, "错误", f"加载应用失败: {str(e)}")

    def show_update_content(self) -> None:
        """显示应用更新页面（横条列表样式）"""
        self.scroll_area.takeWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.clear_items()

        self.title_label.setText("应用更新 - 可更新应用列表")

        try:
            updatable_apps = self.db_util.get_updatable_apps()
            if not updatable_apps:
                empty_label = QLabel("暂无需要更新的应用")
                empty_label.setStyleSheet(f"""
                    color: #666666;
                    font-size: {FONT_BODY}px;
                    padding: 20px;
                    text-align: center;
                """)
                self.list_layout.addWidget(empty_label)
                return

            # 构建可更新应用的完整信息
            remote_soft_map = {soft["name"]: soft for soft in self.db_util.get_software_list()}
            for app in updatable_apps:
                app_name = app["name"]
                remote_soft = remote_soft_map.get(app_name, {})
                
                # 补全应用信息
                app_info = {
                    "name": app_name,
                    "version": app["remote_version"],
                    "description": remote_soft.get("description", f"{app_name} 有新版本可用"),
                    "download_count": remote_soft.get("download_count", 0),
                    "download_url": app["download_url"]
                }

                item = AppListItem(app_info)
                item.download_clicked.connect(self.download_app)
                self.app_items.append(item)
                self.list_layout.addWidget(item)

            self.list_layout.addStretch()

        except Exception as e:
            self.logger.error(f"加载更新应用失败: {e}", exc_info=True)
            QMessageBox.warning(self, "错误", f"加载更新应用失败: {str(e)}")

    def show_manage_content(self) -> None:
        """显示应用管理页面"""
        self.scroll_area.takeWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.clear_items()

        self.title_label.setText("应用管理 - 本地已安装应用")

        try:
            local_apps = SystemAppUtil.get_local_installed_apps()
            if not local_apps:
                empty_label = QLabel("未检测到本地已安装应用")
                empty_label.setStyleSheet(f"""
                    color: #666666;
                    font-size: {FONT_BODY}px;
                    padding: 20px;
                    text-align: center;
                """)
                self.list_layout.addWidget(empty_label)
                return

            # 构建本地应用展示信息
            remote_soft_map = {soft["name"]: soft for soft in self.db_util.get_software_list()}
            for app in local_apps[:50]:  # 限制显示前50个应用
                app_name = app["name"]
                remote_soft = remote_soft_map.get(app_name, {})

                app_info = {
                    "name": app_name,
                    "version": app["version"],
                    "description": remote_soft.get("description", "本地已安装应用"),
                    "download_count": remote_soft.get("download_count", 0),
                    "download_url": remote_soft.get("download_url", app_name)
                }

                item = AppListItem(app_info)
                self.app_items.append(item)
                self.list_layout.addWidget(item)

            self.list_layout.addStretch()

        except Exception as e:
            self.logger.error(f"加载本地应用失败: {e}", exc_info=True)
            QMessageBox.warning(self, "错误", f"加载本地应用失败: {str(e)}")

    def get_cate_name_by_id(self, cate_id: int) -> str:
        categories = self.db_util.get_category_list()
        for cate in categories:
            if cate["id"] == cate_id:
                return cate["name"]
        return "未知分类"

    def download_app(self, package_name: str, download_url: str) -> None:
        try:
            self.download_dialog = DownloadDialog(f"安装 {package_name}", self)
            self.download_dialog.show()
            
            def simulate_install_progress(step: int = 0):
                if step > 100 or not self.download_dialog.isVisible():
                    if step >= 100:
                        # 执行实际安装
                        success = SystemAppManager.install_package(package_name, download_url)
                        if success:
                            QMessageBox.information(self, "成功", f"{package_name} 安装/更新完成！")
                            # 刷新当前页面的按钮状态
                            for item in self.app_items:
                                item.update_button_state()
                        else:
                            QMessageBox.critical(self, "失败", f"{package_name} 安装/更新失败！")
                    return
                self.download_dialog.update_progress(
                    step, f"正在安装 {package_name}...({step}%)")
                QTimer.singleShot(50, lambda: simulate_install_progress(step + 1))
                
            simulate_install_progress(0)
        except Exception as e:
            self.logger.error(f"安装应用失败: {e}", exc_info=True)
            QMessageBox.critical(self, "错误", f"安装 {package_name} 失败: {str(e)}")

# ===================== 主窗口类 =====================
class AppStoreMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = LogUtil.get_logger()
        self.db_util = DBUtil()
        self.init_main_ui()
        self.check_self_update()

    def init_main_ui(self) -> None:
        self.setWindowTitle("统信UOS内网应用商店")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#fafafa"))
        self.setPalette(palette)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.left_menu = LeftMenuList()
        main_layout.addWidget(self.left_menu, 1)

        self.right_content = RightContentArea()
        main_layout.addWidget(self.right_content, 4)

        self.left_menu.menu_clicked.connect(self.on_menu_change)

    def on_menu_change(self, idx: int) -> None:
        """菜单切换处理"""
        self.right_content.current_menu_index = idx
        if idx == 0:
            self.right_content.show_home_content()
        elif idx == 99:
            self.right_content.show_update_content()
        elif idx == 100:
            self.right_content.show_manage_content()
        else:
            self.right_content.show_category_content(idx)

    def check_self_update(self) -> None:
        """检查应用商店自身更新"""
        try:
            update_info = AppStoreUpdateUtil.check_self_update(self.db_util)
            if update_info["need_update"]:
                reply = QMessageBox.question(
                    self,
                    "发现新版本",
                    f"{update_info['message']}\n本地版本：{update_info['local_version']}\n最新版本：{update_info['remote_version']}\n是否更新？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    if update_info["download_url"]:
                        success = AppStoreUpdateUtil.do_self_update(update_info["download_url"])
                        if success:
                            QMessageBox.information(self, "成功", "应用商店更新完成，请重启应用！")
                        else:
                            QMessageBox.critical(self, "失败", "应用商店更新失败！")
                    else:
                        QMessageBox.warning(self, "提示", "未获取到更新包下载链接！")
        except Exception as e:
            self.logger.error(f"检查自更新失败: {e}", exc_info=True)

# ===================== 主函数 =====================
def main():
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    os.environ["QT_FONT_DPI"] = "96"

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("UOS AppStore")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Local")

    LogUtil.init_logger()

    try:
        window = AppStoreMainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        LogUtil.error(f"应用启动失败: {e}", exc_info=True)
        QMessageBox.critical(None, "启动失败", f"应用商店启动失败：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()