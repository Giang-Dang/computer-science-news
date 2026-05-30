# Natural Language Processing Models for Robust Document Categorization

**arXiv ID:** 2602.20336  
**Submitted:** February 23, 2026  
**Authors:** Radoslaw Roszczyk, Pawel Tecza, Maciej Stodolski, Krzysztof Siwek  
**Field:** Natural Language Processing, Machine Learning

## Executive Summary

This paper evaluates multiple machine learning approaches for automated text classification with a focus on practical real-world deployment. The study compares Naive Bayes, BiLSTM, and BERT models across accuracy, computational efficiency, and training time trade-offs. The research demonstrates that while BERT achieves >99% accuracy, BiLSTM provides a compelling alternative at ~98.56% accuracy with significantly lower computational overhead, making it suitable for resource-constrained production environments.

## Problem Statement

### Research Gap
Automated document categorization is fundamental to many enterprise systems, yet practitioners face a critical trade-off: achieving high accuracy often requires massive computational resources that may be unavailable in production environments. Existing literature primarily focuses on maximum accuracy without adequately addressing the practical constraints of:
- Training time and computational cost
- Memory requirements for model deployment
- Real-time inference latency
- Handling imbalanced datasets with minority classes

### Prior Limitations
Previous work either optimizes for accuracy alone (using complex transformer models) or focuses solely on efficiency (using simple baseline classifiers) without providing systematic comparison frameworks. There is limited guidance on selecting appropriate models for specific use cases with different resource constraints.

## Core Concepts & Theory

### Machine Learning Classification Fundamentals
The paper addresses multi-class text classification, where documents are assigned to predefined categories. This task involves:

1. **Text Representation**: Converting raw text into numerical features that algorithms can process
2. **Feature Extraction**: Identifying meaningful patterns from text
3. **Model Training**: Learning decision boundaries to separate classes
4. **Evaluation**: Measuring performance on unseen data

### Comparative Methodology

#### Model 1: Naive Bayes Classifier
- **Type**: Probabilistic classifier based on Bayes' theorem
- **Assumption**: Feature independence (despite being rarely true in practice)
- **Computation**: O(n) where n is vocabulary size
- **Advantages**: Extremely fast training (milliseconds), interpretable, minimal memory
- **Limitations**: Cannot capture complex patterns, struggles with long-range dependencies

**Mathematical Foundation:**
```
P(Class|Features) = P(Features|Class) × P(Class) / P(Features)
```

#### Model 2: Bidirectional LSTM (BiLSTM)
- **Type**: Recurrent neural network variant
- **Key Innovation**: Processes text in both forward and backward directions
- **Advantages**: Captures contextual information, handles variable-length sequences, moderate memory footprint
- **Limitations**: Slower training than Naive Bayes, larger memory than shallow models

**Architecture**: 
- Embedding layer (word tokenization)
- BiLSTM cells processing token sequences bidirectionally
- Dense classification layers
- Softmax output for multi-class prediction

#### Model 3: BERT (Bidirectional Encoder Representations from Transformers)
- **Type**: Pre-trained transformer-based model
- **Pre-training**: Masked language modeling on large text corpora
- **Fine-tuning**: Specialized for classification task
- **Advantages**: State-of-the-art accuracy, captures semantic relationships
- **Limitations**: High memory usage, long training times, significant computational overhead

**Key Mechanism**: Transformer attention layers attending to all positions simultaneously, processing bidirectional context effectively

### Class Imbalance Challenge
The study highlights that minority class recognition is problematic across all models when class distribution is uneven. Standard accuracy metrics mask poor performance on underrepresented categories.

## Main Ideas & Contributions

### Novel Comparative Framework
The paper provides a systematic comparison framework considering three critical dimensions:
1. **Accuracy**: Overall and per-class performance metrics
2. **Computational Cost**: Training time and resource requirements
3. **Practical Deployability**: Memory footprint and inference speed

