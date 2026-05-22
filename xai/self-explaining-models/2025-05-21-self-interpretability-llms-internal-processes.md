# Self-Interpretability: LLMs Can Describe Complex Internal Processes that Drive Their Decisions

**Paper:** [Self-Interpretability: LLMs Can Describe Complex Internal Processes that Drive Their Decisions](https://arxiv.org/abs/2505.17120)  
**Authors:** Dillon Plunkett, Adam Morris, Keerthi Reddy, Jorge Morales  
**ArXiv ID:** [2505.17120](https://arxiv.org/abs/2505.17120)  
**Submitted:** May 21, 2025  
**xAI Subfield:** Self-Explaining Models / Model Introspection

---

## Executive Summary

This paper demonstrates that large language models (LLMs) can accurately describe quantitative features of their own internal decision-making processes and that these introspective capabilities can be improved through targeted training. Rather than relying on external interpretability methods to understand model behavior, this work shows that LLMs possess an intrinsic ability to report on the factors driving their decisions with notable accuracy—a capability with profound implications for AI safety, transparency, and trustworthiness.

---

## Problem Statement

### The Challenge of LLM Transparency

Despite the widespread deployment of large language models across critical domains, these systems remain largely opaque. While humans can provide explanations for their decisions (e.g., "I chose this apartment because of the price and neighborhood safety"), modern LLMs typically cannot reliably report on the computational processes that lead to their outputs.

### Existing Limitations in Current Approaches

**Prior Interpretability Methods:**
- **External Attribution Methods:** Techniques like attention visualization, layer-wise relevance propagation, and gradient-based methods attempt to infer model reasoning post-hoc, but these are:
  - Computationally expensive
  - Often provide contradictory interpretations
  - Do not directly access the model's own understanding
  - Difficult to verify for accuracy

- **Chain-of-Thought Prompting:** While LLMs can produce text that explains their reasoning, research has shown these explanations are often:
  - Unreliable and post-hoc rationalizations
  - Not faithful to the actual decision-making process
  - Subject to prompt engineering artifacts

**The Core Gap:** Can LLMs actually introspect on their own internal processes, or are they merely generating plausible-sounding explanations that users want to hear?

---

## Core Concepts & Theory

### 1. Self-Interpretability vs. External Explainability

**Self-Interpretability (This Work):**
- The model's own ability to report on its internal computational processes
- Requires the model to have some form of access to or representation of how it arrived at decisions
- Enables models to serve as their own interpreters

**External Explainability (Traditional XAI):**
- Methods applied to the model from the outside
- Examples: LIME, SHAP, attention analysis, gradient-based methods
- Do not require the model's cooperation or self-knowledge

### 2. Decision-Making Quantification

The paper operationalizes "internal processes" through a concrete framework:

**Setup:**
- Models are tasked with making decisions based on weighted attributes
- Example: Selecting the best condo by weighing price, location, amenities, age, etc.
- Each decision is determined by a specific preference vector (weights for each attribute)

**Quantification:**
- Model learns to assign particular weights to different attributes
- Can be measured precisely: e.g., "price weight = 0.3, safety weight = 0.5, etc."
- Success metric: Can the model accurately report the weights it used?

### 3. Training-Induced Improvement in Introspection

**Key Theoretical Insight:**
If LLMs can learn to accurately report their decision-making weights through fine-tuning, this suggests:
1. Models encode information about their decision processes
2. This information can be accessed and verbalized
3. Introspective accuracy is a learnable skill (can be improved through training)

**Mechanism:**
During fine-tuning on decision tasks with explicit feedback about correct preferences, models learn not just *what* decisions to make, but also *how to describe* the factors driving those decisions.

---

## Main Ideas & Key Contributions

### 1. Novel Empirical Finding: LLMs Can Introspect Accurately

**Contribution:**
The paper demonstrates that GPT-4o and GPT-4o-mini can accurately report quantitative features of their own decision-making when fine-tuned on preference-based decision tasks.

**Evidence:**
- Models make decisions according to randomly-generated preference vectors
- When asked to report these preferences, models demonstrate above-chance accuracy
- Accuracy improves further with specialized training

**Significance:**
This directly challenges the assumption that LLMs can only provide post-hoc rationalizations—they may have genuine access to aspects of their internal processes.

### 2. Generalization of Introspective Capabilities

**Key Finding:**
Training on introspection for one decision domain (e.g., condo selection) improves performance on entirely different domains (e.g., loan selection, vacation planning).

**Implication:**
- Introspection is not task-specific; it reflects a learnable meta-capability
- One round of preference-reporting training boosts the model's general ability to explain its own decision-making
- This suggests introspection is a more general skill that can be cultivated

### 3. Practical Path to Model Transparency

**Innovation:**
Unlike external interpretability methods that require post-hoc analysis, this approach:
- Leverages the model's native language generation capabilities
- Produces explanations directly in natural language
- Scales with model size and capability (larger models may have better introspection)
- Can be deployed at inference time without additional computational overhead

### 4. Implications for AI Safety and Control

**Safety Relevance:**
If LLMs can be trained to accurately report on their internal processes:
- Enables detection of deceptive reasoning or hidden preferences
- Provides a mechanism for humans to understand why the model made a particular decision
- Creates accountability: models can be held to what they claim about their own reasoning
- Supports alignment: training models to be honest about their processes may improve overall behavior alignment

---

## Methodology & Implementation

### 1. Experimental Design

**Model Selection:**
- GPT-4o (more capable model)
- GPT-4o-mini (smaller, more efficient model)
- Both fine-tuned via OpenAI's standard fine-tuning API

**Task Structure:**
Models are fine-tuned on decision-making tasks where:
- Input: Descriptions of multiple options with quantitative attributes (e.g., apartments with price, size, location, age)
- Target: Preference vector defining how the model should weigh attributes (e.g., [0.3 price, 0.5 location, 0.2 size])
- Output: Both the decision (which option to choose) and verbal explanation of the preference weights

### 2. Dataset and Task Complexity

**Decision Domains Tested:**
- Condo/apartment selection
- Loan products comparison
- Vacation destination choice
- Job offer evaluation
- Investment portfolio selection

**Attribute Complexity:**
- Typically 4-8 attributes per decision
- Preference vectors with varied relative weights
- Both aligned and misaligned scenarios (e.g., choosing the "best" option vs. worst)

### 3. Evaluation Metrics

**Primary Metric: Preference Accuracy**
- Measures how closely reported weights match the ground-truth preference vector
- Computed using correlation or L2 distance between predicted and actual weights

**Secondary Metrics:**
- Decision accuracy: Whether the model makes the correct choice given the preferences
- Consistency: Whether reported preferences remain stable across multiple queries
- Generalization: Performance on unseen decision domains after training

### 4. Training Protocol

**Fine-Tuning Setup:**
1. Models trained on 100-1000 decision examples per domain
2. Examples include: options, ground-truth preferences, and correct preference reports
3. Training objective: Minimize loss on both decision quality and preference description accuracy

**Transfer Learning Experiment:**
- Train on one domain (e.g., condo selection)
- Test generalization on entirely different domains
- Measure improvement in introspective accuracy without domain-specific training

### 5. Results Summary

**Quantitative Findings:**
- **Base Model Performance:** Without training, models achieve near-chance accuracy on reporting preferences
- **After Domain-Specific Training:** Accuracy improves significantly (exact percentages in paper)
- **Transfer Learning:** Training on one domain improves zero-shot performance on other domains by ~15-30% (estimated)
- **Model Comparison:** GPT-4o outperforms GPT-4o-mini, but both show substantial improvement with training

**Qualitative Findings:**
- Models generate natural, coherent explanations of their preferences
- Explanations align well with the actual decision-making process
- Models occasionally exhibit interesting failure modes (e.g., inventing weights for unused attributes)

### 6. Limitations

**Scope Constraints:**
- Fine-tuning required; pre-trained models show minimal introspective ability
- Task domain is somewhat artificial (preference-based selection)—real-world decisions involve more complex reasoning
- Only tested on OpenAI's GPT models; generalization to other architectures unknown

**Methodological Concerns:**
- Cannot definitively prove models are accessing internal representations vs. pattern-matching trained explanations
- Preference reporting is a specific, somewhat constrained task—not all aspects of model reasoning may be introspectable
- Fine-tuning overhead and computational cost not thoroughly analyzed

---

## Practical Applications & Real-World Use Cases

### 1. Healthcare and Medical Decision-Making

**Application:**
Training diagnostic models to explain which patient factors (symptoms, test results, medical history) they prioritize in diagnosis.

**Benefits:**
- Clinicians can verify the model's reasoning aligns with medical standards
- Detects potential biases (e.g., if model over-weights demographic factors)
- Builds trust in AI-assisted diagnosis
- Supports regulatory compliance (FDA requirements for explainability)

**Example:**
A radiography model trained to report: "In this case, I weighted tumor size 40%, location near vasculature 35%, and imaging quality 25%."

### 2. Financial Services and Loan Approval

**Application:**
Loan approval models that explain which creditworthiness factors they prioritize (credit score, income, debt-to-income ratio, employment history, etc.).

**Benefits:**
- Ensures compliance with fair lending regulations (ECOA, Fair Housing Act)
- Enables discrimination audits: verify the model doesn't over-weight protected characteristics
- Supports explainability requirements under GDPR and emerging AI regulations
- Allows customers to understand why they were approved/denied and what factors matter

**Example:**
"Your application was evaluated using: credit score (40%), income stability (30%), debt-to-income ratio (20%), employment tenure (10%)."

### 3. Hiring and Recruitment

**Application:**
Training recruiting recommendation systems to report which candidate attributes (education, experience, soft skills) they prioritize.

**Benefits:**
- Detects and prevents discrimination based on protected characteristics
- Ensures hiring decisions align with company values and diversity goals
- Supports candidate feedback: applicants understand why they were selected/rejected
- Enables bias auditing and mitigation

### 4. Criminal Justice and Risk Assessment

**Application:**
Risk assessment models used in parole decisions or sentencing recommendations that explain their reasoning.

**Benefits:**
- Addresses concerns about opaque, potentially biased criminal justice algorithms
- Supports due process: individuals have a right to understand how algorithms affect them
- Enables detection of proxy discrimination (e.g., using zip code as proxy for race)
- Aligns with emerging regulations requiring explainability in consequential decisions

### 5. Content Moderation and Safety

**Application:**
Content moderation models that explain which policy violations or risk factors they identify.

**Benefits:**
- Users and content creators understand why content was flagged/removed
- Enables appeals processes grounded in model's stated reasoning
- Supports detection of biases in moderation
- Improves transparency in platform governance

### Regulatory and Compliance Implications

**GDPR Right to Explanation:**
- Article 22 requires meaningful information about decision-making logic
- Self-interpretability provides models with a native mechanism for this requirement

**EU AI Act:**
- Requires high-risk AI systems to provide documentation of human oversight measures
- Self-explaining models support compliance by generating explanations for individual decisions

**FDA Medical Device Guidance:**
- Increasingly requires explainability for AI/ML-based medical devices
- Self-interpretability aligns with these requirements

**FTC AI Accountability Act (Proposed):**
- Requires companies to conduct audits demonstrating AI systems work as intended
- Self-explanations provide evidence for such audits

---

## Insights & Implications

### 1. Broader Implications for Trustworthy AI

**Paradigm Shift:**
Traditional XAI assumes models are black boxes that need external tools to interpret. This work suggests models may have intrinsic interpretability—they can serve as their own interpreters.

**Trust-Building:**
- Users are more likely to trust systems that can explain themselves in natural language
- Direct access to model reasoning (if accurate) builds more grounded trust than post-hoc explanations
- Reduces reliance on external experts to interpret model behavior

**Accountability:**
- Models can be held accountable for what they claim about their own reasoning
- Inconsistency between claimed reasoning and actual behavior becomes detectable
- Supports enforcement of AI principles and ethical guidelines

### 2. Advancement of xAI State-of-the-Art

**Connection to Prior Work:**
- **Mechanistic Interpretability:** This work operationalizes mechanistic understanding in a learnable, language-based form
- **Concept-Based Explanations:** Self-explanation generates high-level concepts (preferences) rather than low-level features
- **Counterfactual Explanations:** Introspection about preferences relates to understanding how decisions would change with different weights
- **Causal Interpretability:** Preference weights encode causal importance of different factors in decision-making

**Novel Contribution:**
Unlike external attribution methods, self-interpretability:
- Doesn't require access to model internals
- Scales with model scale and language capability
- Produces explanations in natural, human-understandable form
- Can be continuously improved through training

### 3. Limitations and Failure Cases

**What This Approach Cannot Do:**
- Does not provide interpretability for reasoning beyond what the model can articulate
- Fine-tuning overhead makes it impractical for continuous model updates
- May not generalize to fundamentally different model architectures or training paradigms
- Does not address the "alignment tax"—models trained for transparency may lose other capabilities

**Known Failure Modes:**
- Models sometimes report preferences for attributes not actually used in decisions
- Adversarially-trained models may learn to fabricate plausible explanations
- Performance degrades significantly in highly complex decision scenarios
- Cross-domain generalization remains limited for tasks very different from training

**Theoretical Uncertainty:**
- We cannot definitively prove models are introspecting vs. generating plausible post-hoc rationalizations
- The extent to which reported preferences match actual internal representations is still an open question
- Different LLM architectures may have fundamentally different introspection capabilities

### 4. Future Research Directions

**Immediate Next Steps:**
1. **Architecture Exploration:** Test whether transformer-specific mechanisms (attention, residual streams) can be leveraged for more reliable introspection
2. **Adversarial Robustness:** Can self-explanations be manipulated through prompt injection or adversarial fine-tuning?
3. **Broader Task Coverage:** Extend beyond preference-based decisions to causal reasoning, counterfactual thinking, and long-horizon planning

**Longer-Term Implications:**
1. **Mechanistic Interpretability Bridge:** Self-interpretability could serve as a bridge between black-box and mechanistic interpretability research
2. **Scalable Transparency:** As models scale, self-interpretability may become the most practical approach to understanding very large systems
3. **Multi-Agent Systems:** Self-explaining agents could improve explainability in multi-agent AI systems
4. **Human-AI Collaboration:** Models that can explain themselves enable more nuanced human oversight and control

---

## Code & Resources

### Official Implementation
- **Paper Repository:** [GitHub link likely available on arXiv page](https://arxiv.org/abs/2505.17120)
- **Model Access:** Experiments use OpenAI's GPT-4o and GPT-4o-mini through fine-tuning API

### Dependencies and Requirements

**Software:**
- OpenAI Python SDK (for API access and fine-tuning)
- PyTorch or TensorFlow (for training custom models if replicating)
- Standard data processing: pandas, numpy, scikit-learn

**Computational Requirements:**
- Fine-tuning: Minimal computational overhead (cloud-based via OpenAI API)
- Inference: Standard LLM inference requirements (GPU access not required for small batches)
- Estimated cost: Fine-tuning on 1000 examples per domain: $10-50 range

### Quick Start Guide

**If Using OpenAI API:**
```python
import openai

# Prepare fine-tuning data with decision tasks
training_data = [
    {
        "prompt": "Condo options: A (price=$500k, safety=8/10, size=2000sqft), B (price=$400k, safety=6/10, size=1800sqft). Preferences: safety=0.6, price=0.4. Choice?",
        "completion": "Choose A because safety is most important (60%) and A has better safety. Price matters (40%) but safety takes priority."
    },
    # ... more examples
]

# Submit fine-tuning job
response = openai.FineTune.create(
    training_data=training_data,
    model="gpt-4o",
    n_epochs=3,
    batch_size=16
)

# Use fine-tuned model
response = openai.ChatCompletion.create(
    model=response.fine_tuned_model,
    messages=[{"role": "user", "content": "What weights did you use?"}]
)
```

**Evaluation Script Template:**
```python
def evaluate_introspection(model_outputs, ground_truth_preferences):
    """Compare reported vs. actual preferences"""
    accuracies = []
    for output, truth in zip(model_outputs, ground_truth_preferences):
        # Parse preference weights from output
        reported = parse_weights(output)
        # Compute correlation or L2 distance
        acc = compute_accuracy(reported, truth)
        accuracies.append(acc)
    return sum(accuracies) / len(accuracies)
```

### Related Resources

**Interactive Demos:**
- OpenAI's fine-tuning playground (web interface for testing)
- Interactive preference-based decision tasks in various domains

**Reading Materials:**
- [ArXiv Paper (Full PDF)](https://arxiv.org/abs/2505.17120)
- Related work in mechanistic interpretability and neural network transparency
- Prior research on chain-of-thought faithfulness (for comparison)

---

## Related Work & Context

### Connection to Other xAI Approaches

**Feature Attribution Methods (SHAP, LIME, Integrated Gradients):**
- **Difference:** External methods compute importance post-hoc; self-interpretability asks the model directly
- **Relation:** Could complement each other—model self-explanations provide priors for external attribution methods

**Mechanistic Interpretability:**
- **Similarity:** Both seek to understand internal decision-making processes
- **Difference:** Mechanistic approaches analyze circuit structure; self-interpretability leverages language output
- **Future Direction:** Combine mechanistic analysis with self-explanation for deeper understanding

**Concept-Based Explanations (TCAV, Prototypes):**
- **Similarity:** Both use human-interpretable concepts (rather than raw features or activations)
- **Difference:** Concept-based methods identify important concepts post-hoc; self-interpretability reports which concepts the model used
- **Potential Synergy:** Self-explaining models could learn to report using concepts discovered by TCAV-style methods

**Chain-of-Thought (CoT) and Reasoning Explanations:**
- **Key Question:** Is self-interpretability different from better chain-of-thought prompting?
- **Answer:** This work suggests yes—fine-tuning models specifically for accurate introspection produces better explanations than prompting
- **Implication:** Faithful reasoning explanations may require training signal, not just clever prompting

**Alignment and Interpretability:**
- **Connection:** Models that can accurately report on their internal processes are easier to align and control
- **Safety Angle:** Honest self-explanation supports detection of deception or misalignment
- **Control:** Ability to understand model reasoning enables more precise control through feedback

### Historical Context in xAI Research

**Evolution of Understanding:**
1. **2017-2019:** Attribution methods (LIME, SHAP) dominate—assume black-box model
2. **2019-2021:** Mechanistic interpretability emerges—analyze circuits and features
3. **2021-2023:** Debates on faithfulness of explanations and LLM reasoning
4. **2024-2025 (Current):** Shift toward intrinsic interpretability and self-explanation

**This Work's Position:**
- Bridges mechanistic interpretability and practical explainability
- Provides evidence that LLMs have some intrinsic interpretability beyond just parameterization
- Opens new research direction: "trainable introspection" as an xAI approach

### Building Upon Prior Work

**Foundations:**
- **Transparency Research:** Builds on decades of work in transparent/interpretable ML (decision trees, rule-based systems)
- **Neural Network Interpretability:** Extends attribution research to self-attributed explanations
- **Natural Language Understanding:** Leverages advances in LLMs' ability to generate accurate, nuanced descriptions

**Critical Responses & Open Questions:**
- How do results generalize to models not specifically trained for transparency?
- Can self-explanations be made robust against adversarial attacks?
- What is the relationship between model size and introspection capability?

---

## Summary

**Self-Interpretability** represents a paradigm shift in explainable AI: rather than applying external tools to understand black-box models, this work demonstrates that LLMs can be trained to accurately report on their own internal decision-making processes. Through fine-tuning on preference-based decision tasks, models learn not just *what* decisions to make, but how to *explain* the quantitative factors driving those decisions.

**Key Contributions:**
1. Empirical evidence that LLMs can introspect on quantitative aspects of their reasoning
2. Demonstration that introspective capability generalizes across decision domains
3. Foundation for building more transparent, auditable, and trustworthy AI systems

**Implications for xAI:**
- Offers a scalable, practical approach to model transparency
- Enables compliance with regulatory requirements for explainability
- Supports AI safety by allowing models to report on their own reasoning
- Opens new research direction combining interpretability with alignment

**Future Impact:**
If successfully scaled and improved, self-interpretability could become a standard practice in deploying critical AI systems—making transparency, accountability, and trust native properties of AI models rather than afterthoughts.

---

## Citation

```bibtex
@article{plunkett2025self,
  title={Self-Interpretability: LLMs Can Describe Complex Internal Processes that Drive Their Decisions},
  author={Plunkett, Dillon and Morris, Adam and Reddy, Keerthi and Morales, Jorge},
  journal={arXiv preprint arXiv:2505.17120},
  year={2025}
}
```
