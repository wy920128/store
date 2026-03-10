'''
Author: 王野 18545455617@163.com
Date: 2026-03-07 08:56:21
LastEditors: 王野 18545455617@163.com
LastEditTime: 2026-03-10 09:47:42
FilePath: /store/layout_left.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""左侧分类列表组件"""
from typing import List, Dict, Optional
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from util import query_with_cache  # 导入缓存查询函数


class LeftClassifyPanel(QFrame):
    """左侧分类列表面板"""

    def __init__(self, font: QFont, parent=None):
        super().__init__(parent)
        self.default_font = font
        self.current_classify_id: Optional[int] = None  # None代表首页

        self._init_ui()
        self._load_classifies()

    def _init_ui(self):
        """初始化左侧界面"""
        self.setStyleSheet("""
            QFrame {
                background-color: #f5f5f7;
                border-right: 1px solid #e0e0e0;
            }
        """)
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 分类列表
        self.classify_list = QListWidget()
        self.classify_list.setFont(self.default_font)
        self.classify_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                margin-top: 10px;
            }
            QListWidget::item {
                height: 48px;
                padding-left: 16px;
                border: none;
            }
            QListWidget::item:selected {
                background-color: #e8edf3;
                color: #0066cc;
                border-left: 3px solid #0066cc;
            }
            QListWidget::item:hover:!selected {
                background-color: #f0f2f5;
            }
        """)
        layout.addWidget(self.classify_list)

    def _load_classifies(self):
        """加载分类列表（使用缓存）"""
        self.classify_list.clear()
        # 首页
        home_item = QListWidgetItem("首页")
        home_item.setData(Qt.ItemDataRole.UserRole, None)
        self.classify_list.addItem(home_item)

        # 从缓存查询分类数据
        sql = """
        SELECT id, name, description 
        FROM classify 
        WHERE deleted_time IS NULL 
        ORDER BY id ASC
        """
        classifies = query_with_cache(sql)

        for classify in classifies:
            item = QListWidgetItem(classify["name"])
            item.setData(Qt.ItemDataRole.UserRole, classify["id"])
            self.classify_list.addItem(item)

        # 默认选中首页
        self.classify_list.setCurrentRow(0)
        self.current_classify_id = None

    def get_selected_classify_id(self) -> Optional[int]:
        """获取选中的分类ID"""
        current_item = self.classify_list.currentItem()
        if not current_item:
            return None
        return current_item.data(Qt.ItemDataRole.UserRole)

    def get_selected_classify_name(self) -> str:
        """获取选中的分类名称"""
        current_item = self.classify_list.currentItem()
        return current_item.text() if current_item else "首页"