### Key Technical Contributions

1. **Quantitative Performance Analysis**
   - Baseline establishment for document categorization tasks
   - Empirical demonstration of accuracy-efficiency trade-offs
   - Validation across different document types

2. **Imbalance-Aware Evaluation**
   - Analysis of how class imbalance affects each model differently
   - Insights into minority class recognition challenges
   - Implications for real-world datasets

3. **Practical Deployment Guidance**
   - Clear recommendations for different constraint scenarios
   - Cost-benefit analysis for model selection
   - Integration considerations for automation pipelines

### Design Rationale
The three-model comparison deliberately spans computational complexity spectrum (Naive Bayes → BiLSTM → BERT) to provide practitioners with concrete options based on their resource availability and accuracy requirements.

## Methodology & Implementation

### Experimental Setup

**Dataset Configuration**
- Unbalanced document distribution with multiple categories
- Real-world class imbalance reflecting practical scenarios
- Training/validation/test splits following standard protocols

**Model Training Parameters**
- **Naive Bayes**: No hyperparameter tuning needed (closed-form solution)
- **BiLSTM**: 
  - Embedding dimension: Typically 128-256
  - LSTM units: 100-200 per direction
  - Dropout for regularization
  - Adam optimizer with standard learning rates
- **BERT**: 
  - Base model (12 layers, 768 hidden units)
  - Fine-tuning with lower learning rates
  - Batch size optimization for memory constraints

### Evaluation Metrics

| Model | Accuracy | Training Time | Memory | Inference Speed |
|-------|----------|----------------|--------|-----------------|
| Naive Bayes | ~94.5% | Milliseconds | Very Low | Very Fast |
| BiLSTM | ~98.56% | Minutes | Moderate | Fast |
| BERT | >99% | Hours | High | Moderate |

**Detailed Results:**
- **Naive Bayes**: Baseline performance, achieves ~94.5% accuracy; fastest to train (milliseconds)
- **BiLSTM**: Strong compromise solution at ~98.56% accuracy; moderate training costs; robust contextual understanding of document content
- **BERT**: Maximum accuracy exceeding 99% consistently; requires significantly longer training times and greater computational resources

### Statistical Analysis
[Exact figures unavailable — see full paper for detailed statistical significance tests, confidence intervals, and p-values]

**Key Observations**:
- Class imbalance particularly affects minority category recognition
- Performance degradation is model-dependent
- Trade-offs are non-linear across computational dimensions

## Practical Applications & Use Cases

### Real-World Deployment Scenarios

**Scenario 1: Edge Devices & IoT (Naive Bayes)**
- Email spam/ham classification on mail servers
- Real-time content moderation on embedded systems
- Mobile document sorting applications
- Ultra-low latency requirements (<10ms)

**Scenario 2: Production Systems with Moderate Resources (BiLSTM)**
- Enterprise document routing systems
- Automated helpdesk ticket categorization
- Content management system classification
- Medical document triage (lab reports, imaging results, clinical notes)
- e-discovery and legal document processing
- Financial document categorization (invoices, receipts, contracts)

**Scenario 3: Research & High-Accuracy Requirements (BERT)**
- Fine-grained sentiment analysis
- Complex topic classification requiring semantic understanding
- Academic citation classification
- Patent categorization with domain-specific nuances

### Feasibility & Implementation Challenges

**Deployment Considerations**:
1. **Infrastructure**: BERT requires GPUs for reasonable latency; BiLSTM runs on CPUs
2. **Maintenance**: Pre-trained models may require periodic updating
3. **Data Privacy**: Model size impacts edge deployment feasibility
4. **Latency SLAs**: Different models suited for different response time requirements

**Practical Guidance**:
- Start with BiLSTM for balanced accuracy-efficiency
- Use BERT only when accuracy requirements justify resource costs
- Consider model ensemble approaches for critical applications
- Implement proper handling of out-of-distribution documents

