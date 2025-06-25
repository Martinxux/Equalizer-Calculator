import sys
from PyQt5.QtWidgets import QApplication
from gui import NumberCalculatorGUI

def main():
    """应用程序主入口"""
    app = QApplication(sys.argv)
    
    # 创建并显示主窗口
    calculator = NumberCalculatorGUI()
    calculator.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()