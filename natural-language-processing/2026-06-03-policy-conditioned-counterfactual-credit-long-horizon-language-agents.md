# Policy-Conditioned Counterfactual Credit for Verifiable Reinforcement Learning of Long-Horizon Language Agents

**arXiv ID:** 2606.05263  
**Submitted:** June 3, 2026  
**Authors:** [Research team in RL and language agents]

## Executive Summary

Long-horizon language agents trained with reinforcement learning using verifiable rewards (process rewards, outcome rewards) often learn spurious shortcuts that satisfy terminal verification without achieving genuine task progress. This paper proposes CVT-RL, a constrained policy-gradient algorithm that uses policy-conditioned counterfactual contribution (PCCC) estimation to properly assign credit for each step's contribution to verified success. By combining dense verifiable rewards, intervention-validity gating, and controlled intervention-based credit assignment, CVT-RL enables agents to learn well-grounded reasoning policies that succeed because of genuine evidence chains rather than mathematical shortcuts. The approach represents a critical advance toward trustworthy and verifiable AI agents.

## Problem Statement

Reinforcement learning with verifiable rewards has shown promise for improving reasoning and tool-use in language agents, but critical limitations remain:

1. **Spurious Shortcuts**: Agents learn to satisfy verification criteria without genuine reasoning:
   - Hallucinating evidence chains not retrieved from documents
   - Drifting beliefs progressively farther from supported evidence
   - Performing tool interactions that don't actually contribute to task completion but satisfy terminal checks

2. **Process Reward Causality**: Existing process rewards are correlational, not causal:
   - Reward retrieval, reflection, verification-like steps without checking if they caused final success
   - No mechanism to distinguish between steps that caused success vs. steps that happen to co-occur with success

3. **Attribution Problem**: Without causal intervention analysis, how can we determine if step A truly led to the agent's success or just co-occurred with independent factors?

The core research gap: How can we assign credit to individual steps based on their actual causal contribution to verified task completion?

## Core Concepts & Theory

### Counterfactual Credit Assignment

The foundational insight: A step's contribution should be measured by how different the outcome would be if that step were removed or modified.

**Formal Framework**:

For each step i in a trajectory:
- **Observed outcome**: Final verified success with current trajectory
- **Counterfactual outcome**: Would the agent succeed if step i were removed?
- **Contribution**: Difference between observed and counterfactual outcomes

### Controlled Interventions

Rather than observing counterfactual outcomes (which may be impossible in real agents), CVT-RL uses:

1. **Deletion Intervention**: Remove the step entirely, continue from previous state
2. **Semantic Substitution**: Replace the step with a different semantically meaningful action
3. **Evidence Substitution**: Keep the action structure but use different evidence
4. **Tool-Output Perturbation**: Vary tool outputs to test downstream impact

Each intervention type tests different hypotheses about what made the step valuable.

### Policy-Conditioned Counterfactual Contribution (PCCC) Estimator

The key innovation addresses confounding in counterfactual analysis:

**Challenge**: When we remove a step, the agent's continuation policy changes. The outcome difference could be due to:
- (A) The removed step itself being important
- (B) The policy adapting differently after step removal

**PCCC Solution**:
- Sample continuations from the **frozen reference policy** (the policy at step i+1)
- This holds the policy constant while varying only the removed step
- Use **doubly robust estimation**: Combines direct estimation with regression adjustment to reduce variance
- Adjust for **selection bias**: Some step modifications may be more likely than others—use inverse probability weighting

**Pseudocode**:
```
For each step i:
  Continuation_observed = sample from current policy after step i
  For each intervention type:
    Continuation_counterfactual = sample from frozen policy after intervention
    Outcome_diff = verify(observed_trajectory) - verify(counterfactual_trajectory)
    Adjustment = regression_model(state, step) - regression_model(state_modified, step)
    PCCC_i = Outcome_diff + Adjustment
    Weight = inverse_probability_weight(intervention)
    Credit_i = Weight * PCCC_i
```

### Intervention-Validity Gating

Not all interventions are equally valid for the agent:

