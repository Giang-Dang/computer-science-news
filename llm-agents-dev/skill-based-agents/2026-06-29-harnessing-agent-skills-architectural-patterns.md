# Harnessing Agent Skills: Architectural Patterns and a Reference Architecture for Skill-Mediated LLM Agents

**Authors:** Boming Xia, Liming Zhu, Zhenchang Xing, Qinghua Lu, Dino Sejdinovic, Xiwei Xu (CSIRO Data61, University of New South Wales, University of Edinburgh)

**ArXiv ID:** 2606.20631

**Submitted:** June 29, 2026

---

## Executive Summary

As LLM-based agents evolve from monolithic systems to skill-mediated architectures, critical questions emerge about how to manage the lifecycle of agent skills from creation through evolution. This paper provides an empirical study of how skills are harnessed in practice, identifying ten architectural patterns (five core, five supporting) that govern the transition from skill artifacts to skill-in-use. The authors synthesize these patterns into a reference architecture with four responsibility layers (Supply Chain, Mediation, Execution, Evidence & Feedback), providing practitioners with foundational design guidance for building reliable, auditable, and evolvable agent systems. This work is essential reading for architecting production-grade agentic software development systems.

---

## Problem Statement

### Development Automation Challenge

Modern agent-driven development systems decompose problems across specialized agents, each equipped with domain-specific skills. However, the engineering discipline for managing skills—from specification through deployment, execution, verification, to evolution—has lagged far behind the rapid advancement in agent capabilities.

### Prior Agent System Limitations

1. **Ad-hoc skill integration**
   - Skills bolted on to agents without clear architectural governance
   - No standard for documenting skill contracts or dependencies
   - Difficult to debug or attribute failures to specific skills

2. **Opacity in skill execution**
   - What did a skill actually do? What side effects occurred?
   - No structured way to capture evidence (logs, traces, artifacts)
   - Regression detection and root cause analysis nearly impossible

3. **Skill brittleness and fragility**
   - Skills developed in isolation don't compose reliably
   - Dependencies not explicit (e.g., Skill A requires Skill B output)
   - No mechanism for graceful degradation or fallback

4. **Lack of skill evolution infrastructure**
   - Once deployed, skills are rarely improved
   - No feedback loop from execution to skill developers
   - Difficult to measure skill performance or detect when skills become stale

5. **Accountability and auditing gaps**
   - When an agent makes a bad decision, which skill was at fault?
   - What was the skill's input? Output? Reasoning?
   - Impossible to provide explainability to users

### Research Gap

No systematic guidance existed for:
- Architecting skill-mediated agent systems from first principles
- Separating concerns (supply chain vs. execution vs. feedback)
- Defining architectural responsibilities at each layer
- Establishing patterns for skill lifecycle management

---

## Core Concepts & Theory

### Skill Artifacts and Skills-in-Use

**Skill Artifact (at rest):**
```
Skill Package (on disk / in repository):
├─ Skill Description (markdown or JSON)
│  ├─ Name: "code_review_skill"
│  ├─ Purpose: "Review code for style, correctness, security"
│  ├─ Preconditions: ["Code file provided", "Language understood"]
│  ├─ Postconditions: ["Review document generated", "Issues identified"]
│  ├─ Applicability Scope: "Python, TypeScript, Go"
│  └─ Version: "1.2.3"
├─ Implementation
│  ├─ Executable (Python script, LLM prompt template, REST API)
│  └─ Dependencies (linters, security scanners, ML models)
├─ Testing Suite
│  ├─ Unit tests
│  └─ Integration scenarios
└─ Metadata
   ├─ Author, creation date
   ├─ Usage statistics
   └─ Known limitations
```

**Skill-in-Use (at runtime):**
```
When an agent invokes a skill:
1. Agent selects skill based on task
2. Skill binds to current execution context
3. Skill executes with:
   - Specific input data
   - Specific authority (what can it access/modify?)
   - Specific constraints (timeout, resource limits)
4. Skill produces:
   - Primary output (result)
   - Evidence (execution trace, artifacts)
   - State changes (modified files, database records)
5. Agent consumes output and decides next steps
6. Execution evidence is recorded for audit/evolution
```

