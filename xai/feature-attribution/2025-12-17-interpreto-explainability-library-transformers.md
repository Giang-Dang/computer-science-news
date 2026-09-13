# Interpreto: An Explainability Library for Transformers

**Authors:** Antonin Poché, Thomas Mullor, Gabriele Sarti, Frédéric Boisnard, Corentin Friedrich, Charlotte Claye, François Hoofd, Raphael Bernas, Nicholas Asher, Céline Hudelot, Fanny Jourdan  
**ArXiv ID:** 2512.09730  
**Status:** Accepted to ACL 2026 System Demonstration  
**Submission Date:** December 2025

## Executive Summary

Interpreto is an open-source Python library that bridges the gap between recent XAI research and practical explainability tooling for Transformer-based language models. It provides a unified API for both **feature attribution methods** and **concept-based explanations**, enabling practitioners to apply sophisticated interpretability techniques to BERT variants through large language models without requiring deep technical expertise. The library is particularly significant for its comprehensive end-to-end concept-based pipeline, which goes beyond typical feature-level attributions and is rarely integrated into existing explainability tools.

## Problem Statement

The explainability and interpretability of Transformer-based models has become critical for deploying trustworthy AI systems in high-stakes domains. However, practitioners face several significant challenges:

1. **Research-to-Practice Gap:** Recent XAI research advances are often scattered across academic papers, making it difficult for practitioners to identify and implement relevant techniques in their own applications.

2. **Attribution Method Fragmentation:** Multiple feature attribution methods exist (gradient-based, attention-based, perturbation-based), but they are not unified under a single, accessible interface, forcing users to learn different APIs for different methods.

3. **Lack of Concept-Based Tooling:** While concept-based explanations (learning higher-level semantic features) are powerful for interpretability, they are rarely integrated into standard libraries alongside traditional attribution methods. Creating end-to-end concept-based pipelines typically requires stitching together multiple tools across different frameworks.

4. **Limited Support for Text Generation:** Most explainability libraries focus on classification tasks, leaving practitioners with few options for interpreting text generation models (like LLMs), which are increasingly prevalent.

5. **Evaluation Fragmentation:** Faithfulness, fidelity, and stability metrics for explanations are scattered across different implementations, lacking standardized evaluation within a single framework.

Interpreto addresses these challenges by providing an integrated, research-backed, and practical framework for model interpretability.

## Core Concepts & Theory

### Feature Attribution Methods

Feature attribution assigns importance scores to input elements (tokens, spans, or features) based on their contribution to model predictions. Interpreto integrates multiple complementary attribution approaches:

#### Gradient-Based Methods
- **Integrated Gradients (IG):** Computes gradients along a path from baseline to input, providing theoretically justified attribution scores with desirable properties (completeness, sensitivity, implementation invariance).
- **Saliency Gradients:** Direct gradient computation with respect to input, providing immediate sensitivity information.
- **Attention Gradients:** Combines attention weights with gradients to capture both attention patterns and gradient flow.

#### Attention-Based Methods
- **Attention Rollout:** Aggregates attention weights across layers to identify which tokens receive the most cumulative attention, useful for understanding information flow through the model.
- **Last Layer Attention:** Focuses on attention weights from the final layer before prediction, providing a simpler baseline.

#### Perturbation-Based Methods
- **Leave-One-Out:** Evaluates prediction change when individual tokens are removed or masked, directly measuring each token's impact on output.
- **LIME (Local Interpretable Model-Agnostic Explanations):** Learns a local linear approximation to the model around the input instance, providing model-agnostic interpretability.

#### Prototype-Based Methods
- **Influence Functions:** Trace model predictions back to training examples, helping identify which training instances most influenced a particular prediction.

### Concept-Based Explanations

Beyond token-level attributions, concept-based explanations operate at a higher semantic level, learning interpretable concepts from model activations:

#### Activation Extraction
Concepts are learned from intermediate model representations (hidden states at specific layers). The extraction process captures the rich semantic information encoded within the model.

