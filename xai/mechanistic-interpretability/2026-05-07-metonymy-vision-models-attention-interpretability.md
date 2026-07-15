# Metonymy in Vision Models Undermines Attention-Based Interpretability

**ArXiv ID:** 2605.06095  
**Submission Date:** May 7, 2026  
**Publication Status:** Preprint (28 pages)  
**Authors:** Research team investigating vision transformer interpretability and part-based reasoning  
**Primary Field:** Mechanistic Interpretability, Vision Transformer Explanation, Part-Based Representation Learning

## Executive Summary

This paper exposes a fundamental flaw in attention-based interpretable-by-design methods: modern pretrained vision transformers exhibit strong **intra-object leakage** where latent representations of individual object parts encode information from the entire object rather than just their corresponding image regions. This visual metonymy—the substitution of a part for the whole—undermines the locality assumption underlying part-centric attention mechanisms and concept bottleneck models. The authors propose a two-stage approach to prevent this leakage by design and demonstrate that inherently disentangled feature extraction improves attribute-driven part discovery across multiple tasks.

## Problem Statement

Part-based reasoning has emerged as a classical strategy to improve model interpretability by focusing attention on relevant object parts. This approach typically relies on:

1. **Part-centric attention mechanisms**: Using learned attention over spatial locations to isolate specific object parts
2. **Concept bottleneck models (CBMs)**: Leveraging part-based attribute concepts as intermediate representations
3. **Fundamental assumption (Locality Assumption)**: The latent representation of an object part encodes primarily information about the corresponding image region

However, this paper challenges this foundational assumption by demonstrating that it is **systematically violated** in modern pretrained vision transformers.

### Specific Gaps in Current Approaches

- **Unexamined assumption**: Prior work on part-based interpretability rarely validates whether representations actually localize to their intended parts
- **Scale of leakage**: The amount of intra-object information leakage in modern pretrained models has not been quantitatively measured
- **Impact on interpretability**: The implications of this leakage for the faithfulness of attention-based explanations remain unexplored
- **No systematic mitigation**: Existing methods do not account for this phenomenon when designing interpretable models

## Core Concepts & Theory

### Metonymy in Visual Representation

**Visual Metonymy** is a linguistic concept adapted to computer vision: the substitution of a part for the whole. In the context of vision models:
- A latent representation intended to encode information about part A paradoxically contains information about the entire object
- This occurs despite spatial locality constraints or attention mechanisms designed to isolate parts
- The phenomenon violates the assumption that feature representations are spatially aligned with visual attention

### Locality Assumption

The foundation of part-centric interpretability methods rests on the **locality assumption**:

```
For object part P with corresponding image region R_P:
Latent representation h_P ≈ f(R_P)  [information from region R_P only]

NOT:
h_P ≈ f(R_P ∪ Other regions)  [information from whole object]
```

Modern pretrained vision transformers violate this assumption, meaning:
- Part representations h_P contain information from the entire object O
- Intra-object leakage: I(h_P; O \ R_P) > 0  [mutual information between part representation and other parts]

### Information Leakage Measurement

The paper measures leakage through:

1. **Direct Measurement**: Quantifying mutual information between part representations and non-corresponding object regions
2. **Part-Based Attribute Annotations**: Using structured annotations (e.g., CelebA attributes) where specific parts correspond to specific attributes
3. **Two-stage Comparison**: Comparing standard models (leaking) vs. two-stage disentangled models (non-leaking)

### Two-Stage Disentanglement Approach

**Stage 1: Part-Level Feature Extraction**
- Extract features specifically from each object part using spatial masking or attention
- Constrain receptive fields to prevent long-range interactions

**Stage 2: Attribute/Concept Classification**
- Apply concept classifiers only on disentangled part features
- Prevent information from other parts influencing part-specific predictions

**Key Property**: This two-stage design prevents leakage by architectural constraint rather than hoping it emerges from training.

## Main Ideas & Key Contributions

### 1. Identification of the Metonymy Phenomenon

**Novel Finding**: Modern pretrained vision transformers, despite spatial structure, exhibit strong metonymic representations where part encodings incorporate whole-object information.

**Significance**: This discovery challenges the validity of part-based interpretability methods that assume localized representations are inherent to the learned features.

### 2. Quantitative Measurement of Intra-Object Leakage

The paper provides methods to rigorously measure leakage:
- Utilizing part-based attribute annotations (e.g., per-part labels in CelebA)
- Computing information flow from non-corresponding regions to part representations
- Establishing leakage metrics that can be standardized across models

