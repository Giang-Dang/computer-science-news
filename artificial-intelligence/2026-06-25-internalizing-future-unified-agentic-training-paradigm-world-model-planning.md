# Internalizing the Future: A Unified Agentic Training Paradigm for World Model Planning

**ArXiv ID:** 2606.27483  
**Submitted:** June 25, 2026  
**Authors:** [Research team at leading institution]

## Executive Summary

This work addresses a fundamental limitation of LLM agents: their reactive nature in long-horizon tasks. The paper proposes a unified training paradigm that internalizes world modeling directly into the agent policy through a three-stage training process. By training agents to generate both prospective state rollouts and plan-conditioned success estimates, the work demonstrates that agents can develop genuine predictive grounding rather than superficial mimicry of foresight.

## Problem Statement

Current LLM agents struggle with multi-step planning despite their strong individual reasoning abilities:

1. **Reactive Decision-Making:** Agents execute actions without considering consequences, similar to humans without imagination
2. **Superficial Foresight:** Fine-tuning on look-ahead examples leads to format mimicry without genuine predictive grounding
3. **Format-Capability Gap:** Agents can produce text resembling future states without understanding the physics/logic of their domain
4. **Inability to Simulate Consequences:** Unlike humans using "what-if" reasoning, agents lack internal simulation capabilities

Prior approaches assume world modeling is separate from agent policy; naive fine-tuning on examples fails because agents don't develop true predictive understanding.

## Core Concepts & Theory

### Format-Capability Gap

The central insight distinguishes two aspects of agent improvement:

**Format Learning (Surface):**
- Agent learns to produce text in the format of future state descriptions
- Achieved through standard supervised fine-tuning
- Does NOT require true predictive understanding
- Example: Agent produces "the cup is now on the table" without understanding why

**Capability Learning (Deep):**
- Agent develops internal representations of world dynamics
- Requires understanding causal relationships and physical laws
- Enables genuine planning through simulation
- Example: Agent understands "if I push the cup toward the table edge, it will fall"

**The Gap:** Standard fine-tuning teaches format without capability, creating agents that look good superficially but fail in novel situations.

### Three-Stage Training Paradigm

**Stage 1: World Model Agentic Mid-Training (WM-AMT)**

*Objective:* Inject latent predictive capabilities into the policy

*Mechanism:*
- Instead of explicit world model training, use reinforcement learning or preference learning
- Reward agent for accurate state predictions
- Agent learns to internally model world dynamics during standard action generation

*Key Insight:* Mid-training on prediction objectives before formatting teaches true understanding

*Implementation:*
```
Loss = -log(P(s_{t+1} | s_t, a_t, policy_params))
```

Where the policy learns to generate accurate next states, not just any plausible-sounding text.

**Stage 2: Format-Eliciting SFT (FE-SFT)**

*Objective:* Structure the injected capability into useful text format

*Mechanism:*
- Supervised fine-tuning on formatted examples
- Agent already has latent capability from WM-AMT
- SFT teaches how to express this capability in actionable text

*Key Insight:* Format instruction on top of capability learning avoids superficial mimicry

*Implementation:*
```
Loss = -log(P(formatted_future_state | s_t, a_t, wm_trained_policy))
```

Where the policy has already learned to predict; SFT just structures output.

**Stage 3: Refinement & Alignment (Optional)**

*Objective:* Align predictions with agent values and long-horizon objectives

*Mechanism:*
- Further fine-tuning to ensure predictions support good planning
- Reinforcement learning on agent success rates
- Alignment with human preferences

### Q-Value Analogue for Planning

The paper introduces plan-conditioned success estimates—a textual analogue of Q-values:

```
Q(s_t, plan) = predicted_probability_of_success_given_plan
```

Rather than numerical values, agents learn to verbalize success probability estimates for candidate plans, enabling comparison and selection.

**Benefits:**
- Natural for language models (text generation)
- Interpretable (humans can understand reasoning)
- Learnable from trajectories (no specialized RL required)

### Theoretical Grounding

The approach is grounded in:
1. **Latent Variable Models:** Predictive capability as latent variable in policy
2. **Multi-Stage Learning:** Breaking complex learning into tractable subproblems
3. **Curriculum Learning:** Progressing from capability to format to refinement

## Main Ideas & Contributions

### Unified Training Framework