- **Physical Feasibility**: Can the agent actually perform the modified step?
- **Execution Validity**: Does the modified step fit the agent's action space and syntax?
- **Semantic Coherence**: Does the modification preserve semantic meaning for analysis?

The gating mechanism ensures only valid interventions contribute to credit assignment, preventing spurious credits from physically impossible counterfactuals.

## Main Ideas & Contributions

### 1. Causal Credit via Controlled Interventions

Innovation: Replaces correlational process rewards with causal credit assignment:
- **Before**: Reward retrieval steps because they correlate with success
- **After**: Assign credit based on counterfactual impact—would success still occur without this step?

This prevents agents from gaming the reward signal through unrelated actions that happen to co-occur with success.

### 2. Dense Verifiable Rewards with Intervention-Guided Credit

Rather than sparse rewards at task end:
- Compute verifiable rewards at every step (verifying the current belief/evidence state)
- Use intervention-based credit assignment to propagate step-level signals backward
- Creates dense learning signal focused on verified progress

### 3. Policy-Conditioned Doubly Robust Estimator

Addresses statistical challenges in counterfactual estimation:
- **Policy Conditioning**: Freezes the continuation policy to isolate step contributions
- **Doubly Robust**: Combines direct estimation and regression adjustment—robust to model misspecification in either component
- **Bias Adjustment**: Inverse probability weighting corrects for non-uniform intervention selection

## Methodology & Implementation

### Algorithm: CVT-RL (Constrained Verifiable Trajectory RL)

**High-Level Steps**:

1. **Data Collection**: Agent executes policy, trajectories collected with task success/failure labels
2. **Intervention Generation**: For each step, generate controlled interventions (4 types described above)
3. **PCCC Estimation**: For each intervention, estimate counterfactual outcome using frozen policy continuation
4. **Credit Assignment**: Aggregate PCCC estimates to assign step-level credits
5. **Policy Update**: Use step-level credits to compute policy gradients via constrained optimization
6. **Constraint Enforcement**: Add constraint ensuring policy remains within valid action space under interventions

### Experimental Setup

**Tasks**:
- Long-horizon reasoning tasks (e.g., multi-step question answering)
- Tool-use tasks requiring multiple API calls
- Evidence-grounded tasks where correctness depends on cited sources

**Baselines**:
1. Standard RL with outcome rewards only
2. Standard RL with process rewards (correlation-based)
3. Policy gradient without intervention-based credit
4. Oracle credit assignment (assuming access to true causal graph)

### Evaluation Metrics

1. **Task Success Rate**: Percentage of tasks solved correctly
2. **Verifiable Success**: Success restricted to solutions with valid evidence chains
3. **Evidence Validity**: Percentage of steps backed by retrieved evidence
4. **Belief Consistency**: How consistently agent beliefs remain supported by evidence
5. **Generalization**: Performance on held-out tasks requiring similar reasoning

### Key Results

The paper demonstrates that CVT-RL:
- **Improves Verifiable Success**: Higher fraction of solutions with valid evidence chains vs. standard RL
- **Reduces Shortcuts**: Agents learn genuine reasoning policies instead of mathematical hacks
- **Better Generalization**: Policies learned with intervention-based credit transfer better to new tasks
- **Computational Efficiency**: PCCC estimation adds modest overhead despite multiple interventions

[Exact figures unavailable — see full paper for quantitative metrics across task categories]

## Practical Applications & Use Cases

### 1. Trustworthy AI in Critical Domains

**Healthcare Decision Support**:
- Agent must justify recommendations with verifiable evidence
- CVT-RL ensures agents don't learn shortcuts that satisfy verification without genuine reasoning
- Doctors can trust agent's evidence chains, not just outcomes

**Legal Research Assistance**:
- Agent retrieves relevant case law and cites supporting evidence
- Prevents hallucinated precedents that would mislead lawyers
- Builds trust through verifiable reasoning chains

### 2. Accountable Autonomous Systems

**Financial Analysis**:
- Investment recommendation agents must cite data supporting thesis
- CVT-RL prevents recommendations based on mathematical artifacts
- Auditable decision trails for regulatory compliance

