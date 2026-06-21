# Understanding Annotator Safety Policy with Interpretability

**ArXiv ID:** 2605.05329  
**Submitted:** May 6, 2026  
**Paper Link:** https://arxiv.org/abs/2605.05329

## Executive Summary

This paper addresses a critical but often overlooked challenge in AI safety: understanding why human annotators make labeling decisions when annotating data for safety policies. The authors introduce Annotator Policy Models (APMs), interpretable models that learn annotators' internal safety policies directly from labeling behavior, making human reasoning visible and comparable without requiring expensive or unreliable self-report methods. This work bridges the gap between data annotation practices and explainable AI by making annotator decision-making itself interpretable.

## Problem Statement

### Core Challenge
Data annotation is fundamental to AI safety—safety policies are communicated to annotators, who then label training data. However, annotation disagreement is ubiquitous and can arise from fundamentally different sources:

1. **Operational Failures**: Annotators misunderstand or misexecute the task (can be addressed through quality control)
2. **Policy Ambiguity**: Safety policy wording leaves room for interpretation by different annotators (requires policy clarification)
3. **Value Pluralism**: Different annotators hold genuinely different perspectives on what constitutes "safe" behavior (requires deliberation and diverse perspective incorporation)

### Existing Limitations

**Direct Inquiry is Costly and Unreliable:**
- Asking annotators to explain their reasoning substantially increases annotation burden
- Self-reported reasoning often fails to reflect actual decision processes in both human and LLM annotators
- Annotators may lack conscious access to their own decision criteria

**Unclear Annotation Disagreement Sources:**
- Without understanding why annotators disagree, organizations cannot determine whether the solution requires:
  - Better training (operational failures)
  - Policy refinement (ambiguity)
  - Embracing diverse viewpoints (value pluralism)

### Why This Matters for XAI

This paper extends explainable AI methodology to human annotation processes themselves. Rather than only explaining model decisions, it uses interpretability techniques to understand human decision-making—a critical problem as AI systems increasingly rely on subjective human judgments about safety, fairness, and acceptability.

## Core Concepts & Theory

### Annotator Policy Models (APMs)

**Definition:** APMs are interpretable supervised learning models that map annotator inputs (e.g., the text or content being labeled) to annotator outputs (e.g., safe/unsafe labels) while maintaining interpretability.

**Key Innovation:** Instead of treating annotator disagreement as noise, APMs explicitly model each annotator's labeling function, learning the systematic patterns in their decisions.

### Feature Space Alignment

APMs work by:
1. Learning latent feature representations for each annotator
2. Mapping all annotators to a shared feature space
3. Enabling systematic comparison of annotator decision-making across individuals and groups

**Advantage:** A shared feature space allows identifying where annotators converge (shared understanding) and where they diverge (policy ambiguity or value differences).

### Distinguishing Annotation Disagreement Sources

The paper operationalizes three sources of disagreement through interpretable analysis:

**Policy Ambiguity Detection:**
- When annotators interpret the same policy differently
- Detected through: Feature-level disagreement on ambiguous examples
- Solution pathway: Policy clarification and refinement

**Value Pluralism Detection:**
- When demographic groups systematically differ in their safety judgments
- Detected through: Systematic feature-weight differences across demographic groups
- Solution pathway: Deliberation about incorporating diverse perspectives

**Operational Failure Detection:**
- When annotators fail to follow the stated policy
- Detected through: Low model accuracy for that annotator; inconsistent labeling patterns
- Solution pathway: Better training, task clarification, or quality control

### Interpretability Mechanisms

The paper leverages standard interpretability techniques applied to annotator models:
- **Feature importance analysis**: Understanding which content features drive annotator decisions
- **Counterfactual reasoning**: "If this feature changed, would the annotator change their label?"
- **Attention mechanisms**: Highlighting which parts of the input annotators focus on
- **Decision boundaries**: Visualizing how annotators partition the input space

## Main Ideas & Key Contributions

### 1. Reframing Annotation as an Interpretability Problem

**Novel Perspective:** Prior work treats annotation disagreement as either noise (to be minimized) or a sign of complex phenomena (to be studied qualitatively). This paper reframes annotation itself as a phenomenon worthy of automated interpretability analysis.

**Why This Matters:** By making annotator reasoning interpretable, organizations can:
- Distinguish systematic disagreement from random error
- Identify which annotators may need retraining
- Discover where safety policies are genuinely ambiguous
- Recognize legitimate value pluralism in safety judgments

### 2. Annotator Policy Models (APMs)