### Four Responsibility Layers

**Layer 1: Supply Chain**
- Manages skill artifacts before execution
- Responsibilities:
  - Discovery: How do agents find skills?
  - Curation: Which skills are approved for use?
  - Versioning: Track skill changes over time
  - Composition: How do skills depend on each other?

**Layer 2: Mediation**
- Constructs skill-in-use from artifact + context
- Responsibilities:
  - Selection: Which skill for this task?
  - Binding: Connect skill to specific data/resources
  - Authority: What permissions does this skill have?
  - Contextualization: Provide task-specific prompts/parameters

**Layer 3: Execution**
- Controls skill invocation and interaction
- Responsibilities:
  - Invocation: Call skill with bounded scope
  - Error handling: Gracefully handle failures
  - State isolation: Prevent skills from interfering
  - Resource management: Enforce timeout/memory limits

**Layer 4: Evidence & Feedback**
- Captures evidence and drives improvement
- Responsibilities:
  - Attribution: Which skill produced which result?
  - Verification: Did the skill meet its postconditions?
  - Repair: How do we fix broken skills?
  - Evolution: How do skills improve over time?

**Architecture Diagram:**

```
User Task
    ↓
    ├─ Layer 1: Supply Chain
    │  ├─ Skill Repository
    │  ├─ Dependency Graph
    │  └─ Version Control
    │
    ├─ Layer 2: Mediation
    │  ├─ Skill Selector
    │  ├─ Context Binder
    │  └─ Authority Manager
    │
    ├─ Layer 3: Execution
    │  ├─ Skill Invoker
    │  ├─ Error Handler
    │  └─ Resource Monitor
    │
    ├─ Layer 4: Evidence & Feedback
    │  ├─ Trace Recorder
    │  ├─ Verification Engine
    │  └─ Evolution Feedback
    │
    ↓
Task Outcome + Evidence Log
```

---

## Main Ideas & Contributions

### Contribution 1: Five Core Architectural Patterns

**Pattern 1: Progressive Skill Activation**

**Problem:** When should a skill become available to agents?

**Solution:** Skills progress through lifecycle stages with restricted availability:

```
Lifecycle Stages:
1. Development
   └─ Available to: Skill developer only
   └─ Environment: Local/sandbox
   └─ Risk: High (untested)

2. Beta/Staging
   └─ Available to: Test agents in staging
   └─ Environment: Prod replica, limited traffic
   └─ Risk: Medium (limited exposure)

3. Gradual Rollout
   └─ Available to: 5% → 25% → 50% → 100% of agents
   └─ Environment: Production with canary deployment
   └─ Risk: Low (monitored rollout)

4. Stable
   └─ Available to: All agents
   └─ Environment: Full production
   └─ Risk: Minimal (proven stable)

5. Deprecated
   └─ Available to: Scheduled for removal
   └─ Environment: Supported with warnings
   └─ Risk: Migration needed
```

**Implementation Example:**
```python
class SkillRegistry:
    def is_available(self, skill: Skill, agent: Agent, env: str):
        if skill.status == "development":
            return agent.id == skill.developer_id and env == "local"
        elif skill.status == "beta":
            return env == "staging" or agent.tier == "trusted"
        elif skill.status == "stable":
            return True  # Available to all
        elif skill.status == "deprecated":
            return False  # Scheduled removal
```

**Benefit:** Reduces risk of deploying untested skills while enabling rapid iteration.

---

**Pattern 2: Skill-Execution Authority Separation**

**Problem:** A skill shouldn't have authority equivalent to the agent that invokes it.

**Example Scenario:** A code review skill should read files but not modify repository permissions.

**Solution:** Authority is separate from capability reference.

```
Skill Definition: "code_review_skill"
Capability: "Read Python files, analyze code, generate report"
Authority: "Read /codebase/src/**, write /tmp/review_artifact_*"

Agent Invocation:
agent.invoke(
    skill="code_review_skill",
    input="/codebase/src/main.py",
    permissions=["read:/codebase/src/**"],  ← Restricted!
    constraints={"timeout": 30, "memory": "2GB"}
)
```

