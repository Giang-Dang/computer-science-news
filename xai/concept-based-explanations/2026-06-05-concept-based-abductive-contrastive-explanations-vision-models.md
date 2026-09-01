# Concept-Based Abductive and Contrastive Explanations for Behaviors of Vision Models

**Paper:** Concept-Based Abductive and Contrastive Explanations for Behaviors of Vision Models  
**Authors:** Ronaldo Canizales, Divya Gopinath, Corina Păsăreanu, and Ravi Mangal  
**ArXiv ID:** 2605.06640  
**Submitted:** June 5, 2026  
**Institutions:** NASA Ames Research Center, Carnegie Mellon University, Florida International University

## Executive Summary

This paper extends concept-based explanations to formal abductive and contrastive frameworks, introducing **Concept-based Abductive eXplanations (ConAXps)** and **Concept-based Contrastive eXplanations (ConCXps)** for vision models. The work addresses a critical gap in existing concept-based interpretability methods by establishing causal grounding between concepts and model predictions, providing minimal and formally-defined explanations that bridge the expressivity limitations of prior work.

## Problem Statement

Concept-based explanations have emerged as a promising approach for interpreting deep neural networks by expressing model predictions in terms of high-level, human-understandable concepts rather than low-level pixel-level features. However, existing concept-based methods suffer from significant limitations:

1. **Lack of Causal Grounding**: Many methods do not establish a clear causal connection between identified concepts and model predictions, limiting their reliability for decision-making.

2. **Limited Expressivity**: Most approaches can only infer causal explanations involving single concepts, unable to handle complex multi-concept interactions and relationships.

3. **Insufficient Formalization**: The lack of formal definitions makes it difficult to objectively compare explanations across methods, verify their correctness, or compose them meaningfully.

4. **Distinction from Feature-Level Methods**: While pixel-level abductive and contrastive explanations exist, extending these formalisms to the concept level poses unique challenges, particularly in establishing minimal concept sets.

## Core Concepts & Theory

### Abductive Explanations (ConAXps)

An abductive explanation identifies a **minimal set of concepts** such that:
- When these concepts are retained and all other concepts are erased from the model's internal representation
- The model's prediction remains unchanged (preserves the original prediction)
- The concept set is minimal (no proper subset also preserves the prediction)

Intuitively, abductive explanations answer the question: "What concepts are sufficient for the model to make this prediction?"

**Mathematical Formulation:**
For a model f, input x, and predicted class y:
- ConAXp(x, y) = {C₁, C₂, ..., Cₖ} ⊂ Concepts
- Such that erasing all concepts not in ConAXp preserves f(x) = y
- No proper subset of ConAXp has this property

### Contrastive Explanations (ConCXps)

A contrastive explanation identifies a **minimal set of concepts** such that:
- Erasing these specific concepts from the representation triggers a prediction change
- The original prediction changes to a different class prediction
- The concept set is minimal

Intuitively, contrastive explanations answer: "What concepts, if removed, would change the model's decision?"

