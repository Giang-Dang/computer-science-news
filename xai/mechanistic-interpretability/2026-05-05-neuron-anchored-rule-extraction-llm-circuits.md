# Neuron-Anchored Rule Extraction for Large Language Models via Contrastive Hierarchical Ablation

**ArXiv ID:** 2605.03058  
**Submitted:** May 5, 2026  
**Authors:** [Research team conducting mechanistic interpretability research]  
**Link:** https://arxiv.org/abs/2605.03058

## Executive Summary

This paper introduces MechaRule, a novel pipeline that bridges symbolic rule extraction and mechanistic interpretability by grounding interpretable rules directly in LLM circuits through contrastive hierarchical ablation. The approach identifies sparse "agonist" neurons whose activation causally influences model behavior, enabling faithful symbolic explanations grounded in neural mechanisms. This advances trustworthy AI by combining the symbolic interpretability of rule extraction with the mechanistic faithfulness of circuit analysis.

## Problem Statement

Explainable AI faces a fundamental challenge: symbolic rule extraction methods (like decision trees and logical rules) produce interpretable outputs but lack grounding in actual model computations, making explanations potentially unfaithful to the model's true decision logic. Conversely, mechanistic interpretability can identify which neural components drive behaviors but typically requires hand-crafted hypotheses and expensive neuron-level interventions, limiting scalability.

Prior approaches:
- **Global rule extraction:** Learns symbolic surrogates without mechanistic grounding; risks generating rules that don't reflect actual model computations
- **Standard mechanistic interpretability:** Heavily dependent on manual hypotheses about which neurons matter; expensive brute-force neuron interventions at scale
- **Activation patching:** Effective but produces unstructured high-dimensional datasets difficult to compress into symbolic form

## Core Concepts & Theory

### Mechanistic Interpretability Fundamentals

Mechanistic interpretability aims to reverse-engineer neural networks by identifying interpretable circuits—subsets of model components whose computations directly cause specific behaviors. A circuit includes neurons, attention heads, and their connections that collectively implement a behavioral function.

### Rule Extraction Background

Rule extraction translates neural network decisions into symbolic if-then rules (e.g., "IF feature_A > threshold AND feature_B < threshold THEN decision=X"). Benefits include human interpretability and actionability; challenges include ensuring rules faithfully reflect model behavior.

### Contrastive Hierarchical Ablation

The key innovation is organizing neurons hierarchically and performing group ablations:

1. **Hierarchy Construction:** Neurons are organized into nested groups based on structural and functional similarity
2. **Hierarchical Ablation:** Rather than testing individual neurons, test groups at multiple granularity levels
3. **Contrastive Learning:** Use contrasting conditions (baseline vs. flipped) to identify which neuron activations matter for specific behaviors

This approach dramatically reduces computational cost compared to brute-force neuron-by-neuron intervention while maintaining localization accuracy.

### Agonist Identification

**Agonists** are neurons whose activation changes causally influence target behaviors:
- When agonist activations are suppressed → behavior changes (rules fail)
- Agonist effects are approximately **monotone and saturating**: a few dominant neurons can "outcompete" weaker ones
- Multiple overlapping neurons may flip the same examples, indicating redundancy

This monotone-saturating property is theoretically motivated and empirically validated, enabling efficient localization.

### Mathematical Formulation

For a neuron $n$ and behavior $b$:

**Causal Effect:** $CE(n, b) = P(\text{behavior } b \text{ flips} | n \text{ ablated})$

**Agonist Set:** $A = \{n : CE(n, b) > \tau\}$ for threshold $\tau$

**Rule Generation:** For identified agonist set $A$:
- Extract features $F$ that correlate with agonist activations
- Learn rules: $\text{IF } F_1 \text{ AND } F_2 \ldots \text{ THEN } b \text{ occurs}$

## Main Ideas & Key Contributions

### 1. MechaRule Pipeline

The complete pipeline consists of:

1. **Feature Identification:** Automatically discover features from activation patterns and manually define seed features
2. **Hierarchical Localization:** Efficiently identify sparse agonist neurons using contrastive group ablations
3. **Rule Learning:** Extract symbolic if-then rules grounded in identified agonists using RuleSHAP
4. **Validation:** Test whether rule-predicted behavior matches actual model interventions

### 2. Efficiency Gains

