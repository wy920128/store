#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""右侧应用列表+安装组件"""
import sys
import subprocess
from typing import List, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit,
    QProgressBar, QMessageBox, QScrollArea, QGridLayout, QSizePolicy,
    QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QColor
from util import query_with_cache  # 导入缓存查询函数
from mariadb import MariaDBManager  # 仅用于图标查询

# 应用卡片组件


class AppCard(QWidget):
    """应用卡片"""
    install_clicked = pyqtSignal(dict)

    def __init__(self, app_data: Dict, font: QFont, parent=None):
        super().__init__(parent)
        self.app_data = app_data
        self.default_font = font
        self.mariadb_manager = MariaDBManager()  # 图标查询用
        self.setFixedHeight(80)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Fixed)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        # 应用图标
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(48, 48)
        self._load_icon()
        layout.addWidget(self.icon_label)

        # 信息区
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        name_label = QLabel(self.app_data["name"])
        name_label.setFont(
            QFont(self.default_font.family(), 11, QFont.Weight.Bold))
        desc_label = QLabel(self.app_data.get("description") or "暂无描述")
        desc_label.setFont(self.default_font)
        desc_label.setStyleSheet("color: #666;")
        info_layout.addWidget(name_label)
        info_layout.addWidget(desc_label)
        layout.addLayout(info_layout, stretch=1)

        # 安装按钮
        self.install_btn = QPushButton("安装")
        self.install_btn.setFixedSize(70, 32)
        self.install_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        self.install_btn.clicked.connect(
            lambda: self.install_clicked.emit(self.app_data))
        layout.addWidget(self.install_btn)

    def _load_icon(self):
        """加载应用图标"""
        pixmap = self.mariadb_manager.get_software_icon(self.app_data["id"])
        if pixmap and not pixmap.isNull():
            self.icon_label.setPixmap(pixmap.scaled(
                48, 48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            default_pixmap = QPixmap(48, 48)
            default_pixmap.fill(QColor("#e0e0e0"))
            self.icon_label.setPixmap(default_pixmap)

# 命令执行线程


class CommandThread(QThread):
    log_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(bool, str)

    def __init__(self, software_name: str, pkg_name: Optional[str] = None):
        super().__init__()
        self.software_name = software_name
        self.pkg_name = pkg_name or software_name.lower().replace(" ", "-")
        self.is_windows = sys.platform == "win32"

    def run(self):
        try:
            if self.is_windows:
                self.log_signal.emit(
                    f"【Windows 调试】模拟安装 {self.software_name}...")
                import time
                time.sleep(2)
                self.finish_signal.emit(
                    True, f"Windows 调试：{self.software_name} 模拟安装成功！")
            else:
                self.log_signal.emit(f"【UOS 真实安装】开始安装 {self.software_name}...")
                install_cmd = ["pkexec", "apt", "install", "-y", self.pkg_name]
                process = subprocess.Popen(
                    install_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    bufsize=1,
                    universal_newlines=True
                )
                for line in iter(process.stdout.readline(), ""):
                    if line:
                        self.log_signal.emit(line.strip())
                process.wait()
                if process.returncode == 0:
                    self.finish_signal.emit(
                        True, f"{self.software_name} 安装成功！")
                else:
                    self.finish_signal.emit(
                        False, f"{self.software_name} 安装失败，错误码：{process.returncode}")
        except Exception as e:
            self.finish_signal.emit(False, f"执行异常：{str(e)}")

# 右侧主面板


class RightAppPanel(QWidget):
    """右侧应用列表面板"""

    def __init__(self, font: QFont, parent=None):
        super().__init__(parent)
        self.default_font = font
        self.current_classify_id: Optional[int] = None

        self._init_ui()

    def _init_ui(self):
        """初始化右侧界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 顶部标题栏
        top_bar = QWidget()
        top_bar.setFixedHeight(56)
        top_bar.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(16, 0, 16, 0)
        self.classify_title = QLabel("首页")
        self.classify_title.setFont(
            QFont(self.default_font.family(), 16, QFont.Weight.Bold))
        top_layout.addWidget(self.classify_title)
        layout.addWidget(top_bar)

        # 应用列表滚动区
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ffffff;
            }
            QScrollBar:vertical {
                width: 8px;
                background-color: transparent;
            }
            QScrollBar::handle:vertical {
                background-color: #cccccc;
                border-radius: 4px;
                min-height: 20px;
            }
        """)
        self.app_container = QWidget()
        self.app_grid = QGridLayout(self.app_container)
        self.app_grid.setContentsMargins(16, 16, 16, 16)
        self.app_grid.setSpacing(12)
        scroll_area.setWidget(self.app_container)
        layout.addWidget(scroll_area)

        # 日志与进度条
        self.log_text = QTextEdit()
        self.log_text.setFixedHeight(120)
        self.log_text.setFont(self.default_font)
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(
            "background-color: #f8f8f8; border-top: 1px solid #e0e0e0;")
        layout.addWidget(self.log_text)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

    def load_apps(self, classify_id: Optional[int], classify_name: str):
        """加载指定分类下的应用（使用缓存）"""
        self.current_classify_id = classify_id
        self.classify_title.setText(classify_name)

        # 清空旧应用
        while self.app_grid.count() > 0:
            child = self.app_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 构建SQL并从缓存查询
        if classify_id is None:
            # 首页：所有软件
            sql = """
            SELECT * FROM software 
            WHERE deleted_time IS NULL 
            ORDER BY name ASC
            """
            apps = query_with_cache(sql)
        else:
            # 指定分类：关联查询
            sql = """
            SELECT s.* 
            FROM software s
            JOIN classify2software c2s ON s.id = c2s.software_id
            WHERE c2s.classify_id = %s 
            AND s.deleted_time IS NULL 
            AND c2s.deleted_time IS NULL
            ORDER BY s.name ASC
            """
            apps = query_with_cache(sql, (classify_id,))

        if not apps:
            empty_label = QLabel("暂无应用")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setFont(self.default_font)
            self.app_grid.addWidget(empty_label, 0, 0)
            return

        # 按3列布局
        col_count = 3
        for i, app in enumerate(apps):
            row = i // col_count
            col = i % col_count
            card = AppCard(app, self.default_font)
            card.install_clicked.connect(self._on_install_click)
            self.app_grid.addWidget(card, row, col)

    def _on_install_click(self, app_data: Dict):
        """处理安装点击事件"""
        software_name = app_data["name"]
        pkg_name = app_data["download_url"].split(
            "/")[-1].replace(".deb", "") if app_data.get("download_url") else None

        confirm = QMessageBox.question(
            self, "确认安装",
            f"是否安装 {software_name}？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.log_text.clear()
        self.progress_bar.setVisible(True)

        # 启动安装线程
        self.cmd_thread = CommandThread(software_name, pkg_name)
        self.cmd_thread.log_signal.connect(self._append_log)
        self.cmd_thread.finish_signal.connect(self._on_cmd_finish)
        self.cmd_thread.start()

    def _append_log(self, log: str):
        """追加日志"""
        self.log_text.append(log)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum())

    def _on_cmd_finish(self, success: bool, msg: str):
        """安装完成回调"""
        self.progress_bar.setVisible(False)
        if success:
            QMessageBox.information(self, "成功", msg)
            self.log_text.append(f"\n✅ {msg}")
        else:
            QMessageBox.critical(self, "失败", msg)
            self.log_text.append(f"\n❌ {msg}")
