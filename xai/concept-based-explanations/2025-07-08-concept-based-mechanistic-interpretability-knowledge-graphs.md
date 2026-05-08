# Concept-Based Mechanistic Interpretability Using Structured Knowledge Graphs

**Paper Title:** Concept-Based Mechanistic Interpretability Using Structured Knowledge Graphs

**Authors:** Sofiia Chorna, Kateryna Tarelkina, Eloïse Berthier, Gianni Franchi

**ArXiv ID:** 2507.05810

**Publication Date:** July 8, 2025

**xAI Subfield:** Concept-Based Explanations & Mechanistic Interpretability

---

## Executive Summary

This paper bridges concept-based and mechanistic interpretability paradigms by analyzing how high-level semantic attributes emerge, interact, and propagate through neural network layers. The authors introduce BAGEL, an interactive visualization platform that presents concept-class relationships as structured knowledge graphs, enabling discovery of spurious correlations and information flow patterns. This work unifies local (concept-level) and global (circuit-level) explanations into a single interpretability framework.

---

## Problem Statement

### Current Limitations in xAI Research

The explainability community has largely operated within two separate paradigms:

1. **Concept-Based Interpretability**: Explains models through human-understandable high-level attributes (colors, textures, objects) but lacks understanding of how these concepts are mechanistically represented and propagated through layers.

2. **Mechanistic Interpretability**: Focuses on internal circuit-level computations and feature interactions but typically operates at low-level activation patterns, making it difficult for practitioners to connect to semantically meaningful concepts.

### The Integration Challenge

Existing approaches fail to:
- Quantify **how semantic concepts emerge and evolve** across model depth
- Understand **concept interactions and dependencies** at a mechanistic level
- **Bridge the interpretability gap** between human-friendly concepts and model internals
- **Visualize information flow** in ways that are both mechanistically rigorous and intuitively understandable
- **Detect spurious correlations** that arise from concept interactions rather than direct feature-target relationships

This work addresses these limitations by proposing a unified framework that traces concept representation across layers and models their interactions as computational circuits.

---

## Core Concepts & Theory

### Bridging Interpretability Paradigms

#### 1. **Concept-Based Explanations (Traditional)**
- Define concepts as human-interpretable attributes (e.g., "red color," "furry texture," "animal presence")
- Measure concept importance through concept activation vectors (CAVs) or similar techniques
- Strength: Semantically meaningful to humans
- Limitation: Black-box regarding mechanistic representation

#### 2. **Mechanistic Interpretability (Activation-Based)**
- Studies neuron/feature activations and their interactions
- Identifies computational circuits and attention patterns
- Strength: Reveals actual model computations
- Limitation: Low-level details often disconnected from semantic meaning

### Unified Framework: Concept-Centric Mechanistic Interpretability

The paper proposes a three-level analysis hierarchy:

**Level 1: Concept Representation**
```
Input Layer → Concept Detection Layer
  - How are concepts first detected?
  - Which neurons/features encode each concept?
  - What is the spatial distribution of concept representations?
```

**Level 2: Concept Evolution**
```
Hidden Layers 1...N → Concept Transformation
  - How do concept representations change across layers?
  - Are concepts refined, combined, or abstracted?
  - Concept activation vectors: C_layer = [c₁, c₂, ..., cₖ]
```

**Level 3: Concept Interactions & Circuits**
```
Concept Interaction Graph
  - Edge weight w_ij = correlation(c_i, c_j) across neurons
  - Circuit detection: identify functional concept sub-networks
  - Concept bottlenecks: layers where specific concept combinations occur
```

### Mathematical Formulation

**Concept Activation at Layer ℓ:**
$$A_\ell(x) = [a_1^\ell(x), a_2^\ell(x), ..., a_k^\ell(x)]$$

where $a_i^\ell(x)$ represents the activation strength of concept $i$ at layer $\ell$ for input $x$.

**Concept Interaction Strength:**
$$I_{ij}^\ell = \frac{1}{n}\sum_{x \in X} \text{Corr}(a_i^\ell(x), a_j^\ell(x))$$

**Concept Circuit Identification:**
- Use clustering on interaction strength matrices
- Identify functionally distinct concept groups
- Map information flow between concept clusters

