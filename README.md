## DevOps Config Generator via Amazon Q CLI

A command-line tool to generate DevOps configuration files (Dockerfiles, Terraform, Kubernetes manifests, Ansible playbooks, GitHub Actions workflows, etc.) using Amazon Q's AI-powered chat interface. Outputs are cleaned, split into files, and formatted automatically.

---

### Features

* **Multi-format support**: Generate Dockerfiles, Terraform `.tf` files, Kubernetes YAML, Ansible playbooks, GitHub Actions workflows, and more.
* **ANSI cleanup**: Strips ANSI escape sequences and extraneous help text.
* **Auto-splitting**: Splits multi-file responses into separate files based on markers or filenames.
* **HCL & YAML formatting**: Optionally parse and re-dump HCL2 and YAML for consistent formatting.
* **Interactive mode**: Guided prompts for selecting config type, filenames, and custom options.
---

### Prerequisites

* Python 3.8+ installed
* Amazon Q CLI (`q`) installed and configured with `q chat`
* Optional Python packages for enhanced formatting:

  * `PyYAML` (for YAML parsing)
  * `hcl2` (for HCL2 parsing)

---

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-repo/devops-config-generator.git
   cd devops-config-generator
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Amazon Q CLI is available:

   ```bash
   q chat --help
   ```

---

### Configuration

All prompts and default output filenames are defined in `config.py`:

```python
CONFIG = {
  'dockerfile': {
    'prompt': 'Generate a Dockerfile to ...',
    'files': ['Dockerfile']
  },
  'terraform': { ... },
  # other types...
}
```

You can override prompts and filenames via CLI flags.

---

### Usage

#### Basic

Generate a Dockerfile with defaults:

```bash
python main.py dockerfile
```

#### Custom options

Add extra instructions to the prompt:

```bash
python main.py dockerfile -o "Use Alpine Linux and include curl"
```

Specify custom output filenames:

```bash
python main.py terraform --files main.tf variables.tf
```

#### Prompt Override

Completely overwrite the default prompt using `--prompt`:

````bash
python main.py dockerfile --prompt "Generate a minimal Dockerfile using Debian slim"
```bash
python main.py terraform --files main.tf variables.tf
````

#### Interactive mode

Run guided prompts:

```bash
python main.py --interactive
```

---

### Multi-stage Mode

You can use **multi-stage** mode to break generation into planning and execution phases. In planning phase, you'll review the AI's proposed steps before generating files. you can either edit the plan, accept it as it is, or abort it

1. **Plan**: Run with `--multi-stage` to get a step-by-step plan.

   ```bash
   python main.py dockerfile --multi-stage
   ```
2. **Execute**: After reviewing the plan, re-run without `--multi-stage` to generate files:

   ```bash
   python main.py dockerfile
   ```
---

### How It Works

1. **Prompt**: Constructs a base prompt (from `config.py` or custom) and sends it to Amazon Q via `q chat`.
2. **Cleaning**: Strips ANSI codes and filters out UI artifacts.
3. **Splitting**: Uses regex and file markers to split combined output into separate files.
4. **Formatting**: Optionally re-parses HCL2 or YAML for pretty output.
5. **Saving**: Writes each block to its target filename, creating directories as needed.

For more explainations. checkout the detailed Blog post at: 