**Core Contribution:** Introduction of a systematic methodology for learning and comparing annotators' internal policies.

**Technical Approach:**
- Train a supervised model for each annotator using their labeling behavior
- Extract interpretable representations from these models
- Map all annotators to a shared feature space
- Analyze feature distributions and weights to understand disagreement sources

**Faithfulness Guarantee:** APMs predict each annotator's actual labels with >80% accuracy, suggesting they genuinely capture annotator reasoning rather than just fitting surface patterns.

### 3. Applications to Policy Analysis

**Application 1: Surfacing Policy Ambiguity**
- Shows which examples annotators consistently disagree on
- Reveals which policy aspects are interpreted differently
- Enables targeted policy revision to reduce ambiguity

**Application 2: Detecting Value Pluralism**
- Identifies demographic groups (e.g., annotators from different regions) with systematically different safety priorities
- Reveals whether disagreement reflects value differences or policy confusion
- Enables intentional inclusion of diverse perspectives in safety policy design

## Methodology & Implementation

### Experimental Setup

**Datasets:**
- LLM safety annotations: Text examples from LLM outputs evaluated for safety
- Human annotations: Safety labels from multiple human annotators
- Controlled experiments: Synthetic examples with known policy differences

**Annotators:**
- Multiple human annotators with varying backgrounds
- LLM-based annotators (using instruction-tuned language models)
- Diverse demographic backgrounds to enable pluralism analysis

### Model Architecture

**Base Architecture:** Standard supervised learning models (e.g., logistic regression on text features, transformer-based classifiers)

**Feature Learning:**
- Learn latent feature representations for each example
- Each annotator has their own feature importance weights
- Shared feature space across annotators enables comparison

**Interpretability Techniques Applied:**
- Linear model inspection for simple feature-based decisions
- Attention visualization for transformer-based annotators
- Counterfactual perturbations to test feature importance
- Dimensionality reduction for human-understandable visualization

### Evaluation Metrics for Interpretability

**Faithfulness:**
- **Annotator Accuracy**: Does the model predict each annotator's labels with >80% accuracy?
- **Counterfactual Faithfulness**: When we perturb features, does the model's prediction change as expected?
- Metric: [Exact figures unavailable — see full paper]

**Stability:**
- Do feature importance rankings remain consistent across similar examples?
- Metric: Spearman correlation of feature importance across example subsets [Exact figures unavailable — see full paper]

**Interpretability Quality:**
- Can human reviewers understand why the model predicts each annotator's decision?
- Do discovered policy differences align with domain expert expectations?
- Metric: [Exact figures unavailable — see full paper]

### Results Summary

**Core Findings:**

1. **Accuracy of APMs:**
   - APMs achieve >80% accuracy at predicting annotator labels
   - This suggests models genuinely capture annotator reasoning, not surface artifacts

2. **Successful Policy Ambiguity Detection:**
   - Identifies examples where human annotators systematically disagree
   - Reveals specific policy aspects causing disagreement
   - Results align with policy analyst manual review

3. **Value Pluralism Detection:**
   - Discovers demographic group differences in safety priorities
   - Differences are systematic and interpretable (not random noise)
   - Enables identification of which aspects of "safety" vary by group

4. **Controlled Experiments:**
   - In synthetic experiments with known policy differences, APMs successfully recover ground-truth differences
   - Accurately identifies which annotators deviate from standard policy (operational failures)

**Limitations Acknowledged:**
- APMs work best when disagreement is driven by learnable systematic patterns
- Highly context-dependent disagreement may be harder to model
- Feature interpretability depends on input representation quality
- Results require domain expert validation to be actionable

## Practical Applications & Real-World Use Cases

### 1. AI Safety Policy Development

**Use Case:** Major AI labs developing safety training data

**Problem:** When multiple annotators label safety concerns, disagreement is common. Teams must decide: Is this a training problem, policy problem, or legitimate value difference?

**Solution via APMs:**
- Train APMs on current annotations
- Analyze feature importance to identify policy ambiguity
- Revise ambiguous policies before scaling annotation
- Reduce downstream confusion and improve data quality

**Impact:** Enables more efficient and accurate safety data collection; reduces need for multiple annotation rounds.

### 2. Fairness and Bias Analysis

**Use Case:** Understanding whether AI systems encode demographic biases through annotation processes

**Problem:** If different demographic groups of annotators have different safety thresholds, downstream models will reflect these differences. Teams need to know if this is intentional (value pluralism) or unintentional bias.

