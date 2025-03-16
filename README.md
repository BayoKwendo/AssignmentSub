## Project Setup and Installation


**DynamoDB**: We use a single table for storing client data, leveraging partition and sort keys to segregate data for each client.

**Lambda**: Handles the onboarding logic, including processing input, creating client records, and handling errors.
**API Gateway**: Exposes an HTTP endpoint for triggering the Lambda function.

Below are the instructions to get the project up and running.
---

## Prerequisites

Make sure you have the following tools installed on your machine:

- **AWS SAM CLI**.

## Deployment Instructions
- Clone the repository and navigate to the project directory.
- Run

    ```bash
    sam build
    sam deploy

The output will provide the API endpoint URL. Test it by sending a POST request with client data.
