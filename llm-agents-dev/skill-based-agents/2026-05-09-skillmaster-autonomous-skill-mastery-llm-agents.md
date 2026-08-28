# SkillMaster: Toward Autonomous Skill Mastery in LLM Agents

**ArXiv ID:** 2605.08693  
**Submitted:** May 9, 2026  
**Revised:** May 12, 2026  
**Publication Venue:** ICLR 2026 (expected)

## Executive Summary

This paper presents SkillMaster, a training framework that enables LLM agents to autonomously create, refine, and select skills for task solving. Unlike existing approaches where skill creation and management are governed by external teachers or hand-designed rules, SkillMaster teaches agents to **learn skill management as a learnable behavior**. The framework uses trajectory-informed skill review and counterfactual utility estimation with DualAdv-GRPO to jointly optimize task-solving actions and skill-editing decisions. With experimental improvements of 8.8% on ALFWorld and 9.3% on WebShop, SkillMaster represents a significant advance in autonomous agent evolution and self-improvement.

## Problem Statement

While skills provide an effective mechanism for improving LLM agents on complex tasks—allowing agents to abstract common patterns into reusable procedures—current approaches have fundamental limitations:

### Current Skill Management Limitations

1. **External Governance**: Skill creation and refinement are typically controlled by:
   - External human teachers or oversight systems
   - Hand-designed rules about when to create skills
   - Auxiliary modules (not learned by the agent itself)
   - Post-hoc analysis of agent trajectories

2. **Lack of Autonomous Learning**: Agents cannot:
   - Decide when new skills are needed
   - Evaluate whether proposed skills are useful
   - Refine skills based on evidence from their own experience
   - Select which skills to use for novel problems

3. **Inefficiency**: Without autonomous skill management:
   - Agents waste time on tasks skills could solve efficiently
   - Redundant skill creation (same skill learned multiple ways)
   - Poor skill reuse across domains
   - Skill bloat without performance justification

4. **Scalability Challenges**: Scaling to large skill libraries requires:
   - Automated skill discovery (not feasible with human oversight)
   - Efficient retrieval among hundreds of skills
   - Automatic skill consolidation and removal of obsolete skills

### Research Gap

No existing framework teaches agents to autonomously manage their own skill development. SkillMaster closes this gap by making skill management **a learnable behavior optimized through reinforcement learning**.

## Core Concepts & Theory

### Skill Definition in SkillMaster

A **skill** is a learned, abstract procedure that an agent can invoke to solve sub-problems. In SkillMaster:

- Skills encapsulate domain-specific patterns and strategies
- Skills are **learnable** through reinforcement learning
- Skill libraries **evolve** as agents gain experience
- Agents autonomously decide when to create, refine, or use skills

### The Skill Management Loop

```
┌─────────────────────────────────────────────────┐
│         Task Execution Episode                   │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 1. Task Observation                       │  │
│  │    (agent perceives task state)           │  │
│  └──────────────────────────────────────────┘  │
│           │                                    │
│           ▼                                    │
│  ┌──────────────────────────────────────────┐  │
│  │ 2. Skill Selection                        │  │
│  │    (choose from library or use base LLM)  │  │
│  └──────────────────────────────────────────┘  │
│           │                                    │
│           ▼                                    │
│  ┌──────────────────────────────────────────┐  │
│  │ 3. Task Solving                           │  │
│  │    (execute action sequence)               │  │
│  └──────────────────────────────────────────┘  │
│           │                                    │
│           ▼                                    │
│  ┌──────────────────────────────────────────┐  │
│  │ 4. Trajectory Collection                  │  │
│  │    (record observation, action sequence,  │  │
│  │     reward, final state)                  │  │
│  └──────────────────────────────────────────┘  │
│           │                                    │
│           ▼                                    │
│  ┌──────────────────────────────────────────┐  │
│  │ 5. Skill Review (Trajectory-Informed)    │  │
│  │    ┌─ Did skill succeed?                 │  │
│  │    ├─ Can we propose a better version?   │  │
│  │    ├─ Should we keep current skill?      │  │
│  │    └─ How can we refine it?              │  │
│  └──────────────────────────────────────────┘  │
│           │                                    │
│           ├─────────────┬──────────────┐       │
│           ▼             ▼              ▼       │
│      Propose New    Refine Existing   Retain  │
│      Skill          Skill             Current │
└─────────────────────────────────────────────────┘
           │             │              │
           └─────────────┴──────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │  Skill Utility Estimation │
            │  (counterfactual test on │
            │   related probe tasks)    │
            └──────────────────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │  DualAdv-GRPO Training   │
            │  (update both task and   │
            │   skill-edit policies)   │
            └──────────────────────────┘
```

