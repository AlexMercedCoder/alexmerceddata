import json
import os
import time
import requests
from pathlib import Path

# Configure paths
PROJECT_ROOT = Path(__file__).parent.parent
TERMS_FILE = PROJECT_ROOT / "scripts" / "terms.json"
OUTPUT_DIR = PROJECT_ROOT / "src" / "pages" / "knowledge"

# Make sure output dir exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuration for Local Ollama
# Ensure Ollama is running (e.g. `ollama serve`) and you have the model pulled (`ollama pull mistral`)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral" # You can change this to "llama3" or "phi3" if you prefer

def generate_markdown_content(term_data):
    term = term_data["term"]
    category = term_data["category"]
    keywords = ", ".join(term_data["keywords"])
    
    prompt = f"""
    You are an expert technical author, developer advocate, and Data/AI thought leader.
    Your task is to write a highly authoritative, deep-dive, 2000+ word article on the topic: "{term}".
    
    Context:
    - Category: {category}
    - Required Keywords: {keywords}
    
    Requirements:
    1. The output MUST be strictly valid Markdown.
    2. Do NOT include the YAML frontmatter. Start directly with the H2 (##) introduction.
    3. Use a professional, vendor-neutral tone but demonstrate deep expert knowledge. Include underlying architecture details, performance trade-offs, and real-world implementation strategies.
    4. Use structured headings (H2, H3, H4), bullet points, and code blocks where applicable to break up the text.
    
    Do not include any pleasantries or conversational filler. Output only the raw Markdown content.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 4096
        }
    }

    print(f"Generating content for: {term} via Local Ollama ({OLLAMA_MODEL})...")
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code != 200:
            print(f"Failed to generate {term}: {response.text}")
            return None
            
        response_json = response.json()
        return response_json.get("response", "")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Make sure Ollama is installed and running (run 'ollama serve' in another terminal).")
        exit(1)
    except Exception as e:
        print(f"Error parsing response for {term}: {e}")
        return None

def process_terms():
    with open(TERMS_FILE, "r") as f:
        terms = json.load(f)

    print(f"Loaded {len(terms)} terms from {TERMS_FILE}")

    for idx, term_data in enumerate(terms):
        term = term_data["term"]
        filename = term.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "-") + ".md"
        filepath = OUTPUT_DIR / filename

        if filepath.exists():
            print(f"[{idx+1}/{len(terms)}] Skipping {term} - File already exists.")
            continue

        markdown_body = generate_markdown_content(term_data)
        
        if not markdown_body:
            print(f"Skipping {term} due to generation error.")
            continue
            
        # Clean up any potential markdown code blocks wrapped around the response
        if markdown_body.startswith("```markdown"):
            markdown_body = markdown_body[11:]
        if markdown_body.startswith("```"):
            markdown_body = markdown_body[3:]
        if markdown_body.endswith("```"):
            markdown_body = markdown_body[:-3]
            
        markdown_body = markdown_body.strip()

        # Construct frontmatter
        import datetime
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
        frontmatter = f"""---
layout: '../../layouts/KnowledgeLayout.astro'
title: "{term}: The Definitive Guide"
description: "A comprehensive deep dive into {term}, covering architecture, concepts, and real-world usage in {category}."
date: "{date_str}"
tags: {json.dumps(term_data['keywords'])}
cta_link: "{term_data['target_cta']}"
---

"""
        full_content = frontmatter + markdown_body

        with open(filepath, "w") as f:
            f.write(full_content)

        print(f"[{idx+1}/{len(terms)}] Successfully saved {filename}")

if __name__ == "__main__":
    process_terms()
    print("Batch processing complete!")