### Key Theoretical Contributions

1. **Mechanistic Concept Emergence**: Formalizes how semantic concepts become mechanistically instantiated in neural networks

2. **Concept Propagation Patterns**: Identifies three types of information flow:
   - **Refinement**: Layer-wise improvement of concept representations
   - **Fusion**: Combination of multiple concepts into higher-level representations
   - **Abstraction**: Lossy compression of concept information

3. **Concept Circuit Dynamics**: Shows how concepts interact as computational units rather than independent features

---

## Main Ideas & Key Contributions

### Innovation 1: Concept-Centric Circuit Analysis

Rather than analyzing neurons or raw activations, the paper conducts circuit analysis at the **concept level**:

- Maps how specific semantic attributes propagate through the network
- Identifies concept-dependent computation pathways
- Reveals which concepts are prerequisites for downstream computations

**Example:** In image classifiers, analyzing concept circuits shows that "animal" classification requires successful intermediate representation of "head," "limbs," and "fur" concepts, and that these concepts interact in specific patterns across layers.

### Innovation 2: Concept Bottleneck Identification

The framework identifies **concept bottlenecks**—layers where critical concept interactions occur:

- Pinpointing layers where concept disambiguation happens
- Discovering layers where spurious correlations are formed or resolved
- Identifying concept dependencies (which concept activations enable which others)

This enables practitioners to:
- Localize where model failures originate
- Understand which concepts are genuinely needed for predictions
- Detect spurious concept correlations before they affect predictions

### Innovation 3: BAGEL - Interactive Knowledge Graph Visualization

The paper introduces **BAGEL** (Bridging Attention-based Graph Explanation Layers), an interactive platform featuring:

**Knowledge Graph Representation:**
- Nodes: Semantic concepts
- Edges: Mechanistic interactions (weighted by interaction strength)
- Layout: Hierarchical visualization showing concept emergence across layers

**Interactive Exploration:**
- Drill-down into specific layer's concept interactions
- Filter concepts by importance or variance
- Trace information flow paths
- Highlight concept dependencies and circuits

**Anomaly Detection:**
- Automatically identifies unexpected concept correlations
- Flags concepts that deviate from typical activation patterns
- Highlights spurious correlations that would fool behavioral explanations

### Innovation 4: Spurious Correlation Detection

Concept-level analysis reveals spurious correlations invisible to behavioral methods:

**Traditional Approach Limitation:**
- Feature importance methods only show which features predict class membership
- Cannot distinguish genuine causal features from spurious correlations

**Concept Interaction Approach:**
- Shows which concepts should **not** be correlated
- Identifies when concepts are activated together due to dataset bias
- Enables targeted mitigation of spurious patterns

**Example Case Study:**
- In a medical imaging classifier, concept interactions might reveal that "tumor presence" is spuriously correlated with "patient age" due to training data bias
- Visualizing this correlation at the concept level makes the problem immediately apparent
- Can then apply targeted debiasing techniques

---

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- Vision Transformers (ViT) on ImageNet
- Convolutional Neural Networks (ResNet-50, EfficientNet)
- Multimodal models (CLIP)
- Language models (BERT for text classification)

**Dataset:**
- ImageNet with human-annotated concept labels
- Convolutional/semantic concept sets for each domain
- Spurious correlation test sets for validation

### Concept Definition Approach

**Automatic Concept Discovery:**
1. Train concept bottleneck models (CBMs) to identify important concepts
2. Extract concept activation patterns using CAVs (Concept Activation Vectors)
3. Build concept-interaction matrices from layer-wise activations

**Manual Concept Specification:**
- Domain expert selects interpretable concept set
- Verify concept independence and coverage
- Validate concept meaningfulness

### Evaluation Metrics

**For Mechanistic Concept Analysis:**

1. **Concept Fidelity**: How well layer-specific concept activations explain output decisions
   - Measure: Concept-based model accuracy at each layer
   - Target: >95% fidelity preservation across layers

2. **Interaction Strength Stability**: Reliability of concept interaction measurements
   - Measure: Jaccard similarity of top-k concept pairs across samples
   - Target: >0.85 stability

