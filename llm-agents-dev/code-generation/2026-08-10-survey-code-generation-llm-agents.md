# A Survey on Code Generation with LLM-based Agents

**Paper ID:** arXiv:2508.00083  
**Authors:** Yihong Dong, Xue Jiang, Jiaru Qian, Tian Wang, Kechi Zhang, Zhi Jin, Ge Li  
**Published:** August 2025  
**URL:** https://arxiv.org/abs/2508.00083

## Executive Summary

This comprehensive survey presents a systematic overview of LLM-based code generation agents, which are fundamentally restructuring software development by enabling autonomous end-to-end code workflows. Unlike traditional code generation, code generation agents exhibit three core distinguishing features: autonomy in managing the entire development workflow, expanded task scope across the full software development lifecycle (SDLC), and enhanced engineering practicality with focus on real-world challenges like system reliability and tool integration. This work is essential for understanding the evolution from isolated code generation models to intelligent, adaptive agents that drive modern software engineering practices.

## Problem Statement

Traditional code generation models focus on generating individual code snippets in isolation, lacking the autonomy and context awareness required for production software development. Key limitations of prior approaches include:

- **Limited Autonomy:** Static code generation without dynamic task decomposition, error recovery, or iterative refinement
- **Narrow Task Scope:** Inability to handle full development lifecycle tasks (requirements analysis, design, implementation, testing, debugging, deployment)
- **Engineering Gaps:** Insufficient attention to practical challenges like system reliability, process management, tool integration, and real-world codebase complexity
- **Lack of Adaptive Behavior:** No capability to learn from failures, adapt strategies based on task characteristics, or manage multi-agent coordination

Research gap: Few comprehensive frameworks systematically categorize LLM-based agent architectures, workflows, and evaluation methodologies across the entire development lifecycle.

## Core Concepts & Theory

### Agent Architectures for Code Generation

The survey identifies and categorizes multiple architectural patterns:

**1. Single-Agent Architectures**
```
LLM Agent
    ↓
Task Decomposition
    ↓
Plan Generation
    ↓
Code Implementation
    ↓
Tool Invocation (Execution, Testing, Debugging)
    ↓
Iterative Refinement
```

Single-agent systems use a monolithic LLM to handle all decision-making and execution, with integrated loops for decomposition, planning, and refinement.

**2. Multi-Agent Orchestration**
```
Coordinator Agent
    ├→ Planner Agent ──→ Plan
    ├→ Coder Agent ────→ Code
    ├→ Debugger Agent ──→ Fixes
    └→ Tester Agent ────→ Validation
         ↓ (Feedback Loop)
    Aggregate Results & Adapt
```

Multi-agent systems distribute roles across specialized agents, enabling parallel execution and specialization. Common topologies include hierarchical (coordinator-worker), competitive (ensemble voting), and collaborative (sequential handoffs).

**3. Key Components in Agent Workflows**

- **Task Decomposition:** Breaking down complex coding tasks into manageable subtasks
- **Plan Generation:** Creating structured execution plans before coding
- **Code Implementation:** Generating code with context-awareness and iterative refinement
- **Tool Integration:** Invoking compilers, interpreters, test runners, debuggers, and retrieval systems
- **Feedback Loops:** Incorporating test results, error messages, and intermediate outputs into refinement cycles
- **Error Recovery:** Implementing strategies for handling failures at different workflow stages

### Code Generation Agent Taxonomy

The survey proposes a comprehensive taxonomy across multiple dimensions:

**Workflow Dimension:**
- Single-pass generation (generate once, no iteration)
- Iterative refinement (test → debug → regenerate)
- Plan-then-code (explicit planning before implementation)
- In-context learning (learning from examples within the same conversation)

**Scope Dimension:**
- Snippet-level (small isolated functions)
- Module-level (complete files or packages)
- Repository-level (large-scale codebase changes)
- System-level (microservices and distributed systems)

**Tool Integration Dimension:**
- Static analysis (syntax checking, type checking)
- Dynamic testing (execution, test generation, validation)
- Debugging (error diagnosis, root cause analysis)
- Environment interaction (system calls, API invocations)

## Main Ideas & Contributions

### 1. Systematic Framework for Code Generation Agents

The survey establishes a structured framework covering:
- Core agent architectures (single-agent, multi-agent, hybrid)
- Common workflow patterns and their effectiveness
- Specialized agent roles and responsibilities
- Integration mechanisms with development tools

### 2. Autonomy Through Decomposition and Planning

Code generation agents achieve autonomy via:
- **Task Decomposition:** Breaking problems into manageable units that fit within token limits and reasoning capacity
- **Explicit Planning:** Creating execution plans before code generation, improving success rates
- **Adaptive Strategies:** Adjusting approaches based on task complexity, prior failures, and feedback

### 3. Expanded Scope Across Software Development Lifecycle

- **Requirements & Design:** Understanding specifications and architectural constraints
- **Implementation:** Code synthesis with context awareness
- **Testing & Validation:** Generating and executing test cases
- **Debugging & Refinement:** Identifying and fixing errors
- **Documentation:** Generating and maintaining documentation

