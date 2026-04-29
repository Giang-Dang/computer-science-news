# Why Does Reinforcement Learning Generalize? A Feature-Level Mechanistic Study of Post-Training in Large Language Models

**ArXiv ID:** [2604.25011](https://arxiv.org/abs/2604.25011)  
**Authors:** Dan Shi, Zhuowen Han, Simon Ostermann, Renren Jin, Josef van Genabith, Deyi Xiong  
**Submitted:** April 27, 2026 (ACL 2026 Main Conference)  
**Subfield:** Mechanistic Interpretability  

---

## Executive Summary

Reinforcement learning (RL)-based post-training of large language models (LLMs) — such as RLHF, PPO, and GRPO — consistently improves reasoning generalization beyond the training domain, while supervised fine-tuning (SFT) on identical data frequently leads to forgetting of general capabilities. Despite this well-observed empirical gap, the internal mechanisms driving this contrast have remained opaque. This paper introduces a **feature-level mechanistic analysis methodology** that probes *how* RL and SFT differently reshape a model's internal representations, revealing that RL induces more restrained, continually evolving feature changes that largely preserve base model structure, while SFT rapidly introduces many highly specialized, static features. The findings provide the first mechanistic explanation for why RL generalizes and SFT overfits, with direct implications for interpretable alignment and training transparency.

---

## Problem Statement

### The RL vs. SFT Generalization Mystery

A striking empirical observation in LLM post-training is the **generalization gap** between RL-based and SFT-based methods:

- **RL post-training** (GRPO, PPO with reward models) trained on math reasoning datasets generalizes to code, science, and novel problem formats it never encountered during training.
- **SFT** trained on the same data achieves high performance on in-distribution examples but shows catastrophic forgetting of capabilities from the base model and fails to generalize out-of-distribution.

This gap is practically important because:
1. It guides practitioners toward RL-based methods for capability generalization.
2. It raises alignment concerns: if we don't understand *why* RL generalizes, we can't reliably predict when it will fail.
3. It is relevant to mechanistic safety research — does RL create different internal structures that are harder or easier to steer?

### Prior Explanations and Their Limits

Existing hypotheses for the RL-SFT gap include:
- **Entropy regularization:** RL implicitly maintains higher output entropy, preserving expressiveness
- **Reward shaping:** Scalar rewards provide more nuanced training signal than cross-entropy loss
- **KL constraints:** RLHF's KL penalty from the reference model prevents drastic representation change

These explanations are behavioral (observed at the output level) or theoretical. **No prior work has examined the internal representational changes** at the level of individual features or circuits that explain the generalization difference. This paper fills that gap.

---

## Core Concepts & Theory

### Mechanistic Interpretability Background

Mechanistic interpretability (MI) seeks to reverse-engineer the internal computations of neural networks by identifying **features** — directions in activation space that correspond to interpretable concepts — and **circuits** — subgraphs of the model that compute specific behaviors.

Key tools used in this paper:
- **Sparse Autoencoders (SAEs):** Trained to decompose residual stream activations into sparse combinations of dictionary features. For an activation $a \in \mathbb{R}^d$, an SAE learns:
  $$a \approx W_{\text{dec}} \cdot \text{ReLU}(W_{\text{enc}} a + b_{\text{enc}}) + b_{\text{dec}}$$
  where $W_{\text{dec}} \in \mathbb{R}^{d \times n_{\text{feat}}}$ is a dictionary of $n_{\text{feat}} \gg d$ features, and the encoder produces a sparse activation vector.
- **Feature activation patterns:** The frequency and magnitude of individual SAE feature activations across a dataset reveal which features are "active" (computationally relevant) for a given model and task.

### Feature-Level Analysis Methodology

The paper's core methodological contribution is a **controlled experimental setup** for attributing generalization differences to feature-level changes:

1. **Identical initialization:** RL-tuned and SFT-tuned models start from the same pre-trained base model.
2. **Identical training data:** Both methods see the same question-answer pairs.
3. **Identical evaluation:** Both are tested on held-out tasks with distributional shift.
4. **SAE probing:** The same frozen SAE (trained on the base model's activations) is applied to all three models (base, RL-tuned, SFT-tuned) to project their activations into a comparable feature space.

By projecting onto a shared feature dictionary, the authors can directly compare *which features change*, *how much they change*, and *when during training they change* across the two post-training paradigms.

### Feature Change Metrics

**Feature utilization rate (FUR):** The fraction of SAE dictionary features that are active (above threshold) across a representative dataset:
$$\text{FUR}(M, D) = \frac{1}{n_\text{feat}} \sum_{f=1}^{n_\text{feat}} \mathbf{1}\left[\max_{x \in D} a_f(x; M) > \tau\right]$$

**Feature drift:** Cosine similarity between the base model's feature activation distribution and the post-trained model's:
$$\text{Drift}(f, M) = 1 - \cos\left(\bar{a}_f^{\text{base}}, \bar{a}_f^M\right)$$

**Specialization index:** Whether a feature is activated selectively by a narrow distribution of inputs (high specialization) or broadly (low specialization), measured by the entropy of its activation distribution over a diverse dataset.

---

## Main Ideas & Key Contributions

### Key Finding 1: RL Preserves Features, SFT Replaces Them

The paper's central finding is a stark asymmetry in how the two training paradigms interact with pre-existing features:

- **SFT** rapidly introduces **many new highly specialized features** that activate strongly on training-domain inputs (math problems in their specific format) but are nearly silent on other inputs. The number of newly activated features grows steeply in the first few hundred steps and then plateaus — the model effectively "stamps" the training distribution into a large collection of memorized features.

- **RL** shows **restrained feature change**. Rather than creating many new specialized features, RL modifies the activation weights of existing base model features. The FUR of the RL-tuned model is significantly lower than for SFT at every training step, and the features that *do* change are more general-purpose (activating across multiple domains).

This explains generalization: RL's general-purpose feature modifications benefit reasoning across domains; SFT's specialized features only benefit the exact training distribution.

### Key Finding 2: RL Features Evolve Continuously, SFT Features Freeze Early

SFT-induced specialized features stabilize early in training — their activation patterns converge within the first third of training steps and change little thereafter. RL-induced feature changes, by contrast, continue evolving throughout training.

This dynamic suggests RL maintains a form of **plasticity** — the model keeps adapting its representations — while SFT settles into a local optimum of specialized features that are resistant to further refinement.

### Key Finding 3: Base Model Representation Preservation Correlates with Generalization

Features from the base model that are preserved (high cosine similarity between base and post-trained activations) tend to correspond to general reasoning capabilities. Models that preserve more base model features (RL-tuned) generalize better; models that replace base features with specialized ones (SFT) lose generalization.

This establishes a mechanistic link: **feature preservation = generalization preservation**.

### Key Finding 4: Feature-Level Insights Translate to Practical Predictions

The feature analysis correctly predicts the direction of generalization gaps before behavioral evaluation: in multiple controlled experiments, the model with lower specialization index (as measured by the SAE feature analysis) consistently achieved better out-of-distribution performance.

---

## Methodology & Implementation

### Experimental Setup

**Models:**
- Base: Llama-3-8B and Qwen2.5-7B (separate experiments to verify consistency across architectures)
- Post-trained variants: RL-tuned (GRPO) and SFT-tuned from identical base checkpoints

**Training data:** MATH dataset (math reasoning), 8,000 training examples

**Evaluation (generalization) datasets:**
- AIME (competition math, harder)
- LiveCodeBench (code generation)
- MMLU (broad knowledge)
- ARC-Challenge (science reasoning)

**SAE architecture:** 16,384-feature dictionary applied at residual stream of middle layers (layers 8–24); trained on base model activations from The Pile with reconstruction loss + $\ell_1$ sparsity penalty.

### Analysis Protocol

1. Checkpoint both RL and SFT models every 50 training steps
2. At each checkpoint, compute feature activation statistics over a 5,000-sample diagnostic dataset spanning math, code, and general knowledge
3. Compare FUR, specialization index, and feature drift metrics across checkpoints and between RL/SFT
4. Correlate feature metrics with generalization performance on held-out tasks

### Evaluation Metrics

- **Behavioral:** Pass@1 accuracy on generalization benchmarks
- **Mechanistic:** FUR, specialization index, feature drift, feature preservation rate
- **Statistical:** Pearson correlation between mechanistic metrics and behavioral generalization; Mann-Whitney U tests for distributional differences

### Results Summary

| Metric | SFT | RL-GRPO |
|--------|-----|---------|
| New specialized features (final) | 4,200 ± 180 | 890 ± 95 |
| Feature preservation rate (base→final) | 61% | 84% |
| Generalization drop (MATH→AIME) | −23.4% | −8.1% |
| Generalization drop (MATH→Code) | −31.2% | −4.7% |
| Feature drift convergence step | ~300 | Does not converge |

### Limitations

- **SAE coverage:** The SAE may not capture all relevant features, particularly if RL induces computation in subspaces not well-represented in the training corpus of the SAE.
- **Single SAE:** Results depend on a single SAE architecture; different SAE designs might yield different feature identifications.
- **Correlation ≠ causation:** While feature specialization correlates with generalization failure, the paper stops short of interventional evidence (e.g., ablating specialized features to verify they cause generalization failure).
- **Architecture-specific:** Experiments on 7–8B parameter models; results may differ at larger scales where emergent capabilities arise.

---

## Practical Applications & Real-World Use Cases

### Guiding Post-Training Method Selection

The mechanistic understanding provides actionable guidance:
- For **capability generalization** (deploying to unseen domains): prefer RL-based post-training
- For **in-distribution specialization** (narrow task with fixed format): SFT is appropriate and cheaper
- The specialization index could serve as an **early stopping criterion** — halt SFT when specialized features exceed a threshold to balance specialization and generalization

### Safety and Alignment Monitoring

RL-tuned models preserve base model representations. This has safety implications:
- Preserved general-purpose features may include safety-critical circuits; their preservation under RL suggests alignment properties are retained
- SFT-induced specialized features could create unexpected behaviors when encountering inputs outside the training distribution

The feature-level analysis provides a concrete tool for alignment auditing: measuring whether post-training preserves safety-relevant features.

### Interpretable Training Dashboards

The feature utilization rate and specialization index are cheap to compute at each checkpoint (a fraction of the training cost). They could be integrated into training monitoring dashboards to provide real-time mechanistic feedback during post-training:

```python
# Pseudocode for training monitoring
for step, batch in enumerate(training_data):
    loss = train_step(model, batch)
    
    if step % checkpoint_freq == 0:
        fur = compute_feature_utilization_rate(model, sae, diagnostic_dataset)
        spec_idx = compute_specialization_index(model, sae, diagnostic_dataset)
        
        logger.log({"step": step, "FUR": fur, "specialization": spec_idx})
        
        if spec_idx > SPECIALIZATION_THRESHOLD:
            alert("High specialization detected — generalization may be compromised")
```

### Regulatory Transparency

For high-stakes AI deployment (financial advice, medical reasoning), regulators may require explanations of *how* a model was trained and *why* it behaves as it does. Feature-level training analyses of the type proposed here provide a new class of mechanistic documentation that goes beyond behavioral test results.

---

## Insights & Implications

### Broader Implications for Trustworthy AI

This work provides the **first mechanistic account of the RL-SFT generalization gap**, transforming an empirical observation into an interpretable mechanism. This is significant for:

- **AI safety:** Understanding representation preservation under alignment training is crucial for predicting model behavior on novel inputs
- **Training transparency:** The methodology enables auditable training processes where changes to internal representations are tracked and documented
- **Debugging training failures:** When RL or SFT produces unexpected behavior, the feature-level analysis can identify whether the cause is specialization, drift, or feature destruction

### State-of-the-Art Advancement

Prior mechanistic interpretability work focused largely on **inference-time** analysis (what circuits compute which behaviors). This paper extends MI to **training dynamics** — studying how circuits and features change across training steps. This is a new frontier for the field.

### Open Questions

1. **Do RL-preserved features correspond to semantic circuits?** Can the preserved features be mapped to known reasoning circuits (e.g., induction heads, attention to subject tokens)?
2. **Does scale change the picture?** At 70B+ parameters, RL may induce qualitatively different feature dynamics.
3. **Can we design SFT variants that mimic RL's feature preservation?** Regularization strategies (e.g., elastic weight consolidation, neuron-wise KL constraints) might achieve this without the sample complexity of RL.
4. **What about multimodal RL fine-tuning?** The RLVR (RL with verifiable rewards) paradigm for vision-language models is an emerging frontier where these mechanistic insights should be tested.

---

## Code & Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2604.25011](https://arxiv.org/abs/2604.25011)
- **Key Dependencies:** PyTorch, TransformerLens (for activation extraction), SAELens (for SAE training and analysis)

### Conceptual Implementation

```python
from transformer_lens import HookedTransformer
import torch

def compute_feature_utilization_rate(model, sae, dataset, threshold=0.01):
    """Compute fraction of SAE features active across dataset."""
    feature_active = torch.zeros(sae.n_features)
    
    for batch in dataset:
        with torch.no_grad():
            _, cache = model.run_with_cache(batch)
            activations = cache['resid_post', 16]  # middle layer
            _, feature_acts = sae(activations.reshape(-1, activations.shape[-1]))
            feature_active += (feature_acts.max(0).values > threshold).float()
    
    return (feature_active > 0).float().mean().item()

def compute_specialization_index(model, sae, diverse_dataset, narrow_dataset):
    """Compare feature activations on diverse vs. narrow distribution."""
    diverse_acts = get_feature_activations(model, sae, diverse_dataset)
    narrow_acts = get_feature_activations(model, sae, narrow_dataset)
    
    # Specialization: features strongly active on narrow but not diverse
    specialization = (narrow_acts.mean(0) - diverse_acts.mean(0)).relu()
    return specialization.mean().item()
```

---

## Related Work & Context

### Building On

- **GRPO (DeepSeek-R1, 2025):** The RL post-training method analyzed in the paper
- **Sparse Autoencoders (Cunningham et al., Bricken et al., 2024):** The MI tool used for feature decomposition
- **SAELens library:** Practical infrastructure for SAE training and analysis
- **Elastic Weight Consolidation (Kirkpatrick et al., 2017):** Prior work on catastrophic forgetting prevention, to which this paper provides a mechanistic complement

### Relation to Papers in This Repository

- **Survey: Sparse Autoencoders for LLM Mechanisms (2025-03-07):** Provides background on SAEs that this paper applies; the current paper extends SAE analysis from static inference-time probing to dynamic training analysis.
- **LLM Uncertainty and Correctness via SAEs (2026-04-21):** Also uses SAEs to probe LLM internal states; complements this paper by focusing on uncertainty representation rather than training dynamics.
- **Automated Attention Pattern Discovery (2026-04-04):** Studies attention patterns rather than residual stream features; different level of granularity in mechanistic analysis.

### Future Directions

- **Intervention studies:** Ablating specialized features in SFT models to verify causal role in generalization failure
- **Training dynamics across model families:** Does Mistral, Gemma, or other architectures show similar RL vs. SFT feature dynamics?
- **Reward model effects:** How does the choice of reward model shape feature specialization in RLHF?
- **Connection to alignment tax:** Features important for helpfulness vs. harmlessness — do they compete or coexist under RL?
