from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

model = SentenceTransformer('all-MiniLM-L6-v2')


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

        # Remove duplicates / similar
        cleaned = []
        for word in keywords:
            if not any(word in existing or existing in word for existing in cleaned):
                cleaned.append(word)

        label = " ".join(cleaned[:2])
        return label.title()

    except Exception:
        return "General"


def sort_notes(notes, num_clusters=3):
    try:
        if not notes:
            return {}

        k = min(num_clusters, max(1, len(notes)//2))

        embeddings = model.encode(notes)

        if len(notes) == 1:
            return {"General": notes}

        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)

        grouped = {}
        for note, label in zip(notes, labels):
            grouped.setdefault(label, []).append(note)

        final_output = {}
        used = set()

        for _, group_notes in grouped.items():
            label = generate_label(group_notes)

            # avoid duplicate labels
            base = label
            count = 2
            while label in used:
                label = f"{base} {count}"
                count += 1

            used.add(label)
            final_output[label] = group_notes

        return final_output

    except Exception as e:
        return {"error": str(e)}
