# Automated Interpretability and Feature Discovery in Language Models with Agents

**Paper:** Automated Interpretability and Feature Discovery in Language Models with Agents

**Authors:** Arnau Marin-Llobet, Javier Ferrando (Harvard University)

**ArXiv ID:** 2605.01555

**Publication Date:** May 2, 2026

**Link:** https://arxiv.org/abs/2605.01555

---

## Executive Summary

This paper introduces an autonomous multiagent framework that automates the discovery and interpretation of internal features within large language models (LLMs). By leveraging iterative hypothesis refinement and systematic feature exploration, the framework significantly advances mechanistic interpretability—a critical research direction for understanding "black-box" deep learning systems. This work demonstrates that agent-driven approaches can scale feature interpretation to entire neural networks, addressing a fundamental challenge in trustworthy AI.

---

## Problem Statement

Understanding the internal mechanisms of large language models remains one of the most challenging problems in AI research. Traditional approaches to mechanistic interpretability suffer from several critical limitations:

1. **Manual Feature Discovery:** Identifying interpretable features within LLMs typically requires extensive manual analysis, which doesn't scale beyond small network sections.

2. **Hypothesis Generation Bottleneck:** Current methods rely on researchers manually proposing feature hypotheses, which is both time-consuming and limited by human intuition.

3. **One-Shot Explanations:** Existing approaches like Sparse Autoencoders (SAEs) with autointerp generate single-pass explanations without iterative refinement, potentially missing nuanced feature behaviors.

4. **Polysemanticity and Feature Ambiguity:** Many neurons and activation vectors exhibit polysemantic behavior (responding to multiple, seemingly unrelated concepts), making interpretation difficult and unreliable.

5. **Lack of Systematic Evaluation:** No standardized protocol exists for evaluating interpretation quality across multiple dimensions (accuracy, completeness, generalization).

The paper addresses these gaps by proposing that if humans struggle to scale feature interpretation, perhaps autonomous agents—with their capacity for systematic exploration and iterative reasoning—can tackle this challenge more effectively.

---

## Core Concepts & Theory

### Mechanistic Interpretability Fundamentals

**Mechanistic interpretability** seeks to understand how neural networks perform computations at the algorithmic level—breaking down the "black box" into interpretable components. Unlike post-hoc explanation methods (e.g., attention visualization), mechanistic interpretability aims to identify the actual circuits and mechanisms responsible for model behavior.

Key concepts:

- **Features:** Interpretable dimensions in activation space that encode meaningful information (e.g., "word tokens," "code syntax," "safety concepts")
- **Polysemanticity:** The property where a single neuron or activation responds to multiple unrelated contexts, complicating interpretation
- **Sparse Autoencoders (SAEs):** Neural network components that learn sparse, interpretable representations of dense activations by learning a dictionary of features
- **Feature Attribution:** Identifying which features (or circuits) are responsible for specific model outputs

### Autonomous Agent-Based Interpretation Framework

The paper proposes treating interpretation as an **agentic workflow** rather than a static analysis task. The framework consists of two coupled loops:

#### Loop 1: Explanation Refinement (FeatureExplainer)

A hypothesis-driven agent iteratively refines interpretations:

1. **Hypothesis Proposal:** The agent proposes a primary interpretation and competing alternatives
2. **Controlled Experimentation:** Uses targeted prompt controls to test feature activation patterns
3. **Multi-Metric Evaluation:** Employs a 7-metric battery to rigorously evaluate explanation quality:
   - Consistency (does the explanation hold across contexts?)
   - Clarity (is the interpretation understandable?)
   - Separability (is this feature distinct from others?)
   - Polysemanticity Detection (does the feature respond to multiple concepts?)
   - Causal Validation (does the feature causally influence outputs?)
   - Coverage (what fraction of activations does it explain?)
   - Confidence (how confident is the agent in its explanation?)

4. **Iterative Refinement:** Based on metric feedback, the agent refines its hypothesis and repeats

#### Loop 2: Feature Discovery (FeatureFinder)

A statistical discovery algorithm identifies candidate features:

1. **Prompt Set Generation:** The agent creates diverse prompt sets designed to activate different neural features
2. **Activation Analysis:** Records neuron activations across the entire prompt set
3. **K-Nearest Neighbor Clustering:** Constructs a k-NN graph in activation space to identify densely connected regions (potential features)
4. **Statistical Separability:** Filters candidates based on how well-separated they are in activation space
5. **Semantic Coherence:** Uses linguistic models to verify that candidates form interpretable semantic clusters
6. **Feature Extraction:** Retrieves top candidate features for downstream explanation

### Mathematical Formulation

**Feature Quality Metric:**

The 7-metric evaluation function for a feature candidate f is formulated as:

```
Quality(f) = w₁·Consistency(f) + w₂·Clarity(f) + w₃·Separability(f) 
           + w₄·Polysemanticity(f) + w₅·Causal(f) + w₆·Coverage(f) 
           + w₇·Confidence(f)
```

Where weights (w₁...w₇) are learned from human feedback on feature interpretations.

**Statistical Separability:**

For a feature candidate f with activation distribution A_f, separability is measured as:

```
Separability(f) = min_f' D_KL(A_f || A_f') / E[D_KL(A_f || A_random)]
```

This ensures features are statistically distinct from both other features and random activations.

---

## Main Ideas & Key Contributions

### 1. Agent-Driven Feature Interpretation Workflow

The paper's primary innovation is framing mechanistic interpretability as an **iterative agentic task** rather than a static one-shot process. This enables:

- **Autonomous Hypothesis Refinement:** Agents can propose, test, and refine competing interpretations without human intervention
- **Scale-Up Potential:** Systematic exploration can handle millions of features across entire LLMs
- **Built-in Validation:** Multi-metric evaluation ensures quality at every iteration

### 2. FeatureFinder: Automated Statistical Feature Discovery

The paper introduces an automated algorithm that:

- **Generates Targeted Prompts:** Creates diverse prompt sets to systematically activate different model components
- **Identifies Feature Candidates:** Uses k-NN clustering in activation space to find potential interpretable features
- **Filters by Quality Metrics:** Applies statistical separability and semantic coherence constraints

This removes the manual effort of identifying candidate features, which previously required expert analysis.

### 3. FeatureExplainer: Iterative Interpretation Refinement

The explanation component:

- **Proposes Multi-Hypothesis Explanations:** Generates competing interpretations and lets evaluation metrics determine which is most plausible
- **Tests with Prompt Controls:** Uses targeted prompts to validate features in specific contexts
- **Detects Polysemanticity:** Automatically identifies when features respond to multiple concepts, flagging unreliable interpretations
- **Provides Causal Validation:** Goes beyond correlation to establish causal relationships between features and outputs

### 4. 7-Metric Evaluation Framework

A comprehensive evaluation protocol that measures:

1. **Consistency:** Feature activations align with proposed interpretation across contexts
2. **Clarity:** Interpretations are human-understandable
3. **Separability:** Feature is statistically distinct from other features
4. **Polysemanticity Reduction:** Feature doesn't spuriously respond to unrelated inputs
5. **Causal Impact:** Feature manipulations causally affect model outputs
6. **Coverage:** Feature explains a meaningful fraction of model behavior
7. **Confidence:** The agent's confidence in its interpretation

### 5. Generalization Across Model Families

The framework demonstrates:

- **Generalization to Gemma-2 Family:** Consistent improvements across different model scales and variants
- **Concept Type Coverage:** Works for linguistic, coding, mathematical, and safety-related features
- **Architecture Generalization:** Extends to different transformer architectures and weight-sparse models

### Why This Approach Is Better

Traditional SAE autointerp approaches:
- Generate one-shot explanations without refinement
- Don't systematically validate multiple hypotheses
- Lack polysemanticity detection
- Don't provide causal validation

The agent-driven approach:
- Iteratively refines explanations using feedback
- Systematically compares competing hypotheses
- Explicitly detects and flags problematic polysemantic features
- Provides causal validation through controlled experiments
- Scales to millions of features

---

## Methodology & Implementation

### Experimental Setup

**Model Tested:** Gemma-2 family (multiple sizes)

**Layer Analyzed:** Middle and late-layer activations where interpretable features emerge

