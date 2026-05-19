# Towards Unified Attribution in Explainable AI, Data-Centric AI, and Mechanistic Interpretability

**Authors:** Shichang Zhang, Tessa Han, Usha Bhalla, Himabindu Lakkaraju  
**ArXiv ID:** 2501.18887  
**Submission Date:** January 31, 2025 (Latest version: May 29, 2025)  
**Affiliation:** Harvard Business School AI Institute, Harvard Medical School, Harvard University

---

## Executive Summary

This position paper presents a groundbreaking unified framework that demonstrates feature attribution, data attribution, and component attribution methods—traditionally studied in isolation across explainable AI, data-centric AI, and mechanistic interpretability—share fundamental technical similarities. By revealing that these seemingly distinct attribution paradigms employ similar underlying techniques (perturbations, gradients, and linear approximations), this work advocates for a more integrated theoretical foundation that can accelerate progress across all three interpretability domains and benefit both practical AI systems and foundational research.

---

## Problem Statement

The rapid advancement of machine learning has created a fragmented interpretability landscape:

- **Explainable AI (XAI)** focuses on understanding model predictions through **feature attribution** (identifying which input features influence outputs)
- **Data-Centric AI (DCAI)** emphasizes understanding data quality through **data attribution** (identifying which training examples influence model behavior)
- **Mechanistic Interpretability (MI)** investigates model internals through **component attribution** (identifying which internal neurons/layers contribute to outputs)

These three communities have developed independently with distinct terminology, methodologies, and evaluation metrics. This fragmentation creates several problems:

1. **Reinvention of Wheels:** Similar techniques are rediscovered in different fields under different names
2. **Limited Cross-Pollination:** Advances in one area are not leveraged in others
3. **Scattered Knowledge Base:** Practitioners must consult separate literature and tools for each attribution type
4. **Theoretical Fragmentation:** No unified mathematical framework explains why these diverse methods work
5. **Inefficient Resource Allocation:** Researchers working in isolation miss opportunities for synergy

---

## Core Concepts & Theory

### Attribution Methods: A Taxonomy

Attribution methods answer the fundamental question: **"What explains a model's behavior?"** This question can be asked at three different levels:

#### 1. Feature Attribution (Input-Level)
Determines the importance of input features to a prediction.

**Classic Methods:**
- **LIME (Local Interpretable Model-agnostic Explanations):** Creates local linear approximations by perturbing input features
- **SHAP (SHapley Additive exPlanations):** Uses game-theoretic Shapley values to fairly distribute prediction credit among features
- **Gradient-Based Methods:** Saliency maps compute gradients of outputs w.r.t. inputs
- **Integrated Gradients:** Accumulates gradients along a path from baseline to input

**Mathematical Foundation:**
```
Feature Importance = Attribution(f(x), x)
where x is the input, f is the model, and Attribution 
measures how changing x affects f(x)
```

#### 2. Data Attribution (Training-Level)
Identifies which training examples influenced a model's behavior.

**Classic Methods:**
- **Influence Functions:** Uses second-order Taylor approximation to estimate how removing a training sample affects predictions on test samples
- **Leave-One-Out (LOO):** Directly measures the difference in predictions when removing a training example
- **Data Valuation Methods:** Assigns values to training examples based on their contribution to model performance

**Mathematical Foundation:**
```
Data Influence = I(z_train → f(x_test))
Measures how training sample z_train affects the model's 
behavior on test sample x_test
```

#### 3. Component Attribution (Internal-Level)
Reveals how internal model components (neurons, layers, attention heads) contribute to outputs.

**Classic Methods:**
- **Ablation Studies:** Remove or disable components and observe impact
- **Neuron/Channel Attribution:** Identify which neurons are active for specific inputs
- **Layer-wise Relevance Propagation (LRP):** Backpropagates relevance scores through network layers
- **Probing:** Tests whether components encode specific information

**Mathematical Foundation:**
```
Component Contribution = f(x) - f_without_component(x)
Measures how the model's output changes when a 
component is removed or modified
```

