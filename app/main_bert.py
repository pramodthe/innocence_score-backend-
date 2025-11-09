from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pathlib, pickle, pdfplumber, spacy, torch, tempfile, re

app = FastAPI(title="Innocence-Claim API", version="1.0")

# ---------- CORS for Next.js ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- load pipeline ----------
pkl_path = pathlib.Path(__file__).parent.parent / "models" / "innocence_pipeline.pkl"
with open(pkl_path, "rb") as f:
    bundle = pickle.load(f)
tokenizer, model = bundle["tokenizer"], bundle["model"]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
nlp = spacy.load("en_core_web_sm")

def predict(text: str) -> float:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)
    with torch.no_grad():
        prob = torch.softmax(model(**inputs).logits, dim=1)[0, 1].item()
    return round(prob, 3)

def analyse_pdf(pdf_path: pathlib.Path, cutoff: float):
    rows, total, score_sum = [], 0, 0.0
    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            for sent_idx, sent in enumerate(nlp(text).sents, 1):
                s = sent.text.strip()
                if 10 < len(s) < 500:
                    total += 1
                    score = predict(s)
                    score_sum += score
                    if score >= cutoff:
                        rows.append({
                            "sentence": s,
                            "confidence": score,
                            "page": page_idx,
                            "sent_id": sent_idx,
                        })
    reliability = round((score_sum / total) * 100, 1) if total else 0.0
    tier = "High" if reliability >= 80 else "Medium" if reliability >= 50 else "Low"
    return {"reliability_percent": reliability, "tier": tier}

@app.post("/predict")
async def predict_pdf(
    file: UploadFile = File(...),
    cutoff: float = Form(0.7),
):
    if file.content_type != "application/pdf":
        raise HTTPException(400, "PDF required")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = pathlib.Path(tmp.name)
    try:
        return analyse_pdf(tmp_path, cutoff)
    finally:
        tmp_path.unlink(missing_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}