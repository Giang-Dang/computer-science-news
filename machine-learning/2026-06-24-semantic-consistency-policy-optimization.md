# Semantic Consistency Policy Optimization for Reinforcement Learning of LLM Agents

**ArXiv ID:** 2606.25852  
**Submission Date:** June 24, 2026  
**Submission Status:** Under review at EMNLP 2026  
**Authors:** Peng Xu, Sijia Chen, Junzhuo Li, Xuming Hu  
**Affiliation:** The Hong Kong University of Science and Technology  
**Focus:** Reinforcement Learning, LLM Agents, Long-Horizon Tasks

## Executive Summary

Semantic Consistency Policy Optimization (SCPO) addresses a fundamental problem in reinforcement learning for LLM agents: conflicting credit assignment to semantically similar actions based on whether their trajectory succeeded or failed. Through a value-free reward shaping method, SCPO enables agents to learn from partially-correct progress in failed rollouts by comparing them with successful siblings. Achieving 93.7% success on ALFWorld and 74.8% on WebShop at 1.5B parameters—matching or exceeding stronger baselines—SCPO provides a principled approach to improving agent learning efficiency and effectiveness on complex, long-horizon, sparse-reward tasks.

## Problem Statement

**The Core Challenge:**
Modern reinforcement learning for LLM agents involves:
- Long-horizon tasks requiring multiple steps to completion
- Sparse reward signals (reward only at task completion)
- High-dimensional action spaces (language-based decisions)

**The Semantic Consistency Problem:**
Consider an agent solving a shopping task:
- **Failed Rollout 1:** Clicks "Add to Cart" (Step 1) → Later makes a mistake → Task fails
- **Successful Rollout 2:** Clicks "Add to Cart" (Step 1) → Completes task successfully

Standard group-based RL (training on multiple rollouts per example) trains on both trajectories simultaneously. The result: **Step 1 receives conflicting credit signals:**
- Negative signal from Failed Rollout 1 (trajectory failed)
- Positive signal from Successful Rollout 2 (trajectory succeeded)
- **Same semantic action, opposite gradients!**

**Consequences:**
1. Conflicting gradients slow learning and destabilize training
2. Wasted learning signal from partially-correct progress in failed rollouts
3. Inefficient sample utilization despite having multiple trajectories
4. Agent struggles to recognize correct actions despite attempts

**Why This Matters:**
- LLM agents solving real-world tasks (web navigation, tool use) need efficient learning
- Sparse rewards mean every trajectory is valuable; wasting information hurts performance
- Longer tasks have more partially-correct steps; problem scales with task complexity

## Core Concepts & Theory

### Group-Based Reinforcement Learning for Agents

**Setup:**
For each example (task), train on multiple rollouts:
- Some trajectories reach the goal (success)
- Others fail before reaching the goal (failure)
- Standard approach: Binary reward based on final outcome

**Standard Credit Assignment:**
```
Success trajectory: R=+1 for all steps
Failed trajectory:  R=-1 for all steps
```

**Problem:** Ignores intermediate progress, assigns binary credit regardless of how close to success.

### Semantic Progress and Sibling Comparison

**Key Innovation:**
Compare a failed step not against an arbitrary success, but against its **semantic sibling**—the same step in a successful trajectory solving the same task.

**Sibling Definition:**
In trajectory alignment for the same task:
- Step i in failed trajectory (state s, action a)
- Step j in successful trajectory reaching same/similar state
- These are semantic siblings if they represent equivalent task progress

**Progress Measurement:**
```
Step progress = f(state_in_success, state_in_failure)
```

Measure what additional progress the success trajectory made beyond the failed sibling, rewarding the failed step for matching that progress.

### Value-Free Reward Shaping

Unlike value function methods, SCPO:
- **Doesn't require:** Learning a value function V(s)
- **Instead uses:** Direct comparison of trajectory states as reward signal
- **Advantage:** Simpler, more sample-efficient, stable training

**Reward Formula:**
```
r(step_failed) = α × progress_in_sibling(step_success) × similarity(step_failed, step_success)
```

Where:
- α: Scaling factor for reward magnitude
- progress_in_sibling: How much better the success trajectory did from this point
- similarity: Confidence that failed step is truly a semantic sibling

## Main Ideas & Contributions

### 1. Semantic Sibling Identification

**Challenge:** How to find the "right" successful sibling for each failed step?