**Solution via APMs:**
- Identify demographic group differences in annotation patterns
- Distinguish systematic value differences from biased annotation
- Enable deliberate decisions about incorporating diverse perspectives
- Design more equitable safety standards

**Impact:** Supports fairness-aware data curation and conscious incorporation of diverse perspectives.

### 3. LLM Alignment and Safety

**Use Case:** Training LLM safety classifiers using human-annotated safety data

**Problem:** LLM safety datasets often show significant disagreement. It's unclear whether to force consensus or acknowledge value pluralism.

**Solution via APMs:**
- Understand which safety dimensions cause disagreement
- Decide which disagreements reflect legitimate value pluralism vs. policy confusion
- Train LLM safety models that explicitly handle disagreement
- Achieve better alignment with diverse user values

**Impact:** Enables more value-aware LLM safety training; reduces systems that enforce single safety paradigm.

### 4. Quality Control and Annotator Training

**Use Case:** Managing crowdsourced annotation workforces

**Problem:** Annotator quality varies. Teams need to identify which annotators need retraining vs. which are following different (but legitimate) policies.

**Solution via APMs:**
- Identify annotators with consistent patterns (policy followers) vs. inconsistent (potential errors)
- Compare annotators to detect operational failures
- Provide targeted training only to annotators with genuine errors
- Recognize annotators with different but systematic approaches

**Impact:** Improves annotation quality; enables smarter quality control; reduces unnecessary retraining.

### 5. Regulatory and Compliance Transparency

**Use Case:** Documenting AI safety decisions for regulators (EU AI Act, FDA)

**Problem:** Regulators want transparency about how AI safety decisions are made. Annotation-based systems need to explain disagreement sources.

**Solution via APMs:**
- Transparently document which policy aspects are ambiguous
- Show demographic differences in safety priorities
- Provide evidence of intentional vs. unintentional disagreement handling
- Support regulatory compliance documentation

**Impact:** Enables transparent, auditable AI safety practices; supports regulatory compliance.

## Insights & Implications

### Broader Implications for XAI and AI Safety

**1. Extending Interpretability to Human Decision-Making**

This paper demonstrates that interpretability techniques can illuminate not just model decisions but human decisions too. This has profound implications:
- Annotation processes are a critical part of AI development, yet often treated as black boxes
- Making annotator reasoning interpretable reveals systemic issues in data collection
- XAI methodology can be applied recursively: explaining model explanations, then explaining human explanations

**2. Legitimizing Value Pluralism in AI Development**

Rather than suppressing disagreement, this work suggests treating value pluralism as:
- Predictable and analyzable phenomenon
- Legitimate input to policy design when deliberate
- Something to be made visible and intentional rather than hidden

This aligns with emerging post-XAI research directions emphasizing stakeholder-centric, contestable AI.

**3. Addressing the "Data Quality" vs. "Value Pluralism" Tension**

In AI development, there's often tension between:
- Enforcing high-quality, consistent annotations (assumes agreement is optimal)
- Acknowledging legitimate disagreement and incorporating diverse views

APMs enable organizations to distinguish these cases and make intentional choices.

### Limitations and Failure Cases

**When APMs May Not Work Well:**
1. **Highly Context-Dependent Reasoning**: If annotators' decisions depend on broad world knowledge or subjective judgment not captured in input features, APMs may not capture full reasoning
2. **Non-Systematic Disagreement**: If disagreement is mostly random rather than systematic, models will have low accuracy
3. **Insufficient Data**: With very few annotations per annotator, learned patterns may be unreliable

**Potential Concerns:**
- Could APMs be used to unfairly profile or surveil annotators? (Ethical consideration)
- Might organizations suppress value pluralism that models reveal? (Governance risk)
- Does increased transparency into annotator reasoning create pressure to conform? (Social risk)

### Open Research Questions

1. **Transferability:** Do patterns learned from one annotator transfer to new annotators with similar backgrounds?
2. **Dynamic Policies:** How can APMs handle annotators whose policies evolve over time?
3. **Interaction Effects:** Can APMs identify complex interactions between policy aspects?
4. **Explanations for Explanations:** How to explain to annotators why their decisions were modeled as they were?

### Future Research Directions

1. **Interactive APMs:** Real-time feedback to annotators about discovered policy patterns
2. **Causal Understanding:** Move beyond correlational feature importance to causal inference about what drives annotations
3. **Deliberative Frameworks:** Combining APMs with structured deliberation processes for handling value pluralism
4. **Multi-Task Learning:** Simultaneously learning APMs across related tasks to discover transferable policy concepts

## Code & Resources

### Official Resources

