# Explainable AI: Context-Aware Layer-Wise Integrated Gradients for Explaining Transformer Models

**ArXiv ID:** [2602.16608](https://arxiv.org/abs/2602.16608)  
**Authors:** Melkamu Abay Mersha, Jugal Kalita (University of Colorado Colorado Springs)  
**Date:** February 18, 2026  
**Subfield:** Feature Attribution  
**Keywords:** Integrated Gradients, Transformer explainability, layer-wise attribution, attention gradients, NLP interpretability, CA-LIG

---

## Executive Summary

Transformer models achieve state-of-the-art performance across NLP and vision tasks, yet their deeply nested, multi-head attention structures make standard feature attribution methods inadequate. This paper introduces the **Context-Aware Layer-wise Integrated Gradients (CA-LIG)** framework, which combines layer-by-layer gradient integration with attention-gradient fusion to produce attribution maps that are simultaneously more faithful, context-sensitive, and hierarchically complete than existing methods. CA-LIG addresses the critical gap between final-layer-only attributions and the actual multi-layer decision process.

---

## Problem Statement

Transformer models process information through dozens of stacked attention and feed-forward layers. Standard explanation methods fail in several ways:

1. **Final-layer bias**: Methods like standard IG aggregate attributions from only the final layer, missing how relevance builds up through the network
2. **Context-blindness**: Token-level attributions don't capture cross-token dependencies that are central to transformer computation (e.g., coreference, syntax)
3. **Attention-gradient disconnection**: Attention weights alone are not reliable attributions (attention ≠ explanation), but neither are raw gradients — their combination is needed
4. **Sign loss**: Most methods produce unsigned (magnitude-only) attributions, losing the distinction between features that support vs. oppose a prediction

**Specific failure modes documented in prior work:**
- LIME on BERT produces inconsistent attributions that change with random seed
- Standard IG on transformers attributes large importance to [CLS] token regardless of input
- Attention rollout underestimates the role of early layers in final decisions
- Gradient × input fails to distinguish features that promote vs. suppress a class

---

## Core Concepts & Theory

### Integrated Gradients (Baseline)

Integrated Gradients (Sundararajan et al., 2017) attributes importance to feature $x_i$ as:

$$\text{IG}_i(\mathbf{x}) = (x_i - x_i') \int_0^1 \frac{\partial F(\mathbf{x}' + \alpha(\mathbf{x} - \mathbf{x}'))}{\partial x_i} d\alpha$$

where $\mathbf{x}'$ is a baseline input (e.g., zero embedding), $F$ is the model, and the integral is approximated with Riemann sums over $m$ steps.

**Problem**: When applied globally to the full transformer, this computes a single attribution vector that conflates contributions from all layers.

### Layer-Wise Integrated Gradients

CA-LIG computes IG *within each transformer block* separately. For layer $l$, the block processes input $\mathbf{h}^{(l-1)}$ to produce $\mathbf{h}^{(l)}$:

$$\text{LIG}_i^{(l)}(\mathbf{x}) = (h_i^{(l-1)} - \bar{h}_i^{(l-1)}) \int_0^1 \frac{\partial \text{Block}^{(l)}(\bar{\mathbf{h}}^{(l-1)} + \alpha(\mathbf{h}^{(l-1)} - \bar{\mathbf{h}}^{(l-1)}))}{\partial h_i^{(l-1)}} d\alpha$$

where $\bar{\mathbf{h}}^{(l-1)}$ is the baseline (zero vector) for that layer.

### Attention Gradient Fusion

Attention weights $A^{(l,h)}$ (for layer $l$, head $h$) are combined with their gradients w.r.t. the output logit $y_c$:

$$\text{AttGrad}^{(l,h)}_{i,j} = A^{(l,h)}_{i,j} \cdot \left| \frac{\partial y_c}{\partial A^{(l,h)}_{i,j}} \right|$$

This product captures both the magnitude of attention (how much attention was paid) and its importance (how much the output changed if this attention changed) — addressing the "attention ≠ explanation" critique.

### CA-LIG: The Full Framework

The final attribution for token $i$ w.r.t. class $c$ is:

$$\text{CA-LIG}_i^c = \sum_{l=1}^{L} w_l \left[ \text{LIG}_i^{(l)} \cdot \sigma\left(\sum_h \text{AttGrad}^{(l,h)}_{i,\cdot}\right) \right]$$

where:
- $w_l$: layer importance weight (learned or uniform)
- $\sigma(\cdot)$: sigmoid normalization
- The dot product fuses gradient-based token importance with attention-based context sensitivity

**Signed attributions**: The final scores retain sign from the IG component, indicating whether token $i$ is supportive (+) or suppressive (-) of class $c$.

### Completeness Axiom Satisfaction

CA-LIG satisfies the completeness axiom (sum of attributions equals the difference from baseline):

$$\sum_i \text{CA-LIG}_i^c = F_c(\mathbf{x}) - F_c(\mathbf{x}')$$

This is a formal guarantee that attributions faithfully account for the prediction, not an approximation.

---

## Main Ideas & Key Contributions

### 1. Hierarchical Relevance Decomposition

By computing IG at each layer independently and aggregating, CA-LIG reveals *how* importance flows through the network:
- Early layers: syntactic token importance
- Middle layers: semantic relationship attribution
- Final layers: task-specific relevance

This decomposition is not available from any prior method applied to transformers.

### 2. Context-Sensitive Normalization via Attention Gradients

The attention gradient fusion makes attributions **context-aware**: the importance of token $i$ depends on which other tokens attended to it and with what importance. This captures coreference, syntactic dependencies, and entity relationships that purely gradient-based methods miss.

### 3. Signed Attribution Maps

Unlike Grad-CAM or SHAP's unsigned magnitudes, CA-LIG produces signed maps that allow users to identify:
- Tokens actively pushing the model toward the predicted class
- Tokens actively opposing the predicted class (counterfactual indicators)

### 4. Layer-Specific Attribution Analysis

CA-LIG enables **layer ablation analysis**: removing a specific layer's attribution contribution and measuring faithfulness degradation reveals which layers are most important for specific predictions — a previously unavailable mechanistic insight.

---

## Methodology & Implementation

### Models Tested
- **BERT-base-uncased** (sentiment analysis, NER)
- **RoBERTa-large** (textual entailment, question answering)
- **DistilBERT** (ablation studies)
- **ViT-B/16** (image classification, demonstrating vision extension)

### Datasets
- SST-2 (sentiment analysis)
- MultiNLI (textual entailment)
- CoNLL-2003 (named entity recognition)
- SQuAD 2.0 (question answering)
- ImageNet (vision classification)

### Evaluation Metrics

**Faithfulness metrics:**
- **Comprehensiveness**: Drop in prediction confidence when top-k attributed tokens are removed
- **Sufficiency**: Prediction confidence using only top-k attributed tokens
- **AOPC (Area Over Perturbation Curve)**: Integrated comprehensiveness over all k

**Stability metrics:**
- **Input sensitivity**: Attribution change under minimal input perturbation (should be low)
- **Reproducibility**: Variance across multiple explanation runs (should be zero for deterministic methods)

**Human alignment:**
- Comparison with human rationale annotations from e-SNLI dataset
- Token-level agreement between CA-LIG and human-highlighted tokens

### Comparison Methods
- Integrated Gradients (IG)
- Attention Rollout
- LIME
- SHAP (via SHAP-for-transformers)
- Gradient × Input
- LayerCAM

### Key Results

| Method | Comprehensiveness ↑ | Sufficiency ↓ | Human Align ↑ | Runtime (ms) |
|---|---|---|---|---|
| IG | 0.42 | 0.31 | 0.61 | 240 |
| Attention Rollout | 0.31 | 0.44 | 0.53 | 12 |
| LIME | 0.38 | 0.35 | 0.59 | 3,200 |
| SHAP | 0.45 | 0.28 | 0.63 | 4,100 |
| CA-LIG (ours) | **0.58** | **0.19** | **0.71** | 380 |

CA-LIG achieves best faithfulness and human alignment at only 58% more runtime than standard IG, and 9× faster than SHAP.

### Limitations
- Requires access to intermediate activations (white-box method)
- Integration with 50 steps adds computation vs. attention rollout
- Layer-weight hyperparameter requires tuning for optimal performance on specific tasks
- Extension to decoder-only transformers (GPT-style) requires additional adaptation

---

## Practical Applications & Real-World Use Cases

### Healthcare NLP
Clinical NLP systems (ICD coding, diagnosis support, clinical note summarization) require explanations of which text fragments drove a decision. CA-LIG's signed, layer-resolved attributions allow clinicians to see not just "which words mattered" but "which words supported vs. opposed this diagnosis."

### Legal Document Analysis
Legal AI systems classifying contracts, identifying relevant clauses, or predicting case outcomes must be explainable to lawyers and judges. CA-LIG's context-aware attributions correctly handle legal coreference (e.g., "the party" attributing back to a specific named entity) that single-layer methods miss.

### Financial Regulatory Compliance
NLP models in finance (credit applications, fraud detection narratives, regulatory reporting) are subject to model risk management requirements. CA-LIG's faithfulness guarantees (completeness axiom) provide audit-ready explanations with formal properties.

### Sentiment Analysis and Customer Feedback
Customer experience teams using NLP to classify product feedback can use CA-LIG's signed attributions to distinguish phrases that are confidently positive ("excellent build quality") from phrases actively suppressing positive sentiment ("but the battery is terrible").

### GDPR Article 22 Compliance
Automated decision-making systems under GDPR must provide meaningful information about the logic involved. CA-LIG provides token-level explanations with hierarchical layer attribution, satisfying the "logic of the processing" requirement more rigorously than attention-weight-only methods.

---

## Insights & Implications

### Advancing xAI for Transformers

The vast majority of modern NLP and vision systems use transformer architectures, yet most XAI methods were designed for simpler models and applied to transformers post-hoc. CA-LIG is one of the first methods designed *from the ground up* for the transformer computation pattern, and achieves measurable improvements on all faithfulness metrics.

### Bridging Attribution and Mechanistic Interpretability

CA-LIG's layer-wise decomposition bridges two XAI traditions:
- **Feature attribution** (what inputs matter?)
- **Mechanistic interpretability** (how does computation flow through the network?)

By attributing importance at each layer, CA-LIG begins to answer "not just what, but where in the network did this token become important" — a step toward the circuit-level understanding pursued in mechanistic interpretability.

### Impact on Trust and Adoption

Human alignment scores (0.71 vs. 0.61 for standard IG) suggest CA-LIG explanations will be more trusted by domain experts, which is critical for adoption in regulated industries.

### Open Questions
- How does CA-LIG perform on very long documents where context spans many tokens?
- Can the layer weights be learned end-to-end for specific explanation quality objectives?
- How does CA-LIG extend to multimodal transformers with cross-attention?
- Is the completeness axiom sufficient for regulatory purposes, or do regulators need additional formal guarantees?

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2602.16608](https://arxiv.org/abs/2602.16608)
- **Published:** Neurocomputing (Elsevier), 2026
- **Dependencies:** PyTorch, HuggingFace Transformers, Captum

### Implementation with Captum
```python
from captum.attr import IntegratedGradients, LayerIntegratedGradients
import torch
from transformers import BertModel, BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
model.eval()

text = "The movie was surprisingly good despite the mediocre reviews."
inputs = tokenizer(text, return_tensors="pt")
input_ids = inputs["input_ids"]
baseline_ids = torch.zeros_like(input_ids)  # baseline: zero embeddings

# CA-LIG: layer-wise attribution
layer_attributions = {}
for layer_idx in range(model.config.num_hidden_layers):
    lig = LayerIntegratedGradients(
        lambda x: model(inputs_embeds=x).last_hidden_state[:, 0, :],  # [CLS]
        model.encoder.layer[layer_idx]
    )
    layer_attributions[layer_idx] = lig.attribute(
        inputs=model.embeddings(input_ids),
        baselines=model.embeddings(baseline_ids),
        n_steps=50
    )

# Fuse with attention gradients
attention_grads = compute_attention_gradients(model, inputs)
ca_lig_scores = fuse_attributions(layer_attributions, attention_grads)

# Visualize
tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
for token, score in zip(tokens, ca_lig_scores):
    print(f"{token:20s}: {score:+.4f}")
```

---

## Related Work & Context

### Feature Attribution Foundations
- **Sundararajan et al. (2017)**: Integrated Gradients — theoretical foundation
- **Shrikumar et al. (2017)**: DeepLIFT — reference-based attribution
- **Simonyan et al. (2014)**: Saliency maps — gradient-based attributions

### Transformer-Specific Methods
- **Chefer et al. (2021)**: Transformer interpretability via relevance propagation
- **Abnar & Zuidema (2020)**: Attention rollout
- **Jain & Wallace (2019)**: Attention is not explanation — foundational critique

### Evaluation Methods
- **Samek et al. (2017)**: Evaluating feature attribution with pixel flipping
- **Hooker et al. (2019)**: ROAR benchmark for attribution faithfulness

### Connection to Broader XAI
CA-LIG sits within the **gradient-based attribution** family alongside IG, GradCAM, and Guided Backprop, but extends this family to the transformer architecture specifically. The key innovation is treating the transformer as a hierarchical computation graph rather than a flat function from input to output.

### Where This Leads
- Extension to instruction-tuned LLMs where the prediction target is a generated token
- Multi-modal CA-LIG for vision-language transformers (cross-attention attribution)
- Combining with SAE-based features for integrated mechanistic + attribution analysis
- Real-time attribution systems for production NLP pipelines

---

*Sources:*
- [arxiv.org/abs/2602.16608](https://arxiv.org/abs/2602.16608)
