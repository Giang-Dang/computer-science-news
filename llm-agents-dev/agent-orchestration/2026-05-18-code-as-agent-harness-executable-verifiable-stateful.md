# Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems

**ArXiv ID:** 2605.18747  
**Authors:** Xuying Ning, Katherine Tieu, Dongqi Fu, Tianxin Wei, Zihao Li, Yuanchen Bei, Jiaru Zou, Mengting Ai, Zhining Liu, Ting-Wei Li, Lingjie Chen, Yanjun Zhao, Ke Yang, Bingxuan Li, Cheng Qian, and 27 co-authors  
**Submission Date:** May 18, 2026  
**Type:** Comprehensive survey and architectural framework  
**Status:** Published research guide

---

## Executive Summary

"Code as Agent Harness" presents a unified architectural framework that repositions code not as a mere output of LLM agents but as the operational substrate enabling agent reasoning, acting, verification, and multi-agent coordination. Rather than thinking of agents as systems that generate code, this work frames code as the infrastructure through which agents execute, reason about, and coordinate their behaviors. The paper examines three integrated layers: the harness interface (connecting agents to reasoning and action), harness mechanisms (planning, memory, tool use, feedback), and multi-agent scaling (coordination, workflow orchestration, verification). This conceptual reframing unlocks new possibilities for agent reliability, observability, and coordination while providing a systematic taxonomy for understanding existing agent systems and designing new ones.

---

## Problem Statement

The field of LLM agents has developed along several parallel tracks—code generation, autonomous reasoning, tool use, multi-agent coordination—without a unifying architectural framework. Current thinking frequently dichotomizes:

1. **Code as Output vs. Code as Infrastructure:** Agent systems treat code either as an output to be generated or as an implementation detail of the agent framework, losing sight of code's potential as the central operational substrate.

2. **Execution vs. Reasoning:** Agent designs separate where code is reasoned about from where code is executed, creating disconnects that reduce observability and testability.

3. **Single-Agent vs. Multi-Agent:** Agent coordination mechanisms are bolted on top of single-agent reasoning rather than being integrated from the ground up.

4. **Verification vs. Execution:** Code verification is treated as a post-hoc check rather than an integrated part of the execution pipeline.

5. **Semantic vs. Syntactic:** Agent systems struggle to maintain correspondence between high-level goals and low-level code representations, leading to failures when plans and implementations diverge.

**Research Gap:** No comprehensive framework exists that unifies how code serves as the central infrastructure for agent systems—where it connects reasoning to action, enables verification, and coordinates multiple agents.

---

## Core Concepts & Theory

### The Agent Harness Model

An "agent harness" is the infrastructure through which agents operate. Code-based harnesses provide:

1. **Explicit Representation:** Agent plans, memory, and actions are represented as code artifacts
2. **Executability:** Harness code can be executed to validate agent decisions
3. **Observability:** Execution traces provide detailed visibility into agent reasoning
4. **Verifiability:** Code-based representations enable formal and runtime verification
5. **Composability:** Code artifacts combine to form larger agent workflows

### Three-Layer Harness Architecture

```
┌────────────────────────────────────────────────────────┐
│         MULTI-AGENT COORDINATION LAYER                │
│  (Agent roles, collaboration patterns, orchestration) │
└────────────────────────────────────────────────────────┘
         ↑ shared code artifacts ↓
┌────────────────────────────────────────────────────────┐
│       HARNESS MECHANISMS LAYER                        │
│  (Planning, Memory, Tool Use, Feedback, Optimization) │
└────────────────────────────────────────────────────────┘
         ↑ code interface ↓
┌────────────────────────────────────────────────────────┐
│         HARNESS INTERFACE LAYER                        │
│  (Reasoning, Action, Environment Modeling)            │
└────────────────────────────────────────────────────────┘
```

### Layer 1: Harness Interface

The interface layer defines how code connects agents to their operational world:

#### Reasoning Interface
- **Goal Representation:** Objectives specified as code contracts
- **Reasoning Artifacts:** Generated plans, decompositions, and reasoning traces
- **Semantic Grounding:** Code-based representation of intent

