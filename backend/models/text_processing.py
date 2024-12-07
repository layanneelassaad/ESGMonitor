import re
from transformers import pipeline
import nltk

nltk.download("punkt", quiet=True)
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", device=0)

# Initialize pipelines
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)

def preprocess_text(text):
    """
    Cleans text by removing unnecessary symbols and repetitive patterns.
    """
    text = re.sub(r"[\r\n]+", " ", text)  # Remove line breaks
    text = re.sub(r"\s{2,}", " ", text)  # Remove extra spaces
    return text.strip()

def summarize_text(text, max_length=100):
    """
    Summarize cleaned text in manageable chunks.
    """
    sentences = nltk.sent_tokenize(text)
    chunks = [
        " ".join(sentences[i:i + 10]) for i in range(0, len(sentences), 10)
    ]
    summaries = []
    for idx, chunk in enumerate(chunks):
        try:
            summary = summarizer(chunk, max_length=max_length, min_length=30, do_sample=False)
            summaries.append(summary[0]["summary_text"])
        except Exception as e:
            summaries.append(f"Error summarizing chunk {idx + 1}: {e}")
    return " ".join(summaries)

def extract_branch_summaries(text):
    """
    Extract branch-specific summaries using NER.
    """
    text = preprocess_text(text)
    entities = ner_pipeline(text)
    location_sentences = {}
    
    for entity in entities:
        if entity["entity_group"] == "LOC":
            location = entity["word"]
            location_sentences.setdefault(location, []).append(entity["word"])

    summarized_branches = {}
    for location, sentences in location_sentences.items():
        summarized_text = summarize_text(" ".join(sentences))
        summarized_branches[location] = summarized_text

    return summarized_branches
