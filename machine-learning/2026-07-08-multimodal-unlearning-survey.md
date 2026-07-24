# Multimodal Unlearning Across Vision, Language, Video, and Audio: Survey of Methods, Datasets, and Benchmarks

## Executive Summary

This comprehensive survey provides a unified, system-oriented view of multimodal machine unlearning—the selective removal of knowledge across vision, language, audio, and video modalities from foundation models. As multimodal AI systems inadvertently encode sensitive, copyrighted, biased, or unsafe cross-modal associations from training data, unlearning enables targeted knowledge deletion while preserving overall model utility. The paper presents a structured taxonomy of methods, datasets, and benchmarks that clarifies fundamental trade-offs among deletion strength, retention, efficiency, reversibility, and robustness, establishing a foundation for responsible multimodal AI development.

## Problem Statement

### The Unlearning Imperative

Modern multimodal foundation models present critical challenges for knowledge management:

1. **Privacy and Regulatory Compliance**: GDPR, CCPA, and emerging AI regulations mandate "right to be forgotten" and data deletion capabilities
2. **Copyright and Licensing**: Models trained on copyrighted images, text, video content create liability without removal mechanisms
3. **Bias and Harmful Associations**: Cross-modal biases (e.g., gender stereotypes in image-text associations) require targeted removal
4. **Safety and Adversarial Robustness**: Unsafe content associations (instructions for harm, inappropriate relationships) need selective deletion
5. **Distributed Knowledge Problem**: Knowledge spreads across shared representations, making localized deletion difficult

### Prior Limitations

- **Unimodal Focus**: Existing unlearning research primarily addresses single modalities (text or images), ignoring cross-modal knowledge dependencies
- **Training Retraining Gap**: Retraining from scratch after deletion is computationally prohibitive (100-1000x cost increase)
- **Retention-Deletion Trade-off**: Naive deletion often catastrophically damages remaining model capabilities
- **Evaluation Gaps**: Limited standardized benchmarks for assessing unlearning efficacy across modalities
- **Reversibility Questions**: Insufficient understanding of whether unlearning is truly irreversible

## Core Concepts & Theory

### Unlearning Definitions and Scope

**Machine Unlearning**: Selective modification of learned representations such that model behavior is altered as if specific training samples were never included, without retraining.

**Multimodal Unlearning**: Extension across modalities where deletion targets cross-modal associations and shared representations.

**Unlearning Dimensions**:
- **Modality Scope**: Identity unlearning (faces), content unlearning (copyrighted works), concept unlearning (biases)
- **Deletion Strength**: Exact (identical to retraining) vs. approximate (practical efficiency)
- **Reversibility**: Whether unlearning can be undone (relevant for staged deletion)

### Taxonomy of Unlearning Methods

#### 1. Gradient-Based Approaches
- **Gradient Ascent**: Reverse SGD to increase loss on target data
- **Influence Functions**: Identify training samples contributing most to target behavior
- Trade-off: Moderate efficiency, good retention

#### 2. Parameter-Efficient Methods
- **LoRA Unlearning**: Fine-tune low-rank adaptation factors to induce forgetting
- **Adapter Unlearning**: Modify adapter layers to selectively block learned patterns
- Trade-off: High efficiency, variable deletion strength

#### 3. Pruning and Masking
- **Weight Pruning**: Remove or zero out neurons/channels associated with target knowledge
- **Attention Masking**: Suppress attention patterns linking sensitive modalities
- Trade-off: Interpretable but potentially coarse-grained deletion

## Main Ideas & Contributions

### 1. Unified Multimodal Framework

The survey establishes first cross-modality unlearning taxonomy covering identity, affect, copyright, safety, and personalization unlearning.

### 2. Systematic Method Comparison

Structured comparison across deletion strength, retention, efficiency, reversibility, and robustness.

### 3. Comprehensive Dataset Organization

Datasets categorized by target type, modality, scale, and sensitivity level.

### 4. Benchmarking Frameworks

Standardized evaluation through MLLMU-Bench, ICU-Bench, OFFSIDE, and PULSE.

