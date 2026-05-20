# Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems

**ArXiv ID:** 2605.18747  
**Authors:** Xuying Ning, Katherine Tieu, Dongqi Fu, Tianxin Wei, Zihao Li, and 40+ co-authors  
**Submission Date:** May 18, 2026  
**Note:** This is a comprehensive position paper and survey on code-centric agent design

## Executive Summary

This position paper presents a fundamental paradigm shift in how we conceptualize and architect AI agents: **code as the central infrastructure** for agent systems. Rather than treating code as merely a target output (what language models generate), the paper argues that code should serve as the operational substrate for agent reasoning, acting, environment modeling, and execution-based verification. By positioning code as the agent harness—a unified interface connecting models to reasoning, planning, memory, and tool use—the authors provide a comprehensive framework for building more reliable, transparent, and capable agentic systems.

## Problem Statement

### Current State of Agentic AI Systems
1. **Inconsistent Architecture:** Agentic systems lack standardized patterns, leading to:
   - Bespoke implementations for each application
   - Difficult reproducibility and debugging
   - Fragmented community knowledge
   - High development overhead

2. **Reasoning Opacity:** Current agent systems often:
   - Make reasoning implicit in model outputs
   - Lack clear decision trails
   - Cannot effectively debug failure modes
   - Struggle with reproducibility

3. **State and Execution Issues:**
   - Stateless interactions lose context across reasoning steps
   - Implicit execution logic is hard to control and modify
   - Verification and rollback mechanisms are absent
   - State inconsistencies cause systematic failures

4. **Tool Integration Fragmentation:**
   - No standardized interface for tool composition
   - Integration with external systems is ad-hoc
   - Complex reasoning about tool interactions
   - Difficult to trace failures through tool chains

### Prior Limitations in Agent Design
- **Monolithic Models:** Treating the entire agent as black-box model outputs
- **Implicit Planning:** Planning logic embedded in model weights rather than explicit structures
- **String-Based Reasoning:** Using text strings for complex reasoning limits verification
- **Manual Scaffolding:** Prompts and instructions lack programmatic structure
- **No Standardization:** Each agent implementation reinvents the wheel

### Research Gap
The gap exists between what human-designed software systems achieve (explicit logic, state management, verification, composition) and what current AI agents achieve. What's needed is a framework that:
1. Makes agent reasoning executable and verifiable
2. Provides clear state management
3. Enables composable tool integration
4. Supports transparent decision-making
5. Facilitates debugging and iteration

## Core Concepts & Theory

### The Code-as-Harness Paradigm

**Definition:** Code serves as the agent harness—a structured interface that:
1. **Converts model outputs to executable structures**
2. **Manages stateful execution and reasoning**
3. **Enables verification and debugging**
4. **Coordinates tool composition and execution**
5. **Provides feedback loops for model improvement**

### Three Core Layers of Agent Architecture

**Layer 1: Harness Interface**
Defines where code connects agents to reasoning, action, and environment:

```
Agent (Language Model)
    ↓
Code (Harness Interface)
    ├─→ Reasoning Substrate (semantic representation)
    ├─→ Action Specification (executable operations)
    └─→ Environment Model (state representation)
```

**Harness Components:**
- **Program Structure:** Abstract syntax trees (ASTs) or similar structures
- **Type System:** Ensures generated code is syntactically valid
- **Constraints:** Limits on reasoning scope and action space
- **Grounding:** Links symbolic reasoning to concrete operations

**Layer 2: Harness Mechanisms**
Mechanisms that make harnesses reliable and adaptive:

1. **Planning:**
   - **Explicit Plans:** Code-represented action sequences
   - **Hierarchical Planning:** Abstract goals decomposed to concrete steps
   - **Adaptive Planning:** Replanning based on execution results
   ```python
   plan = [
       ("search", {"query": "customer_name"}),
       ("filter", {"condition": "status==active"}),
       ("format", {"template": "email_template.html"})
   ]
   ```

2. **Memory:**
   - **Working Memory:** Current reasoning state
   - **Episodic Memory:** History of actions and outcomes
   - **Semantic Memory:** Knowledge base and facts
   - **Implementation:** Structured data structures (not string-based)
   ```python
   memory = {
       "working": {"current_task": "...", "progress": 0.7},
       "episodic": [{"action": "...", "result": "...", "timestamp": ...}],
       "semantic": {"facts": {...}, "rules": {...}}
   }
   ```

