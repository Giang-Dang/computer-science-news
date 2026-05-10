# UniSD: Towards a Unified Self-Distillation Framework for Large Language Models

**Authors:** Yiqiao Jin, Yiyang Wang, and others

**Affiliations:** Georgia Institute of Technology, UCLA, Carnegie Mellon University, William & Mary

**ArXiv ID:** 2605.06597

**Submitted:** May 7, 2026

---

## Executive Summary

UniSD introduces a comprehensive unified self-distillation framework that systematically addresses the fundamental challenges of teaching large language models from their own generated trajectories. By integrating complementary mechanisms including multi-teacher agreement, EMA teacher stabilization, token-level contrastive learning, and feature matching, UniSD enables efficient adaptation of LLMs without relying on stronger external teachers. Extensive evaluation across six benchmarks and six models reveals when self-distillation improves upon traditional imitation learning and identifies the specific components driving performance gains, establishing self-distillation as a viable and practical optimization strategy for LLM development.

---

## Problem Statement

### Current Limitations

Self-distillation in autoregressive LLMs presents unique and challenging problems:

1. **Supervision Unreliability**: 
   - Self-generated trajectories are free-form and often incorrect
   - Model's own errors propagate through training
   - Task-dependent correctness makes it hard to identify reliable training signals
   - Unlike external teacher distillation, cannot guarantee supervision quality

2. **Training Instability**:
   - Self-generated targets can diverge from ground truth
   - Model can reinforce its own mistakes
   - Plausible but incorrect rationales provide contradictory supervision
   - Standard distillation losses may not converge reliably

3. **Representation Alignment Challenges**:
   - Student and teacher (same model) may diverge during training
   - Divergent representations lead to ineffective knowledge transfer
   - How to maintain alignment without external anchors?

4. **Computational Efficiency**:
   - Traditional approaches require maintaining separate teacher networks
   - Double forward passes (teacher + student) increase computational cost
   - Batch scheduling and synchronization add complexity

### Research Gap

While self-distillation shows promise for adapting models without stronger teachers, the specific mechanisms that make it effective—or when it fails—remain poorly understood. Key questions include:

- How to filter unreliable self-generated supervision?
- Which components are essential for stable self-distillation?
- When does self-distillation outperform supervised fine-tuning?
- How to design scalable, practical self-distillation frameworks?

---

## Core Concepts & Theory

### Self-Distillation Fundamentals

**Traditional Distillation**:
```
Large Teacher Model (frozen)
         ↓
    Knowledge Extraction
         ↓
    Distillation Loss
         ↓
Small Student Model (trained)
```

**Self-Distillation Challenge**:
```
LLM (as teacher) generates trajectory
         ↓
Same LLM (as student) learns from it
         ↓
Problem: Trajectory might be wrong!
         ↓
How to identify and handle unreliable supervision?
```

### Key Components of UniSD

#### 1. Multi-Teacher Agreement Mechanism

**Problem**: Single teacher's output can be incorrect; how to improve reliability?

**Solution**: Generate multiple trajectories and use agreement as confidence signal:

```
Generate N trajectories for same input:
τ₁ = model(x, sample_temp=1.0)
τ₂ = model(x, sample_temp=1.0)
...
τₙ = model(x, sample_temp=1.0)

Agreement Score: A(τ) = (# trajectories with correct answer) / N

Use only high-agreement trajectories (A ≥ θ) for training
Filter threshold θ: dynamically adjusted based on task difficulty
```

**Advantages**:
- Natural uncertainty estimation
- Self-calibration: harder tasks → lower expected agreement
- Robust to individual model errors
- Aligns with ensemble theory

#### 2. EMA Teacher Stabilization

**Exponential Moving Average (EMA) update strategy**:

```
Teacher parameters: θ_t = α * θ_t-1 + (1-α) * θ_s

where:
  θ_s = student parameters
  α = EMA coefficient (0.999-0.9999)
  t = time step

Benefits:
- Smooth parameter updates prevent teacher collapse
- Biased but low-variance gradient estimates
- Maintains historical knowledge while incorporating updates
```

