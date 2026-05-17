# Fewer Than 1% of Explainable AI Papers Validate Explainability with Humans: Addressing the Critical Gap in XAI Research

## Executive Summary

This paper presents a large-scale empirical study that identifies a critical gap in explainable AI (xAI) research: fewer than 1% of XAI papers provide human-based validation of their explainability claims. By analyzing 18,254 xAI papers, the authors reveal that the overwhelming majority of xAI research lacks empirical evidence demonstrating that AI systems are actually explainable to humans, raising fundamental questions about the rigor and real-world applicability of contemporary xAI methods.

**Paper Details:**
- **Title:** Fewer Than 1% of Explainable AI Papers Validate Explainability with Humans
- **Authors:** Ashley Suh, Isabelle Hurley, Nora Smith, Ho Chit Siu
- **Affiliation:** MIT Lincoln Laboratory
- **ArXiv ID:** [2503.16507](https://arxiv.org/abs/2503.16507)
- **Submitted:** March 13, 2025
- **Venue:** CHI'25 (Late-Breaking Work)

---

## Problem Statement

The field of explainable AI has grown exponentially over the past decade, with researchers proposing countless techniques to make AI systems more interpretable and transparent. However, a fundamental question remains unanswered: **Do these techniques actually make AI explainable to humans?**

Current xAI research suffers from several critical limitations:

1. **Lack of Human Validation**: Most xAI papers present technical solutions for explaining AI behavior without validating whether these explanations are actually understandable or useful to real humans.

2. **Loose Definitions of Explainability**: The field lacks standardized criteria for what constitutes "explainability," leading researchers to rely on loosely defined proxies such as:
   - Presenting outputs in natural language
   - Ensuring responses follow some vague measure of conciseness
   - Mathematical formulations without human evaluation

3. **Gap Between Claims and Evidence**: There is a systematic disconnect between the explainability claims made in research papers and the actual empirical evidence supporting those claims through human studies.

4. **Research Rigor Concerns**: Without human validation, it's unclear whether xAI methods genuinely improve human understanding of AI systems or simply provide researchers with a false sense of confidence about interpretability.

---

## Core Concepts & Theory

### Explainability vs. Interpretability

Before addressing the validation gap, it's essential to distinguish these related concepts:

- **Interpretability**: The degree to which a human can understand and make sense of the internal mechanisms of an AI model (e.g., what features a neural network uses for predictions).

- **Explainability**: The ability to provide clear, human-understandable explanations for an AI system's decisions and behavior in specific contexts.

Critically, **interpretability of a model does not guarantee explainability to users**. A model's weights and mathematical operations may be technically understandable to experts without being explainable to domain practitioners, regulators, or affected individuals.

### Types of XAI Methods

The field typically categorizes xAI approaches:

1. **Model-Specific Methods**: Explanations tailored to particular model architectures
   - Decision trees, rule-based systems (inherently interpretable)
   - Attention mechanisms in deep learning

2. **Model-Agnostic Methods**: Post-hoc explanations applicable to any model
   - Feature importance rankings
   - Saliency maps and visualization techniques
   - Counterfactual explanations
   - LIME (Local Interpretable Model-agnostic Explanations)
   - SHAP (SHapley Additive exPlanations)

3. **Human-Centered Approaches**: Methods explicitly designed with human understanding in mind
   - Natural language explanations
   - Interactive explanation systems
   - Personalized explanations for different stakeholder groups

### Human Evaluation Frameworks

For xAI methods to be meaningful, human evaluation should assess:

- **Comprehensibility**: Do humans understand the explanation?
- **Faithfulness**: Does the explanation accurately reflect the model's reasoning?
- **Sufficiency**: Does the explanation provide enough information for users to understand decisions?
- **Actionability**: Can humans take meaningful action based on the explanation?
- **User Satisfaction**: Do users trust and feel confident in the explanations?

---

## Main Ideas & Key Contributions

### The Core Finding: The Human Validation Gap

The paper's primary contribution is the empirical quantification of a suspected but largely unexamined problem in xAI research:

**Of 18,254 papers containing keywords related to explainability and interpretability:**
- Only **253 papers** (1.4%) included terms suggesting human involvement in evaluating their xAI technique
- Only **128 papers** (0.7%) actually conducted a human study validating their explainability claims
- For every 1,000 xAI papers that don't explicitly mention humans, **fewer than 8 provide any explainability validation**

### Surprising Gap Between Intent and Evidence

A particularly revealing finding concerns papers that explicitly claim human explainability:

- Of papers that mention human evaluation in their claims: **54% provide actual validation; 46% do not**
- This suggests even when authors claim human-centered approaches, half still lack supporting evidence

### Methodological Rigor

The authors employed a systematic methodology:

1. **Librarian-Assisted Search**: Collaborated with a professional librarian to identify papers using explainability/interpretability keywords
2. **Manual Review**: Examined papers to verify whether human validation was truly conducted
3. **Strict Criteria**: Required explicit evidence of human studies—papers claiming explainability benefits without human validation were classified as "no validation"

### Implications of the Gap

The lack of human validation suggests several problems:

1. **Unvalidated Assumptions**: Most xAI research assumes its methods improve human understanding without empirical verification

2. **Mismeasured Success**: The field may be measuring technical interpretability rather than actual human explainability, conflating two distinct concepts

3. **Regulatory Risk**: As AI systems face increasing regulatory scrutiny (EU AI Act, FDA guidelines, GDPR), methods that lack human validation may fail to meet real-world compliance requirements

4. **User Trust Erosion**: Users relying on unvalidated explanations may make poor decisions based on explanations that don't actually improve their understanding

---

## Methodology & Implementation

### Research Design

**Literature Review Protocol:**
- Comprehensive search of academic literature for papers containing keywords: "explainable," "interpretable," "transparency," "interpretability," "explanation," etc.
- Time period: Retrospective analysis of accumulated xAI literature through 2024/early 2025
- Database: Appears to include major sources such as ArXiv, IEEE Xplore, and other academic repositories

**Inclusion/Exclusion Criteria:**
- **Included**: Papers that explicitly discuss methods for making AI systems explainable or interpretable
- **Excluded**: Papers that mention these terms only incidentally or tangentially

### Human Validation Classification

Papers were categorized based on whether they contained evidence of human evaluation:

1. **Human Study Conducted**: Paper includes:
   - Design of explicit human evaluation experiment
   - Participant recruitment and demographics
   - Metrics measuring human understanding, trust, or decision quality
   - Statistical analysis of results

2. **No Human Validation**: Papers presenting:
   - Only technical metrics (faithfulness indices, complexity measures)
   - Explanations without user studies
   - Claims of explainability without supporting evidence

### Analysis Approach

The team conducted:
- **Frequency Analysis**: Percentage of papers with human validation across different publication venues and time periods
- **Temporal Trends**: Whether human validation has increased as xAI matured
- **Keyword Analysis**: Relationship between explicit claims of human-centeredness and actual human validation
- **Stratified Analysis**: Examining validation rates across different xAI method categories

---

## Practical Applications & Real-World Use Cases

### Critical Application Domains

The validation gap has severe implications in domains where AI explainability is non-negotiable:

#### Healthcare & Medical AI
- **Challenge**: Clinicians need to understand AI diagnostic recommendations to validate them against clinical judgment
- **Risk**: Using xAI methods not validated with actual clinicians could lead to misdiagnosis
- **Real-World Example**: Suppose an xAI method highlights pixel-level saliency maps for a chest X-ray diagnosis. Without human validation with radiologists, it's unclear whether radiologists actually find these maps helpful or whether they trust the model more because of them

#### Financial Services & Credit Decisions
- **Challenge**: Regulatory bodies (OCC, Federal Reserve) increasingly require banks to explain AI-driven loan decisions
- **Risk**: Unvalidated explanation methods may not satisfy regulatory scrutiny or judicial review
- **Real-World Example**: A bank uses a complex ML model to decide loan eligibility. An xAI method provides feature importance rankings, but studies haven't shown these improve loan officers' understanding of why an application was denied

#### Criminal Justice & Recidivism Prediction
- **Challenge**: Defendants have a right to understand information used in bail and sentencing decisions
- **Risk**: Unvalidated explanations could provide false confidence while remaining actually unintelligible to non-technical stakeholders
- **Real-World Example**: Risk assessment algorithms use complex interactions between features. Providing feature importance alone may not help judges or defendants understand the actual decision logic

#### Autonomous Systems & Self-Driving Cars
- **Challenge**: Regulators and the public need to understand why autonomous vehicles make critical safety decisions
- **Risk**: Technical explanations of perception and planning algorithms may not convey decision rationale to stakeholders
- **Real-World Example**: An autonomous vehicle's explanation of an emergency maneuver relies on deep learning feature visualizations that may not effectively communicate the safety reasoning to accident investigators

### Regulatory & Compliance Implications

Recent regulatory frameworks explicitly require explainability:

**EU AI Act (2024)**
- High-risk AI systems must provide "meaningful information" to users
- The act's vagueness raises a question: Are unvalidated xAI methods sufficient for compliance?
- This paper suggests most methods have not been tested to determine if they provide "meaningful information" to actual humans

**FDA Guidance on Clinical Decision Support Systems**
- FDA increasingly scrutinizes AI/ML-based medical devices
- Guidance requires explanations to "promote appropriate use"
- Unvalidated explanation methods risk regulatory rejection

**GDPR Right to Explanation**
- Articles 13, 14, and 22 grant individuals rights to obtain explanations of automated decisions
- Unvalidated xAI methods may not satisfy legal requirements for meaningful explanations

---

## Insights & Implications

### Reframing the xAI Research Agenda

This paper suggests the field must undergo a paradigm shift:

1. **From Technical to Human-Centered**: xAI research should prioritize human understanding over technical interpretability metrics

2. **From Post-Hoc Addition to Design Principle**: Rather than adding explanations after model development, explainability should be a core design requirement validated throughout development

3. **From General Solutions to Context-Specific Approaches**: Different user groups (clinicians, loan officers, non-experts, policymakers) require different explanations; one-size-fits-all approaches without human validation are insufficient

### Limitations and Caveats

The paper itself acknowledges important limitations:

1. **Classification Ambiguity**: Some papers may describe human studies in ways not easily captured by keyword-based identification; the 0.7% figure represents a conservative lower bound

2. **Temporal Lag**: The analysis includes retrospective papers; the field may be improving, though the authors' expectations (40% vs. actual 0.7%) suggest improvement is far from complete

3. **Publication Bias**: The analysis focuses on published papers, potentially missing negative results or methods abandoned for lack of human validation

4. **Scope Constraints**: The analysis primarily covers academic literature; industry applications and proprietary xAI systems remain unknown

### Failure Cases and Open Questions

**When Does Explainability Help?**
- Even with human validation, under what conditions do explanations improve decision quality?
- Some studies show explanations can increase confidence without improving accuracy (sometimes decreasing it)

**Whose Understanding Matters?**
- Should validation involve only ML experts, or domain experts, or end users?
- Different stakeholder groups may require different types of explanations

**Scalability of Human Evaluation**
- With thousands of new xAI papers annually, how can the field ensure human validation becomes standard practice?
- What research infrastructure and incentives would encourage more human-centered evaluation?

### Future Research Directions

This work points to several promising directions:

1. **Standardized Human Evaluation Protocols**: Development of shared benchmarks and evaluation frameworks for xAI methods across domains

2. **Interactive and Adaptive Explanations**: Methods that adjust explanations based on user feedback and understanding

3. **Automated Human Evaluation**: Using crowdsourcing, behavioral metrics, or AI-assisted evaluation to scale human validation

4. **Cross-Disciplinary Collaboration**: Partnerships between ML researchers, HCI experts, cognitive scientists, and domain specialists to ensure explanations are grounded in how humans actually learn and make decisions

5. **Transparency About Limitations**: Papers should explicitly discuss which user groups were tested, under what conditions explanations are reliable, and what failure modes exist

---

## Code & Resources

### Official Resources

- **ArXiv Paper**: [2503.16507 - "Fewer Than 1% of Explainable AI Papers Validate Explainability with Humans"](https://arxiv.org/abs/2503.16507)
- **Conference Presentation**: CHI'25 (Late-Breaking Work)
- **Author Affiliation**: [MIT Lincoln Laboratory - Explainable AI Research](https://www.ll.mit.edu/r-d/projects/explainable-artificial-intelligence-decision-support)

### Related Datasets and Tools

While the paper itself is primarily an empirical meta-analysis rather than a software tool, it references important resources:

- **XAI Method Repositories**: LIME, SHAP, Captum (Meta/PyTorch) for common xAI implementations
- **Human Evaluation Frameworks**: 
  - [Human-Centered Evaluation of XAI (Frontiers Review)](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2024.1456486/full)
  - User study templates from HCI community
- **Domain-Specific Evaluation Toolkits**: Clinical decision support evaluation guides (FDA), financial services testing protocols

### Implementation Considerations

**For Researchers Applying This Insight:**

1. **Budget for Human Evaluation**: Allocate 20-40% of research time for designing and conducting human studies
2. **Interdisciplinary Team**: Include HCI researchers, domain experts, and cognitive scientists in validation
3. **Multiple Evaluation Metrics**: Go beyond accuracy; measure comprehension, trust, decision quality, actionability
4. **Report Negative Results**: Transparently discuss cases where explanations didn't help human understanding
5. **Domain-Specific Validation**: Tailor evaluation to actual user needs and contexts

---

## Related Work & Context

### Positioning Within the xAI Landscape

This paper builds on and critiques several branches of xAI research:

#### Feature Attribution Methods
- **LIME** (Ribeiro et al., 2016): Local model-agnostic explanations
- **SHAP** (Lundberg & Lee, 2017): Game-theoretic approach to feature importance
- **Integrated Gradients** (Sundararajan et al., 2017): Saliency-based explanations

**Critique**: These foundational methods were developed with technical rigor but often without human validation of whether they actually improve user understanding.

#### Interpretable Machine Learning
- **Decision Trees, Linear Models**: Inherently interpretable architectures
- **Rule-based Systems**: Explicit symbolic reasoning

**Insight**: Even inherently interpretable models don't guarantee that non-experts will understand predictions; design and communication matter as much as model choice.

#### Human-Centered AI & HCI Research
- **Amershi et al.** (2019): Guidelines for interactive machine learning systems
- **Amershi et al.** (2021): Human-AI interaction patterns
- **Antoun et al.** (2024): Survey on human-centered evaluation of XAI

**Connection**: This paper bridges the gap between technical xAI research and the HCI community's long-standing emphasis on user-centered evaluation.

#### Concept-Based Explanations
- **TCAV** (Testing with Concept Activation Vectors): User-friendly concept-based approaches
- **Prototype Networks**: Learning interpretable feature representations

**Related Problem**: Even concept-based methods lack systematic human validation across diverse user populations.

### Temporal Context: Why Now?

The validation gap is becoming increasingly urgent due to:

1. **Regulatory Pressure**: AI Act, GDPR, and FDA guidance demand explanations without specifying validation requirements
2. **Scale of Deployment**: AI systems now affect millions of users; explainability claims carry real consequences
3. **Maturation of the Field**: XAI moved from research curiosity to practical deployment, raising stakes for unvalidated methods
4. **Increased Scrutiny**: High-profile failures (COMPAS, medical AI errors) have heightened expectations for transparency

### Influencing Research Communities

This work will likely influence:

1. **XAI Conference Communities**: CHI, FAccT (Fairness, Accountability, and Transparency), and NeurIPS XAI workshops
2. **Regulatory Bodies**: Informing guidance on explainability requirements
3. **Industry Adoption**: Companies may realize their xAI implementations lack human validation
4. **Interdisciplinary Collaboration**: Encouraging xAI researchers to partner with HCI, cognitive science, and domain experts

### Open Challenges

The paper raises several unresolved questions for the broader community:

- **How to incentivize human validation?** Current publication norms favor novel methods over rigorous evaluation
- **Who should validate?** Different stakeholders require different expertise
- **When is validation sufficient?** What constitutes adequate human evaluation?
- **How to handle explainability-accuracy trade-offs?** Validated explanations may reduce model performance

---

## Summary of Key Takeaways

1. **Critical Finding**: Only 0.7% of xAI papers provide empirical validation that their methods improve human understanding of AI systems

2. **Field-Wide Problem**: This is not an isolated issue but a systemic gap affecting the vast majority of contemporary xAI research

3. **Methodological Implication**: The field has conflated technical interpretability with human explainability—two distinct concepts requiring different evaluation approaches

4. **Regulatory Risk**: As AI regulation increases, unvalidated xAI methods may fail to meet compliance requirements despite claims of explainability

5. **Research Direction**: The field must shift from purely technical approaches to human-centered validation as a core requirement for xAI research

6. **Practical Imperative**: Organizations deploying xAI methods should validate them with actual users before relying on explanations for critical decisions

---

## References & Further Reading

- **Original Paper**: [Suh, A., Hurley, I., Smith, N., & Siu, H.C. (2025). Fewer Than 1% of Explainable AI Papers Validate Explainability with Humans. CHI'25 Late-Breaking Work.](https://arxiv.org/abs/2503.16507)

- **MIT Lincoln Laboratory News**: [Study Finds That Explainable AI Often Isn't Tested on Humans](https://www.ll.mit.edu/news/study-finds-explainable-ai-often-isnt-tested-humans)

- **Related Survey**: [Human-Centered Evaluation of Explainable AI Applications: A Systematic Review](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2024.1456486/full)

- **Foundational xAI Papers**:
  - Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. KDD'16
  - Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. NeurIPS'17

- **Regulatory Context**:
  - EU AI Act (2024): [Official Text on High-Risk AI Systems](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689)
  - FDA Guidance on Clinical Decision Support Systems (2024)