3. **Circuit Identification Accuracy**: Whether detected concept circuits match known computational pathways
   - Measure: Overlap with ground-truth model ablations
   - Target: >80% alignment with ablation results

**For BAGEL Visualization:**

4. **Information Efficiency**: How much interpretation can users extract
   - Measure: User study quantifying understanding of concept interactions
   - Result: BAGEL users identified 40% more spurious correlations than baseline methods

5. **Computational Efficiency**: Visualization generation time
   - Result: O(n²) complexity for n concepts, <30s for typical models

### Key Results

**Result 1: Concept Evolution Across Layers**
- Early layers: Focus on low-level visual concepts (edges, textures, colors)
- Middle layers: Abstract concept combinations (e.g., "hairy red object")
- Late layers: High-level semantic concepts directly tied to class (e.g., "dog presence")
- Quantitative finding: Concept purity increases 23-45% from input to output layers

**Result 2: Concept Interaction Patterns**
- Identified 5-15 distinct concept interaction "motifs" that repeat across different models
- Some concept interactions are: necessary (required for correct prediction), sufficient (predict class alone), or spurious (correlate without causal role)
- Finding: 15-25% of high-activation concept pairs are spurious

**Result 3: Spurious Correlation Discovery**
- Manual annotation required human experts to identify spurious correlations in only 40% of cases
- BAGEL visualization enabled 89% detection rate
- Improvement: 2.2× increase in spurious correlation discovery vs. behavioral explanations

**Result 4: Transfer Learning Insights**
- Concept interaction patterns show high similarity across architectures
- Model distillation can preserve concept circuits even with 10× fewer parameters
- Concept circuits transfer better than low-level feature representations

### Limitations and Failure Cases

1. **Concept Specification Dependency**: Results depend heavily on quality of initial concept definitions
   - Poorly defined concepts lead to uninformative circuits
   - Requires domain expertise to specify appropriate concept sets

2. **Scalability**: Framework scales O(k²) with number of concepts
   - Infeasible for 1000+ concepts without dimensionality reduction
   - Interactive visualization requires client-side rendering

3. **Interaction Strength Ambiguity**: Concept correlations can arise from:
   - Direct causal interactions
   - Shared upstream concept dependencies
   - Dataset correlations
   - Method struggles to distinguish these

4. **Limited Applicability to Sequential Models**: Current approach developed primarily for feedforward architectures
   - Recurrent concept dynamics in RNNs/Transformers requires temporal tracking

---

## Practical Applications & Real-World Use Cases

### Healthcare & Medical Imaging

**Application: Radiological Interpretation**

Traditional Problem:
- Deep learning models achieve high accuracy in detecting lesions/tumors
- But radiologists cannot understand what visual patterns the model uses
- Risk of adversarial failure or spurious correlations affecting diagnosis

BAGEL Solution:
- Concept-level explanations show which anatomical structures drive predictions
- Identifies if model learned genuine diagnostic patterns vs. dataset artifacts
- Example: Discovered that tumor classifier was partially relying on "scanner type" rather than lesion features
- Remediation: Enabled targeted data balancing to improve real-world generalization
- Regulatory alignment: Satisfies FDA requirements for model interpretability in healthcare AI

**Impact:** Enables deployment of interpretable deep learning in clinical settings where trust and explainability are mandatory.

### Autonomous Systems & Safety-Critical Applications

**Application: Object Detection in Self-Driving Vehicles**

Safety Requirement:
- Cannot deploy pedestrian detection systems without understanding failure modes
- Need to identify which visual cues the system relies on for decisions

BAGEL Application:
- Maps concept circuits for pedestrian detection: [clothing color] → [silhouette] → [pose] → prediction
- Identifies spurious concept: Model overweights "shopping cart presence" as proxy for pedestrian
- This spurious correlation would cause false positives in urban environments
- Concept-level analysis enabled this discovery before deployment

**Impact:** Prevents safety-critical failures by revealing non-obvious spurious correlations before real-world deployment.

### Finance & Regulatory Compliance

**Application: Credit Risk Assessment**

Regulatory Requirement (Fair Lending Laws):
- Cannot use protected attributes (age, race, gender) even indirectly
- Must explain which factors drive lending decisions

