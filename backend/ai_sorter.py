from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# 🔥 Lazy load model (VERY IMPORTANT for Render)
model = None

def get_model():
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
    return model


# 🔥 Smart label generator (clean + no duplicates)
def generate_label(notes):
    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=10
        )

        X = vectorizer.fit_transform(notes)
        feature_names = vectorizer.get_feature_names_out()

        if len(feature_names) == 0:
            return "General"

        scores = X.sum(axis=0).A1

        # Top keywords
        top_indices = scores.argsort()[-5:][::-1]
        keywords = [feature_names[i] for i in top_indices]

        # 🔥 Remove duplicates / overlapping words
        cleaned = []
        for word in keywords:
            if not any(word in existing or existing in word for existing in cleaned):
                cleaned.append(word)

        label = " ".join(cleaned[:2])

        return label.title()

    except Exception:
        return "General"


# 🔥 Main function
def sort_notes(notes, num_clusters=3):
    try:
        if not notes:
            return {}

        # Dynamic clusters
        k = min(num_clusters, max(1, len(notes)//2))

        # Get embeddings
        embeddings = get_model().encode(notes)

        if len(notes) == 1:
            return {"General": notes}

        # Clustering
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)

        # Group notes
        grouped = {}
        for note, label in zip(notes, labels):
            grouped.setdefault(label, []).append(note)

        # Generate labels
        final_output = {}
        used_labels = set()

        for _, group_notes in grouped.items():
            label = generate_label(group_notes)

            # Avoid duplicate category names
            base_label = label
            count = 2
            while label in used_labels:
                label = f"{base_label} {count}"
                count += 1

            used_labels.add(label)
            final_output[label] = group_notes

        return final_output

    except Exception as e:
        return {"error": str(e)}
