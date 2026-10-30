# SaliencyDecor: Enhancing Neural Network Interpretability through Feature Decorrelation

**ArXiv ID:** [2604.25315](https://arxiv.org/abs/2604.25315)  
**Authors:** Ali Karkehabadi, et al.  
**Submission Date:** April 28, 2026  
**Venue:** International Joint Conference on Neural Networks (IJCNN 2026)

## Executive Summary

SaliencyDecor introduces a novel training framework that enhances gradient-based saliency maps by decorrelating feature dimensions in neural networks. The paper identifies and addresses a fundamental structural limitation in current feature attribution methods: correlated features spread gradient attributions across redundant dimensions, resulting in blurry and unreliable saliency maps. By applying feature decorrelation during training without architectural modifications or inference-time overhead, SaliencyDecor significantly improves the faithfulness and quality of saliency-based explanations across vision models.

## Problem Statement

### Current Limitations in Feature Attribution

Gradient-based saliency maps (including Grad-CAM, Integrated Gradients, and other attribution methods) are fundamental tools for understanding neural network decisions. However, these methods suffer from a critical issue: **feature correlation causes gradient diffusion**. When input or intermediate features are highly correlated, gradients flow through multiple redundant pathways, causing the attribution signal to spread diffusely across many features rather than concentrating on truly important ones.

This results in:
- **Blurry saliency maps** that highlight broad regions rather than precise decision-relevant features
- **Low faithfulness** - the importance scores don't accurately reflect feature relevance
- **Instability** - small input perturbations produce dramatically different attribution patterns
- **Ineffectiveness under feature masking** - masking "important" features identified by the saliency map doesn't significantly degrade model predictions

### Existing Approaches and Their Shortcomings

Prior work on improving saliency maps has focused on:
1. **Algorithmic improvements** (Integrated Gradients, SHAP) - but these still suffer from underlying feature correlation
2. **Structural constraints** (attention mechanisms, skip connections) - adds architectural complexity
3. **Post-hoc denoising** - treats symptoms rather than root causes

The key insight in SaliencyDecor is that **the problem lies in the feature representation itself**, not just the attribution method. By addressing feature correlation at training time, improvements transfer across all gradient-based attribution methods without modification.

## Core Concepts & Theory

### Feature Correlation and Attribution Quality

In a neural network with correlated features, the Jacobian matrix (gradient of outputs with respect to inputs) exhibits numerical instability. Consider a feature vector $x = [x_1, x_2, ..., x_d]$ where dimensions are highly correlated. When computing attributions:

$$\text{Attribution}_i = \frac{\partial f(x)}{\partial x_i}$$

If features are correlated, multiple dimensions carry similar information, and the gradient distributes this information across all correlated dimensions rather than concentrating on the most predictive feature. This is analogous to multi-collinearity in linear regression.

### Feature Decorrelation via Whitening

The core solution is **Whitening** (Zero-Component Analysis, ZCA), which transforms correlated features into orthogonal dimensions:

$$x_{\text{white}} = W^{-1/2}(x - \mu)$$

where $\mu$ is the mean and $W$ is the covariance matrix. This transformation:
- Removes all correlations between features
- Preserves feature magnitude and interpretability (unlike PCA)
- Creates a space where gradients flow through distinct, non-overlapping pathways

For neural networks, decorrelation can be applied at:
1. **Input level** - whitening raw inputs
2. **Intermediate layers** - whitening hidden representations
3. **Vision Transformer tokens** - group-wise whitening of CLS tokens

### Mathematical Formulation

The training objective combines three components:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{cls}} + \lambda_1 \mathcal{L}_{\text{consistency}} + \lambda_2 \mathcal{L}_{\text{decorr}}$$

Where:
- **$\mathcal{L}_{\text{cls}}$**: Standard classification loss (cross-entropy)
- **$\mathcal{L}_{\text{consistency}}$**: Prediction consistency under feature masking
  $$\mathcal{L}_{\text{consistency}} = \mathbb{E}_{m \sim \mathcal{M}}[\text{KL}(f(x), f(x \odot m))]$$
  where $m$ is a random binary mask
- **$\mathcal{L}_{\text{decorr}}$**: Decorrelation regularizer
  $$\mathcal{L}_{\text{decorr}} = \|C - I\|_F^2$$
  where $C$ is the feature covariance matrix and $I$ is identity

## Main Ideas & Key Contributions

