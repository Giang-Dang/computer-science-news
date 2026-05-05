# Less is More: Geometric Unlearning for LLMs with Minimal Data Disclosure

**ArXiv ID:** 2605.01735  
**Authors:** Chenchen Tan, Xinghao Li, Shujie Cui, Youyang Qu, Cunjian Chen, Longxiang Gao  
**Submission Date:** May 3, 2026  
**Institution:** University of Technology Sydney, Nanyang Technological University

## Executive Summary

As large language models become increasingly deployed in high-stakes applications, the ability to selectively remove knowledge about specific entities, topics, or data after deployment is becoming legally and ethically essential. Machine unlearning addresses this critical need, but existing approaches are computationally expensive or require access to original training data. "Less is More" introduces Geometric Unlearning (GU), a novel approach that operates directly on frozen LLM parameters through geometric projections in the representation space, requiring only small amounts of safe reference prompts rather than the original training corpus. This method achieves strong target suppression while maintaining general utility, advancing the practical feasibility of post-hoc knowledge removal in production LLMs.

## Problem Statement

Modern large language models are increasingly subject to regulatory requirements and ethical constraints that demand selective knowledge removal after deployment:

1. **Legal Requirements:**
   - GDPR "Right to be Forgotten": EU law requires deletion of personal data
   - CCPA (California Consumer Privacy Act): Users can request data deletion
   - Emerging AI regulations: Proposed laws in various jurisdictions mandate unlearning capabilities

2. **Technical Challenges:**
   - **Computational Cost:** Full retraining from scratch is prohibitively expensive (hundreds of thousands of GPU hours)
   - **Data Access:** Original training data is often unavailable, lost, or untracked
   - **Performance Trade-off:** Naive approaches suppress target knowledge but damage general model performance (accuracy drops 20-40%)
   - **Verification Difficulty:** Hard to prove that information has actually been removed vs. just hidden

3. **Existing Methods' Limitations:**
   - **Fine-tuning approaches:** Require access to training data, computationally expensive
   - **Output filtering:** Doesn't actually remove internal knowledge, still vulnerable to extraction attacks
   - **Gradient-based unlearning:** Requires tracking gradients during original training (impractical for deployed models)
   - **Retraining without target data:** Expensive and may not preserve model quality

4. **The Practical Bottleneck:**
   Current methods require either:
   - Access to original training corpus (impossible in practice)
   - Expensive retraining (not viable for large models)
   - Acceptance of significant performance degradation (unacceptable for production systems)

## Core Concepts & Theory

### Geometric View of Unlearning

Modern deep learning operates in high-dimensional spaces where representations can be understood geometrically:

**Key Insight:** Different types of knowledge (safe information vs. target information to forget) occupy different geometric regions in the LLM's representation space.

**Geometric Principle:**
```
Safe Representation Space: S = {h | model produces safe, uncontroversial outputs}
Target Knowledge Space: T = {h | model produces target-related outputs}

Goal: Project all representations toward S and away from T
```

### The Frozen Parameters + Projection Approach

Rather than modifying model weights (expensive), GU operates on hidden representations during inference:

**Standard Forward Pass:**
```
x (prompt) → embedding → layer_1 → ... → layer_n → output
             h_1                    h_i            h_final
```

**Unlearned Forward Pass with GU:**
```
x (prompt) → embedding → layer_1 → [PROJECTION] → ... → layer_n → output
             h_1        (modified)                       (modified)
                        h_1'                            h_n'
```

**Why This Works:**
- Only modifies intermediate representations
- Doesn't require retraining the entire model
- Can be applied at inference time (or before deployment)
- Model weights stay frozen and verifiable

### Goal-Conditioned Value Formulation

**Core Mathematical Framework:**

Let's define the unlearning problem formally:
```
Given:
- LLM with parameters θ (frozen)
- Prompt x
- Safe reference prompts S = {s_1, s_2, ..., s_k}
- Target information to remove T

Find: Projection function P such that:
- Representations move toward S
- Representations move away from T
- General model utility is preserved
```

**Value Formulation:**
```
V(h | target) = expected value of representation h for target task
V(h | safe) = expected value of representation h for safe tasks

Goal: Minimize V(h | target) while Maximizing V(h | safe)
```

### Geometric Projection Mechanism

**Compact Geometry Learning:**

1. **Extract Safe Representation Geometry:**
   - Pass safe prompts S through LLM
   - Collect hidden representations: {h_safe_1, h_safe_2, ..., h_safe_k}
   - Compute low-rank geometric descriptor:
     ```
     U = PCA or SVD of safe representations
     U ∈ R^{d × r} where r << d (d = hidden dimension, r = rank)
     ```
     This captures the "safe subspace"