- **Baseline:** Brute-force intervention on all neurons = N ablations (expensive for LLMs with millions of neurons)
- **MechaRule:** Hierarchical approach = O(log N) ablations through group testing
- **Result:** 96.8% recall of high-effect agonists while reducing computational cost by orders of magnitude

### 3. Interpretability Innovation

By grounding rules in specific neurons (agonists), the method achieves:
- **Faithfulness:** Rules directly correspond to causal circuit components
- **Explicitness:** Users understand which neurons implement which rules
- **Actionability:** Can modify specific neurons to change behavior predictably

### 4. Bridging Two Paradigms

Connects symbolic and mechanistic interpretability:
- **Symbolic:** Human-interpretable rules
- **Mechanistic:** Neural circuit grounding
- **Result:** Rules that are both interpretable AND faithful to model internals

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- Qwen2 (modern instruction-tuned LLM)
- GPT-J (open-source dense LLM)
- Additional models for generalization validation

**Tasks and Behaviors:**
1. **Arithmetic reasoning:** Model's ability to perform multi-digit addition and multiplication
2. **Jailbreak resistance:** Model's ability to refuse harmful requests
3. **Control behavior:** Ensuring rules don't apply to unintended behaviors

### Datasets

- **Arithmetic:** Curated arithmetic problems (add, multiply) with ground-truth answers
- **Jailbreak:** Harmful prompts with expected refusal responses; benign prompts with expected assistance
- **Behavioral control:** Out-of-distribution examples to validate rule specificity

### Evaluation Metrics

1. **Agonist Recall:** Percentage of high-effect neurons identified by MechaRule vs. brute-force baseline
   - Metric: $\text{Recall} = \frac{\text{Identified agonists} \cap \text{High-effect neurons}}{\text{High-effect neurons}}$

2. **Behavioral Faithfulness:** Does suppressing identified agonists actually change behavior?
   - Metric: Accuracy drop when agonists are ablated

3. **Rule Accuracy:** Do extracted rules predict when model behavior changes?
   - Metric: Precision and recall of rules on held-out test set

4. **Computational Efficiency:** Reduction in number of interventions needed
   - Metric: Ablations required / total possible neurons

### Key Results

| Metric | Qwen2 | GPT-J | Result |
|--------|-------|-------|--------|
| Agonist Recall | 97.2% | 96.4% | High identification accuracy |
| Arithmetic Accuracy Drop (agonist suppression) | 71.1% | 68.3% | Strong causal effect |
| Jailbreak Success Drop | 8.8% | 7.2% | Meaningful behavior modification |
| Computational Cost Reduction | ~500x | ~450x | Massive efficiency gain |

### Limitations

1. **Scope:** Tested on specific behaviors (arithmetic, jailbreak); unclear how well it generalizes to all LLM behaviors
2. **Manual seeding:** Requires some manually defined seed features for rule learning; not fully automated
3. **Threshold sensitivity:** Results depend on choice of agonist threshold $\tau$; optimal selection is task-dependent
4. **Scale:** Works on neurons; circuit-level interactions between neurons not fully captured
5. **Rule complexity:** Extracted rules may still be too complex for high-dimensional feature spaces

## Practical Applications & Real-World Use Cases

### 1. AI Safety & Alignment

**Application:** Understand and modify refusal behaviors in safety-aligned models
- **Use Case:** When an LLM incorrectly refuses helpful requests, MechaRule identifies which neurons cause false refusals, enabling targeted interventions
- **Regulatory Impact:** Supports transparency requirements (GDPR, AI Act) by providing mechanistic explanations for model decisions
- **Example:** Identify neurons responsible for overly cautious refusal patterns and adjust their function

### 2. Healthcare & Medical AI

**Application:** Understand diagnostic decision-making in clinical decision support systems
- **Use Case:** When an AI system recommends a particular treatment, clinicians need to understand the reasoning. MechaRule can identify which computational units drive the recommendation
- **Compliance:** Supports FDA requirements for model transparency in clinical applications
- **Example:** For a radiology AI suggesting lung nodule biopsy, identify neurons that respond to specific image features

### 3. Financial Services

**Application:** Credit scoring and loan approval decisions
- **Use Case:** Regulatory bodies (e.g., FDIC, SEC) require explainability for automated credit decisions. MechaRule enables mechanistic explanations
- **Fairness:** Identify if certain neurons exhibit biased patterns and intervene appropriately
- **Example:** For loan rejection, trace the specific neural computations that weighted applicant's income or credit history

### 4. Content Moderation

