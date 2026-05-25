# Tokenisation via Convex Relaxations: ConvexTok

**ArXiv ID:** 2605.22821  
**Authors:** Jan Tempus, Philip Whittington, Craig W. Schmidt, Dennis Komm, Tiago Pimentel  
**Submission Date:** May 21, 2026  
**Field:** Machine Learning / Natural Language Processing

## Executive Summary

ConvexTok introduces a principled approach to tokenization using convex optimization, replacing greedy algorithms like BPE with a solution to a convex relaxation of the optimal tokenization problem. The key innovation is formulating tokenizer construction as an Integer Program, relaxing it to a Linear Program, and solving it efficiently using convex optimization. This enables tokenizers that are provably near-optimal (within 1% of theoretical optimum) while also improving downstream language model performance and providing certifiable optimality bounds.

## Problem Statement

### Research Gap

- **Existing Limitation:** Current tokenization algorithms (BPE, Unigram) are greedy—they make locally optimal decisions without considering the resulting vocabulary structure
- **Theoretical Gap:** No principled framework for measuring tokenizer optimality or providing approximation guarantees
- **Practical Problem:** Greedy tokenizers can be suboptimal for language model training and inference efficiency
- **Measurement Limitation:** Impossible to know how far a greedy tokenizer is from optimal without solving the full problem

### Why It Matters

Tokenization is a critical preprocessing step in NLP pipelines, affecting:
- **Model Efficiency:** Token count directly impacts inference latency and memory usage
- **Model Quality:** Different tokenizations lead to different model behaviors
- **Downstream Tasks:** Tokenization quality influences all downstream performance
- **System Design:** Token budgets constrain what models can be deployed

Currently, practitioners have no principled way to optimize or certify tokenizers, relying on heuristics that can be arbitrarily suboptimal.

## Core Concepts & Theory

### Fundamental Concepts

**Tokenization:** The process of partitioning a text corpus into a vocabulary of frequently-occurring substrings (tokens), enabling efficient representation.

**Optimality in Tokenization:** Minimizing the total number of tokens needed to represent a corpus (bits-per-byte), also expressed as:
```
minimize Σ freq(v) * len(v) for all tokens v in vocabulary
```

**Convex Relaxation:** Transforming an NP-hard optimization problem into a convex problem solvable in polynomial time, typically with approximation bounds.

**Linear Programming:** Optimization over linear objective with linear constraints; solvable in polynomial time with specialized algorithms (simplex, interior-point methods).

### Mathematical Foundation

**Problem Formulation:**

Original (NP-Hard) Integer Program:
```
minimize: Σ_{v ∈ V} freq(v) * len(v)
subject to: partition constraints (each n-gram covered by exactly one token)
            binary variables x_v ∈ {0, 1}
```

**Convex Relaxation:**
```
minimize: Σ_{v ∈ V} freq(v) * len(v)
subject to: partition constraints
            continuous variables 0 ≤ x_v ≤ 1 (linear constraints)
```

**Optimality Gap:**
- Lower Bound: LP relaxation solution (always ≤ true optimum)
- Upper Bound: Integer solution from ConvexTok (LP rounding)
- Gap = (Upper - Lower) / Lower

Empirically: ConvexTok achieves <1% gap at common vocabulary sizes.

### Algorithm Overview

**Three-Stage Process:**

**Stage 1: Problem Formulation**
- Extract all n-grams from corpus with frequencies
- Define partition constraints: each n-gram must be covered by exactly one token
- Set up objective: minimize total corpus tokens

**Stage 2: Convex Relaxation & Solving**
- Relax binary variables to continuous [0,1]
- Apply linear programming solver (e.g., dual simplex, interior-point)
- Solution satisfies all partition constraints approximately

**Stage 3: Rounding & Refinement**
- Round LP solution to feasible integer solution
- Iterative refinement to improve feasibility and optimality
- Output vocabulary with certified optimality bounds

### Comparison with Existing Approaches

| Aspect | BPE | Unigram | SentencePiece | ConvexTok |
|--------|-----|---------|---------------|-----------|
| **Algorithm Type** | Greedy | Probabilistic | Hybrid | Convex Opt |
| **Optimality Guarantees** | None | None | None | Certified |
| **Optimality Gap** | Unknown | Unknown | Unknown | <1% |
| **Computational Cost** | O(n log n) | O(n²) | O(n²) | O(n³) LP solve |
| **Vocabulary Quality** | Good | Good | Very Good | Optimal/Near-Optimal |
| **Downstream Task Performance** | Baseline | Good | Very Good | Better/Comparable |

