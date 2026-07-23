# AgentStepper: Interactive Debugging of Software Development Agents

**Authors:** Robert Hutter, Michael Pradel  
**ArXiv ID:** 2602.06593  
**Submitted:** February 6, 2026  
**Venue:** IEEE/ACM International Conference on Software Engineering (ICSE 2026)

## Executive Summary

AgentStepper is the first interactive debugger specifically designed for LLM-based software development agents. It enables developers to inspect, control, and interactively manipulate agent trajectories through a structured conversation interface with breakpoints, stepwise execution, and live editing capabilities. The work addresses a critical gap in understanding and debugging complex agent systems that generate hundreds of thousands of tokens across dozens of iterations.

## Problem Statement

Software development agents powered by LLMs demonstrate significant promise for automating tasks like environment setup, issue solving, and program repair. However, understanding and debugging such agents remains fundamentally challenging:

- **Complexity of Agent Execution:** Typical agent trajectories involve dozens of LLM-tool interaction iterations, generating hundreds of thousands of tokens that are difficult to comprehend in real-time
- **Black-box Nature:** Current techniques provide minimal insight into the intermediate reasoning process, making it hard to identify where agents fail
- **Debugging Difficulty:** Developers must trace complex interactions among LLM queries, tool invocations, code modifications, and environmental state changes—a cognitively expensive task
- **Prior Agent System Limitations:** Existing debugging tools are generic program debuggers, not designed for the unique challenges of agent-based development

## Core Concepts & Theory

### Agent Execution Model
AgentStepper models agent execution as a structured conversation loop consisting of:
1. **LLM Prompting:** Agent queries the language model with context
2. **Response Interpretation:** Agent parses LLM output to extract intended tool calls
3. **Tool Invocation:** Agent executes suggested tools and captures outputs
4. **State Management:** Agent feeds tool results back to LLM, updating execution state

### Trajectory Representation
Trajectories are represented as structured conversations among three participants:
- **LLM:** Generates reasoning and tool-calling decisions
- **Agent Program:** Orchestrates the agent's behavior and state
- **Tools:** External systems (shell, IDE, version control) providing feedback

### Debugging Mechanics

**Breakpoints & Stepwise Execution:** Developers can set breakpoints at key interaction points and step through agent execution line-by-line, examining state at each iteration.

**Live Editing:** The system supports interactive modification of:
- Agent prompts (refine instructions in real-time)
- Tool invocations (override or inject alternative tool calls)
- Trajectory resumption (continue from edited state)

**Intermediate State Capture:** Repository-level code changes are captured and displayed at each step, allowing inspection of how the agent's actions affect the codebase.

### Comparison with Traditional Debuggers

```
Traditional Program Debugger    vs    Agent Debugger
├─ Source code & variables             ├─ LLM prompts & responses
├─ Function call stack                 ├─ Agent decision trace
├─ Memory state                        ├─ Tool execution history
└─ Line-by-line execution              └─ Trajectory-level control
```

## Main Ideas & Contributions

### 1. Agent-Native Debugging Interface
AgentStepper introduces the first debugging paradigm specifically designed for agent systems:
- **Conversation-based representation** of agent execution (not traditional source-code representation)
- **Agent-aware breakpoints** that pause at meaningful decision points
- **Tool-level inspection** allowing examination of what agents invoke and why

### 2. Interactive Trajectory Manipulation
Unlike passive logging, AgentStepper allows developers to:
- Pause mid-trajectory and modify prompts to steer agent behavior
- Override failed tool calls and resume execution
- Replay segments with different agent configurations
- Directly edit agent instructions without restarting

### 3. Code-Level Visibility
The system captures and displays intermediate code changes:
- Visual diff of repository state at each agent step
- Ability to inspect what code the agent modified
- Context for understanding why subsequent actions succeeded or failed

## Methodology & Implementation

### Experimental Setup

**Evaluated Agents:**
- ExecutionAgent: A development agent for code execution tasks
- SWE-Agent: State-of-the-art software engineering agent for issue resolution
- RepairAgent: Specialized agent for automated program repair

**Integration Requirements:**
- Minimal code changes needed: 39–42 edited lines per agent
- Agent-agnostic design (works with different LLM backends and tool sets)

### User Study

**Participants:** 12 software developers  
**Tasks:** Identify bugs in agent programs using AgentStepper vs. alternative approaches

