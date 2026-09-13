# Progressive Agent Skill Generation via Reinforcement Learning

**Authors:** Junhao Shen, Zhanqiu Zhang, Yiwen Guo, Hong Cheng  
**Affiliation:** The Chinese University of Hong Kong, LIGHTSPEED, Independent Researcher  
**ArXiv ID:** 2608.01678 (August 3, 2026)

## Executive Summary

This paper introduces Skill-α, a reinforcement learning method for progressively generating high-quality agent skills through sequential editing. The work addresses a fundamental challenge in skill-based agent systems: the lack of natural supervision signals for skill quality. Rather than treating skills as static components, Skill-α formulates skill generation as a sequential decision-making process, where each edit represents an actionable step toward improving agent performance on downstream tasks.

## Problem Statement

Contemporary skill-based agent architectures leverage external skills as modular procedural units that condition inference and improve complex task solving. However, learning-based skill generation faces critical challenges:

1. **Supervision Signal Absence:** Unlike code generation or classification tasks, skills lack direct correctness labels. Their value can only be determined through whether they improve downstream agent behavior on actual tasks.

2. **Skill Quality Evaluation:** Traditional metrics (BLEU, accuracy) don't capture whether a skill genuinely helps agents solve complex problems.

3. **Learning Signal Sparsity:** Feedback signals are indirect and delayed, arriving only after agent execution on downstream tasks.

4. **Skill Composition:** Individual high-quality skills don't necessarily compose well; synergy between skills matters more than individual quality.

5. **Skill Discovery:** The space of possible useful skills is vast and poorly understood.

6. **Generalization Challenges:** Skills learned on training tasks may not transfer effectively to new domains or task types.

The research gap lies in developing methods that can progressively refine skills using only weak, indirect feedback from agent task performance.

## Core Concepts & Theory

### Sequential Skill Refinement

Rather than generating complete skills in one step, Skill-α treats skill generation as an iterative refinement process:

```
Initial Skill Hypothesis → Edit 1 → Intermediate Skill 1 → 
Edit 2 → Intermediate Skill 2 → ... → Final Refined Skill
```

Each edit is a discrete, individually evaluable modification:
- Addition of new clauses or conditions
- Modification of existing parameters
- Reorganization of procedural steps
- Integration of external knowledge or tools

### Reinforcement Learning Framework

The problem is formulated as a Markov Decision Process (MDP):

**State (s):** Current skill representation
- Current procedural code or description
- Skill metadata and usage history
- Agent performance metrics with current skill

**Action (a):** Edit operation to apply
- Type: Addition, Modification, Deletion
- Target: Specific skill component
- Parameters: Edit specifics

**Reward (r):** Downstream task performance
- Primary: Success rate on held-out test tasks
- Secondary: Efficiency metrics (latency, API calls)
- Tertiary: Generalization to new tasks

**Transition:** Apply edit and generate new skill
- LLM-based generation of candidate edits
- Deterministic skill representation update
- Re-evaluation on validation tasks

### Rollback Reward Mechanism

A key innovation is the "rollback reward" that addresses catastrophic failure:

```
Reward(a_t) = α * Performance(s_t+1) - β * |Regression|_t
```

Where:
- α: Weight for improvement signal
- β: Weight for regression penalty
- |Regression|_t: Decrease in performance vs best previous version

This mechanism encourages:
1. Progressive improvement rather than random exploration
2. Conservative modifications that don't degrade existing performance
3. Reverting problematic edits automatically when they cause regression

### Policy Learning

The agent learns a policy π(a|s) that predicts which edit operations are most likely to improve the skill:

```
π(a|s) = P(Edit Type | Current Skill, Task Distribution)
```

Policy training uses:
- **Behavioral Cloning:** Initial learning from human-authored skills or examples
- **Reinforcement Learning:** Refinement using task-based rewards
- **Experience Replay:** Reusing successful edit sequences
- **Curriculum Learning:** Progression from simple to complex skills

## Main Ideas & Contributions

### 1. Skill-α Framework

The paper presents Skill-α, a comprehensive framework for progressive skill generation:

**Key Components:**

1. **Skill Representation:** Skills are represented as modular units with clear interfaces
   - Input specifications
   - Procedural logic (pseudo-code or natural language)
   - Output contracts
   - Dependency declarations

2. **Edit Proposal Generator:** Uses the LLM to propose meaningful edits
   - Analyzes current skill and failure cases
   - Generates candidate modifications
   - Ranks candidates by likelihood of improvement

3. **Skill Evaluator:** Assesses skill quality through agent performance
   - Executes agent with modified skill
   - Collects performance metrics
   - Calculates reward signals

4. **Policy Learner:** Learns which edits to apply in which situations
   - Tracks edit effectiveness patterns
   - Builds edit-success associations
   - Generalizes across similar skills

5. **Validation Module:** Ensures evolved skills maintain reliability
   - Tests on held-out examples
   - Checks for regression on prior tasks
   - Verifies skill composition safety

### 2. Edit Types and Semantics

Different categories of edits serve different improvement purposes:

| Edit Type | Example | Use Case | Risk Level |
|---|---|---|---|
| **Clause Addition** | Add condition or step | Increase specificity | Low |
| **Parameter Tuning** | Adjust thresholds | Optimize efficiency | Low |
| **Procedure Refinement** | Reorganize steps | Improve clarity | Low |
| **Composition** | Combine with other skills | Expand capability | Medium |
| **External Integration** | Connect to tool/API | Add functionality | Medium |
| **Generalization** | Broaden applicability | Improve transfer | Medium |
| **Specialization** | Add domain knowledge | Increase accuracy | Medium |

### 3. Reward Design for Skill Learning

The reward structure balances multiple objectives:

**Primary Reward (Task Success):**
```
r_task = (success_count / total_attempts) * 100
```

**Efficiency Reward:**
```
r_efficiency = 100 * (1 - (tokens_used / baseline_tokens))
```

**Stability Reward:**
```
r_stability = -|current_performance - best_performance|
```

**Composite Reward:**
```
r_total = w1 * r_task + w2 * r_efficiency + w3 * r_stability
```

### 4. Progressive Training Strategy

Training proceeds through phases:

**Phase 1 - Bootstrapping:** (iterations 1-N)
- Use supervised examples to initialize skills
- Behavioral cloning from human-written code
- Establish baseline performance

**Phase 2 - Exploration:** (iterations N+1-2N)
- RL agent explores edit space
- High temperature in proposal generation
- Track which edits improve performance

**Phase 3 - Exploitation:** (iterations 2N+1-3N)
- Focus on high-value edits
- Reduce exploration randomness
- Refine best-performing skill variants

**Phase 4 - Consolidation:** (iterations 3N+1-end)
- Stabilize learned skills
- Verify generalization
- Document final skill specifications

## Methodology & Implementation

### Experimental Setup

**Benchmark Tasks:**
- Code generation (various programming languages)
- Bug fixing and repair
- Test case generation
- Documentation generation
- Refactoring and optimization

**Baseline Comparisons:**
- Static skills (human-authored)
- Random skill generation
- Fine-tuning base LLM
- Other skill learning approaches

### Evaluation Metrics

[Exact figures unavailable — see full paper]

**Learning Efficiency:**
- Number of iterations to reach target performance
- Convergence speed measurement
- Sample efficiency (tasks per learned skill)

**Skill Quality:**
- Task success rate with learned skills
- Performance improvement vs baseline
- Generalization to new task distributions

**Stability Metrics:**
- Regression frequency and magnitude
- Consistency across environments
- Robustness to distribution shift

**Computational Cost:**
- Training time per skill
- Inference overhead
- Memory requirements

### Agent Architecture for Skill Learning

```
┌─────────────────────────────────────────┐
│    Task/Agent Performance Signals       │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│    Reward Calculator                    │
│    ├─ Success Rate                      │
│    ├─ Efficiency Metrics                │
│    └─ Stability Checks                  │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│    Experience Buffer                    │
│    ├─ Edit Sequences                    │
│    ├─ Rewards                           │
│    └─ Performance Traces                │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│    Policy Network                       │
│    ├─ Edit Proposal Distribution        │
│    ├─ Value Estimation                  │
│    └─ Action Selection                  │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│    LLM-based Edit Generator             │
│    ├─ Proposes Candidate Edits          │
│    ├─ Samples from Policy               │
│    └─ Validates Syntax                  │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│    Skill Repository                     │
│    ├─ Current Skills                    │
│    ├─ Intermediate Versions             │
│    └─ Performance History               │
└─────────────────────────────────────────┘
```

### Training Algorithm (Pseudo-code)

```
Initialize: skill_s, policy_π, replay_buffer_B

for episode in 1 to num_episodes:
    state = skill_s
    for step in 1 to max_steps:
        # Get candidate edits
        edits = LLM.propose_edits(state, recent_failures)
        
        # Sample edit from policy
        edit = π.sample(state, edits)
        
        # Apply edit
        new_state = apply_edit(state, edit)
        
        # Evaluate new skill on agent tasks
        reward = evaluate_skill(new_state, validation_tasks)
        
        # Calculate composite reward with rollback
        final_reward = compute_reward_with_rollback(reward)
        
        # Store transition
        B.add((state, edit, new_state, final_reward))
        
        # Update state if improvement
        if final_reward > best_reward:
            state = new_state
            best_reward = final_reward
        
        # Update policy using replay buffer
        if len(B) > batch_size:
            π.update(sample_batch(B))
    
    # Logging and checkpoint
    log_episode_metrics()
```

## Practical Applications & Use Cases

### 1. Domain-Specific Skill Libraries

Skill-α enables development of specialized skills for specific domains:

**Machine Learning Development:**
- Data preprocessing skills
- Model tuning and optimization skills
- Hyperparameter search skills
- Evaluation and analysis skills

**Web Development:**
- Frontend component generation skills
- API integration skills
- Security validation skills
- Performance optimization skills

