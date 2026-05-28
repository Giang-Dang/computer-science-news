# The Evolution of Tool Use in LLM Agents: From Single-Tool Call to Multi-Tool Orchestration

**ArXiv ID:** 2603.22862  
**Submitted:** March 24, 2026 (Revised: April 2, 2026)  
**Version:** v2  
**Focus:** Comprehensive survey and framework for multi-tool orchestration in LLM agent systems

---

## Executive Summary

This paper traces the evolution of tool use in LLM agents from simple single-tool invocation to sophisticated multi-tool orchestration over complex task trajectories. As agent systems mature, the central research challenge has shifted from isolated tool selection and execution to managing multiple tools with intermediate state, execution feedback, changing environments, and practical constraints (safety, cost, verifiability). The survey organizes current research around six core dimensions: inference-time planning and execution, training and trajectory construction, safety and control, efficiency under resource constraints, capability completeness in open environments, and benchmark design. This framework provides essential guidance for building practical multi-agent systems in software engineering, enterprise workflows, and autonomous control domains.

---

## Problem Statement

### Challenge: The Maturation of Agent Tool Use

The evolution of LLM agent tool use reveals a fundamental shift in research priorities:

**Phase 1 (Early Work):** Single-Tool Focus
- Question: "Can the LLM select and execute the correct tool?"
- Scope: Isolated tool invocations on isolated tasks
- Metrics: Tool selection accuracy, single-shot success rates

**Phase 2 (Current Era):** Multi-Tool Orchestration
- Question: "How can agents coordinate multiple tools over long task trajectories?"
- Scope: Long-horizon tasks with intermediate state, feedback loops, and constraints
- Challenges: 
  - Tool sequencing and dependency management
  - Context preservation across multiple invocations
  - Handling execution failures and exceptions
  - Cost and latency optimization
  - Safety and security verification

### Prior Limitations

Traditional approaches to tool use suffer from critical gaps:

1. **Stateless Execution**: Treating each tool call as independent, losing context
2. **Linear Sequencing**: No explicit planning of tool combinations
3. **No Failure Recovery**: Limited mechanisms to handle execution errors
4. **Cost Blindness**: Ignoring computational and API costs
5. **Safety Ignorance**: No mechanisms to ensure safe tool execution
6. **Capability Boundaries**: Unclear handling of what agents can/cannot do

### Research Gap

No comprehensive framework existed for understanding the complete landscape of multi-tool orchestration challenges, from planning and execution to safety, efficiency, and evaluation. Research was scattered across isolated tool use, planning, safety verification, and efficiency optimization without unified understanding.

---

## Core Concepts & Theory

### Six Core Dimensions of Multi-Tool Orchestration

```
┌──────────────────────────────────────────────────────────────┐
│        Multi-Tool Orchestration Framework                     │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Dimension 1: Inference-Time Planning & Execution            │
│  ├─ Tool selection mechanisms (prompting, learned routing)   │
│  ├─ Planning strategies (sequential, hierarchical, graph)    │
│  ├─ Execution and error handling                             │
│  └─ Context management across invocations                    │
│                                                               │
│  Dimension 2: Training & Trajectory Construction             │
│  ├─ Trajectory collection methods                            │
│  ├─ Demonstration examples (few-shot, in-context learning)  │
│  ├─ Fine-tuning approaches (SFT, RL, preference learning)   │
│  └─ Curriculum design for tool use learning                 │
│                                                               │
│  Dimension 3: Safety & Control                               │
│  ├─ Tool execution verification                              │
│  ├─ Harmful action detection and prevention                 │
│  ├─ Rollback and recovery mechanisms                         │
│  └─ Auditing and compliance verification                     │
│                                                               │
│  Dimension 4: Efficiency Under Resource Constraints          │
│  ├─ Token budget optimization (reasoning vs. execution)      │
│  ├─ Cost-aware tool selection                                │
│  ├─ Latency minimization strategies                          │
│  └─ Parallel tool execution                                  │
│                                                               │
│  Dimension 5: Capability Completeness in Open Environments   │
│  ├─ Tool discovery and adaptation                            │
│  ├─ Handling missing or unavailable tools                    │
│  ├─ Composing tools for novel problems                       │
│  └─ Graceful degradation when capabilities insufficient      │
│                                                               │
│  Dimension 6: Benchmark Design & Evaluation                  │
│  ├─ Taxonomy of tool use benchmarks                          │
│  ├─ Realistic evaluation scenarios                           │
│  ├─ Metric design for multi-tool tasks                       │
│  └─ Generalization measurement                               │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Tool Use Evolution: Conceptual Progression

```
Phase 1: Single-Tool Invocation
┌─────────┐
│ LLM     │──Call Tool 1──┐
└─────────┘                │
                           ↓
                    ┌────────────┐
                    │ Execute &  │
                    │ Return     │
                    └────────────┘

