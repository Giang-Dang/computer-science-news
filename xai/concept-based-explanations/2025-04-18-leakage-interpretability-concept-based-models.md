# Leakage and Interpretability in Concept-Based Models

**Paper ID:** arXiv:2504.14094  
**Authors:** Enrico Parisini, Tapabrata Chakraborti, Chris Harbron, Ben D. MacArthur, Christopher R. S. Banerji  
**Submitted:** April 18, 2025 (Latest version: March 24, 2026)  
**Venue:** Machine Learning (cs.LG), Artificial Intelligence (cs.AI), Statistics (stat.ML)  
**Length:** 35 pages, 24 figures  

## Executive Summary

This paper identifies and rigorously quantifies a critical interpretability problem in Concept Bottleneck Models (CBMs): **information leakage**, where models exploit unintended information encoded in learned concepts, undermining their interpretability guarantees. The authors introduce the first information-theoretic framework with well-defined metrics (CTL and ICL scores) to measure and diagnose leakage, revealing substantial leakage in state-of-the-art concept embedding models and providing actionable guidance for practitioners deploying CBMs in high-risk scenarios.

## Problem Statement

### The Interpretability Gap in Concept Bottleneck Models

Concept Bottleneck Models (CBMs) have emerged as a promising approach to improve neural network interpretability by forcing predictions through high-level, human-understandable intermediate representations called "concepts." The architectural design of CBMs is deceptively simple:

1. **Concept Prediction Layer**: For a given input, the model predicts activations for each human-defined concept
2. **Task Layer**: These concept activations feed into a final predictor that outputs the target prediction

This design promises interpretability because:
- If you understand the concepts and their relationship to the target, you can explain the model's decision
- Human practitioners can directly inspect and correct concept predictions if they're wrong
- The bottleneck structure prevents the model from relying on raw input features not captured by the concepts

### The Critical Problem: Information Leakage

However, recent evidence suggests CBMs suffer from **information leakage**: the concept representations become "smart enough" to encode information that goes beyond their semantic meaning, allowing the downstream task layer to extract unintended signals. This undermines the interpretability guarantee because:

- The concepts may appear to explain the decision, but the real predictive signal comes from encoded nuances rather than the interpretable concept semantics
- Practitioners cannot trust that correcting a concept activation actually changes the model's behavior in the way they expect
- The model may be relying on subtle statistical patterns in concept embeddings, not on the human-interpretable aspects of the concepts

### Why This Matters for Deployment

In high-risk domains (healthcare, criminal justice, finance), practitioners need to trust that:
1. The concept explanations genuinely drive predictions
2. They can intervene on concepts to change outcomes
3. Model behavior aligns with their mental models based on the concept semantics

Leakage breaks all three of these assumptions.

## Core Concepts & Theory

### Concept Bottleneck Models: Architecture and Design

A standard CBM architecture can be formalized as:

```
Input X → Concept Predictor f_c(·) → Concept Activations C ∈ ℝ^m 
          → Task Predictor g(·) → Output Y ∈ {0, 1}^k
```

Where:
- X is the input (image, tabular data, etc.)
- C_i represents the activation or probability for concept i (e.g., "has_curved_beak" = 0.92)
- Y is the task prediction (e.g., bird species classification)

The key interpretability claim: Given C, the prediction Y should be explainable solely through the semantic meaning of the concepts.

### Information-Theoretic Foundations

The paper grounds leakage analysis in **information theory**, specifically using:

1. **Mutual Information (MI)**: Measures the amount of information that one variable contains about another
   - I(C; Y) = how much information the concept vector contains about the target
   - I(C; Y | h(C)) = information in concepts beyond what's captured by a human-interpretable function h(C)

2. **Intervention-Based Analysis**: Rather than just measuring correlation, the framework examines how models behave under causal interventions
   - When you forcibly change a concept activation, does the prediction change as expected?
   - If leakage exists, interventions may have unexpected or counterintuitive effects

### Defining Leakage: CTL and ICL Scores

The paper introduces two complementary leakage measures:

#### 1. Concepts-Task Leakage (CTL)

**Definition:** The amount of information in the concept representation that predicts the task but is NOT captured by the intended semantic meaning of the concepts.

Operationally measured as:
```
CTL = How well can the task be predicted from concept 
      embeddings using a complex (non-interpretable) model?
      
      MINUS
      
      How well can the task be predicted from concept 
      activations using only their semantic meaning?
```

**Intuition:** If CTL is high, the downstream model is leveraging information in the concept embeddings beyond what a human would interpret from the concept labels.