### Key Technical Components

#### 1. Trajectory-Informed Skill Review

After each episode, agents perform **reflective analysis**:

```
Trajectory Analysis Prompt:
"""
You are reviewing your performance on a task.

Episode Summary:
- Task: {task_description}
- Actions Taken: {action_sequence}
- Final Result: {success/failure}
- Reward: {episode_reward}

Based on this trajectory:

1. Could a new skill abstract a common pattern
   from your action sequence?

2. Does an existing skill need refinement to
   handle this scenario better?

3. Should existing skills be retained, refined,
   or retired based on utility?

Propose your answer as skill edits.
"""
```

Agents generate skill edit proposals:
- **PROPOSE_NEW_SKILL**: "Create skill X that abstracts pattern Y"
- **REFINE_SKILL**: "Update skill Z to handle case W better"
- **RETIRE_SKILL**: "Skill Z is no longer useful"
- **RETAIN_SKILL**: "Current skills are sufficient"

#### 2. Counterfactual Utility Estimation

For each proposed skill edit, the framework estimates utility via:

**Probe Task Selection**:
- Identify related tasks where the skill might apply
- Select representative probe tasks
- Create synthetic variations

**Utility Measurement**:
```
Utility(Proposed Skill) = 
  Success_Rate(with skill) - Success_Rate(without skill)
  
where both are measured on probe task set
```

This provides direct learning signal for skill-editing decisions: proposals that improve performance on probe tasks get positive reward; those that don't get negative reward.

#### 3. DualAdv-GRPO: Joint Optimization

Standard RL training optimizes a single policy. SkillMaster requires optimizing two interdependent behaviors:

1. **Task-Solving Policy**: Which action to take given state
2. **Skill-Editing Policy**: Whether/how to modify skills

**DualAdv-GRPO** (Dual Advantage Generalized Reward-weighted Policy Optimization):

```
Advantage Function: A(s,a) = Q(s,a) - V(s)

For Task Actions:
  A_task(s,a) = Q_task(s,a) - V(s)
  (reward from completing the task step)

For Skill Edits:
  A_skill(s,edit) = Q_skill(s,edit) - V(s)
  (reward from improved future performance)

Separate Training Paths:
├─ Task Policy Gradient: ∇ log π_task(a|s) * A_task(s,a)
└─ Skill Policy Gradient: ∇ log π_skill(e|s) * A_skill(s,e)

Joint Loss:
  L = α * L_task + (1-α) * L_skill
```

This separation enables:
- Stable training of both policies simultaneously
- Appropriate credit assignment for each policy
- Shared value function for consistency

### Skill Library Architecture

```
Skill Library:
├── Metadata
│   ├─ skill_id: str
│   ├─ description: str
│   ├─ created_date: timestamp
│   ├─ last_used: timestamp
│   ├─ success_rate: float
│   └─ utility_estimate: float
│
├── Invocation Interface
│   ├─ input_specification: Schema
│   ├─ output_specification: Schema
│   └─ dependencies: [Skill]
│
├── Implementation
│   ├─ procedure: str (in natural language or code)
│   ├─ examples: [(input, output)]
│   └─ prerequisites: [condition]
│
└── Evolution History
    ├─ version: int
    ├─ created_from: skill_id (if refined from other)
    └─ modifications: [edit_record]
```

## Main Ideas & Contributions

### 1. Autonomous Skill Creation

**Key Insight**: Agents can learn to propose useful skills by reflecting on their trajectories.

Rather than waiting for external prompting, agents:
- Automatically recognize patterns in their behavior
- Propose skills to abstract repeated patterns
- Validate proposals against probe tasks
- Only commit skills that pass utility threshold

**Result**: Skill creation is continuous and driven by agent experience, not external triggers.

### 2. Trajectory-Informed Reflection

**Key Insight**: An agent's successful trajectory contains evidence of what skills would help.

The framework extracts:
- **Patterns in Actions**: Repeated sequences that could become skills
- **Decision Points**: Places where having a skill would improve choices
- **Failure Analysis**: Why did this task fail? What skill is missing?

This **in-context learning** from own experience is more efficient than learning from external supervision.

### 3. Counterfactual Utility Evaluation

**Key Insight**: Testing proposed skills on related tasks provides objective feedback.