3. **Tool Use:**
   - **Tool Interface Definition:** Formal specifications (OpenAPI, JSON-Schema)
   - **Composition:** Chaining multiple tools
   - **Error Handling:** Explicit fallbacks and recovery
   - **Verification:** Pre-execution validation
   ```python
   tool = {
       "name": "database_query",
       "inputs": {"sql": "str", "connection_id": "int"},
       "outputs": {"results": "list[dict]"},
       "preconditions": ["connection_valid"],
       "postconditions": ["results_valid"]
   }
   ```

4. **Feedback and Control:**
   - **Execution Feedback:** Observe action outcomes
   - **Error Detection:** Identify and classify failures
   - **Corrective Actions:** Automatic or human-guided corrections
   - **Learning:** Update models based on feedback
   ```python
   if execution_result.status == "error":
       error_type = classify_error(execution_result)
       corrective_action = error_handlers[error_type]
       retry_with_modification(plan, corrective_action)
   ```

### Comparison with Alternatives

**Implicit vs. Explicit Reasoning:**
| Aspect | Black-box Agent | Code-as-Harness |
|--------|-----------------|-----------------|
| Reasoning | Implicit in model | Explicit in code |
| Verification | Post-hoc | Pre-execution |
| Debugging | Difficult | Traceable |
| State | Implicit | Explicit |
| Composition | Limited | Flexible |

## Main Ideas & Contributions

### Contribution 1: Code-as-Harness Framework

Establishes a unified conceptual framework where code is the central agent infrastructure:
- **Reasoning Made Executable:** Model outputs converted to structured code
- **Planning Transparency:** Explicit code-represented action sequences
- **Memory Management:** Structured state rather than implicit context
- **Tool Coordination:** Formal tool composition and error handling

### Contribution 2: Systematic Categorization

Provides comprehensive taxonomy of harness components:
- **Interface Types:** How code connects models to execution
- **Mechanism Categories:** Planning, memory, tool use, feedback
- **Implementation Patterns:** Best practices and common architectures
- **Trade-offs:** When to use different harness designs

### Contribution 3: Best Practices and Patterns

Documents empirically-validated design patterns:
- **Stateful Planning:** How to maintain planning state across steps
- **Tool Composition:** Patterns for chaining and orchestrating tools
- **Error Recovery:** Explicit error classification and handling
- **Human Integration:** Points where humans can intervene or guide

### Contribution 4: Architectural Guidance

Provides architects with decision framework for building agent systems:
- **When to use code-based planning** vs. implicit reasoning
- **State management strategies** for different application types
- **Tool integration patterns** for common scenarios
- **Verification and testing** strategies

## Methodology & Implementation

### Study Approach

The paper conducts comprehensive analysis of:
1. **Existing Agent Systems:** Empirical study of current implementations
2. **Design Patterns:** Analysis of what works across implementations
3. **Best Practices:** Community-validated approaches
4. **Trade-offs:** Practical considerations in different scenarios

### Categories of Agent Systems Analyzed

**1. Reasoning-Focused Agents**
- Use cases: Complex decision-making, multi-step problem solving
- Key harness feature: Explicit planning and reasoning verification
- Example: Mathematical reasoning, scientific problem-solving

**2. Tool-Using Agents**
- Use cases: Real-world task execution, API coordination
- Key harness feature: Tool interface specification and composition
- Example: Software engineering agents, automation systems

**3. Interactive Agents**
- Use cases: Dialog systems, collaborative tasks
- Key harness feature: Multi-turn state management
- Example: Customer service, tutoring systems

**4. Embodied Agents**
- Use cases: Robotics, physical world interaction
- Key harness feature: Environment state representation
- Example: Robot manipulation, autonomous systems

### Implementation Patterns

**Pattern 1: Planning as Program Generation**
```python
class PlanningAgent:
    def reason(self, task):
        # Generate plan as executable code
        plan_code = self.model.generate_plan(task)
        plan_ast = parse(plan_code)  # Convert to AST
        return plan_ast
    
    def execute(self, plan):
        for step in plan:
            result = execute_step(step)
            if result.error:
                replanned = self.replan_from(step, result)
                result = execute_step(replanned)
        return result
```