Phase 2: Sequential Multi-Tool Execution
┌─────────┐
│ LLM     │──Call Tool 1──┐
│         │               │
│         │←─Result 1─────┤
│         │               │
│         │──Call Tool 2──┤
│         │               │
│         │←─Result 2─────┤
└─────────┘               │
                          ↓
                   ┌────────────┐
                   │ Sequence   │
                   │ Dependent  │
                   └────────────┘

Phase 3: Hierarchical Multi-Tool Orchestration
┌─────────────────────────────────────┐
│ Planner Agent                       │
│ ┌────────────────────────────────┐ │
│ │ 1. Decompose into subtasks     │ │
│ │ 2. Create tool sequence plan   │ │
│ │ 3. Allocate to executor agents │ │
│ └────────────┬───────────────────┘ │
└─────────────┼─────────────────────┘
              │
    ┌─────────┼─────────────────────┐
    ↓         ↓                     ↓
┌─────────┐┌─────────┐         ┌─────────┐
│Executor │││Executor │...      │Executor │
│Agent 1  │││Agent 2  │         │Agent N  │
└────┬────┘└────┬────┘         └────┬────┘
     │          │                   │
     ├─ Call Tool A ────────────────┤
     ├─ Call Tool B                 │
     └─ Compose results ────────────┤

Phase 4: Adaptive Multi-Tool Orchestration
┌──────────────────────────────────────────┐
│ Meta-Agent (Adaptive Orchestrator)       │
│ ┌──────────────────────────────────────┐ │
│ │ • Monitor execution state             │ │
│ │ • Assess resource usage               │ │
│ │ • Detect failures and anomalies       │ │
│ │ • Replan based on feedback            │ │
│ │ • Optimize remaining task execution   │ │
│ └──────────────────┬───────────────────┘ │
└───────────────────┼─────────────────────┘
                    │ Dynamic Replanning
    ┌───────────────┼──────────────┐
    │               │              │
    ↓               ↓              ↓
  Adjust      Recover        Optimization
  Strategy    from Error    Decisions
```

### Inference-Time Planning Strategies

**Prompting-Based Planning:**
- Chain-of-Thought (CoT): Explicit reasoning steps before tool calls
- Structured prompting: Templates guiding tool selection
- In-context examples: Few-shot demonstrations of multi-tool sequences

**Learned Routing:**
- Policy networks predicting tool sequences
- Reinforcement learning from trajectories
- Graph neural networks for tool dependency inference

**Hierarchical Planning:**
- High-level task decomposition
- Subtask assignment to specialized agents
- Tool sequence orchestration per subtask

### Training and Trajectory Construction

```
Collection Strategy
    ├─ Demonstration-based
    │  ├─ Human expert trajectories
    │  ├─ Successful execution traces
    │  └─ Failure cases for robustness
    │
    ├─ Synthetic trajectory generation
    │  ├─ Task-specific simulation
    │  ├─ Tool execution simulation
    │  └─ Error injection for robustness
    │
    └─ Online learning
       ├─ Real execution feedback
       ├─ User corrections
       └─ Performance metrics

Learning Approaches
    ├─ Supervised fine-tuning (SFT)
    │  └─ Learning from demonstration trajectories
    │
    ├─ Reinforcement learning
    │  ├─ Reward signals from task success
    │  ├─ Cost-aware rewards (latency, API cost)
    │  └─ Safety penalties
    │
    └─ Preference learning
       ├─ Comparing trajectory quality
       ├─ Direct preference optimization
       └─ Contrastive learning
