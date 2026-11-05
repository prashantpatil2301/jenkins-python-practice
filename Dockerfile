FROM python:3.13-slim-trixie

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       chromium \
       chromium-driver \
       fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY conftest.py pytest.ini generate_report.py test_selenium_lab.py ./

ENV RUN_IN_DOCKER=true

CMD ["python", "-m", "pytest", "-v", "--junitxml=reports/results.xml"]