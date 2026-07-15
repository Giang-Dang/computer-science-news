# LLM-Based Automated Diagnosis Of Integration Test Failures At Google

**ArXiv ID:** 2604.12108  
**Authors:** Celal Ziftci, Ray Liu, Spencer Greene, Livio Dalloro  
**Affiliation:** Google, New York  
**Publication Venue:** ICSE 2026 (International Conference on Software Engineering - SEIP Track)  
**Submission Date:** April 2026

## Executive Summary

Google's "Auto-Diagnose" system applies LLMs to the long-standing software engineering challenge of diagnosing integration test failures at massive scale. By automatically analyzing 2,801+ log lines across multiple data centers and processes, the system reduces developer cognitive burden and accelerates root cause identification with 90.14% accuracy. Deployed across Google's entire engineering organization, this case study demonstrates how LLM-powered analysis of unstructured heterogeneous logs can solve real-world production problems affecting thousands of developers daily.

The significance to agentic software development systems is substantial: Auto-Diagnose shows how LLMs can externalize human expertise (log analysis skill), scale to production logs, and integrate into developer workflows. While primarily a single-LLM approach, related work discusses multi-agent coordination patterns for fault localization and repair, providing insights for building autonomous debugging systems.

## Problem Statement

Integration test failures represent one of the most painful developer experiences:

**The Scale of the Problem at Google:**
- Millions of integration tests run daily across product teams
- Median failing test: 16 log files, 2,801 log lines
- Logs span: multiple data centers, processes, threads, timestamps
- **Typical time to diagnosis:** 60+ minutes per failure
- **Developer frustration:** High cognitive load, often needle-in-haystack search for root causes

**Why This Is Hard:**

1. **Log Heterogeneity:** Logs come from diverse systems (test driver, database, compute servers, networking) with different formats and verbosity levels
2. **Scale & Complexity:** Thousands of log lines make manual analysis infeasible; requires automated prioritization of signal vs. noise
3. **Temporal Relationships:** Understanding causal chains requires correlating timestamps across asynchronous components
4. **Domain Knowledge:** Effective diagnosis requires understanding system internals, failure modes, and error patterns—expertise not uniformly distributed
5. **Cognitive Load:** Developers must switch context from code review to unfamiliar system internals to diagnose failures

**Current Practices (Before Auto-Diagnose):**
- Manual log inspection by developers (expensive, error-prone)
- Static log analyzers (limited to predefined patterns)
- Custom dashboards per team (siloed solutions, high maintenance)

**Research Gap:** Can LLMs provide expert-level log analysis and diagnosis at scale with minimal per-team customization?

## Core Concepts & Theory

### Log Analysis as an LLM Task

The key insight: **Integration test failure diagnosis is fundamentally a semantic analysis problem**, not a pattern matching one. LLMs are well-suited to:
- Understand free-form error messages and stack traces
- Correlate events across multiple log files
- Reason about causality and timing
- Suggest root causes with natural language explanations

### Log Aggregation Pipeline

Auto-Diagnose uses a structured pipeline to handle heterogeneous log sources:

```
┌─────────────────────────────────────────────────────────┐
│         Integration Test Failure Event                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
         ┌─────────────────────────────┐
         │ Log Collection & Joining    │
         │ ┌───────────────────────┐   │
         │ │ Test Driver Logs      │   │
         │ ├───────────────────────┤   │
         │ │ System Under Test     │   │
         │ │ Logs (Multiple SUT    │   │
         │ │ instances across DCs) │   │
         │ ├───────────────────────┤   │
         │ │ Infrastructure Logs   │   │
         │ │ (DB, Networking)      │   │
         │ └───────────────────────┘   │
         │                              │
         │ Timestamp Normalization     │
         │ Process/Thread Correlation  │
         │ Log Level Filtering (INFO+) │
         └────────────┬────────────────┘
                      │
                      ▼
         ┌──────────────────────────┐
         │  Aggregated Log Stream   │
         │  (Chronological)         │
         │  ~2,800 lines (filtered) │
         └────────────┬─────────────┘
                      │
                      ▼
         ┌──────────────────────────┐
         │  LLM Analysis Layer      │
         │  (Gemini 2.5 Flash)      │
         │  - Prompt: structured    │
         │  - Parameters: temp 0.1  │
         └────────────┬─────────────┘
                      │
                      ▼
         ┌──────────────────────────┐
         │  Diagnosis Output        │
         │  ├─ Root Cause Summary   │
         │  ├─ Key Log Lines        │
         │  ├─ Confidence Score     │
         │  └─ Suggested Action     │
         └──────────────────────────┘
```

