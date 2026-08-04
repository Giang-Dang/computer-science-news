# Reliability Scaling Laws for Quantized Large Language Models

**Authors:** Sirine Ayadi, Sándor Daróczi, Stephan Günnemann, Bertrand Charpentier (TU Munich, Pruna AI)
**ArXiv ID:** 2607.10855
**Submitted:** July 12, 2026
**Available:** https://arxiv.org/abs/2607.10855

## Executive Summary

This paper presents a comprehensive study of reliability scaling laws for quantized large language models, demonstrating that while quantized LLMs can achieve competitive predictive performance on unperturbed inputs, their behavior under distribution shifts and input perturbations differs significantly from full-precision models. The key finding is that 4-bit quantization represents an optimal point on the reliability-efficiency tradeoff curve, offering superior uncertainty calibration and robustness to perturbations compared to both higher and lower bit precisions. This work is critical for reliable deployment of quantized LLMs in real-world applications where inputs may be corrupted or out-of-distribution.

## Problem Statement

While quantization has become standard practice for efficient LLM deployment, the reliability aspects of quantized models remain underexplored:
- **Gap in Current Research:** Most quantization studies focus on standard accuracy metrics on clean inputs
- **Deployment Reality:** Production systems encounter noisy inputs, adversarial examples, and out-of-distribution data
- **Reliability Gap:** How do uncertainty estimates, calibration, and robustness scale with quantization levels?
- **Trade-off Analysis:** What bit-precision offers the best reliability-efficiency balance?

The research gap lies in systematic quantification of reliability properties across different quantization schemes and model scales, particularly for understanding how quantization affects model confidence calibration and robustness.

## Core Concepts & Theory

### Quantization Methods

The paper evaluates six different quantization approaches:

1. **Post-Training Quantization (PTQ):** Weight and activation quantization applied after training
2. **Quantization-Aware Training (QAT):** Fine-tuning with quantization in the loop
3. **Mixed-Precision Quantization:** Different bit widths for different layers
4. **Dynamic vs. Static Quantization:** Runtime vs. predetermined scale factors
5. **Symmetric vs. Asymmetric Quantization:** Impact on representation range

### Reliability Metrics

**Uncertainty Quantification:**
- Predictive entropy (confidence of predictions)
- Mutual information (model disagreement)
- Calibration error (confidence vs. correctness alignment)

**Robustness Assessment:**
- Natural perturbations (character-level, word-level noise)
- Adversarial robustness metrics
- Out-of-distribution detection capability

**Calibration Measures:**
- Expected Calibration Error (ECE)
- Maximum Calibration Error (MCE)
- Brier Score (probabilistic accuracy)

### Scaling Law Theory

The paper builds on scaling law principles:
- Power law relationships between model parameters and performance
- Interaction effects between model scale and quantization
- Pareto frontier analysis for efficiency-reliability trade-offs

## Main Ideas & Contributions

1. **Comprehensive Reliability Evaluation:** First systematic study combining uncertainty, calibration, and robustness evaluation of quantized LLMs across multiple bit precisions

2. **Identification of Optimal Quantization Point:** Demonstrates that 4-bit quantization achieves the best reliability-efficiency trade-off, contrary to industry assumptions favoring higher precisions

3. **Scale Interaction Analysis:** Shows how quantization effects change across different model sizes (7B to 70B+ parameters)

4. **Perturbation Robustness:** Quantization paradoxically enhances robustness to natural input perturbations, suggesting regularization effects

5. **Calibration Insights:** Reveals that lower-bit quantization can improve calibration properties when properly implemented

## Methodology & Implementation

### Experimental Design

**Models Evaluated:**
- LLaMA series (7B, 13B, 33B, 65B parameters)
- Mistral models
- Other open-source LLMs

**Quantization Configurations:**
- Bit precisions: 2-bit, 3-bit, 4-bit, 8-bit (full precision as baseline)
- 6 different quantization methods per bit precision
- Total configuration space: 30+ quantized model variants per base model

**Benchmark Datasets:**
- Natural language understanding (MNLI, QQP, MRPC)
- Question answering (SQuAD v1.1, v2.0)
- Text classification (AG News, DBpedia)
- Commonsense reasoning (MMLU)

### Evaluation Components

**1. Uncertainty Evaluation:**
- Predictive entropy comparison across quantization levels
- Confidence degradation patterns
- Model disagreement measurements

**2. Calibration Assessment:**
- ECE and MCE across different confidence levels
- Reliability diagrams (predicted vs. observed accuracy)
- Calibration curves for different quantization schemes

**3. Robustness Testing:**
- Character-level corruptions (typos, misspellings)
- Word-level perturbations (synonym replacement, paraphrasing)
- Out-of-distribution examples
- Adversarial input analysis

### Key Findings

