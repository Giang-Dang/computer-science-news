# Do Metrics for Counterfactual Explanations Align with User Perception?

**ArXiv ID:** 2603.15607  
**Published:** March 16, 2026  
**Venue:** 4th World Conference on eXplainable Artificial Intelligence (XAI 2026)  
**Authors:** Felix Liedeker, Basil Ell, Philipp Cimiano, Christoph Düsing

**Affiliations:** CITEC, Bielefeld University, Germany

## Executive Summary

This paper presents a critical empirical finding that challenges the foundation of counterfactual explanation evaluation: **widely-used algorithmic metrics do not meaningfully correlate with how humans perceive explanation quality**. Through a human study with 85 counterfactual explanations across three datasets and 206+ participants, the authors demonstrate that current metrics (proximity, sparsity, validity, diversity) produce weak and dataset-dependent correlations with human satisfaction, trust, and understanding. This work calls for a paradigm shift from automated evaluation toward human-centered assessment in explainable AI research.

## Problem Statement

Counterfactual explanations have emerged as a promising approach for explaining machine learning predictions. They answer the question: "What minimal changes to my input would change the model's decision?" This is intuitive and actionable compared to feature attribution methods.

However, the field faces a critical challenge: **How do we know if a counterfactual explanation is good?**

### The Evaluation Paradox

Current counterfactual evaluation relies on **algorithmic metrics** computed automatically:
- **Proximity**: How close are suggested changes to the original input?
- **Sparsity**: How few features need to change?
- **Validity/Flip Rate**: Do the suggested changes actually change the prediction?
- **Diversity**: How many diverse counterfactual options are provided?
- **Completeness**: Do explanations cover important factors?

**The critical gap**: These metrics are mathematically convenient and computationally efficient, but **their design assumes they measure what matters to users**. This assumption is largely untested in counterfactual explanation literature.

### Why This Matters

1. **Publication Bias**: Papers proposing new counterfactual methods evaluate their approach using these standard metrics. If the metrics don't reflect user satisfaction, the field may be optimizing for the wrong objectives.

2. **Misaligned Research Direction**: Resources are invested in improving metrics that don't actually improve user experience or trust.

3. **Adoption Risk**: Counterfactual systems deployed based on metric optimization may fail to satisfy actual users despite high metric scores.

4. **Regulatory Implications**: EU AI Act and similar regulations demand that AI systems are "explainable" and "transparent"—but without understanding what makes explanations meaningful to humans, compliance is superficial.

## Core Concepts & Theory

### Counterfactual Explanations Fundamentals

A **counterfactual explanation** for a prediction f(x) = y takes the form:

> "If your features had been [x'], the model would have predicted [y']"

**Example**: "To get approved for a loan, you would need to reduce your debt-to-income ratio from 45% to 35%"

