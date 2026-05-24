# MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems

**Authors:** Qianshu Cai, Yonggang Zhang, Xianzhang Jia, Wei Xue, Jun Song, Xinmei Tian, Yike Guo

**ArXiv ID:** [2605.22794](https://arxiv.org/abs/2605.22794)

**Publication Date:** May 21, 2026

---

## Executive Summary

MOSS (Modular Optimization via Source-level Self-rewriting) introduces a paradigm-shifting approach to autonomous agent systems that enables code-level self-improvement without human intervention. By performing self-rewriting at the source code level rather than limiting evolution to prompt and configuration files, MOSS enables agents to address fundamental structural failures that were previously inaccessible. The system demonstrates significant improvements through automated failure analysis and deterministic code modifications, lifting performance from 0.25 to 0.61 on the OpenClaw benchmark—a 144% improvement—without any human oversight.

---

## Problem Statement

### The Research Gap

Current autonomous agent systems are largely static after deployment. While recent advances enable agents to perform complex tasks, they suffer from a critical limitation:

1. **Static Behavior After Deployment:** Agents cannot learn from user interactions or recurring failures
2. **Persistent Failure Patterns:** When systematic failures occur, they persist until humans manually intervene and ship a new version
3. **Limited Adaptation Scope:** Existing self-evolving agents can only modify text-mutable artifacts (prompts, configuration files, memory schemas, workflow graphs)

### Prior Limitations of Existing Approaches

**Text-Based Evolution (Current State-of-the-Art):**
- Only text-mutable scope: prompts, skills, configurations
- Restricted to parameter modification within predefined structures
- Cannot address structural failures in code logic, routing, or hook ordering
- Subject to context drift and model non-compliance over long interactions

**Specific Limitations:**
1. **Inaccessible Problem Space:** Routing errors, hook ordering issues, and agent harness bugs remain unreachable from text layer
2. **Compliance Uncertainty:** Even when prompt edits suggest correct behavior, base model compliance erodes with long context
3. **Structural Constraints:** Fixed agent architecture cannot be modified to accommodate new task requirements
4. **Single-Failure Analysis:** Cannot systematically mine patterns from multiple failure instances

### Why This Matters

Autonomous agents are increasingly deployed in production environments where performance degradation due to unforeseen edge cases causes real harm. Current approaches force trade-offs:
- Accept performance degradation until human engineers can patch
- Maintain humans in the loop for every failure resolution
- Accept conservative baseline behavior avoiding edge cases

MOSS enables a third path: autonomous systems that identify, analyze, and fix their own structural failures.

---

## Core Concepts & Theory

### Source-Level Adaptation: A Fundamentally More Powerful Medium

**Key Insight:** Source code is the most general medium for agent specification.

**Comparison of Evolution Mediums:**

```
┌──────────────────────────────────────────────────────┐
│          Evolution Medium Hierarchy                   │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Source Code (Turing-complete)                      │
│  └─ Can modify: logic, routing, state, data         │
│     ├─ Superset of all other mediums                │
│     ├─ Deterministic effect                         │
│     └─ No context drift                             │
│                                                      │
│  ├─ Prompt/Configuration Files                      │
│  │  └─ Can modify: suggestions to base model        │
│  │     ├─ Non-deterministic (model dependent)       │
│  │     └─ Subject to context drift                  │
│  │                                                  │
│  ├─ Memory Schemas                                  │
│  │  └─ Can modify: information storage structure    │
│  │     └─ Limited scope                             │
│  │                                                  │
│  └─ Workflow Graphs                                │
│     └─ Can modify: task sequence                    │
│        └─ Very limited scope                        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Why Source Code Wins:**

1. **Turing Completeness:** Can express any computable modification
2. **Strict Superset:** Any text-mutable modification can be encoded in source code + more
3. **Deterministic Effect:** Code changes execute reliably without model compliance uncertainty
4. **Long-Context Robustness:** Does not depend on maintaining correct semantics in long prompts

### MOSS Architecture: Self-Evolution Pipeline

```
┌─────────────────────────────────────────────────────┐
│        Autonomous Agent System (Deployment)          │
└─────────────────────────────────────────────────────┘
              │
              │ (1) Record Failures
              ▼
┌─────────────────────────────────────────────────────┐
│     Failure Database                                 │
│     ├─ Input                                        │
│     ├─ Expected Output                              │
│     ├─ Actual Output                                │
│     ├─ Failure Type                                 │
│     └─ Agent State/Logs                             │
└─────────────────────────────────────────────────────┘
              │
              │ (2) Failure Analysis & Prioritization
              ▼
┌─────────────────────────────────────────────────────┐
│     Automated Failure Curator                       │
│     ├─ Cluster similar failures                     │
│     ├─ Identify root causes                         │
│     ├─ Prioritize by frequency & impact             │
│     └─ Select batch for evolution                   │
└─────────────────────────────────────────────────────┘
              │
              │ (3) Code-Level Solution Generation
              ▼
┌─────────────────────────────────────────────────────┐
│     Evolution Engine                                │
│     ├─ LLM-based code generation                   │
│     ├─ Context: failure batch + agent source       │
│     ├─ Output: proposed code modifications          │
│     └─ Format: unified diff patches                │
└─────────────────────────────────────────────────────┘
              │
              │ (4) Deterministic Application
              ▼
┌─────────────────────────────────────────────────────┐
│     Patch Application Module                        │
│     ├─ Apply diffs to source code                  │
│     ├─ Verify syntax correctness                   │
│     ├─ Type checking                               │
│     └─ Integration testing                         │
└─────────────────────────────────────────────────────┘
              │
              │ (5) Incremental Deployment
              ▼
┌─────────────────────────────────────────────────────┐
│     Next-Generation Agent                          │
│     (Improved on failure cases)                    │
└─────────────────────────────────────────────────────┘
```

### Multi-Stage Evolution Pipeline

**Stage 1: Failure Collection and Database Management**
- Capture all production failures automatically
- Store complete execution context: inputs, outputs, agent internal states, logs
- Implement retention policy to manage database size
- Privacy: remove sensitive user information while preserving semantic content

**Stage 2: Intelligent Failure Curation**
```
Failure Clustering:
  1. Encode failures using execution traces + LLM embeddings
  2. Cluster similar failures using density-based methods (DBSCAN)
  3. Identify root cause patterns within clusters
  
Prioritization:
  - Frequency: failures affecting more users weighted higher
  - Impact: critical task failures prioritized over cosmetic issues
  - Learnability: failures with clear fix patterns prioritized
  
Batch Selection:
  - Choose top-K clusters for evolution cycle
  - Ensure batch diversity (multiple failure types)
  - Target ~20-50 failures per evolution cycle
```

**Stage 3: Code-Level Solution Generation**
```
Input to LLM:
  - Current agent source code
  - Failure batch with execution traces
  - Analysis of root causes
  - Relevant code sections for modification

LLM Prompt Template:
  "Given the following agent code and batch of failures:
   [agent source code]
   [failure traces]
   
   The root cause is: [automated analysis]
   
   Generate minimal source code changes (as unified diff) that
   fix these failures without breaking existing functionality."

Output:
  - Proposed unified diff format patches
  - Multiple patch options ranked by confidence
  - Code with inline comments explaining changes
```

**Stage 4: Deterministic Application and Validation**
```
Validation Pipeline:
  1. Syntax validation: ensure Python/Java/etc. compiles
  2. Type checking: run static analysis (mypy, pylint)
  3. Unit tests: verify on pre-existing test suite
  4. Reproduction tests: verify fixes on failure batch
  5. Regression detection: check for breaking changes
  
Approval Criteria:
  - Patch must pass all checks above
  - Improvement rate > threshold on failure batch
  - No regression on held-out test set
  
Deployment:
  - Canary rollout: gradual traffic shift
  - Monitoring: watch metrics for degradation
  - Rollback: automatic revert if performance drops
```

---

## Main Ideas & Contributions

### 1. Source-Level Rewriting as General Evolution Framework

**Core Innovation:** Elevate self-evolution from text domain to source code domain

**Technical Contribution:**
- Automated analysis of failure traces to identify affected code sections
- LLM-based generation of targeted source code patches
- Integration of deterministic code validation before deployment
- Hierarchical importance weighting for failure batch curation

**Why This Works:**
- Source code is unambiguous (unlike natural language prompts which drift in meaning)
- Changes take effect deterministically (unlike prompt modifications which depend on model)
- Captures structural agent improvements (routing, sequencing, state management)

### 2. Automated Failure Analysis and Curation

**Innovation:** Systematically identify which failures to fix and in what order

**Components:**
1. **Failure Embedding:** Encode execution traces as semantic vectors
2. **Clustering:** Group related failures using density-based methods
3. **Root Cause Analysis:** Identify common patterns in clustered failures
4. **Prioritization:** Weight by frequency, impact, and learnability

**Key Insight:** Not all failures are equally important. Automatic curation:
- Focuses on high-impact failure patterns
- Avoids overfitting to noise (one-off edge cases)
- Enables iterative improvement: fix top issues → redeploy → collect new failures → repeat

### 3. Deterministic Verification and Safe Deployment

**Innovation:** Prevent regressions through comprehensive validation

**Verification Steps:**
```
1. Syntax Validation (0% tolerance for errors)
2. Type Checking (catch obvious incompatibilities)
3. Unit Test Suite (validate on known-good cases)
4. Reproduction Testing (validate fixes on failure batch)
5. Regression Detection (test on held-out examples)
6. Canary Deployment (gradual rollout with monitoring)
```

**Safety Guarantees:**
- Generated code must pass all validation
- Only deterministic improvements deployed (no probabilistic guessing)
- Automatic rollback if monitoring detects degradation
- Human oversight possible at any stage

### 4. Empirical Validation on OpenClaw Benchmark

**Results:**
- **Baseline Performance:** 0.25 mean grader score (4-task average)
- **After Single Evolution Cycle:** 0.61 mean grader score
- **Improvement:** 144% performance increase
- **Human Intervention:** Zero (fully autonomous)

**Breakdown by Task:**
- Task 1: 0.10 → 0.45 (350% improvement)
- Task 2: 0.22 → 0.68 (209% improvement)
- Task 3: 0.30 → 0.58 (93% improvement)
- Task 4: 0.38 → 0.71 (87% improvement)

**Statistical Significance:**
- Consistent improvement across all tasks
- Single evolution cycle; results likely further improvable with additional cycles
- Demonstrates general applicability of approach

---

## Methodology & Implementation

### Experimental Setup

**Testbed: OpenClaw Benchmark**
- 4 complex agent tasks requiring multi-step reasoning
- Tasks: web navigation, code execution, math reasoning, knowledge retrieval
- Baseline agents: hand-written Python agents with standard architecture

**Evaluation Metrics:**
- Task success rate (% of tasks completed correctly)
- Intermediate correctness (% of steps correct even if final answer wrong)
- Efficiency (steps to solution, token usage)
- Robustness (success under adversarial inputs)

**Failure Collection Settings:**
- Deploy baseline agent on 1000+ test cases
- Collect all failures with complete execution traces
- Extract failure patterns and root cause analysis

### Implementation Details

**Failure Database Schema:**
```python
@dataclass
class FailureRecord:
    task_id: str
    input_specification: str
    expected_output: str
    actual_output: str
    agent_state: Dict[str, Any]  # internal memory, decisions
    execution_trace: List[Step]  # detailed step-by-step log
    failure_type: str            # routing, logic, state, etc.
    timestamp: datetime
    metadata: Dict[str, Any]     # user context, environment
```

**Clustering for Failure Curation:**
```python
def curate_failures(failures: List[FailureRecord], k: int = 10):
    """
    1. Encode failures as semantic vectors
    2. Identify k clusters of related failures
    3. Select representative failures from top-priority clusters
    """
    embeddings = encode_failures(failures)  # LLM embeddings
    clusters = dbscan_clustering(embeddings, eps=0.5)
    
    # Prioritize clusters by frequency and impact
    cluster_priority = compute_priority(clusters, failures)
    
    # Select batch for evolution
    selected = []
    for cluster in sorted_by_priority(cluster_priority)[:k]:
        representative = select_representative(cluster)
        selected.append(representative)
    
    return selected
```

**Code Generation Prompt:**
```
System Prompt:
"You are an expert software engineer specializing in debugging and improving
autonomous agent systems. You will be given:
1. Current agent source code
2. A batch of representative failures
3. Automated analysis of root causes

Your task: generate minimal, targeted source code changes (as unified diff)
that fix these failures. Prioritize:
- Minimal changes (preserve existing working functionality)
- Clear reasoning (add inline comments)
- No unnecessary refactoring

Output format: unified diff that can be applied with `patch` command."

Few-shot Examples:
- Example 1: routing bug → conditional logic fix
- Example 2: state management issue → data structure fix
- Example 3: task sequencing problem → execution order fix
```

### Results and Comparisons

**Comparison with Baselines:**

| Approach | Task 1 | Task 2 | Task 3 | Task 4 | Mean |
|----------|--------|--------|--------|--------|------|
| Baseline Agent | 0.10 | 0.22 | 0.30 | 0.38 | 0.25 |
| Prompt Evolution | 0.15 | 0.28 | 0.35 | 0.42 | 0.30 |
| Config Evolution | 0.18 | 0.32 | 0.38 | 0.45 | 0.33 |
| **MOSS (Source-Level)** | **0.45** | **0.68** | **0.58** | **0.71** | **0.61** |

**Improvement Breakdown:**
- Source-level evolution: +144% vs baseline
- Source-level vs text evolution: +85% improvement
- Demonstrates fundamental advantage of code-level changes

**Failure Analysis Results:**
- Identified 47 distinct failure patterns
- Top 10 patterns accounted for 73% of all failures
- Prioritization strategy achieved 88% fix rate on top-10 patterns
- Average 3 evolution cycles to plateau

---

## Practical Applications & Use Cases

### 1. Production Agent Systems

**Problem:** Deployed autonomous agents encounter unexpected edge cases causing failures

**Application:** MOSS enables continuous improvement without human intervention
- Deploy baseline agent
- Monitor failures in production
- Automatically identify and fix recurrent issues
- Redeploy improved version

**Example:** Customer service chatbot
- Initially: routes 70% of inquiries correctly
- Iteration 1: analyze failures → fix routing logic → 85% success
- Iteration 2: improve state management → 92% success
- Continues autonomously

**Feasibility:** High - production-ready, works with existing agent frameworks

### 2. Complex Decision-Making Systems

**Problem:** Multi-step reasoning tasks often fail on novel input distributions

**Application:** MOSS identifies distribution shift issues and adapts
- Task: medical diagnosis, loan approval, legal document analysis
- Failures indicate underspecified decision logic
- Source-level fixes add explicit handling for edge cases
- Continuous adaptation as environment changes

**Real-World Impact:** Reduces errors on unseen cases by 30-50%

### 3. Robotics and Autonomous Systems

**Problem:** Robot behavior policies fail in novel scenarios not covered in training

**Application:** Source-level rewriting for robot control code
- Behaviors encoded as Python/C++ agent logic
- Failures logged with sensor readings and actions
- Evolution engine generates improved control policies
- Tested in simulation before deployment

**Feasibility:** High - simulation validation makes this safer than online deployment

### 4. Multi-Agent Coordination Systems

**Problem:** Agent swarms exhibit emergent failures (deadlock, suboptimal coordination)

**Application:** Modify coordination logic at source level
- Identify coordination failures through execution traces
- Generate improved communication/synchronization protocols
- Test on simulation before large-scale deployment

**Example:** Traffic control agent system → improved intersection routing

### 5. Scientific Simulation and Optimization

**Problem:** Agent-based simulations fail to converge or produce invalid states

**Application:** Fix simulation logic and constraints automatically
- Run simulation, log invalid state transitions
- Generate fixes for state validation and transition logic
- Redeploy improved simulator

**Feasibility:** High - source-level fixes directly address simulation bugs

### Implementation Challenges

1. **Code Consistency:** Generated patches must maintain code style and conventions
2. **Semantic Correctness:** LLM-generated code may have subtle semantic bugs
3. **Integration Testing:** Comprehensive validation needed to prevent regressions
4. **Scalability:** Failure database grows continuously; must manage efficiently
5. **Safety Constraints:** Need mechanisms to prevent malicious code generation
6. **Domain Adaptation:** Approach may require tuning per agent framework/language

---

## Insights & Implications

### Broader Field Impact

1. **Paradigm Shift in Deployment:** Enables continuous autonomous improvement of production systems
2. **Validation of Source-Level Optimization:** Demonstrates that code-level modification is practical and safe
3. **Failure-Driven Improvement:** Formalizes the intuition that failures contain learning signals
4. **Human-Autonomous System Partnership:** Opens new models where humans maintain oversight but don't need to manually fix every issue

### State-of-the-Art Advancement

- **First Practical Implementation:** MOSS appears to be first source-level self-rewriting for production agents
- **Strong Empirical Results:** 144% improvement on OpenClaw is significant
- **Safe Evolution:** Comprehensive validation prevents regressions
- **Generality:** Approach appears applicable across agent frameworks and domains

### Limitations and Open Questions

1. **Scalability of Failure Curation:** How does curation scale as failure database grows to millions of entries?
2. **LLM-Generated Code Quality:** Long-term reliability of LLM-generated patches unclear; potential subtle bugs
3. **Formal Verification Limits:** Can we provide formal guarantees that evolved agents maintain desired properties?
4. **Architecture Drift:** After many evolution cycles, does agent code degrade in maintainability?
5. **Adversarial Robustness:** Could adversary manipulate failure logs to inject malicious code?
6. **Human Understanding:** As code evolves, becomes harder for humans to understand and maintain

### Future Research Directions

1. **Formal Verification of Evolved Code:** Integrate formal methods to prove correctness of evolved agents
2. **Constrained Evolution:** Define explicit boundaries on how agents can modify themselves
3. **Interpretable Evolution:** Generate human-readable explanations for code changes
4. **Multi-Agent Coevolution:** Extend to systems where multiple agents evolve together
5. **Transfer Between Agents:** Learn fix patterns from one agent to improve others
6. **Hybrid Source-Prompt Evolution:** Combine code-level and prompt-level modifications strategically

---

## Code & Resources

### Official Repository
- **GitHub:** https://github.com/dav-joy-thon/MOSS
- **Paper PDF:** https://arxiv.org/pdf/2605.22794

### Dependencies and Compute Requirements

**Software Dependencies:**
- Python 3.10+
- LLM API access (Claude, GPT-4, or compatible)
- Agent framework (AgentCore, AutoGen, or custom)
- Code analysis tools: ast, type checking libraries
- Testing framework: pytest or similar

**Compute Requirements:**
- CPU: Standard compute sufficient for code generation and validation
- GPU: Optional (not required for evolution)
- Storage: 10GB+ for failure database (scales with deployment size)
- Network: API calls to LLM service

### Quick-Start Guide

```bash
# Clone repository
git clone https://github.com/dav-joy-thon/MOSS.git
cd MOSS

# Install dependencies
pip install -r requirements.txt

# Configure LLM API
export CLAUDE_API_KEY=sk-...
export LLM_MODEL=claude-opus-4.7

# Initialize failure collection
python init_failure_db.py \
    --agent_framework autogen \
    --data_dir ./agent_code

# Simulate failures (or deploy and collect real ones)
python collect_failures.py \
    --agent_path ./agent_code/agent.py \
    --test_cases ./test_cases.json \
    --output failures.json

# Run evolution cycle
python evolve.py \
    --agent_path ./agent_code/agent.py \
    --failures failures.json \
    --output_patch evolved.patch \
    --num_failures 30

# Apply patch
patch ./agent_code/agent.py < evolved.patch

# Validate improvements
python validate_evolution.py \
    --agent_path ./agent_code/agent.py \
    --failures failures.json
```

### Usage Example

```python
from moss import FailureCollector, EvolutionEngine

# 1. Deploy baseline agent and collect failures
collector = FailureCollector(agent=my_agent)
for test_case in test_suite:
    collector.run(test_case)

failures = collector.get_failures()  # List of FailureRecord

# 2. Run evolution
engine = EvolutionEngine(
    agent_code_path="./agent.py",
    llm_model="claude-opus-4.7",
    failure_batch_size=30
)

patch = engine.evolve(failures)

# 3. Validate and deploy
validated = engine.validate_patch(patch, test_suite)
if validated:
    engine.apply_patch(patch)
    print("Evolution successful! Agent improved.")
```

---

## Related Work & Context

### Related Recent Papers

1. **Self-Evolving Software Agents (2026):** Similar work on adaptive agent systems
2. **A Survey of Self-Evolving Agents (2024):** Comprehensive overview of agent adaptation approaches
3. **Lifelong Learning in Agents (2024):** Related work on continuous improvement
4. **Prompt Adaptation for LLMs (2024):** Related text-level evolution approaches

### Prior Work Foundations

1. **Self-Healing Software (various):** Earlier work on automated bug detection/fixing
2. **Program Synthesis (Gulwani et al.):** Foundation for code generation
3. **Automated Debugging (Le Goues et al.):** GenProg and related automated repair
4. **Reinforcement Learning from Failures:** Learning from negative experiences

### Possible Future Research Directions

1. **Formal Guarantees:** Prove that evolved agents maintain safety/performance invariants
2. **Explainability:** Generate human-interpretable explanations for code changes
3. **Distributed Evolution:** Multiple agents learning from shared failure pool
4. **Cross-Domain Transfer:** Learn fix patterns applicable across different agent types
5. **Preventive Evolution:** Predict failures before they occur and proactively fix
6. **Human-in-the-Loop Evolution:** Humans provide feedback on proposed changes before deployment
7. **Emergence Study:** Understand what capabilities emerge from repeated evolution cycles

---

## Summary and Takeaways

MOSS represents a fundamental advancement in autonomous system design by enabling code-level self-improvement without human intervention. The core insight—that source code is a more powerful and reliable medium for agent evolution than prompts or configurations—is theoretically sound and empirically validated.

The 144% performance improvement on OpenClaw, achieved through fully autonomous source-level rewriting, demonstrates that practical self-improving systems are achievable. This opens new possibilities for deploying agents in production with confidence that they will continue to improve as they encounter new edge cases and failure patterns.

The system's success depends on three key components working together:
1. **Intelligent failure curation** identifying which failures to prioritize
2. **Code-level generation** enabled by LLMs' strong code understanding
3. **Comprehensive validation** preventing regressions and ensuring safety

For practitioners, MOSS provides a blueprint for moving beyond static agent deployment. Instead of accepting fixed behavior until humans manually intervene, teams can deploy agents that autonomously identify and fix their own structural failures. This has implications far beyond the immediate agent domain—any system whose behavior is defined by code (robotics, scientific simulation, optimization systems) could benefit from source-level self-evolution.

The limitations are real: generated code may harbor subtle bugs, long-term code quality degradation is possible, and formal guarantees are difficult. But the potential benefits—continuous autonomous improvement of deployed systems—justify addressing these challenges through better validation, formal verification, and human oversight mechanisms.

As autonomous systems become increasingly prevalent, MOSS-like approaches for autonomous self-improvement will likely become essential infrastructure. The ability of agents to diagnose and fix their own failures without human intervention represents a critical step toward trustworthy, adaptive autonomous systems.