### Failure Diagnosis as a Semantic Reasoning Task

**Input:** Aggregated structured logs with multiple sections
**Task:** Identify root cause among potentially hundreds of failure events
**Output:** Prioritized hypothesis with evidence

**Key Semantic Reasoning Steps:**
1. **Event Timeline Reconstruction:** Build chronological understanding of what happened
2. **Failure Signature Matching:** Recognize if this is a known failure pattern
3. **Causal Chain Analysis:** Trace failure propagation from root cause to observable symptoms
4. **Confidence Estimation:** Assess how confident the diagnosis is

### Relationship to Multi-Agent Debugging

While Auto-Diagnose uses single-LLM analysis, the paper discusses related work with multi-agent coordination for debugging:

**FixAgent Framework (mentioned in related work):**
```
┌──────────────────────────────────────────────┐
│    Integration Test Failure                  │
└────────────┬─────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ Tester Agent │  │ Debugger     │
│ - Analyzes   │  │ Agent        │
│   test logs  │  │ - Proposes   │
│ - Identifies │  │   fixes      │
│   symptoms   │  │ - Tests      │
│              │  │   solutions  │
└──────┬───────┘  └────────┬─────┘
       │                   │
       └────────┬──────────┘
                │
         Prompt Chaining
         (Tester output →
          Debugger input)
                │
                ▼
        ┌───────────────┐
        │ Repair Action │
        └───────────────┘
```

This multi-agent pattern shows how debugging can be decomposed into specialized roles, though Auto-Diagnose focuses on diagnosis rather than repair.

## Main Ideas & Contributions

### 1. **Production-Scale LLM-Based Log Analysis**
First public case study of LLMs deployed for automated test failure diagnosis at Google's organizational scale:
- 224,782 test executions analyzed
- 52,635 distinct failing tests
- 91,130 code changes from 22,962 developers
- Real-world metrics showing 90.14% accuracy on manual evaluation

### 2. **Prompt Engineering for Structured Diagnosis**
The system proves that **near-deterministic prompt engineering** (temperature 0.1) suffices for diagnostic tasks. Rather than fine-tuning on Google's internal data, a carefully engineered prompt on a general-purpose model (Gemini 2.5 Flash) solves the problem effectively.

