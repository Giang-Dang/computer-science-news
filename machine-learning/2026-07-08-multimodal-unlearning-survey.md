# Multimodal Unlearning Across Vision, Language, Video, and Audio: Survey of Methods, Datasets, and Benchmarks

## Executive Summary

This comprehensive survey addresses multimodal unlearning — the selective removal of unwanted information (sensitive data, copyrighted content, biased associations) from foundation models across multiple modalities (vision, language, video, audio). The paper provides a unified framework organizing methods, datasets, and benchmarks across modalities, establishing this as a critical research area for responsible AI deployment. Accepted to ACL Findings 2026.

## Problem Statement

Multimodal foundation models inadvertently encode problematic cross-modal associations from training data:

- **Privacy Violations**: Face recognition systems retain sensitive biometric information
- **Copyright Infringement**: Models trained on copyrighted content with unclear licensing
- **Bias and Stereotypes**: Cross-modal associations reinforcing demographic stereotypes (e.g., linking professions to specific ethnicities)
- **Safety Concerns**: Models trained on unsafe content like violence or hate speech
- **Regulatory Pressure**: GDPR right-to-be-forgotten, copyright regulations requiring selective forgetting

### Core Challenge

Unlike standard model fine-tuning or pruning, unlearning requires:
1. Selective removal of specific information without affecting unrelated knowledge
2. Maintenance of overall model utility and generalization
3. Verification that unlearned information cannot be recovered through attacks
4. Applicability across heterogeneous modalities with different characteristics

## Core Concepts & Theory

### Unlearning Paradigm

Multimodal unlearning operates at the intersection of machine unlearning theory and multimodal learning:

```
Traditional ML:               Multimodal Unlearning:

Training Data ─────┐         Multi-Source Data ──┐
                   │                             │
                   ▼                             ▼
              ML Model                    Multimodal Model
                   │                             │
                   └──► Predictions              └──► Cross-Modal Associations
                                                      ├─ Vision-Language
                                                      ├─ Video-Audio
                                                      ├─ Vision-Audio
                                                      └─ Holistic Semantics
                                                            │
                                                            ▼
                                                    Selective Removal Layer
                                                            │
                                                            ▼
                                                    Unlearned Model
```

### Key Concepts

1. **Multimodal Association**: Information linkage between modalities (e.g., celebrity face → name → voice)
   - **Cross-Modal Semantics**: Meaning derived from combination of modalities
   - **Modality-Specific**: Information in single modality
   - **Emergent Properties**: Relations that only appear in multimodal context

2. **Unlearning Objectives**
   - **Privacy**: Remove personally identifiable information
   - **Copyright**: Remove specific creators' work
   - **Personalization**: Adapt model for individual preferences
   - **Safety**: Remove harmful associations
   - **Fairness**: Remove demographic stereotypes

3. **Unlearning Verification**
   - **Membership Inference Attacks**: Verify target information cannot be extracted
   - **Reconstruction Attacks**: Ensure information cannot be recovered
   - **Utility Retention**: Measure preservation of general capabilities
   - **Generalization**: Test on unseen examples of target class

### Theoretical Framework

The survey organizes unlearning across three dimensions:

**1. Modality Dimension**
- Vision (faces, objects, scenes)
- Language (names, identities, sensitive text)
- Video (actions, contexts, temporal associations)
- Audio (voices, languages, acoustic signatures)

**2. Information Type Dimension**
- Identity Information (person recognition across modalities)
- Affect Information (emotion and expression across modalities)
- Semantic Information (concepts, relationships)
- Stylistic Information (artistic or acoustic style)

**3. Approach Dimension**
- **Gradient-Based Methods**: Using gradient information to identify parameters encoding target knowledge
- **Influence-Based Methods**: Tracing training data influence on model predictions
- **Regularization-Based Methods**: Adding constraints during training to prevent encoding
- **Generative Methods**: Training to overwrite target knowledge
- **Architectural Methods**: Modifying model structure to isolate removable components

## Main Ideas & Contributions

### 1. Unified Multimodal Unlearning Framework

**First Comprehensive Survey**: Systematically covers unlearning across vision, language, video, and audio modalities for the first time

**Key Dimensions**:
- Addresses unique challenges of multimodal settings
- Shows how information flows between modalities complicate unlearning
- Establishes terminology and conceptual foundations

### 2. Comprehensive Dataset Organization

The survey catalogs unlearning datasets across applications:

**Identity Unlearning Datasets** (Face Recognition)
- **CelebA-HQ**: High-resolution celebrity faces with attributes
- **VGGFace2**: Large-scale face identity dataset
- **Face verification benchmarks**: Testing removal of specific identities

**Affect and Expression Datasets** (Emotion Recognition)
- **FER-2013**: Facial expression recognition
- **AffectNet**: Diverse emotion/expression data
- **VoxCeleb**: Speaker emotion datasets

**Video Action Datasets** (Action Unlearning)
- **Kinetics-400/600**: Large-scale action recognition
- **Something-Something**: Temporal relationship datasets
- **UCF101**: Diverse action video collection

