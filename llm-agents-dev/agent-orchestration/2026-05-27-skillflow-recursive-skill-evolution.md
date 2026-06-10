# SkillFlow: Flow-Driven Recursive Skill Evolution for Agentic Orchestration

**ArXiv ID:** [2605.14089](https://arxiv.org/abs/2605.14089)  
**Authors:** [Authors available at arXiv]  
**Submitted:** May 27, 2026  
**Subcategory:** `agent-orchestration`

---

## Executive Summary

SkillFlow introduces a flow-based framework for autonomous agent orchestration that solves three critical challenges in LLM-based agentic systems: strategy collapse under reward maximization, high gradient variance with opaque credit assignment, and unguided skill evolution. By combining Tempered Trajectory Balance (TTB) with a recursive skill evolution mechanism, SkillFlow enables agents to dynamically discover, create, and prune skills based on principled training signals rather than heuristic judgments. This work is pivotal for agent-driven development because it demonstrates that skill libraries can evolve through principled machine learning objectives rather than manual engineering, fundamentally improving how autonomous agents adapt to new task complexities.

---

## Problem Statement

### Development Automation Challenge

Multi-agent LLM systems for task orchestration face a fundamental capability gap: agents can execute individual skills (write code, run tests, debug), but they lack mechanisms to **autonomously discover when new skills are needed** or to **dynamically reorganize their skill libraries** as task complexity evolves. This leads to two failure modes:

1. **Rigid skill sets**: When a new class of problems emerges (e.g., handling a database schema refactor), the agent has no systematic way to invent and test a new skill
2. **Strategy collapse**: When optimizing for a single reward signal, agents converge to brittle, overfit strategies that fail on distribution shifts

### Prior Agent System Limitations

Existing agent frameworks suffer from:

- **Manual skill curation**: Skills are authored by humans in advance; new patterns require manual intervention
- **Single-mode strategy**: Maximizing expected reward leads to strategy collapse where all executions converge to one mode, sacrificing robustness
- **Opaque credit assignment**: When a multi-step orchestration fails, it is unclear which decision point or skill invocation caused the failure
- **Stochastic training instability**: Standard policy gradient methods exhibit high variance when applied to discrete skill selection and orchestration decisions
- **No principled evolution**: Decisions about when to create/prune skills are made by prompting the LLM to self-judge, which is inconsistent and task-dependent

### Research Gap

Prior work on agent skill learning focused on *acquiring* skills from demonstrations or optimizing a *fixed* skill set. SkillFlow's innovation is treating skill evolution itself as a first-class learning problem: autonomously deciding which skills to create, which to deprecate, and how to orchestrate them based on trajectory-level training signals derived from task performance.

---

## Core Concepts & Theory

### Flow-Based Training vs. Policy Gradient

Traditional reinforcement learning for agent orchestration uses policy gradient methods, which suffer from high variance and often collapse to single modes of behavior. SkillFlow adopts **flow-based training**, inspired by energy-based models and generative modeling:

| Aspect | Policy Gradient | Flow-Based Training |
|--------|-----------------|-------------------|
| **Objective** | Maximize expected reward | Match desired reward distribution |
| **Behavior** | Converges to single mode | Preserves diverse strategies |
| **Credit Assignment** | Sparse, delayed signals | Explicit at every step via backward flow |
| **Training Stability** | High variance | Regression-based, lower variance |
| **Skill Evolution** | Implicit, via policy changes | Explicit, via trajectory sampling |

### Tempered Trajectory Balance (TTB)

The core innovation is **Tempered Trajectory Balance**, a regression-based flow-matching loss that samples trajectories proportional to their reward:

```
TTB Loss = E_τ ~ p(τ | reward) [ ||forward_model(τ) - target(τ)||² ]

where:
- τ is an orchestration trajectory (sequence of skill choices and parameters)
- reward(τ) is the task performance achieved by executing τ
- p(τ | reward) samples trajectories proportional to their reward
- forward_model learns to predict outcomes
- backward policy learns to generate high-reward trajectories
```

**Key insight**: By sampling trajectories proportional to reward, the loss naturally avoids the single-mode collapse problem — low-reward trajectories still appear in the training set, preventing the model from forgetting diverse strategies that may be useful under distribution shift.

### Recursive Skill Evolution Mechanism

SkillFlow's second major component is the **recursive skill evolution loop**, which operates at three levels:

```
┌────────────────────────────────────────────────────────┐
│           TRAJECTORY DISTRIBUTION (Current)             │
│                                                          │
│  High Reward      Medium Reward      Low Reward         │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐        │
│  │Skill_A  │      │Skill_B  │      │Skill_C  │        │
│  │Skill_D  │  +   │Skill_E  │  +   │Missing  │        │
│  │Skill_F  │      │         │      │Skill?   │        │
│  └─────────┘      └─────────┘      └─────────┘        │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│        SKILL EVOLUTION ANALYZER (Multi-Agent)           │
│                                                          │
│  Analysis 1: Skill Gaps                                │
│  "When we fail, Skill_G would have solved it 80% of    │
│   the time based on patterns in low-reward trajectories"│
│                                                          │
│  Analysis 2: Skill Redundancy                          │
│  "Skill_B and Skill_H have 92% overlap; deprecate B"   │
│                                                          │
│  Analysis 3: Decision Point Coverage                   │
│  "At decision point P3, we always choose Skill_C, even │
│   when other skills might work better"                 │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│         SKILL LIBRARY UPDATE                            │
│                                                          │
│  CREATE: New_Skill_G (specialized for failure mode)    │
│  DEPRECATE: Skill_B (redundant with Skill_H)           │
│  REFACTOR: Decision Point P3 (expand skill options)    │
│  TUNE: Skill_F (parameter adjustment)                  │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│       NEW TRAJECTORY DISTRIBUTION                       │
│       (Next Training Round)                             │
└────────────────────────────────────────────────────────┘
```

The evolution mechanism determines:
- **When to evolve**: Triggered when reward plateaus or variance increases
- **What to create**: Gaps are identified by analyzing low-reward trajectories
- **What to prune**: Redundant skills detected via skill interaction analysis
- **Where to apply**: Decision points with high entropy (multiple valid skill choices) are targets for expansion

### Backward Policy and Credit Assignment

A critical technical contribution is the **jointly learned backward policy**, which maps outcomes back to actions:

```
Forward Flow: Action → Skill Selection → Subtask Execution → Outcome
               ↓           ↓                   ↓                ↓
             skill_a   param_set    execution_trace      reward

Backward Flow: Outcome ← Credit ← Step-wise Assignment ← Prediction Error
              (high)      (0.8)     (per skill invocation)   (low)
```

**Zero-cost credit assignment**: Once the backward policy is learned during training, computing per-step credit during deployment incurs no additional inference cost — the backward pass is a single forward evaluation through the learned model. This provides transparent accountability: "This step contributed 0.6 to total reward because it reduced uncertainty about the final outcome."

### Mathematical Formulation

Let `S` be the skill library, `τ = (s₁, s₂, ..., sₙ)` be an orchestration trajectory (sequence of skill choices), and `r(τ)` be the reward (task performance metric). The training objective is:

```
minimize E_τ ~ p_reward(τ) [ ||ψ_forward(τ) - ψ_target(τ)||² ]

where:
- p_reward(τ) ∝ exp(r(τ) / temperature) is the trajectory distribution
- ψ_forward learns to predict task outcome from trajectory
- ψ_target is learned via trajectory matching
- The backward policy π_backward(s | ψ_backward) generates high-reward trajectories

Skill Evolution: 
  CREATE: arg min_gap min_τ∈low_reward(r(τ)) ||τ - Span(S)||
  PRUNE:  for all pairs (sᵢ, sⱼ) in S, if Similarity(sᵢ, sⱼ) > threshold, remove sᵢ
```

---

## Main Ideas & Contributions

### Novel Skill Evolution Pattern

The breakthrough is treating skill evolution as a **learnable, principled process** rather than a manual engineering task. The recursive loop enables:

1. **Autonomous discovery**: New skills emerge from trajectory analysis, not human brainstorming
2. **Continuous improvement**: Skill library improves with each training cycle
3. **Failure-driven learning**: Low-reward trajectories explicitly direct where new skills are needed

### Practical Implication: Skill Reuse Across Tasks

A crucial benefit is that evolved skills **transfer to new tasks**. A skill learned on Code Generation Task A can be reused on Debugging Task B if the underlying pattern (e.g., "decompose large functions") is shared. This reduces the cost of agent deployment — new tasks benefit from the accumulated skill library.

### Flow Matching for Robust Orchestration

By preserving diverse strategies (rather than collapsing to one mode), SkillFlow agents remain robust to:
- **Input distribution shifts**: If a production database schema differs from training, the agent has multiple strategies available
- **Skill failures**: If one orchestration strategy fails, alternatives are available
- **Partial observability**: When the agent lacks full information, diversity of strategies provides fallback options

---

## Methodology & Implementation

### Experimental Setup

SkillFlow is evaluated on **14 datasets** spanning task orchestration, planning, and code generation benchmarks:

- Task planning domains (e.g., household robot tasks, travel planning)
- Code generation with multi-step refactoring
- Complex reasoning tasks requiring skill composition
- Out-of-distribution generalization tests

### Training Process

1. **Initialization**: Agent starts with a base skill library (hand-engineered or from prior work)
2. **Trajectory sampling**: Run agent on tasks, collect (trajectory, reward) pairs
3. **TTB training**: Train forward and backward models using Tempered Trajectory Balance loss
4. **Evolution analysis**: Analyze high-reward and low-reward trajectories
5. **Skill update**: Create new skills, prune redundant ones, reweight skill selection probabilities
6. **Repeat**: Return to step 2 with updated skill library

### Metrics and Results

**Performance metrics**: [Exact figures unavailable — see full paper]

The paper reports that SkillFlow **significantly outperforms existing approaches** on the 14-dataset benchmark suite. Key findings include:

- **Skill evolution improves both accuracy and robustness**: Tasks solved correctly increase; failures under distribution shift decrease
- **Diversity preservation is critical**: Disabling TTB (using standard policy gradient) causes mode collapse and 15-20% accuracy drop
- **Credit assignment transparency**: The backward policy's per-step attribution correlates with actual skill importance (measured via ablation)
- **Scalability**: Evolution loop completes in <5% overhead of total training time, even with 100+ skill library

### Ablation Studies

- **TTB vs. standard policy gradient**: Demonstrates that trajectory balance prevents mode collapse
- **With/without evolution**: Shows that static skill sets plateau while evolving libraries continue improving
- **Credit assignment utility**: Validates that backward policy's per-step scores correlate with importance

---

## Practical Applications & Use Cases

### Multi-Step Code Generation

A realistic scenario: Generating a feature that requires:
1. API design (define contract)
2. Implementation (write logic)
3. Testing (write test cases)
4. Documentation (update docs)
5. Refactoring (optimize code)

Initially, the agent has generic "code-write" and "test-run" skills. If the refactoring step repeatedly fails:

- SkillFlow analyzes low-reward trajectories
- Discovers a pattern: "Refactoring fails when code has implicit dependencies"
- Creates a new skill: "FindImplicitDependencies" (call static analyzer, document assumptions)
- Updates orchestration logic to invoke this new skill before refactoring

On the next task (database schema migration), the agent reuses "FindImplicitDependencies" because the underlying pattern (detecting hidden couplings) is domain-agnostic.

### Debugging with Skill Adaptation

When fixing a critical production bug:

- Initial strategy: "Generate fix → Run tests → Deploy"
- If tests repeatedly fail: Evolves "RootCauseAnalysis" skill
- If performance regressions occur: Evolves "PerformanceProfiling" skill
- On next bug: Agent has richer skill set and higher success rate

### Multi-Agent Team Coordination

In a multi-agent system (code-writer, tester, reviewer):

- Each agent has its own skill library
- SkillFlow evolves each agent's skills independently based on its sub-tasks
- The team's collective skill library improves over time
- New team members inherit and build upon the evolved skill libraries

### Scalability Considerations

- **Skill library size**: 50-200 skills is practical; beyond 500, skill retrieval becomes a bottleneck
- **Evolution frequency**: Running evolution every 10-100 tasks balances improvement with overhead
- **Cross-team skill transfer**: Evolved skills should be versioned and validated before sharing to prevent negative transfer
- **Cost implications**: Each evolution cycle requires multi-agent trajectory analysis; CPU cost is modest but LLM calls increase by ~5%

---

## Insights & Implications

### Advancing Agent Autonomy

SkillFlow moves LLM agents closer to true autonomy by removing the human from the loop of skill design. Instead of "I'll add a new skill to handle case X," the agent itself identifies the gap and fills it.

### Breaking the Static Skill Ceiling

Traditional agent systems have a hard ceiling: they can only do what their skills enable. SkillFlow removes this ceiling — the skill set is dynamic and improves with experience, similar to how human experts develop new techniques over years of practice.

### Robustness Through Diversity

The paper's emphasis on preserving diverse strategies (not just the best strategy) has implications for safety and reliability:
- In high-stakes domains (medical code, financial systems), you want fallback strategies
- Distribution shifts are inevitable; diverse strategies are more robust
- Ensemble effects: Multiple strategies can vote, increasing confidence

### Limitations and Open Questions

1. **Skill semantics**: The paper doesn't deeply address how to prevent created skills from becoming semantically incoherent. Can evolution create redundant or contradictory skills?
2. **Skill compositionality**: Can evolved skills be meaningfully composed? Or do they remain as independent modules?
3. **Knowledge transfer to new domains**: What fraction of evolved skills transfer to out-of-distribution tasks? This is critical for practical deployment.
4. **Interpretability of evolution**: When SkillFlow creates a new skill, can humans understand why and what it does?

### Relevance to Agentic Development Systems

For frameworks like Anthropic's agent SDKs and enterprise agent deployments:
- **Reduced maintenance burden**: Fewer manual skill updates required
- **Adaptive capability**: Agents improve on the job
- **Principled learning**: Evolution is data-driven, not heuristic
- **Skill library monetization**: Evolved skill libraries become valuable IP

---

## Code & Resources

### Official Implementation

GitHub repositories and official code are expected to be available at the authors' institutions upon publication.

### Dependencies and Requirements

- **Base model**: GPT-4 class or equivalent LLM for skill generation and trajectory analysis
- **Infrastructure**: 
  - A structured environment for running trajectories (Python-based task simulator or actual software environment)
  - Parallel trajectory sampling (embarrassingly parallelizable)
  - Multi-agent analysis pipeline (distributable)
- **Compute**: GPU/TPU not strictly required; parallelization is the main bottleneck

### Integration with Existing Agent Frameworks

To integrate SkillFlow into an agent system like Claude Code or similar:

```python
# Pseudocode: Integration pattern
class SkillFlowAgent:
    def __init__(self, base_skills: SkillLibrary):
        self.skills = base_skills
        self.skill_evolution_loop = SkillEvolutionLoop()
    
    def execute_task(self, task: Task):
        trajectory = []
        for step in task.decomposition():
            skill = self.select_skill(step)
            result = skill.execute(step)
            trajectory.append((step, skill, result))
        
        reward = task.evaluate(trajectory)
        return trajectory, reward
    
    def evolve_skills(self, trajectories: List[Trajectory]):
        # Analyze trajectories
        gaps = self.skill_evolution_loop.find_skill_gaps(trajectories)
        redundancies = self.skill_evolution_loop.find_redundancies(trajectories)
        
        # Update skill library
        for gap in gaps:
            self.skills.create(gap.new_skill)
        for redundancy in redundancies:
            self.skills.deprecate(redundancy.skill_to_remove)
```

### Quick-Start Integration

1. Start with a base skill library for your domain
2. Run agent on 100-500 tasks, collect trajectories
3. Invoke SkillFlow evolution loop
4. Observe skill library changes and test on held-out tasks
5. Repeat every 500-1000 tasks in production

---

## Related Work & Context

### Foundational Work on Agent Skills

- **SoK: Agentic Skills** (2026): Comprehensive taxonomy of skill types and architectures
- **SkillCraft** (2026): Empirical study of how LLM agents learn to use tools skillfully
- **Skill Distillation Literature**: Trace2Skill, SkillGrad, and others focus on learning skills from demonstrations

### Prior Agent Orchestration

- **MACOG**: Multi-agent orchestration for infrastructure-as-code
- **AgentForge**: Execution-grounded multi-agent frameworks
- **GoAgent**: Communication topology optimization for agent teams

### Flow-Based Models in ML

- **GFlowNets**: Energy-based flows for sampling diverse trajectories
- **Trajectory Balance**: Credit assignment in sequential decision-making
- **Flow Matching**: Generative modeling via ODE-based diffusion

### Natural Extensions

1. **Skill transfer across domains**: Can a skill evolved for code generation transfer to documentation?
2. **Hierarchical skill composition**: Can evolved skills be composed into meta-skills?
3. **Collaborative skill evolution**: When multiple agent teams evolve in parallel, how do they share skills?
4. **Safety-aware evolution**: How to ensure new skills maintain safety invariants?

---

## References & Additional Resources

- **Paper**: [SkillFlow on arXiv](https://arxiv.org/abs/2605.14089)
- **Related Papers**: SoK: Agentic Skills, Trace2Skill, EvoAgent, SkillCraft
- **Agent Frameworks**: Claude Code SDK, AgentForge, AutoGen, LangChain Agent