**Solution - Trajectory Alignment:**
1. **State Representation:** Extract state embedding from agent's internal representations
2. **Alignment Metric:** Measure semantic distance between states in failed vs. successful trajectories
3. **Sibling Matching:** Find state in successful trajectory closest to each failed state
4. **Confidence Filtering:** Only use siblings with high alignment confidence

This enables automatic, principled sibling matching without manual annotation.

### 2. Step-Level Credit from Trajectory Outcomes

**From Binary to Nuanced:**
Instead of binary success/failure credit:

**Standard:** "Step i in failed trajectory → failed = -1"

**SCPO:** "Step i progressed toward state S_j; successful trajectory advanced further from S_j → +0.5"

**Benefit:**
- Partially-correct steps get positive credit when they align with successful progression
- Failed steps still learn what NOT to do next
- Gradient conflicts resolved through state-based reasoning rather than binary labels

### 3. Value-Free Reward Shaping Framework

Unlike value functions requiring extensive training:

**Advantages:**
1. **Stability:** Direct state comparison more stable than learned V(s)
2. **Efficiency:** No need to train auxiliary value network
3. **Interpretability:** Can inspect and understand why rewards assigned
4. **Scalability:** Works with large state spaces without function approximation

**Implementation:**
- Compute rewards on-the-fly during batch processing
- No additional parameters or networks needed
- Compatible with any policy optimization algorithm

### 4. Compatibility with Existing RL Methods

SCPO is a **reward shaping layer** that works with:
- Policy Gradient (PG)
- Proximal Policy Optimization (PPO)
- Actor-Critic methods
- Other group-based RL algorithms

**Integration:** Replace the standard reward signal with SCPO rewards, run existing RL algorithm.

## Methodology & Implementation

### Experimental Setup

**Benchmark Tasks:**

**ALFWorld (Alfredo-Lite):**
- Realistic household simulation
- Tasks: Pick up objects, change settings, solve tasks with tools
- Success rate metric (harder as task complexity increases)
- Baseline models: 71B parameter LLMs

**WebShop:**
- E-commerce website interaction
- Tasks: Find and purchase products matching criteria
- Simulated website with realistic structure and dynamics
- Comparable to real-world web navigation

### Baseline Comparisons

**Standard Group-Based RL:**
- Train on multiple rollouts with binary rewards
- Represents standard approach in literature

**Other Methods:**
- Specialized RL agents (e.g., ReAct framework)
- Fine-tuned models with supervised learning
- Other reward shaping approaches

### Training Protocol

**Data Collection:**
1. Run rollout policy on benchmark tasks
2. Collect multiple trajectories per example (e.g., 4-8)
3. Separate successes and failures

**Reward Computation:**
1. Align failed trajectories with successful counterparts
2. For each step in failed trajectory, compute SCPO reward
3. Create augmented training batch

**Policy Optimization:**
1. Run standard RL algorithm (PPO-like) on augmented batch
2. Optimize policy to maximize total return with SCPO rewards
3. Repeat for multiple epochs

### Evaluation Metrics

**Primary Metrics:**
- **Success Rate:** Percentage of tasks completed successfully
- **Efficiency:** Number of steps before giving up
- **Cumulative Reward:** Sum of shaped rewards over trajectory

**Secondary Metrics:**
- **Convergence Speed:** How quickly success rate improves
- **Sample Efficiency:** Success rate vs. training samples
- **Generalization:** Transfer to similar tasks

### Key Results

**ALFWorld Performance:**
- SCPO: 93.7 ± 4.1% success rate at 1.5B parameters
- Baseline: 88.2 ± 5.3% (comparable approaches)
- Improvement: +5.5% absolute, concentrated on multi-step tasks

**WebShop Performance:**
- SCPO: 74.8 ± 2.0% success rate at 1.5B parameters
- Baseline: 71.1 ± 3.1% (previous state-of-the-art)
- Improvement: +3.7% absolute

**Task Difficulty Analysis:**
- Gains largest on 3+ step tasks requiring sequential reasoning
- Minimal improvement on simple 1-step tasks
- Demonstrates method targets exactly where needed

**Sample Efficiency:**
- Reaches target performance with 30% fewer training samples than baselines
- Shows improved data utilization from sibling comparison

**Convergence Characteristics:**
- More stable training curves than binary-reward baselines
- Less sensitive to hyperparameter variations
- Earlier convergence to high performance

