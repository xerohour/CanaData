import os
import re
import sys

def check_release_blockers(directory="."):
    """
    Scans the repository for TO-DO or FIX-ME comments that are marked as release blockers.
    """
    # Create pattern from strings to avoid self-match
    t_str = "TODO"
    f_str = "FIXME"
    blocker_pattern = re.compile(rf'({t_str}|{f_str}).*(blocker|release)', re.IGNORECASE)
    general_pattern = re.compile(rf'({t_str}|{f_str})')

    found_blockers = False

    for root, dirs, files in os.walk(directory):
        # Skip hidden directories like .git, .github, .roo, etc.
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        # Skip __pycache__
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')

        for file in files:
            # Only check source files and documentation, ignore binaries or .pyc
            if file.endswith(('.py', '.md', '.txt', '.html')) and not file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if blocker_pattern.search(line) and file_path != "./.roo/commands/release.md":
                                print(f"Release blocker found in {file_path}:{line_num}")
                                print(f"  {line.strip()}")
                                found_blockers = True
                            elif general_pattern.search(line) and file_path != "./.roo/commands/release.md":
                                print(f"Warning: {t_str}/{f_str} found in {file_path}:{line_num}")
                except Exception as e:
                    pass

    if found_blockers:
        print("ERROR: Release blockers found. Cannot proceed with release.")
        sys.exit(1)
    else:
        print("SUCCESS: No release blockers found.")
        sys.exit(0)

if __name__ == "__main__":
    check_release_blockers()