**Application:** Detect and understand content moderation decisions
- **Use Case:** Content moderation systems using LLMs make high-stakes decisions on user content. MechaRule helps understand whether moderation is based on intended signals or spurious patterns
- **Example:** Identify if toxicity detection is based on genuinely harmful language or correlates with demographic markers

### 5. Autonomous Systems

**Application:** Understand decision-making in autonomous vehicles and robotic systems
- **Use Case:** When safety-critical decisions fail, mechanistic understanding enables root cause analysis
- **Example:** For autonomous vehicle collision avoidance, identify which neural components respond to pedestrian detection

### Regulatory & Compliance Implications

- **GDPR Right to Explanation:** Articles 13-14 require algorithmic decisions to be explainable; MechaRule provides mechanistic explanations
- **EU AI Act:** Transparency requirements for high-risk AI; mechanistic interpretability strengthens compliance
- **FDA 21 CFR Part 11:** Requires understanding of algorithm behavior in clinical applications
- **Fair Lending Laws:** Require ability to audit decision factors; mechanistic grounding enables this

### Implementation Challenges

1. **Computational Cost:** Even hierarchical ablation requires multiple model forward passes; may be expensive for extremely large models
2. **Feature Interpretation:** Automatically discovered features may be semantically uninterpretable; requires human-in-the-loop validation
3. **Rule Learning:** Converting sparse agonist information to human-friendly rules is non-trivial; RuleSHAP requires tuning
4. **Model Variation:** Rules may differ across model architectures and versions; must re-run analysis for new models

## Insights & Implications

### Broader Impact on Trustworthy AI

1. **Bridging Symbolic and Mechanistic:** This work demonstrates that symbolic rules CAN be grounded in neural mechanisms, contradicting the view that rule extraction and mechanistic interpretability are separate paradigms

2. **Scalability Progress:** By reducing computational cost from N to O(log N) interventions, the paper makes mechanistic interpretability more practical for production systems

3. **Faithfulness Guarantees:** Unlike post-hoc explanations (LIME, SHAP), rules extracted via MechaRule are guaranteed to reflect actual neural computation

### State-of-the-Art Advancement

- **Previous SOTA:** Hand-crafted hypothesis + targeted interventions (e.g., finding specific attention heads)
- **This Work:** Systematic, scalable method to identify ALL causal neurons for a behavior
- **Improvement:** Both more comprehensive and more automated

### Limitations & Open Questions

1. **Behavioral Granularity:** Rules are extracted for specific discrete behaviors (arithmetic, jailbreak). How to handle continuous, nuanced behaviors?

2. **Superposition Problem:** If neurons encode multiple overlapping concepts (superposition), can we still extract clean rules?

3. **Compositionality:** Do rules for sub-behaviors compose to explain complex multi-step reasoning?

4. **Generalization:** Agonist sets for one model may not transfer to similar architectures. Why? How to predict?

5. **Adversarial Robustness:** Can adversarial attacks bypass the identified agonist neurons? What about adversarial examples?

### Future Research Directions

1. **Hierarchical Rule Composition:** Extract rules at multiple levels of abstraction; compose them into interpretable reasoning chains

2. **Dynamic Circuit Analysis:** Current work assumes fixed circuits; how do circuits change during inference? How does attention pattern evolution affect rule applicability?

3. **Cross-Model Transferability:** Develop methods to transfer agonist understanding between models

4. **Real-Time Interpretability:** Enable users to ask "why" questions during inference and get mechanistic answers in real-time

5. **Interventional Reliability:** Beyond suppressing agonists, can we precisely steer behavior by modulating agonist activations?

6. **Scalability to Multimodal Models:** Extend MechaRule to vision-language models where circuits may span image and text modalities

## Code & Resources

### Official Implementation

- **GitHub Repository:** Expected to be released at https://github.com/[paper-authors]/mechanule (check paper for exact link)
- **Code Availability:** Authors typically release code alongside paper publication on arXiv

### Dependencies & Requirements

- **PyTorch:** Model loading and intervention framework
- **Transformers library:** Access to Qwen2, GPT-J, and other HuggingFace models
- **RuleSHAP:** For symbolic rule extraction (may need custom implementation)
- **Activation patching toolkit:** For efficient group ablations

### Computational Requirements

- **Memory:** ~16-32GB GPU memory for full model loading (GPT-J is ~13B parameters)
- **Compute:** Hours to days depending on model size and number of behaviors analyzed
- **Storage:** Model weights + activations cache (50-100GB depending on models)