**Systems Programming:**
- Memory management skills
- Concurrency handling skills
- System call optimization skills
- Performance profiling skills

### 2. Continuous Skill Improvement

Organizations can continuously refine their skill libraries:

1. **Monitor**: Collect agent execution traces and failure cases
2. **Analyze**: Identify skill weaknesses and improvement opportunities
3. **Generate**: Use Skill-α to propose skill enhancements
4. **Validate**: Test proposed improvements on held-out examples
5. **Deploy**: Gradually roll out improved skills

### 3. Cross-Domain Skill Transfer

Learned skills can be adapted to new domains:

- Base skill learned in Language A
- Transfer to Language B with minor edits
- Fine-tune for specific framework or library
- Validate generalization on test set

### 4. Agent Team Coordination

Multiple agents can share and improve skills:

```
Agent 1 → Learns Skill A → Publishes
              ↓
         Skill Repository ← Agent 2 adopts
              ↓
         Agent 3 further improves A
```

### Integration Challenges

1. **Skill Compatibility:** Ensuring improved skills work with existing agent infrastructure
2. **Backward Compatibility:** Maintaining stability when upgrading skills
3. **Performance Monitoring:** Detecting skill regressions in production
4. **Rollback Procedures:** Quick reversion if issues arise

### Cost and Latency Implications

- **Training:** O(T * E) where T = tasks, E = edit iterations
- **Per-Task Overhead:** ~5-10% additional latency for evaluation
- **Storage:** Linear in skill complexity and history
- **API Costs:** Increased LLM calls during learning phase

## Insights & Implications

### Impact on Agent Skill Development

1. **Automated Skill Curation:** Moving from manual skill engineering to learning-based generation
2. **Continuous Improvement:** Skills can improve throughout agent lifecycle
3. **Emergent Specialization:** Unexpected high-performance skills emerging from learning process
4. **Knowledge Preservation:** Learned skills capture organizational knowledge

### Advancement in Skill-Based Frameworks

- **Learning Signal Design:** Better understanding of how to supervise skill generation
- **Sequential Editing:** New paradigm for skill refinement (vs one-shot generation)
- **Policy Learning:** Agents learning which edit operations are effective
- **Compositional Skills:** Insights into how individual skills combine

### Limitations and Open Questions

1. **Skill Representation:** What is the optimal way to represent skills for learning?
2. **Transfer Learning:** How well do skills generalize to different domains?
3. **Compositionality:** Can we formally reason about skill combinations?
4. **Scalability:** How does method scale with skill library size?
5. **Safety Verification:** Can we guarantee learned skills are safe and correct?

### Relevance to Agent Orchestration

This work has implications for how skills are managed in multi-agent systems:

- **Shared Skill Repositories:** Learning benefits extend across agent population
- **Adaptive Skill Selection:** Agents selecting and adapting skills for specific tasks
- **Collaborative Learning:** Skills improving through collective experience
- **Skill Versioning:** Managing multiple skill versions in production

## Code & Resources

**Official Repository:** [Check arXiv page for GitHub link]

**Dependencies:**
- PyTorch or TensorFlow for RL training
- LLM API (GPT-4, Claude, or compatible)
- Task execution environment
- Skill validation framework

**Key Libraries:**
- Stable-Baselines3 (or similar RL library)
- Transformers for LLM fine-tuning
- Gymnasium for task simulation

**Compute Requirements:**
- Training: GPU beneficial (RTX 4090, A100)
- Inference: CPU sufficient
- Memory: 8-32GB depending on skill complexity

**Quick-Start Integration:**

1. Define skill representation format
2. Create task evaluation harness
3. Implement edit proposal generator
4. Set up RL training loop
5. Deploy evaluation infrastructure
6. Start with small skill library
7. Monitor learning curves and stability

## Related Work & Context

### Foundational Research

- **Program Synthesis:** Learning to generate code/procedures
- **Meta-Learning:** Learning to learn in LLMs
- **Reinforcement Learning:** Policy learning and reward design
- **In-Context Learning:** Few-shot skill specification

### Complementary Approaches

- **Fine-tuning:** Direct model adaptation vs skill adaptation
- **Prompt Engineering:** Manual skill specification
- **Retrieval Augmentation:** External skill lookup
- **Multi-Agent Learning:** Collective skill improvement

### Future Research Directions

1. **Theoretical Analysis:** Convergence guarantees and optimality bounds
2. **Interpretable Skills:** Understanding what learned skills encode
3. **Hierarchical Skills:** Composing complex behaviors from simpler skills
4. **Lifelong Learning:** Continuous improvement without catastrophic forgetting
5. **Human-in-the-Loop:** Incorporating human feedback into skill learning
6. **Cross-Modal Skills:** Skills for multimodal agents
7. **Skill Licensing:** Managing intellectual property in shared skill repositories

## Related Topics

- Skill-Based Agent Architectures
- Reinforcement Learning for Agents
- Program Synthesis and Repair
- Policy Learning and Optimization
- Agent Specialization and Adaptation
- Knowledge Representation in Agents
- Multi-Agent Skill Sharing