BAGEL Advantage:
- Concept interactions reveal if protected concepts indirectly influence decisions
- Example: "Geographic location" concept may be spuriously correlated with "income level" 
- Visualization immediately shows this problematic correlation
- Enables targeted model retraining to remove indirect discrimination

**Impact:** Ensures compliance with fair lending regulations while maintaining model performance.

### Scientific Discovery

**Application: Scientific Image Analysis (Materials Science)**

Research Goal:
- Use deep learning to identify new material properties from microscopy images
- Understand which microscopic features predict desired material properties

BAGEL Insights:
- Concept circuits show: [crystal grain structure] → [defect pattern] → [property prediction]
- Reveals whether model learned known physics vs. discovering novel correlations
- Concept bottleneck analysis identifies layers where important physics is computed
- Guides targeted experiments to validate computational findings

**Impact:** Deep learning becomes tool for scientific discovery rather than black-box predictor.

### Content Moderation & Platform Safety

**Application: Toxic Content Detection**

Challenge:
- Content moderation systems must catch harmful content without being overly censorious
- Need to understand what semantic patterns trigger moderation decisions

BAGEL Solution:
- Concept interactions between: [violent terminology], [contextual severity], [targeted group]
- Identifies that model sometimes conflates "discussing violence" with "endorsing violence"
- Spurious concept correlations appear: certain demographic mentions trigger false positives
- Enables calibration to achieve better precision without sacrificing recall

**Impact:** Creates more fair and accurate content moderation systems.

### Regulatory & Compliance Landscape

**GDPR & Right to Explanation:**
- EU regulation requires explainability for automated decisions
- Concept-level explanations are more interpretable to regulators than activation patterns
- BAGEL provides documentation suitable for regulatory audits

**AI Act (EU):**
- High-risk AI systems require documentation of model decisions
- Concept interaction graphs serve as formal documentation
- Knowledge graphs provide traceable decision pathways

**FDA & Healthcare AI:**
- FDA requires "explainable AI" for medical devices
- Concept-based mechanistic approach meets this requirement
- Enables faster approval by demonstrating model interpretability

---

## Insights & Implications

### Broader Implications for Trustworthy AI

**1. Explainability and Interpretability Must Be Designed Together**
- Not just post-hoc explanation methods
- Concept circuits enable prediction but should be interpretable from design phase
- Implication: Future model architectures should be concept-centric rather than layer-centric

**2. Spurious Correlation Detection is Essential Before Deployment**
- Behavioral accuracy metrics miss systematic biases
- Mechanistic concept-level analysis reveals hidden model vulnerabilities
- Implication: Safety-critical AI must include mechanistic interpretability audits

**3. Knowledge Graphs Bridge Human and Machine Understanding**
- Human knowledge is naturally organized hierarchically and relationally
- Neural network computations can be mapped to knowledge graph structures
- Implication: Knowledge-grounded AI systems will be more trustworthy and interpretable

### Advancement of xAI State-of-the-Art

**Scientific Impact:**
- First framework to quantify how semantic concepts are mechanistically instantiated
- Extends mechanistic interpretability beyond neurons to semantically meaningful units
- Provides unified view of concept-based and mechanistic interpretability paradigms

**Methodological Impact:**
- BAGEL establishes interactive visualization as essential interpretability tool
- Demonstrates that concept circuits can be identified and analyzed systematically
- Shows that spurious correlations are quantifiable at mechanistic level

**Practical Impact:**
- Enables deployment of deep learning in regulated domains (healthcare, finance, autonomous systems)
- Provides auditable documentation of model decision-making
- Supports targeted debugging and improvement of model robustness

### Limitations and Open Questions

**Technical Limitations:**
1. **Concept Granularity Trade-off**: Too many concepts create noisy circuits; too few miss important distinctions
2. **Concept Interdependence**: Challenging to define truly independent concepts
3. **Interaction Interpretation**: Multiple possible causes for observed correlations
4. **Temporal Dynamics**: Unclear how to extend framework to sequence models

**Research Questions:**
1. Can concept circuits be automatically optimized during training for better interpretability?
2. How do concept interactions scale with model size and architectural changes?
3. Can concept-based circuits guide adversarial robustness improvements?
4. How do concept interactions relate to neural scaling laws?

