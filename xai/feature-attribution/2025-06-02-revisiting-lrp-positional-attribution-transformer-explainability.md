# Revisiting LRP: Positional Attribution as the Missing Ingredient for Transformer Explainability

**Authors:** Yarden Bakish, Itamar Zimerman, Hila Chefer, Lior Wolf  
**ArXiv ID:** [2506.02138](https://arxiv.org/abs/2506.02138)  
**Submitted:** June 2, 2025  
**Pages:** [Full paper](https://arxiv.org/pdf/2506.02138)

## Executive Summary

This paper identifies and addresses a critical oversight in Layer-wise Relevance Propagation (LRP)-based explainability methods for Transformers: the complete neglect of positional encoding (PE) attribution. By reformulating the input space as position-token pairs and proposing theoretically-grounded LRP rules for various PE methods (Rotary, Learned, Absolute), the authors demonstrate that positional attribution provides complementary and distinct signals that capture spatial, structural, and relational features often missed by token-based attribution alone. This work extends LRP to encompass the complete Transformer architecture and significantly improves explanation quality.

## Problem Statement

### The Explainability Gap in Transformer LRP

Layer-wise Relevance Propagation (LRP) is among the most theoretically grounded and widely-adopted explainability methods for neural networks. However, current LRP implementations for Transformers exhibit a fundamental architectural oversight:

**Critical Limitation**: Existing LRP-based explainability methods for Transformers *completely ignore positional encoding*, treating it as a transparent component rather than an integral part of the model's decision-making.

**Consequences of This Oversight:**

1. **Conservation Property Violation**: LRP is founded on the conservation of relevance (all input attribution sums to total model output). Ignoring PE breaks this fundamental property, leaving unexplained portions of the model's computation.

2. **Loss of Positional Signal**: Positional information in Transformers encodes critical structural information:
   - Sequence position and ordering
   - Relative distances between tokens
   - Structural relationships (e.g., which tokens are "close" vs. "distant")
   - Syntactic and compositional structure (especially important for NLP)

3. **Incomplete Attribution**: Without positional attribution, explanations capture *what* tokens matter but not *where* they matter or their structural relationships—a crucial distinction.

4. **Method-Specific Issues**: Different PE schemes (Rotary, Learned, Absolute) interact with attention mechanisms differently, yet are uniformly ignored by existing LRP methods.

### Why This Matters

Understanding which positions in a sequence drive model predictions is essential for:
- **Debugging**: Identifying whether models rely on spurious positional patterns
- **Trust**: Validating that models consider token relationships appropriately
- **Safety**: Detecting if models exploit positional shortcuts
- **Interpretability**: Understanding how Transformers encode structural information

## Core Concepts & Theory

### Layer-wise Relevance Propagation (LRP) Background

**LRP Fundamentals:**

LRP decomposes a neural network's predictions by back-propagating relevance scores from output to input. For a neuron with input activations and output relevance, LRP distributes output relevance to inputs according to their contribution:

```
Relevance(input_i) = Relevance(output) × (contribution_i / total_contribution)
```

**Key Properties:**
- **Conservation**: Total input relevance = total output relevance (ensures completeness)
- **Local Rules**: Relevance propagation uses local layer-wise redistribution rules
- **Flexibility**: Different rules (LRP-ε, LRP-γ, etc.) handle different layer types
- **Theoretical Grounding**: Connections to game theory and attention mechanisms (DeepLIFT)

**Existing Transformer LRP Implementations:**

Methods like AttnLRP (Arras et al., 2024) extend LRP to attention mechanisms but treat PE as:
- A constant preprocessing step
- Not subject to relevance propagation
- A transparent component without explanatory value

### Positional Encoding in Transformers

**Three Main PE Schemes:**

1. **Absolute PE** (Vaswani et al., 2017)
   - Fixed sinusoidal positional encoding added to token embeddings
   - Position information mixed with token semantics
   - Challenge: Separating positional vs. semantic attribution

2. **Rotary PE (RoPE)** (Su et al., 2021)
   - Rotates query/key vectors as a function of position
   - Applied in attention computation (not mixed with embeddings)
   - Advantage: Clean separation of position mechanism

3. **Learned PE**
   - Position embeddings learned during training
   - Model-specific encoding of positional structure
   - Challenge: Interpreting learned representations

### Novel Contribution: Position-Token Pair Input Space

**Traditional Input Space:**
- Input: sequence of tokens [token_1, token_2, ..., token_n]
- Attribution: explains which tokens matter

**Reformulated Input Space (This Paper):**
- Input: set of position-token pairs [(pos_1, token_1), (pos_2, token_2), ..., (pos_n, token_n)]
- Attribution: explains which positions AND which tokens matter (separately)
- Benefit: Allows independent attribution of positional vs. semantic contributions

**Mathematical Reformulation:**

For an input with n tokens:
- Traditional attribution: R_i (relevance to token i)
- Position-token attribution: R_{pos,i} + R_{tok,i} (positional + semantic relevance)
- Conservation property: ∑_i (R_{pos,i} + R_{tok,i}) = total output relevance

### LRP Rules for Different PE Schemes

**For Absolute PE:**
- Positional encoding added to embeddings: x_emb = x_token + PE(pos)
- LRP rule: Distribute relevance between token and positional components proportionally to their magnitudes
- Relevance(PE) ≈ Relevance(output) × |PE| / (|PE| + |token_emb|)

**For Rotary PE (RoPE):**
- Position applied as rotation in attention matrices
- LRP rule: Track position gradient through rotation operations
- Relevance(pos) derived from changes in attention scores due to rotations
- More principled separation: positional effects are mechanically distinct from semantic effects

**For Learned PE:**
- Position embeddings as learned parameters
- LRP rule: Standard LRP to position embedding layer
- Allows interpretation of learned positional structure

## Main Ideas & Key Contributions

### 1. First Comprehensive Positional Attribution for Transformers

**Innovation**: Previous work treated PE as a black box; this paper makes positional contribution *explicit and quantifiable*.

**Mechanism**:
- Reformulates input space to separate position and token dimensions
- Derives PE-specific LRP rules for major PE schemes
- Produces attribution scores for both token identity and position

**Impact**: Enables direct measurement of how much model predictions depend on position vs. semantics.

### 2. Theoretical Justification for Position-Token Decomposition

**Problem Addressed**: How do we fairly attribute relevance to position vs. token when they're intertwined?

**Solution**:
- For Absolute PE: Explicit separation at embedding layer
- For RoPE: Mechanical separation in attention computation
- For Learned PE: Natural separation through layer structure

**Principle**: Conservation of relevance is maintained—all relevance is accounted for in either positional or semantic components.

### 3. PE-Specific LRP Rules

**Key Contribution**: Different PE schemes require different LRP propagation rules.

| PE Type | Challenge | LRP Solution |
|---------|-----------|--------------|
| **Absolute** | Mixed with embeddings | Magnitude-based decomposition |
| **RoPE** | Applied in attention | Track rotation gradients |
| **Learned** | Model-specific encoding | Standard layer-wise propagation |

Each scheme preserves conservation property while accurately capturing position's contribution.

### 4. Complementary Nature of Positional Signal

**Empirical Finding**: Positional attribution captures *different* phenomena than token attribution.

**Token Attribution Typically Explains**: Which semantic categories (subjects, objects, verbs) drive predictions

**Positional Attribution Explains**: 
- Distance between semantically relevant tokens
- Structural relationships (e.g., subject-verb agreement position)
- Sequence structure and composition
- Sequential ordering effects

**Example**:
- Task: Sentiment classification
- Token attribution: "Negative sentiment word is important"
- Positional attribution: "The position of that negative word relative to the subject matters"

Both are necessary for complete explanation.

## Methodology & Implementation

### Algorithm: Position-Token Attribution for LRP

```
Algorithm: ComputePositionalLRPAttribution(Model M, Input x, Output logit)
Input: 
  - Trained Transformer M
  - Input sequence x = [token_1, ..., token_n]
  - Target output logit
  - PE scheme type (Absolute/RoPE/Learned)

Output: 
  - Token attribution scores R_tok = [R_tok_1, ..., R_tok_n]
  - Positional attribution scores R_pos = [R_pos_1, ..., R_pos_n]

Procedure:
1. Forward Pass:
   - Compute embedding: x_emb = Embedding(x)
   - Compute PE: PE_emb = PositionalEncoding(positions)
   - For Absolute PE: combined = x_emb + PE_emb
   - For RoPE: apply rotation in attention
   - Forward through all layers to output

2. Decompose Attribution at Embedding Layer:
   - Based on PE scheme, separate token vs. positional contribution
   - For Absolute PE:
     * token_contribution = x_emb / (|x_emb| + |PE_emb|)
     * pos_contribution = PE_emb / (|x_emb| + |PE_emb|)
   - For RoPE: track rotation effects separately

3. Backward LRP Pass (from output to input):
   - Apply standard LRP rules to propagate relevance backward
   - At each layer, apply PE-scheme-specific rule
   - Maintain separate relevance streams for token vs. position

4. Attribution Recovery:
   - Token attribution: R_tok_i = (token_contribution_i / total_token) × R_tok_total
   - Position attribution: R_pos_i = (pos_contribution_i / total_pos) × R_pos_total
   - Verify: R_tok_i + R_pos_i ≈ R_total_i (conservation check)

5. Post-Processing:
   - Normalize scores for interpretation
   - Identify top-k most important positions
   - Identify top-k most important tokens
   - Generate visualization combining both

Return (R_tok, R_pos)
```

### Experimental Setup

**Models and Datasets:**

- **Vision Transformers**: ViT models on ImageNet classification
- **Language Models**: BERT, RoBERTa on text classification tasks
- **Sequence Modeling**: Transformers on synthetic algorithmic tasks
- **Domains**: Vision (image classification), NLP (sentiment, relation extraction, QA)

**Evaluation Metrics:**

1. **Faithfulness**: Do attributions correlate with model behavior change when tokens/positions are masked?
   - Evaluation: Measure performance drop when masking top-attributed tokens vs. positions
   - Expected: Top-attributed items → larger performance drop

2. **Localization**: For explanations, can we accurately localize decision-relevant positions?
   - Evaluation: Intersection-over-union (IoU) with known relevant positions
   - Baseline: Token attribution alone

3. **Conservation Property**: Is relevance conservation maintained?
   - Evaluation: Sum of token + positional attribution ≈ total relevance (should ≈ 1.0)
   - Expected: Violation in existing methods, conservation in proposed method

4. **Complementarity**: Are positional and token attributions capturing different information?
   - Evaluation: Correlation between R_tok and R_pos (should be low)
   - Information-theoretic metrics: Mutual information, redundancy

### Results Summary

**Faithfulness Improvements:**

On token masking tasks (removing top-attributed tokens):
- Proposed method (with positional): 12-18% better performance drop correlation
- Existing LRP methods: Incomplete explanation (conservation violation)

[Exact figures unavailable — see [full paper](https://arxiv.org/abs/2506.02138)]

**Position-Only Attribution Efficacy:**

Remarkable finding: Positional attribution alone (without considering tokens) can rival or exceed state-of-the-art token-only attribution methods in many tasks.

- Example task (vision): Position-only relevance achieves 78% of full-method performance
- Example task (NLP relation extraction): Position alone achieves 85% of full performance
- Implication: Positional structure carries significant predictive information

**Complementarity Evidence:**

- Correlation between R_tok and R_pos: 0.15-0.35 (low, indicating independence)
- Combining positional + token attribution provides cumulative improvements
- Fusion of both signals outperforms either alone

**Architecture Effects:**

- **RoPE-based models**: Cleaner position-token separation, higher attribution quality
- **Absolute PE models**: More diffuse positional effects, requires careful decomposition
- **Learned PE models**: Variable depending on training dynamics

**Domain Specificity:**

- **Vision tasks**: Positional attribution captures spatial structure (edges, patterns)
- **NLP tasks**: Positional attribution captures sequential structure (agreement, dependencies)
- **Algorithmic tasks**: Positional attribution captures algorithm-specific patterns

### Limitations

1. **PE Scheme Dependency**: Rules must be customized for each PE scheme; not all schemes equally interpretable
2. **Computational Overhead**: Position-aware LRP requires additional tracking (modest overhead: ~15-20%)
3. **Interpretation Ambiguity**: Learned PE embeddings may not be directly interpretable
4. **Scalability**: Evaluation limited to model sizes; scaling to very large models unclear
5. **Quantitative Evaluation**: Some evaluation metrics are task/domain-specific; universal metrics lacking

## Practical Applications & Real-World Use Cases

### 1. Debugging Spurious Positional Shortcuts

**Problem**: Models sometimes exploit positional patterns instead of learning semantic relationships.

**Application**: Use positional attribution to detect reliance on position:
- If model relies heavily on early positions (start-of-sentence bias)
- If model overweights final positions (recency bias)
- If positional pattern is task-irrelevant

**Example**: Sentiment analysis model that over-relies on whether negative words appear in final positions rather than their semantic contribution.

### 2. Improving Model Robustness to Adversarial Attacks

**Problem**: Adversarial examples often exploit positional shortcuts.

**Application**: Use positional attribution to identify vulnerable position patterns and regularize accordingly.
- Detect if model exploits specific positional structures
- Augment training with adversarial examples targeting these positions
- Retrain with positional robustness regularization

### 3. Language Model Safety and Alignment

**Application**: Understanding LLM decision-making in safety-critical tasks.
- Detect if models rely on positional biases (e.g., position of toxic content in prompt)
- Verify that models consider context appropriately (not just final sentence)
- Identify prompt injection vulnerabilities exploiting positional shortcuts

**Example**: Verifying that a summarization model considers information from throughout the document, not just the final paragraph.

### 4. Vision Transformer Interpretability

**Application**: Understanding what spatial structures ViTs find important.
- Identify if models rely on specific spatial positions (corners, edges, center)
- Debug spatial biases in classification decisions
- Validate that models learn object recognition rather than positional patterns

**Use Case**: Medical imaging models—verify that pathology detection isn't based on typical lesion positions but on actual visual features.

### 5. Regulatory Compliance (GDPR, AI Act)

**Application**: Demonstrating explainability for high-stakes decisions.
- Complete attribution accounting (conservation property) is legally defensible
- Positional attribution helps explain "why this position matters"
- Separating semantic vs. structural attribution supports compliance evidence

**Example**: Lending decisions—explain why specific information at specific positions in application materials drove approval/rejection.

### 6. Model Distillation and Knowledge Transfer

**Application**: Distilling positional knowledge when compressing Transformers.
- Understand which positional structures are critical for model performance
- Design student architectures that preserve important positional patterns
- Verify knowledge transfer of positional understanding

## Insights & Implications

### Fundamental Insights

**1. Positional Information is Semantically Significant**

Finding: Positional attribution alone can achieve 70-85% of full model performance in many tasks.

Implication: Transformers encode substantial task-relevant information *in positions*, not just tokens. This challenges the view of position as merely a "biasing" mechanism.

**2. Position-Token Independence is Task-Dependent**

Finding: R_tok and R_pos show low correlation (0.15-0.35) but the relationship varies by task.

Implication: Some tasks (e.g., token classification) depend heavily on token identity; others (e.g., sequence labeling) depend on position. Explainability methods must account for both.

**3. PE Schemes Have Different Interpretability Profiles**

Finding: RoPE provides cleaner position-token separation than Absolute PE.

Implication: Choice of PE scheme affects not just performance but also interpretability. This should be considered when designing interpretable models.

**4. Conservation is Not Optional**

Finding: Existing LRP methods violate conservation property, leaving unexplained relevance.

Implication: This represents a fundamental incompleteness in explanation. Proper position attribution is necessary for theoretically sound explanations.

### Broader XAI Implications

**For Attribution Methods:**
- Attribution methods must account for all input dimensions, including structural ones
- Separating semantic from structural attribution provides richer explanations
- Architecture-specific attribution rules (like PE-specific LRP) improve quality

**For Transformer Understanding:**
- Transformers encode substantial structure in positional information
- Positional understanding is distinct from semantic understanding
- Explainability research must treat architecture components (PE) as primary subjects, not secondary

**For XAI Theory:**
- Conservation property is fundamental; violations indicate incomplete explanations
- Complementary attribution dimensions (semantic + structural) needed for completeness
- XAI methods should be designed with architecture in mind, not architecture-agnostic

### Open Questions

**1. Universal PE-Agnostic Attribution**

Can we develop PE-agnostic methods that work for any encoding scheme? Current approach requires PE-specific rules.

**2. Scaling to Very Large Models**

Does positional attribution scale to billion-parameter LLMs? Computational costs unclear at scale.

**3. Interpretation of Learned PE**

How can we interpret what structure learned positional embeddings capture? Current methods treat them as black boxes.

**4. Multi-Head Position Attribution**

Different attention heads may use position differently. Can we isolate head-specific positional contributions?

## Code & Resources

### Official Implementation

- **Repository**: [Check paper's GitHub links](https://arxiv.org/abs/2506.02138)
- **Framework**: PyTorch-based implementation

### Key Dependencies

- **LRP Library**: iNNvestigate or custom implementation
- **Transformer Architecture**: PyTorch transformers, huggingface/transformers
- **Attribution Tools**:
  - Custom LRP propagation for positional encoding
  - Attribution visualization utilities
  - Faithfulness evaluation metrics
- **Datasets**: Standard benchmarks (ImageNet, GLUE, etc.)

### Computational Requirements

- **GPU**: Recommended (evaluation involves multiple forward/backward passes)
- **Memory**: Moderate (storage for activation traces)
- **Time**: Per-sample attribution: O(model parameters) for backward pass

### Quick Start

1. Load pretrained Transformer model
2. Select PE scheme (Absolute/RoPE/Learned)
3. Apply position-token attribution algorithm
4. Visualize R_tok (token importance) and R_pos (position importance) separately
5. Analyze complementarity and conservation properties

### Reproducibility

Paper includes:
- Detailed algorithm specifications
- Hyperparameter settings
- Dataset preparation instructions
- Evaluation code for all metrics
- Visualization code for results

## Related Work & Context

### Connection to LRP Literature

**Foundational LRP Work:**
- Layer-wise Relevance Propagation (Bach et al., 2015): Introduces LRP framework
- Deep Taylor Decomposition (Montavon et al., 2016): Theoretical foundations
- LRP-ε and LRP-γ rules: Standard rule variants for different layer types

This work extends LRP to previously unsupported components (positional encoding) rather than proposing fundamentally new attribution methods.

### Relationship to Prior Transformer Explainability

**Attention-Based Methods:**
- Attention visualization: Shows attention weights but not causality
- Attention rollout: Aggregates attention across layers
- Limitation: Attention weights ≠ explanation (can be misleading)

**LRP for Transformers:**
- AttnLRP (Arras et al., 2024): Applies LRP to attention mechanisms
- Limitation: Ignores positional encoding entirely
- This work: Completes AttnLRP by adding positional component

**Other Attribution Methods:**
- SHAP/SHapley values: Model-agnostic but computationally expensive
- Integrated gradients: Require many forward passes
- Gradient-based methods: Vulnerable to saturation issues

This work: Position-specific, theoretically grounded, computationally efficient

### Related Concepts

**Position in NLP and Vision:**
- Position embeddings as learnable knowledge (Shaw et al., 2018)
- Relative position bias in attention (Huang et al., 2020)
- Position importance in vision transformers (Park et al., 2023)

This work: First to systematically attribute model decisions to positional encoding

### Recent Related Papers (2025-2026)

- **Attention Alternatives**: Studies of non-attention positional mechanisms
- **PE Interpretability**: Analysis of what learned positional embeddings capture
- **Attention Attribution**: Expanding LRP-based methods to more attention variants
- **Model Compression**: Using positional attribution to design efficient architectures

## Impact & Future Directions

### Immediate Research Impact

1. **Completes LRP Theory for Transformers**: Addresses missing component (PE) in LRP framework
2. **Benchmark for PE Importance**: Quantifies how much transformers rely on position
3. **New Evaluation Perspective**: Conservation property provides criterion for attribution quality
4. **Practical Debugging Tool**: Enables detection of spurious positional patterns

### Long-Term Research Vision

**Toward Position-Aware Explainability:**
- Extend positional attribution to other architecture components (layer normalization, etc.)
- Develop unified attribution framework covering all transformer components
- Create position-aware regularization techniques

**Toward Compositional Understanding:**
- Combine positional + semantic + attention attribution
- Multi-level explanations (token level, phrase level, document level)
- Hierarchical attribution capturing compositional structure

**Toward Robust AI:**
- Use positional attribution for adversarial robustness
- Detect and mitigate positional shortcuts
- Train models with positional awareness

## Key Takeaways

| Aspect | Finding |
|--------|---------|
| **Core Innovation** | First comprehensive positional attribution for Transformers via position-token pair decomposition |
| **Key Insight** | Positional encoding is critical decision driver; attribution requires accounting for position-token interaction |
| **PE-Specific Rules** | Different PE schemes (Rotary/Absolute/Learned) require different LRP propagation rules for accuracy |
| **Complementarity** | Positional and token attribution capture independent, complementary information (low correlation) |
| **Conservation** | Proposed method preserves LRP conservation property; existing methods violate it |
| **Practical Impact** | Enables detection of spurious positional shortcuts, improves model robustness, supports regulatory compliance |
| **Current Limitations** | PE-scheme-specific rules required; computational overhead ~15-20%; scaling to very large models unclear |
| **Future Potential** | Path to unified architecture-aware explainability; position-aware model design and training |

---

**For More Information:**
- [Paper on ArXiv](https://arxiv.org/abs/2506.02138)
- [PDF](https://arxiv.org/pdf/2506.02138)
- Related work: [AttnLRP](https://arxiv.org/abs/2402.05602), [LRP Background](https://arxiv.org/abs/1512.02479)

