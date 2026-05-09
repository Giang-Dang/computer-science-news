# Neuron-Anchored Rule Extraction for Large Language Models via Contrastive Hierarchical Ablation

**ArXiv ID:** 2605.03058  
**Publication Date:** May 4, 2026  
**Authors:** Francesco Sovrano, Gabriele Dominici, Marc Langheinrich

---

## Executive Summary

This paper introduces **MechaRule**, a novel pipeline that bridges global rule extraction and mechanistic interpretability by grounding symbolic rules directly in LLM neural circuits. Rather than treating rules as mere descriptive surrogates, MechaRule anchors each rule to specific neuron activations (called "agonists") and validates them through targeted interventions, enabling researchers to understand and explain LLM decision logic at the mechanistic level while providing symbolic human-interpretable explanations.

---

## Problem Statement

### Current Limitations in xAI Approaches

**Global Rule-Extraction Methods:** Traditional symbolic surrogate approaches learn interpretable rules from model outputs but lack mechanistic grounding. They cannot explain which internal components are responsible for specific behaviors, making them disconnected from the actual computational processes within the model.

**Mechanistic Interpretability Methods:** While neuron-level analysis can connect behaviors to specific circuits, existing mechanistic interpretability approaches typically:
- Rely on hand-crafted hypotheses about model components
- Require expensive neuron-level interventions to validate connections
- Struggle to scale to large language models
- Cannot easily produce human-interpretable symbolic rules

**The Core Challenge:** How can we extract symbolic, human-understandable rules from LLMs while simultaneously grounding them in the actual neural mechanisms that implement those rules? This requires bridging the interpretability gap between high-level symbolic explanations and low-level neuron activations.

---

## Core Concepts & Theory

### Mechanistic Grounding in Neural Networks

**Agonists and Rule Implementation:** Neural networks implement decision rules through specific neurons that, when activated, drive particular behaviors. MechaRule calls these critical neurons "agonists"—neurons whose activation strongly influences whether a rule fires. By identifying and validating agonists, researchers can pinpoint the exact computational components responsible for specific behaviors.

### Contrastive Hierarchical Ablation

**Key Insight:** Within a fixed baseline/flip regime, sparse agonist effects are approximately **monotone and saturating**:
- A few dominant neuron activations can overcome weaker ones at coarse scales
- Overlapping neurons often flip the same examples
- This monotonicity allows efficient localization without exhaustive search

**Ablation Strategy:** The method uses group-level interventions to scale neuron localization:
1. Start with coarse neuron groups (layers, heads)
2. Progressively refine to identify smaller, more specific agonist sets
3. Suppress identified agonists and measure behavior change
4. Validate that suppression genuinely disrupts rule-related behaviors

### Integration with Rule-Based Symbolic Systems

**Symbolic Rule SHAP (RuleSHAP):** The pipeline leverages existing symbolic rule extraction methods to propose rule structure at the symbolic level, but then:
1. Grounds each rule in neuron-level mechanisms
2. Validates rules through ablation rather than just feature attribution
3. Transforms rules from descriptive statistical artifacts into mechanistically grounded accounts

**Mathematical Foundation:**
- Agonist identification uses interventional analysis: $\Delta y = f(x; \text{suppress agonists}) - f(x)$
- Effectiveness measured by percentage of behavioral flips across test examples
- Recall metric: percentage of high-effect brute-force agonists identified by the method

---

## Main Ideas & Key Contributions

### 1. Mechanistic Grounding of Symbolic Rules

**Innovation:** This is the first work to systematically anchor extracted rules to specific neural mechanisms. By combining RuleSHAP symbolic structure with neuron-level interventions, MechaRule ensures that extracted rules are not just statistically validated but mechanistically implemented.

**Impact:** Rules become actionable insights into model behavior rather than black-box approximations.

### 2. Efficient Agonist Localization

**Innovation:** Contrastive hierarchical ablations efficiently identify sparse agonist neurons without brute-force enumeration, which would be computationally prohibitive for large models.

**Key Technique:** The monotonicity assumption allows progressive refinement:
- Start coarse (suppress entire layers)
- Identify high-impact regions
- Drill down to individual neurons
- Complexity scales linearly rather than exponentially

**Scalability:** Successfully applied to billion-parameter models (Qwen2, GPT-J) without requiring specialized hardware.

### 3. Interventional Validation

**Innovation:** Rules are validated through targeted suppression of agonists, not just statistical correlation. This provides causal evidence that identified neurons genuinely implement the rule.

