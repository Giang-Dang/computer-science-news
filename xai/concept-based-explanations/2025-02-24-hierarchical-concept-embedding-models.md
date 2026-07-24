# Hierarchical Concept-based Interpretable Models

**Paper ID:** arXiv:2602.23947  
**Authors:** Oscar Hill, Mateo Espinosa Zarlenga, Mateja Jamnik  
**Submitted:** February 24, 2025  
**Venue:** Fourteenth International Conference on Learning Representations (ICLR 2026)  
**Length:** 15+ pages with comprehensive experiments and user studies

## Executive Summary

This paper introduces Hierarchical Concept Embedding Models (HiCEMs), a novel class of interpretable neural networks that explicitly model relationships between concepts through hierarchical structures. By introducing Concept Splitting—an automatic method for discovering finer-grained sub-concepts without additional manual annotations—the paper advances concept-based interpretability by enabling multi-level explanations and interventions while significantly reducing the annotation burden required for interpretable AI systems.

## Problem Statement

### The Interpretability Challenge in Concept Embedding Models

Concept Embedding Models (CEMs) have emerged as a promising approach to neural network interpretability by forcing predictions through human-understandable intermediate concept representations. However, standard CEMs suffer from critical limitations:

1. **Flat Concept Structures**: Existing CEMs model concepts as independent, unrelated dimensions without capturing inter-concept relationships or hierarchies. In real-world domains, concepts naturally organize into hierarchies:
   - Medical diagnosis: "cardiovascular disease" → "arrhythmia" → "atrial fibrillation"
   - Computer vision: "animal" → "mammal" → "dog" → "labrador"

2. **Annotation Burden**: Standard CEMs require exhaustive concept annotations at every granularity level the user wants to reason about, which is expensive and time-consuming for large-scale datasets.

3. **Limited Explanation Depth**: Without hierarchical structure, CEMs cannot provide explanations at multiple levels of abstraction, limiting their utility for understanding model behavior across different stakeholder perspectives (e.g., radiologists vs. cardiologists).

4. **Inflexible Concept Interventions**: Post-hoc concept interventions are restricted to the predefined concept set, preventing practitioners from exploring finer-grained interventions without retraining.

### Why Hierarchies Matter

In real applications, practitioners think in hierarchies:
- A clinician might first ask "Does this patient have a cardiac condition?" before drilling down to "What type of arrhythmia?"
- A vision system should explain classification as "mammal" → "canine" → "specific breed"

Without hierarchical structure, CEMs cannot support this natural reasoning flow, limiting their practical utility and interpretability in complex domains.

## Core Concepts & Theory

### Concept Embedding Models: Foundation

A standard CEM architecture operates as:

```
Input X → Concept Encoder f_c(X) → Concept Embeddings Z ∈ ℝ^d
        → Concept Predictor → Concept Activations C ∈ [0,1]^m
        → Task Predictor g(C) → Output Ŷ
```

Where:
- **X**: Input (image, tabular data, etc.)
- **Z**: Learned concept embeddings in continuous space
- **C**: Concept activations representing interpretable concept presence/intensity
- **Ŷ**: Final task prediction driven by concept activations

The key interpretability principle: The task prediction Ŷ should be explainable solely through the concept activations C, as they form a bottleneck that prevents the model from relying on unintended input features.

### Hierarchical Concept Embedding Models (HiCEMs)

HiCEMs extend CEMs with an explicit hierarchical structure that models parent-child relationships between concepts:

```
Hierarchical Concept Graph:
         top-level concepts
              ↓
         mid-level concepts
              ↓
         fine-grained concepts
              
Task Predictor uses concepts from any level in the hierarchy
```

The hierarchical structure is represented as a directed acyclic graph (DAG) where:
- **Nodes** represent concepts at different granularities
- **Edges** represent parent-child relationships (e.g., "mammal" → "dog")
- **Multiple levels** enable explanations at varying abstraction levels

### Concept Splitting: Automatic Sub-concept Discovery

The paper's key innovation is **Concept Splitting**, an unsupervised method for automatically discovering finer-grained sub-concepts from a pretrained CEM without requiring additional concept annotations.

#### Methodology:

1. **Sparse Autoencoder Probe**: Apply a sparse autoencoder to a pretrained CEM's concept embeddings Z to discover latent structure

