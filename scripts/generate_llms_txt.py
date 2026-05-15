import os
import re

LLMS_TXT_PATH = "public/llms.txt"
KNOWLEDGE_DIR = "src/pages/knowledge"

def get_articles():
    articles = []
    for f in os.listdir(KNOWLEDGE_DIR):
        if not f.endswith('.md'):
            continue
        filepath = os.path.join(KNOWLEDGE_DIR, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
        if match:
            slug = f.replace('.md', '')
            articles.append({
                'title': match.group(1),
                'url': f"https://alexmerceddata.com/knowledge/{slug}"
            })
    return sorted(articles, key=lambda x: x['title'])

def update_llms_txt():
    articles = get_articles()
    
    with open(LLMS_TXT_PATH, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Find if we already have a section
    marker = "## Knowledge Base Index:"
    
    if marker in content:
        base_content = content.split(marker)[0]
    else:
        base_content = content + "\n\n"
        
    new_content = base_content + marker + "\n"
    for article in articles:
        new_content += f"- [{article['title']}]({article['url']})\n"
        
    with open(LLMS_TXT_PATH, 'w', encoding='utf-8') as file:
        file.write(new_content)
        
if __name__ == "__main__":
    update_llms_txt()
