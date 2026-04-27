# OThink-SRR1: Search, Refine and Reasoning with Reinforced Learning for Large Language Models

**ArXiv ID:** [2604.19766](https://arxiv.org/abs/2604.19766)  
**Authors:** Haijian Liang, Zenghao Niu, Junjie Wu, Changwang Zhang, Wangchunshu Zhou, Jun Wang (Shenzhen University; OPPO Research Institute)  
**Submitted:** April 2026  
**Field:** Natural Language Processing / Retrieval-Augmented Generation / Reinforcement Learning  

---

## Executive Summary

Retrieval-Augmented Generation (RAG) addresses LLM knowledge gaps by retrieving external documents, but static retrieval pipelines fail on complex multi-hop questions because noise in retrieved passages misdirects reasoning. OThink-SRR1 introduces an iterative **Search-Refine-Reason** loop trained end-to-end via a novel reinforcement learning algorithm (GRPO-IR) that rewards the model for accurately identifying evidence while penalizing unnecessary retrievals. The result is a system that achieves state-of-the-art accuracy on multi-hop QA benchmarks while using fewer retrieval steps and tokens than baselines.

---

## Problem Statement

Standard RAG pipelines perform a single retrieval pass and feed the retrieved documents directly into the LLM context. This fails in two ways for complex questions:

1. **Irrelevant noise:** Retrieved documents often contain text tangentially related to the query. Feeding raw documents forces the model to reason over noise, degrading accuracy.
2. **Multi-hop reasoning gaps:** Complex questions require chaining several retrieval steps (e.g., "What is the birthplace of the CEO of the company that acquired DeepMind?"). A single retrieval cannot satisfy multi-hop requirements.

While recent **dynamic retrieval** strategies (like iterative RAG, ReAct, IRCoT) address the multi-hop problem, they:
- Process full documents at each step, incurring prohibitive cost.
- Do not train the model to filter irrelevant evidence, relying on LLM zero-shot generalization.

---

## Core Concepts & Theory

### Search-Refine-Reason (SRR) Loop

The OThink-SRR1 pipeline operates in three repeating stages:

```
[Search] → Retrieve k documents for current sub-question
     ↓
[Refine] → Distill retrieved docs into concise, relevant facts
     ↓
[Reason] → Update reasoning chain based on distilled facts
     ↓
(Repeat until answer is produced or max steps reached)
```

**Refine stage** is the core innovation: instead of passing raw documents to the reasoning step, a dedicated refiner compresses each retrieved document to only the evidence sentences relevant to the current sub-question. This reduces context length by ~60–70% while preserving key facts.

### GRPO-IR: Group Relative Policy Optimization for Iterative Retrieval

GRPO-IR extends the GRPO reinforcement learning algorithm to the retrieval setting. The reward function has two components:

$$R_{\text{total}} = R_{\text{answer}} - \alpha \cdot R_{\text{retrieval\_penalty}}$$

- **$R_{\text{answer}}$:** Binary reward for whether the final answer matches the ground truth.
- **$R_{\text{retrieval\_penalty}}$:** Penalizes the model for making excessive retrieval calls beyond the minimum needed to answer correctly, discouraging lazy over-retrieval.

The model is trained to balance retrieval quality and efficiency — akin to **evidence-focused attention** learned via RL.

---

## Main Ideas & Key Contributions

1. **OThink-SRR1 Framework:** An iterative Search-Refine-Reason architecture that separates evidence extraction (Refine) from reasoning (Reason).
2. **GRPO-IR Algorithm:** An end-to-end RL training objective that rewards evidence quality and penalizes over-retrieval, enabling the model to learn to be precise.
3. **Efficiency gains:** By compressing documents in the Refine stage, OThink-SRR1 processes significantly fewer tokens per reasoning step.
4. **Improved generalization:** Unlike systems that rely on carefully engineered prompts for retrieval decisions, OThink-SRR1 learns when and how much to retrieve through reinforcement.

---

## Methodology & Implementation

### Datasets & Evaluation

Evaluated on four multi-hop question answering benchmarks:

| Benchmark | Type | Hops |
|-----------|------|------|
| HotpotQA | Open-domain multi-hop | 2 |
| 2WikiMultiHopQA | Entity chain reasoning | 2–3 |
| MuSiQue | Reasoning-intensive | 3–4 |
| Bamboogle | Compositional | 2 |

**Evaluation metrics:** Exact Match (EM) and F1 score.

### Baselines Compared

- Standard RAG (single retrieval)
- IRCoT (iterative retrieval + chain-of-thought)
- ReAct (reasoning + acting)
- Search-o1 (prior search-augmented LLM)

### Key Results

| Model | HotpotQA EM | MuSiQue EM | Avg. Retrievals |
|-------|-------------|------------|-----------------|
| IRCoT | 62.3 | 41.1 | 5.8 |
| Search-o1 | 67.4 | 45.3 | 6.2 |
| **OThink-SRR1** | **73.8** | **52.6** | **3.9** |

OThink-SRR1 achieves higher accuracy with 33% fewer retrieval calls.

---

## Practical Applications & Real-World Use Cases

1. **Enterprise Knowledge Bases:** Answering complex multi-step queries over large internal document collections (legal, financial, medical).
2. **Scientific Literature Research:** Automating literature review by chaining multiple searches across databases.
3. **Customer Support Agents:** Handling nuanced multi-step inquiries that require pulling from multiple policy documents.
4. **Code Debugging:** Retrieving relevant code snippets and documentation in a targeted, iterative fashion.

**Feasibility:** The Refine stage adds latency but significantly reduces total token count per query. In cost-sensitive deployments, the token savings outweigh the extra inference step.

---

## Insights & Implications

- **Key insight:** Separating *evidence extraction* from *reasoning* is more effective than asking LLMs to reason over raw retrieved text — a strong inductive bias that RL training reinforces.
- **Advancing SOTA:** Achieves best-in-class results on 3 of 4 multi-hop QA benchmarks as of April 2026.
- **Limitations:**
  - Refine stage requires an additional LLM call, increasing latency.
  - Performance on very long multi-hop chains (5+ hops) remains limited.
  - The retriever is a fixed black box; jointly training retrieval and reasoning could further improve results.
- **Open questions:** Can GRPO-IR be extended to other tool-augmented LLM settings (code execution, calculator use)?

---

## Code & Resources

- **Paper PDF:** https://arxiv.org/pdf/2604.19766  
- **Affiliations:** Shenzhen University + OPPO Research Institute  
- **Dependencies:** PyTorch, standard RAG infrastructure (e.g., Elasticsearch or FAISS for retrieval), and a base LLM (7B–70B).
- **Computational requirements:** Training on multi-hop QA requires ~8× A100 GPUs; inference is single-GPU compatible for 7B models.

---

## Related Work & Context

- **IRCoT (Trivedi et al., 2022):** Introduced iterative retrieval interleaved with chain-of-thought; OThink-SRR1 adds the Refine stage and RL training.
- **ReAct (Yao et al., 2023):** General framework for reasoning + tool use; OThink-SRR1 specializes and trains end-to-end via RL.
- **GRPO (Group Relative Policy Optimization):** Base RL algorithm that GRPO-IR extends with retrieval-aware rewards.
- **DeepSeek-R1:** Demonstrates RL can dramatically improve reasoning; OThink-SRR1 applies this insight to the retrieval-augmented setting.
- **Future directions:** Combining OThink-SRR1 with structured knowledge graphs for more precise multi-hop evidence chaining.
