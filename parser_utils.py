import re
from config import ANSI_ESCAPE
try:
    import yaml
except ImportError:
    yaml = None

try:
    import hcl2
    HCL2_LOADED = True
except ImportError:
    HCL2_LOADED = False

def remove_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub('', text)

def pretty_format_yaml(text: str) -> str:
    try:
        data = yaml.safe_load(text)
        return yaml.dump(data, sort_keys=False, default_flow_style=False)
    except yaml.YAMLError as e:
        print(f"[!] YAML parsing error during formatting: {e}")
        return text 

def clean_q_output(text: str, ftype: str = None) -> str:
    cleaned = remove_ansi(text)
    lines = cleaned.splitlines()
    # Determine start markers per file type
    if ftype == 'dockerfile':
        markers = [r'^\s*FROM\b']
    elif ftype == 'terraform':
        markers = [r'^\s*(resource|provider|terraform)\b']
    elif ftype == 'kubernetes':
        markers = [r'^\s*(apiVersion|kind|---)\b']
    elif ftype == 'ansible':
        markers = [r'^\s*-\s+name:\s+']
    elif ftype == 'github-actions':
        markers = [r'^\s*name:\s+']
    elif ftype == 'hcl2':
        markers = [r'^\s*(resource|provider|terraform)\b']
    else:
        markers = [r'^\S']

    # Find the start of relevant output
    start = 0
    for i, line in enumerate(lines):
        if any(re.match(p, line) for p in markers):
            start = i
            break

    trimmed = lines[start:]

    # Remove noise (diff markers, formatting characters, help lines)
    filtered = [
        l for l in trimmed
        if not re.match(r'^[━─]+$', l)
        and 'help all commands' not in l.lower()
        and not re.match(r'^\s*[+\-]\s+\d+:', l)
        and not l.strip().startswith(('🛠️', '⋮', '●'))
    ]

    # Replace common bullets with dashes
    result = [l.replace('•', '-').replace('–', '-') for l in filtered]
    body = "\n".join(result).strip()

    if ftype in ['kubernetes', 'ansible', 'github-actions'] and yaml:
        return pretty_format_yaml(body)
    return body

def extract_blocks(text: str, files: list[str], ftype: str) -> dict:
    clean = clean_q_output(text, ftype)
    blocks = {}

    if ftype in ['kubernetes', 'ansible', 'github-actions'] and yaml:
        try:
            docs = list(yaml.safe_load_all(clean))
            for i, doc in enumerate(docs):
                if isinstance(doc, dict):
                    fname = files[min(i, len(files) - 1)]
                    blocks[fname] = yaml.safe_dump(doc, sort_keys=False)
        except Exception as e:
            print(f"[!] Failed to parse YAML for {ftype}: {e}")
            blocks[files[0]] = clean 
        return blocks
    # HCL2 (Terraform)
    if ftype == 'terraform' and HCL2_LOADED:
        try:
            parsed = hcl2.loads(clean)
            blocks[files[0]] = hcl2.dumps(parsed)
            return blocks
        except Exception as e:
            print(f"[!] Failed to parse HCL for {ftype}: {e}")

    # Fallback for non-structured file types
    if len(files) > 1:
        docs = re.split(r'\n---+\n', clean)
        for i, doc in enumerate(docs):
            if i < len(files):
                blocks[files[i]] = doc.strip()
    else:
        blocks[files[0]] = clean

    return blocks