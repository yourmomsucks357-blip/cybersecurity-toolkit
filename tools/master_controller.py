from tools.github_deploy import GitHubDeployer

def generate_code(tool_name, code_template_file):
    with open(code_template_file, "r") as file:
        code_template = file.read()
    generated_code = code_template.format(tool_name=tool_name)
    return generated_code

def compile_and_deploy_code(tool_name, generated_code, deployer):
    deployer.push_file("cybersecurity-toolkit", f"src/{tool_name}.py", generated_code, f"Deploy {tool_name}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python master_controller.py <tool_name> <code_template_file>")
        sys.exit(1)
    tool_name = sys.argv[1]
    code_template_file_path = sys.argv[2]
    token = sys.argv[3] if len(sys.argv) > 3 else input("GitHub token: ")
    deployer = GitHubDeployer(token)
    generated_code = generate_code(tool_name, code_template_file_path)
    compile_and_deploy_code(tool_name, generated_code, deployer)
    print(f"{tool_name} deployed.")

