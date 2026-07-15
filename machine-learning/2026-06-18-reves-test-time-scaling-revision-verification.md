# REVES: REvision and VErification-Augmented Training for Test-Time Scaling

**ArXiv ID:** 2606.18910  
**Authors:** Northwestern University, Amazon AGI, Qualcomm AI Research, University of Minnesota  
**Submitted:** June 18, 2026  
**Field:** Machine Learning, Large Language Models, Reinforcement Learning  

## Executive Summary

REVES proposes a novel training framework that enables efficient test-time scaling through sequential revision and verification of Large Language Model (LLM) outputs. The work addresses a fundamental misalignment in traditional post-training approaches: optimizing single-shot objectives rather than multi-step inference dynamics. By converting intermediate correctable mistakes from successful recovery trajectories into decoupled revision and verification prompts, REVES enables effective learning from near-miss answers while maintaining computational efficiency. The significance lies in achieving state-of-the-art results on reasoning benchmarks with smaller base models and fewer rollouts than evolutionary search systems, advancing practical deployment of reasoning-capable LLMs.

## Problem Statement

Standard post-training methods for LLMs focus on single-turn, single-shot generation—optimizing the probability of immediate correct answers. This approach fails to exploit the structural properties of LLM reasoning:

1. **Reasoning Complexity:** Complex reasoning problems often require multiple steps with intermediate corrections and verification
2. **Inefficient Learning Signal:** Successful recovery trajectories contain valuable learning signals in intermediate steps that are discarded with traditional approaches
3. **Multi-Turn Overhead:** Naive multi-turn reinforcement learning requires extensive sampling, creating prohibitive computational costs
4. **Misalignment with Test Time:** Training optimizes single-shot answers while test-time practices involve multiple attempts and verification

### The Correction Problem

Consider a response where the model generates an incorrect intermediate answer but later corrects itself through sequential prompting:
- Traditional RL sees the final success but wastes the correctable-but-wrong intermediate step
- REVES extracts this intermediate step as a training signal, learning to transform incorrect answers toward correct ones

## Core Concepts & Theory

### Test-Time Scaling vs. Training-Time Optimization

**Traditional Approach:**
- Training: Optimize P(correct answer | input) with RL
- Test-time: Single forward pass generating answer
- Limitation: Cannot leverage iterative refinement capability

**REVES Approach:**
- Training: Optimize both (1) revision capability and (2) verification ability
- Test-time: Generate → verify → revise → repeat
- Advantage: Scalable multi-step inference with learned strategies

### Two-Stage Iterative Framework

The REVES algorithm operates in two alternating stages:

**Stage 1: Online Data and Prompt Augmentation**
- Sample trajectories from current policy
- Identify successful recovery trajectories (paths that eventually reach correct answer)
- Extract intermediate "near-miss" steps where model produced incorrect but potentially correctable answers
- Create two synthetic training samples:
  - **Revision Prompt:** Input → near-miss answer → prompt to fix
  - **Verification Prompt:** Input + answer candidate → prompt to verify correctness

**Stage 2: Policy Optimization**
- Optimize model on augmented revision and verification datasets
- Learn when to attempt revision vs. accept answers
- Learn to identify errors in candidates through verification
- Maintain off-policy nature by decoupling success from original trajectory

### Key Theoretical Insights

**Why Near-Miss Learning Works:**
- Near-miss answers are semantically close to correct answers (short edit distance)
- Model can learn meaningful transformation from near-miss to correct
- Verification learning provides complementary signal for error detection
- Combined approach creates emergent multi-step reasoning capability

**Computational Efficiency:**
- Avoids sampling multiple long trajectories for each training example
- Extracts multiple training signals from single successful trajectory
- Off-policy formulation allows flexible data utilization
- Reduces sampling overhead vs. standard multi-turn RL

**Off-Policy Data Generation:**
- Successful trajectories can be collected in various ways (stochastic sampling, ensemble voting, etc.)
- Focus on using data efficiently rather than strict on-policy requirement
- Enables combination with existing strong baseline models
- Reduces computational requirements compared to conventional approaches

## Main Ideas & Contributions

### Primary Innovation: Near-Miss Extraction

REVES introduces a novel training paradigm that recognizes the value of **partially correct intermediate steps**:

1. **Revision Learning:** Train models to fix their own mistakes
   - Given: Incorrect answer from model
   - Learn: Transformation toward correct answer
   - Application: Test-time refinement of candidate answers

2. **Verification Learning:** Train models to judge answer correctness
   - Given: Answer candidate and supporting context
   - Learn: Prediction of correctness without generating correct answer
   - Application: Test-time selection and halting decision

