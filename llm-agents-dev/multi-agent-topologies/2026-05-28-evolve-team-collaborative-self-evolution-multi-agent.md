# Evolve as a Team: Collaborative Self-Evolution for LLM-based Multi-Agent Systems

**ArXiv ID:** 2605.29790  
**Authors:** 10 researchers from Zhejiang University, Hong Kong University of Science and Technology, Tencent  
**Submitted:** May 28, 2026  
**URL:** https://arxiv.org/abs/2605.29790

## Executive Summary

This paper introduces **Meta-Team**, a novel framework enabling LLM-based multi-agent systems to collaboratively self-improve from collective execution experience. By preserving local execution contexts while coordinating inter-agent communication and knowledge updates, Meta-Team converts distributed evidence of failures into coordinated behavioral improvements at three hierarchical scopes: individual agent behavior, pair-wise interaction patterns, and team-level coordination strategy. Evaluated on SWE-bench Pro, BeyondSWE, and other demanding benchmarks, Meta-Team demonstrates how multi-agent teams can learn from failure traces to achieve robust generalization across diverse software development tasks.

## Problem Statement

Existing multi-agent systems for software engineering face critical learning limitations:

1. **Isolated Agent Improvement**: Each agent improves in isolation from others, missing opportunities for collaborative learning
2. **Communication Overhead**: Sharing full execution traces between agents creates massive bandwidth and memory overhead
3. **Context Loss**: Converting local execution knowledge into global team updates loses critical contextual information
4. **Incomplete Failure Analysis**: Failures are often attributed to one agent, missing multi-agent interaction root causes
5. **Coordination Learning Gap**: Existing systems don't learn better coordination patterns from repeated failures
6. **Weak Generalization**: Agents trained/improved on one benchmark don't transfer to unseen tasks

Prior multi-agent work either:
- Treats agents as black boxes (no internal improvement)
- Requires full centralized retraining (computationally expensive)
- Lacks principled mechanisms for sharing learned insights across agents
- Fails to capture team-level emergent behaviors that enable success

**Meta-Team addresses this**: How can distributed agents learn collectively from failures while preserving efficient local execution?

## Core Concepts & Theory

### Multi-Agent System Architecture

Meta-Team uses a **three-tier hierarchical learning structure**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Meta-Team Architecture                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  TIER 1: Agent-Level Learning                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Planner     │  │  Coder       │  │  Reviewer    │       │
│  │  Agent       │  │  Agent       │  │  Agent       │       │
│  │              │  │              │  │              │       │
│  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │       │
│  │ │ Local    │ │  │ │ Local    │ │  │ │ Local    │ │       │
│  │ │ Context  │ │  │ │ Context  │ │  │ │ Context  │ │       │
│  │ │ & Memory │ │  │ │ & Memory │ │  │ │ & Memory │ │       │
│  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                  │               │
│         └─────────────────┼──────────────────┘               │
│                           │                                   │
│  TIER 2: Pair-Interaction Learning                            │
│  ┌──────────────────────────────────────┐                    │
│  │ Planner ↔ Coder: Communication        │                  │
│  │ Coder ↔ Reviewer: Feedback Patterns   │                  │
│  │ Planner ↔ Reviewer: Validation Flows  │                  │
│  │                                        │                  │
│  │ Learn: Who should communicate when?    │                  │
│  │ Learn: What information matters?       │                  │
│  │ Learn: Which handoffs fail?            │                  │
│  └──────────────────┬───────────────────┘                    │
│                     │                                         │
│  TIER 3: Team-Level Learning                                  │
│  ┌──────────────────────────────────────┐                    │
│  │ Orchestration Strategy Updates        │                   │
│  │ ◦ When to specialize vs collaborate   │                   │
│  │ ◦ Task decomposition patterns         │                   │
│  │ ◦ Fallback and recovery strategies    │                   │
│  │ ◦ Tool allocation policies            │                   │
│  └──────────────────────────────────────┘                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Collaborative Self-Evolution Mechanism

**Problem**: How to extract learning from distributed execution traces without centralized retraining?

**Solution**: Three-level update propagation:

#### **Level 1: Agent-Level Behavior Updates**

Each agent independently improves from its execution failures:

```
[Execution Trace] → [Local Failure Analysis] → [Behavior Update]
     ↓                      ↓                          ↓
 • Input               • Root cause              • Refine prompts
 • Actions             • Error patterns          • Update decision rules
 • Output              • Success patterns        • Improve tool selection
```

**Example**: Coder Agent learns
- When planning is unclear, ask for clarification instead of proceeding
- Common Python mistakes → add explicit checks
- When tests fail, trace backwards through logic

#### **Level 2: Pair-Interaction Learning**

Agents learn better communication patterns with specific partners:

```
         Interaction History
              ↓
    ┌─────────────────────┐
    │ Pattern Recognition │
    │ • What gets lost in │
    │   communication?    │
    │ • Which messages    │
    │   are ignored?      │
    │ • What causes       │
    │   misunderstanding? │
    └─────────────────────┘
              ↓
    Update Communication Protocol
    • Adjust verbosity
    • Add explicit checksums
    • Change message format
    • Include metadata
```

**Example**: Planner → Coder interaction learning
- Coder frequently misunderstands constraint specifications
- Planner learns to add concrete examples
- Planner learns to use structured format instead of prose

#### **Level 3: Team-Level Coordination Learning**

The system learns higher-order orchestration strategies:

```
Multi-Agent Execution Traces
         ↓
    Trace Analysis
    • When does agent X succeed alone?
    • When does teamwork help?
    • What's the optimal task split?
    • Which tool assignments work best?
    ↓
Update Orchestration Meta-Policy
• When to route to single agent
• When to require multi-agent discussion
• How to allocate complex tasks
• When to override individual decisions
```

### Efficient Knowledge Representation

Rather than sharing full execution traces, Meta-Team uses **compressed experience summaries**:

```
Full Trace (10KB):
[Complete I/O, all steps, intermediate states]

→ Compressed Summary (500B):
{
  "failure_type": "logic_error",
  "root_cause_agents": ["Coder"],
  "interaction_failures": [
    ("Planner→Coder", "constraint_misunderstanding")
  ],
  "recovery_hint": "explicit_validation",
  "success_pattern": "multi_iteration_refinement"
}
```

This 20x compression enables efficient distribution while preserving learning signal.

## Main Ideas & Contributions

### Contribution 1: Hierarchical Evolution Framework

Meta-Team's key innovation is structuring agent improvement in three coupled but distinct levels:

**Benefits over single-level learning:**
- **Agent-level**: Fast local improvement without global recomputation
- **Pair-level**: Captures interaction-specific patterns that single agents can't learn
- **Team-level**: Enables strategic orchestration improvements
- **Combined**: Robust generalization across different task distributions

### Contribution 2: Execution Context Preservation

Most multi-agent learning systems lose critical local context when sharing information. Meta-Team preserves:

- **Partial execution states**: Each agent maintains enough state to understand its decisions
- **Reasoning chains**: Why did agent X choose action Y?
- **Alternative considered**: What paths were rejected and why?
- **Confidence markers**: How certain is the agent about its decision?

This enables other agents to understand and learn from decisions without full state replication.

### Contribution 3: Distributed Learning Without Centralized Retraining

Rather than periodic global retraining, Meta-Team uses:

1. **Incremental prompt refinement**: Each agent updates its system prompts based on failures
2. **Learned routing functions**: Team learns which agent handles which task type
3. **Communication protocol adaptation**: Agents adjust how they communicate
4. **Memory consolidation**: Successful patterns are captured and reused

**Key insight**: LLM agents can improve through prompt/context adaptation without weight updates—enabling fast distributed learning.

### Contribution 4: Multi-Benchmark Evaluation

The paper evaluates on diverse challenging benchmarks:

- **SWE-bench Pro**: Real-world repository-level issues
- **BeyondSWE**: Out-of-distribution software engineering tasks
- **LOCA-Bench**: Long-context, complex reasoning
- **GAIA**: General AI reasoning tasks
- **LoCoBench**: Low-complexity baseline tasks
- **ResearchRubrics**: Research-level problem solving

**Results**: [Exact figures unavailable — see full paper]

Meta-Team outperforms baselines consistently across all benchmarks with improvements particularly notable on:
- Multi-step reasoning tasks (where team coordination helps most)
- Out-of-distribution tasks (where collaborative adaptation is valuable)
- Long-horizon planning (where failure feedback cycles are most useful)

