# Scaling Generative Foundation Models for Chest Radiography with Rectified Flow Transformers

## Executive Summary

This paper introduces RadiT (Radiography Transformer), the first billion-parameter generative foundation model trained from scratch for high-fidelity chest radiograph synthesis. By combining rectified flow transformers with 1.2 million clinical radiographs and 1.6 trillion training tokens, the work achieves 4-10x improvements in generation quality metrics over prior methods. This advancement enables controlled, diverse synthetic medical imaging data generation that addresses critical generalization failures in diagnostic AI systems across different patient populations and clinical institutions.

## Problem Statement

Medical imaging AI models face fundamental generalization challenges:

- **Demographic bias**: Models trained on limited populations often fail across different ages, genders, and ethnicities
- **Institutional variation**: Diagnostic models don't generalize across imaging equipment and acquisition protocols from different hospitals
- **Limited dataset diversity**: Medical datasets are small, expensive to collect, and often skewed toward specific populations or pathologies
- **Model robustness testing**: Hard to systematically evaluate AI robustness across diverse conditions without diverse real data
- **Fairness and equity**: Biased models perpetuate healthcare disparities in clinical deployment

Current approaches either use limited real data (creating bias) or simple rule-based synthetic data (lacking realism). There's no method for generating realistic, diverse, controllable chest radiographs at scale—until now.

## Core Concepts & Theory

### Rectified Flow Framework

Rectified flow offers a new approach to generative modeling:

#### Traditional Diffusion vs. Rectified Flow

**Diffusion Models** connect data and noise through random walks:
- Follow stochastic paths from data → noise (forward) or noise → data (reverse)
- Require many denoising steps (typically 50-1000) for quality generation
- Simple noise schedule but computationally expensive sampling

**Rectified Flow** connects data and noise through straight-line trajectories:
- Data and noise are connected via linear interpolation in latent space
- Models learn to follow straight paths rather than random walks
- Enables faster generation with fewer steps (often 1-10 steps sufficient)
- More efficient reverse process learning

#### Mathematical Foundation

In rectified flow:
- A straight-line path is constructed between data point x₀ and noise point x₁
- The model learns a velocity field to follow these optimal paths
- Sampling involves integrating along the learned velocity field
- Results in faster, more stable generation compared to diffusion

### Transformer Architecture for Medical Imaging

**RadiT (Radiography Transformer) Design**:
- Scales transformers to billion-parameter scale while maintaining interpretability
- Preserves spatial structure needed for medical image generation
- Combines rectified flow's efficiency with transformer's modeling capacity

**Key architectural features**:
1. Hierarchical token processing for multi-scale medical features
2. Attention patterns that respect anatomical relationships in radiographs
3. Conditioning mechanisms for controllable generation (pathology, view, demographics)

## Main Ideas & Contributions

### Novel Technical Contributions

1. **Billion-Parameter Medical Generative Model**: First generative foundation model at scale trained from scratch for chest radiography—represents massive scaling-up from prior work

2. **Rectified Flow for Medical Imaging**: Successfully applies rectified flow framework (new generative approach) to highly structured medical imaging domain, showing broad applicability

3. **Controllable Synthesis with Metadata**: Incorporates clinical expert-guided metadata enabling generation control across:
   - Multiple patient demographics (age, gender, body composition)
   - Acquisition parameters (different imaging views: PA, lateral, etc.)
   - Pathological conditions (specific diseases and findings)

4. **State-of-the-Art Quality**: Achieves 4x improvement on FDD and 10x on KDD metrics—dramatic quality jump

### Intuition Behind Design Choices

**Why Rectified Flow?**
- Medical images have well-defined structure; straight-line interpolation preserves this structure better than random walks
- Faster generation enables more training iterations and better convergence
- Fewer sampling steps reduce computational cost of synthesis

**Why Billion-Parameter Scale?**
- Medical diagnosis requires capturing subtle anatomical details across full radiograph
- Large model capacity enables learning complex, diverse radiographic patterns
- Supports fine-grained controllability across multiple dimensions