#### Action Interface
- **Tool Binding:** APIs and tools exposed as function signatures
- **Action Execution:** Actions specified and executed through code
- **Environment Interaction:** Environment state represented as queryable code objects

#### Environment Modeling
- **State Representation:** Current world state as code structures
- **Observation Interface:** Environment queries through code functions
- **Model Updates:** Mechanisms to synchronize code models with actual environment

### Layer 2: Harness Mechanisms

The mechanisms layer implements core capabilities needed for long-horizon agent execution:

#### Planning (Reasoning → Code)

**Goal:** Convert high-level objectives into executable action sequences.

**Mechanisms:**
- **Hierarchical Decomposition:** Goals decomposed into subgoals, each with code representations
- **Constraint Specification:** Constraints on valid solutions encoded in code
- **Search and Optimization:** Different planning strategies (search-based, optimization-based) search through code-specified solution spaces
- **Workflow Orchestration:** Complex plans represented as workflow DAGs with code-specified dependencies

**Execution Model:**
```python
def plan(goal: Goal) -> ActionSequence:
    """Convert goal to executable action sequence"""
    # Decompose goal hierarchically
    subgoals = decompose(goal)
    
    # For each subgoal, generate code-based action plan
    actions = []
    for subgoal in subgoals:
        action_code = generate_action_plan(subgoal)
        actions.append(execute(action_code))
    
    return ActionSequence(actions)
```

#### Memory and Context Management

**Goal:** Preserve context, retrieve relevant evidence, store experience.

**Mechanisms:**
- **Working Memory:** Short-term context for current reasoning step
- **Semantic Memory:** Long-term knowledge stored as code artifacts
- **Episodic Memory:** Past experiences and execution traces
- **Retrieval-Augmented:** Dynamic retrieval of relevant memory based on current context
- **State Persistence:** Mechanisms to maintain consistent state across reasoning steps

**Code Representation:**
```python
class WorkingMemory:
    """Current reasoning context"""
    current_goal: Goal
    intermediate_results: Dict[str, Any]
    reasoning_trace: List[ReasoningStep]
    
class SemanticMemory:
    """Long-term knowledge"""
    skill_library: Dict[str, Skill]
    domain_knowledge: Dict[str, Knowledge]
    patterns: Dict[str, Pattern]

class EpisodicMemory:
    """Past experiences"""
    execution_traces: List[ExecutionTrace]
    failure_cases: List[FailureCase]
    success_patterns: List[SuccessPattern]
```

#### Tool Use and Capability Expression

**Goal:** Enable agents to invoke external tools and APIs effectively.

**Mechanisms:**
- **API Specification:** Tools specified through type signatures and contracts
- **Tool Selection:** Mechanisms to select appropriate tools for current subtask
- **Parameter Binding:** Mechanisms to ground tool parameters to specific values
- **Error Handling:** Recovery strategies when tool invocations fail
- **Tool Composition:** Chaining multiple tools to solve complex problems

**Tool Integration Pattern:**
```python
class Tool:
    """Generic tool interface"""
    name: str
    signature: Callable  # Type signature
    preconditions: Code  # When tool can be used
    effects: Code  # What tool accomplishes
    error_handlers: Dict[Exception, RecoveryStrategy]

def invoke_tool(tool: Tool, params: Dict) -> Result:
    # Verify preconditions
    if not eval(tool.preconditions, params):
        raise PreconditionViolation()
    
    # Execute tool
    result = tool.signature(**params)
    
    # Handle errors
    if isinstance(result, Exception):
        recovery = tool.error_handlers[type(result)]
        return recovery(result, params)
    
    return result
```

#### Feedback and Learning

**Goal:** Enable agents to learn from execution outcomes.

**Mechanisms:**
- **Outcome Evaluation:** Assessing whether actions achieved intended goals
- **Error Attribution:** Determining why failures occurred (planning, execution, environment)
- **Feedback Propagation:** Using feedback to refine planning and action selection
- **Experience Accumulation:** Storing lessons learned for future use

**Feedback Loop:**
```
Plan → Execute → Verify → Evaluate Outcome
  ↑                          ↓
  └─────── Feedback Loop ────┘
```

### Layer 3: Multi-Agent Harness Architecture

