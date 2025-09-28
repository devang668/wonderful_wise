#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的本地HTTP服务器启动脚本
用于运行迅飞语音听写项目
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def start_server(port=8000):
    """启动本地HTTP服务器"""
    # 切换到项目目录
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # 创建HTTP服务器
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🚀 服务器已启动!")
            print(f"📁 服务目录: {project_dir}")
            print(f"🌐 访问地址: http://localhost:{port}")
            print(f"🌐 访问地址: http://127.0.0.1:{port}")
            print("=" * 50)
            print("💡 提示:")
            print("   - 在浏览器中打开上述地址即可使用语音听写功能")
            print("   - 按 Ctrl+C 停止服务器")
            print("=" * 50)
            
            # 自动打开浏览器
            try:
                webbrowser.open(f'http://localhost:{port}')
            except:
                print("⚠️  无法自动打开浏览器，请手动访问上述地址")
            
            # 启动服务器
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ 端口 {port} 已被占用，尝试使用端口 {port + 1}")
            start_server(port + 1)
        else:
            print(f"❌ 启动服务器失败: {e}")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        sys.exit(0)

if __name__ == "__main__":
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("❌ 需要 Python 3.6 或更高版本")
        sys.exit(1)
    
    # 检查必要文件
    required_files = ['index.html', 'js/xf-voice-dictation.js', 'js/crypto-js.min.js']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file in missing_files:
            print(f"   - {file}")
        sys.exit(1)
    
    print("🎤 迅飞语音听写项目 - 本地服务器")
    print("=" * 50)
    
    # 启动服务器
    start_server()