**Why Metadata-Rich Training?**
- Clinical experts provide crucial guidance on what variations matter
- Enables future users to generate specific scenarios (e.g., "60-year-old male with pneumonia, PA view")
- Supports fairness testing across demographic groups

## Methodology & Implementation

### Dataset and Training

**Training Data**:
- 1.2 million chest radiographs from curated, heterogeneous clinical sources
- Expert-guided metadata annotation for each image
- Represents diversity across:
  - Patient demographics (age, gender, body type)
  - Imaging views and protocols
  - Pathological conditions and normal variants
  - Multiple clinical institutions and equipment

**Training Scale**:
- 1.6 trillion tokens processed during training
- Comparable scale to large language models
- Enables learning complex medical image distributions

**Model Variants**:
- **RadiT Base**: Smaller, efficient variant
- **RadiT Large**: Mid-size for balanced performance
- **RadiT XL**: Largest model with best quality

### Experimental Setup

**Evaluation Benchmarks**:
- **CheXGenBench**: Comprehensive benchmark for chest radiograph generation
- **Metrics**:
  - FDD (Fréchet Inception Distance): Measures distribution similarity
  - KDD (Kernel Inception Distance): Alternative distribution metric
  - Perceptual quality metrics
  - Clinical expert evaluation

**Baseline Comparisons**:
- Prior generative medical imaging models
- Diffusion-based radiograph synthesis methods
- Traditional synthetic data approaches

**Evaluation Protocols**:
- Quantitative metrics on held-out test distributions
- Clinical expert evaluation of realism and correctness
- Cross-institutional generalization testing

### Results and Metrics

**Quantitative Performance**:
- **FDD Score**: 4x improvement over prior state-of-the-art
  - Lower FDD = better quality and diversity
  - Indicates much more realistic synthetic radiographs

- **KDD Score**: 10x improvement over prior state-of-the-art
  - Confirms dramatic quality gap across different metrics

**RadiT XL (Largest Model)** shows best performance across all metrics

**Quality Improvements Across Dimensions**:
- Radiographic anatomy: More accurate depiction of chest structures
- Pathological realism: More clinically convincing disease presentations
- Demographic diversity: Realistic variation across age, gender, body composition
- Acquisition variation: Authentic differences between PA, lateral, and other views

## Practical Applications & Use Cases

### Dataset Augmentation
- Generate synthetic radiographs to balance underrepresented patient populations
- Create diverse training sets for diagnostic model development
- Address data scarcity in specialized pathologies

**Example**: Hospital with limited pediatric pneumonia cases can generate realistic synthetic examples for model training and evaluation

### Model Robustness Testing
- Evaluate diagnostic AI performance across systematic variations
- Test model behavior under different acquisition parameters
- Assess generalization across demographic groups

**Example**: Test whether an AI diagnosis model's performance degrades on images from older imaging equipment (common in rural hospitals)

### Fairness and Bias Evaluation
- Generate counterfactual radiographs to test model fairness
- Evaluate if models make different predictions for same pathology across demographics
- Support equitable AI development in healthcare

**Example**: Generate identical pathology in different demographic groups to verify diagnostic model doesn't exhibit demographic bias

### Clinical Data Privacy
- Enable realistic medical imaging training data without actual patient data
- Support collaborative research without HIPAA violations
- Enable external researchers to develop and test algorithms safely

### Education and Training
- Generate radiographic examples for medical student education
- Create diverse case collections for training radiologists
- Support simulation of rare conditions for learning

**Example**: Training radiologists on presentations of rare diseases with diverse patient populations

## Insights & Implications

### Broader Field Impact

**Generative Models for Structured Domains**

This work demonstrates that billion-parameter generative models work well for highly structured, specialized domains like medical imaging. This opens applications in other specialized imaging (pathology, CT, MRI) and structured data synthesis.

**Rectified Flow as Practical Alternative to Diffusion**

Success in medical imaging suggests rectified flow's efficiency advantages translate to real applications. May enable practical deployment where diffusion was too slow.

**Foundation Models for Medical Domains**

Scaling foundation models to specific medical imaging domains (following the LLM paradigm) appears promising for creating general-purpose medical imaging models that can be adapted for various tasks.

### State-of-the-Art Advancement

