import os
import re
import zipfile
import pandas as pd
from rank_bm25 import BM25Okapi

DATA_PATH = "Cranfield"
TEST_CSV = "test.csv"
OUTPUT_CSV = "submission.csv"
OUTPUT_ZIP = "submission.zip"
TOP_K = 50

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

def build_bm25(documents):
    doc_ids = []
    corpus = []
    for doc_id, text in documents.items():
        tokens = tokenize(text)
        doc_ids.append(doc_id)
        corpus.append(tokens)
    bm25 = BM25Okapi(corpus)
    return bm25, doc_ids

def retrieve_bm25(query, bm25, doc_ids, top_k=TOP_K):
    q_tokens = tokenize(query)
    if not q_tokens:
        return []
    scores = bm25.get_scores(q_tokens)
    top_n = min(top_k, len(scores))
    ranked_idx = sorted(range(len(scores)), key=lambda i: (-scores[i], doc_ids[i]))[:top_n]
    return [doc_ids[i] for i in ranked_idx]

def main():
    documents = load_documents(DATA_PATH)
    bm25, doc_ids = build_bm25(documents)

    queries = pd.read_csv(TEST_CSV)
    results = []
    for _, row in queries.iterrows():
        qid = int(row["query_id"])
        qtext = row["query"]
        relevant_docs = retrieve_bm25(qtext, bm25, doc_ids, TOP_K)
        relevant_docs_str = " ".join(str(d) for d in relevant_docs)
        results.append({"query_id": qid, "query": qtext, "relevant_docs": relevant_docs_str})

    df_out = pd.DataFrame(results)
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(OUTPUT_CSV, OUTPUT_CSV)
    print(f"Done! Submission saved to {OUTPUT_ZIP}")

if __name__ == "__main__":
    main()
