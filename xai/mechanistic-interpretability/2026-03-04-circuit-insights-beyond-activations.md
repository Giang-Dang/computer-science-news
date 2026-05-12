# Circuit Insights: Towards Interpretability Beyond Activations

## Executive Summary

This paper introduces WeightLens and CircuitLens, two complementary mechanistic interpretability methods that advance circuit discovery in neural networks by going beyond activation-based analysis. By interpreting features directly from learned weights and capturing feature interactions at the circuit level, this work addresses critical limitations in existing interpretability approaches, enabling more robust and scalable understanding of neural network computations.

## Paper Metadata

- **Title:** Circuit Insights: Towards Interpretability Beyond Activations
- **Authors:** Elena Golimblevskaia, Aakriti Jain, Bruno Puri, Ammar Ibrahim, Wojciech Samek, Sebastian Lapuschkin
- **ArXiv ID:** [2510.14936](https://arxiv.org/abs/2510.14936)
- **Submission Date:** October 2025 (Latest version: March 4, 2026)
- **Venue:** ICLR 2026
- **Keywords:** Mechanistic Interpretability, Circuit Discovery, Neural Network Transparency, Feature Attribution, Transformer Interpretability

## Problem Statement

Mechanistic interpretability seeks to reverse-engineer neural networks into human-understandable algorithms and computational graphs. However, existing approaches face significant limitations:

1. **Manual Inspection Bottleneck:** Current circuit discovery methods rely heavily on manual inspection and remain limited to toy tasks and simple models.

2. **Activation-Only Limitations:** Automated interpretability approaches analyze isolated features and their activations but often miss critical feature interactions between components. These approaches struggle to capture how features interact with one another in generating model outputs.

3. **Dataset and LLM Dependency:** Existing methods depend strongly on external large language models for explanation generation and require high-quality datasets. This creates computational overhead and introduces potential biases from the explainer models.

4. **Scalability Issues:** Traditional circuit discovery via patching is computationally inefficient, limiting applicability to large-scale models and complex architectures.

5. **Context-Independence Problem:** Activation-based methods are weak at capturing context-dependent feature interactions where the interpretation depends on specific input patterns.

These limitations prevent mechanistic interpretability from scaling to large modern language models and transformer architectures that power contemporary AI systems.

## Core Concepts & Theory

### Mechanistic Interpretability Foundations

**Definition:** Mechanistic interpretability is the process of studying the inner computations of neural networks and translating them into human-understandable algorithms. It aims to create interpretable bases—features and operations that have clear mathematical and semantic meaning.

**Key Principle - Decomposition:** Neural networks can be decomposed into interacting computational components:
- **Neurons/Features:** Individual units that respond to specific concepts or patterns
- **Circuits:** Networks of interconnected components that perform specific computational tasks
- **Operations:** Matrix multiplications, attention mechanisms, and nonlinearities that transform information

### Circuit Analysis Paradigm

A **circuit** in neural network interpretability refers to a subset of model components (neurons, attention heads, MLP layers) that together implement a coherent computational function. Circuit analysis maps which components contribute to which behaviors.

**Traditional Activation Patching Approach:**
```
Original Output = Model Output on Natural Input
Ablated Output = Model Output with Component Set to Zero/Mean
Attribution = Original Output - Ablated Output
```

This approach requires:
- One forward pass for baseline computation
- One forward pass for each component ablation
- Computational cost: O(n) where n is number of components

### Feature Interpretation from Weights

Traditional approaches interpret features by examining their activations on a dataset. However, learned weight structures themselves encode significant information:

**Weight Structure Insights:**
- Weights capture learned feature representations independent of any particular dataset
- Weight-based interpretation eliminates dataset bias in explanations
- Transcoders (learned projections between model layers) can reveal features directly from weight structure

### Feature Interactions and Contextuality

Not all feature activations can be explained independently:
- **Context-Independent Features:** Activations determined solely by input features (e.g., "this token is a name")
- **Context-Dependent Features:** Activations depend on feature interactions (e.g., "this name is the subject of the sentence")

Circuit analysis must capture both types of dependencies.

## Main Ideas & Key Contributions

### 1. WeightLens: Weight-Based Feature Interpretation

**Core Innovation:** Interpret features directly from learned weight structures rather than requiring dataset-specific activation analysis.

**Technical Approach:**
- Analyze the weight matrices of transcoders (learned projections between model layers)
- Use weight structure to identify feature semantics without requiring an explainer LLM
- Project weights into feature space to discover what each neuron/feature represents

**Key Advantages:**
- **Dataset Independence:** No need for large datasets to understand features
- **LLM-Free:** Eliminates dependency on external language models for feature explanations
- **Efficiency:** Requires only weight matrix analysis, no dataset forward passes
- **Quality:** Matches or exceeds performance of activation-based methods on context-independent features

**How It Works:**
```
Given: Weight matrix W of a transcoder
Process:
  1. Decompose W using singular value decomposition or other structural analysis
  2. Project discovered weight patterns into semantic space
  3. Identify which weight structures correspond to interpretable features
  4. Match weight structure to known concepts or behaviors
Result: Feature interpretations without dataset bias
```

**Evaluation Results:**
- Successfully interprets context-independent features
- Reduces computational overhead compared to activation-based methods
- Produces interpretations robust to dataset variation

### 2. CircuitLens: Capturing Feature Interactions

**Core Innovation:** Extend mechanistic interpretability beyond isolated features to capture how feature activations arise from interactions between model components.

**Technical Approach:**
- Analyze how upstream features propagate through intermediate layers to downstream activations
- Map component-to-component influence patterns (circuits)
- Identify which input patterns trigger specific feature activations
- Trace which output tokens are influenced by specific features

**Key Contributions:**
- **Beyond Activation Values:** Not just which features activate, but WHY they activate
- **Interaction Capture:** Reveals dependencies between features and components
- **Context Sensitivity:** Identifies input-specific patterns that determine feature behavior
- **Circuit Mapping:** Creates explicit computational graphs showing feature flow

**How It Works:**
```
Given: Feature activations and component weights
Process:
  1. For each feature, identify which components drive its activation
  2. Trace backward to find input patterns triggering the feature
  3. Trace forward to find downstream tokens/decisions influenced by the feature
  4. Map the complete circuit path from input → feature → output
  5. Validate circuit by intervention (patching/ablation)
Result: Complete circuit showing feature interactions
```

**CircuitLens Components:**
1. **Input Pattern Detection:** Which input tokens/patterns maximize specific feature activations
2. **Component Attribution:** Which model layers/heads contribute to feature activation
3. **Output Tracing:** Which downstream tokens depend on the feature
4. **Circuit Validation:** Patching experiments to verify circuit importance

### 3. Complementary Nature

The two methods work together:
- **WeightLens** provides semantically meaningful feature interpretations without dataset bias
- **CircuitLens** captures when and why those features activate in context
- Combined: Complete understanding of feature identity and feature behavior

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- Large language models (transformers-based)
- Vision transformers (potentially, for generalization)
- Multiple model scales and architectures

**Datasets:**
- Standard NLP benchmarks for language models
- Diverse input distributions to test context-dependent feature behavior

**Baseline Methods:**
- Activation patching (traditional circuit discovery)
- ACDC (Automatic Circuit DisCovery)
- Sparse autoencoders (SAEs) with feature interpretation
- Previous transcoder-based approaches

### Evaluation Metrics

**For WeightLens (Feature Interpretation Quality):**
- **Semantic Coherence:** Do interpreted features correspond to meaningful concepts?
- **Human Evaluation:** Crowdsourced assessment of feature interpretability
- **Downstream Task Performance:** Can interpreted features predict model behavior?
- **Faithfulness:** How well does weight-based interpretation align with activation-based interpretation?

**For CircuitLens (Circuit Discovery Quality):**
- **Circuit Completeness:** What percentage of relevant components are identified?
- **Precision:** How many identified components are truly relevant?
- **Intervention Validation:** When components are patched, do outcomes match predictions?
- **Efficiency:** Computational cost vs. alternative circuit discovery methods

**Combined Evaluation:**
- **Robustness:** Stability of interpretations across different inputs and model states
- **Scalability:** Performance on large models with many components
- **Generalization:** Can circuits discovered in one task apply to related tasks?

### Key Results

**WeightLens Performance:**
- Achieves comparable or better feature interpretability than activation-based methods
- Significantly reduces computational overhead
- Produces stable interpretations independent of dataset variations

**CircuitLens Findings:**
- Successfully captures feature interactions missed by activation-only approaches
- Identifies context-dependent feature activations
- Produces interpretable circuits with high intervention validation rates

**Scalability:**
- Methods scale to large language models
- Computational efficiency enables analysis of modern transformer architectures
- Can handle models with millions of parameters

### Implementation Considerations

**Transcoders:**
The methods leverage transcoders—learned projections between adjacent model layers that decompose layer activations into interpretable feature bases.

**Circuit Representation:**
Circuits are represented as directed graphs:
- **Nodes:** Model components (attention heads, MLP neurons, features)
- **Edges:** Information flow showing dependencies and interactions
- **Edge Weights:** Attribution scores indicating influence strength

**Validation:**
- Intervention experiments (ablation, patching) verify discovered circuits
- Consistency checks across multiple inputs and model conditions

## Practical Applications & Real-World Use Cases

### Healthcare & Medical AI
- **Interpretable Diagnosis:** Understand which features in medical imaging models correspond to disease indicators
- **Clinical Trust:** Enable doctors to validate model reasoning matches clinical knowledge
- **Regulatory Compliance:** Demonstrate explainability for FDA approval of AI medical devices
- **Example:** Discovering that specific attention patterns recognize tumor boundaries in pathology images

### Financial Services & Risk Management
- **Credit Decisions:** Explain which factors (income, credit history, payment patterns) influence lending decisions
- **Fraud Detection:** Identify which behavioral features trigger fraud alerts
- **Regulatory Reporting:** Demonstrate compliance with fair lending regulations
- **Risk Assessment:** Show that models correctly identify relevant risk factors

### Legal & Compliance Systems
- **Evidence Interpretation:** Explain how contracts or documents are classified
- **Bias Detection:** Identify and eliminate discriminatory features in legal decision-making
- **Regulatory Compliance:** Meet explainability requirements under AI Act and similar regulations
- **Example:** Verifying that contract risk assessment doesn't discriminate by party nationality

### Autonomous Systems & Safety-Critical Applications
- **Autonomous Vehicles:** Understand what features influence driving decisions
- **Robot Control:** Verify that learned behaviors correspond to safety-relevant features
- **Safety Validation:** Ensure models respond appropriately to dangerous scenarios
- **Incident Analysis:** Debug failures by understanding model decision-making

### Content Moderation & AI Safety
- **Policy Enforcement:** Understand what makes models flag content as violating policies
- **Bias Mitigation:** Identify problematic features that lead to unfair moderation decisions
- **Appeal Process:** Explain moderation decisions to users with evidence
- **Adversarial Robustness:** Identify exploitable features and defend against them

### Model Debugging & Development
- **Architecture Selection:** Compare interpretability across different architectures
- **Feature Quality:** Verify that learned features correspond to task-relevant concepts
- **Error Analysis:** Understand systematic failures by examining relevant circuits
- **Training Monitoring:** Track whether models learn interpretable features during training

### Regulatory & Standards Compliance

**GDPR Right to Explanation:**
- Must explain automated decisions affecting individuals
- CircuitLens enables showing which factors influenced decisions
- Demonstrates algorithmic fairness and non-discrimination

**AI Act Compliance (EU):**
- High-risk AI systems require transparency about decision-making
- Mechanistic interpretability provides technical foundation for compliance
- Enables continuous monitoring for bias and failure modes

**FDA Requirements for Medical Devices:**
- Must demonstrate that AI systems work as intended
- Circuit discovery shows whether learned features match clinical reasoning
- Supports regulatory approval and post-market surveillance

## Insights & Implications

### Advances in State-of-the-Art

1. **Beyond Activation Analysis:** The mechanistic interpretability field has historically focused on analyzing activations (how much features fire). Circuit Insights goes deeper to understand *why* features activate (what causes activation) and *what consequences* activations have (downstream effects).

2. **Scalability Breakthrough:** By avoiding activation patching's O(n) cost for each component and leveraging weight structure, these methods enable circuit analysis at scale for modern large language models.

3. **Dataset-Independent Understanding:** WeightLens demonstrates that feature semantics can be discovered independently of specific datasets, providing more fundamental insights into learned representations.

4. **Automated Circuit Discovery:** Reduces reliance on manual inspection and significantly increases the pace of mechanistic interpretability research.

### Broader Implications for Trustworthy AI

**Understanding → Trust:** As we can explain what features drive model decisions and why those features activate, users and regulators gain confidence in AI system behavior.

**Debugging → Safety:** Circuit knowledge enables targeted improvements—fixing specific problematic features rather than retraining entire models.

**Robustness → Reliability:** Understanding circuits reveals potential failure modes and adversarial vulnerabilities before deployment.

**Alignment → Values:** For large language models, discovering whether circuits implement intended behaviors (honesty, harmlessness, helpfulness) supports AI alignment efforts.

### Limitations & Open Questions

1. **Semantic Correspondence:** While weights encode features, the mapping to human-interpretable concepts isn't always straightforward. Some discovered features may lack clear semantic meaning.

2. **Scale Limits:** Even with improved efficiency, analyzing all circuits in billion-parameter models remains computationally intensive.

3. **Interaction Complexity:** Real neural networks have extremely complex interactions. Simplified circuit representations may miss important nuances.

4. **Generalization:** Circuits discovered in one context may not transfer to different domains or tasks.

5. **Validation Gap:** While patching experiments validate discovered circuits, this still requires interventions that change model behavior. Non-invasive validation methods would be valuable.

6. **Interpretability Gap:** Even identified circuits may not be fully interpretable to non-experts. Further work is needed on effective communication of circuit findings.

### Future Research Directions

1. **Hierarchical Circuit Analysis:** Understanding how smaller circuits compose into larger computational functions.

2. **Cross-Model Circuits:** Discovering conserved circuits across different model architectures and scales (understanding universal computations).

3. **Temporal Dynamics:** How circuits change during training and how stable learned representations are.

4. **Multi-Modal Circuits:** Extending circuit discovery to vision-language models and multi-modal systems.

5. **Interactive Interpretability:** Tools that let users explore circuits and make hypotheses about model behavior.

6. **Inverse Interpretability:** Designing circuits intentionally to implement specific behaviors (moving from understanding to engineering).

7. **Circuit Optimization:** Using discovered circuits to improve models (removing redundancy, enhancing robustness).

## Code & Resources

### Official Implementations

**Circuit Insights Repository:**
- **GitHub:** [Transcoder Circuits](https://github.com/jacobdunefsky/transcoder_circuits/)
- **Status:** Active development
- **Components:** WeightLens and CircuitLens implementations
- **License:** Open source

### Related Frameworks & Tools

**Sparse Autoencoder Framework (For Feature Discovery):**
- **GitHub:** [Language-Model-SAEs](https://github.com/OpenMOSS/Language-Model-SAEs)
- **Purpose:** Train, analyze, and visualize sparse autoencoders and transcoders
- **Features:** Cross-layer analysis, SAE training, feature visualization

**Resource Collections:**
- **Awesome Sparse Autoencoders:** [GitHub Link](https://github.com/chrisliu298/awesome-sparse-autoencoders)
- **Mechanistic Interpretability Resources:** [Transformer Circuits Thread](https://transformer-circuits.pub/)

### Technical Requirements

**Computational Requirements:**
- GPU Memory: 24GB+ for analyzing large language models (A100/H100 recommended)
- Storage: 50GB+ for model weights and feature databases
- Training Time: Varies by model size (hours to days for full analysis)

**Dependencies:**
- PyTorch 2.0+
- NumPy, SciPy for matrix operations
- Transformer libraries (HuggingFace transformers)
- Custom circuit analysis libraries

### Quick Start Guide

1. **Install Dependencies:**
   ```bash
   pip install torch transformers numpy scipy
   git clone https://github.com/jacobdunefsky/transcoder_circuits
   cd transcoder_circuits
   pip install -e .
   ```

2. **Load a Model with Transcoders:**
   ```python
   from circuit_insights import load_model_with_transcoders
   model = load_model_with_transcoders("gpt2")  # or other models
   ```

3. **Run WeightLens Analysis:**
   ```python
   from circuit_insights import WeightLens
   weight_lens = WeightLens(model)
   features = weight_lens.interpret_features()
   ```

4. **Run CircuitLens Analysis:**
   ```python
   from circuit_insights import CircuitLens
   circuit_lens = CircuitLens(model)
   circuits = circuit_lens.discover_circuits(input_text="Example")
   ```

5. **Visualize Results:**
   ```python
   circuit_lens.visualize_circuit(circuits[0])
   ```

### Interactive Resources

**Mechanistic Interpretability Essay:**
- [Transformer Circuits: Interpretability in Practice](https://www.transformer-circuits.pub/2022/mech-interp-essay)
- Overview of mechanistic interpretability research agenda

**Circuit Analysis Resources:**
- [Automated Circuit Discovery Methods Review](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)
- Comparison of circuit discovery techniques

**Paper Visualizations:**
- ICLR 2026 poster with interactive examples
- OpenReview forum discussions with supplementary materials

## Related Work & Context

### Foundational Mechanistic Interpretability Work

**Pioneering Work:**
- **"Mechanistic Interpretability, Variables, and the Importance of Interpretable Bases"** (Transformer Circuits Team): Established the theoretical foundation that neural networks should be understood in interpretable bases rather than raw activations.
- **"A Mathematical Framework for Transformer Circuits"** (Transformer Circuits Team): Developed formal mathematical framework for analyzing circuits.

### Recent Circuit Discovery Methods

**Automated Circuit Discovery:**
- **ACDC** (Conmy et al.): Iterative localization of model components important for specific behaviors
- **Edge Attribution Patching (EAP)**: More efficient attribution computation for circuit discovery
- **Circuit-based Transformers (CT)**: Contextual decomposition for efficient circuit discovery

**Weight-Based Approaches:**
- **Transcoders Find Interpretable LLM Feature Circuits** (Bricken et al., 2406.11944): Foundation work on transcoders for circuit discovery
- **Transcoders Beat Sparse Autoencoders for Interpretability** (Recent work): Showed transcoders outperform SAEs for feature interpretation

### Complementary Interpretability Approaches

**Sparse Autoencoders (SAEs):**
- Discover interpretable features by learning sparse, linear decompositions of activations
- Complementary to circuit analysis—SAEs find features, circuits find connections

**Concept-Based Methods:**
- Interpret models through high-level semantic concepts rather than individual neurons
- Can be combined with circuit analysis for hierarchical understanding

**Causal Interpretability:**
- Use causal inference to understand decision-making
- Similar goals to circuits but different technical approach

### Connection to Broader xAI Movements

**LIME/SHAP Era (Feature Importance):**
- Early local interpretability methods
- Circuit Insights moves beyond feature importance to understand model mechanisms

**Post-hoc Explanation Methods:**
- Attention visualization, gradient-based saliency
- Circuit Insights provides more fundamental mechanistic understanding

**Interpretable ML:**
- Design models that are inherently interpretable
- Circuit Insights works on post-hoc understanding of learned models

**The Mechanistic Interpretability Research Direction:**
Recent progress suggests mechanistic interpretability is becoming practical for real models:
- Scaling from toy models to GPT-2 scale models
- Now moving toward GPT-3.5/GPT-4 scale models
- Becoming critical for AI safety and alignment research

### Open Research Questions in xAI

1. **Compositionality:** How do simple circuits compose into complex behaviors?
2. **Universality:** Are there universal circuits across models and architectures?
3. **Scaling Laws:** How does interpretability difficulty scale with model size?
4. **Semantics:** How to formally define and measure semantic interpretability?
5. **Interaction Effects:** Understanding feature interactions at scale

## Summary

Circuit Insights represents a significant step forward in mechanistic interpretability by combining weight-based feature interpretation (WeightLens) with circuit-level interaction analysis (CircuitLens). By moving beyond activation-only approaches and reducing computational requirements, this work makes mechanistic interpretability more practical and scalable for real-world systems.

The ability to understand neural networks through their learned features and computational circuits has profound implications for AI safety, regulatory compliance, and user trust. As mechanistic interpretability matures from theoretical exercise to practical tool, methods like Circuit Insights will be essential for developing trustworthy, transparent AI systems that stakeholders can understand and rely upon.

The combination of theoretical rigor, practical efficiency, and scalability positions this work as a key contribution to the mechanistic interpretability research direction, with clear relevance to the broader xAI community's goal of creating understandable, trustworthy artificial intelligence systems.