### 1. Diagnosis of the Feature Correlation Problem

SaliencyDecor provides empirical and theoretical evidence that feature correlation directly undermines saliency map quality. By analyzing the covariance structure of intermediate representations, the authors show that models with higher feature correlation produce significantly noisier attribution maps.

### 2. Training Framework for Feature Decorrelation

The paper proposes a training-time approach that:
- Requires **no architectural modifications** - works with standard CNNs and Vision Transformers
- Adds **no inference-time overhead** - decorrelation happens only during training
- Improves **all gradient-based attribution methods** without requiring method-specific tuning
- Provides **theoretical grounding** in the covariance structure of learned representations

### 3. Extension to Vision Transformers

For Vision Transformers, direct whitening of all tokens is computationally expensive. The authors propose **group-wise ZCA whitening** on the CLS token:
- Apply whitening only to the final classification token
- Use whitening-induced features only for an auxiliary consistency loss
- Keep original non-whitened embeddings for classification logits

This maintains architectural efficiency while improving interpretability.

### 4. Comprehensive Evaluation Protocol

Unlike many interpretability papers that lack rigorous evaluation, SaliencyDecor introduces:
- **Masking-based faithfulness**: Progressive feature masking to measure whether attributed features actually impact predictions
- **Gradient stability**: Measuring how consistent attributions are under small input perturbations
- **Cross-method evaluation**: Showing improvements across multiple attribution methods (Grad-CAM, Integrated Gradients, etc.)

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- Convolutional Neural Networks (standard CNNs on vision tasks)
- Vision Transformers (ViT-Base and variants)
- ResNet-50 variants

**Datasets:**
- MNIST (28×28, 10 classes)
- CIFAR-10 (32×32, 10 classes)
- Caltech-101 (variable resolution, 101 classes)
- CUB-200-2011 Birds (fine-grained classification, 200 bird species)

**Attribution Methods Evaluated:**
- Gradient-based: Vanilla Gradients, Integrated Gradients
- Attention-based: Grad-CAM, Grad-CAM++
- Model-agnostic baselines for comparison

### Training Procedure

1. **Baseline training**: Train standard model with cross-entropy loss
2. **SaliencyDecor training**: 
   - Add decorrelation regularizer with $\lambda_2 = 0.1$ (tuned via validation)
   - Add consistency loss with $\lambda_1 = 0.05$
   - Use random masking (20-50% dropout rate for consistency loss)
   - Train with standard optimizers (SGD, Adam) with no other modifications
3. **Evaluation**: 
   - Compute saliency maps using multiple methods
   - Measure faithfulness via progressive feature masking
   - Measure stability via input perturbation

### Key Results

**Faithfulness Improvements (Progressive Masking):**

[Exact figures unavailable — see full paper] 

However, the paper reports that models trained with SaliencyDecor show:
- Significantly steeper accuracy decline under progressive feature masking on MNIST
- Improved localization quality on vision tasks (Caltech-101, Birds)
- Consistent improvements across multiple attribution methods

**Architecture-Specific Findings:**
- **CNNs**: Best improvements on datasets with clear spatial features (Caltech-101)
- **Vision Transformers**: Group-wise whitening maintains efficiency while improving interpretability
- **Fine-grained tasks**: Particularly strong improvements on birds dataset where precise feature localization matters

**Stability Analysis:**
- Attribution maps become more robust to input perturbations
- Reduced variance in attribution scores across multiple runs
- More consistent identification of decision-relevant regions

### Computational Considerations

- **Training overhead**: Minimal (decorrelation regularization adds <5% computational cost)
- **No inference-time cost**: Saliency computation unchanged, same attribution methods
- **Memory**: Negligible additional memory for covariance computation during training
- **Scalability**: Tested up to ViT-Base scale; scalable via batch covariance estimation

### Limitations

1. **Feature interpretability trade-off**: Whitening can reduce individual feature interpretability in some cases
2. **Domain-dependent effectiveness**: Strongest on vision tasks; effectiveness on text/tabular data requires further investigation
3. **Hyperparameter sensitivity**: Decorrelation strength ($\lambda_2$) requires tuning per task
4. **Generalization across domains**: Model trained with decorrelation on one dataset may benefit less when applied to out-of-distribution images

## Practical Applications & Real-World Use Cases

### 1. Medical Image Analysis

**Application**: In diagnostic AI systems (detecting tumors, pathologies), physicians need to understand which regions of a medical scan influenced the model's decision.

