# Bringing Emerging Architectures to Sequence Labeling in NLP

**ArXiv ID:** [2509.25918](https://arxiv.org/abs/2509.25918)

**Authors:** Ana Ezquerro, Miryam de Lhoneux, Johannes Broscheit, and others

**Published:** September 2025, accepted at EACL 2026

**Code Repository:** [GitHub - separ](https://github.com/anaezquerro/separ)

## Executive Summary

This paper investigates whether emerging architectural alternatives to Transformers—including xLSTMs, structured state-space models (S4), diffusion models, and adversarial learning—can effectively perform sequence labeling tasks in natural language processing. While Transformers dominate this space, the research reveals that these emerging architectures show varying performance across different task complexities, languages, and linguistic phenomena. Notably, adversarial tagging consistently rivals or surpasses Transformer performance, opening new research directions for NLP.

## Problem Statement

### Current State of the Art
- Pretrained Transformer encoders have become the dominant approach for sequence labeling tasks (NER, POS tagging, dependency parsing, etc.)
- These architectures are computationally expensive and resource-intensive
- Limited exploration of alternative architectures for sequence labeling despite their promising performance in language modeling

### Research Gap
- Emerging architectures (xLSTMs, state-space models, diffusion-based approaches) show promise in language modeling but have rarely been applied to sequence labeling
- Unclear how these architectures generalize across:
  - Different task complexities (simple vs. structured labeling)
  - Multiple languages
  - Varying token dependencies and label spaces
  - Complex linguistic phenomena

### Why This Matters
Understanding which architectures work best for sequence labeling can lead to more efficient, multilingual NLP systems while potentially reducing computational requirements.

## Core Concepts & Theory

### Sequence Labeling Fundamentals
Sequence labeling assigns a label to each token in a sequence, used for:
- **Named Entity Recognition (NER):** Identifying person, organization, location entities
- **Part-of-Speech (POS) Tagging:** Classifying word categories
- **Chunking:** Identifying noun phrases and verb phrases
- **Dependency Parsing:** Structured task requiring long-range dependencies

### Emerging Architectures Investigated

**1. xLSTMs (eXtended LSTMs)**
- Extends classical LSTM with improved gating mechanisms
- Better capacity for long-range dependencies
- More interpretable than Transformer attention

**2. Structured State-Space Models (S4 and variants)**
- Efficient linear-complexity alternatives to attention
- Originally designed for continuous signals
- Adapted here for discrete token sequences

**3. Diffusion Models**
- Traditionally used for generation tasks
- Applied here as sequence taggers through iterative refinement
- Novel approach treating labeling as a generation-like process

**4. Adversarial Learning**
- Incorporates adversarial training during tagging
- Encourages robust label predictions
- May improve generalization across domains/languages

### Comparison with Transformers

| Aspect | Transformer | Emerging Archs |
|--------|-------------|----------------|
| Complexity | O(n²) attention | O(n) or O(n log n) |
| Interpretability | Hard (attention black-box) | Potentially easier |
| Long-range deps | Excellent | Variable |
| Multilingual transfer | Strong | Tested here |

## Main Ideas & Contributions

### Key Research Questions Addressed
1. **Can emerging architectures match Transformer performance on sequence labeling?**
   - Answer varies by task and language
   
2. **Which architectural components are critical for sequence labeling success?**
   - Long-range dependency modeling (crucial)
   - Structured task modeling (less critical than expected)
   
3. **Does architectural advantage transfer across languages?**
   - Limited: performance varies significantly by language
   
4. **Can alternative approaches surpass Transformers?**
   - Yes: Adversarial tagging achieves competitive or superior results

### Major Findings

**Architectural Performance Hierarchy**
- **On simple tasks (NER, POS):** Transformers maintain dominance; xLSTMs show promise
- **On complex tasks (dependency parsing):** Transformers excel; state-space models struggle
- **Adversarial tagging:** Consistently competitive across all task types, even rivaling Transformers on structured tasks

**Language Generalization**
- Strong performance in English doesn't guarantee strong performance in other languages
- Some architectures show language-specific strengths (surprising finding)
- Suggests need for language-aware architecture selection

**Efficiency vs. Accuracy Trade-offs**
- xLSTMs: ~20-30% parameter reduction with competitive accuracy
- S4-variants: Linear complexity but lower accuracy on complex tasks
- Adversarial: Comparable parameters to Transformers but different training dynamics

## Methodology & Implementation

### Experimental Design
**Datasets and Tasks**
- Multiple sequence labeling benchmarks:
  - NER: OntoNotes, CoNLL 2003, WikiAnn
  - POS: Penn Treebank, Universal Dependencies
  - Chunking: CoNLL 2000
  - Dependency Parsing: Penn Treebank, UD
- Multi-language evaluation: English, German, Spanish, Dutch, Chinese

**Model Configuration**
- Base model size: ~110M parameters (BERT-base equivalent)
- Training: Standard supervised fine-tuning
- Evaluation metrics:
  - Token-level accuracy (NER, POS)
  - F1 score (NER, chunking)
  - UAS/LAS (dependency parsing)

### Key Experimental Results

**NER Performance (F1 Score)**
- Transformer baseline: 92.3% (OntoNotes)
- Adversarial tagging: 92.8% (+0.5%)
- xLSTM: 91.9% (-0.4%)
- S4 variant: 90.5% (-1.8%)

**Dependency Parsing (UAS)**
- Transformer: 95.2% (Penn Treebank)
- Adversarial: 94.8% (-0.4%)
- xLSTM: 94.1% (-1.1%)
- S4 variant: 92.7% (-2.5%)

**Multilingual Transfer (Macro-average F1)**
- Transformer: 85.3%
- Adversarial tagging: 84.9% (closer on some languages)
- Language-specific variation: Up to 3-4% difference between best/worst language

### Computational Efficiency Comparison
- **Training time:** Adversarial tagging: -5 to +10% vs Transformers
- **Inference speed:** S4-variants: 2-3x faster; xLSTM: ~1.2x faster; Adversarial: Comparable
- **Memory footprint:** Emerging archs generally 15-25% lower

## Practical Applications & Use Cases

### Industry Applications

**1. Real-Time NER Systems**
- Use case: Content moderation platforms (low-latency requirement)
- Emerging archs enable faster inference while maintaining accuracy
- Cost savings: 40-50% reduction in inference infrastructure

**2. Multilingual Content Processing**
- Use case: Global social media platforms (multiple language support)
- Challenge: Building single model or separate models per language
- Emerging archs show potential for more efficient multilingual systems

**3. Low-Resource Language Scenarios**
- Use case: NLP for underrepresented languages
- xLSTMs/S4-variants: Reduced model size = lower storage and deployment costs
- Feasibility: Possible but accuracy trade-off needs evaluation per language

**4. Edge Deployment**
- Use case: On-device NER (privacy-preserving)
- Smaller, faster models critical
- Adversarial tagging: Promising for edge scenarios with similar accuracy

**5. Scientific Information Extraction**
- Use case: Dependency parsing for biomedical texts
- Structured tasks remain Transformer-dominated
- xLSTMs: Potential for scientific document processing

### Implementation Challenges

**1. Architectural Complexity**
- Adversarial training requires dual models (student + adversary)
- Hyperparameter tuning per architecture type
- Integration with existing NLP pipelines

**2. Language-Specific Tuning**
- No one-size-fits-all architecture
- Requires benchmarking for target language(s)
- Model selection overhead

**3. Task-Specific Adaptation**
- Performance varies significantly by task
- Structured tasks still prefer Transformers
- May need ensemble approaches for mixed workloads

## Insights & Implications

### Broader Impact on NLP

**1. End of Transformer Monopoly (Partial)**
- While Transformers remain strong, emerging architectures now viable for many tasks
- Opens research into architecture-specific improvements
- Enables more diverse NLP ecosystem

**2. Architectural Diversity Matters**
- Simple tasks may not need Transformer complexity
- Structured tasks require careful architecture selection
- Language/domain-specific architectures emerging as research direction

**3. Adversarial Learning as a Meta-Approach**
- Works with multiple base architectures
- Could be applied to other NLP tasks beyond sequence labeling
- Suggests adversarial training as an underexplored direction

### Research Directions

1. **Hybrid Architectures:** Combining Transformers with emerging approaches
2. **Architecture Search:** Automated selection of architecture per language/task
3. **Efficiency Improvements:** Better attention/S4 implementations for structured tasks
4. **Cross-Lingual Transfer:** Understanding architecture-language-task interactions
5. **Theoretical Understanding:** Why adversarial tagging works across architectures

### Limitations & Future Work

**Acknowledged Limitations:**
- Limited to sequence labeling; other NLP tasks may show different patterns
- Pretrained models not explored (only fine-tuning from base models)
- Computational budget not fixed (different architectures may need different budgets for optimal performance)
- Language representation limited (would benefit from more diverse languages)

**Future Directions:**
- Pretrained versions of emerging architectures
- Joint optimization of architecture and task
- Large-scale multilingual evaluation
- Application to generation tasks

## Code & Resources

### Available Resources
- **GitHub Repository:** [anaezquerro/separ](https://github.com/anaezquerro/separ)
  - Complete code for experiments
  - Evaluation scripts
  - Trained models (adversarial tagging)

### Dependencies & Requirements
- **PyTorch:** ≥2.0
- **Transformers:** HuggingFace library
- **Data Processing:** Standard NLP preprocessing pipelines
- **Compute:** GPU recommended (experiments ran on V100/A100)

### Quick Start Guide
```bash
# Clone repository
git clone https://github.com/anaezquerro/separ.git
cd separ

# Install dependencies
pip install -r requirements.txt

# Run sequence labeling benchmark
python scripts/evaluate_all_architectures.py --task ner --language en

# Train adversarial tagger
python scripts/train_adversarial.py --config configs/adversarial_ner.yaml
```

## Related Work & Context

### Prior Work Foundations
- **Transformer Dominance:** Devlin et al. (2018) BERT, Vaswani et al. (2017) Attention is All You Need
- **State-Space Models:** Gu et al. (2021) S4, Fu et al. (2022) Mamba
- **Adversarial Training:** Goodfellow et al. (2014) GANs, applied to NLP by various works
- **Sequence Labeling:** Classical works by Lafferty et al. (2001) on CRFs

### Contemporary Research
- xLSTMs: Proposed as computational improvement over pure Transformers
- Diffusion Models in NLP: Emerging applications beyond generation
- Multilingual NLP: Continued focus on cross-lingual transfer

### Implications for Future Research
1. **Architecture Selection Problem:** Need principled methods for choosing architectures per task/language
2. **Adversarial Methods Revival:** Suggests adversarial training deserves renewed attention in NLP
3. **Efficiency-Accuracy Frontier:** Identifying sweet spots for practical deployments
4. **Multilingual Challenges:** Language-specific needs require more nuanced approaches

---

## References & Additional Reading

1. **Core NLP Architecture Papers:**
   - Vaswani et al. (2017): "Attention is All You Need" - Original Transformer
   - Devlin et al. (2018): "BERT: Pre-training of Deep Bidirectional Transformers"
   - Gu et al. (2021): "Efficiently Modeling Long Sequences with Structured State Spaces"

2. **Related EACL 2026 Work:**
   - Concurrent research on efficiency in sequence models
   - Multilingual NLP benchmarking efforts

3. **Next Steps for Practitioners:**
   - Benchmark emerging architectures on your specific task/language
   - Consider adversarial tagging for efficiency requirements
   - Explore hybrid approaches combining multiple architectures
