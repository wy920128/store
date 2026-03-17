'''
Author: 王野 18545455617@163.com
Date: 2026-03-10 11:06:46
LastEditors: 王野 18545455617@163.com
LastEditTime: 2026-03-17 18:27:09
FilePath: /store/start.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# 导入自定义工具类和窗口类
from util import LogUtil
from layout import AppStoreMainWindow


def start():
    """主函数"""
    # 初始化日志
    LogUtil.init_logger()
    logger = LogUtil.get_logger()
    logger.info("启动统信UOS内网应用商店")

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    font = QFont("Noto Sans SC", 10)  # UOS默认字体
    app.setFont(font)

    # 创建主窗口
    window = AppStoreMainWindow()
    window.show()

    exit_code = app.exec_()
    logger.info(f"应用商店退出，退出码: {exit_code}")
    sys.exit(exit_code)


if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        import logging
        logging.basicConfig(level=logging.ERROR)
        logging.error(f"应用启动失败: {str(e)}", exc_info=True)
        sys.exit(1)