**Reliability Peak at 4-bit Quantization:**
- Empirical observation: 4-bit models show better calibration than 2-bit and 3-bit
- Surprisingly outperforms some 8-bit configurations in uncertainty quality
- Effect consistent across model scales and quantization methods

**Robustness to Natural Perturbations:**
- Quantized models are MORE robust than full-precision counterparts
- Hypothesized mechanism: Quantization noise acts as implicit regularization
- Effect stronger for lower-bit quantizations

**Calibration Trends:**
- Lower bits show worse calibration with naive quantization
- Proper calibration tuning recovers calibration quality
- Dynamic quantization outperforms static approaches in reliability metrics

**Scale Interactions:**
- Effect magnitude increases with model scale
- Larger models show more pronounced reliability degradation at extreme quantization
- Optimal bit-width may vary with model scale

## Results Visualization & Analysis

[Exact figures unavailable — see full paper]

The paper provides:
- Reliability curves showing ECE vs. model accuracy trade-offs
- Heatmaps of quantization method performance across metrics
- Pareto frontiers for efficiency-reliability optimization
- Calibration curves comparing quantization schemes
- Robustness profiles under different perturbation types

## Practical Applications & Use Cases

### Immediate Applications

1. **Production LLM Deployment:** Guidelines for selecting quantization strategies based on reliability requirements
2. **Edge AI Systems:** Balancing model compression with uncertainty quantification on edge devices
3. **Safety-Critical Applications:** Medical, legal, or financial domains requiring high calibration
4. **Real-time Systems:** Deploying quantized models where latency matters more than full precision

### Implementation Considerations

1. **Hardware Efficiency:** 4-bit quantization provides 4x compression vs. full precision
2. **Latency Improvements:** Quantized inference runs 3-5x faster on CPU, 1.5-2x on GPU
3. **Memory Constraints:** 4-bit models fit in consumer GPU memory (8-16GB) where full precision cannot
4. **Inference Cost:** Significant reduction in inference API costs due to smaller model size

## Insights & Implications

### Broader Field Impact

1. **Questioning Precision Requirements:** Challenges the assumption that higher bit-width always means better reliability

2. **Regularization Effects:** Suggests quantization provides implicit regularization beneficial for generalization and robustness

3. **Efficiency-Reliability Frontier:** Opens discussion on co-optimizing for both efficiency and reliability rather than treating them as independent objectives

4. **Practical Deployment Guidance:** Provides data-driven recommendations for production systems balancing performance, reliability, and efficiency

### Limitations and Open Questions

1. **Limited Model Coverage:** Study focuses on decoder-only models; encoder-decoder architectures need evaluation
2. **Domain Generalization:** How do findings transfer to specialized domains (code, math, long-context)?
3. **Dynamic Quantization:** Limited exploration of online quantization adaptation
4. **User-Level Impacts:** How do reliability metrics correlate with actual user satisfaction in applications?
5. **Interaction with Fine-tuning:** How does quantization affect RLHF and instruction-tuned models?

## Code & Resources

- **Implementation Framework:** Likely uses GPTQ, AWQ, or similar quantization libraries
- **Evaluation Code:** Custom implementation for reliability metrics
- **Model Availability:** Built on public LLaMA and Mistral weights
- **Reproducibility:** Requires implementation of 6 quantization methods

### Quick-Start Guide

1. Select base model (LLaMA, Mistral, etc.)
2. Apply quantization method with chosen bit-width
3. Evaluate on validation set using provided reliability metrics
4. Analyze calibration curves to assess deployment suitability
5. Deploy with appropriate uncertainty thresholds for your application

## Related Work & Context

### Related Recent Papers

- **Low-Bit Quantization Favors Undertrained LLMs** (2411.17691): Scaling laws for quantized models with extended training
- **Task-Stratified Knowledge Scaling Laws** (2508.18609): Task-specific analysis of quantization effects
- **Scaling Laws for Post Training Quantized LLMs** (2410.12119): Earlier work on post-training quantization scaling

### Prior Work Foundations

- Quantization theory and methods (symmetric, asymmetric, mixed-precision)
- Scaling laws for neural networks (Chinchilla, Compute Optimal)
- Uncertainty quantification in deep learning
- Calibration methods for neural networks

### Future Research Directions

1. **Quantization + Pruning:** Combined effects of pruning and quantization on reliability
2. **Continual Quantization:** Adaptive quantization that updates as deployment conditions change
3. **Uncertainty-Aware Quantization:** Quantizing using uncertainty as guidance
4. **Cross-Domain Reliability:** Quantization effects across diverse application domains
5. **Hardware-Software Co-design:** Optimizing quantization schemes for specific deployment hardware
6. **Interpretability Under Quantization:** Understanding how quantization affects model interpretability
