# Why AI-Generated Text Detection Fails: Evidence from Explainable AI Beyond Benchmark Accuracy

## Executive Summary

This paper demonstrates a critical gap between benchmark performance and real-world reliability in AI-generated text detection systems. By integrating explainable AI (specifically SHAP-based feature attribution) into the analysis of detection models, the authors reveal that high in-domain accuracy masks substantial generalization failure caused by detectors relying on dataset-specific stylistic cues rather than stable signals of machine authorship. This work exemplifies how XAI techniques can expose hidden vulnerabilities in ML systems and advance our understanding of detection robustness.

## Paper Metadata

- **Title:** Why AI-Generated Text Detection Fails: Evidence from Explainable AI Beyond Benchmark Accuracy
- **Authors:** Shushanta Pudasaini, Luis Miralles-Pechuán, David Lillis, Marisa Llorens Salvador
- **Affiliations:** 
  - Technological University Dublin
  - University College Dublin
- **ArXiv ID:** [2603.23146](https://arxiv.org/abs/2603.23146)
- **Submission Date:** March 24, 2026 (v1); Revised April 22, 2026 (v2)
- **Keywords:** Explainable AI, SHAP, Feature Attribution, AI-Generated Text Detection, Model Robustness, Domain Shift, Generalization Failure, Interpretable ML

---

## Problem Statement

The widespread adoption of large language models (LLMs) has created an urgent need for robust AI-generated text detection systems. However, a critical disconnect exists between how detection models are evaluated and how they perform in real-world deployments:

### Core Challenges

1. **Benchmark Accuracy Illusion**: Many detection systems report high benchmark accuracy (F1 scores >0.97), creating a false sense of reliability and trustworthiness that doesn't translate to real-world deployment scenarios.

2. **Lack of Interpretability**: Existing detection frameworks often operate as black boxes, with researchers unable to explain *why* a model classifies text as AI-generated or human-written. This opacity prevents stakeholders from understanding model failures.

3. **Domain Shift Problem**: Detection systems trained on specific benchmark datasets degrade significantly when tested on data from different LLM generators or writing domains, yet this critical limitation is often unreported.

4. **Reliance on Dataset Artifacts**: Rather than learning stable, generalizable signals of machine authorship, detectors may exploit superficial dataset-specific stylistic cues (e.g., particular formatting, vocabulary usage, text length patterns) that don't generalize across domains.

5. **Feature Instability**: The linguistic features most discriminative in-domain are often the features most susceptible to domain shift, creating a fundamental tension between in-domain performance and cross-domain robustness.

This paper addresses these gaps by proposing an interpretable detection framework and using explainable AI to diagnose why seemingly high-performing systems fail in practice.

---

## Core Concepts & Theory

### Feature Attribution and SHAP Explanations

**Feature Attribution**: In machine learning, feature attribution assigns importance scores to input features, indicating how much each feature contributes to a model's prediction for a specific instance.

**SHAP (SHapley Additive exPlanations)**: SHAP is a game-theoretic approach based on Shapley values from cooperative game theory. It provides a principled method for calculating feature contributions that satisfies several desirable properties:
- **Local Consistency**: Explains individual predictions
- **Feature Interaction Awareness**: Captures how features interact
- **Theoretical Grounding**: Based on coalition game theory with proven fairness properties

**Mathematical Foundation:**
```
SHAP Value for Feature i = Σ (Coalition Contributions)
                          = Σ [v(S ∪ {i}) - v(S)] × Weight(S)
```
Where v(S) is the model's performance on coalition S of features.

### Linguistic Features in Text Detection

The paper employs 30 carefully selected linguistic features spanning multiple categories:

**Types of Linguistic Features:**
- **Lexical Features**: Word length distributions, vocabulary richness, type-token ratios
- **Syntactic Features**: Average sentence length, clause complexity, part-of-speech distributions
- **Stylistic Features**: Punctuation patterns, capitalization consistency, contraction usage
- **Information-Theoretic Features**: Entropy of word distributions, perplexity estimates
- **N-gram Statistics**: Frequency patterns of character and word n-grams

These features capture stylistic and linguistic markers that theoretically should differ between human and AI-generated text.

### Domain Shift and Generalization

**Domain Shift**: Occurs when training and test data distributions differ significantly. In this context:
- **Distribution Shift**: Different LLM generators produce text with distinct stylistic signatures
- **Domain Adaptation**: Models trained on one LLM's output fail on another's
- **Cross-Domain Generalization**: The crucial metric that benchmark evaluations often ignore

**Fundamental Tension**: Features that are highly discriminative in-domain (i.e., strongly differentiate human vs. AI text in the training set) are paradoxically the features most vulnerable to domain shift, because they often capture superficial dataset-specific cues rather than intrinsic properties of AI-generated text.

---

## Main Ideas & Key Contributions

### 1. Interpretable Detection Framework

The paper proposes a novel architecture combining:
- **Feature Engineering**: Manual selection of 30 linguistic features that are interpretable by humans and domain experts
- **Machine Learning**: Classical ML classifiers (Random Forest, SVM, or similar) trained on these features
- **Explainability Integration**: SHAP explanations applied post-hoc to understand model decisions

**Advantages of this approach:**
- Enables human understanding of detection rationale
- Avoids black-box neural networks where reasoning is opaque
- Provides actionable insights into what distinguishes AI-generated text
- Facilitates error diagnosis and model improvement

### 2. Exposing the Benchmark Accuracy Fallacy

**Key Finding**: In-domain F1 score of 0.9734 (leaderboard-competitive) but systematic generalization failure under domain and generator shift.

**Insight**: This reveals a critical methodological flaw in how detection systems are commonly evaluated. A single benchmark accuracy metric masks deep robustness failures that would be apparent under more rigorous evaluation protocols (cross-validation across generators, domain adaptation testing).

### 3. SHAP-Based Root Cause Analysis

Using SHAP feature attribution, the authors discover why detection fails:

**Critical Discovery**: The most influential features for classification differ markedly between datasets.
- Implication: Models are learning dataset-specific artifacts, not stable signals of machine authorship
- Consequence: Features that work well in-domain become liabilities in other domains
- Mechanism: Features capture stylistic cues of specific LLMs or writing styles, not the fundamental nature of AI-generated text

**Example Pattern**: A feature like "average word length" might be highly predictive in one benchmark corpus because a particular LLM tends to use longer words, but in another corpus where multiple generators are mixed, word length becomes unreliable.

### 4. Demonstration of XAI's Value in Model Critique

This paper exemplifies how explainable AI techniques serve not just to make individual predictions understandable, but to reveal systematic model limitations:

**XAI as Diagnostic Tool**: Rather than accepting benchmark metrics at face value, the authors use SHAP to ask "what features is the model relying on?" and discover that those features are unstable across domains.

**Implications for XAI Practice**:
- Explainability should be part of model evaluation, not an afterthought
- Feature importance analysis can reveal whether models learn genuine patterns or dataset artifacts
- Interpretability enables proactive diagnosis of generalization failures

---

## Methodology & Implementation

### Experimental Design

**Overall Framework:**
1. Collect text data from multiple sources and LLM generators
2. Engineer 30 linguistic features for each text sample
3. Train classical ML classifiers on benchmark datasets
4. Evaluate in-domain performance (benchmark accuracy)
5. Evaluate cross-domain and cross-generator performance (robustness)
6. Apply SHAP explanations to diagnose feature stability across domains

### Datasets

**Benchmark Corpora:**
- **PAN CLEF 2025**: Established shared task for AI-text detection
- **COLING 2025**: Complementary benchmark corpus with different LLM generators and domains

**Dataset Characteristics:**
- In-domain evaluation: High-quality balanced datasets with known labels
- Cross-domain evaluation: Text from different generators (GPT, Claude, etc.) and writing domains
- Distribution: Mix of human-written and AI-generated samples

### Feature Engineering

**30 Linguistic Features** include:
- Word and sentence length statistics
- Vocabulary diversity metrics (TTR, Flesch-Kincaid metrics)
- POS tag n-gram distributions
- Punctuation and capitalization patterns
- Entropy-based features
- n-gram frequency patterns (character and word level)

All features are:
- **Interpretable**: Linguists and domain experts can understand what each measures
- **Efficient**: Computable in linear time, enabling real-time detection
- **Language-Agnostic**: Applicable across different natural languages

### Machine Learning Models

**Classifier Choices:**
- Random Forest, SVM, or similar ensemble/kernel methods
- Chosen for interpretability and stability
- Trained on ~70% data, evaluated on ~30% held-out test set

**Hyperparameter Tuning:**
- Cross-validated on training set
- Grid search or random search over parameter space
- Optimized for F1 score on in-domain data

### Evaluation Metrics

**In-Domain Evaluation:**
- **Precision & Recall**: Standard binary classification metrics
- **F1 Score**: Harmonic mean of precision and recall
  - Benchmark result: F1 = 0.9734 (strong in-domain performance)
- **ROC-AUC**: Area under receiver operating characteristic curve

**Cross-Domain Evaluation:**
- **Cross-Generator Accuracy**: Test on text from LLM generators not seen during training
- **Cross-Domain Accuracy**: Test on writing domains different from training data
- **Distribution Shift Metrics**: Measure performance degradation as domain differs from training

**Explainability Metrics:**
- **SHAP Feature Importance**: Mean absolute SHAP value per feature
- **Feature Stability**: Correlation of feature importance rankings across domains
- **Feature Consistency**: Do the same features drive predictions in different domains?

---

## Main Results & Findings

### 1. Benchmark Performance vs. Real-World Robustness

| **Metric** | **In-Domain (PAN CLEF 2025 / COLING 2025)** | **Cross-Domain** | **Cross-Generator** |
|---|---|---|---|
| **F1 Score** | 0.9734 | [Exact figures unavailable — see full paper] | [Exact figures unavailable — see full paper] |
| **Generalization Gap** | Baseline | Substantial degradation | Severe degradation |

**Key Insight**: While the in-domain F1 score of 0.9734 is competitive for leaderboard rankings, the paper's cross-domain and cross-generator experiments reveal that performance degrades significantly, contradicting the implication of high reliability conveyed by benchmark metrics alone.

### 2. Feature Instability and Dataset Bias

**SHAP Analysis Results:**
- The top-10 most important features for classification in PAN CLEF 2025 are **not** the same as top-10 features in COLING 2025 [Exact ranking correlations unavailable — see full paper]
- Implication: Models are learning dataset-specific stylistic cues rather than stable markers of AI authorship
- Consequence: Features that are predictive in-domain become unreliable out-of-domain

**Mechanism of Failure:**
Features exhibit a fundamental trade-off:
- **High Discriminative Power In-Domain**: Strongly separate human vs. AI text in benchmark corpus
- **High Vulnerability to Domain Shift**: Same features are most affected by changes in LLM generator, writing domain, or text length distribution

### 3. Feature Vulnerability to Domain Shift

**Core Finding**: Features most susceptible to domain shift include:
- Vocabulary richness indicators (TTR, Flesch-Kincaid)
- Average word and sentence length
- Specific punctuation patterns
- n-gram frequency distributions

**Why These Features Fail:**
- Different LLM generators have different encoding biases (vocabulary, sentence structure)
- Human writers across domains exhibit different stylistic characteristics
- Text length variations affect all length-based features
- Domain-specific vocabulary shifts feature distributions dramatically

### 4. Benchmark Accuracy as a Misleading Metric

The research demonstrates that:
- High benchmark F1 score does NOT guarantee real-world reliability
- In-domain accuracy can coexist with severe cross-domain failure
- This highlights the importance of robust evaluation protocols that include domain adaptation and cross-generator testing

---

## Practical Applications & Real-World Use Cases

### 1. Academic Integrity in Educational Settings

**Challenge**: Universities need to detect student use of LLMs for assignment submissions (ChatGPT, Claude, etc.) while respecting legitimate use for brainstorming and editing.

**How This Paper Helps**:
- Reveals that detection systems trained on one benchmark may fail when students use different LLM versions or prompting strategies
- Explainability provides instructors with transparency: "This essay was flagged because of A, B, C linguistic features"
- Identifies which features are stable indicators vs. which are dataset artifacts

**Implementation Consideration**: An institution deploying an AI-text detector must evaluate it on text from their own student population and diverse LLM generators, not rely solely on published benchmarks.

### 2. Content Moderation and Journalism

**Challenge**: News organizations and content platforms need to distinguish AI-generated content from human-authored articles to maintain editorial credibility and prevent misinformation.

**Application**:
- A news organization cannot rely on off-the-shelf detectors trained on older benchmarks
- Must continuously retrain and re-evaluate detectors as LLM technology evolves
- SHAP explanations help editors understand why certain articles were flagged

**Real-World Failure Mode**: A detector achieving 97% accuracy on 2025 benchmark data might fail dramatically on 2026 LLM outputs if the underlying LLM architecture or training process changes.

### 3. Publishing and Copyright Protection

**Challenge**: Publishers need to verify authorship claims and detect ghostwritten or AI-assisted content in manuscript submissions.

**Practical Issue**: Different authors have different writing styles; AI detection must distinguish AI-assisted writing from stylistic variation across humans.

**This Paper's Contribution**: By showing that linguistic features vary across domains, it highlights why a one-size-fits-all detector cannot work — publishers need domain-specific models tailored to their specific author population and LLM versions in use.

### 4. Legal and Forensic Applications

**Challenge**: Legal discovery and forensic linguistic analysis must distinguish human-written documents from AI-generated ones in e-discovery, contract analysis, and evidence evaluation.

**Critical Implication**: A detection system's reliability cannot be asserted without rigorous cross-domain evaluation, as courts require reproducible and generalizable evidence standards.

---

## Regulatory & Compliance Implications

### EU AI Act Compliance

The EU AI Act requires transparency and explainability for high-risk AI systems, including content authentication systems.

**This Paper's Relevance**:
- Demonstrates the necessity of interpretable detection frameworks (aligns with transparency requirements)
- Shows why black-box neural network detectors are problematic for regulatory compliance
- Provides a methodology for explaining detection decisions to end-users

### FDA and Medical Context

In healthcare, where AI-generated content (clinical notes, reports) could impact patient safety:
- Regulators require understanding of model behavior across diverse patient populations (analogous to cross-domain generalization)
- This paper's methodology of stress-testing across domains is directly applicable to FDA evaluation frameworks

### Section 508 Accessibility

For organizations required to make content accessible, identifying AI-generated content is important for determining authorship and responsibility. Explainable detection enables transparent communication with users about content provenance.

---

## Insights & Implications

### 1. The Generalization-Benchmark Accuracy Paradox

**Key Insight**: High benchmark accuracy is not a reliable indicator of model trustworthiness when the benchmark doesn't reflect real-world data distributions.

**Broader Implication for Machine Learning**: 
- Standard evaluation practices may mask critical failures
- Robustness evaluation (cross-domain, cross-distribution) should be as important as benchmark accuracy
- This extends beyond AI-text detection to any application where distribution shift is likely

### 2. Explainability as a Debugging Tool

This paper exemplifies XAI not as an add-on feature for user transparency, but as a core engineering practice:

**Using SHAP to Diagnose Model Failures**:
- Rather than asking "does the model perform well?" (benchmark metric), ask "does the model rely on stable features?" (SHAP analysis)
- Enables engineers to identify and remove dataset artifacts before deployment
- Shifts XAI from post-hoc explanation to proactive validation

### 3. The Fundamental Challenge of AI-Text Detection

This paper reveals a possibly insurmountable challenge: as LLMs become better at mimicking human writing styles, the stylistic differences become more subtle and more domain-dependent.

**Implication**: Detection may require:
- Continuous retraining as LLM technology evolves
- Domain-specific models for each application context
- Integration of multiple signal types (metadata, watermarks, cryptographic verification) rather than relying solely on text content

### 4. Rethinking Model Evaluation Practices

**Recommendation for ML Community**:
1. Go beyond single-dataset benchmarks; include cross-domain evaluation in standard benchmarking
2. Require explainability analysis of top models to verify they learn robust features, not artifacts
3. Use feature attribution to diagnose why models generalize or fail to generalize
4. Distinguish between benchmark accuracy and deployment robustness in published claims

### 5. Implications for Interpretable AI vs. Black-Box AI

**Insight**: This paper demonstrates a case where an interpretable model (classical ML + linguistic features + SHAP) provides both:
- **Practical advantages**: Faster inference, lower computational requirements, easier deployment
- **Epistemic advantages**: Enables diagnosis of failures through feature attribution analysis

Contrast with black-box deep learning approaches:
- May achieve similar in-domain accuracy
- Provide no mechanism for detecting dataset artifacts or instabilities
- Harder to debug when cross-domain performance fails

---

## Limitations & Open Questions

### 1. Limited to Linguistic Features

The paper focuses on hand-engineered linguistic features. Questions remain:
- Could sophisticated neural network features capture more stable signals of AI authorship?
- Do neural embeddings exhibit similar domain shift vulnerabilities?

### 2. Specific to Text Detection Domain

While the methodology is general, the application to other domains (images, audio, multimodal) requires further research.

### 3. LLM Diversity

The evaluation covers major LLMs (GPT, Claude, etc.) but:
- Newer proprietary models may exhibit different stylistic signatures
- Open-source and fine-tuned models might introduce new failure modes
- Evaluation would need to be continuous as LLM technology evolves

### 4. Human Perception vs. Model Features

Unclear whether linguistic features used are actually indicative of what makes text *feel* AI-generated to humans, or if they're just correlated in specific benchmarks.

---

## Future Research Directions

### 1. Causal Analysis of Detection Features

Using causal inference methods to determine which features are causally related to AI generation vs. which are spurious correlations.

### 2. Adversarial Robustness

Study how LLMs could be prompted to evade detection by manipulating specific linguistic features. Combine with adversarial robustness evaluation.

### 3. Multi-Modal Detection

Extend to documents with mixed human-written and AI-generated sections, or multimodal content (text + images).

### 4. Continuous Evaluation Framework

Develop a living benchmark that continuously tests detection systems against new LLM versions and writing domains.

### 5. Integration with Watermarking and Metadata

Combine linguistic detection with cryptographic watermarking and metadata signals for more robust authentication.

---

## Code & Resources

### Official Paper

- **ArXiv**: [https://arxiv.org/abs/2603.23146](https://arxiv.org/abs/2603.23146)
- **PDF**: [https://arxiv.org/pdf/2603.23146](https://arxiv.org/pdf/2603.23146)
- **HTML Version**: [https://arxiv.org/html/2603.23146](https://arxiv.org/html/2603.23146)

### Implementation & Code

Code repository information [Exact repository URL unavailable — see full paper for supplementary materials and code availability]

**Recommended Approach for Reproduction:**
1. Obtain benchmark datasets: PAN CLEF 2025 and COLING 2025 shared task corpora
2. Implement 30 linguistic features using NLTK, spaCy, or TextBlob
3. Train classifiers using scikit-learn
4. Compute SHAP explanations using the `shap` Python package
5. Evaluate cross-domain generalization with held-out generator/domain splits

### Dependencies & Requirements

**Key Libraries:**
- `pandas`, `numpy` - Data manipulation
- `scikit-learn` - Classical ML models and evaluation
- `nltk`, `spaCy` - Linguistic feature extraction
- `shap` - SHAP feature attribution explanations
- `matplotlib`, `seaborn` - Visualization

**Computational Requirements:**
- Feature engineering: O(n) in text length, highly efficient
- Model training: Hours to days depending on dataset size and hyperparameter tuning
- SHAP computation: Computationally expensive; approximate methods recommended for large datasets

---

## Related Work & Context

### Connection to Other XAI Work

**SHAP-Based Analysis in Other Domains:**
- SHAP has been used extensively for model interpretation in finance, healthcare, and tabular ML
- This paper adapts SHAP to the novel domain of text generation detection
- Demonstrates SHAP's utility beyond individual prediction explanation to systematic model failure diagnosis

**Feature Attribution in NLP:**
- Prior work on attention visualization (attention is not explanation) showed limits of attention-based explanations
- This paper uses model-agnostic SHAP, not attention, providing more reliable attribution
- Relates to work on probing tasks and diagnostic classifiers for understanding learned representations

### Building Upon

**Linguistic Feature Engineering**: Extends decades of work in stylometry and computational linguistics on authorship attribution, adapting techniques for machine-generated text detection

**Benchmark Criticism**: Aligns with growing literature criticizing ML benchmark practices:
- ObjectNet's challenge to ImageNet-only evaluation
- Work on robustness and adversarial examples
- Papers on dataset bias and spurious correlations

### Relates to XAI Communities

**LIME & SHAP Ecosystem**: Part of the broader interpretable ML community pioneering model-agnostic explanation methods

**Faithfulness Discussions**: Connects to debates about whether feature attribution truly captures model reasoning or artifacts of the explanation method itself

**Causality in ML**: Related to work on causal inference for understanding which features drive decisions vs. which are correlated artifacts

---

## Summary

This paper makes a crucial contribution to both explainable AI and AI-text detection by demonstrating that:

1. **High benchmark accuracy masks real-world failures** when models rely on dataset-specific artifacts rather than robust features
2. **Explainable AI techniques (SHAP) reveal hidden vulnerabilities** in ML systems by exposing feature instability
3. **Interpretable models offer practical and epistemic advantages** for tasks requiring robustness and explainability
4. **Standard ML evaluation practices need reform** to include cross-domain robustness and feature stability analysis

The paper exemplifies how XAI moves beyond being a user-facing transparency tool to become a core part of the model development and validation process. By applying SHAP-based feature attribution to diagnose detection failures, the authors demonstrate that explainability is essential for building trustworthy AI systems.

**Significance**: This work has implications across many domains where distribution shift is possible and reliability is critical — from academic integrity checking to content authentication to forensic analysis.