**Authority Levels:**
```
Read-Only: Access file system, read memory (safe)
Write-Local: Create/modify files in /tmp (contained)
Write-System: Modify codebase (controlled)
Execute: Run shell commands (dangerous)
Admin: Access system resources (restricted)
```

**Benefit:** Enables safe composition of skills even from untrusted sources.

---

**Pattern 3: Verifiable Skill Contract**

**Problem:** How do we verify that a skill did what it claimed to do?

**Solution:** Explicit skill contracts define preconditions, postconditions, and side effects.

```
Skill Contract Specification:

Skill: "add_test_coverage"

Preconditions (input requirements):
  - Must have: Source code file path
  - Must have: Test framework type (pytest/unittest/jest)
  - Must have: Minimum coverage threshold (e.g., 80%)
  - Optional: Existing test suite path

Postconditions (guarantees on success):
  - Will produce: Test file in same directory
  - Will include: At least N_cov assertions
  - Will satisfy: Coverage threshold on functions
  - Will not: Modify original source code
  - Will not: Break existing tests

Side Effects (observable changes):
  - File system: Creates /code/test_*.py
  - Environment: May install testing libraries
  - External: No network calls

Error Cases (expected failures):
  - Precondition not met → Error 400 "Missing input"
  - Unsupported language → Error 422 "Language not supported"
  - Timeout after 60s → Error 504 "Processing time exceeded"

Verification Strategy:
  1. Before execution: Check preconditions
  2. After execution: Verify postconditions
  3. Detect side effects: Monitor file system, environment
  4. Rollback on failure: Restore pre-execution state
```

**Verification Implementation:**
```python
class SkillContract:
    def verify_preconditions(self, input_data):
        if not os.path.exists(input_data.file_path):
            raise PreconditionError("File not found")
        if input_data.coverage_threshold < 0 or > 100:
            raise PreconditionError("Invalid threshold")
        return True
    
    def verify_postconditions(self, output, input_data):
        test_file = output.generated_test_path
        coverage = measure_coverage(test_file, input_data.file_path)
        if coverage < input_data.coverage_threshold:
            raise PostconditionError(
                f"Coverage {coverage}% < threshold {input_data.coverage_threshold}%"
            )
        # Verify original code unchanged
        original_hash = input_data.source_code_hash
        current_hash = hash_file(input_data.file_path)
        if original_hash != current_hash:
            raise PostconditionError("Source code was modified")
        return True
```

**Benefit:** Enables automated verification and provides audit trail.

---

**Pattern 4: Runtime Skill-BOM (Bill of Materials)**

**Problem:** Debugging failures is hard when multiple skills interact.

**Solution:** Maintain Skill-BOM tracking all skills invoked during a run.

```
Execution Trace (Skill-BOM):

Task: "Refactor authentication module"

[10:00:00] Invoked: analyze_skill v2.1
          Input: /auth/session.py
          Output: "3 candidates for refactoring identified"
          Duration: 2.3s
          Status: SUCCESS
          Authority Used: read:/auth/**

[10:00:02] Invoked: refactor_propose_skill v1.8
          Input: /auth/session.py + candidates
          Output: /tmp/refactor_proposal_123.md
          Duration: 8.1s
          Status: SUCCESS
          Authority Used: read:/auth/**, write:/tmp/**

[10:00:10] Invoked: test_generation_skill v3.0
          Input: /auth/session.py + /tests/auth/*
          Output: /tests/test_refactor.py (1,245 lines)
          Duration: 15.3s
          Status: SUCCESS
          Authority Used: read:/auth/**, read:/tests/**, write:/tests/**

[10:00:25] Invoked: test_execution_skill v2.4
          Input: /tests/test_refactor.py
          Output: "Test run completed: 142 pass, 3 fail"
          Duration: 22.1s
          Status: PARTIAL_FAILURE
          Failed Tests: test_session_timeout, test_concurrent_login, test_token_refresh
          Authority Used: execute:/tests/**

Summary:
├─ Total Skills Invoked: 4
├─ Success Rate: 75% (3/4)
├─ Total Execution Time: 48.8s
├─ Bottleneck: test_execution_skill (45.1% of time)
├─ Failure Cause: test_session_timeout failed (investigate skill #4)
└─ Recommendation: Rerun test with extended timeout or modify concurrent_login logic
```

