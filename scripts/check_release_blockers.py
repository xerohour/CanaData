import os
import sys

def check_for_release_blockers(directory="."):
    """
    Searches the codebase for TODO or FIXME comments, which are release blockers.
    Ignores common non-code directories.
    """
    blockers_found = False

    ignore_dirs = {'.git', '__pycache__', 'output', 'venv', 'env', '.env', '.pytest_cache'}
    ignore_files = {'check_release_blockers.py'}

    for root, dirs, files in os.walk(directory):
        # Remove directories to ignore
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]

        for file in files:
            if file in ignore_files or file.endswith('.pyc'):
                continue

            filepath = os.path.join(root, file)

            # Skip binary files or unreadable files
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if 'TODO' in line or 'FIXME' in line:
                            print(f"Release blocker found in {filepath} at line {line_num}:")
                            print(f"  {line.strip()}")
                            blockers_found = True
            except UnicodeDecodeError:
                # Likely a binary file, skip it
                pass
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    return blockers_found

if __name__ == "__main__":
    print("Checking for release blockers (TODO/FIXME)...")
    if check_for_release_blockers():
        print("\n❌ Release blocked! Please resolve TODO/FIXME comments before release.")
        sys.exit(1)
    else:
        print("\n✅ No release blockers found. Good to go!")
        sys.exit(0)
