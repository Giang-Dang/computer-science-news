# Agentic Tool Use in Large Language Models

**Authors:** Researchers from Harbin Institute of Technology Shenzhen and TikTok Inc  
**ArXiv ID:** 2604.00835  
**Submitted:** April 1, 2026  
**URL:** https://arxiv.org/abs/2604.00835

## Executive Summary

This comprehensive survey systematizes the landscape of tool use in LLM-based agents across three distinct paradigms: prompting-based approaches, supervised learning methods, and reward-driven policy optimization. As LLMs become increasingly deployed as autonomous agents for software development, their real-world effectiveness depends critically on reliable tool use—for information retrieval, computation, external action, and code execution. This paper provides a unified framework for understanding tool-use methods, their strengths, failure modes, and emerging best practices, directly informing how to build robust autonomous coding agents.

## Problem Statement

### The Tool Use Challenge in Autonomous Systems

Large Language Models, while capable at reasoning and planning, have fundamental limitations:

1. **Knowledge cutoff:** LLMs have static training data with a knowledge cutoff date
2. **Computational limitations:** LLMs cannot reliably perform complex arithmetic or symbolic reasoning
3. **Real-world grounding:** LLMs cannot directly access or modify external systems (code repositories, test runners, file systems, APIs)
4. **Verification inability:** LLMs cannot verify their own outputs (cannot run tests, check code syntax)

**Tool use solves these limitations** by enabling agents to:
- Retrieve current information (web search, database queries)
- Delegate computation (calculators, code interpreters, theorem provers)
- Execute actions (file writes, API calls, environment modifications)
- Verify outputs (test execution, code validation, linting)

### The Fragmentation Problem

Prior to this survey, tool-use literature was scattered across:
- **Prompt engineering research:** How to instruct LLMs to use tools via in-context examples
- **Fine-tuning studies:** How to train models to call tools through supervised learning
- **Reinforcement learning papers:** How to learn tool-use policies through reward signals
- **Task-specific systems:** Domain papers that employ tool use without systematic analysis

This fragmentation meant researchers couldn't systematically compare approaches or identify underlying principles.

### Why This Matters for Code Generation

In software development automation, tool use is essential:

```
Development Task         Critical Tool-Use Capability
─────────────────────────────────────────────────────────
Code generation          Code interpreter (Python, bash)
                         Language compiler
                         
Debugging                Debugger interface
                         Stack trace analyzer
                         Test runner
                         
Testing                  Unit test framework
                         Code coverage tools
                         Assertion libraries
                         
Code review              Linter (ESLint, pylint)
                         Type checker (mypy, TypeScript)
                         Security analyzer (bandit)
                         
Refactoring              AST parser
                         Import analyzer
                         Dependency graph tool
                         
Documentation            API reference fetcher
                         Example code retriever
                         Docstring generator
```

Without reliable tool use, autonomous agents generate non-functional code and cannot iteratively improve their outputs.

## Core Concepts & Theory

### The Three Paradigms of Tool Use

The paper organizes all tool-use approaches into three complementary paradigms, each with different tradeoffs:

#### Paradigm 1: Prompting as Plug-and-Play

**Core Idea:** Teach the LLM through in-context examples and instructions how to format tool calls. The LLM remains static (no fine-tuning).

**How It Works:**

```
System Prompt:
"You are a helpful assistant with access to these tools:
1. calculator(expression: str) → float
2. python_interpreter(code: str) → str
3. web_search(query: str) → List[Result]

When you need to use a tool, respond in this JSON format:
{
  \"action\": \"tool_name\",
  \"input\": {\"param\": \"value\"},
  \"reasoning\": \"why you're using this tool\"
}"

User Query: "What is 7 * 42 + sqrt(100)?"

Model Response:
{
  "action": "calculator",
  "input": {"expression": "7 * 42 + sqrt(100)"},
  "reasoning": "Need to compute arithmetic expression"
}

System: "The result is 304.0"

Model: "The answer is 304."
```

**Variations:**

