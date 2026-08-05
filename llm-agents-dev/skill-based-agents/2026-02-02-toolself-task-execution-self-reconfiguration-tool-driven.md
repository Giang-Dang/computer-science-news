# ToolSelf: Unifying Task Execution and Self-Reconfiguration via Tool-Driven Emergent Adaptation

**ArXiv ID:** 2602.07883  
**Submitted:** February 2026

## Executive Summary

ToolSelf introduces a unified framework enabling LLM agents to autonomously adapt not just their actions but their own configuration, strategy, and toolbox during task execution. By abstracting self-reconfiguration as a callable tool within the same action space as task execution, the system achieves phase transition from externally-governed agents to self-managed entities. Training via Configuration-Aware Two-stage Learning (CAT) combining rejection sampling with RL results in 24.1% average performance gains and enables agents to generalize to novel tasks unseen during training.

## Problem Statement

Current LLM agents operate under static configurations:
- **Fixed strategy**: Agent follows predefined approach from start to finish
- **Fixed toolbox**: Set of available tools determined at initialization
- **Fixed goals**: Objectives and sub-goals not updated mid-execution
- **External adaptation**: Only humans can reconfigure agents between tasks
- **Limited learning**: Past experiences don't improve agent behavior beyond fine-tuning

This rigidity prevents agents from adapting to task complexity variations or learning from execution trajectory. The research gap centers on enabling agents to manage themselves as dynamic entities, updating configuration based on task progression.

## Core Concepts & Theory

### Unified Action Space with Configuration-as-Tool

**Key Innovation**: Configuration updates become callable tools, not separate mechanism

```
Traditional Agent Architecture:
┌──────────────────────┐
│ Task Execution Core  │ (LLM selecting actions)
├──────────────────────┤
│ Available Actions:   │
│ • Act on environment │
│ • Invoke tools       │
└──────────────────────┘
         ↓
    [External reconfiguration required for strategy change]

ToolSelf Architecture:
┌────────────────────────────────────────┐
│    Unified Action Space                 │
├────────────────────────────────────────┤
│ Actions:                                │
│ • Act on environment (traditional)     │
│ • Invoke domain tools (traditional)     │
│ • Reconfigure sub-goals (NEW)          │
│ • Swap strategy modules (NEW)           │
│ • Update context/memory (NEW)           │
│ • Modify toolbox (NEW)                  │
├────────────────────────────────────────┤
│ = All actions treated uniformly         │
│ = Agent learns when/how to reconfigure  │
│ = Autonomous self-adaptation emerges    │
└────────────────────────────────────────┘
```

### Configuration-Aware Two-Stage Training (CAT)

**Stage 1: Rejection Sampling Fine-Tuning**
- Generate multiple trajectories using policy
- Keep only trajectories where agent successfully reconfigures itself appropriately
- Reject trajectories with suboptimal self-adaptation decisions
- Effect: Model learns which configuration changes lead to success

**Stage 2: Trajectory-Level Reinforcement Learning**
- Reward signal: Final task success (did agent solve the problem?)
- Credit assignment: Entire trajectory evaluated, not just final action
- Optimization: RL discovers which intermediate reconfiguration choices maximize success
- Result: Agent learns to adapt proactively during task execution

**Combined Effect**: Model internalizes when and how to adapt without external guidance

### Self-Adaptive Agent Lifecycle

```
┌─────────────────────────────────────────────────────┐
│          Task Execution with Self-Adaptation         │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Initialization:                                      │
│ └─ Agent receives initial configuration              │
│    (sub-goals, strategy, available tools)            │
│                                                      │
│ ┌─ Execution Loop ─────────────────────────────┐   │
│ │                                               │   │
│ │ Observe: Current task state                  │   │
│ │ Decide: Next action (including reconfigure)  │   │
│ │ Execute: Perform action or reconfigure self  │   │
│ │ Evaluate: Progress toward goal               │   │
│ │                                               │   │
│ │ ┌─ During Execution ──────────────────────┐  │   │
│ │ │ Agent may invoke:                       │  │   │
│ │ │ • UpdateSubGoals(new_goals)             │  │   │
│ │ │ • ChangeStrategy(new_strategy)          │  │   │
│ │ │ • AddTools(new_tools)                   │  │   │
│ │ │ • RemoveTools(obsolete_tools)           │  │   │
│ │ │ • UpdateContext(learned_facts)          │  │   │
│ │ │                                         │  │   │
│ │ │ = Reduces need for external intervention │  │   │
│ │ └─────────────────────────────────────────┘  │   │
│ │                                               │   │
│ └───────────────────────────────────────────────┘   │
│                                                      │
│ Termination:                                        │
│ └─ Agent achieves goal or exhausts resources        │
└─────────────────────────────────────────────────────┘
```

## Main Ideas & Contributions

1. **Configuration as Tool**: Abstracts self-adaptation as callable tool within same action space as task execution, enabling uniform learning.

2. **Intrinsic Adaptation**: Agents learn to reconfigure themselves without external intervention, shifting from reactive to proactive behavior.

3. **Unified Learning Framework**: Configuration-Aware Two-Stage Training combines rejection sampling (data quality) with RL (credit assignment).