#### Agent Roles

Agents in coordinated systems take on specialized roles:

**Manager/Orchestrator**
- Decomposes high-level goals into subtasks
- Assigns subtasks to specialized agents
- Coordinates execution and synthesizes results

**Planner**
- Creates detailed plans for solving specific subtasks
- Reasons about feasibility and resource requirements
- Communicates plans to implementers

**Coder/Implementer**
- Generates code solutions for specific subtasks
- Tests and debugs implementations
- Reports results back to manager

**Reviewer/Verifier**
- Validates generated code against specifications
- Checks for security issues and best practices
- Approves or requests revisions

**Tester**
- Designs and executes test cases
- Validates that code meets requirements
- Reports coverage and edge cases

#### Collaboration Modes

**Programming Mode (Add New Functionality)**
```
Goal → Planner → Coder → Reviewer → Tester → Integration
```

**Repair Mode (Fix Bugs)**
```
Bug Report → Debugger → Coder → Reviewer → Regression Tester
```

**Debate Mode (Decide Between Approaches)**
```
Problem → [Agent A proposes] ↔ [Agent B proposes]
              ↓ (Evaluator judges)
           Consensus/Winning Approach
```

**Red-Teaming Mode (Security/Robustness)**
```
Implementation → Attacker (tries to break) → Defender (fixes) → Repeat
```

#### Workflow Topologies

**Hierarchical Topology**
```
        Manager
        /  |  \
      /    |    \
   Agent1 Agent2 Agent3
```
Central coordinator delegates to specialists, collects results.

**Peer Topology (Consensus-Based)**
```
  Agent1 ←→ Agent2
    ↑         ↑
    └────↔────┘
      Agent3
```
Agents negotiate and reach consensus through communication.

**Streaming/Pipeline Topology**
```
Agent1 → Agent2 → Agent3 → Agent4
(each stage processes output of previous)
```
Sequential processing where output of one agent feeds into next.

**Graph-Based Topology**
```
      Task1
     /     \
  Task2    Task3
     \     /
      Task4
```
Complex dependencies represented as DAG with dynamic scheduling.

### Plan-Execute-Verify Loop

The core operational pattern:

```
┌─────────────────────────────────────────────┐
│           PLAN PHASE                        │
│  (Agent generates code-based plan)          │
│  Plan serves as executable specification    │
└─────────────────────────────────────────────┘
         ↓ (plan is code)
┌─────────────────────────────────────────────┐
│         EXECUTE PHASE                       │
│  (Plan executed in sandbox)                 │
│  Changes recorded in audit trail            │
│  Rollback possible if needed                │
└─────────────────────────────────────────────┘
         ↓ (execution trace)
┌─────────────────────────────────────────────┐
│         VERIFY PHASE                        │
│  (Compare intended vs actual)               │
│  Deterministic sensors validate state       │
│  Human reviews safety-critical actions      │
└─────────────────────────────────────────────┘
```

**Key Innovation:** Plans are code artifacts that can be:
- Inspected before execution
- Executed deterministically
- Verified against specifications
- Debugged if needed

---

## Main Ideas & Contributions

### 1. Unified Conceptual Framework

**Contribution:** Repositions code from output to substrate, providing a single lens through which to view agent systems.

**Key Innovation:** Rather than separate categories (code generation, planning, tool use), this framework sees all as aspects of how code serves as the operational harness.

**Impact:** Enables researchers and practitioners to reason systematically about agent architecture decisions.

### 2. Three-Layer Harness Architecture

**Contribution:** Provides systematic taxonomy for agent system components.

**Key Innovation:** Distinguishes interface layer (how agents connect to world), mechanisms layer (how agents reason and act), and coordination layer (how agents work together).

**Impact:** Supports principled design of new agent systems and evaluation of existing ones.

### 3. Code-Based Representation of Plans

**Contribution:** Advocates representing plans as executable code rather than abstract specifications.

**Key Innovation:** Enables execution-based verification: plans can be tested before committing to irreversible actions.

**Impact:** Dramatically improves agent reliability by catching plan errors before execution.

### 4. Integrated Multi-Agent Orchestration

