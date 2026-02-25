import os
from pathlib import Path

def get_size(path):
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_size(entry.path)
            except Exception:
                pass
    except Exception:
        pass
    return total

def analyze_repo(root_path):
    root = Path(root_path)
    file_sizes = []
    dir_sizes = {}

    print(f"Scanning {root}...")

    # Scan top-level directories
    for entry in os.scandir(root):
        if entry.name == '.git':
            dir_sizes[entry.name] = get_size(entry.path)
            continue
            
        if entry.is_dir(follow_symlinks=False):
            size = get_size(entry.path)
            dir_sizes[entry.name] = size
        elif entry.is_file():
            file_sizes.append((entry.path, entry.stat().st_size))

    # Scan for largest files recursively (top 20)
    print("\nScanning for largest files recursively...")
    large_files = []
    for root_dir, dirs, files in os.walk(root):
        if '.git' in dirs:
            dirs.remove('.git')
        
        for name in files:
            try:
                path = os.path.join(root_dir, name)
                size = os.path.getsize(path)
                large_files.append((path, size))
            except Exception:
                pass
    
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    print("\n=== Top 10 Directories by Size ===")
    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)[:10]
    for name, size in sorted_dirs:
        print(f"{name}: {size / (1024**3):.2f} GB")

    print("\n=== Top 20 Largest Files ===")
    for path, size in large_files[:20]:
        print(f"{path}: {size / (1024**2):.2f} MB")

if __name__ == "__main__":
    analyze_repo(".")
