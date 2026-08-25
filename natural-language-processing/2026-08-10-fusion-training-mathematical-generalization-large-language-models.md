# Fusion Training for Mathematical Generalization in Large Language Models

**Authors:** Congfeng Cao, Pengyu Zhang, Jelke Bloem  
**Institution:** University of Amsterdam, Institute for Logic, Language and Computation  
**arXiv ID:** 2608.09893  
**Submission Date:** August 10, 2026  
**Conference:** ACL SRW 2026 (ACL Student Research Workshop)  
**Categories:** Computation and Language, Machine Learning

## Executive Summary

This paper presents Thinking Mode Fusion (TMF), a systematic study of training large language models to simultaneously support both concise responses and extended reasoning through long-form thinking. The research analyzes critical hyperparameters including data ratio and training schedule between thinking and non-thinking modes, revealing asymmetric interactions between the two modes that inform optimal training strategies for mathematical reasoning tasks.

## Problem Statement

Recent advances in LLMs have introduced "thinking modes" that enable extended reasoning before answering, inspired by chain-of-thought and similar explicit reasoning techniques. However, several challenges remain:

1. **Trade-off between modes:** It remains unclear how to balance training between concise and reasoning modes
2. **Data ratio optimization:** What proportion of training data should focus on thinking vs. non-thinking modes?
3. **Training schedule interaction:** How do different training schedules affect the quality of both modes?
4. **Asymmetric dynamics:** Do the modes have equal importance, or does one dominate the other?
5. **Generalization:** How do these choices affect mathematical reasoning performance specifically?

The research gap: Systematic study of thinking mode fusion training dynamics to understand optimal configuration for improved mathematical generalization.

## Core Concepts & Theory

### Thinking Mode Fusion (TMF)

TMF unifies two distinct reasoning modes within a single LLM:

**Non-Thinking Mode:**
- Direct answer without intermediate reasoning steps
- Fast inference
- Suitable for simple queries
- Lower latency critical for real-time applications

**Thinking Mode:**
- Extended reasoning chain before final answer
- Slower but potentially more accurate
- Suitable for complex mathematical and analytical problems
- Enables interpretability through reasoning steps

### Training Paradigms

**Parallel Training:**
- Both modes trained simultaneously with shared backbone
- Potential for interference or mutual benefit

**Sequential Training:**
- Thinking mode trained first, then non-thinking
- Different mode-specific curriculum effects

**Interleaved Training:**
- Alternating focus on each mode
- Potential for balancing performance

### Mode Interaction Dynamics

The key insight: modes don't interact symmetrically. Increasing one mode's data emphasis can degrade the other's performance.

## Main Ideas & Contributions

### 1. Systematic Empirical Analysis
- Comprehensive study of data ratios between thinking/non-thinking supervision
- Evaluation of multiple training schedules
- Clear characterization of trade-offs

### 2. Asymmetric Mode Interaction
- **Key finding:** Increasing non-thinking mode data reduces thinking mode accuracy
- Inverse relationship: more concise training interferes with reasoning
- Suggests thinking mode is more fragile or requires sustained focus

### 3. Training Schedule Optimization
- Different schedules modulate the thinking/non-thinking trade-off
- Optimal schedule depends on chosen data ratio
- Provides practical guidance for practitioners

### 4. Mathematical Reasoning Focus
- Evaluation on mathematical problem-solving tasks
- Benchmark construction with multiple data ratios and schedules
- Results specifically relevant to reasoning-critical applications

## Methodology & Implementation

### Experimental Framework

```
LLM Backbone (shared)
        ↓
    ┌───┴───┐
    ↓       ↓
Thinking  Non-Thinking
Mode      Mode
    ↓       ↓
    └───┬───┘
        ↓
    Training Loop
        ↓
    Evaluation
```

### Key Variables

**Data Ratio (non-thinking : total training):**
- Low ratio: emphasize thinking mode (e.g., 20:80)
- Balanced: equal emphasis (e.g., 50:50)
- High ratio: emphasize non-thinking mode (e.g., 80:20)

**Training Schedules:**
1. **Parallel:** Both modes trained with constant data ratios
2. **Curriculum 1:** [Specific schedule from paper]
3. **Curriculum 2:** [Specific schedule from paper]

### Dataset & Evaluation

- **Benchmark:** Mathematical problem-solving tasks
- **Metrics:** [Exact metrics unavailable — see full paper]
  - Likely includes: accuracy, reasoning validity, response conciseness, latency
