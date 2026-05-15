import os
import re

KNOWLEDGE_DIR = "src/pages/knowledge"

def get_slug(filename):
    return filename.replace('.md', '')

def extract_title_and_body(content):
    # match frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return None, None, content
    frontmatter = match.group(1)
    body = match.group(2)
    
    title_match = re.search(r'^title:\s*"(.*?)"', frontmatter, re.MULTILINE)
    title = title_match.group(1) if title_match else None
    return frontmatter, title, body

def process_file(filepath, articles):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    frontmatter, title, body = extract_title_and_body(content)
    if not frontmatter or not title:
        return False
        
    original_body = body
    
    # Sort articles by length of title descending, to match longer terms first
    sorted_articles = sorted(articles, key=lambda x: len(x['title']), reverse=True)
    
    for article in sorted_articles:
        if article['title'] == title:
            continue # Don't link to itself
            
        term = article['title']
        slug = article['slug']
        
        # We only want to replace the FIRST occurrence in normal paragraph text.
        # Split by codeblocks
        parts = re.split(r'(```.*?```)', body, flags=re.DOTALL)
        
        new_parts = []
        replaced = False
        
        for part in parts:
            if part.startswith('```') or replaced:
                new_parts.append(part)
                continue
                
            # Process part line by line
            lines = part.split('\n')
            new_lines = []
            for line in lines:
                if replaced or line.startswith('#'):
                    new_lines.append(line)
                    continue
                
                # Check if term is in line. Avoid replacing inside existing links [term](url)
                # or [text containing term](url)
                # A simple negative lookbehind/lookahead for brackets
                pattern = r'(?<!\[)\b' + re.escape(term) + r'\b(?!\])(?![^\[]*\])'
                if re.search(pattern, line):
                    line = re.sub(pattern, f'[{term}](/knowledge/{slug})', line, count=1)
                    replaced = True
                new_lines.append(line)
            new_parts.append('\n'.join(new_lines))
            
        body = "".join(new_parts)

    if body != original_body:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"---\n{frontmatter}\n---\n{body}")
        return True
    return False

def main():
    files = [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith('.md')]
    articles = []
    
    # First pass: collect titles and slugs
    for f in files:
        filepath = os.path.join(KNOWLEDGE_DIR, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        _, title, _ = extract_title_and_body(content)
        if title:
            articles.append({
                'title': title,
                'slug': get_slug(f)
            })
            
    print(f"Loaded {len(articles)} articles for cross-linking.")
    
    PILLAR_ALIASES = {
        "data-lakehouse": ["Data Lakehouse", "Data Lakehouses", "data lakehouse"],
        "apache-iceberg": ["Apache Iceberg", "apache iceberg"],
        "agentic-lakehouse": ["Agentic Lakehouse", "Agentic Analytics", "agentic lakehouse"],
        "apache-iceberg-architecture": ["Apache Iceberg Architecture", "Iceberg Architecture", "Iceberg architecture"],
        "apache-iceberg-vs-delta-lake-vs-hudi": ["Apache Iceberg vs Delta Lake vs Apache Hudi", "Iceberg vs Delta", "Iceberg vs Hudi", "Delta Lake vs Iceberg", "Hudi vs Iceberg"],
        "data-lakehouse-vs-data-lake-vs-data-warehouse": ["Data Lakehouse vs Data Lake vs Data Warehouse", "Lakehouse vs Data Warehouse"]
    }
    
    for slug, aliases in PILLAR_ALIASES.items():
        for alias in aliases:
            articles.append({
                'title': alias,
                'slug': slug
            })
    
    # Second pass: cross-link
    updated_count = 0
    for f in files:
        filepath = os.path.join(KNOWLEDGE_DIR, f)
        if process_file(filepath, articles):
            updated_count += 1
            
    print(f"Updated {updated_count} files with cross-links.")

if __name__ == "__main__":
    main()