### 3. Upper Bound Establishment via Disentangled Design

By constructing a two-stage model that **prevents leakage by architectural design**, the authors establish:
- An upper bound on what perfect part disentanglement could achieve
- Empirical evidence that disentanglement significantly improves interpretability
- A reference point for evaluating other part-based methods

### 4. Implications for Concept Bottleneck Models

**Critical Impact**: Concept Bottleneck Models (CBMs) and similar approaches that rely on part-centric concepts are vulnerable to:
- Part representations that don't truly encode what they claim to represent
- Unfaithful explanations based on spurious correlations within objects
- Degraded transparency despite the use of interpretable intermediate representations

### 5. Practical Solutions for Disentangled Features

The two-stage approach offers a concrete, implementable solution:
- Architectural modifications that enforce disentanglement
- Improved attribute discovery performance
- Foundation for building more trustworthy interpretable models

## Methodology & Implementation

### Experimental Setup

**Datasets Used**:
- **CelebA**: 202,599 face images with 40 binary attributes (appearance features like eyeglasses, bangs, hats)
- Additional vision datasets with part-based annotations for evaluating generalization

**Models Tested**:
- Standard pretrained vision transformers (ViT)
- ResNet and other convolutional architectures as baselines
- Concept Bottleneck Models using part-based concepts

### Evaluation Metrics for Interpretability

1. **Intra-Object Leakage Score**: 
   - Measures mutual information between part representations and non-corresponding regions
   - Higher score = more leakage = less localized representations

2. **Salience-Guided Faithfulness Coefficient (SaCo)**:
   - Compares impacts of high-salience vs. low-salience pixel subsets on predictions
   - Evaluates whether attention mechanisms truly capture decision-relevant regions
   - Expected property: High-salience regions should impact predictions more than low-salience regions

3. **Part Discovery Accuracy**:
   - Measures how well discovered part representations align with annotated object parts
   - Evaluated on attribute prediction tasks with per-part ground truth labels

4. **Disentanglement Metrics**:
   - Quantify separation between different part representations
   - Measure independence of part features from whole-object context

### Key Experimental Procedures

**Step 1: Leakage Quantification**
- Train standard pretrained models on part-aware attribute prediction
- Measure information in part representations stemming from non-corresponding regions
- Document leakage magnitude across different model architectures

**Step 2: Two-Stage Disentanglement Model**
- Stage 1: Spatially restrict feature extraction to single parts via masking or architectural constraints
- Stage 2: Apply concept classifiers only on masked/localized features
- Prevent backpropagation of gradients across part boundaries

**Step 3: Comparative Evaluation**
- Compare standard vs. disentangled models on:
  - Leakage metrics
  - Faithfulness coefficients
  - Part discovery accuracy
  - Downstream task performance

### Results [Exact figures unavailable — see full paper]

- **Leakage Magnitude**: Modern pretrained ViTs exhibit significant intra-object leakage compared to inherently disentangled two-stage models
- **Faithfulness Improvement**: Disentangled models show improved salience-guided faithfulness coefficients
- **Attribute Discovery**: Two-stage approach improves part-to-attribute alignment on CelebA evaluation
- **Generalization**: Findings hold across multiple model architectures and dataset types
- **Trade-offs**: Performance on standard vision tasks remains competitive despite architectural constraints for disentanglement

### Limitations of the Approach

1. **Computational Overhead**: Two-stage disentanglement requires additional per-part forward passes (approximately 2x computational cost for models with many parts)
2. **Scalability**: Approach scales with number of object parts; complex objects with many parts may face challenges
3. **Architectural Constraints**: Requires significant modifications to standard vision transformers; not immediately compatible with all existing pretrained models
4. **Part Definition Dependency**: Requires predefined part definitions; fully automatic part discovery remains open
5. **Evaluation Data**: Requires part-annotated datasets like CelebA; generalization to datasets without part annotations unclear

## Practical Applications & Real-World Use Cases

### Medical Imaging

**Challenge**: Physicians need to understand which anatomical regions drive diagnostic decisions (tumors, lesions, anomalies)

**Application**: 
- Deploy disentangled vision models that localize explanations to specific anatomical parts (e.g., lung regions, cardiac structures)
- Ensure explanations genuinely reflect model reasoning, not spurious part correlations
- Improve trust in AI-assisted diagnosis

**Regulatory Relevance**: FDA approval for computer-aided detection systems increasingly requires transparent reasoning traceable to clinical evidence

### Autonomous Systems & Safety-Critical Perception