### 4. Engineering Practicality Focus

The shift from theoretical capability to practical deployment requires:
- **System Reliability:** Error handling, fault tolerance, recovery mechanisms
- **Process Management:** Workflow orchestration, state management, logging
- **Tool Integration:** Seamless interaction with development environments (IDEs, version control, CI/CD)
- **Scalability & Cost:** Handling large codebases with efficient token usage and parallel execution

## Methodology & Implementation

### Evaluation Benchmarks

The survey catalogs mainstream benchmarks for code generation agents:

**1. Single-Task Benchmarks**
- **HumanEval:** 164 Python problems with reference implementations and test cases
- **MBPP:** 974 Python problems spanning multiple programming paradigms
- **CodeXGLUE:** Multi-faceted code understanding tasks including code-to-code, code-to-text, and text-to-code

**2. Multi-Task Benchmarks**
- **AgentBench:** 8 interactive tasks supporting multi-step decision-making and intermediate behavior evaluation
- **CodeAgentBench:** Multi-step coding tasks (planning, implementation, debugging, refinement)
- **SWE-bench:** Real GitHub issues and pull requests for realistic software engineering tasks

**3. Domain-Specific Benchmarks**
- **Repository-level reasoning:** Handling large codebases with complex interdependencies
- **Infrastructure-as-Code:** AWS CloudFormation and Terraform templates
- **Data Science:** Jupyter notebooks and ML pipeline generation

### Evaluation Metrics

- **Pass@k:** Percentage of tasks solved with k attempts (k=1, k=5, k=10)
- **Success Rate:** Task completion with correct functionality
- **Intermediate Behavior:** Quality of planning, decomposition, and debugging steps
- **Efficiency:** Token usage, latency, cost-effectiveness
- **Robustness:** Performance across diverse task types and complexity levels

### Key Findings on Agent Performance

[Exact figures unavailable — see full paper] but literature indicates:
- Multi-agent systems show 15-30% improvement over single-agent baselines on complex tasks
- Plan-then-code approaches achieve higher success rates than direct generation
- Repository-level reasoning remains challenging, with success rates 20-40% lower than snippet-level tasks
- Tool integration (compilation, testing, debugging) is critical for practical applications

## Practical Applications & Use Cases

### 1. Software Development Automation
- **Code Review & Refinement:** Autonomous improvement of code quality, style, and patterns
- **Bug Detection & Fixing:** Systematic identification and repair of defects
- **Feature Implementation:** End-to-end development of new functionality from specifications
- **Code Migration:** Refactoring and modernization of legacy systems

### 2. Specific Development Workflows
- **Test-Driven Development:** Generating tests first, then implementing to satisfy tests
- **Continuous Integration/Deployment:** Automated validation and deployment decision-making
- **Documentation:** Auto-generating and maintaining comprehensive code documentation
- **API Integration:** Automatically discovering and using APIs within workflows

### 3. Multi-Agent Coordination Examples
- **Hierarchical:** Orchestrator delegates to specialized agents (planner, coder, debugger, tester)
- **Ensemble:** Multiple agents generate solutions, voting or ranking to select best option
- **Sequential Handoff:** Agents pass work downstream with context and validation
- **Collaborative Review:** Agents critique and improve each other's work iteratively

### 4. Integration Challenges & Solutions
- **Token Limitations:** Implementing chunking, summarization, and progressive context refinement
- **Tool Reliability:** Handling tool failures, timeouts, and malformed outputs gracefully
- **State Management:** Tracking progress, caching results, managing multi-step execution state
- **Cost Optimization:** Efficient use of API calls, caching, and selective verification

## Insights & Implications

### Impact on Software Development
1. **Paradigm Shift:** From tools that assist developers to agents that drive development autonomously
2. **Skill Requirements:** Developers transition from writing code to designing agent workflows and prompts
3. **Quality Metrics:** New evaluation criteria beyond code correctness (reliability, cost, latency, adaptability)
4. **Team Structure:** Introduction of agent orchestrators, workflow designers, and agent trainers

### Advancement in Autonomous Coding
1. **End-to-End SDLC Coverage:** Moving beyond snippet generation toward full software engineering tasks
2. **Real-World Applicability:** Increasing focus on production systems with reliability and scalability requirements
3. **Adaptive Agents:** Evolution toward agents that learn from feedback and adapt strategies dynamically
4. **Generalization:** Improving agent performance across diverse programming languages, frameworks, and domains

### Limitations & Open Questions
1. **Context Window Constraints:** Large codebases exceed LLM context, requiring sophisticated chunking strategies
2. **Test Coverage:** Agents struggle with comprehensive test generation and mutation testing
3. **Design Reasoning:** Limited ability to make high-level architectural decisions
4. **Hallucination & Correctness:** Potential for agents to confidently produce incorrect code requiring verification layers
5. **Tool Dependency:** Heavy reliance on well-designed tools and APIs for agent interaction
6. **Reproducibility & Determinism:** Challenges in making agent workflows reproducible and predictable

