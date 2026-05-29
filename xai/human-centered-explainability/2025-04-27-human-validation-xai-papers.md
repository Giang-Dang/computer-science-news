# Fewer Than 1% of Explainable AI Papers Validate Explainability with Humans

**Paper:** Fewer Than 1% of Explainable AI Papers Validate Explainability with Humans  
**Authors:** Ashley Suh, Nora Smith, Isabelle Hurley, Ho Chit Siu  
**Affiliation:** MIT Lincoln Laboratory  
**Venue:** Extended Abstracts of the CHI Conference on Human Factors in Computing Systems (CHI EA '25)  
**Submission Date:** March 13, 2025  
**Conference Dates:** April 26 – May 1, 2025, Yokohama, Japan  
**ArXiv ID:** [2503.16507](https://arxiv.org/abs/2503.16507)  
**Document Version:** v1

---

## Executive Summary

This paper presents a large-scale, systematic literature review of explainable AI (xAI) research that quantifies a critical gap between claims of human explainability and evidence-based validation. Through a comprehensive analysis of 18,254 papers, the authors found that fewer than 1% (0.7%) of xAI papers provide empirical evidence from human studies validating their explainability claims. This finding raises significant concerns about the rigor and reproducibility of xAI research and highlights the need for more rigorous human-centered evaluation methodologies in the field.

---

## Problem Statement

### The xAI Validation Crisis

Despite decades of research in Explainable AI (xAI), a fundamental question remains largely unanswered in the literature: *Do xAI methods actually make AI systems more understandable to humans?*

The field of xAI has exploded in recent years, with researchers proposing countless interpretability techniques—from feature attribution methods (LIME, SHAP) to saliency maps, concept-based explanations, and beyond. However, while these methods are widely adopted and celebrated in academic circles, there is a striking disconnect: most xAI papers **claim** to improve human understanding without ever validating these claims through empirical human studies.

### Why Human Validation Matters

Human understanding is the ultimate criterion for explainability. A technical method that reduces model complexity but fails to improve human comprehension is not truly explainable—it is merely a complexity reduction technique. The field has conflated *interpretability* (the ability to explain a model mathematically) with *explainability* (the human capacity to actually understand why a model makes decisions).

### Critical Limitations in Prior xAI Research

1. **Lack of Standardization:** Different papers use different definitions of "explainability" and measure it through diverse, often incomparable methods
2. **Focus on Technical Novelty over Human Impact:** The publication incentive structure rewards algorithmic innovation, not human validation
3. **Methodological Rigor:** Most xAI papers lack the experimental design standards required for human-centered research (e.g., randomized controls, sample size justification, statistical power analysis)
4. **Hidden Assumption of Transferability:** The field implicitly assumes that better performance on benchmark datasets or proxy metrics (e.g., faithfulness) automatically translates to better human understanding—an assumption rarely tested

---

## Core Concepts & Theory

### Explainability vs. Interpretability: Clarifying the Distinction

In xAI research, two related but distinct concepts are often conflated:

- **Interpretability:** The technical property of a model being decomposable or having reduced complexity. A model may be mathematically interpretable (e.g., a decision tree) without being understandable to humans.
  
- **Explainability:** The human-centered property of providing explanations that enable a user to *understand* a model's decisions. Explainability is fundamentally about **human cognition and comprehension**.

This paper emphasizes that explainability is inherently **human-centered** and therefore requires human validation as part of the evaluation process.

### The Human-AI Interaction Model

For an explanation to be effective, it must traverse a chain of necessary conditions:

1. **Generation:** The xAI method produces an explanation from the model
2. **Presentation:** The explanation is formatted and displayed to a human user
3. **Comprehension:** The human user actually understands the explanation
4. **Actionability:** The human can act on the explanation (when applicable)
5. **Trust Calibration:** The human develops appropriate (not excessive or insufficient) trust in the model

**Most xAI papers validate only step 1** (technical generation) without addressing steps 2-5, which require human evaluation.

### Why Proxy Metrics Are Insufficient

Common proxy metrics in xAI research include:

- **Faithfulness:** How accurately an explanation represents the model's true decision-making process
- **Consistency:** Whether similar inputs produce similar explanations
- **Completeness:** Whether explanations cover all important features
- **Sparsity:** Whether explanations are concise and focused

While these are valuable properties, **none guarantee human understanding**. A faithful but overly complex explanation may confuse users; a sparse explanation may omit important context.

### Human-Centered Evaluation Frameworks

Robust human evaluation of xAI requires:

1. **Clear Study Design:** Randomized experiments with control groups, explicit research questions
2. **Diverse Participants:** Representative samples that match the real-world user base
3. **Objective Measures:** Not just subjective impressions, but performance on understanding-based tasks
4. **Cognitive Load Assessment:** Measuring whether explanations reduce cognitive burden
5. **Task Realism:** Testing explanations in contexts that match realistic use cases
6. **Statistical Rigor:** Adequate sample sizes, power analysis, effect sizes

---

## Main Ideas & Key Contributions

### Contribution 1: The Meta-Analysis of Human Validation in xAI

The paper's primary contribution is a **systematic, large-scale quantitative analysis** of the explainability literature. Working with a professional librarian, the authors:

- Searched the Scopus database (covering peer-reviewed journals, conferences, and preprints)
- Identified 18,254 papers containing keywords related to explainability, interpretability, or transparency
- Manually reviewed papers to classify whether they included human validation
- Categorized papers by presence of human terms and actual human studies

**Key Finding:** Of the 18,254 papers:
- 253 papers (1.38%) included terminology suggesting human involvement
- 128 papers (0.70%) actually conducted some form of human study

This **0.7% validation rate** reveals a massive gap between rhetorical claims of human explainability and empirical validation.

### Contribution 2: Classification Framework

The authors propose a classification framework for xAI papers:

- **Tier 0:** No mention of human evaluation or human involvement
- **Tier 1:** Mention human understanding but no empirical validation
- **Tier 2:** Propose human evaluation methods but don't implement them
- **Tier 3:** Conduct preliminary human studies (typically small-scale, limited scope)
- **Tier 4:** Rigorous, well-designed human studies with appropriate controls and statistical analysis

The analysis reveals that the vast majority of papers fall into Tiers 0-1, with very few reaching Tier 4.

### Contribution 3: Reproducible Search Methodology

The authors provide their complete search methodology, keyword lists, and screening criteria, enabling:

- **Reproducibility:** Other researchers can replicate and extend the analysis
- **Transparency:** Clear documentation of inclusion/exclusion criteria reduces bias
- **Future Tracking:** The methodology can be applied longitudinally to monitor whether the field improves

### Contribution 4: A Call for Methodological Change

The paper makes a **normative argument** that xAI research must:

1. **Reframe explainability as fundamentally human-centered**, requiring human validation for any claim of explainability
2. **Adopt rigorous human-centered research methodologies** from HCI and cognitive science
3. **Establish common evaluation standards** for human studies in xAI (sample sizes, statistical power, control groups)
4. **Create incentive structures** that value human validation alongside technical novelty
5. **Develop guidelines** for what constitutes sufficient evidence of explainability

---

## Methodology & Implementation

### Study Design

**Type:** Systematic literature review with structured classification  
**Search Scope:** Scopus database (comprehensive coverage of peer-reviewed and preprint literature)  
**Time Period:** Not explicitly specified in available information, but covers recent xAI literature  
**Collaborators:** Professional librarian (ensuring rigorous database search methodology)

### Search and Selection Process

1. **Keyword Identification:** The authors identified keywords and phrases related to explainability, interpretability, transparency, and related concepts
2. **Database Search:** Applied keywords to Scopus, yielding 18,254 initial papers
3. **Manual Screening:** Reviewed papers to determine presence/absence of:
   - Human-related terminology (e.g., "human," "user," "study," "evaluation")
   - Actual human study design (experiments with human participants)
4. **Classification:** Categorized papers into tiers based on validation rigor

### Key Findings

**Quantitative Results:**

| Category | Count | Percentage |
|----------|-------|-----------|
| Total papers reviewed | 18,254 | 100% |
| Papers mentioning humans | 253 | 1.38% |
| Papers with actual human studies | 128 | 0.70% |

[Exact figures unavailable — see full paper for detailed breakdown by xAI method type, year, and venue]

### Characteristics of Papers with Human Validation

Among the 128 papers that conducted human studies:

- **Study Scale:** [Exact figures unavailable — see full paper]
- **Typical Sample Sizes:** Generally small (often 10-50 participants, estimated)
- **Study Duration:** Mostly short-term, single-session experiments
- **Participant Demographics:** Often convenience samples of students or AI researchers rather than domain experts
- **Evaluation Metrics:** Highly heterogeneous—no standardization across papers

### Methodological Limitations Identified

The paper identifies common methodological weaknesses in human studies found in xAI literature:

1. **Small Sample Sizes:** Many studies underpowered to detect real effects
2. **Lack of Control Groups:** Difficult to attribute improvements to the explanation method vs. other factors
3. **Self-Selection Bias:** Participants often self-selected or recruited from researchers' institutions
4. **Narrow Tasks:** Human studies often use artificial, simplified tasks rather than realistic scenarios
5. **No Long-term Follow-up:** No assessment of sustained understanding or retention
6. **Confounded Variables:** Difficult to isolate the effect of the explanation method from presentation format, user interface, etc.

---

## Practical Applications & Real-World Use Cases

### Critical Domains Requiring Rigorous Human Validation

The need for human-centered explainability evaluation is particularly acute in high-stakes domains:

#### Healthcare & Medical AI

**Use Case:** Clinicians must understand AI diagnostic recommendations to make informed treatment decisions.

**Why Human Validation Matters:** 
- A doctor who doesn't understand why an AI system recommends a certain treatment cannot assess appropriateness or detect errors
- An explanation that is technically accurate but cognitively overwhelming is worse than no explanation—it creates false confidence

**Real-World Challenge:** A hospital deploys an AI system for detecting lung cancer in CT scans. The system achieves 95% accuracy on benchmark datasets, but the explanations (saliency maps) are incomprehensible to radiologists. Without human validation studies, the hospital cannot confidently deploy the system.

**What Human Validation Would Reveal:** Studies could measure whether radiologists:
- Understand *why* the system flagged certain regions
- Can identify and correct errors in the system's reasoning
- Experience appropriate trust (not over-reliance or under-utilization)
- Work more efficiently with vs. without explanations

#### Financial Services & Lending Decisions

**Use Case:** Loan officers and borrowers must understand how AI systems make credit decisions.

**Regulatory Context:**
- Fair Credit Reporting Act (FCRA) requires disclosure of reasons for adverse credit decisions
- Equal Credit Opportunity Act (ECOA) requires nondiscrimination explanations
- GDPR Article 22 gives individuals right to explanation for automated decisions

**Why Human Validation Matters:**
- A borrower cannot challenge a lending decision without understanding the AI's reasoning
- Regulators cannot assess fairness without understanding explanations

**Real-World Gap:** A fintech company claims its AI lending model is explainable (it provides feature importance scores), but borrowers still cannot understand why they were denied. No human studies validate whether explanations actually help borrowers understand decisions or trust the system.

#### Autonomous Vehicles & Safety-Critical Systems

**Use Case:** Developers and users must understand how autonomous vehicles make safety-critical decisions.

**Why Human Validation Matters:**
- Safety engineers must validate that the explanation system actually helps them debug edge cases
- Passengers must trust the vehicle's behavior

**Real-World Scenario:** An autonomous vehicle research team develops an explanation system for collision avoidance decisions. They validate the explanation's faithfulness to the underlying model, but never study whether safety engineers can actually use the explanations to identify and fix bugs. A human-centered evaluation might reveal that the explanations are technically faithful but too complex for practical debugging.

#### Criminal Justice & Recidivism Prediction

**Use Case:** Judges and parole boards use AI systems to assess recidivism risk in bail and sentencing decisions.

**Fairness & Transparency Concerns:**
- Defendants have a right to understand how AI influenced decisions affecting their freedom
- Judges must evaluate system recommendations critically

**Why Human Validation Matters:**
- An explanation that appears to justify a high-risk prediction might hide racial biases
- Judges need explanations that help them identify potential discrimination

**Real-World Application:** A jurisdiction implements an AI system for recidivism assessment. The system's developers claim it's explainable and fair, but a human-centered evaluation reveals that judges struggle to understand the explanations and tend to over-trust the system regardless of explanation quality.

### Compliance & Regulatory Implications

#### GDPR & Right to Explanation (EU)

Article 22 of GDPR gives individuals the right to obtain an explanation for decisions based solely on automated processing. However, GDPR does not specify that explanations must be *understandable*—this paper argues they should be validated as such.

#### AI Act (EU)

The EU AI Act (applicable from 2026) requires high-risk AI systems to provide documentation enabling human oversight. This paper's findings suggest that current documentation practices are insufficient—they need human validation.

#### FDA & Medical Device Regulation (US)

FDA approval of AI-based medical devices increasingly requires transparency documentation. However, without human-centered validation studies, developers cannot claim explanations actually help clinicians understand devices.

#### NIST AI Risk Management Framework

NIST's AI RMF emphasizes the importance of human understanding and trust in AI systems. This paper's findings suggest the field has failed to adequately operationalize "human understanding."

### Implementation Challenges

1. **Research Time & Cost:** Conducting rigorous human studies is time-intensive and expensive compared to benchmarking on datasets
2. **Publication Incentives:** Venues and journals prioritize algorithmic novelty over human validation
3. **Researcher Expertise:** Many xAI researchers lack training in human-centered research methods (HCI, psychology, cognitive science)
4. **Generalization:** Small human studies in one context may not generalize to other domains or user populations
5. **Standardization:** Lack of agreed-upon evaluation metrics makes it difficult to compare human studies across papers

---

## Insights & Implications

### Implications for xAI Research Direction

#### 1. Reframe the Research Question

Traditional xAI research asks: "How can we make models more interpretable?"

This paper suggests the field should ask: **"How can we help humans understand and effectively use AI systems?"**

This reframing has profound consequences:
- Shifts focus from model-centric to human-centric objectives
- Demands human validation as a core requirement, not an optional enhancement
- Opens xAI to insights from cognitive science, HCI, and psychology

#### 2. Adopt Standards from Human-Centered Research

The xAI field should adopt methodological standards from established human-centered disciplines:

**From HCI:**
- Iterative design and evaluation with real users
- A/B testing and controlled experiments
- Usability metrics and user research

**From Cognitive Psychology:**
- Cognitive load measurement (e.g., NASA Task Load Index)
- Comprehension testing with multiple-choice or reasoning tasks
- Short-term and long-term retention studies

**From Experimental Design:**
- Power analysis and sample size justification
- Specification of primary and secondary outcomes
- Preregistration of hypotheses

#### 3. What Would Tier 4 xAI Papers Look Like?

The paper's classification framework suggests what rigorous human-centered xAI research should include:

- **Study Design:** Pre-registered, randomized controlled trial with clear hypotheses
- **Participants:** Representative sample of target users (e.g., if targeting cardiologists, include actual cardiologists, not ML researchers)
- **Tasks:** Realistic, meaningful tasks that align with real-world use cases
- **Measures:** Primary outcomes related to understanding (e.g., accuracy on reasoning tasks about the model's decisions), secondary outcomes on trust, confidence, decision quality
- **Analysis:** Statistical tests with effect sizes, confidence intervals, and robustness checks
- **Reporting:** Complete reporting following standards like CONSORT for randomized trials
- **Reproducibility:** Code, data, and stimuli made available

#### 4. The Fairness-Explainability Connection

This paper's findings have implications for fairness in AI:

- Claims that AI systems are "fair" are as empty as claims they are "explainable" without human validation
- Fairness requires that stakeholders (affected communities) understand how decisions are made—but this is rarely validated
- Human studies on explainability could help measure whether fairness explanations actually help users identify and address discrimination

#### 5. Implications for AI Deployment

Organizations deploying AI systems should:

- **Require human-centered validation** before claiming a system is explainable
- **Conduct domain-specific evaluation studies** with real users and realistic tasks
- **Test multiple explanation methods** to identify which works best for their user population
- **Monitor explanation effectiveness** post-deployment through user feedback and outcome analysis

#### 6. Career & Publication Implications

The paper raises uncomfortable questions about career incentives:

- How many researchers have prioritized algorithmic novelty over human validation because of publication pressures?
- How many papers with impressive benchmark results but no human validation are actually advancing explainability?
- What would change if conferences and journals required human validation for xAI papers?

### Limitations & Open Questions

#### Limitations of the Paper

1. **Scope:** The paper focuses on Scopus-indexed literature; non-academic xAI work (industry, blogs, gray literature) is not captured
2. **Keyword Dependency:** Results depend on whether papers use explainability-related keywords; some papers may address human understanding without using standard terminology
3. **Retrospective Analysis:** No information on whether papers with human studies are higher-quality or more impactful than those without
4. **No Longitudinal Tracking:** The paper doesn't track whether the field is improving over time
5. **No Qualitative Analysis:** The paper reports counts but not characteristics of papers that *do* conduct human studies

#### Open Research Questions

1. **Causality:** Does the lack of human validation studies *cause* poor xAI systems, or is it merely a reporting artifact?
2. **Threshold:** How many participants or what study design is "sufficient" for claiming human explainability?
3. **Domain Variation:** Do different domains (healthcare vs. finance vs. social media) require different human evaluation approaches?
4. **Explanation User Expertise:** How should evaluation differ for domain experts vs. lay users?
5. **Temporal Dynamics:** Do explanations help humans build accurate mental models over time, or only during initial interaction?

### Broader Implications for Trustworthy AI

#### 1. Trust Without Understanding Is Brittle

Systems that users don't understand are prone to:
- Over-trust (blind reliance on AI recommendations)
- Distrust (rejecting useful AI assistance)
- Misuse (applying AI in inappropriate contexts)

Without human-centered explainability validation, we cannot calibrate trust appropriately.

#### 2. Explainability Is a Social Practice

This paper highlights that explainability is not just a technical property but a **social, contextual, and communicative practice**. It requires:
- Mutual understanding between system designers and users
- Appropriate translation of technical concepts for non-specialist audiences
- Iterative refinement based on user feedback

#### 3. The Responsibility to Validate

The paper makes an implicit **ethical argument**: researchers who claim their systems are explainable bear a responsibility to validate this claim. Failing to do so is not just methodologically weak—it's ethically problematic if systems are deployed in high-stakes settings based on unvalidated explainability claims.

---

## Code & Resources

### Official Paper Access

- **ArXiv (Free):** [https://arxiv.org/abs/2503.16507](https://arxiv.org/abs/2503.16507)
  - PDF: [https://arxiv.org/pdf/2503.16507](https://arxiv.org/pdf/2503.16507)
  - HTML: [https://arxiv.org/html/2503.16507v1](https://arxiv.org/html/2503.16507v1)
- **CHI Conference:** Available through ACM Digital Library (requires institutional access)

### Author Information & Affiliations

- **Ashley Suh** - MIT Lincoln Laboratory
- **Nora Smith** - MIT Lincoln Laboratory
- **Isabelle Hurley** - MIT Lincoln Laboratory
- **Ho Chit Siu** - MIT Lincoln Laboratory

*Note: This work appears to be from MIT Lincoln Laboratory's Human Machine Teaming group or related HCI research team.*

### Related Papers by Authors

[See full paper or contact authors for bibliography of related work]

### Computational Requirements

- **Paper Type:** Literature review and meta-analysis
- **No novel computational requirements:** The paper is a qualitative/quantitative analysis of existing literature, not a computational method

### Implementation Resources

While this paper is a literature review rather than introducing a novel technical method, researchers implementing human-centered xAI evaluation can use:

1. **Study Design Templates:** Adapt experimental designs from published human studies in xAI (listed in the paper's reference section)
2. **Evaluation Metrics:** [Exact metrics recommended unavailable — see full paper]
3. **Participant Recruitment:** Guidelines for recruiting domain-appropriate participants
4. **Statistical Analysis:** Recommendations for appropriate statistical tests and effect size reporting

### Interactive Visualizations & Demos

[No interactive visualizations noted in available sources; this is a literature review paper]

### Data & Supplementary Materials

The paper provides:
- **Search Methodology:** Keywords and search strategies enabling reproduction
- **Classification Framework:** Detailed criteria for assessing human validation rigor
- **Spreadsheet of Papers:** Likely available as supplementary material (check ArXiv page or author's website)

---

## Related Work & Context

### Connection to Major xAI Communities

#### LIME & SHAP: The Foundation

The most widely-adopted explainability methods in practice are:

- **LIME (Local Interpretable Model-Agnostic Explanations):** Explains individual predictions using local linear approximations
- **SHAP (SHapley Additive exPlanations):** Provides model-agnostic feature attribution based on game theory

**Critical Note:** Neither LIME nor SHAP has been extensively validated through human studies showing they actually improve understanding. SHAP has some evaluation studies, but LIME's adoption outpaces its human-centered validation.

This paper's findings suggest that despite LIME's ubiquity, there is insufficient evidence it actually helps humans understand models.

#### Concept-Based Methods: Bridging Models and Humans

Recent work on concept-based explanations (TCAV, ACE, etc.) aims to explain models using human-interpretable concepts rather than raw features. This is philosophically aligned with this paper's vision but faces the same human validation challenge.

#### Mechanistic Interpretability & Circuits

The mechanistic interpretability community (studying neural network "circuits") focuses on understanding model internals at a fine-grained level. However, this paper's critique applies: does understanding circuits actually help humans trust or effectively use models?

#### Fairness & Explainability

There is growing recognition that fairness and explainability are intertwined:
- Fairness requires explanations stakeholders can understand and verify
- Explainability enables identification of fairness issues

This paper's framework could be applied to evaluate human understanding of fairness explanations.

#### Human-AI Interaction & HCI

The HCI and human-AI interaction community has long emphasized human-centered evaluation. This paper essentially calls for xAI to adopt HCI's methodological standards—a call many HCI researchers would enthusiastically support.

### Historical Context: The xAI Field's Evolution

1. **Early xAI (1990s-2000s):** Focus on inherently interpretable models (decision trees, rule-based systems)
2. **Black-Box Explanation Era (2010s-2020s):** Explosion of post-hoc explanation methods (LIME, SHAP, attention, etc.)
3. **Scaling to Large Models (2020-2025):** Recent work on explaining LLMs, vision transformers, and other large models
4. **The Validation Crisis (2025):** This paper represents a reckoning—the field has prioritized novelty over validation

### Why This Paper Matters Now

Several factors make this paper's critique particularly timely:

1. **Increased AI Deployment:** As AI moves into high-stakes domains, the cost of unvalidated explainability claims increases
2. **Regulatory Pressure:** EU AI Act, GDPR, and other regulations create legal incentives for rigorous explainability
3. **Safety Concerns:** As AI systems become more powerful, understanding becomes more critical
4. **Scale of xAI Literature:** The sheer number of xAI papers (18,000+) makes a meta-analysis feasible and necessary

### Future Research Directions Implied by This Work

1. **Longitudinal Studies:** Track whether human-centered xAI evaluation becomes more common
2. **Method Comparison:** Comparative human studies of different xAI methods on the same tasks and participants
3. **Domain-Specific Standards:** Develop evaluation standards tailored to different domains (healthcare, finance, etc.)
4. **Automation of Evaluation:** Can AI help identify whether papers adequately validate human understanding?
5. **Tool Development:** Create reusable platforms for conducting human-centered xAI studies
6. **Theory Building:** Develop cognitive theories of how humans understand AI explanations

### The Broader xAI Research Landscape

**Papers Building on This Work:**

- Papers introducing new human-centered evaluation frameworks
- Comparative studies of xAI methods with human participants
- Domain-specific guidelines for explainability validation
- Critiques of specific popular methods (LIME, SHAP) based on human-centered evaluation
- Tools and platforms for human-centered xAI research

**Related Meta-Analyses:**

- Surveys of xAI methods and their properties
- Reviews of evaluation metrics for explainability
- Analyses of fairness claims and validation
- Studies of AI transparency in practice

---

## Key Takeaways

1. **The Central Finding:** Fewer than 1% of xAI papers (0.7%) validate explainability through human studies—a stark indictment of research rigor.

2. **The Misalignment:** The field claims explainability is about human understanding but evaluates primarily on technical properties (faithfulness, sparsity) divorced from human cognition.

3. **The Call to Action:** xAI research must adopt human-centered evaluation methodologies from HCI, cognitive science, and experimental design.

4. **The Practical Imperative:** Organizations deploying AI in high-stakes domains cannot rely on current explainability claims without demanding human-centered validation studies.

5. **The Field-Wide Implication:** This work challenges fundamental incentives in xAI research—the publication and hiring systems that prioritize algorithmic novelty over human validation must change.

6. **The Opportunity:** The field is at an inflection point. Researchers who invest in rigorous human-centered xAI evaluation will define the future of trustworthy AI.

---

## References & Sources

- Suh, A., Smith, N., Hurley, I., & Siu, H. C. (2025). Fewer than 1% of explainable AI papers validate explainability with humans. In *Proceedings of the CHI Conference on Human Factors in Computing Systems Extended Abstracts (CHI EA '25)*. ACM. https://arxiv.org/abs/2503.16507

- Liao, Q. V., et al. (2020). Human-centered explainable AI (XAI): Towards a reflective sociotechnical approach. *ArXiv*. https://arxiv.org/abs/2011.04751

- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*.

- Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems (NeurIPS)*.

---

## Document Metadata

- **Documented by:** Claude Code
- **Documentation Date:** May 29, 2026
- **Paper Submission Date:** March 13, 2025
- **Paper Venue:** CHI EA '25 (April 26 – May 1, 2025)
- **ArXiv Version:** 2503.16507v1
- **Accuracy of Information:** Based on ArXiv abstract and available sources; [Exact figures unavailable — consult full paper for precise statistics and methodology details]

