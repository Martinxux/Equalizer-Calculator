from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from calculator import NumberCalculator
from datetime import datetime
import os

class NumberCalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator = NumberCalculator()
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("均衡计算器")
        self.setFixedSize(800, 220)  # 增加高度以容纳公式
        
        # 设置样式表
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f5f5f5;
                font-family: 'Microsoft YaHei';
                font-size: 18px;
            }
            QLabel {
                font-size: 18px;
                color: #333;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-size: 18px;
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 18px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            #result_display {
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)  # 更小的边距
        main_layout.setSpacing(6)  # 更小的控件间距
        main_widget.setLayout(main_layout)
        
        # 输入部分
        input_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        
        # 输入和计算区域
        input_group = QVBoxLayout()
        main_layout.addLayout(input_group)
        
        # 输入行
        input_row = QHBoxLayout()
        input_group.addLayout(input_row)
        
        input_label = QLabel("输入Tap Values:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("例如: 0.1,-0.5,0.4 这是测试数据")
        self.input_field.setMinimumWidth(250)  # 更窄的输入框
        
        input_row.addWidget(input_label)
        input_row.addWidget(self.input_field)
        
        # 计算按钮
        calculate_btn = QPushButton("计算")
        calculate_btn.clicked.connect(self.calculate)
        input_row.addWidget(calculate_btn)
        
        # 结果显示区域
        result_layout = QHBoxLayout()
        input_group.addLayout(result_layout)
        
        output_label = QLabel("均衡值转换结果:")
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        # self.result_display.setFixedHeight(30)
        self.result_display.setPlaceholderText("计算结果将显示在这里...")
        self.result_display.setStyleSheet("font-size: 18px")
        result_layout.addWidget(output_label)
        result_layout.addWidget(self.result_display)
        
        # 复制按钮
        copy_btn = QPushButton("复制")
        copy_btn.clicked.connect(self.copy_result)
        result_layout.addWidget(copy_btn)
        
        # 备注和历史区域
        note_history_layout = QHBoxLayout()
        main_layout.addLayout(note_history_layout)
        
        # 备注部分
        note_layout = QHBoxLayout()
        note_history_layout.addLayout(note_layout)
        
        note_label = QLabel("添加该参数备注:")
        self.note_field = QLineEdit()
        self.note_field.setPlaceholderText("计算后可添加备注信息，例如：Tdecq=1.5")
        
        save_note_btn = QPushButton("保存备注")
        save_note_btn.clicked.connect(self.save_note)
        
        note_layout.addWidget(note_label)
        note_layout.addWidget(self.note_field)
        note_layout.addWidget(save_note_btn)
        
        # 历史按钮
        history_btn = QPushButton("查看历史")
        history_btn.clicked.connect(self.show_history)
        note_history_layout.addWidget(history_btn)

        # 公式说明
        formula_label = QLabel("计算公式: result[i] = round((input[i] / sum(abs(input))) * 1000)")
        formula_label.setStyleSheet("font-size: 16px; color: #555; margin-top: 10px;")
        formula_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(formula_label)
        
    def calculate(self):
        """执行计算并显示结果"""
        input_text = self.input_field.text().strip()
        if not input_text:
            QMessageBox.warning(self, "输入错误", "请输入数字!")
            return
            
        try:
            # 处理数字但不带备注
            result = self.calculator.process_numbers(input_text)
            self.result_display.setText(result)
            self.last_result = result  # 保存计算结果
        except Exception as e:
            QMessageBox.critical(self, "计算错误", str(e))   
            
    def copy_result(self):
        """复制当前结果到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_display.text())
        
    def save_note(self):
        """保存计算结果备注"""
        note = self.note_field.text().strip()
        if not note:
            QMessageBox.warning(self, "输入错误", "请输入备注内容!")
            return
            
        try:
            # 获取当前计算结果
            current_result = self.result_display.text()
            if not current_result:
                QMessageBox.warning(self, "操作错误", "请先进行计算!")
                return
                
            # 直接更新备注
            self.calculator.update_note(current_result, note)
            
            QMessageBox.information(self, "保存成功", "备注已保存!")
            self.note_field.clear()
        except Exception as e:
            QMessageBox.critical(self, "保存错误", f"保存备注失败: {str(e)}")

            
    def show_history(self):
        """直接打开日志文件"""
        log_file = f'number_calculator_log_{datetime.now().strftime("%Y%m%d")}.log'
        try:
            os.startfile(log_file)
        except FileNotFoundError:
            QMessageBox.information(self, "历史记录", "今日暂无历史记录")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开日志文件失败: {str(e)}")