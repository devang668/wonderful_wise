import json
import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
prompt = "The default response is the language spoken by the user, unless they explicitly request the use of a certain language. " \
"Violating this rule will result in punishment for the violation"

def send_ai_request(choose, messages, stream=False):
    """
    发送请求到指定的AI提供商
    
    参数:
        choose: 包含提供商名称和配置文件路径的列表，格式如["provider_name", "config_path"]
        messages: 消息列表，格式如[{"role": "user", "content": "Hello"}]
        stream: 是否流式返回，默认为False
    
    返回:
        API响应的JSON数据
    """
    provider_name, config_path = choose
    
    # 加载配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        return f"加载配置文件失败: {str(e)}"
    
    # 获取指定提供商的配置
    provider_config = config.get('providers', {}).get(provider_name)
    if not provider_config:
        return f"未找到提供商配置: {provider_name}"
    
    # 构建请求头，替换API密钥
    headers = {}
    for key, value in provider_config.get('headers', {}).items():
        headers[key] = value.replace('{api_key}', provider_config.get('api_key', ''))
    
    # 构建请求体
    payload = {
        "stream": stream,
        "model": provider_config.get('default_model'),
        "messages": messages
    }
    
    # 发送请求
    try:
        response = requests.post(
            url=provider_config.get('url'),
            json=payload,
            headers=headers
        )
        response.raise_for_status()  # 抛出HTTP错误
        return response.json()
    except Exception as e:
        return f"请求失败: {str(e)}"