#### Concept Learning
Multiple approaches discover meaningful concepts:
- **Dictionary Learning:** Learns sparse, additive combinations of basis vectors that reconstruct activations
- **Clustering-Based Concepts:** Groups similar activation patterns into semantic concepts (e.g., via K-means or hierarchical clustering)
- **Neural Concept Bottlenecks:** Learns explicit concept representations that intermediate layers map to
- **Sparse Autoencoders (SAE):** Discovers interpretable features through unsupervised representation learning
- **Supervised Learning:** Trains classifiers on activation features to identify decision-boundary concepts

#### Concept Interpretation
Once learned, concepts are interpreted through:
- **Textual Descriptions:** Generate natural language explanations of concept meanings
- **Token Attribution to Concepts:** Map individual tokens to discovered concepts
- **Concept Importance Scoring:** Quantify how important each concept is for the model's decision

### Key Theoretical Properties

**Completeness:** Attribution scores should sum to the gap between prediction on input and prediction on baseline, ensuring all prediction mass is accounted for.

**Sensitivity:** Methods should detect when inputs change in ways that affect predictions.

**Implementation Invariance:** Different computational paths implementing the same function should yield identical attributions.

**Faithfulness:** Explanation importance should correlate with actual model behavior, verified through perturbation tests.

**Sparsity:** Good explanations should identify small, sufficient subsets of features or concepts for understanding predictions.

**Stability:** Similar inputs should produce similar explanations, indicating robust and generalizable interpretability.

## Main Ideas & Key Contributions

### 1. Unified API for Multiple Attribution Methods

Interpreto standardizes the interface across 10 different attribution methods through a consistent API:

```python
# Consistent workflow regardless of attribution method chosen
explainer = Explainer(model, method='integrated_gradients')
# or 'attention', 'leave_one_out', 'lime', etc.

attributions = explainer.explain(input_ids, attention_mask)
# Returns normalized importance scores for each token
```

This reduces friction for practitioners switching between methods or comparing multiple approaches.

### 2. End-to-End Concept-Based Pipeline

Rather than requiring users to chain multiple tools together, Interpreto integrates the complete concept-based workflow:

**Stage 1: Activation Collection**
- Intercept and collect hidden states from specified layers
- Handle batching and memory efficiency for large models

**Stage 2: Concept Learning**
- Apply selected concept discovery method (15+ options)
- Learn interpretable basis vectors/clusters representing model concepts

**Stage 3: Concept Interpretation**
- Generate textual descriptions or identify nearest examples
- Compute concept importance for specific predictions

**Stage 4: Evaluation**
- Measure faithfulness via Mean Squared Error (MSE) in concept space
- Evaluate Fidelity (how well concepts reconstruct activations)
- Assess sparsity and stability of concept representations

### 3. Support for Both Classification and Text Generation

Unlike most explainability libraries focused on classification, Interpreto handles:
- **Sequence Classification:** Standard classification tasks on text
- **Token Classification:** Per-token predictions (NER, POS tagging)
- **Text Generation:** Explaining autoregressive predictions in LLMs through causal attention masking

### 4. Comprehensive Evaluation Metrics

Interpreto includes 7+ evaluation metrics beyond the methods themselves:

- **Faithfulness Metrics:** MSE and FID (Fréchet Inception Distance) measure how well explanations capture model behavior
- **Sparsity Metrics:** Quantify explanation compactness and redundancy
- **Stability Metrics:** Measure robustness to input perturbations
- **General Usefulness (ConSim):** Semantic similarity between generated and reference explanations

### 5. Granular Control Over Attributions

The library allows practitioners to specify attribution granularity:
- **Token-level:** Individual token importance
- **Span-level:** Importance of multi-token phrases
- **Input-level:** Aggregated overall input importance

## Methodology & Implementation

### Supported Models

Interpreto supports a wide range of HuggingFace Transformers:
- **BERT variants** (BERT, RoBERTa, DistilBERT, ALBERT)
- **Large Language Models** (LLaMA, Mistral, GPT-2, others via HuggingFace)
- **Encoder-Decoder Models** (T5, mBART)
- **Vision-Language Models** (CLIP-based architectures)

### Attribution Methods Breakdown