**Content Moderation**:
- Agents make moderation decisions with verifiable policy reasoning
- Can cite specific content and policies violated
- Enables appeal processes based on evidence

### 3. Transparent AI Assistance

**Research Assistance**:
- Literature analysis agents can cite papers supporting conclusions
- Teachers/reviewers can verify agents aren't making up citations
- Enables high-confidence use of AI in knowledge work

**Information Retrieval**:
- Search agents return results with explicit reasoning chains
- Users understand how results were retrieved, not just what was retrieved
- Builds interpretability and trust

## Insights & Implications

### Broader Field Impact

This work demonstrates:

- **Causal is Better Than Correlational**: Even with limited tools, causal credit assignment (via interventions) beats correlation-based process rewards
- **Verifiable Success > Raw Success**: The constraint that success must be verifiable isn't a limitation—it's what makes systems trustworthy
- **Intervention-Based Analysis**: Controlled perturbations can estimate causality without access to full causal graphs
- **Dense Rewards from Sparse Verification**: Can convert sparse outcome signals into dense step-level signals through counterfactual analysis

### State-of-the-Art Advancement

- Shifts from "Does the agent succeed?" to "Can we verify why the agent succeeded?"
- Moves beyond process rewards toward causal credit assignment
- Demonstrates that modern RL techniques (doubly robust estimation, policy conditioning) enable more trustworthy agent learning

### Limitations & Open Questions

1. **Computational Cost**: Multiple interventions per step increase training time—can this be optimized?
2. **Intervention Design**: Are the 4 intervention types sufficient for all domains? How to design domain-specific interventions?
3. **Frozen Policy Assumption**: How does credit quality degrade if the policy changes during training?
4. **Scaling to Complex Reasoning**: How does the approach scale to very long-horizon tasks (100+ steps)?
5. **Transfer Learning**: Can PCCC estimates learned on one task transfer to help learn other tasks?

## Code & Resources

### Implementation Requirements
- **Language Model Base**: GPT-3 scale or larger for complex reasoning
- **Verification System**: Domain-specific verification (document retrieval, knowledge base checking, etc.)
- **Tool API**: Standardized interface for agent tool calls
- **Intervention Module**: Code to generate and apply controlled interventions

### Dependencies
- RL framework (PyTorch or TensorFlow)
- Policy gradient algorithms (PPO, GRPO, or actor-critic methods)
- Inverse probability weighting libraries
- Doubly robust estimation implementations

### Compute Requirements
- **Training**: Significant compute needed for multiple interventions per step
- **Sampling**: Frozen policy continuation sampling can be parallelized
- **Scaling**: Domain-dependent but feasible on modern hardware

## Related Work & Context

### Foundation Areas
- **Counterfactual Inference**: Classical causal inference in econometrics and program evaluation
- **Credit Assignment in RL**: Policy gradient methods, advantage estimation, temporal difference learning
- **Verifiable AI**: Interpretability, explainability, and verification of AI systems
- **Process Rewards**: Using intermediate signals for RL in language models

### Related Recent Work
- Outcome supervision with sparse rewards for language models
- Process supervision and dense reward signals for reasoning
- Causal analysis in machine learning
- Trustworthy AI and verifiable systems

### Future Research Directions

1. **Multi-Agent Verification**: How to assign credit in teams of agents with interdependent verification?
2. **Adaptive Interventions**: Can agents learn which interventions are most informative for their own credit assignment?
3. **Domain Generalization**: Pre-train PCCC estimators on diverse tasks to transfer to new domains?
4. **Hierarchical Reasoning**: Credit assignment for hierarchical task decomposition
5. **Interactive Verification**: Agents querying humans about counterfactual outcomes to improve credit estimates
6. **Theoretical Analysis**: Convergence guarantees and sample complexity of CVT-RL
7. **Robustness**: How adversarially-designed interventions might fool the credit assignment system

## Keywords

counterfactual credit assignment, verifiable reinforcement learning, long-horizon reasoning, language agents, causal inference, doubly robust estimation, process rewards, trustworthy AI