### Quick Start (Expected)

```python
from mechanule import MechaRule
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-7B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B")

# Initialize MechaRule
ruler = MechaRule(model, hierarchical=True)

# Extract rules for arithmetic behavior
rules = ruler.extract_rules(
    task="arithmetic",
    behaviors=["addition", "multiplication"],
    seed_features=["digit_recognition", "carry_operation"]
)

# Validate rules
validation_scores = ruler.validate_rules(rules, test_dataset)

# Suppress agonists and observe behavior change
modified_logits = ruler.suppress_agonists(input_ids, agonist_indices)
```

### Interactive Visualizations

- **Neuron Activation Maps:** Visualize which agonist neurons activate for different inputs
- **Rule Decision Trees:** Display extracted rules as interpretable decision trees
- **Ablation Effects:** Graph showing behavior change as groups of neurons are ablated

## Related Work & Context

### Connections to Other xAI Approaches

**Feature Attribution Methods (LIME, SHAP, Integrated Gradients):**
- **Similarity:** Also identify important features for decisions
- **Difference:** MechaRule grounds explanations in actual neural circuits, not approximations
- **Advance:** More faithful than post-hoc attribution; computationally more expensive

**Concept-Based Explanations (TCAV, ACE):**
- **Similarity:** Map activations to human-interpretable concepts
- **Difference:** MechaRule focuses on causal neurons, not concept clusters
- **Advance:** Can extract symbolic rules from concepts; integrates both paradigms

**Other Mechanistic Interpretability Work:**
- **Automated Circuit Discovery:** Previous papers identified circuits manually (e.g., attention head roles)
  - MechaRule automates and scales this process
- **Sparse Autoencoders:** Identify interpretable features; MechaRule uses similar ideas but anchors to rule extraction
- **Activation Patching:** Standard mechanistic method; MechaRule makes it efficient and rule-grounded

### Prior Work on Rule Extraction from Neural Networks

- **Neural Network Rule Extraction (1990s-2000s):** Early methods lacked mechanistic grounding
- **CIRL (2021):** Concept Bottleneck Models extract concepts; MechaRule extends to full rule logic
- **RuleSHAP:** Extracts symbolic rules; MechaRule provides neural grounding

### Building Blocks This Work Synthesizes

1. **Mechanistic Interpretability** (Vig & Belinkov 2019; Elhage et al. 2021)
2. **Activation Patching** (Wang et al. 2022; Meng et al. 2023)
3. **Hierarchical Clustering** (Neuron grouping based on activation patterns)
4. **Rule Extraction** (RuleSHAP, Interpretable Decision Trees)

### Where This Research Leads

**Short-term (1-2 years):**
- Extensions to larger models (GPT-4 scale) using more efficient ablation strategies
- Application to more diverse behaviors (reasoning, creativity, multimodal tasks)
- Integration with alignment research for targeted safety improvements

**Medium-term (2-5 years):**
- Real-time mechanistic explanations during inference
- Cross-model agonist transfer and meta-analysis
- Integration with model editing techniques (RANK-ONE, MEMIT)

**Long-term (5+ years):**
- Mechanistic understanding deep enough for provable correctness
- Fully interpretable models designed around mechanistic primitives
- Mechanistic circuit repository (analogous to GitHub for circuits)

### xAI Community Connections

- **Aligned with:** Anthropic's interpretability research direction; Mech Interp conferences
- **Complements:** SHAP and LIME communities by providing grounded explanations
- **Influences:** Safety alignment research; fairness and bias detection communities
- **Extends:** Work on causal interpretability and counterfactual explanations

## Related Papers to Read Next

1. **"Automated Interpretability: Feature Discovery in LLMs"** (2605.01555) - Automates feature discovery; complements agonist identification
2. **"Patch-Effect Graph Kernels for LLM Interpretability"** (2605.06480) - Alternative approach to analyzing activation patching data
3. **"Causally Grounded Mechanistic Interpretability for LLMs"** (2603.09988) - Bridges circuits and natural language explanations
4. **"Sparse Autoencoders for LLM Mechanistic Interpretability"** - Foundation for feature discovery
5. **"The Scaling Laws of Mechanistic Interpretability"** - How circuit complexity scales with model size

---

**Document Status:** Comprehensive research documentation  
**Last Updated:** May 10, 2026  
**Accuracy Note:** Based on publicly available research materials and search results; for complete details see official arXiv paper
