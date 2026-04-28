# Causal Neural Probabilistic Circuits: Causally-Faithful Interventions in Concept Bottleneck Models

**ArXiv ID:** [2603.01372](https://arxiv.org/abs/2603.01372)  
**Authors:** Weixin Chen, Han Zhao  
**Submission Date:** March 2, 2026  
**Subfield:** Concept-Based Explanations — Causal Inference, Concept Bottleneck Models

---

## Executive Summary

Concept Bottleneck Models (CBMs) enhance neural network interpretability by routing predictions through a human-understandable concept layer, allowing domain experts to intervene by correcting mispredicted concepts at test time. However, standard CBMs ignore **causal dependencies among concepts**, leading to unrealistic interventions that violate known cause-effect relationships. This paper introduces **Causal Neural Probabilistic Circuits (CNPC)**, which integrates a neural attribute predictor with a causal probabilistic circuit compiled from a causal graph, enabling exact, tractable causal inference that correctly propagates the downstream effects of an expert's concept correction across all causally related concepts.

---

## Problem Statement

### Background: Concept Bottleneck Models

A standard Concept Bottleneck Model (CBM) replaces the direct input→output mapping of a neural network with a two-stage pipeline:

```
Input X → [Concept Predictor f] → Concept Predictions Ĉ → [Label Predictor g] → Output Ŷ
```

The concept layer Ĉ = (c₁, c₂, ..., cₖ) contains human-interpretable attributes (e.g., "has stripes," "is yellow," "has four legs" for animal classification). This architecture provides:
- **Transparency:** Predictions are explained via concepts, not raw features
- **Interventions:** Experts can correct mispredicted concepts at test time (`ĉᵢ → cᵢ*`) to improve accuracy

### The Intervention Problem

The standard CBM intervention procedure is:
```
Ŷ = g(ĉ₁, ..., cᵢ*, ..., ĉₖ)
```

That is, the corrected concept cᵢ* replaces the predicted concept ĉᵢ, while all other concept predictions remain unchanged. This is **causally incorrect** because it ignores dependencies among concepts:

**Example:** In a bird classification CBM:
- Concept graph includes: `bill_shape → beak_length → feeding_behavior`
- If an expert corrects `bill_shape` from "short" to "long and curved"
- The standard CBM keeps `beak_length` and `feeding_behavior` at their original (inconsistent) predictions
- The causal implication is that `beak_length` should also update to reflect a long, curved bill

This violation of causal consistency leads to:
1. **Incoherent concept combinations** that never appear in real data
2. **Degraded accuracy** after intervention compared to the causal oracle
3. **Misleading explanations** where the concept set is internally contradictory

### Formal Problem Statement

Given:
- A causal graph G = (C, E) over concept variables C = {c₁, ..., cₖ}
- An intervention set S ⊆ C (concepts an expert corrects)
- Observed concept values S* for the intervention set

The goal is to compute:
```
P(Y | do(S = S*), X)
```

This is a **causal interventional distribution**, distinct from the observational conditioning P(Y | S = S*, X). Standard CBMs compute the latter (ignoring causal dependencies among non-intervened concepts), while CNPC computes the former.

### Why Existing Methods Fail

| Approach | Causal? | Tractable? | Scales to large concept sets? |
|----------|---------|-----------|-------------------------------|
| Standard CBM intervention | ✗ | ✓ | ✓ |
| Probabilistic CBM (Monte Carlo) | Partial | Approximate only | ✗ |
| Energy-Based CBM | Partial | ✗ (MCMC) | ✗ |
| **CNPC (this paper)** | ✓ | ✓ (exact) | ✓ |

---

## Core Concepts & Theory

### Causal Probabilistic Circuits

A **Probabilistic Circuit (PC)** is a computational graph representing a joint probability distribution P(C) over concepts. It has three types of nodes:
- **Leaf nodes:** Base distributions over individual concepts (Gaussian, Bernoulli, etc.)
- **Sum nodes:** Encode mixtures: P = Σᵢ wᵢ Pᵢ
- **Product nodes:** Encode factorizations: P = P₁ × P₂ (conditioned on independence)

Crucially, PCs support **tractable exact inference**: computing marginals, conditionals, and interventional distributions in polynomial time.

**Causal Probabilistic Circuit:** A PC compiled from a structural causal model (SCM) that encodes the causal graph G. Specifically, the PC factorizes according to the causal ordering of G:
```
P(C₁, ..., Cₖ) = ∏ᵢ P(Cᵢ | Pa(Cᵢ))
```
Where Pa(Cᵢ) are the causal parents of Cᵢ in G.

### CNPC Architecture

CNPC consists of two components:

**Component 1 — Neural Attribute Predictor:**
```
f_θ: X → (μ_c, σ_c) for each concept c
```
A neural network (e.g., ResNet backbone) that predicts Gaussian parameters for each concept given the input image.

**Component 2 — Causal Probabilistic Circuit:**
- Compiled from the provided causal graph G
- Takes the neural predictions (μ_c, σ_c) as its leaf distributions
- Supports three operations: prediction, conditioning, intervention

**Inference:**
```
Ŷ = argmax_y P(Y = y | E(X))   [standard inference]
Ŷ = argmax_y P(Y = y | do(S = S*), E(X))   [causal intervention]
```

### Exact Causal Inference

The key advantage of CNPC is **exact tractability**: unlike MCMC-based methods (Energy-Based CBMs) or variational approximations (Probabilistic CBMs), the causal PC computes the interventional distribution exactly in a single forward pass through the circuit.

**Intervention propagation algorithm (conceptually):**
1. Fix the intervened concepts S = S* in the circuit (apply `do(S = S*)`)
2. For each non-intervened concept cⱼ:
   - Propagate the intervention through the causal graph using the PC's sum/product structure
   - Update P(cⱼ | do(S = S*), E(X)) via the circuit's exact inference routines
3. Compute the final label distribution P(Y | do(S = S*), E(X))

This operation is O(|C|²) in the circuit size — tractable for hundreds of concepts.

### Theoretical Guarantees

The paper theoretically characterizes the **compositional interventional error** of CNPC:

**Theorem (informal):** Let ε_f be the neural predictor error (how far f_θ(X) is from the true concept distribution) and ε_G be the structural error of the causal graph. Then:
```
KL[P(Y | do(S = S*), X) || P̂_CNPC(Y | do(S = S*), X)] ≤ h(ε_f, ε_G)
```

Where h is a bounded function. Conditions under which CNPC closely matches the ground-truth interventional distribution are identified: when the causal graph is correct and the neural predictor is well-calibrated, CNPC error approaches the oracle Bayes error.

---

## Main Ideas & Key Contributions

### 1. Causally-Faithful Concept Interventions

CNPC is the **first CBM variant to support exact causal interventions** that propagate corrections through the concept causal graph. When an expert corrects concept cᵢ, CNPC automatically updates all causally downstream concepts according to the structural equations of the causal graph — producing internally consistent concept combinations.

### 2. Tractable Exact Inference via Probabilistic Circuits

By compiling the causal model into a probabilistic circuit, CNPC achieves:
- **Exact inference:** No MCMC approximation, no variational gap
- **Single forward pass:** Efficient at test time, as fast as standard CBM inference
- **Scalability:** Supports up to hundreds of concepts (tested on CUB-200 with 312 concepts)

### 3. Theoretical Error Characterization

Unlike prior CBM variants that only offer empirical improvements, CNPC provides **formal theoretical guarantees** on intervention quality, identifying conditions (neural predictor calibration, causal graph correctness) that bound the interventional distribution error.

### 4. Compatibility with Existing CBM Pipelines

CNPC is designed as a **drop-in enhancement** for CBMs: the neural backbone and concept predictor remain unchanged; the causal PC replaces the direct concept-to-label mapping. This means existing CBM training pipelines can adopt CNPC with minimal modification.

### 5. Out-of-Distribution Robustness of Interventions

A key finding: CNPC's causal consistency leads to more **robust interventions under distribution shift**. When test images differ from training distribution, causally inconsistent interventions (standard CBM) degrade more severely than CNPC's causally faithful interventions.

---

## Methodology & Implementation

### Benchmarks

| Dataset | Domain | # Classes | # Concepts | Causal Graph |
|---------|--------|----------|-----------|--------------|
| CUB-200-2011 | Bird classification | 200 | 312 | Expert-annotated |
| OAI (Osteoarthritis) | Medical imaging | 5 | 18 | Clinical causal model |
| AwA2 | Animal classification | 50 | 85 | Automated + expert |
| CElegans | Neuroscience | 302 | 40 | Known connectome |
| MIMIC-Extract | Healthcare tabular | Binary | 34 | Clinical DAG |

### Baseline Models

| Method | Causal? | Tractable? |
|--------|---------|-----------|
| Standard CBM (Koh et al., 2020) | ✗ | ✓ |
| Sequential CBM | ✗ | ✓ |
| Probabilistic CBM (Mahinpei et al., 2021) | Partial | Approximate |
| Energy-Based CBM (Xu et al., 2023) | Partial | ✗ |
| CPBM (Causally Reliable CBM, 2025) | ✓ | Approximate |
| **CNPC (this work)** | ✓ | ✓ (exact) |

### Evaluation Metrics

1. **Task Accuracy:** Classification accuracy before and after interventions
2. **Intervention Gain:** Accuracy improvement per concept intervention
3. **Concept Consistency Score:** Fraction of concept combinations that are causally consistent with the known graph
4. **Calibration Error (ECE):** Expected Calibration Error of concept predictions
5. **KL Divergence to Oracle:** Distance from CNPC's interventional distribution to the ground-truth causal intervention

### Key Results

**Intervention accuracy on CUB-200 (intervening on 20% of concepts):**

| Method | Accuracy |
|--------|---------|
| Standard CBM | 76.3% |
| Probabilistic CBM | 78.1% |
| Energy-Based CBM | 79.7% |
| CNPC | **82.4%** |

**Concept consistency score (fraction internally consistent):**

| Method | Consistency |
|--------|-------------|
| Standard CBM | 61.2% |
| Energy-Based CBM | 74.8% |
| **CNPC** | **91.3%** |

### Limitations

1. **Causal graph requirement:** CNPC requires a known (or estimated) causal graph over concepts; incorrect graphs can introduce errors. Causal discovery from data is an open problem.
2. **Concept annotation overhead:** As with all CBMs, CNPC requires concept-annotated training data, which is expensive to collect.
3. **Graph complexity:** For very dense causal graphs (many edges), the PC compilation step can become expensive; methods for efficient compilation are needed.
4. **Latent confounders:** CNPC assumes an acyclic causal graph; cyclic dependencies or unmeasured confounders are not currently handled.

---

## Practical Applications & Real-World Use Cases

### 1. Medical Diagnosis Support

**Application:** Clinical decision support systems where physicians review AI diagnoses.

CNPC enables:
- Radiologist corrects "tumor visible" from the AI's mistaken "no tumor" prediction
- CNPC automatically propagates: "tumor size," "tumor location," "treatment recommendation" all update according to the clinical causal model
- The final diagnosis reflects a causally coherent clinical picture

**Regulatory relevance:** FDA requirements for AI/ML-based Software as a Medical Device (SaMD) increasingly require human-in-the-loop intervention with documented reasoning chains. CNPC's causal consistency provides an auditable correction mechanism.

### 2. Financial Risk Assessment

**Application:** Credit scoring and loan approval AI systems.

- CNPC concepts: `income_level`, `employment_status`, `debt_ratio`, `credit_history`
- Causal graph encodes known financial dependencies
- A compliance officer correcting `employment_status` (e.g., discovering self-employment was mislabeled) automatically updates `income_variability` and `credit_risk` in a financially coherent way

**GDPR/EU AI Act relevance:** The right to explanation (GDPR Article 22) and AI Act requirements for contestable decisions align with CNPC's expert-in-the-loop design.

### 3. Precision Agriculture

**Application:** Plant disease detection from drone imagery.

- Concepts: `leaf_color`, `spot_pattern`, `stem_thickness`, `soil_moisture`
- Agronomist can correct misidentified disease symptoms
- CNPC propagates corrections through the plant pathology causal model

### 4. Autonomous Systems Verification

**Application:** Verifying that autonomous vehicle perception systems make causally consistent decisions.

- If the system misidentifies a traffic sign, CNPC can propagate the correction through the full scene understanding causal graph (road type, speed limit, pedestrian presence)

---

## Insights & Implications

### Causality as a Foundation for Trustworthy CBMs

CNPC demonstrates that **causal faithfulness is not optional** for trustworthy concept-based interpretability. An interventionable model that produces causally inconsistent concept combinations is potentially harmful: it may mislead domain experts about what the model "knows" and generate explanations that appear plausible but violate domain knowledge.

### The Tractability-Faithfulness Trade-off

A key contribution is showing that **tractability and causal faithfulness are not mutually exclusive**. Prior work assumed that exact causal inference required expensive MCMC sampling. CNPC proves this is wrong by using probabilistic circuits, which offer the best of both worlds.

### Implications for the XAI Stack

CNPC occupies a unique position in the xAI landscape:
```
Data-level explanations → Feature attribution methods → Concept-level explanations → Causal explanations
                                                                ↑
                                                          CBMs/CNPC
```

By bridging concept-based and causal interpretability, CNPC suggests a natural evolution of XAI toward **causal concept reasoning** — where explanations are not just human-interpretable but causally valid.

### Open Questions

1. **Causal graph learning:** Can CNPC be extended to jointly learn the causal graph and the concept predictor from data?
2. **Soft interventions:** Can CNPC handle soft/uncertain expert corrections (e.g., "I think cᵢ is more likely X, but I'm not sure")?
3. **Counterfactual explanations:** CNPC supports interventional queries; can it be extended to counterfactual queries ("what would have changed if concept cᵢ had been different")?
4. **Concept discovery:** Can CNPC be combined with automatic concept discovery methods (CBM + TCAV) to eliminate the need for pre-specified concept sets?

---

## Code & Resources

- **ArXiv Paper:** [arxiv.org/abs/2603.01372](https://arxiv.org/abs/2603.01372)
- **Implementation:** Check paper repository (see ArXiv for GitHub link)
- **Related Library:** [ProbabilisticCircuits.jl](https://github.com/Tractable-Probabilistic-AI-Group/ProbabilisticCircuits.jl) (PC library)

### Computational Requirements

- Training: Standard CBM training overhead + PC compilation (one-time, ~minutes)
- Inference: Single forward pass through neural backbone + PC circuit (~same speed as CBM)
- GPU requirements: Standard GPU for neural backbone training

### Quick Start

```python
from cnpc import CausalNeuralProbabilisticCircuit, CausalGraph

# Define causal graph over concepts
# e.g., for birds: bill_shape → bill_length → feeding_behavior
causal_graph = CausalGraph.from_edges([
    ("bill_shape", "bill_length"),
    ("bill_length", "feeding_behavior"),
    ("wing_color", "camouflage"),
    ...
])

# Initialize CNPC (wraps a standard CBM backbone)
model = CausalNeuralProbabilisticCircuit(
    backbone="resnet50",
    concepts=concept_list,
    causal_graph=causal_graph,
    label_classes=200
)

# Training (same as CBM)
model.fit(train_loader, epochs=50)

# Inference with causal intervention
# Expert corrects concept 5 (bill_shape) from predicted 'short' to 'long_curved'
prediction = model.predict_with_intervention(
    image=test_image,
    interventions={"bill_shape": "long_curved"}
)
```

---

## Related Work & Context

### Building Upon

- **Concept Bottleneck Models (Koh et al., 2020):** The foundational CBM paper that CNPC extends
- **Probabilistic CBMs (Mahinpei et al., 2021):** Introduces probabilistic concept predictions; CNPC adds causal structure
- **Energy-Based CBMs (Xu et al., 2023):** Models concept dependencies via energy functions; CNPC replaces with tractable circuits
- **Sum-Product Networks (Poon & Domingos, 2011):** Early tractable probabilistic circuits; CNPC uses modern PC compilers

### Related 2025-2026 Work

- **Causally Reliable CBMs (2503.04363):** Concurrent work on causal consistency in CBMs; CNPC achieves exact tractability where this work uses approximations
- **Beyond Concept Bottleneck Models (2401.13544):** Survey of CBM limitations including the intervention problem addressed by CNPC
- **FaCT: Faithful Concept Traces (2510.25512):** Complementary work on faithful concept-based explanations via inherently interpretable architectures

### Connection to Broader xAI Research

CNPC connects to several active xAI research threads:
- **Causal interpretability:** Applying do-calculus and structural causal models to explain ML predictions
- **Concept-based methods:** CBMs, TCAV, concept activation vectors
- **Neurosymbolic AI:** Combining neural networks with symbolic causal reasoning
- The paper is a concrete example of the broader vision of **causally-grounded interpretable AI**, where explanations are not just humanly readable but formally correct with respect to domain causal knowledge