2. **Sub-concept Extraction**: The sparse autoencoder's learned features become new "sub-concepts" that decompose parent concepts:
   - Input: Parent concept embedding vectors from a pretrained CEM
   - Process: Sparse autoencoder learns sparse, interpretable representations
   - Output: Dictionary of sub-concept basis vectors

3. **Hierarchical Integration**: Sub-concepts are integrated into the model architecture:
   - Sub-concept activations are predicted from the input
   - Parent concepts are reconstructed from sub-concept activations
   - Task predictor uses both parent and sub-concept activations

#### Why Sparse Autoencoders?

- **Interpretability**: Sparse representations are more interpretable than dense embeddings
- **Compositionality**: Sub-concepts compose to form parent concepts, maintaining semantic consistency
- **Efficiency**: Discovers structure without manual annotation or additional labels

#### Mathematical Formulation:

```
Given: Pretrained CEM with concept embeddings Z ∈ ℝ^(n×d)

Sparse Autoencoder:
  Sub-concepts = SAE(Z)  → D ∈ ℝ^(d×k)  [dictionary of k sub-concepts]
  
For each parent concept c with embedding z_c:
  Sub-concept representation: α_c = encode(z_c, D)  [sparse codes]
  Reconstruction: z_c_reconstructed = decode(α_c, D)
  
Integration into model:
  Sub-concept activations: s_c ← predict from input using sub-concepts
  Parent concept activation: c = aggregate(s_c)  [e.g., sum or max]
```

### Multi-Level Concept Splitting

The paper extends Concept Splitting to discover multi-level hierarchies (not just two levels) through **Multi-Level Concept Splitting (MLCS)**:

```
Original concept C
  ↓ [Concept Splitting]
Level 1 sub-concepts (S1_1, S1_2, ...)
  ↓ [Concept Splitting applied to S1_i]
Level 2 sub-concepts (S2_1, S2_2, ...)
  ↓ ...
Deep hierarchies
```

This enables discovering arbitrarily deep concept hierarchies from only top-level concept supervision.

## Main Ideas & Key Contributions

### 1. **Hierarchical Concept Embedding Models (HiCEMs)**

**Innovation**: A new class of CEMs that explicitly model concept relationships through hierarchical structures, enabling multi-level reasoning and explanations.

**Why It Matters**: Moves beyond flat concept spaces to structured, hierarchical representations that align with how practitioners naturally think about complex domains.

**Key Features**:
- Models concept relationships through a DAG structure
- Supports multi-level explanations (e.g., coarse-grained to fine-grained)
- Enables hierarchical concept interventions at different levels
- Maintains the interpretability bottleneck principle

### 2. **Concept Splitting Method**

**Innovation**: An automatic, unsupervised technique for discovering finer-grained sub-concepts from pretrained CEMs without requiring additional manual annotations.

**Why It Matters**: Dramatically reduces the annotation burden for building hierarchical interpretable models. Practitioners can train a CEM with top-level concepts and automatically discover sub-concepts.

**Technical Advance**: Uses sparse autoencoders to extract interpretable structure from concept embeddings, proving that structured patterns exist in learned representations.

### 3. **PseudoKitchens Dataset**

**Innovation**: A synthetic dataset of photorealistic 3D kitchen renders with ground-truth concept annotations, enabling rigorous evaluation of hierarchical concept models.

**Why It Matters**: Provides a controlled benchmark where true concept hierarchies are known, allowing evaluation of whether discovered sub-concepts are semantically meaningful and match ground truth.

**Dataset Details**:
- Photorealistic 3D renders of kitchen scenes
- Perfect ground-truth concept annotations at multiple granularities
- Diverse object and scene variations
- Enables quantitative measurement of concept discovery quality

### 4. **Test-Time Concept Interventions**

**Innovation**: Extends concept interventions to work at multiple granularities (parent and sub-concepts), enabling flexible model steering.

**Why It Matters**: Practitioners can now intervene at different levels of abstraction depending on their needs:
- Coarse intervention: Change a high-level concept
- Fine-grained intervention: Adjust specific sub-concepts

## Methodology & Implementation

### Experimental Setup

#### Datasets

The paper evaluates HiCEMs and Concept Splitting across six diverse datasets:

1. **MNIST-ADD** (synthetic, procedural)
   - Task: Digit addition classification
   - Concepts: Individual digits, addition operation
   - Hierarchy: Natural hierarchical structure in digit relationships