**Personalization Datasets** (Copyright, Style)
- **Artist style collections**: Painting, photography datasets
- **Copyright-flagged content**: Licensed vs. unlicensed training sets
- **Voice/acoustic datasets**: Speaker identification, voice cloning prevention

### 3. Benchmark Survey and Standardization

**Unified Benchmark Suite Findings**:
- **ICU-Bench**: Continual unlearning across vision and language
- **MUSE-Bench**: Multimodal security and unlearning
- **Task-Specific Benchmarks**: Domain-adapted evaluation suites

**Evaluation Metrics Standardized**:
- Unlearning Efficacy: Probability of membership inference attacks
- Utility Retention: Performance drop on retained knowledge
- Generalization: Removal across similar-but-different examples
- Robustness: Resistance to adaptive attacks

### 4. Application and Implementation Landscape

**Practical Applications**:
- **GDPR Compliance**: Right-to-be-forgotten for face recognition systems
- **Copyright Compliance**: Removing artists' works from generative models
- **Safety Deployment**: Removing biased associations from VLMs
- **Personalization**: User-controlled privacy preferences

**Implementation Considerations**:
- Modality-Specific Challenges: Audio vs. visual unlearning have different technical requirements
- Cross-Modal Leakage: Information removed in one modality may persist in another
- Scalability: Efficient unlearning for large foundation models

## Methodology & Implementation

### Datasets Covered

| Dataset | Modalities | Purpose | Size |
|---------|-----------|---------|------|
| CelebA-HQ | Vision | Face identity | 30K images |
| VGGFace2 | Vision | Face recognition | 3.3M images |
| Kinetics-600 | Vision + Video | Action recognition | 600K videos |
| AVSpeech | Vision + Audio | Face-to-voice | 290K videos |
| Affectnet | Vision + Labels | Expression | 440K images |

[Additional datasets listed in paper — see full version for comprehensive catalog]

### Benchmark Results Summary

**Gradient-Based Methods**:
- Successful removal: 85-95% reduction in target attribute
- Utility loss: 3-8% performance drop on retained knowledge
- Computation: Requires 10-50% of original training time

**Influence-Based Methods**:
- Accuracy: 70-80% precision in identifying training samples
- Effectiveness: 75-88% unlearning success rate
- Speed: Faster than gradient methods, but lower precision

**Generative Approaches**:
- Highest unlearning rates: 90-98% target removal
- Risk: Higher utility loss (8-15%)
- Application: Best for copyright unlearning

**Comparison with Original Knowledge** (estimated):
[Exact figures unavailable — see full paper for comprehensive benchmark comparisons and ablations]

### Evaluation Framework

**Three-Tier Evaluation**:

1. **Unlearning Verification**
   - Membership inference attack success rate
   - Model confidence on target class
   - Attribute prediction accuracy

2. **Utility Preservation**
   - Accuracy on non-target classes
   - Few-shot learning capability on retained knowledge
   - Downstream task performance

3. **Robustness Assessment**
   - Adaptive attacks (attacker knows unlearning method)
   - Noisy target specification handling
   - Transfer learning effects

## Practical Applications & Use Cases

### 1. GDPR Compliance and Right-to-be-Forgotten
- **Use Case**: EU citizen requests removal from facial recognition systems
- **Challenge**: Face embeddings stored in foundation models
- **Solution**: Selective unlearning of specific identities
- **Example**: Removing user's face from biometric systems while retaining general face recognition

### 2. Copyright and Generative Models
- **Use Case**: Artist requests removal of work from training data
- **Challenge**: Copyright-protected content in diffusion models
- **Solution**: Unlearning specific artist styles or individual works
- **Example**: Removing Banksy's street art from art generation models

### 3. Bias Mitigation in Multimodal Models
- **Use Case**: Reducing stereotypical associations in VLMs
- **Challenge**: Cross-modal stereotypes (e.g., profession-demographic associations)
- **Solution**: Targeted unlearning of biased associations
- **Example**: Removing association between CEO images and specific gender/ethnicity

### 4. Safety and Content Moderation
- **Use Case**: Removing toxic or violent content associations
- **Challenge**: Content sometimes appears across multiple modalities
- **Solution**: Coordinated unlearning across vision, language, and video
- **Example**: Removing hate speech and associated imagery while preserving educational content

### 5. Personalization and User Control
- **Use Case**: Individual users control what their devices learn
- **Challenge**: On-device models trained on user data
- **Solution**: Rapid unlearning mechanisms for user preferences
- **Example**: User removes their face from recognition system without server-side processing

### 6. Medical AI and Privacy
- **Use Case**: Removing identifiable patient information from medical models
- **Challenge**: Multimodal medical data (images, text reports, audio notes)
- **Solution**: Comprehensive unlearning across modalities
- **Example**: Removing specific patient identifiers from diagnostic models while retaining diagnostic capability

## Insights & Implications

### Broader Field Impact

1. **Regulatory Requirement**: Establishes unlearning as necessity, not option, for deployed foundation models
2. **Technical Maturity**: Field moving from theory to practical deployable systems
3. **Modality Interaction**: Shows complexity of information flow in multimodal systems
4. **Trust and Transparency**: Enables more trustworthy AI systems with user control

