FROM python:3.9-alpine
WORKDIR /app
RUN pip install pg8000
COPY app.py .
CMD ["python","app.py"]