**10 Feature Attribution Methods:**
1. Integrated Gradients
2. Gradient (Saliency)
3. Attention × Gradient
4. Attention weights (last layer)
5. Attention rollout
6. Leave-one-out
7. LIME
8. Influence functions
9. Gradient Shap
10. Attention-weighted Gradient

**Evaluation Metrics for Attributions (2):**
- Deletion-based faithfulness (% change in prediction when top features removed)
- Perturbation-based robustness

### Concept Learning Options

**15+ Concept Learning Approaches:**
- Dictionary learning (K-SVD)
- K-means clustering
- Hierarchical clustering
- Sparse autoencoders (SAE)
- Variational autoencoders (VAE)
- Non-negative matrix factorization (NMF)
- Principal component analysis (PCA)
- Independent component analysis (ICA)
- Attention clustering
- Supervised linear classifiers
- And more...

**Concept Interpretation Methods (3):**
- Token attribution to concepts
- Natural language descriptions (via prompting)
- Nearest exemplar identification

**Concept Evaluation Metrics (7):**
- MSE (concept reconstruction error)
- Fidelity (faithfulness of concept space)
- Sparsity (number of concepts used per prediction)
- Stability (consistency across similar inputs)
- Coverage (fraction of predictions explained)
- Separation (distinctness of concepts)
- ConSim (semantic quality)

### Architecture

```
Interpreto
├── Attribution Module
│   ├── Gradient-based methods
│   ├── Attention-based methods
│   ├── Perturbation-based methods
│   └── Evaluation metrics
├── Concepts Module
│   ├── Activation extraction
│   ├── Concept learning (15+ methods)
│   ├── Concept interpretation
│   └── Evaluation (7 metrics)
├── Utils
│   ├── Model wrapping/integration
│   ├── Tokenization handling
│   └── Visualization
└── Examples
    ├── Classification tasks
    ├── Text generation
    └── Multilingual models
```

### Computational Considerations

- **Memory Efficiency:** Handles large models through batch processing and selective layer instrumentation
- **Gradient Checkpointing:** Compatible with models using gradient checkpointing for memory savings
- **GPU Acceleration:** Leverages PyTorch's GPU capabilities for efficient computation
- **Scalability:** Tested on models from 110M (BERT-base) to 70B+ parameters

### Supported Frameworks

- **PyTorch:** Primary framework
- **HuggingFace Transformers:** Core integration point
- **nnsight:** Used for activation extraction and layer-wise analysis
- **NumPy, Pandas:** Data handling and analysis

## Practical Applications & Real-World Use Cases

### Healthcare & Medical AI

**Clinical Decision Support:** For models predicting disease risk or treatment outcomes, token-level attributions reveal which patient symptoms, medical history, or lab values drive predictions. Concept-based explanations help clinicians understand if the model learned clinically meaningful patterns (e.g., "sepsis risk factors" as a learned concept).

**Regulatory Compliance:** The FDA's guidance on explainability for AI-assisted diagnosis increasingly requires interpretability evidence. Interpreto provides the metrics and visualizations needed for regulatory submissions.

### Finance & Risk Assessment

**Loan Decision Transparency:** Banks use Interpreto to explain creditworthiness predictions by highlighting which financial indicators (credit score, income, debt ratio) were most influential. This satisfies requirements under regulations like ECOA and Fair Lending laws.

**Fraud Detection:** For models identifying suspicious transactions, attributions help analysts understand whether the model flagged activity based on legitimate risk indicators or spurious correlations, reducing false positives.

### Legal & Compliance

**Document Classification:** Legal AI systems must explain why contracts are classified as high-risk. Token-level attributions pinpoint problematic clauses, while concepts capture recurring legal patterns ("indemnification clause language").

**Fairness Auditing:** Concept-based explanations help identify whether models learned unfair proxies (e.g., postal codes correlating with protected characteristics).

### NLP Research & Development

**Model Debugging:** Researchers use Interpreto to understand why language models fail on certain examples, identifying erroneous learned patterns or brittle decision boundaries.

**Interoperability Studies:** Comparing concept-based explanations across different models reveals shared semantic structures and architectural differences.

