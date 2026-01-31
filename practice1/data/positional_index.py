import os
import re
import zipfile
from collections import defaultdict
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

def build_positional_index(documents: dict[str, str]):
    positional_index: dict[str, dict[str, set[int]]] = defaultdict(dict)
    doc_terms = {}
    for doc_id, text in documents.items():
        terms = tokenize(text)
        doc_terms[doc_id] = set(terms)
        doc_set = defaultdict(set)
        for i in range(len(terms)):
            doc_set[terms[i]].add(i)
        for term in doc_set.keys():
            positional_index[term][doc_id] = doc_set[term]
    print(f"Positional index size: {len(positional_index)} terms")
    return positional_index, doc_terms

def retrieve(query, positional_index, doc_terms):
    q_terms = tokenize(query)
    if not q_terms:
        return []

    # candidate docs: union of docs containing any query term
    candidate_docs = set()
    for term in q_terms:
        for d in positional_index.get(term, {}).keys():
            candidate_docs.add(d)

    scored = []
    for doc_id in candidate_docs:
        # base score: number of unique query terms present in doc
        score = sum(1 for t in set(q_terms) if doc_id in positional_index.get(t, {}))

        # strict consecutive phrase check (exact order, no gaps)
        phrase_found = False
        first_positions = positional_index.get(q_terms[0], {}).get(doc_id, set())
        if first_positions and len(q_terms) > 1:
            # for each start position of first term, check consecutive positions for subsequent terms
            for start in first_positions:
                ok = True
                for offset, term in enumerate(q_terms[1:], start=1):
                    positions = positional_index.get(term, {}).get(doc_id, set())
                    if (start + offset) not in positions:
                        ok = False
                        break
                if ok:
                    phrase_found = True
                    break
        elif first_positions:
            # single-term query: any occurrence counts as a match
            phrase_found = True

        if phrase_found:
            score += 5  # phrase bonus, tuneable

        scored.append((score, doc_id))

    # sort by score desc, then doc_id asc for deterministic output
    scored.sort(key=lambda x: (-x[0], x[1]))
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