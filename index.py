#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UOS应用商店 - 主入口"""
import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

# 导入拆分后的组件
from layout_left import LeftClassifyPanel
from layout_right import RightAppPanel
from mariadb import MariaDBManager
from util import cache_manager  # 缓存管理器
from upgrade import check_app_upgrade  # 新增：导入更新函数

# ===================== 更新检查线程（避免阻塞UI） =====================


class UpgradeCheckThread(QThread):
    """后台检查更新线程（不阻塞主界面）"""
    upgrade_result = pyqtSignal(bool, str)

    def run(self):
        try:
            # 执行更新检查
            is_updated = check_app_upgrade()
            if is_updated:
                self.upgrade_result.emit(True, "应用已更新到最新版本！")
            else:
                self.upgrade_result.emit(False, "当前已是最新版本，无需更新")
        except Exception as e:
            self.upgrade_result.emit(False, f"更新检查失败：{str(e)}")

# ===================== 主窗口 =====================


class AppStoreMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UOS 应用商店")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)

        # 初始化MariaDB（仅用于图标操作）
        self.mariadb_manager = MariaDBManager()
        self.mariadb_manager.connect()

        # 全局字体
        self.is_windows = sys.platform == "win32"
        self.default_font = QFont(
            "Microsoft YaHei", 10) if self.is_windows else QFont("Noto Sans SC", 10)

        # 初始化界面
        self._init_ui()

        # 启动时清理过期缓存
        cache_manager.clear_expired_cache()

        # 新增：后台检查更新（不阻塞UI）
        self._check_upgrade()

    def _init_ui(self):
        """初始化主界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左侧分类面板
        self.left_panel = LeftClassifyPanel(self.default_font)
        self.left_panel.classify_list.itemClicked.connect(
            self._on_classify_click)
        main_layout.addWidget(self.left_panel)

        # 右侧应用面板
        self.right_panel = RightAppPanel(self.default_font)
        main_layout.addWidget(self.right_panel, stretch=1)

        # 默认加载首页应用
        self.right_panel.load_apps(
            self.left_panel.get_selected_classify_id(),
            self.left_panel.get_selected_classify_name()
        )

    def _check_upgrade(self):
        """后台检查更新"""
        upgrade_thread = UpgradeCheckThread()
        upgrade_thread.upgrade_result.connect(self._on_upgrade_check_finish)
        upgrade_thread.start()

    def _on_upgrade_check_finish(self, is_updated: bool, msg: str):
        """更新检查完成回调"""
        # 显示更新结果提示框
        if is_updated:
            QMessageBox.information(self, "更新成功", msg)
            # 可选：更新后重启应用
            # QMessageBox.information(self, "提示", "应用已更新，需要重启生效！")
        else:
            # 无需更新/失败，仅打印日志（不弹窗）
            print(f"更新检查结果：{msg}")

    def _on_classify_click(self):
        """分类点击事件"""
        classify_id = self.left_panel.get_selected_classify_id()
        classify_name = self.left_panel.get_selected_classify_name()
        self.right_panel.load_apps(classify_id, classify_name)

    def closeEvent(self, event):
        """关闭窗口"""
        self.mariadb_manager.close()
        event.accept()


# ===================== 入口函数 =====================
if __name__ == "__main__":
    # 高DPI适配（仅保留缩放策略，避免报错）
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei", 10) if sys.platform ==
                "win32" else QFont("Noto Sans SC", 10))

    # 样式适配
    if sys.platform == "linux":
        app.setStyle("Fusion")
    else:
        app.setStyle("WindowsVista")

    # 启动主窗口
    window = AppStoreMainWindow()
    window.show()

    # 运行应用
    sys.exit(app.exec())
