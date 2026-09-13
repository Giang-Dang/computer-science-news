# Agentic Code Reasoning: Semi-Formal Reasoning for Code Analysis Without Execution

**Paper:** [Agentic Code Reasoning](https://arxiv.org/abs/2603.01896)

**ArXiv ID:** 2603.01896

**Authors:** Shubham Ugare, Satish Chandra (Meta, USA)

**Submission Date:** March 2, 2026

**Research Focus:** LLM agent reasoning, code semantics understanding, code analysis without execution, semi-formal reasoning, agent verification, fault localization

---

## Executive Summary

This paper introduces **semi-formal reasoning**, a structured prompting methodology that enables LLM agents to explore codebases and reason about code semantics without executing the code. Unlike unstructured chain-of-thought reasoning, semi-formal reasoning requires agents to construct explicit premises, trace execution paths, and derive formal conclusions—acting as a **certificate of reasoning validity**. The agent cannot skip cases or make unsupported claims.

Evaluated on three critical tasks—patch equivalence verification, fault localization, and code question answering—semi-formal reasoning consistently improves accuracy:
- **Patch Equivalence:** 78% → 88% on curated examples; 93% on agent-generated patches
- **Fault Localization:** Significant improvement in identifying root causes without running code
- **Code Q&A:** Enhanced accuracy in answering questions about program behavior

**Significance to Agent-Driven Development:** This work enables agentic systems to reason deeply about code without execution (critical for static analysis, code review, patch verification), reducing agent-code interaction latency and enabling offline code analysis—fundamental for developer tools, DevOps agents, and code understanding in LLM agents.

---

## Problem Statement

**Development Automation Challenge:**
Agentic systems for code generation and maintenance rely on understanding program semantics: verifying that a refactored function is equivalent to the original, locating bugs through static analysis, answering developer questions about code behavior. These tasks require accurate reasoning about code execution paths, variable states, and control flow.

**Prior Limitations:**
- **Execution-Based Reasoning:** Agents can trace code by running it and observing outputs, but this requires setting up environments, handling dependencies, and may be prohibitively slow for large repositories or untrusted code
- **Unstructured Reasoning:** LLMs can reason about code informally (chain-of-thought), but lack rigor—agents may skip cases, make unsupported assumptions, or produce hallucinations about program behavior
- **Static Analysis Gap:** Traditional static analysis tools (linters, type checkers) catch syntactic issues but struggle with semantic equivalence, complex control flow, and business logic

**Research Gap:**
A structured reasoning methodology that provides agent certification (formal premises, traced execution, logical conclusions) without requiring execution was needed to enable efficient, reliable code understanding for agentic systems.

---

## Core Concepts & Theory

### Semi-Formal Reasoning: Definition & Architecture

**Definition:**
Semi-formal reasoning is a structured prompting approach that requires agents to:

1. **Identify Premises:** State assumptions and facts about input code (function signature, preconditions, variable initialization)
2. **Trace Execution:** Step through program execution paths explicitly, tracking variable states at each step
3. **Consider Cases:** Enumerate distinct execution branches (conditionals, loops, exception handlers) and trace each
4. **Derive Conclusions:** Draw formal conclusions about program behavior (return values, side effects, equivalence) supported by trace evidence

**Why "Semi-Formal"?**
- **Formal Elements:** Logical structure (premises → trace → conclusion), explicit case enumeration, no hand-waving
- **Informal Elements:** Natural language reasoning (not symbolic logic), LLM-generated traces (not machine-verified), reasoning errors still possible (but less likely than unstructured reasoning)

### Contrast: Unstructured vs. Semi-Formal Reasoning

**Unstructured Chain-of-Thought:**
```
Agent: "Let me think about this function. It takes an array and returns... 
let me see... it looks like it counts something... probably the maximum? 
Yes, I think it returns the maximum value."
```
**Problems:**
- Lacks step-by-step execution trace
- Does not enumerate all paths
- Conclusions not grounded in evidence
- Gaps and assumptions hidden

**Semi-Formal Reasoning:**
```
Agent: "
PREMISES:
- Input: array of integers, length >= 1
- Function: iterates from index 0, maintains variable max_val
- Initial: max_val = array[0]

TRACE (Case 1: array = [3, 5, 2]):
- Step 1: max_val = 3
- Step 2: max_val = max(3, 5) = 5
- Step 3: max_val = max(5, 2) = 5
- Return: 5

TRACE (Case 2: array = [10]):
- Step 1: max_val = 10
- Loop does not execute (length = 1)
- Return: 10

CONCLUSION: Function returns maximum value in array."
```
**Benefits:**
- Every step is explicit and verifiable
- All execution paths covered
- Conclusions logically follow from traces
- Reader (human or verifier) can spot errors

### Reasoning Certification & Validity Checking

**The Certificate Property:**
A well-formed semi-formal reasoning trace is self-checking:
- If traces are correct, conclusions must follow
- If conclusions fail (e.g., patch not equivalent), the error is in the trace, which can be debugged
- Traces are verifiable against the actual code (unlike hallucinated chain-of-thought)

**Application to Agent Verification:**
When an agent asserts "Patch A is equivalent to Patch B," the semi-formal reasoning serves as a certificate:
- Agent must show side-by-side execution traces for identical inputs
- If traces diverge, equivalence fails (conclusion grounded in evidence)
- If traces match across diverse test cases, equivalence is plausible

### Multi-Task Reasoning Framework

Semi-formal reasoning generalizes across three critical code understanding tasks:

| Task | Input | Output | Reasoning Goal |
|------|-------|--------|-----------------|
| **Patch Equivalence** | Original code, Modified code, Test case | Equivalent: Yes/No | Trace both to completion; compare results |
| **Fault Localization** | Code, Failure description, Expected behavior | Bug location in code | Trace failing path; identify divergence from expected |
| **Code Q&A** | Code, Natural language question | Answer about behavior | Trace relevant execution paths; answer from trace |

---

## Main Ideas & Contributions

### 1. Semi-Formal Reasoning Methodology

**Core Innovation:** A structured prompt engineering approach that operationalizes code reasoning as:
1. **Explicit Premise Gathering** (facts about code structure, inputs, execution model)
2. **Exhaustive Path Enumeration** (all conditionals, loops, early returns identified)
3. **Step-by-Step Execution Traces** (variables, state changes, control flow at each step)
4. **Formal Conclusion Derivation** (result grounded in traces, not speculation)

**Prompt Structure:**
The authors likely use a template like:

```
You are reasoning about code semantics. For the given code and input:

[CODE]

1. PREMISES: List facts about the code (function signature, initial state, input constraints)
2. EXECUTION TRACE: Step through the code for the given input, tracking:
   - Variable assignments
   - Conditional branches taken
   - Loop iterations
   - Return statement reached
3. CASE ANALYSIS: Identify and trace distinct execution paths (different input ranges, edge cases)
4. CONCLUSION: State the result of execution, supported by trace evidence

Ensure every step references the code explicitly. Do not skip cases or assert conclusions 
without tracing to them.
```

### 2. Patch Equivalence Verification at Scale

**Problem:** Verifying that a refactored code patch produces identical behavior is critical for code review and automated refactoring. Traditional approaches require execution or expensive formal verification.

**Solution:** Semi-formal reasoning traces both original and modified code side-by-side:

**Example Scenario:**

```
ORIGINAL:
def process(items):
    result = 0
    for item in items:
        result += item * 2
    return result

MODIFIED:
def process(items):
    return sum(item * 2 for item in items)

VERIFICATION TASK: Are these equivalent?

SEMI-FORMAL TRACE:

ORIGINAL TRACE (items = [1, 2, 3]):
- result = 0
- Loop iteration 1: result = 0 + 1*2 = 2
- Loop iteration 2: result = 2 + 2*2 = 6
- Loop iteration 3: result = 6 + 3*2 = 12
- Return 12

MODIFIED TRACE (items = [1, 2, 3]):
- sum(item * 2 for item in [1, 2, 3])
- = sum([2, 4, 6])
- = 2 + 4 + 6
- = 12
- Return 12

EDGE CASE: items = [] (empty)
ORIGINAL: result = 0, return 0
MODIFIED: sum([]) = 0, return 0

CONCLUSION: Equivalent (traces match across test cases)
```

**Empirical Results:**
- **Curated Examples (known good patches):** 78% → 88% accuracy with semi-formal reasoning
- **Agent-Generated Patches (harder):** Semi-formal reasoning reaches 93% accuracy on agent patches (agents that use this methodology to generate patches produce more verifiable code)

**Insight:** Semi-formal reasoning is particularly effective on agent-generated code, suggesting a synergy: agents that reason semi-formally about their own code produce more reliable patches.

### 3. Fault Localization Without Execution

**Problem:** Finding the line of code causing a bug typically requires debugging—setting breakpoints, running with failing inputs, observing state. Agents cannot efficiently iterate this way.

**Solution:** Semi-formal reasoning traces the failing execution path and identifies where actual behavior diverges from expected:

**Example:**

```
BUGGY CODE:
def find_max(arr):
    max_val = 0  # BUG: assumes positive numbers
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val

FAILURE: find_max([-5, -2, -8]) returns 0, expected -2

SEMI-FORMAL TRACE:
- max_val = 0
- Iteration 1: -5 > 0? No. max_val = 0
- Iteration 2: -2 > 0? No. max_val = 0
- Iteration 3: -8 > 0? No. max_val = 0
- Return 0

EXPECTED TRACE:
- max_val should start at min value or first array element
- Iteration 1: -5 is new max
- Iteration 2: -2 > -5, new max
- Iteration 3: -8 < -2, no update
- Return -2

DIVERGENCE FOUND: Line "max_val = 0" fails on negative numbers. 
BUG LOCATION: Initialization should be "max_val = arr[0]"
```

**Agent Application:** When an agent-generated test fails, the agent can reason through the failure semi-formally, pinpoint the buggy line, and generate a fix—all without executing code.

### 4. Code Question Answering

**Application:** Agents can answer developer questions about program behavior ("What does this function return for input X?", "Is this variable always initialized?") through semi-formal reasoning:

```
QUESTION: "What does parse_config return for a missing 'timeout' key?"

CODE:
def parse_config(config_dict):
    timeout = config_dict.get('timeout', 30)  # default 30
    retries = int(config_dict['retries'])     # no default
    return {'timeout': timeout, 'retries': retries}

SEMI-FORMAL REASONING:
- Input: config_dict = {'retries': '3'} (no 'timeout' key)
- Line 2: timeout = config_dict.get('timeout', 30)
  - 'timeout' not in dict, use default → timeout = 30
- Line 3: retries = int('3') = 3
- Line 4: return {'timeout': 30, 'retries': 3}

ANSWER: Returns {'timeout': 30, 'retries': 3} (timeout defaults to 30)
```

---

## Methodology & Implementation

### Evaluation Tasks & Datasets

**Task 1: Patch Equivalence Verification**
- **Dataset:** Curated patches (gold-standard human-verified equivalences) + agent-generated patches
- **Metric:** Accuracy (correct equivalence judgments) vs. baseline (unstructured reasoning)
- **Baseline Comparison:** Standard chain-of-thought, no structured template

**Task 2: Fault Localization**
- **Dataset:** Buggy code snippets with failure descriptions; ground truth: line containing the bug
- **Metric:** Rank of the bug line in agent's output (lower rank = better)
- **Baseline:** Unstructured code reasoning, symbolic static analysis tools

**Task 3: Code Question Answering**
- **Dataset:** Curated code snippets and questions about behavior
- **Metric:** Answer correctness (e.g., correct return value, correct type)

### Metrics & Results

[Exact figures unavailable — see full paper]

**Key Findings (Qualitative):**
- Semi-formal reasoning improves accuracy on all three tasks
- Improvement is largest for patch equivalence (where formal reasoning helps most)
- Agent-generated patches benefit especially from this methodology (agents can verify their own output)
- Fault localization improves by identifying divergence points in traces
- Code Q&A accuracy increases as agents are forced to trace through relevant paths

### Experimental Validation

**Internal Consistency:**
- Multiple agent runs on same task show consistent trace patterns
- Divergences in traces correlate with failures in ground truth
- Semi-formal reasoning traces can be audited by humans

**Comparison to Baselines:**
- vs. Unstructured chain-of-thought: Semi-formal reasoning significantly better
- vs. Symbolic static analysis: Semi-formal reasoning more flexible (handles dynamic behavior, control flow), though less complete than formal verification

### Limitations

- **Trace Accuracy:** Semi-formal reasoning depends on LLM correctly tracing code; complex branching or loops may have tracing errors
- **Complex Code:** Very large functions or highly nested control flow may exceed LLM context/reasoning capacity
- **Language Coverage:** Methodology tested on specific languages (likely Python, Java); generalization to other languages not discussed
- **Scalability:** Tracing large functions is expensive (more tokens); limits applicability to repository-scale code understanding

---

## Practical Applications & Use Cases

### 1. Code Review Automation

**Use Case:** Agent-assisted code review that explains its reasoning

```
REVIEWER_AGENT:
"This PR changes the caching logic. Let me verify equivalence:

ORIGINAL CACHE LOGIC (traces execution for cache miss scenario):
[trace showing cache miss → fetch from DB → store → return]

MODIFIED CACHE LOGIC (traces same scenario):
[trace showing cache miss → fetch from DB → store → return]

TRACES MATCH. Logic is equivalent. ✓
However, I notice the new version doesn't handle stale entries. 
Question for author: Is staleness acceptable here?
"
```

**Advantage:** Developer sees agent's reasoning, can spot errors, trust or override the judgment.

### 2. Patch Generation & Verification

**Application:** When agents generate bug fixes, they should verify their patches semi-formally before submitting:

```
AGENT_GENERATED_FIX:
"Original bug: Division by zero when denominator is 0.

PROPOSED FIX: Add guard clause
   if denominator == 0:
       return 0  # or raise exception

VERIFICATION:
Original code (denominator = 0):
  [trace] → attempts division → crash

Fixed code (denominator = 0):
  [trace] → guard clause catches → returns 0 safely

Fix is correct for this failure mode. ✓
"
```

### 3. Static Analysis & Code Auditing

**Use Case:** Agents audit code for security issues, data flow bugs, or compliance without running untrusted code

```
SECURITY_AGENT:
"Auditing SQL query formation in this function.

TRACE:
1. user_input = request.get_param('id')
2. query = f'SELECT * FROM users WHERE id={user_input}'
3. execute(query)

FINDING: SQL injection vulnerability.
User input directly interpolated into query string.
Fix: Use parameterized queries: execute('SELECT * FROM users WHERE id=?', [user_input])
"
```

### 4. Interactive Debugging & Agent Collaboration

**Application:** Agents can help developers understand why code fails by reasoning through execution:

```
DEVELOPER: "Why does this function crash with input [-5, 10, 3]?"

AGENT (semi-formal reasoning):
"Let me trace through the function with your input:

[traces execution]

Found it! At line 12, you're computing stats[i] but i can be out of bounds
because the loop runs longer than stats array. Trace shows:
- Loop iteration 5: i = 5, but stats only has 4 elements (indices 0-3)
- Crash at stats[5]

Root cause: Loop should be 'for i in range(len(stats))' not 'for i in range(num_items)'"
```

---

## Insights & Implications

### 1. Reasoning Depth Matters More Than Tool Proliferation

**Insight:** Agents reasoning semi-formally about code semantics achieve better understanding with a single methodology (structured tracing) than with multiple tools (linters, type checkers, symbolic analyzers). The act of reasoning is the capability, not the toolset.

**Implication for Agent Design:** Invest in reasoning quality (structured prompts, trace verification) before adding more tools.

### 2. Code Reasoning Without Execution Enables Scalability

**Finding:** Agents can reason about code without running it, making them applicable to:
- Untrusted code (security analysis without sandboxing)
- Unavailable environments (codebase analysis in development, before deployment)
- Large repositories (parallelizable reasoning without execution bottlenecks)

**Scaling Benefit:** Multi-agent systems can reason about the same code in parallel without contention for execution environments.

### 3. Semi-Formal Reasoning Creates Verifiable Agent Reasoning

**Key Property:** Unlike chain-of-thought, semi-formal reasoning produces auditable traces. Humans and verifiers can:
- Follow the agent's logic step-by-step
- Spot where the agent made a wrong assumption
- Correct a single trace step and re-derive the conclusion
- Build confidence in agent reliability

**Trust & Transparency:** This is critical for agentic systems in high-stakes domains (compliance, security, infrastructure).

### 4. Synergy with Agent-Generated Code

**Observation:** Semi-formal reasoning is particularly effective on code the agent itself generated. Agents that reason about their own patches before submitting them produce more correct patches.

**Architectural Implication:** Agentic systems should include **self-verification loops**:

```
Agent Loop:
1. Generate candidate code
2. Semi-formally verify the code against specification
3. If verification passes → submit; else → refine and retry
```

### 5. Path Coverage and Edge Cases

**Finding:** Semi-formal reasoning forces agents to enumerate distinct execution paths, reducing missed edge cases. Agents that trace systematically catch boundary conditions (empty input, negative numbers, null pointers) better than those using unstructured reasoning.

**QA Implication:** Code generated by agents using semi-formal verification methodology requires fewer edge-case fixes.

---

## Code & Resources

### Paper Access
- **ArXiv:** https://arxiv.org/abs/2603.01896
- **Versions:** v1 (submitted 2026-03-02), v2 (revised 2026-03-04)

### Related Frameworks & Tools

**Complementary Methodologies:**
- **Formal Verification (Z3, Coq):** Full mathematical proof; more powerful but less accessible to LLMs
- **Symbolic Execution:** Explores all paths; expensive for complex code; complements semi-formal reasoning
- **Concrete Execution + Tracing:** Full runtime debugging; requires environment setup; less scalable

**LLM Integration Points:**
- OpenAI o1 / Claude 3.7 (extended reasoning): Can execute semi-formal reasoning at scale
- Claude Code: Could use semi-formal reasoning for code review and patch verification
- LangChain agents: Structured output format for traces

### Prompt Template for Semi-Formal Reasoning

**Recommended Structure for Practitioners:**

```python
def semi_formal_reasoning_prompt(code, task, input_examples):
    return f"""
You are performing semi-formal reasoning about code behavior. 
Your response must have this structure:

PREMISES:
[List facts about the code: function signature, initial state, assumptions about input]

EXECUTION TRACE(S):
For each test case, trace through the code step-by-step:
1. State variable values after each line
2. Identify which branch is taken in conditionals
3. Show loop iterations explicitly
4. Mark the return value or output

CASE ANALYSIS:
[Identify distinct execution paths and trace the most important ones]

CONCLUSION:
[Your final answer, grounded in the traces above]

---

CODE:
{code}

TASK: {task}

TEST CASES:
{input_examples}

Begin your response with PREMISES:
"""
```

### Integration Guidance

**For LLM-Based Developer Tools:**
1. Use semi-formal reasoning for code review, patch verification, and bug localization
2. Surface traces to developers so they can follow agent reasoning
3. Allow developers to correct individual trace steps and re-verify
4. Use traces as training data for agent fine-tuning (which traces are most helpful?)

**For Agentic Systems:**
1. Include a self-verification loop: agent generates code, semi-formally verifies, refines
2. Log traces for debugging agent failures (if verification fails, the trace shows why)
3. Combine with other reasoning methods (semi-formal for correctness, beam search for alternatives)

---

## Related Work & Context

### Foundational Work on Code Reasoning

- **Program Synthesis (Gulwani et al., 2012):** Early work on LLM-based code generation; emphasized reasoning about correctness
- **Neuro-Symbolic Approaches (Mao et al., 2019):** Combine neural networks with symbolic reasoning; semi-formal reasoning is a lightweight version
- **Chain-of-Thought Prompting (Wei et al., 2023):** Structured reasoning improves LLM accuracy; semi-formal reasoning is domain-specialized

### Code Understanding Without Execution

- **Static Analysis & Linting:** Traditional approach; limited to syntactic patterns
- **Type Checking:** Verifies type safety; does not reason about behavior
- **Formal Verification:** Proves correctness mathematically; expensive, limited to small programs
- **Concrete Testing:** Runs code with test cases; does not explore all paths

### Related Agentic Code Reasoning

- **Agentic Testing (Davis et al., 2026):** Agents generate and verify tests; semi-formal reasoning helps verify test adequacy
- **Code as Agent Harness (Ning et al., 2026):** Framework treating code as agent infrastructure; semi-formal reasoning aids agent self-understanding
- **Prompt Engineering for Code (Iyer et al., 2023):** Generic prompt optimization; semi-formal reasoning is a domain-specific technique

### Open Questions

1. **Scalability:** Can semi-formal reasoning scale to large functions or entire modules?
2. **Language Diversity:** How does the methodology adapt to languages with complex control flow (Go, Rust, Kotlin)?
3. **Abstraction Levels:** Can agents reason semi-formally about abstractions (classes, APIs, libraries)?
4. **Hybrid Approaches:** How to combine semi-formal reasoning with execution feedback for maximum accuracy?
5. **Human-Agent Collaboration:** Do developers find semi-formal traces helpful, or do they prefer other explanations?

---

## Citation

```bibtex
@article{Ugare2026agentic,
  title={Agentic Code Reasoning},
  author={Ugare, Shubham and Chandra, Satish},
  journal={arXiv preprint arXiv:2603.01896},
  year={2026}
}
```