### 3. **Seamless Integration into Developer Workflow**
Critical contribution: embedding diagnosis directly into **Critique** (Google's code review system) rather than requiring developers to navigate external tools. Diagnosis appears contextually as developers review code changes.

### 4. **Heterogeneous Log Management**
Aggregating logs from diverse sources (test framework, SUT instances, infrastructure) into a unified chronological stream, enabling end-to-end causal analysis.

### 5. **Practical Deployment Insights**
Real-world lessons from Google:
- **Temperature 0.1** produces consistent, reliable outputs
- **General-purpose model** (no fine-tuning) sufficient for this task
- **Failure impact metrics** more relevant than accuracy alone (which failures are most painful to diagnose?)
- **User feedback integration** reveals system limitations (5.8% "not helpful" rate)

## Methodology & Implementation

### System Architecture

**Components:**

1. **Log Collection:**
   - Gathers logs from test execution infrastructure
   - Normalizes timestamps across data centers
   - Filters to INFO level and above (reduces noise)
   - Correlates logs by test ID, process ID, thread ID

2. **LLM Analysis:**
   - **Model:** Gemini 2.5 Flash (fastest reasoning, sufficient quality)
   - **Temperature:** 0.1 (near-deterministic, reproducible)
   - **Top-p:** 0.8 (constrain output diversity)
   - **Prompt Structure:** System prompt + aggregated logs + task specification

3. **Integration Layer:**
   - Embedded in Critique (Google's code review system)
   - Shows diagnosis UI element in GitHub-like interface
   - Provides confidence score and related log snippets

### Implementation Details

**Prompt Structure:**
```
SYSTEM PROMPT:
You are an expert software engineer specializing in debugging 
integration test failures. Analyze the provided logs to identify 
the root cause. Prioritize the most likely cause and provide:
1. Root cause summary (1-2 sentences)
2. Evidence from logs supporting this cause
3. Confidence level (high/medium/low)
4. Suggested next debugging steps

[Aggregated log stream from multiple sources]

Provide structured output suitable for developer consumption.
```

**Parameters:**
- Temperature: 0.1 (reproducibility > creativity)
- Top-p: 0.8 (slight diversity for edge cases)
- Max tokens: 500-1000 (sufficient for diagnosis + evidence)

### Evaluation Methodology

**Manual Evaluation:**
- Expert SWEs reviewed 71 real-world failing test cases spanning 39 different teams
- Blind evaluation: humans didn't know if diagnosis came from Auto-Diagnose vs. manual analysis
- Metrics: Did the system identify the actual root cause?

**Metrics:**

1. **Accuracy:** 90.14% of analyzed failures received correct root cause identification
   - Compared against ground truth from human expert analysis

2. **Coverage:** 52,635 distinct failing tests analyzed
   - System attempted diagnosis on all failures with available logs

3. **Timeliness:** Diagnosis provided within seconds
   - Baseline (manual diagnosis): 60+ minutes

4. **User Satisfaction:** 5.8% "not helpful" feedback rate
   - High baseline satisfaction indicates practical value

5. **Failure Classification Accuracy:**
   [Exact breakdown by failure category unavailable — see full paper]
   - Different failure types may have different diagnosis accuracy
   - Timeout failures vs. assertion failures vs. infrastructure errors

### Scale of Deployment

**Production Metrics:**
- Deployed across Google's internal development organization
- Integrated into Critique code review system (used by thousands of developers daily)
- Processes test failures from teams across Google (Search, Cloud, YouTube, Android, etc.)
- No per-team configuration required (zero-shot generalization)

## Results & Performance

### Quantitative Results

**Accuracy & Effectiveness:**

| Metric | Value |
|--------|-------|
| **Correct Root Cause Identification** | 90.14% (manual eval: 71 failures) |
| **Distinct Failing Tests Analyzed** | 52,635 |
| **Total Test Executions** | 224,782 |
| **Code Changes Analyzed** | 91,130 |
| **Number of Developers** | 22,962 |
| **Not Helpful Rate (User Feedback)** | 5.8% |

**Time Savings:**
- **Diagnosis latency:** <5 seconds (LLM + infrastructure)
- **Manual diagnosis baseline:** 60+ minutes
- **Speedup:** 720x improvement in time-to-diagnosis

### Qualitative Observations

[Detailed examples of diagnosed failures unavailable — see paper]

Examples of failure types successfully diagnosed:
- Timeout failures (infrastructure / performance issues)
- Assertion failures (logic bugs in SUT)
- Dependency failures (external service unavailable)
- Resource exhaustion (memory/disk space)
- Race conditions (concurrency-related flakes)

**Failure Types with Lower Accuracy:** [Specific categories not disclosed]
- Likely: intermittent flakes, race conditions, cascading failures

### User Feedback Integration

The 5.8% "not helpful" rate provides actionable data:
- Users can flag when diagnosis is incorrect
- Feedback aggregated per team and failure category
- Informs future prompt refinement and multi-agent approaches

## Practical Applications & Use Cases

### 1. **Code Review Integration**
Primary deployment: developers see diagnosis as they review code changes that introduce test failures. This contextual integration is critical—developers don't need to leave their workflow.

### 2. **Organizational Scale**
Applicable to any large engineering organization with:
- High volume of integration tests
- Diverse codebases and failure modes
- Heterogeneous log sources
- Need for rapid developer feedback

### 3. **Extending to Multi-Agent Repair**
While Auto-Diagnose focuses on diagnosis, the infrastructure enables extension:
- **Tester Agent:** Analyzes logs → root cause
- **Debugger Agent:** Proposes code fixes based on diagnosis
- **Verifier Agent:** Tests proposed fix candidates
- Agents coordinate via prompt chaining or structured APIs

### 4. **Specialized Domains**
Beyond integration tests:
- **Performance regression investigation:** Analyze performance traces
- **Production incident debugging:** Analyze application logs at scale
- **Flaky test diagnosis:** Identify intermittent failure patterns

## Insights & Implications

### 1. **LLMs Are Production-Ready for Structured Diagnosis**
Auto-Diagnose proves LLMs can solve real engineering problems at scale with high accuracy (90%+), not just research benchmarks. The key: well-engineered prompts + clear task definition.

### 2. **Workflow Integration Matters More Than Accuracy**
A 90% accurate tool integrated into developer workflow (Critique) has vastly more impact than a 95% accurate tool requiring developers to use a separate interface. The lesson: **usability architecture affects practical impact**.

### 3. **Prompt Engineering Outperforms Fine-Tuning**
Despite Google's access to massive internal data, prompt engineering on a general-purpose model proved sufficient. This suggests:
- Domain-specific fine-tuning has diminishing returns for well-structured tasks
- Transfer learning from general-purpose models is powerful
- Reduces need for collecting and maintaining training datasets

### 4. **Multi-Agent Patterns Emerge Naturally**
While Auto-Diagnose is single-agent, the paper's related work discusses natural multi-agent decomposition:
- **Tester agent:** Symptom identification
- **Debugger agent:** Root cause analysis + fix generation
- **Verifier agent:** Solution validation

This suggests multi-agent approaches for end-to-end failure resolution (diagnosis + repair).

### 5. **Scale Enables New Possibilities**
Processing 224,782 test executions reveals patterns impossible to detect manually:
- Common failure signatures across teams
- Systemic infrastructure issues
- Regressions introduced by code changes
- Opportunities for automated fixes

### 6. **Remaining Challenges**
- **Intermittent flakes:** Race conditions and timing-dependent failures harder to diagnose
- **Cascading failures:** When A fails and causes B to fail, determining which is root cause
- **Infrastructure-related:** Failures in external services without rich logs

## Code & Resources

**Official Release:** Internal Google system (not open-source)
- Integrated into Critique code review system
- Not available as standalone tool

**Relevant Public Work:**
- Related papers on LLM-based program repair and debugging
- GitHub: Look for public implementations inspired by Auto-Diagnose

**Dependencies & Requirements:**
- LLM API access (Google Gemini, OpenAI GPT, or equivalent)
- Log aggregation infrastructure (Fluentd, ELK, Datadog, or custom)
- Code review system integration capability
- Python/Go backend for orchestration

**Quick Implementation Guide (for other organizations):**

1. **Set up log collection:**
   - Capture test driver logs
   - Aggregate SUT logs (possibly from distributed systems)
   - Normalize timestamps and correlate events

2. **Craft task-specific prompt:**
   - Define what "root cause" means for your failures
   - Specify failure categories relevant to your system
   - Include examples of well-diagnosed failures

3. **Integrate into developer workflow:**
   - Connect to code review system
   - Show diagnosis as developers introduce failing tests
   - Collect user feedback for iteration

4. **Monitor accuracy:**
   - Periodically sample results for manual review
   - Track which failure types are diagnosed correctly
   - Refine prompts based on errors

## Related Work & Context

### Prior Work on Test Failure Diagnosis
- **Static analysis approaches:** Pattern matching on log signatures
- **ML-based approaches:** Trained classifiers on historical failures
- **Manual approaches:** Expert SWEs analyzing logs (baseline)

Auto-Diagnose improves on these by leveraging LLM semantic understanding.

### LLM-Based Software Engineering
- **Copilot/CodeX:** Code completion and generation
- **CodeBERT-based approaches:** Semantic code search and repair
- **LLM-based debugging:** This work and others exploring diagnosis automation

### Multi-Agent Debugging Systems
The paper references multi-agent patterns relevant to this repository:
- **Agent Communication:** How Tester and Debugger agents coordinate
- **Hierarchical Orchestration:** Diagnosis then repair workflows
- **Iterative Refinement:** Agents improving solutions through feedback loops

### Connection to Repository Themes

1. **Tool Use & LLM Agents:** Auto-Diagnose shows LLMs as specialized tools (diagnosis) within larger software development workflows
2. **Multi-Agent Testing & Debugging:** Foundation for coordinating diagnosis + repair agents
3. **Skill-Based Agent Architectures:** Each agent (Tester, Debugger) represents specialized skill
4. **Production Agentic Systems:** Demonstrates real-world deployment patterns and challenges

### Future Research Directions

1. **End-to-End Repair:** Extend diagnosis to automated fix generation and validation (multi-agent pipeline)
2. **Interpretability:** Explain *why* the system believes the diagnosis is correct
3. **Few-Shot Learning:** Adapt to new failure types with minimal examples
4. **Proactive Prevention:** Use diagnosed failure patterns to suggest code improvements before failures occur
5. **Cross-Organizational Patterns:** Share failure signatures across Google projects and beyond

## Summary

Auto-Diagnose represents a milestone in applying LLMs to production software engineering challenges. By demonstrating 90%+ accuracy on real integration test failures at scale, seamless workflow integration, and practical deployment across thousands of developers, it proves that agentic systems can solve long-standing developer pain points. The paper's insights on multi-agent coordination (Tester + Debugger patterns) and prompt engineering serve as foundations for building comprehensive autonomous software engineering systems that handle diagnosis, repair, and verification.