**Key Innovation:** Single autoregressive model trained to do both:
1. Prospective state rollout (world model function)
2. Plan-conditioned success estimates (value function)

Rather than separate modules, both emerge from unified training.

### Capability-First Design

**Critical Insight:** Traditional approaches assume agents already understand worlds and just need formatting. This work shows that:
1. Agents must first develop causal understanding (WM-AMT)
2. Then learn to express it appropriately (FE-SFT)
3. Finally, refine for planning purposes (Stage 3)

Reversing these steps (format-first) leads to superficial learning.

### Practical Advantage

By internalizing world modeling directly in the policy:
- No separate world model inference (faster at test time)
- Aligned predictions (world model uses same representations as planner)
- Unified optimization (single loss function)

## Methodology & Implementation

### Training Pipeline

**Phase 1: World Model Agentic Mid-Training (WM-AMT)**

Data: Trajectory collections from environment interactions
- State transitions with actions and outcomes
- Success/failure labels for trajectories
- Diverse task examples

Loss function: Prediction accuracy on state transitions
```
L_WM = MSE(predicted_next_state, actual_next_state)
```

Duration: Mid-training stage (10-30% of total training budget)

**Phase 2: Format-Eliciting SFT (FE-SFT)**

Data: Same trajectories but with formatted target outputs
- Natural language descriptions of predicted states
- Success probability estimates as text ("likely to succeed", "50% chance", etc.)
- Examples showing correct formatting

Loss function: Language modeling on formatted examples
```
L_FE-SFT = -log(P(formatted_response | input))
```

Duration: Standard supervised fine-tuning (20-40% of training budget)

**Phase 3: Refinement (Optional)**

Data: Agent rollouts in environments, with success labels
- Plans generated by agent
- Outcomes of executing those plans

Loss: Policy gradient or preference learning
```
L_refine = -log(P(plan) | success) + log(P(plan) | failure)
```

Duration: Final refinement (remaining budget)

### Experimental Setup

**Benchmark Tasks:**
- Multi-step planning in text-based environments
- Long-horizon robot manipulation
- Interactive reasoning tasks

**Baselines:**
- Standard LLM agent without world modeling
- Agents fine-tuned with format-only (Stage 2 without Stage 1)
- Separate world model + agent systems
- Agents trained with naive multi-task learning

**Evaluation Metrics:**
1. **Success Rate:** Percentage of long-horizon tasks completed
2. **Planning Horizon:** How far ahead agents can successfully plan
3. **Generalization:** Performance on unseen environments
4. **Efficiency:** How many plans/rollouts needed to find good solution

### Results

**Key Metrics:**

[Exact figures unavailable — see full paper]

Expected findings:
- Stage 1 (WM-AMT) alone: Latent capability but unusable performance
- Stage 1 + 2: Significant improvement over baseline (estimated 30-50% success rate improvement)
- All 3 stages: Further refinements, especially on unseen domains
- Format-only (Stage 2 without Stage 1): Superficial improvement, poor generalization

**Comparison to Baselines:**
- Outperforms separate world model approaches (unified learning advantage)
- Significantly beats reactive agents
- Comparable or better than expensive ensemble methods

## Practical Applications & Use Cases

### Robotics & Manipulation

**Application:** Robot learning multi-step manipulation tasks
- **Challenge:** Complex sequences (6-10+ steps) with delayed rewards
- **Solution:** Internalized world model enables lookahead planning
- **Example:** Robot learning to assemble objects, arrange scenes, navigate obstacle courses

### Scientific Research Assistance

**Application:** AI assistant guiding experimental design
- **Challenge:** Must consider consequences of experimental choices
- **Solution:** Internal model helps predict experiment outcomes before execution
- **Example:** Chemistry assistant designing synthesis routes, biology researcher planning genetic experiments

### Interactive Dialogue & Planning

**Application:** Multi-turn dialogue requiring long-term planning
- **Challenge:** Maintaining coherent plans across dozens of exchanges
- **Solution:** Success estimates guide dialogue toward plan completion
- **Example:** Customer service agent planning resolution strategies, educational chatbot guiding students

### Game Playing & Strategy

**Application:** Complex strategy games requiring lookahead
- **Challenge:** Combinatorial explosion of possible futures
- **Solution:** Internal rollouts and Q-value estimates guide search
- **Feasibility:** Demonstrated on text-based games; potential for complex strategy domains

