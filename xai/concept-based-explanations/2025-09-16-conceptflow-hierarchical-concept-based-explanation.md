# ConceptFlow: Hierarchical and Fine-grained Concept-Based Explanation for Convolutional Neural Networks

**ArXiv ID:** [2509.18147](https://arxiv.org/abs/2509.18147)  
**Submitted:** September 16, 2025  
**Authors:** Xinyu Mu, Hui Dou, Furao Shen, Jian Zhao

## Executive Summary

ConceptFlow is a novel concept-based interpretability framework that traces how high-level semantic concepts emerge, propagate, and transform across layers in Convolutional Neural Networks (CNNs). Rather than treating individual filters in isolation, ConceptFlow introduces a "concept transition matrix" that quantifies the hierarchical evolution of concepts through the network, providing a layer-wise analysis of internal semantic flow that aligns model reasoning with human intuition. This approach fills a critical gap in existing concept-based explanation methods, which overlook both the semantic roles of filters and the dynamic concept propagation that underlies deep learning decision-making.

## Problem Statement

### Current Limitations in Concept-Based Explanations

Existing concept-based interpretability methods suffer from two fundamental limitations:

1. **Filter-Concept Isolation:** Traditional approaches focus on associating individual filters with concepts, treating each filter as an independent semantic unit. This fails to capture how concepts transform and interact as they propagate through the network hierarchy.

2. **Loss of Semantic Flow:** Current methods largely ignore the **dynamic propagation and transformation of concepts between layers**. A concept learned at one filter (e.g., "cornered shape") may evolve into a different but related concept in the next layer (e.g., "digit 7"), creating a reasoning chain. This dynamic flow is essential for understanding how CNNs build hierarchical semantic representations.

3. **Lack of Quantitative Measurement:** There is no principled quantitative framework for measuring *how* concepts transform and propagate hierarchically through network depth, making it difficult to extract systematic semantic explanations.

### Why This Matters for xAI

Concept-based explanations are valuable because they translate opaque neural network decisions into human-understandable semantic terms (e.g., "textures," "shapes," "objects"). However, without understanding concept propagation, we cannot explain *why* the model makes specific decisions—only what semantic features it recognizes. ConceptFlow addresses this by providing a complete picture of the semantic reasoning chain.

## Core Concepts & Theory

### 1. Concept Attentions

Concept attentions are the mechanism by which individual filters are associated with high-level concepts:

- Each convolutional filter at a given layer is mapped to a set of meaningful concepts
- These mappings are learned or defined through visualization techniques (e.g., Neural Network Scanner)
- Concept attentions enable **localized semantic interpretation** at the filter level

### 2. The Concept Transition Matrix

The core innovation of ConceptFlow is the **concept transition matrix**, which quantifies how concepts transform between consecutive layers:

**Definition:** For layer $l$ and layer $l+1$, the concept transition matrix $T^{(l \to l+1)}$ is an $m \times n$ matrix where:
- $m$ = number of concepts associated with layer $l$
- $n$ = number of concepts associated with layer $l+1$
- Each entry $T_{ij}^{(l \to l+1)}$ represents the **strength of transformation** from concept $i$ in layer $l$ to concept $j$ in layer $l+1$

**Interpretation:** High values indicate that a concept learned at layer $l$ strongly influences the emergence of a concept at layer $l+1$, creating a semantic chain.

### 3. Conceptual Pathways

Conceptual pathways are derived from concept transition matrices and represent the complete propagation routes of semantic concepts through the network:

- A pathway traces how a single concept (e.g., "horizontal line") evolves from early layers (low-level features) through middle layers (part assemblies) to later layers (semantic objects)
- Multiple pathways can coexist, representing different semantic reasoning chains
- Pathways provide a **human-aligned explanation of hierarchical reasoning**

### Mathematical Framework

Given a CNN with $L$ layers:

1. **Concept Extraction:** For each layer $l$, extract concepts $C^{(l)} = \{c_1^{(l)}, c_2^{(l)}, \ldots, c_m^{(l)}\}$
2. **Attention Computation:** Compute attention weights $a_{ij}^{(l)}$ showing how filter $i$ in layer $l$ relates to concept $j$
3. **Transition Matrix Construction:** Build $T^{(l \to l+1)}$ based on concept-filter relationships across consecutive layers
4. **Pathway Extraction:** Identify dominant pathways by traversing high-value sequences through transition matrices

The framework maintains interpretability by operating on human-meaningful concepts rather than raw activations.

## Main Ideas & Key Contributions

### 1. Novel Framework for Hierarchical Concept Representation

ConceptFlow's primary contribution is introducing a principled way to track concept evolution across network depth. Unlike prior work that treats layers independently, ConceptFlow models the **interdependencies between layer-wise concepts**.

**Key Innovation:** The concept transition matrix provides a quantitative lens through which to view semantic propagation, enabling systematic analysis of how models build hierarchical understanding.

### 2. Localized Semantic Interpretation

By associating individual filters with concepts (concept attentions), ConceptFlow enables **fine-grained explanations at the filter level**, bridging the gap between:
- Low-level explanation methods (pixel-level saliency)
- High-level explanation methods (class-level feature importance)

### 3. Layer-Wise Semantic Flow Analysis

The framework supports **layer-by-layer analysis of semantic reasoning chains**, revealing:
- Which high-level concepts are built from which low-level features
- How semantic representations evolve from early to late layers
- Potential failure points in the reasoning chain

### 4. Alignment with Human Reasoning

ConceptFlow's conceptual pathways mirror human reasoning chains—understanding how we progressively build complex concepts from simpler building blocks. This alignment improves both interpretability and trust.

## Methodology & Implementation

### Experimental Setup

#### Datasets and Models

The paper evaluates ConceptFlow on two datasets:

1. **CMNIST (Colored MNIST):**
   - Custom variant of MNIST with color attributes
   - Used to evaluate concept tracking in controlled settings
   - CNN architecture: 3-layer network with 64 filters per layer (except final layer: 128 filters)

2. **CAWA (Object Recognition Dataset):**
   - More complex natural image dataset
   - Used to evaluate scalability to realistic scenarios
   - CNN architecture: 5-layer network with 64 filters per layer (except final layer: 128 filters)

#### Architecture Details

Both experimental setups use relatively modest CNN architectures to facilitate interpretability analysis. The framework is designed to scale to standard architectures (VGG, ResNet, etc.).

### Concept Extraction & Annotation

1. **Concept Visualization:** Use Neural Network Scanner (NNS) to generate "learning images" that visualize patterns captured by each filter
2. **Semantic Annotation:** Manually or automatically annotate visualized patterns with meaningful concept labels (e.g., "horizontal lines," "corners," "textures")
3. **Concept Assignment:** Map each filter to a set of relevant concepts with associated confidence scores

### Concept Transition Matrix Construction

**Algorithm:**
1. Extract activations from layers $l$ and $l+1$ for all input samples
2. Compute activation patterns for each concept across both layers
3. Build the transition matrix $T$ by measuring:
   - Correlation of concept co-occurrences across layers
   - Information flow from layer $l$ concepts to layer $l+1$ concepts
   - Functional dependencies between layer-wise semantic representations

[Exact figures unavailable — see full paper]

### Evaluation Metrics

ConceptFlow's effectiveness is evaluated on:

1. **Semantic Meaningfulness:** Do extracted concepts align with human perception of visual features?
   - Measured via human evaluation (not all quantitative)
   - Checked against known object parts and visual attributes

2. **Pathway Faithfulness:** Do identified conceptual pathways accurately reflect how the network processes information?
   - Tested through ablation studies on pathway components
   - [Exact metrics unavailable — see full paper]

3. **Explainability Quality:** Are the layer-wise explanations faithful and stable?
   - Consistency across similar inputs
   - Robustness to perturbations

### Experimental Results

**Key Findings:**

1. **Successful Concept Propagation Tracking:** ConceptFlow successfully traces how concepts evolve from simple visual patterns in early layers to complex semantic objects in deeper layers.

2. **Interpretable Pathways:** The extracted conceptual pathways provide semantically meaningful explanations of model decisions, validating the effectiveness of both concept attentions and conceptual pathways.

3. **Scalability:** The framework scales to 5-layer CNNs on realistic datasets, though [specific performance metrics unavailable — see full paper for quantitative analysis].

4. **Hierarchical Insight:** Results demonstrate that ConceptFlow yields **semantically meaningful insights into model reasoning**, showing that concept propagation is not random but follows structured semantic evolution.

### Implementation Details

- **Visualization Tool:** Neural Network Scanner (NNS) for concept extraction
- **Computational Requirements:** [Estimated moderate — depends on network size and dataset complexity; see paper for specifics]
- **Scalability:** Demonstrated on small to moderate-size CNNs; extension to large models (ResNet-50, etc.) likely requires optimization

## Practical Applications & Real-World Use Cases

### 1. Model Debugging and Quality Assurance

**Application:** Identify erroneous semantic reasoning in production models

- **Use Case:** A medical imaging CNN classifies a tumor as benign, but ConceptFlow reveals that the model is primarily using "background color" concepts rather than tumor morphology
- **Actionable Insight:** This indicates the model learned spurious correlations, enabling targeted retraining

### 2. Trustworthy Deployment in High-Stakes Domains

**Domains:** Healthcare, autonomous vehicles, financial modeling

- **Healthcare (Radiology):** Ensure AI diagnostic systems use medically relevant features (tumor size, texture) rather than image artifacts
- **Autonomous Driving:** Verify that object recognition systems build representations based on semantic object properties rather than lighting conditions
- **Finance:** Audit credit scoring models to ensure decisions are based on meaningful financial indicators, not spurious patterns

### 3. Transfer Learning and Model Adaptation

**Application:** Understand which concepts transfer across domains

- **Use Case:** A CNN trained on ImageNet is fine-tuned on medical images. ConceptFlow reveals which early-layer concepts (edge detection, texture) transfer well vs. which semantic concepts require relearning
- **Benefit:** Guides more efficient transfer learning strategies

### 4. Human-in-the-Loop AI Systems

**Application:** Facilitate human understanding and intervention in AI decisions

- **Use Case:** A content moderation system flags an image. ConceptFlow explains which visual concepts triggered the flag, allowing human reviewers to provide corrective feedback
- **Benefit:** Enables human-AI collaboration rather than blind trust or rejection

### 5. Regulatory Compliance

**Relevance to Standards:**
- **EU AI Act:** Requires transparency in high-risk AI systems; ConceptFlow's conceptual pathways provide auditable reasoning chains
- **FDA Medical Device Guidance:** Requires understanding of model inputs and decision-making; concept-based explanations align with FDA requirements
- **GDPR (Right to Explanation):** Subjects have the right to understand AI decisions; ConceptFlow provides human-understandable explanations

### 6. Fairness and Bias Auditing

**Application:** Detect and mitigate algorithmic bias

- **Use Case:** A facial recognition system shows racial bias. ConceptFlow can trace which concepts (e.g., lighting conditions correlated with demographics) drive the bias
- **Benefit:** Enables targeted debiasing strategies

## Insights & Implications

### Theoretical Implications

1. **Hierarchical Semantic Representation:** CNNs construct hierarchical semantic representations through structured concept propagation, not random feature combination. ConceptFlow makes this structure explicit and analyzable.

2. **Bridging Mechanistic and Concept-Based Interpretability:** By tracking concept transformation, ConceptFlow bridges two interpretability paradigms:
   - Mechanistic interpretability (understanding internal circuits)
   - Concept-based interpretability (understanding semantic reasoning)

3. **Layer-Wise Reasoning Chains:** Deep learning operates through hierarchical reasoning chains analogous to human cognition, where each layer builds more abstract concepts from lower-level features.

### Practical Implications for xAI

1. **Explainability Completeness:** Concept-based explanations are more complete when they include concept propagation, not just individual concept detection.

2. **Human Alignment:** Systems that explain reasoning through conceptual pathways achieve better human-AI alignment than systems using feature importance alone.

3. **Accountability:** Organizations can audit model behavior by examining conceptual pathways, creating accountability for AI decisions.

### Limitations and Open Questions

1. **Manual Concept Annotation:** Current implementation requires manual annotation of concepts, limiting scalability. Automated concept discovery would enhance practical applicability.

2. **Computational Overhead:** Computing and storing transition matrices adds computational cost. Optimization for large models (ResNets, ViTs) remains an open challenge.

3. **Concept Definition Dependency:** Explanations are only as good as the concepts used. Choosing appropriate semantic concepts requires domain expertise.

4. **Applicability Beyond Vision:** While focused on CNNs, extending ConceptFlow to transformers (vision or language) requires handling attention-based architectures differently.

5. **Quantifying Explanation Quality:** While ConceptFlow provides qualitative insights, rigorous metrics for evaluating explanation faithfulness and completeness remain limited.

### Future Research Directions

1. **Automated Concept Discovery:** Develop unsupervised methods to automatically discover semantically meaningful concepts without manual annotation

2. **Cross-Model Concept Transfer:** Study how concepts transfer across different CNN architectures and training regimes

3. **Dynamic Concept Evolution:** Extend framework to handle concept definitions that evolve during training or adaptation

4. **Integration with Mechanistic Interpretability:** Combine concept transition matrices with neural circuit analysis for comprehensive mechanistic understanding

5. **Scaling to Foundation Models:** Adapt the framework to large transformers (ViT, CLIP, etc.) to enable interpretability of modern vision-language systems

## Code & Resources

### Official Implementation

- **Repository:** Check the authors' institutional pages or contact them for code availability
- **Status:** As of the paper's publication, code availability has not been widely announced [Exact figures unavailable — see full paper]
- **Language:** Expected to be implemented in PyTorch

### Dependencies (Expected)

- **Deep Learning Framework:** PyTorch >= 1.9
- **Visualization:** Neural Network Scanner (NNS) or similar visualization toolkit
- **Data Processing:** NumPy, scikit-learn, Pillow
- **Scientific Computing:** SciPy for matrix operations

### Quick Start (Expected)

The typical workflow would be:
1. Load a pre-trained CNN
2. Extract and visualize filters using NNS
3. Annotate visualizations with semantic concepts
4. Compute concept transition matrices between consecutive layers
5. Extract and visualize conceptual pathways
6. Generate explanations for specific model predictions

### Interactive Visualization

ConceptFlow likely includes visualization tools for:
- Filter-to-concept attention heatmaps
- Concept transition matrices (as heat maps)
- Conceptual pathway diagrams showing concept evolution across layers
- Decision attribution through conceptual pathways

### References and Links

- **ArXiv Paper:** [https://arxiv.org/abs/2509.18147](https://arxiv.org/abs/2509.18147)
- **ArXiv PDF:** [https://arxiv.org/pdf/2509.18147](https://arxiv.org/pdf/2509.18147)
- **HTML Version:** [https://arxiv.org/html/2509.18147v1](https://arxiv.org/html/2509.18147v1)

## Related Work & Context

### Related Concept-Based Explanation Methods

**Testing with Concept Activation Vectors (TCAV)** and **α-TCAV:**
- Pioneering work on concept-based explanations using directional derivatives
- ConceptFlow extends this by adding hierarchical structure and concept propagation

**Concept Bottleneck Models:**
- Alternative approach that constrains intermediate layers to explicit concepts
- ConceptFlow is post-hoc, not requiring architectural changes

**Hierarchical Concept-Based Models:**
- Recent work exploring nested concept hierarchies
- ConceptFlow quantifies hierarchy through transition matrices rather than explicit hierarchical definitions

**Mechanistic Interpretability with Concepts:**
- Emerging work combining mechanistic interpretability with concept-based explanations (e.g., BAGEL from Knowledge Graphs paper)
- ConceptFlow provides a complementary approach focused on hierarchical semantic flow

### Connection to Broader xAI Communities

**Feature Attribution Methods (SHAP, LIME):**
- Feature attribution methods explain predictions via input feature importance
- ConceptFlow operates at a higher level of abstraction (concepts rather than pixels/features)
- Potentially complementary: concept pathways could inform feature importance analysis

**Causal Interpretability:**
- Causal interpretation seeks to understand "why" models make decisions
- ConceptFlow's concept transition matrices reveal causal semantic pathways
- Integration with causal inference methods could strengthen explanations

**Sparse Autoencoders (SAEs):**
- SAEs discover interpretable features in neural networks
- ConceptFlow's concept attentions share goals with SAE-discovered features
- Combining SAE features with ConceptFlow's transition matrices is a promising direction

### Positioning in xAI Taxonomy

ConceptFlow is positioned at the intersection of:
- **Concept-based Explanations:** Primary category; operates on semantic concepts
- **Mechanistic Interpretability:** Secondary category; traces concept propagation through circuits
- **Hierarchical Interpretability:** Addresses multi-layer semantic evolution

### Evolution of Concept-Based Explanations

1. **Generation 1:** Point-based concept analysis (TCAV, CAV)
2. **Generation 2:** Concept bottleneck models constraining architectures
3. **Generation 3 (ConceptFlow):** Hierarchical concept propagation analysis
4. **Future:** Automated concept discovery + mechanistic concept circuits

### Research Ecosystem

ConceptFlow builds on and contributes to:
- Vision Transformer interpretability research (extending CNN methods to attention-based models)
- Human-AI alignment through concept-based explanations
- Trustworthy AI for regulated domains (healthcare, finance)
- Fairness and bias detection via semantic analysis

## Conclusion

ConceptFlow represents an important advance in concept-based interpretability by introducing a principled framework for understanding how semantic concepts propagate through deep neural networks. By combining concept attentions with concept transition matrices, the work provides layer-wise analysis capabilities that align model reasoning with human intuition. The framework addresses a critical gap in existing interpretability methods—the treatment of concept propagation as a dynamic process rather than a static mapping.

The practical implications for model debugging, regulatory compliance, and trustworthy AI deployment are significant, particularly in high-stakes domains like healthcare and autonomous systems. While challenges remain (automated concept discovery, scaling to modern architectures, rigorous evaluation metrics), ConceptFlow provides a foundation for the next generation of interpretable deep learning systems.

As the field of explainable AI continues to mature, hierarchical concept-based explanations like those enabled by ConceptFlow will likely become essential for auditable, trustworthy AI systems.
