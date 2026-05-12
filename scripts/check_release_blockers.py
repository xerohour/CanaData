import sys
import os
import re

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    todo_fixme_pattern = re.compile(r'(TOD' + r'O|FIX' + r'ME)')
    found_issues = []

    # Directories to ignore
    ignore_dirs = {'.git', '__pycache__', '.pytest_cache', 'output', '.venv', 'env', 'venv', 'node_modules', '.roo'}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to exclude ignored directories
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        for filename in filenames:
            if not filename.endswith('.py') and not filename.endswith('.md') and not filename.endswith('.html'):
                 continue
            if filename == 'check_release_blockers.py':
                 continue

            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if todo_fixme_pattern.search(line):
                            found_issues.append((filepath, line_num, line.strip()))
            except Exception as e:
                print(f"Error reading {filepath}: {e}", file=sys.stderr)

    if found_issues:
        print("Release blockers found:")
        for filepath, line_num, line in found_issues:
            rel_path = os.path.relpath(filepath, root_dir)
            print(f"{rel_path}:{line_num}: {line}")
        sys.exit(1)
    else:
        print("No release blockers found.")
        sys.exit(0)

if __name__ == '__main__':
    main()
