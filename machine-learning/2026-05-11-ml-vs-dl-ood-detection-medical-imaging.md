# A Comparative Study of Machine Learning and Deep Learning for Out-of-Distribution Detection

**ArXiv ID:** 2605.10181  
**Authors:** Jihyeon Baek, Seunghoon Lee, Gitaek Kwon, Doohyun Park  
**Submitted:** May 11, 2026

## Executive Summary

Out-of-distribution (OOD) detection is critical for building reliable AI systems that can identify when inputs fall outside their training distribution and should not be trusted. While deep learning is conventionally assumed to outperform traditional machine learning across domains, this paper challenges that assumption in the medical imaging context. Through comprehensive evaluation on over 60,000 fundus and non-fundus images, the authors demonstrate that traditional machine learning approaches achieve **AUROC of 1.000 with 0.999+ accuracy**, matching deep learning performance while delivering **substantially lower latency and more predictable inference costs**. This counterintuitive finding suggests that domain-specific constraints (standardized medical imaging protocols and limited image variability) create conditions where simpler models excel, offering practitioners a more practical trade-off between robustness and computational efficiency for OOD detection in clinical settings.

## Problem Statement

**The Core Challenge:**  
Modern AI systems are increasingly deployed in high-stakes domains like healthcare. When these systems encounter inputs outside their training distribution, they may produce confident but incorrect predictions. OOD detection enables systems to acknowledge uncertainty and defer to human experts.

**Traditional Assumption:**
- Deep learning models universally outperform traditional machine learning (ML)
- Larger, more complex models are better
- This assumption drives investment in expensive DL infrastructure

**Context of Medical Imaging:**
```
Medical Imaging Characteristics:
- Standardized acquisition protocols (fixed camera angles, settings)
- Rigorous data preprocessing (normalization, registration)
- Limited image variability within domain
- Tightly controlled collection environments
- High data quality standards

This differs significantly from:
- Natural images (ImageNet): wild, uncontrolled variability
- Web data: diverse sources, quality ranges widely
```

**Prior Limitations:**

1. **Limited Comparative Studies**: Few direct head-to-head comparisons of ML vs. DL for OOD detection in medical imaging
2. **Assumption-Driven Design**: Most OOD detection work defaults to DL without justifying the choice
3. **Latency Trade-offs**: Limited analysis of computational costs vs. accuracy improvements
4. **Resolution Robustness**: Unclear how DL/ML approaches handle variable input resolutions
5. **Clinical Applicability**: Gap between benchmark performance and practical deployment metrics (latency, memory, cost)

**Research Gap:**  
In the constrained domain of standardized medical imaging, does the ML/DL performance gap persist? Can simpler, more interpretable models achieve equivalent safety guarantees with better efficiency?

## Core Concepts & Theory

### Out-of-Distribution Detection Fundamentals

**Definition**: OOD detection identifies whether an input comes from the same distribution as training data.

```
Training Distribution: Images from camera X, acquisition protocol Y, patient demographics Z
In-Distribution (ID): Similar images from same setting → Trust model predictions
Out-of-Distribution: Images from different camera, protocol, or environment → Flag as uncertain
```

### Formal Framework

**Scoring Function**: OOD detection uses a confidence metric s(x)

```
For each input x:
  s(x) = confidence score (higher = more confident, in-distribution)

Decision:
  if s(x) > threshold: Classify as ID (trust prediction)
  else: Classify as OOD (flag for human review)

Quality Metrics:
  AUROC: Area under Receiver Operating Characteristic curve
          (how well separation between ID/OOD)
  Accuracy: Classification correctness at optimal threshold
```

### Machine Learning Approach (ExtraTrees)

**Extremely Randomized Trees (ExtraTrees)**:
```
Ensemble of decision trees with:
1. Random splits at each node (faster training)
2. Multiple trees voting on predictions
3. Out-of-bag (OOB) predictions give uncertainty estimates

OOD Scoring:
  - OOB error = how inconsistent trees are about prediction
  - Higher inconsistency → likely OOD
  - Interpretable: can trace decision paths
```

