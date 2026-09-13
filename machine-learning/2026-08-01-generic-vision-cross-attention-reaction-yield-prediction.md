# Generic Vision and Cross-Attention for Reaction Yield Prediction

**Authors:** Qiwei Han, Chi Zhou  
**arXiv ID:** 2608.00776  
**Submission Date:** August 1, 2026  
**Categories:** Machine Learning, Chemical Physics  
**Paper Length:** 12 pages, 4 figures

## Executive Summary

This paper proposes a novel multimodal approach to reaction yield prediction by combining generic computer vision models with tabular molecular descriptors through cross-attention mechanisms. By leveraging 2D molecular topology visualization alongside traditional quantum chemical descriptors, the method achieves superior predictive accuracy (Test RMSE 5.27%) while providing mechanistic interpretability through spatial feature attribution.

## Problem Statement

Reaction yield prediction is critical for accelerating synthetic chemistry, but traditional methods suffer from significant limitations:

1. **1D quantum descriptors constraints:** Standard molecular descriptors (quantum properties, electronic structure) lack explicit spatial information about molecular geometry and steric effects
2. **Limited feature representation:** Pure quantum-based approaches cannot capture complex steric interactions and spatial relationships critical for predicting reaction outcomes
3. **Interpretability gap:** Black-box models fail to explain which molecular features drive yield predictions
4. **Data efficiency:** Requires large datasets of quantum calculations, which are computationally expensive to generate

The research gap: Can multimodal learning that incorporates visual representations of molecular structure improve predictive accuracy and provide mechanistic insights?

## Core Concepts & Theory

### Multimodal Learning Framework

The paper leverages the principle that different representations of the same entity can provide complementary information:
- **Tabular modality:** Physical-organic chemistry descriptors (electronic, steric, electronic effects)
- **Visual modality:** 2D skeletal representations of molecular structures

### Cross-Attention Mechanism

Cross-attention allows the model to dynamically align and fuse information between modalities:
- Query vectors from one modality attend to key-value pairs from another
- Enables selective information flow based on learned relevance
- Allows each modality to guide interpretation of the other

### Vision as a Generic Feature Extractor

A surprising finding: generic computer vision backbones (e.g., ResNets, ViTs) trained on image classification can be repurposed to extract meaningful features from molecular structure images without specialized chemistry pretraining.

## Main Ideas & Contributions

### 1. Dual-Modal Architecture
- **Vision pathway:** Generic CNN/ViT processes 2D skeletal molecular structures
- **Tabular pathway:** Dense networks process quantum and chemistry descriptors
- **Fusion layer:** Cross-attention module learns optimal information weighting

### 2. Superior Performance Through Multimodal Synergy
- Vision backbone alone outperforms quantum-only baselines
- Combined cross-attention model achieves best results
- Demonstrates value of architectural diversity over single-modality sophistication

### 3. Mechanistic Interpretability
- **Spatial feature attribution:** Vision pathway learns where to focus spatially (e.g., reactive centers)
- **Descriptor-guided querying:** Tabular features guide which spatial regions to attend
- **Chemical hierarchy learning:** Model learns to prioritize critical steric bottlenecks

## Methodology & Implementation

### Model Architecture

```
Input: 2D Molecular Image + Tabular Descriptors
       ↓
[Vision Backbone]  [Tabular Dense Network]
       ↓                    ↓
[Feature Extraction]  [Descriptor Features]
       ↓                    ↓
       ←─ Cross-Attention ─→
            ↓
[Fusion Features]
            ↓
[Yield Predictor]
            ↓
      Yield Prediction
```

### Dataset & Experimental Setup

- **Input representations:** 2D skeletal structures rendered as images + chemical descriptors
- **Target:** Reaction yield (continuous variable)
- **Test RMSE:** 5.27% (on normalized scale)
- **Evaluation:** Standard train/validation/test splits with multiple random seeds

### Key Results