Rather than hand-tuning when to create skills, utility estimation:
- Measures concrete performance impact
- Enables direct comparison of competing skill proposals
- Provides RL training signal (reward for useful skills)
- Prevents skill bloat (unused skills get zero utility)

### 4. Stable Joint Training (DualAdv-GRPO)

**Key Insight**: Task-solving and skill-management are coupled but distinct.

Naive joint training leads to:
- Credit assignment confusion (did reward come from action or skill edit?)
- Policy oscillation (updating both policies simultaneously)
- Unstable convergence

DualAdv-GRPO stabilizes training by:
- Separate advantage estimation for task vs. skill policies
- Independent gradient updates with balanced weighting
- Shared value function for consistency

## Methodology & Implementation

### Experimental Setup

**Benchmarks**:
1. **ALFWorld**: Embodied agents solving household tasks (6 task families, 100+ tasks each)
2. **WebShop**: E-commerce shopping tasks (1000s of variations)

**Baselines**:
- Single-agent without skills
- Agents with pre-created skill libraries
- Agents with external skill creation (non-autonomous)
- State-of-the-art skill-based agents

**Metrics**:
- **Task Success Rate**: Percentage of tasks completed successfully
- **Total Score**: Aggregate metric combining success and task quality
- **Skill Library Size**: Number of learned skills over time
- **Skill Utility**: Average utility of skills in active use
- **Sample Efficiency**: Tasks-to-goal vs. tokens-to-goal

### Key Results

**ALFWorld Performance**:
- Success rate improvement: +8.8% over SOTA
- No task family falls below 95% success rate
- Indicates robust, general skill mastery (not overfitting)

**WebShop Performance**:
- Success rate: improved from 72.7% to 82.0% (+9.3%)
- Overall score: improved from 85.2 to 95.0
- Score > Success indicates agents achieving high-quality solutions (not just task completion)

**Skill Evolution**:
- Agents learn highly task-relevant skills (abstractions of common patterns)
- Skills show transfer: learned on one task family, effective on others
- Skill library stabilizes at ~20-30 skills (not unlimited growth)
- Older skills accumulate higher utility scores

## Practical Applications & Use Cases

### Use Case 1: Programming Assistance

**Scenario**: An autonomous coding agent working on a repository

**Skill Evolution**:
```
Initial: No skills, base LLM only

After Task 1: "optimize_loops_skill"
- Pattern: many tasks involve loop optimization
- Skill: systematic techniques for loop improvements

After Task 2: "documentation_skill"  
- Pattern: well-documented code gets higher scores
- Skill: comment generation and doc-string templates

After Task 3: "error_handling_skill"
- Pattern: error cases need defensive coding
- Skill: common exception patterns and handlers

After Task 10: 
- Agent has specialized skills for: optimization, documentation,
  error handling, testing, refactoring
- Can apply meta-skills: "when to use which skill"
```

As the agent encounters new tasks, it reuses and refines existing skills, improving efficiency.

### Use Case 2: Autonomous Debugging

An agent continuously improves by learning debugging skills:

```
Learned Skills:
├─ trace_execution: Follow program flow to find bugs
├─ hypothesis_testing: Systematically test bug theories
├─ log_analysis: Extract patterns from error logs
└─ root_cause_analysis: Connect symptoms to causes
```

Each new bug provides evidence for refining these skills.

### Use Case 3: Multi-Domain Agent

An agent operating across multiple domains (web, mobile, backend):

```
Common Skills:
├─ test_generation_skill
├─ documentation_skill
└─ refactoring_skill

Domain-Specific Skills:
├─ web:
│   ├─ state_management_skill
│   ├─ routing_skill
│   └─ styling_skill
├─ mobile:
│   ├─ layout_skill
│   ├─ navigation_skill
│   └─ permission_handling_skill
└─ backend:
    ├─ schema_design_skill
    ├─ optimization_skill
    └─ concurrency_skill
```

The agent learns to specialize skills while also developing domain-crossing abstractions.

## Insights & Implications

### Key Findings

1. **Autonomy Works**: Agents can learn skill management as effectively as external systems, with the added benefit of continuous improvement
2. **Trajectory Provides Signal**: Self-reflection on episodes is sufficient to drive skill discovery
3. **Utility Matters**: Counterfactual testing prevents skill bloat and focuses learning on impactful abstractions
4. **Stability Achievable**: DualAdv-GRPO enables joint training without policy oscillation

### Design Principles for Skill-Based Agents