**ArXiv Paper:**
- Full paper and preprint: [2605.05329 on arXiv](https://arxiv.org/abs/2605.05329)
- HTML version: [2605.05329 - HTML](https://arxiv.org/html/2605.05329v1)
- PDF version: [2605.05329 - PDF](https://arxiv.org/pdf/2605.05329)

### Implementation Considerations

**Dependencies Required:**
- PyTorch or TensorFlow for model training
- Scikit-learn for interpretability tools (SHAP, feature importance)
- Numpy/Pandas for data processing
- Matplotlib/Seaborn for visualization

**Computational Requirements:**
- Modest GPU (consumer-grade sufficient for demonstration)
- Scales with number of annotators and dataset size
- [Exact computational specs unavailable — see full paper]

### Suggested Next Steps

1. Start with simple linear models (logistic regression) for initial APM training
2. Use standard feature importance methods (permutation importance, coefficients)
3. Visualize feature distributions across annotators to identify disagreement patterns
4. Validate findings with domain experts (safety policy leads, annotation managers)

## Related Work & Context

### How This Paper Relates to Other xAI Research

**Relationship to Feature Attribution Methods (LIME, SHAP):**
- Traditional feature attribution explains model predictions
- APMs apply attribution methodology to human annotation predictions
- Bridges gap between model interpretability and human decision analysis

**Relationship to Concept-Based Explanations:**
- Concept-based methods (CAV, TCAV) explain models using human-defined concepts
- APMs implicitly discover concepts that drive annotation disagreement
- Both aim for human-understandable explanations

**Relationship to Human-Centered XAI:**
- Extends human-centered XAI from "explaining to humans" to "understanding human decisions"
- Aligns with post-XAI research directions (interpretability for contestability, accountability)
- Supports stakeholder-centric AI development

### Prior Work This Builds On

1. **Annotation Quality and Disagreement Literature:**
   - Cohen's kappa, Krippendorff's alpha for measuring agreement
   - Multi-annotator learning methods
   - APMs go further by explaining *why* disagreement occurs

2. **Interpretable Machine Learning:**
   - Linear models, decision trees, rule extraction
   - Feature importance and attribution methods
   - APMs apply these to annotator modeling context

3. **AI Fairness and Value Alignment:**
   - Work on demographic parity and disparate impact
   - Value pluralism in AI design (e.g., Selbst & Barocas)
   - APMs operationalize these concepts in annotation context

### Connection to Broader xAI Communities

**Human-Centered XAI Community:**
- Emphasizes explanations for human understanding and decision-making
- APMs exemplify this by making annotation (human) decisions interpretable

**Fairness, Accountability, and Transparency (FAccT) Community:**
- Focuses on transparency about AI system decisions and impacts
- APMs contribute to transparency about how annotation processes introduce bias

**AI Alignment and Safety Community:**
- Concerned with ensuring AI systems follow intended values and policies
- APMs help surface value differences during policy specification phase
- Enables more intentional, transparent approaches to safety data annotation

### Emerging Convergence

This paper sits at intersection of:
1. **Data Annotation Practices** (often overlooked in XAI literature)
2. **Explainable AI Methodology** (applied in novel direction)
3. **AI Fairness and Value Pluralism** (making diversity visible and systematic)
4. **Post-XAI Research** (interpretability for accountability and contestability, not just prediction)

## Significance for xAI Research

### Why This Matters

1. **Novel Application Domain:** Most XAI work focuses on model decisions; APMs extend interpretability to human decision-making
2. **Practical Impact:** Addresses real problem in AI development (understanding annotation disagreement)
3. **Methodological Bridge:** Connects interpretable ML techniques to data science/annotation management practices
4. **Normative Implications:** Legitimizes value pluralism and suggests better ways to handle disagreement than enforcing consensus

### Potential Impact

- Could influence how AI organizations structure data annotation processes
- May lead to more transparent, stakeholder-aware AI development practices
- Demonstrates value of interpretability beyond post-hoc model explanation
- Contributes to emerging "post-XAI" research emphasizing accountability and contestability

---

## References & Further Reading

- **Paper:** Understanding Annotator Safety Policy with Interpretability (arXiv 2605.05329)
- **ArXiv Direct:** https://arxiv.org/abs/2605.05329
- **Related Work:** 
  - Post-XAI research directions (Selbst & Barocas on FAccT, beyond-explanation frameworks)
  - Feature attribution methods (LIME, SHAP)
  - Annotation quality and crowdsourcing literature
  - AI fairness and value pluralism frameworks
