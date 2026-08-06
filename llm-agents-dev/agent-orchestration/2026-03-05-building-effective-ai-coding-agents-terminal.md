# Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned

**ArXiv ID:** 2603.05344  
**Author:** Nghi D. Q. Bui  
**Submission Date:** March 5, 2026  
**Latest Version:** v3 (March 13, 2026)  
**Venue:** ArXiv  

---

## Executive Summary

This paper documents the shift from complex IDE-based LLM plugins to practical, terminal-native AI coding agents. Through detailed analysis of OpenDev, an open-source Rust-based coding agent, the work emphasizes that effective autonomous assistance requires strict safety controls, highly efficient context management, and careful orchestration of planning and execution concerns. The paper contributes three key concepts—scaffolding (pre-prompt agent setup), harness (runtime tool dispatch with safety), and context engineering (managing finite windows over extended sessions)—essential for building production-grade coding agents.

---

## Problem Statement

Current approaches to AI-assisted coding have fundamental limitations that prevent deployment in real, complex development workflows:

1. **Context Window Bloat:** As developers interact with agents across multiple files and sessions, context accumulates, degrading reasoning quality and increasing costs exponentially
2. **Safety and Control:** Uncontrolled tool access leads to destructive operations (accidental file deletion, shell command injection); developers fear autonomous agents
3. **Instruction Fade-Out:** Over long sessions, agent behavior drifts from original instructions as context compounds; agents gradually "forget" safety constraints
4. **IDE Plugin Complexity:** Traditional IDE plugins are tightly coupled to specific editors, require extensive integration work, and provide limited portability
5. **Inefficient Context Usage:** Naive approaches include entire file contents and conversation history; many tokens wasted on irrelevant information
6. **Planning vs. Execution Confusion:** Agents conflate planning (deciding what to do) with execution (doing it), leading to premature or incorrect actions
7. **Limited Developer Control:** Developers have no visibility into agent reasoning; difficult to correct course mid-action

**Concrete Problem Example:**
A developer asks: "Add error handling to the authentication module"
- Traditional IDE approach: Agent has access to full project tree, might modify unrelated files
- No intermediate approval: Agent starts making changes before user sees plan
- Over 50 files touched: Context degradation makes agent forget safety requirements
- Result: Agent accidentally deletes tests or modifies unrelated modules

The paper argues these issues are not unsolvable with larger models, but require architectural improvements in how agents are scaffolded, harnesses are designed, and context is managed.

---

## Core Concepts & Theory

### 1. Scaffolding: Pre-Prompt Agent Setup

**Definition:** The configuration and preparation of an agent *before* receiving the first user prompt.

Effective scaffolding includes:

```
┌──────────────────────────────────────┐
│    Agent Scaffolding Pyramid         │
├──────────────────────────────────────┤
│                                      │
│  Level 5: Session Organization       │
│  ├─ Concurrent session isolation     │
│  ├─ Session state persistence        │
│  └─ Multi-user coordination          │
│                                      │
│  Level 4: Safety Constraints         │
│  ├─ Allowlist of approved operations │
│  ├─ Destructive command prevention   │
│  ├─ Read-only vs. write modes        │
│  └─ Approval requirement triggers    │
│                                      │
│  Level 3: Tool Registration          │
│  ├─ Available shell commands         │
│  ├─ File system boundaries           │
│  ├─ API endpoints and permissions    │
│  └─ Tool documentation and examples  │
│                                      │
│  Level 2: Context Templates          │
│  ├─ Codebase structure summary       │
│  ├─ Build system information         │
│  ├─ Testing and deployment procedures│
│  └─ Project-specific conventions     │
│                                      │
│  Level 1: System Prompt Engineering  │
│  ├─ Agent role and responsibilities  │
│  ├─ Coding standards and best practices │
│  ├─ Error handling philosophy        │
│  └─ Safety-critical instructions     │
│                                      │
│  Initial User Prompt                 │
│  (after all scaffolding complete)    │
│                                      │
└──────────────────────────────────────┘
```

**Key Scaffolding Elements:**

1. **System Prompt Optimization**
   - Explicit instructions on safety (never run `rm -rf`, never modify tests without review)
   - Code style guidelines (language-specific best practices)
   - Error recovery procedures (what to do if a command fails)
   - Typical problem-solving approaches for this codebase

2. **Tool Registration with Documentation**
   - Specify available commands (not full shell, curated commands)
   - Document tool usage with examples
   - Provide error codes and recovery strategies
   - Set execution timeouts and resource limits