**Activation Representation:** 
- Sparse Autoencoders extract features from dense activations
- Feature vectors processed through k-NN clustering

**Baseline Comparisons:**
- One-shot SAE autointerp (previous SOTA)
- Manual feature discovery
- Random feature baselines

### Feature Discovery Process

**Dataset:** Diverse corpus of 1M+ prompts covering:
- General language tasks
- Coding and programming
- Mathematics and logic
- Safety and alignment scenarios
- Domain-specific applications

**Activation Sampling:** 
- Record activations at specified layers for all prompts
- Compute activation statistics (mean, variance, percentiles)
- Build k-NN graph in activation space

**Statistical Filtering:**
- D-KL divergence > threshold for separability
- Semantic coherence score from CLIP/language model > threshold
- Coverage (% of activations explained) > threshold

### Evaluation Metrics & Results

#### Quantitative Results

**Improvement over SAE Autointerp:**
- Consistency: +34% improvement in feature activation alignment
- Polysemanticity Detection: 87% accuracy in identifying multi-concept features
- Causal Validation: 78% of proposed features show causal impact on outputs
- Coverage: Explains 65% of meaningful variance across tested models

**Concept Type Performance:**
- Linguistic Features: 92% human agreement with interpretations
- Coding Features: 88% human agreement
- Mathematical Features: 84% human agreement
- Safety Features: 91% human agreement (critical for alignment research)

**Generalization:**
- Gemma-2-9B: 123 features discovered with >90% quality
- Gemma-2-27B: 156 features discovered with >88% quality
- Weight-sparse models: >85% quality maintained

#### Qualitative Insights

**Example Discovered Features:**

1. **"Natural Language Processing" Feature** (Layer 18)
   - Activates on: NLP tasks, parsing, tokenization discussions
   - Distinguishes from other features with 94% separability
   - Causally influences NLP-related outputs

2. **"Safety Concern Detector" Feature** (Layer 20)
   - Activates on: Safety questions, ethical dilemmas, harmful requests
   - Polysemantic aspects: Also activates on emergency/urgent contexts (detected)
   - 91% human agreement on interpretation

3. **"Code Structure Feature" Feature** (Layer 19)
   - Responds to code syntax, loops, conditionals
   - 8 sub-components identified through iterative refinement
   - Causally impacts code generation quality

### Limitations

1. **Computational Cost:** Iterative agent-based approach is more resource-intensive than one-shot methods
   - Feature discovery: ~24 GPU-hours per model
   - Explanation refinement: ~10 GPU-hours per 100 features

2. **Polysemanticity Handling:** The framework detects polysemantic features but doesn't fully resolve them
   - Flags them for manual investigation
   - Suggests hypothetical splitting strategies

3. **Layer Coverage:** Currently focuses on middle/late layers where features are most interpretable
   - Early layers remain harder to interpret
   - Attention heads partially covered

4. **Semantic Coherence Validation:** Relies on external language models (CLIP) which may have their own biases

---

## Practical Applications & Real-World Use Cases

### 1. AI Safety & Alignment

**Problem:** How can we ensure LLMs behave safely and according to human values?

**Application:** The framework identifies safety-relevant features (e.g., "refusal mechanisms," "fairness detectors," "harm-aversion"). This enables:
- **Behavioral Auditing:** Verify that safety features are working as intended
- **Misbehavior Detection:** Identify when safety features malfunction
- **Intervention Design:** Precisely target features that need adjustment
- **Causal Alignment:** Understand causal pathways leading to unsafe outputs

**Example:** Discovering that a "harmful-content-detector" feature also spuriously activates on legitimate emergency discussions, leading to over-refusal—an interpretable failure mode that can be surgically fixed.

### 2. Medical AI & Healthcare Diagnostics

**Problem:** Regulatory bodies (FDA, EMA) require explainability in clinical AI systems.

**Application:** Applying mechanistic interpretability to medical LLM systems:
- **Feature Validation:** Verify that the model uses clinically meaningful features (e.g., "symptom patterns," "contraindication detection")
- **Trust Assurance:** Provide regulators with mechanistic explanations of diagnostic reasoning
- **Error Analysis:** Identify features responsible for misdiagnosis
- **Regulatory Compliance:** Support FDA/EMA approval processes with interpretability evidence

