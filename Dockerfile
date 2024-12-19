# Use the official Playwright image from the Docker Hub
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install Python dependencies directly
RUN pip install --no-cache-dir \
    aspose-words==23.12.0 \
    attrdict==2.0.1 \
    Faker==5.0.1 \
    gmaily==0.0.3 \
    jsonpath-ng==1.6.0 \
    jsonpickle==2.0.0 \
    pylint==3.0.3 \
    pytest-order==1.2.0 \
    pytest-rerunfailures==12.0 \
    pytest-xdist==3.5.0 \
    pytest_check==2.2.2 \
    pytest==6.2.5 \
    python-dotenv==1.0.0 \
    request-boost==0.8 \
    requests==2.31.0 \
    requests-toolbelt==1.0.0 \
    wrapt \
    deepdiff \
    antigate \
    playwright \
    pyyaml \
    trcli \
    elasticsearch \
    pyperclip \
    allure-pytest \
    psycopg2-binary \
    opencv-python \
    pytest-xdist

# Copy the application code
COPY . .

# Make the directory for Allure results accessible
VOLUME ["/reports/allure-results"]

# Define the command to run your tests and generate Allure results
CMD ["sh", "-c", "pytest -n ${THREADS_COUNT:-1} --alluredir=/reports/allure-results"]