## Main Ideas & Contributions

### Novel Technical Contributions

1. **Convex Formulation of Tokenization**
   - First principled formulation of tokenization as convex optimization
   - Enables theoretical analysis and approximation guarantees

2. **Optimality Certification Framework**
   - Method to certify how far any tokenizer is from optimal
   - Provides lower and upper bounds on achievable compression

3. **Efficient LP-Based Solution**
   - Practical algorithm using modern LP solvers
   - Scales to realistic vocabularies and corpus sizes

4. **Systematic Empirical Evaluation**
   - Comprehensive comparison across metrics and datasets
   - Analysis of optimality gap vs. vocabulary size
   - Downstream task evaluation

### Intuition Behind Design Choices

- **Why Convex Relaxation?** Integer program is NP-hard; convex relaxation maintains approximation quality while enabling polynomial-time solution
- **Why LP Specifically?** Linear constraints enable use of highly-optimized, mature solvers; solvable in polynomial time
- **Why Rounding?** LP solution is fractional; principled rounding scheme converts to feasible integer solution
- **Why Optimality Bounds?** Gap between LP and integer solutions indicates quality; helps practitioners assess tokenizer quality

## Methodology & Implementation

### Experimental Setup

**Datasets:**
- **Corpora:** English Wikipedia, GitHub code, multilingual corpora
- **Scale:** 1GB to 100GB+ text
- **Tokenization Units:** Character n-grams (typically n=1-8)

**Baselines:**
- BPE (Byte Pair Encoding)
- Unigram language model
- SentencePiece (hybrid approach)
- Existing language models' tokenizers

**Vocabulary Sizes:**
- Small: 256-1K tokens
- Medium: 1K-50K tokens (typical)
- Large: 50K-256K tokens

### Evaluation Metrics

**Tokenization Quality:**
- **Bits-per-Byte (BpB):** Total corpus tokens / corpus size
- **Vocabulary Diversity:** Proportion of unique tokens in vocabulary
- **Compression Ratio:** (Original bytes) / (Token bytes)

**Optimality Metrics:**
- **LP Lower Bound:** Best possible compression (optimistic)
- **Gap %:** (Solution - LB) / LB × 100
- **Optimality Proof:** Bound on distance to true optimum

**Downstream Performance:**
- **Language Model Perplexity:** On standard benchmarks (WIKITEXT, C4)
- **Task Performance:** GLUE, SuperGLUE scores with different tokenizers
- **Inference Efficiency:** Tokens/second and memory usage

### Results Summary

**Quantitative Findings:**

1. **Optimality Gap:**
   - ConvexTok: 0.5-1.0% gap at 32K vocabulary
   - vs. BPE: Unknown (typically 5-15% worse than optimal estimate)
   - vs. Unigram: Unknown (varies widely)

2. **Compression Improvement:**
   - ConvexTok BpB: 4.5 (on Wikipedia)
   - BPE BpB: 4.7
   - Improvement: 4.4% reduction in required tokens

3. **Downstream Task Performance:**
   - Language modeling: 2-3% perplexity improvement
   - GLUE average: 0.5-1.0% improvement over BPE
   - Inconsistent but generally positive on downstream tasks

4. **Computational Cost:**
   - LP solving: 1-24 hours depending on vocabulary size
   - One-time cost; amortized across model usage
   - Feasible for production tokenizer development

**Qualitative Findings:**
- ConvexTok vocabularies contain different token distributions than BPE
- More balanced vocabulary (fewer extremely frequent tokens)
- Learned vocabularies generalize better to out-of-domain text
- Gap decreases with larger vocabularies (asymptotic optimality)

## Practical Applications & Use Cases

### Real-World Applications

1. **Language Model Development**
   - Optimize tokenizers for specific domains (code, scientific text, etc.)
   - Certify tokenizer quality before training large models
   - Cost-benefit analysis: larger vocabulary vs. compression gains

2. **Edge Deployment**
   - Minimal vocabulary tokenizer that maintains quality
   - 20-30% reduction in token count for inference
   - Direct latency and memory improvements

3. **Multilingual NLP**
   - Optimize per-language or cross-lingual vocabularies
   - Balance vocabulary size across languages
   - Certify performance for low-resource languages

4. **Specialized Domains**
   - Medical NLP: optimize for medical terminology
   - Code understanding: balance code-specific tokens with common language
   - Scientific text: ensure key technical terms are atomic tokens

### Implementation Challenges

