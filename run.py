#!/usr/bin/env python3
"""
LangGraph 提示词管理工具启动脚本
"""

import os
import sys
import subprocess

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import flask
        print("✓ Flask 已安装")
        return True
    except ImportError:
        print("✗ Flask 未安装")
        return False

def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("✗ 依赖安装失败")
        return False

def create_directories():
    """创建必要的目录"""
    directories = ["templates", "static", "prompts"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ 目录 {directory} 已创建")

def main():
    """主函数"""
    print("=" * 50)
    print("LangGraph 提示词管理工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        print("\n正在安装依赖...")
        if not install_dependencies():
            print("请手动运行: pip install -r requirements.txt")
            return
    
    # 创建目录
    print("\n创建必要目录...")
    create_directories()
    
    # 启动应用
    print("\n启动Web服务器...")
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    main()