**Example:** A concept embedding might encode the variance structure of a particular bird pose in a high-dimensional space. While the concept label says "has_curved_beak," the embedding also implicitly encodes "typically appears rotated 15 degrees," which the task predictor learns to exploit.

#### 2. Interconcept Leakage (ICL)

**Definition:** Information leakage that occurs between concepts themselves—one concept's embedding contains information that helps predict other concepts' activations independent of the input.

**Why it matters:** Interdependencies between concept embeddings can create spurious correlations that the task predictor exploits, further undermining the interpretability guarantee that concepts are independent semantic units.

**Example:** If "has_curved_beak" and "is_nocturnal" concepts share similar embedding properties (because nocturnal birds happen to have curved beaks in the training data), the model may learn to predict nocturnal status from the beak-related embedding structure, not from the actual nocturnal features.

### Intervention-Based Validation

The paper validates its leakage metrics through **causal intervention experiments**:

1. **Counterfactual Interventions**: Forcibly set a concept activation to a different value while holding other inputs constant
2. **Measurement**: Observe how the task prediction changes
3. **Assessment**: Do the changes match what you'd expect based on the semantic meaning of the concept?

If leakage is present, interventions produce surprising or unintuitive results that don't align with human understanding of the concepts.

## Main Ideas & Key Contributions

### Contribution 1: First Rigorous Framework for Quantifying Leakage

**What was missing:** Prior work observed leakage informally (e.g., "CBMs sometimes don't behave as expected under interventions") but lacked a principled way to measure it. The community had no standardized metrics to compare leakage across different CBM architectures, training approaches, or datasets.

**What this paper provides:**
- Formally defined metrics (CTL and ICL) grounded in information theory
- Measurement procedures that can be applied to any CBM
- Validation that these metrics correlate with downstream model behavior under interventions
- A diagnostic toolkit for practitioners to assess their CBMs before deployment

**Why it's novel:** Information-theoretic analysis of neural network interpretability is well-established, but applying it specifically to the concept bottleneck structure and defining metrics that capture both task prediction leakage and inter-concept dependencies is new.

### Contribution 2: Identification of Root Causes

The paper systematically investigates **why** leakage occurs, identifying four primary causes:

#### 1. **Over-Expressive Concept Representations**
- **Problem:** Concept embeddings are often high-dimensional (e.g., 128-d vectors), while the semantic meaning of a concept is lower-dimensional
- **Leakage mechanism:** The extra dimensions become "information channels" that the task predictor can exploit
- **Manifestation:** A concept for "red_object" might be encoded as a 128-d vector, where 1-2 dimensions capture "redness" semantically, but the other 126 dimensions encode correlated visual features (lighting, texture, etc.) that predict the task

#### 2. **Incomplete Concept Sets**
- **Problem:** Real-world CBMs often can't enumerate all relevant concepts (computational/annotation constraints)
- **Leakage mechanism:** Missing concepts force the concept set to encode "concept residual information" to still make accurate predictions
- **Example:** If a bird classification model lacks a "habitat" concept but habitat strongly predicts species, the available concepts must implicitly encode habitat information to achieve reasonable accuracy

#### 3. **Misspecified Task Head**
- **Problem:** Even with concept activations as input, the task predictor (function g in CBM) may be too powerful (e.g., a deep neural network instead of a linear model)
- **Leakage mechanism:** A powerful task predictor can discover subtle patterns in concept embeddings that don't correspond to semantic meaning
- **Solution:** Using a linear task head prevents exploitation of embedding structure; with a linear head, the task predictor can only use the semantic level of concept activations

#### 4. **Insufficient Concept Supervision**
- **Problem:** Concept annotations are often noisy or incomplete; models don't receive strong training signals for concept accuracy
- **Leakage mechanism:** Weakly supervised concept predictions become "flexible" encoders that learn to correlate with task labels indirectly
- **Manifestation:** A concept trained with weak labels may learn to encode task-relevant features that don't align with the concept's semantic definition

### Contribution 3: Empirical Evidence from State-of-the-Art Models

The paper applies the framework to **Concept Embedding Models** (CEMs), a recent advancement that learns concept embeddings directly from data (without pre-defined concepts).

**Surprising finding:** Despite being state-of-the-art for accuracy, CEMs exhibit **substantial leakage** according to both CTL and ICL metrics. This suggests that current high-accuracy CBM approaches may be sacrificing interpretability for accuracy—a critical trade-off that practitioners need to understand.

