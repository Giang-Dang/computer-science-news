# Agentic Tool Use in Large Language Models: A Comprehensive Paradigm Framework

**Authors:** Researchers from Harbin Institute of Technology Shenzhen and TikTok Inc.  
**ArXiv ID:** 2604.00835  
**Submitted:** April 1, 2026  
**Status:** Under review

## Executive Summary

Tool use is fundamental to autonomous agents, yet the field remains fragmented across tasks, tools types, and training paradigms with no unified framework for understanding tool-use methods. This comprehensive survey organizes agentic tool use into three paradigms—prompting (frozen models), supervised learning, and reward-driven reinforcement learning—analyzing their evolution, methods, strengths, and failure modes. By unifying perspectives across code generation, math reasoning, information retrieval, and embodied tasks, the work provides practical guidance for practitioners and identifies critical research gaps in the path toward truly autonomous agent systems for software development and beyond.

## Problem Statement

### Development Automation Challenge
Autonomous agents for software engineering require reliable tool use to interact with:
- **External APIs** (GitHub, Docker, Cloud services)
- **Computational Tools** (compilers, linters, test runners)
- **Information Systems** (code search, documentation, databases)
- **Execution Environments** (terminals, IDEs, REPLs)

Yet real-world effectiveness remains inconsistent, with agents struggling to:
- Decide *whether* to use tools
- Select *which* tools from many options
- Format *correct inputs* to tools
- *Interpret and recover from* tool failures

### Prior Fragmentation
The literature is scattered:
- **Prompting literature**: Focus on in-context learning and chain-of-thought
- **Fine-tuning literature**: Task-specific supervised learning, often undocumented
- **RL literature**: Treating agent training as pure policy optimization
- **Tool-specific papers**: Focused on narrow domains (code, math, search)

Result: **No unified understanding** of how different tool-use methods relate, when each applies, and what failure modes to expect.

### Research Gap
A systematic taxonomy is needed that:
- Organizes existing methods into coherent paradigms
- Clarifies trade-offs between paradigms
- Identifies which paradigm suits which development tasks
- Guides practitioners toward evidence-based choices

## Core Concepts & Theory

### What is Agentic Tool Use?
Tool use in LLMs involves:
1. **Tool Awareness**: Agent knows available tools and their capabilities
2. **Tool Selection**: Decides which tool(s) to use for current step
3. **Input Formatting**: Translates reasoning into correct tool input
4. **Output Interpretation**: Parses and understands tool response
5. **Integration**: Incorporates tool result into reasoning
6. **Error Recovery**: Handles failed tool calls gracefully

### Three Fundamental Paradigms

The survey organizes tool-use approaches into three paradigms based on how the LLM's weights are updated:

```
┌──────────────────────────────────────────────────────────────┐
│              AGENTIC TOOL USE PARADIGMS                      │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Paradigm I: PROMPTING AS PLUG-AND-PLAY                      │
├─────────────────────────────────────────────────────────────┤
│ • LLM weights remain frozen                                  │
│ • Tool use elicited through prompts, demonstrations, feedback│
│ • Low deployment cost, high iteration speed                 │
│ • Examples: In-context learning, chain-of-thought, agents   │
│ • Failure Mode: Context bloat as tools/demos grow           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Paradigm II: SUPERVISED TOOL LEARNING                        │
├─────────────────────────────────────────────────────────────┤
│ • LLM fine-tuned on labeled or synthetic tool-use data      │
│ • Tool behavior internalized in weights                     │
│ • Faster inference, reduced reliance on prompt tuning       │
│ • Examples: Agent-FLAN, ToolAlpaca, FireAct, ToolFormer    │
│ • Failure Mode: Overfitting to distribution; new tools      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Paradigm III: REWARD-DRIVEN TOOL POLICY LEARNING            │
├─────────────────────────────────────────────────────────────┤
│ • Long-horizon RL with tool-use trajectories as training   │
│ • Learns tool policies optimizing task-specific rewards    │
│ • Highest ceiling but requires reward signal design        │
│ • Examples: RLHF for agents, inverse RL, actor-critic RL  │
│ • Failure Mode: Reward hacking, sample inefficiency        │
└─────────────────────────────────────────────────────────────┘
```