**Example:** Discovering that a medical diagnostic model uses a feature for "drug interaction warnings" that correlates perfectly with known contraindications, providing strong evidence of reliable clinical reasoning.

### 3. Financial Risk Assessment

**Problem:** Financial institutions need explainable decisions for credit, investment, and compliance.

**Application:** Using mechanistic interpretability on financial LLMs:
- **Risk Factor Identification:** Discover which features predict financial risk
- **Regulatory Reporting:** Provide detailed explanations for algorithmic decisions
- **Fraud Detection:** Identify features that detect suspicious patterns
- **Model Auditing:** Verify compliance with financial regulations (e.g., Dodd-Frank, MiFID II)

**Example:** Identifying that a credit scoring model uses features for "debt-to-income patterns" and "payment history consistency," enabling auditors to validate fair lending practices.

### 4. Legal & Compliance AI

**Problem:** Legal and compliance decisions must be explainable and auditable.

**Application:** Mechanistic interpretability for legal document analysis and compliance checking:
- **Evidence Chain Discovery:** Identify features that trace legal reasoning
- **Contractual Understanding:** Verify that contract analysis features capture key legal concepts
- **Compliance Auditing:** Ensure the model recognizes regulatory requirements
- **Liability Management:** Document the decision-making logic for potential disputes

### 5. Autonomous Systems & Robotics

**Problem:** Autonomous vehicles and robots must be interpretable for safety certification.

**Application:** Understanding decision-making in vision+language models used for autonomous systems:
- **Perception Feature Validation:** Verify that visual features correctly identify objects, pedestrians, etc.
- **Safety Critical Features:** Identify features responsible for emergency responses
- **Failure Mode Analysis:** Understand why the system made dangerous decisions
- **Trust & Certification:** Support safety certifications with mechanistic evidence

---

## Insights & Implications

### Implications for Trustworthy AI

1. **Scalability of Interpretability:** This work demonstrates that mechanistic interpretability can scale beyond toy models. If agents can systematically explore millions of features, transparency becomes feasible for production LLMs.

2. **Automation of Understanding:** The framework shifts interpretability from a manual, labor-intensive process to an automated one. This has profound implications:
   - Makes interpretability economically viable for large-scale deployment
   - Enables continuous monitoring of model behavior
   - Supports rapid iteration on safety improvements

3. **Agentic Approaches to AI Understanding:** The success of autonomous agents in feature discovery suggests that agents themselves might be powerful tools for understanding other agents—an interesting recursive insight.

4. **Validation Through Iteration:** The iterative refinement approach mimics the scientific method, where hypotheses are tested and refined based on evidence. This is a more robust approach than one-shot analysis.

### Advancement of State-of-the-Art

**Previous Bottleneck:** Feature discovery required manual inspection of activation patterns and often relied on researcher intuition.

**New Capability:** Automated discovery of interpretable features scales to entire models with quality metrics ensuring reliability.

**SOTA Improvement:** 
- 34% improvement over SAE autointerp in consistency
- Introduces polysemanticity detection (new capability)
- Provides causal validation (previously limited)
- Handles 10x more features than manual approaches

### Limitations & Open Questions

1. **Computational Efficiency:** The iterative approach is expensive. Future work should explore more efficient hypothesis generation and testing strategies.

2. **Polysemanticity Resolution:** The framework detects polysemanticity but doesn't fully resolve it. Can we decompose polysemantic features into interpretable sub-components?

3. **Causality vs. Correlation:** While causal validation is stronger than correlation, it remains limited by the availability of safe interventions. Can we design safer or more targeted experiments?

4. **Human Alignment:** The 7-metric evaluation is designed for LLM interpretation, but not all metrics equally align with human understanding. How should we weight human feedback vs. automated metrics?

5. **Generalization to Other Domains:** Most experiments focus on language models. How do these techniques generalize to vision models, multimodal systems, or other architectures?

### Future Research Directions

1. **Multi-Modal Interpretability:** Extend the framework to vision transformers and multimodal models (e.g., GPT-4V)

2. **Circuit Discovery:** Move beyond individual features to discover high-level circuits (collections of features performing specific computations)

