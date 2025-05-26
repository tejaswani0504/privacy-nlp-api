from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import re

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

class Post(BaseModel):
    text: str

@app.post("/analyze")
def analyze_post(post: Post):
    doc = nlp(post.text)
    risks = {"high": [], "medium": [], "low": []}

    if re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", post.text):
        risks["high"].append("Aadhaar Number")

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            risks["medium"].append(f"Name: {ent.text}")
        elif ent.label_ == "GPE":
            risks["medium"].append(f"Location: {ent.text}")
        elif ent.label_ == "ORG":
            risks["low"].append(f"Organization: {ent.text}")

    return {"risks": risks}