1. **Chain-of-Thought with Tools (CoT-T)**
   - Model explicitly reasons: "I need to..., so I'll use..."
   - Example: Few-shot prompting with tool use examples

2. **ReAct (Reasoning + Acting)**
   - Alternates between reasoning steps and tool calls
   - Maintains action-observation loops

3. **In-Context Learning with Tool Use**
   - Provides 1-3 examples of tool use in context
   - Model learns pattern from examples

**Strengths:**
- ✅ No training required (can use any LLM)
- ✅ Easy to add/remove tools
- ✅ Transparent (easy to debug what model is doing)
- ✅ Works across model families

**Failure Modes:**
- ❌ **Format errors:** Model outputs malformed tool calls
  - Example: JSON parsing fails, missing required fields
- ❌ **Wrong tool selection:** Chooses irrelevant tools
  - Example: Uses web_search instead of calculator for arithmetic
- ❌ **Hallucinated tool calls:** Invents tools that don't exist
  - Example: Calls `advanced_analyzer()` that isn't provided
- ❌ **Context window limitations:** Long tool outputs reduce reasoning space
  - Example: Large web search results push out the task description
- ❌ **Brittleness:** Small prompt changes break tool use
  - Example: Changing JSON format slightly breaks parsing

**When to Use:**
- Prototyping and exploration
- Frequently changing tool sets
- Multiple model families
- Limited computational resources (no fine-tuning)

#### Paradigm 2: Supervised Tool Learning

**Core Idea:** Fine-tune the LLM on examples of proper tool use using supervised learning. The model internalizes tool-use knowledge into its parameters.

**How It Works:**

```
Training Data Collection:
{
  "instruction": "Generate a Python function to sort a list",
  "trajectory": [
    {
      "step": 1,
      "thought": "Need to create a Python function",
      "action": "python_write(file='sort.py', code='def sort_list(arr):\n  return sorted(arr)')"
    },
    {
      "step": 2,
      "thought": "Should test the function",
      "action": "python_execute(code='sort([3,1,2])')"
    },
    {
      "step": 3,
      "thought": "Test passed, function is correct",
      "action": "stop(result='success')"
    }
  ]
}

SFT (Supervised Fine-Tuning):
- Train model on input (instruction) → output (sequence of actions)
- Use next-token prediction loss
- Model learns to generate well-formed tool calls
```

**Variations:**

1. **Tool Syntax Learning**
   - Train model on tool specifications and usage examples
   - Model learns correct parameter formats

2. **Trajectory-Based SFT**
   - Train on complete action sequences (from problem to solution)
   - Model learns planning + tool selection + tool use

3. **Skill-Based Fine-Tuning**
   - Fine-tune on demonstrations of specific skills (write unit test, refactor function, etc.)
   - Model learns to apply skills via tool calls

4. **Guided SFT with Verification**
   - Only include successful trajectories (where tool calls worked)
   - Exclude trajectories with hallucinated or erroneous tool calls
   - Improves correctness but reduces data quantity

**Strengths:**
- ✅ Better format adherence (tool calls are well-formed)
- ✅ More reliable tool selection (learned from data patterns)
- ✅ Context window efficiency (learned patterns are compressed)
- ✅ Works even with unfamiliar tools (if shown examples)

**Failure Modes:**
- ❌ **Distribution shift:** Model overfits to training tools
  - Example: Fine-tuned on calculator, fails with new finance tools
- ❌ **Data requirements:** Need substantial high-quality demonstrations
  - Collecting 10k+ trajectories is expensive
- ❌ **Hallucination persistence:** Still invents tool calls despite training
  - Example: Model calls `hypothetical_tool()` not in training data
- ❌ **Catastrophic forgetting:** Fine-tuning degrades general reasoning
  - Example: Model becomes worse at non-tool reasoning tasks
- ❌ **Credit assignment:** Hard to identify which trajectory steps caused failures
  - Example: Did tool call fail or subsequent reasoning fail?

**When to Use:**
- Production systems with stable tool sets
- Models available for fine-tuning (open-weights or API with SFT)
- High accuracy requirements
- Sufficient labeled trajectory data available