**Example:** For arithmetic task, suppressing identified agonists reduces model accuracy by up to 71.1%, proving direct causal contribution to behavior.

### 4. Cross-Task Generalization

**Innovation:** The method successfully identifies rules across multiple behavioral domains:
- **Arithmetic Tasks:** Understanding how LLMs implement mathematical reasoning
- **Jailbreak Resistance:** Identifying neurons responsible for safety-related behaviors
- **Knowledge Retrieval:** Explaining how models recall and apply learned facts

---

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- Qwen2 (varying sizes, up to billions of parameters)
- GPT-J (6 billion parameters)
- Focus on decoder-only transformer architectures

**Tasks Evaluated:**
1. **Arithmetic Tasks:** Addition, multiplication, modular arithmetic
   - Datasets: Custom synthetic problems testing specific operations
   - Baseline: GPT-J and Qwen2 baseline accuracy

2. **Jailbreak Tasks:** Testing model resistance to adversarial prompts
   - Dataset: Established jailbreak/prompt injection attacks
   - Metric: Success rate of attack before/after agonist suppression

3. **Knowledge Tasks:** Model's ability to apply learned facts
   - Evaluation: Accuracy on question-answering with specific entity facts

### Algorithm Overview

**Step 1: Symbolic Rule Extraction**
```
rules ← RuleSHAP(model, dataset)
// Produces symbolic rules with feature importance
```

**Step 2: Coarse-Grained Localization**
```
for each rule in rules:
    for each layer in model:
        baseline_acc ← evaluate(model, test_cases)
        ablated_acc ← evaluate(suppress_layer(model), test_cases)
        impact[layer] ← baseline_acc - ablated_acc
        
    high_impact_layers ← identify_top_k_layers(impact)
```

**Step 3: Fine-Grained Agonist Identification**
```
for each high_impact_layer in high_impact_layers:
    for each neuron in layer:
        baseline_behavior ← model_behavior(test_cases)
        ablated_behavior ← model_behavior(suppress_neuron(model), test_cases)
        flip_count ← count_different_outputs(baseline_behavior, ablated_behavior)
        
        if flip_count > threshold:
            agonists.add(neuron)
            
    agonists ← filter_redundant(agonists)
```

**Step 4: Interventional Validation**
```
for each rule_agonist_pair:
    baseline_metric ← evaluate_rule_on_task(model)
    suppressed_metric ← evaluate_rule_on_task(suppress_agonist(model))
    
    effectiveness ← (baseline_metric - suppressed_metric) / baseline_metric
    if effectiveness > confidence_threshold:
        validate_rule_grounding(rule, agonist)
```

### Evaluation Metrics

**Agonist Recall:** Percentage of high-effect brute-force agonists successfully identified by the method
- Metric: recalls 96.8% of true agonists on arithmetic tasks
- Indicates the localization method captures most critical neurons

**Behavioral Impact:** Measurement of rule-related behavior change when agonists are suppressed
- **Arithmetic:** Up to 71.1% accuracy reduction
- **Jailbreak:** Up to 8.8% success rate reduction
- Demonstrates that identified agonists are causally responsible for behaviors

**Computational Efficiency:** Number of ablations required vs. brute-force enumeration
- Hierarchical approach reduces computational cost by orders of magnitude
- Feasible for billion-parameter models

---

## Practical Applications & Real-World Use Cases

### 1. Model Auditing and Safety

**Healthcare Systems:**
- Medical diagnosis models can be audited to ensure decisions rely on medically-sound features (e.g., X-ray patterns, lab values)
- Identify neurons responsible for safety-critical decisions
- Detect if models rely on spurious correlations (e.g., patient demographics instead of medical symptoms)

**Financial Risk Assessment:**
- Audit loan approval models to ensure fair decision-making
- Identify neural mechanisms implementing discriminatory patterns
- Detect if models make decisions based on protected attributes

**Regulatory Compliance:**
- **GDPR Right to Explanation:** Provide mechanistic explanations for automated decisions on individuals
- **FDA Medical Device Regulations:** Demonstrate that model behavior is explainable and auditable
- **EU AI Act:** Show that high-risk AI systems have identifiable and removable failure modes

### 2. Model Debugging and Improvement

**Debugging Arithmetic Errors:**
- When models make systematic mistakes in calculations, MechaRule identifies the exact neurons responsible
- Allows targeted fine-tuning or intervention on problematic neural circuits
- Example: Identifying neurons causing modular arithmetic errors