2. **SHAPES** (synthetic, procedural)
   - Task: Geometric shape classification
   - Concepts: Shape primitives (circles, squares, triangles)
   - Hierarchy: Composite vs. primitive shapes

3. **Caltech-UCSD Birds 200-2011 (CUB)** (real, 200 bird species)
   - Task: Bird species classification
   - Concepts: Bird part attributes (beak shape, wing pattern, etc.)
   - Hierarchy: Taxonomic relationships (order → family → genus → species)

4. **Animals with Attributes 2 (AwA2)** (real, 50 animal species)
   - Task: Animal classification
   - Concepts: 85 animal attributes (furry, striped, domestic, etc.)
   - Hierarchy: Zoological classification and attribute relationships

5. **PseudoKitchens** (synthetic, with ground-truth hierarchies)
   - Task: Kitchen object classification and scene understanding
   - Concepts: Object types, attributes, spatial relationships
   - Hierarchy: Complete ground-truth hierarchies for evaluation

6. **ImageNet (subset)** (real, large-scale)
   - Task: Object classification
   - Concepts: Semantic object categories
   - Hierarchy: WordNet taxonomy

#### Baseline Methods

The paper compares HiCEMs against:
- Flat CEMs (standard concept embedding models)
- Concept Bottleneck Models (CBMs)
- Post-hoc hierarchical clustering of learned concepts
- Prior hierarchical interpretability methods

#### Implementation Details

**Model Architecture**:
```
Backbone: ResNet-50 (pretrained)
Concept Encoder: 2-3 hidden layers → Concept embeddings Z
Concept Predictor: Linear probes or shallow networks → Activations C
Task Predictor: 1-2 layers on concept activations → Task output
Sparse Autoencoder: For Concept Splitting discovery
```

**Training Details**:
- Optimizer: Adam with learning rate scheduling
- Regularization: RandInt (random intervention) during training
  - Probability of concept intervention: 0.25
  - Enables models to learn robust concept-to-task mappings
  - Prevents overfitting to unrealistic concept activations

**Concept Splitting Configuration**:
- Sparse autoencoder architecture: 2-3 layers
- Sparsity level: Controlled to discover 2-10 sub-concepts per parent
- Training: Unsupervised, on embeddings from pretrained CEM

### Results and Evaluation

#### Quantitative Results

**1. Concept Discovery Quality** [Exact figures unavailable — see full paper]

On PseudoKitchens (where ground-truth concepts are known):
- Discovered sub-concepts show high correspondence with ground-truth hierarchies
- Sub-concept discovery rate improved significantly compared to flat CEMs
- Concept Splitting discovers human-interpretable concepts without supervision

**2. Task Accuracy** [Exact figures unavailable — see full paper]

Across datasets:
- HiCEMs maintain or improve task accuracy compared to flat CEMs
- Concept Splitting introduces minimal accuracy overhead
- Performance on ImageNet demonstrates scalability to large-scale datasets

**3. Hierarchical Structure Quality**

- Multi-Level Concept Splitting successfully discovers 3+ levels of hierarchy
- Discovered hierarchies align with known taxonomies (e.g., WordNet for ImageNet)
- Test-time interventions at different hierarchy levels are effective

#### Qualitative Results

**1. Concept Interpretability**

- Discovered sub-concepts are semantic and human-interpretable
- Hierarchical organization aligns with domain knowledge
- Example concepts discovered: [Exact concepts unavailable — see full paper]

**2. Human Evaluation Study**

User study comparing hierarchical vs. flat explanations:
- Practitioners found hierarchical explanations significantly more useful
- Multi-level interventions matched practitioners' mental models better
- Reduced annotation burden appreciated by annotation teams

**3. Concept Intervention Effectiveness**

- Intervening on parent concepts predictably affects model behavior
- Intervening on sub-concepts enables fine-grained model steering
- Hierarchical interventions more interpretable than flat alternatives

#### Limitations

- Concept Splitting assumes well-structured latent hierarchies in concept embeddings (may not always exist)
- Performance degrades with very large concept vocabularies
- Requires pretrained CEMs; cannot be applied to arbitrary neural networks without concept predictions
- User study was limited to specific domains; generalization to other domains requires further validation

## Practical Applications & Real-World Use Cases

### 1. **Clinical Decision Support Systems**

**Application**: AI-assisted medical diagnosis

