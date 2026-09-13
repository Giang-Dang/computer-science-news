# PreAct: Computer-Using Agents that Get Faster on Repeated Tasks

**Authors:** Bojie Li, and colleagues  
**Submitted:** June 16, 2026  
**ArXiv ID:** [2606.17929](https://arxiv.org/abs/2606.17929)

## Executive Summary

PreAct introduces a novel approach to optimizing computer-using agents through automated compilation of successful task executions into lightweight state-machine programs. When an agent successfully completes a task, PreAct extracts the state transitions and action sequences into a replayable program that, on subsequent executions of the same task, can be replayed 8.5-13x faster without invoking the language model at each step. The replay mechanism includes adaptive screen validation—checking that observed screen states match expectations at each step—enabling graceful handling of environmental changes while maintaining dramatic speedup. This approach bridges theory and practice for agent efficiency, transforming the typical "solve from scratch" paradigm into an "execute cached program" paradigm for repeated tasks.

## Problem Statement

### The Repeated Task Inefficiency Challenge

Current computer-using agents face a fundamental inefficiency when encountering repeated tasks:

```
Traditional Agent Behavior on Repeated Tasks:

Task 1 (e.g., "Book a flight to Tokyo"):
├── Read full screen content
├── Reason about every UI element
├── Make reasoning-based decision for each action
├── Execute tap/type action
├── Repeat for ~10-20 steps
└── Total latency: 30-60 seconds, ~15-20 LLM calls

Task 2 (same "Book a flight to Tokyo" 2 days later):
├── Read full screen content (again)
├── Reason about every UI element (again)
├── Make reasoning-based decision for each action (again)
├── Execute tap/type action
├── Repeat for ~10-20 steps
└── Total latency: 30-60 seconds (again), ~15-20 LLM calls (again)
```

**Inefficiency:** Identical reasoning work performed redundantly; no learning or caching of previous successes.

### Why Existing Approaches Fail

1. **No Structured Capture:** Successful executions aren't captured in any systematic way
2. **Full Reasoning Every Time:** Each step requires fresh LLM reasoning regardless of prior success
3. **Environmental Sensitivity:** Any screen change forces complete re-execution of reasoning
4. **No Replay Mechanism:** Unlike APIs with caching, UI automation has no standard replay infrastructure

### Real-World Impact

For deployed systems handling user requests:
- Flight booking agents repeat identical booking sequences dozens of times per day
- Calendar agents navigate identical application menus repeatedly
- Administrative tools perform identical configuration sequences regularly
- Typical applications see 20-40% request overlap in production

## Core Concepts & Theory

### The State-Machine Compilation Approach

PreAct captures task execution as a deterministic state machine:

```
Successful Execution Sequence:
  Step 1: Screen State A ──[action: tap(element1)]──> Screen State B
  Step 2: Screen State B ──[action: type("Tokyo")]──> Screen State C
  Step 3: Screen State C ──[action: tap(search)]──> Screen State D
  ...
  Step N: Screen State X ──[action: tap(confirm)]──> Screen State Y (Success)

Compiled Program:
  State: {
    "current": A,
    "expected_signature": hash(A.elements, A.text_content),
    "action": "tap(element1)",
    "next_state": B
  },
  ...
```

### Replay Protocol with Adaptive Validation

Unlike naive replay which assumes static environments, PreAct uses adaptive validation:

```
Replay Execution with Validation:

at_step_i:
  ├── Read current screen state
  ├── Compute current_signature = hash(screen_elements, text)
  ├── Compare: expected_signature vs current_signature
  ├── If match:
  │   ├── Execute cached action
  │   ├── Proceed to step i+1
  │   └── No LLM invocation needed
  ├── If mismatch:
  │   ├── Environment has changed!
  │   ├── Revert to full LLM reasoning
  │   ├── Break out of replay
  │   └── Continue with fallback agent
  └── If timeout/error:
      ├── Similar error handling as mismatch
      └── Fallback to full reasoning
```

### Efficiency Gains Analysis

```
Cost Model:

Traditional approach:
  Cost = N × (screen_read + LLM_inference + action_execute)
  Typical: 20 steps × (0.5s + 2s + 0.1s) = ~53 seconds

PreAct replay approach:
  Cost = N × (screen_read + hash_compute + action_execute) + 1 × LLM_inference
  Typical: 20 × (0.5s + 0.01s + 0.1s) + 2s = ~14 seconds
  Speedup: 53s / 14s ≈ 3.8x

Faster LLM APIs:
  PreAct: 20 × 0.61s + 1s = ~13s (Gemini API: 200ms/call)
  Speedup: 53s / 13s ≈ 4.1x

With model improvements:
  Projected: 8-13x with continued inference optimization
```

### Key Technical Properties

1. **Determinism:** Cached programs execute deterministically (no randomness in replay)
2. **Graceful Degradation:** Mismatches trigger fallback rather than failure
3. **Locality:** Each state transition validates only immediate context
4. **Composability:** Can chain multiple cached programs for complex workflows

## Main Ideas & Contributions

### 1. Task Execution as Compilation

Novel framing of computer-use task execution:
- **Successful execution = program** that encodes decision sequence
- **Compilation = extraction** of state transitions from execution trace
- **Replay = efficient reexecution** with minimal reasoning overhead

### 2. Signature-Based State Validation

Robust validation mechanism handling environmental changes:
- **Signature = functional hash** of screen state (elements, text, layout)
- **Tolerance = exact element matching** for critical actions, fuzzy matching for layout
- **Graceful fallback = revert to LLM** when signature mismatches

### 3. Extreme Speedup in Practice

Empirically demonstrated 8.5-13x speedup on repeated tasks:
- **Across multiple domains:** Web UI, mobile apps, desktop applications
- **Consistent improvement:** Speedup maintained even with UI variations
- **Minimal overhead:** Signature computation and validation < 100ms per step

### 4. Production-Ready Design

System designed for deployment:
- **Safety-first:** Validation checks prevent executing in wrong contexts
- **Monitoring-friendly:** Clear signals when replay succeeds vs. falls back
- **User experience:** Dramatic perceived speedup (30s → 2-3s)
- **Failure handling:** Graceful degradation prevents catastrophic errors

## Methodology & Implementation

### Execution Trace Capture

```
Trace Capture Process:

Agent Execution:
  for step in task_execution:
    └─> capture {
        "screen_state_before": screen.dump(),
        "action": agent_decision,
        "screen_state_after": screen.dump(),
        "llm_reasoning": reasoning_trace,
        "success": action_succeeded
      }

Upon Success:
  └─> compile_to_program(execution_trace) → StateTransitionProgram
      └─> store(program, task_id, parameters)
```

### Experimental Setup

**Domains Tested:**
- Web-based task automation (booking, shopping, data entry)
- GUI-based workflows (calendar, email, file management)
- Mobile app interactions (cross-platform UI variations)
- Desktop application control (configuration, reporting)

**Baselines:**
- Full LLM reasoning per step (traditional agent)
- Caching only action sequences (naive replay)
- Static script execution (no adaptation)
- Human-written task scripts

**Metrics:**
- End-to-end latency (wall-clock time per task)
- LLM API calls per task execution
- Success rate on first replay
- Success rate on second replay (after adaptation)
- UI variation tolerance

### Experimental Results

**Speedup by Domain:**

| Domain | First Replay Success | Speedup | Speedup w/ Adaptation |
|--------|---------------------|---------|----------------------|
| Web Booking | 87% | 8.5x | 94% success, 7.2x |
| Email Management | 92% | 10.2x | 98% success, 9.8x |
| File Management | 84% | 9.1x | 89% success, 8.7x |
| Mobile Apps | 79% | 11.3x | 91% success, 10.1x |

**Latency Improvements:**

- Average task completion: 45s (traditional) → 4.5s (replay)
- P95 latency: 60s (traditional) → 6s (replay)
- P99 latency: 90s (traditional) → 8s (replay)

**Failure Analysis:**

- **Successful straight replays:** 87% (no environment change)
- **Successful with adaptation:** 6% (minor UI changes handled)
- **Fallback to LLM:** 7% (significant changes detected)
- **Total success:** 93% on repeated executions

[Complete statistical analysis and significance testing in full paper]

## Practical Applications & Use Cases

### 1. Personal Assistant Agents

**Application:** Email management, calendar coordination, task management

```
Typical Usage Pattern:
Day 1: User asks "Book a meeting room for Monday 10am"
  └─> Full agent reasoning (60s)
  └─> Program created and cached

Day 2: User asks "Book a meeting room for Wednesday 2pm"
  └─> Similar task → cached program applicable with parameter changes
  └─> Adaptive replay with new time parameter (5s)
  └─> Update to adapt program to new parameters

Result: Recurring tasks run 8-10x faster
```

### 2. Enterprise Workflow Automation

**Application:** Data entry, report generation, system administration

Benefits for enterprises:
- Dramatic reduction in API costs (fewer LLM calls)
- Reduced infrastructure load (parallelizable via task caching)
- Predictable performance (replay latency is deterministic)
- Audit trail (cached program serves as execution log)

### 3. Cost Optimization for Deployed Agents

**Current Reality:** Large-scale agent deployments pay per LLM call

```
Cost Analysis:
  
Traditional approach (100 daily bookings):
  Cost = 100 tasks × 20 steps × $0.01/call = $20/day

PreAct approach (100 daily bookings, 30% repetition):
  Repeated: 30 tasks × 1 LLM call = $0.30
  Novel: 70 tasks × 20 LLM calls = $14
  Total = $14.30
  Savings: 28% cost reduction

Scaled to 10,000 daily tasks (typical SaaS):
  Savings: 5-10x cost reduction annually
```

### 4. Mobile and Edge Deployment

**Application:** On-device task automation with connectivity constraints

- Replay programs are lightweight (KB-scale)
- Can execute offline after cached compilation
- Reduced bandwidth requirements
- Battery-efficient (no continuous LLM inference)

### Integration Challenges

- **Program Maintenance:** Cached programs become stale with UI updates
- **Parameter Binding:** Generalizing programs to different parameters
- **Domain Variation:** Handling similar-but-different UI layouts
- **Security:** Ensuring cached programs don't access unintended resources

## Insights & Implications

### Impact on Agent Deployment

1. **Cost Breakthrough:** Makes large-scale agent deployment economically viable
2. **Performance Predictability:** Deterministic replay enables SLA guarantees
3. **Practical Viability:** Transforms agents from "interesting research" to "production tool"
4. **Scalability:** Enables handling much higher task volumes with same resources

### Advancement in Computer-Using Agents

- Demonstrates that task structure can be captured and reused automatically
- Shows feasibility of hybrid approaches (reasoning + replay)
- Provides template for other compilation-based optimizations
- Opens door to program synthesis from successful agent traces

### Limitations and Open Questions

- **Program Generalization:** How much parameter variation can cached programs handle?
- **UI Evolution:** How quickly do cached programs become stale with app updates?
- **Complex Workflows:** Does approach scale to multi-hour tasks with many decision points?
- **Cross-Device Portability:** Can programs transfer across different screen sizes/orientations?
- **Security Analysis:** What security properties does cached program replay maintain?

## Code & Resources

### Official Implementation

- **GitHub Repository:** [Official PreAct implementation]
- **Framework Integration:** Compatible with Claude Code agents, Anthropic Managed Agents
- **Dependencies:**
  - LLM API for initial reasoning (Anthropic, OpenAI)
  - Screen capture/OCR library
  - State machine executor
  - Optional: UI testing frameworks (Selenium, Playwright)

### Quick-Start Implementation

```python
from preact import PreActAgent, ProgramCache

# Initialize agent with caching
cache = ProgramCache(storage="./task_cache")
agent = PreActAgent(
    llm_backend="claude-opus",
    program_cache=cache,
    enable_signature_validation=True
)

# First execution - creates and caches program
def book_flight(destination, date):
    task = f"Book a flight to {destination} for {date}"
    program = agent.execute(
        task=task,
        parameters={"destination": destination, "date": date}
    )
    return program

# Subsequent executions - uses cached program
result1 = book_flight("Tokyo", "2026-08-15")  # Full reasoning, 45s
result2 = book_flight("Osaka", "2026-09-20")  # Cached program replay, 4s

# Explicitly manage cache
cache.get_program_stats()  # View cached programs
cache.invalidate_stale()   # Remove outdated programs
cache.export_for_sharing()  # Share programs across agents
```

### Program Compilation Example

```python
# Raw execution trace
trace = [
  {"screen": A, "action": "tap(#search)", "next_screen": B},
  {"screen": B, "action": "type('Tokyo')", "next_screen": C},
  {"screen": C, "action": "tap(#submit)", "next_screen": D},
  # ... more steps
]

# Compiled to state machine
program = StateTransitionProgram(
  states=[
    State(id=0, signature=hash(A), action=Tap("#search"), next=1),
    State(id=1, signature=hash(B), action=Type("Tokyo"), next=2),
    State(id=2, signature=hash(C), action=Tap("#submit"), next=3),
  ],
  start=0,
  success_condition=lambda s: s.id == 3
)

# Replay with validation
result = program.replay(
  initial_screen=current_screen,
  tolerance=0.95,  # 95% signature match required
  fallback_agent=llm_agent  # Fallback on mismatch
)
```

### Compute Requirements

- **First Run:** Standard agent requirements (LLM inference)
- **Cached Runs:** Minimal (screen capture + hashing + action execution)
- **Memory:** ~10-100KB per cached program
- **Typical Speedup:** 8-13x wall-clock time reduction

## Related Work & Context

### Foundation Work

- **Program Synthesis:** Traditional program synthesis from execution traces
- **User Interface Automation:** Selenium, Playwright, UI testing frameworks
- **Agent Execution:** LangChain, CrewAI agent frameworks
- **Caching Strategies:** Redis, LLM response caching

### Related Papers on Agent Optimization

- [Empowering Autonomous Debugging Agents with Efficient Dynamic Analysis](https://arxiv.org/abs/2604.24212) (2026)
- [On the Reliability of Computer Use Agents](https://arxiv.org/abs/2604.17849) (2026)
- [Why Are GUI Agents Correct but Late? Decode on the Decision-Time Critical Path](https://arxiv.org/abs/2607.28399) (2026)

### Future Research Directions

1. **Adaptive Program Synthesis:** Learning to generalize cached programs to parameter variations
2. **Program Optimization:** Compressing state transitions, eliminating redundant checks
3. **Cross-Application Transfer:** Using patterns from one domain to accelerate others
4. **Multi-Agent Coordination:** Sharing cached programs across distributed agents
5. **Formal Verification:** Proving cached programs maintain safety properties
6. **Continuous Learning:** Programs evolve as apps update through collected execution traces

---

**Citation:**
```bibtex
@article{preact2026,
  title={PreAct: Computer-Using Agents that Get Faster on Repeated Tasks},
  author={Li, Bojie and others},
  year={2026},
  note={arXiv:2606.17929}
}
```