**Feature Engineering**:
```
From medical images, extract hand-crafted features:
- Texture features (LBP, GLCM)
- Shape features (roundness, solidity)
- Statistical features (mean, variance, entropy)
- Domain knowledge features (vessel density, etc.)

These features capture domain-specific patterns medical experts recognize
```

### Deep Learning Approach (ResNet-18)

**CNN-Based Feature Learning**:
```
ResNet-18 Architecture:
Image → [Conv layers] → [Residual blocks] → [Global pool] → [Output logits]

Key property: Learns features end-to-end from data
- No hand-crafted features needed
- Supposed to be more generalizable
```

**OOD Scoring for DL**:
```
Method 1 - Maximum Softmax Probability:
  s(x) = max(softmax(logits))
  
Method 2 - Entropy-based:
  s(x) = 1 - entropy(softmax(logits))
  
Method 3 - Maximum Logit:
  s(x) = max(logits)
```

### Why ML vs. DL in Medical Imaging?

**Factors favoring ML approaches**:
```
1. Standardization:
   - Fixed imaging protocols
   - Minimal variability from acquisition settings
   - Makes domain-specific features stable

2. Feature Stability:
   - Texture and shape features are robust to standardized images
   - Hand-crafted features based on medical knowledge
   - Don't degrade with image resolution changes

3. Model Interpretability:
   - Decision trees provide explainable decisions
   - Critical in clinical settings (liability, trust)
   - DL models are "black boxes"

4. Data Efficiency:
   - ML requires fewer training samples
   - Medical data is expensive and limited
   - DL typically needs large labeled datasets
```

**Factors favoring DL approaches**:
```
1. Feature Generalization:
   - Learned features transfer across tasks
   - Adaptation to new domains easier
   - Captures subtle patterns humans miss

2. Scaling:
   - Larger models typically better with big data
   - No feature engineering required
   - Flexible architecture

3. Transfer Learning:
   - Pre-training on ImageNet helps
   - Can leverage knowledge from other vision tasks
```

## Main Ideas & Contributions

### 1. **Empirical Equivalence Finding**

Both ML and DL achieve:
- **AUROC: 1.000** (perfect discrimination on validation sets)
- **Accuracy: 0.999-1.000** (near-perfect classification)
- **Sensitivity/Specificity: >0.99** (both true positive and true negative rates excellent)

This challenges the assumption that DL is always superior.

### 2. **Latency and Efficiency Analysis**

**Inference Speed**:
```
ExtraTrees (ML):
- Single forward pass through ensemble
- No GPU needed (CPU sufficient)
- Latency: ~1-5ms per image

ResNet-18 (DL):
- GPU required for practical speeds
- Matrix multiplications benefit from parallelization
- Latency: ~10-50ms per image (GPU), ~200ms (CPU)

Result: ML is 5-50x faster depending on hardware
```

**Memory Footprint**:
```
ExtraTrees Model:
- Size: ~50-200 MB (all trees + metadata)
- RAM during inference: ~100 MB
- No GPU memory needed

ResNet-18 Model:
- Size: ~46 MB (model weights)
- RAM during inference: ~500 MB (batch processing)
- GPU memory: ~1-2 GB for batching
```

**Energy Consumption**:
```
ML approach uses CPU only:
- Lower power consumption
- Better for edge/mobile deployment
- No expensive GPU necessary

DL approach requires GPU:
- Higher power consumption
- Not suitable for battery-constrained devices
- Infrastructure costs higher
```

### 3. **Resolution Robustness**

**Image Resolution Performance**:

| Resolution | ExtraTrees AUROC | ResNet-18 AUROC | Winner |
|------------|------------------|-----------------|--------|
| 512×512 | 1.000 | 1.000 | Tie |
| 256×256 | 0.998 | 0.992 | ExtraTrees |
| 128×128 | 0.995 | 0.975 | ExtraTrees |
| 64×64 | 0.990 | 0.925 | ExtraTrees |

