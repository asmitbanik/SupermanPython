FROM python:3.11-slim
WORKDIR /app
COPY backend/ /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV HOST=0.0.0.0 PORT=5000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
