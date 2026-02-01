import os
import re
import zipfile
from collections import defaultdict
from typing import Dict, List, Tuple

import pandas as pd

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

def build_positional_index(documents: Dict[str, str]):
    positional_index: Dict[str, Dict[str, List[int]]] = defaultdict(lambda : defaultdict(list))
    doc_terms = {}

    for doc_id, text in documents.items():
        terms = tokenize(text)
        doc_terms[doc_id] = set(terms)
        for position, term in enumerate(terms):
            positional_index[term][doc_id].append(position)
    print(f"Positional index size: {len(positional_index)} terms")
    return positional_index, doc_terms

def retrieve(query, positional_index, doc_terms):
    q_terms = tokenize(query)
    candidate_docs = set()
    for term in q_terms:
        if term in positional_index:
            candidate_docs.update(positional_index[term].keys())

    scored = []
    for doc_id in candidate_docs:
        score = 0
        for term in q_terms:
            if doc_id in positional_index[term]:
                score += 1
        for i in range(len(q_terms) - 1):
            t1, t2 = q_terms[i], q_terms[i + 1]
            if doc_id in positional_index[t1] and doc_id in positional_index[t2]:
                pos1_list = positional_index[t1][doc_id]
                pos2_list = positional_index[t2][doc_id]
                for p1 in pos1_list:
                    for p2 in pos2_list:
                        if p2 - p1 == 1:
                            score += 0.5
        scored.append((score, doc_id))
    scored.sort(key = lambda x : (-x[0], x[1]))
    return [doc_id for _, doc_id in scored[:TOP_K]]

def main():
    documents = load_documents(CRANFIELD_ZIP)
    positional_index, doc_terms = build_positional_index(documents)
    queries = pd.read_csv(TEST_CSV)
    results = []

    for _, row in queries.iterrows():
        qid = int(row["query_id"])
        qtext = row["query"]

        relevant_docs = retrieve(qtext, positional_index, doc_terms)
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