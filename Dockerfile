FROM python:3.11.4-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["uvicorn",\
    "quepid_es_proxy.main:app",\
    "--host", "0.0.0.0",\
    "--port", "5000"\
    ]
