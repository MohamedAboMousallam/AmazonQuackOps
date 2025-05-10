import argparse
from config import * 
from prompt import prompt_interactive
from generate import generate_file
# CLI entry point
def main():
    parser = argparse.ArgumentParser(description='DevOps config generator via Amazon Q')
    parser.add_argument('type', nargs='?', choices=CONFIG.keys(), help='Type to generate')
    parser.add_argument('-o','--options', default='', help='Extra prompt options')
    parser.add_argument('--prompt', help='Custom prompt override')
    parser.add_argument('--files', '-f', nargs='+', help='Custom output filenames')
    parser.add_argument('--multi-stage', action='store_true')
    parser.add_argument('--interactive', '-i', action='store_true')
    args = parser.parse_args()

    if args.interactive:
        if args.type or args.files or args.options or args.prompt or args.multi_stage:
            parser.error("--interactive cannot be combined with other arguments")
        ftype, files, opts, multi, custom = prompt_interactive()
    else:
        if not args.type:
            parser.error("Specify a type or use --interactive")
        ftype = args.type
        files = args.files if args.files else CONFIG[ftype]['files']
        opts, multi, custom = args.options, args.multi_stage, args.prompt

    generate_file(ftype, files, opts, multi, custom)

if __name__ == '__main__':
    main()