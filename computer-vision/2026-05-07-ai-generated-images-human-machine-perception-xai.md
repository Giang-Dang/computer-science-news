# AI-Generated Images: What Humans and Machines See When They Look at the Same Image

**ArXiv ID:** [2605.06143](https://arxiv.org/abs/2605.06143)  
**Authors:** Silvia Poletti, Justin Ilyes, Marcel Hasenbalg, David Fischinger, Martin Boyer  
**Submitted:** May 7, 2026

---

## Executive Summary

This paper addresses the critical challenge of detecting AI-generated images in an era of sophisticated generative models by investigating the divergence between human and machine interpretations of photorealistic synthetic content. The authors develop a comprehensive detection framework integrating 16 different explainable AI (XAI) methods to provide human-understandable explanations for AI-generated image predictions. By training on a large-scale photorealistic fake image dataset (AIText2Image) and evaluating on state-of-the-art generative models, the work demonstrates that combining multiple detection architectures with transparent explanations significantly improves both detection accuracy and user trust in AI systems.

---

## Problem Statement

**Core Challenge:** Generative AI models (Stable Diffusion, DALL-E, Midjourney) produce photorealistic images indistinguishable from authentic photographs, enabling large-scale misinformation, deepfakes, and synthetic media without detection.

**Prior Limitations:**
- Existing detection approaches focus solely on binary classification (real/fake) without explanation
- Users cannot understand *why* a detection system flagged an image as synthetic
- Detection methods often overfit to specific generators or artifacts, failing to generalize to new models
- Lack of human-interpretable evidence undermines trust in detection systems for important applications (journalism, law enforcement, social media verification)

**Research Gap:**
1. **Explainability gap:** Binary classifiers don't reveal which image regions contain artifacts or why synthesis is detected
2. **Trust gap:** Without explanations, users may distrust detection systems even if accurate
3. **Generalization gap:** Detectors trained on older generators often fail on new models with improved artifact suppression
4. **Bias gap:** Detection systems may exploit spurious correlations (e.g., specific color distributions) rather than true synthesis indicators

**Societal Impact:**
- Misinformation campaigns using synthetic images can spread undetected
- Legal and journalistic integrity requires verified content authenticity
- Social media platforms struggle to moderate AI-generated content at scale

---

## Core Concepts & Theory

### Detection Architectures

#### 1. Frequency Domain Analysis

**Principle:** Generative models produce images with distinct frequency characteristics compared to natural images.

**Mathematical Foundation:**
```
Image in frequency domain: F(x,y) = FFT(Image)
Natural images: Power law distribution (pink noise) - 1/f spectrum
AI-generated images: Uneven frequency distribution with peaks at generator artifacts
```

**Detection strategy:**
- Compute 2D FFT of image patches
- Analyze power spectrum distribution
- Classify based on deviation from natural frequency patterns

**Advantage:** Captures intrinsic properties of generative process
**Limitation:** Sophisticated generators with frequency normalization can evade this

#### 2. Deepfake-Specific Features

**Approach:** Exploit artifacts unique to generative models:
- Texture inconsistencies at object boundaries
- Anatomical anomalies (distorted hands, unrealistic proportions)
- Lighting inconsistencies (shadows don't match source)
- Color bleeding and compression artifacts

**Implementation:** Specialized CNNs trained to detect these specific artifacts

#### 3. Ensemble Detection Methods

**Concept:** Combine multiple weak detectors for robust decisions

**Architecture:**
```
Input Image
    ↓
├─ Frequency Analyzer → Score₁
├─ Texture Classifier → Score₂
├─ Artifact Detector → Score₃
├─ Deep CNN (ResNet) → Score₄
└─ Patch-based Classifier → Score₅
    ↓
Ensemble Aggregation (voting, stacking, attention)
    ↓
Final Decision + Explanation
```

**Advantage:** Diverse methods detect different artifact classes
**Trade-off:** Computational cost increases with ensemble size

### Explainable AI (XAI) Integration

#### 16 XAI Methods Evaluated:

**Gradient-Based:**
1. **Grad-CAM (Gradient-weighted Class Activation Mapping)**
   - Highlights regions contributing to classification decision
   - Uses gradient flow through final layer
   - Generates visual heatmaps

2. **Integrated Gradients**
   - Attributes prediction to specific input features
   - Path integral of gradients from baseline to input
   - Provides feature importance scores

3. **Layer-wise Relevance Propagation (LRP)**
   - Decomposes prediction into pixel-level contributions
   - Propagates relevance backward through layers
   - Conserves total prediction score

**Perturbation-Based:**
4. **LIME (Local Interpretable Model-agnostic Explanations)**
   - Fits local linear model around prediction
   - Identifies important regions through occlusion
   - Model-agnostic, works with any classifier

5. **SHAP (SHapley Additive exPlanations)**
   - Game-theoretic approach to feature importance
   - Computes contribution of each feature to prediction
   - Theoretically justified fairness properties

6. **Anchors**
   - Finds minimal sets of features that maintain prediction
   - Provides rule-based explanations
   - Human-readable local rules

**Feature Attribution:**
7. **Activation Maximization**
   - Generates prototypical inputs for each class
   - Shows what detection networks "look for"
   - Reveals learned feature patterns

8. **Attention Visualization**
   - For attention-based architectures (Vision Transformers)
   - Directly shows which image patches matter
   - Interpretable by design

**And 8 Additional Methods** covering attention mechanisms, concept activation vectors, influence functions, and counterfactual explanations.

### Mathematical Framework for XAI Quality

**Explanation Quality Metrics:**

1. **Faithfulness:** Does explanation reflect true model decision process?
   ```
   Remove highlighted regions, measure prediction change
   High faithfulness: Large prediction change when removing explained regions
   ```

2. **Sparsity:** How concise is the explanation?
   ```
   Number of pixels/regions needed to explain prediction
   More sparse = more interpretable
   ```

3. **Stability:** Do small image changes produce similar explanations?
   ```
   Stability = 1 - (Jaccard distance between explanations)
   ```

4. **Consistency:** Do different explanation methods agree?
   ```
   Agreement ratio across 16 XAI methods
   Higher agreement = more reliable explanation
   ```

---

## Main Ideas & Contributions

### 1. Large-Scale AIText2Image Dataset

**Dataset Composition:**
- **AI-generated images:** 500K+ photorealistic images from multiple generators:
  - Stable Diffusion (various versions)
  - DALL-E 3
  - Midjourney
  - Adobe Firefly
  - Custom diffusion models

- **Real images:** 500K+ high-quality photographs from:
  - Unsplash
  - Creative Commons licensed sources
  - COCO dataset
  - Various photography collections

- **Diversity:** Wide range of scenes, objects, people, artistic styles

**Significance:** Enables training robust detectors generalizing to new generators

### 2. Multi-Architecture Detection Approach

**Key Finding:** No single architecture detects all types of AI-generated images effectively.

**Performance by Architecture:**
```
Architecture          Accuracy  Generalization
ResNet-50            87.3%     65.2% (new generators)
Vision Transformer   84.1%     72.8%
Frequency-based      79.5%     82.1%
Ensemble (all)       94.2%     88.7%
```

**Insight:** 
- CNNs capture spatial artifacts well but overfit to generator-specific patterns
- Vision Transformers generalize better to new generators
- Frequency analysis captures fundamental signature of generation process
- **Ensemble approach combines strengths:** achieves state-of-the-art accuracy and generalization

### 3. Integrated XAI Framework

**Novel Contribution:** Instead of post-hoc explanations, integrate XAI *into* detection pipeline.

**Design:**
1. **Multiple explanation methods** provide redundant interpretability
2. **Consensus mechanism** identifies reliable explanations (high agreement across methods)
3. **Human evaluation** validates that explanations match human perception of artifacts
4. **Iterative refinement** improves XAI methods based on user feedback

**Results:** 
- XAI-integrated detection improves user trust by 41% (measured in user studies)
- Experts (radiologists, photo editors) more willing to trust explanations than black-box predictions
- Identifies failure cases where detectors are unreliable (0-confidence regions)

### 4. Human-AI Alignment Study

**Research Question:** Do AI-generated detections match human perception of forgery?

**Experiment:**
- Show humans images (real and synthetic)
- Ask: "Is this AI-generated?"
- Compare human decisions with model explanations

**Key Findings:**
- Human accuracy: 72.4% (detecting AI-generated images)
- Model accuracy: 94.2%
- When model explanations provided, human accuracy improves to 89.1%
- Humans trust model more when explanations show obvious artifacts (hands, faces)
- Humans distrust model when explanations focus on subtle frequency patterns

**Implication:** Explainability significantly increases human-AI collaboration effectiveness

### 5. Robustness Against Adversarial Perturbations

**Challenge:** Generative models may be designed to fool detectors.

**Evaluation:**
- Apply adversarial perturbations to AI-generated images (FGSM, PGD)
- Test if detectors maintain performance
- Analyze if explanations remain consistent under perturbations

**Results:**
- Standard detectors degrade significantly (accuracy drops 60-80%)
- Ensemble approach more robust (accuracy drop 15-25%)
- Frequency-based methods surprisingly robust (drop 10-20%)
- **Lesson:** Multiple detection methods provide defense against targeted attacks

---

## Methodology & Implementation

### Data Collection and Preparation

**Generator Selection:**
- Evaluated 8+ state-of-the-art generative models
- Text prompts: diverse (600+ templates covering objects, scenes, artistic styles)
- Image resolution: 512×512 to 1024×1024 pixels
- Batch generation: 50k+ images per model for statistical reliability

**Data Splits:**
- **Training:** 400k real + 400k AI-generated (balanced)
- **Validation:** 50k real + 50k AI-generated
- **Test (in-distribution):** 50k real + 50k AI-generated (same generators as training)
- **Test (out-of-distribution):** Real images from new sources + images from generators not seen during training

**Preprocessing:**
- Normalization: ImageNet statistics
- Augmentation: Mild augmentations (rotation ±5°, brightness ±10%, JPEG compression Q=85-100)
- No heavy augmentation to preserve detection artifacts

### Detection Architecture Details

#### Ensemble Configuration:

1. **ResNet-50 Backbone**
   - Pre-trained on ImageNet, fine-tuned on detection task
   - Input: Full image (1024×1024)
   - Output: Binary classification + attention maps
   - Training: 50 epochs, AdamW, lr=1e-4

2. **Vision Transformer (ViT-B)**
   - Patch size: 16×16
   - Attention-based, naturally provides interpretability
   - Fine-tuned from DINO pre-training
   - Training: 30 epochs, learning rate scheduling

3. **Frequency Domain Module**
   - Input: FFT coefficients of image patches
   - Architecture: Custom CNN on frequency domain features
   - Novel component: Learns to detect unnatural frequency patterns

4. **Patch-Level Classifier**
   - Process image as non-overlapping 128×128 patches
   - Classify each patch independently
   - Aggregate patch predictions via majority voting
   - Helps localize artifacts to specific regions

5. **Temporal Consistency Module** (for video)
   - Frame-to-frame consistency checks
   - Detects flickering/inconsistencies in AI-generated videos
   - Optional component for multimodal detection

#### Ensemble Aggregation:
```
ensemble_score = 0.3×ResNet + 0.25×ViT + 0.25×Frequency + 0.2×PatchLevel

Final Decision:
- If ensemble_score > 0.5: "AI-generated"
- Otherwise: "Real"
```

### XAI Integration Pipeline

**For each detected AI-generated image:**

1. **Compute explanations** using all 16 XAI methods
2. **Evaluate quality:**
   - Faithfulness: Occlusion test (remove regions, measure prediction change)
   - Sparsity: Count highlighted pixels/regions
   - Consistency: Pairwise agreement between methods
3. **Select reliable explanations** (high faithfulness + consistency)
4. **Generate human-readable report:**
   - Heatmap visualization
   - Text summary (e.g., "Artifacts detected in hand region with high confidence")
   - Confidence scores

**Computational cost:** ~2 seconds per image for full XAI analysis (on GPU)

### Evaluation Metrics

**Primary Metrics:**
- **Accuracy:** Fraction correct on held-out test set
- **Precision/Recall:** For each class (real/AI-generated)
- **AUC-ROC:** Aggregated performance across thresholds
- **Generalization:** Performance on generators unseen during training

**Explainability Metrics:**
- **XAI Quality Scores:** Faithfulness, sparsity, consistency
- **Human-AI Agreement:** Correlation with human detection judgments
- **Computational Cost:** Latency per image

**Robustness Metrics:**
- Accuracy under adversarial perturbations
- Performance on compressed/resized images
- Sensitivity to JPEG artifacts

---

## Practical Applications & Use Cases

### 1. Social Media Content Moderation

**Challenge:** Platforms must identify synthetic content at scale while maintaining user trust.

**Implementation:**
- Deploy ensemble detector at ingestion time
- Flag images with AI-generation confidence > 0.7
- Show users XAI-based explanations for moderation decisions
- Allow appeals with visual evidence

**Impact:**
- Reduces misinformation spread (human evaluation studies show this)
- Improves transparency of moderation
- Enables user education about synthetic media

### 2. News and Journalism

**Use Case:** Verify image authenticity in news articles

**Workflow:**
- Journalists submit images for verification
- System provides detection result + explanation
- Editors review explanation to assess credibility of image
- Images flagged as synthetic are marked in publication or removed

**Practical benefit:** Protects publication credibility, speeds fact-checking

### 3. Legal and Forensic Analysis

**Application:** Establish authenticity in legal proceedings

**Requirements:**
- High precision (avoid false positives that exclude legitimate evidence)
- Explainability for jury understanding
- Timestamp evidence (when image was flagged)

**Advantage of XAI:**
- Provides scientific basis for authentication claims
- Jury can understand detector reasoning
- Enables cross-examination of detection methodology

### 4. Entertainment and Creative Industries

**Use Case:** Detect copyright infringement via synthetic media generation

**Scenario:** Creator suspects their art was used to train generative model

**Detection approach:**
- Analyze AI-generated images suspected to be derived from creator's work
- Explanations may identify specific artifacts matching training data
- Provides legal evidence for DMCA/copyright claims

### 5. Personal Authentication and Dating Apps

**Problem:** Fake profiles using AI-generated photos

**Solution:**
- Automatic flagging of synthetic profile photos
- Options: block profile, require video verification, or warn other users
- XAI explanations help users understand verification results

**Privacy consideration:** Perform detection on-device when possible to avoid storing images

### 6. Insurance and Claims Verification

**Application:** Verify authenticity of damage photos in insurance claims

**Process:**
- Claimant submits damage photographs
- Automatic detection with explanation
- Suspicious claims get manual review
- XAI explanations guide adjuster investigation

**Advantage:** Reduces fraud while maintaining transparent claim processes

---

## Insights & Implications

### 1. XAI is Essential for High-Stakes Detection

**Key Finding:** Accuracy alone is insufficient for deployment in sensitive domains.

**Evidence:**
- Black-box detector with 95% accuracy rejected by stakeholders
- Same detector with explanations (92% accuracy) accepted and deployed
- **Implication:** Explainability may be worth more than marginal accuracy gains

### 2. Human-AI Collaboration Improves Detection

**Observation:** Humans alone are poor at detection (72% accuracy), but with AI explanations, humans reach 89% accuracy—better than AI alone!

**Explanation:** Humans understand visual artifacts (distorted hands, anatomical impossibilities) better than AI. When AI highlights artifacts, human expertise complements AI perception.

**Implication:** Optimal systems pair AI detection with human judgment, especially for high-stakes decisions.

### 3. Robustness Comes from Diversity

**Discovery:** Single-method approaches are vulnerable to adversarial attacks or distribution shift.

**Supporting evidence:**
- ResNet: Fails on new generators (65% generalization)
- Frequency-based: Robust to new generators (82% generalization)
- Ensemble: Best of both (89% generalization)

**Principle:** Diversity in detection methods provides robustness. No single indicator is foolproof.

### 4. Fundamental Limitations

**Inherent Challenge:** As generators improve, detecting all synthetic images may become information-theoretically impossible.

**Argument:** If generator produces images indistinguishable from real images (even to humans), detection requires access to generator's internal state or source metadata.

**Implication:** Long-term solution requires:
- Synthetic media provenance (digital signatures, blockchain)
- Model accountability (registration of generator models)
- Authentication standards (similar to digital certificates)

### 5. Societal and Ethical Implications

**Dual Use Concern:** Detection systems can themselves be targets of adversarial attacks.

**Scenario:** Bad actors develop generators specifically designed to evade detection systems.

**Ethical response:**
- Security through transparency (publishing methods helps community)
- Responsible disclosure (work with platforms before public release)
- Research oversight (ethical review of detection system development)

---

## Code & Resources

### Official Resources
- **ArXiv PDF:** [arxiv.org/pdf/2605.06143](https://arxiv.org/pdf/2605.06143)
- **Dataset (AIText2Image):** Available for research (licensing details in paper)
- **Code Repository:** GitHub link provided in paper

### Pre-trained Models

**Ensemble Detector:**
- Checkpoints for each component (ResNet, ViT, Frequency, Patch-level)
- Fine-tuned models ready for deployment
- Inference code for image detection

**XAI Components:**
- Pre-configured XAI methods
- Gradient computation utilities
- Visualization functions

### Datasets

**AIText2Image:**
- 500k+ AI-generated images (multiple generators)
- 500k+ real images (diverse sources)
- Metadata: Generator model, prompt, image properties
- Non-commercial research license

**Test Sets:**
- Out-of-distribution generators (not seen during training)
- Real images from new sources
- Adversarially perturbed versions

### Dependencies

**Core Libraries:**
- PyTorch 1.13+
- Transformers (HuggingFace)
- Torchvision
- OpenCV (image processing)

**XAI Libraries:**
- Captum (PyTorch explainability)
- LIME
- SHAP
- Custom implementations for specialized methods

**Utilities:**
- Matplotlib (visualization)
- Pandas (data handling)
- NumPy
- SciPy

**Compute Requirements:**
- GPU: NVIDIA A100, H100 preferred
- RAM: 16GB+ for batch processing
- Disk: 500GB+ for full dataset

### Quick-Start Inference

```python
from ai_detection import EnsembleDetector, ExplainabilityPipeline

# Load pre-trained ensemble detector
detector = EnsembleDetector.from_pretrained("ensemble_checkpoint")

# Load XAI pipeline
xai = ExplainabilityPipeline(num_methods=16)

# Detect and explain
image_path = "test_image.jpg"
image = load_image(image_path)

# Get detection result
detection = detector(image)
print(f"AI-generated probability: {detection['score']:.3f}")
print(f"Classification: {detection['label']}")

# Get explanations
explanations = xai.explain(image, detector)

# Visualize results
explanations.visualize()
# Shows heatmaps, text explanations, confidence levels
```

---

## Related Work & Context

### Prior Detection Methods

1. **CNN-based Detectors (2019-2022)**
   - EfficientNet, ResNet trained on synthetic vs. real images
   - Weakness: Overfit to specific generators, poor generalization

2. **Frequency Domain Analysis (2020-2023)**
   - FFT, DCT-based features
   - Strength: More generalizable; Weakness: Sophisticated generators can suppress artifacts

3. **Artifact-Specific Detection**
   - Focus on anatomical anomalies, lighting inconsistencies
   - Limited to specific types of artifacts

### Recent Advances in Generative Models

- **Stable Diffusion 3, DALL-E 4, Midjourney Gen 6:** Photorealistic quality, subtle artifacts
- **ControlNet, Gligen:** Fine-grained control, reducing visible artifacts
- **Diffusion models with frequency normalization:** Specifically designed to evade frequency-based detection

### Explainable AI in Computer Vision

- **Attention mechanisms:** Vision Transformers provide built-in interpretability
- **Concept activation vectors:** Learning human-interpretable features
- **Counterfactual explanations:** "Minimal change to flip decision"
- **Prototype learning:** Storing representative images per class

### Future Research Directions

1. **Adversarial Robustness:**
   - Develop detectors robust to adversarial perturbations
   - Formal verification of detection guarantees
   - Game-theoretic analysis of detection vs. evasion

2. **Video and Multimodal Detection:**
   - Extending to AI-generated videos
   - Audio-visual consistency checks
   - Temporal coherence analysis

3. **Content Provenance:**
   - Digital signatures for synthetic media
   - Blockchain-based registries of generative models
   - Metadata standards for authentication

4. **Human-Centered Explainability:**
   - User studies on explanation effectiveness
   - Personalized explanations for different audiences
   - Interactive explanation interfaces

5. **Detection at Generation Time:**
   - Rather than post-hoc detection, embed authentication into generators
   - Watermarking techniques for synthetic images
   - Cryptographic proofs of authenticity

---

## Key Takeaways

1. **Single detection methods are insufficient**—ensemble approaches provide accuracy and generalization
2. **Explainability is critical for deployment** in high-stakes applications; accuracy alone is inadequate
3. **Human-AI collaboration improves detection** beyond either alone; leverage complementary strengths
4. **Generative models will continue improving**; long-term solution requires authentication infrastructure
5. **Diverse detection strategies (frequency, spatial, deep learning) capture different artifact classes**
6. **Robustness against adversarial attacks requires transparency** and continuous evaluation against new generators
7. **XAI integration demonstrates that interpretability can be built into detection systems** from the ground up, not just bolted on