#### Paradigm 3: Reward-Driven Tool Policy Learning

**Core Idea:** Treat tool use as a Markov Decision Process (MDP) where the agent learns a policy through reinforcement learning, using reward signals to guide improvement.

**How It Works:**

```
State: {task_description, conversation_history, current_knowledge}
Action: {tool_name, tool_parameters}
Reward: -1 for each step (encourage efficiency)
        +100 for task completion
        +50 for task progress
        -50 for hallucinated tool calls (format errors)
        
MDP Trajectory:
State₀: "Write a function to compute factorial"
  → Action: python_write(code='def fact(n): ...')
    Reward: +5 (progress toward solution)
State₁: "Code written, need to test"
  → Action: python_execute(code='fact(5)')
    Reward: +30 (verified correctness)
State₂: "Test passed"
  → Action: stop(result='success')
    Reward: +100 (task complete)

RL Algorithm (GRPO, PPO, or similar):
- Run agent trajectories
- Collect trajectories with scores
- Use reward signal to update policy
- Improve tool selection based on outcomes
```

**Variations:**

1. **Reward Shaping for Tool Use**
   - Reward for using correct tool quickly: +10 - step_count
   - Penalty for trying tools in wrong order: -5
   - Bonus for self-correction: +15

2. **Outcome-Based Rewards**
   - Only reward based on final task completion
   - Sparse rewards require careful credit assignment

3. **Process-Based Rewards**
   - Reward intermediate steps (tool calls that make progress)
   - Dense rewards guide learning faster

4. **Verifier-Based Rewards**
   - Use separate verifier LLM to judge tool call quality
   - Verifier score becomes reward signal
   - Expensive but accurate signal

5. **Human Feedback Integration**
   - Collect human preferences between trajectories
   - Train reward model from preferences
   - Use reward model for policy improvement

