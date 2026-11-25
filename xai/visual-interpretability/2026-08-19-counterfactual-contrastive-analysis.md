# Counterfactual Contrastive Analysis: Visual Explanations through Disentangled Generative Models

**ArXiv ID:** [2608.19032](https://arxiv.org/abs/2608.19032)

**Authors:** Yunlong He and Pietro Gori (Télécom Paris)

**Submission Date:** August 19, 2026 (revised September 3, 2026)

**Venue:** MICCAI 2026

---

## Executive Summary

This paper addresses a critical challenge in visual explainability: generating **counterfactual explanations (CEs)** that are both realistic and minimally edited. Rather than relying on decision boundaries or classifier gradients, the authors propose **Counterfactual Contrastive Analysis (CCA)**, a classifier-free approach built on **Contrastive Analysis** and **StyleGAN2**. By learning to separate class-shared factors from class-specific factors in image generative models, CCA produces visual counterfactuals that maintain semantic coherence while faithfully explaining why a model changed its prediction. The method achieves superior disentanglement and generation quality compared to prior work, with practical efficiency gains (0.25 seconds per image) on medical imaging datasets.

---

## Problem Statement

### The Challenge of Visual Explanations

Deep learning models excel at image classification but lack interpretability. When a model's prediction changes on a test image, stakeholders in high-stakes domains (medicine, law enforcement, autonomous vehicles) need to understand **why** the decision changed. Visual counterfactual explanations (VCEs) provide one answer: they show minimal edits to the input image that would flip the model's classification, thereby revealing what visual features the model considers decisive.

### Limitations of Existing Approaches

1. **Classifier-dependent methods:** Many VCE approaches rely on decision boundaries or classifier gradients, which can inadvertently bias explanations toward classifier artifacts rather than true causal factors.
2. **Implausibility and unrealism:** Generated counterfactuals may contain visual artifacts, anatomically impossible edits (in medical imaging), or unnatural pixel manipulations.
3. **Lack of disentanglement:** Existing methods struggle to separate class-agnostic visual factors (lighting, pose, background) from class-specific features (the presence or absence of a tumor, disease marker, or object).
4. **Scalability and speed:** Earlier methods are computationally expensive, limiting real-time deployment.
5. **Limited multi-directional coverage:** Most work focuses on explaining a single class transition; bidirectional explanations (healthy↔diseased) are rarely explored systematically.

### Why Contrastive Analysis?

The authors leverage **Contrastive Analysis (CA)**, a classical multivariate technique from statistics that:
- Operates on data distributions, not individual classifiers
- Separates **shared factors** (C) across both classes from **salient (class-specific) factors** (S)
- Avoids direct dependence on the classifier, reducing explanations' vulnerability to classifier biases

---

## Core Concepts & Theory

### Contrastive Analysis (CA)

Contrastive Analysis is a statistical method for comparing two datasets:

**Inputs:**
- Two datasets: X₁ (class 0) and X₂ (class 1)
- Each viewed as a multivariate Gaussian (classical CA) or in latent space (modern generative variant)

**Goal:**
- Decompose the variance into:
  - **Shared component (C):** directions where both classes are variable
  - **Salient component (S₁ or S₂):** directions where only one class varies

**Mechanism:**
- Compute covariance matrices Σ₁ and Σ₂ for each class
- Identify eigenvectors of the difference (Σ₁ - Σ₂)
- Positive eigenvalues → class 1 salient; negative eigenvalues → class 2 salient
- Remaining directions → shared

**Mathematical Formulation:**

```
Σ₁ = Cov(X₁)
Σ₂ = Cov(X₂)
Δ = Σ₁ - Σ₂
(v_i, λ_i) = eig(Δ)

If λ_i > 0: v_i is class 1 salient
If λ_i < 0: v_i is class 2 salient
Otherwise: v_i is shared
```

### Classical vs. Generative CA

**Classical CA:** Applied directly to data distributions; requires Gaussian assumptions.

**Generative CA:** Applies CA in the latent space of a generative model (StyleGAN2):
- Sample latent vectors z from both classes
- Project into generative model's latent space
- Apply CA to separate disentangled factors
- Reconstruct images by synthesizing along salient directions

**Key Innovation:** CA naturally separates class-specific appearance factors from background, pose, and lighting—exactly the factors needed for plausible counterfactuals.

### StyleGAN2 Latent Space Structure

StyleGAN2's latent space has a hierarchical organization:
- **W-space (style space):** High-level semantic features; better disentanglement than z-space
- **F-space (feature space):** Intermediate feature maps before image synthesis
- **Coarse levels (early layers):** Control layout, pose, global structure
- **Medium levels:** Control textures and shape details
- **Fine levels (late layers):** Control color and fine details

**CCA Enhancement:** The paper introduces editing in **both W-space and F-space** to preserve fine details (e.g., anatomy) better than W-space editing alone.

---

## Main Ideas & Key Contributions

### 1. Classifier-Free Visual Counterfactual Generation

**Contribution:** Moving away from classifier-gradient-driven explanations, CCA generates counterfactuals purely from the generative model's learned factors. This decouples explanations from classifier idiosyncrasies.

**Benefit:** Explanations reflect the class-conditional distributions directly, not classifier decision boundaries, yielding more faithful and interpretable counterfactuals.

### 2. Enhanced Contrastive Analysis with Flexible Salient Factors

**Classical CA assumption:** Exactly one class has salient variation in each direction.

**CCA innovation:** Allows **both classes to have salient factors**, enabling representation of multiple appearance modes within a class (e.g., small and large tumors, different skin lesion types).

**Implementation:** Relaxes the strict orthogonality constraint; weights salient factors by their eigenvalue magnitude to rank importance.

### 3. F-Space Refinement for Anatomically-Aware Editing

**Problem:** W-space editing alone can produce unrealistic medical images (e.g., impossible tumor locations or missing anatomy).

**Solution:** After editing in W-space, refine the intermediate feature map (F-space):
- Extract W-space latent codes for healthy and diseased images
- Interpolate or swap W-space factors
- Refine at the F-layer to preserve anatomical coherence
- Decode to RGB

**Result:** More plausible and anatomically sound counterfactuals compared to W-space-only methods.

### 4. Empirical Disentanglement Measurement

**Metric: Separation Gap (Δ)**

Measures how well salient factors (S) are separated from shared factors (C):

```
Δ = ||Σ_C^(S)|| / ||Σ_S||

where:
- Σ_S = variance of salient factors
- Σ_C^(S) = covariance between C and S
- Lower Δ → better disentanglement
```

**CCA achieves the lowest Δ compared to baselines,** indicating superior separation of class-specific from class-shared factors.

### 5. Efficient Generation via Pre-trained StyleGAN2

**Computational Advantage:** Leveraging pre-trained StyleGAN2 avoids expensive end-to-end training.

**Speed:** 0.25 seconds per image on medical datasets—suitable for clinical workflows.

**Trade-off:** Depends on StyleGAN2 quality; works best when StyleGAN2 can generate realistic images in the target domain.

---

## Methodology & Implementation

### Architecture Overview

```
Input: Two datasets D₀ (class 0) and D₁ (class 1)

Step 1: Pre-training (Off-the-shelf)
├─ Train or load StyleGAN2 on combined dataset
└─ Extract W-space latent distributions p(w|class)

Step 2: Contrastive Analysis in W-Space
├─ Sample latent vectors w₀ ~ p(w|class 0), w₁ ~ p(w|class 1)
├─ Compute Σ₀ = Cov(w₀), Σ₁ = Cov(w₁)
├─ Eigendecompose Δ = Σ₁ - Σ₀
├─ Assign eigenvectors to [C | S₁ | S₂]
└─ Project: w = w_C + w_S

Step 3: Counterfactual Generation via Factor Swapping
├─ For image x from class 0:
│  ├─ Encode to w-space (or invert through StyleGAN2)
│  ├─ Replace w_S^(0) with w_S^(1) (swap to class 1 factors)
│  └─ Decode to image
└─ Optionally: Refine in F-space

Step 4: F-Space Refinement (Optional)
├─ Extract intermediate features f from refined W-space trajectory
├─ Fine-tune features to maintain spatial coherence
└─ Re-decode to final image

Output: Counterfactual image x'
```

### Datasets

The paper evaluates CCA on three medical imaging datasets from [MedMNIST](https://medmnist.com/):

1. **BloodMNIST:**
   - Blood cell classification (8 classes, reduced to binary healthy/abnormal)
   - 28×28 grayscale images
   - ~11,200 training samples

2. **OCTMNIST:**
   - Optical coherence tomography (OCT) scans of the retina
   - Binary: normal vs. drusen (age-related macular degeneration marker)
   - 28×28 grayscale

3. **BraTS2023 (Binary Subset):**
   - Brain MRI slices
   - Binary: healthy tissue vs. tumor
   - 128×128 grayscale
   - Multi-directional experiments: healthy→tumor and tumor→healthy

### Evaluation Metrics

**Synthesis Quality (Standard):**
- **L2 Distance:** Pixel-level difference (lower is better for counterfactuals close to originals)
- **LPIPS (Learned Perceptual Image Patch Similarity):** Perceptual distance; better aligns with human judgment
- **MS-SSIM (Multi-Scale Structural Similarity Index):** Preserves structural integrity
- **FID (Fréchet Inception Distance):** Measures distribution match; validates domain realism

**Disentanglement Quality:**
- **Separation Gap (Δ):** Measures class-factor separation (CCA-specific)
- **Bidirectional KL Divergence (BKL):** How well swapped samples match the target class distribution

**Counterfactual-Specific:**
- **Flip Ratio (FR):** Percentage of generated counterfactuals that change classifier prediction (faithfulness)
- **Mean Absolute Difference (MAD):** Average pixel change magnitude (minimality)
- **Trajectory Analysis:** Smooth class probability changes along interpolation path, indicating coherent explanations

### Results

**Disentanglement (Separation Gap):**
- CCA: **0.04–0.08** (depending on dataset)
- Baselines (CA, PCA variants): 0.12–0.20
- **Implication:** CCA achieves 2–3× better disentanglement

**Generation Quality:**
- BloodMNIST LPIPS: CCA ~0.15 (baseline ~0.25)
- BraTS FID: CCA ~25 (baseline ~40–50)
- **Speed:** 0.25 s/image (practical for clinical use)

**Faithfulness:**
- Flip Ratio on BraTS: **92–98%** of generated counterfactuals successfully flip classifier predictions
- Trajectory probability curves: smooth and monotonic (class 0→1 as interpolation progresses)

**Comparison:**
- Superior to prior VCE work (e.g., VAE-CE, Contrastive Explanations)
- Competitive with or better than recent diffusion-based methods
- More efficient than adversarial search–based approaches

---

## Practical Applications & Real-World Use Cases

### Medical Imaging

**Radiologist Decision Support:**
- Radiologists face high-stakes classification decisions (cancer screening, disease staging)
- CCA generates realistic "what-if" images showing boundary conditions
- **Example:** A radiologist classifies a chest X-ray as normal. CCA shows a minimal edit (artifact or early infiltrate) that would trigger a "concerning" label, helping the radiologist understand the model's decision boundary

**Tumor Detection and Segmentation:**
- In BraTS, CCA generates healthy→tumor counterfactuals revealing where tumors are anatomically plausible
- Clinicians validate that generated tumors match realistic disease presentations
- Improves trust in AI-assisted diagnosis

**Regulatory and Audit Compliance:**
- FDA and EU AI Act increasingly require explainability for high-risk medical AI
- Visual counterfactuals provide tangible, auditable evidence of model reasoning
- CCA's disentanglement ensures explanations reflect true class factors, not spurious correlations

### Autonomous Systems

**Vehicle Perception:**
- Autonomous vehicle cameras classify pedestrians, obstacles, road signs
- CCA could show minimal image perturbations that would change classification
- Reveals robustness gaps: "what small change in lighting/occlusion breaks detection?"

**Failure Mode Analysis:**
- Generate counterfactuals for misclassified images to understand what visual cues the model is missing
- Improves safety validation before deployment

### Legal and Hiring Systems

**Bias Detection in Facial Recognition:**
- CCA could reveal minimal demographic changes (age, skin tone) that flip classification
- Quantifies disparities: different demographic groups might have different counterfactual distances
- Supports fairness audits under EU AI Act and GDPR

---

## Insights & Implications

### 1. Classifier-Free Explanations Scale Better

The paper's core insight is that moving explanations *outside* the classifier (into the generative model) reduces brittleness and improves interpretability. This suggests future XAI work should:
- Decouple explanation generation from model outputs
- Use class-conditional generative models as a stable reference
- Reduce adversarial vulnerability in explanations themselves

### 2. Disentanglement and Plausibility Are Linked

Superior disentanglement (low separation gap) correlates with:
- More realistic counterfactuals (fewer artifacts)
- Better trajectory smoothness (interpretable interpolation paths)
- Higher flip ratios (faithful explanations)

**Implication:** Focusing on disentanglement metrics early in model development improves downstream explainability.

### 3. F-Space Refinement Matters for Domain-Specific Explanations

For domains with strong structural priors (medical imaging, anatomical coherence), editing only W-space is insufficient. F-space refinement preserves domain semantics and dramatically improves plausibility.

**Broader lesson:** One-size-fits-all explanation methods may fail in specialized domains; domain-aware editing layers improve trust.

### 4. Counterfactual Trajectories as Validation

The smooth, monotonic class probability changes along generated trajectories serve as a **built-in validity check**:
- Jagged probability curves suggest implausible intermediate images
- Smooth curves indicate the explanation is coherent and interpretable

This metric could be generalized beyond medical imaging.

### 5. Open Questions and Limitations

1. **Scalability to larger models:** BraTS experiments use 128×128 images. How does CCA perform on 512×512 or 1024×1024 medical scans or natural images?

2. **Multi-class scenarios:** Experiments focus on binary classification. Extending CA to K > 2 classes requires choosing which pairs to compare.

3. **Data distribution drift:** CCA's separation relies on estimating covariances from finite samples. How sensitive is it to data drift or limited training data in rare diseases?

4. **Mechanistic understanding:** Does disentanglement in StyleGAN2 correspond to clinically meaningful visual concepts, or are factors still entangled along dimensions not captured by the generative model?

5. **User studies:** While quantitative metrics improve, human validation of counterfactual plausibility and usefulness remains limited. What explanations actually change clinician behavior?

---

## Code & Resources

### Official Resources
- **GitHub:** Code availability pending (check https://github.com/biomedia-mira/ for related work)
- **Paper:** [ArXiv:2608.19032](https://arxiv.org/abs/2608.19032)
- **MICCAI 2026 Version:** Published in MICCAI proceedings (accessible through conference site)

### Dependencies & Requirements

**Core Libraries:**
- Python 3.9+
- PyTorch 1.12+
- StyleGAN2-Ada-PyTorch (or similar StyleGAN2 implementation)
- NumPy, SciPy (for Contrastive Analysis eigendecomposition)
- Scikit-learn (optional, for metrics)

**Data:**
- MedMNIST datasets (freely available via torchvision or direct download)
- Pre-trained StyleGAN2 models on target domains (or train custom models)

**Computational Requirements:**
- GPU recommended (NVIDIA A100 or similar for fast inference)
- 0.25 seconds per image on modern GPUs
- Memory: ~4GB for StyleGAN2 weights + batch processing

### Quick Start

```python
import torch
from stylegan2 import StyleGAN2
import numpy as np
from scipy.linalg import eigh

# 1. Load pre-trained StyleGAN2
model = StyleGAN2.load_pretrained('medical')

# 2. Sample latent codes from two classes
w0 = model.sample_w(num=100, label=0)  # Class 0 (healthy)
w1 = model.sample_w(num=100, label=1)  # Class 1 (diseased)

# 3. Contrastive Analysis
cov0 = np.cov(w0.T)
cov1 = np.cov(w1.T)
delta = cov1 - cov0
evals, evecs = eigh(delta)

# 4. Identify salient and shared factors
shared_idx = evals near zero
salient_idx = abs(evals) > threshold

# 5. Generate counterfactual by swapping salient factors
w_cf = w0.clone()
w_cf[:, salient_idx] = w1[: , salient_idx]
img_cf = model.synthesis(w_cf)
```

### Interactive Demos
- Medical imaging counterfactuals can be visualized on platforms like Gradio or Streamlit
- Real-time generation suitable for clinician testing

---

## Related Work & Context

### Counterfactual Explanations (Broader Field)

**Classical counterfactual work:**
- **Wachter et al. (2017):** Algorithmic counterfactual explanations via optimization in input space; defines the concept for ML
- **Review: Verma et al. (2020):** Comprehensive survey of counterfactual explanations

**Visual counterfactual approaches:**
- **VAE-CE (2021):** Uses VAE latent space; less disentangled than StyleGAN2
- **Contrastive Explanations (Dhurandhar et al., 2019):** Early work on contrastive visual explanations
- **Recent work (2024–2025):** Diffusion-based visual counterfactuals (more flexible but slower)

### Disentangled Representation Learning

**Key references:**
- **β-VAE (Higgins et al., 2017):** Foundational work on disentanglement via variational objectives
- **Factor-VAE, β-TCVAE:** Improved disentanglement metrics
- **StyleGAN2 latent analysis (Srinivasan et al., 2019):** Seminal work showing W-space semantic disentanglement

**CCA's relationship:** Unlike supervised disentanglement methods (β-VAE), CCA is unsupervised yet leverages class labels directly, offering a middle ground.

### Contrastive Analysis & Generative Models

**Contrastive Analysis roots:**
- Classical statistical technique (Flury & Riedwyl, 1988) for comparing two populations
- Recent revival in deep generative modeling for semi-supervised and unsupervised learning

**Related generative approaches:**
- **Conditional GANs (cGANs):** Direct class conditioning; less disentanglement
- **Diffusion models for counterfactuals:** Emerging area; slower but highly flexible
- **Energy-based models:** Alternative framework for classifier-free generation

### Connection to Mechanistic Interpretability

**Broader implications:**
- CCA's decomposition into shared vs. salient factors resonates with mechanistic interpretability research (e.g., monosemanticity in sparse autoencoders)
- Suggests that disentangled representations naturally emerge when comparing class-conditional distributions
- Could inspire new interpretability metrics based on factor separability

---

## Recent Related Work (2025–2026)

1. **[2609.37638] Targeted Visual Counterfactual Explanations for Contrastive Vision-Language Model** (Sept 2026): Mask-guided counterfactuals for CLIP; complements CCA for foundation models

2. **[2601.21851] Visual Disentangled Diffusion Autoencoders** (Dec 2025): Diffusion-based disentanglement; compares generation quality with StyleGAN2 approaches

3. **[2610.00895] Towards Fast and Disentangled Counterfactuals for Visual Foundation Models** (Oct 2025): Addresses scalability to large models; CCA could be adapted

4. **[2605.12701] Do Fair Models Reason Fairly?** (May 2026): Counterfactual consistency in fairness; relevant for auditing CCA explanations' fairness properties

---

## Limitations & Failure Modes

### 1. StyleGAN2 Quality Ceiling

If the generative model cannot synthesize high-quality images in the target domain, counterfactual quality suffers.
- **Mitigation:** Domain-specific StyleGAN2 pre-training or fine-tuning
- **Limitation:** No guarantee that pre-trained models exist for all domains

### 2. Covariance Estimation in High Dimensions

W-space is typically 512-dimensional. Estimating full covariance from finite samples can be noisy.
- **Observed:** Separation gap increases with smaller datasets
- **Mitigation:** Regularization, dimensionality reduction, or Bayesian covariance estimation

### 3. Binary Classification Focus

Most experiments target binary tasks (healthy/diseased, class A/B).
- **Multi-class extension:** Requires choosing pairwise comparisons; not all pairs are equally informative
- **Workaround:** One-vs-rest CA for each class

### 4. Interpretability of Learned Factors

Even after disentanglement, individual salient factors may not have semantic meaning to humans.
- **Challenge:** "What visual feature does this eigenvector represent?"
- **Future work:** Add concept-based layers (TCAV, etc.) on top of CCA

### 5. Validation in Practice

Clinical validation remains limited. The paper reports quantitative metrics (flip ratio, FID) but lacks large-scale clinician feedback studies.

---

## Implications for Trustworthy AI

### Regulatory Compliance

- **EU AI Act (Article 13):** Requires explainability for high-risk AI systems; visual counterfactuals provide auditable, tangible explanations
- **FDA Guidance (Proposed):** Recommends disentangled, classifier-agnostic explanations; CCA aligns with these principles
- **GDPR Right to Explanation:** Visual counterfactuals help users understand why they were denied a service (if vision models are involved)

### Model Auditing

- **Fairness audits:** Generate counterfactuals across demographic groups to detect disparities
- **Robustness testing:** Identify minimal perturbations that flip predictions; reveals adversarial vulnerabilities
- **Safety validation:** In autonomous systems, understand decision boundaries

### Human-AI Collaboration

- **Clinician trust:** Realistic counterfactuals (via F-space refinement) build confidence in AI recommendations
- **Training & education:** Visual explanations help domain experts understand model reasoning
- **Debiasing:** Transparent explanations highlight spurious correlations, enabling data or model corrections

---

## Open Research Directions

1. **Semantic factor discovery:** Automatically label what each disentangled factor represents (tumor size, location, texture, etc.)

2. **Counterfactual minimality:** Extend minimality metrics beyond L2 distance to include perceptual and semantic measures

3. **Causal counterfactuals:** Combine CCA with causal inference frameworks to generate interventional counterfactuals (not just observational)

4. **Generalization across datasets:** How well do CCA factors transfer across different imaging protocols or patient populations?

5. **Interactive refinement:** Allow users to specify which factors to vary, enabling human-guided counterfactual generation

---

## Conclusion

Counterfactual Contrastive Analysis represents a significant advance in visual explainability by moving beyond classifier-gradient-dependent methods. By leveraging **classifier-free generative modeling** and **disentangled representation learning**, CCA produces realistic, faithful, and interpretable visual counterfactuals—especially valuable in medical imaging and high-stakes AI systems.

The key contributions—enhanced contrastive analysis, F-space refinement, and empirical disentanglement measurement—address real-world challenges in generating plausible explanations. The paper's focus on medical imaging datasets (BloodMNIST, OCTMNIST, BraTS) demonstrates practical applicability, while the low computational cost (0.25 s/image) makes it deployable in clinical workflows.

**For practitioners:** CCA provides a principled, efficient method for generating visual explanations in medical AI and other vision applications.

**For researchers:** The work opens pathways for classifier-agnostic explainability, domain-aware refinement strategies, and seamless integration of generative models with interpretability research.

---

## References & Links

### Primary Source
- **ArXiv Paper:** [https://arxiv.org/abs/2608.19032](https://arxiv.org/abs/2608.19032)
- **MICCAI 2026:** [https://papers.miccai.org/miccai-2026/paper/3698_paper.pdf](https://papers.miccai.org/miccai-2026/paper/3698_paper.pdf)

### Key Related Papers

**Counterfactual Explanations:**
- Wachter, T., Mittelstadt, B., & Russell, C. (2017). Counterfactual Explanations without Opening the Black Box. arXiv:1711.00399
- Verma, S., Dickerson, J., & Hines, K. (2020). Counterfactual Explanations and Algorithmic Recourse for ML. arXiv:2010.10596

**Disentangled Representation Learning:**
- Higgins, I., Matthey, L., Pal, A., et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework. ICLR.
- Srinivasan, R., Vig, J., & Feige, I. (2019). Full-Gradient Representation for Neural Network Visualization. NeurIPS.

**StyleGAN2 & Generative Models:**
- Karras, T., Laine, S., Aittala, M., et al. (2020). Analyzing and Improving the Image Quality of StyleGAN. CVPR.
- Upchurch, P., et al. (2020). Deep Image Prior. IJCV.

**Visual Interpretability:**
- Zhang, Q., & Zhu, S. C. (2018). Visual Interpretability for Deep Learning. IEEE Trans. Pattern Anal. Mach. Intell.
- Fong, R. C., & Vedaldi, A. (2017). Interpretable Explanations of Black Boxes by Meaningful Perturbation. ICCV.

**Medical AI & Explainability:**
- Caruana, R., Lou, Y., Gehrke, J., et al. (2015). Intelligible Models for Healthcare. KDD.
- Vilone, G., & Longo, L. (2021). Explainability and Interpretability in AI: A Survey. arXiv:2104.13200

**Contrastive Analysis & Statistics:**
- Flury, B., & Riedwyl, H. (1988). Multivariate Statistics: A Practical Approach. Chapman & Hall.
- Jing, L., & Tian, Y. (2020). Self-Supervised Learning: Generative or Contrastive. IEEE TPAMI.

### Datasets
- **MedMNIST:** [https://medmnist.com/](https://medmnist.com/)
- **BraTS Challenge:** [https://www.med.upenn.edu/cbica/brats/](https://www.med.upenn.edu/cbica/brats/)

### Tools & Frameworks
- **StyleGAN2-Ada-PyTorch:** [https://github.com/NVlabs/stylegan2-ada-pytorch](https://github.com/NVlabs/stylegan2-ada-pytorch)
- **PyTorch:** [https://pytorch.org/](https://pytorch.org/)
- **MedMNIST Python Package:** [https://pypi.org/project/medmnist/](https://pypi.org/project/medmnist/)

### Visual Counterfactual Baselines
- **VAE-CE:** Goyal, Y., et al. (2021). Counterfactual Visual Explanations. ICML.
- **Contrastive Explanations:** Dhurandhar, A., et al. (2019). Explanations based on the Missing. NeurIPS.
- **Diffusion-based approaches:** Reviewed in [2601.21851] and recent 2025–2026 papers

---

## Author & Citation

**How to Cite:**

```bibtex
@inproceedings{he2026counterfactual,
  author = {He, Yunlong and Gori, Pietro},
  title = {Counterfactual Contrastive Analysis},
  booktitle = {Proceedings of the 29th International Conference on Medical Image Computing and Computer-Assisted Intervention (MICCAI 2026)},
  year = {2026},
  url = {https://arxiv.org/abs/2608.19032}
}
```

**Authors:**
- **Yunlong He** – Télécom Paris, Institut Polytechnique de Paris
- **Pietro Gori** – Télécom Paris, Institut Polytechnique de Paris

---

**Last Updated:** November 25, 2026  
**Repository:** [Giang-Dang/computer-science-news](https://github.com/Giang-Dang/computer-science-news)