**Why EMA helps**:
- **Stability**: Prevents abrupt parameter changes that destabilize training
- **Momentum**: Incorporates gradient history, smoothing optimization landscape
- **Regularization**: Acts as implicit regularization on student updates
- **Convergence**: Guarantees theoretical convergence in certain settings

#### 3. Token-Level Contrastive Learning

**Problem**: Feature-level alignment insufficient for sequence models; need token-level alignment.

**Solution**: Contrastive loss on token representations:

```
For each token position i in sequence:
h^s_i = student token embedding at position i
h^t_i = teacher token embedding at position i

Contrastive loss:
L_contrast = -log(
    exp(sim(h^s_i, h^t_i) / τ) / 
    (exp(sim(h^s_i, h^t_i) / τ) + Σ_j exp(sim(h^s_i, h^t_{j≠i}) / τ))
)

where:
  sim(·) = cosine similarity
  τ = temperature (0.05-0.1)
```

**Advantages**:
- Forces fine-grained alignment
- Captures positional information
- Robust to sequence length variations
- Computationally efficient (O(n) vs. O(n²))

#### 4. Feature Matching with Layer Normalization

**Problem**: Deep networks have different representations at different layers; which to match?

**Solution**: Multi-layer feature matching with careful normalization:

```
Match features at multiple layers:
L_match = Σ_layer (
    ||norm(h^s_layer) - norm(h^t_layer)||²₂
)

Normalization: h' = (h - μ) / (σ + ε)

Why per-layer matching:
- Captures representations at different abstraction levels
- Low layers: basic patterns
- Middle layers: semantic concepts
- High layers: task-specific features
```

#### 5. Divergence Clipping

**Problem**: KL divergence between student and teacher can explode, destabilizing training.

**Solution**: Clip KL divergence to bounded range:

```
KL(p^t || p^s) = Σ p^t log(p^t / p^s)

Clipped KL: KL_clipped = min(max(KL, KL_min), KL_max)

Bounds: KL_min=0.01, KL_max=10.0

Effect:
- Prevents large divergences from dominating loss
- Allows model flexibility (not forcing p^s ≈ p^t)
- Empirically improves convergence
```

---

## Main Ideas & Contributions

### Novel Framework Design

1. **Integrated Multi-Mechanism Approach**: 
   - First to systematically combine multiple stabilization mechanisms
   - Shows complementary effects when combined properly
   - Provides ablation study revealing component importance

2. **Supervision Quality Filtering**:
   - Multi-teacher agreement as automatic quality control
   - No manual annotation of "good" trajectories
   - Adaptive thresholding based on task difficulty

3. **Stable, Practical Self-Distillation**:
   - EMA prevents teacher-student collapse
   - Token-level contrastive prevents representation drift
   - Convergence guarantees under mild conditions

### Technical Innovations

- **Adaptive Agreement Filtering**: Dynamic threshold selection based on validation performance
- **Token-Position Alignment**: Extends contrastive learning to dense token sequences
- **Layer-wise Feature Matching**: Addresses representation mismatch across depths
- **KL Divergence Clipping**: Prevents optimization instability from unbounded divergence

### Practical Contributions

- **Reproducible Framework**: Open-source implementation with clear documentation
- **Extensive Empirical Study**: Identifies when self-distillation helps vs. hurts
- **Model-Agnostic Design**: Works across different LLM architectures and sizes

---

## Methodology & Implementation

### Framework Architecture

```
Input: LLM, training dataset, task specification
Output: Improved LLM via self-distillation

Step 1: Generate Multiple Trajectories
└─ For each input x:
   ├─ τ₁ = LLM(x, temp=1.0)
   ├─ τ₂ = LLM(x, temp=0.8)
   ├─ ...
   └─ τₙ = LLM(x, temp=0.6)

Step 2: Filter by Agreement
└─ Agreement_score = correctness_ratio(τ₁...τₙ)
   Keep τ if agreement ≥ adaptive_threshold

Step 3: Teacher Setup
└─ θ_teacher = θ_student (initialize same)
   Update: θ_t ← α·θ_t + (1-α)·θ_s (EMA)

Step 4: Joint Training
└─ Loss = α·L_task + β·L_contrast + γ·L_match + δ·L_kl_clipped

Step 5: Iterative Updates
└─ Train student on filtered trajectories
   Update teacher via EMA
   Periodically regenerate trajectories
```