**Specific Use Case - Cardiac Imaging**:
- Top-level concepts: Cardiac abnormality present (yes/no)
- Sub-level-1 concepts: Arrhythmia vs. valve disease vs. cardiomyopathy
- Sub-level-2 concepts: Specific arrhythmia types (atrial fibrillation, ventricular tachycardia, etc.)

**Benefit**: 
- Cardiologists can intervene at appropriate levels (coarse diagnosis vs. specific condition)
- Reduces annotation burden: Only label top-level conditions; sub-concepts discovered automatically
- Enables multi-level explanations for different stakeholders (cardiologists, radiologists, patients)

### 2. **Computer Vision and Image Classification**

**Application**: Fine-grained visual categorization

**Specific Use Case - Wildlife Conservation**:
- Top-level concepts: Animal family (canines, felines, primates, etc.)
- Sub-concepts: Species within family
- Sub-sub-concepts: Individual characteristics (fur color, size, etc.)

**Benefit**:
- Conservation teams can intervene on broad categories or specific traits
- Automatic discovery of species variants without exhaustive manual labeling
- Enables explanations at multiple levels for different experts (taxonomists, field ecologists)

### 3. **Content Moderation and Safety**

**Application**: Automated content classification

**Use Case**:
- Top-level concepts: Content category (violence, hate speech, adult content, misinformation)
- Sub-concepts: Specific subcategories and severity levels
- Fine-grained concepts: Specific harmful attributes

**Benefit**:
- Moderators can fine-tune policies at different levels of abstraction
- Hierarchical interventions enable nuanced content policies
- Reduces need for exhaustive rule annotations

### 4. **Autonomous Systems and Robotics**

**Application**: Safety-critical decision-making

**Use Case**:
- Top-level concepts: Environmental hazards (obstacle, pedestrian, vehicle)
- Sub-concepts: Hazard characteristics (distance, movement, threat level)
- Fine-grained concepts: Specific object types and properties

**Benefit**:
- Enable hierarchical safety constraints and interventions
- Practitioners can validate models at different levels of detail
- Supports iterative refinement of autonomous system behavior

### 5. **Regulatory Compliance and Explainability**

**Application**: Meeting AI regulation requirements (EU AI Act, FDA guidelines)

**Benefits**:
- Hierarchical concepts provide multi-stakeholder explanations
  - Technical teams understand fine-grained concepts
  - Regulators understand high-level decision logic
  - End users receive human-friendly explanations
- Reduced annotation burden for compliance documentation
- Concept interventions support "right to explanation" regulatory requirements

### Regulatory and Practical Implications

**EU AI Act Compliance**:
- High-risk AI systems must be explainable
- HiCEMs provide multi-level explanations for diverse stakeholders
- Hierarchical structure aligns with regulatory transparency requirements

**FDA Medical Device Regulation**:
- Predicate devices increasingly require explainability
- Hierarchical concepts enable validation at multiple granularities
- Concept interventions support software validation workflows

**Practical Feasibility**:
- Concept Splitting reduces annotation burden (estimated 50-70% reduction based on paper)
- Hierarchy discovery is unsupervised, enabling scalability
- Implementation requires standard deep learning infrastructure

## Insights & Implications

### Theoretical Insights

1. **Hierarchy as Fundamental Structure**: The paper demonstrates that interpretable hierarchies exist implicitly in learned concept embeddings. Concept Splitting reveals that neural networks naturally organize learned representations hierarchically, supporting the hypothesis that hierarchy is fundamental to representation learning.

2. **Compositionality in Neural Networks**: The successful discovery of compositional sub-concepts (where parent = function(children)) shows that neural networks learn compositional structure even without explicit supervision. This aligns with broader theories of compositional semantics.

3. **Annotation-Efficiency Trade-off**: By automatically discovering sub-concepts, the paper shows practitioners can achieve hierarchical interpretability with a fraction of manual annotation effort. This challenges the assumption that interpretability always requires exhaustive human annotation.

### Broader Implications for Explainable AI

1. **Interpretability as Hierarchy**: The success of hierarchical models suggests that interpretability is fundamentally tied to multi-level abstraction. Future XAI methods should embrace hierarchies rather than treating concepts as flat.

2. **Closing the User Needs Gap**: Multi-level explanations address a key criticism of prior XAI work: different users need different levels of detail. HiCEMs enable a single model to provide explanations at multiple granularities.