- **Test sets:** Multiple test configurations for comprehensive evaluation

### Key Results

**Asymmetric Trade-off Pattern:**
- Increasing non-thinking supervision → decreased thinking mode accuracy
- Effect is significant and consistent across schedules
- [Exact percentages unavailable — see full paper]

**Schedule Dependence:**
- Optimal data ratio varies by training schedule
- No single best ratio across all curricula
- Trade-off curves show different slopes for different schedules

**Performance Metrics:**
[Exact figures unavailable — see full paper]

## Practical Applications & Use Cases

### 1. Production LLM Systems
- **Query routing:** Route queries to appropriate mode based on complexity estimation
- **Cost-aware deployment:** Use non-thinking mode for simple queries to reduce latency/cost
- **Accuracy requirements:** Use thinking mode for accuracy-critical tasks

### 2. Educational Systems
- **Student feedback:** Provide reasoning chains for pedagogical value
- **Verification:** Long-form reasoning enables automated checking of student work
- **Scaffolding:** Extended reasoning serves as example for students

### 3. Scientific Computing
- **Theorem proving:** Thinking mode for formal mathematics
- **Problem-solving:** Extended reasoning for complex scientific problems
- **Research assistance:** Transparency for academic integrity

### 4. Business Applications
- **Financial analysis:** Mathematical accuracy critical for financial reasoning
- **Risk assessment:** Extended reasoning for high-stakes decisions
- **Audit trails:** Explicit reasoning for compliance and accountability

### 5. AI Safety & Interpretability
- **Alignment verification:** Inspect reasoning chains for alignment with values
- **Error analysis:** Understand failure modes through reasoning traces
- **Trustworthiness:** Transparency increases human trust in automated systems

## Insights & Implications

### For Model Development

1. **Mode balance is critical:** Naive approaches (equal weighting) may not be optimal
2. **Curriculum matters:** Training order and schedule interact with data ratios
3. **Mathematical reasoning requires focus:** Thinking mode needs dedicated training emphasis
4. **Asymmetry informs design:** The asymmetric interaction suggests architectural insights needed

### For the Field

1. **Reasoning modes aren't free:** Extended reasoning capability requires training trade-offs
2. **Data allocation is strategic:** Optimal configuration depends on target use cases
3. **Joint training is feasible:** Both modes can coexist in single model without severe degradation
4. **Mathematical tasks demand reasoning:** Data ratios must account for task difficulty

### Theoretical Implications

1. **Mode interference suggests shared representations:** Thinking and non-thinking modes may share backbone bottlenecks
2. **Curriculum learning principles apply:** Mode interaction follows curriculum learning dynamics
3. **Specialized reasoning paths:** May benefit from more isolated thinking pathways

## Code & Resources

- **Conference:** ACL SRW 2026 (Student Research Workshop)
- **Reproducibility:** Student research workshop emphasis suggests code/materials will be released
- **Benchmark:** Custom mathematical reasoning benchmark for mode fusion evaluation
- **Implementation:** Likely built on standard LLM training frameworks (HuggingFace, PyTorch)

## Related Work & Context

### Chain-of-Thought Reasoning
- Original CoT papers (Wei et al., 2022)
- Variations and extensions of reasoning traces
- Implicit vs. explicit reasoning

### LLM Training & Fine-tuning
- Instruction tuning
- Preference learning and RLHF
- Multi-task learning in large models

### Mathematical Reasoning in LLMs
- Math benchmarks (GSM8K, MATH, etc.)
- Specialized reasoning architectures
- Verification and correctness checking

### Curriculum Learning
- Training order effects
- Data ratio optimization
- Sequential vs. parallel training

## Future Research Directions

1. **Scaling laws:** How do findings scale to larger models and datasets?
2. **Generalization across tasks:** Do optimal ratios transfer to non-mathematical reasoning?
3. **Hardware constraints:** Latency/memory trade-offs for deployment scenarios
4. **Hybrid approaches:** Could separate heads for each mode improve results?
5. **Automated scheduling:** Meta-learning optimal training schedules
6. **Reasoning quality:** Deeper analysis of reasoning steps and logical validity
7. **User studies:** How do humans evaluate reasoning chains vs. conciseness?

## Conclusion

This paper addresses the practical challenge of training LLMs that excel at both quick responses and deep reasoning. By systematically studying the trade-offs between thinking and non-thinking modes, the work provides actionable insights for practitioners building reasoning-capable LLMs while advancing our understanding of how multiple capabilities can be integrated within single models.