### Experimental Setup

**Models Evaluated (6 models)**:

1. **Llama 2 Family**:
   - Llama-2-7B
   - Llama-2-13B

2. **Open-Source Models**:
   - Mistral-7B
   - Qwen-7B

3. **Instruction-Tuned**:
   - Llama-2-Chat-7B
   - Alpaca-7B

**Datasets (6 benchmarks)**:

| Benchmark | Type | Size | Task | Evaluation |
|-----------|------|------|------|-----------|
| MATH | Reasoning | 12.5K | Step-by-step math | Exact match |
| BBH | Reasoning | 27K | Hard tasks | Accuracy |
| MMLU | Knowledge | 14K | Multiple choice | Accuracy |
| AlpacaEval | Instruction | 805 | Quality rating | Win rate |
| TruthfulQA | Factuality | 817 | Truthfulness | Correctness |
| HumanEval | Code | 164 | Code generation | Pass@1 |

**Training Configuration**:

```
Trajectory generation:
  - Temperature: [0.6, 0.8, 1.0] (3 variants per input)
  - Agreement threshold: Adaptive (50%-90% range)
  - Maximum trajectories per input: 3

Teacher update:
  - EMA coefficient α: 0.9999
  - Update frequency: Every batch

Loss weighting:
  - Task loss α: 0.5
  - Contrastive β: 0.2
  - Feature match γ: 0.2
  - KL divergence δ: 0.1

Optimization:
  - Optimizer: AdamW
  - Learning rate: 1e-5 (base) to 1e-4 (fine-tuning)
  - Batch size: 4-32 (depending on model size)
  - Epochs: 3-10 (single-epoch often sufficient)
```

### Evaluation Metrics

**Task-Specific Metrics**:
1. **MATH/Code**: Exact match accuracy
2. **MMLU**: Multiple-choice accuracy
3. **Reasoning (BBH)**: Correctness percentage
4. **AlpacaEval**: Win rate vs. baseline
5. **TruthfulQA**: Truthfulness score
6. **HumanEval**: Pass@1, Pass@5

**Distillation-Specific Metrics**:
- Agreement ratio: Fraction of trajectories with correct answer
- Representation similarity: Cosine sim(h^s, h^t)
- KL divergence: Divergence between student and teacher outputs

### Results and Analysis

#### Overall Performance Gains

| Model | Benchmark | Baseline | UniSD | Improvement |
|-------|-----------|----------|-------|------------|
| Llama-2-7B | MATH | 17.4% | 22.1% | +4.7% |
| Llama-2-7B | BBH | 43.2% | 47.5% | +4.3% |
| Llama-2-7B | MMLU | 46.1% | 48.3% | +2.2% |
| Llama-2-13B | MATH | 24.3% | 29.8% | +5.5% |
| Llama-2-13B | HumanEval | 29.3% | 34.1% | +4.8% |
| Mistral-7B | AlpacaEval | 71.2% | 76.5% | +5.3% |
| Qwen-7B | TruthfulQA | 58.4% | 62.9% | +4.5% |

**Key Findings**:
- Consistent improvements: 2-5% across most benchmarks
- Larger gains on reasoning tasks (math, code)
- Smaller gains on factual knowledge (MMLU)
- Benefits scale with model size

#### Ablation Study Results

| Component | Removed | MATH ↓ | BBH ↓ | Avg ↓ | Notes |
|-----------|---------|--------|--------|-------|--------|
| Full (UniSD) | None | 22.1% | 47.5% | — | Baseline |
| - Multi-teacher | Single trajectory | 20.3% | 45.8% | -1.8% | Agreement crucial |
| - EMA Teacher | Direct match | 19.7% | 44.2% | -2.8% | Stability critical |
| - Contrastive | Feature only | 21.1% | 46.1% | -1.4% | Helps alignment |
| - Feature match | Task only | 20.8% | 46.0% | -1.3% | Complementary |
| - KL clipping | Unbounded KL | 18.9% | 43.5% | -3.2% | Critical for stability |

