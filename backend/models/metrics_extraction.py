import re
from transformers import pipeline
import nltk
from collections import defaultdict
nltk.download("punkt", quiet=True)

# Initialize summarizer and NER pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", device=0)

def preprocess_text(text):
    """
    Clean and preprocess the input text.
    """
    text = re.sub(r"[\r\n]+", " ", text)  # Remove line breaks
    text = re.sub(r"\s{2,}", " ", text)  # Remove extra spaces
    return text.strip()

def summarize_text(text, max_length=100):
    sentences = nltk.sent_tokenize(text)
    chunks = [" ".join(sentences[i:i + 10]) for i in range(0, len(sentences), 10)]
    summaries = []
    for idx, chunk in enumerate(chunks):
        try:
            print(f"Summarizing chunk {idx + 1}: {chunk[:100]}...")
            summary = summarizer(chunk, max_length=max_length, min_length=30, do_sample=False)
            summaries.append(summary[0]["summary_text"])
        except Exception as e:
            print(f"Error summarizing chunk {idx + 1}: {e}")
            summaries.append(f"Error summarizing chunk {idx + 1}: {e}")
    return " ".join(summaries)

def summarize_ghg_efforts(text):
    """
    Summarize GHG efforts from the provided ESG text.
    """
    try:
        return summarize_text(text, max_length=100)
    except Exception as e:
        return f"Error summarizing GHG efforts: {e}"

def summarize_by_branches(text, chunk_size=1000):
    sentences = nltk.sent_tokenize(text)
    location_sentences = defaultdict(list)
    for sentence in sentences:
        print(f"Processing sentence: {sentence[:100]}")
        entities = ner_pipeline(sentence)
        for entity in entities:
            if entity["entity_group"] == "LOC":
                print(f"Detected location: {entity['word']}")
                location_sentences[entity["word"]].append(sentence)
    summaries = {}
    for location, sentences in location_sentences.items():
        try:
            combined_text = " ".join(sentences)
            summary = summarizer(combined_text, max_length=100, min_length=30, do_sample=False)
            summaries[location] = summary[0]["summary_text"]
        except Exception as e:
            summaries[location] = f"Unable to summarize this location's data: {e}"
    return summaries


def generate_esg_recommendations(ghg_summary, branch_summaries):
    """
    Generate ESG recommendations based on summaries.
    """
    recommendations = []
    if ghg_summary:
        recommendations.append(f"Focus on reducing emissions: {ghg_summary[:100]}...")

    for branch, summary in branch_summaries.items():
        recommendations.append(f"In {branch}: Enhance ESG practices related to {summary[:100]}...")

    if not recommendations:
        recommendations.append("No specific recommendations available.")
    return recommendations
