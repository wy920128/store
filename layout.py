"""
统信UOS内网应用商店 - UI布局整合
修复分类加载数据类型不匹配问题
"""
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QMessageBox, QHeaderView, QTabWidget,
    QProgressBar, QDialog, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor

# 导入工具类
from util import (
    LogUtil, DBUtil, SystemAppUtil, AppStoreUpdateUtil,
    ValidateUtil, TimeUtil
)

# ===================== 下载进度对话框 =====================


class DownloadDialog(QDialog):
    """下载进度对话框"""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(400, 100)

        # 布局
        layout = QVBoxLayout(self)

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

# ===================== 左侧分类列表 =====================


class LeftCategoryList(QWidget):
    """左侧分类列表组件"""
    category_clicked = pyqtSignal(str)  # 分类点击信号

    def __init__(self):
        super().__init__()
        self.logger = LogUtil.get_logger()
        self.db_util = DBUtil()
        self.init_ui()
        self.load_categories()

    def init_ui(self):
        """初始化UI"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        # 标题
        title_label = QLabel("应用分类")
        title_label.setFont(QFont("Noto Sans SC", 12, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        # 分割线
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #e0e0e0;")
        self.layout.addWidget(line)

        # 分类列表
        self.category_list = QListWidget()
        self.category_list.setFont(QFont("Noto Sans SC", 10))
        # 设置列表样式（适配UOS）
        self.category_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: #f8f8f8;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)
        self.category_list.itemClicked.connect(self.on_category_click)
        self.layout.addWidget(self.category_list)

        # 刷新按钮
        refresh_btn = QPushButton("刷新分类")
        refresh_btn.setFont(QFont("Noto Sans SC", 9))
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        refresh_btn.clicked.connect(self.load_categories)
        self.layout.addWidget(refresh_btn)

    def load_categories(self):
        """加载分类列表（修复数据类型不匹配）"""
        try:
            self.category_list.clear()
            # 修改：直接获取分类数据，避免条件拼接
            categories = self.db_util.get_data("category")

            if not categories:
                self.logger.warning("分类列表为空")
                QMessageBox.information(self, "提示", "暂无分类数据")
                return

            for cate in categories:
                item = QListWidgetItem(cate["name"])
                item.setData(Qt.ItemDataRole.UserRole, cate["id"])
                self.category_list.addItem(item)

            self.logger.info(f"加载分类列表: {len(categories)}个分类")
        except Exception as e:
            self.logger.error(f"加载分类失败: {e}", exc_info=True)
            QMessageBox.warning(self, "错误", f"加载分类失败: {str(e)}")

    def on_category_click(self, item):
        """分类点击事件"""
        cate_name = item.text()
        self.logger.info(f"选中分类: {cate_name}")
        self.category_clicked.emit(cate_name)

# ===================== 右侧展示区域 =====================


class RightContentArea(QWidget):
    """右侧内容展示区域"""

    def __init__(self):
        super().__init__()
        self.logger = LogUtil.get_logger()
        self.db_util = DBUtil()
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # 顶部标题
        self.title_label = QLabel("应用列表")
        self.title_label.setFont(QFont("Noto Sans SC", 14, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Noto Sans SC", 10))
        self.layout.addWidget(self.tab_widget)

        # 1. 应用列表标签页
        self.app_list_widget = QWidget()
        self.app_list_layout = QVBoxLayout(self.app_list_widget)

        # 应用表格
        self.app_table = QTableWidget()
        self.app_table.setColumnCount(6)
        self.app_table.setHorizontalHeaderLabels([
            "应用名称", "版本", "大小", "下载量", "提供者", "操作"
        ])
        # 自适应列宽
        self.app_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        # 设置表格样式
        self.app_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #eee;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background-color: #f8f8f8;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 4px;
            }
        """)
        self.app_list_layout.addWidget(self.app_table)
        self.tab_widget.addTab(self.app_list_widget, "应用列表")

        # 2. 应用更新标签页
        self.update_widget = QWidget()
        self.update_layout = QVBoxLayout(self.update_widget)

        self.update_table = QTableWidget()
        self.update_table.setColumnCount(4)
        self.update_table.setHorizontalHeaderLabels([
            "应用名称", "当前版本", "最新版本", "操作"
        ])
        self.update_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.update_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #eee;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background-color: #f8f8f8;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 4px;
            }
        """)
        self.update_layout.addWidget(self.update_table)
        self.tab_widget.addTab(self.update_widget, "应用更新")

        # 3. 应用管理标签页
        self.manage_widget = QWidget()
        self.manage_layout = QVBoxLayout(self.manage_widget)

        self.manage_table = QTableWidget()
        self.manage_table.setColumnCount(2)
        self.manage_table.setHorizontalHeaderLabels([
            "应用名称", "版本"
        ])
        self.manage_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.manage_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #eee;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background-color: #f8f8f8;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 4px;
            }
        """)
        self.manage_layout.addWidget(self.manage_table)
        self.tab_widget.addTab(self.manage_widget, "应用管理")

    def load_category_apps(self, cate_name: str):
        """加载指定分类的应用（修复分类查询）"""
        try:
            self.title_label.setText(f"{cate_name} - 应用列表")

            if cate_name == "应用更新":
                self.load_updatable_apps()
                self.tab_widget.setCurrentWidget(self.update_widget)
            elif cate_name == "应用管理":
                self.load_managed_apps()
                self.tab_widget.setCurrentWidget(self.manage_widget)
            else:
                # 加载普通分类应用（修复：使用安全查询）
                self.load_normal_apps(cate_name)
                self.tab_widget.setCurrentWidget(self.app_list_widget)
        except Exception as e:
            self.logger.error(f"加载分类应用失败: {e}", exc_info=True)
            QMessageBox.warning(self, "错误", f"加载应用失败: {str(e)}")

    def load_normal_apps(self, cate_name: str):
        """加载普通分类应用（修复数据类型不匹配）"""
        # 修改：使用安全的分类查询方法
        category = self.db_util.get_category_by_name(cate_name)
        if not category:
            self.app_table.setRowCount(0)
            QMessageBox.information(self, "提示", f"分类 {cate_name} 不存在或无数据")
            return

        cate_id = category["id"]
        # 获取关联的软件ID（修改：使用参数化条件）
        c2s = self.db_util.get_data(
            "category2software", f"category_id = {cate_id}")
        soft_ids = [item["software_id"] for item in c2s]

        if not soft_ids:
            self.app_table.setRowCount(0)
            QMessageBox.information(self, "提示", f"分类 {cate_name} 下暂无应用")
            return

        # 获取软件信息
        softs = self.db_util.get_data(
            "software", f"id IN ({','.join(map(str, soft_ids))})")

        # 填充表格
        self.app_table.setRowCount(len(softs))
        for row, soft in enumerate(softs):
            # 应用名称
            self.app_table.setItem(row, 0, QTableWidgetItem(soft["name"]))
            # 版本
            self.app_table.setItem(
                row, 1, QTableWidgetItem(soft["version"] or ""))
            # 大小
            self.app_table.setItem(
                row, 2, QTableWidgetItem(soft["size"] or ""))
            # 下载量
            self.app_table.setItem(row, 3, QTableWidgetItem(
                str(soft["download_count"] or 0)))
            # 提供者（简化处理）
            self.app_table.setItem(row, 4, QTableWidgetItem("UOS官方"))

            # 下载按钮
            download_btn = QPushButton("下载")
            download_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            """)
            download_btn.clicked.connect(
                lambda checked, url=soft["download_url"], name=soft["name"]: self.download_app(url, name))
            self.app_table.setCellWidget(row, 5, download_btn)

        self.logger.info(f"加载{cate_name}分类应用: {len(softs)}条")

    def load_updatable_apps(self):
        """加载可更新应用"""
        updatable_apps = SystemAppUtil.get_updatable_apps(self.db_util)

        if not updatable_apps:
            self.update_table.setRowCount(0)
            QMessageBox.information(self, "提示", "暂无可更新应用")
            return

        self.update_table.setRowCount(len(updatable_apps))
        for row, app in enumerate(updatable_apps):
            # 应用名称
            self.update_table.setItem(row, 0, QTableWidgetItem(app["name"]))
            # 当前版本
            self.update_table.setItem(
                row, 1, QTableWidgetItem(app["local_version"]))
            # 最新版本
            self.update_table.setItem(
                row, 2, QTableWidgetItem(app["remote_version"]))

            # 更新按钮
            update_btn = QPushButton("更新")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            """)
            update_btn.clicked.connect(
                lambda checked, url=app["download_url"], name=app["name"]: self.download_app(url, name))
            self.update_table.setCellWidget(row, 3, update_btn)

    def load_managed_apps(self):
        """加载本地已装应用"""
        local_apps = SystemAppUtil.get_local_installed_apps()

        if not local_apps:
            self.manage_table.setRowCount(0)
            QMessageBox.information(self, "提示", "未检测到本地应用")
            return

        self.manage_table.setRowCount(len(local_apps))
        for row, app in enumerate(local_apps):
            # 应用名称
            self.manage_table.setItem(row, 0, QTableWidgetItem(app["name"]))
            # 版本
            self.manage_table.setItem(row, 1, QTableWidgetItem(app["version"]))

    def download_app(self, url: str, app_name: str):
        """下载应用（模拟进度）"""
        if not ValidateUtil.validate_url(url):
            QMessageBox.warning(self, "错误", "下载链接无效")
            return

        # 显示下载进度框
        self.download_dialog = DownloadDialog(f"下载 {app_name}", self)
        self.download_dialog.show()

        # 模拟下载进度
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

        status = f"下载中... {self.progress_value}%"
        if self.progress_value == 100:
            status = "下载完成！"

        self.download_dialog.update_progress(self.progress_value, status)

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
        # 窗口配置
        self.setWindowTitle("统信UOS内网应用商店")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)

        # 设置窗口样式（适配UOS）
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
        """)

        # 中心组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        # 左侧分类列表
        self.left_panel = LeftCategoryList()
        self.left_panel.setMaximumWidth(200)
        self.left_panel.setMinimumWidth(180)
        self.left_panel.category_clicked.connect(self.on_category_click)
        main_layout.addWidget(self.left_panel)

        # 右侧内容区域
        self.right_panel = RightContentArea()
        main_layout.addWidget(self.right_panel)

    def on_category_click(self, cate_name: str):
        """分类点击回调"""
        self.right_panel.load_category_apps(cate_name)

    def check_self_update(self):
        """检查应用商店自身更新"""
        # 后台线程检查更新
        class UpdateCheckThread(QThread):
            result = pyqtSignal(dict)

            def run(self):
                result = AppStoreUpdateUtil.check_self_update(DBUtil())
                self.result.emit(result)

        # 启动线程
        self.update_thread = UpdateCheckThread()
        self.update_thread.result.connect(self.on_self_update_check)
        self.update_thread.start()

    def on_self_update_check(self, result: dict):
        """自更新检查结果回调"""
        if result["need_update"]:
            reply = QMessageBox.question(
                self, "应用商店更新",
                f"{result['message']}\n当前版本: {result['local_version']}\n最新版本: {result['remote_version']}\n是否更新？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                # 执行更新
                if AppStoreUpdateUtil.do_self_update(result.get("download_url", "")):
                    QMessageBox.information(self, "成功", "更新完成，请重启应用商店")
                    self.close()
                else:
                    QMessageBox.warning(self, "失败", "更新失败，请手动下载安装")
        else:
            self.logger.info(result["message"])

    def closeEvent(self, event):
        """关闭事件"""
        self.db_util.close()
        self.logger.info("应用商店已关闭")
        event.accept()