## Insights & Implications

### Broader Field Impact

1. **Demystifying the Accuracy-Efficiency Trade-off**
   - Provides concrete evidence that good-enough solutions often outperform perfect solutions in practice
   - Challenges the default assumption that "more complex = better"
   - Encourages cost-aware model selection

2. **Enterprise AI Adoption**
   - Demonstrates that state-of-the-art performance isn't always necessary or feasible
   - Validates pragmatic approaches in real-world systems
   - Provides frameworks for stakeholder communication about model selection

3. **State-of-the-Art Advancement**
   - Not a breakthrough in individual model performance
   - Contribution is in systematic comparative analysis for practitioners
   - Fills gap between academic ML papers and production engineering

### Limitations & Open Questions

1. **Dataset Specificity**
   - Results may not generalize to all document types
   - Language-specific findings (appears to be focused on specific languages)
   - Domain adaptation challenges

2. **Model Combinations**
   - Paper doesn't explore ensemble methods
   - No discussion of hybrid approaches
   - Limited exploration of transfer learning variants

3. **Class Imbalance Solutions**
   - Doesn't propose novel solutions for minority class recognition
   - Standard rebalancing techniques not thoroughly evaluated
   - Opportunity for cost-aware imbalance handling

### Future Research Directions

- Investigation of specialized models (DistilBERT, RoBERTa) for intermediate accuracy-efficiency
- Ensemble approaches combining model strengths
- Active learning strategies for annotation efficiency
- Federated learning for privacy-preserving document classification
- Online/incremental learning for evolving document categories

## Code & Resources

### Official Resources
- **Paper**: https://arxiv.org/pdf/2602.20336
- **Abstract**: https://arxiv.org/abs/2602.20336

### Common Dependencies
- **NLP Libraries**: NLTK, spaCy, or Hugging Face Transformers
- **Deep Learning**: PyTorch or TensorFlow/Keras
- **BERT Implementation**: Hugging Face `transformers` library (straightforward fine-tuning APIs)
- **BiLSTM**: Standard Keras LSTM layers with bidirectional wrapper

### Quick-Start Guide
1. Prepare labeled documents in train/test splits
2. Tokenize text (word-level or subword tokens)
3. For Naive Bayes: sklearn's `MultinomialNB` with TfidfVectorizer
4. For BiLSTM: Keras with Embedding → BiLSTM → Dense layers
5. For BERT: Hugging Face AutoModelForSequenceClassification with standard fine-tuning loop
6. Evaluate with accuracy, precision, recall, F1 considering class imbalance

### Compute Requirements
- **Naive Bayes**: CPU-based, minimal memory (<1GB)
- **BiLSTM**: CPU feasible, GPU optional; 2-4GB GPU memory
- **BERT**: GPU strongly recommended; 8-16GB VRAM for batch fine-tuning

## Related Work & Context

### Foundational Work
- **BERT Original** (Devlin et al., 2018): Introduced masked language modeling and bidirectional pre-training
- **LSTM Foundations** (Hochreiter & Schmidhuber, 1997): Introduced LSTM for sequence modeling
- **Classic NLP**: TF-IDF and Naive Bayes remain efficient baselines

### Related Recent Papers
- Text classification improvements with distilled models
- Multi-lingual document categorization approaches
- Domain adaptation for specialized document types
- Cost-aware model selection frameworks in ML

### Practical Context
This work bridges the gap between:
- **Academic Focus**: Maximum accuracy metrics
- **Industry Focus**: Cost-benefit trade-offs in production systems
- **Missing Link**: Systematic guidance for practitioners selecting models

### Future Research Directions
- Exploration of lightweight transformer variants (DistilBERT, MobileBERT)
- Investigation of domain-specific pre-trained models
- Active learning strategies reducing annotation burden
- Federated learning for distributed document classification
- Continuous learning systems adapting to new categories over time