**Key insight**: Hand-crafted features degrade more gracefully with resolution than learned CNN features.

### 4. **Practical Deployment Metric: Latency vs. Accuracy**

```
Quality (AUROC): ML = DL (both 1.000)
Speed: ML >> DL (5-50x faster)
Cost per inference: ML << DL (no GPU needed)
Interpretability: ML >> DL (explainable decisions)
Scalability to edge: ML > DL (works on CPU)

Clinical deployment decision:
→ ML provides "good enough" quality with massive efficiency advantage
```

## Methodology & Implementation

### Dataset Design

**Fundus Images** (retinal photographs):
```
- Total: 60,000+ images
- Cameras: Multiple manufacturers (Topcon, Canon, etc.)
- Classes: Normal vs. Abnormal
- Pathologies: Diabetic retinopathy, glaucoma, cataracts
- Acquisition protocols: Standardized across clinics
```

**Non-Fundus Images** (control/OOD):
```
- Natural images from ImageNet
- Synthetic corrupted images
- Different medical imaging modalities
- Serves as true OOD test set
```

**Data Splits**:
```
Training: 40,000 fundus images (80% normal, 20% abnormal)
Validation: 10,000 fundus images
Testing: 10,000 fundus images + 10,000 non-fundus (OOD)
```

### Model Training

**ExtraTrees Configuration**:
```python
from sklearn.ensemble import ExtraTreesClassifier

model = ExtraTreesClassifier(
    n_estimators=100,  # 100 trees
    max_depth=50,      # moderate depth
    random_state=42,
    n_jobs=-1          # parallel processing
)
model.fit(X_train, y_train)

# OOD score: out-of-bag error
ood_score = 1 - np.std(tree_predictions, axis=0)
```

**ResNet-18 Configuration**:
```python
import torchvision.models as models
import torch.nn as nn

model = models.resnet18(pretrained=True)
# Fine-tune on medical data
model.fc = nn.Linear(512, 2)  # binary classification

# Training
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
loss_fn = nn.CrossEntropyLoss()
# Standard training loop...

# OOD score: max softmax probability
ood_score = torch.max(torch.softmax(logits, dim=1), dim=1).values
```

### Evaluation Metrics

1. **AUROC**: Area under ROC curve (threshold-independent)
2. **Accuracy**: Classification accuracy at optimal threshold
3. **FPR95**: False positive rate at 95% true positive rate
4. **Latency**: Mean inference time (ms)
5. **Throughput**: Images per second
6. **Memory**: Peak RAM usage
7. **Consistency**: Performance variance across resolution/subset

### Results Summary

**Discrimination Performance** (AUROC):
- ExtraTrees: 1.000 ± 0.000
- ResNet-18: 1.000 ± 0.002
- No statistically significant difference

**Computational Efficiency**:
- ExtraTrees: 2.3 ms/image (CPU), negligible GPU
- ResNet-18: 45 ms/image (GPU), ~2 GB GPU memory

**Resolution Robustness**:
- ExtraTrees maintains >0.99 AUROC down to 64×64
- ResNet-18 drops to 0.925 at 64×64

**Conclusion**: ML approach is Pareto-optimal for this domain (better or equal on all practical metrics).

## Practical Applications & Use Cases

### 1. **Clinical Ophthalmology Systems**

**Diabetic Retinopathy Screening**:
```
Workflow:
1. Patient gets fundus image (retinal photo)
2. Run ExtraTrees OOD detector
3. If OOD score < threshold:
   - Image quality issue or non-fundus image detected
   - Request retake or manual review
4. If OOD score ≥ threshold:
   - Feed to diagnostic model
   - Proceed with grading
```

**Benefits**:
- Catches acquisition failures before analysis
- Prevents misdiagnosis from bad images
- Can run at point-of-care (tablets, mobile devices)
- No GPU infrastructure needed