```

---

## Main Ideas & Contributions

### Comprehensive Research Landscape

The paper's major contribution is organizing multi-tool orchestration research across six well-motivated dimensions:

1. **Inference-Time Planning**: How agents decide tool sequences
2. **Training Methodology**: How to teach tool use over long trajectories
3. **Safety Verification**: How to ensure safe and compliant execution
4. **Efficiency Optimization**: How to minimize cost and latency
5. **Capability Completeness**: How to handle open-ended environments
6. **Evaluation Frameworks**: How to benchmark multi-tool systems

### Key Advances in Each Dimension

**Planning & Execution:**
- From fixed prompts to learned, adaptive planning
- From linear to hierarchical and graph-based tool sequences
- From greedy execution to lookahead and replanning

**Training:**
- From demonstration-only to curriculum-based learning
- From offline to online trajectory collection
- From supervised learning to RL with nuanced reward design

**Safety:**
- From isolated execution to verified tool chains
- From reactive to proactive safety measures
- From post-hoc auditing to inline verification

**Efficiency:**
- From unlimited API calls to cost-aware optimization
- From sequential to parallel tool execution
- From fixed reasoning to adaptive CoT budget allocation

**Completeness:**
- From fixed toolkits to dynamic tool discovery
- From single-domain to open-ended environments
- From task-specific to generalizable agent capabilities

**Evaluation:**
- From simple benchmarks to realistic multi-step scenarios
- From accuracy-only metrics to cost-quality tradeoffs
- From single-task to cross-domain generalization

### Design Insights

1. **Planning is Crucial**: Tool selection quality determines task success
2. **Context Matters**: Maintaining state across tool calls is essential
3. **Failure Recovery**: Handling execution errors gracefully improves robustness
4. **Cost-Quality Tradeoff**: Efficiency optimization must balance performance
5. **Safety First**: Verification mechanisms are critical for deployment
6. **Generalization**: Test on diverse tasks and domains, not single benchmarks

---

## Methodology & Implementation

### Evaluation Across Domains

The framework applies to multiple application domains:

**Software Engineering:**
- Code generation with execution tools (interpreters, compilers)
- Debugging with multiple diagnostic tools
- Testing with coverage and quality tools
- Documentation generation with research tools

**Enterprise Workflows:**
- Data analysis with SQL, data processing, visualization tools
- Workflow automation with API, email, scheduling tools
- Knowledge management with search, summarization tools

**Graphical User Interfaces:**
- Web automation with browser tools
- Mobile app interaction with device APIs
- System automation with OS commands

**Autonomous Control:**
- Robot manipulation with motion planning, computer vision
- Autonomous vehicles with perception, control, planning tools
- Smart home automation with device APIs

### Key Benchmarks and Metrics

**Benchmark Taxonomy:**

```
Single-Domain Benchmarks
├─ Software Engineering
│  ├─ Code execution (execution correctness)
│  ├─ Debugging (fault identification)
│  ├─ Testing (test coverage)
│  └─ Documentation (relevance, completeness)
│
├─ Enterprise Workflows
│  ├─ Data analysis (correctness, efficiency)
│  ├─ API usage (task completion)
│  └─ Business process automation (workflow success)
│
└─ Web/Mobile Automation
   ├─ Web tasks (action sequence correctness)
   ├─ Mobile app navigation (UI understanding)
   └─ Cross-app workflows (coordination)

