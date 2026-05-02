# Hidden Breakthroughs in Language Model Training

**ArXiv ID**: [2506.15872](https://arxiv.org/abs/2506.15872)  
**Authors**: Sara Kangaslahti, Elan Rosenfeld, Naomi Saphra  
**Institutions**: Harvard University; Google Research  
**Published**: June 18, 2025  
**Venue**: ICLR 2026  
**Field**: Machine Learning, Training Dynamics, Interpretability

---

## Executive Summary

Training loss is the primary lens through which we observe language model training, but it is a fundamentally coarse metric: it collapses the model's performance on millions of diverse data points into a single scalar. This ICLR 2026 paper from Harvard and Google Research argues—and empirically demonstrates—that language models undergo many significant **capability breakthroughs during training that are completely invisible in aggregate loss curves**. The authors introduce POLCA, a method that decomposes loss changes along the low-rank training subspace to reveal hidden, interpretable transitions where models acquire new skills. This work has significant implications for how we understand, monitor, and design neural network training.

---

## Problem Statement

### The Coarseness of Aggregate Loss

When we train a language model, we monitor a single scalar: the average negative log-likelihood across the training batch. This loss typically follows a smooth, monotonically decreasing curve with the occasional dramatic discontinuity—sometimes called a **phase transition** or **grokking event**—where the model suddenly learns a new capability.

The prevailing assumption is: *if there's no visible discontinuity in the loss, nothing interesting happened.* This assumption is wrong.

Consider a concrete example: suppose a model is simultaneously learning arithmetic carrying (e.g., 9+8=17) and basic noun-verb agreement. During a training epoch:
- The model makes a breakthrough on *carrying*: loss on carrying examples drops sharply.
- The model regresses slightly on *noun-verb agreement*: loss on those examples ticks up.
- **Net effect**: the aggregate loss barely moves.

The carrying breakthrough—a significant cognitive capability the model just acquired—is invisible in the training curve.

### The Consequences of Invisible Breakthroughs

1. **Misjudging training progress**: A plateauing loss curve might be misinterpreted as lack of progress when the model is actually rapidly acquiring new capabilities.
2. **Poor training interventions**: Learning rate schedules, early stopping, and data mixing decisions made based on aggregate loss may be suboptimal.
3. **Opaque emergent capabilities**: The field has debated whether emergent capabilities arise suddenly or gradually. This work provides evidence that the answer depends entirely on how you measure.
4. **Weak interpretability**: Understanding *when* a model acquired a capability is a prerequisite for understanding *how*.

### Prior Art and Its Limitations

Previous methods for studying training dynamics include:
- **Loss Curvature Analysis (LCA)**: Analyzes the curvature of the loss landscape. Captures some breakthroughs but misses many hidden ones.
- **Fisher Information**: Tracks the Fisher information matrix as a proxy for learning dynamics. Partial signal, but not decomposable into interpretable skill clusters.
- **Direct loss clustering**: Group samples by their loss values or loss changes. As shown in the paper, this fails to identify homogeneous skill-specific clusters.

All prior methods share the limitation of not exploiting the geometric structure of the **training subspace**—the low-dimensional manifold along which gradient updates actually move the model.

---

## Core Concepts & Theory

### 1. The Low-Rank Training Subspace

A fundamental empirical finding from optimization research is that during stochastic gradient descent (SGD), model updates lie approximately within a **low-dimensional subspace** of parameter space. Despite a neural network having billions of parameters, the gradient directions used across all training steps span only a relatively small number of dimensions.

Formally, let `Δθ_t = θ_t - θ_{t-1}` be the parameter update at step `t`. The matrix of stacked updates `[Δθ_1, Δθ_2, ..., Δθ_T]` has a low effective rank—a property observed consistently across architectures and tasks.

This subspace can be characterized by the **top eigenvectors of the loss Hessian** (or its approximation via the empirical Fisher information matrix).

### 2. Projecting Loss Changes onto the Subspace

For each training sample `x_i`, the change in loss between step `t-1` and step `t` is:

```
ΔL_i(t) = L(x_i; θ_t) - L(x_i; θ_{t-1})
```

Rather than averaging these changes (which gives the aggregate loss), POLCA projects each sample's loss change onto the basis vectors of the low-rank training subspace:

```
v_k = k-th eigenvector of the loss Hessian (restricted to training subspace)

Projected change for sample x_i along basis vector v_k:
  p_{i,k}(t) = <∇_θ L(x_i; θ_t), v_k>
```

Where `<·, ·>` denotes the inner product. Intuitively, `p_{i,k}(t)` measures how much of sample `x_i`'s loss change at step `t` is attributable to movement along direction `v_k` in parameter space.

### 3. Iterative Basis Construction

The POLCA basis is constructed iteratively:

```
Algorithm: POLCA Basis Construction
─────────────────────────────────────────────────────
Input: Hessian H, previous basis vectors {v₁, ..., v_{k-1}}
Output: Next basis vector v_k

1. Compute projection nullspace: 
   P = I - Σᵢ vᵢvᵢᵀ  (project out already-found directions)
2. Compute projected Hessian: 
   H_proj = P · H · P
3. Find top eigenvector:
   v_k = argmax_{||v||=1} vᵀ H_proj v
4. Return v_k
─────────────────────────────────────────────────────
```

This ensures each basis vector captures a direction of maximum loss variation that is **orthogonal** to all previously found directions—yielding a diverse, non-redundant decomposition.

### 4. Clustering to Find Interpretable Groups

With the projected loss changes `p_{i,k}(t)` computed for all samples and basis vectors, POLCA applies clustering to group samples that exhibit similar dynamics:

```
Feature vector for sample x_i: 
  f_i = [p_{i,1}(t₁), ..., p_{i,1}(tₙ), p_{i,2}(t₁), ..., p_{i,K}(tₙ)]
  (projected changes across all basis vectors and checkpoints)

Clustering: K-means or hierarchical clustering on {f_i}

Result: Clusters C_1, C_2, ..., C_m where each cluster groups
        samples with similar projected loss dynamics
```

### 5. Identifying Hidden Breakthroughs

A **hidden breakthrough** in a cluster `C_j` is identified when:
- The aggregate loss is smooth (no discontinuity)
- But the projected loss for cluster `C_j` along some basis vector `v_k` shows a sharp discontinuity

This is formalized as: the projected loss curve `{Σ_{x∈C_j} p_{x,k}(t)}_t` exhibits a step change (detected via changepoint detection) while the aggregate loss `{Σ_x L(x; θ_t)}_t` does not.

---

## Main Ideas & Key Contributions

### Contribution 1: The Hidden Breakthrough Phenomenon

The central empirical finding: **language models frequently acquire new capabilities at points where aggregate loss is smooth**. These breakthroughs are hidden because gains on some sample subgroups are offset by losses on others, averaging out in the aggregate metric.

This is not a rare edge case—35.5% of identified clusters exhibit hidden breakthroughs according to POLCA, compared to 0% detectable by direct loss analysis.

### Contribution 2: POLCA Methodology

The POLCA method provides a principled, geometry-aware way to disaggregate training dynamics. Unlike ad hoc clustering on raw loss values, POLCA exploits the known structure of the training process (the low-rank gradient subspace) to find meaningful decompositions.

### Contribution 3: Validation on Synthetic and Natural Language Tasks

The paper provides rigorous validation:
- **Synthetic arithmetic**: The "carrying" skill (handling carry operations in multi-digit addition) serves as a ground-truth test case with known acquisition timing.
- **Natural language**: Real language modeling tasks where skill acquisition timing can be validated against probing classifiers.

### Contribution 4: Comparison Against Baselines

Systematic comparison against four alternative methods (exact loss, change in exact loss, LCA, Fisher information), showing POLCA's superiority in recovering interpretable, homogeneous clusters.

---

## Methodology & Implementation

### Experimental Setup

#### Synthetic Arithmetic Tasks

The authors train small language models on arithmetic tasks (multi-digit addition) where skills can be precisely defined:
- **Skill: Carrying** — Correctly propagating carry operations (e.g., 9+8=17 requires a carry)
- Ground truth: A sample either requires carrying or not (binary, labeled)
- This provides an objective measure of cluster homogeneity (do clusters correspond to "carrying" vs "non-carrying"?)

#### Natural Language Tasks

- Standard language modeling on a curated corpus
- Skills are identified post-hoc via probing classifiers
- Validation: Do discovered clusters correspond to linguistically meaningful categories?

### Evaluation Metrics

**Cluster Homogeneity**: For a cluster `C` and a ground-truth skill label `s`, homogeneity measures how purely the cluster maps to a single skill value:

```
Homogeneity(C) = max(|C ∩ s=0| / |C|, |C ∩ s=1| / |C|)
```

A score of 1.0 means all samples in the cluster share the same skill label (perfect homogeneity). A score of 0.5 is random.

**Fraction of Hidden Breakthroughs**: The proportion of discovered clusters that show sharp transitions in projected loss while the aggregate loss is smooth.

### Key Quantitative Results

#### Cluster Homogeneity for Arithmetic "Carrying" Skill

| Method | Max Homogeneity |
|--------|----------------|
| Exact loss clustering | 0.514 (near random) |
| Change in exact loss | 0.524 (near random) |
| LCA | — |
| Fisher information | — |
| **POLCA** | **0.973** |

POLCA achieves near-perfect cluster homogeneity, correctly separating carrying from non-carrying examples.

#### Fraction of Clusters with Hidden Breakthroughs

| Method | Hidden Breakthrough Rate |
|--------|--------------------------|
| Exact loss | 0.0% |
| Change in exact loss | 0.0% |
| LCA | 1.9% |
| Fisher information | 28.4% |
| **POLCA** | **35.5%** |

POLCA finds nearly twice as many hidden breakthroughs as Fisher information and nearly 20× more than LCA.

### Computational Cost

- **Hessian approximation**: Computing the full Hessian is infeasible for large models. The authors use the **empirical Fisher information matrix** (outer product of gradients) as an approximation.
- **Scalability**: POLCA's computational complexity scales with the number of basis vectors and training checkpoints, not model size directly. The authors demonstrate feasibility on models up to ~1B parameters.
- **Checkpointing frequency**: More frequent checkpoints yield finer-grained breakthrough detection at higher storage cost.

---

## Practical Applications & Real-World Use Cases

### 1. Improved Training Monitoring

MLOps teams monitoring large training runs could use POLCA to:
- Detect when the model has learned a target capability (e.g., code generation, multilingual understanding)
- Identify regressions on specific skills masked by improvements elsewhere
- Set more informative stopping criteria than "loss has plateaued"

### 2. Curriculum Learning Design

Knowing *when* a model acquires prerequisite skills enables better curriculum design:
- Switch from basic to advanced examples at the right moment
- Identify which examples are "stuck" (no breakthrough across training) and need reweighting

### 3. Understanding Emergent Capabilities

One of the most debated questions in LLM scaling research is whether emergent capabilities arise suddenly or gradually. POLCA provides a tool to answer this per-capability:
- Is the capability hidden in aggregate loss but present in POLCA decomposition (suggesting it emerges gradually but is masked)?
- Or does it appear suddenly even in POLCA (suggesting genuine phase transition)?

### 4. Model Evaluation and Capability Auditing

Regulatory and safety-focused evaluation could use POLCA to:
- Determine *exactly* when a model first acquired a sensitive capability during training
- Provide evidence for or against capability claims in model documentation

### 5. Debugging Training Failures

When a model fails to learn a desired capability despite seemingly good aggregate loss:
- POLCA could reveal whether the capability is being partially learned but masked by regressions
- Or whether it is genuinely not being learned (no cluster shows associated dynamics)

---

## Insights & Implications

### The Measurement Problem in Deep Learning

This paper is part of a broader trend questioning whether aggregate scalar metrics are adequate for understanding complex neural network training. The finding that **35.5% of capability acquisitions are invisible to aggregate loss** is a strong empirical argument for multi-dimensional evaluation metrics.

### Phase Transitions Are More Common Than We Think

The lore of "grokking" (Nanda et al., 2023) and "emergent capabilities" (Wei et al., 2022) suggests that capability acquisition is rare and dramatic. POLCA suggests the opposite: capability acquisitions are **frequent and routine**, but most are hidden by the aggregate loss lens. The dramatic visible phase transitions may be special cases where a breakthrough is large enough to dominate the aggregate signal.

### Connection to Mechanistic Interpretability

Mechanistic interpretability aims to understand *which circuits* in a model are responsible for *which capabilities*. POLCA provides the temporal complement: *when* during training did each circuit emerge? Combining circuit analysis (spatial) with POLCA (temporal) could yield a complete picture of capability development.

### Limitations

- **Hessian approximation error**: The empirical Fisher may be a poor approximation of the true loss Hessian in high-loss regions or for non-standard architectures.
- **Basis sensitivity**: The choice of how many basis vectors to use (the rank of the decomposition) is a hyperparameter with unclear optimal setting.
- **Scalability to frontier models**: Current experiments are on relatively small models. Whether POLCA's basis construction is tractable for 100B+ parameter models requires further study.
- **Cluster labeling**: POLCA identifies clusters but does not automatically label them. A human expert or probing classifier is still needed to interpret *what skill* each cluster represents.

### Open Questions

1. **Do hidden breakthroughs follow the same scaling laws as visible ones?** Does more compute lead to proportionally more hidden breakthroughs?
2. **Can POLCA drive active training interventions?** Could a training loop automatically detect hidden breakthroughs and adjust data mixing in real time?
3. **Cross-architecture generalization**: Does the low-rank training subspace structure hold for all architectures (MoE, State Space Models), or is it Transformer-specific?
4. **Connection to loss landscape geometry**: How do hidden breakthroughs relate to saddle points, barriers, and flat regions in the loss landscape?

---

## Code & Resources

- **ArXiv Paper**: [https://arxiv.org/abs/2506.15872](https://arxiv.org/abs/2506.15872)
- **ICLR 2026 Poster**: [https://iclr.cc/virtual/2026/poster/10008294](https://iclr.cc/virtual/2026/poster/10008294)
- **OpenReview**: [https://openreview.net/forum?id=eiEIKGuqaf](https://openreview.net/forum?id=eiEIKGuqaf)

### Implementing POLCA (Sketch)

```python
import torch
import numpy as np
from sklearn.cluster import KMeans

def compute_empirical_fisher(model, dataloader):
    """Approximate Hessian via empirical Fisher (outer product of gradients)."""
    fisher = None
    model.zero_grad()
    for batch in dataloader:
        loss = model(batch).loss
        loss.backward()
        grads = torch.cat([p.grad.view(-1) for p in model.parameters()])
        if fisher is None:
            fisher = grads.unsqueeze(1) @ grads.unsqueeze(0)
        else:
            fisher += grads.unsqueeze(1) @ grads.unsqueeze(0)
        model.zero_grad()
    return fisher / len(dataloader)

def polca_basis(fisher, n_components=10):
    """Extract top eigenvectors of Fisher as POLCA basis."""
    # In practice: use randomized SVD for large models
    eigenvalues, eigenvectors = torch.linalg.eigh(fisher)
    # Return top-k eigenvectors (columns)
    return eigenvectors[:, -n_components:].flip(-1)

def project_loss_changes(model_checkpoints, dataloader, basis):
    """Compute projected loss changes for each sample at each checkpoint."""
    projections = []
    for t in range(1, len(model_checkpoints)):
        model_t = model_checkpoints[t]
        model_prev = model_checkpoints[t-1]
        for batch in dataloader:
            # Compute per-sample loss change
            with torch.no_grad():
                loss_t = per_sample_loss(model_t, batch)
                loss_prev = per_sample_loss(model_prev, batch)
            delta_loss = loss_t - loss_prev
            # Project onto basis
            # (Simplified; real implementation requires gradient-based projection)
            projections.append(delta_loss)
    return torch.stack(projections)

def identify_hidden_breakthroughs(projected_losses, aggregate_loss):
    """Find clusters with discontinuities in projected but not aggregate loss."""
    features = projected_losses.numpy()
    kmeans = KMeans(n_clusters=20)
    cluster_labels = kmeans.fit_predict(features.T)  # cluster over samples
    
    hidden_breakthroughs = []
    for cluster_id in range(20):
        cluster_mask = cluster_labels == cluster_id
        cluster_proj_loss = projected_losses[:, cluster_mask].mean(dim=1)
        # Detect changepoint in cluster_proj_loss
        # (Use ruptures, statsmodels changepoint, or similar)
        has_changepoint = detect_changepoint(cluster_proj_loss)
        has_aggregate_changepoint = detect_changepoint(aggregate_loss)
        if has_changepoint and not has_aggregate_changepoint:
            hidden_breakthroughs.append(cluster_id)
    
    return hidden_breakthroughs
```

### Required Dependencies

```bash
pip install torch transformers
pip install scikit-learn          # K-means clustering
pip install ruptures              # Changepoint detection
pip install numpy scipy
```

---

## Related Work & Context

### Building Blocks

| Work | Contribution | Relation to POLCA |
|------|-------------|-------------------|
| **Grokking** (Power et al., 2022) | Delayed generalization as training phase transition | POLCA reveals that grokking-like events are far more common, just hidden |
| **Emergent Abilities** (Wei et al., 2022) | Capabilities emerge suddenly at scale | POLCA reframes emergence: most abilities emerge gradually, some are hidden by metric choice |
| **Loss Curvature Analysis** (various) | Using curvature to track learning | Baseline comparison; POLCA significantly outperforms LCA |
| **Progress Measures** (Barak et al., 2022) | Tracking algorithmic phases in grokking | POLCA generalizes this to natural language without requiring algorithmic tasks |
| **Edge of Stability** (Cohen et al., 2021) | Training dynamics at the boundary of stability | Related observation that loss landscapes are not static during training |

### Contemporary and Follow-On Work

- **Crosscoding Through Time** (arXiv:2509.05291): Directly cites POLCA, extending the analysis to track emergence and consolidation of linguistic representations in LLM pretraining—using sparse autoencoders to identify feature circuits.
- **ICLR 2026 Workshop on Training Dynamics**: Multiple follow-up works apply POLCA-style analysis to MoE models and vision transformers.

### Where This Research May Lead

1. **Automated curriculum design**: Training systems that detect hidden breakthroughs and dynamically adjust data mixtures in response.
2. **Capability timelines**: Precise attribution of when safety-relevant capabilities (e.g., deceptive alignment, autonomous self-improvement) first emerge during training.
3. **Better evaluation protocols**: Using POLCA-style decomposition as a standard evaluation tool in model training reports, rather than only aggregate loss curves.
4. **Neural scaling laws for hidden capabilities**: Do hidden breakthroughs also follow power-law scaling with compute, or do they have qualitatively different scaling behavior?
5. **Merging with mechanistic interpretability**: Combining POLCA's temporal view (when capabilities emerge) with circuit-level analysis (which neurons/heads are responsible) for a complete theory of capability acquisition.
