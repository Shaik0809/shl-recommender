import json
import os


def load_catalog():
    path = os.path.join(os.path.dirname(__file__), "data", "catalog.json")
    with open(path) as f:
        return json.load(f)


def search(query, top_k=5):
    catalog = load_catalog()
    query_words = query.lower().split()
    results = []

    for assessment in catalog:
        score = 0
        text = (
            assessment["name"] + " " +
            assessment["description"] + " " +
            " ".join(assessment["keywords"]) + " " +
            " ".join(assessment["job_levels"])
        ).lower()

        for word in query_words:
            if word in text:
                score += 1

        if score > 0:
            results.append((score, assessment))

    results.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in results[:top_k]]


if __name__ == "__main__":
    results = search("java developer")
    for r in results:
        print(r["name"], "-", r["test_type"])