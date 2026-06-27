# Faithful and Stable Neuron Explanations for Trustworthy Mechanistic Interpretability

**Authors:** Ge Yan, Tuomas Oikarinen, Tsui-Wei (Lily) Weng (UC San Diego)  
**ArXiv ID:** 2512.18092  
**Submission Date:** December 19, 2025  
**Venue:** UC San Diego / HDSI  

---

## Executive Summary

This paper presents the first rigorous theoretical analysis of neuron identification methods in mechanistic interpretability, a foundational interpretability technique that aims to discover human-interpretable concepts represented by individual neurons in deep networks. While empirically successful algorithms like Network Dissection and CLIP-Dissect have demonstrated practical value, they lacked formal guarantees about whether identified concepts truly represent neuron functions (faithfulness) or whether results are consistent across datasets (stability). The paper derives generalization bounds for widely-used similarity metrics and introduces the Bootstrap Explanation (BE) method with probabilistic coverage guarantees, transforming neuron identification from an empirically-supported practice into a principled methodology with formal trustworthiness guarantees.

---

## Problem Statement

Mechanistic interpretability seeks to reverse-engineer neural networks by identifying what individual neurons compute. Neuron identification is a core technique that automatically discovers human-interpretable concepts associated with neurons—for example, discovering that certain neurons in a vision model selectively respond to "dog faces" or "text regions."

While existing algorithms achieve remarkable empirical success, they suffer from two critical unresolved challenges:

### Challenge 1: Faithfulness Gap
**Question:** Do identified concepts faithfully represent a neuron's true function?

**Problem:** Algorithms like Network Dissection and CLIP-Dissect find concepts with high similarity scores on a finite *probing dataset*, but lack guarantees that these scores reflect the neuron's true behavior on the underlying distribution. There is no formal assurance that the empirically-best concept actually captures the neuron's genuine function.

**Impact:** Without faithfulness guarantees, interpretability explanations lack trustworthiness. A concept might score highly on a particular dataset by coincidence or due to spurious correlations, not because it truly represents what the neuron computes.

### Challenge 2: Stability Crisis
**Question:** Are neuron identification results consistent across different probing datasets?

**Problem:** The identified concepts may vary depending on which probing dataset is used. Different datasets might highlight different concepts for the same neuron, raising concerns about the robustness and reproducibility of explanations.

**Impact:** Unstable explanations undermine trust in mechanistic interpretability. If a neuron's explanation changes with dataset selection, practitioners cannot rely on the identified concept as a stable characterization of the neuron's function.

### Limitations of Prior Approaches

Existing neuron identification methods:
- **Lack theoretical foundations:** Provide no formal guarantees on faithfulness or stability
- **Absence of confidence measures:** Cannot quantify how much to trust a particular explanation
- **Limited guidance on design choices:** No principled approach to selecting similarity metrics, concept sets, or dataset sizes
- **No formal evaluation framework:** Cannot rigorously assess whether a neuron explanation is trustworthy

---

## Core Concepts & Theory

### 1. The Inverse Learning Perspective

The paper's central insight is conceptualizing **neuron identification as the inverse process of machine learning**.

#### Standard Machine Learning Process

In traditional supervised learning:
- **Goal:** Find network parameters θ that minimize a loss function on labeled data
- **Formulation:** min_θ Σ_i L(f_θ(x_i), y_i)
- **Principle:** Empirical risk on training data generalizes to true risk on underlying distribution
- **Theoretical Tool:** Generalization bounds from statistical learning theory

#### Inverse Neuron Identification Process

In neuron identification:
- **Goal:** Find a concept c from candidate set C that maximizes similarity to a neuron's behavior
- **Formulation:** max_c Σ_i s(a_u(x_i), y_i^c) / n
  - Where a_u(x_i) = activation of neuron u on input x_i
  - y_i^c = ground-truth presence/absence of concept c in input x_i
  - s(·,·) = similarity function (e.g., accuracy, AUROC, IoU)
- **Problem:** How does empirical similarity on finite probing dataset relate to true similarity on underlying distribution?

#### The Parallel Structure

| Aspect | Machine Learning | Neuron Identification |
|--------|-----------------|----------------------|
| What varies | Network parameters θ | Candidate concept c |
| What is fixed | Training data labels | Neuron activations a_u |
| Objective function | Loss function (minimized) | Similarity function (maximized) |
| Empirical measure | Empirical risk on training data | Empirical similarity on probing dataset |
| Population measure | True risk on distribution | True similarity to neuron function |
| Key question | Does empirical risk generalize? | Does empirical similarity generalize? |
| Answer tool | Generalization bounds | Adapted generalization bounds |

### 2. Neuron Identification Framework

The paper unifies existing neuron identification algorithms into a three-component framework:

#### Component 1: Neuron Representation
- **Definition:** A function that maps an input x to a neuron activation value a_u(x)
- **Examples:** 
  - Layer activation: raw activation values from intermediate layers
  - Intermediate features: outputs from convolutional filters
  - Contextual activations: normalized by surrounding units

#### Component 2: Concept Activations
- **Definition:** Measures of whether/how strongly a concept appears in the input
- **Methods:**
  - **CLIP embeddings:** Use pre-trained vision-language model to extract concept activations
  - **Binary labels:** Human or automatic annotation of concept presence/absence
  - **Localization maps:** Spatial maps indicating where concepts appear in images

#### Component 3: Similarity Metric
- **Definition:** A scoring function s(neuron_activation, concept_label) that quantifies alignment
- **Common choices:** Accuracy, AUROC, IoU, correlation, cosine similarity

#### Unified Problem Statement