### Paradigm I: Prompting as Plug-and-Play

**Core Mechanism**: Frozen LLM reasonsvia instructions, examples, and environment feedback

**Key Methods**:
- **In-Context Learning**: Few-shot examples showing tool usage patterns
- **Chain-of-Thought (CoT)**: Step-by-step reasoning with tool invocations
- **React Pattern**: Reasoning → Action → Observation cycles
- **Instruction Fine-Tuning**: Training on natural language instructions (weights frozen for tool use)

**Strengths**:
- Fastest iteration: Modify prompts, see results immediately
- No retraining required when tools change
- Transparent: Easy to debug and audit reasoning
- Scalable: Works with any LLM via API

**Weaknesses**:
- **Context Bloat**: As tools/examples grow, prompt length explodes (8k → 128k tokens)
- **Brittle Decision-Making**: Tool selection based on shallow pattern matching
- **Poor Error Recovery**: Limited reasoning about tool failures
- **Cost**: Each inference includes full prompt + long context processing

**Application to Development Tasks**:
- Best for: Exploratory coding agents, prototype development
- Challenging for: Complex multi-step workflows, error recovery scenarios

### Paradigm II: Supervised Tool Learning

**Core Mechanism**: LLM fine-tuned on tool-use trajectories to internalize tool knowledge

**Key Methods**:
- **Agent-FLAN**: Synthetic data generation + supervised fine-tuning on tool-use patterns
- **ToolAlpaca**: Instruction tuning with tool-invocation outputs
- **FireAct**: Automatic prompt optimization + fine-tuning
- **ToolFormer**: Continuous corpus with labeled tool-use opportunities
- **Task-Specific Fine-Tuning**: Domain-specific tools (GitHub, Docker, etc.)

**Training Data Sources**:
```
Manual Annotations (high quality, small scale)
           ↓
Synthetic Data Generation (large scale, variable quality)
           ↓
Human Feedback / Reinforcement Learning from Feedback (expensive)
           ↓
In-Domain Trajectories (real agent executions, biased)
```

**Strengths**:
- **Faster Inference**: Tool knowledge internalized; reduced prompt overhead
- **Robust Selection**: Learned patterns for when/what to use tools
- **Generalization**: Transfers to new tasks in similar domain
- **Error Recovery**: Fine-tuning data can include failure recovery patterns

**Weaknesses**:
- **Retraining Required**: Adding new tools requires dataset augmentation + retraining
- **Distribution Shift**: Performance degrades on out-of-domain tools
- **Data Requirements**: Requires 100s-1000s of annotated examples
- **Limited Adaptability**: Cannot quickly adopt ad-hoc tools

**Application to Development Tasks**:
- Best for: Standardized development workflows (CI/CD, testing, linting)
- Challenging for: Novel tools, one-off integrations, rapidly evolving APIs

### Paradigm III: Reward-Driven Tool Policy Learning

**Core Mechanism**: Reinforcement learning with task-specific rewards guides tool-use policy

**Key Methods**:
- **RLHF for Agents**: Learn tool policies from human preferences over trajectories
- **Inverse Reinforcement Learning**: Infer reward from expert tool-use demonstrations
- **Actor-Critic RL**: Value function guides tool selection under uncertainty
- **Multi-Agent RL**: Multiple agents with cooperative/competitive tool-use dynamics
- **Curriculum RL**: Progressive task difficulty with adaptive tool introduction

**Reward Design Considerations**:
```
                     ┌─────────────────────────────┐
                     │    Reward Composition       │
                     └─────────────────────────────┘
                            ↙        ↓        ↘
                   Task Reward  |  Tool Reward  |  Efficiency Reward
                   ─────────────────────────────────────────────────
                   • Accuracy    |  • Tool Score | • Token Count
                   • Correctness |  • Relevance  | • Latency
                   • Coverage    |  • Success    | • Cost
```