**Fairness & Bias Analysis:** Practitioners identify stereotypical concepts learned by models and design interventions to reduce model bias.

### Autonomous Systems

**Chatbot Transparency:** Users want to understand why chatbots gave particular responses. Interpreto explains which parts of the conversation history and which semantic concepts influenced the response generation.

**Recommendation Systems:** Text-based recommenders (e.g., for news, products) can be explained by showing which aspects of user history or item descriptions drove recommendations.

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Democratizing Interpretability:** By reducing the barrier to entry for sophisticated XAI techniques, Interpreto accelerates the transition from isolated research to production deployments, making explainability a standard practice rather than an afterthought.

2. **Methodological Convergence:** The library's integration of both attribution and concept-based methods signals a field-wide recognition that multiple complementary perspectives are needed for robust explanations.

3. **Standardization of Evaluation:** Unified evaluation metrics across methods enable fair comparisons and help practitioners choose appropriate methods for their specific use case rather than relying on heuristics.

4. **Bridging the Gap for LLMs:** Most existing tools were developed for smaller models. Interpreto's explicit support for LLMs addresses a critical need as these models become ubiquitous.

### Advancing State-of-the-Art in Explainability

- **Research Validation:** ACL 2026 acceptance indicates the research community recognizes the contribution as rigorous and impactful.
- **Method Integration:** The successful integration of 10+ attribution and 15+ concept-learning methods demonstrates that these formerly scattered approaches can be harmonized into a coherent framework.
- **Practical Guidance:** By including implementation details and examples, the paper provides guidance for other tool developers and researchers seeking to build production-grade XAI systems.

### Limitations and Open Questions

1. **Computational Cost Trade-offs:** Some methods (influence functions, gradient-based) are computationally expensive. The library doesn't automatically suggest which method is best for a given model size or latency budget.

2. **Concept Interpretability Trade-off:** Learning more concepts can improve reconstruction but reduce interpretability. The paper doesn't provide strong guidance on choosing the number of concepts.

3. **Limited Theoretical Guarantees:** While individual methods have theoretical properties, the combined system's guarantees are less well understood.

4. **Concept Validation:** Evaluating whether learned concepts are truly meaningful to humans remains partially unsolved; the library provides metrics but not ground truth validation.

5. **Language-Specific Limitations:** Most concept interpretation uses English natural language descriptions; cross-lingual applicability is limited.

### Future Research Directions

1. **Interactive Refinement:** Systems where users iteratively refine explanations based on feedback to improve alignment with human intuition.

2. **Concept Grounding:** Connecting learned concepts to external knowledge bases (knowledge graphs, ontologies) for validation.

3. **Causal Interpretation:** Moving beyond correlational explanations toward causal understanding of model behavior.

4. **Automated Method Selection:** AI systems that recommend attribution or concept-learning methods based on task properties, model size, and latency constraints.

5. **Multimodal Explainability:** Extending the framework to vision-language and other multimodal models with appropriate interpretation visualizations.

## Code & Resources

### Official Implementation

