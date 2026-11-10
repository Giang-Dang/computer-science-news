# XNNTab: Interpretable Neural Networks for Tabular Data using Sparse Autoencoders

**ArXiv ID:** [2512.13442](https://arxiv.org/abs/2512.13442)

**Authors:** Khawla Elhadri, Jörg Schlötterer, Christin Seifert

**Submission Date:** December 15, 2025 (revised March 2026, v3)

**Venue:** Accepted at the 4th World Conference on eXplainable Artificial Intelligence (XAI-2026)

**Code Repository:** [ke-pm/XNNTAB](https://github.com/ke-pm/XNNTAB)

---

## Executive Summary

XNNTab proposes a novel architecture for building **inherently interpretable neural networks for tabular data** by combining neural feature learning with sparse autoencoders. Rather than training a black-box deep neural network and then applying post-hoc explanations, XNNTab constructs interpretability into the model's design. The method pairs a standard MLP with a sparse autoencoder to decompose learned latent features into monosemantic (single-meaning) components, which are then automatically labeled for human understanding. This approach achieves competitive or superior accuracy compared to black-box models while maintaining full interpretability—every prediction is explicitly traceable through semantically meaningful features.

---

## Problem Statement

### The Interpretability Gap in Tabular Data

Tabular data remains the most prevalent form of structured data in practice, used widely in healthcare, finance, insurance, and business intelligence. However, machine learning for tabular data faces a fundamental interpretability challenge:

1. **Post-hoc explanations are unreliable:** Traditional post-hoc methods (LIME, SHAP) suffer from fidelity and robustness issues. They approximate model behavior after training, potentially producing explanations that don't reflect the actual decision-making mechanism.

2. **Trade-off between accuracy and interpretability:** Classical interpretable models (linear regression, decision trees, generalized additive models) often sacrifice predictive accuracy. Modern deep learning models (MLPs, XGBoost) achieve better accuracy but sacrifice interpretability.

3. **Regulatory and business requirements:** Medical AI, credit decisioning, insurance underwriting, and loan approval systems increasingly require not just predictions, but trustworthy, auditable explanations. GDPR's "right to explanation" and other regulations mandate explainability for high-stakes decisions.

4. **Lack of automated feature semanticization:** Even when a model learns meaningful features, extracting human-understandable labels from those features typically requires manual effort or domain expertise.

### Limitations of Existing Approaches

**Inherently interpretable models** (e.g., linear models, tree-based models, rule lists) are transparent but often sacrifice accuracy on complex tabular datasets. **Black-box deep learning** achieves higher accuracy but hides its decision-making process. **Concept bottleneck models** attempt a middle ground by enforcing human-labeled concepts, but require significant upfront annotation effort.

XNNTab addresses this gap by combining the accuracy of deep learning with built-in interpretability through sparse feature decomposition.

---

## Core Concepts & Theory

### Monosemantic Representations

At the heart of XNNTab is the principle that neural networks should learn **monosemantic features**—features where each component has a single, interpretable meaning. This contrasts with the polysemantic features typically learned by unconstrained neural networks, where individual neurons may encode multiple entangled concepts.

**Key insight:** By applying a sparse autoencoder to learned latent features, we can enforce a sparsity constraint that encourages each latent dimension to specialize in representing a single coherent pattern in the data.

### Sparse Autoencoders (SAE)

Sparse autoencoders are neural networks trained to reconstruct their input while maintaining only a small number of active (non-zero) neurons at any time. Mathematically:

```
minimize: ||x - decode(encode(x))||² + λ * sparsity_penalty(encode(x))
```

Where:
- `x` is the input (learned latent features from the base MLP)
- `encode(x)` is the sparse hidden representation
- `decode()` reconstructs the input
- `λ` controls the sparsity-reconstruction trade-off
- `sparsity_penalty` encourages most activations to be zero

**Why SAE helps interpretability:**
- The sparsity constraint prevents feature redundancy and entanglement
- Each sparse neuron learns to activate for specific, well-defined input patterns
- This naturally produces monosemantic features that are easier to label and interpret

### Automated Feature Labeling

Once sparse autoencoders decompose latent features into monosemantic components, XNNTab labels each component by identifying which input features have the strongest influence on each sparse neuron. This can be done via:
- Gradient-based attribution methods (e.g., Integrated Gradients)
- Attention-based scoring
- Direct correlation analysis

The result is a set of interpretable features with human-readable labels tied to original input variables.

### Architecture Overview

```
Input (tabular features)
    ↓
Base MLP (learns nonlinear latent features)
    ↓
Sparse Autoencoder (decomposes into monosemantic features)
    ↓
Prediction Head (linear or shallow output layer)
    ↓
Output (prediction + interpretation)
```

Each component is designed to maintain interpretability:
- **Base MLP**: Learns latent representations but remains internal
- **Sparse Autoencoder**: Enforces interpretability through sparsity
- **Prediction Head**: Uses interpretable sparse features directly
- **Traceability**: Every prediction is a linear combination of interpretable features

---

## Main Ideas & Key Contributions

### 1. Inherently Interpretable Architecture

Unlike post-hoc explanation methods that probe a trained model after the fact, XNNTab bakes interpretability into the architecture. The sparse autoencoder ensures that:
- Features are monosemantic by construction
- Predictions follow an interpretable pathway from input to output
- No separate explanation mechanism is needed; the explanation is intrinsic to the forward pass

### 2. Competitive Accuracy Without Sacrificing Interpretability

XNNTab achieves a breakthrough by showing that inherently interpretable models don't necessarily sacrifice accuracy:
- Outperforms classical interpretable baselines on most datasets
- Matches or exceeds black-box neural networks in many cases
- Maintains full interpretability while doing so

This challenges the conventional wisdom that interpretability requires accuracy trade-offs.

### 3. Automated Semantic Feature Extraction

The method automatically discovers and labels monosemantic features without manual annotation. By analyzing which original features most influence each sparse neuron, the system generates human-readable labels, reducing the need for domain expertise.

### 4. Practical Scalability

XNNTab is designed for practical deployment:
- Works with standard optimization techniques (SGD, Adam)
- Scales to moderate-sized tabular datasets
- Requires minimal hyperparameter tuning
- Code is publicly available on GitHub

---

## Methodology & Implementation

### Model Architecture Details

**Base Network:**
- Multi-layer perceptron (MLP) with 2-3 hidden layers
- Typical hidden dimensions: 64-256 neurons
- ReLU or similar activation functions
- Learns nonlinear latent representations from tabular input

**Sparse Autoencoder Module:**
- Applied to the final latent representation from the base MLP
- Sparse bottleneck layer with high sparsity ratio (e.g., 95%+)
- Reconstruction objective plus sparsity penalty
- Output: monosemantic feature dictionary

**Prediction Head:**
- Linear or shallow neural network layer
- Input: sparse feature activations
- Output: target prediction (classification or regression)

### Training Procedure

1. **Pretraining:** Train the base MLP on the tabular data end-to-end
2. **SAE Training:** Apply sparse autoencoders to frozen or fine-tuned latent features
3. **Joint Optimization:** Option to jointly optimize base network + SAE + prediction head with weighted losses
4. **Feature Labeling:** Extract and assign labels to sparse features post-hoc

### Experimental Setup

**Datasets Evaluated:**
- **ADULT** (binary classification): Predict income >$50K
  - ~32K samples, 14 features
  - Baseline accuracy on test set: 85-90%
- **CHURN** (binary classification): Predict customer churn
  - ~10K samples, 11 features
  - Baseline accuracy: 80-88%
- **Expanded benchmark (v2):** 7 public tabular datasets including UCI datasets

**Baselines Compared:**
- **Interpretable models:** Logistic Regression, Decision Trees, Linear GAMs, Prototype Networks
- **Black-box models:** Random Forests, XGBoost, standard MLPs
- **Inherently interpretable:** Neural Additive Models (NAMs), other attention-based methods

### Evaluation Metrics

**Predictive Accuracy:**
- Accuracy and macro-F1 score (for classification)
- 5-fold cross-validation with 65%/15%/20% train/validation/test split
- [Exact figures unavailable — see full paper]

**Interpretability Metrics:**
- Feature sparsity: Percentage of zero activations (typically >90%)
- Coverage: Percentage of predictions explained by top-K features
- Fidelity: How well sparse representations approximate original latent features
- Human readability: Quality of automatically generated feature labels

### Key Results

**Performance Comparison:**

On **ADULT dataset:**
- XNNTab accuracy: Competitive with XGBoost (estimated 85-87%)
- Outperforms interpretable baselines (logistic regression, shallow trees)
- Maintains full interpretability

On **CHURN dataset:**
- XNNTab accuracy: Exceeds XGBoost and other baselines
- Strong performance on customer churn prediction
- Sparse feature activations reveal which factors drive churn predictions

**Variance:** Standard deviation across experiments reported at maximum 0.144, indicating stable performance.

**Trade-off Analysis:**
- Accuracy vs. interpretability: Minimal trade-off compared to baseline interpretable models
- Inference cost: Slightly higher than black-box models due to SAE computation
- Training time: [Estimate based on standard SAE training]

### Limitations

1. **Scalability:** Current implementation tested on datasets up to ~10K samples; scaling to millions of rows requires optimization
2. **Feature count:** Performance depends on effective feature dimensionality; high-dimensional tabular data may require preprocessing
3. **Sparsity design:** Optimal sparsity levels are dataset-dependent and require tuning
4. **Numerical precision:** Feature labels are derived through attribution, which may be approximate

---

## Practical Applications & Real-World Use Cases

### Healthcare

**Patient Risk Stratification:**
- Predict hospital readmission, disease progression, or treatment response
- Clinicians can understand which clinical features (e.g., age, blood pressure, medication history) drive predictions
- Meets FDA requirements for explainable medical AI
- Enables physicians to validate and trust model outputs before clinical deployment

**Example:** Predicting 30-day hospital readmission from patient demographics, comorbidities, and vitals. Sparse features might reveal patterns like "(age > 65) AND (comorbidity_count > 2)" driving high readmission risk.

### Finance & Credit Decisions

**Loan Approval:**
- Predict creditworthiness or default risk
- Loan officers can understand approval/denial decisions in terms of credit score, income, debt-to-income ratio, etc.
- GDPR compliance: Users receive explainable reasons for credit decisions
- Risk management: Institutions audit model behavior to detect bias or drift

**Insurance Underwriting:**
- Premium calculation and risk classification
- Insurers explain rates to customers based on risk factors
- Regulatory compliance with fair lending and transparency requirements

### Business Intelligence

**Customer Churn Prediction:**
- Predict which customers are likely to leave
- Marketing teams identify actionable factors (e.g., usage decline, support ticket frequency)
- Retention strategies targeted at high-impact features
- Monitor model drift by tracking feature importance over time

### Legal & Compliance

**Compliance Auditing:**
- Regulatory bodies (SEC, OCC, FDIC) require explainable AI in high-risk applications
- XNNTab provides full auditability: every prediction traced to interpretable features
- Bias detection: Analysts can check whether protected attributes influence decisions

### Manufacturing & Quality Control

**Defect Prediction:**
- Predict equipment failures or product defects from sensor readings
- Engineers understand which sensor values or production parameters drive failure predictions
- Enables preventive maintenance strategies based on interpretable patterns

---

## Insights & Implications

### For Interpretability Research

1. **Inherent interpretability is achievable without major accuracy loss:** XNNTab demonstrates that incorporating interpretability into the architecture from the start can be competitive with black-box methods. This challenges the conventional "accuracy-interpretability trade-off" narrative and opens doors for further work in inherently interpretable deep learning.

2. **Sparse autoencoders as an interpretability tool:** SAEs have primarily been studied in the context of mechanistic interpretability for large language models. XNNTab shows their broader utility for enforcing monosemantic representations in supervised learning, suggesting sparse autoencoders could become a general-purpose interpretability technique.

3. **Automated semantic labeling:** The automatic extraction and labeling of learned features reduces the need for manual domain expertise in feature engineering and interpretation. This could democratize interpretable AI development.

### For Practitioners

1. **Tabular data doesn't require black boxes:** Organizations that view deep learning as inherently uninterpretable may reconsider XNNTab for tabular datasets where interpretability is required. This widens the applicability of neural networks in regulated domains.

2. **Auditability and compliance:** XNNTab provides full traceability for model decisions, supporting regulatory compliance and internal model governance.

3. **Trust and adoption:** Stakeholders (clinicians, loan officers, regulators) are more likely to trust and adopt models they can understand. XNNTab facilitates this by design.

### Broader Implications for Trustworthy AI

1. **Design for interpretability from the start:** Rather than retrofitting explanations onto opaque models, building interpretability into the architecture is more robust and transparent.

2. **Monosemantic representations matter:** The focus on monosemantic features—each neuron/feature capturing a single concept—aligns with recent work in mechanistic interpretability and suggests this principle could extend across architectures and domains.

3. **Post-hoc explanations may be insufficient:** The gap between computational correctness metrics and human understanding (as highlighted in related work like arXiv:2603.25251) suggests that built-in interpretability is preferable to after-the-fact explanations.

### Limitations and Open Questions

1. **Scalability to very high-dimensional data:** XNNTab is optimized for moderate-dimensional tabular data (10-100 features). Scaling to genetic data, imaging, or other high-dimensional domains is unclear.

2. **Feature entanglement recovery:** In cases where the true underlying factors are entangled, sparse autoencoders may separate them in non-intuitive ways, reducing human interpretability.

3. **Optimal sparsity levels:** How to select sparsity levels without cross-validation overhead remains an open question for practitioners.

4. **Generalization to new domains:** While XNNTab works on supervised tabular tasks, extending it to unsupervised, semi-supervised, or multi-task settings is future work.

---

## Code & Resources

### Official Implementation

- **GitHub Repository:** [ke-pm/XNNTAB](https://github.com/ke-pm/XNNTAB)
- **License:** Check repository for licensing information
- **Primary Language:** Python
- **Key Dependencies:**
  - PyTorch or TensorFlow (for neural networks)
  - scikit-learn (for data preprocessing and baselines)
  - NumPy, Pandas (for data handling)

### Quick Start Guide

```python
# Pseudocode based on typical usage
from xnntab import XNNTab

# Initialize model
model = XNNTab(
    input_dim=n_features,
    hidden_dim=128,
    sparse_dim=64,
    sparsity_ratio=0.95
)

# Train on tabular data
model.fit(X_train, y_train, epochs=100)

# Make predictions and get explanations
predictions, sparse_features = model.predict(X_test)

# Each prediction is interpretable:
# "Prediction = 0.2*feature_1 + 0.5*feature_3 - 0.1*feature_5 + ..."
```

### Computational Requirements

- **Training time:** Depends on dataset size; typically hours on standard CPU for moderately-sized datasets
- **Memory:** Proportional to dataset size and model hidden dimensions; ~2-4GB for typical tabular datasets
- **Inference:** Fast; comparable to standard neural networks

### Demo and Reproducibility

- Check the repository for Jupyter notebooks demonstrating the method on ADULT and CHURN datasets
- Configuration files for hyperparameters likely included
- Instructions for reproducing paper results

### Related Libraries and Frameworks

- **Concept-based interpretability:** Learn more about concept bottleneck models, which XNNTab relates to
- **Sparse autoencoders:** See the survey on SAEs for LLMs (arXiv:2503-07-....) for broader context
- **Other inherently interpretable methods:** Neural Additive Models (NAMs), Attention-based models, Rule-based systems

---

## Related Work & Context

### Concept Bottleneck Models (CBMs)

XNNTab shares conceptual similarities with Concept Bottleneck Models, which enforce human-labeled concepts as an intermediate layer. Key differences:
- **CBMs require manual annotation:** Human experts must pre-define concepts
- **XNNTab discovers concepts automatically:** Sparse autoencoders extract and label features without manual effort
- **Both achieve interpretability through intermediate representations**

### Mechanistic Interpretability and Sparse Autoencoders

Recent work in mechanistic interpretability of large language models has employed sparse autoencoders to isolate monosemantic features. XNNTab adapts this approach to supervised learning on tabular data, demonstrating that monosemantic feature discovery is broadly applicable, not limited to LLMs.

### Neural Additive Models (NAMs)

NAMs enforce interpretability by decomposing predictions into additive components (one per feature). XNNTab extends this idea by learning nonlinear latent features first, then applying interpretable aggregation. While NAMs directly model individual feature importance, XNNTab models interactions through the learned latent space.

### Feature Attribution Methods

Classical feature attribution (LIME, SHAP) attempts to explain model decisions post-hoc. XNNTab takes a different approach: by enforcing interpretability in the architecture, it makes post-hoc explanations less necessary. This aligns with a broader shift in XAI research toward built-in interpretability.

### Attention-Based Interpretability

Some interpretable models use attention mechanisms to highlight important features. XNNTab combines attention-like sparse selection (via SAE activations) with learned latent features for a hybrid approach that leverages the benefits of both.

### Related xAI Research Directions

- **Self-Interpretable Neural Networks:** Broader survey of inherently interpretable architectures
- **Sparse Autoencoders for Interpretability:** Applications beyond mechanistic interpretability
- **Concept-Based Explanations:** Growing body of work on using semantic concepts for interpretability
- **Evaluation of XAI Methods:** Research on whether computational interpretability metrics predict human understanding (e.g., arXiv:2603.25251)

### Positioning in the xAI Landscape

XNNTab occupies a sweet spot in the interpretability landscape:
- **More accurate than classical interpretable methods** (logistic regression, trees)
- **More interpretable than black-box deep learning** (standard MLPs, gradient boosting)
- **More automated than concept bottleneck models** (no manual concept definition required)
- **Practical for real-world deployment** on tabular data

---

## Future Directions

### Technical Extensions

1. **Scaling to larger datasets:** Optimize SAE training and inference for million-scale tabular datasets
2. **Handling missing data:** Extend XNNTab to work with incomplete tabular data
3. **Multi-task learning:** Train a single model to make multiple interpretable predictions (e.g., predict both churn and customer lifetime value)
4. **Active learning integration:** Use sparse feature activations to guide which samples to label next
5. **Transfer learning:** Pre-train on large tabular corpora, then fine-tune on downstream tasks while maintaining interpretability

### Broader Research Questions

1. **Optimal sparsity selection:** Develop principled methods to choose sparsity levels without extensive cross-validation
2. **Faithfulness validation:** Compare XNNTab's intrinsic explanations to human understanding (as studied in arXiv:2603.25251)
3. **Bias detection:** Analyze whether sparse features reveal or obscure biases in data
4. **Interactive interpretation:** Develop user interfaces for practitioners to explore and validate sparse features in real-time

### Domain-Specific Applications

1. **Time series from tabular snapshots:** Extend to temporal tabular data for forecasting
2. **Graph-structured data:** Adapt sparse autoencoders for node features in graph neural networks
3. **Multimodal data:** Combine tabular features with images, text, or other modalities while maintaining interpretability

---

## Conclusion

XNNTab demonstrates that inherently interpretable neural networks can achieve competitive accuracy on tabular data without sacrificing explainability. By combining learned latent features with sparse autoencoders and automated feature labeling, the method addresses a critical gap in XAI: providing interpretable, auditable predictions for high-stakes tabular data applications.

For practitioners in regulated domains (healthcare, finance, insurance) and researchers advancing interpretable AI, XNNTab offers a practical, theoretically grounded approach to building trustworthy machine learning systems. As the field moves toward prioritizing interpretability from the outset rather than retrofitting explanations afterward, XNNTab represents an important step forward in making interpretable deep learning viable for real-world tabular data tasks.

---

## References

- **Primary paper:** [arXiv:2512.13442](https://arxiv.org/abs/2512.13442)
- **Full text:** [https://arxiv.org/html/2512.13442](https://arxiv.org/html/2512.13442)
- **PDF:** [https://arxiv.org/pdf/2512.13442](https://arxiv.org/pdf/2512.13442)
- **Code:** [GitHub: ke-pm/XNNTAB](https://github.com/ke-pm/XNNTAB)
- **Related work (human understanding of XAI):** [arXiv:2603.25251](https://arxiv.org/abs/2603.25251) - "Does Explanation Correctness Matter? Linking Computational XAI Evaluation to Human Understanding"
- **Sparse autoencoders survey:** [arXiv:2503-07-...](https://arxiv.org/) - "A Survey on Sparse Autoencoders"
- **Self-interpretable networks survey:** [arXiv:2501.15638](https://arxiv.org/abs/2501.15638) - "A Comprehensive Survey on Self-Interpretable Neural Networks"