## Practical Applications & Use Cases

### Web Navigation and E-commerce

**Applications:**
- Shopping assistants finding products and completing transactions
- Travel booking systems navigating complex websites
- Research task automation (literature search, data gathering)

**Advantages:**
- Complex, multi-step tasks benefit most from SCPO
- Real websites provide clear success/failure distinction
- Enables personalized shopping agents

**Challenges:**
- Websites change structure; requires adaptation
- Training on diverse websites needed for generalization
- Privacy and TOS considerations for autonomous shopping

### Tool Use and API Integration

**Scenarios:**
- Agents using software APIs to accomplish goals
- Chain-of-tool orchestration (email → calendar → reminder)
- Database query optimization through agent planning

**Benefits:**
- Clear task completion signals (API returns success/failure)
- Compositional action spaces enable semantic sibling matching
- Improved efficiency reduces tool-use overhead

**Implementation Considerations:**
- API availability during training
- Handling API changes and versioning
- Cost management for tool use during agent training

### Information Extraction and Reasoning

**Use Cases:**
- Fact verification by retrieving and comparing sources
- Multi-source information synthesis
- Evidence gathering for question answering

**Applicability:**
- Clear ground truth for success (facts verified)
- Natural task decomposition supports sibling matching
- Reduces hallucination through reward shaping

### Household Robotics

**Future Applications:**
- Robots learning household tasks through interaction
- Sim-to-real transfer of learned behaviors
- Multi-step manipulation tasks (prepare meal, clean room)

**Considerations:**
- Sim-to-real gap affects reward signals
- Safety constraints during exploration
- Sample efficiency critical for physical systems

## Insights & Implications

### State-of-the-Art Advancement

1. **Credit Assignment:** Solves semantic consistency problem in agent RL
2. **Efficiency:** 30% sample efficiency improvement while improving performance
3. **Generality:** Applicable to any policy optimization method
4. **Practicality:** No additional networks, stable training

### Broader Research Implications

1. **Agent Learning:** Demonstrates that trajectory comparison reveals teachable signals
2. **Reward Design:** Shows value of semantic-aware reward shaping over binary signals
3. **Multi-Trajectory RL:** Explains why group-based training can be more efficient when properly designed
4. **LLM Agent Reasoning:** Suggests how agents best learn from exploration data

### Limitations and Challenges

**Technical Limitations:**
1. **Sibling Alignment:** Requires meaningful state representation; poor representation hurts performance
2. **State Embedding Quality:** Depends on language model's internal representation quality
3. **Trajectory Diversity:** Needs sufficient successful trajectories to find good siblings

**Generalization Concerns:**
1. **Task Diversity:** Alignment metrics trained on one task set may not transfer
2. **Model Size:** Results shown at 1.5B; scaling to 70B+ may reveal different dynamics
3. **Sparse Success:** If success rate too low, insufficient positive examples for sibling matching

**Practical Challenges:**
1. **Computational Cost:** Trajectory alignment adds per-batch overhead
2. **State Representation:** Unclear which layer/representation works best for alignment
3. **Hyperparameter Tuning:** Similarity thresholds, reward scaling need task-specific tuning

## Code & Resources

### Official Resources
- **ArXiv Paper:** https://arxiv.org/abs/2606.25852
- **HTML Version:** https://arxiv.org/html/2606.25852v1

### Benchmark Resources
- **ALFWorld:** https://github.com/alfworld/alfworld
- **WebShop:** https://github.com/web-shop/webshop
- **Evaluation Scripts:** Benchmarks include standard evaluation harnesses

### Dependencies
- **PyTorch:** For policy network and training
- **Hugging Face Transformers:** For LLM backbones
- **ALFWorld/WebShop:** Specific benchmark environments
- **Standard RL libraries:** PPO, policy gradient implementations

### Quick-Start Implementation

**Step 1: Trajectory Collection**
```python
# Run rollouts on tasks using exploration policy
# Collect multiple trajectories per task
# Separate successful and failed trajectories
```

**Step 2: State Alignment**
```python
# Extract state embeddings from LLM hidden states
# Compute alignment metrics between failed and successful trajectories
# Identify semantic siblings
```

**Step 3: Reward Shaping**
```python
# For each step in failed trajectory:
#   Find sibling in successful trajectory
#   Compute progress differential
#   Assign shaped reward
```