**Pattern 2: Stateful Memory Management**
```python
class StatefulAgent:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []
        self.semantic_memory = {}
    
    def think(self, observation):
        # Update working memory
        self.working_memory.update(observation)
        
        # Retrieve relevant episodic memories
        relevant = retrieve(self.episodic_memory, observation)
        
        # Combine for reasoning
        context = combine([self.working_memory, relevant, self.semantic_memory])
        return self.model.reason(context)
    
    def act(self, action):
        result = execute(action)
        # Log to episodic memory
        self.episodic_memory.append({
            "action": action,
            "result": result,
            "timestamp": now(),
            "context": self.working_memory.copy()
        })
        return result
```

**Pattern 3: Tool Composition with Verification**
```python
class ToolUsingAgent:
    def __init__(self, tools):
        self.tools = {tool.name: tool for tool in tools}
        self.tool_graph = build_dependency_graph(tools)
    
    def plan_tool_usage(self, goal):
        # Generate tool sequence
        sequence = self.model.generate_tool_sequence(goal, self.tool_graph)
        
        # Verify preconditions
        for tool_call in sequence:
            tool = self.tools[tool_call.name]
            if not all(check_precondition(p) for p in tool.preconditions):
                return self.replanned_sequence(goal)
        
        return sequence
    
    def execute_tools(self, sequence):
        results = []
        for tool_call in sequence:
            result = self.tools[tool_call.name](**tool_call.args)
            if not result.success:
                recovery = self.error_recovery(tool_call, result)
                result = execute(recovery)
            results.append(result)
        return results
```

### Evaluation Framework

**Key Metrics:**
1. **Correctness:** Do agents produce correct outputs?
2. **Verifiability:** Can outcomes be traced to specific decisions?
3. **Debuggability:** How easily can failures be diagnosed?
4. **Composability:** Can components be reused across agents?
5. **Efficiency:** What is computational overhead of explicit structure?
6. **Robustness:** How well do agents handle errors?

### Dataset and Benchmarks

While this is a position/survey paper, analysis includes:
- **Agent Benchmark Suite:** HumanEval (code generation), SWE-bench (software engineering), ARC (reasoning)
- **Tool Composition Tasks:** Multi-step tool chains with error conditions
- **Interactive Tasks:** Multi-turn dialog and collaborative problem-solving
- **Real-World Systems:** Analysis of production agent systems

## Practical Applications & Use Cases

### 1. Software Engineering Agents
**Application:** Automated code generation, debugging, testing
**Harness Design:**
- Explicit code generation as primary output
- Tool use for IDE operations, testing, version control
- Episodic memory of past code attempts and lessons learned
- Error feedback from test failures

**Benefits:**
- Generated code is immediately executable and verifiable
- Test failures provide structured feedback
- Can apply code-level optimizations and refactoring

### 2. Scientific Research Agents
**Application:** Literature search, hypothesis testing, result interpretation
**Harness Design:**
- Planning layer for research methodology
- Tool interface for database queries, simulations, analysis
- Semantic memory of papers and findings
- Structured reasoning about experimental results

**Benefits:**
- Explicit hypothesis statements and test protocols
- Reproducible research methodology
- Clear traceability of conclusions to evidence

### 3. Data Analysis Agents
**Application:** Exploratory data analysis, reporting, anomaly detection
**Harness Design:**
- Code generation for analysis pipelines
- Tool use for database queries and statistical operations
- Working memory for intermediate results
- Structured output formatting

**Benefits:**
- Generated analysis code is reusable and auditable
- Intermediate results enable human inspection
- Error detection through code validation

### 4. Autonomous Robotics
**Application:** Robot task planning and execution
**Harness Design:**
- Explicit action planning with precondition checking
- Environmental state representation
- Tool interface for robot actions
- Feedback loop from sensors

**Benefits:**
- Verifiable safety properties before execution
- Clear rollback mechanisms for failed actions
- Explicit reasoning about physical constraints

### 5. Business Process Automation
**Application:** Workflow orchestration, data processing, reporting
**Harness Design:**
- Explicit workflow representation as code
- Tool integration with enterprise systems
- State management across workflow steps
- Audit trail and error handling

**Benefits:**
- Workflows are inspectable and auditable
- Clear SLA enforcement through explicit timeouts and retries
- Easy integration with existing business systems

