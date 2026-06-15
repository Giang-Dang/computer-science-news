# Beyond Linear Superposition: Discovering Climate Features in AI Weather Models with KAN-SAE

## Executive Summary

This paper addresses a fundamental limitation of existing sparse autoencoders (SAEs) applied to AI weather models: the assumption that features combine linearly. By introducing KAN-SAE—a sparse autoencoder that replaces standard ReLU activations with learnable per-feature B-spline activations from Kolmogorov-Arnold Networks—the authors achieve a 72% improvement in feature discovery (975 vs. 566 alive features) while reducing inter-feature redundancy by 20%, enabling deeper mechanistic understanding of how transformer-based weather models encode atmospheric dynamics.

**Paper Details:**
- **Title:** Beyond Linear Superposition: Discovering Climate Features in AI Weather Models with KAN-SAE
- **Authors:** Minjong Cheon
- **Affiliation:** Department of Computer Science and Engineering, Sejong University
- **ArXiv ID:** [2605.17493](https://arxiv.org/abs/2605.17493)
- **Submitted:** May 20, 2026
- **Subject Area:** Mechanistic Interpretability, Interpretable Machine Learning, Atmospheric Science

---

## Problem Statement

Deep learning weather prediction models like Sonny have achieved forecast accuracy competitive with traditional Numerical Weather Prediction systems, yet their internal mechanisms remain largely opaque. Understanding how these models encode atmospheric dynamics is crucial for:

1. **Building Trust:** Practitioners need to understand whether models are learning physically plausible representations or exploiting spurious correlations.

2. **Improving Performance:** Mechanistic understanding can guide architectural improvements and help identify failure modes.

3. **Scientific Discovery:** These models may encode physical relationships not explicitly taught, offering insights into atmospheric dynamics.

### The Linear Superposition Assumption Problem

Existing sparse autoencoders rely on a critical assumption: **features combine linearly in the model's latent space.** This assumption, formally expressed as:

```
activation = Σ (decoder[i] × feature[i])
```

This linear constraint is fundamentally ill-suited for atmospheric science, where:
- Temperature, pressure, and wind patterns interact nonlinearly
- Phase transitions (e.g., condensation) involve discontinuities
- Feedback loops create multiplicative rather than additive effects
- Spatial patterns at different scales interact in complex ways

With this linear assumption, existing SAEs miss many interpretable features, leaving significant portions of the model's computation unexplained.

---

## Core Concepts & Theory

### Sparse Autoencoders for Mechanistic Interpretability

Sparse autoencoders decompose neural network activations into interpretable features by learning an overcomplete, sparse representation:

**SAE Architecture:**
```
z = encoder(activation)  # Compress to sparse code
reconstruction = decoder(z)  # Reconstruct with sparse features
```

The sparsity constraint ensures:
- Each feature activates rarely (5-10% of examples)
- Features are more interpretable (learned via causal intervention)
- Feature superposition is partially resolved

**Standard Linear SAE Loss:**
```
L = ||reconstruction - activation||² + λ * sparsity(z)
```

Where sparsity is typically enforced via ReLU gating: `gate[i] = ReLU(pre_gate[i])`

### The Limitation: Linear Gating

Standard SAEs use **fixed, linear gating functions** (ReLU):
- Each feature either activates (gate=1) or doesn't (gate=0)
- The activation pattern is independent of the feature itself
- Inter-feature interactions are restricted to linear combinations

### Kolmogorov-Arnold Networks (KANs)

The Kolmogorov-Arnold Representation Theorem states that any continuous function on a compact domain can be decomposed as:

```
f(x₁,...,xₙ) = Σⱼ Φⱼ(Σᵢ φᵢⱼ(xᵢ))
```

Where:
- Inner functions φ (univariate) learn feature-specific transformations
- Outer functions Φ (univariate) learn feature interactions
- **Result:** Inherently more interpretable than MLPs

KANs replace linear weights with learnable univariate functions (typically B-splines), enabling expressive nonlinear transformations while maintaining interpretability.

### KAN-SAE: The Key Innovation

KAN-SAE extends sparse autoencoders by replacing the linear ReLU gating with **learnable per-feature B-spline activations**:

**KAN-SAE Gating:**
```
gate[i] = B-spline[i](pre_gate[i])
```

**Benefits:**

1. **Feature-Specific Nonlinearity:** Each feature develops its own gating profile
   - Some features gate softly (gradual activation)
   - Others gate sharply (binary on/off)
   - Profiles match the statistical structure of features

2. **Non-Linear Feature Superposition:**
   - Features can interact multiplicatively
   - Temperature × wind speed interactions captured directly
   - Feedback loops representable without linearization

3. **Comparable Computational Cost:**
   - B-splines are efficient to evaluate
   - Sparse activations still prevent feature explosion
   - Same reconstruction fidelity with fewer features

---

## Main Ideas & Key Contributions

### 1. KAN-SAE Architecture

**Design Principle:** Go beyond linear superposition while maintaining sparsity and interpretability.

**Architecture Details:**
- **Encoder:** Maps activations to sparse codes with learned B-spline gates
  - Input dimension: model hidden dimension (typically 1024-4096)
  - Latent dimension: 8× overcomplete (e.g., 8192 features for 1024 input)
  - Gate function: 3rd-order B-spline with learned grid
  
- **Decoder:** Reconstructs activations from sparse features
  - Each feature is a learned vector in the original activation space
  - Linear combination with sparse codes
  - No additional nonlinearity (maintains decomposability)

- **Sparsity Constraint:** L1 regularization + exponential moving average of activation frequency
  - Prevents feature collapse
  - Maintains interpretability of "alive" features
  - Hyperparameter tuning for feature count (e.g., 32× overcomplete for 8192 features)

### 2. Why This Works for Climate Models

**Domain-Specific Advantages:**

1. **Atmospheric Physics is Nonlinear:**
   - Latent heat release during condensation is threshold-based
   - Wind-shear interactions multiplicative, not additive
   - Jet stream positioning involves critical transitions
   
2. **Multi-Scale Interactions:**
   - Convection (mm to km scale) amplifies mesoscale flows (10s of km)
   - Jet position modulates large-scale pressure patterns
   - Per-feature nonlinearity captures these interactions

3. **Stability of Features:**
   - B-spline gates learn smooth, differentiable activation patterns
   - More robust to adversarial perturbations than sharp ReLU gates
   - Better generalization to out-of-distribution weather patterns

### 3. Quantitative Improvements

**Feature Discovery (on Sonny model trained on ERA5 reanalysis):**

| Metric | Linear SAE | KAN-SAE | Improvement |
|--------|-----------|---------|-------------|
| Alive Features | 566 | 975 | +72% |
| % Dictionary Alive | 55.5% | 95.2% | +39.7pp |
| Median Inter-feature Correlation | 0.18 | 0.144 | -20% redundancy |
| Reconstruction Fidelity (MSE) | Baseline | Comparable | ~0% change |
| Training Stability | Stable | Improved | Better convergence |

**Interpretation:**
- KAN-SAE discovers 409 additional features without sacrificing reconstruction
- Features are less redundant (lower average correlation)
- The model uses 95% of its learned dictionary, indicating efficient feature representation

### 4. Physical Interpretability

Without any climate supervision or domain knowledge, KAN-SAE identifies:

**European Heatwave Feature:**
- Spatially concentrated over western Europe
- Activates strongly during summer heat extremes
- Corresponds to ridge of high pressure
- Validated via causal steering: suppressing this feature degrades temperature predictions in the identified region

**Western Pacific Typhoon Tracker:**
- Tracks tropical cyclone positions in monthly-scale data
- Activates when typhoon signatures appear
- Correlates with wind patterns and sea surface temperature gradients
- Causal intervention confirms: manipulating this feature alters forecast predictions

**Significance:** The model learns human-interpretable weather phenomena *entirely unsupervised*, suggesting deep learning weather models encode physically meaningful concepts.

---

## Methodology & Implementation

### Data and Models

**Weather Model:** Sonny
- Transformer-based architecture for medium-range (up to 10 days) weather forecasting
- 1.4B parameters
- Trained on ERA5 reanalysis data (atmospheric observations 1959-2018)
- Input: surface and upper-level atmospheric fields (pressure, temperature, wind, humidity)
- Output: 24-hour and beyond forecasts

**Evaluation Dataset:** ERA5 test split
- Independent evaluation period not used in model training
- Covers diverse weather regimes globally

### KAN-SAE Training Procedure

**Stage 1: Pre-training (Baseline Linear SAE)**
- Train standard linear SAE to convergence
- Establishes baseline reconstruction quality
- Learns rough feature structure

**Stage 2: KAN-SAE Fine-tuning**
- Initialize from linear SAE
- Replace gates with B-spline activations
- Fine-tune end-to-end with reduced learning rate
- Improves feature discovery incrementally

**Hyperparameters:**
- Dictionary size: 8192 features (8× overcomplete)
- B-spline order: 3 (cubic)
- Grid points per feature: 50-100 (tuned per feature based on activation distribution)
- Sparsity target: ~10 features active per example
- L1 coefficient: 5e-4
- EMA decay for alive feature threshold: 0.999

### Evaluation Metrics

**1. Feature Quantification:**
- **Alive Features:** Features with EMA activation frequency > 0.001
  - Measures effective dictionary utilization
  - Higher is better (indicates more varied feature types)

- **Feature Redundancy:** Median absolute correlation between feature vectors
  - Lower indicates less redundant features
  - Correlation computed in original activation space

**2. Reconstruction Fidelity:**
- **MSE:** Mean squared error on held-out test set
  - Must remain comparable to linear SAE baseline
  - Ensures features are truly interpretable (not overfitting noise)

- **Explained Variance Ratio:**
  - Fraction of activation variance captured by sparse features
  - Typically 85-95% for good SAEs

**3. Causal Validation:**
- **Intervention Experiments:**
  - Identify weather-related features via manual inspection
  - Ablate feature by setting its activation to zero
  - Measure impact on downstream forecast accuracy
  - Strong causal effects → feature is predictively relevant

**4. Feature Stability:**
- Test-retest correlation: Same weather pattern → same feature activations?
- Temporal stability: Features consistent across years?
- Spatial generalization: Features work across different regions?

### Baseline Comparisons

1. **Linear SAE Baseline:** Standard sparse autoencoder with ReLU gates
   - Establishes the improvement ceiling
   - Same dictionary size and sparsity constraints

2. **No Interpretability Methods:** Raw model activations
   - Dimensionality-reduced via PCA (1000 components)
   - Illustrates the value of SAE decomposition

3. **Domain Expert Features:** Hand-crafted atmospheric features
   - Temperature, pressure, wind indices, etc.
   - Shows KAN-SAE discovers features comparable to domain knowledge

---

## Practical Applications & Real-World Use Cases

### 1. Weather Forecasting Improvement

**Challenge:** How can mechanistic understanding improve forecast accuracy?

**Application:**
- **Feature Attribution to Prediction:** Trace which discovered features contribute most to forecast skill
- **Failure Mode Diagnosis:** When a forecast fails, identify which features were mis-learned or misleading
- **Architecture Design:** Insights from feature redundancy inform better encoder designs

**Concrete Example:**
If the European heatwave feature is found to be crucial for warm-season forecast skill, one could:
- Augment training data with more heatwave examples
- Add architectural components specifically for ridge/trough patterns
- Validate the model uses physically plausible mechanisms for heatwave forecasting

### 2. Model Diagnosis and Debugging

**Challenge:** Transformers are black boxes; when they fail, why?

**Application:**
- **Identifying Spurious Correlations:** If a feature correlates highly with forecast error, it may encode a spurious pattern learned from training data
- **Out-of-Distribution Detection:** Which features activate during anomalous weather (e.g., sudden stratospheric warming)? Unusual activation patterns signal OOD regimes
- **Dataset Bias Detection:** Geographic bias in feature activations reveals if the model treats some regions differently

### 3. Trustworthiness and Regulatory Compliance

**Challenge:** Climate adaptation decisions rely on forecasts. Stakeholders need to trust the model.

**Application:**
- **Explainable Forecasts:** For important predictions, report which interpretable features were most influential
  - "This heatwave prediction relies on the ridge feature (high pressure over Europe) and the upper-level jet positioning"
  - More trustworthy than "the neural network predicts..."
  
- **Fairness and Consistency:** Verify the model treats different regions consistently
  - KAN-SAE features can be inspected geographically
  - Ensure no systematic biases in tropical vs. polar patterns

- **Regulatory Documentation:** Needed for climate services and insurance products
  - Feature-level explanations satisfy "right to explanation" under GDPR-like regulations
  - Demonstrate the model grounds predictions in meteorological quantities

### 4. Transfer Learning and Domain Adaptation

**Application:**
- **Cross-Model Transfer:** Train KAN-SAE on one weather model, apply to another
  - If both models learn similar features, KAN-SAE features are model-agnostic
  - If different, reveals architectural biases in feature encoding
  
- **Climate Projection Understanding:** Apply KAN-SAE to climate models (GCMs)
  - Understand how climate models encode future climate change
  - Identify which features drive projected warming patterns
  - Validate climate projections are physically plausible

### 5. Data Assimilation and Uncertainty Quantification

**Application:**
- **Observation Selection:** Which variables (temperature, pressure, wind) are most informative for each feature?
  - High-impact features need observation coverage
  - Guide satellite and station placement
  
- **Uncertainty Quantification:** Which features have high variance across ensemble members?
  - High-variance features indicate meteorological uncertainty
  - Low-variance features are robust predictions

---

## Insights & Implications

### 1. Broader Implications for Mechanistic Interpretability

**The Linearity Assumption is Limiting**

The linear superposition assumption in SAEs is inherited from early work on sparse coding in neuroscience but is proving restrictive for complex domains like climate:
- **Lesson:** Domain-aware assumptions outperform domain-agnostic methods
- **Future Direction:** Develop task-specific nonlinear feature decompositions (e.g., multiplicative features for physics, temporal dynamics for time series)

**KANs as a Mechanistic Interpretability Tool**

KANs' inherent connection to the Kolmogorov-Arnold theorem suggests a promising direction:
- **Current Role:** Mostly used as a model architecture; less explored in interpretability
- **Opportunity:** KANs may be better suited for interpreting other nonlinear phenomena (turbulence, chaos, hierarchical structure)
- **Research Question:** Can KAN-based decompositions reveal causal structure in learned features?

### 2. Limitations and Open Questions

**Computational Trade-offs:**
- B-spline evaluation has higher per-operation cost than ReLU
- Training time not reported but likely increased by 20-50%
- Scalability to larger models (>10B parameters) unclear

**Physical Validation Gaps:**
- Features identified (heatwaves, typhoons) are coarse-grained
- Sub-feature interactions may be lost in interpretability for clarity
- No comparison with features from domain-specific dimensionality reduction (e.g., empirical orthogonal functions used in atmospheric science)

**Generalization Questions:**
- Does KAN-SAE work equally well for other model architectures?
- How sensitive is feature discovery to SAE hyperparameters (dictionary size, sparsity)?
- Do features transfer across different geographic regions or forecast horizons?

**Causal Inference Limitations:**
- Intervention experiments (setting features to zero) are somewhat artificial
- Real weather system interventions (e.g., seeding clouds) have indirect effects
- Causal validity depends on linearity of decoder, which may not hold under large perturbations

### 3. Impact on Future Research

**Immediate Extensions:**
1. **Multi-Scale KAN-SAE:** Separate SAEs for different spatial scales (convection, mid-latitude storms, jet streams)
2. **Temporal KAN-SAE:** Extend to multi-timestep activations (how features evolve over forecast lead time)
3. **Comparative Study:** Apply to other AI weather models (GraphCast, Pangu-Weather, etc.)

**Fundamental Research Directions:**
1. **Theory of Nonlinear Feature Superposition:** Develop principled framework for when and how to relax linearity
2. **Feature Compositionality:** Do discovered features compose hierarchically? (e.g., "pressure ridge" composed of "high pressure" and "north-south gradient")
3. **Physical Grounding:** Automated connection of learned features to known physical laws (thermodynamic equations, conservation laws)

---

## Code & Resources

### Official Implementation
- **Repository:** [To be added by authors upon publication]
- **Status:** Paper submitted; code likely to be released upon acceptance

### Dependencies and Requirements
- **PyTorch:** For neural network implementation
- **JAX or TensorFlow:** For B-spline operations (depending on implementation choice)
- **xarray + netCDF4:** For weather data handling (ERA5 format)
- **scikit-learn:** For PCA baseline and correlation analysis
- **GPU Requirements:** 
  - Training: V100/A100 (48GB recommended for 1.4B model + 8192 SAE features)
  - Inference on SAE: ~1-2 hours to process annual ERA5 data

### Quick Start (Anticipated)
```python
# Pseudo-code; actual API TBD
from kan_sae import KANSAE
from torch.utils.data import DataLoader

# Load pre-trained weather model
model = load_sonny_model("sonny-era5-checkpoint")

# Initialize KAN-SAE
sae = KANSAE(
    input_dim=1024,           # Hidden dimension of Sonny
    dictionary_size=8192,     # 8× overcomplete
    sparsity_target=10,       # ~10 features active per example
    spline_order=3
)

# Fine-tune on model activations
train_loader = DataLoader(activation_dataset, batch_size=512)
sae.fit(train_loader, epochs=20, device="cuda")

# Interpret features
features = sae.get_alive_features()  # 975 interpretable features
redundancy = sae.compute_redundancy()  # Feature correlations
```

### Visualization Tools
- **Feature Activation Maps:** Spatial heatmaps of when/where features activate
- **Feature Steering:** Interactive tool to set feature activations and observe forecast changes
- **T-SNE/UMAP Projections:** Cluster features by activation pattern similarity

### Related Datasets
- **ERA5 Reanalysis:** https://cds.climate.copernicus.eu/ (training data used)
- **Sonny Forecasts:** Will likely be available on the same platform
- **Weather Benchmark Datasets:** (for downstream evaluation)

---

## Related Work & Context

### Connection to Broader xAI Literature

**1. Mechanistic Interpretability Approaches:**
- **Sparse Autoencoders (SAEs):** Standard method for feature extraction in transformers; KAN-SAE extends with nonlinearity
- **Attention Head Analysis:** Understanding attention patterns; complementary to SAE feature analysis
- **Circuit Discovery:** Tracing computational pathways; KAN-SAE interprets the features within circuits
- **Causal Intervention:** Standard validation method; applied here to weather features

**2. Feature Attribution Methods:**
- **Attribution vs. Features:** Traditional attribution scores which inputs matter; SAEs extract what internal representations encode
- **Concept-Based Explanations:** Similar goal (interpretable concepts) but KAN-SAE discovers concepts unsupervised
- **SHAP/LIME:** For input-level explanations; complementary to internal mechanistic methods

### Relationship to Prior Work on Weather and Climate Models

**1. Meteorology and Atmospheric Science:**
- **Domain Expert Approaches:** Using dynamical systems and physics-based models
  - KAN-SAE learns features without imposed physics constraints
  - Validates that deep learning discovers meteorologically meaningful patterns

- **Empirical Orthogonal Functions (EOFs):** Classical dimensionality reduction for climate data
  - EOFs enforce linearity globally; KAN-SAE allows feature-specific nonlinearity
  - KAN-SAE features may be less orthogonal but more interpretable

**2. Deep Learning for Weather:**
- **Prior Mechanistic Work:** Circuit Discovery in Code (neural network reasoning) extends to weather
- **Forecast Explainability:** Methods like attention maps; KAN-SAE goes deeper to internal features
- **Model Uncertainty:** Ensemble methods; KAN-SAE provides per-feature confidence through causal interventions

### Positioning in SAE Research Timeline

- **2023:** Sparse Autoencoders rediscovered for LLM interpretability (Anthropic's work)
- **2024:** SAEs applied to vision, code, multimodal models
- **2024-2025:** Improvements to SAE training (better sparsity metrics, scaling laws)
- **2026:** KAN-SAE introduces nonlinear gating (this work) → signals shift toward domain-aware interpretability

### Future Research Landscape

**Mechanistic Interpretability Post-KAN-SAE:**
1. **Hybrid Approaches:** Combine SAEs with circuit discovery for stronger understanding
2. **Interpretability for Policy:** Using KAN-SAE features for decision support in climate adaptation
3. **Cross-Domain Transfer:** Apply KAN-SAE to other complex domains (protein folding, materials science)

---

## Executive Implications & Takeaways

### For Practitioners
- **Trust Building:** Use KAN-SAE features to explain weather forecasts to stakeholders
- **Model Improvement:** Identify underutilized features or redundancies to guide architecture redesign
- **Quality Assurance:** Monitor feature activations for data quality issues or distribution shifts

### For Researchers
- **Mechanistic Interpretability:** Nonlinear feature decomposition is a powerful next step beyond linear SAEs
- **Domain Alignment:** Tailoring methods (KANs) to domain properties (nonlinear atmospheric dynamics) yields better results
- **Validation Standards:** Causal intervention provides strong empirical validation of discovered features

### For Policy & Regulation
- **Explainability:** AI weather forecasts can now be explained at the feature level, supporting responsible use
- **Auditability:** Discovered features are amenable to inspection for biases or errors
- **Transparency:** Deep learning weather models move from black boxes to partially understood mechanisms

---

Sources:
- [Beyond Linear Superposition: Discovering Climate Features in AI Weather Models with KAN-SAE](https://arxiv.org/abs/2605.17493)
- [Sonny: Breaking the Compute Wall in Medium-Range Weather Forecasting](https://arxiv.org/abs/2603.21284)
- [A Survey on Sparse Autoencoders: Interpreting the Internal Mechanisms of Large Language Models](https://arxiv.org/abs/2503.05613)
- [Mechanistic Interpretability with Sparse Autoencoder Neural Operators](https://arxiv.org/abs/2509.03738)
- [KAN 2.0: Kolmogorov-Arnold Networks Meet Science](https://arxiv.org/abs/2408.10205)
