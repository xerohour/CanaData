import os
import sys

def check_release_blockers():
    ignore_dirs = {
        'tests', 'performance_tests', 'output', '.git', '.roo', '.vscode',
        '__pycache__', '.jules', '.Jules'
    }
    blockers_found = False

    for root, dirs, files in os.walk('.'):
        # Exclude ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            # Skip non-text files or specific extensions if needed, but for now we'll check common ones
            if file.endswith(('.py', '.md', '.txt', '.yml', '.yaml', '.sh')):
                file_path = os.path.join(root, file)

                # Skip this script itself
                if os.path.abspath(file_path) == os.path.abspath(__file__):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if 'TODO' in line or 'FIXME' in line:
                                print(f"{file_path}:{line_num}: {line.strip()}")
                                blockers_found = True
                except UnicodeDecodeError:
                    # Skip binary files or files with unknown encoding
                    pass

    if blockers_found:
        print("\nRelease blockers (TODO/FIXME) found! Please resolve them before releasing.")
        sys.exit(1)
    else:
        print("No release blockers found.")
        sys.exit(0)

if __name__ == "__main__":
    check_release_blockers()
