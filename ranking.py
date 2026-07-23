from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_candidates(job_description, resumes_data, top_n=10):
    """
    AI ranking using TF-IDF + Cosine Similarity
    """

    if len(resumes_data) == 0:
        return []

    docs = [job_description]

    for candidate in resumes_data:
        docs.append(candidate["text"])

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(docs)

    scores = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    ).flatten()

    ranked = []

    for i, score in enumerate(scores):

        final_score = (
            (score * 100) * 0.6 +
            resumes_data[i]["score"] * 0.4
        )

        candidate = resumes_data[i].copy()

        candidate["ai_score"] = round(float(score * 100), 2)
        candidate["final_score"] = round(final_score, 2)

        ranked.append(candidate)

    ranked.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return ranked[:top_n]