# Arabic Address NER API

Named Entity Recognition for Arabic addresses using a fine-tuned **AraBERT** model, served via **FastAPI** and deployed on **AWS Lambda** as a Docker container.

---

## What Does It Do?

Accepts a raw Arabic address string, runs it through a preprocessing pipeline, and returns a structured JSON object with all extracted entities. Missing entities are returned as `null`.

**Entities (10 types):**


`CITY` , `AREA` , `MINI_AREA` ,  `NUM_STREET` , `MAIN_STREET` , `STREET` , `LANDMARK` , `BUILDING` , `FLOOR` , `APARTMENT` 

---

## Project Structure


├── main.py              
├── preprocess.py         
├── requirements.txt     
├── Dockerfile            
└── arabertNER_Model/     
    ├── training_args.bin
    ├── tokenizer_config.json
    ├── model.safetensors    
    ├── tokenizer.json
    └── config.json
```
---
## Download model.safetensors
            from (https://drive.google.com/drive/folders/1wHWKPISB-5ctJzEhoQsL6NE_X1LGtYFT?usp=sharing)
```

## Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn main:app --reload
```

---

## Run with Docker

```bash
# Build
docker build -t arabic-ner-api .

# Run
docker run -p 8000:8000 arabic-ner-api
```

---

## API Endpoints

### `POST /predict`

Accepts a raw Arabic address and returns extracted entities.

**Request:**
```json
{
  "text": "شارع التحرير عمارة ٥ الدور الثالث شقة ٩ المهندسين الجيزة"
}
```

**Response:**
```json
{
  "CITY": "الجيزه",
  "AREA": "المهندسين",
  "MINI_AREA": null,
  "NUM_STREET": null,
  "MAIN_STREET": null,
  "STREET": "التحرير",
  "LANDMARK": null,
  "BUILDING": "٥",
  "FLOOR": "الثالث",
  "APARTMENT": "٩"
}
```

> Entities not found in the address are returned as `null`.

---

### `GET /ping`

Health check to verify the API is running.

**Response:**
```json
{
  "status": "ok"
}
```