**Step 4: Policy Optimization**
```python
# Use shaped rewards in standard RL algorithm
# Run PPO or similar policy optimization
# Iterate until convergence
```

## Related Work & Context

### Prior Reinforcement Learning for Agents

**Trajectory-Based Methods:**
- Offline RL: Learning from fixed dataset of trajectories
- Behavioral Cloning: Imitating successful trajectories
- Trajectory Stitching: Combining trajectory segments

**Online Learning Methods:**
- PPO: Policy gradient with clipped objectives
- Actor-Critic: Value and policy function training
- REINFORCE variants: Standard policy gradient methods

**LLM Agent Training:**
- Instruction Fine-Tuning: Supervised learning on demonstrations
- RLHF: Reward model learning from human preferences
- Self-Play: Agents learning through competition

### Reward Shaping Research

**Classical Work:**
- Reward Shaping (Ng et al., 1999): Using domain knowledge to accelerate learning
- Inverse RL: Learning reward functions from demonstrations
- Preference Learning: Learning from preference pairs

**Recent Approaches:**
- Dense Rewards from Sparse: Auxiliary objectives for denser signals
- Intrinsic Motivation: Curiosity, empowerment, novelty seeking
- Skill Learning: Learning hierarchical policies with learned rewards

### Multi-Trajectory Learning

**Related Methods:**
- Ensemble Methods: Training multiple policies and combining
- Conservative RL: Staying close to data distribution
- Contrastive Learning: Using trajectory pairs for representation learning

### Contemporary Papers

- "Reason in Chains, Learn in Trees: Self-Rectification and Grafting for Multi-turn Agent Policy Optimization" (2604.07165)
- "Beyond Trajectory-Level Attribution: Graph-Based Credit Assignment for Agentic Reinforcement Learning" (2605.26684)
- "StepPO: Step-Aligned Policy Optimization for Agentic Reinforcement Learning" (2604.18401)
- "Policy Improvement Reinforcement Learning" (2604.00860)

## Future Research Directions

### Immediate Extensions

1. **Multi-Modal Sibling Matching:** Extend beyond text (incorporate visual state if available)
2. **Adaptive Similarity Thresholds:** Learn optimal alignment thresholds per task
3. **Multi-Step Look-ahead:** Consider progress multiple steps beyond sibling
4. **Weighted Trajectory Ensembles:** Combine signals from multiple successful siblings

### Medium-Term Research

1. **Representation Learning:** Joint learning of state embeddings optimized for sibling matching
2. **Hierarchical Decomposition:** Applying SCPO to subtask learning and skill hierarchies
3. **Transfer Learning:** Transferring learned sibling matching patterns across tasks
4. **Batch Composition:** Optimally grouping trajectories for training

### Long-Term Vision

1. **Continual Learning:** Agents improving through continuous interaction with environments
2. **Curriculum Learning:** Progressively harder tasks as agent capabilities improve
3. **Theory Development:** Formal analysis of credit assignment in multi-trajectory settings
4. **General Purpose Agents:** Foundation for autonomous agents solving diverse real-world tasks

### Alternative Research Directions

1. **Combining with Imitation:** Hybrid approaches blending IL and RL
2. **Uncertainty Estimation:** Understanding confidence in sibling matches
3. **Interpretability:** Understanding what agents learn from semantic siblings
4. **Scalability:** Efficient sibling matching for high-throughput training

---

## Summary

Semantic Consistency Policy Optimization provides a practical and principled solution to a real problem in LLM agent training: conflicting credit assignments for semantically similar actions. By comparing failed trajectories with successful siblings at the state level, SCPO eliminates gradient conflicts while extracting learning signal from partially-correct exploration. The demonstrated improvements (93.7% on ALFWorld, 74.8% on WebShop) with 30% better sample efficiency show the method's practical value.

This work advances agentic AI by addressing a fundamental challenge in learning from exploration: how to provide clear credit signals when most trajectories partially succeed. As agents tackle increasingly complex, long-horizon tasks in realistic environments, techniques like SCPO that improve learning efficiency become essential for practical deployment. The insights about semantic sibling matching may also apply beyond agent RL, inspiring new approaches to credit assignment in diverse reinforcement learning settings.

The paper demonstrates that with careful consideration of what agents are actually learning—at the semantic level rather than binary outcome level—we can significantly improve their efficiency and performance on challenging real-world tasks.
