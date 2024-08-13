FROM python:3.12-alpine
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
# Expose the port that the app runs on
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]