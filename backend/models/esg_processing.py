from transformers import pipeline
from models.recommendations import generate_esg_recommendations, summarize_by_branches
import nltk

# Initialize NLP components
nltk.download("punkt", quiet=True)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)

def summarize_ghg_efforts(text, chunk_size=1024, max_length=300):
    """
    Summarize GHG efforts and other ESG highlights from the text.
    """
    print("Starting GHG efforts summarization...")
    sentences = nltk.sent_tokenize(text)
    chunks = [" ".join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]
    summaries = []

    for i, chunk in enumerate(chunks):
        try:
            summary = summarizer(chunk, max_length=max_length, min_length=50, do_sample=False)
            summaries.append(summary[0]["summary_text"])
            print(f"Chunk {i+1} summarized successfully.")
        except Exception as e:
            print(f"Error summarizing chunk {i+1}: {e}")

    return " ".join(summaries) if summaries else "Unable to generate summary."

def process_esg_report(file_path, file_type):
    """
    Process the ESG report and extract ESG highlights.
    """
    from models.text_extraction import extract_text_from_file

    print("Extracting text from file...")
    text = extract_text_from_file(file_path, file_type)

    print("Sample text extracted:")
    print(text[:500])  # Print the first 500 characters for debugging

    print("Summarizing GHG efforts...")
    ghg_summary = summarize_ghg_efforts(text)

    print("Extracting branch summaries...")
    branch_summaries = summarize_by_branches(text)

    print("Generating recommendations...")
    recommendations = generate_esg_recommendations(branch_summaries, ghg_summary)

    return {
        "ghg_efforts_summary": ghg_summary,
        "branch_summaries": branch_summaries,
        "recommendations": recommendations,
    }
