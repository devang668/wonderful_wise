#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音对话系统启动脚本
同时启动前端静态服务器和后端Flask服务器
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def start_frontend_server(port=8000):
    """启动前端静态服务器"""
    try:
        print(f"🚀 启动前端服务器 (端口 {port})...")
        subprocess.run([
            sys.executable, '-m', 'http.server', str(port)
        ], cwd=Path(__file__).parent, check=True)
    except KeyboardInterrupt:
        print("\n👋 前端服务器已停止")
    except Exception as e:
        print(f"❌ 前端服务器启动失败: {e}")

def start_backend_server(port=5000):
    """启动后端Flask服务器"""
    try:
        print(f"🚀 启动后端服务器 (端口 {port})...")
        backend_dir = Path(__file__).parent / 'code'
        os.chdir(backend_dir)
        
        # 设置环境变量
        env = os.environ.copy()
        env['FLASK_APP'] = 'app_fixed.py'
        env['FLASK_ENV'] = 'development'
        
        subprocess.run([
            sys.executable, 'app_fixed.py'
        ], check=True, env=env)
    except KeyboardInterrupt:
        print("\n👋 后端服务器已停止")
    except Exception as e:
        print(f"❌ 后端服务器启动失败: {e}")

def main():
    print("🎤 AI语音对话系统启动器")
    print("=" * 50)
    
    # 检查必要文件
    required_files = [
        'voice-chat.html',
        'code/app_fixed.py',
        'js/xf-voice-dictation.js',
        'js/crypto-js.min.js'
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        print("❌ 缺少必要文件:")
        for file in missing_files:
            print(f"   - {file}")
        sys.exit(1)
    
    print("✅ 文件检查完成")
    print()
    
    # 启动后端服务器（在单独线程中）
    backend_thread = threading.Thread(target=start_backend_server, daemon=True)
    backend_thread.start()
    
    # 等待后端服务器启动
    print("⏳ 等待后端服务器启动...")
    time.sleep(3)
    
    # 启动前端服务器
    try:
        print("🌐 访问地址:")
        print(f"   - 语音对话: http://localhost:8000/voice-chat.html")
        print(f"   - 文本聊天: http://localhost:8000/index.html")
        print("=" * 50)
        print("💡 提示:")
        print("   - 语音对话需要麦克风权限")
        print("   - 按 Ctrl+C 停止所有服务器")
        print("=" * 50)
        
        # 自动打开浏览器
        try:
            webbrowser.open('http://localhost:8000/voice-chat.html')
        except:
            print("⚠️  无法自动打开浏览器，请手动访问上述地址")
        
        # 启动前端服务器（主线程）
        start_frontend_server()
        
    except KeyboardInterrupt:
        print("\n👋 所有服务器已停止")
        sys.exit(0)

if __name__ == "__main__":
    main()