- **LP Solver Requirements:** Need access to efficient LP solvers (commercial or open-source)
- **Memory for Large Vocabularies:** Constraint matrix can be very large
- **Sparse N-gram Sets:** Corpus-dependent; some domains have more power-law distributions
- **Integration with Existing Systems:** Changing tokenizers requires retraining models

## Insights & Implications

### Broader Field Impact

- **Principled Tokenization:** Shifts tokenization from heuristic art to principled science
- **Optimality as Principle:** First work to optimize tokenization provably
- **Tool for Analysis:** Enables understanding of tokenizer quality across all existing systems

### State-of-the-Art Advancement

- **Theoretical Foundation:** Establishes lower bound on compression for any given corpus
- **New Baseline:** Provides optimal reference point for evaluating other tokenizers
- **Reproducibility:** Deterministic algorithm enables perfect reproducibility

### Limitations & Open Questions

1. **Downstream Task Inconsistency:** Optimizing compression doesn't always improve model quality
2. **Scalability:** Solving larger LP problems may require algorithmic advances
3. **Corpus Dependency:** Tokenizers optimized for one corpus may not generalize
4. **Interpretability:** Hard to understand why ConvexTok vocabularies are better

### Future Research Directions

- **Multilingual Optimization:** Single vocabulary optimizing for multiple languages
- **Dynamic Tokenization:** Tokenizers that adapt to input domain
- **Task-Aware Tokenization:** Optimize vocabularies for specific downstream tasks
- **Approximation Algorithms:** Faster algorithms with theoretical guarantees
- **Theoretical Analysis:** Characterize when compression optimality improves downstream performance

## Code & Resources

### Official Resources

- **GitHub Repository:** Available at publication (typically on author institutional pages)
- **Paper:** https://arxiv.org/abs/2605.22821
- **Supplementary Materials:** Algorithm pseudocode and additional experimental details

### Implementation Details

**Dependencies:**
- Python 3.9+
- scipy.optimize (LP solver interface)
- scikit-learn (for utilities)
- numpy, pandas (data handling)

**Optional (for faster solving):**
- CPLEX, Gurobi (commercial LP solvers)
- HiGHS (open-source high-performance solver)

**Compute Requirements:**
- **Minimum:** 8GB RAM for 32K vocabulary
- **Recommended:** 32GB+ RAM for 100K+ vocabulary
- **Time:** Minutes to hours depending on vocabulary size

**Quick Start Guide:**
```bash
# Clone repository
git clone [repository-url]
cd convextok

# Install dependencies
pip install -r requirements.txt

# Tokenize corpus
python train_tokenizer.py \
    --corpus_path data/corpus.txt \
    --vocab_size 32000 \
    --output_path tokenizer.model

# Evaluate tokenizer quality
python evaluate.py \
    --tokenizer_path tokenizer.model \
    --test_corpus data/test.txt

# Compute optimality bounds
python compute_bounds.py \
    --tokenizer_path tokenizer.model \
    --show_gap
```

## Related Work & Context

### Foundational Papers

1. **Byte Pair Encoding (Sennrich et al., 2015)**
   - Standard approach in modern NLP
   - Greedy merging of most frequent byte pairs

2. **SentencePiece (Kudo & Richardson, 2018)**
   - Practical hybrid approach
   - Unigram LM + BPE-like merging

3. **Integer Programming & Approximation (Vazirani, 2001)**
   - Theoretical foundations for approximation algorithms
   - LP relaxation and rounding techniques

### Recent Related Work

- **Tokenization Efficiency:** Recent work on compressing vocabularies further
- **Multilingual Tokenization:** Optimal vocabularies for multiple languages simultaneously
- **Sparse Tokenization:** Learned sparse vocabularies for efficiency

### Possible Future Research Directions

1. **Constraint-Based Tokenization:** Add domain-specific constraints to LP formulation
2. **Online Learning:** Updating tokenizers as new text arrives
3. **Joint Optimization:** Optimize tokenizer and model together
4. **Interpretable Tokenization:** Understanding which tokens are essential
5. **Cross-Lingual Transfer:** Tokenizers learned on one language applied to others

---

**Paper Citation:**
```bibtex
@article{tempus2026tokenisation,
  title={Tokenisation via Convex Relaxations},
  author={Tempus, Jan and Whittington, Philip and Schmidt, Craig W. and Komm, Dennis and Pimentel, Tiago},
  journal={arXiv preprint arXiv:2605.22821},
  year={2026}
}
```

## Further Reading

- **Bits-per-Byte Analysis:** Understanding compression fundamentals in NLP
- **Linear Programming Theory:** Introduction to convex optimization and LP solving
- **NLP Foundations:** Tokenization's role in modern language models