**Contribution:** Frames multi-agent systems not as independent agents coordinating but as integrated systems where code artifacts enable coordination.

**Key Innovation:** Shared code repositories, structured artifact exchange, and role-based responsibility enable sophisticated multi-agent workflows.

**Impact:** Enables complex multi-agent systems for software engineering, scientific discovery, and enterprise automation.

### 5. Harness-Bench: Evaluation Framework

**Contribution:** Proposes systematic evaluation methodology for agent harnesses.

**Key Innovation:** Measures not just task success but harness effects, regression rates, and ablation studies.

**Impact:** Enables principled comparison of different agent harness designs.

---

## Methodology & Implementation

### Agent System Design Process

When designing an agent system using the harness framework:

#### 1. Define Harness Interface

```python
class AgentHarness:
    """Define how agent interacts with environment"""
    
    def reasoning_interface(self) -> ReasoningCapability:
        """How does agent express goals and reasoning?"""
        return GoalLanguage(goal_format=PythonAST)
    
    def action_interface(self) -> ActionCapability:
        """How does agent take actions?"""
        return ToolInterface(tools=[...])
    
    def environment_model(self) -> EnvironmentModel:
        """How does agent model world state?"""
        return StateRepresentation(state_format=PythonDataStructures)
```

#### 2. Implement Harness Mechanisms

```python
class AgentMechanisms:
    """Implement reasoning and action capabilities"""
    
    def planner(self) -> Planner:
        """Convert goals to action sequences"""
        return HierarchicalPlanner()
    
    def memory_system(self) -> Memory:
        """Manage context and experience"""
        return IntegratedMemory(
            working_memory=WorkingMemory(),
            semantic_memory=SemanticMemory(),
            episodic_memory=EpisodicMemory()
        )
    
    def tool_manager(self) -> ToolManager:
        """Manage tool invocation and error handling"""
        return ToolManager(tools=[...])
    
    def feedback_loop(self) -> FeedbackMechanism:
        """Learn from outcomes"""
        return ExecutionOutcomeAnalyzer()
```

#### 3. Design Multi-Agent Coordination (if needed)

```python
class MultiAgentHarness:
    """Coordinate multiple agents"""
    
    def define_agent_roles(self) -> RoleAssignment:
        return {
            'orchestrator': OrchestratorAgent(),
            'planner': PlannerAgent(),
            'coder': CoderAgent(),
            'reviewer': ReviewerAgent()
        }
    
    def define_collaboration_mode(self) -> CollaborationMode:
        return ProgrammingMode()  # or RepairMode, DebateMode, etc.
    
    def define_workflow_topology(self) -> WorkflowTopology:
        return HierarchicalTopology()  # or PeerTopology, StreamingTopology, etc.
    
    def shared_artifacts(self) -> ArtifactStore:
        """Central repository for code artifacts"""
        return CodeRepository(
            plans=[],
            implementations=[],
            tests=[],
            traces=[]
        )
```

### Case Study: Coding Assistance Agent System

**Goal:** Autonomous agent that can author patches and resolve issues in live codebases.

**Harness Design:**

```
┌─ Harness Interface ──────────────────────┐
│ Reasoning: Goal = "Fix issue X in repo"  │
│ Action: Tools = {code_read, code_edit,   │
│          run_tests, git_commit}          │
│ Environment: Repository state            │
└──────────────────────────────────────────┘
        ↓
┌─ Harness Mechanisms ─────────────────────┐
│ Planner: Issue → Repo Analysis → Plan    │
│ Memory: Repo knowledge, past patches     │
│ Tools: Read, Edit, Test, Commit          │
│ Feedback: Test results → Plan refinement │
└──────────────────────────────────────────┘
        ↓
┌─ Multi-Agent Coordination ───────────────┐
│ Roles: Analyzer, Coder, Tester, Reviewer │
│ Workflow: Serial pipeline with review    │
│ Artifacts: Patches, tests, documentation│
└──────────────────────────────────────────┘
```

**Execution:**
1. Analyzer reads issue and relevant code
2. Planner creates patch plan (as executable code)
3. Coder generates implementation
4. Tester creates and runs test cases
5. Reviewer validates against guidelines
6. System commits if approved

