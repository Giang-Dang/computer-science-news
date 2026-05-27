# TraceCoder: A Trace-Driven Multi-Agent Framework for Automated Debugging of LLM-Generated Code

**ArXiv ID:** [2602.06875](https://arxiv.org/abs/2602.06875)  
**Authors:** Jiangping Huang, Wenguang Ye, Weisong Sun, Jian Zhang, Mingyue Zhang, Yang Liu  
**Submitted:** February 6, 2026  
**Venue:** ICSE 2026 — 48th International Conference on Software Engineering (April 12–18, 2026, Rio de Janeiro, Brazil)  
**Subcategory:** `testing-debugging`

---

## Executive Summary

TraceCoder is a multi-agent framework that reimagines automated debugging by emulating the **observe-analyze-repair** process of expert human debuggers — using runtime trace instrumentation instead of superficial pass/fail signals to diagnose and repair bugs in LLM-generated code. The system achieves up to a 34.43% relative improvement in Pass@1 accuracy over state-of-the-art baselines, including a 82.00% Pass@1 on ClassEval using Gemini-2.5-Flash. This work is of high significance to agent-driven development because it establishes that deep runtime observability, structured causal reasoning, and historical learning are the key ingredients for reliable autonomous debugging — a capability that is prerequisite for any self-healing development pipeline.

---

## Problem Statement

### Development Automation Challenge

LLMs frequently generate code that is syntactically correct and structurally plausible but contains subtle semantic bugs — off-by-one errors, incorrect state management, wrong algorithm implementations, or faulty interaction patterns between components. When deployed in automated development pipelines, these bugs must be detected and corrected autonomously without human intervention.

The fundamental challenge is that most bugs are **not detectable from test output alone**. A test failure tells you *that* something is wrong, but not *where* or *why*. Without understanding the root cause, repair attempts are essentially guesswork — the LLM patches one symptom while the underlying bug persists or new bugs are introduced.

### Prior Agent System Limitations

Existing automated debugging approaches rely on **superficial signals**:

| Approach | Signal Used | Limitation |
|----------|-------------|------------|
| Self-Debugging (Chen et al.) | Error message + failing test | No visibility into internal execution |
| INTERVENOR | Test results + code diff | Cannot distinguish root cause from symptom |
| LLM Self-Repair | Pass/fail feedback | Prone to spurious repairs that mask bugs |
| Iterative Prompting | Compiler errors | Only catches syntax/type errors |

All of these approaches treat the program as a **black box** — they observe inputs and outputs but have no window into the execution path, variable states, or control flow that reveals why a test fails.

### Research Gap

No prior automated debugging framework instrumented LLM-generated code with diagnostic probes to capture **fine-grained runtime traces** that enable causal analysis — the way an expert debugger actually diagnoses bugs. Additionally, no prior system incorporated a mechanism to learn from failed repair attempts to avoid repeating the same incorrect fixes.

---

## Core Concepts & Theory

### The Expert Debugging Process: Observe-Analyze-Repair

Human expert debuggers follow a principled process:

1. **Observe**: Run code with observability instrumentation (print statements, debugger watches, profiler) to capture what actually happens during execution
2. **Analyze**: Causally reason from observations to identify the specific location and nature of the bug
3. **Repair**: Apply a targeted fix based on causal understanding, not pattern matching

TraceCoder operationalizes this three-step process as a coordinated multi-agent pipeline where each step is performed by a specialized agent with the appropriate tools and capabilities.

### Runtime Trace Instrumentation

The foundation of TraceCoder is **code instrumentation** — automatically inserting diagnostic probes into the program before execution:

```python
# Original LLM-generated code (contains a bug)
def merge_sorted_arrays(arr1, arr2):
    result = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    # Bug: missing remainder handling
    return result

# After instrumentation by Instrumentation Agent
def merge_sorted_arrays(arr1, arr2):
    TRACE.log("ENTER merge_sorted_arrays", locals())
    result = []
    i, j = 0, 0
    TRACE.log("INIT", {"i": i, "j": j, "arr1_len": len(arr1), "arr2_len": len(arr2)})
    while i < len(arr1) and j < len(arr2):
        TRACE.log("LOOP_ITER", {"i": i, "j": j, "arr1[i]": arr1[i], "arr2[j]": arr2[j]})
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
        TRACE.log("AFTER_APPEND", {"result_so_far": result[:]})
    TRACE.log("EXIT_LOOP", {"final_result": result, "i": i, "j": j})
    # Bug is now visible: loop exits with i=1, j=0, but arr2[0:] never appended
    return result
```

### Historical Lesson Learning Mechanism (HLLM)

A key innovation is the **HLLM** — a mechanism for learning from failed repair attempts to prevent recurrence of the same mistakes:

```
Pseudocode: HLLM

LESSON_BOOK = []

for repair_attempt in range(max_attempts):
    patch = RepairAgent.propose(code, trace, causal_analysis)
    result = execute_with_tests(apply_patch(code, patch))
    
    if result.passes:
        return apply_patch(code, patch)  # Success
    else:
        # Extract lesson from failure
        lesson = AnalysisAgent.extract_lesson(
            patch=patch,
            failure_reason=result.failure_trace,
            hypothesis="Why did this patch fail?"
        )
        LESSON_BOOK.append(lesson)
        
        # Future repair prompt includes lessons
        repair_prompt = base_prompt + format_lessons(LESSON_BOOK)
        # "Avoid: appending None instead of the element itself (tried, failed)"
        # "Avoid: using extend() which mutates shared state (tried, failed)"
```

### Rollback Mechanism

To ensure stable convergence, TraceCoder enforces a **strict improvement invariant**: each repair attempt must not make the system worse.

```
Pseudocode: Rollback

def apply_repair_with_rollback(code, patch):
    baseline_score = evaluate(code)  # e.g., number of passing tests
    candidate = apply_patch(code, patch)
    candidate_score = evaluate(candidate)
    
    if candidate_score >= baseline_score:
        return candidate  # Improvement or neutral (keep)
    else:
        TRACE.log("ROLLBACK", {
            "reason": "patch degraded performance",
            "baseline": baseline_score,
            "candidate": candidate_score
        })
        return code  # Rollback to previous state
```

This prevents the common failure mode where a patch fixes one test but breaks three others, leading to a net regression.

---

## Main Ideas & Contributions

### Novel Multi-Agent Architecture

TraceCoder introduces a **four-agent collaborative debugging pipeline**:

```
┌─────────────────────────────────────────────────────────────────┐
│                     TRACECODER PIPELINE                          │
│                                                                  │
│  ┌──────────────────────┐                                        │
│  │  INSTRUMENTATION     │  Agent 1: Analyzes code structure,    │
│  │       AGENT          │  inserts diagnostic probes at         │
│  │                      │  strategic points (loop bounds,        │
│  │  Tools: AST parser,  │  function entry/exit, state           │
│  │  Probe injector      │  mutations, branch conditions)         │
│  └──────────┬───────────┘                                        │
│             │ Instrumented code                                  │
│             ▼                                                    │
│  ┌──────────────────────┐                                        │
│  │    TEST EXECUTOR     │  Runner: Executes instrumented         │
│  │     (Deterministic)  │  code against failing test cases,     │
│  │                      │  captures runtime traces               │
│  └──────────┬───────────┘                                        │
│             │ Runtime traces + test results                      │
│             ▼                                                    │
│  ┌──────────────────────┐                                        │
│  │    CAUSAL ANALYSIS   │  Agent 2: Reasons over traces to      │
│  │       AGENT          │  identify root cause (not symptoms),  │
│  │                      │  generates causal hypothesis           │
│  │  Tools: Trace reader,│                                        │
│  │  HLLM lesson book    │                                        │
│  └──────────┬───────────┘                                        │
│             │ Root cause analysis + causal hypothesis            │
│             ▼                                                    │
│  ┌──────────────────────┐                                        │
│  │    REPAIR AGENT      │  Agent 3: Generates targeted patch    │
│  │                      │  based on causal analysis +           │
│  │  Tools: Code editor, │  historical lessons from HLLM         │
│  │  Diff generator      │                                        │
│  └──────────┬───────────┘                                        │
│             │ Proposed patch                                     │
│             ▼                                                    │
│  ┌──────────────────────┐                                        │
│  │  ROLLBACK VALIDATOR  │  Agent 4: Validates patch does not    │
│  │                      │  regress existing passing tests;      │
│  │  Tools: Test runner, │  commits or rolls back                │
│  │  Score comparator    │                                        │
│  └──────────────────────┘                                        │
│                                                                  │
│        ↑ Loop until: all tests pass OR max attempts reached      │
│          Each loop updates HLLM lesson book                      │
└─────────────────────────────────────────────────────────────────┘
```

### Information Flow: From Trace to Repair

```
Failing Test Case
      │
      ▼
Instrumented Execution
      │
      ▼
Runtime Trace:
  [ENTER merge_sorted_arrays: arr1=[1,3], arr2=[2,4]]
  [LOOP_ITER: i=0, j=0, comparing 1 vs 2]
  [AFTER_APPEND: result=[1]]
  [LOOP_ITER: i=1, j=0, comparing 3 vs 2]
  [AFTER_APPEND: result=[1,2]]
  [LOOP_ITER: i=1, j=1, comparing 3 vs 4]
  [AFTER_APPEND: result=[1,2,3]]
  [EXIT_LOOP: final_result=[1,2,3], i=2, j=1]
  → EXPECTED: [1,2,3,4] (missing arr2[1:])
      │
      ▼
Causal Analysis:
  "Loop exits when i reaches len(arr1)=2.
   At exit, j=1 and arr2[j:]=[4] is non-empty.
   Root cause: no handling for remaining elements
   after one array is exhausted."
      │
      ▼
Targeted Repair:
  +result.extend(arr1[i:])
  +result.extend(arr2[j:])
      │
      ▼
Rollback Check: 2/2 tests pass → COMMIT
```

### Comparison with Prior Approaches

| Aspect | Self-Debugging | INTERVENOR | TraceCoder |
|--------|---------------|------------|------------|
| Observability | Black-box | Semi-transparent | Full trace |
| Root Cause Analysis | No | Partial | Yes (causal) |
| Historical Learning | No | No | Yes (HLLM) |
| Stability Guarantee | No | No | Yes (rollback) |
| Pass@1 on ClassEval | ~61% (best prior) | ~55% | **82%** |

---

## Methodology & Implementation

### Datasets and Benchmarks

TraceCoder is evaluated on three widely used benchmarks:

| Benchmark | Description | Focus |
|-----------|-------------|-------|
| **HumanEval+** | 164 Python programming problems with extended test suites | Algorithmic correctness |
| **ClassEval** | 100 class-level code generation tasks | Object-oriented programming complexity |
| **BigCodeBench** | 1,140 tasks requiring diverse function calls and complex instructions | Real-world library usage |

### LLM Backends Tested

The framework is evaluated with multiple LLM backends to assess generalizability:
- Gemini-2.5-Flash-0417 (primary reported model)
- Additional models for cross-LLM evaluation

### Experimental Protocol

```
For each task in benchmark:
  1. Generate initial code using base LLM
  2. Run test suite → identify failing tests
  3. If fails:
     a. Instrumentation Agent adds probes
     b. Execute instrumented code, capture traces
     c. Analysis Agent performs causal analysis (with current HLLM book)
     d. Repair Agent generates patch
     e. Rollback Validator checks improvement
     f. If improved: commit; update HLLM book with lesson
     g. If not improved: rollback; add lesson; increment attempt counter
     h. Repeat from (b) if attempts < max_attempts
  4. Record final pass/fail and attempt count

Metric: Pass@1 (fraction passing on first evaluation after repair)
Baseline comparisons: Self-Debugging, INTERVENOR, raw LLM generation
```

### Key Results

| Benchmark | Model | Raw LLM | Self-Debugging | INTERVENOR | TraceCoder | Improvement |
|-----------|-------|---------|----------------|------------|------------|-------------|
| ClassEval | Gemini-2.5-Flash | ~50% | 61% | ~55% | **82%** | **+34.43%** |
| BigCodeBench | Multiple | varies | baseline | baseline | **best** | consistent |
| HumanEval+ | Multiple | varies | baseline | baseline | **best** | consistent |

The 34.43% relative improvement on ClassEval represents the headline result, demonstrating that class-level code (with complex object interactions) particularly benefits from trace-based debugging where inter-method state is visible.

### Instrumentation Strategy Details

The Instrumentation Agent uses static analysis (AST parsing) to identify high-value probe locations:

1. **Function boundaries**: Entry/exit with full parameter/return state
2. **Loop control variables**: Iteration indices, comparison values, accumulator states
3. **Branching conditions**: Which branch was taken and on what values
4. **State mutation points**: Before/after any assignment to shared state
5. **Exception sites**: If/when exceptions are thrown and with what context

The agent is aware of overhead: probes are inserted strategically rather than exhaustively, limiting trace volume while maximizing diagnostic value.

---

## Practical Applications & Use Cases

### Direct Software Development Applications

1. **Automated code review with deep diagnostics**: Replace shallow static analysis with trace-based dynamic analysis to identify bugs that only manifest at runtime
2. **CI/CD self-healing pipelines**: When tests fail in CI, TraceCoder automatically diagnoses and proposes fixes, reducing time-to-fix from hours to minutes
3. **LLM-assisted development copilots**: When a developer's LLM-generated code fails tests, the copilot provides trace-based explanations rather than vague error messages
4. **Regression debugging**: When a code change breaks existing tests, trace comparison between passing and failing executions isolates the regression source
5. **Test-driven repair**: Given a failing test suite, automatically produce code changes that make all tests pass while maintaining the rollback guarantee

### Concrete Multi-Agent Debugging Workflow: API Endpoint Bug

```
Scenario: LLM-generated pagination logic fails tests

Failing test:
  test_get_users_page_2():
    response = client.get("/users?page=2&limit=10")
    assert response.json()["users"][0]["id"] == 11  # Fails: returns id=1

TraceCoder pipeline:

1. Instrumentation:
   + TRACE.log("PAGINATION", {"page": page, "limit": limit, "offset": page*limit})
   + TRACE.log("QUERY", {"sql": query_str, "params": params})
   + TRACE.log("RESULT_COUNT", {"count": len(results)})

2. Execution trace:
   [PAGINATION: page=2, limit=10, offset=20]  ← Bug found!
   [QUERY: SELECT * FROM users LIMIT 10 OFFSET 20]
   [RESULT_COUNT: count=0]

3. Causal Analysis:
   "offset=page*limit=20 when page=2. But page is 1-indexed.
   Correct offset should be (page-1)*limit=10.
   Root cause: off-by-one in page indexing."

4. Repair:
   -offset = page * limit
   +offset = (page - 1) * limit

5. Validation: All 5 pagination tests pass → COMMIT
Total time: ~45 seconds
```

### Integration Challenges

- **Language support**: Instrumentation currently focuses on Python; extending to JavaScript, Java, Go requires language-specific AST parsers and probe injectors
- **External dependencies**: Code that calls databases, external APIs, or file systems requires mock/sandbox environments for safe instrumented execution
- **Trace volume management**: Complex programs generate large traces; relevance filtering is essential to keep Analysis Agent context manageable
- **Security**: Executing instrumented code requires sandboxed environments to prevent malicious code execution

### Cost and Latency Implications

| Component | Latency | Cost Driver |
|-----------|---------|-------------|
| Instrumentation | Low (AST ops) | Negligible |
| Instrumented execution | Medium (runtime + tracing) | Compute time |
| Causal analysis | Medium (LLM call) | Token count (trace can be large) |
| Repair generation | Low (LLM call) | Short context usually sufficient |
| Validation | Low (test runner) | Compute time |

Net effect: TraceCoder adds 10–30 seconds per repair attempt compared to simple re-prompting, but dramatically reduces the *number* of attempts needed due to targeted repairs.

---

## Insights & Implications

### Impact on Agent-Driven Development

TraceCoder establishes that **observability is the missing ingredient** in autonomous debugging agents. The fundamental limitation of prior systems was treating execution as a black box — the same mistake junior developers make when debugging without a debugger. By giving agents the same runtime visibility that expert engineers use, the gap between autonomous and human debugging quality narrows substantially.

This has broad implications: any autonomous development agent should have access to runtime trace tools, not just static analysis and test output.

### Advancement in Autonomous Coding

The HLLM is a significant advance in **agent memory for debugging**: by accumulating lessons from failed repair attempts within a single debugging session, the agent effectively performs in-context reinforcement — learning what not to try without expensive fine-tuning. This is an efficient approximation of the experience that makes senior developers better debuggers than junior ones.

The rollback mechanism addresses a critical reliability concern in autonomous systems: **guarantee of non-regression**. For deployment in production CI pipelines, this guarantee is essential — an autonomous agent that might make things worse is not trustworthy for production use.

### Limitations

- The framework requires executable environments for instrumented code; it cannot debug code that cannot be run (e.g., infrastructure-as-code, configuration files)
- Instrumentation assumes deterministic execution; non-deterministic code (threading, randomness) produces inconsistent traces
- HLLM lessons are session-scoped; there is no cross-session learning from past debugging experiences
- Very deep call stacks or recursive functions generate traces that overwhelm the Analysis Agent's context window

### Open Research Questions

- Can trace-based analysis extend to **multi-file bugs** where root causes span module boundaries?
- What is the optimal probe placement strategy that maximizes diagnostic value per trace token?
- Can HLLM lessons be persisted and shared across debugging sessions (persistent agent memory)?
- How does TraceCoder perform on bugs requiring understanding of **distributed system behavior** (race conditions, network failures)?

### Relevance to Skill Frameworks

The TraceCoder architecture maps naturally onto a **debugging skill** in an agent framework:
- `instrument_code(code, language)` → Instrumentation Agent skill
- `analyze_trace(trace, test_results)` → Causal Analysis skill
- `repair_code(code, analysis, lesson_book)` → Repair Agent skill
- `validate_patch(original, patched, test_suite)` → Validation skill

The HLLM lesson book could be implemented as a **skill-scoped memory store** that persists lessons within a debugging task context, enabling agents to avoid repeating mistakes across multiple repair cycles.

---

## Code & Resources

- **ArXiv Paper:** https://arxiv.org/abs/2602.06875
- **Conference:** ICSE 2026 — [Paper at ICSE](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/145/TraceCoder-A-Trace-Driven-Multi-Agent-Framework-for-Automated-Debugging-of-LLM-Gener)
- **Note:** The ICSE proceedings paper contains implementation details; check IEEE Xplore or the conference proceedings for supplementary materials

### Dependencies and Compute Requirements

- Python runtime with AST manipulation libraries (`ast`, `libcst`)
- LLM API with function/tool calling support (Gemini, Claude, GPT-4)
- Sandboxed Python execution environment (Docker, subprocess with timeouts)
- Test framework integration (pytest, unittest)
- Optional: structured logging framework for trace capture

### Conceptual Integration Guide

```python
from tracecoder import TraceCoderDebugger, InstrumentationConfig

debugger = TraceCoderDebugger(
    llm_backend="claude-sonnet-4-6",
    instrumentation_config=InstrumentationConfig(
        probe_points=["function_boundaries", "loops", "branches", "mutations"],
        max_trace_tokens=8000,  # Limit trace size for Analysis Agent context
    ),
    max_repair_attempts=5,
    rollback_enabled=True,
    hllm_enabled=True
)

# Debug failing code
result = debugger.debug(
    code=failing_code,
    test_suite=test_cases,
    language="python"
)

if result.success:
    print(f"Fixed in {result.attempts} attempts")
    print(f"Root cause: {result.causal_analysis}")
    print(f"Patch: {result.patch}")
else:
    print(f"Could not fix: {result.failure_reason}")
    print(f"Lessons learned: {result.lesson_book}")
```

---

## Related Work & Context

### Related Papers

- **Self-Debugging** (Chen et al., 2023): The foundational work on LLM self-repair using error messages; TraceCoder extends this with trace-based observability
- **INTERVENOR** ([arXiv:2311.09868](https://arxiv.org/abs/2311.09868)): Multi-turn interactive repair with compiler feedback; TraceCoder outperforms by using runtime traces
- **RGD: Multi-LLM Based Agent Debugger** ([arXiv:2410.01242](https://arxiv.org/abs/2410.01242)): Refinement and generation guidance for debugging; complementary LLM-centric approach
- **AgentCoder** ([arXiv:2312.13010](https://arxiv.org/abs/2312.13010)): Test designer + executor agent pipeline for generation; debugging focus in TraceCoder vs generation focus in AgentCoder
- **Rethinking the Value of Agent-Generated Tests** ([arXiv:2602.07900](https://arxiv.org/abs/2602.07900)): Related ICSE 2026 work analyzing how agent-generated tests affect debugging quality

### Prior Foundational Work

- **Delta Debugging** (Zeller, 2002): Classic automated debugging by minimizing failure-inducing inputs — TraceCoder applies similar systematic narrowing but through LLM-driven causal analysis
- **Dynamic Program Analysis**: Foundational techniques (memory profilers, execution tracers, sanitizers) that TraceCoder operationalizes as agent tools
- **BigCodeBench** ([arXiv:2406.15877](https://arxiv.org/abs/2406.15877)): The benchmark showing LLMs struggle with real-world library calls — exactly the class of bugs TraceCoder addresses well
- **SWE-Bench**: Repository-level debugging benchmark that provides direction for future TraceCoder evaluation at larger scales

### Future Research Directions

- **Cross-session lesson persistence**: HLLM lessons stored in vector databases for retrieval across debugging sessions
- **Proactive instrumentation**: Rather than reactive debugging, proactively instrument code during generation to catch bugs before tests fail
- **Trace-based test generation**: Using runtime traces from passing executions to automatically generate edge-case tests
- **Multi-language support**: Extending instrumentation to JavaScript, Java, Go, and Rust
- **Distributed system debugging**: Adapting trace analysis for multi-service architectures with distributed traces (OpenTelemetry integration)
- **Repository-scale evaluation**: Applying TraceCoder to SWE-Bench and SWE-Bench Lite to evaluate on real GitHub issues
