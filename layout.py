"""
统信UOS内网应用商店 - 修复CSS属性兼容版
解决Unknown property word-wrap/box-shadow报错
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QMessageBox,
    QProgressBar, QDialog, QLabel, QScrollArea, QGridLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QFont, QColor

# 导入工具类
from util import (
    LogUtil, DBUtil, SystemAppUtil, AppStoreUpdateUtil,
    ValidateUtil
)

# ===================== 全局常量 =====================
# 卡片布局切换阈值
CARD_LAYOUT_SWITCH_WIDTH = 1100  # 宽度>1100时4列，否则3列
# 右侧最小宽度
RIGHT_MIN_WIDTH = 700
# 卡片尺寸
CARD_WIDTH_3COL = 220  # 3列时卡片宽度
CARD_WIDTH_4COL = 180  # 4列时卡片宽度
CARD_HEIGHT = 200      # 卡片固定高度

# ===================== 下载进度对话框 =====================


class DownloadDialog(QDialog):
    """下载进度对话框（兼容Qt样式）"""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(400, 100)
        # 移除box-shadow，改用border和background实现
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e8e8e8;
            }
            QProgressBar {
                border: none;
                border-radius: 10px;
                background-color: #f0f0f0;
                height: 20px;
                text-align: center;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background-color: #0078d7;
                border-radius: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                margin-top: 10px;
            }
        """)

        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # 状态标签
        self.status_label = QLabel("准备下载...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def update_progress(self, value: int, status: str):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(status)
        if value >= 100:
            QTimer.singleShot(1000, self.close)

# ===================== 自定义应用卡片（兼容Qt样式） =====================


class AppCard(QWidget):
    """应用卡片组件（修复CSS属性兼容）"""
    download_clicked = pyqtSignal(str, str)  # 下载点击信号（url, name）

    def __init__(self, app_info: dict, parent=None):
        super().__init__(parent)
        self.app_info = app_info
        self.init_ui()

    def init_ui(self):
        """初始化卡片UI（兼容Qt样式）"""
        self.setFixedSize(QSize(CARD_WIDTH_3COL, CARD_HEIGHT))
        # 替换box-shadow为border+渐变背景模拟阴影效果
        # 移除word-wrap，改用Qt的wordWrap属性
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e8e8e8;
            }
            QWidget:hover {
                border: 1px solid #d0d0d0;
                background-color: #fafafa;
            }
            QLabel#name_label {
                color: #333333;
                font-size: 20px;
                font-weight: bold;
                padding: 15px 15px 5px 15px;
                border: none;
            }
            QLabel#version_label {
                color: #666666;
                font-size: 12px;
                padding: 0 15px 8px 15px;
                border: none;
            }
            QLabel#desc_label {
                color: #999999;
                font-size: 12px;
                padding: 0 15px 15px 15px;
                border: none;
                line-height: 1.4;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 0;
                font-size: 16px;
                margin: 0 15px 15px 15px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004a80;
            }
        """)

        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 应用名称
        name_label = QLabel(self.app_info.get("name", "未知应用"))
        name_label.setObjectName("name_label")
        layout.addWidget(name_label)

        # 版本号
        version_label = QLabel(f"版本：{self.app_info.get('version', '未知版本')}")
        version_label.setObjectName("version_label")
        layout.addWidget(version_label)

        # 描述（截取前50个字符，使用Qt的wordWrap属性）
        desc = self.app_info.get("description", "暂无描述")
        if len(desc) > 50:
            desc = desc[:50] + "..."
        desc_label = QLabel(desc)
        desc_label.setObjectName("desc_label")
        desc_label.setWordWrap(True)  # Qt原生换行属性，替代word-wrap
        layout.addWidget(desc_label)

        # 弹性空间（按钮靠下）
        layout.addStretch()

        # 下载/更新按钮
        btn_text = "更新" if "local_version" in self.app_info else "下载"
        self.download_btn = QPushButton(btn_text)
        self.download_btn.clicked.connect(self.on_download_click)
        layout.addWidget(self.download_btn)

    def resize_card(self, is_4col: bool):
        """调整卡片尺寸（3列/4列）"""
        width = CARD_WIDTH_4COL if is_4col else CARD_WIDTH_3COL
        self.setFixedWidth(width)

    def on_download_click(self):
        """下载/更新按钮点击"""
        url = self.app_info.get("download_url", "")
        name = self.app_info.get("name", "未知应用")
        self.download_clicked.emit(url, name)

# ===================== 左侧菜单列表（无黑边框+兼容样式） =====================


class LeftMenuList(QWidget):
    """左侧菜单列表组件（纯扁平化，无黑边框）"""
    menu_clicked = pyqtSignal(int)  # 菜单点击信号（传递index值）

    def __init__(self):
        super().__init__()
        self.logger = LogUtil.get_logger()
        self.db_util = DBUtil()
        self.init_ui()
        self.load_menu()

    def init_ui(self):
        """初始化UI（无黑边框+兼容Qt样式）"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f8f8;
                border-radius: 12px;
                border: none;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                margin: 0 10px 10px 10px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004a80;
            }
            QLabel#title_label {
                color: #333333;
                font-weight: bold;
                font-size: 18px;
                padding: 15px 0;
                text-align: center;
                margin: 0;
                border: none;
            }
            QListWidget {
                border: none;
                background-color: transparent;
                padding: 5px 0;
            }
            QListWidget::item {
                padding: 12px 15px;
                margin: 2px 10px;
                border-radius: 8px;
                color: #333333;
                font-size: 20px;
                border: none;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
                border: none;
            }
            QListWidget::item:hover:!selected {
                background-color: #e8f4ff;
                color: #0078d7;
                border: none;
            }
            QListWidget::item:disabled {
                color: #999999;
                background-color: transparent;
                border: none;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 标题
        title_label = QLabel("应用商店")
        title_label.setObjectName("title_label")
        self.layout.addWidget(title_label)

        # 菜单列表（无黑边框）
        self.menu_list = QListWidget()
        self.menu_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # 移除焦点框
        self.menu_list.itemClicked.connect(self.on_menu_click)
        self.layout.addWidget(self.menu_list)

        # 刷新按钮
        refresh_btn = QPushButton("刷新菜单")
        refresh_btn.clicked.connect(self.load_menu)
        self.layout.addWidget(refresh_btn)

    def load_menu(self):
        """加载菜单列表：首页(0) → 分类(分类ID) → 应用更新(99) → 应用管理(100)"""
        try:
            self.menu_list.clear()

            # 1. 首页（index=0）
            home_item = QListWidgetItem("首页")
            home_item.setData(Qt.ItemDataRole.UserRole, 0)
            home_item.setFont(QFont("Noto Sans SC", 20))
            self.menu_list.addItem(home_item)

            # 2. 数据库分类列表（index=分类ID）
            categories = self.db_util.get_category_list()
            if not categories:
                empty_item = QListWidgetItem("暂无分类数据")
                empty_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                empty_item.setForeground(QColor("#999999"))
                empty_item.setFont(QFont("Noto Sans SC", 15))
                self.menu_list.addItem(empty_item)
            else:
                for cate in categories:
                    cate_item = QListWidgetItem(cate["name"])
                    cate_item.setData(Qt.ItemDataRole.UserRole, cate["id"])
                    cate_item.setFont(QFont("Noto Sans SC", 15))
                    self.menu_list.addItem(cate_item)

            # 3. 应用更新（index=99）
            update_item = QListWidgetItem("应用更新")
            update_item.setData(Qt.ItemDataRole.UserRole, 99)
            update_item.setFont(QFont("Noto Sans SC", 15))
            self.menu_list.addItem(update_item)

            # 4. 应用管理（index=100）
            manage_item = QListWidgetItem("应用管理")
            manage_item.setData(Qt.ItemDataRole.UserRole, 100)
            manage_item.setFont(QFont("Noto Sans SC", 15))
            self.menu_list.addItem(manage_item)

            self.logger.info(f"加载菜单完成：首页 + {len(categories)}个分类 + 应用更新 + 应用管理")

            # 默认选中首页
            self.menu_list.setCurrentItem(home_item)
            self.on_menu_click(home_item)

        except Exception as e:
            self.logger.error(f"加载菜单失败: {e}", exc_info=True)
            QMessageBox.warning(self, "错误", f"加载菜单失败: {str(e)}")

    def on_menu_click(self, item):
        """菜单点击事件"""
        menu_index = item.data(Qt.ItemDataRole.UserRole)
        if menu_index is None:
            return

        menu_name = item.text()
        self.logger.info(f"选中菜单: {menu_name} (index={menu_index})")
        self.menu_clicked.emit(menu_index)

# ===================== 右侧内容展示区域（卡片式布局+兼容样式） =====================


class RightContentArea(QWidget):
    """右侧内容展示区域（自适应卡片式布局）"""

    def __init__(self):
        super().__init__()
        self.logger = LogUtil.get_logger()
        self.db_util = DBUtil()
        self.current_menu_index = 0
        self.app_cards = []  # 存储应用卡片实例
        self.init_ui()

    def init_ui(self):
        """初始化UI（卡片式布局+兼容Qt样式）"""
        self.setMinimumWidth(RIGHT_MIN_WIDTH)
        # 移除所有不兼容的CSS属性，改用Qt支持的写法
        self.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
                border: none;
            }
            QLabel#title_label {
                color: #333333;
                font-size: 20px;
                font-weight: bold;
                padding: 0 0 20px 0;
                border: none;
                margin: 0;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QWidget#scroll_content {
                background-color: transparent;
                padding: 10px;
            }
            QLabel#home_desc {
                color: #666666;
                font-size: 14px;
                line-height: 1.8;
                padding: 20px;
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e8e8e8;
            }
            QTableWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e8e8e8;
                gridline-color: #f0f0f0;
            }
            QHeaderView::section {
                background-color: #f8f8f8;
                border: none;
                padding: 12px;
                font-size: 14px;
                color: #333333;
            }
            QTableWidget::item {
                padding: 10px;
                font-size: 14px;
                color: #333333;
                border: none;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # 顶部标题
        self.title_label = QLabel("统信UOS内网应用商店 - 首页")
        self.title_label.setObjectName("title_label")
        self.layout.addWidget(self.title_label)

        # 滚动区域（容纳卡片布局）
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout.addWidget(self.scroll_area)

        # 滚动内容容器
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scroll_content")
        self.card_layout = QGridLayout(self.scroll_content)
        self.card_layout.setSpacing(20)
        self.scroll_area.setWidget(self.scroll_content)

        # 初始化各内容
        self.init_home_content()
        self.show_home_content()

        # 监听窗口大小变化，自适应卡片布局
        self.resize_event_timer = QTimer()
        self.resize_event_timer.setSingleShot(True)
        self.resize_event_timer.timeout.connect(self.adjust_card_layout)
        self.resizeEvent = self.on_resize  # 重写resize事件

    def on_resize(self, event):
        """窗口大小变化事件"""
        self.resize_event_timer.start(100)  # 防抖
        super().resizeEvent(event)

    def adjust_card_layout(self):
        """自适应调整卡片布局（3列/4列）"""
        if not self.app_cards:
            return

        # 判断是否切换为4列
        is_4col = self.width() > CARD_LAYOUT_SWITCH_WIDTH
        col_count = 4 if is_4col else 3

        # 重新排列卡片
        for idx, card in enumerate(self.app_cards):
            card.resize_card(is_4col)
            row = idx // col_count
            col = idx % col_count
            self.card_layout.addWidget(card, row, col)

    def clear_cards(self):
        """清空所有卡片"""
        for card in self.app_cards:
            card.setParent(None)
        self.app_cards.clear()

    # -------------------- 首页内容 --------------------
    def init_home_content(self):
        """初始化首页内容"""
        self.home_widget = QWidget()
        home_layout = QVBoxLayout(self.home_widget)
        home_layout.setContentsMargins(0, 0, 0, 0)
        home_layout.setSpacing(20)

        # 首页介绍
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
        home_desc.setWordWrap(True)  # Qt原生换行
        home_layout.addWidget(home_desc)

        # 统计信息
        stats_widget = QWidget()
        stats_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e8e8e8;
                padding: 15px;
            }
            QLabel {
                font-size: 14px;
                color: #666666;
                border: none;
                padding: 0 15px 0 0;
            }
        """)
        stats_layout = QHBoxLayout(stats_widget)

        cate_count = len(self.db_util.get_category_list())
        cate_label = QLabel(f"应用分类：{cate_count} 个")
        stats_layout.addWidget(cate_label)

        local_app_count = len(SystemAppUtil.get_local_installed_apps())
        local_label = QLabel(f"本地应用：{local_app_count} 个")
        stats_layout.addWidget(local_label)

        home_layout.addWidget(stats_widget)

    def show_home_content(self):
        """显示首页内容"""
        self.clear_cards()
        self.title_label.setText("统信UOS内网应用商店 - 首页")
        # 替换滚动区域内容为首页
        self.scroll_area.takeWidget()
        self.scroll_area.setWidget(self.home_widget)

    # -------------------- 分类应用卡片展示 --------------------
    def show_category_content(self, cate_id: int):
        """显示分类应用卡片"""
        self.scroll_area.takeWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.clear_cards()

        # 获取分类名称
        cate_name = self.get_cate_name_by_id(cate_id)
        self.title_label.setText(f"应用分类 - {cate_name}")

        # 加载应用数据
        try:
            softs = self.db_util.get_software_by_category(cate_id)
            if not softs:
                QMessageBox.information(self, "提示", "该分类下暂无应用")
                return

            # 创建应用卡片
            col_count = 4 if self.width() > CARD_LAYOUT_SWITCH_WIDTH else 3
            for idx, soft in enumerate(softs):
                # 补充默认描述（如果没有）
                if not soft.get("description"):
                    soft["description"] = f"{soft.get('name')} - 官方正版应用，安全可靠"

                card = AppCard(soft)
                card.download_clicked.connect(self.download_app)
                self.app_cards.append(card)

                # 布局卡片
                row = idx // col_count
                col = idx % col_count
                self.card_layout.addWidget(card, row, col)

            self.logger.info(f"加载分类ID={cate_id}的应用卡片: {len(softs)}个")

        except Exception as e:
            self.logger.error(f"加载分类应用失败: {e}", exc_info=True)
            QMessageBox.warning(self, "错误", f"加载应用失败: {str(e)}")

    # -------------------- 应用更新卡片展示 --------------------
    def show_update_content(self):
        """显示应用更新卡片"""
        self.scroll_area.takeWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.clear_cards()

        self.title_label.setText("应用更新 - 本地可更新应用")

        try:
            updatable_apps = self.db_util.get_updatable_apps()
            if not updatable_apps:
                QMessageBox.information(self, "提示", "暂无需要更新的应用")
                return

            # 创建更新卡片
            col_count = 4 if self.width() > CARD_LAYOUT_SWITCH_WIDTH else 3
            for idx, app in enumerate(updatable_apps):
                # 补充描述
                app["description"] = f"当前版本：{app['local_version']}，最新版本：{app['remote_version']}"
                card = AppCard(app)
                card.download_clicked.connect(self.download_app)
                self.app_cards.append(card)

                # 布局卡片
                row = idx // col_count
                col = idx % col_count
                self.card_layout.addWidget(card, row, col)

            self.logger.info(f"加载可更新应用卡片: {len(updatable_apps)}个")

        except Exception as e:
            self.logger.error(f"加载可更新应用失败: {e}", exc_info=True)
            QMessageBox.warning(self, "错误", f"加载可更新应用失败: {str(e)}")

    # -------------------- 应用管理（表格展示） --------------------
    def show_manage_content(self):
        """显示应用管理（表格布局，本地应用）"""
        self.scroll_area.takeWidget()
        self.clear_cards()

        self.title_label.setText("应用管理 - 本地已安装应用")

        # 创建应用管理表格
        manage_widget = QWidget()
        manage_layout = QVBoxLayout(manage_widget)

        self.manage_table = QTableWidget()
        self.manage_table.setColumnCount(2)
        self.manage_table.setHorizontalHeaderLabels(["应用名称", "版本"])
        self.manage_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        # 加载本地应用
        local_apps = SystemAppUtil.get_local_installed_apps()
        if not local_apps:
            self.manage_table.setRowCount(0)
            QMessageBox.information(self, "提示", "未检测到本地已安装应用")
        else:
            self.manage_table.setRowCount(len(local_apps))
            for row, app in enumerate(local_apps):
                self.manage_table.setItem(
                    row, 0, QTableWidgetItem(app["name"]))
                self.manage_table.setItem(
                    row, 1, QTableWidgetItem(app["version"]))

        manage_layout.addWidget(self.manage_table)
        self.scroll_area.setWidget(manage_widget)

    # -------------------- 通用方法 --------------------
    def get_cate_name_by_id(self, cate_id: int) -> str:
        """通过分类ID获取名称"""
        categories = self.db_util.get_category_list()
        for cate in categories:
            if cate["id"] == cate_id:
                return cate["name"]
        return "未知分类"

    def download_app(self, url: str, app_name: str):
        """下载/更新应用"""
        if not ValidateUtil.validate_url(url):
            QMessageBox.warning(self, "错误", "下载链接无效")
            return

        self.download_dialog = DownloadDialog(f"下载 {app_name}", self)
        self.download_dialog.show()

        # 模拟下载
        self.progress_value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_download)
        self.timer.start(100)

        self.logger.info(f"开始下载应用: {app_name}, URL: {url}")

    def simulate_download(self):
        """模拟下载进度"""
        self.progress_value += 1
        if self.progress_value > 100:
            self.timer.stop()
            return

        status = f"下载中... {self.progress_value}%" if self.progress_value < 100 else "下载完成！"
        self.download_dialog.update_progress(self.progress_value, status)

    def switch_content_by_menu_index(self, menu_index: int):
        """根据菜单index切换内容"""
        if menu_index == 0:
            self.show_home_content()
        elif menu_index == 99:
            self.show_update_content()
        elif menu_index == 100:
            self.show_manage_content()
        else:
            self.show_category_content(menu_index)

# ===================== 主窗口 =====================


class AppStoreMainWindow(QMainWindow):
    """应用商店主窗口"""

    def __init__(self):
        super().__init__()
        self.logger = LogUtil.get_logger()
        self.db_util = DBUtil()
        self.init_ui()
        self.check_self_update()

    def init_ui(self):
        """初始化主窗口"""
        self.setWindowTitle("统信UOS内网应用商店")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)  # 整体最小尺寸
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fafafa;
                border: none;
            }
        """)

        # 中心组件
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
                border: none;
            }
        """)
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 左侧菜单
        self.left_panel = LeftMenuList()
        self.left_panel.setMaximumWidth(240)
        self.left_panel.setMinimumWidth(220)
        self.left_panel.menu_clicked.connect(self.on_menu_click)
        main_layout.addWidget(self.left_panel)

        # 右侧内容区域
        self.right_panel = RightContentArea()
        main_layout.addWidget(self.right_panel)

    def on_menu_click(self, menu_index: int):
        """菜单点击回调"""
        self.right_panel.switch_content_by_menu_index(menu_index)

    def check_self_update(self):
        """检查自更新"""
        class UpdateCheckThread(QThread):
            result = pyqtSignal(dict)

            def run(self):
                result = AppStoreUpdateUtil.check_self_update(DBUtil())
                self.result.emit(result)

        self.update_thread = UpdateCheckThread()
        self.update_thread.result.connect(self.on_self_update_check)
        self.update_thread.start()

    def on_self_update_check(self, result: dict):
        """自更新回调"""
        if result["need_update"]:
            reply = QMessageBox.question(
                self, "应用商店更新",
                f"{result['message']}\n当前版本: {result['local_version']}\n最新版本: {result['remote_version']}\n是否更新？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                if AppStoreUpdateUtil.do_self_update(result.get("download_url", "")):
                    QMessageBox.information(self, "成功", "更新完成，请重启应用商店")
                    self.close()
                else:
                    QMessageBox.warning(self, "失败", "更新失败，请手动下载安装")
        else:
            self.logger.info(result["message"])

    def closeEvent(self, event):
        """关闭事件"""
        self.db_util.close_remote_conn()
        self.logger.info("应用商店已关闭")
        event.accept()


# ===================== 程序入口 =====================
if __name__ == "__main__":
    LogUtil.init_logger()

    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMessageBox {
            font-size: 14px;
            border-radius: 12px;
            border: 1px solid #e8e8e8;
        }
        QMessageBox QPushButton {
            padding: 8px 16px;
            font-size: 14px;
            border-radius: 8px;
            border: none;
        }
    """)

    main_window = AppStoreMainWindow()
    main_window.show()

    sys.exit(app.exec())