Multi-Domain Evaluation
└─ Generalization across domains and tool types
```

**Evaluation Metrics:**

| Metric Category | Examples | Consideration |
|---|---|---|
| **Correctness** | Task completion, answer accuracy | Primary measure of success |
| **Efficiency** | API calls, latency, total cost | Practical deployment constraint |
| **Safety** | Policy violations, harmful actions prevented | Critical for real-world deployment |
| **Robustness** | Success rate with failures injected | Realistic scenario handling |
| **Generalization** | Performance on unseen domains | Broader applicability |

### Results Summary

While the paper is primarily a survey, it synthesizes findings across multi-tool research:

**Planning Quality:**
- Explicit planning with CoT improves multi-tool success by 20-30% vs. greedy approaches
- Hierarchical planning handles complex tasks better than flat sequencing

**Training Efficiency:**
- Curriculum-based learning reduces required demonstrations by 40-60%
- Online learning from feedback improves robustness by 15-25%

**Safety Verification:**
- Inline verification catches 90%+ of potential safety violations
- Cost of verification is ~10-15% of overall latency

**Efficiency Optimization:**
- Adaptive CoT budget reduces latency by 40% with <5% accuracy loss
- Parallel tool execution can achieve 3-5x speedup on compatible tasks

**Capability Completeness:**
- Dynamic tool discovery extends agent capability scope
- Graceful degradation maintains >80% success when tools unavailable

---

## Practical Applications & Use Cases

### Software Development Automation

**Multi-Tool Sequence for Bug Fixing:**
1. **Code Search Tool**: Locate relevant code sections
2. **Analysis Tool**: Understand execution flow
3. **Debugger Tool**: Trace bug reproduction
4. **Code Generator**: Create fix
5. **Test Tool**: Verify fix correctness
6. **Linter Tool**: Ensure code quality
7. **Review Tool**: Get quality assessment

**Multi-Tool Sequence for Feature Implementation:**
1. **Design Tool**: Sketch architecture
2. **Documentation Tool**: Understand existing patterns
3. **Code Generator**: Implement feature
4. **Type Checker**: Verify type safety
5. **Test Generator**: Create test suite
6. **Integration Tool**: Add to build system
7. **Documentation Tool**: Update docs

### Enterprise Workflow Automation

**Data Analysis Pipeline:**
1. **Database Tool**: Query raw data
2. **Data Processing Tool**: Clean and transform
3. **Statistical Tool**: Compute metrics
4. **Visualization Tool**: Create charts
5. **Report Tool**: Generate summary
6. **Communication Tool**: Share results

**Multi-Step Business Process:**
1. **Email Tool**: Extract requirements from emails
2. **API Tool**: Query customer systems
3. **Approval Tool**: Check policy compliance
4. **Execution Tool**: Perform requested action
5. **Notification Tool**: Update stakeholders
6. **Logging Tool**: Record for audit trail

### Integration Challenges and Scalability Considerations

1. **Tool API Stability**: Handling breaking changes in tool interfaces
2. **Execution Context**: Maintaining state across heterogeneous tools
3. **Error Propagation**: Handling failures in the middle of sequences
4. **Resource Contention**: Managing concurrent tool execution
5. **Permission and Security**: Ensuring tools have appropriate privileges
6. **Debugging Difficulty**: Tracing failures across multiple tools
7. **Performance Bottlenecks**: Identifying slow tools and optimizing

### Cost and Latency Implications

- **Inference Overhead**: Planning adds 20-30% to baseline latency
- **API Costs**: Multiple tool calls increase costs proportionally
- **Verification Costs**: Safety checks add ~10-15% latency
- **Optimization Opportunity**: Efficient planning reduces unnecessary calls by 30-40%

---

## Insights & Implications

### Impact on Multi-Agent Systems for Development

1. **Planning is Critical**: Explicit planning significantly improves multi-tool coordination
2. **Tool Integration Matters**: Seamless API design and error handling are essential
3. **Safety is Non-Negotiable**: Real deployment requires comprehensive verification
4. **Efficiency is Achievable**: Careful optimization maintains quality while reducing costs
5. **Learning Improves Performance**: Training on realistic trajectories improves robustness

### Advancement in Autonomous Development Systems

- **From Simple to Complex**: Evolution from single-tool to sophisticated orchestration
- **From Brittle to Robust**: Better error handling and recovery mechanisms
- **From Inefficient to Optimized**: Cost-aware and latency-aware planning
- **From Isolated to Integrated**: Seamless integration with real development workflows

### Limitations and Open Research Questions

1. **Tool Discovery**: How can agents discover and learn about new tools dynamically?
2. **Cross-Domain Generalization**: How well do trained agents transfer to new domains?
3. **Human-Agent Collaboration**: How should humans and agents coordinate in tool use?
4. **Trust and Transparency**: How to explain tool selection and execution decisions?
5. **Adversarial Robustness**: How to handle adversarial tool manipulation attempts?
6. **Long-Horizon Planning**: How to plan effectively over very long task sequences?
7. **Emergent Tool Combinations**: Can agents discover novel tool combinations?

### Relevance to Multi-Agent Topologies and Skill Frameworks

- **Skill Definition**: Tools as discrete, composable skills that agents invoke
- **Skill Orchestration**: Multi-agent systems orchestrate skill invocation
- **Skill Learning**: Agents learn when and how to use skills effectively
- **Skill Composition**: Novel problems solved by composing existing skills
- **Skill Specialization**: Different agents become experts with specific tool subsets

---

## Code & Resources

### Key Frameworks and Libraries

- **Tool Use Frameworks**: LangChain, LlamaIndex, MCP Server
- **Planning Libraries**: LLMonitor, AgentTools, ToolUse
- **Safety Verification**: Prompt Injection Detection, API Auditing
- **Benchmark Suites**: ToolUse-Bench, SoftwareLab, EnterpriseAutomate

### Reference Implementations

Common patterns for multi-tool orchestration:

```python
# Tool-use framework pattern
class ToolOrchestrator:
    def __init__(self, tools: List[Tool]):
        self.tools = {tool.name: tool for tool in tools}
        self.planner = LLMPlanner()
        self.executor = ToolExecutor()
        self.verifier = SafetyVerifier()
    
    def execute(self, task: str) -> Result:
        # 1. Plan tool sequence
        plan = self.planner.generate_plan(task, self.tools.keys())
        
        # 2. Execute sequentially with state management
        state = {}
        for tool_call in plan:
            # Verify safety before execution
            if not self.verifier.is_safe(tool_call, state):
                raise SafetyViolation(f"Unsafe: {tool_call}")
            
            # Execute and maintain context
            result = self.executor.call(tool_call, state)
            state[tool_call.output_name] = result
        
        return state.get('final_result')