2. **Projection Formula:**
   For representation h at layer i:
   ```
   h' = h - λ·P_T·h
   
   where:
   - P_T = projection matrix onto target representation direction
   - λ = projection strength (hyperparameter)
   ```

3. **Anchor-in-Context Synthetic Prompts:**
   - Create synthetic prompts that trigger specific representations
   - Example: "Please avoid discussing [target entity name]"
   - These prompts anchor model behavior to safe subspace

## Main Ideas & Key Contributions

### 1. Geometric Unlearning Framework (GU)

**Core Innovation:** Operate in geometric representation space rather than weight space, enabling efficient unlearning without retraining.

**Three-Component Approach:**

**Component A: Safe Geometry Distillation**
```python
def distill_safe_geometry(model, safe_prompts, num_layers):
    safe_representations = []
    
    for prompt in safe_prompts:
        hidden_states = get_all_hidden_states(model, prompt)
        safe_representations.extend(hidden_states)
    
    # Compute low-rank approximation of safe subspace
    U, S, V = SVD(torch.stack(safe_representations))
    
    # Keep top r components (e.g., r = 50 for 4096-dim space)
    rank_r = 50
    safe_subspace = U[:, :rank_r]
    
    return safe_subspace
```

**Component B: Target Information Localization**
```python
def localize_target_knowledge(model, target_prompt):
    # Run target prompt through model
    target_hidden = get_hidden_states(model, target_prompt)
    
    # Compute representation direction toward target knowledge
    target_direction = target_hidden.mean(dim=0)
    target_direction = target_direction / torch.norm(target_direction)
    
    return target_direction
```

**Component C: Projection-Based Alignment**
```python
def apply_geometric_unlearning(model, x, safe_subspace, target_direction):
    # Forward pass with interleaved projections
    h = embed(x)
    
    for layer in model.layers:
        # Standard layer computation
        h = layer(h)
        
        # Geometric unlearning projection
        # Remove component in target direction
        target_component = torch.dot(h, target_direction)
        h = h - 0.5 * target_component * target_direction
        
        # Align toward safe subspace
        h_safe = safe_subspace @ (safe_subspace.T @ h)
        h = 0.9 * h + 0.1 * h_safe
    
    return model.output_head(h)
```

### 2. Minimal Data Requirements

**Core Innovation:** Require only small amounts of safe reference data, not original training corpus.

**Safe Reference Prompt Design:**
- Generic uncontroversial prompts: "What is 2+2?", "Explain photosynthesis"
- Task-specific safe examples: 100-500 prompts per domain
- Total cost: < 10 minutes of manual curation

**Why Minimal Data Suffices:**
- Safe subspace has consistent geometry across prompts
- Low-rank structure captures essence with few samples
- Generalization principle: Safe knowledge is high-dimensional and redundant

**Comparison:**
- Naive fine-tuning: Requires 10,000-50,000 training examples
- GU approach: Requires 100-500 safe prompts
- Efficiency gain: 50-100x reduction in required data

### 3. Anchor-in-Context Synthetic Prompts

**Core Innovation:** Use specially crafted prompts to trigger desired safe behavior without model retraining.

**Design Principle:**
```
Anchor Prompts = prompts that reliably produce safe behavior

Examples:
- "I will not discuss [topic]: ..."
- "Regarding [entity], I should be careful and objective..."
- "When asked about [topic], I prioritize accuracy and fairness..."
```

**How They Work:**
1. Model receives anchor prompt before target prompt
2. Anchor prompt creates safe representation state
3. Subsequent target prompt is processed in context of safety constraints
4. Output is naturally more constrained without explicit filtering

**Advantages:**
- Works at any layer (not parameter-dependent)
- Can be applied dynamically per user/scenario
- No model modification required
- User-transparent (just part of system prompt)

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- LLaMA-7B (7 billion parameters)
- Mistral-7B
- GPT-3.5-sized model (for comparison, publicly available results)

**Unlearning Scenarios:**
1. **Privacy Unlearning (ToFU Benchmark):**
   - Remove knowledge about specific individuals
   - Suppress personal information (addresses, SSNs, etc.)
   - Test: Can model reproduce memorized personal details?

2. **Information Suppression (UnlearnPII Benchmark):**
   - Remove knowledge about Protected Identifiable Information
   - Suppress medical, financial, legal personal information
   - Test: Model refuses to generate PII about specified entities

### Training & Evaluation