### Implementation Challenges

1. **Model Capability:** Models must reliably generate valid code
2. **Error Recovery:** Detecting and recovering from code errors
3. **Execution Overhead:** Structured execution is slower than implicit reasoning
4. **Type System Design:** Balance expressiveness and safety
5. **Composability:** Ensuring components work together reliably

## Insights & Implications

### Paradigm Shift in Agent Design

**From Implicit to Explicit:**
- Rather than reasoning embedded in model weights
- Reasoning becomes executable and inspectable code
- Enables transparent decision-making and debugging

**From Stateless to Stateful:**
- Current agents treat each interaction independently
- Code-as-harness maintains structured state across interactions
- Enables long-horizon reasoning and learning

**From Monolithic to Modular:**
- Replaces end-to-end models with component architectures
- Promotes reuse and composition of agent components
- Enables mixing models with symbolic reasoning

### Field Impact

**Research Implications:**
- Opens new research directions in agent verification and formal methods
- Enables better evaluation of agent reasoning quality
- Facilitates systematic comparison of agent architectures

**Practical Impact:**
- Dramatically improves debuggability of deployed agents
- Enables enterprise adoption of agent systems
- Supports compliance and auditing requirements

### Fundamental Insights

1. **Structure Beats Strings:** Structured representations enable verification and composition that strings cannot
2. **Explicitness Enables Debugging:** Making reasoning explicit enables diagnosis and improvement
3. **Composition is Key:** Complex capabilities emerge from composing simple, verified components
4. **State Matters:** Explicit state management is critical for long-horizon reasoning
5. **Feedback is Crucial:** Execution feedback provides essential signal for agent improvement

### Limitations and Open Questions

1. **Scalability:** How does overhead of code generation and execution scale?
2. **Generalization:** Do patterns identified work for diverse domains?
3. **Human-AI Collaboration:** How to best integrate human oversight in code-based systems?
4. **Formal Verification:** Can we formally verify agent behavior?
5. **Emergent Behavior:** Can we predict and control emergent behaviors in code-based systems?

## Code & Resources

### Official Resources
- **ArXiv Paper:** https://arxiv.org/abs/2605.18747
- **Full Paper:** https://arxiv.org/pdf/2605.18747.pdf
- **Related GitHub:** https://github.com/YennNing/Awesome-Code-as-Agent-Harness-Papers (curated papers on the topic)

### Dependencies & Framework Requirements

**Core Requirements:**
- Python 3.8+
- Language Models: GPT-4, Claude, Llama, or similar code-capable models
- Code Execution Environment: Sandboxed Python/Node.js for safety
- Type System: Pydantic, dataclasses, or similar for structure definition

**Key Libraries for Implementation:**
```
typing>=3.8
pydantic>=2.0
ast (standard library)
json (standard library)
dataclasses (standard library)
```

**Optional (for specific implementations):**
```
langchain>=0.1.0  # Agent orchestration
anthropic>=0.7.0  # Claude API for code generation
openai>=1.0.0     # GPT API
execute-restricted-python  # Safe code execution
```

### Implementation Patterns

**1. Basic Code-Generation Agent Framework**
```python
from typing import List, Dict, Any
from pydantic import BaseModel
import ast
import json

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    returns: Dict[str, Any]

class PlanStep(BaseModel):
    tool: str
    arguments: Dict[str, Any]

class Agent:
    def __init__(self, model, tools: List[ToolDefinition]):
        self.model = model
        self.tools = {t.name: t for t in tools}
        self.execution_history = []
    
    def generate_plan(self, task: str) -> List[PlanStep]:
        # Generate code that represents the plan
        prompt = f"""
        Given tools: {json.dumps([t.dict() for t in self.tools.values()])}
        Task: {task}
        
        Generate a Python plan as a list of tool calls.
        Output only valid Python code.
        """
        code = self.model.generate(prompt)
        plan = ast.literal_eval(code)  # Parse code to data
        return [PlanStep(**step) for step in plan]
    
    def execute_plan(self, plan: List[PlanStep]) -> List[Any]:
        results = []
        for step in plan:
            tool = self.tools[step.tool]
            result = self.execute_tool(tool, step.arguments)
            self.execution_history.append({
                "tool": step.tool,
                "arguments": step.arguments,
                "result": result
            })
            results.append(result)
        return results
    
    def execute_tool(self, tool: ToolDefinition, args: Dict) -> Any:
        # Validate arguments against tool spec
        # Execute tool safely
        # Return result
        pass
```