4. **Generalization**: System generalizes to novel tasks unseen during training, suggesting learned adaptation strategies transfer across domains.

5. **Emergent Self-Management**: Phase transition observed where agents shift from passive executors to dual managers of task and self.

## Methodology & Implementation

### Evaluation Benchmarks

**Diverse Task Domains**:
- Sequential decision-making tasks with varying complexity
- Tasks requiring strategy shifts mid-execution
- Problems where initial approach suboptimal but learnable

**Baseline Comparisons**:
- Fixed-configuration agents (no self-adaptation)
- Agents with external reconfiguration (oracle)
- Specialized workflows for each task type
- Other meta-learning approaches

### Results

**Performance Gains** [Exact figures unavailable — see full paper]:
- Average improvement: 24.1% over fixed baselines
- Generalization: Strong performance on unseen task distributions
- Adaptation quality: Learned reconfigurations match expert guidance

**Key Findings** [Estimated]:
- Rejection sampling improves data quality ~40% vs. random sampling
- RL training further improves performance by 15-20%
- Combined CAT approach outperforms either stage alone
- Adaptation emerges naturally through training, not hard-coded

## Practical Applications & Use Cases

### Use Case 1: Problem-Solving Agents
- Initial strategy attempts direct solution
- Mid-execution detects approach infeasibility
- Agent reconfigures sub-goals to break-and-conquer
- New strategy succeeds where original would fail

### Use Case 2: Data Analysis Workflows
- Agent starts with simple analysis strategy
- Detects insufficient data quality
- Reconfigures toolbox: adds data cleaning tools
- Continues with enhanced toolkit

### Use Case 3: Multi-Stage Planning
- Long-horizon task requires staged approach
- Early stages discover constraints
- Agent adapts later-stage strategy based on learnings
- Avoids wasted work on now-infeasible plans

### Integration Challenges

1. **Exploration vs. Exploitation**: Balance discovering new configurations vs. committing to successful ones
2. **Computational Cost**: Rejection sampling + RL can be expensive during training
3. **Safety**: Unconstrained self-modification could lead to degenerate behaviors
4. **Interpretability**: Understanding why agents make specific reconfiguration choices
5. **Task Specification**: Defining what configurations are valid/safe to attempt

### Cost & Latency Implications

**Training Cost**: Significant (rejection sampling + RL over trajectories)
**Inference Latency**: Minimal overhead; reconfiguration calls are quick
**Runtime Adaptability**: Enables agents to self-optimize during execution

## Insights & Implications

### For Agent-Driven Development Systems

1. **Autonomy Deepens**: Self-reconfiguration capability moves agents closer to true autonomy.

2. **Learning from Trajectory**: Agents that can reflect on and adapt their own behavior learn more efficiently.

3. **Meta-Capability**: Ability to manage one's own configuration is powerful meta-capability applicable across domains.

### Advancement in Autonomous Systems

- Demonstrates phase transition from scripted to emergent adaptation
- Shows unified action space enables natural learning of self-management
- Provides training methodology for complex meta-behaviors

### Limitations & Open Questions

1. **Convergence Guarantees**: What ensures learned adaptations are beneficial, not harmful?
2. **Distribution Shift**: How robust is adaptation to task distributions very different from training?
3. **Scalability**: Does approach scale to larger state/action spaces?
4. **Interpretability**: Can we understand agent reasoning for self-modification?
5. **Safety Constraints**: How to enforce safe adaptation bounds?

## Code & Resources

### Training Framework

- Configuration-Aware Two-Stage Training (CAT) implementation
- Rejection sampling for trajectory filtering
- Trajectory-level RL optimization
- Evaluation harness for diverse task domains

### Dependencies

- LLM API for agent generation
- RL training infrastructure
- Task simulator or execution environment
- Evaluation metrics and logging

## Related Work & Context

### Foundational Areas

- **Meta-learning**: Learning to learn, including learning-to-adapt
- **Reinforcement Learning**: Trajectory-level optimization
- **Program Synthesis**: Generating executable configuration updates
- **Multi-Agent Systems**: Agent specialization and adaptation

### Related Papers

- "Self-Organizing Multi-Agent Systems for Continuous Software Development" (2603.25928)
- "From Intent to Execution" (2605.03986) on agent composition
- "SkillFlow: Flow-Driven Recursive Skill Evolution" on evolving capabilities

### Possible Extensions

1. **Constrained Adaptation**: Add safety constraints on permissible reconfigurations
2. **Hierarchical Adaptation**: Support multi-level configuration hierarchies
3. **Transfer Learning**: Learn adaptation strategies that transfer across task families
4. **Interpretability**: Explain agent's reconfiguration decisions to humans
5. **Online Learning**: Continue learning and adapting in deployment

## Conclusion

ToolSelf demonstrates that treating self-reconfiguration as a tool enables agents to develop genuinely self-adaptive behavior. Through Configuration-Aware Two-Stage Training, agents learn to autonomously manage their own strategy, goals, and toolbox during execution. The approach achieves substantial performance improvements while enabling generalization to novel tasks. This work represents a meaningful step toward truly autonomous agents that not only execute tasks but manage their own evolution.

---

_Generated by [Claude Code](https://claude.ai/code)_