### Secondary Contributions

1. **Two-Stage Training Procedure:** Alternating augmentation and optimization balances computational cost with learning signal diversity
2. **Entropy-Guided Mining:** Identifies hardest intermediate steps based on entropy patterns in successful trajectories
3. **Decoupled Loss Design:** Revision and verification learn independently, preventing shortcut learning
4. **Empirical Validation:** Demonstrates effectiveness across multiple reasoning domains

## Methodology & Implementation

### Training Procedure

**Initialization:**
- Start with base LLM (4B, 7B, or larger)
- Initialize with standard supervised fine-tuning on reasoning demonstrations
- Establish baseline single-turn performance

**Data Collection Phase:**
```
For each training example:
  1. Sample multiple rollouts from current policy
  2. For rollouts reaching correct answer:
     a. Identify all intermediate steps where output is incorrect
     b. Extract entropy signal: H = -Σ p_i log(p_i) where p_i are logits
     c. Select K hardest intermediate steps (lowest entropy)
     d. Create revision prompt: "Fix this answer: [near-miss] → [correct]"
     e. Create verification prompt: "Is this answer correct? [candidate]"
  3. Accumulate synthetic training examples
```

**Optimization Phase:**
```
1. Create batched dataset from augmented examples
2. Optimize revision objective: Cross-entropy loss on fixing mistakes
3. Optimize verification objective: Binary classification on correctness
4. Apply weighted combination: Loss = α * L_revision + β * L_verification
5. Continue for specified training steps
```

### Experimental Setup

**Benchmarks Evaluated:**
- **LiveCodeBench:** Code generation and reasoning on programming problems
- **Circle Packing:** Geometric reasoning and problem-solving
- **Domain-Specific Reasoning:** Additional reasoning benchmarks

**Baseline Comparisons:**
- Standard supervised fine-tuning (single-turn)
- Multi-turn reinforcement learning (standard approach)
- Evolutionary search with multiple rollouts
- SETS (self-verification approach)

**Metrics:**
- **Pass@1:** Single attempt success rate
- **Accuracy:** Performance on test set
- **Efficiency:** Number of rollouts needed to reach target performance
- **Model Size:** Performance relative to model parameter count

### Key Results

**LiveCodeBench Performance:**
- REVES achieves +6.5 point improvement over RL baseline
- +4.0 point improvement over standard multi-turn training
- Outperforms larger evolutionary search systems while using:
  - 4B base model (smallest tested)
  - Far fewer rollouts during training
  - Lower computational requirements

**Circle Packing (Geometric Reasoning):**
- Matches previously reported state-of-the-art
- Achieved with smallest base model tested (4B parameters)
- Significantly fewer rollouts than previous evolutionary methods

**Generalization Analysis:**
- Revision and verification skills transfer across problem domains
- Smaller models with REVES training outperform larger models with standard training
- Training efficiency improves substantially with near-miss extraction

## Practical Applications & Use Cases

### Software Development and Code Generation
- Automated code generation with self-correction capabilities
- Bug detection and fixing through iterative revision
- Test-case generation and validation
- Code refactoring suggestions with verification

### Mathematical Problem Solving
- Step-by-step mathematical reasoning with intermediate checking
- Theorem proving with verification of logical steps
- Computation-intensive problem solving with multiple attempts
- Educational AI tutors providing corrective feedback

### Scientific Research Assistance
- Literature review and synthesis with verification of claims
- Hypothesis generation and empirical validation
- Experimental design with multiple iteration rounds
- Research question decomposition and structured exploration

### Business and Data Analysis
- Multi-step analytical reasoning for business insights
- Report generation with automated fact-checking
- Decision support systems with iterative refinement
- Quality assurance for generated content

### Healthcare and Medical AI
- Clinical reasoning with sequential diagnostic refinement
- Treatment recommendation generation and verification
- Medical literature analysis and synthesis
- Patient risk assessment with multiple validation steps

### Legal and Compliance
- Contract analysis with iterative clause review
- Regulatory compliance checking and verification
- Case law research and legal argument construction
- Policy interpretation with systematic verification

## Insights & Implications

### Field Impact

REVES represents a paradigm shift in LLM post-training methodology:

1. **Efficiency Breakthrough:** Demonstrates that well-designed training can dramatically reduce computational requirements for test-time scaling
2. **Smaller Model Viability:** Shows competitive performance achievable with smaller models through better training
3. **Practical Deployment:** Makes reasoning-capable models more practical for resource-constrained environments
4. **Training-Test Alignment:** Bridges gap between training objectives and actual test-time usage patterns

### Key Insights

