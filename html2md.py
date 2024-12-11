# Last updated: 2024-12-11

import re
import requests
from bs4 import BeautifulSoup
import os



url = 'https://arxiv.org/html/2412.05341v1'

def extract_title_and_summary(section):
    title = section['title'] if 'title' in section else 'Untitled'

    content = section['content'] if 'content' in section else ''
    summary_match = re.search(r'### Summary and Topic:\s*(.+)', content, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else 'No summary found'

    return {
        'title': title,
        'summary': summary
    }

def extract_arxiv(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    sections = []
    current_section = None

    for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
        if element.name in ['h1', 'h2', 'h3']:
            if current_section:
                current_section['content'] = ' '.join(current_section['content'])
                sections.append(current_section)
            title_text = element.get_text(strip=True)
            rematch = re.match(r'^((?:IV|IX|V?I{0,3})(?:\.\d+)?|\d+(?:\.\d+)?)([A-Z].+)$', title_text)
            if rematch:
                _tnum, _text = rematch.groups()
                title_text = f'{_tnum} {_text}'
            else:
                title_text = re.sub(r'(\d)([A-Za-z])', r'\1. \2', title_text)
            
            #print(title_text.strip())
            current_section = {
                'title': title_text.strip(),
                'content': []
            }
        elif element.name == 'p' and current_section:
            paragraph = element.get_text(strip=True)
            if paragraph:
                current_section['content'].append(paragraph)

    if current_section:
        current_section['content'] = ' '.join(current_section['content'])
        sections.append(current_section)

    return sections

def generate_markdown(keyword, related_keywords):
    markdown = f'# {keyword}\n'

    for entry in related_keywords:
        title = entry['title']
        print(title)
        if title[0].isdigit() or title[0] in ['I', 'V', 'X']:
            summary = 'summary' # 임시
            dot_idx = -1
            if '.' in title:
                dot_idx = title.find('.')
            elif '-' in title:
                dot_idx = title.find('-')
            
            # sub-sub-title
            if title[dot_idx+1].isdigit():
                if dot_idx == -1:
                    markdown += f'## {title}\n'
                    markdown += f'### {summary}\n'
                else:
                    markdown += f'### {title}\n'
                    markdown += f'#### {summary}\n'
            # sub-title
            elif title.startswith('I') or title.startswith('V') or title.startswith('X'):
                markdown += f'## {title}\n'
                markdown += f'### {summary}\n'
            else:
                markdown += f'## {title}\n'
                markdown += f'### {summary}\n'

    print(markdown)

    extract_md(markdown)

def extract_md(md_text, name='./output.md'):
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name, 'w', encoding='utf-8') as file:
        file.write(md_text)



sections = extract_arxiv(url)

title_and_summaries = []
for section in sections:
    section['content'] = 'summary' # 임시
    title_and_summary = extract_title_and_summary(section)
    title_and_summaries.append(title_and_summary)

generate_markdown('Main Keyword', title_and_summaries)