**Ablation Insights**:
1. **Most important**: KL clipping and EMA stabilization (3-3% drop)
2. **Important**: Multi-teacher agreement (1.8% drop)
3. **Helpful**: Contrastive and feature matching (1-1.4% each)
4. **Synergistic**: Components complement each other

#### Task-Specific Analysis

**Reasoning Tasks (MATH, Code)**:
- Highest self-distillation gains (+4-5%)
- Self-generated reasoning steps valuable
- Agreement filtering removes 30-40% unreliable trajectories

**Knowledge Tasks (MMLU)**:
- Smaller gains (+2-2%)
- Self-distillation less beneficial for fact recall
- Teacher trajectory often equally uncertain

**Generation Quality (AlpacaEval)**:
- Significant gains (+5%)
- Self-distillation improves stylistic coherence
- Multi-trajectory generation increases diversity

---

## Practical Applications & Use Cases

### LLM Adaptation Scenarios

1. **Efficient Fine-Tuning**:
   - Task: Adapt Llama-2-7B for domain-specific reasoning
   - Traditional: Full-parameter fine-tuning with 10K labeled examples
   - UniSD: Self-distillation on 5K unlabeled examples
   - Result: 4-5% improvement with half the labeled data requirement
   - Benefit: Reduced annotation cost and time-to-deployment

2. **Continuous Model Improvement**:
   - Task: Iteratively improve a deployed LLM using user interactions
   - Traditional: Collect feedback, manually annotate, retrain
   - UniSD: Generate trajectories, filter by agreement, self-distill
   - Result: Incremental improvements without external supervision
   - Benefit: Perpetual model improvement cycle

3. **Cross-Domain Transfer**:
   - Task: Adapt model from general domain to medical/legal domain
   - Traditional: Requires domain expert annotation
   - UniSD: Self-distillation on domain corpus without labels
   - Result: 3-4% improvement in domain-specific tasks
   - Benefit: Faster domain adaptation with minimal annotation

### Real-World Implementation Examples

**Example 1: Medical QA System**
```
Scenario: Deploy Llama-2-7B for medical question answering
Challenge: Limited labeled medical data, need high accuracy

Solution with UniSD:
├─ Step 1: Generate 3 trajectories per query using sampling
├─ Step 2: Filter by agreement (threshold: 70%)
│   └─ Keep only queries where ≥2/3 trajectories agree
├─ Step 3: Self-distill with medical corpus (10K queries)
└─ Step 4: Deploy improved model

Results:
├─ Baseline accuracy: 72.1%
├─ After self-distillation: 76.8% (+4.7%)
├─ Improvement comparable to 5K expert annotations
└─ No manual annotation required!

Deployment:
├─ Model size: 7B (unchanged)
├─ Latency: <500ms per query
├─ Cost: Training only, no annotation
└─ Maintenance: Can continuously self-improve
```

**Example 2: Code Generation System**
```
Scenario: Improve code generation for HumanEval-style tasks
Challenge: Need pass rate improvement, limited training examples

Solution with UniSD:
├─ Generate multiple code solutions per problem
├─ Filter by execution correctness (agreement)
├─ Self-distill on filtered solutions
└─ Update deployed model

Results:
├─ Pass@1: 29.3% → 34.1% (+4.8%)
├─ Pass@5: 45.2% → 51.1% (+5.9%)
└─ Improvement without new training data!

Benefits:
├─ Faster iteration on model improvements
├─ No need to curate correct solutions
└─ Automated quality control via agreement filtering
```

**Example 3: Reasoning Task Improvement**
```
Scenario: MATH problem-solving improvement for student tutoring
Challenge: Need accurate step-by-step reasoning explanations

Solution with UniSD:
├─ Generate multiple solution trajectories
├─ Keep trajectories where majority reaches correct answer
├─ Self-distill reasoning patterns
└─ Deploy for tutoring

Results:
├─ Accuracy: 17.4% → 22.1% (+4.7%)
├─ Reasoning quality: Subjective improvement in explanations
└─ Fewer hallucinated mathematical steps

Application:
├─ Student tutoring system
├─ Automated homework grading
└─ Math problem generation
```

