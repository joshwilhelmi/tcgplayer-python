#!/usr/bin/env python3
"""
Markdown Lint Fixer

Automatically fixes common markdownlint issues:
- MD013: Line length (break long lines)
- MD026: Remove trailing punctuation from headings
- MD034: Wrap bare URLs in angle brackets
"""

import re
import sys
from pathlib import Path
from typing import List


def fix_line_length(content: str, max_length: int = 80) -> str:
    """Fix MD013: Break long lines."""
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        if len(line) > max_length and not line.strip().startswith("```"):
            # Try to break at natural points
            words = line.split()
            current_line = ""
            broken_lines = []

            for word in words:
                if len(current_line + " " + word) <= max_length:
                    current_line += (" " + word) if current_line else word
                else:
                    if current_line:
                        broken_lines.append(current_line)
                    current_line = word

            if current_line:
                broken_lines.append(current_line)

            fixed_lines.extend(broken_lines)
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_heading_punctuation(content: str) -> str:
    """Fix MD026: Remove trailing punctuation from headings."""
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        # Check if this is a heading
        if re.match(r"^#{1,6}\s+", line):
            # Remove trailing punctuation (:, ., !, ?)
            line = re.sub(r"[:.!?]+$", "", line)
        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_bare_urls(content: str) -> str:
    """Fix MD034: Wrap bare URLs in angle brackets."""
    # Pattern to match bare URLs (http/https)
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'

    def wrap_url(match):
        url = match.group(0)
        # Don't wrap if already wrapped or if it's in a code block
        if url.startswith("<") and url.endswith(">"):
            return url
        return f"<{url}>"

    return re.sub(url_pattern, wrap_url, content)


def fix_markdown_file(file_path: Path) -> None:
    """Fix all markdown issues in a file."""
    print(f"Fixing {file_path}...")

    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        # Apply fixes
        content = fix_heading_punctuation(content)
        content = fix_bare_urls(content)
        content = fix_line_length(content)

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            print(f"✅ Fixed {file_path}")
        else:
            print(f"✅ No changes needed for {file_path}")

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")


def main():
    """Main function."""
    if len(sys.argv) > 1:
        files = [Path(f) for f in sys.argv[1:]]
    else:
        # Default to all markdown files in the project
        files = list(Path(".").rglob("*.md"))
        # Filter out venv and other directories
        files = [
            f for f in files if "venv" not in str(f) and "node_modules" not in str(f)
        ]

    print(f"🔧 Fixing {len(files)} markdown files...")
    print()

    for file_path in files:
        if file_path.is_file():
            fix_markdown_file(file_path)

    print()
    print("🎉 Markdown fixing complete!")
    print("Run 'make markdown' to check remaining issues.")


if __name__ == "__main__":
    main()
