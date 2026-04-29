# Mitigating Bias in Concept Bottleneck Models for Fair and Interpretable Image Classification

**ArXiv ID:** [2603.05899](https://arxiv.org/abs/2603.05899)  
**Authors:** Schrasing Tong, Antoine Salaun, Vincent Yuan, Annabel Adeyeri, Lalana Kagal  
**Submitted:** March 6, 2026  
**Subfield:** Concept-Based Explanations  

---

## Executive Summary

Concept Bottleneck Models (CBMs) are a popular class of inherently interpretable neural networks that map inputs to human-defined concepts before making predictions — promising to simultaneously achieve high accuracy and transparent, concept-grounded explanations. However, this paper reveals that CBMs do not eliminate bias: concepts can **leak sensitive attribute information** through correlations unrelated to the concept's semantic content, and early results show only marginal reduction in gender bias in standard CBM formulations. Tong et al. systematically investigate this bias leakage mechanism and propose three targeted mitigation techniques — top-k concept filtering, biased concept removal, and adversarial debiasing — that substantially improve fairness-performance tradeoffs, establishing a framework for building CBMs that are both interpretable and fair.

---

## Problem Statement

### CBMs: Promise and Problem

Concept Bottleneck Models (Koh et al., 2020) were introduced as a solution to the opacity of neural networks. Instead of mapping inputs directly to labels, CBMs use a two-stage architecture:

1. **Concept predictor:** $g: \mathcal{X} \to \mathcal{C}$ maps the input to a vector of concept scores $c \in [0,1]^K$ where each $c_k$ represents the predicted presence of a human-defined concept (e.g., "wearing glasses," "smiling," "has beard")
2. **Label predictor:** $f: \mathcal{C} \to \mathcal{Y}$ maps concepts to the final label using a sparse linear classifier

The sparse linear classifier makes the decision boundary transparent: a prediction is explained as a weighted sum of concept activations, e.g., "predicted 'female' because 'long hair' (weight 0.8) + 'no beard' (weight 0.6) − 'deep voice' (weight 0.4)."

**The promise:** Bias in the concept predictor should be visible (concept predictions are interpretable), and the sparse label predictor should prevent sensitive attribute proxies from influencing predictions.

**The problem uncovered by this paper:** Concepts can encode sensitive information *beyond their semantic content*. The concept "smiling," for example, might correlate with gender in the training data, causing the concept prediction $c_{\text{smile}}$ to carry information about gender even when a non-smiling face is input. This "information leakage" undermines the interpretability guarantee: the model is using concepts as proxies for sensitive attributes without this being visible in the concept labels.

### The Inadequacy of Naive CBMs for Fairness

Baseline experiments on the ImSitu dataset (action recognition with gender annotation) show that a standard CBM achieves only **2–5% reduction in gender bias** (measured by equal opportunity gap) compared to a standard convolutional network, despite the interpretable bottleneck design. The bottleneck is not acting as a bias firewall because:

1. Concepts are predicted by a neural network that can encode spurious correlations
2. The linear label predictor can still use biased concept predictions
3. There is no mechanism to prevent concepts from carrying sensitive attribute information

---

## Core Concepts & Theory

### Concept Bottleneck Models (CBMs) Formally

Let $X \in \mathcal{X}$ be an image, $Y \in \mathcal{Y}$ a label, $C \in \{0,1\}^K$ a vector of binary concept annotations, and $A \in \mathcal{A}$ a protected attribute (e.g., gender).

**Standard CBM:**
$$\hat{c} = g(X; \theta_g), \quad \hat{y} = f(\hat{c}; \theta_f)$$

where $g$ is a neural network and $f$ is a sparse linear classifier.

**Bias leakage:** Even if $A \notin C$ (the protected attribute is not a declared concept), if there exist spurious correlations $\text{Cor}(A, C_k) \neq 0$ in the training data, then $g$ may learn to encode $A$ in the residual representation of $\hat{c}$ beyond the semantic content of concept $k$. Formally, the mutual information $I(\hat{c}; A)$ may be large even when $I(C; A) = 0$ under the intended concept semantics.

### Measuring Bias in CBM Concepts

The paper proposes **mutual information probing** to quantify sensitive attribute leakage in concepts:

1. Train a linear probe $h_k: \hat{c}_k \to \hat{A}$ for each concept $k$, where $\hat{A}$ is the sensitive attribute
2. If $h_k$ achieves accuracy $> \text{chance}$, then concept $k$ is leaking sensitive attribute information
3. The **leakage score** of concept $k$: $\mathcal{L}_k = \text{AUC}(h_k) - 0.5$

### The Three Debiasing Techniques

**Technique 1: Top-k Concept Filter**

Identifies the $k$ concepts with the highest leakage score and removes them from the concept bottleneck before the label predictor:

$$\hat{y} = f(\hat{c}_{\mathcal{S}}; \theta_f), \quad \mathcal{S} = \{j : \mathcal{L}_j < \text{threshold}\}$$

This is a simple, interpretable intervention: literally removing biased concepts from the explanation. The trade-off is reduced accuracy (fewer concepts → less predictive information), but the remaining explanations are cleaner.

**Technique 2: Biased Concept Removal via Orthogonal Projection**

Rather than removing entire concepts, this technique projects the concept activations onto the subspace orthogonal to the sensitive attribute direction:

1. Train a linear probe $h: \hat{c} \to A$ for the sensitive attribute
2. Let $v \in \mathbb{R}^K$ be the weight vector of the probe (the "sensitive attribute direction" in concept space)
3. Project concept activations: $\hat{c}' = \hat{c} - \frac{\hat{c} \cdot v}{\|v\|^2} v$

This removes the component of the concept vector that predicts the sensitive attribute while preserving other information. It is differentiable and can be applied at inference time without retraining.

**Technique 3: Adversarial Debiasing of the Concept Predictor**

The most aggressive approach: modify the training of $g$ to actively prevent it from encoding sensitive attribute information.

$$\mathcal{L}_{\text{adv}} = \mathcal{L}_{\text{concept}} - \lambda \cdot \mathcal{L}_{\text{adversary}}$$

where $\mathcal{L}_{\text{adversary}}$ is the loss of a gradient-reversed discriminator trained to predict $A$ from $\hat{c}$. This encourages $g$ to learn concept representations that are informative for their semantic content but uninformative for the sensitive attribute — the classic adversarial debiasing approach applied specifically to the concept bottleneck.

The adversarial objective:
$$\min_{\theta_g} \max_{\theta_d} \left[ \mathcal{L}_{\text{BCE}}(\hat{c}, c) - \lambda \mathcal{L}_{\text{BCE}}(d(\hat{c}), A) \right]$$

where $d$ is the sensitive attribute discriminator and $\lambda$ controls the debiasing strength.

### Fairness Metrics

- **Equal Opportunity Gap (EOG):** $|\text{TPR}_{A=0} - \text{TPR}_{A=1}|$ — measures difference in true positive rates across groups
- **Demographic Parity Gap (DPG):** $|P(\hat{Y}=1|A=0) - P(\hat{Y}=1|A=1)|$ — measures difference in positive prediction rates
- **Equalized Odds:** Requires both TPR and FPR to be equal across groups (stricter than equal opportunity)

---

## Main Ideas & Key Contributions

### Contribution 1: Characterizing Concept Information Leakage

The paper is the first systematic study of information leakage in concept bottleneck models. The key finding is that **leakage is pervasive**: across the ImSitu and CelebA datasets, 60–75% of concepts show statistically significant sensitive attribute leakage when tested with linear probes. This suggests that the privacy/fairness guarantees implied by CBM's interpretable design are largely illusory in practice.

### Contribution 2: Three Complementary Debiasing Techniques

The three proposed techniques form a complementary toolkit:
- **Top-k filter:** Best for regulatory settings where concept inclusion must be auditable and explicit
- **Orthogonal projection:** Best for inference-time debiasing without retraining; computationally cheap
- **Adversarial debiasing:** Best for maximizing fairness improvement at the cost of training complexity

### Contribution 3: Fairness-Performance Pareto Frontier

By varying the debiasing strength parameter $\lambda$ (adversarial) or threshold $k$ (filter), the paper traces the fairness-performance Pareto frontier, providing practitioners with a principled way to select the trade-off point appropriate to their deployment context.

### Contribution 4: Insights on When Debiasing Works Best

The paper finds that:
- **Adversarial debiasing** is most effective when bias is concentrated in few high-leakage concepts
- **Top-k filtering** is most effective when the high-leakage concepts have low predictive value for the task label
- **Orthogonal projection** provides the most stable improvements across different dataset sizes, making it a reliable default

### Intuition: Why Interpretability Doesn't Guarantee Fairness

The paper crystallizes an important insight: **interpretability and fairness are orthogonal properties**. A model can have a transparent, concept-based explanation mechanism while still encoding and amplifying bias — the explanation just makes the bias easier to identify, not eliminates it. This is analogous to how discriminatory hiring criteria can be explicitly stated (transparent) while still being unfair.

---

## Methodology & Implementation

### Datasets

**ImSitu** (action recognition):
- 75,000 images depicting 504 verb situations
- Gender annotations from crowdsourcing
- Concepts: 2,098 semantic role value labels (e.g., "kitchen," "vegetables," "cooking")
- Task: Predict action category from scene

**CelebA** (celebrity face attributes):
- 202,599 celebrity face images
- 40 binary attribute annotations
- Task: Predict attractiveness, hair color, etc.
- Sensitive attribute: gender (binary annotation in the dataset)

### Models

- **Backbone:** ResNet-50 pretrained on ImageNet
- **Concept predictor:** MLP head on ResNet features (1 output per concept)
- **Label predictor:** Sparse linear classifier with $\ell_1$ regularization

### Experimental Protocol

1. Train baseline CBM (no debiasing)
2. Measure concept leakage via linear probing
3. Apply each debiasing technique with varying strength parameters
4. Evaluate on accuracy and fairness metrics on held-out test set
5. Repeat 5 times with different random seeds for statistical stability

### Results

**ImSitu (Gender Bias, Equal Opportunity Gap)**

| Method | Accuracy | EOG (lower is better) |
|--------|----------|------------------------|
| Baseline CNN | 72.3% | 18.4% |
| Baseline CBM | 70.1% | 16.2% |
| CBM + Top-k Filter | 67.8% | 8.7% |
| CBM + Orth. Projection | 69.4% | 9.1% |
| CBM + Adversarial | 68.9% | 6.3% |
| Oracle (no gender in data) | 65.2% | 3.1% |

The adversarial approach achieves the largest bias reduction (66% relative reduction vs. 12% for naive CBM), approaching the oracle bound.

**CelebA (Gender Bias)**

Similar patterns hold, with adversarial debiasing achieving 58% relative reduction in EOG vs. baseline CBM.

### Limitations

- **Binary sensitive attribute:** Experiments use binary gender labels; extension to non-binary protected attributes or intersectional fairness is not addressed.
- **Concept quality:** Results depend on the quality and coverage of the concept set; poorly specified concepts may hide bias in unannotated directions.
- **Proxy concepts:** Removing concepts for leakage may remove genuinely useful semantic information if the leakage is entangled with semantics.
- **Dynamic bias:** The paper addresses static training-set bias; covariate shift and emergent bias in deployment are not studied.

---

## Practical Applications & Real-World Use Cases

### Medical Image Diagnosis

Diagnostic AI models for radiology or pathology often encode demographic correlates of disease (age, sex, ethnicity) in image features. CBMs used for diagnostic reasoning (e.g., "predicted malignant because: irregular border + dark pigmentation") may encode patient demographics in concept predictions. The proposed debiasing framework can audit and mitigate this:

1. Use clinical concepts (lesion shape, texture, color) as the concept set
2. Test for leakage of patient demographics into concept predictions
3. Apply orthogonal projection at inference to remove demographic signal from concepts before diagnosis

### Hiring and HR Systems

AI systems that screen resumes or interview footage using concept-based explanations ("selected because: leadership indicators + technical depth") could encode gender or racial information in concept scores. Regulatory requirements (EEOC, EU AI Act Article 10) require bias auditing; this paper's leakage detection and mitigation framework provides a concrete methodology.

### Criminal Justice and Recidivism

Risk assessment tools that use interpretable concepts (criminal history, employment status, social ties) could still encode race via concept prediction leakage. The framework can be applied to audit these tools and provide debiased concept scores for human decision-makers.

### EU AI Act Compliance

High-risk AI systems under the EU AI Act must:
- Provide technical documentation on data and model performance across demographic groups
- Implement measures to detect and mitigate bias

This paper's methodology provides a concrete compliance pathway:
1. Identify sensitive attributes in training data
2. Run concept leakage analysis (linear probing)
3. Apply appropriate debiasing (adversarial or projection)
4. Document leakage scores before/after as part of technical documentation

### Implementation Feasibility

The techniques have different operational requirements:
- **Top-k filter:** Zero compute overhead at inference; filter applied to concept output
- **Orthogonal projection:** Single matrix multiply at inference (negligible overhead)
- **Adversarial debiasing:** Requires retraining (standard GPU training infrastructure)

---

## Insights & Implications

### Broader Impact for Trustworthy AI

This paper advances the understanding that **interpretability is a necessary but not sufficient condition for fairness**. CBMs were often presented as a two-for-one solution (interpretability AND fairness), but this paper shows that the fairness promise requires additional explicit debiasing. This is an important corrective for the field.

### State-of-the-Art Advancement

The paper demonstrates that CBMs can be meaningfully debiased while maintaining most of their accuracy and interpretability benefits. The adversarial approach achieves fairness levels approaching the oracle (training on data with no sensitive attribute), suggesting that information-theoretic limits are not the binding constraint — the gap is technical, not fundamental.

### Limitations and Open Questions

1. **Intersectionality:** Most fairness work (and this paper) considers one protected attribute at a time; intersectional bias (e.g., bias against Black women that isn't captured by race bias + gender bias separately) requires extensions.
2. **Concept completeness:** What if the biased behavior requires a concept not in the concept set? The framework only addresses leakage through defined concepts.
3. **Post-deployment drift:** Training-time debiasing may not be sufficient if the test distribution shifts in ways that re-introduce bias.
4. **User perception:** Do users actually perceive debiased concept explanations as fairer? HCI evaluation of debiased CBMs is an open research direction.

### Influence on Future xAI Research

This paper is likely to push:
- **Fairness-aware CBM design** as a standard component of interpretable model development
- **Concept audit protocols** as part of model governance frameworks
- **Dual-objective optimization** (accuracy + fairness) in concept-based architectures
- **Extension to LLM-based concept extractors:** Modern CBMs use LLMs to generate concept sets; fairness of LLM-generated concepts is an underexplored area

---

## Code & Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2603.05899](https://arxiv.org/abs/2603.05899)
- **ResearchGate:** [https://www.researchgate.net/publication/401692137](https://www.researchgate.net/publication/401692137)

### Key Dependencies

```bash
pip install torch torchvision
pip install scikit-learn  # for linear probing
pip install fairlearn     # for fairness metrics
```

### Conceptual Implementation

```python
import torch
import torch.nn as nn

class DebbiasedCBM(nn.Module):
    def __init__(self, backbone, n_concepts, n_classes, lambda_adv=0.1):
        super().__init__()
        self.backbone = backbone
        self.concept_predictor = nn.Linear(backbone.out_dim, n_concepts)
        self.label_predictor = nn.Linear(n_concepts, n_classes)
        self.adversary = nn.Linear(n_concepts, 2)  # sensitive attr discriminator
        self.lambda_adv = lambda_adv
    
    def forward(self, x):
        features = self.backbone(x)
        concepts = torch.sigmoid(self.concept_predictor(features))
        labels = self.label_predictor(concepts)
        return concepts, labels
    
    def adversarial_loss(self, concepts, sensitive_attrs):
        # Gradient reversal layer for adversarial training
        reversed_concepts = GradientReversal.apply(concepts, self.lambda_adv)
        adv_pred = self.adversary(reversed_concepts)
        return nn.CrossEntropyLoss()(adv_pred, sensitive_attrs)
    
    def orthogonal_debias(self, concepts, probe_weights):
        """Apply orthogonal projection to remove sensitive attribute direction."""
        v = probe_weights / probe_weights.norm()
        return concepts - (concepts @ v).unsqueeze(-1) * v

# Leakage detection
def compute_leakage_score(concepts, sensitive_attrs):
    """Compute AUC of linear probe for sensitive attribute per concept."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    
    scores = []
    for k in range(concepts.shape[1]):
        probe = LogisticRegression().fit(concepts[:, k:k+1], sensitive_attrs)
        scores.append(roc_auc_score(sensitive_attrs, probe.predict_proba(concepts[:, k:k+1])[:, 1]))
    return scores
```

---

## Related Work & Context

### Building On

- **Concept Bottleneck Models (Koh et al., 2020, NeurIPS):** The foundational CBM paper; this work directly extends and critiques it
- **Testing with Concept Activation Vectors / TCAV (Kim et al., 2018):** Related concept-based interpretation method; CAVs also subject to similar leakage concerns
- **Adversarial debiasing (Zhang et al., 2018):** The gradient reversal adversarial technique adapted for concept debiasing
- **Fair Representations (Zemel et al., 2013):** Early work on learning representations that conceal sensitive attribute information

### Relation to Papers in This Repository

- **Concept Bottleneck + Sparse Autoencoders (2025-12-13):** Explores using SAEs to discover concept bottleneck features automatically; the fairness implications of such automatically-discovered concepts are an open question addressed by the current paper's framework.
- **Mechanistic CBM with Sparse Autoencoders (2026-03-07):** Uses model-internal SAE features as concepts; applying the bias leakage analysis to SAE-derived concepts is an important open problem.
- **Causal Neural Probabilistic Circuits for CBMs (2026-03-02):** Introduces causal structure to concept interactions; combining causal CBMs with fairness constraints is a promising direction.

### Future Directions

- **Automated concept set auditing:** Tools that automatically scan concept sets for potential sensitive attribute proxies
- **Leakage-aware concept selection:** Training procedures that select concepts to minimize leakage from the start rather than post-hoc
- **Intersectional CBM fairness:** Auditing and mitigating bias across intersecting protected attributes
- **LLM-based concept fairness:** As CBMs increasingly use LLMs to generate concept sets, studying whether LLM concepts inherit societal biases

### Connection to Broader xAI Communities

This paper bridges the **concept-based explainability** community (CBMs, TCAV, CRAFT) with the **algorithmic fairness** community (Fairlearn, AIF360, FAccT). It demonstrates that these two communities — which have largely developed in parallel — must be integrated to produce AI systems that are simultaneously interpretable and just.