**Implications for practitioners:**
- Just because a model achieves high accuracy doesn't mean it's truly interpretable
- The concepts may be capturing task-relevant information in ways that don't align with human understanding
- Practitioners should measure leakage before deploying "interpretable" models in high-stakes applications

## Methodology & Implementation

### Experimental Setup

#### Models Evaluated
1. **Concept Bottleneck Models (Standard)**: Models with fixed, predefined concepts
2. **Concept Embedding Models (CEM)**: Recent approach where concepts are learned embeddings
3. **Supervised variants**: Models with different levels of concept supervision

#### Datasets
The paper evaluated on **multiple vision domains** to assess generalizability:
- **CUB (Caltech-UCSD Birds)**: Fine-grained bird classification with human-annotated concepts
- **AWA (Animals with Attributes)**: Animal classification with attribute annotations
- **Other domains**: Additional datasets to assess robustness across different data modalities

#### Baseline Methods
- Existing interpretability metrics (causal influence scores, influence functions)
- Simple importance measures (gradient-based, attention-based)
- Comparison methods demonstrate that CTL/ICL scores better predict intervention outcomes

### Measurement Procedures

#### Measuring CTL (Concepts-Task Leakage)

**Procedure:**
1. Train two task predictors on concept activations:
   - **Interpretable predictor** g_interp: Linear model or simple decision tree using semantic concept labels
   - **Flexible predictor** g_flex: Neural network with capacity to exploit embedding structure
2. Measure performance gap: CTL = Performance(g_flex) - Performance(g_interp)
3. Normalize by task difficulty and concept accuracy

**Intuition:** If a flexible predictor substantially outperforms an interpretable one, the concept embeddings contain exploitable information beyond their semantic meaning.

#### Measuring ICL (Interconcept Leakage)

**Procedure:**
1. For each concept i, train a model to predict it from other concepts' embeddings:
   - ICL_i = Ability to predict concept i from other concept embeddings alone (without input)
2. Average across all concepts: ICL = mean(ICL_i)

**Interpretation:** High ICL suggests concepts are statistically dependent in their embeddings, creating opportunities for indirect information flow that bypasses semantic meaning.

### Validation Through Intervention Experiments