**Quantitative Performance:**
- Test RMSE: 5.27% (estimated absolute percentage)
- Vision-only baseline: [Exact figures unavailable — see full paper]
- Quantum-only baseline: [Exact figures unavailable — see full paper]
- Improvement over baselines: [Exact percentages unavailable — see full paper]

**Mechanistic Findings:**
1. Vision pathway learns spatial region importance independent of tabular features
2. Steric identification (bulky groups affecting reactivity) is offloaded to visual pathway
3. Cross-attention learns dynamic prioritization of steric bottlenecks (e.g., aryl halides)
4. Different descriptors show varying importance across reaction types

## Practical Applications & Use Cases

### 1. Synthetic Chemistry Optimization
- **Reaction screening:** Predict yields before expensive experimental synthesis
- **Reaction condition optimization:** Identify which structural features limit yield
- **Scale-up planning:** Understand mechanistic bottlenecks before scale-up

### 2. Drug Discovery
- **Lead optimization:** Predict synthetic accessibility and intermediate yields
- **Route planning:** Identify high-risk synthesis steps early
- **Parallel synthesis:** Prioritize which compounds to synthesize based on predicted yields

### 3. Materials Science
- **Polymer synthesis:** Predict monomer reactivity and polymerization yields
- **Catalysis:** Correlate catalyst structure with reaction efficiency
- **Organic synthesis:** Design scaffolds with predicted synthetic efficiency

### 4. Process Chemistry
- **Batch optimization:** Predict yields under varying conditions
- **Waste reduction:** Identify structural modifications that improve yields
- **Cost analysis:** Understand which synthetic routes are most efficient

### 5. Academic Research
- **Mechanistic understanding:** Visual attribution reveals steric effects
- **Hypothesis generation:** Identify unexpected structural factors affecting yields
- **Literature analysis:** Predict yields for reactions not yet conducted

## Insights & Implications

### Field Impact

1. **Multimodal > Single-Modal:** For chemistry problems, combining structural visualization with descriptors provides richer signals than either alone
2. **Generic models are useful:** Vision models trained on natural images transfer effectively to molecular structure visualization
3. **Interpretability via vision:** Visual modality provides more interpretable mechanistic insights than pure descriptor-based models
4. **Steric reasoning:** The model's ability to identify steric bottlenecks suggests computer vision is naturally suited to spatial chemistry problems

### Methodological Insights

1. **Cross-attention is crucial:** Simple concatenation or separate pathway would likely underperform
2. **Asymmetric importance:** Vision seems more important for identifying critical features than tabular descriptors
3. **Hierarchical learning:** Model learns chemistry-relevant hierarchies (e.g., functional group prioritization)

## Code & Resources

- **Related work:** ChemFusion (multimodal reaction prediction), other multimodal chemistry models
- **Dependencies:** PyTorch, standard vision libraries (torchvision), descriptor calculation tools
- **Data requirements:** Reaction database with known yields and molecular structures
- **Reproducibility:** 12-page paper with 4 figures should enable reproduction

## Related Work & Context

### Reaction Prediction & Yield Estimation
- Traditional QSAR models and descriptor-based approaches
- Neural reaction prediction models
- Deep learning for reaction outcome prediction

### Multimodal Learning in Chemistry
- Graph neural networks + images
- Molecule representation learning
- Foundation models for chemistry

### Vision-Language & Cross-Attention Models
- Vision-language pretraining (CLIP, BLIP)
- Cross-modal learning architectures
- Attention mechanisms in neural chemistry

## Future Research Directions

1. **Larger-scale evaluation:** Validation on diverse reaction types and chemical space
2. **Condition dependency:** Extend to predict yields under varying reaction conditions
3. **Multi-step synthesis:** Extend framework to predict overall synthesis route efficiency
4. **Comparative chemistry:** Predict relative yields across reaction variants
5. **Active learning:** Combine predictions with experimental feedback for iterative optimization
6. **Real-world deployment:** Integration into chemistry software and laboratory information systems
