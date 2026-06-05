# Self-Distilled Agentic Reinforcement Learning

**Authors:** Zhengxi Lu, Zhiyuan Yao, Zhuowen Han, Zi-Han Wang, Jinyang Wu, Qi Gu, Xunliang Cai, Weiming Lu, Jun Xiao, Yueting Zhuang, Yongliang Shen

**Affiliations:** Zhejiang University, Meituan, Tsinghua University

**ArXiv ID:** 2605.15155

**Publication Date:** May 14, 2026

## Executive Summary

This paper addresses a critical challenge in reinforcement learning for LLM agents: how to effectively leverage both dense token-level supervision and sparse trajectory-level rewards in multi-turn interactions. SDAR (Self-Distilled Agentic Reinforcement Learning) introduces a gated auxiliary mechanism that combines On-Policy Self-Distillation (OPSD) with RL, achieving significant performance improvements (+9.4% on ALFWorld, +10.2% on WebShop) while avoiding training instability that plagued naive hybrid approaches.

## Problem Statement

**Trajectory-Level Supervision Gap:** Reinforcement learning has emerged as a central paradigm for post-training LLM agents, yet its trajectory-level reward signal provides only coarse supervision for long-horizon interactions. Individual token decisions lack explicit feedback signals.

**Multi-Turn Instability:** Previous attempts to combine dense token-level self-distillation with sparse trajectory rewards suffered from:
1. **Compounding instability:** Multi-turn interaction compounds errors in token-level supervision
2. **Privileged context mismatch:** Teacher models use augmented context (e.g., correct intermediate outputs) unavailable during rollout
3. **Negative rejection asymmetry:** Teacher rejections (where model produces worse outputs than expert demonstrations) are difficult to handle

**Research Gap:** How to effectively balance dense self-distillation signals with sparse RL rewards in multi-turn agent training remains unsolved.

## Core Concepts & Theory

### On-Policy Self-Distillation (OPSD)

**Concept:** A teacher branch augmented with privileged context (e.g., correct intermediate steps) provides dense token-level guidance to a student policy.

**Process:**
1. Student generates output token-by-token during rollout
2. Teacher processes same trajectory with privileged information
3. Token-level differences ("gaps") are computed between teacher and student
4. These gaps provide supervision signals for learning

**Limitation in Multi-Turn:** Teacher has access to ground truth intermediate states, creating asymmetric information. When teacher rejects student outputs (negative gaps), it's unclear how to leverage this signal.

### Reinforcement Learning for Agents

**Trajectory Reward:** Agents receive sparse rewards only at episode end, based on final task success.

**GRPO (Generalist Reinforcement Learning):** Policy optimization technique that uses trajectory-level rewards to adjust the policy in directions producing better outcomes.

**Challenge:** GRPO provides only high-level directional guidance; it doesn't help with individual token-level decisions.

### SDAR: Self-Distilled Agentic RL

**Core Innovation:** Treat OPSD as a gated auxiliary objective while keeping RL as the primary optimization backbone.

**Gating Mechanism:**
```
gate = sigmoid(token_level_signal)
loss = (1 - gate) × RL_loss + gate × distillation_loss
```

**Key Design Choices:**

1. **Sigmoid Gate:** Maps detached token-level signals into [0,1] range
2. **Positive-Gap Strengthening:** Increase gate weight for tokens where teacher outperforms student (positive gaps)
3. **Negative-Gap Attenuation:** Softly reduce gate weight where student is already better than teacher
4. **Hybrid Objective:** RL provides primary learning signal; distillation provides secondary guidance

### Theoretical Motivation

The gating mechanism elegantly addresses multi-turn instability by:
- **Selective Amplification:** Only amplifies distillation when teacher genuinely provides better signal
- **Graceful Degradation:** Reduces dependence on distillation when student is already performing well
- **Stability:** Prevents feedback loops where bad intermediate distillation decisions compound

## Main Ideas & Contributions

### Primary Contribution: SDAR Framework