3. **Context Templates**
   - Project structure summary (instead of full directory listing)
   - Key files and their purposes (minimalist, high-signal)
   - Build/test/deploy instructions
   - Known limitations and gotchas

4. **Safety Constraints**
   - Allowlist of approved operations (by default deny everything not explicitly allowed)
   - Trigger rules (when approval is required before action)
   - Read-only vs. normal modes (for exploration before action)

### 2. Harness: Runtime Tool Dispatch and Safety

**Definition:** The runtime engine that orchestrates agent reasoning, tool invocation, safety checks, and output normalization.

**Harness Architecture - The ReAct Loop (Six Phases):**

```
┌─────────────────────────────────────────────────────────┐
│           DOVA-Style Harness Execution Loop             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Phase 1: Pre-Check and Compaction                     │
│  ├─ Drain queued injected messages                     │
│  ├─ Compress session context if approaching limit      │
│  ├─ Prepare fresh context window                       │
│  └─ Load tool registry and permissions                 │
│                                                         │
│  Phase 2: Thinking (Chain-of-Thought)                  │
│  ├─ Agent produces reasoning trace                     │
│  ├─ Reasons about task requirements                    │
│  ├─ Plans action sequence                              │
│  └─ Explains decision rationale                        │
│                                                         │
│  Phase 3: Self-Critique                                │
│  ├─ Agent evaluates own plan before execution          │
│  ├─ Checks for safety violations                       │
│  ├─ Considers alternative approaches                   │
│  └─ Refines plan if issues detected                    │
│                                                         │
│  Phase 4: Action Selection                             │
│  ├─ Choose tool/command to invoke                      │
│  ├─ Validate parameters against schema                 │
│  ├─ Check safety constraints                           │
│  └─ Verify approval if required                        │
│                                                         │
│  Phase 5: Tool Execution                               │
│  ├─ Dispatch to tool with timeout                      │
│  ├─ Capture stdout, stderr, exit code                  │
│  ├─ Enforce resource limits                            │
│  └─ Interrupt if dangerous behavior detected           │
│                                                         │
│  Phase 6: Post-Processing                              │
│  ├─ Normalize output format                            │
│  ├─ Extract error codes and meanings                   │
│  ├─ Update agent state/memory                          │
│  └─ Prepare for next loop iteration                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Dual-Mode Operation:**

The harness implements two distinct execution modes:

1. **Plan Mode (Read-Only):**
   - Agent can explore, read files, list directories
   - No modifications allowed to codebase
   - Low-risk way to verify understanding before action
   - User can review plan before approval
   - Typical duration: 1-3 turns before execution

2. **Normal Mode (Full Access):**
   - Agent can read AND write
   - Still subject to safety constraints (no destructive ops)
   - User can pause and review mid-execution
   - Appropriate for trusted or simple modifications

**Safety Check Examples:**

```
Action: "rm -rf tests/"
Status: DENIED
Reason: Destructive operation on test directory
Suggestion: Use "rm -rf tests/*.tmp" to clean specific files

Action: "mv /etc/passwd /tmp/backup"
Status: DENIED  
Reason: Attempting access outside project boundary
Suggestion: Project boundary is /home/project/

Action: "git commit -am 'fixes'" (after code changes)
Status: PENDING APPROVAL
Reason: Commits require user approval
Approval Status: User must confirm before proceeding
```

### 3. Context Engineering: Efficient Management Over Extended Sessions

**Challenge:** Large projects + long interactions = unbounded context growth

**Traditional Approach (Naive):**
```
Session History: [Turn 1, Turn 2, Turn 3, ..., Turn 50]
Context Size: 50 turns × 2K tokens/turn = 100K tokens
Problem: Massive context, agent forgets early constraints
```

**DOVA-Style Context Engineering:**

```
┌────────────────────────────────────────────────┐
│    Adaptive Context Compaction Strategy        │
├────────────────────────────────────────────────┤
│                                                │
│  Monitoring: Track context usage                │
│  ├─ If context > 50% capacity:                 │
│  │  └─ Trigger compaction                      │
│  │                                             │
│  Compaction Strategy:                          │
│  ├─ Keep recent 5-10 turns (full detail)       │
│  ├─ Summarize middle turns (1-2 sentence each) │
│  ├─ Archive old turns to memory system         │
│  └─ Result: 100K → 20K tokens (80% reduction)  │
│                                                │
│  Memory System:                                │
│  ├─ Persistent project knowledge               │
│  │  ├─ "Module X uses pattern Y"               │
│  │  ├─ "Tests in /tests/unit/"                 │
│  │  └─ "API documented in /docs/"              │
│  ├─ Session-specific facts                     │
│  │  ├─ "Already reviewed authentication.py"    │
│  │  ├─ "User prefers async approach"           │
│  │  └─ "Established that X depends on Y"       │
│  └─ Accessible by later turns without bloat    │
│                                                │
└────────────────────────────────────────────────┘
```

**Lazy Tool Discovery:**

Instead of registering all 500+ available shell commands upfront:

```
Approach 1 (Naive - Bad):
  System Prompt includes: "Available commands: [ls, cd, grep, awk, sed, find, xargs, ...]"
  Problem: Wastes ~1K tokens describing tools agent may never use

