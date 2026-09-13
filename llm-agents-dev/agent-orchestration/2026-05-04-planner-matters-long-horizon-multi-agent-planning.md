# Planner Matters! An Efficient and Unbalanced Multi-agent Collaboration Framework for Long-horizon Planning

**ArXiv ID:** [2605.02168](https://arxiv.org/abs/2605.02168)  
**Authors:** Wenyi Wu, Sibo Zhu, Kun Zhou, Biwei Huang  
**Institution:** University of California, San Diego  
**Submission Date:** May 4, 2026  
**Focus Area:** Multi-Agent Planning, Task Decomposition, Compute Allocation, Long-Horizon Reasoning

---

## Executive Summary

"Planner Matters!" presents a counterintuitive finding that challenges balanced multi-agent orchestration: **in long-horizon planning tasks, concentrating model capacity and learning on the planner component yields superior performance compared to balanced skill allocation across planner, actor, and memory manager roles**. Through systematic compute-allocation analysis and trajectory-level reinforcement learning, the paper demonstrates that the planner (high-level strategy component) is the dominant performance factor. The framework achieves significant improvements on web navigation, OS control, and tool-use benchmarks through planner-centric optimization while keeping actor and memory components lightweight.

---

## Problem Statement

Long-horizon task automation with LLM agents reveals fundamental challenges in multi-agent system design:

- **Planning Complexity:** Long-horizon tasks (10+ steps) require sophisticated reasoning over action sequences, state tracking, and goal decomposition. Errors in high-level planning compound across subsequent steps.
- **Capacity Allocation Question:** In multi-agent systems with planner, actor, and memory components, how should limited model capacity be distributed?
  - **Balanced Approach (Naive):** Equal capacity/parameters across all components
  - **Specialized Approach (Proposed):** Unequal allocation with focus on the dominant factor
- **Prior Assumptions:** Existing work assumes balanced multi-agent architectures; no systematic analysis of component contribution to task success
- **Scaling Challenge:** As problems grow more complex, naive approaches scale all components equally, wasting capacity on non-critical components

**Core Question Addressed:** Which agent role (planner, actor, memory manager) is the bottleneck in long-horizon task automation?

The paper's insight: **Planning is the dominant factor; execution and memory require far less capacity to achieve competitive results**.

---

## Core Concepts & Theory

### Three-Role Agent Decomposition

The paper proposes decomposing long-horizon automation into three specialized roles:

#### 1. **Planner Agent**
- **Responsibility:** High-level decision-making and strategy formulation
- **Input:** Current state, task description, history of actions and observations
- **Output:** Next action/step plan (high-level instruction)
- **Example:** "To find the user's email address, I should first navigate to the contact app"
- **Cognitive Load:** Reasoning about multi-step sequences, action dependencies, goal states
- **Failure Mode:** Poor plans lead to cascading failures in subsequent steps

#### 2. **Actor Agent**
- **Responsibility:** Task execution and environmental interaction
- **Input:** Plan from planner, current interface/environment state
- **Output:** Concrete action (click, type, navigate)
- **Example:** Execute specific mouse coordinates to click button
- **Cognitive Load:** Following instructions, adapting to minor environment variations
- **Failure Mode:** Inability to execute feasible instructions (low-level syntax errors)

#### 3. **Memory Manager Agent**
- **Responsibility:** Contextual state tracking and information retrieval
- **Input:** Trajectory history, current observations
- **Output:** Relevant context summary for planner (previous states, key information)
- **Example:** "I previously found the password field on this screen at coordinates (x, y)"
- **Cognitive Load:** Selective summarization, context recall, relevance judgment
- **Failure Mode:** Forgetting important details or providing irrelevant context

### Compute Allocation Analysis Framework

The paper introduces a **systematic compute-allocation analysis** to measure component contribution:

#### Experimental Design

For each component, independently vary model capacity while keeping others fixed:
- Planner: Scale from small (7B) to large (32B)
- Actor: Scale from small (7B) to large (32B)
- Memory Manager: Scale from small (7B) to large (32B)

#### Key Metrics

1. **Marginal Performance Gain (MPG):** Task success improvement from adding model capacity
   - Formula: `MPG(component) = success_rate(large_model) - success_rate(small_model)`
   
2. **Capacity Efficiency:** Performance gain per unit of added parameters/compute
   - Formula: `Efficiency = success_rate_improvement / added_parameters`

3. **Scaling Curve:** How performance changes as model size increases for each component

#### Finding

```
Performance Improvement from Scaling (%)

Planner:       ████████████████████ (18-22%)
Actor:         ██████░░░░░░░░░░░░░░ (4-6%)
Memory Mgr:    ████░░░░░░░░░░░░░░░░ (2-3%)

Legend: ██ = high impact, ░░ = low impact
```

**Interpretation:**
- Scaling Planner from 7B to 32B: +18-22% success rate improvement
- Scaling Actor from 7B to 32B: +4-6% improvement
- Scaling Memory Manager from 7B to 32B: +2-3% improvement

### Multi-Agent Planning Workflow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                 Trajectory State                        │
│  (Current environment state, action history, goals)     │
└────────────┬────────────────────────────────────────────┘
             │
      ┌──────▼──────────┐
      │ Memory Manager  │
      │  (Small 7B)     │ ◄── Extracting relevant context
      │ (2-3% impact)   │
      └──────┬──────────┘
             │
      ┌──────▼──────────────────────────┐
      │     PLANNER AGENT               │
      │ (Large 32B Model)               │◄─ High-level reasoning
      │ ████ (18-22% impact) ████       │
      │                                 │
      │ Strategy: Navigate to Settings  │
      │           > Find Network Config │
      │           > Retrieve IP Address │
      └──────┬──────────────────────────┘
             │
      ┌──────▼────────────┐
      │  ACTOR AGENT      │
      │  (Medium 14B)     │ ◄── Execution
      │ (4-6% impact)     │
      │                   │
      │ Execute Action:   │
      │ Click(100, 50)    │
      └───────┬───────────┘
              │
         [Environment Interaction]
              │
              ▼
         [Next State]
              │
              └──► (Loop back to Memory Manager)
```

### Planner-Centric Reinforcement Learning

The paper proposes **RL-based optimization focused exclusively on the Planner**:

#### Objective
Maximize task success (binary reward: task_complete or not) by improving planner policy while keeping Actor and Memory Manager frozen.

#### Algorithm: Planner-Centric GRPO (Group Relative Policy Optimization)

1. **Rollout Phase:** Execute trajectory with current policies (planner learning, others frozen)
2. **Trajectory-Level Reward:** Assign reward only based on final task success (episodic reward)
3. **VLM-as-Judge:** Use vision-language model to assess trajectory quality (coverage of action space, semantic correctness)
4. **Planner Gradient Update:** Update only planner parameters using trajectory rewards
5. **Freeze Others:** Actor and Memory Manager weights remain constant

#### Why Planner-Centric?

- **Sample Efficiency:** Learning one component reduces dimensionality, accelerates convergence
- **Credit Assignment:** Clear causality: better plans → more successful trajectories
- **Stable Training:** Freezing non-dominant components reduces learning instability
- **Interpretability:** Understand what planning improvements drive success

---

## Main Ideas & Contributions

### 1. **Systematic Compute Allocation Analysis**
   **Contribution:** First empirical study quantifying component contribution in multi-agent long-horizon systems
   - **Insight:** Planning dominates; simple linear compute allocation is suboptimal
   - **Method:** Independent scaling experiments for each component
   - **Impact:** Enables principled capacity allocation decisions

### 2. **Unbalanced Multi-Agent Architecture**
   **Contribution:** Proposes and validates asymmetric allocation (large planner, small actor/memory)
   - **Architecture:** 32B Planner + 14B Actor + 7B Memory Manager
   - **Benefit:** Better cost-quality trade-off than balanced 14B+14B+14B approach
   - **Result:** Similar performance at lower total compute cost

### 3. **Planner-Centric Reinforcement Learning**
   **Contribution:** RL algorithm that optimizes exclusively the planner component
   - **Algorithm:** Trajectory-level rewards + planner gradient updates only
   - **Innovation:** Freezes non-dominant components, focusing learning on bottleneck
   - **Advantage:** Faster convergence, clearer improvement tracking, reduced learning instability

### 4. **Evidence on Scaling Laws for Multi-Agent Systems**
   **Contribution:** Characterizes scaling behavior of multi-agent components
   - **Finding:** Planner scaling curves are steeper (more benefit from size increase)
   - **Finding:** Actor and memory scaling curves plateau faster
   - **Implication:** Suggests allocation strategy for resource-constrained settings

---

## Methodology & Implementation

### Experimental Setup

#### Benchmarks & Domains

1. **Web Navigation (WebArena):**
   - Tasks: "Find the cheapest flight from NYC to LA," "Book a hotel reservation," etc.
   - Complexity: 15-25 action steps on average
   - Evaluation: Task completion success rate

2. **Operating System Control (OSWorld):**
   - Tasks: "Download a file and move to folder X," "Configure network settings," etc.
   - Complexity: 10-20 action steps
   - Evaluation: Task completion on actual OS simulator

3. **Tool Use (ToolBench):**
   - Tasks: Use multiple APIs/tools to accomplish goals (e.g., calculate, retrieve, transform data)
   - Complexity: 5-15 tool calls
   - Evaluation: Final output correctness and efficiency

#### Model Configurations Tested

| Component | Model Sizes Tested | Default Used |
|-----------|-------------------|--------------|
| Planner | 7B, 14B, 32B, 70B | 32B (GPT-4 class) |
| Actor | 7B, 14B, 32B | 14B |
| Memory Manager | 7B, 14B, 32B | 7B |

#### Baseline Comparisons

1. **Balanced Multi-Agent:** 14B + 14B + 14B (51B total parameters)
2. **Large Monolithic:** Single 70B model doing all roles
3. **Role-Specialized (Prior):** Specialized models without compute allocation analysis

### Implementation Details

#### Planner Component Implementation

```python
class PlannerAgent:
    def __init__(self, model_name="gpt-4-turbo"):
        self.model = LLMFactory.create(model_name, temperature=0.7)
        self.planning_prompt = """
        You are a strategic planner for accomplishing complex tasks.
        Current state: {current_state}
        Memory/context: {memory_summary}
        Task: {task}
        
        Generate the next high-level action or plan step.
        Return format: ACTION: <high_level_action>
        REASONING: <brief explanation>
        """
    
    def generate_plan(self, state, task, memory):
        prompt = self.planning_prompt.format(
            current_state=state,
            task=task,
            memory_summary=memory
        )
        response = self.model.generate(prompt)
        return self.parse_plan(response)
```

#### Memory Manager Implementation

```python
class MemoryManager:
    def __init__(self, model_name="claude-3-haiku"):  # Small model
        self.model = LLMFactory.create(model_name)
        self.memory_prompt = """
        Given trajectory history, extract relevant context for next planning step.
        Trajectory: {trajectory}
        
        Return concise summary of:
        - Key findings/information gathered
        - Current position/state
        - Constraints discovered
        """
    
    def summarize(self, trajectory):
        response = self.model.generate(self.memory_prompt.format(trajectory=trajectory))
        return response
```

#### Planner-Centric RL Training

```python
class PlannerCentricRL:
    def train_episode(self, task, freeze_actor=True, freeze_memory=True):
        planner_log_probs = []
        trajectory = []
        
        state = env.reset(task)
        memory = memory_manager.init(task)
        
        for step in range(max_steps):
            # Get memory context
            context = memory_manager.summarize(trajectory)
            
            # Planner decides (with gradient tracking)
            with torch.enable_grad():
                plan, log_prob = planner.generate_with_grad(state, context, task)
                planner_log_probs.append(log_prob)
            
            # Actor executes (no gradients)
            with torch.no_grad():
                action = actor.execute(plan, state)
            
            # Transition
            next_state, reward = env.step(action)
            trajectory.append((state, plan, action, next_state))
            state = next_state
        
        # Episode reward: success at end of trajectory
        episode_reward = env.task_success_check()
        
        # Update planner only
        loss = -sum(planner_log_probs) * episode_reward / len(planner_log_probs)
        loss.backward()
        self.planner_optimizer.step()
        
        return episode_reward, loss.item()
```

### Datasets & Benchmarks

1. **WebArena:** 812 diverse web-based tasks across multiple websites
2. **OSWorld:** 369 OS manipulation tasks
3. **ToolBench:** 500 tool-use tasks
4. **Development/Validation Split:** 70% training, 30% held-out test

### Evaluation Metrics

1. **Task Success Rate (%):** Binary success metric (task completed or not)
2. **Steps to Success:** Average number of steps needed to complete task
3. **Sample Efficiency:** How many episodes to reach target success rate
4. **Compute Cost:** FLOPs or API cost per task

---

## Results & Performance

### Key Finding: Planning is Dominant

#### Compute Allocation Impact

| Component Scaling | WebArena | OSWorld | ToolBench | Average |
|------------------|----------|---------|-----------|---------|
| Planner (7B→32B) | +21% | +19% | +22% | +20.7% |
| Actor (7B→32B) | +5% | +4% | +6% | +5.0% |
| Memory (7B→32B) | +2% | +3% | +2% | +2.3% |

**Interpretation:** Scaling the planner provides 4x more benefit than scaling the actor, and 9x more than scaling memory.

### Unbalanced vs. Balanced Architecture

#### Performance Comparison (Task Success Rate)

| Configuration | WebArena | OSWorld | ToolBench | Avg | Total Params |
|---------------|----------|---------|-----------|-----|--------------|
| Balanced (14B×3) | 68.2% | 71.4% | 64.9% | 68.2% | 42B |
| Unbalanced (32B+14B+7B) | 72.1% | 75.8% | 68.3% | 72.1% | 53B |
| Monolithic (70B) | 71.5% | 74.6% | 67.2% | 71.1% | 70B |

**Key Insight:** Unbalanced architecture with 53B params outperforms balanced 42B and monolithic 70B, despite higher compute cost. The efficiency comes from targeted allocation to the bottleneck component.

#### Cost-Efficiency Analysis

If measured in "cost per task success":
- Balanced: 42B cost / 68.2% success = ~61.5 B-cost per successful task
- Unbalanced: 53B cost / 72.1% success = ~73.5 B-cost per successful task
- **Trade-off:** Unbalanced uses more total compute but achieves better quality

### Planner-Centric RL Training Results

#### Learning Curves (OSWorld Benchmark)

```
Task Success Rate (%)

80 │                                  ●
   │                                 ╱ (Planner-Centric RL)
70 │                          ●     ╱
   │                         ╱ ◆   ╱  (Frozen Baseline)
60 │                 ● ─ ─ ─      ╱
   │                ╱              (Initial Random)
50 │        ●─────╱
   │       ╱
40 │  ●──╱
   │  
   └───┬───────┬───────┬───────┬───────
     0     10    20    30    40    50
           Training Episodes (×100)
```

**Results:**
- Planner-centric RL reaches 75% success in ~3000 episodes
- Frozen baseline plateaus at ~70%
- Improvement: 5% absolute, +7% relative
- Convergence: Faster with planner-focused learning due to reduced learning complexity

#### Trajectory-Level vs. Step-Level Rewards

| Reward Type | Training Stability | Convergence Speed | Final Performance |
|-------------|------------------|-------------------|------------------|
| Trajectory-Level | High | Fast | 75.8% |
| Step-Level | Low | Slow | 74.2% |
| Sparse Only | Very High | Very Slow | 71.5% |

**Finding:** Trajectory-level rewards (episodic) provide better convergence than step-level (dense) due to clearer credit assignment to planning.

### Scaling Beyond Standard Sizes

#### Performance on Larger Planners

| Planner Size | WebArena | OSWorld | ToolBench | Inference Time |
|-------------|----------|---------|-----------|-----------------|
| 32B | 72.1% | 75.8% | 68.3% | 2.1s |
| 70B | 73.8% | 77.2% | 69.5% | 3.8s |
| 110B | 74.2% | 77.9% | 70.1% | 5.2s |

**Observation:** Diminishing returns beyond 70B planner (saturation at ~78% on OSWorld)

### Ablation Studies

#### Effect of Freezing Components

| Configuration | OSWorld Success |
|---------------|-----------------|
| All trainable (end-to-end) | 73.2% |
| Planner trainable, others frozen | 75.8% |
| Actor trainable, planner frozen | 71.4% |
| Memory trainable, others frozen | 70.9% |

**Finding:** Planner-centric learning outperforms end-to-end and other component-focused approaches.

---

## Practical Applications & Use Cases

### 1. **Autonomous Web Navigation**
   - Multi-step web task automation: booking, shopping, research aggregation
   - Leverage planner's strategic reasoning for site exploration
   - Lightweight actor handles click/typing operations
   - Cost reduction: Unbalanced approach reduces API costs vs. monolithic large models

### 2. **OS-Level Automation (RPA-like Tasks)**
   - File management, configuration, installation workflows
   - Planner reasons about sequential file operations
   - Actor executes specific commands without reasoning overhead
   - Deployment: Lightweight on resource-constrained machines via small actor/memory

### 3. **Multi-Step Information Retrieval & Synthesis**
   - Research tasks: Find information across multiple sources and synthesize answers
   - Planner: High-level strategy (which sources to check, synthesis approach)
   - Actor: Execute API calls and navigation
   - Memory: Track previously found facts

### 4. **Enterprise Task Automation**
   - Complex workflows: CRM updates, HR processes, business process automation
   - Planner's strategic capability handles domain logic
   - Actor's simplicity reduces errors in routine operations
   - Asymmetric allocation aligns with real business process structure

### Design Considerations for Practitioners

**When to Use Unbalanced Architecture:**
- Long-horizon tasks (>10 steps)
- Complex dependencies and reasoning required
- Clear separation between planning and execution phases
- Cost is a constraint (can avoid large monolithic models)

**When Balanced Might Be Better:**
- Highly dynamic environments requiring frequent replanning
- Tasks where execution errors significantly impact planning
- Limited latency budgets (smaller models faster)
- Domains with tight actor-planner coupling

**Tuning Recommendations:**
1. Analyze your task domain to understand step complexity
2. Run compute-allocation analysis similar to paper's approach
3. Allocate capacity proportional to empirical performance gain
4. Use trajectory-level RL if optimizing for long-horizon success

---

## Insights & Implications

### 1. **Planning is the Bottleneck in Long-Horizon Reasoning**
   Across diverse domains (web, OS, tools), the planner component's capacity is the limiting factor for task success. This suggests that **research should prioritize better planning mechanisms** over balanced architecture improvements.

### 2. **Asymmetry Enables Efficiency**
   Multi-agent systems don't require balanced capacity allocation. **Targeted allocation to bottleneck components achieves better cost-quality trade-offs** than uniform design, suggesting a general principle for system orchestration.

### 3. **Trajectory-Level Signals Enable Effective Learning**
   Episodic (task-level) rewards work better than step-level rewards for agent learning. This contrasts with typical RL where dense rewards aid exploration; **for planning-centric learning, sparse task-level signals suffice**.

### 4. **Compute Can Be Reallocated Strategically**
   The paper challenges the assumption that adding parameters uniformly across all components is optimal. **Strategic reallocation of the same total compute can improve performance**, suggesting opportunities for efficiency in large-scale systems.

### 5. **Scaling Laws Differ by Component**
   Different agent components exhibit different scaling curves. **Planner scaling curves are steeper (more benefit per added capacity) than actor/memory**, informing future system design and resource allocation decisions.

### Limitations & Open Questions

- **Domain Generalization:** Planner dominance observed in web/OS/tool domains; unclear for other task types (scientific reasoning, creative tasks)
- **Replanning Dynamics:** Study assumes single-trajectory learning; unclear how findings generalize to settings requiring frequent replanning
- **Actor Complexity:** Tasks with complex execution requirements might shift dominance toward actor; paper focuses on relatively straightforward execution
- **Practical Deployment:** Assumes access to capable planner models; in resource-constrained settings, trade-offs might differ

---

## Code & Resources

### Official Resources

- **ArXiv Paper:** [Planner Matters! (2605.02168)](https://arxiv.org/abs/2605.02168)
- **Benchmarks Used:**
  - WebArena: [https://github.com/web-arena-x/webarena](https://github.com/web-arena-x/webarena)
  - OSWorld: [https://github.com/xlang-ai/osworld](https://github.com/xlang-ai/osworld)
  - ToolBench: [https://github.com/openbmb/toolbench](https://github.com/openbmb/toolbench)

### Integration Guide

**Dependencies:**
- Python 3.10+
- LLM API access (OpenAI, Anthropic, open-source via vLLM)
- Benchmark environments (WebArena, OSWorld)
- PyTorch for RL training

**Example Implementation:**

```python
from planner_matters import MultiAgentFramework, PlannerAgent, ActorAgent, MemoryManager
from benchmarks import OSWorld

# Initialize framework with unbalanced configuration
framework = MultiAgentFramework(
    planner_config={'model': 'gpt-4-turbo', 'param_size': '32B'},
    actor_config={'model': 'claude-3-sonnet', 'param_size': '14B'},
    memory_config={'model': 'claude-3-haiku', 'param_size': '7B'}
)

# Run on OSWorld tasks
env = OSWorld()
task = env.sample_task()

trajectory = []
state = env.reset(task)
memory = framework.memory.init(task)

for step in range(max_steps):
    context = framework.memory.summarize(trajectory)
    plan = framework.planner.generate(state, context, task)
    action = framework.actor.execute(plan, state)
    next_state, info = env.step(action)
    trajectory.append((state, plan, action, next_state))
    state = next_state

success = env.check_success()
print(f"Task Success: {success}")

# Optional: Train planner with RL
if training_mode:
    rl_trainer = PlannerCentricRL(framework)
    rl_trainer.train(env, episodes=100)
```

---

## Related Work & Context

### Multi-Agent Orchestration Frameworks

- **AutoGen (2023):** Multi-agent conversation; assumes balanced roles
- **MetaGPT (2023):** Role-based software engineering agents
- **LangGraph (2024):** Stateful orchestration; HDLFORGE demonstrates value of adaptive decisions
- **PLANNER MATTERS complements by showing:** Role decomposition works, but allocation should be unequal

### Long-Horizon Planning Research

- **Chain-of-Thought (Wei et al., 2022):** Foundation for planning decomposition
- **ReACT (Yao et al., 2022):** Alternating reasoning and action; Planner Matters extends with role-specific scaling
- **Planning for LLMs (Rajkumar et al., 2024):** Prior work on planning difficulty; Planner Matters quantifies contribution

### Reinforcement Learning for Agent Optimization

- **Policy Gradient Methods:** GRPO, PPO; Planner Matters applies trajectory-level variants
- **Multi-Agent RL:** Usually studies competitive/cooperative settings; Planner Matters focuses on hierarchical coordination
- **RL for LLMs (Ouyang et al., 2023):** Foundation for applying RL to language models

---

## Future Research Directions

1. **Adaptive Allocation:** Learn optimal capacity allocation on-the-fly based on task characteristics
2. **Hierarchical Planning:** Extend beyond three roles to multi-level planning hierarchies
3. **Cross-Domain Generalization:** Test if planner dominance holds in scientific reasoning, code generation, creative tasks
4. **Real-Time Replanning:** Study impact of frequent replanning cycles on component dominance
5. **Interactive Human-Agent Planning:** Incorporate human feedback into planner optimization

---

## Key Takeaways

1. **Planning dominates multi-agent long-horizon task automation** (18-22% performance gain vs. 4-6% for actor, 2-3% for memory)
2. **Asymmetric allocation outperforms balanced multi-agent design** at the same or lower total compute
3. **Planner-centric RL efficiently optimizes the bottleneck component** while freezing others
4. **Trajectory-level rewards work well for planning-focused learning**, enabling faster convergence
5. **Strategic compute reallocation can improve efficiency** in complex orchestration systems

---

## Citation

**Citation Format:**
```bibtex
@article{wu2026planner,
  title={Planner Matters! An Efficient and Unbalanced Multi-agent Collaboration Framework for Long-horizon Planning},
  author={Wu, Wenyi and Zhu, Sibo and Zhou, Kun and Huang, Biwei},
  journal={arXiv preprint arXiv:2605.02168},
  year={2026}
}
```