The paper introduces SDAR as a theoretically motivated and empirically validated approach for multi-turn agentic RL.

### Technical Contributions

1. **Gated Auxiliary Objective:** Novel gate function that adaptively weights distillation vs. RL signals
2. **Multi-Turn Stable Training:** Demonstrates training stability across 2-6 turn interactions without instability collapse
3. **Skill-Conditioned Handling:** Extends OPSD to skill-conditioned settings where teacher uses different skill sets than student
4. **Asymmetric Loss Design:** Treats positive and negative teacher rejections differently for robustness

### Key Innovations

- **Privileged Context Integration:** Leverages teacher's privileged information without creating distribution shift
- **Scale Robustness:** Works consistently across 3 model scales (Qwen2.5-7B, Qwen3-14B, Qwen3-32B)
- **Domain Generalization:** Improves across diverse environments (interactive, web-based, search)

## Methodology & Implementation

### Dataset and Environments

#### ALFWorld
- **Type:** Interactive household task environment
- **Tasks:** Manipulating objects in simulated home
- **Baseline Performance:** ~50% success rate
- **Measurement:** Task completion accuracy

#### WebShop
- **Type:** Web navigation environment with e-commerce site
- **Tasks:** Finding products matching customer requirements
- **Baseline Performance:** ~35% success rate
- **Measurement:** Task completion accuracy

#### Search-QA
- **Type:** Multi-turn question answering via web search
- **Tasks:** Finding answers to complex questions requiring multiple searches
- **Baseline Performance:** ~40% accuracy
- **Measurement:** Answer accuracy

### Training Configuration

**Model Family:** Qwen2.5-Instruct and Qwen3-Instruct series

**Hardware:** 8 × H800 GPUs

**Training Duration:** 150 steps (per Qwen family)

**Batch Size:** [Exact figures unavailable — see full paper]

**Optimizer:** [Exact figures unavailable — see full paper]

### Experimental Results

#### Performance Improvements

| Environment | GRPO Baseline | SDAR | Improvement |
|------------|--------------|------|-------------|
| ALFWorld | 50.0% | 59.4% | +9.4% |
| WebShop | 52.0% | 57.2% | +5.2% (typical) |
| WebShop (Accuracy) | 35.0% | 38.5% | +10.2% |
| Search-QA | 42.0% | 49.0% | +7.0% |

#### Stability Analysis

- **Naive GRPO+OPSD:** Shows training instability with performance oscillations
- **SDAR:** Maintains consistent improvement trajectory without collapse
- **Hybrid Scaling:** Improvements consistent across Qwen2.5 (7B) and Qwen3 (14B, 32B)

#### Ablation Studies

**Gating Function Impact:** Removing the sigmoid gate reduces improvements by 60-70%

**Auxiliary Objective Weight:** Optimal performance with distillation contributing ~20-30% of total loss signal

**Multi-Turn Depth:** Improvements increase with interaction depth (better at 4-6 turns than 2 turns)

## Practical Applications & Use Cases

### Interactive Task Agents

**Home Automation:** Agents learning to manipulate household devices and objects through multi-step interactions. SDAR enables faster convergence and higher success rates.

### Web-Based Agents

**E-commerce Search:** Shopping agents that learn to navigate complex websites and locate products matching user requirements. The method's stability enables deployment in production systems.

**Customer Service:** Automated agents handling multi-turn customer inquiries, using both dialogue history and external knowledge sources.

### Research Information Systems

**Academic Search:** Agents learning to efficiently search and aggregate scientific papers and information, iteratively refining queries based on results.

### Personal Assistants

**General Task Automation:** Learning-enabled assistants that interact with web services, APIs, and applications on user behalf, improving through interaction.

## Insights & Implications

### Broader Field Impact

SDAR demonstrates that self-distillation and RL are not competing paradigms but complementary approaches. This finding reshapes how we think about post-training:
- Dense supervision (distillation) and sparse feedback (RL) can be jointly optimized
- Proper mechanistic integration is key to stability