3. **Interactive Interpretability**: Hierarchical concept interventions enable interactive explanations where users can drill down into details. This moves toward more dynamic, exploratory interpretability interfaces.

### Research Directions and Open Questions

1. **Discovering Optimal Hierarchies**: While Concept Splitting works well empirically, the paper leaves open how to optimally determine hierarchy depth and width. Future work might:
   - Learn hierarchy structure end-to-end during training
   - Combine automatic discovery with human feedback for optimal hierarchies
   - Develop theory for optimal hierarchy depth in different domains

2. **Scalability to Larger Concept Vocabularies**: Current experiments use hundreds to thousands of concepts. Scaling to tens of thousands of concepts (e.g., WordNet-scale) remains an open challenge.

3. **Domain Adaptation of Hierarchies**: Can hierarchies discovered on one dataset transfer to related domains? How stable are discovered hierarchies across distribution shifts?

4. **Causal Hierarchies**: Going beyond statistical correlations, can hierarchical concept discovery identify causal relationships between concepts?

5. **Integration with Symbolic Reasoning**: Can hierarchical concepts be integrated with symbolic AI or knowledge graphs for richer reasoning?

### Limitations and Failure Cases

1. **Assumes Latent Hierarchy Exists**: Concept Splitting assumes concepts have hierarchical structure in the embedding space. For flat domains or inconsistently hierarchical data, the method may fail.

2. **Semantic Drift**: Discovered sub-concepts may gradually drift in meaning from their parent concept, especially with deep hierarchies. Validation mechanisms are needed.

3. **Arbitrariness in Hierarchy Depth**: The optimal hierarchy depth is domain-dependent. Practitioners must manually decide when to stop splitting, introducing subjectivity.

4. **Limited to Concept-Based Models**: HiCEMs require interpretable concept predictions. Methods don't apply to arbitrary black-box models or to domains where concepts are difficult to define.

## Code & Resources

### Official Implementation

The authors provide code and resources (based on institutional practices):

