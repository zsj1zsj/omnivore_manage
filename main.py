from omnivoreql import OmnivoreQL

def det(v):
	if v:
		return v
	else:
		return 0

omnivoreql_client = OmnivoreQL("209dc288-b2f6-4b31-aa10-281b7bfb81a9")

def get_all_articles():
    all_articles = []
    has_next_page = True
    end_cursor = 0
    while has_next_page:
        # 使用 end_cursor 获取下一页
        articles = omnivoreql_client.get_articles(after=end_cursor)
        # 添加当前页的文章到总列表
        all_articles.extend([edge['node'] for edge in articles['search']['edges']])
        # 更新分页信息
        page_info = articles['search']['pageInfo']
        has_next_page = page_info['hasNextPage']
        end_cursor = page_info['endCursor']
        print(end_cursor)
    return all_articles

# 获取所有文章
# 获取的articlek可以拿到wordCount，也就是字数，但是这个字数是包含html tag的
all_articles = get_all_articles()
edge_list = all_articles['search']['edges']
filtered_nodes = [edge['node'] for edge in edge_list if det(edge['node']['wordsCount']) > 1000]

# 打印文章总数
print(f"Total articles: {len(all_articles)}")

# 如果你还需要获取每篇文章的详细内容
profile = omnivoreql_client.get_profile()
username = profile['me']['profile']['username']

for node in filtered_nodes:
    slug = node['slug']
    article_detail = omnivoreql_client.get_article(username, slug)
    content = article_detail['article']['article']['content']
    # 这里你可以处理或存储文章内容
    print(f"Article: {node['title']}")
    print(f"Content length: {len(content)}")
    print("---")
