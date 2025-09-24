FROM python:3.9-slim

RUN pip install --no-cache-dir psycopg2-binary pandas

COPY etl.py /app/etl.py

WORKDIR /app

CMD ["python", "etl.py"]