**Mathematical Formulation:**
For a model f, input x, predicted class y, and contrastive class y':
- ConCXp(x, y → y') = {C₁, C₂, ..., Cₘ} ⊂ Concepts
- Such that erasing ConCXp from the representation changes f(x) from y to y'
- No proper subset of ConCXp achieves this change

### Relationship to Feature-Level Methods

The paper builds on established formal definitions of abductive and contrastive explanations at the feature/pixel level, but extends them to concept-level explanations. The key distinction is that concepts operate at a higher semantic level, requiring different algorithms for identifying minimal concept sets.

### Theoretical Grounding

The approach is grounded in **formal methods for explanation**, drawing connections to:
- **Symbolic explanations** and logical reasoning about model behavior
- **Causal reasoning** frameworks that establish direct causal links between concepts and predictions
- **Minimality principles** from formal verification and model checking

## Main Ideas & Key Contributions

### 1. Formal Concept-Based Abductive and Contrastive Explanations

The paper's primary contribution is formalizing abductive and contrastive explanations at the concept level. This provides:

- **Clear semantics**: Well-defined meaning of what a concept-based explanation represents
- **Algorithmic foundations**: Concrete algorithms for computing these explanations
- **Minimality guarantees**: Ensures explanations are truly minimal (no unnecessary concepts included)
- **Composability**: Enables combining multiple explanations for deeper understanding

### 2. Generalization Beyond Single Concepts

Unlike existing concept-based methods that typically identify single most-relevant concepts, ConAXps and ConCXps handle:

- **Multi-concept interactions**: Explanations can include multiple concepts that jointly influence predictions
- **Complex relationships**: Captures how multiple concepts work together to produce predictions
- **Backup mechanisms**: Reveals redundant concept pathways when erasing concepts doesn't change predictions (unlike abductive explanations which must preserve behavior)

### 3. Bridging Symbolic and Connectionist Approaches

The framework bridges:
- **Symbolic explanations** (formal, minimal, verifiable) from the XAI literature
- **Connectionist representations** (neural network-based concept learning)
- Combines rigor of formal methods with flexibility of deep learning

### 4. Analysis of Misclassified Samples

For misclassified examples, the paper shows how concept-based abductive and contrastive analysis can identify:

- **Concept-based repairs**: Which concepts, if corrected or emphasized, would fix the misclassification
- **Root causes of errors**: Which concepts misled the model or were incorrectly learned
- **Systematic model failures**: Patterns in which concept combinations lead to prediction errors

## Methodology & Implementation

### Framework Architecture

The methodology assumes:

1. **Pre-trained Deep Neural Network**: A CNN trained on visual classification tasks with inputs as images and outputs as class predictions
2. **Concept Extractor**: A mechanism for extracting concept representations from intermediate layers or learned concept vectors
3. **Concept Manipulation**: Ability to erase or retain specific concepts in the representation space

### Algorithm Overview

**Computing ConAXps (Abductive Explanations):**

1. **Concept Encoding**: Extract concept representations for input x from model internals
2. **Candidate Generation**: Initialize with all concepts that are "active" (non-zero or above threshold)
3. **Minimization**: Iteratively remove concepts one-by-one
4. **Verification**: Test if removing each concept changes the prediction
5. **Greedy Refinement**: Keep only those concepts whose removal changes predictions
6. **Output**: The minimal set of "sufficient" concepts

**Computing ConCXps (Contrastive Explanations):**

1. **Concept Encoding**: Same as above
2. **Target Class Selection**: Choose target contrastive class y'
3. **Candidate Generation**: Test various subsets of concepts
4. **Verification**: Find which concept erasures trigger transition from y to y'
5. **Minimization**: Identify minimal sufficient concept sets
6. **Output**: The minimal set of "necessary" concepts for changing predictions

### Experimental Setup

**Models Tested:** [Exact architectures unavailable — see full paper]
- Vision models trained on image classification
- Focused on models where concept interpretability is important

**Datasets:** [Exact datasets unavailable — see full paper]
- Standard image classification benchmarks
- Domain-specific vision datasets where concept understanding is critical

**Concept Extraction Methods:** [Details unavailable — see full paper]
- Learned concept vectors from model training
- Extracted from intermediate layers using attention mechanisms
- May include human-labeled semantic concepts

### Evaluation Metrics

The paper employs multiple dimensions for evaluating concept-based explanations:

1. **Sufficiency**: Do retained concepts (ConAXps) preserve the original prediction?
   - Measures: Accuracy of prediction preservation

2. **Necessity**: Do erased concepts (ConCXps) actually trigger prediction changes?
   - Measures: Success rate of prediction change

3. **Minimality**: Are explanations truly minimal?
   - Measures: Size of minimal concept sets compared to baselines
   - Ensures no redundant concepts included

4. **Human Interpretability**: Can humans understand the concept sets?
   - Qualitative evaluation of concept semantics
   - Feasibility of acting on explanations

5. **Faithfulness**: Do concept-based explanations truly reflect model behavior?
   - Comparison with other explanation methods
   - Robustness to concept perturbations

### Results Summary

[Exact figures unavailable — see full paper]

The experimental results demonstrate that:

- **Minimal explanations**: ConAXps and ConCXps identify smaller concept sets compared to methods that include all relevant concepts
- **Semantic meaningfulness**: Identified concepts align with human understanding of important visual features
- **Multi-concept interactions**: Examples reveal non-trivial concept combinations that jointly drive predictions
- **Error analysis**: Concept-based repairs successfully identify fixes for misclassified examples

### Computational Considerations

**Computational Complexity:** [Details unavailable — see full paper]

The problem of finding minimal concept sets is related to the Set Cover problem (NP-hard in general). The paper likely addresses this through:
- Greedy approximation algorithms
- Heuristic pruning strategies
- Leveraging model structure for efficiency

**Scalability:** [Details unavailable — see full paper]
- Approach's scalability to large models with thousands of concepts
- Practical runtime considerations for real-world deployment

### Limitations

1. **Concept Definition Dependency**: Quality of explanations depends heavily on how well concepts are defined or learned; poorly captured concepts limit explanation utility

2. **Concept Completeness**: Requires that all relevant semantic concepts can be adequately represented; missing concepts can lead to incomplete explanations

3. **Erasing Mechanism**: The concept erasure procedure (setting to zero, noise injection, etc.) may create unrealistic representations the model hasn't seen, potentially distorting explanations

4. **Single Model Assumption**: Current formulation applies to a single model; generalizing to multiple models or model families requires additional work

5. **Binary Concept Assumption**: Current approach treats concepts as present/absent; continuous concept strengths may require modifications

## Practical Applications & Real-World Use Cases

### Medical Imaging

**Application Domain:** Computer-aided diagnosis systems for detecting diseases in medical images

**Use Case:**
- A CNN trained to detect tumors in radiology scans may rely on subtle visual patterns
- ConAXps can identify which anatomical concepts (e.g., "tissue density," "suspicious borders," "location") are sufficient for diagnosis
- ConCXps can reveal which concepts, if eliminated/hidden, would reverse the diagnosis
- **Value**: Helps radiologists understand model reasoning and build trust in AI-assisted diagnosis

**Regulatory Implications:**
- FDA regulations for medical device AI require transparency and interpretability
- Concept-based explanations provide the formal rigor necessary for regulatory approval
- Enables compliance with AI transparency requirements

### Autonomous Vehicle Perception

**Application Domain:** Object detection and classification in autonomous vehicles

**Use Case:**
- Vision models must classify pedestrians, vehicles, traffic signs, road conditions
- ConAXps identify which visual concepts (e.g., "person-shaped silhouette," "moving patterns," "reflective surfaces") drive object detection
- ConCXps reveal vulnerabilities: which concept changes could cause misclassification
- **Value**: Safety analysis to understand failure modes and improve robustness

**Regulatory Implications:**
- ISO/SAE standards for autonomous vehicle safety require interpretable decision-making
- Concept-based explanations demonstrate that model decisions follow expected reasoning patterns

### Finance and Credit Decisions

**Application Domain:** Image-based financial assessment (e.g., collateral appraisal, fraud detection)

**Use Case:**
- Computer vision systems analyze property images for valuation or insurance assessment
- ConAXps identify which visual concepts (building condition, location features, property characteristics) influence valuations
- ConCXps reveal which visual elements, if modified, would change assessment
- **Value**: Transparency enables human oversight and compliance with fair lending regulations

### Content Moderation

**Application Domain:** Moderation systems detecting harmful content in images

**Use Case:**
- Computer vision systems flag inappropriate content for review
- ConAXps identify which visual concepts triggered content flags
- ConCXps show what changes would remove flags
- **Value**: Helps content moderators understand AI decisions, enables targeted improvement, reduces false positives

### Bias and Fairness Analysis

**Application Domain:** Identifying and mitigating bias in vision systems

**Use Case:**
- ConAXps reveal which concepts the model relies on (e.g., if detecting faces, which facial attributes drive predictions)
- ConCXps show undesired concept dependencies
- **Value**: Identifies unfair concept dependencies and guides debiasing efforts

## Insights & Implications

### Theoretical Advances

1. **Formalization of Concept-Based Explanations**: Extends formal explanation theory from pixel-level to semantic-level concepts, advancing the theoretical foundations of XAI

2. **Causal Reasoning at Scale**: Provides a practical framework for establishing causal relationships between high-level concepts and model predictions in deep neural networks

3. **Bridging Symbolic and Neural Methods**: Demonstrates how formal symbolic reasoning can be grounded in connectionist models

### Methodological Impact

1. **Minimal Explanations**: The minimality constraint ensures explanations are as simple as possible while remaining correct, improving human interpretability

2. **Formal Verification Potential**: Concept-based abductive and contrastive explanations could enable formal verification of neural network behavior properties

3. **Composable Explanations**: The formal framework enables combining multiple explanations for deeper understanding (e.g., "to make prediction A, concepts {C1, C2} are sufficient; to prevent prediction A, {C3} must be absent")

### Broader Implications for Trustworthy AI

1. **Regulatory Alignment**: Formal definitions and minimal explanations align with regulatory requirements for interpretable, transparent AI systems

2. **Human-AI Alignment**: Concept-based explanations in natural language semantic concepts bridge the gap between human understanding and model internals

3. **Debugging and Improvement**: Identifies specific concepts responsible for errors, enabling targeted model improvement and debiasing

4. **Transfer and Generalization**: Concept-based explanations may transfer across related models or domains better than pixel-level features

### Research Directions and Open Questions

1. **Scalability**: How do these methods scale to modern large-scale vision models (Vision Transformers, CLIP-based models) with millions of concepts?

2. **Concept Definition**: How should concepts be defined or learned to maximize explanation utility? Are learned concepts interpretable?

3. **Concept Interactions**: Can we characterize complex interactions between concepts? Are there "concept algebras" that reveal compositional structure?

4. **Robustness**: How robust are concept-based explanations to adversarial perturbations or distribution shifts?

5. **Temporal Evolution**: How do concept dependencies evolve during training? Can we track concept emergence and specialization?

6. **Multi-Modal Concepts**: Can we extend concept-based explanations to multi-modal models combining vision, language, and other modalities?

### Limitations and Failure Cases

1. **Concept Capture Problem**: If concepts cannot adequately capture the model's decision factors, explanations will be incomplete or misleading

2. **Explanation Overfitting**: ConAXps/ConCXps might identify spurious concept combinations that happen to preserve predictions due to model quirks rather than true decision logic

3. **Out-of-Distribution Behavior**: Concept erasure creates representations not seen during training; model behavior in this regime may not reflect true decision-making

4. **Concept Polysemy**: Single concepts might have multiple semantic meanings depending on context, complicating interpretation

## Code & Resources

### Official Implementations

**GitHub Repository:** [Official implementation link unavailable — see full paper]

The authors likely provide implementations for:
- Computing ConAXps and ConCXps for different concept extraction methods
- Concept evaluation and visualization tools
- Benchmarking scripts for standard vision datasets

### Dependencies and Requirements

**Core Dependencies:** [Exact specifications unavailable — see full paper]
- PyTorch or TensorFlow for model training and inference
- Standard computer vision libraries (torchvision, OpenCV)
- Concept extraction and manipulation libraries

**Computational Requirements:** [Estimates unavailable — see full paper]
- Likely requires GPU for reasonable runtime on large models
- Memory requirements scale with model size and number of concepts
- Concept set search may require significant computation for high-dimensional concept spaces

### Quick Start Guide

Typical usage workflow [estimated]:
1. Load pre-trained vision model and concept extractor
2. Select input image and target class
3. Run ConAXp computation: `conaxp_result = compute_conaxp(model, image, target_class)`
4. Run ConCXp computation: `concxp_result = compute_concxp(model, image, target_class, contrastive_class)`
5. Visualize results with concept importance and concept descriptions

## Related Work & Context

### Concept-Based Interpretation Methods

**TCAV (Testing with Concept Activation Vectors)** - Identified and tested concepts through the lens of linear model behavior; this work extends to formal causal explanations

**Concept Bottleneck Models (CBMs)** - Explicitly constrain models to operate through semantic concepts; this work's formalism could apply to understanding CBM predictions

**SISA (Semantic Importance Similarity Attention)** - Proposes similarity-based concept relevance; this work takes a more formal causal approach

**ProtoTree & Case-Based Models** - Use prototypical examples as explanations; this work's minimality principle relates to prototype selection

### Formal Explanation Methods

**Abductive and Contrastive Explanations at Pixel Level** - Prior work formalized these concepts for feature-level explanations; this paper extends to semantically-meaningful concepts

**Symbolic XAI** - Methods using logical reasoning and formal methods for explanation; this work bridges symbolic and connectionist approaches

**Causal Interpretability** - Methods establishing causal relationships in neural networks; ConAXps/ConCXps provide a concrete instantiation of causal concepts

### Related Concept-Based XAI Work

1. **Concept Bottleneck Models (CBMs)**: Constrain models to operate explicitly through human-defined concepts, enabling transparent decision-making. This paper's methods could enhance CBM interpretability.

2. **Attention-Based Concept Discovery**: Methods like ACE (Automated Concept-based Explanations) automatically discover concepts from model activations. This work's formal framework applies to discovered concepts.

3. **Semantic Segmentation for Explanations**: Uses segmentation masks to identify concept regions. ConAXps/ConCXps could provide formal evaluation of these regional explanations.

### Broader XAI Landscapes

This work fits within broader xAI research addressing:
- **Feature Attribution Methods** (SHAP, LIME): This work operates at higher semantic levels
- **Saliency and Attention Visualization**: Complements visual explanations with formal semantic grounding
- **Model Distillation and Surrogate Models**: Alternative approach; this work analyzes original model directly

### Connection to XAI Communities

- **Mechanistic Interpretability Community**: Shares goal of understanding internal model computations; operates at different levels (circuits vs. concepts)
- **Fairness and Bias Research**: Concept-based explanations enable identifying bias sources at semantic level
- **Neuroscience-Inspired AI**: Concepts parallel how neuroscience interprets neural populations in biological brains

### Future Research Directions

1. **Concept Emergence and Learning**: Understanding how concepts emerge during training and evolve with model updates

2. **Concept Algebras**: Formalizing how concepts combine and interact (e.g., concept unions, intersections, hierarchies)

3. **Dynamic Explanations**: Extending ConAXps/ConCXps to temporal and sequential models (video, time series, language)

4. **Multi-Modal Concept Interactions**: Understanding how concepts interact across vision, language, and other modalities

5. **Explanation Debugging**: Developing methods to verify that explanations are correct and not artifacts of the explanation method itself

## References and Further Reading

**ArXiv Paper Link:** https://arxiv.org/abs/2605.06640

**Full HTML Version:** https://arxiv.org/html/2605.06640v1

**PDF Version:** https://arxiv.org/pdf/2605.06640

## Conclusion

"Concept-Based Abductive and Contrastive Explanations for Behaviors of Vision Models" provides a rigorous formal framework for understanding neural network predictions through high-level semantic concepts. By extending established formal explanation methods from the pixel level to the concept level, the paper advances the theoretical foundations of explainable AI and provides practical tools for trustworthy, interpretable vision systems. The work's emphasis on minimality, causal grounding, and formal verification positions it as an important step toward AI systems that can explain themselves in terms humans can understand and act upon.
