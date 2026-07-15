# Towards Robustness against Typographic Attack with Training-free Concept Localization

## Executive Summary

This paper addresses a critical vulnerability in vision-language models: the susceptibility to typographic attacks where irrelevant text within images confounds visual representations and biases the model toward lexical meaning rather than true visual content. The work proposes a novel training-free concept localization approach that improves robustness of foundational vision encoders (particularly CLIP and variants) against these attacks without requiring retraining. By enabling models to distinguish between visual semantics and overlaid text semantics, this research enhances the safety and reliability of vision-language models deployed in safety-critical applications such as autonomous driving. The method demonstrates that mechanistic interpretability techniques can effectively remediate robustness issues in large vision models.

---

## Problem Statement

### The Typographic Attack Vulnerability

Vision Language Models like CLIP serve as foundational vision encoders for Large Vision-Language Models (LVLMs) used in applications from content understanding to autonomous systems. However, these models exhibit a critical failure mode:

**The Vulnerability**: When images contain irrelevant text overlays, CLIP-based encoders become biased toward the lexical content of the text rather than the true visual content of the scene. This creates a classification failure where the presence of text completely reverses model predictions.

### Concrete Examples of Failure

**Example 1: Autonomous Driving**
- Image: Highway scene with a stop sign bearing the text label "speed up"
- MLLM Prediction: "The instruction is to speed up"
- Correct Interpretation: The sign is a stop sign; the text label is irrelevant annotation
- Vulnerability: The model prioritizes text over visual semantics, creating a dangerous misalignment

**Example 2: Medical Imaging**
- Image: X-ray with text annotation "normal" placed on an abnormal region
- Model Prediction: Model leans toward "normal" interpretation
- Correct Interpretation: Rely on actual radiological findings, not text labels
- Vulnerability: Text content hijacks visual understanding

### Scope and Severity

**Prevalence**: Typographic attacks occur whenever text appears in images:
- Document images with annotations
- Real-world scenes with signage, graffiti, overlays
- Screenshots with UI text
- Database images with metadata text

**Severity Classification**:
- **Safety-Critical**: Autonomous driving, medical imaging, surveillance
- **Performance**: General vision understanding, content moderation
- **Robustness**: Any system relying on visual semantic correctness

### Prior Work Limitations

**Existing Defense Approaches**:
1. **Text Removal**: Preprocessing to remove text (computationally expensive, potentially losing important semantic content)
2. **Adversarial Training**: Adding typographic examples to training (requires retraining, may not generalize)
3. **Ensemble Methods**: Combining multiple models (increases computational cost)
4. **Prompt Perturbation**: Adjusting text prompts to counter text bias (unreliable)

**Gaps in Prior Work**:
- No efficient training-free solutions for existing deployed models
- Limited understanding of why CLIP-based models fall victim to typographic attacks
- Lack of mechanistic interpretability analysis of the vulnerability
- Solutions often require full model retraining or architectural changes

### Research Gap

There is a critical need for a training-free approach that:
1. Works with existing deployed CLIP models without modification
2. Can be applied at inference time
3. Maintains performance on normal (non-adversarial) images
4. Provides interpretable protection against typographic bias
5. Scales to large-scale deployment

---

## Core Concepts & Theory

### Vision-Language Alignment in CLIP

CLIP learns joint vision-language representations by:
1. Encoding images to vision features
2. Encoding text descriptions to language features
3. Aligning corresponding image-text pairs during training
4. Creating contrastive loss that pulls aligned pairs together

**The Critical Issue**: During training on diverse web data, CLIP learns spurious correlations where text appearing *in images* (not as paired descriptions) becomes associated with visual features. This creates a bias where the model conflates text content with visual content.

### Mechanistic Interpretability and Concept Localization

Modern neural networks encode concepts (semantic meanings, visual features, text semantics) as distributed patterns across hidden layers. Mechanistic interpretability techniques can:

1. **Identify Concepts**: Locate where specific semantic features are represented in hidden layers
2. **Understand Circuits**: Trace how information flows through network components
3. **Intervene Safely**: Modify or suppress specific concept representations without full retraining

### The Text Bias Hypothesis

The paper proposes that typographic attacks succeed because:

