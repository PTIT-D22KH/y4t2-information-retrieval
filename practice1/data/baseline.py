import os
import re
import zipfile
import pandas as pd
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

DATA_PATH = "Cranfield"
TEST_CSV = "test.csv"
OUTPUT_CSV = "submission.csv"
OUTPUT_ZIP = "submission.zip"
TOP_K = 50
RRF_K = 60  # RRF constant (higher -> smoother fusion)

TOKEN_PATTERN = re.compile(r"[a-z0-9]+", re.I)
EN_STOPWORDS = {
    "the","and","is","in","to","of","a","an","for","with","on","by","as","that","this","it","from"
}

def tokenize(text: str):
    if not text:
        return []
    text = text.lower()
    tokens = TOKEN_PATTERN.findall(text)
    return [t for t in tokens if t not in EN_STOPWORDS]

def load_documents(data_path):
    documents = {}
    for file_name in os.listdir(data_path):
        if not file_name.endswith(".txt"):
            continue
        full_path = os.path.join(data_path, file_name)
        if not os.path.isfile(full_path):
            continue
        doc_id = os.path.splitext(os.path.basename(file_name))[0]
        with open(full_path, "r", encoding="utf-8") as f:
            documents[doc_id] = f.read()
    print(f"Loaded {len(documents)} documents")
    return documents

def build_bm25(documents, doc_ids):
    corpus_tokens = [tokenize(documents[d]) for d in doc_ids]
    bm25 = BM25Okapi(corpus_tokens)
    return bm25, corpus_tokens

def build_tfidf(documents, doc_ids):
    # use a simple whitespace/token-based analyzer via join of tokens
    corpus_texts = [" ".join(tokenize(documents[d])) for d in doc_ids]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus_texts)
    return vectorizer, tfidf_matrix

def rrf_scores(ranked_list, k=RRF_K):
    # ranked_list: list of doc indices in descending order (best first)
    scores = {}
    for rank, doc_idx in enumerate(ranked_list, start=1):
        scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank)
    return scores

def retrieve_combined(query, bm25, tfidf_vectorizer, tfidf_matrix, doc_ids, top_k=TOP_K):
    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    # BM25 ranks
    bm25_scores = bm25.get_scores(q_tokens)
    bm25_ranked = sorted(range(len(bm25_scores)), key=lambda i: -bm25_scores[i])

    # TF-IDF ranks (cosine similarity)
    q_text = " ".join(q_tokens)
    q_vec = tfidf_vectorizer.transform([q_text])
    cos_sim = linear_kernel(q_vec, tfidf_matrix).flatten()
    tfidf_ranked = sorted(range(len(cos_sim)), key=lambda i: -cos_sim[i])

    # RRF fusion
    fused = {}
    for d, s in rrf_scores(bm25_ranked).items():
        fused[d] = fused.get(d, 0.0) + s
    for d, s in rrf_scores(tfidf_ranked).items():
        fused[d] = fused.get(d, 0.0) + s

    # sort by fused score then by doc_id for tie-break
    ranked = sorted(fused.items(), key=lambda x: (-x[1], doc_ids[x[0]]))
    top_doc_ids = [doc_ids[idx] for idx, _ in ranked[:top_k]]
    return top_doc_ids

def main():
    documents = load_documents(DATA_PATH)
    doc_ids = list(documents.keys())

    bm25, _ = build_bm25(documents, doc_ids)
    tfidf_vectorizer, tfidf_matrix = build_tfidf(documents, doc_ids)

    queries = pd.read_csv(TEST_CSV)
    results = []
    for _, row in queries.iterrows():
        qid = int(row["query_id"])
        qtext = row["query"]
        relevant_docs = retrieve_combined(qtext, bm25, tfidf_vectorizer, tfidf_matrix, doc_ids, TOP_K)
        results.append({
            "query_id": qid,
            "query": qtext,
            "relevant_docs": " ".join(str(d) for d in relevant_docs)
        })

    df_out = pd.DataFrame(results)
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(OUTPUT_CSV, OUTPUT_CSV)
    print(f"Done! Submission saved to", OUTPUT_ZIP)

if __name__ == "__main__":
    main()
