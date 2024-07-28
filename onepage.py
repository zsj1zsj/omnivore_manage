from omnivoreql import OmnivoreQL
import re
from chatgpt import DeepSeekAPI

def remove_html_tags(text):
    # 使用正则表达式移除HTML标签
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def det(v):
    """返回输入值或0（如果输入值为空）"""
    return v if v else 0

def get_first_article_content(api_key):
    """获取第一篇满足要求的文章并输出文章内容"""
    omnivoreql_client = OmnivoreQL(api_key)
    all_articles = omnivoreql_client.get_articles()
    edge_list = all_articles['search']['edges']
    
    # 过滤出字数超过1000的文章
    filtered_nodes = [edge['node'] for edge in edge_list if det(edge['node']['wordsCount']) > 1000]
    if not filtered_nodes:
        return None
    
    # 获取第一篇满足条件的文章
    node = filtered_nodes[0]
    slug = node['slug']
    
    profile = omnivoreql_client.get_profile()
    username = profile['me']['profile']['username']
    
    # 获取文章详情并移除HTML标签
    article_detail = omnivoreql_client.get_article(username, slug)
    content = remove_html_tags(article_detail['article']['article']['content'])
    
    return content


if __name__ == '__main__':
    api_key = "209dc288-b2f6-4b31-aa10-281b7bfb81a9"
    content = get_first_article_content(api_key)
    
    deepseek = DeepSeekAPI('sk-7c51b68ff66243d1945effc882b65885')
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"用中文总结文本：{content}"}
    ]
    
    if content:
        response = deepseek.create_chat_completion(
            model="deepseek-chat",  # 替换为DeepSeek模型ID
            messages=messages
        )
        print(response)
    else:
        print("没有找到符合条件的文章。")