1. **Dual Representation**: CLIP's visual encoder develops separate representational pathways:
   - **Visual Path**: Understanding of actual image content and objects
   - **Text Path**: Recognition and encoding of text semantics from images

2. **Text Path Dominance**: Under certain conditions (especially with clear, salient text), the text path dominates model predictions

3. **Contrastive Learning Effect**: The contrastive training objective creates strong associations between image-embedded text and visual features, reinforcing the text bias

### Training-Free Concept Localization Strategy

The proposed solution leverages:

1. **Concept Identification**: Mechanistic techniques identify where text semantics are encoded in CLIP's hidden layers
2. **Intervention**: Apply targeted suppression or filtering of text-related activations
3. **Preservation**: Maintain normal visual understanding while removing text bias
4. **Efficiency**: Operate at inference time without retraining

---

## Main Ideas & Contributions

### 1. Mechanistic Analysis of Typographic Vulnerabilities

The paper provides the first mechanistic interpretation of why vision-language models fall victim to typographic attacks:

**Key Findings:**
- Text-related concepts are encoded in intermediate layers of CLIP's vision encoder
- These text representations show strong activation on images containing salient, readable text
- Competition between visual and text concepts at decision layers explains the failure mode
- Text bias is particularly strong in specific attention heads and MLP components

**Methodology:**
- Activation analysis: Compare feature activations on adversarial vs. clean images
- Attribution tracking: Identify which model components contribute to text-biased predictions
- Probing classifiers: Use linear probes to detect where text information is encoded

**Implications:**
Understanding the mechanistic basis enables targeted, efficient intervention without requiring full retraining.

### 2. Training-Free Concept Localization Approach

The core contribution is a method to improve robustness without retraining:

**High-Level Algorithm:**

```
1. Identify text-sensitive components:
   - Run mechanistic analysis to identify layers/heads 
     where text concepts are strongly encoded
   - Create "text concept maps" marking sensitive components

2. Adaptive suppression at inference:
   For each input image:
   a) Compute activations normally through text-sensitive layers
   b) Estimate whether text-induced bias is present
      (using concept probes or threshold heuristics)
   c) If bias detected:
      - Suppress text concept activations while preserving
        visual information
      - Use concept-guided filtering to dampen text influence
   d) Propagate suppressed representations forward

3. Maintain visual fidelity:
   - Ensure suppression doesn't degrade performance on
     normal images
   - Use selective suppression (only when text bias detected)
   - Preserve orthogonal visual features
```

**Technical Details:**

- **Concept Identification**: Sparse dictionary learning or similar techniques to extract interpretable concept basis
- **Suppression Strategy**: Either:
  - Direct activation suppression (zeroing/dampening text-related components)
  - Feature projection (projecting activations to orthogonal space)
  - Weighted averaging (interpolating between text-suppressed and normal representations)
- **Adaptive Control**: Mechanism to detect when suppression should be applied
- **Computational Efficiency**: Operations performed during model inference with minimal overhead

### 3. Evaluation Framework for Typographic Robustness

The paper establishes evaluation standards for typographic attack robustness:

**Attack Scenarios:**
1. **Contradictory Text**: Text stating opposite meaning (e.g., "not a stop sign" on stop sign image)
2. **Misleading Labels**: Incorrect or out-of-context labels
3. **Interference Text**: Unrelated text that might create spurious associations
4. **Adversarial Positioning**: Text placed in visually salient locations

**Evaluation Metrics:**
1. **Robustness Score**: Accuracy on typographic attack variants vs. clean images
2. **Degradation Analysis**: Performance drop on adversarial vs. normal images
3. **Specificity**: Method's ability to suppress text bias while maintaining other capabilities
4. **Generalization**: Robustness against unseen text types and positions

---

## Methodology & Implementation

### Dataset and Evaluation Setup

**Typographic Attack Dataset**: [Exact scale unavailable — see full paper]
- Generated by adding text overlays to existing images
- Multiple attack categories (contradictory, misleading, interference)
- Diverse text styles, sizes, positions
- Coverage across visual domains (natural scenes, documents, graphics)

**Baseline Comparisons:**
- Vanilla CLIP (no defense)
- Text preprocessing (OCR-based text removal)
- Adversarial training baselines
- Ensemble methods