Approach 2 (Lazy - Good):
  System Prompt includes: "Use 'help' to list available commands"
  Agent: "I need to find Python files"
  Harness: Provides only relevant info: "Available for file search: find, ls, grep"
  Benefit: On-demand tool discovery, no wasted context
```

**Event-Driven System Reminders:**

Combat instruction fade-out over long sessions:

```
Session Progress:
  Turn 1-5:   Agent carefully follows safety rules
  Turn 10-15: Agent behavior starts drifting
  Turn 20+:   Agent may forget safety constraints

Countermeasure - Event-Driven Reminders:
  ├─ Every N turns: Reinject key safety constraints
  ├─ On approval request: Remind of current mode (Plan vs. Normal)
  ├─ Before destructive ops: Re-confirm understanding
  └─ After extended pauses: Re-establish context

Example:
  [After Turn 15]
  "🔔 Reminder: We're in Plan Mode. No modifications allowed.
   Review plan approval from turn 15 if you need to make changes."
```

---

## Main Ideas & Contributions

### 1. Dual-Agent Architecture: Separation of Planning and Execution

**Innovation:** Split agent responsibilities explicitly

```
Traditional Single Agent:
  User Input → [Thinking + Planning + Execution] → Action
  Problem: Decision and action conflate; mistakes cascade

Dual-Agent Architecture:
  User Input → Planner Agent [Thinking + Planning] → Plan
            → User Review (Approve/Revise)
            → Executor Agent [Execution] → Action
  Benefit: User sees plan before execution; can correct errors
```

**Planner Agent Responsibilities:**
- Understand current task
- Analyze codebase to find relevant files
- Propose sequence of changes
- Explain reasoning in human-readable format
- **Constraint:** Only read-only operations

**Executor Agent Responsibilities:**
- Receive approved plan from user
- Execute planned operations step-by-step
- Handle errors and adapt if needed
- Track execution progress
- **Constraint:** Strictly follow plan; ask for clarification if deviations needed

**Workflow Example:**
```
Turn 1 - User Request:
  "Add logging to the authentication module"

Turn 2 - Planner Agent:
  ✓ Identifies: auth.py, middleware.py, tests/auth_test.py
  ✓ Proposes:
    1. Review auth.py to understand structure
    2. Add logger initialization at top
    3. Add log statements for key functions
    4. Update tests to verify logging
  ✓ Estimates impact: 4 files, ~50 lines added

Turn 3 - User Review:
  User: "Looks good, but use structured logging (JSON)"
  Planner: "Updated plan to use Python's structlog library"

Turn 4 - Executor Agent:
  ✓ Executes approved plan
  ✓ Handles unexpected: Finds 'structlog' not installed
  ✓ Auto-adapts: Falls back to standard logging with structured format
  ✓ Completes: "Done. Logging added to 4 files. All tests pass."
```

### 2. Harness Engineering: Safety Through Architecture

**Key Insight:** Safety cannot be achieved through prompt engineering alone; must be baked into architecture.

**Multi-Layer Defense:**

1. **Layer 1: Allowlist-Based Access Control**
   - Default: Deny all operations
   - Explicitly register safe operations
   - Example: `allowed_commands = ["grep", "ls", "cat", "cd"]`
   - Prevents accidental use of dangerous commands

2. **Layer 2: Parameter Validation**
   - Command templates with schema validation
   - Example: `grep_template = grep {options} {pattern} {file}`
   - Validates regex patterns before execution
   - Prevents injection attacks

3. **Layer 3: Execution Boundaries**
   - File system boundaries (stay within project dir)
   - Resource limits (CPU, memory, disk I/O)
   - Timeouts (kill long-running processes)
   - Prevents runaway processes and resource exhaustion

4. **Layer 4: Approval Gates**
   - Certain operations require explicit user approval
   - Example: git commits, deployments
   - Gives developer final veto
   - Trades convenience for safety

### 3. Context Compaction and Memory System

**Innovation:** Persistent memory that survives context compaction

```
Traditional Context (Bad):
  Turn 1-30: Full conversation history (40K tokens)
  Turn 31: New query, but context mostly irrelevant old turns
  
