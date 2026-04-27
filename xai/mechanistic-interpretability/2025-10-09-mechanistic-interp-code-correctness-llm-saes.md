# Mechanistic Interpretability of Code Correctness in LLMs via Sparse Autoencoders

**ArXiv ID:** [2510.02917](https://arxiv.org/abs/2510.02917)  
**Authors:** Kriz Tahimic, Charibeth Cheng (De La Salle University, Philippines)  
**Date:** October 9, 2025 (Published ICLR 2026)  
**Subfield:** Mechanistic Interpretability  
**Keywords:** sparse autoencoders, code LLMs, code correctness, Gemma-2, MBPP, activation steering, mechanistic interpretability

---

## Executive Summary

LLMs are increasingly generating code that enters production software, yet their internal mechanisms for evaluating code correctness remain opaque. This ICLR 2026 paper applies sparse autoencoders to the internals of Gemma-2 on coding tasks, identifying specific feature directions that correspond to code correctness detection and correction. The work reveals that models employ two distinct mechanisms — detection (predicting incorrect code) and correction (fixing errors) — with surprising tradeoffs between them, and that successful code generation depends mechanistically on attending to test cases rather than problem descriptions.

---

## Problem Statement

AI-generated code is increasingly deployed in critical software systems, with reports suggesting 20-40% of code in some organizations is now AI-generated. Understanding *when* and *why* LLMs generate incorrect code is essential for:
- Safe deployment of AI coding assistants
- Automatic program repair systems
- Code review automation

**The core interpretability challenge:**
1. LLMs generate both correct and incorrect code with high confidence
2. We cannot predict which outputs are trustworthy without executing them
3. Standard output-level methods (beam search, temperature tuning) treat generation as a black box

**The key question:** Are there internal representations in LLMs that correspond to "this code is correct/incorrect"? If so, can we leverage them to improve reliability?

**Prior work limitations:**
- Static analysis approaches don't generalize to novel bugs
- Probing classifiers show information is present but can't explain the mechanism
- No prior work traced *how* code correctness information flows through LLM computations

---

## Core Concepts & Theory

### Sparse Autoencoders for Feature Discovery

Given residual stream activations $\mathbf{x} \in \mathbb{R}^d$ at the final prompt token, an SAE learns:

$$\mathbf{h} = \text{ReLU}(\mathbf{W}_e \mathbf{x} + \mathbf{b}_e), \qquad \hat{\mathbf{x}} = \mathbf{W}_d \mathbf{h} + \mathbf{b}_d$$

with training objective:
$$\mathcal{L} = \|\mathbf{x} - \hat{\mathbf{x}}\|_2^2 + \lambda \|\mathbf{h}\|_1$$

The L1 penalty encourages **monosemanticity**: each feature (column of $\mathbf{W}_d$) tends to activate for one coherent concept.

### Detection vs. Correction Directions

The paper makes a fundamental distinction between two types of directions in the SAE latent space:

**Predictor directions** (detection): Feature vectors that activate more strongly for incorrect code than correct code. Selected using **t-statistics** comparing activation distributions:
$$t_i = \frac{\mu_{\text{incorrect},i} - \mu_{\text{correct},i}}{\sqrt{s^2_{\text{incorrect},i}/n_1 + s^2_{\text{correct},i}/n_2}}$$

**Steering directions** (correction): Feature vectors that, when added to activations, increase the probability of generating correct code. Selected using **separation scores**:
$$\text{sep}_i = \text{cosine\_sim}(\mathbf{W}_{d,i}, \mathbf{c}^* - \mathbf{c}^-)$$

where $\mathbf{c}^*$ is the mean activation for correct code and $\mathbf{c}^-$ for incorrect code.

### Activation Patching

To verify that identified directions are *causally* involved in correctness (not merely correlated), the paper uses **activation patching**: replace the activation at a specific position with the activation from a "corrupted" run and measure the change in output probability.

$$\Delta P = P(\text{correct} | \text{patched activation}) - P(\text{correct} | \text{original activation})$$

A large $\Delta P$ indicates the patched component is causally involved in the correctness prediction.

---

## Main Ideas & Key Contributions

### 1. First SAE-Based Analysis of Code Correctness Mechanisms

The paper provides the first **mechanistic** analysis of how LLMs internally represent code correctness, going beyond probing classifiers to identify specific causal feature directions.

### 2. Detection-Correction Tradeoff Discovery

A key finding: **the directions that best detect incorrect code are NOT the same as the directions that best fix incorrect code.** This detection-correction tradeoff is a fundamental property of the model's representations:

- Detection directions: highly selective for incorrect code features (syntax errors, undefined variables, wrong type usage)
- Correction directions: encode structural properties of correct solutions (indentation patterns, standard library usage, return value conventions)
- Optimizing for one degrades performance on the other

This has profound implications for code repair systems: you cannot simply "negate" the detected-error direction to produce a correction.

### 3. Test Case Attention is Mechanistically Critical

Through attention analysis and activation patching, the paper discovers that **attending to test cases** (rather than the problem description) is the mechanistic driver of successful code generation:

- Models that generate correct code show high attention from the generation tokens to the test case tokens
- Models that generate incorrect code attend primarily to the problem description
- Patching attention to redirect focus toward test cases improves correctness rates

This provides actionable guidance: prompt formats that make test cases more salient should improve LLM coding performance.

### 4. Weight Orthogonalization for Direction Analysis

The paper introduces **weight orthogonalization** to separate entangled features in the SAE: removing the contribution of a dominant direction from the weight matrix $\mathbf{W}_e$ to find orthogonal directions that capture distinct aspects of correctness.

$$\mathbf{W}_e^{\perp} = \mathbf{W}_e - \mathbf{W}_e \mathbf{d}\mathbf{d}^T$$

where $\mathbf{d}$ is the dominant direction. This technique generalizes beyond code to any setting where features are entangled.

---

## Methodology & Implementation

### Model
- **Gemma-2-9B** (primary) — 9B parameter transformer from Google DeepMind
- **Gemma-2-2B** (ablation) — smaller variant for computational efficiency

### Dataset
- **MBPP** (Mostly Basic Python Problems): 374 problems with test cases
- Problems split into: correct generation set (where Gemma-2-9B succeeds) and incorrect generation set
- Human annotation of error types: syntax errors, logic errors, off-by-one errors, wrong algorithm

### SAE Training Details
- Applied to residual stream at the *final prompt token* (position -1, just before generation begins)
- Dictionary size: 65,536 features
- Training: 50K samples (correct and incorrect code mixed)
- Baseline: zero vector (no prompt)
- Sparsity: λ = 10⁻³

### Evaluation Protocol

**Detection evaluation:**
- Train classifier on top predictor directions
- Evaluate on held-out MBPP test problems
- Metric: AUROC for predicting code correctness before execution

**Steering evaluation:**
1. Start with a problem that Gemma-2-9B answers incorrectly
2. Add steering direction (scaled by coefficient $\alpha$) to residual stream at final prompt token
3. Re-generate code and evaluate with test cases
4. Metric: pass@1 improvement over baseline

**Attention analysis:**
- Extract attention maps for all heads across all layers
- Compare attention to test case tokens vs. problem description tokens for correct vs. incorrect generations
- Identify critical attention heads via activation patching

### Results

**Detection:** Top predictor directions achieve 0.81 AUROC on held-out MBPP problems — models reliably represent code correctness internally before generating.

**Steering:**
| Setting | pass@1 Improvement | Disruption (correct→incorrect) |
|---|---|---|
| Predictor directions (detection) | +8% | +21% (harmful) |
| Steering directions (correction) | +19% | +6% |
| Both combined | +15% | +14% |

**Attention finding:** Redirecting attention from problem description to test cases via patching improves pass@1 by 11% on incorrect-generation problems.

### Limitations
- Analysis limited to one model family (Gemma-2)
- MBPP problems are relatively simple; harder competitive programming problems may show different patterns
- Steering at inference time adds computational overhead
- Findings may be specific to Python; other programming languages not tested

---

## Practical Applications & Real-World Use Cases

### AI Coding Assistants (GitHub Copilot, Cursor, etc.)

The detection directions could be deployed as a **real-time correctness indicator**: before showing generated code to the user, compute the predictor direction activation and display a confidence score. High-confidence predictions of incorrectness trigger automatic regeneration or human review flagging.

### Automated Code Review

CI/CD pipelines could use the identified features as a fast pre-screening step before sending code to expensive static analysis tools. The 0.81 AUROC detection accuracy provides meaningful signal for triage.

### Test-Driven Development (TDD) Enhancement

The finding that test case attention is mechanistically critical suggests a prompt engineering improvement: **structure prompts to make test cases maximally prominent** (e.g., present test cases first, then problem description). This is immediately actionable without any model modification.

### Software Security

Security vulnerabilities are a form of code incorrectness. The framework could be extended to identify features associated with specific vulnerability patterns (SQL injection, buffer overflow, command injection), enabling mechanistic security scanning.

### Regulatory Compliance for AI Code Generation

EU Cyber Resilience Act requires secure-by-design software. AI code generation tools that can demonstrate mechanistic analysis of their reliability properties provide stronger evidence of compliance than purely behavioral evaluations.

---

## Insights & Implications

### Mechanistic Basis of LLM Coding Reliability

The paper demonstrates that LLM coding reliability is not purely emergent and opaque — it has identifiable mechanistic components that can be analyzed, monitored, and (partially) controlled. This is a significant advance for building trustworthy AI coding tools.

### The Detection-Correction Duality

The discovery that detection and correction are mechanistically distinct has broad implications beyond code:
- Medical diagnosis AI: detecting an abnormality vs. recommending a treatment may use different circuits
- Financial fraud detection: identifying fraudulent patterns vs. suggesting remediation may be mechanistically separable
- This duality may be a general property of LLM task solving, not just coding

### Test Cases as Mechanistic Anchors

The finding that test cases serve as mechanistic anchors for correctness connects to the broader insight that **task-relevant grounding** (test cases, examples, ground-truth labels) improves LLM performance not just statistically but mechanistically. This suggests new directions for in-context learning research.

### Advancing the ICLR 2026 Interpretability Agenda

This paper was accepted at ICLR 2026, which had a strong interpretability track. It represents the growing maturity of the field: moving from "here's a feature I found" to "here's what causal role this feature plays and how to leverage it."

### Open Questions
- Do the identified features generalize across programming languages (Python → Java, JavaScript)?
- Can the detection-correction tradeoff be reduced by training SAEs on a mixture of correct and incorrect generations?
- Are there analogous detection-correction distinctions in other task domains (math, reasoning, factual recall)?
- Can the attention redirecting technique be implemented efficiently at inference without activation patching?

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2510.02917](https://arxiv.org/abs/2510.02917)
- **OpenReview:** [https://openreview.net/forum?id=FyQPpkASsV](https://openreview.net/forum?id=FyQPpkASsV)
- **Related Tools:**
  - [SAELens](https://github.com/jbloomAus/SAELens)
  - [TransformerLens](https://github.com/neelnanda-io/TransformerLens) for Gemma models
  - [MBPP dataset](https://github.com/google-research/google-research/tree/master/mbpp)

### Reproducing Key Results
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from saelens import SAE
import torch

model = AutoModelForCausalLM.from_pretrained("google/gemma-2-9b")
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-9b")

# Load pretrained SAE on Gemma-2-9B residual stream
sae = SAE.from_pretrained("gemma-2-9b-layer20")  # layer 20 found most informative

def get_correctness_activation(problem_prompt):
    """Get residual stream activation at final prompt token."""
    inputs = tokenizer(problem_prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    # Final prompt token residual stream at layer 20
    return outputs.hidden_states[20][0, -1, :]

def predict_correctness(problem_prompt, predictor_directions, threshold=0.0):
    """Predict if generated code will be correct before generation."""
    activation = get_correctness_activation(problem_prompt)
    sparse_features = sae.encode(activation)
    
    # Compute predictor direction activations
    pred_scores = [sparse_features[d].item() for d in predictor_directions]
    return sum(pred_scores) / len(pred_scores) > threshold

def steer_toward_correct(problem_prompt, steering_directions, alpha=2.0):
    """Steer model toward generating correct code."""
    inputs = tokenizer(problem_prompt, return_tensors="pt")
    
    def steering_hook(module, input, output):
        # Add steering directions to final prompt token
        output[0][:, -1, :] += alpha * steering_directions.sum(0)
        return output
    
    hook = model.model.layers[20].register_forward_hook(steering_hook)
    with torch.no_grad():
        generated = model.generate(**inputs, max_new_tokens=200)
    hook.remove()
    
    return tokenizer.decode(generated[0])
```

---

## Related Work & Context

### Building On
- **Bricken et al. (2023)**: Monosemanticity — foundational SAE work
- **Anthropic (2024)**: Scaling monosemanticity — large-scale SAE on Claude models
- **Conmy et al. (2023)**: Automated circuit discovery in transformers
- **McDougall et al. (2023)**: Copy suppression mechanisms in GPT-2

### Prior Code Interpretability Work
- **Troshin & Chirkova (2022)**: Probing transformers for program semantics
- **Wan et al. (2022)**: What do large language models know about programming?
- **Hellendoorn et al. (2020)**: Code naturalness and language model likelihood

### ICLR 2026 Mechanistic Interpretability Track
This paper contributes to a growing cluster of ICLR 2026 papers applying mechanistic interpretability to specific domains:
- Mathematical reasoning circuits
- Factual recall mechanisms
- In-context learning circuits

### Where This Research Leads
1. **Multi-language analysis**: extending to JavaScript, Java, C++ to identify universal vs. language-specific features
2. **Security feature analysis**: finding features associated with vulnerability patterns
3. **Steering-enhanced code generation**: production systems that steer toward correct features in real time
4. **Test-case-aware prompting**: systematic prompt engineering derived from the attention analysis findings

---

*Sources:*
- [arxiv.org/abs/2510.02917](https://arxiv.org/abs/2510.02917)
- [openreview.net/forum?id=FyQPpkASsV](https://openreview.net/forum?id=FyQPpkASsV)
