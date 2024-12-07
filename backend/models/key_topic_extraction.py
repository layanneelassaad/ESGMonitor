from collections import defaultdict

def extract_key_topics(clauses, min_confidence=0.8):
    """
    Extracts key topics from clauses by grouping entities with subword handling.
    Filters out low-confidence entities and merges entity groups.
    """
    key_topics = set()

    for clause in clauses:
        grouped_entities = defaultdict(list)
        current_entity_group = None

        for entity in clause.get("entities", []):
            entity_type = entity.get("entity", "")
            word = entity.get("word", "").strip()
            score = entity.get("score", 0)

            if score < min_confidence:
                continue

            if entity_type.startswith("B-"):
                current_entity_group = entity_type[2:]  # Remove "B-"
                grouped_entities[current_entity_group].append(word)
            elif entity_type.startswith("I-") and current_entity_group == entity_type[2:]:
                if word.startswith("##"):
                    grouped_entities[current_entity_group][-1] += word[2:]  # Merge subword tokens
                else:
                    grouped_entities[current_entity_group][-1] += f" {word}"

        # Clean and collect topics
        for topic_group, words in grouped_entities.items():
            topic = " ".join(words).strip()
            if topic:
                key_topics.add(topic)

    # Remove unexpected symbols or noise from the key topics
    cleaned_key_topics = [topic.replace("##", "").strip() for topic in key_topics if topic]

    return list(cleaned_key_topics)