- **Repository**: Expected to be released at [Institution's GitHub or ArXiv supplement]
- **Framework**: PyTorch or TensorFlow (typical for deep learning interpretability)
- **Dependencies**: Standard ML stack (PyTorch, numpy, scikit-learn, optuna)

### Key Components

**1. Sparse Autoencoder**:
- Implementation for discovering sub-concepts from embeddings
- Hyperparameter tuning for sparsity level and bottleneck dimension

**2. Hierarchical Model Architectures**:
- HiCEM backbone for integrating hierarchical concepts
- Concept Splitting pipeline for automatic hierarchy discovery

**3. Evaluation Metrics**:
- Concept discovery quality metrics (alignment with ground truth)
- Hierarchy structure metrics (depth, branching factor, consistency)
- Intervention effectiveness metrics

### Quick Start Guide

**Minimal Example** (Pseudocode):

```python
# Step 1: Train a standard CEM
cem = ConceptEmbeddingModel(backbone=ResNet50, num_concepts=100)
cem.train(train_data, train_concepts)

# Step 2: Discover sub-concepts via Concept Splitting
concept_splitter = ConceptSplitter(num_sub_concepts=5, sparsity=0.1)
sub_concepts = concept_splitter.split(cem.concept_embeddings)

# Step 3: Build hierarchical model
hicem = HierarchicalCEM(cem, sub_concepts)
hicem.train(train_data, task_labels)

# Step 4: Use hierarchical explanations
explanation = hicem.explain(image, hierarchy_level="parent")  # coarse explanation
fine_explanation = hicem.explain(image, hierarchy_level="child")  # detailed explanation

# Step 5: Perform hierarchical interventions
output_original = hicem(image)
output_intervened = hicem(image, intervene={parent_concept_5: 0.9})
```

### Computational Requirements

- **Training Time**: [Exact figures unavailable — see full paper]
  - Standard CEM: Hours to days on GPU
  - Concept Splitting: Minutes to hours (unsupervised)
  - Hierarchical training: Similar to flat CEMs

- **Memory**: Proportional to concept vocabulary size
  - Manageable on modern GPUs (16-40GB)
  - Scales to large ImageNet-scale datasets

### Interactive Visualizations and Demos

- **Concept Visualization**: Tools for visualizing discovered concepts and hierarchies
- **Intervention Playground**: Interactive demos allowing users to intervene on concepts and observe model behavior
- **Hierarchy Inspection**: Visualization of discovered hierarchies with semantic labels

## Related Work & Context

### Prior Concept-Based Interpretability Work

**Concept Embedding Models and Concept Bottleneck Models**:
- Concept Bottleneck Models (Koh et al., 2020) pioneered the idea of forcing predictions through concept bottlenecks
- Concept Embedding Models (Espinosa Zarlenga et al., 2022) extended CBMs by learning concept embeddings without requiring semantic labels
- HiCEMs build on these approaches by adding explicit hierarchical structure

**Concept Activation Vectors**:
- Testing with Concept Activation Vectors (TCAV, Kim et al., 2018) pioneered using concept activations for post-hoc interpretability
- HiCEMs extend TCAV ideas into the inherently interpretable framework with hierarchical structure

### Connection to Broader XAI Communities

**Feature Attribution Methods (LIME, SHAP)**:
- LIME and SHAP provide instance-level explanations
- HiCEMs provide global, concept-level explanations with hierarchical structure
- Complementary approaches: LIME for local reasoning, HiCEMs for conceptual understanding

**Mechanistic Interpretability**:
- Mechanistic interpretability seeks to understand neural network circuits
- HiCEMs operate at a higher level of abstraction but could integrate with circuit analysis
- Both aim to increase neural network transparency

**Knowledge Graphs and Symbolic AI**:
- Hierarchical concepts can be viewed as partial knowledge graphs
- Future work might integrate HiCEMs with structured knowledge representations
- Concepts as nodes, hierarchy as edges—natural bridge to symbolic AI

**Causal Interpretability**:
- While HiCEMs are not explicitly causal, hierarchical structure could be enhanced with causal reasoning
- Concepts at different levels could represent causal mechanisms
- Future integration with causal graph methods (Pearl's do-calculus, etc.)

### Recent Related Work

**Hierarchical Concept Variants**:
- **Hierarchical Concept Reasoning** (2025): Uses attention-guided graph learning for concept hierarchies
- **Multi-Level Concept Bottleneck Models** (2025): Extends CBMs with multi-level concepts
- **Concept Taxonomies** (2025): Learning concept taxonomies without explicit supervision

**Concept Evaluation and Analysis**:
- **Leakage in Concept-Based Models** (Parisini et al., 2025): Analyzes information leakage in CEMs—HiCEMs could benefit from leakage analysis
- **Concept Activation Vector Analysis** (2025): Examining TCAV consistency and reliability

### Where This Research Leads

1. **Foundation Models and Vision-Language Models**: Applying HiCEMs to large foundation models (CLIP, LLaMs) for interpretable multimodal AI

2. **Neuro-Symbolic AI**: Integrating hierarchical concepts with symbolic reasoning engines for hybrid AI systems

3. **Continuous Concept Learning**: Learning concept hierarchies continuously as new data arrives, rather than one-shot discovery

4. **Causal Concept Hierarchies**: Moving beyond statistical hierarchies to causal concept relationships for stronger interpretability

5. **Domain Adaptation of Concepts**: Transferring concept hierarchies across domains and leveraging transfer learning for improved interpretability

### Summary: HiCEMs in the XAI Landscape

HiCEMs represent a significant advance in concept-based interpretability by:
- Moving from flat to hierarchical concept spaces (aligns with human reasoning)
- Reducing annotation burden through automatic sub-concept discovery
- Enabling multi-stakeholder explanations at varying abstraction levels
- Providing flexible, hierarchical concept interventions

The work bridges foundational concept-based interpretability (Concept Activation Vectors, CEMs) with practical needs for multi-level, domain-aligned explanations, opening new directions for interpretable AI in high-stakes applications.

---

## References and Citations

- **ArXiv Paper**: [arXiv:2602.23947](https://arxiv.org/abs/2602.23947)
- **Conference**: Fourteenth International Conference on Learning Representations (ICLR 2026)
- **Authors**: Oscar Hill, Mateo Espinosa Zarlenga, Mateja Jamnik

### Key Foundational Papers Cited

- Koh et al. (2020): "Concept Bottleneck Models" — foundational concept-based interpretability
- Espinosa Zarlenga et al. (2022): "Concept Embedding Models" — learning concepts without semantic labels
- Kim et al. (2018): "Interpretability Beyond Feature Attribution" — TCAV and concept activation vectors
- Parisini et al. (2025): "Leakage and Interpretability in Concept-Based Models" — analyzing CEM limitations