### Unified Attribution Framework

The paper demonstrates these three attribution types employ **three core techniques**:

#### Technique 1: Perturbation-Based Attribution
Remove or modify aspects (features, data, components) and observe output changes.

**Formal Definition:**
```
Attribution = E[f(x) - f(x_perturbed)]
or
Attribution = |ΔOutput| when aspect is removed/modified
```

**Examples:**
- LIME perturbs input features
- Leave-One-Out removes training samples
- Ablation removes model components

**Advantages:** Model-agnostic, intuitive, easy to implement  
**Disadvantages:** Computationally expensive, may test unrealistic scenarios

#### Technique 2: Gradient-Based Attribution
Compute how small changes in one domain propagate through the model via gradients.

**Formal Definition:**
```
Attribution = ∂f/∂aspect
Computes the sensitivity of model output to changes in the aspect
```

**Examples:**
- Saliency maps: ∇_x f(x)
- Influence functions: ∇_z Loss(f(z), y)
- Neuron gradients: ∇_neuron f(x)

**Advantages:** Computationally efficient, mathematically principled  
**Disadvantages:** Limited to differentiable models, may suffer from saturation

#### Technique 3: Linear Approximation Methods
Fit interpretable linear models to approximate the relationship between aspects and outputs.

**Formal Definition:**
```
f(x) ≈ β₀ + Σ(βᵢ × featureᵢ)
Linear model approximates model behavior locally or globally
```

**Examples:**
- LIME: Fits local linear model to feature importance
- Shapley values: Linear aggregation of marginal contributions
- Concept-based attribution: Linear combination of concept activations

**Advantages:** Highly interpretable, theoretically grounded (game theory)  
**Disadvantages:** Approximation errors, assumes additivity

### Unification Insights

The paper reveals that these techniques can be applied across all three attribution domains:

| Attribution Type | Perturbation | Gradients | Linear Approximation |
|-----------------|-------------|-----------|-------------------|
| **Feature** | LIME, Occlusion | Integrated Gradients, Saliency | SHAP, LRP |
| **Data** | Leave-One-Out | Influence Functions | Datamodels |
| **Component** | Ablation Studies | Attention Gradients | Concept Probing |

---

## Main Ideas & Key Contributions

### 1. Theoretical Unification

**Contribution:** The paper establishes that feature, data, and component attributions are not fundamentally different, but rather applications of the same underlying techniques to different domains.

**Key Insight:** 
```
Attribution Problem = {
    Domain: [Features, Data, Components]
    Technique: [Perturbation, Gradients, Linear Approximation]
    Target: Model behavior explanation
}
```

**Why This Matters:** Advances in one domain can be directly transferred to others. For example, innovations in robust gradient-based feature attribution can be applied to data attribution and component attribution.

### 2. Cross-Domain Knowledge Transfer

**Contribution:** Demonstrates how methods from one community can benefit another.

**Examples:**
- **From XAI to DCAI:** Robustness improvements from feature attribution (e.g., handling data drift) apply to influence function robustness
- **From MI to XAI:** Sparse autoencoders from mechanistic interpretability can provide interpretable component features for feature attribution
- **From DCAI to MI:** Data valuation techniques can identify which training examples best train interpretable neurons

### 3. Unified Evaluation Framework

**Contribution:** Proposes common evaluation metrics applicable across attribution types.

**Key Metrics:**
- **Faithfulness:** Do attributions accurately reflect model behavior?
- **Sensitivity:** Do attributions change when actual influencing aspects are modified?
- **Stability:** Are attributions consistent across similar inputs?
- **Completeness:** Do attributions explain the entire model output?
- **Actionability:** Can practitioners act on the attributions to improve systems?

### 4. Identifying Research Gaps and Opportunities

**Contribution:** Highlights underexplored areas by viewing attribution holistically.

**Key Opportunities:**
1. **Integrated Attribution Pipelines:** Systems that combine feature, data, and component attribution for comprehensive model understanding
2. **Robust Attribution Methods:** Techniques that remain reliable under distribution shift across all domains
3. **Scalable Methods:** Handling large models and datasets for all attribution types
4. **Human-AI Collaboration:** Designing attribution explanations tailored to different user needs

