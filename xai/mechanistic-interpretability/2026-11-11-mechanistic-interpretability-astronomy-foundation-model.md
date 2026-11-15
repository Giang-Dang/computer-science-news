# A Mechanistic Interpretability Study of an Astronomy Foundation Model

**ArXiv ID:** [2611.15653](https://arxiv.org/abs/2611.15653)

**Authors:** Rachel C. Zhang, Alberto Bietti, Wes Gurnee, Alessandro Favero, Miles Cranmer

**Submitted:** November 11, 2026 | **Accepted:** NeurIPS 2026

**Status:** Oral presentation at NeurIPS 2026 Workshop on Interpretability for Discovery

---

## Executive Summary

This paper presents the first causal mechanistic interpretability study of an astronomy foundation model (AION-1), investigating why combining imaging data with photometric data improves redshift prediction accuracy. By applying sparse autoencoders (SAEs) and causal intervention analysis to the model's internal representations, the authors localize the source of multimodal advantage, reveal that linear decodability does not imply causal importance, and demonstrate that astronomy provides a unique setting for interpretability research due to the availability of ground-truth physical measurements.

---

## Problem Statement

Despite the growing adoption of foundation models in astronomy, there is limited understanding of how these models combine different data modalities (imaging, spectroscopy, photometry) to make predictions. Previous interpretability work on neural networks has focused on domains like vision or language, where ground truth is less accessible. The key questions this paper addresses are:

1. **Why does multimodal information help?** When AION-1 combines imaging with photometry for redshift prediction, where does the performance gain originate in the network?
2. **How reliable are existing interpretability signals?** Can linear decodability from a layer predict the causal importance of that layer's representations?
3. **How can astronomy-specific domain knowledge improve interpretability analysis?** Astronomy has verifiable physical properties (e.g., galaxy characteristics) that can ground interpretability claims.

Prior work on foundation models has focused on scaling and task performance, but mechanistic understanding of how foundation models process multimodal astronomical data is largely absent. This gap limits our ability to understand model failure modes, improve training, and build trustworthy systems for scientific discovery.

---

## Core Concepts & Theory

### Sparse Autoencoders (SAEs)

SAEs are a key tool for decomposing the polysemantic (multiply-meaning) nature of neurons in deep neural networks. In AION-1's case, individual neurons may respond to multiple distinct features or concepts. By training an autoencoder on the activations of a specific layer, the authors learn a sparse dictionary of interpretable features:

- The SAE maps high-dimensional neuron activations to a lower-dimensional sparse code.
- Each dimension of the sparse code represents a distinct "feature" that may be more interpretable than individual neurons.
- Sparsity encourages each dimension to activate only when a specific pattern is present in the input.

### Causal Intervention Analysis

To move beyond correlation to causality, the authors use causal intervention (ablation/patching) techniques:

- **Direct intervention:** Modify specific latent codes or activations and observe downstream effects on model output.
- **Comparison with passive observation:** Show that features that can be linearly decoded from a layer's activations don't necessarily have causal effects on the model's predictions.
- **Counterfactual analysis:** Perform targeted edits to images (e.g., removing dust, adjusting brightness) and measure the causal chain through the model.

### Information vs. Causality Trade-off

A central finding is that **information content ≠ causal importance**. A layer may contain decodable information about a feature, but that information may not be used by the model for prediction. This distinction is crucial for mechanistic interpretability and reveals that standard linear probing (reading information from activations) provides an incomplete picture of model computation.

---

## Main Ideas & Key Contributions

### 1. Localization of Multimodal Advantage

The paper's primary contribution is pinpointing where AION-1 gains predictive advantage from combining imaging and photometry:

- **First encoder block concentration:** Most of the multimodal advantage for redshift prediction is localized to the first encoder block of the model.
- **Spatial extended and dust-attenuated galaxies:** The improvement is concentrated in specific galaxy populations (spatially extended, dust-attenuated sources) rather than being uniform across all objects.
- **Quantified improvement:** The paper provides estimates of contribution magnitudes, allowing researchers to understand which parts of the model drive which improvements.

### 2. Linear Decodability ≠ Causal Importance

The study reveals an important caveat for mechanistic interpretability work:

- One attention head's output in a specific layer can be **linearly decoded** to predict the multimodal advantage.
- However, **causal interventions** on this head show **negligible impact** on redshift predictions.
- This decoupling means that naive interpretability techniques (linear probing, attention visualization) can mislead us about model computation.
- Implication: Causal methods are necessary for rigorous mechanistic interpretability.

### 3. Astronomy as a Testbed for Interpretability

The paper positions astronomy as a uniquely valuable domain for interpretability research:

- **Ground truth availability:** Unlike vision classification (ImageNet) or language tasks (GLUE), astronomy has physical measurements that ground interpretability claims. Redshift, stellar mass, dust extinction, and galaxy morphology are measurable quantities.
- **Multimodal nature:** Different observational modalities (imaging, spectroscopy, photometry) offer natural interventions and ablations.
- **Scientific motivation:** Interpretability insights can directly improve scientific discovery and our understanding of astronomical phenomena.

---

## Methodology & Implementation

### Model and Setup

- **Foundation Model:** AION-1 (base variant), approximately 300 million parameters.
- **Architecture:** AION-1 uses modality-specific tokenization (images, photometry, spectra) followed by transformer-based masked modeling.
- **Task:** Multimodal redshift prediction (photometry alone vs. photometry + imaging).
- **Baseline Performance:** Photometry alone provides a baseline redshift prediction; adding imaging improves predictions.

### Analytical Procedure

1. **Sparse Autoencoder Training:**
   - Train SAEs on frozen AION-1 encoder activations for each layer.
   - Learn sparse dictionaries of features from the high-dimensional neuron activations.
   - Typical SAE dimensions: learned features numbering in the hundreds.

2. **Causal Intervention:**
   - Perform ablation experiments by zeroing out or perturbing specific latent codes.
   - Measure changes in model redshift output.
   - Compare information (via linear probing) with causality (via intervention).

3. **Counterfactual Image Edits:**
   - Generate synthetic variations of input images (e.g., dust removal, brightness adjustment).
   - Trace how these edits propagate through the model's internal representations.
   - Correlate internal feature activations with observable physical phenomena.

4. **Galaxy Population Analysis:**
   - Stratify results by galaxy properties (dust attenuation, size, morphology).
   - Show that multimodal advantage is heterogeneous across galaxy populations.

### Datasets and Evaluation Metrics

- **Data source:** Legacy Survey photometry and imaging data used for AION-1 pretraining.
- **Evaluation metrics:**
  - Redshift prediction error (quantitative)
  - Feature activation correlation with physical galaxy properties (qualitative validation)
  - Causal effect size of individual features on redshift output
  - Information content vs. causal importance comparison
- **Validation:** Results validated against known astronomy domain knowledge (e.g., dust attenuation is known to affect imaging).

---

## Practical Applications & Real-World Use Cases

### 1. Foundation Model Auditing

Mechanistic interpretability provides a systematic way to audit foundation models before deployment:

- **Understanding failure modes:** By localizing which parts of the model are responsible for specific predictions, researchers can identify where the model may fail (e.g., on specific galaxy populations).
- **Debugging multimodal fusion:** Understanding how different data modalities are combined helps improve model design and training.

### 2. Improving Model Training and Architecture

Interpretability insights can directly improve model development:

- **Feature importance for training:** Identifying which features drive predictions informs data collection and preprocessing priorities.
- **Architecture optimization:** Knowledge about where multimodal information is most useful can guide architectural choices (e.g., which transformer blocks should receive multimodal inputs).

### 3. Scientific Discovery

Mechanistic interpretability can enhance astronomical research:

- **Galaxy population studies:** Understanding which properties of galaxies drive multimodal advantage improves our understanding of galaxy physics and observational limitations.
- **Optimal observational strategy:** By understanding what imaging adds over photometry, astronomers can design more efficient observation campaigns.
- **Cross-domain transfer:** Insights about multimodal fusion in astronomy may transfer to other scientific domains (medicine, climate science, etc.).

### 4. Regulatory and Trustworthiness Implications

- **AI Act compliance:** Understanding how high-stakes foundation models make decisions is critical for compliance with AI regulations.
- **Scientific reproducibility:** Mechanistic interpretability supports reproducible science by clarifying model decision-making.
- **Astronomer-in-the-loop systems:** By making foundation models more interpretable, we can build systems where astronomers understand and can override model decisions.

---

## Insights & Implications

### Theoretical Insights

1. **Linear decodability is insufficient for causality:** This finding has implications for all mechanistic interpretability work, suggesting that linear probing and attention visualization need to be validated with causal methods.

2. **Heterogeneous effects across data:** The multimodal advantage is not uniform; specific galaxy populations benefit more from imaging. This suggests that foundation models learn dataset-specific patterns that generalize differently across domains.

3. **Sparse features as interpretability primitives:** SAEs successfully decompose AION-1's representations into interpretable features, validating SAEs as a general tool for foundation model interpretability.

### Practical Implications

1. **Avoid false confidence in linear probing:** Researchers should combine linear decodability analysis with causal interventions to avoid misleading conclusions about model computation.

2. **Domain-specific interpretability settings are valuable:** Astronomy's ground-truth measurements make it an exceptional testbed. Similar opportunities may exist in medical imaging, materials science, and other domains with measurable outcomes.

3. **Multimodal fusion is interpretable:** Rather than treating multimodal foundation models as black boxes, mechanistic interpretability can provide insights into how different modalities are combined.

### Open Questions and Future Work

1. **Generalization to larger models:** Does the localization of multimodal advantage hold for larger AION-L and AION-XL models?

2. **Causal directions:** What is the causal direction of information flow? Is imaging information fused early (first encoder block) or does it influence later layers?

3. **Transfer learning:** Do the interpretable features learned from AION-1 transfer to other astronomy foundation models or to other domains?

4. **Robustness of SAE decomposition:** How sensitive are the learned sparse features to SAE hyperparameters (sparsity coefficient, dictionary size)?

---

## Code & Resources

- **Primary paper:** [arXiv:2611.15653](https://arxiv.org/abs/2611.15653)
- **Full PDF:** https://arxiv.org/pdf/2611.15653
- **HTML version:** https://arxiv.org/html/2611.15653
- **NeurIPS 2026 Workshop:** Interpretability for Discovery
- **Related AION-1 paper:** [AION-1: Omnimodal Foundation Model for Astronomical Sciences (arXiv:2510.17960)](https://arxiv.org/abs/2510.17960)
- **Project page and code:** Check the paper's arXiv abstract page for links to supplementary materials and code
- **Computational requirements:** 
  - SAE training: GPU-accelerated (specifics not stated; typical SAE training on 300M-parameter model activations requires substantial compute)
  - Inference: Frozen encoder runs efficiently; counterfactual analysis requires forward passes for perturbed inputs

---

## Related Work & Context

### Related Mechanistic Interpretability Work

- **Sparse Autoencoders (SAEs) overview:** SAEs have become a standard tool in mechanistic interpretability, building on work by Bau et al. (feature visualization) and recent work in LLM interpretability (e.g., on language models).
- **Attention Head Intervention (arXiv:2601.04398):** Similar causal analysis approach but focused on attention mechanisms in text transformers.
- **Causal mediation in neural networks:** This work extends prior causal analysis techniques (e.g., causal tracing, activation patching) to multimodal settings.

### Domain-Specific Interpretability

- **Medical imaging interpretability:** Similar mechanisms apply to multimodal medical AI, where imaging, lab results, and patient history are combined. This work provides a blueprint for auditing medical foundation models.
- **Climate and materials science:** Other scientific domains with measurable ground truth could benefit from similar mechanistic interpretability approaches.

### Foundation Models in Astronomy

- **AION-1 ecosystem:** This paper is part of the growing AION-1 foundation model work. Related papers study uncertainty quantification, multimodal alignment, and detection channel biases in AION-1.
- **Broader context:** As astronomy adopts large-scale foundation models, interpretability and trustworthiness become critical for scientific adoption.

### Future xAI Research Directions

1. **Causal-first design:** Future interpretability work should prioritize causal methods over passive observation from the outset.
2. **Domain-grounded interpretability:** Leveraging ground truth and domain knowledge (as in astronomy) should be a standard practice in interpretability research.
3. **Scalability of mechanistic interpretability:** As foundation models grow larger, SAEs and causal intervention techniques must scale efficiently.
4. **Interdisciplinary collaboration:** Interpretability work in scientific domains benefits from close collaboration with domain experts (astronomers, physicians, materials scientists).

---

## Conclusion

This paper demonstrates that mechanistic interpretability can successfully analyze multimodal foundation models and uncover where and why different data modalities contribute to predictions. By showing that astronomy provides a unique testbed with ground-truth measurements, the authors establish a template for rigorous interpretability research in scientific domains. The critical distinction between linear decodability and causal importance highlights the need for causal methods in interpretability work. As foundation models become central to scientific discovery and high-stakes decision-making, this work shows a path toward building trustworthy and interpretable systems.

---

*Document compiled from arXiv preprint and research methodology. For exact metrics, implementation details, extended results, and supplementary materials, refer to the full paper at [arXiv:2611.15653](https://arxiv.org/abs/2611.15653).*