**Skill-BOM Metadata Schema:**
```yaml
SkillInvocation:
  skill_id: "refactor_propose_skill"
  skill_version: "1.8"
  timestamp: "2026-06-29T10:00:02Z"
  invocation_id: "run_abc123_step_2"
  
  input:
    file_path: "/auth/session.py"
    analysis_candidates: [...]  # Reference to previous skill output
  
  output:
    proposal_document: "/tmp/refactor_proposal_123.md"
    confidence_score: 0.87
    estimated_improvement: "12% latency reduction, 8% lines removed"
  
  execution_metrics:
    duration_seconds: 8.1
    tokens_used: 2847
    api_cost: "$0.14"
  
  verification:
    preconditions_met: true
    postconditions_verified: true
    side_effects_detected: ["file_created:/tmp/refactor_proposal_123.md"]
  
  performance_profile:
    cpu_percent: 45
    memory_mb: 342
    disk_io_mb: 1.2
```

**Benefit:** Enables comprehensive post-mortem analysis and continuous improvement.

---

**Pattern 5: Skill-Agent Co-Evolution Loop**

**Problem:** How do skills improve based on real-world usage?

**Solution:** Establish feedback loop from execution evidence to skill developers.

```
Co-Evolution Cycle:

Day 1: Skill Deployed
├─ test_generation_skill v1.0 deployed
├─ Coverage: 85% of refactoring tasks
└─ Artifacts saved to evidence database

Days 2-7: Collect Execution Data
├─ 1,247 invocations across different codebases
├─ Success rate: 78%
├─ Common failure patterns detected:
│  ├─ 15% fail: Missing edge case in concurrent code
│  ├─ 4% fail: Inadequate test setup code
│  └─ 3% fail: Type annotations not preserved
├─ User feedback: "Generated tests are brittle"
└─ Skill cost: $2,847 total (avg $2.28/invocation)

End of Week: Evolution Phase
├─ Skill developer reviews evidence
├─ Identifies root causes:
│  ├─ Test setup code (fix: add fixture generation)
│  ├─ Edge cases (fix: enhance prompt with concurrent patterns)
│  └─ Type preservation (fix: parse AST for signatures)
├─ Publish test_generation_skill v1.1
└─ Metrics tracked: Improvement per user feedback metric

Month 1: Convergence
├─ v1.0 → v1.1: Success rate 78% → 84% (+6pp)
├─ v1.1 → v1.2: Success rate 84% → 89% (+5pp)
├─ Cost improved: $2.28 → $1.94/invocation (-15%)
├─ v1.2 promoted to stable
└─ v1.0 deprecated

Ongoing: Continuous Improvement
├─ Even v1.2 monitored for degradation
├─ New patterns detected → v1.3 in development
├─ Skills that plateau are candidates for replacement
```

**Evidence-Driven Improvement Metrics:**

```
Skill Performance Dashboard:

test_generation_skill v1.2
├─ Invocations: 3,847 (↑45% from v1.1)
├─ Success Rate: 89% (↑5pp from v1.1)
├─ Avg Duration: 14.2s (↓2.1s from v1.1)
├─ Cost per Use: $1.94 (↓$0.34 from v1.1)
├─ User Rating: 4.2/5.0 (↑0.6 from v1.1)
├─ SLA Compliance: 96% (↑8pp from v1.1)
├─ Time to Deprecation: ~12 months
│  (when v2.0 based on new approach ships)
└─ Trend: Improving (stable or green) ✓
```

**Benefit:** Skills continuously improve based on empirical evidence, not speculation.

---

### Contribution 2: Five Supporting Architectural Patterns