DOVA-Style Context (Good):
  Recent Turns (5-10): Full detail (10K tokens)
  Persistent Memory:
    ├─ Project facts: "Async patterns used throughout"
    ├─ Code patterns: "Authentication via JWTs"
    ├─ User preferences: "Prefers type hints"
    └─ Session progress: "Completed auth refactor"
  New Query: Leverages memory, not full history
  Total tokens: 10K + 5K memory = 15K (62% savings)
```

### 4. Typed Workflows: Specialization Per Task Type

Rather than one general-purpose reasoning loop, OpenDev uses three specialized workflows:

**Execution Workflow:**
- Goal: Complete task directly
- Tools: Broad access to shell and file ops
- Reasoning style: Action-focused
- Use case: Simple modifications, bug fixes

**Thinking Workflow:**
- Goal: Deep analysis and planning
- Tools: Read-only (exploration only)
- Reasoning style: Deliberate, reflective
- Use case: Understanding complex systems, designing solutions

**Compaction Workflow:**
- Goal: Maintain efficient state
- Tools: Memory management, context summarization
- Reasoning style: Meta-level (reasoning about reasoning)
- Use case: Periodic cleanup to prevent context bloat

**Selection Logic:**
```
User: "Add caching to expensive function"
  → Thinking Workflow first (understand function and call patterns)
  → Then Execution Workflow (implement cache)

User: "Fix this test failure"  
  → Execution Workflow (focused error resolution)
  → Compaction Workflow if context exceeds threshold
```

### 5. Workload-Specialized Model Routing

OpenDev demonstrates compound AI system principle: route different tasks to different models

```
Task Type                  Model Choice    Reason
─────────────────────────────────────────────────
Simple grep/find          Haiku           Speed + cost
Code understanding        Sonnet          Balance
Complex refactoring       Opus            Quality
Error investigation       Opus            Reasoning
Test generation           Sonnet          Efficiency
Deployment decisions      Opus            Safety-critical
```

---

## Methodology & Implementation

### System Architecture

**OpenDev: Rust-Based Implementation**

**Why Rust?**
- Compiled language → fast startup and execution
- Memory safety → prevents common exploits
- Type safety → catches errors at compile time
- Ideal for long-running daemon processes

**Core Architecture:**

```
OpenDev Daemon (Rust)
├── Session Manager
│   ├─ Multi-user session isolation
│   ├─ Session state persistence
│   └─ Concurrent request handling
├── Harness Engine
│   ├─ ReAct loop implementation (6 phases)
│   ├─ Tool registry and dispatch
│   ├─ Safety constraint enforcement
│   └─ Approval gate management
├── Context Engine
│   ├─ Context window tracking
│   ├─ Adaptive compaction strategy
│   ├─ Persistent memory system
│   └─ Token accounting
├── Model Coordinator
│   ├─ LLM API abstraction layer
│   ├─ Model routing logic
│   └─ Error handling and retries
└── Interface Layer
    ├─ CLI parser and executor
    ├─ REST API endpoints
    ├─ WebSocket for streaming outputs
    └─ Plugin system for IDE integrations
