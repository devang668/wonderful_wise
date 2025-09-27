# "Authorization": "sk-b49297368cc8899fd297158ed1ea4c245fec5cf23ee2945cea1d8d9d3461e8e4",
# 单一的测试 为了了验证接口是否可用

import requests

url = "https://openai.qiniu.com/v1/chat/completions"
headers = {
    "Authorization": "sk-2e282136ce6bcc5aa2f7b32e6b34811133d0d3f26d39696495a03c217b0dbdb0",
    "Content-Type": "application/json"
}
payload = {
    "stream": False,
    "model": "doubao-1.5-vision-pro",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())

# 提取 content
data = response.json()
content = data["choices"][0]["message"]["content"]
print(content)

# print(response.json())