### Broader Applications

- **Domain Adaptation**: Healthcare, finance, legal domains
- **Multilingual Models**: Self-distill in low-resource languages
- **Instruction Tuning**: Improve instruction-following without external judges
- **Alignment**: Improve safety properties through self-distillation

---

## Insights & Implications

### Theoretical Insights

1. **Self-Supervision Viability**: 
   - Challenges previous assumptions that models can't learn from themselves
   - Shows that with proper filtering and stabilization, self-supervision works
   - Suggests self-distillation as fundamental optimization principle

2. **Stability Requirements**:
   - Three mechanisms critical for stability: EMA, KL clipping, contrastive learning
   - Single mechanisms insufficient; complementary components necessary
   - Aligns with optimization theory on non-convex optimization

3. **Task Dependency**:
   - Reasoning tasks benefit most from self-distillation
   - Factual tasks show diminishing returns
   - Suggests self-distillation fits specific problem structures

### State-of-the-Art Implications

1. **Beyond Supervised Fine-Tuning**: 
   - Challenges assumption that external supervision always better
   - Shows semi-supervised approaches viable for LLMs
   - Opens new directions in model adaptation

2. **Reduced Annotation Dependency**:
   - Enables model improvement without human annotation
   - Critical for domains lacking sufficient labeled data
   - Democratizes LLM improvement

3. **Efficiency Gains**:
   - Improvement comparable to supervised fine-tuning
   - Reduces data requirement by ~50% in some settings
   - Better computational ROI on limited budgets

### Limitations and Open Questions

**Limitations**:
1. **Task Scope**: Best for reasoning; limited gains on factual knowledge
2. **Model Dependency**: Works best on models with reasonable baseline performance
3. **Trajectory Distribution**: Requires diverse self-generated trajectories
4. **Computational Cost**: Multiple trajectories increase generation cost

**Open Research Questions**:

1. **Theoretical Foundation**:
   - What properties of tasks make them amenable to self-distillation?
   - Can we predict a priori which tasks will benefit?
   - Formal convergence analysis for autoregressive models?

2. **Mechanism Optimization**:
   - Optimal agreement thresholds for different tasks?
   - Better filtering methods than simple agreement voting?
   - Adaptive weighting of loss components?

3. **Scalability**:
   - Does self-distillation scale to 100B+ parameter models?
   - How to efficiently generate multiple trajectories for long-form text?
   - Distributed training considerations?

4. **Combining with Other Techniques**:
   - Interaction with LoRA, QLoRA fine-tuning?
   - Combination with reinforcement learning from human feedback (RLHF)?
   - Effect of quantization on self-distillation stability?

---

## Code & Resources

### Official Resources

