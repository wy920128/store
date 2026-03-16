'''
Author: 王野 18545455617@163.com
Date: 2026-03-10 11:06:46
LastEditors: 王野 18545455617@163.com
LastEditTime: 2026-03-16 16:14:55
FilePath: /store/main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
import os
# 调整导入顺序，确保路径优先（3.7对导入顺序更敏感）
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 替换PyQt6为PyQt5（3.7不兼容PyQt6）
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# 导入自定义工具类和窗口类
from util import LogUtil
from layout import AppStoreMainWindow  # 需确保layout.py已同步降级为PyQt5


def main():
    """主函数（适配Python3.7.3）"""
    # 初始化日志
    LogUtil.init_logger()
    logger = LogUtil.get_logger()
    logger.info("启动统信UOS内网应用商店（Python3.7.3+PyQt5）")

    # 创建应用
    app = QApplication(sys.argv)

    # ===== 关键修复：PyQt5 高DPI适配（替换Qt6的高DPI配置）=====
    # 方案1：启用高DPI自动缩放（PyQt5原生支持）
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    # 设置全局字体（适配统信UOS，3.7语法兼容）
    font = QFont("Noto Sans SC", 10)  # UOS默认字体
    app.setFont(font)

    # 创建主窗口
    window = AppStoreMainWindow()
    window.show()

    exit_code = app.exec_()
    logger.info(f"应用商店退出，退出码: {exit_code}")
    sys.exit(exit_code)


if __name__ == "__main__":
    # 3.7 建议增加异常捕获，避免启动崩溃无日志
    try:
        main()
    except Exception as e:
        # 初始化应急日志（若LogUtil未加载成功）
        import logging
        logging.basicConfig(level=logging.ERROR)
        logging.error(f"应用启动失败: {str(e)}", exc_info=True)
        sys.exit(1)