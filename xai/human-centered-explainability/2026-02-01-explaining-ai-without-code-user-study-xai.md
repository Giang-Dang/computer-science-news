# Explaining AI Without Code: A User Study on Explainable AI in No-Code ML Platforms

**ArXiv ID:** [2602.11159](https://arxiv.org/abs/2602.11159)  
**Authors:** Natalia Abarca, Andrés Carvallo, Claudia López Moncada, Felipe Bravo-Marquez  
**Submission Date:** February 2026  
**Subfield:** Human-Centered Explainability — User Studies, No-Code AI, Democratization of XAI

---

## Executive Summary

The democratization of machine learning through no-code platforms creates a new challenge: how do we make model explanations meaningful and accessible to users who lack programming expertise? This paper presents and evaluates a human-centered XAI module integrated into **DashAI**, an open-source no-code ML platform, incorporating three complementary explanation techniques (Partial Dependence Plots, Permutation Feature Importance, and KernelSHAP). Through a user study with 20 participants spanning ML novices and experts, the authors demonstrate that non-technical users can successfully interpret XAI explanations with ≥80% task success rate, while uncovering systematic differences in how novices and experts perceive explanation quality — with implications for how XAI systems should be designed for different user populations.

---

## Problem Statement

### The Explainability Democratization Gap

Explainable AI has made significant progress in developing powerful explanation techniques — SHAP, LIME, Integrated Gradients, attention maps. However, these tools share a critical design assumption: **the user has sufficient technical knowledge to interpret them**. SHAP values require understanding of Shapley theory; attention maps require familiarity with transformer architectures; partial dependence plots require understanding of marginal distributions.

### No-Code ML Platforms: Power Without Understanding

No-code ML platforms (AutoML, low-code tools) have dramatically lowered the barrier to *training* machine learning models. Business analysts, healthcare professionals, educators, and researchers without programming backgrounds can now build predictive models. But this creates a new paradox:

```
Easy to build ML models → Hard to understand why they make predictions
```

The person most likely to deploy a model in a high-stakes domain (a doctor, a judge, a social worker) may be the least equipped to interpret traditional XAI outputs. Meanwhile, they are often the person most responsible for the model's consequences.

### The Research Gap

While XAI usability research exists, prior work almost exclusively studied:
- **Technical users** (data scientists, researchers) using specialized XAI tools
- **Standalone explanation interfaces** separate from model-building workflows
- **Expert-designed explanations** rather than platform-integrated, workflow-native explanations

There was no prior study of **non-technical users interpreting XAI explanations within a no-code ML workflow** — the exact scenario increasingly common in practice.

### Specific Research Questions

1. Can ML novices successfully complete basic explanation interpretation tasks?
2. How do novices and experts differ in perceived explanation quality (satisfaction, trust, accuracy)?
3. Which explanation types (PDP, PFI, SHAP) are most accessible to non-technical users?
4. Do explanations improve user trust in the model — and is this trust calibrated?

---

## Core Concepts & Theory

### The Three Explanation Techniques

The DashAI XAI module implements three model-agnostic explanation techniques:

#### 1. Partial Dependence Plots (PDP)

PDPs show the marginal effect of one or two features on the predicted outcome, averaging over all other features:

```
PDP(x_s) = E_{x_c}[f(x_s, x_c)] = (1/n) Σᵢ f(x_s, x_c^(i))
```

Where x_s is the feature of interest, x_c is the complement (all other features), and f is the model.

**Visual representation:** A line plot showing how predicted probability changes as the feature value varies.

**Accessibility advantage:** Directly answers "how does feature X affect the prediction?" without requiring any statistical background beyond reading a line graph.

#### 2. Permutation Feature Importance (PFI)

PFI measures global feature importance by randomly shuffling a feature's values and measuring the resulting increase in prediction error:

```
PFI(x_j) = L(f, X_{shuffled_j}) - L(f, X)
```

A large increase in error when feature j is shuffled indicates that feature j is important to the model.

**Visual representation:** A bar chart ranking features by their importance.

**Accessibility advantage:** Directly answers "which features matter most?" — a question naturally interpretable by non-technical users.

#### 3. KernelSHAP

KernelSHAP computes approximate Shapley values — the fair distribution of prediction credit among features — using a kernel-weighted local linear model:

```
SHAP(xᵢ) ≈ argmin_{g ∈ G} L(f, g, πₓ) + Ω(g)
```

Where G is the class of additive linear models, πₓ is the SHAP kernel (weighting samples by their similarity to the explained instance), and Ω(g) is a regularization term.

Shapley values satisfy desirable axioms: efficiency (values sum to the prediction), symmetry (equal contributions get equal values), dummy (zero-impact features get zero), linearity.

**Visual representation:** A waterfall or force plot showing each feature's positive/negative contribution to a specific prediction.

**Accessibility advantage:** Answers "why did the model make THIS specific prediction?" at the instance level.

### The DashAI Platform

DashAI is an open-source no-code ML platform with a web-based interface. The XAI module was designed following UX principles for non-technical users:
- **Layered disclosure:** Simple visualizations first, mathematical details available on demand
- **Plain language:** Explanation titles and labels avoid technical jargon
- **Contextual help:** Tooltips explain each visualization without requiring separate documentation
- **Comparative view:** Explanations are shown alongside model performance metrics for calibrated trust

### Human-Centered XAI Design Principles

The module applies established human-centered XAI design principles (Liao et al., 2020; Wang et al., 2021):

1. **Proximity:** Explanations are generated within the model-building workflow (not in a separate tool)
2. **Actionability:** Each explanation is paired with guidance on what to do with the insight
3. **Causality illusion avoidance:** PDP documentation explicitly notes correlational (not causal) interpretation
4. **Appropriate trust:** The explanation interface includes model performance metrics to discourage over-reliance

---

## Main Ideas & Key Contributions

### 1. First XAI User Study in a No-Code ML Platform

This is the **first user study evaluating XAI explanations integrated directly into a no-code ML workflow**, studying participants without coding experience using a complete model-building + explanation interface. Prior user studies evaluated standalone explanation tools or assumed users were data scientists.

### 2. High Task Success Rate for Non-Technical Users

The primary finding: **ML novices can successfully interpret XAI explanations** with ≥80% task success rate across all explanation types. This challenges the implicit assumption that XAI is only accessible to technical users.

**Task success by explanation type:**
| Explanation | Novice Success Rate | Expert Success Rate |
|-------------|-------------------|--------------------|
| PFI (bar chart) | 88.3% | 96.7% |
| PDP (line plot) | 82.1% | 94.2% |
| KernelSHAP | 80.4% | 95.8% |

### 3. Novice-Expert Divergence in Perceived Quality

While novices successfully complete tasks, they differ from experts in *how they evaluate* explanation quality:

**Novices:**
- Rate explanations as highly useful, accurate, and trustworthy (ESS mean: 4.1/5)
- Show high trust improvement after viewing explanations (TiA improvement: +0.7)
- Tend toward over-reliance: high trust even for poor-quality explanations

**Experts:**
- More critical of explanation completeness and sufficiency (ESS mean: 3.2/5)
- Show moderate trust improvement (TiA improvement: +0.3)
- Correctly identify limitations of model-agnostic explanations (e.g., PDP marginalizes distribution)

This finding has direct implications for XAI design: novices need **calibration mechanisms** to prevent uncritical trust in model explanations.

### 4. Explanation Satisfaction Scale (ESS) Validation

The paper validates the **Explanation Satisfaction Scale (ESS)** for the no-code ML context. ESS (internal consistency Cronbach's α = 0.74) is an existing questionnaire for measuring explanation quality perception, adapted here for non-technical users.

### 5. Trust in Automation (TiA) Improvement

Explanations significantly improve perceived predictability and confidence on the **Trust in Automation scale** (TiA, α = 0.60). This confirms that XAI explanations do change user-model relationships — but the change is more pronounced for novices, raising calibration concerns.

### 6. Open-Source Contribution: DashAI XAI Module

The paper contributes a fully open-source, deployable XAI module for no-code ML. Unlike research prototypes, DashAI is designed for real-world deployment and includes:
- Full implementation of PDP, PFI, and KernelSHAP
- User interface with layered disclosure design
- Documentation and tutorials for platform users

---

## Methodology & Implementation

### Study Design

**Participants:** N = 20 (10 novices: 0-1 year ML experience; 10 experts: 3+ years ML experience)  
**Setting:** Remote, think-aloud protocol with screen recording  
**Platform:** DashAI web interface (browser-based, no installation)

### Tasks

Participants completed three types of explanation tasks for each explanation type:

1. **Feature identification:** "Which feature has the most impact on the prediction?" (PFI task)
2. **Trend interpretation:** "As age increases, does predicted salary increase or decrease?" (PDP task)
3. **Instance explanation:** "Why did the model predict this person will default on a loan?" (SHAP task)

### Datasets Used in the Study

| Dataset | Domain | # Features | # Samples | Prediction Task |
|---------|--------|-----------|---------|----------------|
| Adult Income | Socioeconomic | 14 | 32,561 | Income >$50K |
| Pima Diabetes | Healthcare | 8 | 768 | Diabetes diagnosis |
| Titanic Survival | Historical | 7 | 891 | Survival prediction |

These datasets were selected for:
- **Familiarity:** Non-technical users have intuitions about the domain (income, health)
- **Interpretability ground truth:** Known causal relationships allow validating interpretation accuracy

### Instruments

**Explanation Satisfaction Scale (ESS):** 8-item Likert questionnaire measuring:
- Satisfaction with explanation detail
- Perceived accuracy of explanation
- Usefulness for decision-making
- Completeness of information provided

**Trust in Automation Scale (TiA):** 19-item questionnaire measuring:
- Propensity to trust the system
- Perceived predictability
- Reliability confidence

**Task success:** Coded by two independent raters (Cohen's κ = 0.83, near-perfect agreement)

### Limitations

1. **Small sample size (N=20):** Limits statistical power and generalizability; future work requires larger, more diverse samples
2. **Convenience sampling:** Participants recruited from university community; may not represent target user population (e.g., healthcare professionals, legal practitioners)
3. **Short-term trust effects:** The study measures immediate trust changes; long-term trust calibration effects are unknown
4. **Simplified tasks:** Real-world XAI tasks are more complex; the controlled tasks may overestimate success rates
5. **English-only interface:** Limits accessibility research for non-English-speaking populations

---

## Practical Applications & Real-World Use Cases

### 1. Healthcare Decision Support

**Scenario:** A primary care physician uses a no-code clinical prediction model to assess patient readmission risk. The KernelSHAP explanation shows that the model heavily weighted "recent ER visits" — the physician can validate this clinically relevant feature and adjust their trust accordingly.

**Research implication:** The finding that novices over-trust explanations is critical here: physicians with limited ML experience may follow AI recommendations uncritically. The paper's call for calibration mechanisms is directly applicable to clinical AI safety.

### 2. Legal and Criminal Justice

**Scenario:** A paralegal uses a no-code recidivism prediction tool. PFI shows that "prior convictions" is the most important feature, prompting legal scrutiny of whether this feature introduces racial bias.

**Regulatory implication:** The EU AI Act classifies law enforcement AI as high-risk, requiring "appropriate human oversight." SHAP-based explanations in no-code platforms could support this requirement for non-technical legal professionals.

### 3. Education and Teacher Assessment

**Scenario:** A school administrator uses a no-code model to predict student dropout risk. PDP shows that "attendance rate" has a non-linear effect on risk (high risk below 70%, then rapid improvement). This actionable insight doesn't require understanding machine learning.

### 4. Small Business and Non-Profits

**Scenario:** A non-profit uses a no-code ML platform to optimize resource allocation. PFI reveals which demographic factors drive donation patterns, enabling targeted outreach — without requiring a data scientist on staff.

### 5. GDPR Right to Explanation

Article 22 of GDPR requires that individuals subject to automated decisions receive meaningful explanations. DashAI's XAI module provides a deployable implementation of this requirement for organizations building no-code ML systems — without requiring legal teams to understand SHAP mathematics.

---

## Insights & Implications

### Democratization Requires Calibration

The study's most important finding is that **democratizing XAI creates a calibration problem**: novices are enthusiastic adopters of explanations but may lack the critical framework to identify explanation limitations. This is not a reason to withhold explanations — rather, it is a design challenge: XAI for non-technical users must include explicit uncertainty communication and trust calibration mechanisms.

### The Novice-Expert Gap Is Not About Comprehension

Novices achieve comparable task success rates to experts, demonstrating that **comprehension is not the limiting factor**. The gap is in *evaluation*: experts can identify when an explanation is insufficient or potentially misleading; novices generally cannot. Future work should focus on teaching explanation evaluation skills, not just explanation interpretation.

### Platform-Native XAI Is Essential

The study suggests that **standalone XAI tools are insufficient** for non-technical users: explanations must be integrated into the workflow where decisions are made. A separate explanation dashboard requires users to context-switch, while platform-native explanations reduce cognitive load and improve contextual understanding.

### Trust Is Not the Right Metric Alone

The TiA improvement for novices (high trust increase) versus experts (moderate trust increase) shows that trust improvement is not straightforwardly good. What matters is **calibrated trust**: appropriate trust in reliable explanations, appropriate skepticism about incomplete ones. Future XAI evaluation should measure trust calibration (accuracy of trust), not just trust level.

### Open Questions

1. **Longitudinal trust effects:** Does XAI improve decision quality over time, or does over-reliance degrade performance?
2. **Explanation style preferences:** Do different professional domains (medical, legal, financial) prefer different explanation formats?
3. **Adaptive explanations:** Can XAI systems detect user expertise and adapt explanation complexity accordingly?
4. **Cross-cultural accessibility:** Are the same visualization formats universally accessible, or do cultural conventions affect interpretation?
5. **Adversarial explanations:** Can sophisticated users be misled by technically correct but strategically chosen SHAP explanations?

---

## Code & Resources

- **ArXiv Paper:** [arxiv.org/abs/2602.11159](https://arxiv.org/abs/2602.11159)
- **DashAI Platform:** [github.com/DashAI-Team/DashAI](https://github.com/DashAI-Team/DashAI) (open source)
- **SHAP Library:** [github.com/shap/shap](https://github.com/shap/shap)
- **PDPbox:** Partial Dependence Plot library

### DashAI Quick Start

```bash
# Install DashAI
pip install dashai

# Launch the no-code ML platform
dashai server
```

Navigate to `http://localhost:3000` to access the interface. The XAI module is accessible from the "Explain Model" tab after training any classifier.

### Implementing the XAI Module Components

```python
import shap
import numpy as np
from sklearn.inspection import permutation_importance, partial_dependence

# Permutation Feature Importance
result = permutation_importance(model, X_test, y_test, n_repeats=30)
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance_mean': result.importances_mean,
    'importance_std': result.importances_std
}).sort_values('importance_mean', ascending=False)

# Partial Dependence Plot
pd_result = partial_dependence(model, X_test, features=['age'], kind='average')

# KernelSHAP
explainer = shap.KernelExplainer(model.predict_proba, shap.sample(X_train, 100))
shap_values = explainer.shap_values(X_test[:10])
shap.waterfall_plot(shap.Explanation(
    values=shap_values[1][0],
    base_values=explainer.expected_value[1],
    data=X_test.iloc[0],
    feature_names=feature_names
))
```

---

## Related Work & Context

### Human-Centered XAI Literature

- **User Study on SHAP vs. LIME (Chromik et al., 2021):** Found domain experts prefer feature-based explanations; CNPC extends this to non-expert users
- **Explanation Satisfaction Scale (ESS) (Hoffman et al., 2018):** Original ESS development; this paper validates it for ML contexts
- **Appropriate Reliance on AI (Buçinca et al., 2021):** Foundational work on trust calibration in AI systems; directly relevant to the novice over-trust finding

### No-Code ML and AutoML

- **AutoML Benchmarking (Zoller & Huber, 2021):** Demonstrates no-code ML accessibility gains
- **MLJAR (Płoński, 2021):** Another no-code ML platform — DashAI adds XAI capabilities lacking in most AutoML tools

### Related 2025-2026 Papers

- **"Beyond XAI: Post-XAI Research Directions" (2602.24176):** Argues current XAI has reached a plateau; this paper's calibration findings support the need for new research directions
- **"Dataset from User Study on XAI Comprehensibility" (Nature Scientific Data, 2025):** Companion dataset to user studies on XAI comprehension
- **"The Explainable AI Dilemma under Knowledge Imbalance" (npj Digital Medicine, 2025):** Medical XAI study showing experts and non-experts differ in XAI utility — validated by this paper's findings in a general ML context

### Connection to Broader xAI Themes

This paper sits at the intersection of several xAI research threads:
- **Human-computer interaction (HCI) and AI:** How do people actually use AI explanations?
- **AI fairness and accountability:** Can non-technical users use explanations to audit model bias?
- **Educational AI:** How do we teach people to critically evaluate AI explanations?
- **Regulatory compliance:** Bridging the gap between technical XAI outputs and legally meaningful explanations

The paper's most lasting contribution may be its demonstration that **xAI research cannot optimize only for technical quality** — it must simultaneously optimize for human accessibility, calibration, and appropriate use.