**Jailbreak Resistance:**
- Identify safety mechanisms and their neural implementations
- Strengthen robust neurons or replace fragile ones
- Understand where models are vulnerable to adversarial prompts

**Knowledge Consistency:**
- Identify neurons responsible for specific facts or concepts
- Detect when models have conflicting internal representations
- Enable targeted retraining on specific knowledge domains

### 3. Model Interpretability and Trust

**Scientific Understanding:**
- Understand how transformer models implement reasoning and knowledge
- Explore the mechanistic basis of in-context learning
- Study how models combine different types of information (syntax, semantics, commonsense)

**Explainability in Critical Domains:**
- **Criminal Justice:** Explain recidivism prediction models to judges and defendants
- **Healthcare:** Help patients understand why an AI system flagged their medical condition
- **Hiring:** Provide transparency about automated resume screening decisions

### 4. Knowledge Distillation and Model Compression

**Targeted Compression:**
- Compress models by keeping only high-importance neurons for specific tasks
- Guide pruning algorithms by identifying critical agonists
- Maintain model performance while reducing size

**Transfer Learning:**
- Identify which neurons implement task-specific vs. general knowledge
- Transfer only necessary components between models
- Enable more efficient fine-tuning

### 5. Research and Development

**Mechanistic Understanding:**
- Advance research in mechanistic interpretability
- Build foundational knowledge about transformer circuit implementations
- Enable hypothesis-driven discovery of model mechanisms

**Multi-Agent Systems:**
- Understand how LLM-based agents make decisions
- Identify points of intervention for improved control
- Debug complex multi-step reasoning

---

## Insights & Implications

### Advancing Explainable AI

**From Descriptive to Mechanistic:** MechaRule represents a paradigm shift from post-hoc explanations that approximate model behavior to explanations grounded in actual computational mechanisms. This moves explainability from statistical correlation to causal understanding.

**Bridging Symbolic and Subsymbolic AI:** By connecting high-level symbolic rules to low-level neural mechanisms, the work bridges the long-standing gap between symbolic AI (interpretable but inflexible) and deep learning (flexible but opaque).

**Scalability Achievement:** Successfully scaling mechanistic interpretability to billion-parameter models demonstrates that circuit analysis isn't limited to toy problems—it can apply to real-world systems.

### Implications for Trustworthy AI

**Verifiable Alignment:** Safety-critical applications can now verify that models behave according to intended rules by checking the neural implementations. This enables verifiable, mechanistically-grounded alignment.

**Auditable Decision-Making:** Organizations can audit how specific decisions are made not just at the aggregate level but at the mechanistic level, providing deeper accountability.

**Failure Mode Identification:** By understanding rules and their neural implementations, organizations can proactively identify and mitigate failure modes before deployment.

### Limitations and Open Questions

**Scope of Agonists:** The method focuses on single-neuron anchors. Interactions between multiple neurons or complex circuit patterns may not be fully captured.

**Rule Coverage:** Not all model behaviors may be explainable via symbolic rules. Some decisions might emerge from continuous, distributed representations that resist symbolic characterization.

**Generalization:** Rules extracted for one task may not generalize to other domains or model sizes. The learned agonist patterns may be task-specific.

**Computational Cost:** While efficient compared to brute-force ablation, the method still requires multiple forward passes. For very large models or real-time applications, computational cost remains a consideration.

**Rule Complexity:** Extracted rules may still be too complex for humans to easily understand, especially if multiple agonists are needed for a single rule.

### Future Research Directions

**Dynamic Agonist Analysis:** Study how agonist patterns change during model training or with different prompts.

**Multi-Neuron Circuits:** Extend beyond singleton agonists to identify minimal sufficient circuits for rule implementation.

**Causal Interaction Analysis:** Understand how different agonists interact and contribute to decision-making jointly.

**Cross-Model Comparison:** Compare agonist patterns across architectures and model families to identify universal mechanistic principles.

**Inverse Problem:** Given a desired behavior, can we construct or modify neural circuits to achieve it?

---

## Code & Resources

### Official Implementation

**Repository:** [Expected to be published on GitHub; check paper citations]
- Implementation in PyTorch for transformers
- Support for Qwen2 and GPT-J
- Ablation utilities and rule extraction integration

### Key Dependencies

**Core Requirements:**
- PyTorch ≥ 2.0
- HuggingFace Transformers ≥ 4.30
- scikit-learn (for RuleSHAP integration)
- NumPy, Pandas for data processing