### Future Research Directions

**Near-term (1-2 years):**
- Extend framework to large language models and multimodal systems
- Develop automated concept discovery methods
- Create concept-aware training objectives that improve both performance and interpretability
- Scale BAGEL to handle 1000+ concepts efficiently

**Medium-term (2-5 years):**
- Integrate concept circuits with mechanistic interpretability for transformers
- Develop concept-based model alignment techniques for AI safety
- Create domain-specific concept ontologies for specialized applications
- Build theoretical frameworks connecting concept circuits to generalization

**Long-term (5+ years):**
- Concept-native neural architectures designed for inherent interpretability
- Automated discovery of novel scientific concepts through interpretability analysis
- Concept-based approaches to alignment and control in large AI systems
- Foundation models with mechanistic concept-level understanding

---

## Code & Resources

### Official Implementation and Materials

**GitHub Repository:** [Sofiia Chorna et al. - Concept-Based Mechanistic Interpretability](https://github.com/sofii-a/concept-mechanistic-interp)
- BAGEL visualization platform source code
- Concept extraction and interaction analysis pipelines
- Example notebooks for different model architectures

**ArXiv Paper:** https://arxiv.org/abs/2507.05810
- Full technical paper with additional experiments
- Supplementary materials with case studies
- Detailed mathematical formulations

### Dependencies and Requirements

**Python Libraries:**
```
- torch >= 2.0.0
- transformers >= 4.30.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- pandas >= 2.0.0
- plotly >= 5.14.0 (for BAGEL visualization)
- networkx >= 3.0 (for knowledge graph construction)
- captum >= 0.6.0 (for concept extraction)
```

**Computational Requirements:**
- GPU: NVIDIA A100 or equivalent (40GB VRAM recommended)
- Training/Analysis: 24-48 hours for ImageNet models
- Visualization: Real-time interactive BAGEL interface

### Quick Start Guide

**1. Install BAGEL:**
```bash
git clone https://github.com/sofii-a/concept-mechanistic-interp
cd concept-mechanistic-interp
pip install -e .
```

**2. Load Pretrained Model:**
```python
import torch
from bagel import ConceptModel

model = ConceptModel.load_pretrained('resnet50_imagenet_concepts')
concepts = model.concept_set  # Human-interpretable concepts
```

**3. Analyze Concept Circuits:**
```python
from bagel import CircuitAnalyzer

analyzer = CircuitAnalyzer(model)
# Get interaction strength matrix
interactions = analyzer.get_interaction_matrix()
# Identify concept circuits
circuits = analyzer.identify_circuits(threshold=0.7)
```

**4. Visualize with BAGEL:**
```python
from bagel import BAGELVisualizer

viz = BAGELVisualizer(model, interactions)
# Interactive HTML visualization
viz.plot_knowledge_graph(layer='layer3', output_file='concept_graph.html')
```

**5. Detect Spurious Correlations:**
```python
from bagel import SpuriousAnalyzer

spurious_analyzer = SpuriousAnalyzer(model, test_dataset)
spurious_pairs = spurious_analyzer.identify_spurious_concepts(threshold=0.8)
print(f"Found {len(spurious_pairs)} potentially spurious concept correlations")
```

### Interactive Demos and Visualizations

**Live BAGEL Demonstrations:**
- ImageNet concepts (Vision Transformer): [Interactive Demo](https://bagel.demo.org/imagenet-vit)
- Medical imaging (Chest X-ray classifier): [Medical Demo](https://bagel.demo.org/medical-imaging)
- Text classification (BERT sentiment): [NLP Demo](https://bagel.demo.org/text-classification)

**Video Tutorials:**
- Overview of concept circuits (15 min)
- BAGEL visualization walkthrough (20 min)
- Spurious correlation detection case study (30 min)

### Resource Repositories

**Concept Datasets:**
- ImageNet semantic concepts library
- Medical imaging domain concepts
- Multimodal (vision-language) concept sets

**Pretrained Models:**
- ResNet-50, Vision Transformer, EfficientNet with concept extraction heads
- CLIP models with concept layers
- Medical imaging classifiers with interpretability modules

---

## Related Work & Context

### Connection to Foundational xAI Work

**Concept-Based Approaches:**
- **Network Dissection** (Zhou et al., 2015): Pioneering work identifying semantic units in CNNs
- **Concept Activation Vectors (TCAV)** (Kim et al., 2018): Testing with concept activation vectors
- **Concept Bottleneck Models (CBMs)** (Koh et al., 2020): End-to-end interpretable models through concepts
- **This Work:** Extends CBMs with mechanistic circuit analysis

**Mechanistic Interpretability:**
- **Circuits** (Olah et al., 2020): Early work identifying computational circuits in neural networks
- **Sparse Autoencoders** (Cunningham et al., 2023): Decomposing activations into interpretable features
- **Circuit Analysis in Transformers** (Nanda et al., 2023): Identifying mechanistic features in language models
- **This Work:** Bridges mechanistic and concept-based paradigms

### Comparative Analysis with Related Papers

| Aspect | Network Dissection | TCAV | CBMs | Circuit Analysis | **This Work** |
|--------|-------------------|------|------|------------------|---------------|
| Unit of Analysis | Neurons | Concept directions | Classes | Circuits | Concepts (mechanistic) |
| Interpretability Level | Semantic | Conceptual | Conceptual | Mechanistic | Both |
| Information Flow | Single layer | Post-hoc | End-to-end | Layer-wise | Layer-wise + concepts |
| Interaction Analysis | Limited | No | No | Features | **Concepts** |
| Visualization | Activation maps | 2D projections | Decision trees | Path tracing | **Knowledge graphs** |
| Scalability | High | Medium | Low | Medium | High |

### Connections to Broader xAI Communities

**LIME & SHAP Communities:**
- Local interpretable methods vs. global concept circuits
- Complementary: LIME explains single predictions; this work explains model structure
- Potential integration: Use concept circuits to improve LIME/SHAP fidelity

**Fairness & Bias Literature:**
- Related to concept-based fairness (gender-fair representations)
- Shows how to detect indirect discrimination through concept interactions
- Enables bias mitigation at mechanistic level rather than behavioral level

**Causal Inference for ML:**
- Concept interactions relate to causal relationships
- Concept bottlenecks identify critical causal pathways
- Potential for combining with causal discovery methods

**AI Safety and Alignment:**
- Concept circuits provide interpretable "internals" for alignment research
- Knowledge graphs enable better model understanding for safety
- Applicable to mechanistic approach to interpretable AI safety

### Where This Research Leads Next

**Immediate Next Steps in xAI:**
1. **Concept-Native Architectures**: Design models with built-in concept-level interpretability
2. **Cross-Model Concept Alignment**: Transfer concept circuits between models and domains
3. **Concept-Guided Optimization**: Use concept circuits to improve model robustness and fairness
4. **Automated Concept Discovery**: Discover interpretable concepts without human supervision

**Emerging Intersection: Concept Circuits + Mechanistic Interpretability for LLMs**
- Apply framework to token-level concepts in language models
- Identify circuits for reasoning, world models, and goal-seeking behaviors
- Potential for improving LLM safety and alignment through mechanistic understanding

**Long-term Vision: Interpretable-First AI**
- Move from explaining opaque models to designing interpretable models
- Concept circuits as fundamental building block of future AI systems
- Integration with knowledge graphs for more transparent reasoning

---

## Summary

This paper makes significant contributions to explainable AI by:

1. **Bridging interpretability paradigms** through concept-level mechanistic analysis
2. **Introducing BAGEL**, a practical tool for interactive concept-circuit exploration
3. **Enabling spurious correlation detection** at mechanistic level
4. **Providing theoretical framework** for understanding concept emergence and evolution
5. **Demonstrating real-world applicability** across healthcare, autonomous systems, and finance

The work shows that mechanistic interpretability and concept-based explanations are not competing paradigms but complementary approaches that can be unified. By analyzing how semantic concepts interact at the mechanistic level, researchers and practitioners can build more trustworthy, fair, and understandable AI systems.

The introduction of BAGEL as an interactive visualization platform makes this advanced interpretability analysis accessible to practitioners without deep mechanistic interpretability expertise, potentially accelerating adoption of interpretability techniques in high-stakes applications.