### Harness-Bench Evaluation Framework

```python
class HarnessBench:
    """Evaluate agent harness systems"""
    
    def task_success_rate(self, agent: Agent, tasks: List[Task]) -> float:
        """Basic metric: % of tasks successfully completed"""
        pass
    
    def harness_effect(self, agent: Agent, tasks: List[Task]) -> Dict:
        """Measure impact of harness design choices"""
        return {
            'planning_quality': measure_plan_quality(agent),
            'memory_effectiveness': measure_memory_utilization(agent),
            'tool_selection_accuracy': measure_tool_accuracy(agent),
            'error_recovery_rate': measure_recovery_success(agent)
        }
    
    def regression_detection(self, agent: Agent, tasks: List[Task]) -> float:
        """Measure: does agent successfully complete previously-solved tasks?"""
        pass
    
    def ablation_study(self, agent_config: HarnessConfig) -> Dict:
        """Measure contribution of each harness component"""
        results = {}
        for component in agent_config.components:
            disabled_config = disable_component(agent_config, component)
            results[component.name] = measure_performance_drop(disabled_config)
        return results
```

---

## Results and Evaluation

### Harness-Bench Results

The paper presents results across multiple categories of agent systems:

#### Coding Agents

**Benchmark:** Software development tasks (bug fixes, feature implementation)

**Findings:**
- Code-based harnesses improve success rate by 18.3% vs. text-based plans
- Plan-verify loop catches 72% of problematic implementations before execution
- Multi-agent coordination with shared artifacts outperforms sequential individual agents by 23%

#### GUI Automation Agents

**Benchmark:** GUI interaction tasks (form filling, workflow automation)

**Findings:**
- DOM-based environment model enables 94% accuracy in element selection vs. 71% for vision-only
- Tool composition (click → wait → verify) outperforms single-action sequences
- State verification prevents cascading errors (prevents 65% of multi-step failures)

#### Scientific Discovery Agents

**Benchmark:** Hypothesis testing in simulation environments

**Findings:**
- Explicit experiment specifications (as code) improve reproducibility
- Shared artifact repository enables agents to build on each other's work
- Workflow orchestration enables complex pipelines (data generation → simulation → analysis)

#### Embodied Agents

**Benchmark:** Robotic control and interaction

**Findings:**
- Code-based policy representation enables transfer learning
- Simulator-based verification reduces real-world failures by 54%
- Skill libraries reduce development time for new behaviors by 40%

### Open Challenges Identified

**1. Evaluation Beyond Final Task Success**
- Current metrics focus on pass/fail. Need metrics for:
  - Plan quality and safety
  - Robustness and failure recovery
  - Data efficiency and learning speed
  - Human interpretability and controllability

**2. Verification Under Incomplete Feedback**
- Real environments provide incomplete feedback. How do agents verify plans when:
  - Outcomes are delayed
  - Feedback is probabilistic
  - Causality is unclear
  - Multiple simultaneous actions have interdependent effects

**3. Regression-Free Harness Improvement**
- As agent systems improve, how do we:
  - Prevent performance regression on previously-solved tasks
  - Maintain backward compatibility
  - Validate that improvements generalize

**4. Consistent Shared State in Multi-Agent Systems**
- When multiple agents modify shared code artifacts:
  - How do we maintain consistency
  - How do we handle concurrent modifications
  - How do we prevent race conditions

**5. Human Oversight for Safety-Critical Actions**
- For high-stakes decisions (financial transactions, medical recommendations):
  - How do we enable human-in-the-loop decision making
  - How do we explain agent reasoning to humans
  - How do we maintain human control and accountability

**6. Extensions to Multimodal Environments**
- Current work focuses on text/code. Extensions needed for:
  - Visual reasoning and planning
  - Multimodal information fusion
  - Cross-modal grounding
  - Embodied agent scenarios

---

## Practical Applications & Use Cases

### 1. Autonomous Coding Assistants

**Application:** AI agents that autonomously author, review, and commit code patches.

**Harness Design:**
- Interface: Repository state as code artifacts
- Mechanisms: Planning (issue analysis), memory (codebase knowledge), tools (read/write/test/commit)
- Coordination: Multi-agent (analyzer, coder, reviewer, tester)