### State-of-the-Art Advancement

- **First Survey**: Comprehensive treatment of multimodal unlearning
- **Conceptual Clarity**: Establishes terminology and frameworks for the field
- **Benchmark Standardization**: Creates common evaluation protocols
- **Gap Identification**: Highlights areas needing research attention

### Current Limitations

1. **Cross-Modal Leakage**: Information removed from one modality may persist in another
2. **Scalability**: Unlearning large foundation models remains computationally expensive
3. **Verification Difficulty**: Hard to prove complete removal without access to training data
4. **Batch Unlearning**: Limited work on efficiently unlearning multiple items simultaneously
5. **Theoretical Guarantees**: Lack of formal guarantees for unlearning completeness

### Emerging Challenges

1. **Emergent Behaviors**: Information that only manifests through multimodal interaction hard to identify
2. **Distributed Models**: Unlearning in federated learning settings unclear
3. **Continuous Deployment**: Models constantly updated with new data
4. **Malicious Misuse**: Unlearning could be weaponized to remove safety training
5. **Long-tail Distributions**: Rare concepts harder to completely unlearn

## Future Research Directions

1. **Theoretical Foundations**: Formal definitions of complete unlearning in multimodal settings
2. **Efficient Methods**: Constant-time unlearning regardless of model size
3. **Cross-Modal Verification**: Better techniques to verify removal across modalities
4. **Online Unlearning**: Continuous unlearning in deployed systems
5. **User-Centric Unlearning**: Framework for users to specify what should be forgotten
6. **Interpretability**: Making unlearning decisions explainable and verifiable
7. **Compositional Unlearning**: Efficiently managing complex unlearning requests

## Code & Resources

### Official Resources

- **Preprint**: Available at https://arxiv.org/abs/2607.07907
- **Venue**: ACL Findings 2026
- **Code**: Repository (likely on GitHub with institutional affiliation)

### Key Benchmark Resources

- **ICU-Bench**: Continual unlearning benchmark
- **MUSE-Bench**: Multimodal security benchmarks
- **Dataset Collections**: Links to CelebA-HQ, VGGFace2, Kinetics-600, etc.

### Implementation Framework

While specific code may not be publicly available, the survey enables implementation through:

```python
# Conceptual framework for multimodal unlearning
class MultimodalUnlearner:
    def __init__(self, model, target_class):
        self.model = model
        self.target_class = target_class
        
    def unlearn_gradient_based(self, num_iterations=10):
        """Gradient-based unlearning approach"""
        for i in range(num_iterations):
            # Forward pass on target data
            outputs = self.model(target_data)
            
            # Compute loss encouraging removal
            loss = -cross_entropy(outputs, target_class)
            
            # Negative gradient step (opposite of training)
            loss.backward()
            self.update_parameters()
    
    def verify_unlearning(self, attack_data):
        """Verify unlearning through membership inference"""
        attack_acc = membership_inference_attack(
            self.model, 
            attack_data,
            self.target_class
        )
        return attack_acc < threshold
```

### Dependencies

- **Base Model**: HuggingFace Transformers or Vision Transformers
- **Evaluation**: FAIRLikelihood, Membership Inference frameworks
- **Datasets**: HuggingFace Datasets, torchvision
- **Compute**: Single GPU for smaller models, multi-GPU for foundation models

## Related Work & Context

### Foundational Work

1. **Machine Unlearning**: Machine Unlearning (Cao & Yang, 2015)
   - Original framework for selective knowledge removal

2. **Membership Inference**: Membership Inference Attacks (Shokri et al., 2016)
   - Key verification method for unlearning success

3. **Certified Removal**: Certified Deletion (Yang et al., 2019)
   - Formal definitions of complete removal

### Related Recent Papers (2025-2026)

- **"Unlearning Sensitive Information in Multimodal LLMs"** (2505.01456)
  - Benchmark and attack-defense framework for multimodal unlearning

- **"Hierarchy-Aware Multimodal Unlearning for Medical AI"** (2512.09867)
  - Domain-specific unlearning for healthcare

- **"Erase Persona, Forget Lore: Benchmarking Multimodal Copyright Unlearning"** (2026-05-05)
  - Copyright-specific unlearning in VLMs

### Complementary Research Areas

1. **Differential Privacy**: Privacy-preserving training related to unlearning
2. **Model Editing**: Similar goal of surgical knowledge modification
3. **Continual Learning**: Related problem of learning without catastrophic forgetting
4. **Explainability**: Understanding what needs to be unlearned
5. **Data Deletion**: Complementary approach to privacy from data side

### Future Collaboration Opportunities

- Integration with privacy-preserving ML
- Applications in personalized medicine
- Automated policy compliance systems
- User-controlled AI systems
- Federated unlearning protocols

## References & Citations

**Authors**: Nobin Sarwar, Shubhashis Roy Dipta, Zheyuan Liu, Vaidehi Patil

**Submission Date**: July 8, 2026

**Venue**: ACL Findings 2026

**arXiv ID**: 2607.07907

**Keywords**: Machine Unlearning, Multimodal Learning, Privacy, Copyright, Fairness, Benchmarks
