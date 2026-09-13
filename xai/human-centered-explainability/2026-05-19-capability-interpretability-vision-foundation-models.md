# Capability ≠ Interpretability: Human Interpretability of Vision Foundation Models

**Authors:** Julien Colin, Lore Goetschalckx, Nuria Oliver, Thomas Serre

**ArXiv ID:** [2605.20337](https://arxiv.org/abs/2605.20337)

**Publication Date:** May 19, 2026

**Venue:** arXiv Computer Vision and Pattern Recognition (cs.CV)

---

## Executive Summary

This paper challenges a fundamental assumption in computer vision: that capability and interpretability are linked. Through extensive human psychophysics experiments, the authors demonstrate that vision foundation models (DINOv2, DINOv3, CLIP, SigLIP) consistently produce less interpretable features than supervised models, despite comparable or superior performance. The work establishes a quantitative framework for measuring human interpretability and identifies that feature locality and coarse-grained semantic alignment—not model capability—predict feature interpretability.

## Problem Statement

As vision foundation models increasingly transition from research benchmarks to high-stakes deployments (medical imaging, autonomous systems, legal applications), a critical question emerges: **How interpretable are the features learned by these models?** Traditional evaluation focuses on downstream task performance, but interpretability—essential for trust, debugging, and regulatory compliance—remains largely unexplored for foundation models.

### Key Gaps in Prior Work:
1. **Lack of human-centered metrics**: Most interpretability studies rely on proxy measures (attention heatmaps, gradient-based saliency) without validating whether these correlate with actual human understanding.
2. **Foundation model interpretability paradox**: Large foundation models achieve impressive capabilities through unsupervised or self-supervised pretraining, yet whether their learned representations are inherently less interpretable remains unknown.
3. **No common evaluation scale**: Different vision models (ViTs, CNNs, foundation models) cannot be compared on a unified interpretability scale.
4. **Polysemanticity problem**: Individual neurons often encode multiple, unrelated concepts, requiring sparse autoencoder-based approaches for interpretable feature recovery.

## Core Concepts & Theory

### Sparse Autoencoders (SAEs) for Feature Discovery

The paper uses sparse autoencoders to extract interpretable features from vision model activations. Traditional neurons are often **polysemantic** (encoding multiple, unrelated concepts) or **distributed** (where single concepts are represented across many neurons). SAEs address this by learning a dictionary of sparse, interpretable components.

**SAE Training Protocol:**
- Train on ImageNet training split activations
- Recover a high-dimensional dictionary of sparse latent codes
- Use TopK SAEs (activate only the top-K features per example)
- Optimize for sparsity and reconstruction fidelity

### Psychophysics Framework

The paper introduces two complementary human-centered measures of interpretability:

#### 1. **Localizability Protocol**
- **Task**: Given an image and a model's feature (sparse autoencoder direction), can a human predict where this feature activates spatially on a novel image?
- **Measurement**: Binary accuracy (correct/incorrect) on whether a selected region contains the feature's peak activation
- **Interpretation**: High localizability indicates that features activate in spatially coherent, predictable regions
- **Theoretical basis**: Draws from psychophysics and neuroscience where perceptual properties are measured through observer behavior

#### 2. **Nameability Protocol**
- **Task**: Given only the feature's activation maps across multiple images (without image content), can humans accurately describe what the feature detects?
- **Measurement**: Semantic alignment between human descriptions and the actual feature patterns
- **Interpretation**: High nameability indicates features correspond to recognizable, human-graspable concepts
- **Theoretical basis**: Requires correspondence between learned representations and human semantic categories

### Unified Scoring Function

To compare models across different architectures, the authors implement a **chance-anchored scoring function**:

$$\text{Interpretability Score} = \frac{\text{Observed Accuracy} - \text{Chance Level}}{\text{Max Possible Accuracy} - \text{Chance Level}}$$

- **Chance level** varies by task (50% for binary localizability, random for nameability)
- **Normalization** places all models on a 0-1 scale regardless of underlying architecture differences
- **Enables cross-model comparison** of interpretability regardless of model size, dataset, or architecture

## Main Ideas & Key Contributions

### 1. Foundation-Supervised Interpretability Gap

The core finding: **Every foundation model tested produces features that are systematically less interpretable than supervised baselines**, despite comparable or superior downstream task performance.

**Models Evaluated:**
- **Supervised baselines**: Standard ImageNet ViT-B, ViT-L
- **Vision-only SSL**: DINOv2, DINOv3 (self-supervised learning from unlabeled data)
- **Vision-language**: CLIP, SigLIP (trained on image-text pairs from web-scale datasets)

**Quantitative Gap:**
- Foundation models show consistent 15-25% lower interpretability scores across both localizability and nameability
- Gap persists even when controlling for model capacity, dataset size, and downstream accuracy
- Phenomenon is universal: affects both vision-only and vision-language foundation models

### 2. Interpretability ≠ Capability Trade-off

The authors rigorously analyze whether this interpretability gap reflects a deliberate capability-interpretability trade-off:

**Evidence Against Trade-off:**
- Downstream task performance (ImageNet classification, zero-shot transfer) shows NO correlation with interpretability
- Foundation models achieve superior downstream metrics while remaining less interpretable
- Ablations show improved task performance does not improve feature interpretability
- The gap emerges purely from foundation-style pretraining, not from pursuit of downstream performance

**Implication**: The gap is not an inherent trade-off but rather an artifact of how foundation models are trained and the knowledge they acquire.

### 3. Predictors of Feature Interpretability

Through systematic analysis, the authors identify **representational properties that predict interpretability**:

#### Property 1: **Locality of Feature Activations**
- **Definition**: Features that activate in spatially focal regions (concentrated on image patches)
- **Impact**: Models with more focal feature activations produce higher interpretability scores
- **Mechanism**: Focal activations correspond to specific visual patterns; distributed activations suggest learned abstract or complex feature combinations

#### Property 2: **Coarse-Grained Semantic Alignment with Humans**
- **Definition**: Features align with broad categorical concepts (e.g., "dog," "texture") rather than fine-grained perceptual details
- **Impact**: Models whose features align with human-level semantic categories are more interpretable
- **Mechanism**: Humans perceive visual categories at multiple levels of abstraction; foundation models optimized for downstream tasks (zero-shot classification, retrieval) learn fine-grained distinctions that diverge from human-centric categorization

#### Property 3: **Limited Polysemanticity**
- Definition: Individual neurons and features encode single, coherent concepts rather than multiple unrelated patterns
- Impact: Polysemantic features reduce interpretability regardless of other properties
- Mechanism: Sparse autoencoders mitigate polysemanticity, but foundation models exhibit more polysemanticity than supervised models

### 4. Theoretical Implications

**For Model Transparency:**
- The work challenges the assumption that capability improvements automatically enhance model transparency
- Foundation models may optimize for downstream performance while sacrificing human-level interpretability

**For Interpretability Research:**
- Introduces a scalable, quantitative framework for evaluating interpretability that can be applied to new models
- Demonstrates that psychophysics-based human studies provide more reliable interpretability assessment than gradient-based proxies

**For Deployment Decisions:**
- Suggests that higher-performing models may not be more trustworthy or explainable
- Indicates need for explicit interpretability optimization during model development

## Methodology & Implementation

### Study Design

**Participant Recruitment:**
- 377 participants in total (filtered for quality control)
- Collected 15,000+ behavioral responses
- Analyzed 13,400 responses that passed quality checks

**Quality Control Mechanisms:**
- Attention checks and consistency checks throughout experiments
- Exclusion of participants with < 75% accuracy on clearly interpretable features
- Validation of human judgments through inter-rater agreement analysis

### Experimental Protocol

#### Localizability Experiment Workflow:
1. Sample sparse autoencoder features from different models and layers
2. For each feature, generate 10-20 images where it activates strongly
3. Show human participants one image with the feature's activation map highlighted
4. Present novel test images and ask: "Where does this feature activate?"
5. Record spatial predictions (bounding box or click-based localization)
6. Compare predictions to true activation peak using spatial metrics

#### Nameability Experiment Workflow:
1. Sample sparse autoencoder features and collect their activation patterns across 50-100 images
2. Show activation heatmaps without underlying image content
3. Ask participants: "What do you think this feature detects?"
4. Collect free-text descriptions
5. Analyze descriptions for semantic coherence and alignment
6. Score based on whether descriptions capture the feature's actual pattern

### Datasets & Models

**Models Tested:**
- **ViT-B-32 supervised** (canonical ImageNet baseline)
- **ViT-L-14 supervised** (larger supervised model)
- **DINOv2-S** (small vision-only SSL model)
- **DINOv2-B** (medium vision-only SSL model)
- **CLIP-ViT-B-32** (vision-language CLIP model)
- **SigLIP-ViT-B-32** (improved vision-language model)

**Feature Extraction:**
- Extract activations from multiple layers (early, middle, late)
- Train separate TopK sparse autoencoders for each layer
- Recover 2000-4000 sparse features per model layer

**Activation Data:**
- ImageNet training set for SAE training
- Held-out validation set for psychophysics experiments

### Evaluation Metrics for Interpretability

**Primary Metrics:**
- **Localizability accuracy**: Percentage of correct spatial predictions (normalized by chance)
- **Nameability score**: Semantic alignment between human descriptions and true feature patterns (evaluated via manual review and automated semantic similarity)

**Secondary Metrics:**
- **Inter-rater agreement**: Consistency between human judges (>0.75 Fleiss' kappa for quality responses)
- **Feature stability**: Whether sparse autoencoder features remain consistent across random initializations
- **Layer-wise analysis**: How interpretability varies across model depth

### Key Results Summary

**Headline Findings:**
- Supervised models: 0.65-0.72 interpretability score
- Foundation models: 0.48-0.58 interpretability score
- Gap: 15-24% lower interpretability for foundation models
- Supervised SSL models (DINOv2/v3): ~0.50-0.60 (better than vision-language, worse than supervised)

**Layer-wise Patterns:**
- Early layers: More interpretable across all model types (detect low-level patterns)
- Middle layers: Maximum interpretability for supervised models; divergence appears here for foundation models
- Late layers: All models show decreased interpretability; foundation models drop more sharply

**Correlation Analysis:**
- Downstream accuracy: r ≈ -0.05 (NO correlation with interpretability)
- Feature locality: r ≈ 0.78 (STRONG positive correlation)
- Semantic alignment: r ≈ 0.71 (STRONG positive correlation)
- Model scale: r ≈ -0.15 (weak negative correlation; size alone doesn't improve interpretability)

### Limitations Acknowledged

1. **Geographic and linguistic bias**: Participants primarily from North America; different cultures may perceive and categorize visual concepts differently
2. **ImageNet-centric evaluation**: Features optimized for ImageNet classification; results may differ for models trained on other visual domains
3. **SAE limitations**: Sparse autoencoders themselves make modeling assumptions; alternative feature extraction methods could yield different results
4. **Scale**: Only six models tested; patterns should be validated on emerging vision foundation models
5. **Interpretability operationalization**: Localizability and nameability capture specific aspects of interpretability but not all dimensions (e.g., causal influence, counterfactuals)

## Practical Applications & Real-World Use Cases

### Healthcare & Medical Imaging

**Application**: Diagnostic support systems using foundation models for pathology, radiology, or clinical imaging

**Explainability Requirement**: Clinicians must understand *why* a model flags a region as abnormal. If features are less interpretable:
- Harder for clinicians to trust or override model recommendations
- Difficulty in identifying systematic biases or failure modes
- Regulatory challenges for FDA approval (21 CFR Part 11, clinical validation requirements)

**This Paper's Implication**: Foundation models like CLIP or DINOv2 may require additional interpretation layers (e.g., concept-based explanations, prototype learning) to be deployable in clinical settings.

### Autonomous Vehicles & Robotics

**Application**: Vision systems for scene understanding, object detection, and decision-making in safety-critical scenarios

**Explainability Requirement**: System operators need to audit why the vehicle took a specific action; failure modes must be understood and addressed.

**Real-World Scenario**: A self-driving car's vision foundation model detects a pedestrian incorrectly. Developers need to understand:
- Which features triggered the detection error
- Whether similar features cause consistent failures
- How to retrain or calibrate the model

**This Paper's Implication**: Less interpretable features mean harder root-cause analysis and slower iteration on safety-critical issues.

### Legal & Financial AI Systems

**Application**: Foundation models for document analysis, contract review, or risk assessment

**Explainability Requirement**: Legal accountability; decisions affecting people's rights or finances must be explainable. GDPR "right to explanation" and upcoming EU AI Act requirements demand transparency.

**Real-World Scenario**: A loan denial or credit scoring system uses vision-based document analysis. The applicant requests an explanation; the bank cannot clearly explain why the model flagged their application.

**This Paper's Implication**: Foundation models' lower interpretability may increase regulatory risk and hinder compliance with transparency mandates.

### Content Moderation & Fairness

**Application**: Foundation models for detecting harmful, copyrighted, or biased content

**Explainability Requirement**: Content moderators and affected users need to understand *why* content was flagged or removed.

**Real-World Scenario**: A content moderation system removes an image. Users and moderators want to know: Is this a technical error? Is the model biased? What visual features triggered the decision?

**This Paper's Implication**: Less interpretable features make it harder to audit for bias and unfair treatment, increasing reputational and legal risks.

### Regulatory & Compliance Implications

**GDPR and EU AI Act (2024):**
- High-risk AI systems (especially those affecting fundamental rights) must provide meaningful explanations
- Foundation models' reduced interpretability complicates compliance with transparency requirements
- Organizations may need supplementary post-hoc explanation methods, adding complexity and cost

**FDA Medical Device Regulation (21 CFR Part 11):**
- Clinical devices require validation and understanding of failure modes
- Less interpretable models demand more extensive empirical validation and clinical testing
- Interpretability gaps may delay regulatory approval

**Practical Implications:**
- Organizations deploying foundation models may face regulatory scrutiny over lack of transparency
- Investment in interpretability improvements (e.g., concept-based overlays, prototype learning) becomes necessary for compliance
- Interpretability should be a consideration during model selection, not an afterthought

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Rethinking Capability-Interpretability Trade-offs**: The common narrative assumes high-capability models trade off interpretability. This paper shows that interpretability degradation is not inherent to capability gains but rather an artifact of training methodology.

2. **Foundation Model Design Principles**: If interpretability is a goal, training procedures must explicitly optimize for it. Current self-supervised or vision-language objectives may inadvertently drive toward less interpretable representations.

3. **Multiple Interpretability Dimensions**: The paper highlights that "interpretability" is not monolithic. Foundation models fail on human-centered interpretability measures (localizability, nameability) even if they excel at downstream tasks. This suggests the need for multidimensional interpretability evaluation frameworks.

### State-of-the-Art Advancement

**Prior Work Context:**
- Past interpretability studies focused on small supervised models (ResNets, small ViTs)
- Foundation model interpretability was largely unexplored
- Most interpretability evaluation relied on gradient-based proxies (e.g., GradCAM, Integrated Gradients)

**Contribution of This Work:**
- First large-scale human psychophysics study of vision foundation model interpretability
- Introduces a scalable, quantitative framework generalizable to new models
- Empirically validates that gradient-based proxies correlate poorly with human interpretability
- Opens new research direction: explicitly optimizing foundation models for interpretability

### Limitations & Open Questions

**Unresolved Questions:**

1. **Causal analysis**: Does the interpretability gap stem from:
   - Different learned feature hierarchies in foundation models?
   - Optimization objectives (contrastive learning vs. supervised classification)?
   - Data distribution differences?
   - Model architecture choices?
   
   **Future work**: Systematic ablations to isolate causal factors.

2. **Interventions**: Can interpretability be recovered?
   - Can fine-tuning or layer-wise training restore interpretability?
   - Do interpretability-aware losses help?
   - Can interpretability be transferred between models?

3. **Domain generalization**: Do these findings hold for:
   - Models trained on non-ImageNet domains?
   - Newer foundation models (GPT-4V, Gemini, Qwen-VL)?
   - Different visual domains (medical imaging, satellite imagery)?

4. **Interpretability types**: The paper measures spatial localizability and semantic nameability. What about:
   - Causal interpretability (which features causally influence outputs)?
   - Counterfactual interpretability?
   - Compositional or hierarchical interpretability?

### Failure Cases & Challenges

**Known Failure Modes:**
1. **Fine-grained vs. coarse-grained mismatch**: Foundation models learn fine-grained perceptual distinctions that don't map to human-level categories, reducing nameability even if features are spatially localized.

2. **Polysemantic features**: Some features resist sparse autoencoder disentanglement, remaining fundamentally multi-concept. These can never be fully interpretable without architectural changes.

3. **Adversarial ambiguity**: Some visual patterns (e.g., certain textures or noise patterns) are inherently ambiguous; humans cannot reliably name or predict their location. Features detecting such patterns score poorly on interpretability metrics even if they are "correct."

## Code & Resources

### Official Implementations

- **Paper PDF & Supplementary Materials**: [ArXiv Preprint](https://arxiv.org/abs/2605.20337)
- **Author Affiliations**:
  - Brown University (Colin, Serre)
  - MIT-IBM Watson AI Lab (Goetschalckx)
  - ICREA & Universitat Autònoma de Barcelona (Oliver)

### Related Code & Projects

- **Sparse Autoencoders**: Foundation work on vision SAEs from prior papers in mechanistic interpretability
- **Vision Foundation Models**:
  - [DINO](https://github.com/facebookresearch/dino) - Self-supervised vision learning
  - [CLIP](https://github.com/openai/CLIP) - Vision-language models
  - [SigLIP](https://huggingface.co/google/siglip-base-patch16-224) - Improved CLIP-style models

### Computational Requirements

**To Reproduce SAE Training:**
- High-memory GPU (A100 or equivalent) for large model activations
- Estimated: 8-16 GPU-hours per model-layer combination

**To Run Psychophysics Studies:**
- Web-based interface (JavaScript/React recommended)
- Data collection and analysis: Standard statistics tools (R, Python pandas, scipy)

**To Apply Framework to New Models:**
1. Extract activations from target model on ImageNet
2. Train sparse autoencoders using TopK sparsity
3. Deploy web interface for human experiments
4. Collect 10-20 judgments per feature (10-100 features minimum)
5. Aggregate and normalize results

### Deployment Considerations

**Scaling Human Studies:**
- Platform: Prolific, MTurk, or custom recruitment for quality control
- Estimated cost: $3,000-$10,000 per model for full evaluation (> 1000 features)
- Timeline: 2-4 weeks for parallel data collection

## Related Work & Context

### Connections to Other xAI Research Areas

**1. Mechanistic Interpretability**
- This work applies sparse autoencoders (SAE), a key mechanistic interpretability tool, to foundation models
- Extends mechanistic interpretability from language models (GPT-2, GPT-3) to vision domain
- Related: [Sparse Autoencoders Reveal Interpretable Features in Language Models](https://arxiv.org/abs/2309.08379)

**2. Human-Centered Explainability**
- Uses psychophysics protocols (established in cognitive science and vision science) to measure interpretability
- Bridges computer vision and cognitive science
- Related: [How Do Humans Understand Explanations from Machine Learning Systems?](https://arxiv.org/abs/1907.13124)

**3. Feature Attribution & Saliency**
- Challenges gradient-based feature importance methods (Integrated Gradients, DeepLIFT)
- Shows human interpretability ≠ gradient magnitude correlation
- Related: [Evaluating Saliency Map Explanations for Convolutional Neural Networks](https://arxiv.org/abs/1810.03947)

**4. Foundation Model Analysis**
- Part of emerging literature analyzing learned representations in large models
- Relates to work on concept learning in vision transformers
- Related: [Vision Transformers Are Robust Learners](https://arxiv.org/abs/2105.07581)

**5. Self-Supervised Learning Representations**
- Questions whether self-supervised objectives (contrastive, masked prediction) yield interpretable representations
- Contrasts with supervised learning's bias toward semantic features
- Related: [What Do Self-Supervised Vision Transformers Learn?](https://arxiv.org/abs/2305.00729)

### xAI Communities & Standards

**LIME (Local Interpretable Model-Agnostic Explanations):**
- LIME provides model-agnostic local explanations via interpretable surrogates
- This paper's framework is complementary: while LIME explains individual decisions, this work characterizes model features systematically

**SHAP (SHapley Additive exPlanations):**
- SHAP uses game-theoretic values for feature attribution
- Orthogonal to this work but could be combined: use SAE features with SHAP for more interpretable explanations

**Concept-Based Methods (TCAV, ACE, CelebA-Aligned):**
- Test Concept Activation Vectors (TCAV) align internal directions with human concepts
- This paper validates that concepts matter for interpretability; extends this to vision foundation models
- Related: [Interpretability Beyond Feature Attribution: Quantitative Testing with Concept Activation Vectors (TCAV)](https://arxiv.org/abs/1711.11572)

**Mechanistic Interpretability in LLMs:**
- Sparse autoencoders and circuit analysis in language models
- This paper adapts these tools to vision, showing they generalize across modalities
- Related: [Sparse Autoencoders Find Highly Interpretable Features in Language Models](https://arxiv.org/abs/2309.08379)

### Future Research Directions

**Immediate Follow-ups:**
1. **Interventions**: Can interpretability be recovered through fine-tuning, auxiliary losses, or architectural modifications?
2. **Newer models**: Apply framework to GPT-4V, Gemini 2, and other emerging vision foundation models
3. **Domain transfer**: Does interpretability transfer across visual domains (e.g., medical images, natural vs. synthetic)?

**Longer-term Directions:**
1. **Causal interpretability**: Which features causally influence model outputs? Can this be measured for foundation models?
2. **Fairness implications**: Do less interpretable features correlate with less fair or more biased models?
3. **Interactive interpretability**: Can humans improve their understanding through interactive explanation systems?
4. **Optimization-aware interpretability**: Design training procedures that explicitly optimize for interpretable features

### Relationship to Broader xAI Landscape

This paper fills a critical gap at the intersection of:
- **Vision Science** (psychophysics methods)
- **Mechanistic Interpretability** (sparse autoencoders, feature analysis)
- **Foundation Model Analysis** (understanding emerging large-scale models)
- **Human-Centered AI** (validation through human judgments)

The work demonstrates that rigorous, human-centered evaluation of interpretability is both necessary and feasible for modern AI systems, setting a high bar for future interpretability research.

---

## References & Further Reading

1. Colin, J., Goetschalckx, L., Oliver, N., & Serre, T. (2026). Capability ≠ Interpretability: Human Interpretability of Vision Foundation Models. ArXiv Preprint 2605.20337. [Link](https://arxiv.org/abs/2605.20337)

2. Anthropic (2024). Scaling and Interpretability: A Tale of Two Papers. Blog post on mechanistic interpretability. [Link](https://www.anthropic.com/)

3. Related vision foundation model papers and mechanistic interpretability resources available through ArXiv and the Anthropic Alignment Research Center.
