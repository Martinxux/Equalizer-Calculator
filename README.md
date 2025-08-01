# 功能已集成到[DataMaster](https://github.com/Martinxux/DataMaster#)
# 均衡计算器 (Equalizer Calculator)

## 项目概述
这是一个基于PyQt5的GUI应用程序，用于计算和处理Tap Values输入。它可以将输入的数值进行均衡计算，并支持结果复制、备注添加和历史记录查看功能。

## 功能特点
- 输入Tap Values进行计算
- 自动归一化计算结果并乘以1000
- 计算结果复制功能
- 为计算结果添加备注
- 按天记录计算历史
- 简洁美观的用户界面

## 使用方法
1. 在输入框中输入Tap Values，用逗号分隔（例如：0.1,-0.5,0.4）
2. 点击"计算"按钮获取结果
3. 结果会自动显示在结果框中
4. 可点击"复制"按钮复制结果
5. 可在备注框中输入备注信息并点击"保存备注"
6. 点击"查看历史"可以查看当天的计算记录

## 核心算法
输入的数字会经过以下处理：
1. 计算所有数字绝对值的和
2. 每个数字除以这个和（归一化）
3. 结果乘以1000并四舍五入
4. 返回处理后的整数列表

公式表示为：
```
result[i] = round((input[i] / sum(abs(input))) * 1000)
```

## 依赖项
- Python 3.x
- PyQt5

## 安装与运行
1. 安装依赖：
```bash
pip install PyQt5
```

2. 运行程序：
```bash
python main.py
```

## 文件结构
```
.
├── .gitignore
├── README.md          # 项目说明文件
├── calculator.py      # 核心计算逻辑
├── gui.py            # 用户界面实现
└── main.py           # 程序入口
```

## 日志记录
计算结果会按天记录到日志文件中，格式为：
`number_calculator_log_YYYYMMDD.log`
