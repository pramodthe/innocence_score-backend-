import torch, pathlib, nltk
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from app.preprocess import split_sentences
nltk.download('punkt', quiet=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

MODEL_PATH = pathlib.Path(__file__).parent.parent / "models/distilbert_innocence"
tokenizer  = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)
model      = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH).to(device).eval()

@torch.no_grad()
def predict_sentences(text: str, cutoff: float = 0.70):
    sents = split_sentences(text)
    if not sents:
        return []
    encoded = tokenizer(sents, truncation=True, padding=True,
                        max_length=128, return_tensors='pt').to(device)
    logits = model(**encoded).logits
    probs  = torch.softmax(logits, dim=1)[:, 1].cpu().tolist()
    return [{'sentence': s, 'confidence': round(p, 3)}
            for s, p in zip(sents, probs) if p >= cutoff]