---

## Methodology & Implementation

### Paper Structure & Research Approach

**Methodology:** Systematic literature review and comparative analysis of attribution methods across three domains

**Approach:**
1. Surveyed representative methods in each domain
2. Analyzed underlying technical approaches
3. Mapped common techniques across domains
4. Identified theoretical connections
5. Proposed unified framework

### Analysis Framework

#### Step 1: Decompose Attribution Methods
For each method (LIME, SHAP, Influence Functions, Ablation, etc.):
- Identify the core technique (perturbation/gradient/linear approximation)
- Express in unified mathematical notation
- Compare with analogous methods in other domains

#### Step 2: Identify Similarities
Group methods by:
- **Technical approach** (what technique they use)
- **Scope** (what aspects they attribute)
- **Evaluation criteria** (how performance is measured)

#### Step 3: Cross-Domain Mapping
Create correspondence tables showing:
- Which XAI methods are equivalent to DCAI methods
- How MI component attribution parallels feature attribution
- What techniques are shared across domains

### Key Methods Analyzed

**Feature Attribution Methods:**
- LIME (perturbation + linear approximation)
- SHAP (Shapley values + linear aggregation)
- Integrated Gradients (gradients)
- Occlusion (perturbation)
- Attention mechanisms (gradients)

**Data Attribution Methods:**
- Influence Functions (gradients + Taylor approximation)
- Leave-One-Out validation (perturbation)
- Data Shapley (Shapley values + linear aggregation)
- Datamodels (linear approximation)
- Tracin (gradient-based)

**Component Attribution Methods:**
- Layer-wise Relevance Propagation (gradients)
- DeconvNet (gradient-based)
- Ablation/Knockoff (perturbation)
- Concept Activation Vectors (linear probing)
- Sparse Autoencoders (linear decomposition)

### Mathematical Unification Example

**LIME Feature Attribution:**
```
Explanation(x) = argmin_g Σ L(f(x'), g(x')) × π(x, x') + Ω(g)
L: Loss (perturbation-based)
π: Proximity weight
Ω: Regularizer promoting interpretability
```

**Influence Functions (Data Attribution):**
```
I_up(z) = -∇_θ Loss(f_θ(x_test), y_test) · H_θ^-1 · ∇_θ Loss(f_θ(z), y)
Uses gradients to quantify training influence
```

**Common Pattern:** Both use loss gradients; LIME perturbs features, Influence Functions perturb training data.

---

## Practical Applications & Real-World Use Cases

### 1. Healthcare & Medical AI

**Scenario:** Predicting patient outcomes using electronic health records (EHR)

**Application of Unified Framework:**
- **Feature Attribution:** Identify which clinical variables (symptoms, lab results) drove a diagnosis prediction
- **Data Attribution:** Find which similar patient cases in training data most influenced this prediction
- **Component Attribution:** Understand which learned medical knowledge patterns the model used

**Real-World Impact:**
- Clinicians gain trust by understanding prediction rationale
- Identify when models rely on spurious features (e.g., hospital codes instead of medical severity)
- Discover data quality issues (mislabeled cases influence predictions)
- Improve model robustness by removing unreliable training examples

**Regulatory Compliance:**
- FDA AI/ML guidance requires interpretability for clinical decision support
- GDPR: Right to explanation for decisions affecting individuals
- ISO 42001: AI management systems require explainability

### 2. Financial Services & Credit Decisions

**Scenario:** Loan approval, credit scoring, fraud detection

**Application of Unified Framework:**
- **Feature Attribution:** Which financial metrics (income, credit history, debt ratio) determined loan approval?
- **Data Attribution:** Which similar applicants in historical data shaped this model?
- **Component Attribution:** What learned credit patterns drove the decision?

**Real-World Impact:**
- Fair lending compliance (ECOA, FHA): Ensure decisions aren't discriminatory
- Detect potential redlining or protected class proxies
- Identify which training data introduces bias
- Explain decisions to applicants and regulators