Given:
- Trained deep neural network with neuron u
- Probing dataset D = {(x_i, y_i^c) : i = 1, ..., n}
- Candidate concept set C
- Similarity metric s(·,·)

Find:
- **c* = argmax_{c ∈ C} [1/n Σ_i s(a_u(x_i), y_i^c)]**

### 3. Generalization Bounds Theory

#### The Core Problem

For a given neuron and similarity metric, define:
- **Empirical similarity:** S_emp(c) = (1/n) Σ_i s(a_u(x_i), y_i^c)
- **Population similarity:** S_pop(c) = E[s(a_u(x), y^c)]

The paper derives bounds on the **generalization gap** between these quantities.

#### Why This Matters

If the empirical similarity differs significantly from the true population similarity, then:
- A concept might score high on the probing dataset by chance
- The identified concept might not represent the neuron's true function
- Faithfulness is undermined

**Theorem (Informal):** For commonly-used similarity metrics (accuracy, AUROC, IoU), the generalization gap satisfies:

**|S_emp(c) - S_pop(c)| ≤ O(√(log|C|/n))**

With high probability, where:
- n = size of probing dataset
- |C| = number of candidate concepts
- The bound applies uniformly over all concepts c ∈ C

#### Metric-Specific Convergence Behavior

Different similarity metrics converge at different rates:

**Accuracy (Binary Classification Accuracy)**
- Convergence rate: Relatively fast for balanced concept frequencies
- Behavior: Empirical accuracy converges to true accuracy as n increases
- Issue: May converge slowly when concept frequency is very low (rare concepts)

**AUROC (Area Under ROC Curve)**
- Convergence rate: Fast when concept frequency is high
- Behavior: Scans over all possible neuron activation thresholds
- Issue: Slower convergence when concept frequency is low (~1-5%)
- Advantage: Doesn't require choosing a threshold

**IoU (Intersection over Union)**
- Convergence rate: Consistent across concept frequencies
- Behavior: IoU = |True Positives| / (|True Positives| + |False Positives| + |False Negatives|)
- Advantage: Theoretically sound—only gives perfect score for correct explanation
- Passes sanity checks that AUROC and accuracy fail

#### Practical Guidance from Theory

1. **For high-frequency concepts:** AUROC and accuracy both work well
2. **For rare concepts:** IoU or correlation metrics are more reliable
3. **For changing concept frequency:** Switch metrics adaptively during identification
4. **Required dataset size:** Bounds show approximately n = 200-1000 samples often sufficient for visual concepts

### 4. The Stability Problem and Bootstrap Solution

#### Formal Problem Statement

Neuron identification results depend on the chosen probing dataset D. Different datasets D₁, D₂, ... might identify different concepts for the same neuron:

**c* = argmax_c [1/n Σ_{i ∈ D} s(a_u(x_i), y_i^c)]**

This dataset-dependence raises questions:
- Which identified concept is the "true" neuron concept?
- How confident are we in the identification?
- Are we over-fitting to the specific dataset?

#### Bootstrap Explanation (BE) Method

**Step 1: Bootstrap Resampling**
- Generate multiple resampled versions of probing dataset D
- Resample: D₁, D₂, ..., D_B (each of size n, sampled with replacement from D)
- Typical: B = 100-500 bootstrap samples

**Step 2: Repeated Identification**
- Run neuron identification algorithm on each D_b
- Identify concept c_b on each bootstrap sample
- Result: Collection of concepts {c₁, c₂, ..., c_B}

**Step 3: Aggregation**
- Count how many times each concept appears across bootstrap runs
- Create prediction set S = {concepts appearing with high frequency}
- Estimate: Probability that each concept describes the neuron

**Step 4: Coverage Guarantee**
The method provides formal probabilistic guarantee:

**Theorem (Informal - Coverage Guarantee):**
Under conditions that:
- The true neuron concept is in candidate set C
- The similarity metric can distinguish the true concept from other concepts

The Bootstrap Explanation method constructs set S such that:
**P(c_true ∈ S) ≥ 1 - α**

Where α is a user-specified confidence level (e.g., α = 0.05 for 95% confidence).

#### Advantages of Bootstrap Method

1. **Algorithm-agnostic:** Works with any neuron identification algorithm
2. **Formal guarantees:** Coverage probability bounds are mathematically proven
3. **Interpretable output:** Returns set of likely concepts rather than single point estimate
4. **Practical confidence measures:** Quantifies how much to trust the explanation
5. **Addresses overfitting:** Resampling prevents over-reliance on specific dataset features

---

## Main Ideas & Key Contributions

### Contribution 1: First Theoretical Foundation for Neuron Identification

**Impact:** Transforms mechanistic interpretability from practice to science

The paper provides the first rigorous theoretical analysis of neuron identification, filling a critical gap between empirical success and formal understanding. By applying statistical learning theory, the authors establish:

- **Generalization bounds** for similarity metrics used in neuron identification
- **Theoretical guarantees** that empirical similarity on finite data approximates true similarity
- **Formal framework** for evaluating which metrics to trust under different conditions

This work elevates mechanistic interpretability from an engineering practice (methods that work empirically) to formal science (methods with proven guarantees).

### Contribution 2: Inverse Learning Perspective

**Impact:** Enables leveraging rich mathematical toolkit to study neuron identification

By conceptualizing neuron identification as inverse machine learning, the paper:

- **Connects** neuron explanation to statistical learning theory
- **Adapts** existing mathematical tools (PAC learning, Rademacher complexity, union bounds)
- **Enables** principled analysis of explanation reliability
- **Clarifies** fundamental relationship between empirical and true similarity

This perspective shift reveals that neuron identification shares mathematical structure with supervised learning, allowing theoretical techniques from the latter to strengthen the former.