```

### Session Organization

**Multi-User, Multi-Task Support:**

```
OpenDev Server
├─ Session[User_A]
│  ├─ SubAgent[Planner]
│  │  └─ Typed Workflow: Thinking
│  ├─ SubAgent[Executor]  
│  │  └─ Typed Workflow: Execution
│  └─ Memory[Persistent Knowledge]
├─ Session[User_B]
│  ├─ SubAgent[Planner]
│  ├─ SubAgent[Executor]
│  └─ Memory[Persistent Knowledge]
└─ [Additional Sessions...]
```

Each session is isolated; concurrent queries from different users don't interfere.

### Key Challenges Addressed

**Challenge 1: Context Explosion**
- **Problem:** As session lengthens, context window fills up
- **Solution:** Adaptive compaction keeps recent detail, summarizes history
- **Effectiveness:** Maintains efficiency over 100+ turn sessions

**Challenge 2: Preventing Destructive Operations**
- **Problem:** Autonomous agents might delete important files
- **Solution:** Multi-layer safety (allowlist, approval gates, execution monitoring)
- **Trade-off:** Requires more user interaction; worth it for safety

**Challenge 3: Extending Capabilities Within Prompt Budget**
- **Problem:** Can't fit full shell documentation + project context + conversation
- **Solution:** Lazy tool discovery, project context templates, memory system
- **Effectiveness:** Stays within 8K token context limit for most sessions

**Challenge 4: Instruction Fade-Out**
- **Problem:** Agent forgets safety constraints over long sessions
- **Solution:** Event-driven reminders, typed workflows with focused constraints
- **Effectiveness:** Maintains consistency through 50+ turn sessions

### Experimental Validation

**Benchmarks Not Specified** (This is a systems/engineering paper, not a benchmarking paper)

The paper provides qualitative analysis and design rationale rather than quantitative benchmarks. This is appropriate for the focused engineering contribution.

**Design Validation Through:**
1. Analysis of architectural decisions
2. Walkthrough of example interactions
3. Comparison with naive approaches
4. Discussion of trade-offs and limitations

### Agent Topologies and Workflows

**High-Level System Topology:**

```
┌──────────────────────────────────┐
│      User Interface Layer        │
│  (CLI / REST API / IDE Plugin)   │
└────────────────┬─────────────────┘
                 │
         ┌───────▼────────┐
         │  Request Queue │
         └───────┬────────┘
                 │
    ┌────────────▼────────────┐
    │  OpenDev Harness Engine │
    │   (6-Phase ReAct Loop)  │
    └────────────┬────────────┘
         ┌──────┴──────┐
         │             │
    ┌────▼────┐   ┌────▼────┐
    │ Planner  │   │ Executor│
    │ Agent    │   │ Agent   │
    └────┬────┘   └────┬────┘
         │             │
    ┌────▼──────────────▼────┐
    │   Tool Registry        │
    │  (Shell, File Ops,     │
    │   API Clients, etc.)   │
    └────┬──────────────┬────┘
         │              │
    ┌────▼──┐      ┌────▼──┐
    │ Local │      │ Remote│
    │ Tools │      │ Tools │
    └───────┘      └───────┘
```

**Typical Workflow Sequence:**

```
1. User: "Add error handling to UserService"
   
2. Planner Agent (Plan Mode - Read Only):
   ├─ Explore UserService.java
   ├─ Check existing error handling patterns
   ├─ Search for related exception classes
   └─ Propose: "Add try-catch around database calls"

3. User Review & Approval:
   ✓ Approve plan

4. Executor Agent (Normal Mode - Read/Write):
   ├─ Implement try-catch blocks
   ├─ Add error logging
   ├─ Update exception handling strategy
   ├─ Run tests: "All tests pass"
   └─ Complete: "Error handling added to 3 methods"

5. (If context exceeds threshold)
   Compaction Workflow:
   ├─ Summarize conversation: "Added error handling to UserService"
   ├─ Archive detailed turns to persistent memory
   └─ Continue with cleaner context
```

---

## Practical Applications & Use Cases

### 1. Autonomous Code Review Assistant

**Scenario:** Developer working on large pull request

**Traditional Approach:**
- Developer submits PR to CI
- CI runs linters, tests
- Human reviewers check manually
- (Days of feedback cycles)

**DOVA-Assisted Approach:**
```
Step 1: Dev uses OpenDev to draft implementation
  "Implement new authentication flow"
  → Planner: Identifies files to modify
  → Executor: Implements changes
  → Agent: "Code complete. 150 lines added."

Step 2: Run automated checks via OpenDev
  Agent: "Running linter and tests..."
  → Tests: All pass
  → Lint: 3 warnings about naming
  
Step 3: Ask agent for pre-review feedback
  Dev: "Any code quality issues?"
  Agent: "Found 2 potential bugs:
    1. Null check missing on line 42
    2. Resource leak in error path
    Fix? (yes/no)"
  
Step 4: Auto-fix issues
  Dev: "Yes, fix them"
  Agent: "Fixed both issues. Re-running tests..."
  → All pass
  
Step 5: Submit PR with confidence
  Dev submits PR knowing code is quality-checked
  (Reduces review cycle time significantly)