- **ArXiv Paper**: https://arxiv.org/abs/2605.06597
- **Implementation**: Expected to be released (check authors' GitHub)

### Dependencies

**Core Libraries**:
- PyTorch 2.0+
- transformers (HuggingFace)
- numpy, scipy
- tensorboard (logging)

**Model Requirements**:
- Llama 2 / Mistral / Qwen model weights
- vLLM or similar for efficient inference (optional but recommended)

### Compute Requirements

**Training**:
- Hardware: Single A100 (40GB) GPU recommended
- For smaller models: A10 (24GB) or RTX 4090 (24GB) acceptable
- Time per epoch: 
  - 7B model: 30-60 minutes
  - 13B model: 60-120 minutes

**Inference**:
- GPU Memory: 8-16GB (for 7B model)
- Latency: 50-200ms per query (depends on length)

**Dataset Storage**:
- MATH dataset: 150MB
- BBH: 50MB
- Full evaluation suite: ~1GB

### Quick-Start Code

```python
# Pseudo-code for UniSD training
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b")

# Initialize teacher (EMA)
teacher_model = copy.deepcopy(model)
ema_alpha = 0.9999

# Training loop
def self_distillation_step(batch_input, batch_target):
    # Generate multiple trajectories
    trajectories = []
    for temp in [0.6, 0.8, 1.0]:
        outputs = model.generate(
            batch_input, 
            temperature=temp, 
            max_length=256
        )
        trajectories.append(outputs)
    
    # Compute agreement and filter
    agreement_scores = compute_agreement(trajectories, batch_target)
    mask = agreement_scores > threshold
    
    # Compute losses
    loss_task = task_loss(model(batch_input), batch_target)
    loss_contrast = contrastive_loss(
        model.get_hidden_states(),
        teacher_model.get_hidden_states()
    )
    loss_match = feature_match_loss(model, teacher_model)
    loss_kl = kl_div_clipped(model, teacher_model, threshold=10.0)
    
    # Combined loss
    total_loss = (
        0.5 * loss_task + 
        0.2 * loss_contrast + 
        0.2 * loss_match + 
        0.1 * loss_kl
    )
    
    # Update student
    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()
    
    # Update teacher via EMA
    with torch.no_grad():
        for param_s, param_t in zip(
            model.parameters(), 
            teacher_model.parameters()
        ):
            param_t.data = ema_alpha * param_t.data + \
                          (1 - ema_alpha) * param_s.data
    
    return total_loss.item()

# Training
for epoch in range(num_epochs):
    for batch in train_loader:
        loss = self_distillation_step(batch['input'], batch['target'])
```

---

## Related Work & Context

### Related Recent Papers

1. **Knowledge Distillation**:
   - "Distilling the Knowledge in Neural Networks" (Hinton et al., 2015)
   - "DistiLLM: Towards Streamlined Distillation for Large Language Models" (2024)
   - "Self-Data Distillation for Recovering Quality in Pruned LLMs" (2024)

2. **Self-Supervision and Contrastive Learning**:
   - "SimCLR: A Simple Framework for Contrastive Learning" (2020)
   - "MoCo: Momentum Contrast for Unsupervised Visual Representation Learning"
   - "Token-Level Contrastive Learning" (2023)

3. **LLM Adaptation**:
   - "LoRA: Low-Rank Adaptation of Large Language Models" (2021)
   - "RLHF: Learning from Human Preferences" (Ouyang et al., 2022)
   - "Prompt Tuning and Prefix Tuning" (2021)

4. **Stability in Training**:
   - "Layer Normalization" (Ba et al., 2016)
   - "Deep Residual Learning for Image Recognition" (He et al., 2015)
   - "Gradient Clipping and Normalization" techniques

### Prior Work Foundations

- **Transformer Architecture**: Vaswani et al., 2017
- **Language Model Pre-training**: Devlin et al. (BERT), Radford et al. (GPT)
- **Instruction Tuning**: Wei et al., 2021; Ouyang et al., 2022
- **Distillation Theory**: Hinton et al., 2015; Romero et al., 2014

### Future Research Directions

1. **Enhanced Filtering**:
   - Machine learning-based trajectory quality prediction
   - Confidence calibration for automatic threshold selection
   - Uncertainty-aware filtering using Bayesian methods

2. **Advanced Mechanisms**:
   - Hierarchical self-distillation (layer-wise, block-wise)
   - Progressive self-distillation with curriculum learning
   - Multi-task self-distillation across domains

3. **Scalability**:
   - Distributed self-distillation for 100B+ models
   - Efficient trajectory generation (caching, early-exit)
   - Online adaptation with streaming data

4. **Integration**:
   - Self-distillation + RLHF combination
   - Self-distillation for alignment and safety
   - Multi-agent collaborative self-distillation

---

## Summary

UniSD represents a significant advance in self-supervised adaptation of large language models. By systematically addressing the challenges of learning from self-generated trajectories through multi-teacher agreement, EMA stabilization, token-level contrastive learning, and divergence clipping, it demonstrates that models can effectively improve themselves without external supervision. The extensive evaluation across six benchmarks and six models provides compelling evidence that self-distillation is not only theoretically viable but practically valuable for real-world model improvement. With consistent 2-5% improvements and the potential to reduce annotation requirements by half, UniSD opens new avenues for efficient, scalable LLM adaptation and continuous improvement without human supervision.
