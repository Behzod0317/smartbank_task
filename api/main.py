from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from fastapi.responses import JSONResponse
import logging
import sentry_sdk
import uvicorn


sentry_sdk.init(dsn="https://fe9730ef5656d7ec2d0e1c83a5e85558@o4508245833940992.ingest.de.sentry.io/4508245850587216", traces_sample_rate=1.0)


app = FastAPI()


try:
    device = -1  
    ner_model = pipeline("ner", model="Beehzod/smart-finetuned-ner", tokenizer="Beehzod/smart-finetuned-ner", device=device)
    classify_model = pipeline("sentiment-analysis", model="Beehzod/smart_sentiment_analysis", tokenizer="Beehzod/smart_sentiment_analysis", device=device)
except Exception as e:
    logging.error("Error loading models", exc_info=e)
    sentry_sdk.capture_exception(e)
    raise HTTPException(status_code=500, detail="Error loading models")


class TextRequest(BaseModel):
    text: str

# @app.post("/ner")
# async def ner(text_request: TextRequest):
#     text = text_request.text
#     try:
#         entities = ner_model(text)
        
#         merged_entities = []
#         temp_entity = None

#         for entity in entities:
#             if temp_entity and entity["entity"].startswith("I-") and temp_entity["entity"][2:] == entity["entity"][2:]:
#                 temp_entity["word"] += entity["word"].replace("##", "")
#                 temp_entity["end"] = entity["end"]
#                 temp_entity["score"] = min(temp_entity["score"], float(entity["score"]))  # Take minimum score
#             else:
#                 if temp_entity:
#                     merged_entities.append(temp_entity)
#                 temp_entity = {
#                     "entity": entity["entity"],
#                     "score": float(entity["score"]),
#                     "start": entity["start"],
#                     "end": entity["end"],
#                     "word": entity["word"].replace("##", "")
#                 }

#         if temp_entity:
#             merged_entities.append(temp_entity)
        
#         return JSONResponse(content={"entities": merged_entities})
#     except Exception as e:
#         logging.error("NER model error", exc_info=e)
#         sentry_sdk.capture_exception(e)
#         raise HTTPException(status_code=500, detail="Error processing NER request")

@app.post("/ner")
async def ner(text_request: TextRequest):
    text = text_request.text
    try:
        entities = ner_model(text)

        merged_entities = []
        temp_entity = None

        for entity in entities:
            # Check if the current entity is a continuation of the previous (B-PER followed by I-PER)
            if (
                temp_entity 
                and entity["entity"].startswith("I-") 
                and temp_entity["entity"][2:] == entity["entity"][2:]
            ):
                # Add space if it's a continuation and not immediately following
                temp_entity["word"] += " " + entity["word"].replace("##", "")
                temp_entity["end"] = entity["end"]
                temp_entity["score"] = min(temp_entity["score"], float(entity["score"]))  # Take minimum score
            else:
                # If no continuation, append completed entity
                if temp_entity:
                    merged_entities.append(temp_entity)
                # Start a new entity
                temp_entity = {
                    "entity": entity["entity"],
                    "score": float(entity["score"]),
                    "start": entity["start"],
                    "end": entity["end"],
                    "word": entity["word"].replace("##", "")
                }

        # Append any remaining entity
        if temp_entity:
            merged_entities.append(temp_entity)

        return JSONResponse(content={"entities": merged_entities})
    except Exception as e:
        logging.error("NER model error", exc_info=e)
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Error processing NER request")
@app.post("/classify")
async def classify(text_request: TextRequest):
    text = text_request.text
    try:
        prediction = classify_model(text)
        return JSONResponse(content={"classification": prediction})
    except Exception as e:
        logging.error("Classification model error", exc_info=e)
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Error processing classification request")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
