from tools.github_deploy import GitHubDeployer

def generate_and_deploy_tool(tool_name, template_file, token):
    generated_code = generate_python_code(tool_name, template_file)
    with open(f"{tool_name}.py", "w") as py_file:
        py_file.write(generated_code)
    deploy_tool_to_github(tool_name, generated_code, token)

def generate_python_code(tool_name, template_file):
    with open(template_file, "r") as tmpl:
        code_tmpl = tmpl.read()
    generated_code = code_tmpl.format(tool_name=tool_name)
    return generated_code

def deploy_tool_to_github(tool_name, code_content, token):
    deployer = GitHubDeployer(token)
    deployer.push_file("cybersecurity-toolkit", f"src/{tool_name}.py", code_content, f"Deploy {tool_name}")
    print(f"{tool_name} deployed to GitHub.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python master_controller.py <tool_name> <template_file> [token]")
        sys.exit(1)
    tool_name = sys.argv[1]
    template_file_path = sys.argv[2]
    token = sys.argv[3] if len(sys.argv) > 3 else input("GitHub token: ")
    generate_and_deploy_tool(tool_name, template_file_path, token)

