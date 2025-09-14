"""Utility functions used in our graph."""

from typing import Optional, Tuple, List
import os 
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek
# Load environment variables from .env file
load_dotenv()

from langchain_community.chat_models import ChatTongyi
from langchain_openai import AzureChatOpenAI

from langchain_aws import ChatBedrockConverse
from langchain_google_genai import ChatGoogleGenerativeAI
from logger import logger
from langchain_ollama import ChatOllama


def ollama_local(model_name: str = "magistral:24b"):
    llm = ChatOllama(
        model=model_name,
        temperature=0.2,
    )
    logger.info(f"LLM Initiating ollama_local model: {model_name}")
    return llm

def azure_openai():
    # 从环境变量读取配置，如果没有设置则使用默认值
    api_version = os.getenv("OPENAI_API_VERSION", "2024-05-01-preview")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY environment variable is required")
    
    os.environ["OPENAI_API_VERSION"] = api_version
    os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint
    os.environ["AZURE_OPENAI_API_KEY"] = api_key
    
    llm = AzureChatOpenAI(
        model_name="gpt-4o",
        temperature=0.7,
        api_version=api_version,
        azure_endpoint=endpoint,
        azure_deployment="gpt-4o",
        openai_api_version=api_version
    )
    logger.info(f"LLM Initiating azure_openai model")
    return llm

def gemini_openai(model_name: str = 'gemini-2.5-pro-preview-05-06'):
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=1.0,
        max_retries=2,
        api_key=os.environ["GEMINI_API_KEY"] #os.getenv("GEMINI_API_KEY"),
    )
    logger.info(f"LLM Initiating gemini_openai model")
    return llm

def qwen_turbo():
    # 初始化两个模型：一个用于普通对话，一个用于图像
    model_turbo = ChatTongyi(
        #model="qwen-plus",
        model = "qwen-plus",
        streaming=False,
        temperature=0.7
    )
    
    model_vl = ChatTongyi(
        model="qwen-vl-max",
        streaming=False,
        temperature=0.7
    )


    logger.info(f"LLM Initiating qwen_turbo model")
    logger.info(f"LLM Initiating qwen_turbo model")
    return model_turbo, model_vl

def openai_gpt():
    provider = 'openai'
    # 确保使用支持视觉的模型
    model = 'gpt-4o'  
    llm = init_chat_model(model, model_provider=provider,temperature=0.7)
    logger.info(f"LLM Initiating openai_gpt model")
    return llm

def deepseek():
    llm = ChatDeepSeek(
        model="deepseek-chat",
        api_key=os.environ["DEEPSEEK_API_KEY"],
    )
    logger.info(f"LLM Initiating deepseek model")
    return llm


def aws_claude():
    llm = ChatBedrockConverse(
        model=os.environ["AWS_MODEL"],
        region_name = os.environ["AWS_REGION"],
        temperature=0.2,
        max_tokens=None,
        aws_access_key_id=os.environ["AWS_KEYID"],
        aws_secret_access_key=os.environ["AWS_KEY"],
    )
    logger.info(f"LLM Initiating aws_claude model")
    return llm

def init_generation_model():
    # 使用通义千问模型
    #llm = azure_openai()
    #llm = ollama_local_qwen3()
    #llm = ollama_local_llama4("llama4:128x17b")
    #llm = ollama_local_deepseek_tool()
    #llm = ollama_local('gpt-oss:20b')
    llm = deepseek()
    #llm = openai_gpt()
    #llm = aws_claude()
    #llm = gemini_openai()
    #llm = aws_claude()
    #llm, llm_vl = qwen_turbo()
    return llm

def init_reflection_model():
    # 使用通义千问模型
    #llm = azure_openai()
    #llm = ollama_local_qwen3()
    #llm = ollama_local_llama4("llama4:128x17b")
    #llm = ollama_local_deepseek_tool()
    #llm = ollama_local('gpt-oss:20b')
    llm = deepseek()
    #llm = openai_gpt()
    #llm = aws_claude()
    #llm = gemini_openai()
    #llm = aws_claude()
    #llm, llm_vl = qwen_turbo()
    return llm
    
def convert_to_string_list(long_string):
    """
    将长字符串转换为字符串列表，保留所有换行和空行
    
    参数:
        long_string: 包含换行符的长字符串
        
    返回:
        字符串列表，每个元素对应原始字符串中的一行
    """
    # 使用splitlines()方法保留空行
    lines = long_string.splitlines(keepends=True)
    
    # 移除每行末尾的换行符（但保留空行）
    return [line.rstrip('\n') for line in lines]

if __name__ == "__main__":
    llm = init_model()
    print(llm.invoke("你好"))

    




