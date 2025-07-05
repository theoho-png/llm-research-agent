FROM python:3.9-slim

WORKDIR /app
COPY src/agent /app/agent
COPY tests /app/tests
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "agent.main"]