**Example:** If the model rejects a loan due to "low income," unified attribution reveals:
- Feature: Income is the primary factor (feature attribution)
- Data: Similar applicants with low income in training set had high default rates (data attribution)
- Component: A neural network layer learned income thresholds (component attribution)

### 3. Criminal Justice & Risk Assessment

**Scenario:** Recidivism prediction, bail decisions, sentencing recommendations

**Unified Framework Application:**
- **Feature Attribution:** Which factors (prior arrests, age, employment) influenced risk score?
- **Data Attribution:** Which historical cases most shaped this prediction?
- **Component Attribution:** What patterns did the model learn about criminality?

**Critical Use Case:** Algorithmic bias detection
- Identify disparate impact on protected groups
- Trace bias to specific training examples or learned patterns
- Understand whether decisions are based on legitimate predictive factors

### 4. Content Moderation & NLP Models

**Scenario:** Detecting toxic comments, misinformation, or harmful content

**Unified Framework Application:**
- **Feature Attribution:** Which words/phrases triggered the toxicity classification?
- **Data Attribution:** Which training examples of toxic content drove this decision?
- **Component Attribution:** Which learned semantic patterns identified harmful content?

**Real-World Impact:**
- Understand model errors and reduce false positives/negatives
- Detect when models confuse context (sarcasm, reclaimed terminology)
- Improve training data quality
- Make moderation decisions more transparent to users

### 5. Autonomous Systems & Safety-Critical AI

**Scenario:** Self-driving cars, autonomous drones, robotics

**Application of Unified Framework:**
- **Feature Attribution:** Which sensor inputs (camera, LIDAR, radar) drove the navigation decision?
- **Data Attribution:** Which training scenarios most influenced this behavior?
- **Component Attribution:** Which learned driving policies or safety constraints activated?

**Critical for Safety:**
- Understand why the system made a risky decision
- Verify that decisions follow learned safety constraints
- Identify when the model relies on unreliable sensor data
- Improve training data for edge cases

### 6. AI Governance & Regulatory Compliance

**Scenario:** EU AI Act, GDPR, sector-specific regulations (FDA, financial regulators)

**Unified Attribution for Compliance:**
- **Feature Attribution:** Proves decisions based on legitimate factors, not protected attributes
- **Data Attribution:** Identifies biased training data for removal
- **Component Attribution:** Shows the model learned appropriate decision-making patterns

**Compliance Examples:**
- **EU AI Act (Article 22):** Right to explanation for decisions with legal effects
- **GDPR (Article 13):** Transparency about automated decision-making
- **FDA Guidance:** Interpretability requirements for clinical AI
- **Basel III (Banking):** Model risk management and explainability

---

## Insights & Implications

### Broader Implications for Trustworthy AI

#### 1. Towards Integrated AI Systems
- **Current State:** Practitioners use separate tools for feature importance, data debugging, and mechanistic analysis
- **Future Vision:** Unified systems where all three attribution types are computed together for holistic understanding
- **Implication:** This reduces cognitive load and prevents contradictory conclusions

#### 2. Accelerating Interpretability Research
- **Current Challenge:** Each domain solves similar problems independently
- **Unified Approach:** Cross-domain insights accelerate progress
- **Example:** Efficiency improvements in feature attribution gradients benefit influence function computation

#### 3. Building Trustworthy ML Pipelines
- **Data Quality:** Use data attribution to identify and remove problematic training examples
- **Model Fairness:** Use feature attribution to ensure equitable decisions
- **Model Correctness:** Use component attribution to verify learned patterns are meaningful

#### 4. Enabling Stakeholder Trust
- **For Domain Experts:** Feature attribution helps validate domain knowledge in predictions
- **For Developers:** Data attribution helps debug model failures
- **For Regulators:** All three attributions provide comprehensive compliance evidence
- **For End Users:** Unified explanations are more understandable than separate explanations

### Advances to the State-of-the-Art in Explainability

