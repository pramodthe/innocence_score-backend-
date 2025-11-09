import re, pdfplumber, pathlib, nltk, pandas as pd
from nltk.tokenize import sent_tokenize
nltk.download('punkt', quiet=True)

JUNK = re.compile(r'<footer>.*?</footer>|<header>.*?</header>|^\s*\d+\s*\|\s*P\s*a\s*g\s*e.*|Dictate Express.*', flags=re.I)

def extract_inmate(pdf_path: pathlib.Path, last_name: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as doc:
        for p in doc.pages:
            text += " " + (p.extract_text() or "")
    text = JUNK.sub(" ", text)
    # keep only inmate lines
    lines = [re.sub(rf"^{last_name},?\s+[A-Z]\.\s*", "", l, flags=re.I)
             for l in text.splitlines()
             if re.match(rf"^{last_name},?\s+[A-Z]\.", l, flags=re.I)]
    return " ".join(lines)

def split_sentences(text: str):
    return [s.strip() for s in sent_tokenize(text) if len(s.split()) >= 6]