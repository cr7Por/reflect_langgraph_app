# save_mtv_script.py 批处理功能使用说明

## 新增功能

在 `save_mtv_script.py` 中新增了 `save_graph_batch_to_excel` 函数，用于从JSON文件生成批处理Excel文件。

## 功能说明

### `save_graph_batch_to_excel` 函数

**功能**：从JSON文件读取镜头数据，生成包含指定列的Excel文件，用于批处理

**参数**：
- `json_file`: 包含镜头数据的JSON文件路径
- `output_file`: 输出Excel文件路径（可选，默认自动生成）

**返回值**：
- 成功：生成的Excel文件路径
- 失败：None

## 使用方法

### 1. 命令行使用

```bash
# 基本用法（自动生成输出文件名）
python save_mtv_script.py batch mtv_data.json

# 指定输出文件名
python save_mtv_script.py batch mtv_data.json batch_input.xlsx

# 默认模式（生成MTV脚本Excel文件）
python save_mtv_script.py
```

### 2. 在代码中调用

```python
from save_mtv_script import save_graph_batch_to_excel

# 生成批处理Excel文件
result = save_graph_batch_to_excel("mtv_data.json", "batch_input.xlsx")
if result:
    print(f"文件生成成功: {result}")
else:
    print("文件生成失败")
```

## 输入JSON文件格式

JSON文件必须包含 `sections` 字段，格式如下：

```json
{
  "sections": [
    {
      "镜头序号": 1,
      "镜头描述": "高空俯拍暮色城市，灯光如星河点点...",
      "景别": "全景",
      "角度": "俯视",
      "运镜方式": "轨道缓慢拉近 → 稳定器轻推",
      "对应台词/时间点": "00:00‑00:07 前奏",
      "备注": "暖金调色 + 轻微雾化；加入0.4s雨滴特写作为呼吸镜头。"
    },
    {
      "镜头序号": 2,
      "镜头描述": "水面特写，雨滴落下激起涟漪...",
      "景别": "特写",
      "角度": "正面",
      "运镜方式": "手持慢摇 → 稳定器下推",
      "对应台词/时间点": "00:07‑00:12 留意街灯的金光",
      "备注": "金色光环CG，颜色从 #D4A35F 渐变至 #F2C1C1（柔粉）保持自然光感。"
    }
  ]
}
```

## 输出Excel文件格式

生成的Excel文件包含两个工作表：

### 1. Batch_Data 工作表
包含以下列：
- **user_prompt**: 组合的镜头信息（格式：镜头序号：1，镜头描述：xxx，景别：xxx，角度：xxx，运镜方式：xxx，对应台词/时间点：xxx，备注：xxx）
- **generation_content**: 空内容（批处理后自动填充）
- **reflection_advice**: 空内容（批处理后自动填充）
- **user_feedback**: 空内容（需要手动填写）

### 2. 使用说明 工作表
包含各列的详细说明和示例。

## 列宽设置

- user_prompt: 80字符宽度（容纳长文本）
- generation_content: 50字符宽度
- reflection_advice: 50字符宽度
- user_feedback: 50字符宽度

## 错误处理

函数会检查：
- JSON文件是否存在
- JSON文件格式是否正确
- 是否包含必需的 `sections` 字段
- `sections` 是否为列表类型

## 使用流程

1. **准备JSON文件**：确保包含镜头数据的JSON文件格式正确
2. **生成批处理Excel**：使用 `save_graph_batch_to_excel` 函数生成Excel文件
3. **填写用户反馈**：在Excel文件的 `user_feedback` 列中填写反馈（可选）
4. **运行批处理**：使用 `excel_batch.py` 脚本处理Excel文件

## 示例

```bash
# 1. 生成批处理Excel文件
python save_mtv_script.py batch mtv_city_xu.json batch_input.xlsx

# 2. 运行批处理（需要prompt文件）
python excel_batch.py --input_file batch_input.xlsx --prompt_file prompts/veo3_gen_prompt_shot.json -o result.xlsx

# 或者使用短参数名
python excel_batch.py -i batch_input.xlsx -p prompts/veo3_gen_prompt_shot.json -o result.xlsx
```

## 注意事项

- JSON文件必须使用UTF-8编码
- 镜头数据中的字段名称必须与示例一致
- 生成的Excel文件会自动设置合适的列宽
- 输出文件名如果不指定，会自动生成带时间戳的文件名
