import re

CONFIG = {
    'dockerfile':    { 'prompt': 'Generate a simple generic Dockerfile template for a containerized application. Include comments explaining each instruction. Do not assume a specific language or framework.', 'files': ['Dockerfile'] },
    'terraform':     { 'prompt': 'Generate a simple generic Terraform configuration template to provision AWS infrastructure. Do not include specific services. Use placeholders and comments for customization.', 'files': ['main.tf', 'variables.tf', 'outputs.tf'] },
    'kubernetes':    { 'prompt': 'Generate a simple Kubernetes deployment template. Use placeholders for container images, names, and ports. Include comments to explain each section.', 'files': ['k8s-configurations.yaml'] },
    'ansible':       { 'prompt': 'Generate a simple generic Ansible playbook template to configure a server. Do not assume specific roles or packages. Use placeholder tasks and comments.', 'files': ['playbook.yml'] },
    'github-actions':{ 'prompt': 'Generate a simple GitHub Actions CI/CD workflow template with placeholder steps. Do not assume a specific language or framework. Include comments to guide customization.', 'files': ['.github/workflows/ci-cd.yml'] }
}

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