**Value:** Developers focus on high-level decisions while agents handle implementation details.

### 2. GUI and Operating System Automation

**Application:** Agents that interact with GUI applications and operating systems through automation.

**Harness Design:**
- Interface: DOM tree/accessibility API as environment model
- Mechanisms: Visual reasoning, action sequencing, error recovery
- Tools: Click, type, scroll, extract text, verify state

**Value:** Automating repetitive tasks and enabling accessibility for users with disabilities.

### 3. Scientific Discovery Pipelines

**Application:** Multi-agent systems that design experiments, run simulations, and analyze results.

**Harness Design:**
- Interface: Scientific domain model (hypotheses, experiments, data)
- Mechanisms: Experimental design, simulation execution, statistical analysis
- Coordination: Specialist agents (hypothesis generation, experimentation, analysis)

**Value:** Accelerate scientific discovery by automating experimental workflows.

### 4. DevOps and Infrastructure Automation

**Application:** Agents that provision, configure, and manage cloud infrastructure.

**Harness Design:**
- Interface: Infrastructure as code (Terraform, CloudFormation)
- Mechanisms: Planning (deployment strategies), tool use (API calls), verification (health checks)
- Coordination: Multiple agents for different infrastructure domains

**Value:** Enable rapid, reliable infrastructure changes at scale.

### 5. Enterprise Workflow Automation

**Application:** Multi-agent systems that coordinate complex business processes.

**Harness Design:**
- Interface: Workflow specifications as executable processes
- Mechanisms: Task decomposition, execution coordination, exception handling
- Coordination: Role-based agents (initiator, processor, approver, logger)

**Value:** Streamline business processes and reduce human error.

---

## Insights & Implications

### 1. Code as First-Class Operational Substrate

**Insight:** Code is not just an output format but the fundamental substrate through which agents operate—enabling reasoning, action, verification, and coordination.

**Implication:** Future agent systems should be designed around code-based representations from the ground up, rather than bolting code generation onto existing agent architectures.

### 2. Executability Enables Verification

**Insight:** By representing plans as executable code, agents can verify plans before commitment, catching errors before they cause damage.

**Implication:** Verification should be integrated into agent execution loops, not applied post-hoc.

### 3. Multi-Agent Coordination Requires Shared Representations

**Insight:** Agents coordinate effectively when they share representations (code artifacts, execution traces, specifications).

**Implication:** Multi-agent systems should center on shared artifact repositories rather than point-to-point communication.

### 4. Agent Reliability Emerges from Architecture

**Insight:** An agent's reliability depends not just on the underlying model quality but fundamentally on the harness architecture—how it reasons, what tools it has access to, how it coordinates with other agents.

**Implication:** Agent system design is as important as model selection in determining overall reliability.

### 5. Harness Design is Empirical

**Insight:** The paper demonstrates that different harness designs (planning strategies, memory systems, tool sets, coordination patterns) have measurable impacts on performance.

**Implication:** Harness design should be treated as an empirical science, with systematic experimentation and benchmarking.

---

## Code & Resources

### Official Resources

- **Harness-Bench Repository:** Reference implementations and evaluation suite
- **Case Study Implementations:** Coding agents, GUI agents, scientific discovery agents
- **Documentation:** Framework guides and design patterns

### Dependencies and Frameworks

**Coding Agent Case Study:**
- Repository: Git-based code repository (local or GitHub)
- LLM: Claude, GPT-4, or compatible models
- Tools: Code editors, test runners, linters
- Environment: Command-line execution sandbox

**GUI Automation Case Study:**
- Browser: Playwright for web automation
- Accessibility: Native OS APIs for desktop automation
- Vision: Optional computer vision for visual grounding
- Tools: Browser DevTools, OS automation APIs

**Scientific Discovery Case Study:**
- Simulation: Custom domain simulator or existing scientific software
- Data: Datasets relevant to domain
- Analysis: Scientific computing libraries (NumPy, SciPy, TensorFlow)
- Visualization: Plotting and analysis tools

### Quick-Start Integration Pattern