### Relevance to Skill Frameworks
- **Agent Specialization:** Natural fit for skill-based architectures where agents master specific domains
- **Skill Composition:** Complex development tasks decompose into reusable agent skills
- **Skill Learning:** Agents can acquire new skills through fine-tuning and reinforcement learning
- **Dynamic Skill Selection:** Orchestrators can select appropriate skills based on task requirements

## Code & Resources

### Official Repositories & Tools
- **AgentBench:** Multi-step agent evaluation benchmark with interactive tasks
  - Repository: OpenBMB/AgentBench
  - Supports various code generation agents and domains
- **CodeAgentBench:** Comprehensive benchmark for code generation agents
  - Focus on multi-step coding tasks (planning, implementation, debugging)
  - Evaluates both task success and intermediate behaviors
- **OpenCode:** Framework for building and evaluating code generation agents
  - Multi-provider agent routing with explicit permission-controlled subagent architectures
  - Supports various LLM backends and tool integrations

### Popular Agent Frameworks for Code Generation
- **Anthropic Claude with tool use:** Native function calling and iterative refinement
- **OpenAI Code Interpreter:** Interactive Python execution environment
- **LangChain Agents:** Flexible agent framework with tool integration
- **AutoGPT/AgentGPT:** Open-source agent orchestration frameworks
- **Copilot/Codeium:** IDE-integrated code generation assistants

### Compute & API Requirements
- **Model Requirements:** Access to capable LLMs (GPT-4, Claude 3.5+, open-source alternatives like Llama 3)
- **Tool Integration:** Compilers, interpreters, test runners, static analysis tools
- **Token Budget:** Typical complex tasks require 5K-50K tokens depending on codebase and workflow
- **Latency:** Multi-agent workflows introduce 2-5x latency overhead compared to direct generation

### Quick-Start Integration Guide

```python
# Example: Simple code generation agent with test validation
from anthropic import Anthropic

client = Anthropic()

def code_generation_agent(task: str, max_iterations: int = 3) -> dict:
    """Multi-turn code generation agent with test validation."""
    
    conversation_history = []
    current_code = None
    
    # Initial code generation
    conversation_history.append({
        "role": "user",
        "content": f"Generate Python code to solve: {task}"
    })
    
    for iteration in range(max_iterations):
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=conversation_history
        )
        
        assistant_message = response.content[0].text
        current_code = extract_code_block(assistant_message)
        
        # Validate with tests
        test_results = run_tests(current_code)
        
        if test_results["passed"]:
            return {
                "code": current_code,
                "success": True,
                "iterations": iteration + 1
            }
        
        # Continue refinement if tests fail
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        conversation_history.append({
            "role": "user",
            "content": f"Tests failed: {test_results['errors']}\n"
                      f"Please fix the code and ensure all tests pass."
        })
    
    return {
        "code": current_code,
        "success": False,
        "iterations": max_iterations
    }

# Usage
result = code_generation_agent("Implement a binary search function")
print(f"Success: {result['success']}, Iterations: {result['iterations']}")
```

## Related Work & Context

### Foundational Work in Code Generation
- **Seq2Seq models:** Early neural approaches to code generation
- **CodeBERT:** Pre-trained models for code understanding
- **GPT-3 Code:** Demonstrated in-context learning for code synthesis
- **GitHub Copilot:** Industrial deployment of neural code completion

### Related Papers on Agent Orchestration
- **Reinforcement Learning for LLM-based Multi-Agent Systems through Orchestration Traces** (arXiv:2605.02801): Framework for optimizing agent interactions through RL
- **AgentForge: Execution-Grounded Multi-Agent LLM Framework** (arXiv:2604.16314): Framework for building multi-agent systems with execution grounding
- **From Agent Loops to Structured Graphs** (arXiv:2604.13671): Scheduler-theoretic approach to agent execution
- **ABSTRAL: Automated Multi-Agent System Design via Skill-Referenced Adaptive Search** (arXiv:2603.24879): Automatic agent system design through skill discovery

### Emerging Trends & Future Research
1. **Vertical Integration:** Combining specialized models for different development phases
2. **Feedback Integration:** Continuous learning from deployment metrics and user feedback
3. **Formal Verification:** Integration of theorem provers and formal methods
4. **Human-in-the-Loop:** Collaborative workflows combining agent suggestions with human expertise
5. **Cross-Language Agents:** Supporting multiple programming languages and paradigms
6. **Domain-Specific Agents:** Specialization for particular frameworks (React, Django, etc.) or domains (data science, systems)

## Discussion & Critical Perspective

The survey reveals a field in transition from research proof-of-concepts to production systems. Key insights include:

1. **Maturity Gap:** While base models are powerful, agent orchestration and workflow management remain immature
2. **Cost-Quality Tradeoff:** Multi-agent systems improve quality but at higher computational cost
3. **Specialization Wins:** Agents tuned for specific domains/tasks significantly outperform general models
4. **Integration Complexity:** Real-world deployment requires careful consideration of tool reliability and error handling
5. **Measurement Challenges:** Existing benchmarks may not capture practical software engineering challenges

The transition from isolated code generation to end-to-end agent-driven development represents a fundamental shift in how software is created, requiring rethinking of development processes, team organization, and quality assurance methodologies.
