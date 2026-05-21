# Lost in State Space: Probing Frozen Mamba Representations

**ArXiv ID:** [2605.00253](https://arxiv.org/abs/2605.00253)

**Authors:** Bhagyashree Wagh (University of Washington), Akash Singh (University of Florida)

**Submission Date:** April 30, 2026

**Field:** Natural Language Processing, Machine Learning

---

## Executive Summary

This paper investigates whether the recurrent state in Mamba language models can serve as semantic sentence representations without fine-tuning or pooling heads. Through systematic analysis using frozen-feature probing on five NLP benchmarks, the researchers reveal critical structural limitations in Mamba's state accumulation mechanism: severe anisotropy and representational collapse. These findings challenge assumptions about the interpretability of state-space models and quantify failure modes in extracting semantic information from frozen representations.

---

## Problem Statement

State-space models like Mamba present an intriguing architectural opportunity: their recurrent mechanism theoretically produces a compressed summary of all tokens processed. This raises the hypothesis that at fixed patch boundaries, token-level outputs could provide semantic sentence summaries without additional pooling, fine-tuning, or special tokens like [CLS].

However, the paper identifies three key research gaps:

1. **Lack of empirical validation:** No systematic evaluation of whether Mamba's state actually preserves semantic information in frozen-feature settings
2. **Unexplored structural properties:** Understanding of anisotropy and representational collapse in SSM states remains limited
3. **Comparison with baselines:** Without baseline comparisons, it's unclear if Mamba states outperform simple pooling strategies

The motivation stems from Transformers' success with frozen features in representation learning, where [CLS] tokens and attention mechanisms enable effective sentence representations. Whether similar principles apply to recurrent state spaces remains unexamined.

---

## Core Concepts & Theory

### State-Space Models (SSMs) and Mamba

**State-Space Model Fundamentals:**
State-space models discretize continuous dynamical systems using the form:

```
h(t) = Ah(t-1) + Bx(t)
y(t) = Ch(t) + Dx(t)
```

Where h(t) is the hidden state, x(t) is input, and y(t) is output. This linear time-invariant (LTI) system can be unrolled as:

```
h_n = A^n h_0 + Σ(A^(n-i-1) B x_i)
```

**Mamba's Selective Mechanism:**
Mamba improves upon vanilla SSMs by introducing input-dependent parameters, allowing the model to selectively focus on relevant tokens and compress information adaptively:

```
A_n = A + (A * softmax(sA(x_n)))
B_n = B ⊙ softmax(sB(x_n))
```

The recurrent state h_n thus accumulates compressed token information according to learned selectivity functions.

### Frozen-Feature Probing Protocol

The paper employs strict frozen-feature probing:

1. **Feature Extraction:** Extract representations from pretrained Mamba-130M without any fine-tuning
2. **Probe Design:** Train lightweight linear classifiers on extracted features
3. **Multiple Strategies:** Test four extraction methods:
   - Patch boundary readouts (last token in patch)
   - Mean pooling over patch
   - CLS-style special token (hypothetical)
   - Maximum pooling

### Structural Pathologies

**Anisotropy:** Mean pairwise cosine similarity approaching 1.0 (0.9999) indicates collapsed representation space where nearly all vectors point in similar directions, destroying discriminative information.

**Representational Collapse:** The raw accumulated state shows severe degradation in information preservation despite the projection layer, suggesting the state mechanism itself loses semantic structure.

---

## Main Ideas & Contributions

### Novel Hypothesis and Empirical Validation

**Core Hypothesis:** "Can Mamba's recurrent state provide semantic sentence summaries for free?"

The paper systematically evaluates whether patch boundary readouts from Mamba's accumulated state outperform naive pooling baselines, challenging implicit assumptions about SSM interpretability.

### Key Technical Contributions

1. **Comprehensive Benchmarking Framework:** Systematic evaluation across five tasks (sentiment analysis, grammaticality detection, paraphrase, semantic similarity, document classification) with multiple random seeds

2. **Quantified Structural Analysis:** First systematic characterization of anisotropy and representational collapse in Mamba states, with precise metrics

3. **Failure Mode Documentation:** Clear evidence that:
   - Patch boundaries do not consistently outperform mean pooling
   - Information preservation breaks down before reaching output projection
   - Frozen-feature settings expose architectural limitations invisible in fine-tuning scenarios

### Intuition Behind Design Choices

The researchers chose this strict frozen-feature protocol because:
- **Interpretability:** Frozen features reveal what information is inherently available without adaptation
- **Fairness:** Allows comparison across different extraction strategies without confounding fine-tuning effects
- **Practical Relevance:** Many applications require frozen representations for efficiency

By testing multiple extraction strategies, the paper avoids oversimplifying Mamba's capabilities while remaining precise about its limitations.

---

## Methodology & Implementation

### Experimental Setup

**Model Architecture:**
- Pretrained Mamba-130M backbone (frozen)
- No fine-tuning on downstream tasks
- Multiple extraction strategies applied to same frozen model

**Benchmark Tasks:**
1. **SST-2:** Binary sentiment classification (movie reviews)
2. **CoLA:** Grammaticality detection (linguistic corpus)
3. **MRPC:** Paraphrase detection (Microsoft Research)
4. **STS-B:** Semantic textual similarity (continuous scores 0-5)
5. **IMDb:** Long document sentiment (binary classification)

### Evaluation Metrics

**Primary Metric:** 
- Accuracy or Pearson correlation (depending on task)
- Evaluated using linear probes trained on extracted representations

**Analysis Metrics:**
- Mean pairwise cosine similarity (anisotropy)
- Variance analysis of raw SSM states
- Projection layer information preservation

### Probe Design

Simple logistic regression classifiers with:
- L2 regularization to prevent overfitting
- 3 random seeds for stability
- Standard hyperparameter tuning on validation splits

### Key Findings

| Task | Patch Boundary | Mean Pooling | Outcome |
|------|---|---|---|
| SST-2 | 82.3% | 82.8% | Pooling wins |
| CoLA | 71.5% | 72.1% | Pooling wins |
| MRPC | 68.9% | 69.4% | Pooling wins |
| STS-B | 0.621 corr | 0.634 corr | Pooling wins |
| IMDb | 76.2% | 76.8% | Pooling wins |

**Structural Findings:**
- Mean pairwise cosine similarity: 0.9999 (extreme anisotropy)
- Projection layer adds critical information not present in raw state
- State collapse occurs during accumulation, not at output

---

## Practical Applications & Use Cases

### Direct Applications

1. **Representation Learning:** Guidelines for using Mamba in frozen-feature scenarios (e.g., transfer learning with limited compute)

2. **Architecture Design:** Insights for improving future SSM architectures to better preserve semantic information in accumulated states

3. **Model Comparison:** Provides methodology for fairly comparing representation quality across different model families

### Applicable Domains

1. **Efficient NLP Systems:** Resource-constrained environments where frozen representations are required
2. **Transfer Learning:** Domain adaptation with limited fine-tuning budgets
3. **Semantic Similarity Tasks:** Information retrieval, clustering, similarity search applications

### Real-World Examples

- **Few-shot Learning:** Where frozen representations become critical for adapting to new tasks with minimal examples
- **Retrieval-Augmented Systems:** Where dense representations from the backbone must preserve semantic information
- **Efficient Deployment:** Mobile or edge applications requiring frozen models for inference

### Feasibility and Implementation Challenges

**Challenge 1: Architecture Limitations**
The anisotropy issue is inherent to SSM design, not easily fixable at the application level. May require architectural modifications (e.g., learned temperature scaling, whitening layers).

**Challenge 2: Overhead of Analysis**
Extracting and analyzing state representations adds computational cost; requires careful optimization for production systems.

**Challenge 3: Generalization**
Findings may be specific to Mamba-130M and GLUE-family tasks; scaling to larger models or diverse domains needs validation.

---

## Insights & Implications

### Broader Field Impact

1. **State-Space Model Limitations:** Challenges the narrative that SSMs are a transparent alternative to Transformers. Their recurrent mechanism can suffer from similar information bottlenecks as attention-based models.

2. **Representation Learning Principles:** Suggests that frozen-feature learning may require explicit mechanisms (projection, normalization) across architecture families, not just Transformers.

3. **Model Interpretability:** Demonstrates that theoretical clarity about a mechanism (e.g., "states are compressed summaries") doesn't guarantee practical interpretability.

### State-of-the-Art Advancement

- **Negative Result Value:** Challenges assumptions in the community about SSM superiority for representation learning
- **Methodological Contribution:** Provides a template for probing frozen representations in emerging architectures
- **Benchmark Contribution:** Adds rigorous evaluation to the GLUE tasks for SSM-family models

### Limitations and Open Questions

**Limitations:**
1. Small model scale (130M parameters) — findings may not extend to larger Mamba variants
2. Limited to GLUE tasks — other domains (vision, code) remain unexplored
3. Single SSM architecture — comparisons with other state-space models (Grok, etc.) lacking

**Open Research Directions:**
1. Can architectural modifications (normalization layers, learned gating) mitigate anisotropy?
2. Do larger Mamba models exhibit different accumulation properties?
3. Are there task-specific extraction strategies that outperform uniform pooling?
4. How do fine-tuning dynamics interact with the structural pathologies identified?

---

## Code & Resources

### Official Repositories

- **arXiv Paper:** [2605.00253](https://arxiv.org/abs/2605.00253)
- **Related Work:** Mamba GitHub ([state-spaces/mamba](https://github.com/state-spaces/mamba))

### Dependencies & Requirements

**Python Libraries:**
```
torch>=2.0.0
transformers>=4.30.0
numpy>=1.24.0
scikit-learn>=1.2.0
```

**Model Requirements:**
- Pretrained Mamba-130M checkpoint (from state-spaces/mamba)
- GLUE dataset suite (via Hugging Face Datasets)
- ~8GB GPU memory for inference

### Quick-Start Guide

```bash
# 1. Install dependencies
pip install torch transformers numpy scikit-learn datasets

# 2. Download pretrained Mamba
from transformers import AutoModel
model = AutoModel.from_pretrained("state-spaces/mamba-130m")

# 3. Extract frozen representations
import torch
input_ids = tokenizer(text, return_tensors="pt")["input_ids"]
with torch.no_grad():
    outputs = model(input_ids, output_hidden_states=True)
    representations = outputs.hidden_states[-1]

# 4. Train linear probe
from sklearn.linear_model import LogisticRegression
probe = LogisticRegression(C=1.0, max_iter=1000)
probe.fit(representations.numpy(), labels)
```

---

## Related Work & Context

### Related Recent Papers

1. **"Characterizing Mamba's Selective Memory using Auto-Encoders"** (arXiv:2512.15653) - Analyzes Mamba's state structure via autoencoders, complementary to this work's direct probing

2. **"A Theoretical Analysis of Mamba's Training Dynamics"** (arXiv:2602.12499) - Provides theoretical grounding for understanding feature filtering in SSMs

3. **"Probing Language Models for Understanding of the Physical World"** (Related methodology) - Establishes frozen-feature probing as a standard evaluation approach

### Prior Work Foundations

- **Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers"** (2018) - Established the [CLS] token + fine-tuning paradigm
- **Gu et al., "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"** (2023) - Introduced the Mamba architecture
- **Hewitt & Liang, "Designing and Interpreting Probes with Control Tasks"** (2019) - Methodology for controlled probing tasks

### Future Research Directions

1. **Architectural Improvements:** Design SSM variants with better state accumulation properties (e.g., hierarchical states, learned normalization)

2. **Cross-Architecture Comparison:** Apply the frozen-feature probing protocol to other SSM variants (Grok, S4, Hyena) and hybrid models

3. **Task-Specific Optimization:** Investigate whether task-aware state extraction strategies can overcome structural limitations

4. **Multi-Scale Analysis:** Study representation properties at different points in the recurrent computation, not just patch boundaries

5. **Integration with Transformers:** Hybrid architectures combining SSM selectivity with Transformer attention mechanisms for better frozen-feature learning
