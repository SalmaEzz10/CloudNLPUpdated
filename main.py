from fastapi import FastAPI, Response
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from mangum import Mangum
from preprocess import preprocessing
import json

SAVED_MODEL_DIR = "./arabertNER_Model"

tokenizer = AutoTokenizer.from_pretrained(SAVED_MODEL_DIR)
model = AutoModelForTokenClassification.from_pretrained(SAVED_MODEL_DIR)
model.eval()

ENTITIES = [
    "CITY", "AREA", "MINI_AREA", "NUM_STREET", "MAIN_STREET",
    "STREET", "LANDMARK", "BUILDING", "FLOOR", "APARTMENT"
]


def predict_address(address: str) -> dict:
    inputs = tokenizer(
        address,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predictions = torch.argmax(outputs.logits, dim=2)[0].tolist()
    word_ids = inputs.word_ids()

    word_label_map = {}
    for idx, word_id in enumerate(word_ids):
        if word_id is None:
            continue
        if word_id not in word_label_map:
            word_label_map[word_id] = predictions[idx]

    original_words = address.split()

    extracted = {}
    current_entity = None

    for word_id in sorted(word_label_map.keys()):
        if word_id >= len(original_words):
            continue

        label_id = word_label_map[word_id]
        label = model.config.id2label[label_id]
        word_text = original_words[word_id]

        if label.startswith("B-"):
            current_entity = label[2:]
            extracted[current_entity] = [word_text]

        elif label.startswith("I-"):
            entity_type = label[2:]
            if current_entity == entity_type and entity_type in extracted:
                extracted[entity_type].append(word_text)

            else:
                current_entity = entity_type
                extracted[entity_type] = [word_text]

        else:
            current_entity = None


    final_output = {
        e: " ".join(extracted[e]) if e in extracted else None
        for e in ENTITIES
    }

    return final_output


app = FastAPI()


class AddressInput(BaseModel):
    text: str


@app.post("/predict")
def predict_endpoint(data: AddressInput):
    preprocessed = preprocessing(data.text)
    result = predict_address(preprocessed)
    return Response(
        content=json.dumps(result, ensure_ascii=False, indent=2),
        media_type="application/json"
    )


@app.get("/ping")
def ping(response: Response):
    response.status_code = 200
    return {"status": "ok"}


handler = Mangum(app)