**Strengths**:
- **Long-Horizon Reasoning**: Optimizes across entire task, not just next step
- **Adaptability**: Can learn new tools via reward signal alone
- **Sample Efficiency**: Modern RL can reach expert performance in 100s-1000s of trajectories
- **Compositionality**: Learned policies can compose for complex workflows

**Weaknesses**:
- **Reward Engineering**: Designing good rewards is domain-specific and difficult
- **Sample Complexity**: Still requires substantial interaction with environments
- **Instability**: RL training can be unstable; mode collapse on suboptimal policies
- **Interpretability**: Learned policies less transparent than prompting

**Application to Development Tasks**:
- Best for: Complex multi-step workflows (debugging, refactoring, optimization)
- Challenging for: Sparse reward environments, safety-critical operations

## Main Ideas & Contributions

### 1. Unified Taxonomy of Tool-Use Approaches
The paper provides the first systematic organization of tool-use literature:

| Aspect | Paradigm I (Prompting) | Paradigm II (Supervised) | Paradigm III (RL) |
|--------|----------------------|----------------------|-----------------|
| **LLM Frozen?** | Yes | No | No |
| **Feedback Type** | Environment | Labeled Data | Reward Signal |
| **Update Frequency** | Per-inference | Per-training batch | Per-trajectory |
| **Iteration Speed** | Fastest | Medium | Slowest |
| **Inference Cost** | Highest | Medium | Medium |
| **Adaptability** | None | Retraining only | Dynamic |
| **Scalability** | Limited by context | Proportional to model | RL infrastructure |

### 2. Evolution Timeline of Tool Use in LLMs

**2023 Era (Prompting Dominance)**:
- In-context learning and chain-of-thought
- Simple few-shot demonstrations
- Limited to 4-8 tools

**2024 Era (Supervised Learning Expansion)**:
- Synthetic data generation at scale
- Fine-tuning on tool-use trajectories
- 10-100 tools per model

**2025-2026 Era (RL and Hybrid Approaches)**:
- Learning tool policies via RL
- Multi-agent tool orchestration
- 100-1000s of tools accessible
- Agentic workflow optimization

### 3. Failure Modes and Mitigation Strategies

**Paradigm I Failures**:
- *Problem*: Context saturation (prompts > 100k tokens)
- *Solution*: Adaptive context windowing, skill abstractions
- *Problem*: Tool selection errors under ambiguity
- *Solution*: Ranking systems, tool description optimization

**Paradigm II Failures**:
- *Problem*: Distribution shift with new tools
- *Solution*: Continual learning, meta-learning approaches
- *Problem*: Data annotation bottleneck
- *Solution*: Synthetic data with large base models

**Paradigm III Failures**:
- *Problem*: Reward hacking / specification gaming
- *Solution*: Multi-objective rewards, conservative policy learning
- *Problem*: Sample inefficiency in complex environments
- *Solution*: Behavior cloning pretraining, exploration bonuses

### 4. Comparative Analysis Framework
For practitioners choosing between paradigms:

**Choose Prompting (Paradigm I) if**:
- Fast iteration and experimentation needed
- Limited computational budget for fine-tuning
- Tool set is small and stable
- Interpretability and auditability are critical
- Organization lacks RL infrastructure

**Choose Supervised Learning (Paradigm II) if**:
- Tool set is well-defined and stable
- Sufficient annotated data (100s-1000s examples)
- Inference efficiency is critical
- Organization has fine-tuning infrastructure
- Domain is well-understood

**Choose RL (Paradigm III) if**:
- Complex multi-step workflows requiring long-horizon reasoning
- Tool set is large or rapidly evolving
- Adaptive behavior to new tools/tasks needed
- Computational budget allows for interaction/training
- Organization has RL expertise and infrastructure

## Methodology & Implementation

### Literature Analysis Scope
- **Papers Reviewed**: 200+ peer-reviewed and preprint papers
- **Timeframe**: 2022-2026 focus (foundational work 2020-2022)
- **Domains Covered**:
  - Code generation and software engineering (50 papers)
  - Mathematical reasoning (35 papers)
  - Information retrieval and QA (40 papers)
  - Embodied agents and robotics (35 papers)
  - Multi-modal agents (40 papers)