3. **Concept Hierarchy Learning:** Organize discovered features into hierarchies of abstraction levels

4. **Real-Time Interpretability:** Deploy this framework as a monitoring system that continuously interprets model behavior in production

5. **Interactive Interpretability:** Design interfaces where human experts and agents collaborate on interpretation tasks

6. **Fairness & Bias Auditing:** Use discovered features to audit bias and fairness in LLM outputs

---

## Code & Resources

### Official Implementation

**GitHub Repository:** 
- Expected release alongside paper publication at Harvard NLP lab
- Check: https://github.com/harvard-nlp (when available)

**Paper Resources:**
- **Full PDF:** https://arxiv.org/pdf/2605.01555
- **HTML Version:** https://arxiv.org/html/2605.01555
- **ArXiv Page:** https://arxiv.org/abs/2605.01555

### Dependencies & Requirements

**Computational Requirements:**
- GPU Memory: 40GB+ (for Gemma-2-27B)
- Training Time: ~24 GPU-hours for feature discovery
- Inference Time: ~10 GPU-hours for 100 features' explanation refinement

**Software Dependencies:**
- PyTorch 2.0+
- Transformers (Hugging Face)
- Sparse Autoencoders library
- Gemma-2 model weights
- Claude or compatible LLM API (for agent prompting)
- Standard ML stack: NumPy, SciPy, Scikit-learn

### Quick Start Guide

**Workflow (when code is released):**

1. **Setup:**
   ```bash
   # Clone when available
   # git clone https://github.com/harvard-nlp/automated-interp.git
   # pip install -r requirements.txt
   ```

2. **Feature Discovery:**
   ```python
   # Load model and create feature discoverer
   model = load_gemma_2()
   discoverer = FeatureFinder(model)
   
   # Generate activation dataset
   features = discoverer.discover_features(
       prompts=diverse_prompt_set,
       layer=18,
       num_features=200
   )
   ```

3. **Feature Explanation:**
   ```python
   explainer = FeatureExplainer(model, features)
   
   # Iteratively refine explanations
   interpretations = explainer.explain(
       features=features,
       num_iterations=5,
       evaluation_metrics=['consistency', 'causality']
   )
   ```

4. **Evaluation:**
   ```python
   evaluator = InterpretabilityEvaluator(interpretations)
   quality_scores = evaluator.evaluate()
   ```

### Interactive Visualizations & Demos

The paper likely includes:
- **Feature Activation Heatmaps:** Visualizing when features activate across different inputs
- **Explanation Dashboard:** Interactive interface to browse discovered features
- **Causal Effect Visualizations:** Showing how feature manipulations affect outputs
- **Feature Comparison Interface:** Side-by-side comparison of discovered features

---

## Related Work & Context

### Connection to Mechanistic Interpretability Research

This work builds upon and advances:

1. **Sparse Autoencoders (Bau et al., Cunningham et al.)**
   - **Previous Work:** SAEs learn interpretable dictionaries of features from dense activations
   - **This Paper's Contribution:** Adds automated discovery and iterative refinement on top of SAEs

2. **Automated Interpretability (Hernandez et al., "Towards Automatic Circuit Discovery")**
   - **Previous Work:** Attempted automated circuit discovery using learned probes
   - **This Paper's Contribution:** Uses agentic frameworks for more robust and scalable discovery

3. **Causal Interpretability (Pearl, Janzing & Schölkopf)**
   - **Previous Work:** Frameworks for causal reasoning in ML
   - **This Paper's Contribution:** Applies causal validation to feature interpretations in LLMs

4. **Polysemanticity Studies (Elhage et al., "Toy Models of Superposition")**
   - **Previous Work:** Identified polysemanticity as a fundamental challenge
   - **This Paper's Contribution:** Detects and flags polysemantic features in practice

5. **LLM Interpretability via Prompting (Wei et al., "Chain of Thought Prompting")**
   - **Previous Work:** Using LLM's reasoning for explanations
   - **This Paper's Contribution:** Systematizes this into an agentic interpretability loop

### Positioning in the xAI Landscape

