import openai
import os
import requests


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
    prompt = input("Describe your deployment requirements: ")
    choice = input("Provide a GitHub link/zip file to your repository (1/2): ")
    if choice == "1":
        while True:
            repo = input("Enter the GitHub link: ")
            if not download_github_repo(repo):
                print("Failed to download the repository. Please try again.")
    else:
        while True:
            repo = input("Provide the relative path to the zip file: ")
            if os.path.exists(repo):
                break
            print("Invalid path. Please try again.")

    return prompt, repo


if __name__ == "__main__":
    # Greets the user
    welcome()

    # Collects user input
    prompt, repo = user_input()
