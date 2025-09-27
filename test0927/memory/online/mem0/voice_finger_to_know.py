
"""
查询七牛云 TTS 音色列表（等价于 curl 命令）
"""
import os
import requests

# 1. 填上你的真实 key
API_KEY = "sk-b49297368cc8899fd297158ed1ea4c245fec5cf23ee2945cea1d8d9d3461e8e4"          # <-- 改成自己的

url = "https://openai.qiniu.com/v1/voice/list"
headers = {"Authorization": f"Bearer {API_KEY}"}

resp = requests.get(url, headers=headers, timeout=10)
resp.raise_for_status()          # 如果返回非 200 会抛异常

voices = resp.json()
# 2. 漂亮打印
# for v in voices:
#     print(f"{v['voice_type']:30} | {v['voice_name']:15} | {v['category']}")


with open("voices.txt", "w", encoding="utf-8") as f:
    for v in voices:
        f.write(f"{v['voice_type']:30} | {v['voice_name']:15} | {v['category']}\n")    