**Pattern 6: Skill Composition Manifest**
- Documents how multiple skills work together
- Specifies output-to-input compatibility
- Enables automated composition validation

**Pattern 7: Partial Failure Resilience**
- One skill fails; workflow continues if possible
- Fallback skill invocation
- Partial result aggregation

**Pattern 8: Skill Resource Budgeting**
- Each skill gets a time/cost/memory budget
- Enforces fair resource allocation
- Prevents runaway skill execution

**Pattern 9: Skill Metadata Indexing**
- Full-text search over skill descriptions
- Capability-based discovery
- Similar skill detection (skill deduplication)

**Pattern 10: Evidence Compression**
- Skill execution generates large traces
- Selective archival (keep recent, compress old)
- Privacy-preserving evidence storage

---

## Methodology & Implementation

### Empirical Grounding

**Data Source:**
- 15 production agent systems from industry partners
- 6-month execution logs (>2 million skill invocations)
- Interviews with 28 agent engineers and skill developers
- Code analysis of 800+ deployed skills

### Reference Architecture Implementation

**Full Architecture Stack:**

```
┌─ Supply Chain Layer ─────────────────────────┐
│  ┌─ Skill Repository                       │
│  │  ├─ Version Control (git-based)         │
│  │  ├─ Semantic Search Index               │
│  │  └─ Dependency Graph                    │
│  └─ Package Management                      │
│     ├─ Skill Packaging (versioned folders) │
│     ├─ Approval Workflow (manual/auto)     │
│     └─ Dependency Resolution               │
└──────────────────────────────────────────────┘

┌─ Mediation Layer ────────────────────────────┐
│  ┌─ Skill Selector                         │
│  │  ├─ Task-to-Skill Matcher              │
│  │  ├─ Performance Predictor              │
│  │  └─ Fallback Strategy                  │
│  ├─ Context Binder                         │
│  │  ├─ Input Provider                     │
│  │  └─ Prompt Template Renderer           │
│  └─ Authority Manager                      │
│     ├─ Permission Resolver                │
│     └─ Security Policy Enforcement        │
└──────────────────────────────────────────────┘

┌─ Execution Layer ────────────────────────────┐
│  ┌─ Skill Invoker                          │
│  │  ├─ Synchronous Execution              │
│  │  ├─ Asynchronous Queuing               │
│  │  └─ Timeout Management                 │
│  ├─ Error Handler                          │
│  │  ├─ Exception Catching                 │
│  │  ├─ Retry Logic                        │
│  │  └─ Graceful Degradation               │
│  └─ Resource Monitor                       │
│     ├─ CPU/Memory Tracking                │
│     ├─ Cost Metering                      │
│     └─ Budget Enforcement                 │
└──────────────────────────────────────────────┘

┌─ Evidence & Feedback Layer ──────────────────┐
│  ┌─ Trace Recorder                         │
│  │  ├─ Event Logging                      │
│  │  ├─ Artifact Collection                │
│  │  └─ Trace Storage                      │
│  ├─ Verification Engine                    │
│  │  ├─ Contract Checking                  │
│  │  ├─ Assertion Evaluation               │
│  │  └─ Regression Detection               │
│  └─ Evolution Feedback                     │
│     ├─ Performance Metrics                │
│     ├─ Failure Analysis                   │
│     └─ Skill Improvement Signals          │
└──────────────────────────────────────────────┘
```

### Implementation Technologies

**Recommended Stack:**

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Supply Chain** | Git + semantic indexing (OpenSearch) | Version control + search |
| **Mediation** | LLM-based selector + vector DB | Flexible skill matching |
| **Execution** | Async task queue (Celery/RQ) | Scalable skill invocation |
| **Evidence** | Event streaming (Kafka) + time-series DB | Real-time monitoring |

### Empirical Results from Case Studies

**Case Study 1: Code Refactoring Agent (Company A)**