**Challenge**: Autonomous vehicles must explain attention to specific objects (pedestrians, vehicles, obstacles)

**Application**:
- Develop part-based attention for multi-part objects (e.g., vehicle body vs. wheels vs. windows)
- Detect when the model's "attention" to claimed parts is actually influenced by irrelevant context
- Enable failure mode analysis: "The model claims attention to pedestrian head, but actually uses background context"

**Safety Impact**: Improved interpretability enables identification of edge cases and adversarial vulnerabilities

### Fairness and Bias Detection

**Challenge**: Models may make decisions based on correlated attributes rather than claimed features

**Application**:
- Use disentangled representations to detect when decisions attributed to one feature (e.g., "facial expression") actually depend on another feature (e.g., "skin tone")
- Audit for spurious correlations within objects that enable discrimination
- Design fairness interventions based on true causal factors

**Compliance**: Aligns with GDPR requirements for meaningful human explanation and AI Act provisions on discrimination

### Finance and Credit Decisions

**Challenge**: Interpretable machine learning for loan approval requires credible explanations

**Application**:
- Ensure that feature importance claims reflect actual decision drivers, not metonymic correlations
- Detect when "age" importance actually reflects correlated life-stage indicators
- Build trustworthy automated systems compliant with Fair Lending regulations

### Content Moderation and Harmful Content Detection

**Challenge**: Identifying whether systems genuinely focus on harmful content or exploit correlated features

**Application**:
- Deploy interpretable models that localize attention to specific concerning regions
- Verify that claimed features (e.g., "violent imagery") aren't metonymic proxies for other attributes
- Enable more accurate auditing of moderation systems

## Insights & Implications

### Paradigm Shift in Interpretable AI

This work fundamentally challenges the assumption that **attention mechanisms naturally produce localized, interpretable representations**. Key implications:

1. **Interpretability-by-Design is Insufficient**: Merely using part-centric concepts or attention doesn't guarantee faithful, localized representations
2. **Architectural Enforcement Needed**: Achieving true disentanglement requires explicit constraints, not just training objectives
3. **Validation is Essential**: Part-based interpretability methods must empirically validate the locality assumption rather than assuming it

### Limitations and Future Directions

**Open Questions**:
- Can fully automatic part discovery achieve comparable disentanglement without hand-defined parts?
- How does leakage vary with model scale, training data, and architecture?
- Can similar phenomena be observed in other modalities (video, 3D)?
- What is the fundamental trade-off between expressiveness and disentanglement?

**Failure Cases**:
- For objects with inherent ambiguity in part boundaries (e.g., abstract shapes), disentanglement may be ill-defined
- Highly correlated parts (e.g., left and right eyes in faces) may resist complete disentanglement
- Transfer to new domains/part definitions may require retraining

**Broader Implications for XAI**:
- Questions the faithfulness of many existing interpretable-by-design methods
- Suggests that interpretability auditing (checking assumptions) should be standard practice
- Highlights the need for mechanistic understanding beyond post-hoc explanations

### Connection to Broader xAI Research

1. **Concept-Based Explanations**: Directly impacts interpretability of CBM and TCAV-based methods
2. **Mechanistic Interpretability**: Adds to understanding of how representations are actually structured in neural networks
3. **Faithfulness and Reliability**: Contributes to the debate on what constitutes a faithful explanation
4. **Model Transparency**: Demonstrates that architectural transparency alone doesn't ensure interpretability

### Research Trajectory

This work sits at the intersection of:
- **Representation Learning**: How do neural networks organize learned features?
- **Interpretability Theory**: What assumptions underlie different explanation approaches?
- **Model Design**: How to build systems with guaranteed interpretability properties?

Future research may explore:
- Disentanglement techniques that scale to high-part-count scenarios
- Automatic part discovery with accompanying leakage guarantees
- Integration with other interpretability paradigms (e.g., causal reasoning)
- Extension to language and multimodal models

## Code & Resources

### Official Implementation and Repositories