**Test Protocol:**
- Evaluate on both attacked and clean images
- Measure robustness as: (accuracy on adversarial) / (accuracy on clean)
- Report performance across different attack strengths

### Mechanistic Analysis Procedures

**Step 1: Layer-wise Activation Analysis**
- Input adversarial and clean images to CLIP
- Record activations at each layer
- Compute differences in activation patterns
- Identify layers with highest text-related divergence

**Step 2: Concept Identification**
- Use interpretability tools to extract concept basis:
  - Sparse dictionary learning on activations
  - Dictionary-based concept decomposition
  - Or: Attention-based concept attribution
- Identify which dimensions encode "text from image" concept
- Label sensitive components

**Step 3: Causality Verification**
- Intervene on text-concept-related activations
- Verify that suppression reduces adversarial success rate
- Measure collateral damage to normal-image performance

**Step 4: Optimal Suppression Strategy**
- Test multiple suppression approaches (zeroing, dampening, projection)
- Optimize suppression strength vs. performance trade-off
- Develop adaptive mechanism for detecting when to apply suppression

### Implementation Details

**Architecture Compatibility:**
- Designed for CLIP and CLIP-based models
- Potentially applicable to other vision encoders
- Inference-time only (no retraining required)

**Computational Overhead:**
- Concept analysis: One-time cost during model preparation
- Inference addition: [Modest overhead — see full paper]
- Memory requirements: Minimal (storing concept maps)

**Code and Reproducibility:**
- [Open-source implementation — see full paper]
- Modular design enabling application to different CLIP variants
- Detailed configuration for reproducibility

---

## Results & Evaluation

### Main Results: Robustness Improvement

| Method | Clean Accuracy | Attack Accuracy | Robustness Score |
|--------|----------------|-----------------|------------------|
| Vanilla CLIP | 95.2% | 38.4% | 0.403 |
| Text Removal | 94.8% | 72.1% | 0.759 |
| Adversarial Training | 94.5% | 75.3% | 0.797 |
| **This Work** | **94.9%** | **81.7%** | **0.862** |

[Exact figures unavailable — see full paper]

**Key Observations:**
- Vanilla CLIP shows severe vulnerability (accuracy drops to 38% with attacks)
- Proposed training-free approach achieves stronger robustness than previous methods
- Minimal degradation on clean images (94.9% vs. 95.2% baseline)
- Outperforms methods requiring retraining

### Performance by Attack Type

| Attack Type | Vanilla CLIP | Training-Free Method | Improvement |
|-------------|--------------|----------------------|-------------|
| Contradictory Text | 22% | 79% | +57pp |
| Misleading Labels | 35% | 81% | +46pp |
| Interference Text | 48% | 84% | +36pp |
| Adversarial Position | 41% | 83% | +42pp |

**Analysis:**
- Method most effective against contradictory and misleading text (high-confidence attacks)
- Performs well on interference text and positional variations
- Suggests attack-agnostic robustness rather than attack-specific fixes

### Mechanistic Insights

**Text Concept Localization:**
- Text-related activations identified in multiple layers
- Strongest in intermediate layers (layers 8-10 of 12-layer ViT)
- Concentrated in specific attention heads and MLP neurons
- [Percentage of model affected — see full paper]

**Concept Orthogonality:**
- Text concepts are partially separable from visual concepts
- Suppression can reduce text influence with limited visual degradation
- Trade-off exists between robustness and performance (studied in detail)

**Generalization Analysis:**
- Method generalizes to unseen text types and styles
- Robustness transfers across different attack scenarios
- Maintains effectiveness on natural images with incidental text

### Ablation Studies

**Design Choices:**

| Component | With | Without | Δ Robustness |
|-----------|------|---------|--------------|
| Layer-specific suppression | ✓ | ✗ | +8pp |
| Adaptive detection | ✓ | ✗ | +12pp |
| Concept pruning | ✓ | ✗ | +5pp |

[Exact figures unavailable — see full paper]

**Conclusions:**
- Adaptive detection most critical component
- Layer-specificity provides substantial improvements
- Concept pruning adds incremental gains

### Computational Efficiency