1. **Make Reflection Explicit**: Agents need dedicated reflection mechanism, not implicit in action selection
2. **Measure Skill Utility**: Test skills on probe tasks to provide direct learning signal
3. **Balance Stability**: Separate advantage functions for different policy types
4. **Skill Library Discipline**: Remove/archive low-utility skills to prevent bloat
5. **Version Skills**: Track skill evolution to enable rollback if refinements fail

### When Skill Learning Works Best

- Tasks with **repeated patterns** (skills can abstract them)
- **Large task distributions** (more evidence to learn from)
- **Clear success metrics** (utility can be objectively measured)
- **Sufficient compute budget** (exploration and skill testing cost tokens)

### Limitations

- **Overhead**: Counterfactual utility testing adds computational cost
- **Skill Quality**: Learned skills may be suboptimal; refinement is gradual
- **Domain Transfer**: Skills learned in one domain may not transfer well
- **Explainability**: Learned skills can be opaque compared to hand-designed ones

## Code & Resources

### Implementation Frameworks

The paper likely uses:
- **PyTorch**: Neural network implementations
- **Hugging Face Transformers**: LLM backbone
- **Gym/ALE**: Benchmark environments (ALFWorld, WebShop)
- **RL Libraries**: PPO, GRPO implementations

### Quick-Start Integration Guide

While official code availability [Exact figures unavailable — see full paper], typical integration would:

1. **Define Skill Format**:
   ```python
   @skill
   def refactor_loop(source_code: str) -> str:
       """Refactor loops for efficiency"""
       # LLM-based implementation
       pass
   ```

2. **Setup Skill Library**:
   ```python
   skill_library = SkillLibrary()
   skill_library.register(refactor_loop)
   ```

3. **Enable Autonomous Learning**:
   ```python
   agent = SkillMaster(
       base_model=llm,
       skill_library=skill_library,
       enable_autonomous_creation=True,
       utility_threshold=0.05
   )
   ```

4. **Training Loop**:
   ```python
   for episode in episodes:
       trajectory = agent.episode(task)
       skills_proposed = agent.reflect(trajectory)
       utilities = evaluate_utilities(skills_proposed)
       agent.update_policy(utilities)
   ```

### Dependencies

- Python 3.10+
- PyTorch 2.0+
- Transformers 4.36+
- Environment simulators (ALFWorld SDK, WebShop)

## Related Work & Context

### Foundational Skill-Based Agent Research

- **Voyager**: Lifelong learning through skill accumulation and chain-of-thought reasoning
- **MIND-Skill**: Quality-guaranteed skill generation for agents
- **SkillOS**: Learning skill curation for self-evolving agents
- **SkillCraft**: LLM agents learning tool use skillfully

### Skill Management Approaches

- **Hand-Designed Skills**: Human experts create skill libraries (expensive, limited)
- **Supervised Learning**: External teachers specify when/how to create skills
- **Automatic Extraction**: Post-hoc analysis of successful trajectories
- **Autonomous Learning** (SkillMaster): Agents learn skill management through RL

### Reinforcement Learning Contributions

- **Policy Gradient Methods**: Foundation for gradient-based policy learning
- **Advantage Estimation**: Standard RL technique; SkillMaster's dual-advantage is novel
- **Credit Assignment**: Problem of attributing rewards to actions; dual-advantage approach novel
- **Curriculum Learning**: Related to idea of learned task selection based on skill mastery

## Future Research Directions

1. **Continual Learning**: How do skill libraries evolve over very long horizons (millions of tasks)?
2. **Skill Consolidation**: When/how should similar skills be merged to reduce library size?
3. **Transfer Learning**: Can skills learned in one domain transfer effectively to others?
4. **Skill Interpretability**: How to make learned skills understandable and verifiable?
5. **Multi-Agent Skill Sharing**: Can agents learn from each other's discovered skills?
6. **Skill Security**: How to prevent learned skills from encoding harmful behaviors?

## References & Citation

```bibtex
@article{SkillMaster2026,
  author = {[Authors]},
  title = {SkillMaster: Toward Autonomous Skill Mastery in LLM Agents},
  journal = {International Conference on Learning Representations (ICLR)},
  year = {2026},
  month = {May},
  arxivId = {2605.08693},
  url = {https://arxiv.org/abs/2605.08693}
}
```

## Further Reading

For practitioners implementing skill-based agents:
- See "Agent Skills for Large Language Models" (2602.12430) for architectural patterns
- See "Harnessing Agent Skills" (2606.20631) for reference architecture
- See "SoK: Agentic Skills" (2602.24) for comprehensive skill survey
