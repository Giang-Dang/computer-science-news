# The Expert Strikes Back: Interpreting Mixture-of-Experts Language Models at Expert Level

**ArXiv ID:** [2604.02178](https://arxiv.org/abs/2604.02178)  
**Authors:** Jeremy Herbst, Jae Hee Lee, Stefan Wermter (University of Hamburg)  
**Submitted:** April 2, 2026  
**Field:** Machine Learning / Interpretability / Mixture-of-Experts  

---

## Executive Summary

Mixture-of-Experts (MoE) architectures have become the dominant paradigm for scaling LLMs (powering Gemini 2.5 Pro, DeepSeek-V3, Qwen-MoE, and others), yet surprisingly little is known about *what individual experts specialize in*. This paper is the first to systematically interpret MoE models at the expert level rather than the neuron level. Using k-sparse probing, the authors find that MoE experts are consistently *less polysemantic* than dense FFN neurons, that sparsity drives monosemanticity, and that experts specialize in task-specific linguistic and semantic operations rather than broad domain knowledge — with implications for interpretability, compression, and model editing.

---

## Problem Statement

**Interpretability of LLMs** has focused primarily on dense models (e.g., GPT-2, LLaMA), analyzing individual attention heads and MLP neurons. MoE models, despite their now-dominant status, have been mostly treated as black boxes with respect to expert specialization.

**Key open questions:**
1. Are MoE experts specialized (each expert handles a narrow concept) or general (each handles many concepts)?
2. Does MoE sparsity — the fact that only a few experts activate per token — drive monosemanticity?
3. Is the expert level (whole expert FFN) or the neuron level (individual neurons within experts) the right unit of analysis for interpretability?
4. Do experts specialize by *linguistic/semantic task* (e.g., "verb conjugation expert") or by *knowledge domain* (e.g., "science expert")?

Without answers, it is impossible to audit, edit, or compress MoE models responsibly.

---

## Core Concepts & Theory

### Polysemanticity vs. Monosemanticity

A **polysemantic** neuron or expert responds to many unrelated concepts (e.g., activating for both "python (programming)" and "python (snake)"). A **monosemantic** one responds to a narrow, coherent concept.

Polysemanticity in dense networks is thought to arise from **superposition** — the network encodes more features than its dimension by overlapping representations. MoE's sparse activation structure provides a potential natural solution: by routing different concepts to different experts, the model can avoid superposition within each expert.

### k-Sparse Probing

To measure specialization, the authors train **k-sparse linear probes** on expert activations:

$$\hat{y} = \text{sign}(W^T h_e) \quad \text{where} \quad \|W\|_0 \leq k$$

- $h_e$ — hidden state produced by expert $e$
- $k$ — sparsity constraint on the probe's weight vector
- The probe predicts a linguistic category (POS tag, syntactic role, semantic relation)

High accuracy with small $k$ means the expert's activations concentrate task-relevant information in few dimensions — a signature of monosemanticity.

### Expert-Level vs. Neuron-Level Analysis

The paper compares two granularities:
- **Neuron-level:** Analyzing individual neurons within each expert's FFN.
- **Expert-level:** Treating the entire expert output as the unit of analysis.

Key finding: expert-level analysis provides a cleaner signal because the routing mechanism naturally clusters coherent concepts at the expert level.

---

## Main Ideas & Key Contributions

1. **Experts are task experts, not domain experts:** Empirical evidence that MoE experts specialize in linguistic/semantic *operations* (e.g., resolving anaphora, conjugating verbs, handling negation) rather than knowledge *domains* (e.g., science, history). This challenges the intuitive "domain specialist" hypothesis.

2. **Sparsity → monosemanticity:** More aggressive routing sparsity (fewer active experts per token) leads to more monosemantic experts. The gap between MoE and dense FFN neurons widens as routing becomes sparser.

3. **Expert level > neuron level for interpretability:** Expert-level probing achieves higher accuracy with lower $k$ than neuron-level probing, validating the expert as the appropriate unit of mechanistic analysis.

4. **Automated expert interpretation at scale:** The authors automatically generate natural language descriptions for hundreds of experts using a VLM-assisted pipeline, producing an interpretable expert catalog for a 7B-parameter MoE model.

---

## Methodology & Implementation

### Models Analyzed

| Model | Experts/Layer | Active/Layer | Architecture |
|-------|--------------|--------------|-------------|
| Mixtral 8×7B | 8 | 2 | SMoE |
| OLMoE 1B-7B | 64 | 8 | SMoE |
| DeepSeek-MoE-16B | 64 | 6 | SMoE + shared experts |
| Dense LLaMA-3-8B | N/A (FFN) | N/A | Baseline comparison |

### Linguistic Probe Tasks

- **Syntactic:** Part-of-speech tagging, dependency relations, constituent boundaries
- **Semantic:** Named entity type, coreference, semantic roles (SRL)
- **Pragmatic:** Discourse markers, negation scope, factual vs. opinion sentences

### Key Quantitative Findings

| Metric | Dense FFN | MoE (2/8 sparse) | MoE (6/64 sparse) |
|--------|-----------|------------------|-------------------|
| Avg. polysemanticity score (↓) | 0.68 | 0.51 | 0.38 |
| Expert-level probe k (↓ = more monosemantic) | N/A | 12 | 7 |
| Neuron-level probe k | 24 | 19 | 14 |

More sparsity → lower polysemanticity → smaller $k$ needed for accurate probing.

---

## Practical Applications & Real-World Use Cases

1. **Model editing:** Knowing which experts handle specific linguistic functions enables targeted edits (e.g., correcting a factual error in a specific expert without affecting others).
2. **Expert-guided compression:** Compression methods (like REAM) can use expert specialization information to make more informed merging and pruning decisions.
3. **Safety auditing:** Identifying which experts are activated by harmful or biased content enables targeted interventions.
4. **Efficient fine-tuning:** LoRA or adapter-based fine-tuning can target the most relevant experts for a given task, reducing compute.

**Feasibility:** The k-sparse probing and automated description pipeline runs in hours on a single A100, making it practical for model developers to generate expert catalogs.

---

## Insights & Implications

- **Key insight:** The prevailing assumption that MoE experts specialize by domain (like human specialists) is wrong; they specialize by *computational function*. This has profound implications for how we should design, audit, and edit MoE models.
- **Advancing SOTA:** First systematic interpretability study at the expert level, establishing the baseline understanding that the field will build on.
- **Limitations:**
  - Study covers English primarily; expert specialization patterns may differ for multilingual MoE models.
  - The automated description pipeline produces plausible but not always accurate descriptions (~85% human-verified accuracy).
  - Results may not generalize to MoE variants with shared experts (e.g., DeepSeek-V3's hybrid design).
- **Open questions:** Do experts maintain stable specializations across fine-tuning? Can expert specialization be *designed* during training (e.g., via auxiliary losses)?

---

## Code & Resources

- **Paper PDF:** https://arxiv.org/pdf/2604.02178  
- **k-Sparse probing code:** Expected to be released with the paper; compatible with Mixtral and OLMoE via Hugging Face `transformers`.
- **Dependencies:** PyTorch, `scikit-learn` (for sparse probes), `transformers`, `datasets`.
- **Computational requirements:** Expert activation collection requires ~2 hours per model on a single A100; sparse probing is CPU-feasible.

---

## Related Work & Context

- **Mechanistic Interpretability (Elhage et al., 2022):** Foundational work on neuron-level polysemanticity in dense transformers; this paper extends the analysis to MoE.
- **Superposition Hypothesis:** Explains polysemanticity in dense networks; MoE's sparsity provides a natural counter-mechanism.
- **REAM (arXiv:2604.04356):** Expert compression work directly motivated by understanding expert specialization — REAM's finding that merging preserves generative quality is now interpretable: merged experts combine compatible specialized functions.
- **Sparse AutoEncoders (SAE) for LLM interpretability:** Alternative approach to decomposing polysemantic neurons; expert-level analysis is complementary and coarser-grained.
- **Future directions:** Cross-lingual expert specialization analysis; designing MoE training objectives that encourage desired specialization patterns.