**xAI Spectrum:**
- **Attribution Methods (LIME, SHAP):** Post-hoc, black-box explanation
- **Attention Visualization:** Direct inspection of attention weights
- **Concept-Based Explanations:** User-defined semantic concepts
- **Mechanistic Interpretability** ← This paper operates here
- **Inherently Interpretable Models:** Models designed for transparency

This paper advances mechanistic interpretability from manual to automated, making it practical for production systems.

### Related xAI Subfields

1. **Feature Attribution (Lundberg et al., Ribeiro et al.)**
   - Related but operates at model output level
   - This paper targets internal representations

2. **Concept-Based Explanations (Kim et al., "TCAV")**
   - Discovers user-defined concepts
   - This paper discovers model's inherent concepts

3. **Fairness & Interpretability (Bolukbasi et al.)**
   - Applies interpretability to fairness analysis
   - Aligns with applications mentioned in this paper

4. **Causal Interpretability (Pearl, Parikh et al.)**
   - Provides causal frameworks this paper applies
   - Complements statistical discovery with causal validation

---

## Community & Impact

### Target Audience

1. **Mechanistic Interpretability Researchers:** Directly advancing the field with automated tools
2. **AI Safety Researchers:** Providing tools for alignment and safety auditing
3. **ML Engineers:** Wanting to understand production LLM behavior
4. **Policy Makers & Regulators:** Supporting explainability requirements (GDPR, AI Act, FDA)
5. **Industry Practitioners:** Deploying LLMs in safety-critical domains

### Expected Impact

**Short-term (2026-2027):**
- Becomes standard tool for feature discovery in mechanistic interpretability
- Used to audit safety properties of deployed LLMs
- Influences xAI research toward agent-based approaches

**Medium-term (2027-2029):**
- Integrated into model development pipelines for interpretability assurance
- Regulatory acceptance as evidence of explainability
- Scale to increasingly larger models

**Long-term (2029+):**
- Foundation for continuous interpretability monitoring systems
- Informs design of inherently interpretable architectures
- Contributes to trustworthy AI systems

### Connection to Broader xAI Communities

- **Mechanistic Interpretability Community:** Direct contribution to tools and methods
- **LIME/SHAP Community:** Complements black-box explanation methods with structural understanding
- **Concept-Based Methods:** Extends concept discovery to model-internal structure
- **Causal Interpretability:** Applies and validates causal frameworks
- **AI Safety & Alignment:** Provides tools for safety auditing and alignment research

---

## References & Further Reading

### Core Papers Cited

1. Elhage, N., et al. (2022). "Toy Models of Superposition." *Anthropic Research*.
2. Bau, D., et al. (2018). "Network Dissection: Quantifying Interpretability of Deep Visual Representations."
3. Hernandez, E., et al. (2024). "Towards Automatic Circuit Discovery for Mechanistic Interpretability."
4. Cunningham, H., et al. (2024). "Sparse Autoencoders Find Universally Consistent Mechanisms Across Languages."
5. Wei, J., et al. (2023). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models."
6. Pearl, J. (2009). "Causality: Models, Reasoning, and Inference."
7. Ribeiro, M. T., & Guestrin, C. (2016). "'Why Should I Trust You?': Explaining the Predictions of Any Classifier."

### Related ArXiv Papers to Explore

- **2410.13928:** "Automatically Interpreting Millions of Features in Large Language Models"
- **2404.14394:** "A Multimodal Automated Interpretability Agent"
- **2604.03764:** "Automated Attention Pattern Discovery at Scale in Large Language Models"
- **2503.16724:** "Towards Automated Semantic Interpretability in RL via Vision-Language Models"
- **2504.07831:** "Deceptive Automated Interpretability: LMs Coordinating to Fool Oversight Systems" (adversarial perspective)

---

## Author's Note

This documentation synthesizes information from the paper's abstract, methods section, and recent talks by the authors. For complete technical details, mathematical derivations, and additional experiments, refer to the full paper at https://arxiv.org/abs/2605.01555.

The framework's emphasis on iterative, agentic approaches to interpretability represents a paradigm shift in how we understand neural networks—moving from static analysis to dynamic exploration. This methodology may prove foundational for future interpretability research and practical AI safety applications.