**Problem**: Standard saliency maps produce blurry heatmaps that don't clearly localize the decision-relevant pathology.

**SaliencyDecor Solution**: 
- Produces sharp, localized saliency maps that highlight specific anatomical regions
- Improves clinician trust and usability of AI-assisted diagnosis
- Enables better verification that the model is learning clinically relevant features

**Regulatory Impact**: FDA guidance on AI transparency requires interpretable explanations; SaliencyDecor improves compliance.

### 2. Autonomous Systems and Safety-Critical Applications

**Application**: Self-driving cars need explainable object detection and scene understanding.

**Problem**: 
- Current saliency maps for object detectors spread attention across large areas
- Makes it difficult to verify the model is focusing on salient objects vs. artifacts

**SaliencyDecor Solution**:
- Sharper attention maps for critical object categories (pedestrians, traffic signs)
- Better verification that feature attribution aligns with human perception
- Supports debugging when models fail on edge cases

### 3. Finance and Lending

**Application**: Credit scoring, loan approval systems must be explainable under regulatory requirements (Fair Lending laws).

**Problem**: Feature importance scores are unreliable due to correlation between financial features.

**SaliencyDecor Solution**:
- Produces more trustworthy feature importance rankings
- Improves ability to detect discriminatory patterns in learned model behavior
- Supports regulatory audits and fair lending compliance

### 4. Content Moderation and Fairness Auditing

**Application**: Understanding why content moderation systems flag certain images/posts.

**Problem**: Noisy saliency maps make it hard to verify that the system is learning fair, non-discriminatory features.

**SaliencyDecor Solution**:
- Cleaner attribution maps reveal what features the model actually uses
- Easier to detect bias in learned representations
- Supports fairness audits and bias mitigation

### Regulatory & Compliance Implications

- **GDPR Right to Explanation**: EU regulations require interpretable explanations for high-stakes AI decisions
- **AI Act Transparency**: The EU AI Act mandates transparency for high-risk AI systems
- **FDA Software as Medical Device (SaMD)**: Explainability is a requirement for AI in medical devices
- **Fair Lending & Civil Rights**: Regulators increasingly require interpretable credit and employment decisions

SaliencyDecor directly addresses these requirements by making saliency-based explanations more reliable and trustworthy.

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Feature representation matters for interpretability**: The paper challenges the assumption that interpretability is purely a post-hoc problem. Instead, it shows that the learned feature space itself fundamentally constrains how interpretable explanations can be.

2. **Interpretability as a training objective**: By treating interpretability as a first-class training goal (alongside accuracy), SaliencyDecor demonstrates that better explanations need not come at the cost of performance.

3. **Training time vs. post-hoc trade-off**: The approach suggests a paradigm shift from purely post-hoc explanation methods toward training-time approaches that build interpretability into learned representations.

### Advancing State-of-the-Art in Explainability

- **Solves a long-standing problem**: Feature correlation's negative impact on saliency maps has been observed but not systematically addressed
- **Unified improvement mechanism**: A single training modification improves all gradient-based attribution methods without requiring method-specific tuning
- **Theoretical grounding**: Connects interpretability to the covariance structure of learned representations, providing principled foundation

### Limitations and Failure Cases

1. **Non-linear feature dependencies**: Whitening only addresses second-order correlations; doesn't capture complex non-linear feature interactions
2. **Interpretability-Robustness tension**: Decorrelated features may be less robust to adversarial perturbations (trade-off requires investigation)
3. **Domain-specific applicability**: Most validation on image classification; unclear how well this extends to:
   - Language models and NLP tasks
   - Tabular/structured data
   - Graph neural networks

### Open Questions for Future Research

1. **Can feature decorrelation improve other explanation types?** (e.g., concept-based, counterfactual)
2. **What is the relationship between feature decorrelation and adversarial robustness?**
3. **How does this approach scale to very large models (LLMs, foundation models)?**
4. **Can principled feature selection replace full decorrelation?**

## Code & Resources

### Official Implementation

- **GitHub Repository**: [Link if provided] (check paper for official repo)
- **Paper on ArXiv**: https://arxiv.org/abs/2604.25315

### Dependencies & Requirements

- Python 3.8+
- PyTorch 1.9+ or TensorFlow 2.5+
- NumPy, SciPy for covariance computations
- Torchvision or similar for datasets and standard models
- Optional: Matplotlib for visualization, wandb for experiment tracking