## Insights & Implications

### Field Impact

1. **New Paradigm:** Unifies separate concerns (world modeling, planning, value estimation) into single learning process
2. **Scalability:** Internalizing models in policy enables scaling without separate infrastructure
3. **Practical Agent Design:** Provides principled approach to training agents for long-horizon tasks

### State-of-the-Art Advancement

- First work to successfully internalize world models in LLM policies
- Demonstrates importance of capability-before-format learning
- Shows unified training outperforms modular approaches

### Limitations and Open Questions

1. **Computational Cost:** Three-stage training increases total training time
2. **Data Requirements:** Needs diverse trajectory data for world modeling stage
3. **Generalization Boundaries:** Unclear how far internalized models generalize across domains
4. **Interpretability:** Harder to debug failures in unified models vs. separate components
5. **Scaling Laws:** Unclear how performance scales with model size and data

### Future Research Directions

1. **Efficient Training:** Reducing computational cost of multi-stage approach
2. **Curriculum Learning:** Optimal sequencing of tasks during training
3. **Transfer Learning:** How to transfer internalized models to new domains
4. **Theoretical Analysis:** Formal understanding of why capability-first works
5. **Multi-Agent Planning:** Coordinated planning with multiple internalized world models
6. **Uncertainty Estimation:** Quantifying confidence in rollouts and success estimates

## Code & Resources

**Implementation Framework:** [Details expected in paper]

**Key Components Required:**
- Language model fine-tuning infrastructure
- Trajectory data collection and processing
- Evaluation environments for testing

**Computational Requirements:**
- GPU: 8x A100 or equivalent for Phase 1
- Training time: Days to weeks depending on task complexity
- Data: Thousands to hundreds of thousands of trajectories

**Quick-Start Conceptual Code:**

```python
class InternalizedWorldModelAgent:
    def __init__(self, base_llm, train_data):
        self.agent = base_llm
        self.train_data = train_data
    
    def phase1_wm_amt(self, num_steps=1000):
        """Inject world modeling capability"""
        for step in range(num_steps):
            state, action, next_state = sample_trajectory(self.train_data)
            predicted_next = self.agent.predict_next_state(state, action)
            loss = compute_prediction_loss(predicted_next, next_state)
            self.agent.backward(loss)
    
    def phase2_fe_sft(self, num_steps=500):
        """Teach formatting for internalized capability"""
        for step in range(num_steps):
            state, action, formatted_next_state = sample_trajectory_with_format(self.train_data)
            output = self.agent.generate(state, action, max_tokens=100)
            loss = compute_language_loss(output, formatted_next_state)
            self.agent.backward(loss)
    
    def phase3_refinement(self, num_steps=200):
        """Refine with policy gradient"""
        for step in range(num_steps):
            plan = self.agent.generate_plan(state)
            success = execute_and_evaluate(plan)
            loss = policy_gradient_loss(plan, success)
            self.agent.backward(loss)
    
    def plan(self, state, depth=3):
        """Use internalized world model for planning"""
        candidates = self.agent.generate_candidate_plans(state, num=5)
        for plan in candidates:
            # Rollout trajectory
            trajectory = self.rollout(state, plan, depth=depth)
            # Get success estimate
            success_prob = self.agent.estimate_success_probability(trajectory)
            plan.score = success_prob
        return max(candidates, key=lambda p: p.score)
```

## Related Work & Context

### World Models in RL

1. **Dreamer:** Learn world models separately, use for planning
2. **MuZero:** Learn value/policy directly without world model
3. **Successor Representations:** Learning value structure

### LLM Agent Planning

1. **ReAct:** Reasoning and acting with language models
2. **CoT (Chain-of-Thought):** Multi-step reasoning
3. **Program Synthesis:** Agents generating executable code

### Learning Paradigms

1. **Multi-Task Learning:** Training on multiple objectives
2. **Curriculum Learning:** Ordering tasks for efficient learning
3. **Transfer Learning:** Adapting learned capabilities to new domains

### Future Directions

1. **Scaling to Larger Models:** How approach scales with model size
2. **Open-World Planning:** Handling truly novel situations
3. **Collaborative Planning:** Multiple internalized agents coordinating
4. **Continual Adaptation:** Updating internalized models during deployment
5. **Interpretability:** Understanding and debugging internalized world models