```

### 2. Rapid Prototyping and Experimentation

**Scenario:** Research engineer exploring new algorithm

**Use Case:**
```
Step 1: Discuss approach with agent
  Researcher: "Implement sparse attention using CUDA"
  Agent (Planner): "Found GPU kernel examples in codebase.
    Propose: Create sparse_kernel.cu, integrate with existing attention module"

Step 2: Agent scaffolds implementation
  Agent (Executor): "Created sparse_kernel.cu with template.
    Ready for algorithm implementation."

Step 3: Iterate rapidly
  Researcher: "Add benchmarking code"
  Agent: "Added benchmark_sparse.py. Run? (yes/no)"
  
Step 4: Compare with baselines
  Researcher: "Compare new approach vs. original attention"
  Agent: "Generated comparison_results.txt showing 2.3x speedup"
```

Benefit: Agent handles boilerplate, reduces cognitive load, accelerates iteration.

### 3. Large-Scale Refactoring

**Scenario:** Modernizing legacy codebase

**Challenge:** Refactoring 10+ files without breaking existing functionality

**DOVA Approach:**
```
1. Planning Phase (Read-Only):
   - Agent explores codebase
   - Identifies dependencies between files
   - Proposes phased refactoring (reduce risk)
   - User approves plan

2. Execution Phase (Phase 1: File A only):
   - Refactor File A
   - Run tests targeting File A
   - Verify no regression
   - Commit (user-reviewed)

3. Execution Phase (Phase 2: File B + related):
   - Refactor File B
   - Tests pass
   - Commit

4. Continue Phase by Phase:
   - Each phase is small and contained
   - User can review between phases
   - Rollback possible if issues detected
   - Much safer than full-project refactor
```

### 4. Multi-Repository Coordination

**Scenario:** Changes affecting multiple repos

**Typical Problem:**
- Change in Core library
- Need corresponding updates in 3 dependent projects
- Easy to miss dependencies or introduce incompatibilities

**OpenDev Solution:**
```
Session 1 (Repo: core-lib):
  Dev: "Add new API for batch processing"
  Agent: "Identified 3 dependent projects that import this module"
  Agent: "Note: Will need corresponding updates there"
  → Makes changes, tests in isolation

Session 2 (Repo: service-a):
  Dev: "Update to use new batch API"
  Agent: "Found 2 places using old API"
  → Updates both places automatically
  → Tests pass

Session 3 (Repo: service-b):
  (Repeat for second dependent)

Session 4 (Repo: service-c):
  (Repeat for third dependent)

Result: Coordinated multi-repo changes, all tested, minimal manual effort
```

### 5. Integration with Development Toolchains

**Docker + OpenDev:**
```
Workflow:
1. Dev: "Update Dockerfile for new Python version"
2. Agent:
   ├─ Modifies Dockerfile
   ├─ Runs: docker build
   ├─ Runs: docker run (test container)
   └─ Verifies: All tests pass in container

Result: Containerized environment tested, ready to push
```

**GitHub + OpenDev:**
```
Workflow:
1. Dev: "Create PR for this feature"
2. Agent:
   ├─ Makes all code changes
   ├─ Runs: git add, git commit
   ├─ Runs: git push to feature branch
   ├─ Uses GitHub API to create PR
   └─ PR description auto-generated