```
Before (Monolithic Architecture):
├─ Single agent with ~30 hard-coded functions
├─ Success rate: 62% on codebase transformations
├─ Avg time per task: 48s
├─ Cost: $4.20 per task
├─ When skill breaks: Entire agent becomes unreliable

After (Skill-Mediated with Patterns):
├─ Decomposed into 8 specialized skills
├─ Success rate: 89% (+27pp)
├─ Avg time per task: 22s (-54%)
├─ Cost: $1.80 per task (-57%)
├─ When skill breaks: Use fallback; impact localized
├─ Improvement cycle: 2-3 weeks (vs. 6 weeks monolithic)
```

**Case Study 2: Security Analysis Agent (Company B)**

```
Key Challenge: Accountability when security issues missed

Before (No Skill-BOM):
├─ Agent flags 1,247 potential vulnerabilities
├─ 156 false positives (12.5% waste)
├─ When false positive occurs: Can't trace which component failed

After (Skill-BOM + Verification):
├─ Skill-BOM captures each analysis component
├─ Pattern detected: Pattern-matching skill has high false positive rate on regex patterns
├─ Skill developer fixes: Improves pattern accuracy
├─ False positives reduced: 12.5% → 3.2% (-74%)
├─ Cost reduction: $2.8K/month (fewer false investigations)
```

**Case Study 3: Test Generation Agent (Company C)**

```
Measurement: Impact of Progressive Skill Activation

Deployment Strategy:

Week 1: Internal testing only
├─ test_gen_skill v2.0 tested by dev team
├─ Issues found: 2 edge cases in async test generation
├─ Cost: ~$150 (dev cost only)

Week 2: Beta (25% of production traffic)
├─ 5,000 invocations
├─ Issues found: 1 pattern collision in TypeScript generics
├─ Fix deployed

Week 3: Gradual rollout (50% → 75%)
├─ 25,000 invocations
├─ Stable performance observed
├─ User feedback: Excellent (4.6/5.0)

Week 4: Full production (100%)
├─ High-volume deployment
├─ Confidence: Very high (proven stable over 25K+ invocations)

Alternative (Direct 100% Deployment):
├─ Would have exposed 30M+ invocations to edge cases
├─ Potential impact: 12,000+ failed tests (6% failure rate)
├─ Cost: $120K + reputation damage
```

---

## Practical Applications & Use Cases

### 1. Autonomous Code Review System

**Architecture:**
```
Review Agent
├─ Skill: static_analysis (style, type errors)
├─ Skill: security_analyzer (vulnerability patterns)
├─ Skill: performance_reviewer (algorithmic complexity)
├─ Skill: documentation_verifier (docstring quality)
└─ Skill: maintainability_scorer (cyclomatic complexity)

Each skill has:
├─ Progressive activation (beta-tested before promotion)
├─ Verifiable contract (e.g., "will output JSON with X fields")
├─ Runtime Skill-BOM (logs which analyses ran)
└─ Co-evolution (improves based on developer feedback)
```

**Impact:**
- Code review turnaround: 24h → 15m
- Review consistency: Varies by reviewer → Standardized
- False positive rate: Continuously decreases as skills improve
- Developer satisfaction: Increased (faster, clearer feedback)

### 2. Continuous Refactoring Agent

**Workflow:**
```
1. analyze_code_skill: Identify refactoring opportunities
2. refactor_propose_skill: Generate refactoring candidates
3. test_generation_skill: Create tests for refactored code
4. test_execution_skill: Validate refactoring preserves behavior
5. code_quality_skill: Measure improvement metrics
6. commit_skill: Submit to version control (with approval gate)

Skill-BOM tracks:
├─ Which refactorings were rejected (and why)
├─ Which preserve behavior (and which don't)
├─ Performance improvements measured
└─ Developer confidence in each skill
```

**Success Metrics:**
- 87% of proposed refactorings accepted
- Lines of code: -8% (consolidated duplicates)
- Test coverage: +3pp (new edge cases)
- Maintenance cost: -12% (easier to understand)

### 3. Multi-Model Development Agent

**Problem:** Different models excel at different tasks
- Model A: Fast, good for simple generation
- Model B: Powerful, better for complex reasoning
- Model C: Specialized, best for domain-specific tasks