- **Paper Repository**: Full implementation details available in paper supplementary materials
- **GitHub**: [Check for official release at paper's project page or author institution]
- **Dependencies**: PyTorch, torchvision, standard computer vision libraries

### Key Dependencies and Requirements

- **Python**: 3.8+
- **PyTorch**: 1.10+
- **CUDA**: Recommended for efficient training (GPU memory: ~16GB for standard experiments)
- **Data**: CelebA dataset (requires download from official source)

### Quick Start (Estimated from methodology)

```python
# Pseudocode for two-stage disentangled model
import torch
import torchvision.models as models

# Stage 1: Part-specific feature extraction
def extract_part_features(image, part_mask, backbone_model):
    # Apply spatial masking to isolate part
    masked_image = image * part_mask
    # Extract features from masked input
    part_features = backbone_model(masked_image)
    return part_features

# Stage 2: Part-specific classification
def classify_part_attribute(part_features, concept_classifier):
    # Apply concept classifier only on part features
    prediction = concept_classifier(part_features)
    return prediction

# Full pipeline
image = load_image(...)
parts = get_part_definitions(...)  # e.g., [left_eye, right_eye, mouth, ...]

for part_name, part_mask in parts:
    part_feat = extract_part_features(image, part_mask, backbone)
    attr_pred = classify_part_attribute(part_feat, classifiers[part_name])
    print(f"{part_name}: {attr_pred}")
```

### Computational Requirements

- **Training Time**: [Estimated as higher than standard models due to per-part processing]
- **Inference Time**: Scales linearly with number of parts (~2-5x slower than single-pass models for typical part counts)
- **Memory**: Manageable within standard GPU memory with batch size adjustments

### Available Resources

- **Datasets**: CelebA with part annotations (40 attributes)
- **Baselines**: Standard vision transformers, ResNet models
- **Evaluation Tools**: Suggested metrics and evaluation code structure described in methodology section

## Related Work & Context

### Connection to Foundational XAI Methods

1. **Concept Activation Vectors (CAV)**: This work extends questioning of concept-based explanations begun by CAV research
2. **Concept Bottleneck Models**: Directly challenges the interpretability claims of CBM-style architectures
3. **SHAP and LIME**: Relates to debates about what constitutes a faithful local or global explanation
4. **Attention Visualization**: Challenges the interpretation of attention weights as direct explanations

### Recent Related Papers

- **Part-Based Reasoning**: Prior work on using parts for interpretability (referenced but flawed)
- **Representation Leakage**: Related to privacy literature on information leakage in learned representations
- **Vision Transformer Understanding**: Contextualizes within broader work on ViT interpretation
- **Faithfulness of Explanations**: Contributes to literature questioning whether explanations actually reflect model reasoning

### Prior Mechanistic Interpretability Work in Vision

- Attention-based explanations (challenged by this work)
- Feature visualization techniques
- Activation maximization methods
- Neuron-level interpretability approaches

### How This Advances xAI

**Distinctive Contributions**:
1. First systematic study of intra-object representation leakage
2. Quantitative framework for measuring leakage
3. Architectural solution to prevent leakage by design
4. Empirical validation of failures in existing interpretable-by-design methods

**Positioning in the Field**:
- **Critique/Validation**: Challenges assumptions in existing methods
- **Constructive**: Proposes concrete architectural fixes
- **Mechanistic**: Provides insights into how representations are actually structured
- **Practical**: Enables more trustworthy interpretable model design

### Future Research Directions

1. **Leakage in Other Domains**: Do similar phenomena occur in NLP, audio, or multimodal models?
2. **Automatic Disentanglement**: Can we achieve disentanglement without manual part definitions?
3. **Scalability**: How to efficiently handle objects with thousands of meaningful parts?
4. **Multi-Object Scenes**: Extension to images with multiple objects and complex interactions
5. **Theoretical Foundations**: Formal characterization of when disentanglement is achievable

## Broader Impact and Significance

This paper makes a **critical contribution to interpretable AI** by:

1. **Exposing Limitations**: Demonstrates that a widespread assumption in interpretable-by-design methods is systematically violated
2. **Enabling Better Auditing**: Provides tools to verify whether interpretability claims are actually valid
3. **Guiding Future Design**: Suggests that architectural constraints are necessary for true interpretability
4. **Building Trust**: Contributes to more reliable, trustworthy AI systems by preventing false confidence in flawed explanations

The work is particularly important for high-stakes applications where incorrect interpretability claims could lead to misplaced trust in unreliable systems.

---

**Paper Summary for Quick Reference**:
- **Key Innovation**: Identification and measurement of intra-object representation leakage in vision models
- **Main Contribution**: Two-stage architecture preventing leakage; empirical validation of interpretability failures
- **Practical Implication**: Existing part-based interpretability methods may be less faithful than claimed
- **Actionable Takeaway**: Use disentangled architectures when part-based interpretability is critical
- **Impact Level**: High (challenges fundamental assumptions in interpretable AI)

---

*Document compiled from ArXiv preprint and research methodology. For exact metrics, implementation details, and extended results, refer to the full paper at arXiv:2605.06095*
