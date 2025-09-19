# Excel批处理脚本使用说明

## 修改内容

已成功修改 `excel_batch.py` 脚本，现在支持从JSON文件读取 `generation_prompt` 和 `reflection_prompt`。

## 主要变更

1. **添加了 `prompt_file` 参数**：现在需要指定包含prompt的JSON文件路径
2. **新增 `load_prompts()` 方法**：从JSON文件加载prompt数据
3. **修改了Excel列检查**：不再需要Excel文件包含 `generation_prompt` 和 `reflection_prompt` 列
4. **更新了处理逻辑**：使用从文件加载的prompt而不是Excel中的列

## 使用方法

### 命令行语法
```bash
python excel_batch.py --input_file <input_file> --prompt_file <prompt_file> [-o output_file] [-v]
```

### 参数说明
- `--input_file, -i`: 输入Excel或CSV文件路径（必需）
- `--prompt_file, -p`: 包含generation_prompt和reflection_prompt的JSON文件路径（必需）
- `-o, --output`: 输出文件路径（可选，默认自动生成）
- `-v, --verbose`: 详细输出模式

### 示例
```bash
# 使用默认输出文件名
python excel_batch.py --input_file sample_input.xlsx --prompt_file prompts/veo3_gen_prompt_shot.json

# 使用短参数名
python excel_batch.py -i sample_input.xlsx -p prompts/veo3_gen_prompt_shot.json

# 指定输出文件名
python excel_batch.py --input_file sample_input.xlsx --prompt_file prompts/veo3_gen_prompt_shot.json -o result.xlsx

# 详细输出模式
python excel_batch.py --input_file sample_input.xlsx --prompt_file prompts/veo3_gen_prompt_shot.json -v
```

## JSON文件格式

prompt文件必须包含以下字段：

```json
{
  "generation_prompt": [
    "第一行prompt内容",
    "第二行prompt内容",
    "..."
  ],
  "reflection_prompt": [
    "第一行reflection内容", 
    "第二行reflection内容",
    "..."
  ]
}
```

或者使用字符串格式：

```json
{
  "generation_prompt": "完整的generation prompt内容",
  "reflection_prompt": "完整的reflection prompt内容"
}
```

## Excel文件格式

现在Excel文件只需要包含以下列：
- `user_prompt`: 用户输入的prompt
- `generation_content`: 生成的内容
- `reflection_advice`: 反思建议
- `user_feedback`: 用户反馈

不再需要 `generation_prompt` 和 `reflection_prompt` 列。

## 处理流程

1. 加载prompt文件（JSON格式）
2. 加载Excel/CSV文件
3. 逐行处理数据，使用从文件加载的prompt
4. 保存处理结果到新的Excel文件

## 错误处理

脚本会检查：
- prompt文件是否存在
- JSON文件格式是否正确
- 是否包含必需的字段
- Excel文件是否包含必需的列