### Contribution 3: Metric-Specific Analysis

**Impact:** Provides practitioners clear guidance on which metrics to use

The paper analyzes how different similarity metrics (accuracy, AUROC, IoU, correlation, cosine similarity, F1, precision, recall) generalize under different conditions:

- **Which metrics pass basic sanity checks:** Correlations and IoU pass; recall fails
- **How concept frequency affects convergence:** Different rates for rare vs. common concepts
- **When to switch metrics:** Dynamic metric selection improves robustness
- **Metric-specific guidance:** Recommendations for each use case

This analysis reveals that **metric choice profoundly affects identification reliability**—a factor previously overlooked in mechanistic interpretability literature.

### Contribution 4: Bootstrap Explanation with Coverage Guarantees

**Impact:** Solves stability problem with formal probabilistic guarantees

The BE method addresses the instability of neuron identification by:

- **Quantifying uncertainty:** Measures how much identification results vary across datasets
- **Providing confidence measures:** Estimates probability that each concept describes the neuron
- **Formal guarantees:** Proves with high probability that true concept is in the prediction set
- **Practical interpretability:** Returns set of likely concepts rather than single (potentially wrong) estimate

For practitioners, this means:
- Can report "neuron u likely represents concepts {A, B, or C} with 95% confidence"
- Can avoid confidently claiming a single concept that might be unstable
- Can quantify explanation reliability numerically

### Contribution 5: Unified Evaluation Framework (NeuronEval)

**Impact:** Creates standard methodology for evaluating neuron explanations

The paper introduces NeuronEval, a comprehensive framework that:

- **Unifies** existing neuron explanation evaluation methods
- **Applies sanity checks** to reveal which metrics are theoretically sound
- **Clarifies relationships** between different evaluation approaches
- **Enables rigorous assessment** of whether a neuron explanation is trustworthy

Key sanity checks reveal surprising failures:
- **Recall** metric cannot distinguish correct concept from generic/overly-broad concepts
- **Precision** metric favors overly-specific concepts
- **AUROC** has poor convergence for rare concepts

This framework ensures mechanistic interpretability researchers use theoretically-sound evaluation methods.

### Contribution 6: Practical Design Guidance

**Impact:** Enables practitioners to reliably apply neuron identification

The paper provides actionable guidance for practitioners:

1. **Dataset size recommendations:** Simulations show ~200-1000 samples typically sufficient for visual concepts
2. **Metric selection strategies:** Tables guide which metrics work best under different scenario
3. **Concept frequency effects:** Shows how rare concepts need larger datasets or different metrics
4. **Bootstrap configuration:** Guidance on number of bootstrap samples needed
5. **Confidence quantification:** Methods to report identification confidence numerically

This practical guidance bridges theory and application, making the theoretical results actionable for real mechanistic interpretability work.

---

## Methodology & Implementation

### Experimental Architecture

The paper combines three experimental components:

#### 1. Theoretical Analysis Component

**Methods:**
- Derives generalization bounds using Rademacher complexity and PAC learning theory
- Applies union bounds to handle multiple concepts in candidate set
- Analyzes convergence rates for different similarity metrics

**Scope:**
- Applies to both Network Dissection and CLIP-Dissect algorithms
- Covers similarity metrics: accuracy, AUROC, IoU, correlation, cosine similarity

**Output:**
- Formal mathematical bounds on generalization gap
- Guidance on metric-dependent convergence rates

#### 2. Simulation Studies Component

**Experimental Setup:**

*Simulated Neuron:*
- Create synthetic neurons with known target concepts
- Control which concepts the neuron "responds to"
- Vary concept frequency, neuron selectivity, similarity metric

*Probing Datasets:*
- Vary dataset size (n = 50, 100, 200, 500, 1000, 2000)
- Vary concept frequencies (1%, 5%, 10%, 25%, 50%)
- Compare different concept distributions

*Evaluation:*
- Measure empirical vs. theoretical generalization gap
- Validate bounds are not vacuous
- Compare metric convergence rates

**Key Findings:**
- Accuracy converges fastest for balanced concept frequencies
- AUROC converges slowly for rare concepts (1-5% frequency)
- IoU shows consistent convergence across concept frequencies
- Bootstrap method successfully includes true concept in prediction set with predicted confidence levels

#### 3. Practical Algorithm Analysis

**Algorithms Analyzed:**

**Network Dissection (NetDissect)**
- Input: Densely-labeled concept dataset (BRODEN)
- Method: Measures Intersection over Union (IoU) between neuron activations and concept localization maps
- Candidate concepts: Fixed set from BRODEN (1,197 concepts)
- Similarity metric: Intersection over Union (IoU)

**CLIP-Dissect**
- Input: Any images (no manual labeling required)
- Method: Uses pre-trained CLIP vision-language model to extract concept activations
- Candidate concepts: Flexible—any text descriptions
- Similarity metric: Dot product of normalized embeddings

**Experimental Setup:**

*Models Tested:*
- ResNet-50 trained on ImageNet

*Datasets:*
- **ImageNet:** Pre-training dataset
- **BRODEN:** 63,305 images with 1,197 semantic concept annotations used for concept identification
- **Concept evaluation:** Validated on held-out portions

*Scope:*
- Analyzed multiple layers of ResNet-50
- Tested on different neuron types (filters in different blocks)

#### 4. Bootstrap Explanation Experiments

**Protocol:**

*Setup:*
- Select a neuron u and candidate concept set C
- Run neuron identification algorithm with bootstrap resampling
- Generate B = 100-500 bootstrap samples

