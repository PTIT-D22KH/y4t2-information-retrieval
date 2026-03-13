import os
import re
import zipfile
from collections import defaultdict
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

CRANFIELD_ZIP = "Cranfield"
TEST_CSV = "test.csv"
OUTPUT_CSV = "submission.csv"
OUTPUT_ZIP = "submission.zip"
TOP_K = 50

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")

def tokenize(text: str):
    return TOKEN_PATTERN.findall(text.lower())


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


def build_inverted_index(documents):
    inverted_index = defaultdict(set)
    doc_terms = {}

    for doc_id, text in documents.items():
        terms = tokenize(text)
        doc_terms[doc_id] = set(terms)
        for term in terms:
            inverted_index[term].add(doc_id)

    print(f"Inverted index size: {len(inverted_index)} terms")
    return inverted_index, doc_terms


def retrieve(query, inverted_index, doc_terms):
    q_terms = tokenize(query)

    candidate_docs = set()
    for term in q_terms:
        candidate_docs |= inverted_index.get(term, set())

    scored = []
    for doc_id in candidate_docs:
        score = sum(1 for t in q_terms if t in doc_terms[doc_id])
        scored.append((score, doc_id))

    scored.sort(key=lambda x: (-x[0], x[1]))

    return [doc_id for _, doc_id in scored[:TOP_K]]
def build_tfidf(documents, doc_ids):
    # use a simple whitespace/token-based analyzer via join of tokens
    corpus_texts = [" ".join(tokenize(documents[d])) for d in doc_ids]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus_texts)
    return vectorizer, tfidf_matrix
def retrieve_combined(query, bm25, tfidf_vectorizer, tfidf_matrix, doc_ids, top_k=TOP_K):
    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    # TF-IDF ranks (cosine similarity)
    q_text = " ".join(q_tokens)
    q_vec = tfidf_vectorizer.transform([q_text])
    cos_sim = linear_kernel(q_vec, tfidf_matrix).flatten()
    tfidf_ranked = sorted(range(len(cos_sim)), key=lambda i: -cos_sim[i])


    top_doc_ids = [doc_ids[idx] for idx, _ in ranked[:top_k]]
    return top_doc_ids

def main():
    documents = load_documents(CRANFIELD_ZIP)
    doc_ids = list(documents.keys())
    tfidf_vectorizer, tfidf_matrix = build_tfidf(documents, doc_ids)

    queries = pd.read_csv(TEST_CSV)
    results = []

    for _, row in queries.iterrows():
        qid = int(row["query_id"])
        qtext = row["query"]

        relevant_docs = retrieve(qtext, inverted_index, doc_terms)
        relevant_docs_str = " ".join(str(d) for d in relevant_docs)

        results.append({
            "query_id": qid,
            "query": qtext,
            "relevant_docs": relevant_docs_str
        })

    df_out = pd.DataFrame(results)
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(OUTPUT_CSV, OUTPUT_CSV)

    print(f"Done! Submission saved to {OUTPUT_ZIP}")


if __name__ == "__main__":
    main()