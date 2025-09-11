from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import datetime
from state import Graph_State
from graph import graph

app = Flask(__name__)

# 默认提示词模板
DEFAULT_PROMPTS = {
    "generate_prompt": "请根据以下内容生成详细的回答：\n\n{user_input}",
    "reflection_prompt": "请对以下内容进行反思和评估：\n\n{generated_content}",
    "user_prompt": "请输入您的问题或需求："
}

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html', prompts=DEFAULT_PROMPTS)

@app.route('/load_default', methods=['POST'])
def load_default():
    """加载默认提示词"""
    return jsonify(DEFAULT_PROMPTS)

@app.route('/load_file', methods=['POST'])
def load_file():
    """从JSON文件加载提示词"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "没有选择文件"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400
        
        if file and file.filename.endswith('.json'):
            data = json.load(file)
            
            # 提取提示词，如果不存在则使用默认值
            prompts = {
                "generate_prompt": data.get("generate_prompt", DEFAULT_PROMPTS["generate_prompt"]),
                "reflection_prompt": data.get("reflection_prompt", DEFAULT_PROMPTS["reflection_prompt"]),
                "user_prompt": data.get("user_prompt", DEFAULT_PROMPTS["user_prompt"])
            }
            
            return jsonify(prompts)
        else:
            return jsonify({"error": "请选择JSON文件"}), 400
            
    except Exception as e:
        return jsonify({"error": f"加载文件失败: {str(e)}"}), 500

@app.route('/save_prompts', methods=['POST'])
def save_prompts():
    """保存提示词到JSON文件"""
    try:
        data = request.json
        prompts_data = {
            "generate_prompt": data.get("generate_prompt", ""),
            "reflection_prompt": data.get("reflection_prompt", ""),
            "user_prompt": data.get("user_prompt", "")
        }
        
        # 创建prompts目录（如果不存在）
        os.makedirs("prompts", exist_ok=True)
        
        # 生成文件名（包含时间戳）
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prompts/prompts_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(prompts_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({"message": f"提示词已保存到: {filename}"})
        
    except Exception as e:
        return jsonify({"error": f"保存失败: {str(e)}"}), 500

@app.route('/generate_content', methods=['POST'])
def generate_content():
    """生成内容（模拟LangGraph的生成和反思过程）"""
    try:
        data = request.json
        generate_prompt = data.get("generate_prompt", "")
        reflection_prompt = data.get("reflection_prompt", "")
        user_prompt = data.get("user_prompt", "")
        
        if not user_prompt.strip():
            return jsonify({"error": "请输入用户提示词"})
        
        # 模拟生成节点
        generated_text = f"基于生成提示词：{generate_prompt}\n\n用户输入：{user_prompt}\n\n生成的内容：\n这是一个模拟的生成内容。在实际应用中，这里会调用LangGraph的生成节点来处理用户输入并生成相应的内容。"
        
        # 模拟反思节点
        reflection_text = f"基于反思提示词：{reflection_prompt}\n\n对生成内容的反思：\n生成的内容质量良好，逻辑清晰，但可能需要进一步完善细节。"
        
        final_content = f"{generated_text}\n\n---反思结果---\n{reflection_text}"
        
        return jsonify({"content": final_content})
        
    except Exception as e:
        return jsonify({"error": f"生成内容失败: {str(e)}"}), 500

@app.route('/save_feedback', methods=['POST'])
def save_feedback():
    """保存用户反馈"""
    try:
        data = request.json
        feedback = data.get("feedback", "")
        
        if feedback.strip():
            with open("feedback.txt", "a", encoding="utf-8") as f:
                f.write(f"反馈：{feedback}\n")
            return jsonify({"message": "反馈已保存"})
        else:
            return jsonify({"error": "请输入反馈内容"})
            
    except Exception as e:
        return jsonify({"error": f"保存反馈失败: {str(e)}"}), 500

if __name__ == '__main__':
    # 创建templates目录
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("prompts", exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)