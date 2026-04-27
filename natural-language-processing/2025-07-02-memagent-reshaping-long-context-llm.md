# MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent

**ArXiv ID:** [2507.02259](https://arxiv.org/abs/2507.02259)  
**Authors:** Hongli Yu, Tinghong Chen, Jiangtao Feng, Jiangjie Chen, Weinan Dai, Qiying Yu, Ya-Qin Zhang, Wei-Ying Ma, Jingjing Liu, Mingxuan Wang, Hao Zhou (ByteDance Research / Tsinghua University)  
**Submitted:** July 2025  
**Venue:** **ICLR 2026 Oral** (Rio de Janeiro, April 2026)  
**Field:** Natural Language Processing / Long-Context LLM / Reinforcement Learning  

---

## Executive Summary

Handling infinitely long documents without performance degradation remains the ultimate unsolved challenge in long-text LLM processing. Length extrapolation techniques and efficient attention methods provide incremental improvements but fundamentally cannot scale to millions of tokens. MemAgent introduces a radically different approach: instead of extending context windows, it trains an **RL-based memory agent** that reads documents in segments, maintaining a compressed memory that it selectively overwrites. Trained with an extended DAPO algorithm, MemAgent extrapolates from an 8K training context to **3.5 million token** QA tasks with less than 10% performance loss — an extraordinary 437× context extrapolation ratio. Selected as an ICLR 2026 Oral, representing top ~1% of accepted papers.

---

## Problem Statement

**The long-context challenge** in LLMs is fundamental:

- Standard transformers have quadratic attention complexity O(n²), making million-token contexts computationally infeasible.
- **Length extrapolation methods** (RoPE scaling, ALiBi, YARN) enable some generalization beyond training context but typically degrade significantly beyond 4–8× the training length.
- **Efficient attention methods** (linear attention, sliding window, sparse attention) reduce compute but compromise information retrieval over very long spans.
- **Retrieval-augmented approaches** require the right information to be retrievable, failing on tasks requiring global reasoning over the full document.

The core challenge: processing a 3.5M token document (a ~2,500-page book) requires either storing all 3.5M token KV-cache (infeasible) or developing a compression mechanism that preserves the information needed to answer arbitrary downstream questions.

---

## Core Concepts & Theory

### MemAgent Workflow

MemAgent processes documents through a novel **multi-conversation RL framework**:

```
Document (arbitrarily long)
        │
        ▼
[Segment 1: 8K tokens] → Memory Agent → Memory State M_1
[Segment 2: 8K tokens] → Memory Agent + M_1 → Memory State M_2
[Segment 3: 8K tokens] → Memory Agent + M_2 → Memory State M_3
        ...
[Segment N: 8K tokens] → Memory Agent + M_{N-1} → Memory State M_N
        │
        ▼
[Query] + M_N → Answer
```

At each segment, the memory agent decides:
1. What information from the current segment to **add** to memory.
2. What information in the current memory to **overwrite** (replace with newer/more relevant content).

This **overwrite strategy** is key: unlike append-only memory (which grows unboundedly), overwriting keeps memory size constant while continuously prioritizing the most task-relevant information.

### Memory Representation

Memory $M_t$ is a fixed-size set of **memory entries** — natural language summaries of key facts, with each entry occupying ~64 tokens. A model with 8K context can maintain a memory of ~64 entries (64 × 64 tokens = 4K tokens for memory, 4K for current segment).

### Extended DAPO for Multi-Conversation RL

Standard RL for LLMs optimizes single-turn responses. MemAgent requires optimizing **across the full sequence of memory updates** — a multi-step decision problem. The authors extend **DAPO (Direct Advantage Policy Optimization)** to handle multi-conversation trajectories:

$$\mathcal{L}_{\text{MemAgent}} = -\mathbb{E}_{\tau \sim \pi_M} \left[ \sum_{t=1}^{N} A_t \cdot \log \pi_M(m_t | s_t, M_{t-1}) \right]$$

where $A_t$ is the advantage for memory update action $m_t$ at step $t$, estimated from the **final answer quality** (end-to-end reward).

A critical innovation: **independent-context multi-conversation generation** allows training on many document segments in parallel by treating each segment-memory pair as an independent training example, dramatically increasing training throughput.

---

## Main Ideas & Key Contributions

1. **MemAgent architecture:** A memory agent operating on fixed-size overwrite memory, enabling arbitrary-length document processing without increasing context window.

2. **Multi-conversation RL training:** Extended DAPO that trains memory update decisions end-to-end from final answer reward signals.

3. **Extraordinary extrapolation:** Trains on 8K context, generalizes to 3.5M tokens — a **437× extrapolation** with <10% performance loss.

4. **95%+ NIAH at 512K:** Achieves over 95% accuracy on the Needle-in-a-Haystack (NIAH) retrieval task at 512K context — the standard benchmark for long-context retrieval.

5. **Architectural agnosticism:** MemAgent can be applied to any base LLM without architectural changes.

---

## Methodology & Implementation

### Training Details

- **Base model:** Qwen2.5-7B (8K context window)
- **Training task:** Long document QA with diverse document types (books, scientific papers, code repositories)
- **Training context:** 8K tokens (segments)
- **Memory size:** Fixed 64 entries × 64 tokens = ~4K token memory
- **RL algorithm:** Extended DAPO with independent-context multi-conversation generation

### Benchmarks

| Benchmark | Task | MemAgent | RoPE-scaled (32K) | YARN (128K) |
|-----------|------|----------|-------------------|-------------|
| NIAH (512K) | Needle retrieval | **95.3%** | 71.2% | 82.4% |
| ∞-Bench (Book QA) | Full-book QA | **67.1%** | 41.3% | 52.8% |
| LongBench v2 | Multi-task long | **73.4%** | 58.2% | 64.1% |
| ManyShot | 3.5M examples | **89.2%** | N/A (OOM) | N/A (OOM) |

### Memory Efficiency

| Method | Context Limit | KV-Cache at 3.5M | GPU Memory (70B model) |
|--------|---------------|-------------------|------------------------|
| Full context | 3.5M | 3.5M tokens | >300 GB (infeasible) |
| Sliding window | ~32K effective | 32K | ~20 GB |
| **MemAgent** | **Unlimited** | **8K** | **~16 GB** |

MemAgent processes 3.5M token documents with 8K token memory — a 437× reduction in KV-cache size.

---

## Practical Applications & Real-World Use Cases

1. **Legal document analysis:** Reasoning over entire case law repositories (millions of tokens) for due diligence and legal research.
2. **Scientific literature review:** Processing all papers in a research area to synthesize findings and identify research gaps.
3. **Codebase reasoning:** Understanding entire large codebases (millions of lines) for bug detection and refactoring.
4. **Book-length content:** Summarizing, answering questions, and extracting insights from novels, textbooks, and technical manuals.
5. **Longitudinal data analysis:** Processing years of logs, records, or time-series descriptions for pattern detection.

**Feasibility:** MemAgent runs on a 16 GB GPU for 7B models (vs. 300+ GB needed for full-context approaches to 3.5M tokens). Latency is O(N × segment_time) where N is the number of segments — linear in document length.

---

## Insights & Implications

- **Key insight:** The long-context problem is better solved by *compression with memory* than by *extending context windows*. Human experts solving long-document tasks don't hold the entire document in working memory — they take notes and refer back selectively. MemAgent mimics this strategy.
- **Advancing SOTA:** ICLR 2026 Oral (top ~1% of submissions). Sets a new standard for long-context LLM generalization, far exceeding prior context extrapolation results.
- **Limitations:**
  - Memory overwriting is irreversible; information not deemed important during the read pass cannot be recovered at query time.
  - Performance depends on the quality of the base LLM's summarization ability; weaker base models produce noisier memory updates.
  - Multi-hop questions that require connecting information from distant document segments (read into memory at different times) may suffer from memory interference.
- **Open questions:** Can MemAgent learn query-conditioned memory updates (knowing the question at read time)? How does performance scale with memory size?

---

## Code & Resources

- **Paper PDF:** https://arxiv.org/pdf/2507.02259  
- **GitHub:** https://github.com/BytedTsinghua-SIA/MemAgent  
- **Hugging Face:** https://huggingface.co/papers/2507.02259  
- **Model weights:** Available via ByteDance Research repository.
- **Dependencies:** PyTorch, Hugging Face `transformers`, custom DAPO RL training code.
- **Computational requirements:** Training requires 32× A100 80GB GPUs (multi-conversation generation); inference runs on 1× A100 for 7B model.

---

## Related Work & Context

- **DAPO (Direct Advantage Policy Optimization):** The base RL algorithm extended by MemAgent; DAPO improves stability over standard PPO for LLM training.
- **YARN / RoPE Scaling:** Context window extension methods; MemAgent dramatically outperforms these on ultra-long contexts.
- **RAPTOR / GraphRAG:** Hierarchical summarization approaches for long documents; MemAgent learns its compression strategy via RL rather than relying on fixed hierarchies.
- **Compressive Transformers (Rae et al., 2020):** Early neural memory approach; MemAgent replaces the fixed compressive function with an RL-trained agent.
- **MemoryAgentBench (ICLR 2026 workshop paper):** Benchmark for evaluating LLM memory agents; MemAgent is a strong baseline.
- **Future directions:** Query-conditioned reading (MemAgent knows the question before reading), multi-agent memory sharing for collaborative document analysis.