**2. Stateful Agent with Memory**
```python
class StatefulAgent:
    def __init__(self, model, tools):
        self.model = model
        self.tools = tools
        self.working_memory = {}
        self.episodic_memory = []
        self.semantic_memory = {}
    
    def observe(self, observation: Dict[str, Any]):
        self.working_memory.update(observation)
    
    def think(self) -> str:
        context = {
            "current_task": self.working_memory.get("current_task"),
            "recent_actions": self.episodic_memory[-5:],
            "relevant_facts": self.retrieve_facts()
        }
        reasoning = self.model.generate_reasoning(context)
        return reasoning
    
    def decide(self, reasoning: str) -> Dict[str, Any]:
        decision = self.model.generate_decision(reasoning)
        return json.loads(decision)  # Parse as structured decision
    
    def act(self, action: Dict[str, Any]):
        result = self.execute_action(action)
        self.episodic_memory.append({
            "action": action,
            "result": result,
            "timestamp": time.time(),
            "context": self.working_memory.copy()
        })
        return result
```

### Quick-Start Guide

**Step 1: Define Your Tools**
```python
tools = [
    ToolDefinition(
        name="search",
        description="Search for information",
        parameters={"query": "string"},
        returns={"results": "list[string]"}
    ),
    ToolDefinition(
        name="retrieve",
        description="Retrieve document details",
        parameters={"document_id": "string"},
        returns={"content": "string"}
    )
]
```

**Step 2: Create Agent**
```python
agent = Agent(model=your_language_model, tools=tools)
```

**Step 3: Execute Tasks**
```python
plan = agent.generate_plan("Find papers about attention mechanisms")
results = agent.execute_plan(plan)
```

## Related Work & Context

### Related Research Areas
1. **Program Synthesis:** Automated code generation from specifications
2. **Neuro-Symbolic AI:** Combining neural networks with symbolic reasoning
3. **Agent Architectures:** BDI agents, cognitive architectures
4. **Tool Use in Language Models:** From Chain-of-Thought to ReAct
5. **Formal Verification:** Verifying agent behavior and safety

### Prior Work Foundations
The paper builds on:
- **ReAct (Yao et al.):** Interleaving reasoning and acting
- **Chain-of-Thought (Wei et al.):** Structured reasoning chains
- **Tool Use in LLMs:** Research on using tools with language models
- **Program Synthesis:** Automated code generation
- **Agent Architectures:** Decades of multi-agent systems research

### Related Papers and Systems
- **AutoHarness:** Automatically synthesizing code harnesses for agents
- **Natural Language Agent Harnesses:** Using NL patterns for agent scaffolding
- **Agentic Harness Engineering:** Observability-driven evolution of harnesses

### Future Research Directions
1. **Formal Verification:** Provable guarantees on agent behavior
2. **Learning to Harness:** Models that learn to generate effective harness code
3. **Optimal Composition:** Discovering optimal ways to combine tools
4. **Transfer Learning:** Harness patterns that transfer across domains
5. **Human-in-the-Loop:** Integration with human decision-making
6. **Emergent Capabilities:** Understanding capabilities arising from harness composition

## Discussion

This position paper reframes how we should think about agentic AI systems. Rather than viewing code as something models generate for external consumption, Code-as-Harness positions code as the fundamental architecture for agent systems.

The implications are profound:
- **Transparency:** Agent reasoning becomes inspectable and verifiable
- **Reliability:** Explicit structure enables error detection and recovery
- **Composability:** Standard interfaces enable mixing and matching components
- **Scalability:** Modular design enables building complex systems systematically
- **Debuggability:** Clear decision trails enable diagnosis and improvement

This shift from implicit to explicit, from monolithic to modular, from stateless to stateful, represents a maturation of agent system design. It aligns AI systems more closely with software engineering best practices while preserving the flexibility and learning capabilities of neural models.

The code-as-harness paradigm provides a bridge between the proven approaches of symbolic AI (explicit reasoning, verification, composition) and the powerful pattern recognition of neural networks (learning, generalization, flexibility).
