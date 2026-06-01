# AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering

**Paper:** [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](https://arxiv.org/abs/2604.13120)  
**ArXiv ID:** 2604.13120  
**Submission Date:** April 2026  
**Authors:** Yunchang Zhu, Liang Wu, Hanqing Lu, Keru Xu, Yuanchun Li, Xiangqun Chen  

## Executive Summary

AgentForge is a specialized multi-agent framework that treats execution verification as a first-class principle in autonomous software engineering. Unlike traditional multi-agent systems where agents coordinate through abstract representations, AgentForge grounds every code decision in a sandboxed execution environment, enabling agents to receive immediate, concrete feedback about code correctness. The framework achieves 40% resolution on SWE-bench Lite, demonstrating that execution-grounded verification is a critical driver of agent reliability in real-world software development automation.

## Problem Statement

**Challenge:**
Large language models can generate syntactically plausible code but cannot reliably verify its correctness without execution. Existing multi-agent systems decompose software engineering tasks (planning, coding, testing, debugging) but lack a principled mechanism to integrate execution feedback, often leading to accumulating errors through the agent pipeline.

**Prior Limitations:**
- Single-agent baselines achieve only 12-14% resolution on SWE-bench Lite
- Multi-agent systems without execution grounding struggle with error propagation
- Agents cannot distinguish between code that compiles and code that solves the problem
- Debugging loops remain disconnected from concrete failure signals

**Research Gap:**
There is no unified framework that combines structured multi-agent decomposition with mandatory execution verification, treating execution feedback as a core architectural principle rather than an afterthought.

## Core Concepts & Theory

### Agent Roles and Responsibilities

AgentForge decomposes software engineering into five specialized agent roles:

1. **Planner Agent:** Analyzes the problem statement and generates a structured execution plan
   - Input: problem description, SWE-bench issue
   - Output: step-by-step plan with predicted locations and change types
   - Uses CoT reasoning to understand the problem space

2. **Coder Agent:** Generates minimal, targeted code changes
   - Input: plan, repository context, file diffs
   - Output: unified diff format patches
   - Follows DRY principle: minimal changes to reduce hallucination

3. **Tester Agent:** Generates executable test cases
   - Input: problem statement, codebase
   - Output: pytest-compatible test suites
   - Validates correctness without executing against original implementation

4. **Debugger Agent:** Repairs failures through iterative execution feedback
   - Input: execution failures, error messages, current code state
   - Output: targeted bug fixes
   - Core to performance: uses concrete failure signals to guide repairs

5. **Critic Agent:** Reviews patches before propagation
   - Input: proposed changes, execution results
   - Output: approval or rejection with reasoning
   - Prevents invalid changes from propagating downstream

### Architectural Principles

**Execution-Grounded Verification:**
```
Problem → Planner → Coder → Tester → [Sandbox Execution]
                                        ↓ (Success)
                                     Output
                                        ↓ (Failure)
                                     Debugger → [Sandbox Execution] → ...
```

Every code change must survive sandboxed execution before propagating. Failure provides concrete, actionable feedback rather than abstract ranking.

**Shared Memory Model:**
All agents share access to:
- Original repository state
- Current working code
- Execution logs and error messages
- Plan history and decisions
- Test results

**Unified Diff Representation:**
Changes encoded as unified diffs enable:
- Minimal, reviewable patches
- Precise dependency tracking
- Easy rollback on failure
- Clear attribution of changes to agent decisions

### Docker Sandbox for Safety and Isolation

AgentForge executes all generated code in isolated Docker containers:
- Each execution gets a fresh environment snapshot
- No persistent state corruption
- Safe timeout handling (prevents infinite loops)
- Automatic cleanup

## Main Ideas & Contributions

### 1. Execution-Grounded Agent Decomposition

Unlike sequential pipelines where errors compound, AgentForge ensures that each agent works with validated code. The Tester-Debugger loop directly closes feedback to code generation, enabling iterative refinement based on actual behavior rather than abstract reasoning.

**Key Innovation:** Failure is not a terminal state but a signal for targeted repair. The Debugger receives concrete error messages (stack traces, assertion failures, test output) rather than vague feedback.

### 2. Specialized Agent Roles with Explicit Contracts

Each agent has a narrow, well-defined responsibility:
- **Planner:** understanding, not coding
- **Coder:** implementation, not testing
- **Tester:** validation, not repair
- **Debugger:** error correction using execution feedback
- **Critic:** quality gates

This specialization allows agents to:
- Maintain focus and reduce hallucination
- Receive role-specific training or prompt engineering
- Be independently validated and improved
- Parallelize safely (Tester and Planner can work concurrently)

### 3. Mandatory Sandbox Execution

Execution-grounded verification ensures:
- No reliance on abstract code quality metrics
- Immediate detection of syntactic errors, import failures, infinite loops
- Concrete evidence of correctness (tests pass)
- Clear failure modes for error analysis

### 4. Iterative Debugger Loop

The Debugger agent bridges the gap between intent and execution:
- Receives full stack traces, test failures, error messages
- Generates targeted patches, not full file rewrites
- Operates under the principle: "fix the symptom of the reported error"
- Escalates to Planner if the root cause suggests fundamental design flaws

## Methodology & Implementation

### Datasets and Benchmarks

**Primary Benchmark: SWE-bench Lite**
- 300 real GitHub issues from popular Python projects
- Requires agents to:
  - Understand issue descriptions
  - Locate affected code
  - Implement fixes
  - Verify with existing test suites
- Evaluation: resolution rate (does the fix pass provided tests?)

**Baseline Comparison:**
- Single-agent LLM (GPT-4): 12-14% resolution
- Chain-of-Thought single agent: 14-16% resolution
- AgentForge (full system): 40.0% resolution

### Experimental Setup

**Agent Implementation:**
- Agents implemented using Claude API with few-shot prompts
- Coder: prompt includes repository structure, similar files (for in-context learning)
- Tester: prompt includes test examples from the codebase
- Debugger: prompt receives full error logs and previous attempts

**Execution Environment:**
- Python 3.9+ isolated Docker containers
- 30-second timeout per execution
- Automatic cleanup of side effects (file writes, process spawns)
- Test execution via pytest

**Evaluation Metrics:**

1. **Primary:** Resolution Rate
   - Percentage of issues where agent-generated fix passes all tests
   - AgentForge: 40.0% on SWE-bench Lite

2. **Secondary:**
   - Patch Size: median diffs per fix (measures minimalism)
   - Token Usage: total API calls per issue
   - Time-to-Resolution: wall-clock time per issue
   - Failure Mode Distribution: which agent stage fails most often?

### Ablation Study Results

**Key Findings:**
- Execution feedback: removes 15-20 percentage points if disabled (40% → 20-25%)
- Role decomposition: removes 8-12 percentage points if collapsed to single agent
- Debugger iteration: 3-4 rounds of iteration cover ~95% of fixable issues
- Critic review: prevents ~3-5% of changes that would fail downstream

**Interpretation:**
Execution feedback is the dominant performance driver, but multi-agent decomposition provides complementary benefits. Neither alone accounts for the full improvement.

## Practical Applications & Use Cases

### 1. Autonomous Bug Fixing

**Scenario:** GitHub issue → automated fix without human intervention
- AgentForge reads issue description and code
- Generates fix
- Runs test suite to verify
- Creates PR with generated patch

**Real-world Impact:** For maintainers, reduces triage overhead; for teams, enables proactive bug fixes before user impact.

### 2. Large-Scale Refactoring

**Scenario:** Migrate codebase from Python 2 to Python 3, or refactor to new API
- Planner generates migration strategy
- Coder applies changes file-by-file
- Tester validates with existing test suite
- Debugger handles edge cases

**Integration Challenge:** requires test suite coverage; teams without tests face higher risk.

### 3. Dependency Upgrade and Security Patching

**Scenario:** security vulnerability in a dependency
- Planner analyzes API changes
- Coder updates code for new API
- Tester catches breaking changes
- Debugger repairs failures

**Cost Implication:** saves engineering time on routine updates; especially valuable for large codebases with many dependencies.

### 4. Code Review and Quality Gates

**Scenario:** Critic agent reviews generated patches before merge
- Detects common error patterns (off-by-one bugs, resource leaks)
- Ensures adherence to codebase style
- Flags high-risk changes for human review

## Insights & Implications

### 1. Execution is the Ground Truth for Code Agents

Abstract metrics (code similarity, AST matching) are poor predictors of correctness. Agents that ground decisions in actual execution behavior achieve substantially better performance. This shifts the research paradigm from "how do we make agents understand code?" to "how do we help agents learn from execution?"

### 2. Multi-Agent Decomposition Reduces Hallucination

Specialization forces agents to stay focused. A Coder that isn't also responsible for testing produces fewer defensive code patterns and fewer overfitting behaviors. Separation of concerns translates to better individual outputs.

### 3. Iteration Beats Single-Pass Generation

Most fixes require 3-4 debugging iterations. Agents that can refine based on concrete feedback systematically outperform one-shot generation. This mirrors human debugging: "try, observe, refine."

### 4. Docker Sandboxing is Critical Infrastructure

Safe execution enables risk-taking (agents can try more radical changes because failures are contained). Without sandboxing, agents become overly conservative.

### 5. Limitations and Open Questions

- **Requires comprehensive test suites:** if test coverage is low, the Tester can't catch bugs
- **Debugging depth:** some issues require root-cause analysis beyond execution feedback (design flaws in architecture)
- **Generalization:** SWE-bench focuses on Python projects; unclear how well this transfers to other languages
- **Human-in-the-loop:** doesn't address cases where human judgment is irreplaceable (API design decisions, security policy changes)

## Agent Topologies and Workflows

### Execution-Grounded Multi-Agent Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    Problem Statement                        │
│                   (GitHub Issue/PR)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │    Planner   │
                  │   (CoT Plan) │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │    Coder     │
                  │  (Generate   │
                  │   Patch)     │
                  └──────┬───────┘
                         │
        ┌────────────────▼───────────────┐
        │                                │
        ▼                                ▼
   ┌──────────┐                   ┌──────────────┐
   │  Tester  │                   │   Critic     │
   │(Generate │                   │  (Review     │
   │ Tests)   │                   │  Patch)      │
   └────┬─────┘                   └──────┬───────┘
        │                                │
        └────────────┬───────────────────┘
                     │
                     ▼
            ┌─────────────────────┐
            │  Docker Sandbox     │
            │  Execution          │
            └────────┬────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
      Success                 Failure
         │                       │
         ▼                       ▼
    ┌─────────────┐        ┌──────────────┐
    │   Output    │        │   Debugger   │
    │   (Fix)     │        │  (Error→Fix) │
    └─────────────┘        └─────┬────────┘
                                 │
                    ┌────────────▼─────────┐
                    │  Iteration Limit?    │
                    └────────┬────────┬────┘
                      No    │         │ Yes
                      ┌─────┘         └──────┬──────┐
                      │                      │      │
                      ▼                      ▼      ▼
                  [Sandbox]            [Give Up]  [Escalate
                                                   to Planner]
```

### Iteration Pattern: Tester-Debugger Feedback Loop

```
[Code] → Test Execution
  ▲              │
  │              ▼
  │         [Failure?]
  │         /        \
  │      Yes           No
  │      │             │
  │      ▼             ▼
  │   Debugger → Coder [Success - Output]
  │     │
  │     └─→ Error Analysis
  │          └─→ Fix Target
  │
  └──────── Repeat (max 4 iterations)
```

## Code & Resources

### Official Repository
- **GitHub:** Likely available from authors; check [arXiv page](https://arxiv.org/abs/2604.13120) for official links
- **Implementation Language:** Python
- **Key Dependencies:**
  - Claude API (or compatible LLM via OpenAI)
  - Docker
  - pytest (for test execution)

### Integration Requirements

**Minimal Setup:**
```bash
# 1. Install dependencies
pip install anthropic docker pytest

# 2. Set up Docker daemon (required for sandbox execution)
docker daemon

# 3. Provide API credentials
export ANTHROPIC_API_KEY="..."

# 4. Point to target repository
agentforge --repo /path/to/project --issue-id <issue_id>
```

**Compute Requirements:**
- CPU: 4+ cores (parallel agent operations)
- Memory: 8+ GB (Docker containers + API clients)
- GPU: Not required
- Network: API calls to Claude (medium bandwidth)

### Cost and Latency Implications

**Per-Issue Cost:**
- Planner: 1-2 API calls
- Coder: 3-5 calls (includes retries)
- Tester: 2-3 calls
- Debugger: 6-8 calls per iteration (3-4 iterations typical)
- **Total:** ~15-25 API calls per issue
- **Estimated Cost:** $0.50-$2.00 per issue (with Claude pricing)

**Latency:**
- Planner: 5-10 seconds
- Coder: 10-20 seconds
- Tester: 10-15 seconds
- Debugger loop: 20-40 seconds per iteration
- **Total:** 1-3 minutes per issue (end-to-end)

## Related Work & Context

### Foundational Work on Code Generation

- **Large Language Models for Code:** Codex, GPT-4 (show LLM capability but lack verification)
- **Chain-of-Thought Prompting:** Wei et al. (underlying reasoning mechanism for Planner)
- **Test-Driven Code Generation:** Zelikman et al. (early work on using tests for verification)

### Contemporary Multi-Agent Systems

- **AutoGPT, BabyAGI:** general-purpose agent frameworks (less specialized for code)
- **Gorilla:** tool-use focused, but no execution grounding
- **Open Hands:** multimodal coding agent (single-agent, no sandbox)

### Code Verification and Testing

- **SWE-bench:** The evaluation benchmark (Jimenez et al., 2024)
- **Repository-level code understanding:** CodeT5+, GraphCodeBERT
- **Automated test generation:** LLM4TestGen, DynaMoPy

### Future Directions

1. **Multi-Language Support:** AgentForge is Python-focused; extending to JavaScript, Java, Go would broaden applicability
2. **Continuous Learning:** Could agents update their Coder prompts based on patterns learned from debugging failures?
3. **Human-in-the-Loop:** Integration points for human developers to guide agents on ambiguous fixes
4. **Cost Reduction:** Can smaller models (Haiku) match performance through better prompting or agent specialization?
5. **Architectural Reasoning:** Extending beyond bug fixes to architectural improvements (refactoring, design patterns)

## References and Further Reading

- **ArXiv Paper:** [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](https://arxiv.org/abs/2604.13120)
- **Evaluation:** [SWE-bench: Can Language Models Resolve Real-world GitHub Issues?](https://arxiv.org/abs/2310.06770)
- **Related Reviews:** [LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision and the Road Ahead](https://arxiv.org/abs/2404.04834)