**Solution with Skill Patterns:**
```
Dynamic Model Selector:
├─ Skill: quick_implementation (uses Model A)
├─ Skill: complex_design (uses Model B)
└─ Skill: domain_expert (uses Model C)

Selection based on:
├─ Task complexity estimation
├─ Latency budget
├─ Cost constraints
└─ Skill success history

Evidence & Feedback:
├─ Track which model/skill succeeds on which task types
├─ Continuously improve model selection heuristics
├─ Detect when to switch models or introduce new ones
```

**Cost Optimization:**
- Before: Use Model B for everything ($0.80/task)
- After: Model A (62% of tasks, $0.02), Model B (28%, $0.50), Model C (10%, $0.25)
- Average cost: $0.18/task (-77.5%)
- Performance: Maintained or improved (specialized models for specific tasks)

### 4. Debugging Agent for Production Issues

**Agent Workflow:**
```
1. trace_analyzer_skill: Parse error traces and logs
2. hypothesis_generator_skill: Propose root causes
3. code_searcher_skill: Find related code
4. test_reproducer_skill: Create minimal reproducers
5. fix_generator_skill: Propose patches
6. regression_tester_skill: Verify fix doesn't break other systems
7. incident_documenter_skill: Generate post-mortem

Skill-BOM Example (for incident #12345):
├─ trace_analyzer found: OutOfMemory in cache eviction
├─ hypothesis_generator proposed: LRU cache not working
├─ code_searcher found: 3 potential locations
├─ test_reproducer created: /tmp/oom_test.py
├─ fix_generator proposed: Fix eviction logic + size limits
├─ regression_tester: All tests pass (regression: 0)
└─ documenter: Post-mortem ready

Accountability:
├─ Each skill's contribution is clear
├─ If fix breaks something: Exactly which regression test failed
├─ Improvement signal: Which skills need tuning
```

**Operational Impact:**
- MTTR (Mean Time To Recovery): 45m → 8m
- Correctness: 78% fixes need follow-up → 92% correct first try
- Confidence: <40% vs. 87% production deployments

---

## Insights & Implications

### Advancement in Autonomous Development Systems

1. **Architecture Matters as Much as Capability**
   - Well-architected skill systems outperform monolithic agents
   - Decomposition enables specialization and iterative improvement
   - Separation of concerns (selection, execution, evidence) improves maintainability

2. **Evidence-Driven Evolution Beats Static Optimization**
   - Skills that improve based on real-world usage vastly outperform static versions
   - Feedback loops create continuous improvement cycles
   - 6-month skills show 2-3x performance improvement

3. **Accountability Through Architecture**
   - Structured skill invocation enables attribution
   - When systems fail, precise root cause analysis is possible
   - Supports regulatory compliance and user trust

### Limitations and Open Questions

1. **Skill Characterization Complexity**
   - Writing good pre/postconditions is non-trivial
   - Incomplete contracts reduce verification value
   - Requires discipline from skill developers

2. **Evidence Storage Scale**
   - 2M+ skill invocations generate terabytes of evidence
   - Storage costs can exceed compute costs
   - Selective archival strategies needed

3. **Cross-Organization Skill Portability**
   - Skills work well within one organization's infrastructure
   - Sharing across organizations requires standardization
   - Security/compliance implications

4. **Automated Skill Evolution**
   - Evidence-driven improvement still largely manual
   - Automatic patching of skills is risky
   - Need better mechanisms for autonomous improvement

### Relevance to Skill Frameworks and Agent Topologies

- Provides foundational architectural guidance for **skill-mediated agents**
- Demonstrates how to build **composable, reliable systems** at scale
- Enables **decentralized skill development** with clear governance
- Supports **multi-agent topologies** through explicit skill composition
- Critical for **production-grade autonomous systems** in software engineering

---

## Code & Resources

### Open-Source Reference Implementation

**Project: SkillHarness**
- Complete implementation of the four-layer architecture
- Patterns 1-5 fully realized
- Python + async/await + FastAPI

**Installation:**
```bash
pip install skill-harness
# or
git clone https://github.com/skillharnessai/skillharness.git
cd skillharness && pip install -e .
```

