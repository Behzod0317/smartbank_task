# Smartbank Task

This project demonstrates a Named Entity Recognition (NER) and Text Classification system built using Hugging Face Transformers. The solution includes:

- **NER model**: Fine-tuned BERT model for recognizing named entities (PERSON, ORGANIZATION, LOCATION).
- **Text Classification model**: Fine-tuned BERT model for sentiment analysis or intent classification (depending on what you used).
  
The system is deployed as a REST API using FastAPI. It exposes the following endpoints:

1. `/ner`: Accepts a piece of text and returns the recognized entities and their types.
2. `/classify`: Accepts a piece of text and returns the predicted sentiment or category.

## Requirements

1. Python 3.x
2. Hugging Face transformers
3. FastAPI
4. Docker (for containerization)
5. Kubernetes (optional)

## Instructions

### Training the models:
- Navigate to the `/model_training` directory and run the Jupyter notebooks for model fine-tuning.

### Running the API:
- Build and run the FastAPI server with Docker:

```bash
docker build -t smart-tasks .
docker run -d -p 1050:1050 smart-tasks
