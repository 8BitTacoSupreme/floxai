#!/usr/bin/env python3
"""
Flox Blog Ingestion Script
Downloads and processes all Flox blog posts for the knowledge base
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
import re

# Add backend to path
sys.path.insert(0, 'backend')

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    
    return text.strip()

def extract_blog_posts():
    """Extract blog post URLs and metadata from the main blog page"""
    print("🔍 Extracting blog post URLs from Flox blog...")
    
    try:
        response = requests.get('https://flox.dev/blog/', timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        posts = []
        
        # Look for blog post links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/blog/' in href and href != '/blog/':
                # Extract title
                title = link.get_text(strip=True)
                if title and len(title) > 10:  # Filter out short/empty titles
                    posts.append({
                        'url': f"https://flox.dev{href}" if href.startswith('/') else href,
                        'title': title,
                        'date': None  # Will extract from individual posts
                    })
        
        # Remove duplicates
        seen_urls = set()
        unique_posts = []
        for post in posts:
            if post['url'] not in seen_urls:
                seen_urls.add(post['url'])
                unique_posts.append(post)
        
        print(f"✅ Found {len(unique_posts)} blog posts")
        return unique_posts
        
    except Exception as e:
        print(f"❌ Error extracting blog posts: {e}")
        return []

def download_blog_post(post_url, title):
    """Download and parse a single blog post"""
    try:
        print(f"📄 Downloading: {title}")
        response = requests.get(post_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract content
        content = ""
        
        # Try to find main content area
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if main_content:
            # Remove script and style elements
            for script in main_content(["script", "style"]):
                script.decompose()
            
            content = main_content.get_text(separator='\n', strip=True)
        else:
            # Fallback: get all text
            content = soup.get_text(separator='\n', strip=True)
        
        # Clean content
        content = clean_text(content)
        
        # Extract date if possible
        date = None
        date_elements = soup.find_all(['time', 'span'], class_=re.compile(r'date|time'))
        for elem in date_elements:
            date_text = elem.get_text(strip=True)
            if re.match(r'\d{1,2}\s+\w+\s+\d{4}', date_text):
                date = date_text
                break
        
        # Extract tags/categories
        tags = []
        tag_elements = soup.find_all(['a', 'span'], class_=re.compile(r'tag|category'))
        for elem in tag_elements:
            tag_text = elem.get_text(strip=True)
            if tag_text and len(tag_text) < 50:  # Reasonable tag length
                tags.append(tag_text)
        
        return {
            'url': post_url,
            'title': title,
            'content': content,
            'date': date,
            'tags': tags,
            'word_count': len(content.split())
        }
        
    except Exception as e:
        print(f"❌ Error downloading {post_url}: {e}")
        return None

def save_blog_post(post_data, output_dir):
    """Save blog post to markdown file"""
    if not post_data:
        return
    
    # Create safe filename
    safe_title = re.sub(r'[^\w\s-]', '', post_data['title'])
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    filename = f"{safe_title[:50]}.md"
    filepath = output_dir / filename
    
    # Create markdown content
    markdown_content = f"""# {post_data['title']}

**URL:** {post_data['url']}
**Date:** {post_data['date'] or 'Unknown'}
**Tags:** {', '.join(post_data['tags']) if post_data['tags'] else 'None'}
**Word Count:** {post_data['word_count']}

---

{post_data['content']}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"💾 Saved: {filename}")

def main():
    """Main ingestion process"""
    print("🚀 Starting Flox Blog Ingestion")
    print("=" * 50)
    
    # Create output directory
    output_dir = Path('data/flox_docs/blogs')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract blog post URLs
    posts = extract_blog_posts()
    if not posts:
        print("❌ No blog posts found")
        return
    
    print(f"\n📚 Processing {len(posts)} blog posts...")
    
    # Download and process each post
    successful = 0
    for i, post in enumerate(posts, 1):
        print(f"\n[{i}/{len(posts)}] Processing: {post['title']}")
        
        post_data = download_blog_post(post['url'], post['title'])
        if post_data:
            save_blog_post(post_data, output_dir)
            successful += 1
        
        # Be respectful to the server
        time.sleep(1)
    
    print(f"\n✅ Ingestion complete!")
    print(f"   📄 Successfully processed: {successful}/{len(posts)} posts")
    print(f"   📁 Saved to: {output_dir}")
    
    # Create index file
    index_file = output_dir / "README.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(f"""# Flox Blog Posts

This directory contains {successful} blog posts from the Flox blog (https://flox.dev/blog/).

## Posts Included

""")
        for post in posts:
            f.write(f"- [{post['title']}]({post['url']})\n")
    
    print(f"📋 Created index: {index_file}")

if __name__ == "__main__":
    main()
