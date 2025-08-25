#!/usr/bin/env python3
"""
Markdown Lint Fixer

Automatically fixes common markdownlint issues:
- MD022: Add blank lines around headings
- MD032: Add blank lines around lists
- MD031: Add blank lines around code blocks
- MD040: Add language to code blocks
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def fix_heading_spacing(content: str) -> str:
    """Fix MD022: Add blank lines around headings."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        fixed_lines.append(line)

        # If this is a heading, ensure blank lines around it
        if re.match(r"^#{1,6}\s+", line):
            # Add blank line above if not at start and previous line isn't blank
            if i > 0 and lines[i - 1].strip() != "":
                fixed_lines.insert(-1, "")

            # Add blank line below if not at end and next line isn't blank
            if i < len(lines) - 1 and lines[i + 1].strip() != "":
                fixed_lines.append("")

    return "\n".join(fixed_lines)


def fix_list_spacing(content: str) -> str:
    """Fix MD032: Add blank lines around lists."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        fixed_lines.append(line)

        # If this is a list item, ensure blank lines around it
        if re.match(r"^[\s]*[-*+]\s+", line) or re.match(r"^[\s]*\d+\.\s+", line):
            # Add blank line above if not at start and previous line isn't blank
            if (
                i > 0
                and lines[i - 1].strip() != ""
                and not re.match(r"^[\s]*[-*+]\s+", lines[i - 1])
                and not re.match(r"^[\s]*\d+\.\s+", lines[i - 1])
            ):
                fixed_lines.insert(-1, "")

            # Add blank line below if not at end and next line isn't blank and isn't a list item
            if (
                i < len(lines) - 1
                and lines[i + 1].strip() != ""
                and not re.match(r"^[\s]*[-*+]\s+", lines[i + 1])
                and not re.match(r"^[\s]*\d+\.\s+", lines[i + 1])
            ):
                fixed_lines.append("")

    return "\n".join(fixed_lines)


def fix_code_block_spacing(content: str) -> str:
    """Fix MD031: Add blank lines around code blocks."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        fixed_lines.append(line)

        # If this is a code block fence, ensure blank lines around it
        if line.strip().startswith("```"):
            # Add blank line above if not at start and previous line isn't blank
            if i > 0 and lines[i - 1].strip() != "":
                fixed_lines.insert(-1, "")

            # Add blank line below if not at end and next line isn't blank
            if i < len(lines) - 1 and lines[i + 1].strip() != "":
                fixed_lines.append("")

    return "\n".join(fixed_lines)


def fix_code_block_language(content: str) -> str:
    """Fix MD040: Add language to code blocks."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        if line.strip() == "```" and i < len(lines) - 1:
            # Check if next line is not a language specifier
            next_line = lines[i + 1].strip()
            if (
                next_line
                and not re.match(r"^[a-zA-Z0-9+#]+$", next_line)
                and not next_line.startswith("```")
            ):
                # Add a generic language specifier
                fixed_lines.append("```text")
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


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


def fix_markdown_file(file_path: Path) -> None:
    """Fix all markdown issues in a file."""
    print(f"Fixing {file_path}...")

    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        # Apply fixes
        content = fix_heading_spacing(content)
        content = fix_list_spacing(content)
        content = fix_code_block_spacing(content)
        content = fix_code_block_language(content)
        # content = fix_line_length(content)  # Commented out as it can be aggressive

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
    print("Run 'markdownlint *.md' to check remaining issues.")


if __name__ == "__main__":
    main()
