# Autodeployment Chat System

## Acknowledgements
- [ChatGPT](https://chatgpt.com/)
- [OpenAI Platform](https://platform.openai.com/docs/overview)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Terraform Documentation](https://www.terraform.io/docs/index.html)
- [Stack Overflow](https://stackoverflow.com/)

There is extensive use of AI assistance in this project, including code generation with GitHub Copilot and
language generation with ChatGPT. The project is a proof of concept and may require further development to
be fully functional.

## Overview
The **Autodeployment Chat System** automates the deployment of applications based on natural language input and a code repository. Designed for users with little to no DevOps experience, the system streamlines the provisioning and deployment process, requiring minimal intervention.

---

## Features
- **Natural Language Processing**: Parses deployment requirements from user input.
- **Code Repository Analysis**: Identifies application types, dependencies, and configurations from a given GitHub repository or zip file.
- **Cloud Provisioning**: Utilizes Terraform to dynamically configure and provision VMs for deployment.
- **Automated Deployment**: Not able to implement it in time.
- **Comprehensive Logs**: Provides detailed logs for each deployment step.

---

## Expected Workflow
- **Inputs**:
  - A natural language description (e.g., "Deploy this Flask application on AWS").
  - A link to a GitHub repository or a zip file containing the application code.

- **Outcome**:
  - Understand the deployment requirements. (somewhat achieved)
  - Deploy the application on a cloud provider (e.g., AWS). (not achieved)

## TODOs:
- Implement automated deployment.
- Improve natural language processing.
- Enhance cloud provisioning capabilities.
- Add support for additional cloud providers.
- Implement a user-friendly interface.
