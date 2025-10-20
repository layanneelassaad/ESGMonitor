from transformers import pipeline
from .devices import hf_device


_device = hf_device()


ner = pipeline(
"ner",
model="dslim/bert-base-NER",
aggregation_strategy="simple",
device=_device,
)


summarizer = pipeline(
"summarization",
model="facebook/bart-large-cnn",
device=_device,
)


sentiment = pipeline(
"sentiment-analysis",
model="distilbert-base-uncased-finetuned-sst-2-english",
device=_device,
)


zero_shot = pipeline(
"zero-shot-classification",
model="facebook/bart-large-mnli",
device=_device,
)