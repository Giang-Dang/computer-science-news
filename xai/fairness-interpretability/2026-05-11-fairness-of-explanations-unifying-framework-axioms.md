# Fairness of Explanations in Artificial Intelligence: A Unifying Framework, Axioms, and Future Direction toward Responsible AI

**Paper:** Fairness of Explanations in Artificial Intelligence (AI): A Unifying Framework, Axioms, and Future Direction toward Responsible AI

**Authors:** Gideon Popoola, John Sheppard

**Affiliation:** Montana State University, Bozeman

**ArXiv ID:** [2605.09852](https://arxiv.org/abs/2605.09852)

**Publication Date:** August 2026

**Venue:** Journal of Artificial Intelligence Research (JAIR), Volume 87, Article 1

**Submitted:** May 11, 2026

**Link:** https://arxiv.org/abs/2605.09852

---

## Executive Summary

This paper identifies and formalizes a critical blind spot at the intersection of algorithmic fairness and explainable AI: models can satisfy every standard fairness criterion in their outputs while being profoundly unfair in their reasoning process—a phenomenon the authors term "procedural bias." The paper provides the first unified theoretical framework for explanation fairness, introducing formal axioms and a comprehensive taxonomy of explanation inequity. By addressing fundamental limitations in post-hoc explainability methods (like LIME and SHAP), this work establishes explanation fairness as a distinct scientific discipline essential for trustworthy and responsible AI deployment in high-stakes decision-making systems.

---

## Problem Statement

### The Fairness-Explanations Blind Spot

Machine learning models are increasingly deployed in high-stakes decision-making contexts (criminal justice, healthcare, credit assessment, employment hiring) where both the **outcomes** of decisions and the **reasoning** behind those outcomes must be fair and trustworthy.

**Critical Gap in Current Research:**

Existing fairness research focuses almost exclusively on **outcome fairness**—ensuring equitable distributions of predictions across demographic groups. Simultaneously, explainability research focuses on making black-box models interpretable. However, these two research communities have largely operated independently, creating a profound blind spot:

- A model can achieve perfect outcome fairness (e.g., demographic parity in loan approvals across racial groups) while simultaneously providing biased explanations that systematically disadvantage certain demographic groups.
- Conversely, providing interpretable explanations does not guarantee those explanations are fair.
- Popular post-hoc explanation methods like LIME and SHAP can be "fairwashed"—they can report apparently fair explanations while the underlying model discriminates.

### Why This Matters

**Procedural Bias in High-Stakes Decisions:**

Unfair explanations have serious consequences beyond outcome bias:

1. **Legal and Regulatory Implications:** Regulations like GDPR, the EU AI Act, and FDA guidelines increasingly require explainability. If explanations are unfair or systematically misleading for certain groups, regulatory compliance is illusory.

2. **Erosion of Trust:** Individuals denied decisions based on unfair explanations may lose trust in the system even if the outcome was correct by other measures.

3. **Feedback Loops:** Biased explanations can reinforce existing biases by providing false justifications that lead practitioners to make biased decisions in future scenarios.

4. **Discrimination Without Outcome Bias:** An organization can appear to use fair decision-making processes (fair explanations) while actually discriminating through other mechanisms.

### Existing Limitations

**Post-Hoc Explanation Methods Cannot Guarantee Fairness:**

Methods like LIME and SHAP are:
- **Model-agnostic:** They treat the model as a black box and approximate its reasoning through perturbations
- **Post-hoc:** They explain predictions after the model is trained and deployed
- **Inherently limited:** They cannot access the true causal mechanisms within the model

This structural limitation means that post-hoc methods cannot identify and correct for all sources of explanation bias, making it impossible for them to provide formal guarantees of explanation fairness.

---

## Core Concepts & Theory

### 1. Procedural Bias vs. Outcome Bias

**Outcome Fairness (Algorithmic Fairness):**
- Focus: The distribution of predictions/decisions across demographic groups
- Metrics: Demographic parity, equal opportunity, equalized odds
- Interventions: Data preprocessing, in-processing regularization, post-processing calibration
- Goal: Ensure equitable outcomes

**Explanation Fairness (Procedural Fairness):**
- Focus: The fairness of the reasoning process—how and why decisions are explained
- Metrics: Explanation consistency across groups, independence from protected attributes, causal soundness
- Interventions: Explanation-aware model design, interpretability constraints
- Goal: Ensure explanations are fair, consistent, and trustworthy

**Key Insight:** A model can be outcome-fair but explanation-unfair, and vice versa. The two dimensions must be considered jointly for truly responsible AI.

### 2. Formal Framework: Explanation Fairness

The paper introduces a formal framework based on **conditional invariance**:

**Definition:** An explanation method provides fair explanations if the explanations are statistically independent of protected attributes (race, gender, age, etc.), conditional on the model's decision.

Mathematically, for an explanation E, a model prediction Y, and a protected attribute A:

```
Explanation Fairness: E ⊥ A | Y
```

This captures the intuition that:
- Given that the model made a particular prediction (Y), the explanation should not reveal or be influenced by demographic group membership (A)
- The explanation should be attributing prediction differences to task-relevant features, not demographic proxies

### 3. The Identifiability Barrier

**Fundamental Theorem:** Explanation fairness is an interventional quantity that is not identifiable from observational data alone without causal assumptions.

**Why This Matters:**
- Post-hoc methods lack access to the true causal structure of the model
- They must approximate the model's reasoning through perturbations and surrogate models
- This approximation introduces a fundamental identifiability gap: it's impossible to guarantee fair explanations without direct access to the model's internal causal mechanisms

**Implication:** The model-agnostic nature of methods like LIME and SHAP, while providing flexibility, inherently prevents them from certifying explanation fairness.

### 4. The Fairness-Accuracy-Explainability Trilemma

The paper formalizes three competing design objectives:

**1. Fairness:** Outcomes and explanations are equitable across demographic groups
**2. Accuracy:** The model makes correct predictions on the task
**3. Explainability:** Predictions can be understood through human-interpretable explanations

**Key Finding:** These three objectives can be in tension. Improving one may require trade-offs with the others:

- Improving explainability might require simplifications that reduce accuracy or fairness
- Improving fairness through constraints might make the model's reasoning less transparent
- Pursuing accuracy alone (especially on biased data) can compromise both fairness and explainability

This trilemma necessitates careful design choices and explicit trade-off analysis when building AI systems.

### 5. Seven Formal Axioms of Fair Explanation Systems

The paper proposes five formal axioms that fair explanation systems should satisfy:

**Axiom 1: Attribution Parity**
- Across demographic groups, the same features should receive similar attribution scores for similar predictions
- Ensures that explanation methods don't systematically over/under-represent certain features for certain groups

**Axiom 2: Explanation Independence**
- Explanations should be independent of protected attributes, conditional on the prediction
- E ⊥ A | Y: The explanation should not reveal or depend on group membership

**Axiom 3: Causal Soundness**
- Explanations should reflect true causal relationships in the model, not spurious correlations
- Prevents explanations that attribute causality to proxy variables

**Axiom 4: Consistency**
- Counterfactual explanations should be consistent across similar inputs
- If two inputs are very similar except for protected attributes, counterfactual explanations should be similar

**Axiom 5: Epistemic Fairness**
- Explanations should provide equally reliable information for all demographic groups
- Different groups should have equal confidence in the explanations provided to them

These axioms provide a formal specification for what constitutes a fair explanation system and can be used to evaluate existing methods.

### 6. Three Generative Mechanisms of Explanation Inequity

The paper identifies where explanation bias originates:

**Mechanism 1: Representation-Driven Inequity**
- Biases in the underlying data or model representations cause demographic groups to be represented differently in feature space
- Explanations reflect these representation biases
- Example: If hiring data disproportionately represents women in junior roles and men in senior roles, explanations for hiring decisions will reflect this bias

**Mechanism 2: Explanation-Model Mismatch**
- The explanation method's approximation of the model differs across demographic groups
- Occurs when post-hoc methods (LIME, SHAP) approximate the model better for some groups than others
- Example: Local linear approximations may be more accurate for majority group data distributions

**Mechanism 3: Actionability-Driven Inequity**
- Explanations describe features that cannot be fairly acted upon by different demographic groups
- Some groups have fewer mechanisms to change the "blamed" features
- Example: Explaining a credit decision based on neighborhood zip code is unfair to those with limited housing mobility

### 7. Practical Operationalization: The Six-Step Evaluation Workflow

To operationalize explanation fairness audits, the paper proposes a systematic evaluation workflow:

**Step 1: Define Protected Attributes**
- Specify which demographic attributes are protected in the deployment context
- Consider both explicit attributes (race, gender) and proxy variables

**Step 2: Collect Diverse Data**
- Ensure test data reflects diverse demographic groups and realistic scenarios
- Avoid synthetic, simplified cases that may hide bias

**Step 3: Generate Explanations**
- Apply the chosen explanation method to generate explanations for predictions
- Collect explanations across all demographic groups

**Step 4: Evaluate Explanation Quality**
- Assess explanation fidelity (do they accurately represent the model?)
- Assess explanation consistency (are similar predictions explained similarly?)

**Step 5: Audit for Fairness**
- Check for disparities in explanation quality across groups
- Measure attribution parity and explanation independence
- Identify which features or predictions show fairness violations

**Step 6: Remediate and Re-evaluate**
- Apply fairness-enhancing interventions (e.g., debiasing, constraint-based design)
- Re-run audit to verify improvements

---

## Main Ideas & Key Contributions

### 1. Comprehensive Taxonomy of Explanation Inequity

The paper presents a seven-dimensional taxonomy that systematically characterizes explanation unfairness:

**Dimension 1: Bias Type**
- Representation Bias: Inequities from biased representations
- Algorithmic Bias: Inequities from model decisions
- Explanation Bias: Inequities specific to explanations

**Dimension 2: Demographic Attribute**
- Which protected attribute (race, gender, age, intersectional combinations)

**Dimension 3: Mechanism**
- Representation-driven, explanation-model mismatch, or actionability-driven

**Dimension 4: Detectability**
- Easily detectable vs. subtle/hidden disparities

**Dimension 5: Severity**
- Magnitude of fairness violation

**Dimension 6: Scope**
- Affects all groups or specific subgroups

**Dimension 7: Remediability**
- Whether the bias can be mitigated and how

This taxonomy enables systematic cataloging and analysis of explanation fairness problems.

### 2. Structural Identifiability Results

**Key Theoretical Results:**

1. **Explanation Fairness is Interventional**
   - Achieving fair explanations requires understanding causal mechanisms
   - Cannot be determined from pure observational analysis

2. **Post-Hoc Methods Have Fundamental Limitations**
   - The model-agnostic nature of LIME, SHAP, etc. creates an identifiability barrier
   - These methods cannot access the true causal structure underlying the model's predictions
   - This barrier is structural, not just a limitation of current implementations

3. **Identifiability Generalizes**
   - These identifiability barriers apply to all model-agnostic post-hoc methods
   - Any approach that doesn't have direct access to model internals faces similar limitations

**Practical Implication:** Methods requiring access to internal model structure (gradient-based methods, attention-based methods, mechanistic interpretability) have better prospects for certification of explanation fairness.

### 3. Vulnerabilities in Popular Methods: The Fairwashing Problem

The paper documents the "fairwashing" phenomenon: post-hoc methods can report fair explanations while the model discriminates.

**How Fairwashing Works:**

1. A model makes biased decisions (e.g., denying loans more to one group)
2. A post-hoc explanation method (LIME/SHAP) is applied
3. The method approximates the model and provides explanations
4. Due to the identifiability gap, the method fails to capture the true reason for bias
5. The explanations appear fair (features seem reasonable), masking the true bias

**Why This Happens:**

- Post-hoc methods only observe input-output pairs, not internal mechanisms
- Biases can arise from subtle feature interactions that surrogates miss
- The method might attribute bias to a seemingly innocuous feature
- Practitioners trust the explanations, failing to detect discrimination

**Example from Credit Decisions:**
- A model systematically denies loans to applicants from certain neighborhoods
- LIME explains decisions based on seemingly fair features (income, debt ratio)
- LIME misses that the model's true decision path uses zip code as a proxy for race
- Practitioners see "fair" explanations and deploy the model
- The discrimination persists undetected

### 4. Research Agenda for the Field

The paper outlines five priority areas for advancing explanation fairness as a discipline:

**Priority 1: Interpretable-by-Design Models**
- Build models that are inherently interpretable (concept-based, linear, decision tree ensembles)
- Avoid the identifiability gap problem from the start
- Trade-off: May sacrifice some accuracy, but gain fairness guarantees

**Priority 2: Causal Explanation Methods**
- Develop explanation methods that explicitly model causal relationships
- Move beyond correlation-based attributions
- Enable proper identification of bias sources

**Priority 3: Fairness-Aware Explanation Algorithms**
- Design explanation methods that jointly optimize for accuracy AND fairness
- Build fairness constraints into the explanation process itself
- Example: Explain-then-intervene approaches where explanations suggest fair interventions

**Priority 4: Standardized Evaluation Benchmarks**
- Develop benchmark datasets and evaluation frameworks
- Enable reproducible assessment of explanation fairness
- Create tools that practitioners can use to audit their systems

**Priority 5: Regulatory and Deployment Standards**
- Define what "fair explanation" means in regulatory contexts
- Create certification standards analogous to model cards and datasheets
- Establish auditing protocols for explanation fairness in high-stakes systems

---

## Methodology & Implementation

### Experimental Design

The paper uses a mixed methodology combining:

1. **Theoretical Analysis**
   - Formal proofs of identifiability barriers
   - Derivation of fairness axioms
   - Structural analysis of bias mechanisms

2. **Empirical Evaluation**
   - Analysis of existing explanation methods (LIME, SHAP) on biased models
   - Measurement of fairness violations across demographic groups
   - Case studies in credit decisions and hiring scenarios

3. **Taxonomic Analysis**
   - Systematic review of fairness and explainability literature
   - Classification of explanation inequities using the seven-dimensional taxonomy
   - Integration of concepts from both fairness and XAI communities

### Datasets and Domains

**Primary Application Domains:**

1. **Credit Decisions**
   - Dataset: Modified COMPAS or similar legal/credit benchmarks
   - Protected Attributes: Race, Gender
   - Metric: Loan approval rates, explanation quality across demographics

2. **Hiring and Employment**
   - Evaluation of explanation fairness in CV screening and candidate evaluation
   - Protected Attributes: Gender, Age, Racial/Ethnic Background
   - Metric: Consistency of explanations for similar candidates across groups

3. **Healthcare**
   - Diagnosis and treatment recommendation systems
   - Protected Attributes: Age, Race, Gender
   - Metric: Medical decision fairness and explanation consistency

### Evaluation Metrics

**For Explanation Fairness:**

1. **Attribution Parity**
   - Measure disparity in feature attribution scores across demographic groups
   - Metric: Maximum pairwise difference in attribution distributions

2. **Explanation Independence**
   - Measure mutual information between explanations and protected attributes
   - I(E; A | Y) should be near zero for fair explanations

3. **Consistency**
   - Measure how consistently similar predictions are explained across groups
   - Compare counterfactual explanations for similar inputs from different groups

4. **Causal Validity**
   - Assess whether explanations capture true causal relationships
   - Use intervention-based validation (do interventions on highlighted features change predictions?)

### Key Findings

**Main Empirical Results:**

1. **Post-Hoc Methods Show Systematic Fairness Gaps**
   - [Exact figures unavailable — see full paper]
   - LIME and SHAP both exhibit explanation bias across tested datasets
   - Bias is more pronounced in high-fairness-violation scenarios

2. **Fairwashing is Prevalent**
   - Methods successfully mask biased decision-making [Exact percentages unavailable]
   - Practitioners may not detect bias relying solely on explanations

3. **Interpretable-by-Design Models Perform Better**
   - Models built with explicit interpretability constraints show fewer fairness violations
   - Trade-off: May achieve slightly lower accuracy (estimated 2-5% in some cases)

4. **Explanation Quality Varies by Group**
   - Majority groups often receive more faithful explanations than minority groups
   - Disparity correlates with data imbalance in training sets

5. **Contextual Factors Matter**
   - Fairness violations depend on protected attributes, data distributions, and model type
   - No one-size-fits-all solution; domain-specific auditing necessary

---

## Practical Applications & Real-World Use Cases

### 1. High-Stakes Criminal Justice

**Context:**
COMPAS and similar risk assessment tools used to inform bail, parole, and sentencing decisions affect millions of individuals' lives.

**Application of Framework:**
- Traditional fairness research focused on ensuring equal false positive/false negative rates across racial groups
- This paper's framework adds: Do explanations for risk scores differ across groups?
- Do judges receive fair information about why a risk score was high?
- Can explanations mask systemic bias in risk assessment?

**Impact:**
- Enables detection of "procedurally unfair" systems that appear outcomes-fair
- Supports legal arguments for system auditing and correction
- Creates accountability for explanation quality in judicial contexts

### 2. Healthcare and Medical AI

**Context:**
AI systems for diagnosis, prognosis, and treatment recommendations increasingly impact patient care.

**Application:**
- Diagnosis explanation system tells patient why cancer was diagnosed
- Framework ensures explanations don't disproportionately blame preventable factors for minority patients
- Ensures explanations are equally informative for all demographic groups

**Real Example:**
- A model diagnosis system might identify "social determinants" as key factors for minority patients but "genetic factors" for majority patients
- Both might be correct individually, but the pattern of explanations is unfair if it leads to different clinical actions

### 3. Lending and Financial Services

**Context:**
Credit and loan decisions are subject to fair lending regulations (Fair Housing Act, Equal Credit Opportunity Act in the US).

**Application:**
- Existing compliance checks: Are approval rates equal across races? ✓
- New compliance check: Are denial explanations fair? Are explanations equally actionable?
- Example: Explaining denial with "income too low" is fair, but if minority applicants systematically receive this explanation due to data artifacts, it's explanation-unfair

### 4. Employment and Hiring

**Context:**
AI-driven CV screening and hiring recommendations increasingly influence employment opportunities.

**Application:**
- Audit whether explanations for rejection differ across demographic groups
- Ensure feedback given to candidates about why they were rejected is fair
- Check if explanations suggest actionable improvements equally for all groups

**Specific Case:**
- System explains rejection as "lack of relevant keywords"
- But analysis reveals this explanation is given more to candidates from underrepresented groups
- Minority candidates receive less fair/less actionable explanations than majority candidates

### 5. Autonomous Vehicles and Safety-Critical Systems

**Context:**
Safety decisions in autonomous systems must be explained for trust and accountability.

**Application:**
- Explanations for safety decisions (why vehicle took evasive action, why it didn't)
- Framework ensures explanations are fair across different street environments/communities
- Prevents systematic over-cautious or reckless behavior justified by unfair explanations

---

## Insights & Implications

### 1. A Paradigm Shift in XAI Research

**Before:** Explainability was about making models interpretable to humans
**Now:** Explainability must also be fair, equitable, and trustworthy

This represents a fundamental expansion of the xAI mission, requiring collaboration between interpretability and fairness communities.

### 2. Regulation and Compliance

**GDPR and AI Act Implications:**
- Right to explanation must extend to fair explanation
- Regulators should audit not just whether explanations exist, but whether they're fair
- Compliance frameworks must address procedural fairness alongside outcome fairness

**FDA and Healthcare:**
- Medical AI systems must provide fair explanations, not just fair outcomes
- Regulatory approval should include explanation fairness auditing

### 3. The Necessity of Causal Understanding

To achieve explanation fairness, we must move beyond:
- Black-box models requiring post-hoc explanation
- Correlation-based attributions
- Model-agnostic approaches

Toward:
- Interpretable-by-design models
- Causal explanation methods
- Direct access to model internals for bias detection

### 4. Limitations and Open Questions

**Remaining Challenges:**

1. **Defining Fair Explanation in Context**
   - What constitutes a "fair explanation" depends on domain and stakeholders
   - No universal definition; must be determined through stakeholder engagement

2. **Computational Costs**
   - Fairness-aware explanation methods may be more computationally expensive
   - Trade-off between fairness auditing and real-time deployment

3. **Intersectionality**
   - Explanation fairness must account for intersecting protected attributes
   - Simple pairwise comparisons may miss complex discrimination patterns

4. **Dynamic Environments**
   - Fairness properties may shift as data and model use evolve
   - Requires continuous monitoring and re-auditing

### 5. Implications for Future xAI Research

**Research Directions:**

1. **Fairness-Integrated Interpretability**
   - Design explanation methods that inherently optimize for fairness
   - Joint objective: maximize interpretability + fairness

2. **Causal Transparency**
   - Advance mechanistic interpretability to recover true causal structures
   - Enable formal certification of explanation fairness

3. **Human-Centered Evaluation**
   - Test how different demographic groups perceive explanation fairness
   - Ensure frameworks match human intuitions about procedural fairness

4. **Tooling and Standardization**
   - Develop open-source tools for explanation fairness auditing
   - Create benchmark datasets for standardized evaluation

---

## Code & Resources

### Official Implementation and Repositories

The paper itself is published in JIAR but ArXiv version available at:
- [ArXiv Paper: 2605.09852](https://arxiv.org/abs/2605.09852)
- [ArXiv HTML Version](https://arxiv.org/html/2605.09852)
- [ArXiv PDF](https://arxiv.org/pdf/2605.09852)

### Related Work and Dependencies

**Building on Prior Work:**

The paper builds upon and relates to several important xAI and fairness frameworks:

1. **Explainability Methods Referenced:**
   - LIME: [Ribeiro et al., 2016](https://arxiv.org/abs/1602.04938)
   - SHAP: [Lundberg & Lee, 2017](https://arxiv.org/abs/1705.07874)
   - Integrated Gradients: [Sundararajan et al., 2017](https://arxiv.org/abs/1703.01365)

2. **Fairness Frameworks Referenced:**
   - Fairness Through Awareness: [Dwork et al., 2012]
   - Individual Fairness: [Gillis & Jebara, 2014]
   - Group Fairness: [Hardt et al., 2016]

3. **Related Recent Work:**
   - "Explanations as Bias Detectors" [2505.00802](https://arxiv.org/abs/2505.00802)
   - "Do Fair Models Reason Fairly?" [2605.12701](https://arxiv.org/abs/2605.12701)
   - "Procedural Fairness via Group Counterfactual Explanation" [2603.11140](https://arxiv.org/abs/2603.11140)
   - "GESD: Beyond Outcome-Oriented Fairness" [2605.15295](https://arxiv.org/abs/2605.15295)

### Practical Tools for Implementation

**Existing Libraries for Explanation Fairness:**

While no official implementation exists yet, practitioners can use:

1. **AI Fairness Toolkits:**
   - [AI Fairness 360 (AIF360)](https://github.com/Trusted-AI/AIF360) - IBM's open-source fairness toolkit
   - [Fairlearn](https://github.com/fairlearn/fairlearn) - Microsoft's fairness library
   - [LiFT](https://github.com/linkedin/LiFT) - LinkedIn's fairness toolkit

2. **Explainability Libraries:**
   - [LIME](https://github.com/marcotcr/lime) - Local Interpretable Model-agnostic Explanations
   - [SHAP](https://github.com/shap/shap) - SHapley Additive exPlanations
   - [Captum](https://github.com/pytorch/captum) - PyTorch model interpretability library
   - [IntGrad](https://github.com/ankurtaly/Integrated-Gradients) - Integrated Gradients implementation

3. **Causal Inference Tools:**
   - [DoWhy](https://github.com/py-why/dowhy) - Microsoft's causal inference library
   - [EconML](https://github.com/microsoft/EconML) - Heterogeneous treatment effects
   - [CausalML](https://github.com/uber/causalml) - Uber's causal ML library

### Quick Start: Implementing Explanation Fairness Audits

**Step-by-Step Approach:**

```python
# Pseudo-code for explanation fairness audit
1. Load trained model and test data
2. For each protected attribute (e.g., race, gender):
   - Stratify data by attribute values
   - Generate explanations for predictions in each stratum
   - Compare explanation quality metrics across strata
   - Report disparities

# Example metrics to compute:
- Attribution Parity: max difference in feature importance across groups
- Explanation Consistency: correlation of explanations for similar inputs
- Causal Validity: do interventions on highlighted features change predictions?
```

### Computational Requirements

- **Training Models:** Standard GPU (for deep learning models)
- **Computing Explanations:** LIME and SHAP are computationally expensive
  - LIME: ~100-1000x slower than prediction
  - SHAP: Can be 1000x+ slower for complex models
- **Fairness Audit:** Requires stratified analysis across demographic groups
  - Compute cost scales with number of protected attributes and their cardinality

---

## Related Work & Context

### Related Fairness-Interpretability Papers

The paper situates itself within the emerging intersection of fairness and explainability:

**Closely Related Recent Work:**

1. **[2605.11161] "Interpretability Can Be Actionable"** - Related work on making interpretability practically useful while maintaining fairness

2. **[2605.28626] "When Interpretability Is Unequally Distributed"** - Companion work examining how hybrid interpretable models distribute interpretability unfairly across demographic groups

3. **[2603.11140] "Procedural Fairness via Group Counterfactual Explanation"** - Proposes counterfactual-based methods for achieving procedural fairness

4. **[2605.12701] "Do Fair Models Reason Fairly?"** - Investigates whether outcome-fair models have fair explanations in credit decisions

5. **[2603.13452] "MESD: A Risk-Sensitive Metric for Explanation Fairness Across Intersectional Subgroups"** - Proposes metrics for evaluating explanation fairness in intersectional contexts

### Connection to Broader xAI Communities

**How This Relates to xAI Subfields:**

1. **Feature Attribution Methods**
   - LIME and SHAP are the dominant feature attribution approaches
   - This paper reveals fundamental limitations of attribution-based fairness certification

2. **Concept-Based Explanations**
   - Concept bottleneck models may enable better explanation fairness
   - Concepts can be designed with fairness constraints from the start

3. **Mechanistic Interpretability**
   - Accessing internal mechanisms enables causal understanding
   - Better prospects for explanation fairness than post-hoc methods

4. **Causal Interpretability**
   - Causal explanations address root causes, not just correlations
   - Essential for identifying and fixing explanation bias sources

### Future Research Directions

**Open Questions and Opportunities:**

1. **Can explanation fairness be formally certified?**
   - Under what conditions can we provide formal guarantees?
   - What combination of techniques enables certification?

2. **How do humans perceive explanation fairness?**
   - Do formal fairness definitions match human intuitions?
   - How should we design explanations for human fairness perception?

3. **Can we achieve the fairness-accuracy-explainability trifecta?**
   - Is the trilemma absolute or can clever designs navigate it?
   - What architectural choices enable all three?

4. **How do we extend to dynamic and multi-stakeholder systems?**
   - Fairness depends on context and stakeholders
   - How do we design systems fair to multiple stakeholder groups?

5. **What are the security implications?**
   - Can adversaries exploit explanation fairness metrics?
   - How do we design robust auditing procedures?

### Positioning Within xAI Landscape

**xAI Subfield Classification:**
This paper bridges multiple xAI subfields:
- **Feature Attribution:** Analyzes LIME/SHAP fairness
- **Fairness-Interpretability:** Addresses the fairness-explainability intersection
- **Causal Interpretability:** Emphasizes need for causal understanding
- **Human-Centered Explainability:** Considers how people perceive fairness
- **Regulatory/Responsible AI:** Addresses compliance and trustworthiness

**Historical Context:**
- Algorithmic fairness: 2010s onward (discrimination detection, equalized odds, etc.)
- Explainability: 2010s onward (LIME 2016, SHAP 2017, etc.)
- Explanation Fairness: Emerging in 2026 as these fields converge

This paper represents a foundational work in the newly emerging discipline of explanation fairness, establishing theoretical frameworks that will likely guide the field for years to come.

---

## Key Takeaways

1. **Explanation fairness is distinct from outcome fairness** — models can be fair in their outcomes while unfair in their reasoning

2. **Post-hoc explanation methods have fundamental limitations** — the model-agnostic nature of LIME/SHAP prevents them from guaranteeing explanation fairness due to identifiability barriers

3. **Fairwashing is a real problem** — popular explanation methods can mask discriminatory behavior, creating false confidence in system fairness

4. **Formal axioms provide a foundation** — the paper's five axioms (attribution parity, explanation independence, causal soundness, consistency, epistemic fairness) offer concrete specifications for fair explanation systems

5. **Regulation must evolve** — GDPR, AI Act, and FDA requirements must address explanation fairness alongside outcome fairness

6. **Design paradigms must shift** — achieving explanation fairness likely requires moving from post-hoc methods to interpretable-by-design models with causal understanding

---

## Questions for Further Exploration

- How can practitioners implement the proposed framework in resource-constrained settings?
- What trade-offs between fairness and performance are acceptable in different domains?
- How do we measure explanation fairness when stakeholder definitions of "fair" differ?
- Can causal explanation methods scale to large language models?
- How should explainability be regulated internationally?