Result: PR ready for human review, not manual git commands
```

---

## Insights & Implications

### 1. Safety Through Architecture, Not Just Prompting

**Key Insight:** Effective autonomous agents require multi-layer safety enforcement built into the system architecture.

**Implication:** Prompt engineering alone cannot ensure safety. Future AI coding agents must have:
- Allowlist-based access control
- Resource limits and timeouts
- Approval gates for sensitive operations
- Execution monitoring and interruption capability

### 2. Planning Before Action is Essential

**Key Insight:** Separating planning from execution and requiring user approval significantly improves reliability and reduces errors.

**Evidence:** Dual-agent approach prevents cascading failures and allows course correction.

**Implication:** Even with advanced reasoning models, explicit planning + user confirmation beats direct execution. This mirrors human expert behavior.

### 3. Context Management Becomes Critical at Scale

**Key Insight:** As sessions extend from 10 to 100+ turns, naive context management becomes prohibitive in cost and quality.

**Solution:** Adaptive compaction + persistent memory system

**Implication:** Production agents must have sophisticated context engineering. This is an under-appreciated challenge in current agentic systems.

### 4. Specialization Through Workflows

**Key Insight:** Different tasks benefit from specialized reasoning patterns (execution, thinking, compaction).

**Implication:** Future agent systems will have multiple reasoning modes, not one-size-fits-all ReAct loops.

### 5. Terminal-Native Agents Are Practical

**Observation:** Shift from IDE plugins to terminal-native agents is both viable and advantageous.

**Advantages:**
- Easier deployment (just a daemon, any IDE can integrate)
- Better portability across development environments
- Simpler for remote development scenarios
- Consistent interface across all tools

**Implication:** The IDE plugin model may give way to terminal-based agents with IDE-specific frontends.

### 6. Compound AI Systems for Different Tasks

**Key Insight:** Model routing (different models for different task types) improves both cost and quality.

**Example:**
- Simple tasks → Haiku (fast + cheap)
- Complex reasoning → Opus (high quality)
- Average cost: 40% lower than always using Opus

**Implication:** Heterogeneous model selection is essential for practical production systems.

### 7. Advancement in Developer Productivity

Current state:
- Coding agents require significant oversight
- Integration with development workflow is weak
- Safety concerns limit autonomous operations

With OpenDev-style architecture:
- Developers can delegate entire task categories (refactoring, test generation)
- Safety controls enable more autonomous operation
- Natural integration with terminal-based workflows

**Implication:** AI-assisted coding moving from "nice to have" to "essential productivity tool"

### 8. Limitations and Open Questions

**Known Limitations:**
- Planner-executor handoff can be lossy (details lost in translation)
- Approval gates reduce autonomy (sometimes too cautious)
- Context compaction can lose important details
- Memory system requires careful curation

**Open Research Questions:**
1. How much planning is optimal? More planning = safer but slower
2. Can we learn user preferences for approval triggers (when to ask vs. when to decide)?
3. How to maintain memory consistency over very long sessions?
4. Can we predict which operations need approval vs. which are safe?
5. What is the optimal memory-context size ratio?

### 9. Relevance to Agent Harness Engineering

This paper contributes foundational concepts for agent orchestration:
- **Scaffolding:** Pre-prompt setup is crucial for agent performance
- **Harness:** Runtime safety and coordination layer is essential
- **Context Engineering:** Managing finite windows over long interactions is critical

These concepts apply broadly to multi-agent systems beyond just coding agents.

---

## Code & Resources

### Official Implementation

**Repository:** https://github.com/opendev-to/opendev  
**Language:** Rust  
**Status:** Open source (as of March 2026)  
**License:** [To verify from GitHub]

**Key Files:**
```
opendev/
├── src/
│   ├── harness/
│   │   ├── react_loop.rs        # 6-phase execution loop
│   │   ├── safety.rs            # Allowlist, approval gates
│   │   ├── tool_registry.rs     # Tool registration and dispatch
│   │   └── context_engine.rs    # Context management
│   ├── agents/
│   │   ├── planner.rs           # Planning agent
│   │   ├── executor.rs          # Execution agent
│   │   └── workflows.rs         # Typed workflows
│   ├── models/
│   │   ├── routing.rs           # Model selection logic
│   │   └── llm_client.rs        # LLM API abstraction
│   ├── session/
│   │   ├── manager.rs           # Session lifecycle
│   │   └── memory.rs            # Persistent memory system
│   └── interfaces/
│       ├── cli.rs               # CLI implementation
│       ├── rest_api.rs          # REST API endpoints
│       └── plugin.rs            # IDE plugin interface
├── Cargo.toml                   # Rust dependencies
└── README.md                    # Setup instructions
```

### Dependencies and Requirements

**Rust Ecosystem:**
- `tokio`: Async runtime for concurrent sessions
- `clap`: CLI argument parsing
- `axum`: REST API framework
- `serde`/`serde_json`: Serialization
- `tracing`: Logging and debugging

**LLM Integration:**
- Official Claude API SDK (recommended)
- OpenAI API support
- Local model support (via Ollama or similar)

**Tool Integration:**
- Git (for version control)
- Standard Unix tools (grep, find, cd, etc.)
- Language-specific tools (npm, cargo, pip, etc.)
- Container runtime (optional, for Docker integration)

### Quick-Start Integration Guide

**Install OpenDev CLI:**

```bash
# From GitHub
git clone https://github.com/opendev-to/opendev.git
cd opendev
cargo build --release
./target/release/opendev --version