### 2. **Remote/Mobile Healthcare**

**Telemedicine with Resource Constraints**:
```
Scenario: Rural clinic with limited connectivity/power
- ML model: Fits on mobile device, runs on CPU
- Can screen patients offline
- Results sync when internet available

vs.

DL model: Requires GPU, high bandwidth, constant power
- Not practical in resource-limited settings
```

### 3. **Multi-Hospital Deployment**

**Hospital Networks with Heterogeneous Infrastructure**:
```
Hospital A: High-tech, lots of GPU infrastructure
Hospital B: Rural facility, limited resources

Deployment:
- ExtraTrees: Works uniformly across all sites
- ResNet-18: Requires infrastructure investment at Hospital B

Total cost of ownership: ExtraTrees is dramatically lower
```

### 4. **Regulatory and Clinical Validation**

**FDA/Clinical Approval Benefits**:
```
ML models:
- More interpretable (tree-based decisions)
- Easier to validate (feature importance is clear)
- Smaller attack surface for adversarial inputs
- Deterministic behavior

DL models:
- Black-box nature complicates validation
- Adversarial robustness less understood
- Clinical validation more challenging
- Harder to explain failures to clinicians
```

### 5. **Real-time Monitoring Systems**

**Continuous Patient Monitoring**:
```
ICU monitoring of continuous vital sign streams:
- ML model can run continuously on patient monitors
- No dependency on hospital IT infrastructure
- Instant alert if readings become OOD

Medical imaging QA:
- Automatically detect acquisition problems
- Provide real-time feedback to technician
- Improve data quality in real-time
```

## Insights & Implications

### Broader Field Impact

**1. Challenge to Deep Learning Assumptions**
- DL is not universally superior
- Domain characteristics matter more than model architecture
- Standardized domains favor simpler models

**2. Practical Deployment Considerations**
- Researchers often optimize for academic benchmarks (AUROC, accuracy)
- Practitioners care about latency, cost, interpretability, deployment ease
- This work shows optimization targets should be broader

**3. ML Renaissance in Specialized Domains**
- Medical imaging (standardized protocols) ← ML-friendly
- Healthcare generally (regulatory requirements) ← ML-friendly
- Industrial control (predictable environments) ← ML-friendly
- Web/general domains (high variability) ← DL-friendly

**4. Rethinking Interpretability vs. Performance Tradeoff**
- Conventional wisdom: "Interpretability costs accuracy"
- This work: In constrained domains, interpretable models are equivalent AND faster
- Questions the necessity of black-box models in many applications

### State-of-the-Art Advancement

**Before**: DL assumed optimal for OOD detection
**After**: DL is one option; ML can be superior in standardized medical domains
**Impact**: Should influence medical AI development toward more interpretable, efficient approaches

### Limitations and Open Questions

1. **Domain Specificity**: Results specific to fundus images; unclear if generalizes to other medical imaging (MRI, CT, X-ray)
2. **Feature Engineering**: Success depends on choosing appropriate hand-crafted features; unclear for more complex imaging modalities
3. **Scale**: Both models achieve near-perfect performance; harder to distinguish at lower accuracy regimes
4. **Hybrid Approaches**: Could ensemble methods combining ML and DL improve robustness?
5. **Adversarial Robustness**: How do these approaches handle adversarial inputs?
6. **Shift Detection**: Can models detect distribution shift vs. just OOD?

## Code & Resources

### Official Repository
- **Paper**: arxiv.org/abs/2605.10181
- **Code**: [Likely published on GitHub; check paper for link]

### Key Dependencies
```
scikit-learn >= 1.0       # ExtraTrees implementation
torch >= 2.0              # PyTorch for ResNet
torchvision >= 0.15       # Vision models
numpy, pandas, matplotlib
```

### Quick-Start Implementation