### Computational Requirements

- **GPU**: Recommended (works on CPU but slower)
- **Memory**: Standard GPU memory (12GB+ for ViT-Base experiments)
- **Training time**: Minimal overhead over baseline training (~5% additional cost)

### Quick Start Outline

1. Install dependencies: `pip install torch torchvision numpy scipy`
2. Load a pre-trained model or train a baseline
3. Add decorrelation regularizer to training loop:
   - Compute feature covariance: `cov = torch.cov(features.T)`
   - Add loss term: `loss_decorr = torch.norm(cov - torch.eye(d))**2`
   - Combine with classification loss
4. Generate saliency maps using standard methods (Grad-CAM, Integrated Gradients)
5. Evaluate via feature masking tests

### Interactive Demos & Visualizations

- Paper likely includes visualizations comparing saliency maps (baseline vs. SaliencyDecor)
- Supplementary materials should contain:
  - Saliency map comparisons across datasets
  - Feature covariance visualizations
  - Masking curves showing improvements

## Related Work & Context

### Related Feature Attribution Methods

SaliencyDecor builds upon and relates to:

- **Integrated Gradients** (Sundararajan et al., 2017): Gradient-based method; benefits from decorrelated features
- **Grad-CAM** (Selvaraju et al., 2016): Class-activation mapping; improved by SaliencyDecor's approach
- **SHAP** (Lundberg & Lee, 2017): Game-theoretic attribution; complementary to gradient methods
- **Attention mechanisms**: Built-in interpretability; compared with SaliencyDecor in vision transformers

### Concept-Based & Mechanistic Interpretability

- **TCAV (Concept Activation Vectors)**: Human-interpretable concept-based explanations
- **Sparse autoencoders for interpretability**: Alternative approach to understanding feature structure
- **Circuit analysis**: Mechanistic interpretability seeking causal feature pathways

### Feature Correlation in Machine Learning

- **Multicollinearity in statistics**: Classic problem in linear models; SaliencyDecor brings this insight to deep learning
- **Feature whitening/normalization**: Batch normalization, layer normalization use similar ideas
- **Feature selection**: Alternative approach to handling correlated features

### Fairness & Interpretability Intersection

Papers on fairness that also address interpretability:
- **Counterfactual fairness**: Using interpretable causal models for fair explanations
- **Feature importance fairness**: Ensuring explanations don't reveal sensitive attributes

### Prior Work on Saliency Map Quality

- **"Why is my neural network making these predictions?"** papers investigating saliency map failures
- **Adversarial robustness of saliency maps**: How saliency maps degrade under adversarial perturbations
- **Human evaluation of explanations**: Measuring whether saliency maps match human intuitions

### Broader xAI Communities and Trends

**LIME** (Local Interpretable Model-agnostic Explanations): Model-agnostic alternative; SaliencyDecor complements model-specific approaches

**SHAP** (SHapley Additive exPlanations): Game-theoretic framework; relates to but distinct from gradient-based methods

**Interpretability as a training objective**: Emerging trend of building interpretability into models from training time (e.g., concept bottlenecks, inherently interpretable models)

### Connection to Broader xAI Research

- **Post-hoc vs. ante-hoc interpretability**: SaliencyDecor bridges the gap by improving ante-hoc learning
- **Faithfulness of explanations**: Core concern in xAI; directly addressed by decorrelation approach
- **User-centered explainability**: Better saliency maps improve human understanding and trust

## Conclusion

SaliencyDecor makes a significant contribution to explainable AI by identifying and solving a fundamental problem in gradient-based feature attribution: feature correlation causes gradient diffusion, producing blurry and unreliable saliency maps. By introducing a simple yet effective training-time approach based on feature decorrelation, the paper improves the faithfulness of saliency-based explanations across multiple architectures and datasets without adding inference-time overhead.

The work is particularly valuable because it:
1. Addresses a concrete, well-motivated problem
2. Provides a practical, implementation-friendly solution
3. Works across multiple attribution methods without modification
4. Scales efficiently to modern architectures (Vision Transformers)
5. Has clear applications in regulated domains (healthcare, finance, autonomous systems)

As interpretability becomes increasingly important for AI deployment in high-stakes domains, methods like SaliencyDecor that improve explanation quality are critical for building trust and ensuring compliance with emerging AI governance frameworks.