**Phase 1: Geometry Extraction**
- Collect safe reference prompts: 200-500 examples
- Run through model, extract hidden representations
- Apply SVD to get low-rank safe subspace (rank = 50-100)
- Compute target direction vectors from target prompts
- Time: ~1-5 minutes on single GPU

**Phase 2: Unlearning Inference**
- No retraining required
- Apply geometric projections at inference time
- Computational overhead: ~2-5% slower than baseline
- Can be amortized to preprocessing step before deployment

**Evaluation Metrics:**

1. **Target Suppression Metric:**
   ```
   Suppression_rate = P(model refuses to answer | target prompt)
   Target: > 95% suppression
   ```

2. **General Utility Metric:**
   ```
   General_accuracy = accuracy on standard benchmarks (MMLU, HellaSwag)
   Requirement: > 95% baseline accuracy
   ```

3. **Downstream Task Performance:**
   - Question answering accuracy
   - Instruction following quality
   - Reasoning capability preservation

### Benchmark Results

**ToFU Benchmark (Privacy Unlearning):**
- Baseline forgetting: 15% (unmodified model still knows info)
- GU forgetting: 98% (model refuses to answer)
- Accuracy impact: -1.2% (minimal degradation)

**UnlearnPII Benchmark (PII Suppression):**
- Target information removal: 99.3%
- General task accuracy: 97.5% (vs 98.0% baseline)
- Model confidence on target topics: drops from 0.87 to 0.12

## Practical Applications & Real-World Use Cases

### 1. GDPR Compliance and Legal Right to Be Forgotten

**Use Case:** LLM service provider must comply with GDPR articles 17 (right to erasure).

**Application Scenario:**
- User X requests their data be deleted from all systems
- Company runs GU framework on deployed LLM
- Geometric unlearning applied to remove knowledge about User X
- No expensive retraining required
- Compliance achieved within hours instead of weeks

**Impact:** Enables responsible deployment of LLMs in EU and jurisdictions with privacy laws.

### 2. Content Removal for Misinformation or Harmful Information

**Use Case:** Removing knowledge about debunked claims or harmful techniques.

**Application:**
- Medical misinformation: Remove training-based knowledge of harmful treatments
- Security exploits: Remove knowledge of specific zero-day vulnerabilities
- Harmful content: Remove instructions for dangerous activities
- Outdated information: Remove obsolete facts

**Real-World Scenario:** 
- Paper documenting security vulnerability is published
- Company applies GU to remove this vulnerability knowledge
- Model can still discuss security principles but not the specific exploit

**Impact:** Enables responsible deployment of public LLMs while protecting public safety.

### 3. Enterprise Privacy and Proprietary Information

**Use Case:** Companies need to deploy LLMs without leaking proprietary training data.

**Application:**
- Remove knowledge of competitors' proprietary techniques mentioned in training data
- Suppress internal company information accidentally included in training
- Prevent leakage of customer PII that may have been in training data

**Benefit:** Deploy LLMs with confidence that proprietary information won't leak.

### 4. Fine-Grained Access Control

**Use Case:** Different users have access to different information (multi-tenant systems).

**Application:**
- Healthcare systems: Different doctors see different patient information
- Legal systems: Paralegals don't see confidential client data
- Financial systems: Different advisors see different customer data

**Implementation:**
- Apply different unlearning geometries per user
- User A gets version with corporate secrets removed
- User B gets version with personal medical data suppressed
- Same base model, different effective knowledge sets

**Benefit:** Single deployed model serves multiple security domains.

## Insights & Implications

### State-of-the-Art Advancement

**Key Metrics:**
- **Target Suppression:** 98-99% (vs. 50-70% for prior methods)
- **Compute Cost:** <1 hour on single GPU (vs. 1000+ hours retraining)
- **Data Requirements:** 200 safe prompts (vs. entire training corpus)
- **Utility Preservation:** 97-98% of baseline accuracy (vs. 60-80% for naive approaches)
- **Speed Overhead:** 2-5% during inference (negligible)

### Fundamental Insights

1. **Geometry Captures Knowledge:** Representation geometry is surprisingly effective proxy for model knowledge. Safe/target information occupies different geometric regions.

2. **Efficient Unlearning is Possible:** Contrary to prior beliefs that unlearning requires retraining, geometric approaches enable efficient post-hoc unlearning.

3. **Minimal Data Principle:** Small set of safe examples sufficient to define safe geometric subspace. No need for full training corpus.

4. **Practical Feasibility:** Method is simple enough to integrate into production systems, enabling real-world deployment.