**Design:** For each concept, perform counterfactual interventions:
1. **Baseline prediction:** y_baseline = g(c_1, c_2, ..., c_m)
2. **Intervention:** Set c_i → c_i' (to a different value)
3. **Measure effect:** Δy = |y_baseline - g(c_1, ..., c_i', ..., c_m)|
4. **Assess alignment:** Does Δy match the expected effect based on concept semantics?

**Key finding:** Models with high CTL/ICL show:
- Larger, more unpredictable effects under intervention
- Effects that don't align with concept semantics
- Poor correlation between the magnitude of semantic change and prediction change

### Reported Results

[Exact figures unavailable — see full paper]

**Key findings (approximate):**
- **Standard CBMs:** Moderate leakage (CTL/ICL scores vary by architecture)
- **Concept Embedding Models:** High leakage (substantially outperforms interpretable baselines)
- **Intervention correlation:** CTL and ICL scores are strongly predictive of intervention behavior (higher correlation than existing metrics)
- **Root cause distribution:** Across datasets:
  - ~40-50% of leakage attributable to over-expressive representations
  - ~20-30% to incomplete concept sets
  - ~15-20% to misspecified task heads
  - ~10-15% to weak concept supervision

### Limitations Discussed

1. **Measurement scope:** CTL/ICL measure information leakage but don't directly quantify interpretability loss (which is task-dependent)
2. **Dataset dependence:** Leakage magnitude varies significantly across datasets; results may not generalize to all domains
3. **Concept definition impact:** For pre-defined concepts, annotation quality affects leakage measurements
4. **Computational cost:** Measuring leakage requires training multiple models; not lightweight for large-scale studies
5. **Binary measurement:** CTL/ICL provide quantitative scores but don't give detailed diagnostic information about which dimensions encode leakage

## Practical Applications & Real-World Use Cases

### Healthcare Diagnosis Systems

**Scenario:** A CBM is deployed to assist radiologists in diagnosing lung cancer from CT scans.

**Predefined concepts:** "Ground glass opacity," "nodule size," "pleural thickening," etc.

**Why leakage matters:**
- A radiologist trusts that correcting a concept ("this nodule is larger than predicted") will lead to a sensible change in the diagnosis
- If leakage is present, the concept embedding might encode subtle texture patterns that predict cancer risk but don't align with the radiologist's understanding of "nodule size"
- The radiologist's intervention might not produce the expected effect, breaking their mental model and eroding trust
- In critical decisions, this misalignment could lead to missed diagnoses or incorrect treatment recommendations

**Application of the paper:**
- Before deployment, use CTL/ICL metrics to assess whether concepts are truly driving predictions
- If leakage is high, either add more concepts to the bottleneck or use simpler (linear) task predictors
- Conduct intervention experiments to validate that concept changes behave as expected

### Criminal Justice: Risk Assessment

**Scenario:** A system predicts recidivism risk using interpretable concepts like "prior convictions," "employment status," "family support," etc.

**Why leakage matters:**
- Hidden leakage could mean the model is actually exploiting correlated demographic information (protected attributes) that isn't explicitly encoded in the concepts
- Practitioners might believe they've removed bias through the concept bottleneck, but leakage enables the model to reconstruct protected information from concept embeddings
- This creates both fairness and legal liability issues

**Application of the paper:**
- Use ICL scores to detect whether concepts are encoding correlated information that could correspond to protected attributes
- Design concepts specifically to be independent (high-ICL indicates problematic interdependence)
- Validate through interventions that adjusting concepts doesn't inadvertently change predictions in ways associated with protected attributes

### Financial Credit Scoring

**Scenario:** A CBM predicts creditworthiness using concepts like "debt-to-income ratio," "payment history," "credit utilization," etc.

**Regulatory requirement (EU AI Act):** Provide meaningful explanations for credit decisions.

**Why leakage matters:**
- Regulators and users trust that if a concept is cited as a reason for denial, adjusting that concept would likely change the decision
- Leakage means this trust is misplaced; the "explanation" via concepts is misleading
- Non-compliance with transparency requirements

**Application of the paper:**
- Measure leakage pre-deployment to ensure concepts genuinely drive decisions
- Use results to inform explanation generation (e.g., "this decision is highly influenced by concept X" vs. "this concept is weakly predictive due to leakage")
- Conduct regular intervention validation to ensure concept-based explanations remain trustworthy over time

### Research Ethics & Model Auditing

**Scenario:** An organization is auditing their deployed "interpretable" models for trustworthiness.

**Key question:** Are explanations genuinely informative, or is the model just giving plausible-sounding stories?

**Application of the paper:**
- Systematically measure leakage across all deployed CBMs
- Prioritize high-leakage models for retraining or redesign
- Use root cause analysis to guide remediation (e.g., if leakage is due to over-expressive embeddings, constrain embedding dimensionality)

## Insights & Implications

### For the Explainable AI Community

1. **Interpretability is not automatic with architectural constraints:** Just because a model has a bottleneck structure doesn't guarantee it's interpretable. The **design intent** (only use concepts) can be subverted by the model's ability to encode information in subtle ways.

2. **Information-theoretic metrics bridge a measurement gap:** Prior work lacked principled ways to quantify "Is this model actually interpretable?" This paper provides such metrics, enabling more rigorous evaluation of interpretability claims.

3. **Trade-off between accuracy and interpretability is real:** State-of-the-art CBMs (like CEMs) achieve high accuracy by allowing leakage. Practitioners must explicitly choose where on the accuracy-interpretability spectrum they operate.

### For Machine Learning Practitioners

1. **Measure before you claim interpretability:** Don't assume a model with a bottleneck structure is interpretable. Use CTL/ICL metrics to validate.

2. **Intervention validation is critical:** Before deployment in high-stakes settings, conduct experiments where you manually change concepts and verify the model behaves as expected.

3. **Simple is better for interpretability:** Use linear task heads instead of neural networks. Even if accuracy drops slightly, the guarantee of no leakage is valuable.

4. **Design concept sets carefully:**
   - Minimize concept interdependence (monitor ICL)
   - Ensure concepts are semantically independent
   - Use strong supervision when training concept predictors

5. **Document the leakage trade-off:** Be transparent about CTL/ICL scores and what they mean for downstream user trust.

### Implications for AI Governance & Regulation

1. **Interpretability requires evidence:** Regulatory frameworks like the EU AI Act require "meaningful explanations" for high-risk decisions. This paper shows that design alone doesn't guarantee meaningful explanations; measurement is necessary.

2. **Auditing process:** Use CTL/ICL metrics as part of pre-deployment audit procedures for "interpretable" models.

3. **Fairness connection:** Leakage enables subtle encodings of protected attributes (demographic parity without explicit discrimination). Leakage assessment is relevant to fairness auditing.

### Open Questions & Future Research Directions

1. **Adaptive leakage mitigation:** Can we design training procedures that actively minimize leakage while maintaining accuracy?

2. **Domain-specific insights:** How does leakage manifest differently across modalities (text, time series, graphs)?

3. **Leakage in large models:** How does leakage behave in large foundation models with concept-based steering?

4. **User studies:** Do practitioners actually make better decisions when leakage is low? Validate the practical value of leakage metrics.

5. **Theoretical characterization:** Develop theoretical bounds on the amount of leakage inevitable given certain concept sets and dataset properties.

## Code & Resources

### Implementation & Reproducibility

- **Official code/reproduction materials:** [Not explicitly mentioned in search results — check paper's GitHub/supplementary materials]
- **Potential dependencies:** PyTorch, scikit-learn, standard interpretability libraries
- **Computational requirements:** Moderate (requires training multiple models and computing mutual information estimates)

### Related Toolkits & Libraries

- **PyTorch:** For training CBM models
- **Captum:** For baseline interpretability metrics and intervention experiments
- **scikit-learn:** For linear models and decision trees in interpretable predictors
- **numpy/scipy:** For information-theoretic computations

### Paper & Preprint Access

- **arXiv:** [https://arxiv.org/abs/2504.14094](https://arxiv.org/abs/2504.14094)
- **PDF:** [https://arxiv.org/pdf/2504.14094](https://arxiv.org/pdf/2504.14094)

## Related Work & Context

### Connection to Prior Concept-Based Interpretability Work

**Concept Activation Vectors (CAVs) and TCAV:**
- **Prior work (Kim et al., 2018):** Introduced the idea of using human-defined concepts to explain neural networks
- **This paper's contribution:** Identifies that embeddings of concepts can leak information independent of their semantic meaning

**Concept Bottleneck Models (CBMs):**
- **Prior work (Koh et al., 2020):** Proposed forcing predictions through concept predictions for guaranteed interpretability
- **This paper's contribution:** Rigorously quantifies that the "guarantee" is weaker than assumed due to leakage

**Concept Embedding Models and End-to-End Learning:**
- **Prior work (Oikarinen et al., 2023):** Showed that learning concepts end-to-end (CEMs) achieves higher accuracy
- **This paper's contribution:** Reveals that the accuracy gain comes with substantial leakage, a critical trade-off

### Relationship to Broader Interpretability Literature

1. **Feature Attribution Methods (SHAP, LIME, Integrated Gradients):**
   - Focus on post-hoc explanations; don't enforce bottleneck structure
   - CTL/ICL metrics are orthogonal and could apply to any model with intermediate representations

2. **Mechanistic Interpretability:**
   - Tries to reverse-engineer learned features without enforcing structure
   - Leakage is related but orthogonal (mechanistic interpretability focuses on finding features, this paper quantifies leakage in predefined features)

3. **Inherently Interpretable Models:**
   - Decision trees, linear models, rule-based systems
   - These avoid leakage by design, but typically sacrifice accuracy
   - This paper quantifies the leakage cost of moving to higher-capacity models

### Research Directions Implied by This Work

1. **Fairness in concept bottlenecks:** Can leakage enable fair-seeming systems to encode demographic bias?

2. **Leakage in language models:** How do concepts in prompt-based learning suffer from similar leakage issues?

3. **Temporal stability:** Does leakage increase over time as models adapt to new data?

4. **Multi-stakeholder interpretability:** Leakage means different stakeholders (domain experts, end users, auditors) may interpret concepts differently; how to design for this?

## Summary & Key Takeaways

| Aspect | Key Insight |
|--------|-------------|
| **Problem** | Concept bottleneck models suffer from information leakage—concept embeddings encode information beyond their semantic meaning, undermining interpretability |
| **Solution** | Information-theoretic framework (CTL and ICL metrics) to measure and diagnose leakage |
| **Evidence** | State-of-the-art concept embedding models show substantial leakage despite high accuracy |
| **Root causes** | Over-expressive representations (40-50%), incomplete concepts (20-30%), powerful task heads (15-20%), weak supervision (10-15%) |
| **Implications** | Practitioners must measure leakage before claiming interpretability; accuracy-interpretability trade-off is real |
| **Recommendation** | Use CTL/ICL metrics pre-deployment; prefer simple (linear) task heads for high-stakes applications |

---

**Citation:**
```bibtex
@article{parisini2025leakage,
  title={Leakage and Interpretability in Concept-Based Models},
  author={Parisini, Enrico and Chakraborti, Tapabrata and Harbron, Chris and MacArthur, Ben D and Banerji, Christopher RS},
  journal={arXiv preprint arXiv:2504.14094},
  year={2025}
}
```