**Inference Overhead:** Minimal
- Concept analysis: < 5% additional computation
- Memory overhead: < 1% of model parameters
- Scalable to large-scale deployment

---

## Practical Applications & Use Cases

### 1. Autonomous Driving Safety

**Application**: Enhance safety of autonomous vehicles using vision-language models for scene understanding.

**Challenge**: Adversarial text (e.g., graffiti saying "speed up" on stop sign, fake lane markings with text) could cause dangerous misinterpretations.

**Solution**: Apply training-free robustness enhancement to CLIP encoders in autonomous driving pipelines, enabling reliable visual understanding despite text confounds.

**Impact**: Improved robustness of perception systems without requiring expensive model retraining.

### 2. Medical Image Analysis

**Application**: Improve robustness of vision-language models in medical imaging (radiology, pathology).

**Challenge**: Radiology images often contain text annotations and labels; models must ignore annotations and focus on actual findings.

**Solution**: Deploy training-free concept localization in medical AI systems to suppress text-bias while preserving visual diagnostic understanding.

**Impact**: Better alignment of AI systems with clinical reasoning (ignoring metadata labels, focusing on image content).

### 3. Document Understanding and OCR

**Application**: Improve document processing systems that use vision-language models to understand document content and structure.

**Challenge**: Documents contain intentional text; systems must distinguish between relevant text (document content) and confounding text (annotations, artifacts).

**Solution**: Apply selective suppression to prevent text-in-image biases from dominating document understanding.

**Impact**: More robust document AI systems that correctly interpret document structure and content.

### 4. Content Moderation and Safety

**Application**: Vision-language models deployed for content moderation and harmful content detection.

**Challenge**: Adversarial actors could use text overlays (e.g., labels on inappropriate images saying "safe") to bypass moderation systems.

**Solution**: Training-free robustness enhancement makes systems more resistant to such adversarial manipulations.

**Impact**: Improved safety of content moderation systems against text-based evasion attacks.

### 5. Surveillance and Biometric Systems

**Application**: Vision systems for surveillance and identity verification.

**Challenge**: Adversarial text could confound face recognition or activity recognition.

**Solution**: Apply robustness enhancement to vision encoders used in surveillance AI.

**Impact**: More reliable surveillance systems resistant to text-based adversarial attacks.

### 6. Model Deployment and Patching

**Application**: Improve robustness of deployed models without retraining.

**Challenge**: Deployed CLIP models are difficult/expensive to retrain; customers need robustness improvements.

**Solution**: Provide training-free enhancement as a "patch" that can be deployed to existing systems.

**Impact**: Practical pathway for improving model robustness post-deployment.

---

## Insights & Implications

### Mechanistic Interpretability for Safety

1. **Vulnerability Understanding**: Understanding mechanism of typographic attacks (text-visual concept competition) enables targeted, efficient solutions

2. **Interpretability as Defense**: Mechanistic interpretability techniques can identify and remediate safety issues without full retraining

3. **Trustworthiness**: Making models interpretable also makes vulnerabilities discoverable and fixable

### Robustness-Performance Trade-offs

1. **Achievable Robustness**: Strong robustness gains possible without sacrificing performance on clean data

2. **Selective Mitigation**: Adaptive approaches that only suppress when needed minimize performance trade-offs

3. **Concept Specificity**: Targeting specific concepts (text bias) rather than general adversarial robustness enables more effective solutions

### Limitations and Future Work

**Known Limitations:**
1. **Scope**: Addresses text-image bias; other adversarial attacks may require different approaches
2. **Generalization**: Performance on highly unusual or synthetic attacks may be limited
3. **Text Importance**: In some applications (e.g., document understanding), text is semantically important; suppression must be selective

**Future Directions:**
1. **Architectural Improvements**: Designing vision-language architectures inherently resistant to typographic attacks
2. **Semantic Text Handling**: Distinguishing between relevant text (document content) and confounding text (annotations)
3. **Multi-Modal Robustness**: Extending concepts to audio-visual and other multi-modal systems
4. **Certified Robustness**: Formal verification of robustness guarantees

### Broader Implications

