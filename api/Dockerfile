FROM python:3.10

COPY requirements.txt .

COPY smart_sentiment_pipeline.pkl .

COPY smart-finetuned-ner.pkl .

COPY main.py .

RUN pip install -r requirements.txt

EXPOSE 1050

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1050"]


# FROM python:3.10

# # Set working directory
# WORKDIR /app

# # Copy dependencies and application files
# COPY requirements.txt .
# COPY smart_sentiment_pipeline.pkl .
# COPY smart-finetuned-ner.pkl .
# COPY main.py .

# # Install dependencies
# RUN pip install -r requirements.txt

# # Expose the application port
# EXPOSE 1050

# # Start the application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1050"]
