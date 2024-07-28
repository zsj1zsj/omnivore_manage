import requests

class DeepSeekAPI:
    def __init__(self, api_key, base_url='https://api.deepseek.com'):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

    def create_chat_completion(self, model, messages):
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()


if __name__ == '__main__':
    # 替换为你的DeepSeek API密钥和基础URL
    api_key = 'sk-7c51b68ff66243d1945effc882b65885'
    base_url = 'https://api.deepseek.com'

    # 创建DeepSeekAPI实例
    deepseek = DeepSeekAPI(api_key, base_url)

    # 设置请求消息
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "是鸡生蛋还是蛋生鸡？"}
    ]

    # 调用API
    response = deepseek.create_chat_completion(
        model="deepseek-chat",  # 替换为DeepSeek模型ID
        messages=messages
    )

    # 打印响应数据
    print(response)
