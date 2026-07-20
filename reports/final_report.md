
# 🧪 Final Report — Optimizing a RAG Pipeline for ANVISA Regulatory Question Answering

**Author:** Carlos Montefusco  
**Course:** MSc Data Science & AI – LLM/RAG Engineering  
**Project:** Retrieval-Augmented Generation System Optimization  
**Date:** 2025  

---

# 🗂️ Table of Contents
1. [Introduction](#introduction)  
2. [Dataset & Problem Definition](#dataset)  
3. [Baseline RAG System](#baseline)  
4. [Evaluation Framework](#evaluation-framework)  
5. [Chunking Strategy Optimization](#chunking)  
6. [Reranker Optimization](#reranker)  
7. [Query Rewriting (HyDE) Evaluation](#hyde)  
8. [Adopting Semantic Splitting](#semantic-splitting)  
9. [Final Optimal Configuration](#final-config)  
10. [Final Architecture](#architecture)  
11. [Conclusion](#conclusion)  
12. [Appendix — Code Snippets](#appendix)

---

# <a name="introduction"></a>1. 📘 Introduction

The objective of this project was to transform a simple RAG chatbot into a **high-precision expert assistant for ANVISA regulatory documents**, evaluating each stage of retrieval through structured experiments.

---

# <a name="dataset"></a>2. 📚 Dataset & Problem Definition

The dataset includes key ANVISA regulatory documents:

- RDC 09/2015  
- RDC 46/2009  
- IN 57/2020  
- Portaria 344  

---

# <a name="baseline"></a>3. 🧪 Baseline RAG System

Baseline performance showed perfect *faithfulness* but weak retrieval (*precision*).

---

# <a name="evaluation-framework"></a>4. 🧪 Evaluation Framework

Using RAGAS metrics: faithfulness, context precision, and context recall, the pipeline was evaluated across multiple strategies.

---

# <a name="chunking"></a>5. 🧱 Chunking Strategy Optimization

| chunk_size | overlap | precision | recall |
|------------|---------|-----------|--------|
| **512**    | **50**  | **0.50**  | **0.75** |
| 768        | 115     | 0.25      | 0.42 |
| 1024       | 200     | 0.25      | 0.25 |

Optimal:  
`chunk_size = 512`, `overlap = 50`

---

# <a name="reranker"></a>6. 🧠 Reranker Optimization

| retriever_k | reranker_n | precision | recall |
|-------------|------------|-----------|--------|
| 10          | 2          | 1.0       | 0.50 |
| 10          | 5          | 0.20      | 0.66 |
| **20**      | **5**      | **1.0**   | 0.50 |

Chosen strategy:  
`retriever_k = 20`, `reranker_n = 5`

---

# <a name="hyde"></a>7. 🔍 Query Rewriting (HyDE) Evaluation

HyDE improved general queries but **hurt precision** for regulatory questions.

Conclusion:  
`USE_HYDE = False`

---

# <a name="semantic-splitting"></a>8. ✂️ Semantic Splitting

SemanticSplitterNodeParser replaces fixed-size chunking for more meaningful chunk boundaries.

Configuration:

```
BUFFER_SIZE = 1  
BREAKPOINT_PERCENTILE_THRESHOLD = 90  
SEMANTIC_SPLITTER_EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
```

---

# <a name="final-config"></a>9. 🧩 Final Optimal Configuration

```
SIMILARITY_TOP_K = 20
RERANKER_TOP_N = 5
USE_HYDE = False
SEMANTIC_SPLITTER_EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BUFFER_SIZE = 1
BREAKPOINT_PERCENTILE_THRESHOLD = 90
```

---

# <a name="architecture"></a>10. 🏗️ Final Architecture

```
User Query → Condensed Query → Retriever(top_k=20)
→ Semantic Splitter Chunks → Reranker(top_n=5)
→ LLM → Answer + Source Citations
```

---

# <a name="conclusion"></a>11. 🎉 Conclusion

Through systematic evaluation and optimization, the RAG chatbot became a **high-precision, regulatorily aligned assistant** with transparent retrieval and accurate citations.

---

# <a name="appendix"></a>12. 📎 Appendix — Code Snippets

## Semantic Splitter

```python
semantic_splitter = SemanticSplitterNodeParser(
    buffer_size=BUFFER_SIZE,
    breakpoint_percentile_threshold=BREAKPOINT_PERCENTILE_THRESHOLD,
    embed_model=get_splitter_embedding_model()
)
```

## Reranker

```python
reranker = SentenceTransformerRerank(
    top_n=RERANKER_TOP_N,
    model=RERANKER_MODEL_NAME
)
```