### Dependencies and Compute Requirements

**Core Dependencies:**
- Python 3.10+
- FastAPI (REST API)
- Redis (caching + queuing)
- PostgreSQL (skill metadata + execution logs)
- OpenSearch (semantic indexing)
- Celery (async task execution)

**Infrastructure:**
- 2+ CPU cores
- 4GB+ RAM (for indexing)
- 100GB+ storage (for execution traces)

### Quick-Start Integration Guide

```python
from skillharness import SkillRegistry, AgentExecutor, SkillBOM

# Initialize components
registry = SkillRegistry(repo_path="/skills")
executor = AgentExecutor(registry=registry)
bom = SkillBOM()

# Define a skill
@registry.skill(
    name="code_review_skill",
    version="1.0",
    preconditions=["code_file_provided"],
    postconditions=["review_generated", "issues_identified"]
)
def review_code(file_path: str) -> dict:
    """Review code for style, security, performance."""
    # Implementation
    return {"issues": [...], "suggestions": [...]}

# Use in agent execution
task = "Review the authentication module"
selected_skill = registry.select_best_skill(task)

result = executor.invoke(
    skill=selected_skill,
    input_data={"file_path": "/auth/main.py"},
    authority={"read": ["/auth/**"]},  # Restricted permissions
    timeout=30
)

# Access execution evidence
trace = bom.get_trace(executor.last_invocation_id)
print(f"Skill {trace.skill_name} v{trace.skill_version} executed")
print(f"Duration: {trace.duration}s, Cost: ${trace.cost:.2f}")
print(f"Success: {trace.status == 'SUCCESS'}")

# Use for continuous improvement
metrics = bom.compute_skill_metrics(
    skill_name="code_review_skill",
    time_window="7d"
)
print(f"Success Rate: {metrics.success_rate:.1%}")
print(f"Avg Duration: {metrics.avg_duration:.1f}s")
```

---

## Related Work & Context

### Foundational Work

- **Operating System Design Patterns:** Separation of concerns in OS kernel (applies to skill harness)
- **Microservice Architecture:** Independent deployability, versioning
- **DevOps & CI/CD:** Artifact pipelines, progressive deployment, evidence collection

### Related Agent Papers

1. **SoK: Agentic Skills -- Beyond Tool Use** (arXiv:2602.20867)
   - Taxonomy of agentic skills
   - This paper provides architectural patterns for skill implementation

2. **Agent Skills for Large Language Models** (arXiv:2602.12430)
   - Skills as architectural primitive
   - Complements with lifecycle management perspective

3. **Code as Agent Harness** (arXiv:2605.18747)
   - Harness engineering for agent systems
   - Overlapping concerns with execution layer

### Future Research Directions

1. **Automatic Skill Generation**
   - From execution traces to new skills
   - Discovering patterns that deserve specialization

2. **Formal Verification of Skills**
   - Prove contracts hold mathematically
   - Safety guarantees for critical skills

3. **Federated Skill Learning**
   - Skills improve across multiple organizations
   - Privacy-preserving evidence sharing

4. **Skill Economics**
   - Model for sustainable skill development
   - When to build vs. buy skills
   - Marketplace mechanisms for skills

---

## Summary

This paper provides essential architectural guidance for building production-grade, skill-mediated LLM agent systems. By identifying five core architectural patterns (Progressive Activation, Authority Separation, Verifiable Contracts, Runtime Skill-BOM, Co-Evolution Loop) and synthesizing them into a four-layer reference architecture, the authors address critical gaps in current agent system engineering.

The empirical foundation—drawn from 2M+ skill invocations across 15 production systems—lends credibility and practical relevance. The case studies demonstrate substantial improvements: code review agents show 27pp success rate improvement and 54% latency reduction, security analysis systems achieve 74% false positive reduction, and development cycle times compress from weeks to days.

For practitioners building autonomous software development systems, this work provides a roadmap for architecting reliable, auditable, and continuously improving agent systems. The patterns and reference architecture are immediately applicable and represent the current best practices in agentic AI system design.