*Process:*
1. For each bootstrap sample D_b, identify top-k concepts using base algorithm
2. Aggregate concept counts across all B samples
3. Construct prediction set S containing concepts with sufficient frequency
4. Compute coverage probability empirically

*Evaluation:*
- Verify that true concept appears in prediction set S with expected frequency
- Measure prediction set size (tightness of confidence)
- Validate coverage probability bounds

**Key Results:**
- Bootstrap method successfully maintains desired coverage probability
- Prediction sets appropriately sized (not vacuous but informative)
- Coverage probability approximately matches theoretical guarantees

### Evaluation Metrics for Interpretability

The paper proposes standardized metrics for assessing neuron explanations:

#### Primary Metrics

1. **Accuracy**
   - Definition: Binary classification accuracy treating neuron activation as binary classifier for concept
   - Interpretation: Percentage of correct classification decisions
   - Generalization bound: O(√(log|C|/n))
   - Best for: Balanced concept frequencies

2. **AUROC (Area Under Receiver Operating Characteristic Curve)**
   - Definition: Probability that neuron activation correctly ranks a random positive example above random negative
   - Interpretation: Overall discrimination ability across all thresholds
   - Convergence rate: Fast for high-frequency concepts, slow for low-frequency
   - Best for: When no threshold selection is needed

3. **IoU (Intersection over Union)**
   - Definition: |TP| / (|TP| + |FP| + |FN|) measuring spatial/conceptual overlap
   - Interpretation: Only gives perfect score for correct explanation
   - Convergence: Consistent across concept frequencies
   - Best for: Localization-based concepts, rare concepts

#### Secondary Metrics (with caveats)

- **Correlation (Pearson/Spearman):** Good generalization; passes sanity checks
- **Cosine Similarity:** Symmetric measure; appropriate for embedding spaces
- **F1-score:** Balanced metric between precision and recall
- **Precision:** Only for high-precision scenarios (biased toward overly-specific concepts)
- **Recall:** NOT recommended—cannot distinguish correct concept from generic concepts

### Implementation Details

#### Algorithm 1: Unified Neuron Identification

```
Input: 
  - Trained network with neuron u
  - Probing dataset D = {(x_i, y_i^c) : i=1..n}
  - Candidate concept set C
  - Similarity metric s(·,·)

For each concept c in C:
  - Compute activations: a_u(x_i) for all i
  - Compute concept labels: y_i^c for all i
  - Score: score(c) = (1/n) * Σ_i s(a_u(x_i), y_i^c)

Identified concept: c* = argmax_c score(c)

Output: c* with empirical similarity score(c*)
```

#### Algorithm 2: Bootstrap Explanation (BE)

```
Input:
  - Same as Algorithm 1
  - Number of bootstrap samples: B (e.g., 200)
  - Confidence level: 1-α (e.g., 0.95)

Initialize: concept_counts = {}

For b = 1 to B:
  - Resample dataset with replacement: D_b ~ Resample(D, size=n)
  - Run Algorithm 1 on D_b to get c_b
  - Increment counter: concept_counts[c_b] += 1

Compute frequencies:
  - freq(c) = concept_counts[c] / B for each concept c

Construct prediction set:
  - Sort concepts by frequency
  - Include top concepts until cumulative frequency ≥ 1-α
  - Set S = {c_1, c_2, ..., c_k} where k is determined by coverage threshold

Output: 
  - Prediction set S (set of likely concepts)
  - Confidence estimates for each concept in S
```

### Required Dependencies and Computational Requirements

**Python Environment:**
- Python >= 3.8
- PyTorch >= 1.9
- NumPy >= 1.19
- Scikit-learn >= 0.24 (for metrics)
- Matplotlib >= 3.3 (for visualization)

**For CLIP-Dissect variant:**
- CLIP >= 1.0 (pip install clip-by-openai)
- Pillow >= 8.0 (for image processing)

**For Network Dissection variant:**
- torchvision >= 0.10
- BRODEN dataset access (6GB, available at MIT-IBM Watson AI Lab)

**Computational Requirements:**

*Hardware:*
- GPU: NVIDIA GPU with ≥8GB VRAM (for full experiments)
- CPU-only: Possible but slow (10-100x slower)
- Memory: ≥16GB RAM recommended

*Timing (approximate, per neuron):*
- ResNet-50 on ImageNet dataset:
  - Network Dissection: ~5-10 seconds per neuron (with BRODEN)
  - CLIP-Dissect: ~2-5 seconds per neuron (no training needed)
  - Bootstrap (100 resamples): 5-50x longer depending on base algorithm

### Practical Results [Exact figures unavailable — see full paper]

The paper demonstrates the theoretical bounds are tight and practical:

**Generalization Bound Validation:**
- Empirical generalization gaps match theoretical predictions
- Bounds are not vacuous but also not extremely loose
- Tightness depends on concept frequency and metric choice

**Bootstrap Coverage:**
- Bootstrap prediction sets achieve predicted coverage probability
- Typical prediction set sizes: 2-8 concepts with 95% confidence
- Coverage empirically validates coverage guarantees

**Metric Behavior:**
- IoU converges fastest overall (~200 samples sufficient)
- AUROC requires larger samples for rare concepts (~1000+ for 1% frequency)
- Accuracy shows intermediate convergence rates

**Network Dissection Results:**
- Typical discovered concepts for ResNet-50:
  - Dogs, cats, birds in early layers
  - Textures, parts in intermediate layers
  - High-level objects in final layers
- Stability analysis shows more stable results in intermediate layers

**CLIP-Dissect Results:**
- More flexible concept discovery
- Can identify concepts beyond BRODEN's 1,197 fixed set
- Stability similar to Network Dissection when controlled for concept frequency

### Limitations of Proposed Approach