**Near-Miss Recognition:**
- Partially correct intermediate outputs contain substantial learning signal
- Standard RL loss formulation discards these signals by only tracking final outcomes
- Systematic extraction of near-misses enables efficient learning from limited data

**Revision vs. Verification Duality:**
- Revision alone insufficient—models can generate plausible-but-wrong answers
- Verification alone insufficient—models lack knowledge to revise their own mistakes
- Combination creates emergent capability for iterative reasoning

**Efficiency-Effectiveness Trade-off:**
- Carefully designed training enables test-time scaling without proportional training cost
- Smaller models can achieve large model performance through better training
- Computational budget better spent on quality training than model scale

### Research Directions

1. **Cross-Domain Generalization:** Investigating how revision and verification skills transfer across different problem domains
2. **Interpretability:** Understanding what patterns models learn for revision and verification decisions
3. **Scaling Laws:** Characterizing how performance scales with model size and training data under REVES framework
4. **Hybrid Approaches:** Combining REVES with other test-time scaling techniques (beam search, ensemble methods)
5. **Domain Adaptation:** Adapting revision and verification skills to new domains efficiently

### Limitations and Open Questions

- **Complexity Ceiling:** Performance under extremely complex multi-step reasoning tasks not fully explored
- **Verification Accuracy:** How accurate does verification need to be for effective scaling?
- **Domain Transfer:** Optimal strategies for applying learned revision skills to novel domains
- **Failure Analysis:** Understanding failure modes of revision and verification
- **Hyperparameter Sensitivity:** Tuning weighting between revision and verification objectives

## Code & Resources

### Dependencies
- PyTorch 2.0+ for model training
- Transformers library (HuggingFace) for base LLM models
- Python 3.10+ for implementation
- CUDA 11.8+ for GPU acceleration (optional but recommended)

### Model Requirements
- Base LLM: 4B-70B parameter range tested
- Memory: 16GB+ for 4B models, 40GB+ for 7B models, 80GB+ for larger models
- Storage: 50GB+ for model checkpoints and datasets

### Integration Framework

```python
# REVES Training Pseudo-code
def train_with_reves(base_model, training_examples):
    for epoch in range(num_epochs):
        # Stage 1: Augment data with near-miss extraction
        augmented_data = []
        for example in training_examples:
            trajectories = sample_trajectories(base_model, example)
            for trajectory in trajectories:
                if trajectory.reaches_correct_answer():
                    near_misses = extract_near_misses(trajectory)
                    for near_miss in near_misses:
                        # Create revision and verification samples
                        augmented_data.append(
                            create_revision_sample(near_miss, example.correct_answer)
                        )
                        augmented_data.append(
                            create_verification_sample(near_miss, is_correct=False)
                        )
        
        # Stage 2: Optimize on augmented data
        for batch in create_batches(augmented_data):
            revision_loss = compute_revision_loss(base_model, batch)
            verification_loss = compute_verification_loss(base_model, batch)
            total_loss = alpha * revision_loss + beta * verification_loss
            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()
    
    return base_model
```

## Related Work & Context

### Prior Work Foundations

**Test-Time Scaling Methods:**
- Beam search and sampling for multi-hypothesis generation
- Self-consistency prompting using voting across multiple samples
- Evolutionary algorithms for iterative refinement
- Ensemble methods for improved reasoning

**Self-Improvement Approaches:**
- Self-critiquing for output evaluation
- Chain-of-thought prompting for step-by-step reasoning
- Verification networks for checking intermediate steps
- Feedback-driven refinement

**Training Methodologies:**
- Reinforcement Learning from Human Feedback (RLHF) with ranking objectives
- Multi-turn conversation training
- Instruction following and few-shot learning
- Curriculum learning for staged complexity

### Related Recent Papers

- **SETS (Self-Verification):** Learning to verify answers without generating correct ones
- **Evolutionary Search Methods:** Multiple rollouts with voting for correctness
- **Self-Reflection Methods:** Models critiquing and improving their own outputs
- **Intermediate Step Training:** Learning from step-wise intermediate reasoning

### Future Research Directions

1. **Unified Framework:** Developing theory unifying revision learning with other self-improvement techniques
2. **Verification-Aware Sampling:** Using verification probability to guide rollout sampling
3. **Hierarchical Reasoning:** Applying REVES to complex multi-level reasoning problems
4. **Continual Learning:** Enabling models to improve through interaction with environment
5. **Scaling Properties:** Understanding how REVES scales to larger models and longer reasoning chains

---

**Paper Link:** [arXiv:2606.18910](https://arxiv.org/abs/2606.18910)