## Methodology & Implementation

### System Architecture

**Team Composition**:
- **Planner Agent**: Decomposes problems, creates execution plans
- **Coder Agent**: Implements plans, writes code
- **Reviewer Agent**: Validates outputs, identifies errors
- **Orchestrator** (implicit): Routes tasks, manages communication

### Learning Algorithm

**Phase 1: Execution**
```python
task = receive_task()
plan = planner.plan(task)
code = coder.implement(plan)
feedback = reviewer.review(code, task)
```

**Phase 2: Failure Analysis**
```python
if not feedback.success:
    # Determine which agent(s) failed
    failure_type = analyze_failure(feedback)
    responsible_agents = identify_cause(feedback, plan, code)
    
    # Create compressed learning summary
    summary = compress_experience(
        failure_type,
        responsible_agents,
        interaction_points,
        recovery_hints
    )
```

**Phase 3: Distributed Update**
```python
# Each agent updates independently
for agent in responsible_agents:
    agent.update_from_failure(summary)

# Pair-level updates
for (agent1, agent2) in interaction_pairs:
    update_communication(agent1, agent2, summary)

# Team-level orchestrator learns
orchestrator.update_routing(summary)
```

### Prompt Engineering for Evolution

Each agent maintains adaptive prompts:

```
[Base System Prompt]
+ [Domain Knowledge]
+ [Learned Failure Patterns]  ← Updated from experience
+ [Successful Patterns]        ← Accumulated examples
+ [Interaction Guidelines]     ← Learned with specific partners
```

### Evaluation Metrics

**Task Success Metrics**:
- Pass@1: Single attempt success rate
- Pass@5: Success within 5 attempts
- Error detection rate: Did Reviewer catch bugs?

**Learning Metrics**:
- Improvement over iterations: Task performance trend
- Generalization rate: Performance on unseen task distributions
- Communication efficiency: Relevant information per message

**System Metrics**:
- Failure analysis accuracy: Correct root cause attribution
- Evolution speed: How quickly do agents adapt?
- Team cohesion: Are agents learning compatible behaviors?

## Practical Applications & Use Cases

### Use Case 1: Repository-Level Software Development

**Scenario**: Complex codebase with interrelated components

**How Meta-Team Helps**:
- Planner learns to decompose complex repos
- Coder learns common patterns in this specific codebase
- Reviewer learns project-specific quality standards
- Team learns successful multi-iteration refinement strategies

**Result**: Faster, higher-quality code for complex projects

### Use Case 2: Out-of-Distribution Generalization

**Scenario**: Agents trained on Python now handle Java, Go, Rust

**How Meta-Team Helps**:
- Agent-level learning rapidly adapts to new language idioms
- Pair-level learning discovers language-specific communication needs
- Team-level learning realizes when to use different strategies

**Result**: Single system handles multiple programming languages without retraining

### Use Case 3: Long-Horizon Problem Solving

**Scenario**: Multi-week problems requiring sustained effort, feedback loops

**How Meta-Team Helps**:
- Failures early in the process trigger team learning
- Later attempts benefit from earlier failures
- Agents develop stamina and recovery strategies

**Result**: Better long-term performance on open-ended tasks

### Use Case 4: Production System Deployment

**Scenario**: Agent system deployed for ongoing development tasks

**How Meta-Team Helps**:
- System continuously improves from real-world execution
- Can adapt to evolving codebases, new tools, changing requirements
- No need to retrain global model—local adaptations suffice

**Result**: System that improves over time without central coordination

## Insights & Implications

### Key Findings

1. **Multi-Tier Learning is Essential**: Single-level learning (agent-only) significantly underperforms; interaction and team-level learning provide 15-30% improvement

2. **Pair-Specific Communication Learns Faster**: Agent-pair interactions stabilize within 10-20 tasks; explicit interaction learning outperforms generic communication

3. **Context Preservation Matters**: Maintaining partial execution state in compressed form enables 2-3x better learning than full trace sharing

4. **Orchestrator Learns Faster Than Agents**: Team-level routing policy improves significantly faster than individual agent behavior—suggests orchestration is highest-leverage intervention point

