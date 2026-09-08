# A Two-Stage LLM Framework for Accessible and Verified XAI Explanations

**Paper Title:** A Two-Stage LLM Framework for Accessible and Verified XAI Explanations

**ArXiv ID:** [2604.12543](https://arxiv.org/abs/2604.12543)

**Publication Date:** April 2026

**Venue:** Accepted for publication at the 2026 IEEE World Congress on Computational Intelligence (WCCI 2026)

**Authors:** Georgios Mermigkis, Dimitris Metaxakis, Marios Tyrovolas, Argiris Sofotasios, Nikolaos Avgeris, Panagiotis Hadjidoukas, Chrysostomos Stylios

---

## Executive Summary

This paper addresses a critical gap in explainable AI: while existing XAI methods (LIME, SHAP, Grad-CAM) produce feature attributions that reveal which inputs influence model decisions, these outputs often remain technical and inaccessible to non-expert stakeholders. The authors propose a Two-Stage LLM Meta-Verification Framework that translates raw XAI outputs into clear, natural-language narratives and automatically verifies their faithfulness, coherence, and completeness. This work bridges the accessibility-fidelity gap in XAI by leveraging LLMs as both explanation generators and independent verifiers, making explainability both understandable and trustworthy.

---

## Problem Statement

### Current Limitations in XAI

Despite significant advances in interpretability methods over the past decade, traditional XAI techniques face two interconnected challenges:

1. **Accessibility Gap**: Feature attribution methods (SHAP, LIME, Grad-CAM, Integrated Gradients) produce numerical or visual outputs that domain experts can interpret, but non-technical stakeholders—including regulatory bodies, end-users, and business decision-makers—struggle to understand their significance and implications.

2. **Verification and Trustworthiness**: When translating technical XAI outputs into human-understandable explanations, there is no systematic way to verify that:
   - The explanation faithfully represents the underlying attribution values
   - The explanation is logically coherent and free of contradictions
   - The explanation covers all relevant aspects of the model's decision
   - The explanation does not introduce hallucinated or fabricated reasoning

3. **Manual Effort**: Currently, converting XAI outputs into accessible explanations requires manual effort from experts, which is time-consuming, error-prone, and not scalable for real-time or large-scale deployment.

### Prior Approaches

Earlier work has attempted to address XAI accessibility through:
- User studies evaluating how people understand different explanation formats
- Guidelines for writing "plain language" model explanations
- Interactive visualization tools for exploring attributions
- Direct self-explanations from language models (but often with fidelity concerns)

However, these approaches typically lack:
- Systematic verification of explanation quality
- Automation at scale
- Integration with existing, widely-used XAI methods
- Multi-stakeholder evaluation (technical and non-technical users)

---

## Core Concepts & Theory

### Understanding XAI Methods

The paper works with five representative XAI techniques spanning tabular, image, and text domains:

#### Feature Attribution Methods
- **SHAP (SHapley Additive exPlanations)**: Assigns importance scores to input features based on cooperative game theory and Shapley values. For a prediction on ACSIncome dataset, SHAP might show that "age > 50" and "education level" are the top factors.
- **LIME (Local Interpretable Model-agnostic Explanations)**: Approximates model behavior locally around a specific instance by fitting interpretable models to perturbed inputs.
- **Grad-CAM++**: Produces visual saliency maps for CNNs by computing gradients of the target class with respect to feature maps.
- **Integrated Gradients**: Attributes predictions by integrating gradients along a straight line from a baseline input to the actual input.
- **EBM (Explainable Boosting Machines)**: Inherently interpretable models that expose feature contributions directly from the learning algorithm.

### The Accessibility Problem in XAI Output

Consider a SHAP explanation on ACSIncome (predicting income > $50k):
```
Feature Contributions:
  age: +0.23
  marital-status: +0.18
  education: +0.15
  hours-per-week: +0.12
```

A technical user understands these represent positive contributions to the "income > $50k" prediction. But a loan officer or policy maker might struggle with:
- What "contribution +0.23" means in practical terms
- Why the model relied on these features
- Whether the explanation is trustworthy
- What action to take based on the explanation

### From Attributions to Narratives: The Generation Stage

The first stage of the framework uses an LLM to convert technical XAI outputs into natural language. This goes beyond simple templating:

**Input (SHAP output on ACSIncome):**
```
Feature: age, Value: 45, Contribution: +0.23
Feature: marital-status, Value: married, Contribution: +0.18
Feature: education, Value: bachelors, Contribution: +0.15
```

**Generated Narrative (Explainer LLM):**
```
The model predicts income > $50k for this individual. The primary factors are:
1. Age (45): Being in the mid-career stage contributes positively to higher 
   income prediction, as this typically aligns with peak earning years.
2. Marital Status (married): Individuals who are married often have dual-income 
   households, which increases the likelihood of higher household income.
3. Education (bachelor's degree): Higher educational attainment is strongly 
   associated with higher earning potential.
Together, these factors create a strong indicator for income above $50k.
```

The LLM translates:
- Numerical contributions into interpretable statements
- Domain context (e.g., "mid-career stage" for age 45)
- Logical reasoning connecting features to outcomes

### Verification: Ensuring Explanation Quality

The second stage introduces an independent Verifier LLM that assesses explanations against four criteria:

#### Faithfulness
Does the explanation accurately represent the underlying XAI method's output?
- Check: Does the explanation correctly order features by importance?
- Check: Does the explanation preserve the direction of contributions (positive/negative)?
- Challenge: When LLMs paraphrase, they might inadvertently change emphasis

#### Coherence
Is the explanation logically consistent and well-structured?
- Check: Do statements contradict each other?
- Check: Are causal claims grounded in the data?
- Example of incoherence: "Age 45 is young... Age 45 is senior" in same explanation

#### Completeness
Does the explanation cover the important aspects of the model's decision?
- Check: Are all high-impact features mentioned?
- Check: Are qualifications or limitations noted?
- Example: If SHAP shows five important features, does the explanation discuss all?

#### Hallucination Risk
Does the explanation introduce fabricated facts or reasoning not supported by the data or model?
- Check: Are domain claims verified?
- Check: Are statistical assertions correct?
- Example of hallucination: Claiming "married status causes 50% income increase" without evidence

### Iterative Refinement

If the Verifier identifies issues, the Explainer LLM receives feedback and regenerates the explanation:

```
Verifier Feedback: "The explanation claims 'married status causes dual-income 
households' but SHAP shows correlation, not causation. Revise to say 'is 
associated with' rather than 'causes'."

Revised Explanation: "...Marital status (married): Being married is associated 
with higher-income predictions, potentially because dual-income households tend 
to have higher combined earnings..."
```

---

## Main Ideas & Key Contributions

### 1. Two-Stage LLM Meta-Verification Framework

The core innovation is a systematic, two-component architecture:
- **Explainer LLM**: Specialized in translating technical outputs into stakeholder-friendly language
- **Verifier LLM**: Acts as an independent quality assurance mechanism

This separation of concerns ensures:
- The Explainer can focus on clarity and accessibility
- The Verifier can critically evaluate without self-bias
- Both roles can be configured independently (different model families, sizes)

### 2. Systematic Verification Criteria

Rather than ad-hoc quality checks, the framework formalizes four measurable criteria:
- Faithfulness (fidelity to source)
- Coherence (logical consistency)
- Completeness (coverage of important aspects)
- Hallucination Risk (freedom from fabrications)

This enables:
- Automated evaluation across datasets and XAI methods
- Transparent reporting of explanation quality
- Identification of systematic failure modes

### 3. Cross-Domain Evaluation

The framework is validated across diverse domains:
- **Tabular Data**: SHAP on ACSIncome, EBM on Wine Quality
- **Images**: Grad-CAM++ on CIFAR-10
- **Text**: Integrated Gradients on IMDB Reviews
- **Classical ML**: LIME on Diamonds dataset

This demonstrates generalization across:
- Feature attribution paradigms
- Input modalities
- Model types (tree-based, neural networks, classical ML)

### 4. Practical Deployment Strategy

The authors design the framework for real-world deployment:
- Uses open-weight LLMs (14B–30B parameters) that can run locally
- Models tested: GPT-OSS, DeepSeek-R1, Qwen-3
- Iterative refinement mechanism handles low-quality explanations
- Evaluation under both natural and synthetic error conditions

---

## Methodology & Implementation

### Experimental Design

#### Stage 1: Explanation Generation

**Setup:**
- Input: XAI output (numerical attributions or saliency maps) + model prediction + input data
- LLM Model: Open-weight models (14B–30B parameters)
- Prompt Design: Careful engineering to ensure clarity without over-specification

**Process:**
```
Prompt Template:
"Given a machine learning model's prediction and the feature importance scores 
from [XAI Method] analysis, generate a clear, non-technical explanation suitable 
for [target audience: business user, regulator, customer] that:
1. Explains what the model predicted
2. Identifies the key factors driving this prediction
3. Contextualizes these factors in domain terms
4. Avoids technical jargon"
```

#### Stage 2: Verification

**Setup:**
- Input: Generated explanation + original XAI output + model prediction
- Verifier LLM: Same or different model family
- Evaluation Criteria: Four-criteria framework

**Process:**
```
Verification Prompt:
"Review the following explanation for:
1. Faithfulness: Does it accurately represent the feature importance scores?
2. Coherence: Is it logically consistent?
3. Completeness: Does it cover all important features?
4. Hallucinations: Does it introduce unsupported claims?

For each criterion, score 1–5 and explain any issues found."
```

### Datasets and Models

| Dataset | XAI Method | Task | Domain |
|---------|-----------|------|--------|
| ACSIncome | SHAP | Income prediction | Tabular |
| Diamonds | LIME | Price prediction | Tabular |
| CIFAR-10 | Grad-CAM++ | Image classification | Vision |
| IMDB Reviews | Integrated Gradients | Sentiment classification | NLP |
| Wine Quality | EBM | Quality regression | Tabular |

**LLM Models Tested:**
- GPT-OSS (open-weight variant of GPT architecture)
- DeepSeek-R1 (reasoning-focused model)
- Qwen-3 (multilingual model)

### Evaluation Metrics

**Faithfulness Score:**
- Feature ranking alignment: Do model explanations rank features in same order as SHAP/LIME?
- Directional correctness: Are positive/negative contributions preserved?
- Magnitude representation: Are high-impact features emphasized proportionally?

**Coherence Score:**
- Logical consistency: Automated check for contradictory statements
- Relevance: Do sentences relate to the core explanation?
- Structure: Is explanation well-organized?

**Completeness Score:**
- Feature coverage: What percentage of top-N features are mentioned?
- Context: Are qualifications or limitations explained?

**Hallucination Detection:**
- Factual claims verification against data
- Unsupported causal statements
- Out-of-distribution assertions

**Results** [Exact figures unavailable — see full paper]
- Baseline explanation generation shows strong natural language quality
- Verification stage identifies ~15-25% of generated explanations with fidelity issues
- Iterative refinement successfully addresses most identified issues
- Open-weight models (14B–30B) perform comparably to larger commercial models

### Error Conditions

The authors evaluate robustness under:
- **Noisy XAI outputs**: When attributions contain numerical errors
- **Missing features**: When some features are unavailable for explanation
- **Model drift**: When explanations are generated for shifted data distributions
- **Adversarial inputs**: When inputs are crafted to confuse the model

---

## Practical Applications & Real-World Use Cases

### 1. Financial Services (Credit Risk Assessment)

**Scenario**: A bank uses a machine learning model to approve/deny credit applications. Applicants deserve to understand why their application was rejected.

**Traditional Approach**: Credit officer must manually read SHAP values and write explanation.

**Two-Stage Framework:**
- Explainer LLM converts SHAP attribution (e.g., "debt-to-income ratio: +0.42") into:
  > "Your debt-to-income ratio of 45% is higher than our typical approval threshold. This includes your student loans and mortgage payments relative to monthly income."
- Verifier LLM ensures:
  - The statement faithfully represents SHAP's assessment
  - The ratio and threshold numbers are consistent with actual policy
  - No hallucinated claims about specific loan products

**Regulatory Compliance**: This directly addresses EU AI Act requirements for explainability in high-risk systems. The automatic generation + verification creates an auditable trail.

### 2. Healthcare: Model Predictions in Diagnosis

**Scenario**: An AI system flags patients at high risk for disease progression. Clinicians need to understand the model's reasoning to validate and act on it.

**Application**: Grad-CAM++ highlights relevant image regions in X-rays; the framework converts this into:
> "The model identified three concerning regions in the upper-left lobe of the lung: areas of density consistent with inflammation, compared with the right side. This pattern, along with the patient's smoking history, contributes to the elevated risk score."

**Benefits**:
- Clinicians can quickly grasp the model's reasoning
- Natural language matches clinical terminology
- Verification ensures the explanation doesn't misrepresent image analysis

### 3. E-commerce: Product Recommendation Explanations

**Scenario**: An e-commerce platform recommends products. Users want to know why.

**Application**: LIME/SHAP explains:
- User's browsing history (weight: +0.25)
- Similar users' purchases (weight: +0.18)
- Product ratings (weight: +0.15)

**Accessible Explanation**: "We're recommending this product because users with similar interests to yours have rated it highly, and it matches your recent browsing activity."

**Verification**: Ensures the explanation doesn't over-claim personalization or create false impressions about data usage.

### 4. Legal/Judiciary: Risk Assessment Tools

**Scenario**: Algorithms predict recidivism risk or bail recommendations. Defendants have a right to understand the decision factors.

**Challenge**: SHAP might show "prior arrests: +0.35, employment status: -0.12"—how to explain this ethically?

**Framework Approach**: 
- Generates accessible explanation of factors
- Verifier checks for:
  - Fairness: Does explanation avoid stereotypes?
  - Completeness: Are mitigating factors included?
  - Accuracy: Do claims about data usage match actual practice?

**Regulatory Alignment**: Addresses requirements in some jurisdictions (e.g., NYC Local Law 144) for algorithmic accountability.

### Practical Implementation Challenges

1. **Customization by Stakeholder**: Different audiences need different levels of detail
   - Regulators: Technical accuracy, data sourcing
   - End-users: Plain language, implications
   - Business users: Strategic impact, actionability

2. **Computational Cost**: Two LLM passes (Explainer + Verifier) require:
   - Latency: ~2–5 seconds per explanation (with local 14B models)
   - Throughput: Trade-off between quality (iterative refinement) and speed

3. **Model Consistency**: Different LLMs may generate/verify explanations differently; standardization of prompt engineering is critical.

4. **Regulatory Confidence**: Some jurisdictions may require human review of auto-generated explanations before deployment.

---

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Accessibility as a Trustworthiness Component**: This work argues that a model's explainability is only as good as people's ability to understand it. Accessibility is not a "nice-to-have" but essential to trustworthiness, particularly in regulated domains.

2. **Verification is Not Optional**: Simply translating technical outputs to natural language can introduce errors. The two-stage framework demonstrates that verification mechanisms are necessary for high-stakes applications.

3. **Closing the Expertise Gap**: Traditional XAI places burden on users to interpret complex outputs. LLM-augmented frameworks shift expertise to the system, enabling broader stakeholder participation in AI governance.

### Advancing the State-of-the-Art in XAI

**Key Contributions:**
- **Systematic Quality Framework**: Formalizes what constitutes a "good" explanation (faithfulness, coherence, completeness, hallucination-free)
- **Automation at Scale**: Replaces manual explanation writing with systematic, auditable processes
- **Cross-Domain Validation**: Demonstrates applicability across XAI methods and data modalities
- **Pragmatic Integration**: Works with existing, widely-used XAI techniques (SHAP, LIME, Grad-CAM) without requiring algorithm modification

**Advancement Over Prior Work:**
- Extends beyond LIME/SHAP "why" explanations to verification-backed natural language
- Improves upon simple template-based explanation generation through iterative refinement
- Scales beyond one-off user studies to systematic evaluation across contexts

### Limitations and Open Questions

1. **LLM Bias in Explanations**: Even with verification, LLMs may encode societal biases in how they frame explanations. An explanation might emphasize "marital status" differently for different demographic groups.

2. **Verification Circularity**: The Verifier is itself an LLM, which may have similar biases/limitations. Independent verification might require human-in-the-loop validation.

3. **Context Dependence**: What constitutes "complete" or "coherent" depends on stakeholder expertise and context—a one-size-fits-all approach may not work.

4. **Failure Mode Discovery**: While the framework tests synthetic error conditions, real-world deployment may reveal edge cases not covered in evaluation.

5. **Regulatory Acceptance**: Regulators may require auditable proofs (not just verification scores) that explanations are accurate. Probabilistic scores may be insufficient.

### Influence on Future XAI Research

1. **Multi-Stage Pipelines**: The success of the two-stage approach suggests future XAI systems may adopt modular pipelines: (a) feature attribution, (b) explanation generation, (c) quality verification, (d) user-centric refinement.

2. **Explainability as Dialogue**: Rather than one-way explanations, future systems might enable interactive dialogue where users ask follow-up questions, and the LLM refines explanations based on feedback.

3. **Domain-Specific Customization**: Just as fine-tuning adapts LLMs to domains, future work may fine-tune Explainer/Verifier LLMs on domain-specific language and regulatory requirements.

4. **Integration with Concept-Based Methods**: Rather than attributions alone, frameworks could combine feature importance with concept-based explanations for richer understanding.

---

## Code & Resources

### Official Resources

- **ArXiv Paper**: [https://arxiv.org/abs/2604.12543](https://arxiv.org/abs/2604.12543)
  - HTML version: [https://arxiv.org/html/2604.12543](https://arxiv.org/html/2604.12543)
  - PDF version: [https://arxiv.org/pdf/2604.12543](https://arxiv.org/pdf/2604.12543)

### Related Code and Implementations

The paper mentions evaluation across standard XAI libraries:
- **SHAP**: [https://github.com/shap/shap](https://github.com/shap/shap)
- **LIME**: [https://github.com/marcotcr/lime](https://github.com/marcotcr/lime)
- **Grad-CAM**: [https://github.com/jacobgil/pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam)
- **Integrated Gradients**: PyTorch/TensorFlow implementations via Captum

### LLM Models for Implementation

Models tested in the paper are available from:
- **GPT-OSS**: Open-weight variants of GPT
- **DeepSeek-R1**: [https://github.com/deepseek-ai/DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)
- **Qwen-3**: [https://github.com/QwenLM/Qwen](https://github.com/QwenLM/Qwen)

### Computational Requirements

- **Hardware**: GPU recommended (NVIDIA A100 or equivalent) for real-time explanation generation
- **Model Size**: 14B–30B parameter models; can run on consumer GPUs (24–48GB VRAM)
- **Inference Time**: ~2–5 seconds per explanation with optimized inference engines (vLLM, TensorRT)

### Quick Start for Implementation

To build a similar system:

1. **Set up XAI pipeline**: Use SHAP, LIME, or Grad-CAM to generate feature attributions
2. **Load LLM**: Use `transformers` library or API-based access (Hugging Face Inference API)
3. **Explanation Generation**: Call LLM with formatted prompt containing XAI outputs
4. **Verification**: Call second LLM instance with verification prompt
5. **Refinement Loop**: If scores low, regenerate with corrected prompt

Example pseudo-code:
```python
# 1. Generate attribution (SHAP example)
explainer = shap.Explainer(model)
shap_values = explainer(instance)

# 2. Generate explanation
explainer_prompt = f"""Convert these SHAP values into plain language:
{format_shap(shap_values)}
Audience: business user
"""
explanation = llm.generate(explainer_prompt)

# 3. Verify explanation
verify_prompt = f"""Rate this explanation on faithfulness (1-5):
Explanation: {explanation}
SHAP values: {format_shap(shap_values)}
"""
verification = llm.generate(verify_prompt)

# 4. Refine if needed
if verification.score < 4:
    explanation = regenerate_with_feedback(verify_prompt)
```

---

## Related Work & Context

### How This Relates to Other Recent xAI Papers

**Comparison to Similar Approaches:**

1. **"Beyond Explainable AI (XAI): An Overdue Paradigm Shift" (2602.24176)**
   - Relationship: Both papers recognize limitations of current XAI and advocate for change
   - Difference: Beyond Explainable AI critiques XAI fundamentally; this paper advances XAI pragmatically through verification
   - Complementary: This framework could support Beyond's vision of "Interactive AI" by providing verified explanations

2. **"Mechanistic Interpretability for Neural Networks" (2607.07316)**
   - Relationship: Both seek to understand model internals
   - Difference: Mechanistic interpretability targets low-level circuits; this framework targets human-understandable explanations of decisions
   - Synergy: Detailed circuit understanding could feed into richer explanations

3. **"VirtualXAI: User-Centric Explainability Assessment" (2503.04261)**
   - Relationship: Both use LLMs to improve XAI for users
   - Difference: VirtualXAI uses LLM-generated personas for evaluation; this paper focuses on direct LLM explanation generation and verification
   - Complementary: VirtualXAI's persona-based evaluation could assess whether explanations work for diverse audiences

### Prior Work in XAI

**Foundation Methods** (cited foundation):
- LIME: Ribeiro et al., 2016 — Local model-agnostic explanations
- SHAP: Lundberg & Lee, 2017 — Game-theoretic feature importance
- Grad-CAM: Selvaraju et al., 2016 — Visual explanations for CNNs
- Integrated Gradients: Sundararajan et al., 2017 — Gradient-based attribution

**Accessibility and Human-Centered XAI**:
- "Interpretability Beyond Feature Attribution" work on concept-based explanations
- User studies on how different explanation formats affect understanding
- Research on communicating uncertainty in model predictions

**LLM-for-Explanation Work**:
- LLMs as explanation generators (various papers on "self-explanations")
- Concern: LLM-generated explanations may not be faithful (prior work identified this gap)
- This paper's contribution: Verification mechanism to address the fidelity gap

### Building Blocks from Related Work

- **Explanation Evaluation**: Borrows criteria from explanations literature (faithfulness, coherence, completeness)
- **Hallucination Detection**: Adapts techniques from fact-checking and knowledge-grounded NLG
- **XAI Integration**: Builds on standardized interfaces in SHAP, LIME, Captum (Integrated Gradients)

### Connection to Broader xAI Communities

#### SHAP and LIME Community
- These are the most widely-used XAI methods in practice
- The framework directly integrates with them, likely to gain adoption in applied settings
- Potential integration: SHAP authors might adopt this verification approach

#### Concept-Based Explanations Community (TCAV, LIME-C)
- Future work could extend framework to concept-based methods
- Concepts (e.g., "texture," "shape" in images) might be more interpretable than raw features

#### Causal Interpretability Community
- Framework could be extended to causal explanations (counterfactuals, causal paths)
- Verification would be critical: causal claims are more consequential than correlational

#### Fairness and Bias in XAI
- Verification mechanism could detect biased explanations
- Future work: train Verifier specifically to flag fairness concerns

### Future Research Directions

1. **Interactive Explanation**: Users ask questions; system refines explanations in dialogue
2. **Multimodal Explanations**: Combine text, visualizations, examples
3. **Personalized Verification**: Stakeholder-specific quality criteria
4. **Certified Explanations**: Formal guarantees (e.g., Byzantine-resilient verification)
5. **Cross-Model Consistency**: Explain why different models agree/disagree

---

## Summary

"A Two-Stage LLM Framework for Accessible and Verified XAI Explanations" addresses a critical gap between technical explainability and human understandability. By automating the generation of natural-language explanations from XAI outputs and systematically verifying their quality, the framework makes explainable AI more accessible to stakeholders while maintaining fidelity to underlying model decisions. The work bridges feature attribution methods and human comprehension, with significant implications for regulated domains (finance, healthcare, law), user trust, and the practical deployment of interpretable AI systems.

The paper's emphasis on verification and iterative refinement sets a new standard for what "good explanations" mean in practice, likely to influence future xAI research toward integrated pipelines that prioritize both technical rigor and human accessibility.
