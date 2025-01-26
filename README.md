# Autodeployment Chat System

## Overview
The **Autodeployment Chat System** automates the deployment of applications based on natural language input and a code repository. Designed for users with little to no DevOps experience, the system streamlines the provisioning and deployment process, requiring minimal intervention.

---

## Features
- **Natural Language Processing**: Parses deployment requirements from user input.
- **Code Repository Analysis**: Identifies application types, dependencies, and configurations from a given GitHub repository or zip file.
- **Cloud Provisioning**: Utilizes Terraform to dynamically configure and provision VMs for deployment.
- **Automated Deployment**: Updates code settings (e.g., replacing `localhost` with public IPs) and deploys applications.
- **Comprehensive Logs**: Provides detailed logs for each deployment step.

---

## System Requirements
- **Inputs**:
  - A natural language description (e.g., "Deploy this Flask application on AWS").
  - A link to a GitHub repository or a zip file containing the application code.

- **Outputs**:
  - Successfully deployed applications accessible via a VM's public IP.
  - Deployment logs detailing provisioning, deployment, and adjustments.

---

## Setup Instructions
### Prerequisites
1. **Terraform**: Install Terraform from [https://www.terraform.io/downloads.html](https://www.terraform.io/downloads.html).
2. **Cloud Account**: Create an account on a supported cloud provider (e.g., AWS).
3. **Python Environment**: Install Python (version 3.8+).
4. **Dependencies**: Install required Python packages:
   ```bash
   pip install -r requirements.txt
