# ConEx: Human-Interpretable Saliency Maps via Concept-Aware Attribution

**ArXiv ID:** [2610.04605](https://arxiv.org/abs/2610.04605)

**Authors:** Yehonatan Elisha, Oren Barkan, Ziv Weiss Haddad, Noam Koenigstein

**Submitted:** October 3, 2026

**Accepted Venue:** ICML 2026

## Executive Summary

ConEx introduces a novel framework that bridges the gap between low-level saliency visualization and high-level concept-based explanations, enabling models to explain their predictions through human-understandable concepts rather than pixel-level importance maps. By leveraging vision-language models to discover class-specific concepts without manual supervision and pairing them with spatial saliency information, ConEx provides both faithfulness and interpretability—two traditionally competing objectives in explainable AI.

## Problem Statement

Existing explainability approaches face a fundamental tradeoff:

- **Saliency-based methods** (e.g., gradient-based visualizations, attention maps) highlight which pixels influence a model's prediction but lack semantic meaning. A user sees highlighted regions without understanding *why* those regions matter.
  
- **Concept-based methods** (e.g., TCAV, concept bottlenecks) map model decisions to human-understandable concepts but traditionally require manual specification of concepts or produce concept activations without spatial localization, limiting actionability.

- **Manual concept definition is expensive:** Acquiring human-labeled concepts for every model and domain is time-consuming and inconsistent across annotators.

ConEx addresses this by automatically discovering semantically meaningful concepts from class-specific visual patterns and providing both *where* concepts appear (spatial saliency) and *how much* they contribute to the prediction (concept-level attribution).

## Core Concepts & Theory

### 1. Concept Activation Vectors (CAVs)

ConEx learns concept activation vectors—latent representations that encode the presence of interpretable visual concepts within a model's feature space. Unlike traditional CAVs that require human annotation or concept classifiers, ConEx's CAVs are:

- **Discovered unsupervised:** Mined from class-specific patterns without manual concept labels
- **Spatially grounded:** Each CAV has a corresponding spatial mask showing where the concept appears in the input
- **Architecture-aware:** CAV extraction uses layer-wise strategies specific to the model family (CNNs vs. Vision Transformers)

### 2. Vision-Language Priors for Concept Discovery

ConEx leverages pre-trained vision-language models (e.g., CLIP, SAM) to bootstrap concept discovery:

1. **Text attribute extraction:** Generate text descriptions of visual attributes for each class (e.g., "red color," "striped pattern") using label-free language model reasoning
2. **Spatial grounding:** Use zero-shot segmentation (GroundedSAM) to ground text attributes into spatial masks on example images
3. **Concept validation:** Retain only concepts that meet thresholds for occurrence rate and spatial coverage

This approach is fundamentally different from manual concept specification: instead of asking humans to define concepts a priori, the framework discovers what visual patterns actually matter for classification.

### 3. Architecture-Specific Masking for Noise Reduction

A key contribution is addressing segmentation noise from zero-shot segmentation models. ConEx applies architecture-specific masking:

- **For CNNs (ResNet, VGG, EfficientNet):** Use layer-wise feature masking to isolate concept-specific activations
  - Extract features from intermediate CNN layers (e.g., layer 4 in ResNet50)
  - Apply spatial masks aligned to the feature map resolution
  - Reduce noisy activations through multiplicative gating
  
- **For Vision Transformers (ViT):** Aggregate attention patterns across patch embeddings without additional masking (ViTs' patch-based architecture provides inherent spatial structure)

This design reduces concept activation noise and improves the purity of learned concept representations.

### 4. Saliency Generation via Concept Attribution

ConEx produces saliency maps through two complementary pathways:

- **Global saliency:** Class-level concept attribution showing how much each concept contributes to the final prediction
- **Local saliency:** Pixel-level maps showing where each concept appears and its spatial influence

The attribution is computed via:
$$\text{Attribution}_{\text{concept}} = \text{Relevance}(\text{CAV}, \text{layer}) \times \text{Spatial Mask}$$

This multiplicative fusion ensures that only spatially relevant concept activations contribute to the final explanation.

## Main Ideas & Key Contributions

### 1. Unified Framework for Saliency and Concepts

ConEx is the first framework to:
- Generate spatial saliency maps that are **tied to semantic concepts** rather than generic pixel importance
- Maintain **architectural compatibility** across CNNs and ViTs without model retraining
- Eliminate the need for **manual concept engineering** through vision-language priors

### 2. Novel Evaluation Metrics

The paper introduces two metrics for assessing concept quality:

- **Vector-Concept Match (VCM):** Measures how well learned concept activation vectors align with their intended visual meaning (e.g., is the "red" concept actually detecting red regions?)
  
- **Concept-Class Match (CCM):** Evaluates whether discovered concepts correlate with class labels (e.g., do "whiskers" concepts appear more in cat images?)

These metrics address a gap in existing concept-based evaluation: prior work lacks principled metrics to assess concept coherence without manual annotation.

### 3. Comprehensive Multi-Dimensional Evaluation

ConEx is evaluated across four independent dimensions:

1. **Faithfulness:** Using perturbation tests and the FunnyBirds benchmark to verify that explanations reflect true model behavior
2. **Concept Quality:** Via VCM and CCM metrics to ensure concepts are semantically meaningful
3. **Segmentation Accuracy:** Evaluating spatial localization of concepts against object masks where available
4. **Human Interpretability:** Demonstrating that concept-saliency maps are more actionable than pixel-level saliency alone

### 4. State-of-the-Art Performance

The paper reports:
- **Faithfulness:** Exceeds baselines on perturbation-based metrics and FunnyBirds evaluation
- **Concept Discovery:** More semantically coherent concepts compared to unsupervised concept extraction methods
- **Robustness:** Consistent performance across model families and image domains

## Methodology & Implementation

### 1. Pipeline Overview

```
Class → Text Attributes (via LLM) 
        ↓
Spatial Masks (via GroundedSAM)
        ↓
Concept Validation (occurrence/coverage thresholds)
        ↓
CAV Learning (architecture-specific masking)
        ↓
Saliency Generation (multiplicative fusion)
        ↓
Human-Interpretable Explanations
```

### 2. Experimental Setup

**Models Tested:**
- CNN architectures: ResNet50, ResNet101, VGG16, EfficientNet-B4, EfficientNet-B7
- Vision Transformers: ViT-B/16, ViT-L/16, DeiT-B

**Datasets:**
- ImageNet (large-scale object classification)
- [Exact secondary dataset names unavailable — see full paper]
- [Exact tertiary dataset names unavailable — see full paper]

**Evaluation Metrics:**
- **Perturbation-based faithfulness:** Measure prediction changes when concepts are masked
- **FunnyBirds benchmark:** Synthetic dataset with controlled part-based concepts
- **Concept purity:** Vector-Concept Match (VCM) and Concept-Class Match (CCM) [Exact threshold values unavailable — see full paper]
- **Spatial accuracy:** Intersection-over-Union (IoU) against available object segmentation masks

### 3. Key Implementation Details

- **Concept discovery:** 10-50 concepts per class (estimated; exact number unavailable)
- **CAV dimensionality:** Matches the feature space dimension of each architecture
- **Masking threshold:** Architecture-specific values for concept occurrence and coverage (exact values unavailable — see full paper)
- **Computational cost:** Inference overhead compared to baseline models (estimated as moderate to low for single forward pass)

### 4. Results Summary

[Exact numerical results unavailable — see full paper for detailed tables]

The paper demonstrates:
- Significant improvements over non-concept baselines on faithfulness metrics
- ConEx concepts are more semantically coherent than unsupervised concept extraction
- Spatial concept localization is competitive with or exceeds existing saliency methods
- Performance is consistent across diverse model architectures and datasets

## Practical Applications & Real-World Use Cases

### 1. Medical Imaging Diagnosis

**Use Case:** A radiologist needs to understand why a model flagged a chest X-ray as abnormal.

**ConEx Advantage:** Instead of seeing pixel-level heatmaps, the radiologist receives concept-level explanations such as:
- "Dark nodule detected (80% contribution)"
- "Irregular border pattern (15% contribution)"
- "Tissue density anomaly (5% contribution)"

Each concept comes with a spatial saliency map showing exactly where the anomaly is located and why it's classified as abnormal.

### 2. Autonomous Vehicle Safety Verification

**Use Case:** Testing a traffic sign classifier's robustness and correctness.

**ConEx Advantage:** Engineers can verify that the model attends to the correct visual concepts:
- "Red color" concept should dominate stop sign decisions
- "Octagonal shape" concept should appear for stop signs
- Absence of spurious concepts (e.g., "text location") confirms the model isn't exploiting artifacts

### 3. Fairness and Bias Detection

**Use Case:** Auditing a face recognition system for demographic bias.

**ConEx Advantage:** Identifies which visual concepts drive identity predictions:
- If "skin tone" concepts appear among top predictors, the model may be biased
- If "facial structure" dominates and "skin tone" is low-ranked, the model is more robust
- Human auditors can directly verify concept relevance for fairness

### 4. Content Moderation at Scale

**Use Case:** Understanding why a model flags inappropriate content.

**ConEx Advantage:** Moderators receive semantic explanations tied to policy violations:
- "Violence-related content (78%)" with spatial localization
- "Hate speech context (12%)" with supporting evidence
- Reduces over-reliance on pixel-level pattern matching that may not align with actual policy

### 5. Regulatory Compliance

**Use Case:** Demonstrating AI system transparency under GDPR, EU AI Act, or FDA requirements.

**ConEx Advantage:**
- **GDPR (Right to Explanation):** Concept-saliency explanations are more meaningful to users than technical pixel-level heatmaps
- **EU AI Act:** High-risk systems can document which visual features drive decisions
- **FDA Medical Device Approval:** Clear documentation of which clinical indicators the model uses

## Insights & Implications

### 1. Bridging Two Worlds

ConEx shows that saliency visualization and concept-based reasoning are *complementary*, not competing objectives. The unified framework demonstrates that:
- Saliency without concepts lacks semantic grounding → hard to act on
- Concepts without saliency lose spatial specificity → hard to verify
- Combined approach unlocks both interpretability *and* actionability

### 2. Unsupervised Concept Discovery at Scale

By leveraging vision-language models, ConEx removes a major bottleneck in concept-based XAI: the need for expensive manual concept engineering. This has implications for:
- **Scalability:** Systems can be deployed across new domains without redefining concepts
- **Consistency:** Concept discovery is reproducible and not subject to annotator disagreement
- **Adaptability:** Concepts can be updated as dataset or task requirements change

### 3. Architecture-Agnostic Explainability

The method works across CNNs and ViTs with minimal modification, suggesting a path toward truly model-agnostic explainability. This contrasts with many recent interpretability methods that require architecture-specific retraining or extensive adaptation.

### 4. Open Research Questions

- **Concept granularity:** How do discovered concepts vary with model depth, dataset size, and task complexity?
- **Concept drift:** How stable are learned concepts across model updates or retraining?
- **Concept transfer:** Can concepts learned from one model/dataset transfer to others?
- **Concept hierarchies:** Can ConEx discover hierarchical concept relationships (e.g., "color" as parent of "red")?

### 5. Limitations and Failure Cases

- **Vision-language model bias:** Concepts are constrained by biases in the VLM used (e.g., CLIP)
- **Segmentation quality:** Zero-shot segmentation (GroundedSAM) can fail on fine-grained visual patterns
- **Interpretability of concept vectors:** While concepts are semantic, the underlying CAVs remain black-box representations in feature space
- **Computational overhead:** Concept discovery involves multiple forward passes through segmentation models; exact computational cost unspecified

## Code & Resources

**Official Implementation:** [Repository link not provided in available sources]

**Dependencies:**
- Vision-Language Models: CLIP (OpenAI)
- Segmentation: GroundedSAM
- Model architectures: PyTorch or TensorFlow
- Evaluation: FunnyBirds, standard attribution toolkits

**Quick Start Guide:**
[Specific instructions unavailable — see full paper or official repository]

**Interactive Visualizations:**
[Availability of demos or interactive tools unspecified in search results]

## Related Work & Context

### Connection to Existing xAI Frameworks

1. **TCAV (Testing with Concept Activation Vectors) — Kim et al., 2018**
   - **Prior approach:** Requires manual concept definition or training concept classifiers
   - **ConEx innovation:** Discovers concepts automatically from vision-language priors
   - **Improvement:** Eliminates manual engineering; adds spatial grounding

2. **SHAP & LIME — Lundberg & Lee, 2017; Ribeiro et al., 2016**
   - **Prior approach:** Feature-level attributions without semantic meaning
   - **ConEx innovation:** Ties attributions to interpretable concepts
   - **Improvement:** Explanations are more actionable for domain experts

3. **Concept Bottleneck Models — Koh et al., 2020**
   - **Prior approach:** Forces intermediate layer predictions to match concepts
   - **ConEx innovation:** Post-hoc concept discovery; no model retraining
   - **Improvement:** Works with existing deployed models; more practical

4. **ProtoPNet & Prototype-based Methods — Chen et al., 2019**
   - **Prior approach:** Learns prototypical image patches
   - **ConEx innovation:** Concept-level rather than instance-level explanations; inherent spatial localization
   - **Improvement:** More generalizable across diverse visual patterns

### Broader xAI Research Trends

**Concept-based methods surge:** The xAI community has increasingly recognized that high-level concept representations better serve human understanding than pixel-level features. ConEx is positioned at the forefront of this shift.

**Vision-language models as explanation tools:** The use of CLIP and similar models for semantic understanding is becoming standard in recent xAI work, democratizing access to semantic priors.

**Multi-dimensional evaluation:** ConEx's four-part evaluation (faithfulness, concept quality, spatial accuracy, human interpretability) reflects a maturation of xAI evaluation standards beyond single metrics.

### Future Research Directions

- **Temporal concept evolution:** How do concepts change during model training or fine-tuning?
- **Cross-domain concept transfer:** Can concepts learned from ImageNet transfer to domain-specific tasks?
- **Concept interactions:** Do discovered concepts interact in non-linear ways to drive predictions?
- **Provably faithful explanations:** Combining ConEx with formal verification methods to guarantee explanation faithfulness
- **Multimodal extensions:** Extending concept-saliency explanations to video, audio, or text domains

## Summary of Key Contributions

1. **First unified framework** combining spatial saliency with semantic concept explanations
2. **Unsupervised concept discovery** via vision-language models, eliminating manual engineering
3. **Architecture-specific masking** that reduces noise in CNN and ViT concept representations
4. **Novel evaluation metrics** (VCM, CCM) for assessing concept quality and alignment
5. **Comprehensive multi-dimensional evaluation** demonstrating state-of-the-art performance across faithfulness, concept quality, spatial accuracy, and human interpretability

---

**Generated with [Claude Code](https://claude.ai/code)**