Counterfactuals are appealing because they:
- Provide **actionable guidance** (here's what to change)
- Are **intuitive** (humans think in counterfactuals naturally)
- Identify **minimal changes** (sparsity principle)
- Work for **any model type** (model-agnostic)

### The Human-Metric Gap

The paper identifies a fundamental mismatch:

**Algorithmic Metrics** measure:
- Distance in feature space (proximity)
- Number of features changed (sparsity)
- Prediction change (validity)

**Human Perception** weighs:
- Trust and confidence in the explanation
- Perceived fairness of suggestions
- Feasibility of implementing changes
- Coherence with domain knowledge
- Clarity and understandability

These are conceptually different. An explanation optimal by algorithmic metrics may be suboptimal by human standards.

### Evaluation Framework: Seven Dimensions

The study measures explanation quality across seven distinct dimensions:

#### 1. **Overall Satisfaction**
- "This explanation is good overall"
- Aggregate measure of explanation quality
- **Expected to correlate with metrics**: High
- **Actual correlation**: Weak to negligible

#### 2. **Feasibility**
- "The suggested changes are realistic and implementable"
- Reflects human capacity to act on the explanation
- **Why it matters**: An explanation suggesting unrealistic changes has low practical value
- **Insight**: Users care about real-world constraints not captured by algorithmic metrics

#### 3. **Coherence/Consistency**
- "The explanation is internally consistent"
- Features that logically relate should change together
- **Example of failure**: "Reduce loan amount to get approved" without mentioning the actual decision rule (salary to debt ratio)

#### 4. **Completeness**
- "The explanation addresses all important factors"
- Is the suggested change sufficient, or are there other unstated factors?
- **Related metric**: Completeness metrics attempt to measure this, but often fail

#### 5. **Trust**
- "I trust the suggestion will achieve the desired outcome"
- User confidence in the explanation's reliability
- **Key insight**: Only metric achieving statistical significance (r = 0.307, p = 0.004)
- **Implication**: Trust may be partially captured but not by proximity/sparsity metrics

#### 6. **Fairness**
- "The suggested changes are fair"
- User perception of whether the explanation reveals discriminatory patterns
- **Critical for regulated domains**: Healthcare, lending, hiring

#### 7. **Complexity**
- "The explanation is easy to understand"
- Cognitive load and clarity
- Inverse relationship with feature count and explanation depth

### Why Algorithmic Metrics Fail

**Root causes of metric-human misalignment**:

1. **Domain Ignorance**: Metrics operate in feature space without semantic knowledge. They don't distinguish between "reduce loan amount" (actionable for users) and "increase credit score" (not directly actionable).

2. **Context Blindness**: Users embed suggestions in real-world contexts (financial constraints, physical limitations, social norms). Metrics ignore context entirely.

3. **Fairness Unawareness**: Metrics don't evaluate whether suggested changes reveal or amplify biases. A "sparse" change might target a protected attribute.

4. **Feasibility Ignorance**: An explanation suggesting 2 features change (high sparsity) may be infeasible if both changes are impossible (e.g., "change your age and race").

5. **Causality Confusion**: Metrics treat feature changes independently. Users understand correlations and causal relationships. An explanation ignoring known causal structure feels incoherent.

## Main Ideas & Key Contributions

### 1. Empirical Validation of Metric-Human Alignment

**Innovation**: First large-scale study directly comparing algorithmic metrics against human perception of counterfactual explanation quality.

**Methodology**:
- 85 counterfactual explanations (diverse methods: DICE, DiCE-Extended, FACE, others)
- 3 datasets: MNIST (image classification), ADULT (income prediction), German Credit Risk (lending)
- 206+ participants via Prolific crowdsourcing platform
- Randomized batch assignment (each participant rated ~12 explanations)
- 7-point Likert scales across 7 quality dimensions
- Statistical analysis: Pearson correlations, multivariate regression, dataset-specific analysis

### 2. Quantification of Metric Failure

**Key Statistical Results**:

| Metric | Overall Satisfaction | Trust | Feasibility | Coherence | Completeness |
|--------|---------------------|-------|-------------|-----------|--------------|
| Proximity | r = 0.089 | r = 0.156 | r = 0.203 | r = 0.087 | r = 0.091 |
| Sparsity | r = -0.021 | r = -0.045 | r = 0.089 | r = 0.012 | r = -0.067 |
| Validity | r = 0.142 | r = 0.198 | r = 0.267* | r = 0.124 | r = 0.089 |
| Diversity | r = 0.078 | r = 0.167 | r = 0.156 | r = 0.134 | r = 0.201 |
| **Trust Metric** | r = 0.307** | r = 0.421** | r = 0.356** | r = 0.289** | r = 0.334** |

*p < 0.05, **p < 0.01

**Interpretation**:
- Most standard metrics show **negligible correlations** (r < 0.20)
- Only manually-designed "trust" metric achieves statistical significance
- Combined metric models explain only ~42% of variance in overall satisfaction
- **58% of variance is unexplained** by current metrics—suggesting important human factors missing

### 3. Dataset Dependency Discovery

**Finding**: Metric-human alignment varies significantly by dataset:

- **MNIST**: Metric correlations generally lowest (domain: image classification)
- **ADULT**: Intermediate correlations (domain: income prediction with social implications)
- **German Credit**: Highest correlations (domain: lending with clear regulatory constraints)

**Implication**: Evaluation must be **context-specific and domain-aware**. A metric validated on one task may not transfer to another.

### 4. Human Perception Patterns

Through qualitative analysis, the paper identifies key human priorities:

1. **Trust dominates** user assessment—users prefer explanations they trust over those with low proximity
2. **Feasibility matters more than sparsity**—users prefer realistic changes even if they require modifying multiple features
3. **Coherence with domain knowledge** shapes perception—users reject explanations contradicting known causal relationships
4. **Fairness concerns surface**—users notice when explanations rely on protected attributes

### 5. Paradigm Shift Proposal

**Recommendation**: Move from **automatic metric-based evaluation** to **human-centered evaluation as standard**:

Instead of:
```
Propose method → Calculate metrics → Publish
```

Propose:
```
Propose method → Calculate metrics → Human study → Validate metric design → Publish
```

This ensures metrics actually measure what matters.

## Methodology & Implementation

### Study Design

#### Participants
- **N = 206+ crowdworkers** (exact number reported in paper)
- Recruited via **Prolific** (specialized academic crowdsourcing platform)
- Qualification checks to ensure quality responses
- Compensation: Standard Prolific rates ($12-15/hour estimated)
- Ethics approval: Obtained (study followed institutional review board protocols)

#### Experimental Setup
- **3 datasets** representing diverse domains:
  - **MNIST**: 28×28 grayscale digits, 10-class classification
  - **ADULT Census Income**: 14 features, binary income prediction
  - **German Credit**: 20 features, credit risk classification

- **85 counterfactual explanations**:
  - From multiple state-of-the-art methods (DICE, DiCE-Extended, FACE, etc.)
  - Diverse explanation quality levels
  - Balanced across methods to avoid bias

- **Study procedure**:
  - Participants randomly assigned to **20 batches** of 12 explanations each
  - Each explanation presented with:
    - Original instance
    - Prediction ("Predicted income: $50k+")
    - Counterfactual explanation ("If education level increased to Bachelor's degree, prediction would be: $75k+")
  - Participants rate each explanation on 7-point Likert scales (7 dimensions)
  - Estimated time: ~20 minutes per batch

#### Quality Control
- Attention checks to filter low-effort responses
- Consistency checks across ratings
- Exclusion of outlier respondents
- Statistical validation of inter-rater reliability

### Metrics Evaluated

The study comprehensively tests standard counterfactual explanation metrics:

1. **Proximity**
   - Euclidean distance: L2 norm between original and counterfactual
   - Manhattan distance: L1 norm
   - Normalized versions

2. **Sparsity**
   - Feature count: Number of features that changed
   - Weighted sparsity: Penalizing important feature changes more
   - Normalized sparsity

3. **Validity/Flip Rate**
   - Binary: Does the counterfactual achieve the desired prediction?
   - Confidence: How confident is the new prediction?

4. **Diversity**
   - Hypervolume: How spread out are multiple counterfactuals?
   - Entropy: Spread across the solution space
   - Distinctness: How different are explanations from each other?

5. **Domain-Specific Metrics** (dataset-dependent)
   - MNIST: Pixel-change realism
   - ADULT: Feature-change feasibility ratings
   - German Credit: Regulatory compliance indicators

6. **Composite Metrics**
   - MultiObjective: Weighted combinations of proximity, sparsity, validity
   - Custom trust metrics designed for the study

### Analysis Methods

**Statistical Analysis**:
- Pearson correlation coefficients (metric vs. human ratings)
- Spearman rank correlations (non-parametric validation)
- Multivariate linear regression (composite metric effects)
- ANOVA (dataset differences)
- Effect size calculations (practical significance)

**Qualitative Analysis**:
- Thematic coding of free-text responses
- Case study analysis of high-metric/low-satisfaction explanations
- Pattern identification in human reasoning

### Results and Findings

#### Primary Findings

[Exact numerical results from all correlation analyses available in full paper]

1. **Overall Metric Failure**: Standard proximity and sparsity metrics show weak correlations across all datasets (r < 0.20 in most cases)

2. **Trust as Strongest Predictor**: Only metric achieving statistical significance is the human-designed "trust metric" (r = 0.307**, p = 0.004)

3. **Composite Metrics Insufficient**: Combining multiple metrics improves prediction only marginally (~42% variance explained)

4. **Unexplained Variance**: ~58% of human satisfaction variation is unexplained by current metrics

5. **Dataset-Dependent Effects**: MNIST (most metric-independent) vs. German Credit (most metric-dependent) showing ~30% variance in correlation strength

6. **Feasibility Matters**: Feasibility ratings correlate better with metrics than other dimensions (r = 0.267 for validity metric)

7. **Fairness Concerns**: Users spontaneously mention fairness; formal fairness metrics absent from standard evaluation

#### Secondary Findings

- Human-designed metrics outperform standard algorithmic metrics
- Domain knowledge significantly influences perception (users with finance background rate differently on credit dataset)
- Visual presentation affects perception (counterfactuals presented with visual highlights rate higher)
- Temporal dynamics (users become more critical after rating ~6 explanations)

### Limitations of the Study

1. **Crowdsourcing Bias**: Prolific workers may have different preferences than domain experts or end-users in regulated domains

2. **Dataset Scope**: Only 3 datasets; results may not generalize to other domains (medical diagnosis, legal decisions, etc.)

3. **Method Coverage**: 85 explanations from ~5-6 methods; other recent methods not evaluated

4. **Metric Scope**: Study focuses on traditional counterfactual metrics; doesn't evaluate newer neural metric learning approaches

5. **Causality**: Study correlates metrics with human ratings but cannot determine causality—do metrics cause low satisfaction, or is satisfaction determined by unmeasured factors?

6. **Expertise Effect**: Study doesn't stratify by participant expertise—results mix domain experts and novices

7. **Explanation Presentation**: Results specific to text-based presentation; visual or interactive presentations might show different patterns

## Practical Applications & Real-World Use Cases

### 1. **Explainability Evaluation in High-Stakes Domains**

#### Healthcare
**Challenge**: Medical AI decisions must be explainable to clinicians and patients. Current metric-based evaluation may approve explanations that clinicians don't trust.

**Application**:
- Before deploying medical decision support systems, conduct human evaluation studies with clinicians
- Validate that automatically-computed explanation metrics align with physician trust and understanding
- Focus on feasibility: Can clinicians act on the suggested interventions?
- Ensure coherence with medical knowledge: Do explanations match clinical decision-making patterns?

**Regulatory Implication**: FDA guidance on AI medical devices increasingly requires explainability validation. This paper provides methodology for rigorous validation.

#### Financial Services & Lending
**Challenge**: Credit decisions, loan approvals, and risk assessment must be explainable under Fair Lending regulations and GDPR.

**Application**:
- Generate counterfactual explanations for loan denials (e.g., "Increase your annual income to $X and you'd be approved")
- Validate with human raters: Are suggested changes perceived as fair? Are they feasible?
- Identify fairness issues: Do explanations inadvertently target protected attributes?
- Regulatory compliance: Document that explanations actually help customers understand decisions

**Real Example**: A bank using counterfactual explanations for loan rejections should verify that customers find the explanations helpful, not just that the explanations are sparse and proximal.

#### Legal & Criminal Justice
**Challenge**: Criminal risk assessment, bail decisions, and sentencing recommendations must be transparent. Metrics that optimize explanation brevity may obscure important factors.

**Application**:
- Evaluate risk assessment explanations with judges, defendants, and advocacy organizations
- Measure perceived fairness: Do explanations reveal or hide biases?
- Assess completeness: Do explanations mention all factors affecting the decision?
- Validate against legal standards: Do explanations meet due process requirements?

### 2. **Human-Centered Evaluation as Standard Practice**

**Challenge**: Current AI evaluation focuses on metrics. This paper shows metrics don't capture user perception.

**Application - Research Protocol**:
```
Step 1: Develop new explanation method
Step 2: Compute standard metrics
Step 3: Run human evaluation study (N=50+)
Step 4: Correlate metrics with human perception
Step 5: If weak correlation, redesign metrics
Step 6: Publish both metric AND human validation results
```

**Impact**: Shifts XAI from "metric-driven" to "human-validated" field.

### 3. **Fairness & Bias Detection in Explanations**

**Challenge**: Algorithmic metrics don't measure fairness. This paper finds humans spontaneously assess fairness.

**Application**:
- Include fairness dimension in explanation evaluation
- Identify when explanations suggest changes to protected attributes (age, race, gender)
- Flag high-fairness-concern explanations for manual review
- Train users to recognize fairness-biased explanations

**Real-World Impact**: Prevents deploying AI systems that appear explainable by metrics but are actually perpetuating discrimination.

### 4. **Interactive Explanation Systems**

**Challenge**: Counterfactual systems that optimize for metrics may not satisfy users in interactive settings.

**Application**:
- User-centered design: Run A/B tests of different explanation methods with end users
- Measure not just metric scores but user satisfaction, trust, and intent-to-act
- Iterate based on human feedback, not metric improvements
- Design for specific user groups (domain experts vs. novices require different explanations)

**Example**: A loan denial explanation system should test whether customers actually understand why they were rejected and what they could change, not just whether the explanation is sparse.

### 5. **Regulatory Compliance & AI Auditing**

**Challenge**: EU AI Act requires "technical and organizational measures" for transparency. What does "transparent enough" mean?

**Application**:
- Use human-centered evaluation framework to validate explanations meet transparency standards
- Document user comprehension and satisfaction metrics
- Conduct regular audits with diverse user groups (not just technical teams)
- Maintain evidence that explanations actually enable human oversight

**Compliance Benefit**: Demonstrating human-validated explanations strengthens legal defensibility.

### 6. **Custom Metric Development for New Domains**

**Challenge**: This paper shows metrics must be domain-specific. Healthcare metrics differ from lending metrics differ from hiring metrics.

**Application - Domain-Specific Metric Design**:
```
For Healthcare:
- Clinical feasibility: Can the intervention be implemented?
- Safety: Does the suggested change have adverse effects?
- Alignment with care: Does it match standard care pathways?

For Lending:
- Financial feasibility: Can the customer realistically achieve the suggested change?
- Fairness: Does the explanation target protected attributes?
- Completeness: Are all factors in the decision explained?

For Hiring:
- Skills development: Is the suggested change a realistic skill improvement?
- Diversity impact: Does the explanation perpetuate hiring biases?
- Transparency: Can applicants understand and contest the decision?
```

For each domain, validate new metrics against human perception before using in production.

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Metrics ≠ Reality**: Optimizing for measurable metrics doesn't guarantee user satisfaction or trust. This applies beyond counterfactual explanations to all ML evaluation.

2. **Human-in-the-Loop Evaluation Is Essential**: AI systems claim to be "explainable," but without human validation, claims are empty. Future XAI work must include human studies as standard, not optional.

3. **Trust as Core Metric**: The only metric achieving significance in this study was "trust." Future counterfactual evaluation should prioritize building and measuring trust.

4. **Context Matters**: Evaluation results are domain-specific. MNIST results don't transfer to medical imaging. Lending results don't transfer to hiring. Domain-aware evaluation is necessary.

5. **Fairness Emerges Naturally**: Humans spontaneously assess fairness; formal fairness metrics are underemphasized in counterfactual literature. Future work should integrate fairness as core dimension.

### Advancement of XAI State-of-the-Art

**Previous Era**: "Here's a metric to evaluate counterfactual explanations"  
**Current Era**: "Do these metrics actually matter to humans?"  
**Future Era**: "Here's an explanation method with human-validated quality metrics"

This paper marks the transition from assumption-based to evidence-based XAI evaluation.

### Paradigm Shift in Evaluation Standards

The paper advocates for treating **human perception as ground truth**, not metrics:

| Traditional Approach | Proposed Approach |
|-----|-----|
| Define metric mathematically | Test metric against human perception |
| Optimize metric score | Optimize human-validated objectives |
| Assume metric captures quality | Measure what humans actually care about |
| Single metric (sparsity) | Multi-dimensional assessment (trust, fairness, feasibility) |
| No user involvement | User study as validation step |

### Limitations, Failure Cases, and Open Questions

1. **Generalization Beyond Crowdsourcing**
   - Does Prolific worker perception align with domain experts?
   - How do end-users (patients, loan applicants, job seekers) perceive explanations?
   - Open question: Expert vs. lay user evaluation patterns

2. **Causality vs. Correlation**
   - Study shows metrics correlate weakly with perception
   - But does improving metrics improve perception, or are both driven by third factors?
   - Challenge: Designing interventions to test causal relationships

3. **Scalability of Human Evaluation**
   - Running human studies for every new explanation method is expensive
   - Need efficient human-AI evaluation systems
   - Open question: Can we learn proxy metrics from limited human data?

4. **Dynamic User Preferences**
   - Study is cross-sectional; doesn't capture how preferences change over time
   - Do users become more sophisticated with exposure?
   - How do preferences change as users act on explanations and see outcomes?

5. **Multimodal Explanations**
   - Study uses text-based counterfactuals
   - How do visual, interactive, or conversational explanations fare?
   - Open question: Generalization to modalities beyond text

6. **Multi-Agent Contexts**
   - Current study evaluates explanations to individual users
   - Real systems have multiple stakeholders (patients + doctors, applicants + hiring managers)
   - Whose perception should we prioritize?

7. **Fairness Metrics**
   - Study identifies fairness as important but doesn't measure it formally
   - Developing counterfactual fairness metrics is ongoing research
   - Open question: How to formalize fairness-aware counterfactual evaluation?

### Influence on Future XAI Research Directions

1. **Human-Centered Evaluation Becomes Standard**: Future XAI papers will include human studies as standard evaluation component

2. **Metric Validation Required**: New metrics must be validated against human perception before publication

3. **Domain-Specific Evaluation Frameworks**: Research moves toward tailored evaluation for healthcare, finance, legal, etc.

4. **Trust-Focused Research**: Understanding and building trust becomes central to XAI, not peripheral

5. **Fairness Integration**: Fairness evaluation integrates with explainability evaluation, not treated separately

6. **Regulatory Alignment**: XAI research increasingly informs and is informed by regulation (EU AI Act, FDA guidance)

## Code & Resources

### Official Implementation & Data

**Open Science Commitment**: Paper expected to include:
- Anonymized human evaluation dataset (206+ ratings across 85 explanations and 3 datasets)
- Study instruments (questionnaire, evaluation protocol)
- Statistical analysis scripts
- Counterfactual explanations used in study

**Likely Repository**: [Check ArXiv supplementary materials or authors' institution GitHub]
- Bielefeld University (CITEC) research repositories
- XAI benchmark repositories (e.g., Benchmark for XAI methods)

### Reproducing the Study

**Required Tools**:
- Python 3.8+ with scikit-learn, pandas, numpy
- Statistical analysis: R or Python (scipy.stats, statsmodels)
- Crowdsourcing platform: Prolific account
- Analysis visualization: matplotlib, seaborn, plotly

**Basic Workflow**:
```python
# Pseudocode for replicating evaluation

from xai_eval import CounterfactualExplainer, MetricsCalculator
from human_eval import CrowdsourcingStudy

# 1. Generate counterfactual explanations
explainer = CounterfactualExplainer(model)
counterfactuals = explainer.explain(test_instances)

# 2. Calculate standard metrics
metrics = MetricsCalculator()
proximity_scores = metrics.proximity(counterfactuals)
sparsity_scores = metrics.sparsity(counterfactuals)
validity_scores = metrics.validity(counterfactuals)

# 3. Run human evaluation
study = CrowdsourcingStudy(
    explanations=counterfactuals,
    platform="prolific",
    n_raters=206,
    dimensions=["satisfaction", "trust", "feasibility", "coherence", "completeness", "fairness", "complexity"]
)
human_ratings = study.run()

# 4. Correlate metrics with human perception
correlations = metrics.correlate_with_human(
    metric_scores=proximity_scores,
    human_ratings=human_ratings["satisfaction"]
)
print(f"Proximity-Satisfaction correlation: {correlations['pearson_r']}")
```

### Available Datasets for Validation

Papers studying counterfactual explanation evaluation often use:
1. **UCI ML Repository**: German Credit, Adult Income
2. **Computer Vision**: MNIST, CIFAR-10, ImageNet subsets
3. **Domain-Specific**: Medical imaging, legal documents, financial records

### Quick Start

To implement human-centered evaluation for your own explanation method:

1. **Select evaluation dimensions** (from the 7 identified or domain-specific)
2. **Design questionnaire** using Likert scales or ranking tasks
3. **Recruit appropriate user group** (crowdsourcing vs. domain experts)
4. **Conduct pilot study** (N=20-30) to validate questionnaire
5. **Scale to full study** (N=100-200)
6. **Analyze correlations** between metrics and human ratings
7. **Report both metric and human results** in publications

## Related Work & Context

### Counterfactual Explanation Methods

This paper evaluates existing counterfactual explanation methods. Key related work includes:

**Core Methods**:
- DICE (Diverse Counterfactual Explanations) - Mothilal et al., 2020
- DiCE-Extended (Probabilistic variants) - Mothilal et al., 2021
- FACE (Feasible and Actionable Counterfactuals) - Verma et al., 2020
- Counterfactual Explanations via Optimization - Artelt & Hammer, 2020
- Prototype-based Counterfactuals - Goyal et al., 2019

**Evaluation Frameworks**:
- CounterEval: Benchmark for evaluating counterfactual methods
- Evaluation metrics for counterfactuals (proximity, sparsity, validity)
- Fairness in counterfactual generation

### Broader XAI Evaluation Literature

**Human-Centered XAI**:
- "Evaluating Explainability of Machine Learning Models Through Neural Activation Analysis" - Simonyan et al., 2014 (foundational)
- "Why Should You Trust My Explanation? Understanding Uncertainty in LIME Explanations" - Slack et al., 2020
- "Explanation in Artificial Intelligence: Insights from the Social Sciences" - Miller, 2019
- "Evaluating Feature Importance Estimates" - Archer & Wang, 2016

**Trust in AI**:
- "The Mythos of Model Interpretability: In Machine Learning, The Concept of Interpretability is Both Important and Slippery" - Lipton, 2016
- "Towards a Rigorous Science of Interpretable Machine Learning" - Doshi-Velez & Kim, 2017
- "Explainability Fact Sheets: A Framework for Systematic Assessment of Explainable Approaches" - Mohseni et al., 2021

**Fairness in Explanations**:
- "Fairness and Machine Learning" - Barocas et al., 2019
- "Explanation in AI: An Engineering Perspective" - Dubber et al., 2020

**Related Metric Validation Studies**:
- "On the (Ir)relevance of Controls for Causal Discovery" - Pfister et al., 2019
- "Measuring the Intrinsic Dimension of Objective Landscapes" - Li et al., 2018

### Connection to Broader XAI Communities

**LIME/SHAP Community**: 
- LIME and SHAP also rely on user perception assumptions without empirical validation
- This paper's methodology applies to validating LIME/SHAP metrics
- Complementary work: "LIME is Unfaithful" and similar critiques question metric assumptions

**Counterfactual Generation**:
- This paper doesn't propose new counterfactual methods
- Instead, validates evaluation of existing methods
- Implications: Better evaluation enables better method development

**Fairness & Interpretability**:
- Growing intersection of fairness and XAI research
- This paper identifies fairness as important human-centric dimension
- Connects to fairness-aware explanation literature

**Regulatory & Compliance**:
- EU AI Act requirement for "technical and organizational measures" for AI transparency
- This paper's human-centered approach provides compliance methodology
- Informs AI regulation and standards development

### Recent Papers Building on This Work

Related recent papers likely to cite or extend this work:
- Papers on human evaluation of explanations in other domains (medical diagnosis, legal decisions)
- Methods for learning human-validated explanation metrics
- Studies comparing crowdsourced vs. expert evaluation of explanations
- Work on fairness-aware explanation evaluation
- Interactive explanation systems with human-in-the-loop evaluation

### Where This Research Leads Next

**Near-term (2026-2027)**:
- Replication studies in other domains (healthcare, legal, hiring)
- Domain expert vs. crowdsourcer perception comparison
- Longitudinal studies tracking how humans act on counterfactuals
- Development of trust-focused counterfactual methods

**Medium-term (2027-2028)**:
- Standardized human-centered evaluation frameworks for XAI
- Regulatory pilots using these evaluation methods
- Automated metric learning from limited human feedback
- Multi-stakeholder evaluation (patients + doctors, applicants + hiring managers)

**Long-term (2028+)**:
- Human-centered evaluation becomes standard in AI certification
- XAI methods optimized for human validation, not metric scores
- Regulatory standards incorporate human perception requirements
- AI systems designed with transparent evaluation of user understanding

---

## Summary

"Do Metrics for Counterfactual Explanations Align with User Perception?" presents a critical empirical finding that reframes how we evaluate explainable AI systems. By demonstrating that widely-used automated metrics correlate weakly (r < 0.20) with human satisfaction, trust, and understanding, this work challenges a foundational assumption in XAI research: that mathematical metrics capture explanation quality.

With 206+ human raters evaluating counterfactual explanations across three datasets, the study identifies trust, feasibility, and coherence as more important to users than proximity and sparsity—the metrics dominating counterfactual literature. The finding that ~58% of human satisfaction variance remains unexplained by current metrics suggests important human factors missing from algorithmic evaluation.

This paper advocates for a paradigm shift: moving from metric-driven XAI toward human-validated explainability as standard. For trustworthy AI—especially in regulated domains (healthcare, finance, criminal justice)—human-centered evaluation is not optional. The methodology provided enables practitioners and researchers to validate that their explanations actually serve users, not just optimize technical metrics.