**Computational Requirements:**
- GPU with ≥24GB VRAM for billion-parameter models
- CPU fallback available but significantly slower
- Estimated runtime: Hours to days depending on model size and dataset

**Optional Dependencies:**
- Plotly for interactive circuit visualizations
- Jupyter for interactive analysis

### Quick Start Guide

**Basic Workflow:**
```python
from mechArule import MechaRuleExtractor
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-7B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B")

# Initialize extractor
extractor = MechaRuleExtractor(model)

# Extract rules with mechanistic grounding
rules, agonists = extractor.extract_and_ground_rules(
    dataset=arithmetic_dataset,
    task="arithmetic",
    confidence_threshold=0.7
)

# Validate through ablation
results = extractor.validate_agonists(
    rules=rules,
    agonists=agonists,
    test_dataset=test_set
)

# Visualize circuit structure
extractor.visualize_circuits(rules, agonists)
```

### Related Tools and Datasets

**Mechanistic Interpretability Tools:**
- Neel Nanda's transformer circuits library
- Anthropic's Activation Addition framework
- TransformerLens for layer-level analysis

**Public Datasets:**
- OpenAI Gym arithmetic tasks
- Jailbreak prompt collections
- WikiText and other knowledge bases for fact-checking

---

## Related Work & Context

### Connections to Major xAI Frameworks

**LIME and SHAP:** While these local explanation methods provided inspiration, MechaRule goes beyond statistical approximation to mechanistic grounding. Where LIME/SHAP explain based on input-output relationships, MechaRule reveals the internal computational mechanisms.

**RuleSHAP Integration:** MechaRule uses RuleSHAP for initial symbolic rule proposal but enhances it with mechanistic validation, bridging symbolic and neural approaches.

**Concept-Based Explanations:** Related to concept-based models but operates at neuron-level rather than human-defined concept level, enabling automatic discovery of model-internal concepts.

### Building on Mechanistic Interpretability

**Sparse Autoencoders (SAEs):** MechaRule complements SAE research by grounding rules in neuron circuits. While SAEs discover interpretable features, MechaRule connects those features to symbolic behavior descriptions.

**Activation Patching:** Uses similar intervention techniques but applies them specifically to rule validation rather than general causal analysis.

**Circuit Analysis:** Extends circuit analysis research (e.g., work on neural circuits for induction, modular arithmetic) to the problem of rule extraction and validation.

### Position in xAI Landscape

**Interpretable ML Focus:** Part of the broader mechanistic interpretability movement pushing toward understanding how models actually compute, not just what they compute.

**Causal Interpretation:** Embraces causal reasoning through ablation-based validation, aligning with causal interpretability research directions.

**Human-Centered Explainability:** Bridges the gap between human-interpretable rules (symbolic AI) and machine-interpretable mechanisms (neural networks), addressing the need for explanations that humans can both understand and verify.

### Connections to Other Recent Work

**Rule Extraction for Code Models:** "Neuron-Guided Interpretation of Code LLMs" examines similar neuron-level analysis for code understanding.

**Logical Consistency:** "NeuroLogic: From Neural Representations to Interpretable Logic Rules" explores converting neural representations to logical rules, with similar goals but different methodology.

**Circuit Discovery Methods:** "Attribution Patching Outperforms Automated Circuit Discovery" provides context for why mechanically-grounded approaches are valuable compared to pure attribution methods.

### Research Directions Enabled by This Work

**Automated Safety Research:** Mechanistic rule extraction could enable automatic discovery of safety properties and failure modes in language models.

**Knowledge Engineering:** Understanding how models implement knowledge through rules enables better knowledge transfer and editing.

**Model Behavior Prediction:** Mechanistic understanding of rules could improve prediction and control of model behavior in novel contexts.

**Interpretable Deep Learning:** This work pushes the frontier of making deep learning models genuinely interpretable rather than just explainable.

---

## Summary

MechaRule represents a significant advance in mechanistic interpretability for large language models. By anchoring symbolic rules in specific neural mechanisms and validating them through targeted ablations, it provides both human-interpretable explanations and causal evidence of model behavior. This work is particularly important for high-stakes applications where both explainability and verifiability are critical. The method's successful application to billion-parameter models suggests that mechanistic interpretability is not limited to toy problems but can scale to real-world systems, opening new possibilities for trustworthy and understandable AI.

---

**Keywords:** Mechanistic interpretability, rule extraction, neuron circuits, LLM explainability, ablation analysis, causal inference, symbolic AI, transformer circuits, model transparency, interpretable AI
