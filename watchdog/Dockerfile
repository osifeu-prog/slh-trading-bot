FROM python:3.11-slim
RUN pip install requests
COPY watchdog.py /app/watchdog.py
WORKDIR /app
CMD ["python", "watchdog.py"]
