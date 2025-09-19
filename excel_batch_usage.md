# Excel/CSV批处理脚本使用说明

## 功能描述

`excel_batch.py` 是一个用于批量处理Excel和CSV数据的脚本，它能够：

1. 从Excel或CSV文件加载数据（包含generation_prompt, reflection_prompt, user_prompt, generation_content, reflection_advice, user_feedback列）
2. 调用 `generation_graph_flow_v1` 对每一行数据进行处理
3. 将生成的新的generation_content和reflection_advice保存到新的Excel或CSV文件中

## 文件结构

```
excel_batch.py          # 主批处理脚本
create_sample_excel.py  # 创建示例Excel文件的脚本
sample_input.csv        # 示例CSV文件
test_excel_batch.py     # 测试脚本
excel_batch_usage.md    # 使用说明文档
```

## 使用方法

### 1. 准备Excel或CSV文件

Excel或CSV文件必须包含以下列：
- `generation_prompt`: 生成提示词
- `reflection_prompt`: 反思提示词  
- `user_prompt`: 用户提示词
- `generation_content`: 生成内容（初始值）
- `reflection_advice`: 反思建议（初始值）
- `user_feedback`: 用户反馈

### 2. 运行批处理脚本

#### 基本用法
```bash
# 处理Excel文件
python excel_batch.py input_file.xlsx

# 处理CSV文件
python excel_batch.py input_file.csv
```

#### 指定输出文件
```bash
# 输出为Excel文件
python excel_batch.py input_file.csv -o output_file.xlsx

# 输出为CSV文件
python excel_batch.py input_file.xlsx -o output_file.csv
```

#### 详细输出模式
```bash
python excel_batch.py input_file.csv -v
```

### 3. 测试脚本功能

可以使用提供的示例文件测试脚本：

```bash
# 运行测试脚本
python test_excel_batch.py

# 或者直接处理示例CSV文件
python excel_batch.py sample_input.csv
```

## 输出结果

脚本会生成一个新的Excel或CSV文件，包含：

### 原始数据列
- 所有输入的原始列数据

### 新增的处理结果列
- `processed_generation_content`: 处理后的生成内容
- `processed_reflection_advice`: 处理后的反思建议
- `reflect_count`: 反思次数
- `process_error`: 处理错误信息（如果有）
- `process_timestamp`: 处理时间戳

### 处理摘要表
- 总行数
- 成功处理行数
- 失败行数
- 处理时间
- 输入文件路径
- 输出文件路径

**注意**: 
- Excel输出会包含两个工作表：`Processed_Data`（主数据）和`Processing_Summary`（摘要）
- CSV输出会生成两个文件：主数据文件和`_summary.csv`摘要文件

## 错误处理

脚本包含完善的错误处理机制：

1. **文件检查**: 验证输入文件是否存在
2. **列检查**: 验证Excel或CSV文件是否包含必需的列
3. **行级错误处理**: 单行处理失败不会影响其他行的处理
4. **详细日志**: 记录所有处理过程和错误信息

## 日志记录

脚本使用项目中的logger模块记录详细的处理信息，包括：
- 文件加载状态
- 每行处理进度
- 错误信息和堆栈跟踪
- 处理统计信息

## 注意事项

1. **异步处理**: 脚本使用异步处理，确保与LangGraph的兼容性
2. **内存管理**: 对于大文件，脚本逐行处理以节省内存
3. **进度显示**: 每处理10行会显示一次进度
4. **文件编码**: 支持UTF-8编码的Excel和CSV文件

## 依赖要求

确保安装了以下Python包：
- pandas
- openpyxl
- asyncio
- 项目中的其他依赖（graph.py, state.py, utils.py, logger.py等）

## 示例工作流程

1. 准备包含所需列的Excel或CSV文件
2. 运行 `python excel_batch.py your_file.csv` 或 `python excel_batch.py your_file.xlsx`
3. 等待处理完成
4. 检查生成的输出文件和处理摘要
5. 查看日志文件了解详细处理过程

## 快速开始

1. 使用提供的示例文件测试：
   ```bash
   python excel_batch.py sample_input.csv
   ```

2. 查看生成的输出文件：
   - `sample_input_processed_YYYYMMDD_HHMMSS.csv` - 处理后的数据
   - `sample_input_processed_YYYYMMDD_HHMMSS_summary.csv` - 处理摘要
