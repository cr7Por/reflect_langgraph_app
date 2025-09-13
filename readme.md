# LangGraph 提示词管理工具

一个基于Flask的Web界面，用于管理LangGraph的生成节点和反思节点提示词。

## 功能特性

- **左侧板块**：提示词管理
  - 加载默认提示词按钮
  - 从JSON文件加载提示词功能
  - 三个可编辑的提示词输入框：
    - 生成节点提示词
    - 反思节点提示词  
    - 用户提示词
  - 保存提示词到JSON文件功能

- **中间板块**：内容生成
  - 生成内容按钮
  - 显示生成内容的文本框

- **右侧板块**：反馈收集
  - 修改意见输入框
  - 保存反馈功能

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
```bash
# 复制环境变量示例文件
cp env.example .env

# 编辑 .env 文件，填入你的 API 密钥
# 至少需要设置 AZURE_OPENAI_API_KEY
```

3. 运行程序：
```bash
python app.py
```

4. 在浏览器中访问：http://localhost:5000

## 环境变量配置

项目需要以下环境变量（参考 `env.example` 文件）：

- `AZURE_OPENAI_API_KEY`: Azure OpenAI API 密钥（必需）
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI 端点
- `OPENAI_API_VERSION`: OpenAI API 版本
- `GEMINI_API_KEY`: Gemini API 密钥（可选）
- `AWS_MODEL`, `AWS_REGION`, `AWS_KEYID`, `AWS_KEY`: AWS 配置（可选）

## 使用说明

1. **加载提示词**：
   - 点击"加载默认提示词"按钮加载预设的提示词模板
   - 点击"从文件加载"按钮选择JSON文件加载自定义提示词
   
2. **编辑提示词**：在左侧编辑三个提示词输入框中的内容

3. **保存提示词**：点击"保存提示词"按钮将当前提示词保存为JSON文件

4. **生成内容**：点击"生成内容"按钮生成内容

5. **反馈收集**：在右侧输入修改意见并保存反馈

## JSON文件格式

提示词JSON文件应包含以下字段：
```json
{
  "generation_prompt": "生成节点的提示词模板",
  "reflection_prompt": "反思节点的提示词模板", 
  "user_prompt": "用户提示词模板"
}
```

示例文件：`mtv_script_prompt.json`