```python
from agent_harness import (
    AgentHarness, AgentMechanisms, MultiAgentHarness,
    PlanExecuteVerifyLoop
)

# Step 1: Define harness interface
harness = AgentHarness()
harness.reasoning_interface = GoalLanguage()
harness.action_interface = ToolInterface(tools=[...])
harness.environment_model = StateRepresentation()

# Step 2: Implement mechanisms
mechanisms = AgentMechanisms()
mechanisms.planner = HierarchicalPlanner()
mechanisms.memory = IntegratedMemory()
mechanisms.tool_manager = ToolManager()

# Step 3: Define multi-agent coordination (if needed)
multi_agent = MultiAgentHarness()
multi_agent.roles = {
    'orchestrator': OrchestratorAgent(),
    'worker': WorkerAgent()
}

# Step 4: Execute plan-execute-verify loop
executor = PlanExecuteVerifyLoop(
    harness=harness,
    mechanisms=mechanisms,
    multi_agent=multi_agent
)

result = executor.run(
    goal="Solve problem X",
    max_iterations=10,
    human_review_required_for=['safety_critical_action']
)
```

---

## Related Work & Context

### Agent Systems and Orchestration

- **LangChain, LlamaIndex, CrewAI:** Practical agent frameworks
- **ReAct (Yao et al.):** Reasoning + Acting paradigm
- **AutoGPT, GPT-Engineer:** Early autonomous agent systems

### Multi-Agent Systems

- **MASMAS:** Multi-agent software modeling and simulation
- **Swarm Intelligence:** Coordination without central control
- **Game Theory for Multi-Agent Coordination:** Mechanism design, equilibrium

### Program Synthesis and Code Generation

- **Program Synthesis:** Generating programs from specifications
- **Code Generation:** LLMs for code authorship
- **Program Verification:** Formal verification of correctness

### Workflow and Process Automation

- **Workflow Languages:** BPEL, YAML-based orchestration
- **Business Process Management:** Enterprise workflow automation
- **Executable Specifications:** Specification languages that execute

### Testing and Verification

- **Property-Based Testing:** QuickCheck, Hypothesis
- **Formal Verification:** Model checking, theorem proving
- **Runtime Verification:** Monitoring execution against specifications

### Related Papers from Survey

- **Code Understanding Agents:** Agents that reason about code
- **Agentic Code Generation:** Agents that generate code
- **Multi-Agent Coding:** Teams of agents building software together
- **Agent Debugging (AgentDebugX):** Observability and error recovery
- **Agent Framework Testing (LogicHunter):** Quality assurance for frameworks

### Positioning in Research Landscape

```
Traditional Software Engineering
        ↓
    Agent-Based Development
        ↓
    Code as Agent Harness
        (↓ unifying lens)
    ├─ Code Generation
    ├─ Code Reasoning
    ├─ Tool Use
    ├─ Multi-Agent Coordination
    └─ Verification & Safety
```

### Future Research Directions

1. **Automated Harness Design:** Can we automatically design optimal harnesses for specific problem domains?

2. **Harness Composition:** How can we combine harnesses to solve larger problems?

3. **Adaptive Harnesses:** Can harnesses adapt their structure based on feedback and performance?

4. **Formal Verification:** Can we formally verify properties of code-based harnesses?

5. **Scalability:** How do harnesses scale to very large codebases and complex workflows?

6. **Human-AI Collaboration:** How do we design harnesses that enable effective human-AI partnership?

---

## Key Takeaways

"Code as Agent Harness" provides a foundational conceptual framework for understanding and designing LLM agent systems:

- **Unified Perspective:** Code serves as the central operational substrate for agent systems
- **Systematic Architecture:** Three-layer model (interface, mechanisms, coordination) enables principled design
- **Executable Verification:** Plans as code enable execution-based verification before commitment
- **Multi-Agent Scalability:** Shared code artifacts enable sophisticated multi-agent workflows
- **Empirical Grounding:** Harness design choices have measurable impacts on performance

This work bridges the gap between high-level agent reasoning and low-level execution, providing a systematic approach to building reliable, observable, and coordinated agent systems. As LLM agents become more powerful and are deployed in increasingly complex environments, the harness framework provides essential infrastructure for managing that complexity while maintaining correctness and safety.
