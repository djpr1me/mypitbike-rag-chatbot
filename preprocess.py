from pathlib import Path
import re

def clean_content(text):
    # Delete the first header that starts with #
    text = re.sub(r'^# [^\n]*\n', '', text, count=1, flags=re.MULTILINE)

    # Remove the front matter
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    
    # Delete all component imports
    text = re.sub(r'^import\s+.*?;\n', '', text, flags=re.MULTILINE)
    
    # Remove images, JSX components, links and YouTube embeds
    patterns = [
        r'!\[.*?\]\(.*?\)',                      # Markdown images
        r'<img\s+.*?\/?>',                       # MDX images
        r'<[A-Za-z]+(\s+.*?)?>.*?<\/[A-Za-z]+>', # Any JSX components
        r'{%\s*\w+.*?%}',                        # Liquid-tags
        r'@site/src/components/.*',              # Paths to components
        r'\[.*?\]\(.*?\)',                       # Markdown links
        r'<YouTubeEmbed\s+videoId=".*?"\s*\/>',  # YouTube embeds
    ]
    
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL)
    
    # Remove blank lines and unnecessary hyphenation
    text = re.sub(r'\n{3,}', '\n\n', text.strip())
    
    return text

def process_docs():
    processed_dir = Path("processed_docs")
    processed_dir.mkdir(exist_ok=True)
    
    for doc in Path("docs").rglob("*"):
        # Skip index.md and directories
        if doc.name.lower() == "index.md" or doc.is_dir():
            continue
            
        # Process only .md and .mdx files
        if doc.suffix.lower() in ('.md', '.mdx'):
            try:
                # Read and clear
                content = doc.read_text(encoding='utf-8')
                cleaned = clean_content(content)
                
                # Shaping a new path
                relative_path = doc.relative_to("docs")
                new_stem = relative_path.stem
                
                # Change the .mdx extension to .md
                new_path = processed_dir / relative_path.with_name(f"{new_stem}.md")
                
                # Save the folder structure
                new_path.parent.mkdir(parents=True, exist_ok=True)
                
                new_path.write_text(cleaned, encoding='utf-8')
                
                print(f"Processed: {doc} → {new_path}")
                
            except Exception as e:
                print(f"Error processing {doc}: {str(e)}")

if __name__ == "__main__":
    process_docs()