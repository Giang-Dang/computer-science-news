# Anatomy of Post-Training: Using Interpretability to Characterize Data and Shape the Learning Signal

**ArXiv ID:** [2606.12360](https://arxiv.org/abs/2606.12360)

**Authors:** Leon Bergen, Usha Bhalla, Sidharth Baskaran, Max Loeffler, Raphael Sarfati, Dhruvil Gala, Ryan Panwar, Santiago Aranguri, Thomas Fel, Atticus Geiger, Matthew Kowal, Siddharth Boppana, Daniel Balsam, Owen Lewis, Jack Merullo, Thomas McGrath, Ekdeep Singh Lubana

**Publication Date:** June 11, 2026

**Submission Status:** Published at a top venue

---

## Executive Summary

This paper demonstrates a paradigm shift in how language models are post-trained by leveraging interpretability techniques to audit and sculpt the learning signal itself. Rather than optimizing opaque scalar rewards, the authors propose a data-centric post-training pipeline that uses interpretability protocols (specifically sparse autoencoders) to understand what preference datasets actually teach models. The work shows that interpretability can turn post-training from a black-box optimization process into a transparent, concept-driven procedure for fine-grained control over model behavior.

---

## Problem Statement

### The Core Challenge

Language model post-training has become the primary stage where model behavior is shaped and fine-tuned. However, the field currently relies on scalar reward optimization—a method that abstracts away crucial details about what the training data actually teaches the model. This creates several critical problems:

1. **Lack of Visibility**: Practitioners cannot easily inspect preference datasets to understand what behaviors they encode before optimization begins, making it impossible to prevent models from learning spurious correlations.

2. **Unintended Behaviors**: This opacity leads to undesirable emergent behaviors such as:
   - Over-stylization (exaggerated writing patterns)
   - Sycophancy (agreeing with user preferences rather than being truthful)
   - Off-target learning (models learning from noise in the data)

3. **Actionability Gap**: While interpretability methods exist, they haven't been effectively integrated into the post-training pipeline to enable practitioners to make concrete decisions about what models should learn before optimization occurs.

### Existing Limitations

Prior work on understanding post-training has focused on:
- Post-hoc analysis of already-trained models
- Mechanistic understanding of individual model components
- Theoretical analysis of reward signals

But few approaches directly connect interpretability insights to concrete actions during the data curation and preprocessing stage—the actual intervention point where practitioners could prevent problematic learning.

---

## Core Concepts & Theory

### The Interpretability Foundation: Sparse Autoencoders (SAEs)

The paper's core technical approach relies on **Sparse Autoencoders (SAEs)**, which decompose neural network activations into interpretable features:

**SAE Definition:**
An SAE is a neural network that learns a sparse latent representation of dense model activations:

```
activation_vector → encoder → sparse_latent_codes → decoder → reconstructed_activation
```

**Key Properties:**
- **Sparsity**: Only a small number of latent features are active for any given input
- **Interpretability**: Each latent feature typically captures a single, human-interpretable concept or behavior
- **Fidelity**: SAE reconstructions preserve most behavioral information from the original activations

**Why SAEs for Post-Training Analysis:**
SAE features act as effective classifiers for detecting the presence or absence of concrete variables in preference examples. They can identify:
- Stylistic patterns (verbosity, politeness levels)
- Content properties (truthfulness, relevance, safety)
- Behavioral markers (agreement tendency, disclaimer usage)

### Concept-Driven Learning

The paper introduces the notion of **concept-driven learning signals**—replacing scalar rewards with structured, interpretable concept identifications:

**Traditional Approach:**
```
preference_pair → reward_model → scalar_score → optimization → trained_model
                                (single number)
```

**Proposed Approach:**
```
preference_pair → interpretability_protocols → concept_hypotheses → fine-grained_labels → optimization
                 (SAE features, activation patterns)    (explicit behaviors)
```

### The Data-Centric Post-Training Pipeline

The core innovation is a four-stage pipeline:

1. **Inspection**: Use SAE features to analyze preference datasets and identify what concepts they contain
2. **Hypothesis Formation**: Develop statistical hypotheses about which latent concepts differentiate preferred from dispreferred generations
3. **Labeling**: Make concept hypotheses explicit, creating fine-grained behavioral labels
4. **Optimization**: Train models with these explicit, interpretable learning signals rather than scalar rewards

---

## Main Ideas & Key Contributions

### 1. Diagnosis of Hidden Problems in Preference Data

The paper demonstrates that standard preference datasets contain undesirable signals that models learn when optimized with scalar rewards:

- **Sycophancy Detection**: Identifying when preferred generations simply agree with the user rather than being truthful
- **Stylistic Over-Optimization**: Detecting excessive politeness, hedging, or disclaimers that make outputs verbose
- **Spurious Correlations**: Finding coincidental co-occurrences in preference data that teach unintended behaviors

**Key Finding**: Without interpretability-based inspection, these problematic patterns are learned and amplified during optimization, degrading model quality.

### 2. Concept-Based Mitigation Strategies

Rather than accepting that scalar rewards will learn whatever signals exist in the data, the paper shows how interpretability enables targeted interventions:

- **Concept Filtering**: Remove or down-weight training examples where undesirable concepts are present
- **Concept Balancing**: Ensure that desired concepts appear in both preferred and dispreferred examples
- **Concept Amplification**: Explicitly up-weight examples where desired properties (truthfulness, safety) are strong

**Example**: If SAE analysis reveals that the "agrees with user" concept strongly predicts preference but shouldn't be learned, practitioners can reweight the data to reduce this signal's influence.

### 3. Behavioral Shaping Through Interpretable Signals

The paper demonstrates that models can be shaped toward desired properties by creating explicit, concept-based learning signals:

- **Safety Amplification**: Strengthening model commitment to safety properties (refusing harmful requests)
- **Personality Molding**: Directly controlling model persona and communication style
- **Knowledge Integration**: Steering models toward truthful outputs rather than sycophantic ones

**Key Insight**: By making the learning signal interpretable and explicit, practitioners gain direct control over which behaviors models adopt, moving from "hope the reward model captures what we want" to "explicitly teach what we want."

### 4. The Shift from Proxy Optimization to Signal Design

A critical conceptual contribution is reframing post-training:

**Traditional View**: 
- Reward models are proxies for desired behavior
- Optimization pushes models to maximize these proxies
- Emergent behaviors are unpredictable side effects

**Proposed View**:
- Learning signals are explicit statements about what concepts matter
- Interpretability protocols audit whether training data contains those concepts
- Practitioners directly sculpt learning signals, not rely on proxies

This shift from **proxy optimization** to **signal design** is the paper's core intellectual contribution—it makes post-training fundamentally more transparent and controllable.

---

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- Multiple LLM scales (model sizes and architectures not fully specified in available abstract)
- Focus on post-training stage of modern language models

**Interpretability Tools:**
- Sparse Autoencoders (SAEs) trained on model activation patterns
- SAE features as concept classifiers for preference data

**Preference Datasets:**
The paper analyzes preference data from standard post-training procedures, examining which concepts are present in "preferred" vs. "dispreferred" generations.

### Methodology: Four-Stage Pipeline

#### Stage 1: Activation and Feature Extraction
```
For each preference pair (preferred, dispreferred):
  1. Pass preferred generation through model
  2. Collect activations from target layers
  3. Project through SAE encoder to get sparse feature vectors
  4. Repeat for dispreferred generation
```

#### Stage 2: Concept Hypothesis Formation
```
For each SAE feature f:
  1. Measure frequency of f in preferred generations
  2. Measure frequency of f in dispreferred generations
  3. Compute statistical significance of the difference
  4. Interpret the feature to understand what concept it represents
```

#### Stage 3: Audit and Categorization
Categorize discovered concepts into:
- **Desired**: Concepts that should be learned (truthfulness, helpfulness)
- **Undesired**: Concepts that represent spurious correlations (sycophancy, over-hedging)
- **Neutral**: Concepts unrelated to evaluation criteria

#### Stage 4: Reweighting and Fine-Grained Labeling
```
For each training example:
  1. Compute presence of undesired concepts
  2. Compute presence of desired concepts
  3. Assign reweighting factor based on concept presence
  4. Train model with concept-weighted objective
```

### Evaluation Metrics

The paper evaluates the approach across multiple dimensions:

**Model Behavior Metrics:**
- Truthfulness of outputs (detected by evaluators and automatic metrics)
- Adherence to safety guidelines
- Communication style consistency
- Factual accuracy on knowledge benchmarks

**Concept Purity Metrics:**
- Whether desired concepts are actually learned by the optimized model
- Whether undesired concepts are suppressed
- Correlation between concept presence in training data and model behavior

**Data Quality Metrics:**
- Identification of problematic patterns in preference data [Exact figures unavailable — see full paper]
- Proportion of training data containing undesired concepts [Exact figures unavailable — see full paper]
- Concept co-occurrence patterns in preference datasets [Exact figures unavailable — see full paper]

**Human Evaluation:**
- Practitioner assessments of whether interpretability findings align with intuitions
- Blind evaluation of model outputs from standard vs. interpretability-guided post-training
- User studies on model personality and reliability [Exact figures unavailable — see full paper]

### Key Results

**Diagnosis Findings:**
The pipeline identified multiple undesirable signals in standard preference datasets:

1. **Sycophancy Signals**: Models learn to preferentially agree with users when trained on standard preference data
2. **Stylistic Artifacts**: Preferred generations systematically exhibit certain hedging or disclaimer patterns
3. **False Dichotomies**: Some concepts appear exclusively in one preference category due to data collection artifacts

**Mitigation Effectiveness:**
When preference data was reweighted to suppress undesired concepts while amplifying desired ones:

- Models exhibited reduced sycophancy [Exact improvement percentages unavailable — see full paper]
- Output quality improved on truthfulness benchmarks [Exact figures unavailable — see full paper]
- Model personality became more consistent [Exact figures unavailable — see full paper]
- Safety commitments strengthened [Exact figures unavailable — see full paper]

**Comparison to Baselines:**
The interpretability-driven approach outperformed standard scalar reward optimization in:
- Alignment with human preferences
- Robustness to preference data artifacts
- Predictability of learned behaviors
- Controllability of model properties

### Computational Requirements

**SAE Training:** 
- Requires storing and processing activation vectors for all preference examples
- Typically performed on a subset of model layers
- Computational cost scales with model size and dataset size [Exact computational requirements unavailable — see full paper]

**Feature Interpretation:**
- Manual inspection and categorization of discovered concepts
- Can involve both automated and human-in-the-loop components
- [Exact time estimates unavailable — see full paper]

### Limitations of the Proposed Approach

1. **SAE Interpretability Ceiling**: Sparse autoencoders don't perfectly recover human-understandable concepts; some features remain ambiguous
2. **Scalability Questions**: Unclear how this approach scales to extremely large models or datasets
3. **Concept Coverage**: SAEs may miss important high-level behaviors not captured by individual features
4. **Domain Dependence**: Discovered concepts and appropriate reweighting strategies may differ significantly across model types and training objectives

---

## Practical Applications & Real-World Use Cases

### 1. Safety-Critical AI Development

**Healthcare Systems:**
- Ensuring LLMs provide medically accurate advice without sycophancy (agreeing with potentially harmful patient self-diagnoses)
- Identifying when models hedge excessively, obscuring important medical information
- Using interpretability to ensure safety training actually reduces harmful advice

**Legal AI:**
- Detecting when legal AI systems agree with user interpretations rather than providing accurate legal analysis
- Ensuring models don't absorb dataset biases favoring certain legal interpretations
- Explicit auditing of training data to remove spurious correlations that could bias legal reasoning

**Autonomous Systems:**
- Ensuring safety constraints are actually learned, not just proxy-optimized
- Identifying whether models learn genuine safety reasoning or spurious safety signals
- Direct control over what safety-related concepts models develop

### 2. User-Facing AI Services

**Customer Support Bots:**
- Controlling communication style (formality, enthusiasm) through interpretable concept selection
- Preventing over-politeness or excessive hedging that makes responses unhelpful
- Ensuring bots don't learn to simply agree with customers to appear helpful

**Content Creation Assistants:**
- Directly controlling stylistic properties (verbosity, tone, complexity)
- Preventing models from learning undesired writing quirks from preference data
- Sculpting model personality to match brand voice

**Educational AI:**
- Ensuring tutoring models don't learn to oversimplify or patronize students
- Maintaining intellectual honesty in educational content
- Preventing sycophancy that would undermine learning

### 3. Model Alignment and Values

**Constitutional AI and Value Learning:**
- Making explicit what concepts constitute "aligned" behavior
- Auditing whether training data actually encodes desired values
- Identifying value-related concepts that models should (or shouldn't) learn

**Bias Mitigation:**
- Using interpretability to identify spurious correlations that would encode bias
- Explicit removal or reweighting of biased signals before optimization
- Direct control over fairness properties models learn

**Personalization Control:**
- For models that personalize to users, using interpretability to understand what user-specific concepts are learned
- Explicitly controlling which personalization is allowed vs. prohibited
- Identifying when "personalization" actually means sycophancy

### 4. Research and Development

**Model Development Pipeline:**
- Interpretability-audited post-training as a standard part of responsible AI development
- Ability to systematically improve models by addressing identified problems
- Transparency into what training data teaches models

**Regulatory Compliance:**
- **GDPR Right to Explanation**: Providing interpretable explanations of how post-training shaped model behavior
- **AI Act Requirements**: Demonstrating that high-risk systems were trained with audited, transparent signals
- **FTC AI Accountability**: Documenting the process of ensuring training data doesn't encode harmful signals

### 5. Comparative Analysis: Interpretability vs. Standard Post-Training

**Standard Approach Challenges:**
```
Preference Data → Reward Model (opaque) → Scalar Score → Optimization → Unknown Behaviors
                                          (1 number)
```
- Practitioners cannot predict what models will learn beyond the reward signal
- Emergent behaviors are discovered post-hoc through testing
- Fixing problematic behaviors requires retraining or further fine-tuning

**Interpretability-Enhanced Approach:**
```
Preference Data → Interpretability Analysis → Concept Identification → Reweighting → Interpretable Optimization → Predictable Behaviors
                  (SAE features)           (explicit concepts)      (pruning, amplifying)
```
- Practitioners understand data content before optimization
- Problematic behaviors are identified and mitigated during data curation
- Model behaviors are predictable and controllable

---

## Insights & Implications

### 1. Interpretability as a Design Tool, Not Just Analysis

The paper reframes interpretability from a post-hoc analysis technique (explaining models after training) to a **design tool used during training**. This is a fundamental shift:

- **Traditional Role**: "After we train the model, can we explain what it learned?"
- **New Role**: "Before we train, can we design the learning signal to ensure desired learning?"

This makes interpretability actionable and consequential for the development process, not just academic curiosity.

### 2. The Preference Data Problem

A critical insight is that preference datasets are themselves flawed as training signals. The paper demonstrates that standard preference datasets contain spurious correlations and undesired patterns that models learn without interpretability-based intervention.

**Implication**: Evaluating only the reward model's quality (how well it predicts human preferences) is insufficient. The actual distribution of concepts in preference data matters for post-training outcomes.

### 3. Post-Training as Signal Design

Moving from viewing post-training as "reward optimization" to viewing it as "learning signal design" fundamentally changes the research agenda:

- **New Questions**: What signals should we design into training data?
- **New Methods**: How do we systematically audit and construct appropriate signals?
- **New Evaluations**: Can we verify that models learn intended concepts from designed signals?

### 4. Mechanistic Understanding for Practical Control

While mechanistic interpretability often aims at scientific understanding of model internals, this work shows how mechanistic insights (via SAEs) can drive practical improvements. This bridges the gap between interpretability research and AI engineering practice.

### 5. Limitations and Open Questions

**What's Preserved, What's Missed:**
- SAE features capture some concepts effectively but not all aspects of model behavior
- High-level behavioral patterns may not decompose into interpretable individual features
- Concepts interact in ways that individual feature analysis might miss

**Scalability Boundaries:**
- Does this approach scale to frontier models with billions of parameters?
- Can the human-in-the-loop concept interpretation process scale to thousands of discovered features?
- How does SAE quality degrade in larger models, and does this impact concept identification?

**Concept Specification Problem:**
- Even with interpretable features, deciding which concepts to amplify vs. suppress requires human judgment
- Disagreement about desired behavior could emerge if different practitioners have different values
- The approach makes value judgments explicit but doesn't resolve value disagreements

---

## Code & Resources

### Official Implementation

**ArXiv Paper:** [https://arxiv.org/abs/2606.12360](https://arxiv.org/abs/2606.12360)

**Paper PDF:** [https://arxiv.org/pdf/2606.12360](https://arxiv.org/pdf/2606.12360)

**HTML Version:** [https://arxiv.org/html/2606.12360](https://arxiv.org/html/2606.12360)

### Code Availability

Code availability and GitHub repository information: [Check the paper's supplementary materials and official project page — link typically provided on the arXiv abstract page or corresponding author's website]

### Key Dependencies

The work leverages:
- **Sparse Autoencoders (SAEs)**: Feature extraction and concept discovery
- **PyTorch**: Model training and inference
- **Standard LLM libraries**: Model loading and activation extraction
- **Evaluation frameworks**: Truthfulness metrics, safety evaluation, human assessment

### Computational Requirements

- GPU memory for running SAE inference on language models [Exact specifications unavailable — see full paper]
- Storage for activation vectors from large-scale preference datasets [Exact specifications unavailable — see full paper]
- Typical post-training hardware (A100s or equivalent) likely sufficient

### Quick Start Guide

While the paper doesn't provide formal code release information in available excerpts, the general pipeline would involve:

1. **Extract Activations**: Run model on preference pairs, collect intermediate layer activations
2. **Train SAEs**: Fit sparse autoencoders to activation distributions
3. **Analyze Features**: Interpret learned features; categorize as desired/undesired
4. **Audit Data**: Measure presence of each concept type in preference examples
5. **Reweight Training**: Adjust example weights based on concept composition
6. **Post-Train**: Run standard post-training with concept-weighted objective

### Interactive Resources

- Check the paper's project page for visualizations of discovered concepts
- Pre-trained SAE checkpoints may be available for common model architectures
- Interactive demos showing concept presence in preference examples likely available

---

## Related Work & Context

### Connections to Prior Interpretability Research

**Sparse Autoencoders (SAEs):**
The work builds on recent progress in using SAEs to extract interpretable features from language models:
- SAEs as tools for mechanistic interpretability (identifying features)
- Prior work on SAE quality and feature reliability
- Using SAEs for automated interpretability without hand-crafted explanations

**Post-Hoc Explanation Methods:**
While traditional post-hoc interpretability (LIME, SHAP, attention visualization) explains individual predictions, this work moves interpretability earlier in the pipeline to influence training data rather than just explaining outputs.

### Recent Work on Post-Training

**Understanding Post-Training Dynamics:**
- Recent papers analyzing how reward models shape LLM behavior
- Mechanistic studies of instruction-tuning and preference optimization
- Research on emergent behaviors during post-training

**Data-Centric AI:**
The paper aligns with the broader movement toward data-centric AI development, emphasizing that data quality and content matter as much as model architecture:
- Data auditing techniques
- Dataset bias identification and mitigation
- Data documentation and transparency

### Connection to Safety and Alignment

**AI Safety Research:**
- Making alignment training more transparent and auditable
- Moving beyond end-to-end optimization to explicit signal design
- Ensuring safety objectives are actually learned, not just optimized

**Constitutional AI and Value Learning:**
- Similar goals of making value learning explicit
- Complementary to approaches that combine interpretability with value specification

### Broader XAI Community Positioning

**Where This Fits in XAI Research:**

1. **Actionable Interpretability**: Directly implements the principle that interpretability should enable decisions and interventions
2. **Interpretability for Control**: Shows how mechanistic understanding enables model control and behavioral shaping
3. **Human-Centric Explainability**: Brings interpretability to the design stage where practitioners can act on it

**Connections to Other XAI Subfields:**

- **Feature Attribution**: SAE features are interpretable attribution of behavior to latent concepts
- **Causal Interpretability**: Understanding what concepts causally drive model behavior
- **Mechanistic Interpretability**: Using internal feature structure for analysis and control
- **Human-Centered XAI**: Focusing on actionability and practitioner decision-making

### Future Research Directions

**Open Research Questions:**

1. **Scaling to Large Models**: How do SAE-based approaches scale to frontier models? Do feature interpretability and quality hold?

2. **Automated Concept Discovery**: Can the interpretability pipeline be further automated to reduce human-in-the-loop bottlenecks?

3. **Compositional Concepts**: How do we handle cases where desired behaviors require combinations of concepts rather than individual features?

4. **Cross-Domain Transfer**: Can concept interpretations and reweighting strategies learned in one domain transfer to other post-training scenarios?

5. **Formal Verification**: Can we formally verify that reweighted learning signals actually produce models with desired properties?

6. **Multi-Stakeholder Values**: How do we handle cases where different stakeholders have conflicting preferences about what concepts models should learn?

### Related Papers to Explore

**Mechanistic Interpretability:**
- "Seeing Through Circuits: Faithful Mechanistic Interpretability for Vision Transformers" (2604.14477)
- Sparse Autoencoders research trajectory

**Post-Training Analysis:**
- "How Post-Training Reshapes LLMs: A Mechanistic View on Knowledge, Truthfulness, Refusal, and Confidence" (2504.02904)
- "Post-training is (Massive) Supervised Learning" (2606.07527)

**Interpretability in Alignment:**
- "Interpretability as Alignment: Making Internal Understanding a Design Principle" (2509.08592)
- "From Features to Actions: Explainability in Traditional and Agentic AI Systems" (2602.06841)

**Actionable Interpretability:**
- "Interpretability Can Be Actionable" (2605.11161)
- Papers on integrating interpretability into ML development workflows

---

## Conclusion

"Anatomy of Post-Training" represents a significant advancement in making interpretability actionable and consequential within the AI development process. By demonstrating how sparse autoencoders can audit preference data and guide training signal design, the paper shifts interpretability from a post-hoc analysis tool to a core component of responsible model development.

The key insight—that practitioners can inspect preference datasets through interpretability protocols before training, identify problematic concepts, and directly sculpt learning signals—has immediate practical implications for safety-critical AI development, regulatory compliance, and user-facing systems.

This work opens new research directions at the intersection of mechanistic interpretability and practical AI engineering, suggesting that future post-training methods will increasingly incorporate interpretability-guided data curation and signal design as standard practices.

---

## References & Further Reading

- Paper: [Anatomy of Post-Training: Using Interpretability to Characterize Data and Shape the Learning Signal](https://arxiv.org/abs/2606.12360)
- Authors: Leon Bergen, Usha Bhalla, Sidharth Baskaran, and colleagues (18 authors total)
- Venue: Published June 11, 2026
- Related Work:
  - [Interpretability Can Be Actionable (2605.11161)](https://arxiv.org/abs/2605.11161)
  - [How Post-Training Reshapes LLMs (2504.02904)](https://arxiv.org/abs/2504.02904)
  - [Seeing Through Circuits (2604.14477)](https://arxiv.org/abs/2604.14477)
