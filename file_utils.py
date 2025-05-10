import os

def save_file(content: str, path: str):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ Saved {path}")