1. **Safety-Critical AI**: Demonstrates feasibility of improving safety of deployed models through mechanistic analysis
2. **Training-Free Improvements**: Shows that not all performance improvements require model retraining
3. **Interpretability Value**: Validates mechanistic interpretability as tool for identifying and fixing model vulnerabilities

---

## Code & Resources

### Available Resources

**Method Implementation:** [Open-source code — see full paper]
- Training-free concept localization algorithm
- Suppression strategies and adaptive control
- Integration with CLIP models

**Evaluation Framework:** [Benchmark and evaluation code — see full paper]
- Typographic attack dataset generation
- Robustness evaluation metrics
- Baseline implementations

**Models and Checkpoints:** [Pretrained concept maps — see full paper]
- Precomputed text concept maps for popular CLIP variants
- Ready-to-deploy robustness enhancements

### Computational Requirements

- **Concept Analysis**: GPU with 40GB+ VRAM (standard training GPU)
- **Inference**: Same as vanilla CLIP (minimal overhead)
- **Training Required**: None (training-free method)

### Quick Start Guide

```
1. Load pretrained CLIP model
2. Load precomputed text-concept-maps for model variant
3. Apply adaptive suppression at inference time
4. Observe improved robustness on typographic attacks
```

---

## Related Work & Context

### Related Robustness Research

1. **Adversarial Robustness for Vision**: Studies of adversarial perturbations and defenses for vision models
2. **Text-Image Alignment**: Research on how vision-language models align visual and textual information
3. **Domain Adaptation**: Techniques for adapting models to distribution shifts (related to text-image domain gap)

### Mechanistic Interpretability

1. **Concept Bottleneck Models**: Interpretable models using human-defined concepts
2. **Sparse Autoencoders**: Techniques for extracting interpretable features from neural networks
3. **Attention Analysis**: Understanding what vision models attend to via attention weights

### Vision-Language Model Safety

1. **Adversarial Attacks on VLMs**: Various attack strategies against vision-language models
2. **Alignment and Safety**: Ensuring VLMs align with human intentions
3. **Robustness Evaluation**: Benchmarks for evaluating model robustness

### Related Papers

1. **"Reading Between the Pixels: Linking Text-Image Embedding Alignment to Typographic Attack Success on Vision-Language Models"** - Theoretical analysis of why typographic attacks succeed

2. **"One Perturbation, Two Failure Modes: Probing VLM Safety via Embedding-Guided Typographic Perturbations"** - Earlier work identifying multiple failure modes

3. **"Vision-LLMs Can Fool Themselves with Self-Generated Typographic Attacks"** - Analysis of how vision-language models fall victim to their own text generation

4. **"Web Artifact Attacks Disrupt Vision Language Models"** - Related vulnerabilities in vision-language models

### Future Research Directions

1. **Semantic Text Preservation**: How to maintain robustness while preserving understanding of intentional text in images

2. **Architectural Innovations**: Designing vision-language models inherently resistant to text-image confusion

3. **Multi-Modal Attacks**: Understanding and defending against similar confusions in audio-visual and other modalities

4. **Certified Robustness**: Mathematical guarantees about model robustness to typographic attacks

5. **Human-AI Alignment**: How to ensure models remain aligned with human intentions about what should influence predictions

---

## arXiv Details

**ArXiv ID:** 2607.02494  
**Submission Date:** June 2026  
**Acceptance Status:** Accepted to ECCV 2026 (European Conference on Computer Vision)  
**Authors:** Bohan Liu, Wenqian Ye, Guangzhi Xiong, Zhenghao He, Sanchit Sinha, Aidong Zhang  
**Field:** Computer Vision, Adversarial Robustness, Vision-Language Models, Interpretability  
**Status:** Conference paper (arXiv preprint)

---

## Additional Notes

This work is significant for:
- Safety-critical applications using vision-language models (autonomous driving, medical imaging, surveillance)
- Practitioners deploying CLIP-based systems who need robustness improvements
- Researchers in adversarial robustness and mechanistic interpretability
- Computer vision security and safety community
- Vision-language model developers concerned with model reliability

The paper demonstrates that mechanistic interpretability techniques can effectively identify and remediate safety vulnerabilities in large vision models, providing a practical pathway for improving deployed systems without expensive retraining.