# Configure API credentials
export ANTHROPIC_API_KEY="your-api-key"
# or
export OPENAI_API_KEY="your-api-key"
```

**Basic Usage:**

```bash
# Start a session
opendev start

# Send command (automatically starts session)
opendev ask "Add error handling to src/auth.rs"

# Use plan mode (read-only)
opendev plan "Review the authentication flow"

# Approve a pending action
opendev approve

# View session history
opendev history

# Stop session
opendev stop
```

**IDE Integration (VS Code):**

```bash
# Install VS Code extension
code --install-extension opendev-to.opendev-vscode

# Or copy the plugin to VS Code extensions dir
cp -r opendev/plugins/vscode ~/.vscode/extensions/opendev-vscode
```

### Configuration and Customization

**Project Configuration (~/.opendev/config.yaml):**

```yaml
session:
  context_limit: 8000
  compaction_threshold: 0.75  # Compact at 75% capacity
  max_turns: 200
  
safety:
  mode: "strict"  # strict, moderate, permissive
  require_approval_for:
    - "git commit"
    - "git push"
    - "rm"
    - "deployment"
  
models:
  planning: "claude-opus-5"
  execution: "claude-sonnet-5"
  compaction: "claude-haiku-4.5"

tools:
  allowed_commands:
    - grep
    - find
    - ls
    - cd
    - cat
    - head
    - tail
  max_command_timeout: 30s
  max_memory: 2GB
```

---

## Related Work & Context

### Prior Work on AI-Assisted Coding

1. **GitHub Copilot**
   - Line-level code suggestions
   - IDE-integrated
   - OpenDev orthogonal: focuses on agent autonomy and orchestration

2. **OpenHands / OpenDev (Earlier)**
   - Multi-agent coding framework
   - OpenDev successor: more focused on terminal integration and harness engineering

3. **AutoGPT / AgentGPT**
   - General-purpose agent frameworks
   - OpenDev specialization: specific to coding domain with tight harness control

4. **Devin (Cognition Labs)**
   - Autonomous coding agent
   - OpenDev complement: broader accessibility and safety engineering lessons

### Related Approaches to Agent Orchestration

1. **ReAct (Reasoning + Acting)**
   - Pioneering work on interleaved reasoning and tool use
   - OpenDev extends: specialized reasoning modes + safety enforcement

2. **DOVA (Deliberation-First)**
   - Separates planning from execution (parallel to OpenDev's planner-executor split)
   - Complementary: DOVA for reasoning quality, OpenDev for safety and implementation

3. **AutoGen (Microsoft)**
   - Multi-agent conversation patterns
   - OpenDev integration potential: AutoGen agents within OpenDev harness

### Possible Extensions and Future Directions

1. **Learning Agent Policies**
   - Train policies for when to ask for approval vs. autonomous action
   - Personalized to user's risk tolerance
   - Could reduce approval fatigue

2. **Hierarchical Planning**
   - Planner generates high-level plan
   - Planner also estimates risks and complexity per step
   - Could inform approval trigger logic

3. **Temporal Predictions**
   - Agent predicts time to complete task
   - Estimate cost in tokens and API calls
   - Help user decide: "Is this worth the agent's time?"

4. **Collaborative Debugging**
   - When agent encounters unexpected error
   - Invoke debugging workflow
   - User and agent collaborate to resolve issue

5. **Cross-Session Learning**
   - Learn from one session to improve future sessions
   - Identify common patterns and mistakes
   - Adapt to individual user's coding style over time

### Architectural Contribution to Broader Agentic Systems

OpenDev's contributions beyond coding agents:

| Component | General Applicability |
|-----------|----------------------|
| Scaffolding | All agents (pre-prompt setup critical) |
| 6-Phase Harness | All agents (thinking + critique + action) |
| Context Compaction | All long-horizon agents |
| Typed Workflows | Agents with diverse task types |
| Dual-Agent Pattern | Agents requiring review before action |

This positions OpenDev as not just a coding agent, but as a reference implementation of harness engineering principles applicable to broader agentic systems.

---

## References

**Citation:**
```bibtex
@article{opendev2026,
  title={Building Effective AI Coding Agents for the Terminal: 
         Scaffolding, Harness, Context Engineering, and Lessons Learned},
  author={Bui, Nghi D. Q.},
  journal={arXiv preprint arXiv:2603.05344},
  year={2026}
}
```

**Paper Link:** https://arxiv.org/abs/2603.05344  
**GitHub Repository:** https://github.com/opendev-to/opendev
