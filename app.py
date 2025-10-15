from operator import ge
from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import datetime
from state import Graph_State
from graph import generation_graph_flow_v1
from utils import convert_to_string_list
from logger import logger

app = Flask(__name__)

# 默认提示词模板
DEFAULT_PROMPTS = {
    "generation_prompt": "请根据以下内容生成详细的回答：\n\n{user_input}",
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

            generate_prompt = data.get("generation_prompt", DEFAULT_PROMPTS["generation_prompt"])
            full_generate_prompt = "\n".join(generate_prompt)
            reflection_prompt = data.get("reflection_prompt", DEFAULT_PROMPTS["reflection_prompt"])
            full_reflection_prompt = "\n".join(reflection_prompt)
            user_prompt = data.get("user_prompt", DEFAULT_PROMPTS["user_prompt"])
            full_user_prompt = "\n".join(user_prompt)
                        
            prompts = {
                "generation_prompt": full_generate_prompt,
                "reflection_prompt": full_reflection_prompt,
                "user_prompt": full_user_prompt
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
        language = data.get("language", "zh")

        # 转换成长字符串列表
        # 这里将generate_prompt/reflection_prompt/user_prompt都从data中获取
        generate_prompt = data.get("generation_prompt", "")
        reflection_prompt = data.get("reflection_prompt", "")
        user_prompt = data.get("user_prompt", "")
        generate_string_list = convert_to_string_list(generate_prompt)
        reflection_string_list = convert_to_string_list(reflection_prompt)
        user_string_list = convert_to_string_list(user_prompt)

        prompts_data = {
            "generation_prompt": generate_string_list,
            "reflection_prompt": reflection_string_list,
            "user_prompt": user_string_list
        }
                
        # 生成文件名（包含时间戳）
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prompts/prompts_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(prompts_data, f, ensure_ascii=False, indent=2)
        
        messages = {
            "zh": f"提示词已保存到: {filename}",
            "en": f"Prompts saved to: {filename}"
        }
        return jsonify({"message": messages.get(language, messages["zh"])})
        
    except Exception as e:
        error_messages = {
            "zh": f"保存失败: {str(e)}",
            "en": f"Save failed: {str(e)}"
        }
        return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 500

@app.route('/generate_content', methods=['POST'])
def generate_content():
    """生成内容（模拟LangGraph的生成和反思过程）"""
    try:
        data = request.json
        generation_prompt = data.get("generation_prompt", "")
        reflection_prompt = data.get("reflection_prompt", "")
        user_prompt = data.get("user_prompt", "")
        
        logger.info(f"Generate content request - user_prompt: {user_prompt[:100]}...")
        logger.info(f"Generation prompt length: {len(generation_prompt)}")
        logger.info(f"Reflection prompt length: {len(reflection_prompt)}")
        
        if not user_prompt.strip():
            logger.warning("Empty user prompt provided")
            return jsonify({"error": "请输入用户提示词"})
        
        # 构造初始 state
        content = data.get("content", "")
        logger.info(f"last run generation content: {content}")
        reflect_advice = data.get("reflect_advice", "")
        state = {
            "generation_prompt": generation_prompt,
            "reflection_prompt": reflection_prompt,
            "user_prompt": user_prompt,
            "user_advice": data.get("feedback", ""),
            "content": content,
            "reflecton_advice": reflect_advice,
            "reflect_count": 0
        }

        logger.info("Starting graph execution...")
        # 调用异步 graph
        import asyncio
        result_state = asyncio.run(generation_graph_flow_v1.ainvoke(state))
        generated_text = result_state.get("content", "")
        reflect_advice = result_state.get("reflecton_advice", "")
        
        logger.info(f"Graph execution completed. Generated text length: {len(generated_text)}")
        logger.info(f"Final reflect_count: {result_state.get('reflect_count', 0)}")

        # INSERT_YOUR_CODE
        import json
        import re

        def save_json_to_excel(json_data, excel_filename):
            import pandas as pd
            # 只处理字典或包含"sections"的结构
            if isinstance(json_data, dict) and "sections" in json_data:
                df = pd.DataFrame(json_data["sections"])
            elif isinstance(json_data, list):
                df = pd.DataFrame(json_data)
            else:
                df = pd.DataFrame([json_data])
            df.to_excel(excel_filename, index=False)

        def extract_json_from_text(text):
            """从文本中提取JSON内容，处理markdown代码块等情况"""
            # 移除markdown代码块标记
            text = text.strip()
            
            # 尝试移除 ```json 和 ``` 标记
            if text.startswith('```json'):
                text = text[7:]  # 移除 ```json
            elif text.startswith('```'):
                text = text[3:]  # 移除 ```
            
            if text.endswith('```'):
                text = text[:-3]  # 移除结尾的 ```
            
            text = text.strip()
            
            # 尝试查找JSON对象或数组
            # 查找第一个 { 或 [ 和最后一个 } 或 ]
            start_brace = text.find('{')
            start_bracket = text.find('[')
            
            # 确定起始位置
            if start_brace == -1 and start_bracket == -1:
                return text
            elif start_brace == -1:
                start_pos = start_bracket
                end_char = ']'
            elif start_bracket == -1:
                start_pos = start_brace
                end_char = '}'
            else:
                start_pos = min(start_brace, start_bracket)
                end_char = '}' if start_pos == start_brace else ']'
            
            # 从后往前查找对应的结束字符
            end_pos = text.rfind(end_char)
            
            if end_pos != -1 and end_pos > start_pos:
                text = text[start_pos:end_pos+1]
            
            return text

        # 检查generated_text是否为json格式
        try:
            logger.info(f"Generated text preview (first 200 chars): {generated_text[:200]}")
            
            # 提取JSON内容
            cleaned_text = extract_json_from_text(generated_text)
            logger.info(f"Cleaned text preview (first 200 chars): {cleaned_text[:200]}")
            
            parsed_json = json.loads(cleaned_text)
            
            # 生成文件名（包含时间戳）
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_filename = f"generated_content_{timestamp}.xlsx"
            save_json_to_excel(parsed_json, excel_filename)
            logger.info(f"Generated content saved to Excel: {excel_filename}")
        except json.JSONDecodeError as e:
            logger.warning(f"Generated text is not valid JSON: {e}")
            logger.warning(f"JSON error at position {e.pos}: {generated_text[max(0, e.pos-50):min(len(generated_text), e.pos+50)]}")
        except Exception as e:
            logger.warning(f"Failed to save as Excel: {e}", exc_info=True)
        
        #final_content = f"{generated_text}\n\n---反思结果---#{reflect_advice}"
        
        return jsonify({"content": generated_text, "reflect_advice": reflect_advice})
        
    except Exception as e:
        logger.error(f"Generate content failed: {str(e)}", exc_info=True)
        return jsonify({"error": f"生成内容失败: {str(e)}"}), 500

@app.route('/save_content', methods=['POST'])
def save_content():
    """保存生成的内容到文件"""
    try:
        data = request.json
        content = data.get("content", "")
        language = data.get("language", "zh")
        
        if content.strip():
            # 生成文件名（包含时间戳）
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_content_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messages = {
                "zh": f"内容已保存到: {filename}",
                "en": f"Content saved to: {filename}"
            }
            return jsonify({"message": messages.get(language, messages["zh"])})
        else:
            error_messages = {
                "zh": "没有内容可保存",
                "en": "No content to save"
            }
            return jsonify({"error": error_messages.get(language, error_messages["zh"])})
            
    except Exception as e:
        error_messages = {
            "zh": f"保存内容失败: {str(e)}",
            "en": f"Save content failed: {str(e)}"
        }
        return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 500

@app.route('/load_content', methods=['POST'])
def load_content():
    """从文件加载内容"""
    try:
        language = request.form.get("language", "zh")
        
        if 'file' not in request.files:
            error_messages = {
                "zh": "没有选择文件",
                "en": "No file selected"
            }
            return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 400
        
        file = request.files['file']
        if file.filename == '':
            error_messages = {
                "zh": "没有选择文件",
                "en": "No file selected"
            }
            return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 400
        
        if file and file.filename.endswith('.txt'):
            content = file.read().decode('utf-8')
            return jsonify({"content": content})
        else:
            error_messages = {
                "zh": "请选择TXT文件",
                "en": "Please select a TXT file"
            }
            return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 400
            
    except Exception as e:
        error_messages = {
            "zh": f"加载内容失败: {str(e)}",
            "en": f"Load content failed: {str(e)}"
        }
        return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 500

@app.route('/save_advice', methods=['POST'])
def save_advice():
    """保存Graph反思建议和用户建议"""
    try:
        data = request.json
        reflect_advice = data.get("reflect_advice", "")
        user_advice = data.get("user_advice", "")
        language = data.get("language", "zh")
        
        if not reflect_advice.strip() and not user_advice.strip():
            error_messages = {
                "zh": "没有建议可保存",
                "en": "No advice to save"
            }
            return jsonify({"error": error_messages.get(language, error_messages["zh"])})
        
        # 生成文件名（包含时间戳）
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"advice_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            if reflect_advice.strip():
                f.write("=== Graph反思建议 ===\n")
                f.write(reflect_advice)
                f.write("\n\n")
            
            if user_advice.strip():
                f.write("=== 用户建议 ===\n")
                f.write(user_advice)
                f.write("\n")
        
        messages = {
            "zh": f"建议已保存到: {filename}",
            "en": f"Advice saved to: {filename}"
        }
        return jsonify({"message": messages.get(language, messages["zh"])})
        
    except Exception as e:
        error_messages = {
            "zh": f"保存建议失败: {str(e)}",
            "en": f"Save advice failed: {str(e)}"
        }
        return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 500

@app.route('/load_advice', methods=['POST'])
def load_advice():
    """从文件加载建议"""
    try:
        language = request.form.get("language", "zh")
        
        if 'file' not in request.files:
            error_messages = {
                "zh": "没有选择文件",
                "en": "No file selected"
            }
            return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 400
        
        file = request.files['file']
        if file.filename == '':
            error_messages = {
                "zh": "没有选择文件",
                "en": "No file selected"
            }
            return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 400
        
        if file and file.filename.endswith('.txt'):
            content = file.read().decode('utf-8')
            
            # 解析文件内容，分离Graph反思建议和用户建议
            reflect_advice = ""
            user_advice = ""
            
            if "=== Graph反思建议 ===" in content:
                parts = content.split("=== Graph反思建议 ===")
                if len(parts) > 1:
                    remaining = parts[1]
                    if "=== 用户建议 ===" in remaining:
                        reflect_advice = remaining.split("=== 用户建议 ===")[0].strip()
                        user_advice = remaining.split("=== 用户建议 ===")[1].strip()
                    else:
                        reflect_advice = remaining.strip()
            elif "=== 用户建议 ===" in content:
                parts = content.split("=== 用户建议 ===")
                if len(parts) > 1:
                    user_advice = parts[1].strip()
            
            return jsonify({
                "reflect_advice": reflect_advice,
                "user_advice": user_advice
            })
        else:
            error_messages = {
                "zh": "请选择TXT文件",
                "en": "Please select a TXT file"
            }
            return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 400
            
    except Exception as e:
        error_messages = {
            "zh": f"加载建议失败: {str(e)}",
            "en": f"Load advice failed: {str(e)}"
        }
        return jsonify({"error": error_messages.get(language, error_messages["zh"])}), 500


if __name__ == '__main__':
    # 创建templates目录
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("prompts", exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)