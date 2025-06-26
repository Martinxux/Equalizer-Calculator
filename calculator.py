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
        
    def update_note(self, result_str: str, note: str):
        """更新已有计算结果的备注"""
        if result_str in self.calculation_history:
            self.calculation_history[result_str]['note'] = note
            # 记录备注更新日志
            self.logger.info(f"更新上一组数据备注:Tap Tuner Result = {result_str}  |  备注: {note}")

    def process_numbers(self, number_str: str) -> List[int]:
        """
        处理数字字符串并返回计算结果
        
        参数:
            number_str: 逗号分隔的数字字符串
            
        返回:
            处理后的整数列表
        """
        # 分割字符串并转换为浮点数列表
        try:
            numbers = [float(x) for x in number_str.split(",")]
        except ValueError:
            raise ValueError("输入包含非数字字符")
            
        # 验证输入数字之和必须严格等于1
        total = sum(numbers)
        if total != 1.0:
            raise ValueError(f"输入数字之和不等于1，当前和为: {total}")
            
        try:    
            # 计算绝对值的和
            abs_sum = sum(abs(x) for x in numbers)
            
            if abs_sum == 0:
                result = [0] * len(numbers)  # 避免除以零
            else:
                # 计算每个数字的处理结果并四舍五入
                result = [round((num / abs_sum) * 1000) for num in numbers]
            
            # 生成结果字符串
            result_str = ",".join(map(str, result))
            
            # 存储计算结果
            self.calculation_history[result_str] = {
                'input': number_str,
                'note': '',
                'timestamp': datetime.now()
            }
            
            # 记录计算日志
            self.logger.info(f"Input Tap Values: {number_str} | Tap Tuner Result: {result_str}")
            
            return result_str
            
        except Exception as e:
            raise Exception(f"处理过程中发生错误: {e}")