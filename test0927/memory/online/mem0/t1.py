# test
# print("I love Python\nI am Devang")

from ai_client import send_ai_request 
from prompt import prompt   # 注意：导入的是实例 prompt
from ai_voiice_clean import clean_content

# 选择提供商和配置文件路径
choose = ["qian-niu-doubao", "D:\\ProgramData\\git\\project\\memory\\online\\mem0\\ai_providers.json"]

# 准备消息
scene = "luoli"  
messages = [
    {"role": "system", "content": prompt.language},   # 语言锁定
    {"role": "system", "content": getattr(prompt.role, scene)},
    {"role": "user",   "content": "Hello!,天空在下雨？我的心也是阴郁的"}
]
# 发送请求

response = send_ai_request(choose,messages)
# 提取 content
# data = response.json()
content = response["choices"][0]["message"]["content"]

# 清除不适合的md格式字符
# print(content)
# content = clean_content(content)
print(content)

content = clean_content(content)
print("\n\n")
print(" 干净："+content)
# print(response)