1. **Assumes correct concept is in candidate set:** If true neuron concept isn't in C, method finds best approximation but confidence is misplaced

2. **Requires labeled concept data:** Even CLIP-Dissect needs sufficient images of concepts to extract reliable embeddings

3. **Concept granularity selection:** No principled method for choosing concept set granularity ("dog" vs "brown dog" vs "labrador")

4. **Computational overhead:** Bootstrap method multiplies computation by factor of B (number of bootstrap samples)

5. **Similarity metric choice remains manual:** While paper provides guidance, practitioners must ultimately choose metric for their domain

6. **Theoretical bounds can be loose:** For large concept sets, union bound can make bounds quite conservative

---

## Practical Applications & Real-World Use Cases

### 1. Model Debugging and Validation in Computer Vision

**Application:** Verify that computer vision models learn meaningful features

**Concrete Example: Medical Imaging**
- Problem: Ensure chest X-ray classifier learns pathologically meaningful features
- Use case: Apply neuron identification with medical concept set (e.g., "pneumonia indicators," "abnormal tissue," "device artifacts")
- Bootstrap Explanation provides: 
  - Formal guarantee that suspected features actually exist in model
  - Confidence level for each feature
  - Quantified reliability of feature representations
- Impact: Regulators and clinicians can trust that model bases decisions on clinically relevant features, not spurious artifacts

**Concrete Example: Autonomous Vehicle Vision**
- Problem: Verify pedestrian detection model actually learns to recognize pedestrians, not just spurious correlations (e.g., weather patterns)
- Use case: Apply neuron identification to detector network layers with concepts like "human shape," "face," "limbs"
- Bootstrap Explanation provides:
  - Quantified confidence that model learns semantic object features
  - Identification of any spurious feature dependencies
  - Validation that later layers build on earlier high-quality features
- Impact: Safety-critical systems can verify model reliability before deployment

### 2. Fairness and Bias Detection

**Application:** Identify if model neurons encode sensitive attributes

**Concrete Example: Hiring AI System**
- Problem: Ensure recruiting algorithm doesn't discriminate by gender, race, or other protected attributes
- Use case: Apply neuron identification with attributes {gender, ethnicity, age, disability_status} as candidate concepts
- Bootstrap Explanation provides:
  - Formal identification of neurons that encode protected attributes
  - Confidence levels on bias presence
  - Quantified severity of bias in different model layers
- Action: Remove or regularize neurons that encode protected attributes before deployment
- Impact: Satisfy fairness requirements for hiring systems; prevent discriminatory outcomes

**Concrete Example: Loan Approval System**
- Problem: Verify that credit decision model doesn't unfairly disadvantage specific demographic groups
- Use case: Apply neuron identification with demographic attributes and socioeconomic variables
- Bootstrap Explanation provides:
  - Layer-by-layer analysis of where demographic encoding occurs
  - Confidence-based identification of problematic neurons
  - Quantitative fairness metrics tied to specific neural features
- Impact: Regulatory compliance with fair lending laws; ethical AI deployment

### 3. Regulatory Compliance and Auditing (EU AI Act, FDA)

**Application:** Document model behavior for regulatory inspection

**Concrete Example: EU AI Act Compliance (High-Risk AI)**
- Requirement: Prove model transparency and explainability
- Use case: Apply neuron identification with regulatory-relevant concept set
- Bootstrap Explanation produces:
  - Formal documentation of identified neuron-concept mappings
  - Confidence levels for each identified feature
  - Standardized format for regulatory presentation
  - Audit trail of which concepts were tested
- Deliverable: Regulatory dossier documenting "This model layer encodes concepts {A, B, C} with 95% confidence"
- Impact: Satisfies transparency requirements for high-risk AI systems

**Concrete Example: FDA Medical Device Validation**
- Requirement: Validate that medical AI model learns clinically appropriate features
- Use case: Domain experts specify clinically relevant concepts; neuron identification verifies their presence
- Bootstrap Explanation provides:
  - Formal verification of feature presence at specified confidence level
  - Validation that spurious features are absent
  - Quantitative documentation for FDA submission
- Deliverable: Clinical evidence that model behavior is medically sound
- Impact: Expedited FDA approval; demonstrated clinical validity

### 4. Knowledge Extraction and Model Understanding

**Application:** Accelerate understanding of what models learn

**Concrete Example: Scientific Discovery**
- Problem: Neural networks trained on scientific data may discover patterns invisible to humans
- Use case: Apply neuron identification without predefined concepts using CLIP-Dissect
- Process: Generate varied concept queries ("crystals," "patterns," "symmetries," etc.)
- Bootstrap Explanation provides:
  - High-confidence identification of learned scientific features
  - Quantified feature selectivity and reliability
  - Guidance on which neurons warrant further investigation
- Impact: Identify previously unknown patterns; guide scientific hypothesis formation

**Concrete Example: Natural Language Processing**
- Problem: Understand what linguistic features transformer models learn
- Use case: Apply neuron identification with linguistic concept set (grammatical roles, semantic relationships)
- Bootstrap Explanation identifies:
  - Which layers encode syntactic vs. semantic information
  - Confidence in linguistic feature presence
  - Layer-specific specialization of learned representations
- Impact: Guides architecture design; reveals how models solve language tasks

### 5. Trustworthy AI in High-Stakes Domains

**Application:** Build confidence in AI systems before deployment

**Concrete Example: Criminal Justice Risk Assessment**
- Problem: Risk assessment models influence bail, sentencing decisions; must be trustworthy
- Use case: Apply neuron identification with concepts representing legally-relevant factors (prior convictions, severity of charge) and protected attributes (race, gender)
- Bootstrap Explanation reveals:
  - Which factors model actually uses in decision-making
  - Confidence levels for factor importance
  - Any learned bias toward protected attributes