### Categorization Methodology
Papers classified by:
1. **Paradigm**: Prompting, supervised, or RL-based
2. **Tool Domain**: Code, math, search, embodied, etc.
3. **LLM Architecture**: Decoder-only, encoder-decoder, multimodal
4. **Evaluation Benchmark**: Task-specific benchmarks (HumanEval, MATH, WebBench)
5. **Success Metrics**: Pass@k, BLEU, reward trajectory, etc.

### Key Findings Summary

**Prompting Dominance (2023-2024)**:
- 65% of published papers in 2023 used prompting-only approaches
- Shifted to 45% by 2026 as supervised/RL approaches matured
- Prompting most common for exploration and research

**Supervised Learning Growth**:
- Adoption grew from 5% (2023) to 30% (2026)
- Particularly strong in code generation (40% of 2026 papers)
- Benefits: 15-30% performance gains with fine-tuning

**RL Emergence**:
- Only 3% of papers in 2023, 25% in 2026
- Faster growth but higher barrier to entry
- 50%+ performance gains in complex reasoning tasks

**Performance Trends** (average across domains):
```
                Pass Rate (%) Over Time
100 ├─────────────────────────────────────
   │     ╱╱╱ RL-based (emerging)
 90 ├───╱╱╱╱╱╱╱───────────────────────
   │   ╱   ╱  Supervised Learning
 80 ├─ ╱   ╱ ╱─────────────────────────
   │╱ ╱   ╱ ╱  Prompting
 70 ├───╱ ╱ ╱──────────────────────────
   │   ╱ ╱ ╱
 60 ├───╱ ╱───────────────────────────
   2023  2024   2025   2026
```

### [Exact figures unavailable — see full paper for detailed metrics on HumanEval, MATH, WebBench]

## Practical Applications & Use Cases

### 1. Code Generation with Tool Access
**Scenario**: Autonomous code writing for software projects

**Tool Suite**:
- Compiler/interpreter (Python, TypeScript)
- Linter (ESLint, Pylint)
- Test runner (pytest, Jest)
- Version control (Git)
- Documentation retrieval

**Paradigm Application**:
- **Prompting**: Good for quick prototyping, exploratory coding
- **Supervised**: Best if codebase has consistent patterns to learn
- **RL**: Optimal for multi-file refactoring, optimization across project

### 2. Mathematical Problem Solving
**Scenario**: High school/competition math problems

**Tool Suite**:
- Computer algebra systems (SymPy, Mathematica)
- Numerical solvers
- Visualization tools
- Symbolic reasoning engines

**Paradigm Application**:
- **Prompting**: Effective with chain-of-thought for single problems
- **Supervised**: Fine-tuning on contest math problems
- **RL**: Learning which tools help most for problem categories

### 3. Information-Seeking QA
**Scenario**: Answering questions via retrieval + reasoning

**Tool Suite**:
- Dense retrievers (BM25, embedding-based)
- Re-ranking systems
- Citation mechanisms
- Fact-checking tools

**Paradigm Application**:
- **Prompting**: Works well with retrieval augmentation (RAG)
- **Supervised**: Learning relevance scoring for document selection
- **RL**: Optimizing retrieval strategies per query type

### 4. Testing and Debugging Automation
**Scenario**: LLM agent debugs failing tests

**Tool Suite**:
- Test runner with error traces
- Debugger/REPL access
- Stack trace analyzer
- Historical bug database

**Paradigm Application**:
- **Prompting**: Effective for simple failures (obvious fixes)
- **Supervised**: Learning common failure patterns
- **RL**: Exploring solution space for complex bugs

## Integration Challenges

### Context Window Limitations
- **Prompting**: Prompt + tool descriptions can exceed context limits
- *Solution*: Hierarchical tool organization, abstract summaries

### Tool Availability Variability
- **Supervised**: Models don't gracefully handle new tools
- *Solution*: Continual learning, prefix tuning for new tools