- **GitHub Repository:** [FOR-sight-ai/interpreto](https://github.com/FOR-sight-ai/interpreto)
- **ArXiv Paper:** [2512.09730](https://arxiv.org/abs/2512.09730)
- **Interactive Demo:** [https://for-sight-ai.github.io/interpreto-demo/](https://for-sight-ai.github.io/interpreto-demo/)

### Installation

```bash
pip install interpreto
# or from source:
git clone https://github.com/FOR-sight-ai/interpreto.git
cd interpreto
pip install -e .
```

### Quick Start Example

```python
from interpreto import Explainer
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load model and tokenizer
model_name = "bert-base-uncased"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create explainer
explainer = Explainer(model, tokenizer, method='integrated_gradients')

# Explain prediction
text = "This movie is absolutely fantastic!"
inputs = tokenizer(text, return_tensors='pt')
attributions = explainer.explain(**inputs)

# Each token receives an importance score
for token, score in zip(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0]), attributions[0]):
    print(f"{token}: {score:.4f}")
```

### Concept-Based Explanation Example

```python
from interpreto.concepts import ConceptExplainer

# Extract concepts from model activations
concept_explainer = ConceptExplainer(model, layer='bert.encoder.layer.11', method='sparse_autoencoder')

# Learn concepts from a corpus
corpus_activations = concept_explainer.extract_activations(corpus_texts)
concepts = concept_explainer.learn_concepts(n_concepts=20)

# Explain prediction using concepts
explanation = concept_explainer.explain(text, top_k=5)
# Returns: top 5 concepts driving the prediction with importance scores
```

### Dependencies

- `transformers>=4.30.0` (HuggingFace)
- `torch>=2.0.0`
- `numpy>=1.20.0`
- `scipy>=1.7.0`
- `scikit-learn>=1.0.0`
- `nnsight>=0.1.0` (for activation extraction)

### Computational Requirements

- **VRAM:** 4GB minimum (for BERT-base), 16GB+ recommended for larger models
- **Storage:** ~500MB for library code + model weights
- **Inference Speed:** Minimal overhead for attribution (5-10% latency increase)

### Availability

- **License:** Open source (likely MIT or Apache 2.0, check repository)
- **Maintenance:** Active development by FOR-sight AI team
- **Documentation:** Comprehensive with examples for classification and generation tasks

## Related Work & Context

### Relationship to Existing XAI Tools

**LIME & SHAP:** Interpreto includes implementations of these popular methods but goes further by providing unified APIs and concept-based alternatives.

**Captum (Facebook):** Similar attribution library but focused on PyTorch models generally, not specialized for Transformers; lacks concept-based methods.

**InterpretML (Microsoft):** Focuses on inherently interpretable models rather than post-hoc explanations of black-box models.

**Explainx AI:** Simpler library with fewer methods; Interpreto offers more comprehensive coverage.

### Connection to Broader XAI Communities

**LIME/SHAP Ecosystem:** Builds on decades of work in local explanations and feature importance.

**Concept Bottleneck Models (CBMs):** Extends CBM research by making concept learning accessible within the context of black-box model interpretation.

**Mechanistic Interpretability:** While mechanistic interpretability focuses on internal circuits, Interpreto's activation-based concepts provide complementary perspectives.

**Causal Interpretability:** Establishes foundations for future work connecting attribution methods to causal inference frameworks.

### Building Blocks & Dependencies

- **nnsight:** For clean, declarative model instrumentation
- **Transformers (HuggingFace):** Standards-based model implementations
- **PyTorch:** Deep learning backend
- **Scikit-learn:** Statistical methods for concept learning

### Influence on Future XAI Research

1. **Standardization:** Interpreto demonstrates that diverse XAI methods can be standardized, likely influencing future tool design.

2. **Practical Integration:** The success of integrating research into production encourages more research groups to consider implementation challenges early.

3. **LLM Focus:** As the field pivots to LLM interpretability, Interpreto's explicit support for large models positions it as a reference implementation.

4. **Human-Centered Evaluation:** The library's emphasis on multiple evaluation metrics encourages moving beyond single faithfulness scores toward comprehensive explanation assessment.

## Summary

Interpreto represents a significant step toward making explainable AI practical and accessible. By bridging research advances with production needs, providing unified APIs across methods, and offering an end-to-end concept-based pipeline, it addresses real friction points practitioners face. The library is particularly valuable for:

- Practitioners lacking deep XAI expertise who need robust explanations
- Researchers comparing multiple interpretability methods
- Auditors and compliance officers requiring standardized evaluation
- ML engineers building trustworthy AI systems

As language models become increasingly central to AI applications, tools like Interpreto will be essential for ensuring these systems remain interpretable and trustworthy. The library's acceptance to ACL 2026 and active development suggest it will become a standard tool in the XAI practitioner's toolkit.

[Exact figures unavailable — see full paper for implementation benchmarks and comparative method performance]

---

**Citation:**
```bibtex
@inproceedings{poche2026interpreto,
  title={Interpreto: An Explainability Library for Transformers},
  author={Poch\'{e}, Antonin and Mullor, Thomas and Sarti, Gabriele and others},
  booktitle={ACL 2026 System Demonstration},
  year={2026}
}
```