#### 1. Theoretical Foundation
- **Before:** Each domain had separate theoretical foundations
- **After:** Unified mathematical framework shows deep similarities
- **Impact:** Enables proving properties that apply across all domains

#### 2. Methodological Innovation
- **Benefit 1:** Techniques from one domain can be adapted for others
  - Robust feature attribution methods → robust data attribution
  - Efficient component attribution → efficient data attribution
  
- **Benefit 2:** Comparative analysis reveals best practices
  - Which technique (perturbation/gradient/linear) works best for each problem?
  - Under what conditions should each technique be preferred?

#### 3. Practical Tool Development
- **Current:** Separate tools (SHAP for features, Influence for data, circuit analysis for components)
- **Future:** Integrated tools providing all three types of attribution
- **Benefit:** Practitioners can get complete picture with single tool

### Limitations, Failure Cases, and Open Questions

#### 1. Computational Scalability

**Limitation:** All attribution methods are computationally expensive for large models and datasets

**Feature Attribution:** Computing SHAP values requires model evaluations for each feature
- For 1000-dimensional inputs: ~1000+ model forward passes per prediction
- For large neural networks: Each forward pass is expensive

**Data Attribution:** Influence functions require Hessian computation (O(n) memory, O(n²) computation)
- Intractable for models with millions of parameters
- Approximations lose fidelity

**Component Attribution:** Comprehensive component analysis requires attributing every neuron/layer
- Transformers with billions of parameters present challenges
- Trade-off between comprehensiveness and computational cost

**Open Question:** How can we scale attribution methods to billion-parameter models?

#### 2. Approximation Quality

**Limitation:** All three techniques approximate true causal relationships

**Problem:** Perturbations might test unrealistic scenarios
- Setting pixels to zero in images creates artifacts
- Removing training examples changes data distribution
- Disabling neurons breaks learned information flow

**Consequence:** Attributions may not reflect true importance in natural scenarios

**Open Question:** How can we design perturbations that test realistic counterfactuals?

#### 3. Fairness and Bias Limitations

**Limitation:** Attribution methods cannot guarantee fairness

**Example:** Feature attribution shows a model uses "income" (legitimate) rather than "zip code" (proxy for race)
- But patterns in income distribution are racially correlated
- Removing "zip code" doesn't guarantee fairness

**Challenge:** Attributions explain what the model does, not whether it's fair

**Open Question:** How can attribution methods incorporate fairness constraints?

#### 4. Interpretability Verification

**Limitation:** Even unified attribution methods don't guarantee interpretability

**Problem:** Multiple attributions might lead to conflicting conclusions
- Features and data attributions might disagree on important inputs
- Component attribution might show learned patterns that aren't semantically meaningful

**Consequence:** Practitioners still face cognitive load in reconciling explanations

**Open Question:** How should we resolve conflicts when different attribution types disagree?

#### 5. Task-Specific Challenges

**Feature Attribution:**
- **Challenge:** Different for tabular vs. image vs. text data
- **Example:** Perturbing images is harder than removing features
- **Open Question:** Universal attribution methods or task-specific ones?

**Data Attribution:**
- **Challenge:** Assumes clean labels and stable distributions
- **Problem:** Real-world data is noisy, with distribution shift
- **Open Question:** How to handle label noise and distribution shift?

**Component Attribution:**
- **Challenge:** Models have billions of components
- **Problem:** Full attribution is infeasible
- **Open Question:** Which components to prioritize for analysis?

#### 6. Domain-Specific Gaps

