import subprocess
from file_utils import save_file
from parser_utils import clean_q_output, extract_blocks
from config import CONFIG
try:
    import yaml
except ImportError:
    yaml = None

try:
    import hcl2
    HCL2_LOADED = True
except ImportError:
    HCL2_LOADED = False

def query_amazon_q_cli(prompt: str) -> str:
    proc = subprocess.Popen(['echo', prompt], stdout=subprocess.PIPE)
    result = subprocess.run(
        ['q', 'chat', '--trust-all-tools'],
        stdin=proc.stdout,
        capture_output=True,
        text=True
    )
    proc.stdout.close()
    return result.stdout

def generate_file(ftype: str, files: list[str], options: str, multi_stage: bool, custom_prompt: str = None):
    base_prompt = custom_prompt or CONFIG[ftype]['prompt']
    if not multi_stage:
        prompt = base_prompt + ". Respond only with file contents, no explanation or fences." + (f" {options}" if options else "")
        raw = query_amazon_q_cli(prompt)
        blocks = extract_blocks(raw, files, ftype)
    # Interactive multi-stage with accept/regenerate/abort/edit-prompt
    else:
        # Stage 1: Plan
        plan_prompt = f"Plan files/structure to {base_prompt.lower()}"
        while True:
            print("🧠 Stage 1: Planning with prompt:" + plan_prompt)
            plan = query_amazon_q_cli(plan_prompt)
            plan_clean = clean_q_output(plan)
            print(plan_clean)
            choice = input("Accept plan? (y)es/(r)egenerate/(e)dit prompt/(a)bort: ").strip().lower()
            if choice == 'y':
                # user accepted plan, break to generation stage
                break
            elif choice == 'r':
                # regenerate using the same plan_prompt
                continue
            elif choice == 'e':
                # allow user to edit prompt, then re-run planning loop
                plan_prompt = input("Enter new planning prompt: ")
                continue
            elif choice == 'a':
                print("Aborted by user.")
                return
            else:
                print("Invalid choice. Enter 'y', 'r', 'e', or 'a'.")
                continue
        # Stage 2: Generate each file after plan accepted
        blocks = {}
        for fname in files:
            file_prompt = f"Write full contents of {fname} for: {base_prompt.lower()}. Only content."
            while True:
                print(f"🛠 Stage 2: Generating {fname} with prompt:" + file_prompt)
                out = query_amazon_q_cli(file_prompt)
                content = clean_q_output(out)
                print(content)
                c2 = input(f"Accept {fname}? (y)es/(r)egenerate/(e)dit prompt/(a)bort: ").strip().lower()
                if c2 == 'y':
                    blocks[fname] = content
                    break
                elif c2 == 'r':
                    continue
                elif c2 == 'e':
                    # edit file generation prompt and retry
                    file_prompt = input(f"Enter new file-generation prompt for {fname}: ")
                    continue
                elif c2 == 'a':
                    print("Aborted by user.")
                    return
                else:
                    print("Invalid choice. Enter 'y', 'r', 'e', or 'a'.")
                    continue

    if not blocks:
        save_file(clean_q_output(raw, ftype), f"{ftype}.txt")
        return
    for fname, code in blocks.items():
        if ftype == 'terraform' and HCL2_LOADED:
            try:
                parsed = hcl2.loads(code)
                code = hcl2.dumps(parsed)
            except:
                pass
        if ftype in ['kubernetes','ansible','github-actions'] and yaml:
            try:
                data = yaml.safe_load(code)
                code = yaml.safe_dump(data, sort_keys=False)
            except:
                pass
        save_file(code, fname)