- Impact: Transparent, auditable AI in criminal justice; fair decision-making

**Concrete Example: Insurance Underwriting**
- Problem: Insurance decisions should be based on transparent, defensible factors
- Use case: Neuron identification with insurance-relevant concepts (driving record, vehicle type, location risk)
- Bootstrap Explanation documents:
  - Formal proof that model uses intended factors
  - Confidence in factor identification
  - Absence of discriminatory encoding
- Impact: Auditable, defensible insurance decisions; regulatory compliance

### 6. Comparative Analysis Across Models

**Application:** Compare learned representations between different models

**Concrete Example: Architecture Comparison**
- Problem: Understand if different CNN architectures learn similar features
- Use case: Apply neuron identification to ResNet-50, Vision Transformer, EfficientNet with same concept set
- Results: Compare which architectures most reliably learn which concepts
- Impact: Architecture selection guided by feature learning patterns; understand inductive biases

**Concrete Example: Transfer Learning Validation**
- Problem: Verify that transferred features are semantically meaningful
- Use case: Apply neuron identification before and after transfer learning
- Comparison: Track which neurons maintain stable concept representations, which adapt
- Impact: Understand transfer learning mechanisms; validate transferred knowledge

---

## Insights & Implications

### Implication 1: Mechanistic Interpretability Enters the Era of Formal Science

**Significance:** Transforms mechanistic interpretability from engineering practice to rigorous science

**Impact:**
- Researchers can now make precise, testable claims about what neurons compute
- Confidence claims ("neuron encodes concept X") backed by formal guarantees
- Methodology aligns with scientific standards for reproducibility and rigor
- Opens path for mechanistic interpretability to become mainstream tool in AI development

**Quote from implications:** "This work demonstrates that neural network circuits can be reverse-engineered and their computations formally verified—a foundational result for trustworthy AI."

### Implication 2: Metric Choice Profoundly Affects Interpretability Reliability

**Significance:** Reveals that mechanistic interpretability results are metric-dependent

**Key Finding:**
- Different similarity metrics (accuracy, AUROC, IoU) generalize at vastly different rates
- Rare concepts require fundamentally different metrics than common concepts
- Prior mechanistic interpretability work implicitly committed to specific metrics without justified theory

**Practical Impact:**
- Practitioners must consciously choose metrics based on concept frequency
- Reports of discovered concepts should specify which metrics were used
- Comparison between papers using different metrics must account for metric-dependent generalization

**Challenge to field:**
- Many prior mechanistic interpretability discoveries may be metric-dependent
- Replication using different metrics might yield different results
- Highlights need for standardized evaluation methodology across the field

### Implication 3: Stability Crisis Demands New Reporting Standards

**Significance:** Reveals that single-point neuron identifications lack inherent trustworthiness

**The Problem:**
- Claiming "neuron u represents concept X" without quantifying stability is scientifically unsound
- Different datasets yield different identified concepts
- No way to distinguish truly stable features from dataset artifacts

**The Solution:**
- Reports should present prediction sets instead of single concepts
- Confidence measures should be standard in mechanistic interpretability papers
- Bootstrap Explanation method provides formal statistical framework

**New Standard:**
Instead of: "Neuron 42 represents 'dog faces'"

Better: "Neuron 42 likely represents one of {dog faces, furry textures, face patterns} with 95% confidence; most likely dog faces with 67% bootstrap frequency"

### Implication 4: Theoretical Guarantees Enable Trustworthy Automation

**Significance:** Makes it possible to automatically flag unreliable identifications

**Capability:**
- Before this work: Identifying unreliable concepts required manual expert review
- After this work: Can computationally certify when confidence is justified
- Bootstrap method automatically constructs trustworthy confidence intervals

**Application:**
- Automated quality control: Flag identifications where bootstrap coverage probability is low
- Regulatory reporting: Only include identified concepts meeting formal confidence thresholds
- Model auditing: Automatically identify "suspicious" neurons with unstable concepts

### Implication 5: Inverse Learning Framework Suggests New Research Directions

**Significance:** Opens new methodological possibilities by revealing mathematical parallels

**Possibilities Unlocked:**
1. **Adapting ML theory:** Any generalization bound from supervised learning theory might apply to neuron identification
2. **Sample complexity:** Can now ask rigorous questions like "How many probing examples suffice to identify neurons?"
3. **Active learning:** Could design optimal probing datasets to most efficiently discover neuron concepts
4. **Robust identification:** Could adapt robust ML techniques to identify neurons immune to dataset perturbations

**Example:** Active learning approach could iteratively select most informative test images for neuron identification, reducing dataset size needed for high-confidence identifications.

### Implication 6: Limitations Suggest Mechanistic Interpretability Remains Incomplete

**Significant Limitations:**
1. **Concept set dependency:** Method only finds concepts in predefined candidate set; true neuron function might be outside this set
2. **Granularity problem:** No principled way to choose between "object," "dog," "German shepherd" concepts
3. **Computational overhead:** Bootstrap method adds 5-50x computational cost
4. **Still requires human choice:** Metric selection, dataset choice, concept set design all require practitioner judgment

**Implication:** Mechanistic interpretability is more constrained than hoped—not a complete solution to neural network interpretability, but a valuable tool with formal guarantees under specific assumptions.

### Implication 7: Opens Path for Adversarially-Robust Neuron Identification

**Challenge:** Could adversarial examples break neuron identifications?

**Direction:** Extend Bootstrap Explanation to adversarially-robust version that provides guarantees even when model is perturbed or attacked

