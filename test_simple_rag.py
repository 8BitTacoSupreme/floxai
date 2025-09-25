#!/usr/bin/env python3
"""
Simple test to check if blog posts are loaded in RAG
"""
import sys
import os
sys.path.insert(0, 'backend')

# Test 1: Check if blog files exist
print("🧪 Testing RAG Blog Loading")
print("=" * 50)

import os
from pathlib import Path

docs_path = Path("data/flox_docs")
print(f"📁 Docs path: {docs_path}")
print(f"📁 Exists: {docs_path.exists()}")

if docs_path.exists():
    md_files = list(docs_path.rglob("*.md"))
    print(f"📄 Total .md files: {len(md_files)}")
    
    blog_files = [f for f in md_files if 'blogs' in str(f)]
    print(f"📰 Blog files: {len(blog_files)}")
    
    for blog_file in blog_files:
        print(f"   - {blog_file.name}")
        if 'build' in blog_file.name.lower() and 'publish' in blog_file.name.lower():
            print(f"     ✅ Found build and publish blog post!")
            
            # Check content
            try:
                with open(blog_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'build' in content.lower() and 'publish' in content.lower():
                        print(f"     ✅ Content contains 'build and publish'")
                        print(f"     📊 Content length: {len(content)} characters")
                    else:
                        print(f"     ❌ Content doesn't contain 'build and publish'")
            except Exception as e:
                print(f"     ❌ Error reading file: {e}")
else:
    print("❌ Docs path doesn't exist")