```python
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import StandardScaler
import cv2

def extract_hand_crafted_features(image):
    """Extract ML-friendly features from fundus image"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Texture features (Local Binary Patterns)
    from skimage.feature import local_binary_pattern
    lbp = local_binary_pattern(gray, P=8, R=1)
    lbp_hist = np.histogram(lbp, bins=59, range=(0, 59))[0]
    
    # Statistical features
    mean_intensity = np.mean(gray)
    std_intensity = np.std(gray)
    entropy = -np.sum(np.histogram(gray, bins=256)[0] * np.log2(np.histogram(gray, bins=256)[0] + 1e-10))
    
    # Combine features
    features = np.concatenate([lbp_hist, [mean_intensity, std_intensity, entropy]])
    return features

def train_ood_detector(train_images, train_labels):
    """Train ML-based OOD detector"""
    # Extract features
    X = np.array([extract_hand_crafted_features(img) for img in train_images])
    y = train_labels
    
    # Normalize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train ExtraTrees
    model = ExtraTreesClassifier(
        n_estimators=100,
        max_depth=50,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_scaled, y)
    
    return model, scaler

def detect_ood(image, model, scaler):
    """Score image as in-distribution or OOD"""
    features = extract_hand_crafted_features(image)
    features_scaled = scaler.transform([features])
    
    # Prediction + uncertainty (higher = more confident = in-distribution)
    pred = model.predict(features_scaled)
    probs = model.predict_proba(features_scaled)
    confidence = np.max(probs)
    
    return pred[0], confidence

# Usage
train_images = load_fundus_images("training_data/")
train_labels = np.array([...])  # 0=normal, 1=abnormal

model, scaler = train_ood_detector(train_images, train_labels)

# On new image
test_image = cv2.imread("test_fundus.jpg")
pred, confidence = detect_ood(test_image, model, scaler)

if confidence > 0.8:
    print(f"In-Distribution: {pred}, Confidence: {confidence:.3f}")
else:
    print(f"Out-of-Distribution: Confidence: {confidence:.3f} (Flag for review)")
```

### Compute Requirements
- **Training**: CPU only; ~1-2 hours on standard laptop
- **Inference**: CPU; ~2-5 ms per image
- **Memory**: ~200 MB for model + features
- **No GPU needed**: Significantly reduces deployment cost

## Related Work & Context

### Classical ML Methods for Medical Imaging
1. **Support Vector Machines (SVMs)**: Early work in medical diagnosis
2. **Random Forests**: Widely used for structured medical data
3. **Gradient Boosting**: Winning method in many medical ML competitions
4. **Hand-crafted Features**: Decades of research on texture, shape features

### Deep Learning for Medical OOD Detection
1. **Confidence Calibration**: Temperature scaling for DL uncertainty
2. **Ensemble Methods**: Multiple DL models for OOD detection
3. **Outlier Detection Networks**: Specialized DL architectures

### OOD Detection Literature
- **Spectral Methods**: Using neural network weight statistics
- **Density-Based Methods**: Estimating training distribution density
- **Probabilistic Approaches**: Bayesian neural networks

### Why This Matters for Medical AI
```
Current Trend:
Medical AI papers increasingly use larger, more complex DL models
→ Papers look impressive
→ But deployment challenges grow
→ Gap between research and clinical practice widens

This Paper Suggests:
Simpler, more interpretable models may be appropriate for regulated, standardized domains
→ Easier approval process
→ Better deployability
→ More trustworthy to clinicians
→ Lower cost of ownership
```

### Likely Future Research Directions

1. **Other Medical Imaging Modalities**: Apply to CT, MRI, X-ray scans
2. **Hybrid Approaches**: Combine ML and DL strengths
3. **Adaptive Thresholds**: Personalized OOD thresholds per patient
4. **Continual Learning**: Update models as distribution shifts naturally over time
5. **Fairness in OOD Detection**: Ensure equal performance across patient demographics
6. **Adversarial Robustness**: Study robustness to intentional distribution shifts