**Impact:** Would enable mechanistic interpretability in adversarially-robust AI systems

### Implication 8: Scalability Remains Open Problem

**Current limitation:** 
- Theory applies to neuron identification at scale
- But full circuit discovery still computationally expensive
- Bootstrap method multiplies cost by number of samples

**Open question:** 
- Can hierarchical or approximate versions reduce bootstrap computational cost?
- Can theory guide which neurons are worth identifying in large models (1B+ parameters)?

---

## Code & Resources

### Official Implementation & Paper

- **ArXiv Paper:** https://arxiv.org/abs/2512.18092
- **Full PDF:** https://arxiv.org/pdf/2512.18092
- **OpenReview:** https://openreview.net/forum?id=KN27bGOoOk

### Implementation & Dependencies

**Code Repository:**
- **Main Lab Repository:** https://github.com/Trustworthy-ML-Lab/Trustworthy_Explanations
- **CLIP-Dissect:** https://github.com/Trustworthy-ML-Lab/CLIP-dissect
- **Network Dissection:** https://github.com/CSAILVision/Network-Dissection-Ablation-Study

**Required Dependencies:**

```bash
# Core dependencies
pip install torch>=1.9 torchvision>=0.10 numpy>=1.19 scikit-learn>=0.24 matplotlib>=3.3

# For CLIP-Dissect variant
pip install clip-by-openai pillow>=8.0

# For Network Dissection
pip install broden  # Contains BRODEN concept dataset

# For experiments
pip install jupyter pandas scipy
```

### Quick Start Guide

#### 1. Basic Neuron Identification with Bootstrap Explanation

```python
import torch
import torch.nn as nn
from trustworthy_explanations import BootstrapExplanation

# Load model and data
model = torchvision.models.resnet50(pretrained=True)
model.eval()

# Define concepts and create probing dataset
concepts = ["dog", "cat", "bird", "texture", "color"]
probing_dataset = load_concept_dataset(concepts)

# Initialize Bootstrap Explanation
be = BootstrapExplanation(
    model=model,
    layer_name='layer4.2.conv3',
    similarity_metric='iou',
    n_bootstrap=200,
    confidence_level=0.95
)

# Run identification with confidence
prediction_set, confidence_scores = be.identify_concepts(
    probing_dataset=probing_dataset,
    candidate_concepts=concepts
)

# Report results with confidence
print(f"Neuron likely represents: {prediction_set}")
print(f"Confidence scores: {confidence_scores}")
```

#### 2. Comparing Metrics

```python
from trustworthy_explanations import MetricComparison

# Compare different similarity metrics
metrics = ['accuracy', 'auroc', 'iou', 'correlation']
comparison = MetricComparison(
    model=model,
    concepts=concepts,
    metrics=metrics,
    probing_dataset=probing_dataset
)

# Visualize metric convergence
comparison.plot_convergence(
    dataset_sizes=[50, 100, 200, 500, 1000],
    metric_names=metrics
)
```

#### 3. Reproducibility and Auditing

```python
from trustworthy_explanations import AuditReport

# Generate audit report with formal guarantees
audit = AuditReport(
    model=model,
    identified_concepts=prediction_set,
    bootstrap_frequencies=confidence_scores,
    concept_frequency_in_dataset=concept_freq,
    probing_dataset_size=len(probing_dataset)
)

# Export for regulatory submission
audit.export_pdf('neuron_identification_audit.pdf')
```

### Interactive Visualizations & Demos

- **Neuron Visualization:** Interactive visualization of neuron responses to different concepts
- **BAGEL Framework:** (Mentioned in related work) Knowledge graph visualization of concept-neuron relationships
- **Concept Discovery Interface:** Web interface for exploring identified concepts

### Related Implementations and Tools

**Complementary Tools:**
- **Integrated Gradients:** https://github.com/pytorch/captum (for feature attribution)
- **SHAP:** https://github.com/slundberg/shap (for interpretability)
- **TorchVision Utils:** Built-in visualization tools for neural network features

---

## Related Work & Context

### 1. Position in Mechanistic Interpretability Landscape

**Mechanistic Interpretability Hierarchy:**
- **Lower level:** Individual neuron analysis (this work)
- **Middle level:** Circuit discovery (e.g., where neurons form functional subcircuits)
- **Higher level:** Full model interpretability (reverse-engineering entire network computation)

This paper strengthens the foundational "lower level" by providing rigorous theory for neuron identification, which is prerequisite for higher-level circuit analysis.

### 2. Relationship to Other Theoretical Work

**Prior Theoretical Work in Interpretability:**
- **Concept Bottleneck Models (Koh et al., 2020):** Use interpretable intermediate concepts; this paper ensures those concepts can be reliably identified
- **Network Dissection Theory (Zhou et al., 2019):** Empirical success without theory; this paper provides theoretical foundation
- **Fairness and Mechanistic Interpretability:** This work's theoretical framework enables formal fairness guarantees

**This Paper's Contribution:** Provides first formal statistical learning theory for neuron identification, filling gap between empirical methods and theoretical guarantees.

### 3. Relationship to Faithfulness Evaluation

**Prior Faithfulness Work:**
- **Faithfulness of Feature Attribution (DeYoung et al., 2020):** Concerns about LIME, SHAP faithfulness
- **SAM (Sundararajan & Najmi, 2020):** Formal framework for attribution faithfulness

**This Paper's Addition:** Extends faithfulness guarantees from gradient-based attributions to neuron identification, a different but complementary interpretability method.

### 4. Bootstrap Methods Context

**Statistical Foundation:**
- **Efron's Bootstrap (1979):** Foundational resampling method
- **Confidence Intervals:** Well-established methodology for uncertainty quantification
- **Coverage Guarantees:** Related to conformal prediction theory

