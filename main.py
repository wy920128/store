"""
统信UOS内网应用商店 - 主入口
修复Qt6高DPI属性报错问题
"""
from util import LogUtil
from layout import AppStoreMainWindow
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# 确保导入路径正确
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入布局和工具类


def main():
    """主函数"""
    # 初始化日志
    LogUtil.init_logger()
    logger = LogUtil.get_logger()
    logger.info("启动统信UOS内网应用商店")

    # 创建应用
    app = QApplication(sys.argv)

    # Qt6 高DPI配置（仅保留有效配置）
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # 设置全局字体（适配统信UOS）
    font = QFont("Noto Sans SC", 10)  # UOS默认字体
    app.setFont(font)

    # 创建主窗口
    window = AppStoreMainWindow()
    window.show()

    # 运行应用
    exit_code = app.exec()
    logger.info(f"应用商店退出，退出码: {exit_code}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