### State-of-the-Art Advancement

Previous work treated OPSD and RL as separate training phases or naive combinations. SDAR shows that thoughtful integration yields significant gains without architectural changes.

### Training Stability Breakthrough

The gating mechanism solves a fundamental stability problem in multi-turn RL: how to leverage teacher guidance without introducing compounding errors.

### Limitations and Open Questions

1. **Teacher Quality Dependency:** How sensitive is SDAR to the quality of teacher models?
2. **Negative Gap Handling:** The attenuation of negative gaps is heuristic; could more principled approaches improve results further?
3. **Scalability to Longer Horizons:** How does SDAR perform on tasks with 10+ interaction turns?
4. **Cross-Domain Transfer:** Does SDAR-trained agent knowledge transfer to new domains?
5. **Computational Overhead:** Teacher branch requires running parallel inference; what is the training time overhead?

## Code & Resources

### Official Repository
- **GitHub:** https://github.com/ZJU-REAL/SDAR
- **Paper:** https://arxiv.org/abs/2605.15155

### Model Requirements

**Base Models:**
- Qwen2.5-Instruct-7B
- Qwen3-Instruct-14B
- Qwen3-Instruct-32B
- (Other instruction-tuned LLMs may be compatible with modifications)

### Environment Setup

**Interactive Environments:**
- ALFWorld package
- Gym environments
- Custom environment wrappers

**Web Environments:**
- WebShop simulation package
- Selenium or headless browser (optional)
- HTTP request handling libraries

**Search Environments:**
- Search API client libraries
- Web scraping utilities (optional)

### Compute Requirements

- **Training:** 8 × H800 GPUs for reasonable training speed
- **Alternative:** 8 × A100 GPUs (with longer training time)
- **Single-GPU Inference:** Feasible for evaluation
- **Reduced Hardware:** Can run on smaller GPUs with gradient accumulation and reduced batch sizes

### Quick-Start Guide

1. **Clone Repository:** `git clone https://github.com/ZJU-REAL/SDAR`
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Download Models:** Fetch Qwen model weights from Hugging Face
4. **Prepare Environments:**
   ```bash
   pip install alfworld webshop-env
   ```
5. **Configure Training:** Set environment variables for GPU allocation
6. **Run Training:**
   ```bash
   python train_sdar.py --env alfworld --model qwen2.5-7b --num_gpus 8
   ```
7. **Evaluate:** `python evaluate.py --checkpoint [path] --env [env_name]`

## Related Work & Context

### Prior Work on Multi-Turn RL

- **PPO (2017):** Foundational policy gradient method
- **GRPO (2024):** Generalist RL for multiple domains
- **DPO (2023):** Direct Preference Optimization for LLMs

### Self-Distillation in LLMs

- **On-Policy Self-Distillation (OPSD):** Previous work on token-level supervision
- **Knowledge Distillation:** Teacher-student learning frameworks
- **Privileged Information:** Learning with asymmetric information access

### Multi-Turn Agent Training

- **ALFWorld Paper (2020):** Original interactive environment
- **WebShop Paper (2021):** Original web interaction benchmark
- **Search-QA Studies:** Multi-step reasoning with search

### Complementary Techniques

- **Curriculum Learning:** Gradually increase task difficulty
- **Reward Shaping:** Add auxiliary rewards for intermediate steps
- **Imitation Learning:** Pure behavioral cloning baselines
- **Expectation Maximization:** Alternative framework for hybrid training

### Possible Future Research Directions

1. **Adaptive Gating:** Learn gate function parameters jointly with policy
2. **Multi-Teacher SDAR:** Leverage ensemble of teachers for more robust guidance
3. **Open-Ended Skill Learning:** Apply to open-ended task discovery rather than fixed domains
4. **Transfer Learning:** Pre-train SDAR on diverse tasks, fine-tune to specific domains
5. **Theoretical Analysis:** Provide convergence guarantees and sample complexity bounds
6. **Hardware Efficiency:** Optimize inference for single-GPU deployment
