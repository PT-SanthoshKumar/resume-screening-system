import re
import string
from typing import Iterable, List

try:
    import spacy
except ImportError:  # spaCy is optional; the project can run with regex tokenization.
    spacy = None

try:
    from nltk.corpus import stopwords
except ImportError:
    stopwords = None


_NLP = None
_FALLBACK_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has",
    "have", "in", "is", "it", "of", "on", "or", "that", "the", "to", "with",
    "this", "will", "you", "your", "we", "our", "their", "they", "them"
}


def _load_spacy_model():
    global _NLP
    if _NLP is not None:
        return _NLP
    if spacy is None:
        return None
    try:
        _NLP = spacy.load("en_core_web_sm")
    except OSError:
        _NLP = None
    return _NLP


def get_stop_words() -> set:
    if stopwords is None:
        return _FALLBACK_STOPWORDS
    try:
        return set(stopwords.words("english"))
    except LookupError:
        return _FALLBACK_STOPWORDS


def clean_text(text: str) -> str:
    """Normalize resume or job description text before feature extraction."""
    text = text or ""
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\+?\d[\d\s().-]{7,}\d", " ", text)
    text = text.translate(str.maketrans({c: " " for c in string.punctuation}))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    """Tokenize and lemmatize when spaCy is available, otherwise use regex tokens."""
    cleaned = clean_text(text)
    stop_words = get_stop_words()
    nlp = _load_spacy_model()

    if nlp is not None:
        doc = nlp(cleaned)
        return [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha and not token.is_stop and len(token.text) > 1
        ]

    return [
        token
        for token in re.findall(r"[a-zA-Z]{2,}", cleaned)
        if token not in stop_words
    ]


def normalize_phrase(phrase: str) -> str:
    return " ".join(tokenize(phrase))


def contains_phrase(text: str, phrase: str) -> bool:
    clean_resume = f" {clean_text(text)} "
    clean_phrase = f" {clean_text(phrase)} "
    return clean_phrase in clean_resume


def unique_preserve_order(items: Iterable[str]) -> List[str]:
    seen = set()
    output = []
    for item in items:
        normalized = item.strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            output.append(normalized)
    return output