**Evaluation Metrics:**
- Ability to interpret agent trajectories
- Success rate in identifying bugs in agent implementations
- Time to locate and diagnose issues
- User satisfaction with interactive debugging capabilities

**Results:** [Exact figures unavailable — see full paper]
- AgentStepper significantly improved trajectory interpretation accuracy
- Participants could identify more bugs more quickly than without the tool
- Live editing and breakpoint features rated as most valuable capabilities

### System Architecture

AgentStepper consists of three main components:

**Frontend UI:**
- Conversation visualization (structured display of LLM-tool interactions)
- Breakpoint management interface
- Trajectory timeline with step navigation
- Code diff viewer for repository changes

**Backend Service:**
- Trajectory recording and replay engine
- Breakpoint evaluation logic
- Prompt/tool override handling
- State reconstruction and resumption

**Agent Integration API:**
- Minimal instrumentation required
- Hooks for trajectory recording
- Callback interfaces for breakpoint and override handling

## Practical Applications & Use Cases

### 1. **Bug Diagnosis in Agent Programs**
Developers can debug agent logic without rerunning expensive LLM interactions:
- "Why did the agent choose this tool?"
- "Where did the agent misinterpret the error message?"
- "How did the code modification lead to this failure?"

### 2. **Prompt Engineering & Optimization**
Live editing enables interactive refinement:
- Test prompt changes mid-trajectory without restarting
- Observe how instruction changes affect agent decisions
- Iteratively improve agent prompts based on real execution

### 3. **Failure Analysis & Iteration**
Developers can analyze failure modes:
- Identify systematic decision errors by the agent
- Inject corrected tool calls to test workarounds
- Understand why agents fail on specific patterns

### 4. **Integration with Development Workflows**
- Used alongside traditional code debuggers
- Integration into CI/CD pipelines for agent testing
- Support for team-based debugging (shared trajectory analysis)

### 5. **Software Engineering Tasks**
- Issue resolution (debugging why agents fail to fix issues)
- Program repair (analyzing why repair attempts fail)
- Code generation (understanding why agents produce suboptimal code)

## Insights & Implications

### For Agent Development
1. **Transparency Enabler:** Interactive debugging transforms agents from black-box systems into transparent, inspectable tools
2. **Iteration Accelerator:** Live editing reduces the cost of experimentation and prompt refinement
3. **Quality Assurance:** Systematic bug identification in agent programs improves reliability

### For Software Engineering
1. **New Debugging Paradigm:** Agents require fundamentally different debugging approaches than traditional programs
2. **Trajectory-Level Reasoning:** Understanding agent behavior requires reasoning about sequences of decisions, not individual code lines
3. **Human-Agent Collaboration:** Interactive debugging bridges human developers and autonomous agents

### Limitations and Open Questions
- Scalability to very long trajectories (hundreds or thousands of steps)
- Support for complex distributed multi-agent systems
- Automated suggestion of where to set breakpoints
- Integration with different LLM architectures and prompt formats

## Code & Resources

**Official Repository:** [GitHub link unavailable — see arXiv paper]  
**Dependencies:**
- Python 3.8+
- LLM API access (e.g., Claude, GPT-4)
- Version control system (git)
- Tool integrations (shell, IDE)

**Integration Points:**
- Works with ExecutionAgent, SWE-Agent, RepairAgent
- Extensible to other LLM-based agents with minimal changes
- Compatible with various LLM providers

## Related Work & Context

### Foundation: Agent Systems
- **SWE-Agent** (Jimenez et al.): Software engineering agent with environment interaction
- **ExecutionAgent**: Code execution and debugging agent
- **RepairAgent**: Automated program repair using LLMs

### Related Debugging Work
- Traditional program debuggers (GDB, LLDB)
- Trace-based debugging systems
- Prompt debugging and testing frameworks

### Future Research Directions
1. **Automated Breakpoint Placement:** ML-based suggestions for where to set breakpoints
2. **Multi-Agent Debugging:** Extending to systems with multiple coordinating agents
3. **Causal Analysis:** Identifying root causes of agent failures through intervention analysis
4. **Scaling Approaches:** Techniques for debugging very long trajectories efficiently
5. **Integration with Agent Frameworks:** Native support in AgentForge, MetaGPT, and other orchestration systems

## Keywords
Agent debugging, LLM-based software development, interactive debugging, agent transparency, trajectory analysis, program repair, automated software engineering

---

**Paper Link:** https://arxiv.org/abs/2602.06593  
**PDF:** https://arxiv.org/pdf/2602.06593