## Methodology & Implementation

### Experimental Scope

**Model Architectures Tested**:
- Vision-Language Models: CLIP, BLIP-2, LLaVA
- Generative Models: Stable Diffusion, AudioGen
- Specialized Models: Face recognition, emotion classifiers

### Evaluation Metrics

**Deletion Effectiveness**:
- Membership Inference Attack (MIA) Success Rate
- Forget Score: Task-specific accuracy drop on target samples
- Extraction Attack Resilience

**Retention Quality**:
- General Task Accuracy: Performance on non-target tasks
- Knowledge Distillation Metrics
- Downstream Task Transfer

**Efficiency**:
- Wall-clock Training Time vs. retraining baseline
- Parameter Updates: Fraction of model weights modified
- Memory Overhead

### Benchmark Results Summary

**Identity Unlearning**:
- Gradient-based methods: 85-95% deletion effectiveness, 92-98% retention
- LoRA unlearning: 80-90% effectiveness, 96-99% retention, 10-100x faster

**Copyright Unlearning**:
- Diffusion model unlearning: 70-80% effectiveness
- Generative unlearning: 60-85% effectiveness

**Continual Unlearning**:
- Sequential deletion: Catastrophic forgetting in 30-50% of scenarios
- ICU-Bench: 85%+ utility across 10+ deletion rounds

## Practical Applications & Use Cases

### 1. Privacy-Preserving Machine Learning
- Healthcare imaging: Remove patient scans while preserving disease detection
- Biometric systems: Purge face/voice data post-consent

### 2. Copyright and Licensing Management
- Remove licensed artwork, music, or text when licenses expire
- Track and remove copyrighted training examples

### 3. Bias Mitigation
- Remove gender/race stereotypes from image-caption models
- Systematic removal of proxy features

### 4. Safety and Content Moderation
- Remove instructions for dangerous activities
- Selective removal of misinformation

## Insights & Implications

### State-of-the-Art Advancement

This survey establishes multimodal unlearning as a distinct research area, demonstrating that cross-modal dependencies require coordinated deletion strategies.

### Broader Field Impact

1. **Regulatory Alignment**: Provides technical foundation for GDPR "right to be forgotten"
2. **Model Governance**: Enables post-deployment model modification without expensive retraining
3. **Trustworthy AI**: Critical infrastructure for responsible foundation model deployment

### Limitations and Open Questions

- Scalability to trillion-parameter models
- Cross-domain generalization of unlearning methods
- Formal verification that knowledge is truly unlearned
- Adversarial robustness to recovery attacks
- Temporal dynamics of knowledge resurgence

## Code & Resources

### Benchmark Suites
- MLLMU-Bench: Identity and content unlearning
- ICU-Bench: Continual multimodal unlearning
- OFFSIDE: Misinformation unlearning
- PULSE: Practical evaluation scenarios

### Datasets
- CelebA: 200K face images
- VGGFace2: 3.3M faces
- AffectNet: 1M faces with emotion labels
- LAION subset: Licensed vs. unlicensed image-text pairs

### Compute Requirements
- GPU: A100 or equivalent (80GB+ memory)
- Training time: Hours to days depending on model size

## Related Work & Context

### Foundational Unlearning Work
- **Machine Unlearning (Ginart et al., 2019)**
- **Membership Inference Attacks (Shokri et al., 2016)**
- **Influence Functions (Koh & Liang, 2017)**

### Multimodal Learning Foundations
- **CLIP (Radford et al., 2021)**
- **BLIP (Li et al., 2022)**
- **Stable Diffusion (Rombach et al., 2022)**

### Future Research Directions

1. Formal verification of unlearning
2. Few-shot unlearning
3. Distributed unlearning across model replicas
4. Temporal unlearning for continually trained models
5. Multi-task unlearning
6. Interpretable unlearning

---

**ArXiv ID**: 2607.07907  
**Submitted**: July 8, 2026  
**Venue**: ACL Findings 2026  
**Authors**: Nobin Sarwar, Shubhashis Roy Dipta, Zheyuan Liu, Vaidehi Patil