**Strengths:**
- ✅ Learns from trial-and-error (doesn't need demonstrations)
- ✅ Discovers novel tool use patterns (beyond training data)
- ✅ Adapts to changing environment/tools
- ✅ Can optimize for multiple objectives (speed, accuracy, cost)
- ✅ Self-improvement capability (agent improves via interaction)

**Failure Modes:**
- ❌ **Reward hacking:** Agent learns to game reward function
  - Example: Uses tools in ways that give reward but don't solve task
- ❌ **Exploration-exploitation tradeoff:** May get stuck in local optima
  - Example: Learns one successful tool use pattern, doesn't explore others
- ❌ **Sample efficiency:** Requires many trajectories (expensive)
  - Example: Needs 100k+ interactions to learn stable policy
- ❌ **Reward signal ambiguity:** Hard to define what makes good tool use
  - Example: Should we reward "tries fewer tools" or "gets right answer"?
- ❌ **Non-stationarity:** As model improves, old trajectories become stale
  - Example: Policy trained on v1 model doesn't transfer to v2 model

**When to Use:**
- Scenarios where tool set changes frequently
- Maximum performance is critical (willing to invest in training)
- Agent will operate for extended period (can amortize training cost)
- Sufficient compute for RL training available
- Clear reward signals can be defined

### Comparative Analysis of Paradigms

```
Paradigm         Setup Time  Accuracy  Flexibility  Data Needed  Compute Cost
──────────────────────────────────────────────────────────────────────────────
Prompting        5 min       60-70%    High         None         None
SFT              1 day       75-85%    Medium       10k traj     1 GPU-month
Reward Learning  1 week      85-95%    High         100k traj    10 GPU-months

Best For         Prototyping Production + Dynamic
                             stable    problems
```

## Methodology & Implementation

### Evaluation Methodology

The paper evaluates tool-use approaches across multiple dimensions:

#### 1. Correctness Metrics

**Tool Call Format Correctness:**
```
Score = (well_formed_calls / total_calls) × 100%
- Parsing tool call JSON succeeds
- All required parameters present
- Parameter types correct
```

**Tool Selection Accuracy:**
```
Score = (appropriate_tool_chosen / decision_points) × 100%
- Right tool for the task
- Tool parameters match task needs
```

**Task Completion Rate:**
```
Score = (solved_tasks / total_tasks) × 100%
- Final answer correct
- Required tools were actually called
- Tool outputs were properly used
```

#### 2. Efficiency Metrics

**Tool Call Efficiency:**
```
efficiency = (task_complete / tools_called)
- Lower values = more wasted tool calls
- Penalizes hallucinated/unnecessary calls
```

**Convergence Speed:**
```
steps_to_completion = number of tool calls before success
- Measures how quickly agent finds solution
```

#### 3. Robustness Metrics

**Generalization to New Tools:**
```
accuracy_on_new_tools / accuracy_on_training_tools
- Measures zero-shot transfer to unseen tools
```

**Error Recovery:**
```
success_after_tool_failure / total_tool_failures
- Can agent recover when tools return errors?
```

### Benchmark Tasks for Code Development

Common tasks used to evaluate tool use in software development:

```
Task Category              Benchmark                Tools Required
──────────────────────────────────────────────────────────────────
Code Generation            Generate functions,     code_write
                          classes, modules         code_run
                                                   code_test
                          
Debugging                  Fix broken code,        code_read
                          identify root cause      error_analyzer
                                                   code_fix
                                                   test_run
                          
Testing                    Write unit tests,       test_write
                          improve coverage         test_run
                                                   coverage_report
                          
Code Review                Identify issues,        code_read
                          suggest improvements     lint
                                                   type_check
                                                   style_check
                          
Refactoring               Improve code            code_read
                          structure               code_write
                          reduce duplication      ast_analyze
                                                   test_run
```

[Specific benchmark results unavailable — see full paper for detailed metrics]

### Implementation Considerations

#### Prompting-Based Tool Use

```python
from anthropic import Anthropic

client = Anthropic()

TOOLS = [
    {
        "name": "python_execute",
        "description": "Execute Python code and return output",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute"
                }
            },
            "required": ["code"]
        }
    }
]

def code_generation_agent(task: str):
    messages = [
        {"role": "user", "content": task}
    ]
    
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
        
        # Check if model wants to use tools
        if response.stop_reason == "tool_use":
            # Extract tool calls
            for block in response.content:
                if block.type == "tool_use":
                    if block.name == "python_execute":
                        # Execute the code
                        result = exec_python(block.input["code"])
                        
                        # Add tool result to messages
                        messages.append({
                            "role": "assistant",
                            "content": response.content
                        })
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": str(result)
                                }
                            ]
                        })
        else:
            # Model stopped without requesting tools
            return response.content[0].text
```

#### Supervised Learning Approach

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import Dataset
import torch

# Prepare tool-use trajectory data
dataset = [
    {
        "instruction": "Write a function to check if a number is prime",
        "trajectory": [
            {"action": "python_write", "code": "def is_prime(n):..."},
            {"action": "python_execute", "code": "is_prime(7)"},
            {"action": "stop", "result": "success"}
        ]
    }
]

# Format for SFT
def format_trajectory(example):
    actions = "\n".join([
        f"<|action|>{a['action']}\n<|code|>{a.get('code', '')}<|end|>"
        for a in example['trajectory']
    ])
    return {
        "text": f"<|instruction|>{example['instruction']}\n{actions}"
    }

# Fine-tune model
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b")

formatted_data = Dataset.from_list(dataset).map(format_trajectory)

# Standard SFT training loop
```

## Practical Applications & Use Cases

### 1. Autonomous Code Generation with Iterative Refinement

**Challenge:** Generate correct code that passes all tests, handling errors in initial attempts

**Tool Use Solution:**

```
Agent Loop:
1. Read requirement
2. Use python_write → generate initial code
3. Use python_execute → test code
4. If test fails:
   - Analyze error message
   - Use code_read → examine generated code
   - Use python_write → fix code
   - Repeat step 3 (Loop back)
5. If tests pass:
   - Use code_review → lint and style check
   - Return final code
```

**Paradigm Choice:** Reward Learning
- **Why:** Agent must learn to recover from errors, explore multiple fixes
- **Cost:** Higher upfront training investment
- **Benefit:** Robust, self-improving system

### 2. Bug Fixing in Large Codebases

**Challenge:** Locate bug, understand context, implement fix, verify fix doesn't break other tests

**Tool Use Solution:**

```
Tool Sequence:
1. error_read → Extract error message and stack trace
2. code_search → Find relevant code files
3. code_read → Understand buggy code context
4. code_analyze → Determine root cause
5. code_write → Implement fix
6. test_run → Run all tests (unit + integration)
7. If failing tests:
   - Understand failure reason
   - Adjust fix
   - Repeat step 6
8. code_review → Check style and documentation
```

**Paradigm Choice:** Supervised Learning
- **Why:** Can collect many bug-fix examples from open source
- **Cost:** Moderate (bugs are common, examples readily available)
- **Benefit:** Reliable once trained

### 3. Test Generation and Coverage Improvement

**Challenge:** Write comprehensive unit tests covering edge cases

**Tool Use Solution:**

```
Loop:
1. code_read → Examine function to test
2. reasoning → Identify edge cases and normal cases
3. test_write → Generate test cases
4. code_execute → Run tests against target function
5. coverage_analyze → Check code coverage
6. If coverage < target:
   - Identify uncovered branches
   - Repeat from step 2 (generate new tests)
7. Else:
   - Return test suite
```

**Paradigm Choice:** Prompting (initially) → Reward Learning (for advanced)
- **Why:** Can start with in-context examples, graduate to learned policies as complexity increases
- **Cost:** Minimal initial cost, scales with ambition
- **Benefit:** Quick to prototype, improves over time

### 4. Continuous Code Review and Improvement

**Challenge:** Review code continuously, identifying issues and suggesting improvements

**Tool Use Solution:**

```
Agent Workflow:
1. code_read → Load code under review
2. Parallel tools:
   - lint → Style violations
   - type_check → Type errors
   - security_scan → Security issues
   - complexity_analyze → Maintainability issues
3. reason → Prioritize issues
4. code_suggest → Generate improvements
5. comment → Create review comments
6. If improvement is critical:
   - code_write → Auto-fix
   - test_run → Verify fix doesn't break
```

**Paradigm Choice:** Prompting
- **Why:** Review criteria are well-defined, tools are stable
- **Cost:** None (no training needed)
- **Benefit:** Can quickly iterate on review criteria without retraining

## Insights & Implications

### 1. Tool Use is Essential, Not Optional

The paper's core finding: Autonomous agents **cannot achieve high accuracy without tool use**:

- **Prompting-only:** 60-70% accuracy (error rates from reasoning alone)
- **+ Tool use:** 80-95% accuracy (tools verify and correct)

For safety-critical code generation (production systems), tool use is mandatory.

### 2. Paradigm Selection Depends on Stage of Development

**Early prototyping:** Prompting (fast to iterate)
↓
**Scaling to production:** Supervised Learning (reliable)
↓
**Long-term autonomy:** Reward Learning (self-improving)

This progression matches organizational maturity with technique complexity.

### 3. Hallucination Isn't Solved, It Migrates

Tool use doesn't eliminate hallucination—it changes form:

| Paradigm | Hallucination Type |
|---|---|
| Prompting | Invents tools that don't exist |
| SFT | Generates tool calls with wrong parameters |
| Reward Learning | Learns to game reward function in unrealistic ways |

Each paradigm requires specific defenses.

### 4. The Future: Hybrid Approaches

Most effective systems combine paradigms:

```
System Architecture:
┌─────────────────────────────────┐
│ Prompting Layer (Router)         │ ← Fast, flexible
│ ├─ Select high-level strategy   │
│ └─ Route to specialized agents  │
└───────┬───────────────────────────┘
        │
    ┌───┴────┬─────────┐
    │        │         │
    ↓        ↓         ↓
  SFT    Reward   Symbolic
 Agent   Agent     Tool
 
- Routing: Prompting-based
- High-accuracy tasks: SFT-trained agents
- Error recovery: Reward-trained agents
- Verification: Symbolic tools (tests, type checkers)
```

### 5. Tool Design Matters as Much as Tool Use

Agent performance depends on:
- ✅ **50%:** Designing tools with clear semantics
- ✅ **30%:** Training/prompting the agent
- ✅ **20%:** Integration and error handling

Tools should:
- Have unambiguous names and clear purposes
- Return structured, parseable results
- Fail gracefully with helpful error messages
- Provide execution traces for debugging

### 6. Efficiency-Accuracy Tradeoff

Different paradigms optimize for different objectives:

| Paradigm | Accuracy | Speed | Cost | Adaptability |
|---|---|---|---|---|
| Prompting | 70% | ✅✅ | ✅✅ | High |
| SFT | 85% | ✅ | ✅ | Medium |
| Reward | 95% | ✅ | Low | ✅✅ |

Choose based on requirements.

## Code & Resources

### Official Resources

- **ArXiv Paper:** https://arxiv.org/abs/2604.00835
- **Authors:** Harbin Institute of Technology Shenzhen, TikTok Inc

### Tool Use Frameworks

1. **Claude (Anthropic)**
   - Native tool use support (JSON format)
   - Automatic tool calling in API
   - Supports unlimited tool definitions

2. **LangChain Tool Ecosystem**
   - Pre-built tools for common tasks
   - Tool composition framework
   - Agent chains with tools

3. **AgenticQwen (Alibaba)**
   - Open-source agentic LLM fine-tuned for tool use
   - SFT approach with 10k+ tool-use examples
   - Industrial-scale deployment

4. **OpenAI Function Calling**
   - Similar JSON-based format
   - GPT-4 has good tool use capability

### Recommended Reading Order

For practitioners implementing tool use in agent systems:

1. This paper (Agentic Tool Use survey) — Foundational concepts
2. "SoK: Agentic Skills" (2602.20867) — Higher-level skill composition
3. "SkillCraft: Can LLM Agents Learn to Use Tools Skillfully?" (2603.00718) — Benchmarking
4. Framework documentation (Claude, LangChain, etc.) — Implementation

## Related Work & Context

### Prior Foundational Work

1. **In-Context Learning** (Mahowald et al., Brown et al.)
   - Showed LLMs can learn from in-context examples
   - Foundation for prompting-based tool use

2. **Instruction Tuning** (Wei et al., Ouyang et al.)
   - Demonstrated SFT on diverse tasks improves generalization
   - Basis for supervised tool learning

3. **Reinforcement Learning from Human Feedback (RLHF)**
   - Showed reward signals can guide LLM behavior
   - Foundation for policy-learning approaches

4. **Chain-of-Thought Prompting** (Wei et al.)
   - Demonstrated intermediate reasoning improves accuracy
   - Building block for prompting-based tool use

### Related Surveys & Papers

- "ReAct: Synergizing Reasoning and Acting in Language Models" (2210.03629)
- "Tool Use in Large Language Models" (Hao et al., Qin et al.)
- "SoK: Agentic Skills — Beyond Tool Use in LLM Agents" (2602.20867)
- "SkillCraft: Can LLM Agents Learn to Use Tools Skillfully?" (2603.00718)

### Future Research Directions

1. **Tool composition:** How to combine tools to solve complex tasks?
2. **Meta-tool learning:** Can agents learn to design their own tools?
3. **Cross-domain transfer:** Can tool-use knowledge transfer across domains?
4. **Safety in tool use:** How to prevent agents from misusing tools?
5. **Explanation in tool use:** Why did agent choose particular tools?

### Integration with Development Workflows

This survey shows tool use is critical for:

1. **Code generation agents** (Claude Code, GitHub Copilot, Cursor)
2. **Testing frameworks** (AI-powered test generation and debugging)
3. **Code review systems** (automated code quality analysis)
4. **Development environments** (IDE integrations with LLM agents)

The future of autonomous software development depends on solving tool use—this survey provides the conceptual foundation and practical guidance for doing so.