### RL Infrastructure Requirements
- **RL**: Requires simulation environment, reward signal design
- *Solution*: Start with prompting/supervised; graduate to RL as domain matures

### Safety and Correctness
- All paradigms: Model may invoke tools incorrectly or unsafely
- *Solution*: Tool input validation, sandboxing, human review

## Insights & Implications

### 1. No One-Size-Fits-All Solution
Different development tasks benefit from different paradigms:
- **Exploratory tasks** → Prompting (iterate fast)
- **Well-structured tasks** → Supervised Learning (fast inference, stable)
- **Complex reasoning** → RL (long-horizon optimization)

### 2. Trajectory of Tool Use Evolution
The field is moving toward **hybrid approaches**:
- Base with supervised learning (fast, reliable)
- Enhanced with RL for complex tasks (optimization)
- Fallback to prompting for novel tools (flexibility)

### 3. Importance of Workflow Coordination
Tool use is increasingly **orchestrated** rather than direct:
- Agents reason about tool sequences
- Workflows emerge from composition patterns
- Success depends on coordination, not individual tools

### 4. Future Research Directions
- **Automatic Reward Design**: Learning rewards from task specifications
- **Tool Learning**: Agents that learn new tools on the fly
- **Multi-Agent Tool Orchestration**: Coordination across specialized agents
- **Interpretable Tool Selection**: Understanding when/why agents choose tools
- **Safety-Critical Tool Use**: Formal guarantees for tool-using agents

## Code & Resources

### Academic Resources
- **arXiv Paper**: https://arxiv.org/abs/2604.00835
- **Full Survey**: 35+ pages with detailed taxonomy tables
- **Benchmark Collection**: References to 50+ evaluation benchmarks

### Toolkits and Frameworks
- **OpenAI Function Calling API**: https://platform.openai.com/docs/assistants/overview
- **Anthropic Tool Use**: https://docs.anthropic.com/claude/reference/getting-started-with-the-api
- **LangChain Tools**: https://python.langchain.com/docs/modules/agents/
- **AgentScope**: Open-source multi-agent framework

### Implementation Patterns

**Paradigm I (Prompting) Pattern**:
```python
from anthropic import Anthropic

client = Anthropic()

tools = [
    {"name": "python_repl", "description": "Execute Python code"},
    {"name": "bash_shell", "description": "Run bash commands"}
]

messages = [
    {"role": "user", "content": "Debug this failing test"}
]

response = client.messages.create(
    model="claude-3-5-sonnet",
    max_tokens=2048,
    tools=tools,
    messages=messages
)
```

**Paradigm III (RL) Pattern**:
```python
from rl_agents import PolicyGradientAgent, EnvironmentWrapper

env = EnvironmentWrapper("software_dev_task")
agent = PolicyGradientAgent(model="gpt-4", tools=env.available_tools)

# Training loop
for episode in range(1000):
    trajectory = agent.rollout(env)
    reward = env.compute_reward(trajectory)
    agent.update_policy(trajectory, reward)
```

## Related Work & Context

### Foundational Papers
- **ToolFormer** (Schick et al., 2023): Learning when to use tools via in-context learning
- **ToolAlpaca** (Qin et al., 2023): Instruction-tuning for tool use
- **ART** (Parisi et al., 2022): Automatic reasoning and tool use

### Contemporary Surveys
- Agent architectures and frameworks surveys (Hao et al., 2023)
- LLM-based reasoning surveys (Zhou et al., 2023)
- Function calling paradigms (Anthropic, 2024)

### Future Directions for Research
1. **Automatic Tool Selection**: Learning which tools are relevant without human guidance
2. **Tool Composition**: Combining tools for complex workflows automatically
3. **Adaptive Tool Learning**: Updating tool knowledge from feedback
4. **Safety and Verification**: Formal methods for correct tool use
5. **Scalable Tool Management**: Handling 1000s-10000s of tools efficiently

---

**Citation:**
```bibtex
@article{2026AgenticToolUse,
  title={Agentic Tool Use in Large Language Models},
  author={[Multiple authors]},
  journal={arXiv preprint arXiv:2604.00835},
  year={2026}
}
```