- First practical billion-parameter generative model for medical imaging
- Largest and highest-quality synthetic radiograph generation to date
- Demonstrates path forward for foundation models in specialized medical domains

### Clinical and Ethical Implications

**Positive impacts**:
- Can help reduce demographic bias in diagnostic AI
- Enables diverse training data without recruiting diverse patient populations
- Supports more equitable AI development in healthcare

**Important considerations**:
- Synthetic data quality could mislead model developers if limitations not understood
- Regulatory path for synthetic medical data in clinical development still evolving
- Synthetic data supplements but cannot replace diverse real patient data

### Limitations and Open Questions

1. **Validation Beyond Metrics**: Do clinicians actually find RadiT synthetic radiographs realistic? Do they transfer to real diagnostic task performance?

2. **Rare Pathologies**: Can the model generate clinically accurate radiographs of rare diseases with sufficient training examples?

3. **Hardware Requirements**: What computational infrastructure is needed for generating synthetic radiographs at clinical scale?

4. **Regulatory Framework**: How should synthetic medical imaging data be regulated and validated before clinical use?

5. **Pathology Accuracy**: Can the model maintain anatomical and pathological accuracy while providing demographic diversity?

## Code & Resources

### Official Resources
- **Paper**: https://arxiv.org/abs/2606.19460v1
- **HTML Version**: https://arxiv.org/html/2606.19460v1
- **Institutions**: Imperial College London, University of Edinburgh, Causality in Healthcare AI Hub
- **Dataset**: CheXGenBench benchmark

### Model and Code Availability
- Check paper for official release information
- Likely available through institutional partners (Imperial College, Edinburgh)
- May require institutional review for medical applications

### Dependencies and Requirements

**For inference**:
- PyTorch 2.0+ or TensorFlow 2.10+
- CUDA 11.8+ for GPU acceleration
- 40GB+ GPU memory for RadiT XL
- Recommend multi-GPU setup for batch generation

**For training** (if fine-tuning):
- Large GPU cluster (typically 8+ A100 GPUs)
- 1.2M+ radiographs with metadata annotations
- Clinical validation infrastructure

### Quick-Start Guide for Synthetic Data Generation

```python
# Pseudocode for RadiT usage
from radiology_models import RadiT

model = RadiT.load("radiant-xl")

# Generate synthetic radiograph with specific characteristics
synthetic_xray = model.generate(
    patient_age=45,
    patient_gender="female",
    pathology="pneumonia",
    acquisition_view="PA",  # Posteroanterior view
    num_samples=10,  # Generate 10 variations
)

# Use in training data augmentation
training_data.add_synthetic_images(synthetic_xray)
```

Key parameters:
- `pathology`: Specify condition (normal, pneumonia, tuberculosis, etc.)
- `acquisition_view`: PA, lateral, lordotic
- `patient_demographics`: Control age, gender, body composition
- `num_samples`: Batch generation for efficiency

## Related Work & Context

### Foundation Work
- **Diffusion Models**: Score-based generative modeling and denoising approaches
- **Transformers for Vision**: Vision Transformer and scaling to medical imaging
- **Conditional Generation**: Techniques for controlling generative models

### Related Recent Papers
- **Rectified Flow** (Song et al.): The generative model framework used
- Other billion-parameter vision models and foundation models
- Medical imaging synthesis and data augmentation papers
- Fairness in medical AI research

### Prior Medical Imaging Work
- Smaller-scale radiograph synthesis with GANs and diffusion models
- Dataset augmentation techniques for medical imaging
- Bias and fairness in diagnostic AI

### Future Research Directions

1. **Multi-Modal Medical Foundation Models**: Extend to CT, MRI, pathology images with shared foundation

2. **3D Reconstruction**: Generate volumetric medical data (CT scans) rather than 2D radiographs

3. **Temporal Imaging**: Generate longitudinal imaging sequences showing disease progression

4. **Real-World Deployment**: Validate synthetic data for actual diagnostic model training and clinical validation

5. **Fairness-Aware Generation**: Explicitly optimize generation to minimize bias in generated data

6. **Rare Disease Generation**: Specialized models for generating synthetic examples of ultra-rare conditions
