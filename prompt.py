from config import CONFIG

def prompt_interactive() -> tuple[str,list[str],str,bool,str]:
    print("🚀 Welcome to the interactive DevOps generator!")
    types = list(CONFIG.keys())
    for i, t in enumerate(types, 1):
        print(f"  {i}. {t}")
    choice = int(input("Select a config type by number: ")) - 1
    ftype = types[choice]
    custom = input(f"Enter custom prompt (or leave blank for default): ") or None
    multi = input("Use multi-stage mode? (y/N): ").strip().lower() == 'y'
    opts = input("Extra prompt options? (or leave blank): ")
    file_input = input(f"Output filenames (space-separated) or blank for {CONFIG[ftype]['files']}: ")
    files = file_input.split() if file_input.strip() else CONFIG[ftype]['files']
    return ftype, files, opts, multi, custom
