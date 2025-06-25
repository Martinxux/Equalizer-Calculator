import logging
from typing import List
from datetime import datetime

class NumberCalculator:
    def __init__(self):
        self.setup_logger()
        self.calculation_history = {}  # 存储计算结果和备注
        
    def setup_logger(self):
        """配置日志记录器"""
        self.logger = logging.getLogger('NumberCalculator')
        self.logger.setLevel(logging.INFO)
        
        # 按天创建日志文件
        log_filename = f'number_calculator_log_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        
    def process_numbers(self, number_str: str, note: str = None) -> List[int]:
        """
        处理数字字符串并返回计算结果
        
        参数:
            number_str: 逗号分隔的数字字符串
            note: 可选备注信息(会自动保存)
            
        返回:
            处理后的整数列表
        """
        try:
            # 分割字符串并转换为浮点数列表
            numbers = [float(x) for x in number_str.split(",")]
            
            # 计算绝对值的和
            abs_sum = sum(abs(x) for x in numbers)
            
            if abs_sum == 0:
                result = [0] * len(numbers)  # 避免除以零
            else:
                # 计算每个数字的处理结果并四舍五入
                result = [round((num / abs_sum) * 1000) for num in numbers]
            
            # 生成结果字符串
            result_str = ",".join(map(str, result))
            
            # 存储/更新计算结果和备注
            self.calculation_history[result_str] = {
                'input': number_str,
                'note': note or '',
                'timestamp': datetime.now()
            }
            
            # 记录计算日志（包含备注）
            log_msg = f"Input Tap Values: {number_str} | Result: {result_str}"
            if note:
                log_msg += f" | 备注: {note}"
            self.logger.info(log_msg)
            
            return result_str
            
        except ValueError:
            raise ValueError("输入包含非数字字符")
        except Exception as e:
            raise Exception(f"处理过程中发生错误: {e}")            