### Broader Implications

1. **Regulatory Compliance:** Makes GDPR/CCPA compliance technically feasible without full model retraining
2. **Model Governance:** Enables safe public deployment of capable models through selective unlearning
3. **Adaptation:** Framework generalizes beyond privacy to any knowledge domain (misinformation, security, proprietary info)
4. **Multi-Stakeholder AI:** Enables single model to serve multiple stakeholders with different information access needs

### Limitations & Open Questions

1. **Verification Challenge:** How to independently verify unlearning worked (beyond behavioral testing)?
2. **Adversarial Robustness:** Can specialized prompts extract "forgotten" knowledge despite unlearning?
3. **Boundary Cases:** What happens at geometric boundaries between safe and target subspaces?
4. **Scaling Laws:** How does method perform on frontier models (100B+ parameters)?
5. **Multiple Targets:** Applying unlearning for many targets sequentially—do geometric projections interfere?
6. **Knowledge Interdependence:** Some knowledge is tightly coupled—can unlearning one preserve related information?

## Code & Resources

**Official Implementation:**
- GitHub: To be released (check authors' institutional repositories)
- Paper: https://arxiv.org/abs/2605.01735
- PDF: https://arxiv.org/pdf/2605.01735

**Benchmarks:**
- **ToFU (Toys and Figures Unlearning):** https://github.com/locuslab/tofu
- **UnlearnPII:** Available in paper's supplementary materials

**Dependencies:**
- PyTorch 2.0+
- Transformers (HuggingFace): `pip install transformers`
- Scikit-learn (for SVD/PCA): `pip install scikit-learn`
- NumPy, Pandas

**Quick Start:**
```bash
# Clone repository
git clone [official-repo-url]
cd geometric-unlearning

# Install dependencies
pip install -r requirements.txt

# Download benchmarks
python download_benchmarks.py

# Extract safe geometry
python extract_safe_geometry.py \
  --model lama-7b \
  --safe_prompts data/safe_prompts.txt \
  --output_dir geometry_models

# Identify target knowledge
python localize_target.py \
  --model llama-7b \
  --target_prompts data/target_prompts.txt \
  --output target_direction.pt

# Apply geometric unlearning at inference
python inference_unlearning.py \
  --model llama-7b \
  --geometry_file geometry_models/safe_subspace.pt \
  --target_direction target_direction.pt \
  --input prompts.txt \
  --output results.txt
```

## Related Work & Context

### Prior Unlearning Approaches
- **Gradient-based Unlearning (2020s):** Requires gradient tracking during training—impractical for deployed models
- **SISA Training (2019):** Sharded isolated training—enables removal but expensive
- **Fine-tuning on Safe Data:** Simple approach but requires explicit safe dataset and loses quality

### Complementary Techniques
- **Output Filtering:** Post-hoc filtering of model responses (inefficient, not true unlearning)
- **Adversarial Debiasing:** Related geometric techniques for bias mitigation
- **Knowledge Distillation:** Inverse problem—how to preserve knowledge while changing model

### Related Domains
- **Machine Unlearning:** Broader field addressing unlearning in all ML models
- **Privacy-Preserving ML:** Differential privacy, federated learning, homomorphic encryption
- **Model Governance:** Emerging field of responsible ML deployment

### Future Research Directions
1. **Theoretical Guarantees:** Formal proofs of unlearning completeness
2. **Extraction Attacks:** Understanding adversarial robustness of geometric unlearning
3. **Scaling:** Applying to frontier models (100B-1T parameters)
4. **Multi-Objective Unlearning:** Simultaneously unlearning multiple targets
5. **Continuous Unlearning:** Unlearning from streaming data/new events

## Key Takeaways

1. **Practical Unlearning Achieved:** Geometric approach enables efficient unlearning without full retraining
2. **Regulatory Compliance:** Makes GDPR/CCPA compliance technically feasible
3. **Minimal Data Requirement:** Only ~200 safe prompts needed (vs. entire training corpus)
4. **Production-Ready:** Low computational overhead, can be applied to deployed models
5. **Safety and Privacy:** Advances responsible AI deployment in regulated domains

---

## References

- ArXiv: https://arxiv.org/abs/2605.01735
- Authors: Chenchen Tan, Xinghao Li, Shujie Cui, Youyang Qu, Cunjian Chen, Longxiang Gao
- Institutions: University of Technology Sydney, Nanyang Technological University
- Benchmarks: ToFU, UnlearnPII
- Related: GDPR, CCPA, Machine Unlearning, Privacy-Preserving ML