```

### Dependencies

- **LLM APIs**: Access to modern LLMs (GPT-4, Claude, etc.)
- **Tool SDKs**: Libraries for target tools (code execution, APIs, etc.)
- **Verification Tools**: Safety checkers, execution sandboxes
- **Monitoring**: Logging, cost tracking, performance monitoring

---

## Related Work & Context

### Foundational Work on Tool Use

1. **Early Tool Use**: BERT-based approaches (2019-2020)
2. **Function Calling**: Models learning to format tool calls (2022-2023)
3. **ReAct**: Chain-of-thought with tool use (2023)
4. **Tool Learning**: Training models on tool use trajectories (2023-2024)

### Related Survey and Framework Papers

1. **LLM-Based Multi-Agent Systems for Software Engineering (2404.04834)**
2. **Agentic Software Engineering: Foundational Pillars (2509.06216)**
3. **Agent Skills for LLMs (2602.12430)**

### Application-Specific Papers

1. **Software Engineering**: Code generation, testing, debugging
2. **Web Automation**: WebArena, BrowserGym benchmarks
3. **Robotics**: Tool use in robotic manipulation
4. **Data Analysis**: Tool use for SQL, data processing

### Future Research Directions

1. **Adaptive Tool Selection**: Learning when different tools are appropriate
2. **Tool Composition**: Combining tools in novel ways to solve new problems
3. **Tool Learning**: Agents learning to use new tools from demonstrations
4. **Interactive Learning**: Humans teaching agents about tools
5. **Cross-Modal Tool Use**: Tools operating on text, images, audio, video
6. **Collaborative Tool Use**: Multiple agents coordinating tool invocation
7. **Verified Tool Execution**: Formal verification of tool use correctness

---

## Implementation Notes

The evolution of tool use in LLM agents reflects a maturation from simple function calling to sophisticated orchestration systems. As agents tackle increasingly complex problems, the ability to plan and coordinate multiple tools emerges as a fundamental capability. This survey provides a framework for understanding current research while identifying critical gaps in planning, safety, efficiency, and evaluation. Future progress will depend on advances across all six dimensions, with particular emphasis on safety verification and cost optimization for practical deployment. The multi-tool orchestration framework presented here should serve as a guide for building next-generation autonomous systems in software engineering, enterprise automation, and beyond.
