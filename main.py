# ======================================================================================
# Acknowledgment:
# This code was enhanced with the assistance of OpenAI's ChatGPT,
# a large language model developed by OpenAI. For further information, visit:
# https://openai.com
#
# Author: Weiguo Jiang
# Date: Jan 25 2025
# ======================================================================================


import os
import json
import subprocess
import openai
import requests
import zipfile


# Set OpenAI API key
openai.api_key = "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"


def welcome():
    print("""
    ================================================================================
                    Welcome to AutoDeployment Chat System
    ================================================================================

    This system automates the deployment of applications based on natural 
    language input and a code repository. Whether you're new to DevOps or 
    a seasoned developer, AutoDeploy makes deployment seamless and efficient.

    How it works:
    1. Provide a natural language description of your deployment requirements.
       For example: "Deploy this Flask application on AWS."
    2. Supply a link to your code repository (or upload a zip file of the repo).
    3. Sit back as AutoDeploy:
       - Analyzes your repository to extract necessary details.
       - Dynamically determines the required infrastructure.
       - Provisions resources on a cloud provider (e.g., AWS, Azure, GCP).
       - Deploys your application with minimal intervention.

    ================================================================================
    """)
    return


def download_github_repo(repo_url, save_path="repo.zip"):
    try:
        if not repo_url.endswith(".git"):
            repo_url = repo_url.rstrip("/") + ".git"

        # Extract owner and repository name
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        owner = repo_url.split("/")[-2]

        # Construct the zip download URL
        zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/main.zip"
        print(f"Downloading {repo_name} from {zip_url}...")
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()

        # Save the zip file
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        print(f"Repository downloaded and saved as {save_path}")

        return save_path

    except:
        return None


def user_input():
    deploy_requirements = input("Describe your deployment requirements: ")
    choice = input("Provide a GitHub link/zip file to your repository (1/2): ")
    if choice == "1":
        while True:
            repo = input("Enter the GitHub link: ")
            repo = download_github_repo(repo)
            if repo is None:
                print("Failed to download the repository. Please try again.")
            else:
                break
    else:
        while True:
            repo = input("Provide the relative path to the zip file: ")
            if os.path.exists(repo):
                break
            print("Invalid path. Please try again.")

    return deploy_requirements, repo


def parse_requirements(input_text, repo_content):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a DevOps assistant."},
                    {"role": "user", "content": f"Analyze the following deployment requirement and repository content. "
                                                    f"Provide the application type, dependencies, configurations, "
                                                    f"and necessary VM configuration. Ensure the response is valid JSON and properly formatted. "
                                                    f"Do not include extra comments or explanations, just return a JSON object.\n\n"
                                                    f"Deployment Requirements:\n{input_text}\n\n"
                                                    f"Repository Content:\n{repo_content}"}
                ]
            )
            print()
            print("Analyzed deployment requirements:")
            print(response['choices'][0]['message']['content'])
            print()
            return json.loads(response['choices'][0]['message']['content'])
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            print("Retrying...")


def analyze_repository_with_requirements(path, deploy_requirements):
    combined_content = ""
    with zipfile.ZipFile(path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            try:
                with zip_ref.open(file_name) as f:
                    content = f.read().decode('utf-8')
                    combined_content += f"--- Start of {file_name} ---\n{content}\n--- End of {file_name} ---\n\n"
            except Exception as e:
                print(f"Could not read {file_name}: {e}")

    print("Analyzing the repository content with deployment requirements...")

    return parse_requirements(deploy_requirements, combined_content)


def generate_terraform_config(gpt_response):
    vm_config = gpt_response.get("vm_configuration", {})
    dependencies = gpt_response.get("dependencies", [])
    application_type = gpt_response.get("application_type", "")

    provisioner_commands = [
        "sudo apt update",
        "sudo apt install -y python3-pip" if application_type == "Flask" else "sudo apt install -y nodejs npm",
    ]

    if application_type == "Flask":
        provisioner_commands.append(f"pip3 install {' '.join(dependencies)}")
        provisioner_commands.append("python3 app.py")
    elif application_type == "Node.js":
        provisioner_commands.append("npm install")
        provisioner_commands.append("node app.js")

    # Convert the provisioner commands to a properly formatted string for Terraform
    provisioner_commands_terraform = [f'"{cmd}"' for cmd in provisioner_commands]

    terraform_template = f"""
    provider "aws" {{
      region = "us-east-1"
    }}

    data "aws_ami" "ubuntu" {{
      most_recent = true
      owners      = ["099720109477"] # Canonical's AWS Account ID
      filter {{
        name   = "name"
        values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
      }}
    }}

    resource "aws_instance" "app" {{
      ami           = data.aws_ami.ubuntu.id
      instance_type = "{vm_config.get('type', 't2.micro')}"

      connection {{
        type        = "ssh"
        user        = "ubuntu"
        private_key = file("~/.ssh/id_rsa")
        host        = self.public_ip
      }}

      provisioner "remote-exec" {{
        inline = [{', '.join(provisioner_commands_terraform)}]
      }}
    }}
    """

    with open("main.tf", "w") as f:
        f.write(terraform_template)


def deploy_with_terraform():
    try:
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Terraform execution: {e}")


def main():
    welcome()

    deploy_requirements, repo_path = user_input()

    if repo_path.endswith(".zip"):
        gpt_response = analyze_repository_with_requirements(repo_path, deploy_requirements)
    else:
        print("Unsupported repository format.")
        return

    if gpt_response:
        generate_terraform_config(gpt_response)
        deploy_with_terraform()
    else:
        print("Failed to retrieve deployment requirements from GPT.")


if __name__ == "__main__":
    main()
