# Feature Attribution in Directed Acyclic Graphs Using Edge Intervention

## Executive Summary

This paper introduces DAG-SHAP, a novel feature attribution method that extends Shapley value-based explanations to causal directed acyclic graphs (DAGs) by treating feature edges rather than individual features as attribution objects. By performing edge-based interventions, DAG-SHAP captures both the externality (how features cause other features) and exogenous contributions (direct impact on the prediction) of features in a causal structure, providing more nuanced and causally-grounded explanations compared to traditional node-centric attribution methods.

## Problem Statement

Existing feature attribution methods, particularly Shapley value-based approaches like SHAP, operate under a **node-centric perspective** that treats each feature as an isolated entity. This approach has critical limitations:

1. **Failure to Model Causal Interactions**: Traditional methods do not account for causal relationships between features, even when a causal structure is known.

2. **Conflation of Causation and Correlation**: SHAP and similar methods cannot distinguish between direct causal effects and mere correlations, leading to inflated attribution scores for proxy features.

3. **Incomplete Capture of Feature Contributions**: Existing approaches fail to simultaneously capture:
   - **Externality**: How a feature influences other features within the causal structure
   - **Exogenous effects**: The direct impact of a feature on the prediction

4. **Unreasonable Interpretations**: When features are connected through causal pathways, node-centric methods produce misleading explanations that don't align with actual causal mechanisms.

### Real-World Example
In a wage prediction model with causal relationships: IQ → Education → Years of Experience → Wage, traditional SHAP might over-attribute importance to IQ (a root cause) by not accounting for its influence mediated through other variables, or conversely under-attribute it by treating it as merely correlated.

## Core Concepts & Theory

### Background: Directed Acyclic Graphs (DAGs)

A directed acyclic graph (DAG) is a graphical model where nodes represent variables and directed edges represent causal relationships. The absence of cycles ensures that causal effects can be uniquely determined.

**Key DAG Properties:**
- Each edge represents a direct causal relationship from parent to child
- A node's parents are all variables that directly cause it
- A node's descendants include all variables it causally influences (directly or indirectly)

### Shapley Values and Traditional SHAP

The Shapley value, derived from cooperative game theory, fairly distributes a game's total payoff among players based on their marginal contributions. In feature attribution, the "game" is the model prediction, and "players" are features.

**Traditional SHAP Formula:**
For a feature $i$, the Shapley value is:
$$\text{SHAP}_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(n-|S|-1)!}{n!} [f(S \cup \{i\}) - f(S)]$$

where:
- $F$ is the set of all features
- $f(S)$ is the model's output when only features in set $S$ are present
- $n$ is the total number of features

**Limitations in DAGs:**
- This assumes features are independent in the coalition formation process
- It doesn't account for causal constraints (e.g., conditioning on descendants of a variable)
- It treats correlation as causation

### Edge Intervention and Causal Analysis

The core innovation of DAG-SHAP is replacing feature intervention with **edge intervention**:

**Traditional Intervention (Node-Centric):**
Setting a feature $X_i$ to a reference value $x'_i$, breaking all its incoming and outgoing edges:
$$f(X_i = x'_i)$$

**Edge Intervention (DAG-SHAP):**
Intervening on a specific edge from parent $X_j$ to child $X_i$, denoted as $j \to i$:
- Break the direct causal pathway from $X_j$ to $X_i$
- Preserve all other causal relationships in the graph
- Allow $X_i$ to be determined by its other parents and exogenous factors

**Formal Definition:**
For an edge $j \to i$, the edge intervention is:
$$f^{\overline{j \to i}} = f(X_i^* | X_{\text{parents}(i) \setminus \{j\}})$$

where $X_i^*$ is sampled from the conditional distribution of $X_i$ given all its parents except $X_j$.

### Capturing Feature Contributions

DAG-SHAP decomposes feature importance into two orthogonal components:

1. **Exogenous Effect**: The direct influence of a feature on the prediction
2. **Mediated Effect**: The influence through causal pathways (how the feature affects other features that then affect the prediction)

This decomposition ensures that:
- A root cause receives appropriate credit for its direct impact
- The credit is not inflated by its downstream influences
- Intermediate variables receive credit for their role in mediating causal effects

## Main Ideas & Key Contributions

### 1. Edge-Based Feature Attribution Framework

**Novel Conceptualization**: Rather than treating features as atomic units, DAG-SHAP treats each feature edge as an attribution object. This shift from nodes to edges enables:

- Precise specification of which causal pathway to interrupt
- Distinction between different sources of a feature's influence
- Alignment with causal theory's emphasis on mechanisms

**Innovation**: By asking "how much does the edge from parent $X_j$ to child $X_i$ contribute to the prediction?", the method naturally decomposes feature effects along causal pathways.

### 2. Approximation Algorithm for Practical Computation

Since exact computation of edge-based Shapley values is intractable, the paper introduces an efficient approximation algorithm:

**Algorithm Overview:**
- **Sampling-based approach**: Approximate edge-wise marginal contributions through permutation sampling
- **Computational efficiency**: Use efficient coalition sampling strategies to reduce computation time
- **Scalability**: Demonstrated computation time of 57.5 seconds for 128 parallel threads processing 128 permutations per data point

**Key Algorithmic Details:**
1. Initialize edge contribution estimates to zero
2. For each permutation of edges:
   - Sequentially add edges to the coalition
   - Measure marginal contribution of each edge through edge intervention
   - Accumulate contributions across permutations
3. Average to obtain DAG-SHAP scores

### 3. Handling Causal and Confounded Scenarios

The method properly handles:

**Causal Chains**: A → B → C
- Attribution correctly flows from direct causes through mediation paths
- Doesn't double-count effects

**Confounding**: X ← Z → Y
- Confounders receive appropriate attribution
- Method distinguishes between spurious and causal associations

**Colliders**: A → C ← B
- Correctly avoids conditioning on colliders unless explicitly needed for inference

### 4. Empirical Validation Across Domains

The paper demonstrates superiority over existing methods (Causal SHAP, Off-SHAP, On-SHAP, ASV) on:
- **Census Income Data**: Predicting income based on education, age, and other demographic factors with known causal relationships
- **Labor Market Data (Griliches76)**: Explaining wage predictions using IQ, education, and job experience
- **Synthetic Data**: Controlled experiments demonstrating DAG-SHAP's theoretical correctness

## Methodology & Implementation

### Experimental Setup

**Datasets:**

1. **Census Income Dataset (Adult Dataset)**
   - **Features**: Age, education level, occupation, income, etc.
   - **Target**: Binary classification (income > $50K)
   - **Causal Graph**: Derived from established sociological research on income determinants
   - **Models Tested**: Deep Neural Network (DNN) and XGBoost

2. **Griliches76 Labor Economics Dataset**
   - **Features**: IQ, education level (EDU), years at current job (YEAR)
   - **Target**: Log-transformed weekly income
   - **Causal Structure**: IQ → EDU → YEAR → Wage
   - **Sample Size**: Limited to demonstrate precision on small-scale problems
   - **Models Tested**: DNN and XGBoost

3. **Synthetic Datasets**
   - Generated to validate theoretical properties
   - Control feature distributions and causal relationships
   - Test edge cases and potential failure modes

### Evaluation Metrics

**Primary Metric: Mean Absolute Error (MAE)**
$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |\text{DAG-SHAP}_i - \text{Benchmark}_i|$$

where the benchmark is determined through:
- Ground truth values from synthetic data
- Established causal relationships on real data
- Comparison against alternative methods

**Secondary Metrics:**
- **Computational Efficiency**: Wall-clock time for explanation generation
- **Scalability**: Performance as number of edges and features increases
- **Stability**: Consistency of attributions across random seeds and perturbations

### Results and Performance Comparisons

#### Census Dataset Results

**DNN Model:**
- **DAG-SHAP MAE**: [Exact figures unavailable — see full paper]
- **Performance Relative to Baseline**: 57.1% of second-best method's error
- **Comparison**: Significantly outperforms Causal Shapley Value method

**XGBoost Model:**
- **DAG-SHAP MAE**: 0.40
- **Causal SHAP**: 0.52
- **Off-SHAP**: 0.59
- **On-SHAP**: 1.59
- **ASV (All-Subsets)**: 2.11

**Interpretation**: DAG-SHAP's ~23% improvement over Causal SHAP demonstrates the value of edge-level attribution granularity.

#### Griliches76 Dataset Results

**DNN Model:**
- **DAG-SHAP MAE**: 0.08 (ranked first)
- **Off-SHAP**: 0.27
- **Causal SHAP**: 0.52
- **ASV**: 1.76
- **On-SHAP**: 2.44

**XGBoost Model:**
- [Exact figures unavailable — see full paper]

**Interpretation**: DAG-SHAP achieves >3× lower error than competing methods on the Griliches76 dataset, validating its effectiveness on causal income prediction tasks.

#### Computational Performance

**Configuration**: 128 parallel threads

**Sampling Parameters:**
- 128 permutations: MAE = 5.17%, Runtime = 57.5 seconds
- 256 permutations: MAE = 4.23%, Runtime ≈ 115 seconds (estimated)
- 384 permutations: MAE = 3.71%, Runtime ≈ 172 seconds (estimated)

**Scalability Analysis**:
- Error decreases with more permutations (law of large numbers)
- Computational cost scales linearly with number of permutations
- Parallelization enables practical deployment

### Limitations of the Approach

1. **Requires Known DAG**: Method assumes the causal structure is known or reliably estimated; misspecified DAGs degrade performance

2. **Computational Cost**: Even with approximation, requires multiple permutations; expensive for large numbers of edges

3. **Limited to DAG Structures**: Cannot handle cycles (feedback loops) or time-series causal processes without modification

4. **Background Distribution Dependence**: Results depend on choice of background dataset for computing counterfactual distributions

5. **No Uncertainty Quantification**: Confidence intervals or statistical significance tests for attribution scores are not provided

## Practical Applications & Real-World Use Cases

### Healthcare and Medical Diagnostics

**Application**: Explaining clinical risk prediction models for patient stratification

**Example**: Predicting patient hospital readmission risk
- **Causal Graph**: Comorbidities → Disease Severity → Treatment Choice → Readmission
- **Benefit**: DAG-SHAP can distinguish between:
  - Direct effect of treatment on readmission (exogenous)
  - Indirect effect through disease remission (mediated)
- **Regulatory Advantage**: Aligns with FDA's preference for mechanistic interpretability in clinical AI

**Real-World Impact**: Helps clinicians understand not just what matters, but why and how it matters causally

### Finance and Risk Management

**Application**: Credit scoring and loan default prediction

**Example**: Predicting mortgage default
- **Causal Graph**: Income → Savings Rate → Existing Debt → Payment History → Default Risk
- **Benefit**: Identify which interventions would actually reduce risk:
  - Increasing income (root cause) vs. reducing existing debt (downstream)
  - Different strategies for different borrowers
- **Regulatory Requirement**: Basel III and fair lending regulations require understanding causal mechanisms for credit decisions

### Autonomous Systems and Robotics

**Application**: Explaining decision-making in safety-critical systems

**Example**: Autonomous vehicle collision avoidance
- **Causal Graph**: Pedestrian Distance → Braking Intensity → Collision Risk
- **Benefit**: Understand whether the system's decision was based on:
  - Direct danger assessment (pedestrian distance)
  - Learning from past incidents (mediated through training data)

### Criminal Justice and Legal Systems

**Application**: Explainable risk assessment for judicial decisions

**Example**: Recidivism prediction
- **Known Issue**: Traditional SHAP may conflate correlation with causation (e.g., proxy variables)
- **DAG-SHAP Solution**: Properly separate causal factors from proxies
- **Regulatory**: Supports compliance with algorithmic fairness requirements in sentencing

### Environmental and Climate Science

**Application**: Understanding climate model predictions

**Example**: Regional temperature prediction
- **Causal Graph**: Greenhouse Gas Emissions → Atmospheric CO₂ → Temperature Rise → Precipitation Changes
- **Benefit**: Attribute importance along known causal chains
- **Policy Impact**: Identify which interventions (reducing emissions at different sources) have the strongest effects

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Causality as Accountability**: By grounding explanations in causal mechanisms rather than correlations, DAG-SHAP supports true accountability. Organizations can explain not just "what" was predicted but "why" in mechanistic terms.

2. **From Correlation to Causation**: As regulatory frameworks (GDPR Article 22, EU AI Act) increasingly demand explanations, methods like DAG-SHAP that distinguish causal from spurious relationships become essential for compliance.

3. **Integration with Causal Inference**: DAG-SHAP bridges two previously separate fields:
   - **Interpretable ML**: Feature attribution
   - **Causal Inference**: Causal effect estimation
   - This convergence enables more principled explanations

### Advancing State-of-the-Art in Explainability

1. **Beyond Node-Centric Methods**: Demonstrates that structure-aware attribution (accounting for dependencies) produces fundamentally better explanations

2. **Scalable Causal Explainability**: Provides practical algorithm for causal attribution at scale, making causal reasoning accessible beyond academic settings

3. **Formalization of Mechanism-Level Explanations**: Offers mathematical framework for "mechanistic" explanations, operationalizing concepts from philosophy of science and cognitive psychology

### Limitations and Open Questions

1. **DAG Specification Challenge**: 
   - **Problem**: Real-world causal structures are often unknown or controversial
   - **Question**: How robust is DAG-SHAP to misspecified graphs?
   - **Future Work**: Sensitivity analysis and robustness tests

2. **Scalability to High-Dimensional Graphs**:
   - **Problem**: Current experiments on relatively small DAGs (< 10 edges)
   - **Challenge**: Combinatorial explosion as number of edges grows
   - **Open**: Efficient algorithms for graphs with 100+ features

3. **Time-Series and Feedback Systems**:
   - **Limitation**: Cannot directly handle dynamic causal structures or feedback loops
   - **Extension Needed**: Temporal DAGs or Markov decision processes

4. **Human Evaluation**:
   - **Question**: Do end-users find edge-based attributions more useful than traditional features?
   - **Needed**: User studies comparing DAG-SHAP against baselines

## Code & Resources

### Official Implementation

**Repository**: [Authors' GitHub](https://github.com/) [Exact link unavailable — see paper for repository URL]

**Language**: Python

**Key Dependencies**:
- NumPy/SciPy (numerical computing)
- Pandas (data handling)
- Scikit-learn (baseline ML models)
- TensorFlow/PyTorch (for DNN experiments)
- XGBoost (for gradient boosting experiments)

**Installation**:
```bash
# Assumed installation (exact commands from repository)
git clone [repository-url]
cd dag-shap
pip install -r requirements.txt
```

**Computational Requirements**:
- **Minimum**: CPU with multiprocessing support
- **Recommended**: Multi-core processor (8+ cores for parallel permutation sampling)
- **GPU**: Optional; CPU sufficient for small-to-medium datasets
- **Memory**: 4-8 GB RAM for experiments on datasets tested in paper

### Quick Start Guide

**Basic Usage Pattern**:
```python
# Pseudocode structure (exact API from paper documentation)
from dag_shap import DAGSHAP

# Define causal DAG
causal_dag = {
    'A': [],
    'B': ['A'],
    'C': ['B'],
    'Y': ['A', 'C']
}

# Initialize explainer with DAG
explainer = DAGSHAP(model, causal_graph=causal_dag)

# Compute edge-level attributions
explanations = explainer.explain(instance)
```

### Interactive Visualizations

The paper likely includes:
- **DAG Visualizations**: Graph showing causal structure and feature relationships
- **Attribution Heatmaps**: Edge-wise importance scores
- **Comparison Plots**: DAG-SHAP vs. competing methods across datasets

[Exact links to demos unavailable — see full paper]

### Related Tools and Frameworks

**Complementary Tools**:
- **Causal-Discovery Algorithms**: PC algorithm, FCI for learning DAGs from data
- **SHAP Library**: https://github.com/slundberg/shap (original SHAP implementations)
- **CausalML**: https://github.com/uber/causalml (causal inference library)
- **DoWhy**: https://github.com/py-why/dowhy (causal inference and estimation)

## Related Work & Context

### How DAG-SHAP Relates to Other Recent xAI Papers

1. **vs. Causal SHAP (2509.00846)**
   - **Causal SHAP**: Uses PC algorithm for discovery, IDA for causal strength
   - **DAG-SHAP**: Assumes DAG given, uses edge intervention
   - **Relationship**: DAG-SHAP provides finer-grained (edge-level) attributions; Causal SHAP is more flexible (learns DAG)
   - **Use Case Differentiation**:
     - Causal SHAP: When causal structure is unknown but can be discovered
     - DAG-SHAP: When DAG is known (domain expertise available)

2. **vs. Traditional SHAP Feature Attribution**
   - **Traditional SHAP**: Node-centric, treats features independently
   - **DAG-SHAP**: Edge-centric, accounts for causal dependencies
   - **Key Advance**: Eliminates misleading attributions caused by correlated features

3. **vs. Other Causal Interpretability Work**
   - **Counterfactual Explanations** (DANCE, 2025-11-25): Ask "what if?" scenarios
   - **DAG-SHAP**: Explains "how much does this causal pathway contribute?"
   - **Complementary**: Can combine counterfactual analysis with DAG-SHAP's attributions

### Building Upon Prior Interpretability Methods

1. **Foundation: Shapley Values** (Shapley, 1953)
   - Established fair allocation in cooperative games
   - DAG-SHAP: Extends to causal game where only certain coalitions are valid

2. **Inspiration: SHAP** (Lundberg & Lee, 2017)
   - Made Shapley values practical for ML
   - DAG-SHAP: Extends to account for feature dependencies

3. **Theory: Causal Inference** (Pearl's do-calculus, SCMs)
   - Provides mathematical framework for causal reasoning
   - DAG-SHAP: Operationalizes causal effects for feature attribution

### Future Research Directions This Work Enables

1. **Learning DAGs and Attributing Simultaneously**
   - Combined framework: Learn causal structure and compute attributions iteratively
   - Addresses the "circular" problem of needing DAG to explain

2. **Dynamic Causal Attribution**
   - Extend to time-series and temporal causal models
   - Important for finance, climate, epidemiology

3. **Counterfactual Edge Interventions**
   - "If this causal edge were broken, how much would predictions change?"
   - Bridge between DAG-SHAP and counterfactual explanations

4. **Heterogeneous Treatment Effect Attribution**
   - Personalized explanations: "For this specific patient/user, which causal pathways matter most?"
   - Combines causal heterogeneity with individual attribution

### Connection to Broader xAI Communities

**LIME & SHAP**: DAG-SHAP is a specialized variant extending these foundational methods to causal settings

**Mechanistic Interpretability**: Differs from circuits/SAE approaches (which study neural internals) but shares goal of understanding mechanisms

**Fairness in ML**: Causal grounding helps detect and remove spurious correlations that cause algorithmic bias

**Causal ML**: Bridges gap between causal discovery/inference and model interpretability—historically separate subfields

## References & Citation

**Paper Citation**:
```
Sun, Q., et al. (2026). Feature Attribution in Directed Acyclic Graphs Using Edge Intervention. 
arXiv:2606.15273. Submitted June 13, 2026.
```

**ArXiv Link**: [arXiv:2606.15273](https://arxiv.org/abs/2606.15273)

## Related Papers in This Knowledge Base

- **Causal SHAP** (2025-08-31): Feature attribution with dependency awareness
- **DANCE - Counterfactual Explanations** (2025-11-25): Counterfactual analysis with causal constraints
- **Open Problems in Mechanistic Interpretability** (2026-01-27): Broader interpretability challenges
- **Causality is Key for Interpretability Claims** (2026-02-18): Theoretical foundations of causal explanation
- **Causal Argumentation and Explainability** (2026-05-20): Human-centered causal reasoning
- **LLM Explainability via Counterfactual Chains** (2026-06-04): Causal reasoning in language models

---

**Paper Summary Date**: September 19, 2026

**Documented by**: Claude Code  
**Repository**: [Giang-Dang/computer-science-news](https://github.com/Giang-Dang/computer-science-news)
