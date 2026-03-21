"""
Markdown Processor Skill

Parse, convert, and process Markdown and HTML documents.
"""
import json
import logging
import os
import re
import sys
from typing import Any, Dict, List, Optional

import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """Extract YAML frontmatter from markdown."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                import yaml
                frontmatter = yaml.safe_load(parts[1]) or {}
                return frontmatter, parts[2].strip()
            except:
                pass
    return {}, content


def extract_headings(content: str) -> List[Dict[str, Any]]:
    """Extract headings with levels."""
    headings = []
    for match in re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE):
        headings.append({"level": len(match.group(1)), "text": match.group(2).strip()})
    return headings


def extract_code_blocks(content: str) -> List[Dict[str, str]]:
    """Extract code blocks with language."""
    blocks = []
    pattern = r'```(\w*)\n(.*?)```'
    for match in re.finditer(pattern, content, re.DOTALL):
        blocks.append({"language": match.group(1), "code": match.group(2).strip()})
    return blocks


def generate_toc(headings: List[Dict[str, Any]]) -> str:
    """Generate table of contents from headings."""
    toc = ["## Table of Contents\n"]
    for h in headings:
        indent = "  " * (h["level"] - 1)
        anchor = h["text"].lower().replace(" ", "-").replace("[", "").replace("]", "")
        toc.append(f'{indent}- [{h["text"]}](#{anchor})')
    return "\n".join(toc)


def md_to_html(md_content: str) -> str:
    """Simple markdown to HTML conversion."""
    html = md_content
    
    # Headers
    for i in range(6, 0, -1):
        pattern = r'^' + '#' * i + r'\s+(.+)$'
        html = re.sub(pattern, rf'<h{i}>\1</h{i}>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
    
    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
    
    # Code blocks
    html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Lists
    html = re.sub(r'^\s*-\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\g<0></ul>', html)
    
    # Paragraphs
    html = re.sub(r'\n\n+', '</p><p>', html)
    html = '<p>' + html + '</p>'
    
    return html


def html_to_md(html_content: str) -> str:
    """Simple HTML to markdown conversion."""
    md = html_content
    
    # Headers
    for i in range(1, 7):
        md = re.sub(rf'<h{i}[^>]*>(.+?)</h{i}>', r'{"#" * i}\1', md)
    
    # Code
    md = re.sub(r'<pre><code class="language-(\w*)">(.*?)</code></pre>', r'```\1\n\2```', md, flags=re.DOTALL)
    md = re.sub(r'<code>(.+?)</code>', r'`\1`', md)
    
    # Links
    md = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r'[\2](\1)', md)
    
    # Bold/Italic
    md = re.sub(r'<strong>(.+?)</strong>', r'**\1**', md)
    md = re.sub(r'<em>(.+?)</em>', r'*\1*', md)
    
    # Clean up
    md = re.sub(r'<[^>]+>', '', md)
    
    return md


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for skill invocation."""
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()
    
    action = payload.get("action", "parse")
    file_path = payload.get("file_path")
    content = payload.get("content")
    output_path = payload.get("output_path")
    
    try:
        # Get content from file if provided
        if content is None and file_path:
            if not os.path.exists(file_path):
                return {"result": {"error": f"File not found: {file_path}"}, "metadata": {"timestamp": timestamp}}
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        if not content:
            return {"result": {"error": "content or file_path required"}, "metadata": {"timestamp": timestamp}}
        
        if action == "parse":
            frontmatter, body = extract_frontmatter(content)
            headings = extract_headings(body)
            code_blocks = extract_code_blocks(body)
            
            result = {
                "frontmatter": frontmatter,
                "headings": headings,
                "code_blocks": code_blocks,
                "word_count": len(body.split()),
                "has_frontmatter": bool(frontmatter)
            }
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                result["output_file"] = output_path
            
            return {"result": result, "metadata": {"timestamp": timestamp}}
        
        elif action == "extract_frontmatter":
            frontmatter, _ = extract_frontmatter(content)
            return {"result": {"frontmatter": frontmatter}, "metadata": {"timestamp": timestamp}}
        
        elif action == "extract_headings":
            _, body = extract_frontmatter(content)
            headings = extract_headings(body)
            return {"result": {"headings": headings}, "metadata": {"timestamp": timestamp}}
        
        elif action == "extract_code":
            _, body = extract_frontmatter(content)
            code_blocks = extract_code_blocks(body)
            return {"result": {"code_blocks": code_blocks}, "metadata": {"timestamp": timestamp}}
        
        elif action == "generate_toc":
            _, body = extract_frontmatter(content)
            headings = extract_headings(body)
            toc = generate_toc(headings)
            return {"result": {"toc": toc}, "metadata": {"timestamp": timestamp}}
        
        elif action == "convert_to_html":
            html = md_to_html(content)
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                return {"result": {"html": html, "output_file": output_path}, "metadata": {"timestamp": timestamp}}
            return {"result": {"html": html}, "metadata": {"timestamp": timestamp}}
        
        elif action == "convert_to_markdown":
            md = html_to_md(content)
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(md)
                return {"result": {"markdown": md, "output_file": output_path}, "metadata": {"timestamp": timestamp}}
            return {"result": {"markdown": md}, "metadata": {"timestamp": timestamp}}
        
        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"timestamp": timestamp}}
    
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"timestamp": timestamp, "error": str(e)}}


def register_skill():
    return {"name": "markdown-processor", "description": "Parse, convert, and process Markdown and HTML documents", "version": "1.0.0", "domain": "DATA_FORMAT_HANDLING"}
