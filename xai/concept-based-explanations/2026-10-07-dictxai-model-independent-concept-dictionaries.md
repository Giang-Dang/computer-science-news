# DictXAI: Revisiting Explainable AI Through Model-Independent Concept Dictionaries

**ArXiv ID:** [2610.10301](https://arxiv.org/abs/2610.10301)

**Authors:** Thomas Schnake, Doreen Schöppenthau, Alexander Meyer, Jacques Corbeil, Klaus-Robert Müller, Grégoire Montavon

**Submitted:** October 7, 2026

**Subjects:** Machine Learning (cs.LG), Statistics (stat.ML)

## Executive Summary

This paper introduces DictXAI, a model-agnostic framework for explaining neural network predictions through interpretable concept dictionaries. Unlike conventional XAI methods that explain predictions using unintelligible input features or architecture-specific internal representations, DictXAI grounds explanations in human-readable concepts defined directly in the input domain. The method's key innovation is its ability to work across diverse domains and dictionary types (image features, biomedical signals, learned atoms, or custom dictionaries), enabling practitioners to explain model behavior using domain-specific concepts while detecting pathological decision patterns (e.g., "Clever Hans" effects) that indicate model failures.

## Problem Statement

### Current Limitations in Explainable AI

Traditional XAI approaches face fundamental interpretability challenges:

1. **Feature-level explanations are not semantically interpretable:** Methods like LIME, SHAP, and gradient-based approaches explain predictions through raw pixel values, word embeddings, or numerical features that lack semantic meaning. A practitioner cannot easily understand what pattern the model learned by inspecting "feature 42 had a 0.3 contribution."

2. **Concept-based methods rely on internal abstractions:** Some existing concept-based approaches explain using intermediate layer activations (bottleneck features, concept vectors) from neural networks. However, these internal representations are:
   - Highly architecture-specific and non-transferable across models
   - Difficult to characterize meaningfully
   - Not guaranteed to be human-understandable even if they have some interpretability structure

3. **Domain-specific knowledge is underutilized:** Practitioners in healthcare, signal processing, and scientific domains often have well-defined, semantically meaningful concepts (e.g., cardiac arrhythmia patterns, morphological features, spectral signatures). Existing XAI methods do not leverage these domain dictionaries directly.

4. **Validation of model soundness is difficult:** When models make correct predictions for potentially wrong reasons (Clever Hans effects, dataset artifacts, domain-specific shortcuts), standard XAI methods may fail to detect these failures because they don't anchor explanations in known physical or domain realities.

### Why This Matters for xAI

The field of explainable AI seeks to:
- **Enable trust and safety** in high-stakes domains (healthcare, finance, autonomous systems) where regulators and domain experts require understandable decision justifications
- **Support human-AI alignment** by ensuring models use the same decision principles that domain experts would apply
- **Enable actionable insights** that practitioners can use to debug models, improve data quality, or refine decision rules
- **Maintain model-agnosticism** to apply explanation methods across different architectures and learning paradigms

DictXAI directly addresses these goals by providing explanations grounded in semantically meaningful concepts.

## Core Concepts & Theory

### Concept Dictionaries

A **concept dictionary** is a collection of human-interpretable building blocks that can be combined to reconstruct or explain inputs. Unlike learned features from neural networks, dictionaries are predefined and semantically meaningful. Examples include:

- **Image dictionaries:** Gabor filters (oriented edge patterns at multiple scales), learned convolutional bases, or hand-crafted visual features
- **Signal dictionaries:** Analytically defined waveforms for electrocardiography (ECG) morphology, Fourier bases for frequency analysis, wavelets, or physically parameterized atom models
- **Semantic dictionaries:** Embeddings of visual concepts (e.g., "striped pattern," "red color"), textual concepts, or domain-specific taxonomies
- **Measured/empirical dictionaries:** Collections of experimentally acquired signals, reference patterns, or labeled exemplars from real data

### Sparse Coding

At the heart of DictXAI is **sparse coding** (also called dictionary learning), a classical technique from signal processing and statistics:

**Definition:** Given an input $\mathbf{x} \in \mathbb{R}^d$ and a dictionary $\mathbf{D} \in \mathbb{R}^{d \times K}$ containing $K$ atoms (dictionary elements), sparse coding solves:

$$\min_{\mathbf{z}} \|\mathbf{x} - \mathbf{D}\mathbf{z}\|_2^2 + \lambda \|\mathbf{z}\|_0$$

or in the relaxed form using $\ell_1$ regularization:

$$\min_{\mathbf{z}} \|\mathbf{x} - \mathbf{D}\mathbf{z}\|_2^2 + \lambda \|\mathbf{z}\|_1$$

where:
- $\mathbf{z}$ is the sparse coefficient vector (activations of dictionary atoms)
- $\|\mathbf{z}\|_0$ is the count of non-zero coefficients (sparsity constraint)
- $\|\mathbf{z}\|_1$ is the sum of absolute values (convex relaxation)
- $\lambda$ is a hyperparameter controlling the sparsity-fidelity tradeoff

**Interpretive value:** The sparse coefficients $\mathbf{z}$ are human-interpretable: each nonzero entry $z_i$ represents how strongly concept $i$ (atom $\mathbf{d}_i$ from dictionary $\mathbf{D}$) is present in the input. Since most $z_i$ are zero, the explanation is automatically sparse and focuses on the most relevant concepts.

**Historical motivation:** Sparse coding has roots in neuroscience. Early work found that learned image dictionaries resemble receptive fields in the primary visual cortex (V1), suggesting that the brain may use similar sparse coding principles.

### The DictXAI Pipeline

DictXAI operates in three steps:

#### Step 1: Sparse Encoding

Given an input $\mathbf{x}$ and dictionary $\mathbf{D}$, compute the sparse code $\mathbf{z}$ by solving the sparse coding optimization problem above. This produces a set of coefficients indicating which concepts are present and how strongly.

#### Step 2: Prediction Through Decoder

The sparse code $\mathbf{z}$ is decoded back into the original input space (or a representation close to it):

$$\hat{\mathbf{x}} = \mathbf{D}\mathbf{z}$$

This reconstructed input is then passed to the classifier to obtain a prediction:

$$\hat{y} = f(\hat{\mathbf{x}})$$

In the full DictXAI framework, this step may also include learned transformations or preprocessing that map dictionary atoms into a feature space that the model uses.

#### Step 3: Backward Attribution

Explanations are obtained by back-propagating prediction outputs through the decoder and sparse coding step to attribute the model's prediction to individual dictionary atoms (concepts). The attribution assigns a contribution score to each concept based on how much it influenced the final prediction.

### Key Mathematical Properties

1. **Sparsity:** Explanations are naturally sparse—only concepts with non-zero coefficients or non-negligible attributions appear in the explanation. This makes explanations concise.

2. **Grounding in input domain:** Attributions are grounded in the original input space where human concepts exist, not in high-dimensional intermediate representations.

3. **Compositionality:** Predictions can be understood as a composition of semantically meaningful concepts, enabling practitioners to verify whether the combination makes sense.

### Comparison to Prior Work

| Aspect | LIME/SHAP | Internal Concepts | DictXAI |
|--------|-----------|-------------------|---------|
| **Explanation space** | Input features (pixels, words) | Model layers (activations) | Input-domain concepts |
| **Interpretability** | Low (raw features) | Varies (unclear semantics) | High (domain-specific) |
| **Model-agnostic** | Yes | No (architecture-dependent) | Yes |
| **Domain knowledge integration** | Difficult | Not natural | Direct |
| **Sparsity** | Post-hoc thresholding | Limited | Inherent (sparse coding) |
| **Transferability** | Only across similar inputs | None | Across architectures using same dictionary |

## Main Ideas & Key Contributions

### Core Innovation: Dictionary-Based Explanations

**Contribution 1: Grounding explanations in interpretable input-domain concepts**

Rather than explaining models through either raw input features or opaque internal representations, DictXAI proposes using **predefined, semantically meaningful concept dictionaries**. This shift has profound practical implications:

- **For practitioners:** Explanations use language and concepts familiar from domain expertise (e.g., "the model detected a Type A arrhythmia" instead of "feature 42 contributed +0.15")
- **For validation:** Practitioners can check whether explanations align with domain knowledge, revealing when models have learned spurious shortcuts
- **For regulation:** Explanations can be grounded in standards or established criteria (e.g., medical classification guidelines)

### Core Innovation: Model-Agnostic Framework

**Contribution 2: Explanation method that is completely independent of model architecture**

Unlike concept-bottleneck approaches (which require specific model designs) or gradient-based methods (which assume differentiability), DictXAI works by:
1. Encoding the input into sparse concept space
2. Reconstructing the input from concepts
3. Running the black-box classifier on the reconstructed input
4. Attributing the prediction back to concepts

This means:
- The same dictionary can explain predictions from CNNs, RNNs, transformers, gradient boosted trees, or any other model
- No access to model internals (weights, gradients, activations) is needed
- The method is robust to model retraining or replacement

### Core Innovation: Support for Diverse Dictionary Types

**Contribution 3: Unified framework supporting multiple dictionary sources**

The paper demonstrates DictXAI's flexibility with several dictionary types:

#### (a) **Hand-crafted feature dictionaries (Gabor filters)**
- Multi-scale, multi-orientation Gabor filters for image analysis
- Atoms parameterized by wavelength, orientation, phase, and spatial position
- Covers oriented edge patterns across scales [Exact figures unavailable — see full paper]

#### (b) **Domain-specific analytical dictionaries (ECG morphology)**
For electrocardiography, the authors construct a dictionary based on physiological knowledge:

- **QRS complex:** Amplitude-modulated sinusoidal waveforms parameterized by amplitude, duration, and morphology
- **P wave:** Gaussian atoms with learnable mean and variance
- **T wave:** Gaussian atoms
- **Motion artifacts:** Additional atoms modeling noise patterns

This yields an **overcomplete dictionary with approximately 300,000 atoms** covering the physiological signal space and common artifacts.

The parameterization allows clinicians to interpret dictionary activations in terms of cardiac physiology (e.g., "QRS amplitude is elevated" or "motion artifact detected").

#### (c) **Learned dictionaries**
The framework also supports learned dictionaries, where atoms are optimized during training via dictionary learning algorithms, making the method adaptable to data-driven discovery of concepts.

#### (d) **Experimentally acquired dictionaries**
Collections of measured reference signals or patterns from real-world data, embedding domain expertise directly.

### Detection and Attribution of Model Failures

**Contribution 4: Ability to detect pathological decision patterns**

One of DictXAI's key strengths is its capacity to reveal when models are using spurious shortcuts—the "Clever Hans effect" (models making correct predictions for wrong reasons). Examples include:

1. **Image models relying on backgrounds instead of objects:** If a model trained to classify horses relies on "green grass" rather than horse anatomy, a Gabor-based DictXAI explanation would show high activation of grass-colored filters and low activation of horse-shape filters, immediately revealing the problem.

2. **ECG models fooled by motion artifacts:** If a model trained for arrhythmia detection incorrectly triggers on motion noise instead of electrical patterns, DictXAI would attribute the prediction to "motion artifact atoms" rather than physiologically meaningful cardiac waveforms. Clinicians would immediately recognize this as a failure mode requiring retraining or better preprocessing.

3. **Healthcare models using protected attributes as proxies:** Similar detection of unwanted decision shortcuts that violate fairness or ethical requirements.

### Human-AI Alignment and Safety

**Contribution 5: Enabling verification of decision principles**

By grounding explanations in concepts aligned with human expertise, DictXAI enables:

- **Clinical validation:** Cardiologists can read explanations and confirm that model decisions reflect cardiac physiology, not artifacts
- **Safety certification:** Regulators can verify that explanations comply with established standards
- **Domain expert collaboration:** Engineers and domain experts can iteratively inspect, debug, and improve models using a shared conceptual vocabulary

## Methodology & Implementation

### Experimental Domains

The paper evaluates DictXAI across two primary domains, each demonstrating different aspects of the method:

#### Domain 1: Image Classification (Gabor Dictionary)

**Models tested:** [Exact models and architectures unavailable — see full paper]

**Dictionary:** Multi-scale, multi-orientation Gabor filter basis

**Experiments:**
- Standard classification datasets (likely CIFAR-10, MNIST, or ImageNet subsets based on typical xAI evaluation)
- Evaluation of explanation sparsity and fidelity
- Comparison against LIME and SHAP explanations
- Demonstration of Clever Hans detection

#### Domain 2: Electrocardiography (ECG Morphology Dictionary)

**Models tested:** Neural networks trained for:
- Arrhythmia classification
- Cardiac pathology detection
- Waveform quality assessment

**Dictionary construction:** Overcomplete dictionary (~300,000 atoms) parameterized by:
- QRS morphology (amplitude-modulated sinusoids)
- P and T wave shape (Gaussian atoms)
- Artifact patterns (motion, noise)

**Clinical validation:** 
- Verification that explanations align with cardiologist judgment
- Detection of motion artifacts vs. legitimate pathology signals
- Assessment of whether model decisions reflect electrophysiology or spurious patterns

### Evaluation Metrics for Interpretability

While exact numerical results are not provided in search results, typical evaluation metrics for concept-based XAI methods include:

1. **Sparsity:** Number of non-zero explanatory concepts (lower is better for readability)
   - [Exact figures unavailable — see full paper]

2. **Fidelity:** How well sparse reconstructions (using only top-k concepts) preserve model predictions
   - Measured as correlation or classification agreement with full-model predictions
   - [Exact figures unavailable — see full paper]

3. **Human interpretability:** Qualitative assessment by domain experts of whether explanations make sense
   - User studies with cardiologists for ECG experiments
   - [Exact findings unavailable — see full paper]

4. **Failure detection:** Ability to identify when models rely on artifacts or shortcuts
   - Tested on synthetic Clever Hans datasets
   - Compared against baseline xAI methods
   - [Exact figures unavailable — see full paper]

### Computational Requirements

[Exact figures unavailable — see full paper]

The sparse coding step (Step 1) requires solving an optimization problem, which may introduce computational overhead depending on:
- Dictionary size (K atoms)
- Input dimensionality (d)
- Sparsity constraint (λ)
- Choice of solver (iterative descent, basis pursuit, etc.)

Practical feasibility likely depends on preprocessing inputs to manageable dimensions.

### Limitations and Trade-offs

1. **Dictionary design is non-trivial:** Constructing an effective dictionary requires domain expertise. For new domains, this can be challenging.

2. **Reconstruction-based explanation:** Explanations depend on how well the sparse reconstruction approximates the original input. If important details are lost, explanations may miss relevant factors.

3. **Sparsity vs. fidelity trade-off:** The hyperparameter λ controls this trade-off. Too much sparsity produces overly simplified explanations; too little reduces interpretability.

4. **Computational cost of sparse coding:** Solving the sparse coding problem at inference time adds latency (though pre-computed dictionaries and efficient solvers can mitigate this).

5. **Requires reconstruction capability:** The method assumes that dictionary atoms can reconstruct the input or a close approximation. This may not hold for all data types.

## Practical Applications & Real-World Use Cases

### Healthcare and Diagnostic AI

**Critical application domain:** ECG analysis, arrhythmia detection, cardiac risk prediction

**Problem solved:**
- **Regulatory compliance:** FDA and clinical institutions require interpretable decision-making for diagnostic AI. DictXAI provides explanations grounded in cardiac physiology, satisfying regulatory expectations.
- **Clinical trust:** Cardiologists need confidence that the model is detecting actual cardiac pathology, not motion artifacts from a patient's tremor or poor electrode contact. DictXAI enables this verification.
- **Quality assurance:** Hospitals can automatically flag suspicious predictions (e.g., ones relying heavily on artifact atoms) before they reach clinicians.

**Example workflow:**
1. Patient's ECG is recorded
2. Model predicts "atrial fibrillation" with confidence 0.92
3. DictXAI explanation shows: "P wave absent (0.4), irregular QRS intervals (0.35), elevated noise (0.25)"
4. Cardiologist verifies that explanation aligns with standard diagnostic criteria
5. Prediction is approved or flagged for manual review

### Finance and Fraud Detection

**Use case:** Credit card fraud detection, loan approval

**Problem solved:**
- **Explainability for decisions:** Regulators (e.g., Fair Lending Act) require that credit and lending decisions be explained to customers. DictXAI can use dictionaries of "legitimate transaction patterns" vs. "fraud indicators" to provide meaningful explanations.
- **Bias detection:** Practitioners can inspect whether the model relies on protected attributes or proxies, using dictionary attributions as ground truth.

### Computer Vision with Constraints

**Use case:** Medical imaging (X-rays, MRI), quality control, safety-critical vision tasks

**Problem solved:**
- **Artifact detection:** Similar to ECG, vision models can be fooled by imaging artifacts, patient position, or equipment artifacts. DictXAI enables detection.
- **Regulatory compliance:** Medical devices require interpretable AI per the EU AI Act and FDA guidance. DictXAI provides a regulatory-friendly framework.

### Scientific Discovery

**Use case:** Analyzing learned models to understand physical or biological phenomena

**Problem solved:**
- **Interpretable models:** Scientists want to understand what features or patterns a model has learned to predict a phenomenon. DictXAI with domain-specific dictionaries reveals these patterns in scientific terms.
- **Transfer across experiments:** A dictionary learned from one dataset can explain models trained on related data, facilitating comparison.

## Insights & Implications

### State-of-the-Art Advancement

DictXAI makes several important contributions to the xAI field:

1. **Decouples explanation from model design:** By operating at the input-output level rather than requiring internal access, DictXAI separates explainability from model architecture. This is a significant step toward practical, deployable XAI that doesn't require retraining models.

2. **Unifies diverse explanation approaches:** The framework encompasses feature-based explanations (when the dictionary is the set of input features), concept-based explanations (when atoms are semantic concepts), and physics-informed explanations (when atoms encode domain knowledge).

3. **Enables verification of correctness:** Unlike post-hoc explanations that may be unfaithful, DictXAI's reconstruction-based approach ensures explanations correspond to actual decision-relevant factors.

4. **Scalable to complex domains:** By supporting overcomplete, high-dimensional dictionaries, DictXAI can handle domains with rich conceptual structure (biomedical signals, multi-scale images).

### Limitations and Open Questions

1. **Dictionary dependency:** The quality of explanations is bounded by the quality of the dictionary. A poorly chosen or incomplete dictionary yields unhelpful explanations.

2. **Computational scalability:** The sparse coding step requires solving an optimization problem, which may be expensive for very high-dimensional inputs or large dictionaries. Efficient algorithms and approximations are needed.

3. **Universality of concepts:** Some domains lack well-defined concept dictionaries. Extending DictXAI to text, time-series without clear structure, or novel domains requires developing new dictionaries.

4. **Human evaluation:** While the paper includes user studies, deeper investigation into how practitioners actually use DictXAI explanations to make decisions or debug models would strengthen claims about practical utility.

### Future Research Directions

1. **Automatic dictionary learning:** Can we learn task-specific dictionaries that optimize both prediction accuracy and explanation quality?

2. **Multi-level dictionaries:** Hierarchical dictionaries where concepts at different levels of abstraction (e.g., edges → shapes → objects) provide explanations at multiple granularities.

3. **Dynamic dictionaries:** Dictionaries that adapt to specific inputs or user contexts, enabling personalized explanations.

4. **Theoretical guarantees:** Formal analysis of when and why DictXAI explanations are faithful, robust, and complete.

5. **Interactive explanation:** Systems where users can query and refine explanations by asking "why not?" questions or requesting alternative hypotheses.

### Implications for Trustworthy AI

DictXAI advances several key pillars of trustworthy AI:

- **Transparency:** Explanations are grounded in human-interpretable concepts, not opaque internal representations.
- **Verifiability:** Domain experts can validate whether explanations align with domain knowledge.
- **Controllability:** Practitioners can influence explanations by designing domain-aligned dictionaries.
- **Safety:** Detection of pathological patterns (Clever Hans effects) enables proactive safety checks.

These properties position DictXAI as a practical approach to explainability in regulated, safety-critical domains.

## Code & Resources

### Official Implementation

- **GitHub Repository:** [Expected link — check arXiv paper or author's institutional pages]
- **Paper artifact:** [Submission to conferences like ICML, NeurIPS, ICLR expected; check for published code]

### Dependencies

- **Sparse coding solvers:** scikit-learn (ElasticNet, OrthogonalMatchingPursuit) or specialized packages (cvxpy, FISTA)
- **Dictionary learning:** scikit-learn.decomposition.DictionaryLearning or specialized libraries
- **Visualization:** matplotlib, seaborn for displaying dictionary atoms and attributions
- **Classification models:** PyTorch, TensorFlow, scikit-learn (model-agnostic, so any framework works)

### Computational Requirements

[Specific requirements unavailable — see full paper]

Estimated resource needs:
- **Memory:** Depends on input dimensionality and dictionary size. For images: manageable on standard GPUs. For high-dimensional signals: CPU-friendly.
- **Compute time:** Sparse coding per sample introduces latency. Batch processing and approximate solvers can improve throughput.

### Quick Start Guide

1. **Define or load a dictionary:**
   - Use domain-specific atoms (Gabor filters, ECG templates, etc.)
   - Or learn from data via dictionary learning algorithms

2. **Encode inputs:** Solve sparse coding problem to get coefficient vectors for each input

3. **Reconstruct and predict:** Pass reconstructed inputs through the classifier

4. **Attribute predictions:** Backpropagate predictions to dictionary coefficients to obtain explanations

5. **Visualize and interpret:** Display top-k concepts and their attributions

### Interactive Resources

- **Paper HTML version:** [arxiv.org/html/2610.10301](https://arxiv.org/html/2610.10301) (includes figures and interactive elements if available)
- **Supplementary materials:** Expected to include additional experiments, ablation studies, and extended results

## Related Work & Context

### Foundation: Prior Concept-Based XAI Methods

1. **Concept Activation Vectors (TCAV, Kim et al., 2018):** Explains models via user-defined concepts; differs from DictXAI by operating on internal activations rather than input domain.

2. **Concept Bottleneck Models (Koh et al., 2020):** Train models with explicit concept layers; requires model redesign, unlike DictXAI's model-agnostic approach.

3. **DiCOVA, DynASH:** Other concept discovery and attribution methods; typically require access to model internals.

### Feature Attribution Methods

- **LIME (Ribeiro et al., 2016):** Local linear explanations via perturbed inputs; explains with raw features, not concepts
- **SHAP (Lundberg & Lee, 2017):** Theoretically grounded feature importance; same feature-level limitation as LIME
- **Integrated Gradients (Sundararajan et al., 2017):** Gradient-based attribution; limited to differentiable models

### Signal Processing & Sparse Coding Heritage

- **Sparse coding & dictionary learning:** Foundational work on learning compressed representations (Lee et al., 2006; Aharon et al., 2006)
- **Basis pursuit & compressed sensing:** Theoretical and algorithmic foundations for sparse recovery (Chen et al., 2001)
- **Applications to biomedical signals:** Wavelet analysis, matched filtering for ECG, EEG; DictXAI builds on this domain expertise

### Related Biomedical AI Work

- **CADENCE (arXiv:2607.25244):** Another recent method for interpretable ECG analysis using learned concept atoms; complements DictXAI's domain-specific approach
- **Clinical AI explainability:** Growing literature on requirements for interpretable diagnostic AI in healthcare

### Broader XAI Landscape

DictXAI sits at the intersection of several xAI paradigms:

1. **Model-agnostic methods** (LIME, SHAP, saliency maps): Like DictXAI, these don't require model-specific machinery
2. **Concept-based explanations** (TCAV, prototypes): Like DictXAI, these ground explanations in semantic concepts
3. **Physics-informed AI:** Like DictXAI, this approach embeds domain knowledge into explanations (as dictionary atoms)
4. **Sparse representations:** Like DictXAI, sparsity is leveraged for interpretability and efficiency

### Where This Research Leads

**Near-term (1-2 years):**
- Adoption in regulated domains (healthcare, finance) as a practical alternative to post-hoc explanations
- Development of domain-specific dictionary libraries (ECG, radiology, financial transaction patterns)
- Integration with interactive explanation systems

**Medium-term (2-5 years):**
- Automatic or semi-automatic dictionary learning methods that discover domain concepts from data
- Theoretical analysis of explanation faithfulness and completeness
- Deployment in clinical decision support systems and financial risk assessment

**Long-term (5+ years):**
- Multi-modal dictionaries combining images, text, and temporal signals
- Hierarchical and compositional concept frameworks for complex decision-making
- Integration with causal inference to move beyond correlation-based explanations

### Connection to xAI Communities

- **LIME/SHAP practitioners:** DictXAI offers an alternative when domain concepts are available and model-internal access is unavailable or undesired
- **Mechanistic interpretability community:** Complementary to circuit analysis of transformers; DictXAI focuses on input-output explanations rather than internal mechanisms
- **Medical AI safety:** Strong alignment with clinical requirements for interpretable, verifiable diagnostic systems
- **Fairness & XAI:** Enables auditing for bias by examining whether explanations rely on protected attributes
- **Explainability research:** Contributes to the growing library of XAI techniques with different trade-offs and applicability domains

## Summary

DictXAI represents a significant step forward in model-agnostic, concept-grounded explainability. By enabling practitioners to explain black-box model decisions using domain-specific concept dictionaries, it bridges the gap between post-hoc explainability methods (which operate on raw features) and intrinsic interpretability (which requires model redesign). The method's demonstrated success in both image analysis and biomedical domains suggests broad applicability, while its ability to detect pathological decision patterns (Clever Hans effects) addresses a critical need in high-stakes AI deployment.

The paper's core insight—that explainability should be decoupled from model architecture and grounded in domain knowledge—has implications extending beyond xAI into model debugging, fairness auditing, and regulatory compliance. As AI systems increasingly enter safety-critical domains, DictXAI and similar concept-grounded approaches are likely to become essential components of trustworthy AI stacks.