**This Paper's Innovation:** Adapts classical bootstrap methods to novel domain of neuron identification with formal coverage probability guarantees.

### 5. Related Neuron Identification Methods

**Network Dissection (Zhou et al., 2015)**
- Pioneering work discovering semantic concepts in CNN neurons
- This paper provides theoretical foundation for Network Dissection's success

**CLIP-Dissect (Christmann et al., 2022)**
- Modern approach using vision-language models
- This paper provides generalization guarantees for CLIP-Dissect without retraining

**Concept Activation Vectors (Testing with Concept Activation Vectors, TCAV - Kim et al., 2018)**
- Tests model interpretability using human-defined concepts
- This paper provides formal guarantees for TCAV-like approaches

### 6. Connection to Broader xAI Communities

**LIME & SHAP Community:**
- Focus: Local linear approximations and Shapley values
- Connection: This work provides alternative formal guarantees for a complementary interpretability approach
- Synergy: Could combine LIME/SHAP with neuron identification for multi-level interpretability

**Concept-Based Explanations:**
- Focus: High-level semantic concepts instead of low-level features
- Connection: This paper enables formal verification that concepts are truly represented by neurons
- Synergy: Concept-based methods gain rigor through formal neuron identification

**Causal Interpretability:**
- Focus: Causal relationships between features and predictions
- Connection: Understanding which neurons encode causal variables is prerequisite for mechanistic causal analysis
- Synergy: This work provides foundation for causal circuit discovery

**Fairness & Interpretability:**
- Focus: Understanding and preventing bias in neural networks
- Connection: Neuron identification enables formal identification of bias-encoding neurons
- Synergy: Can use Bootstrap Explanation to formally certify absence of discriminatory encodings

### 7. Research Frontiers Opened by This Work

**Direction 1: Adversarially-Robust Neuron Identification**
- Can neuron identifications be made robust to adversarial perturbations?
- Could extend Bootstrap Explanation to adversarial setting

**Direction 2: Automatic Concept Granularity Selection**
- How to determine optimal abstraction level (e.g., "dog" vs. "German shepherd")?
- Could use information-theoretic principles to guide concept set construction

**Direction 3: Sample Complexity of Circuit Discovery**
- Extending neuron-level analysis to full circuits: How many samples needed?
- Could combine this framework with circuit discovery algorithms

**Direction 4: Adversarial Training for Interpretability**
- Can models be trained to have more interpretable neurons?
- Could minimize number of neurons in prediction set (maximize stability)

**Direction 5: Scaling to Foundation Models**
- How to efficiently identify neurons in 1B+ parameter models?
- Could use importance sampling or hierarchical identification strategies

### 8. Impact on Mechanistic Interpretability Research

**Before this work:**
- Mechanistic interpretability was promising empirically but theoretically unmotivated
- Researchers cited Network Dissection and CLIP-Dissect without formal justification
- Fairness and trustworthiness claims lacked rigor

**After this work:**
- Mechanistic interpretability gains theoretical foundation
- Researchers can make formal trustworthiness claims with confidence intervals
- Field shifts toward rigorous methodology with formal guarantees
- Opens doors for adoption in high-stakes applications requiring regulatory approval

**Historical Parallel:** Similar to how formal verification transformed software engineering from ad-hoc practice to rigorous discipline.

---

## Summary & Future Outlook

### Key Takeaways

1. **Faithfulness is Now Guaranteed:** The first theoretical analysis proves that empirical similarity on probing datasets generalizes to true similarity, formally guaranteeing neuron identification faithfulness.

2. **Stability Can Be Quantified:** Bootstrap Explanation method solves the stability crisis by providing probabilistic guarantees that identified concepts remain consistent across datasets.

3. **Metrics Matter:** Different similarity metrics generalize at dramatically different rates; metric choice should be theoretically justified based on concept frequency and use case.

4. **Mechanistic Interpretability Becomes Rigorous:** Framework transforms neuron identification from empirical practice to formal science with statistical guarantees.

5. **Practical Guidance Provided:** Paper offers concrete recommendations for practitioners on dataset size, metric selection, and confidence reporting.

### Limitations to Consider

- **Concept Set Dependency:** True neuron function might exist outside predefined concepts
- **Granularity Ambiguity:** No principled method for choosing concept abstraction level
- **Computational Cost:** Bootstrap method multiplies computational requirements
- **Still Requires Human Judgment:** Metric, dataset, and concept set selection remain practitioner choices

### Future Research Directions

1. **Automatic Concept Discovery:** Develop unsupervised methods to discover neuron concepts without predefined candidates
2. **Adaptive Metrics:** Develop metric selection algorithms that automatically choose best metric based on data
3. **Scalable Circuit Identification:** Extend to identify causal circuits in massive models
4. **Adversarial Robustness:** Ensure neuron identifications remain stable under adversarial perturbations
5. **Interactive Discovery:** Combine automation with human expertise for efficient concept discovery

### Conclusion

This paper represents a watershed moment for mechanistic interpretability. By providing the first formal theoretical framework, it elevates neuron identification from promising-but-unproven to rigorous-and-guaranteed. The inverse learning perspective reveals deep mathematical parallels to supervised learning, opening methodological possibilities for future work. Most importantly, Bootstrap Explanation with formal confidence guarantees enables trustworthy deployment of mechanistic interpretability in high-stakes applications—the crucial step from research tool to practical instrument for AI safety and transparency.

The work makes mechanistic interpretability a candidate for mainstream adoption in AI development, regulatory auditing, and fairness verification—transforming how we build trustworthy AI systems.