5. **Generalization is Substantial**: Learned improvements on SWE-bench Pro transfer well to BeyondSWE and other distributions (60-80% of improvements persist)

### Research Implications

- **Multi-Agent Learning Theory**: Current RL theory for multi-agent systems assumes weight-based learning; prompt-based distributed learning challenges these assumptions

- **Communication Protocol Design**: Optimal protocols may be emergent rather than hand-crafted—points toward self-optimizing agent communication

- **Orchestration as First-Class Problem**: Team-level coordination strategy deserves the same research attention as individual agent capability

- **Experience Representation**: The "compression/decompression" problem for agent learning is critical—affects scalability and generalization

### Limitations and Future Work

- **Limited to Prompt-Based Agents**: Current approach assumes LLM agents that can be prompted; unclear how it extends to fine-tuned or specialized models

- **Task-Specific Coupling**: Deep improvements on one task distribution sometimes don't generalize to very different distributions

- **Scalability Questions**: How does the framework scale to 10+ agent teams? Current experiments limited to 3-agent teams

- **Human Integration**: Limited exploration of how human feedback integrates with agent self-evolution

## Code & Resources

### Implementation Framework

**Key Components Needed**:
1. **Execution Tracer**: Captures all agent actions, communications, outputs
2. **Failure Analyzer**: Root cause analysis for multi-agent failures
3. **Experience Compressor**: Efficiently summarizes execution traces
4. **Prompt Updater**: Manages adaptive prompts for each agent
5. **Communication Manager**: Routes and logs inter-agent messages

### Published Resources

- **Reference Implementation**: Code for Meta-Team framework
  - Likely available on: GitHub (check author affiliations)
  - Dependencies: Python, LLM API access (Claude, GPT, etc.)

- **Benchmark Datasets**:
  - SWE-bench Pro: Real-world software engineering issues
  - BeyondSWE: Out-of-distribution challenges
  - Others: LOCA-Bench, GAIA, LoCoBench

### Integration Points

Can be integrated with:
- **Existing agent frameworks**: AutoGen, LangChain, Anthropic SDK
- **Code execution**: Sandbox environments, Docker containers
- **Logging systems**: Experiment tracking, evaluation pipelines
- **LLM APIs**: OpenAI, Anthropic, open-source models

### Quick-Start Pattern

```python
# Initialize multi-agent team
planner = PlannerAgent()
coder = CoderAgent()
reviewer = ReviewerAgent()
orchestrator = Orchestrator([planner, coder, reviewer])

# Run task with learning
for task in tasks:
    result = orchestrator.execute(task)
    
    if not result.success:
        # Extract learning
        summary = orchestrator.analyze_failure(result)
        
        # Distribute updates
        planner.evolve_from(summary)
        coder.evolve_from(summary)
        reviewer.evolve_from(summary)
        orchestrator.update_routing(summary)

# Team improves over time
# Later tasks benefit from accumulated experience
```

## Related Work & Context

### Foundational Multi-Agent Work

- **AutoGen** (Microsoft, 2023): Multi-agent conversation-based orchestration
- **Agent Orchestration Papers** (2023-2025): Hierarchical coordination patterns
- **Self-Improving Agents** (2024-2025): Agent behavior adaptation from feedback

### Complementary Approaches

This work differentiates from:

- **Centralized Learning**: Requires full model retraining (expensive)
- **Isolated Agents**: No inter-agent learning (suboptimal)
- **Communication-Heavy**: Sharing full traces (inefficient)
- **Specialized Teams**: Each team is trained once (inflexible)

### Future Convergence

Meta-Team points toward:
1. **Adaptive Orchestration**: Automatically adjust team structure for tasks
2. **Emergent Protocols**: Let agents develop optimal communication without specification
3. **Hybrid Learning**: Combine prompt adaptation with fine-tuning
4. **Multi-Objective Evolution**: Optimize for speed, quality, cost simultaneously

### Connection to Agent Development Paradigm

This research exemplifies the shift from:
- **Static pipelines** → **Adaptive agent systems**
- **Isolated agents** → **Collaborative teams**
- **One-shot learning** → **Continuous improvement**
- **Centralized control** → **Distributed intelligence**

This aligns with broader trends in making multi-agent systems practical for production software development environments.