**Areas Where Unification Breaks Down:**
- Black-box models (no gradients): Limited to perturbation-based methods
- Ensemble models: Component attribution is ambiguous (which component's ensemble member?)
- Active learning systems: Attribution changes as data changes
- Online learning: Models constantly update, attributions become stale

### How This Influences Future xAI Research Directions

#### 1. **Integration and Composability**
Future research should focus on:
- Building systems that combine all three attribution types seamlessly
- Understanding when to apply each type
- Handling conflicts between different attributions

#### 2. **Robustness and Reliability**
Priority areas:
- Robust attribution under distribution shift
- Certified attribution methods (with formal guarantees)
- Attribution error bounds

#### 3. **Scalability Breakthroughs**
Key challenges:
- Efficient Hessian computation for influence functions
- Approximate but reliable Shapley value computation
- Sparse attribution (only important components)

#### 4. **Human-Centered Evaluation**
Emerging direction:
- How well do unified attributions improve human decision-making?
- What visualization and presentation methods work best?
- User studies on interpretability across domains

#### 5. **Causal Interpretability**
Connecting to causal inference:
- Can we strengthen attribution claims with causal graphs?
- How do causal and statistical attributions relate?
- Causal component attribution (what components implement causal mechanisms?)

#### 6. **Fairness and Ethics Integration**
Future work should:
- Incorporate fairness constraints into attribution computation
- Detect when attributions mask unfair decisions
- Design attributions optimized for fairness (not just accuracy)

---

## Code & Resources

### Official Implementation

**Paper Repository:**
- ArXiv: https://arxiv.org/abs/2501.18887
- HTML Version: https://arxiv.org/html/2501.18887v3
- PDF: https://arxiv.org/pdf/2501.18887

**Author's Tutorial & Resources:**
- Tutorial Site: https://shichangzh.github.io/xaiTutorial/
  - Provides interactive explanations of key concepts
  - Code examples for different attribution methods
  - Practical guides for practitioners

### Key Libraries for Unified Attribution

#### Feature Attribution:
- **SHAP:** https://github.com/shap/shap
  - Unified Shapley-based feature importance
  - Supports various model types
  
- **LIME:** https://github.com/marcotcr/lime
  - Local interpretable model-agnostic explanations
  - Model-agnostic approach

- **Captum (PyTorch):** https://captum.ai/
  - Attribution methods for PyTorch models
  - Supports gradients, perturbations, deconvolution

#### Data Attribution:
- **Influence Functions:** https://github.com/kohpangwei/influence-release
  - Implementation of TracIn influence functions
  - Supports TensorFlow models

- **Data Valuation:** https://github.com/amiratag/DataShapley
  - Data Shapley implementation
  - Assigns value to training examples

#### Component Attribution:
- **Sparse Autoencoders:** https://github.com/anthropics/sae-interp
  - Mechanistic interpretability tools from Anthropic
  - Identifies learned features in neural networks

- **TransformerLens:** https://github.com/neelnayan/TransformerLens
  - Analysis tools for transformer internals
  - Head and neuron attribution

### Computational Requirements

**For Feature Attribution (SHAP/LIME):**
- CPU: 2+ cores sufficient for small models
- Memory: 1-4 GB for typical use cases
- Time: Minutes to hours depending on model and dataset size

**For Data Attribution (Influence Functions):**
- CPU: Multi-core recommended
- Memory: 8-32 GB (proportional to model parameters)
- Time: Hours to days for large datasets

**For Component Attribution (SAEs, Circuit Analysis):**
- GPU: Recommended for large models (A100 or equivalent)
- Memory: 16-80 GB depending on model size
- Time: Hours to process full model

### Quick Start Guide

#### 1. Feature Attribution with SHAP
```python
import shap
import xgboost as xgb

# Train model
model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# Create SHAP explainer
explainer = shap.TreeExplainer(model)

# Get SHAP values for test instance
shap_values = explainer.shap_values(X_test[0])

# Visualize
shap.summary_plot(shap_values, X_test)
```

#### 2. Data Attribution with Influence Functions
```python
from influence_functions import TracIn

# Compute influence of training examples on test prediction
influences = TracIn(model, train_data, test_sample)

# Identify most influential training examples
top_influences = sorted(influences.items(), 
                       key=lambda x: abs(x[1]), 
                       reverse=True)[:10]
```

#### 3. Component Attribution with SAEs
```python
from sae_interp import SparseAutoencoder

# Load SAE trained on model layer
sae = SparseAutoencoder.load("layer_5_sae")

# Get feature activations for input
features = sae.encode(hidden_states)

# Identify which features activate for this input
active_features = features[features.abs() > threshold]
```

### Interactive Visualizations and Demos

**Interactive Tutorials:**
- Distill.pub's Interpretability articles: https://distill.pub/
  - Visual explanations of attribution concepts
  - Interactive demonstrations

**Web-based Tools:**
- SHAP Force Plots: https://shap.readthedocs.io/
  - Browser-based visualization of SHAP values
  
- Captum Insights: https://captum.ai/tutorials/
  - Interactive attribution visualization

**Conference Talks:**
- NeurIPS, ICLR, ICML papers often include code and demos
- Search author names for implementation details

---

## Related Work & Context

### Connection to XAI Foundations

This paper builds on decades of interpretability research:

**Feature Attribution Pioneers:**
- **LIME (2016):** Ribeiro et al. introduced local linear approximations
- **SHAP (2017):** Lundberg & Lee unified feature importance using Shapley values
- **Integrated Gradients (2017):** Sundararajan et al. developed path-based gradient attribution
- **Influence Functions (1997):** Cook & Weisberg (influence diagnostics in statistics)
- **TracIn (2020):** Pruthi et al. adapted influence functions for deep learning

**Mechanistic Interpretability:**
- **Circuit Analysis (2021):** Olah et al.'s zoom-in approach to understanding internals
- **Sparse Autoencoders (2023):** Anthropic's method to find interpretable features
- **Attention Head Attribution:** Studying transformer internals

### Related Recent xAI Papers

**Papers Building on Unified Attribution:**

1. **"Circuit Insights: Towards Interpretability Beyond Activations" (2025)**
   - Extends unified framework to circuit discovery
   - Shows perturbation techniques work for circuits
   - Related: Mechanistic interpretability application of perturbation-based methods

2. **"Combining Causal Models for More Accurate Abstractions of Neural Networks" (2025)**
   - Uses causal abstraction with component attribution
   - Shows how to combine multiple high-level models
   - Related: Extends component attribution to causal settings

3. **"Investigating the Duality of Interpretability and Explainability" (2025)**
   - Compares inherently interpretable models vs. post-hoc explanation
   - Related: Complementary perspective on the interpretability landscape

### What Prior Interpretability Work Does It Build Upon?

**Linear Approximation Methods (LIME, SHAP):**
- Based on local linear surrogate models
- Shapley values from cooperative game theory (Shapley, 1953)
- This paper: Recognizes SHAP as specific instance of linear approximation technique

**Gradient-Based Methods:**
- Roots in backpropagation and neural network analysis
- Saliency maps (Simonyan et al., 2013)
- This paper: Shows gradient-based attribution unified across domains

**Perturbation-Based Methods:**
- Occlusion sensitivity (Zeiler & Fergus, 2013)
- Feature knockout (Bach et al., 2015)
- This paper: Identifies perturbation as core technique across all domains

**Influence Functions:**
- Statistics: Cook (1977), Weisberg (1980)
- Deep Learning: Pruthi et al. (2020) adapted to neural networks
- This paper: Shows influence functions as data-domain application of gradient-based techniques

### Where This Research Might Lead

#### Near-term (1-2 years):
1. **Integrated Attribution Tools:** Combined systems providing all three attribution types
2. **Efficiency Improvements:** Faster algorithms leveraging unified perspective
3. **Best Practice Guidelines:** Recommendations for when to use each technique

#### Medium-term (2-5 years):
1. **Causal Attribution:** Extending unified framework to causal inference
2. **Fairness-Aware Attribution:** Incorporating fairness constraints
3. **Scalability Solutions:** Methods for billion-parameter models
4. **Standardized Evaluation:** Shared benchmarks across domains

#### Long-term (5+ years):
1. **AI Safety Applications:** Using unified attribution for alignment verification
2. **Automated Debugging:** Systems that automatically identify and fix model issues using attribution
3. **Interpretable AI by Design:** Methods for building interpretable systems from ground up
4. **Human-AI Collaboration:** Attribution-guided human-AI teams

### Broader xAI Community Connections

**Major xAI Communities Impacted:**

1. **Feature Attribution Community:**
   - Tools: SHAP, LIME, Captum
   - Conferences: ICML XAI, ICLR Interpretability workshops
   - Impact: Unified framework validates existing approaches, suggests improvements

2. **Data-Centric AI Community:**
   - Focus: Data quality, bias, training data analysis
   - Tools: Label Studio, Cleanlab, data valuation systems
   - Impact: Shows data attribution is instance of perturbation/gradient techniques

3. **Mechanistic Interpretability Community:**
   - Focus: Understanding model internals, circuits, learned features
   - Organizations: Anthropic, DeepMind, academic labs
   - Impact: Identifies commonalities with feature/data attribution, enables cross-domain methods

4. **Fairness, Accountability, and Transparency (FAccT) Community:**
   - Focus: Bias detection, fairness verification, transparency
   - Conferences: FAccT, AIES, NeurIPS FAccT workshops
   - Impact: Unified framework improves fairness diagnostics across domains

5. **AI Safety and Alignment Community:**
   - Focus: Ensuring AI systems behave as intended
   - Organizations: Center for AI Safety, Alignment Research Center
   - Impact: Attribution methods crucial for understanding and verifying model alignment

### Cross-Disciplinary Connections

**From Statistics:**
- Influence diagnostics (Cook, 1977)
- Importance sampling, perturbation analysis
- Bootstrap and resampling methods

**From Game Theory:**
- Shapley values (Shapley, 1953) for fair credit allocation
- Cooperative game theory concepts

**From Economics:**
- Demand elasticity (similar to gradient sensitivity)
- Causal inference frameworks

**From Physics:**
- Perturbation theory
- Sensitivity analysis of complex systems

**From Cognitive Science:**
- How humans understand explanations
- Contrastive explanations
- Counterfactual reasoning

---

## Key Takeaways

### For Practitioners:

1. **Use Unified Thinking:** When explaining a model, consider all three levels:
   - What features drove this prediction?
   - What training data shaped the model?
   - What learned patterns activated?

2. **Leverage Cross-Domain Insights:** If you're expert in feature attribution, apply similar thinking to data and component attribution

3. **Choose Techniques Strategically:** For each problem, consider:
   - Perturbation: Easiest to understand, computationally expensive
   - Gradients: Efficient, may have saturation issues
   - Linear: Most interpretable but approximates reality

4. **Expect Complementary Insights:** Different attribution types provide different perspectives; conflicts guide investigation

### For Researchers:

1. **Theoretical Advances:** Unified framework enables proving properties across all domains

2. **Cross-Domain Transfer:** Innovations in one area (e.g., robust feature attribution) apply elsewhere

3. **Scalability Focus:** Solving computational challenges in one domain benefits all three

4. **Evaluation Standardization:** Shared metrics (faithfulness, stability, actionability) across domains

### For Organizations:

1. **Implement Holistically:** Build systems that integrate all three attribution types

2. **Invest in Interpretability:** Unified approach makes interpretability more cost-effective

3. **Prepare for Regulation:** Unified attribution supports compliance across multiple frameworks (GDPR, EU AI Act, FDA)

4. **Build Trust:** Comprehensive explanations (features + data + components) increase stakeholder confidence

---

## References

- Zhang, S., Han, T., Bhalla, U., & Lakkaraju, H. (2025). Towards Unified Attribution in Explainable AI, Data-Centric AI, and Mechanistic Interpretability. *arXiv:2501.18887*
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?" LIME: Low-Fidelity Explanations
- Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. SHAP
- Sundararajan, M., Taly, A., & Yan, Q. (2017). Integrated Gradients
- Pruthi, G., Liu, F., Kurakin, A., & Zald, I. (2020). Influence Functions Can Cause Overconfidence in Deep Learning
- Olah, C., Cammarata, N., Schubert, L., Goh, G., Petrov, M., & Carter, S. (2021). Zoom In: An Introduction to Circuits. Distill
- Anthropic. (2023). Sparse Autoencoders Find Interpretable Features in Language Models
