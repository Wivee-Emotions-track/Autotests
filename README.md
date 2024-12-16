# Playwright Dockerized Test Environment

This repository contains a Dockerized test environment using Playwright and Python. It includes all necessary configurations to run your test suite with Allure reporting.

## Features

- Playwright-based testing using the official Playwright image
- Python environment for testing
- Allure integration for detailed test reports
- Lightweight and efficient setup using Docker

## Getting Started

### Prerequisites

- Docker installed on your system

### Building the Docker Image

1. Clone this repository:
   ```bash
   git clone https://github.com/Wivee-Emotions-track/Autotests/
   cd Autotests
   ```
2. Build the Docker image:
   ```bash
   docker build -t autotests .
   ```

### Running the Tests

1. Run the container:

   ```bash
   docker run --rm -v $(pwd)/reports:/reports autotests
   ```

   This command mounts a local `reports` directory to store Allure results.

2. Test results will be available in the `reports/allure-results` directory.

### Running Health Checks

1. Navigate to the `test_healthcheck/` directory in the repository:

   ```bash
   cd test_healthcheck
   ```

2. Run the health check tests using `pytest`:

   ```bash
   pytest
   ```

   or, if using Docker, execute:

   ```bash
   docker run --rm -v $(pwd)/reports:/reports autotests pytest test_healthcheck/
   ```

3. Test results will be saved in the `reports/allure-results` directory if configured.

### Generating Allure Reports

1. Install Allure on your host machine:

   - Follow the instructions from the [Allure Documentation](https://docs.qameta.io/allure/).

2. Generate the report:

   ```bash
   allure serve reports/allure-results
   ```

   This will start a local server to view your test results.

### Modifying the Tests

1. Copy your test files into the `tests/` directory.
2. Rebuild the Docker image to include your changes:
   ```bash
   docker build -t autotests .
   ```

## Environment Variables

- **ENV**: Specifies the environment configuration. Possible values are `prod`, `staging1`, `staging2`, `staging3`.

- **HEALTHCHECK**: Enables or disables health checks. Possible values are `true` or `false`.

- **VAULT_TOKEN**: Await token for vault. Value is valid vault token
  
You can use these variables like -e Docker parameters or define them in a .env file.

## Notes

- The `CMD` in the Dockerfile runs `pytest` with Allure result generation by default.
- Update the `Dockerfile` to include additional dependencies or modify configurations as needed.

