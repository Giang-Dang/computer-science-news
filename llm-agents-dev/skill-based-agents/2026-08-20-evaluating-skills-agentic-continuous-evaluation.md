# Evaluating Skills, Not Just Agents: Agentic Continuous Evaluation of Skills

**ArXiv ID:** 2608.20614  
**Authors:** Christopher Kevin, Narendran Raghavan, Jean-Francois Puget (NVIDIA)  
**Affiliation:** NVIDIA  
**Publication Venue:** Agent Skills '26 (ACM CAIS 2026), KDD 2026 Workshop on Enterprise AI Agents  
**Submission Date:** August 20, 2026

## Executive Summary

As enterprise agent systems transition from prototypes to production, organizations face a critical challenge: **evaluating whether reusable skills (code packages, tools, workflows) actually improve agent performance on real tasks**. This paper introduces **ACES (Agentic Continuous Evaluation of Skills)**, a repository-native evaluation framework that measures skill effectiveness through live paired trials. Unlike traditional code review gates (which check style and security), ACES directly measures **Skill Lift**: the marginal value a skill contributes to agent task completion. Deployed in NVIDIA's SkillEvaluator framework and evaluated on 145 enterprise skills, ACES provides the first systematic methodology for skill-based agent development, addressing a critical gap in agent lifecycle management.

## Problem Statement

Enterprise agent deployments are evolving from single-agent prototypes to **skill-augmented multi-agent systems**. However, skill validation practices lag decades behind traditional software engineering:

**The Skill Evaluation Gap:**

**Current State (Pre-ACES):**
- Code review gates scan skills for structure, style, and security violations
- No gates verify whether skills actually help agents
- "Skill theater": skills that pass review but degrade agent performance
- False positives: skills that fail review but would improve performance

**Enterprise Pain Points:**
1. **Production Risk:** Skills deployed without evidence of task improvement
2. **Resource Waste:** Teams invest in skills that don't help agent goal completion
3. **Blind Optimization:** No metrics to compare skill implementations or identify best practices
4. **Skill Proliferation:** Unclear which of many similar skills to use (no ranking system)

**Why This Is Hard:**

Traditional metrics fail for skills:
- **Code coverage:** Does not measure agent helpfulness
- **Latency:** Skills may slow agents but improve accuracy (net positive)
- **Style checks:** Orthogonal to actual value delivered
- **Agent benchmarks:** Test fixed datasets; don't measure skill impact on live agent workflows

**Research Gap:** Can we quantify the empirical impact of individual skills on agent task completion? What methodology properly isolates skill contribution from agent variance?

## Core Concepts & Theory

### Skill Definition in Agentic Systems

**A skill in the enterprise agent context:**
- Reusable capability package: code, tools, workflows, prompts
- Designed to augment agent reasoning or action
- Can be: tool implementations, retrieval pipelines, specialized reasoners, workflow orchestrators
- Deployed as versioned, reviewed artifacts

### The Skill Lift Concept

**Skill Lift** = Marginal value of skill conditional on fixed agent, model, task, harness, and scorer

```
Skill Lift = Score(WITH skill) - Score(WITHOUT skill)
```

**Key Properties:**
- **Counterfactual evaluation:** Paired trials measure only the skill's contribution
- **Normalized across conditions:** Isolates skill effect from task randomness
- **Model-agnostic:** Works with any agent and underlying LLM
- **Production-realistic:** Evaluates in live deployment environment

### Paired Trial Methodology

The ACES framework uses **A/B testing for skills**:

```
┌─────────────────────────────────────────────────────────┐
│                    Target Task                           │
└────────────┬─────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│ WITH Skill   │  │ WITHOUT Skill     │
│ (Condition A)│  │ (Condition B)     │
└──────┬───────┘  └────────┬─────────┘
       │                   │
       ▼                   ▼
┌──────────────┐  ┌──────────────────┐
│ Live Agent   │  │ Baseline Agent    │
│ Full skills  │  │ Target skill      │
│              │  │ withheld (others  │
│              │  │ fixed)            │
└──────┬───────┘  └────────┬─────────┘
       │                   │
       ▼                   ▼
┌──────────────────────────────────────┐
│      Trajectory (Execution Log)       │
│  - Actions taken                      │
│  - Tool invocations                   │
│  - Reasoning steps                    │
│  - Final outcome                      │
└──────┬───────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ ATIF: Agent Trajectory Interchange Format               │
│ (Standardized trajectory representation)                │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ Grading: Six Default Runtime Metrics                    │
│  1. Task completion rate                                │
│  2. Steps to completion                                 │
│  3. Tool invocation efficiency                          │
│  4. Error recovery rate                                 │
│  5. Resource usage                                      │
│  6. Custom domain metrics                               │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ SKILL LIFT REPORT                                       │
│ Skill value = WITH score - WITHOUT score                │
│ Statistical significance & confidence intervals         │
└─────────────────────────────────────────────────────────┘
```

### Agent Trajectory Interchange Format (ATIF)

ACES introduces **ATIF**, a standardized format for agent execution logs:
- **Language-agnostic:** Represents any agent's trajectory
- **Reproducible:** Identical trajectories → identical grading
- **Comparable:** Enables cross-agent skill evaluation
- **Extensible:** Custom metrics can be computed from ATIF

**ATIF Captures:**
- Sequence of agent actions (think, call_tool, reason)
- Tool invocations and arguments
- Observations returned from environment
- Reasoning intermediate steps
- Final state and outcome

## Main Ideas & Contributions

### 1. ACES Framework: Paired Live Evaluation

**Core Innovation:** Live paired trials that isolate skill effect

**Two Conditions:**
- **Condition A (WITH skill):** Target skill is available to agent
- **Condition B (WITHOUT skill):** Target skill is withheld; prerequisites, helpers, references, and decoy skills remain fixed

**Why paired design matters:**
- Eliminates task variance (same task, same agent, same execution context)
- Isolates contribution of single skill
- Enables statistical significance testing (paired difference tests)
- Reflects production-realistic conditions

### 2. ATIF: Standard Trajectory Representation

ACES standardizes how agent executions are captured and scored:

**ATIF Components:**
```json
{
  "agent_id": "agent-001",
  "model": "claude-opus-5",
  "task": "resolve_github_issue_42",
  "condition": "with_skill_code_review",
  "trajectory": [
    {
      "step": 1,
      "type": "think",
      "reasoning": "User wants to fix memory leak...",
      "timestamp": "2026-08-20T14:32:00Z"
    },
    {
      "step": 2,
      "type": "call_tool",
      "tool": "code_search",
      "args": {"pattern": "malloc.*without_free"},
      "observation": "Found 3 suspicious patterns in src/memory.c"
    },
    {
      "step": 3,
      "type": "think",
      "reasoning": "These allocations need cleanup..."
    },
    {
      "step": 4,
      "type": "call_tool",
      "tool": "code_review_skill",
      "args": {"file": "src/memory.c", "lines": "10-25"},
      "observation": "Recommendation: add cleanup on line 23"
    }
  ],
  "final_state": {
    "success": true,
    "actions_taken": 8,
    "tools_used": ["code_search", "code_review_skill", "git_commit"],
    "tokens_used": 4200
  }
}
```

### 3. Six Default Runtime Metrics

ACES provides built-in metrics that apply across domains:

| Metric | Definition | Production Value |
|--------|-----------|------------------|
| **Task Completion** | Success rate on target task | Direct ROI measure |
| **Steps to Completion** | Agent steps until goal achieved | Efficiency, cost |
| **Tool Efficiency** | Ratio of useful to total tool calls | Redundancy detection |
| **Error Recovery** | Rate of error-correction success | Robustness |
| **Resource Usage** | Tokens, API calls, latency | Cost control |
| **Domain-Specific** | Custom metrics per task | Flexibility |

### 4. Empirical Evaluation on Enterprise Skills

ACES evaluated 145 real skills from:
- NVIDIA internal enterprise repositories
- Public skill catalogs (open-source agent frameworks)

**Study Coverage:**
- Skill categories: retrieval, reasoning, tool integration, workflow orchestration
- Agent types: support agents, development agents, research assistants
- Domains: customer support, code review, document analysis

**Findings** [Exact figures unavailable — see full paper]:
- Percentage of skills with positive skill lift: [data from paper]
- Average skill lift across evaluated skills: [data from paper]
- Variance in skill quality: [data from paper]
- Correlation between code review pass rate and skill lift: [data from paper]

## Methodology & Implementation

### ACES Implementation in NVIDIA SkillEvaluator

The ACES evaluation methodology is operationalized in **NVIDIA SkillEvaluator**, a multi-tier framework:

**Tier 1: Basic Trajectory Capture**
- Logs raw agent actions
- Minimal overhead

**Tier 2: ATIF Standardization**
- Converts logs to ATIF format
- Enables interoperability

**Tier 3: Paired Evaluation (ACES)**
- Runs WITH and WITHOUT conditions
- Computes Skill Lift
- Provides statistical analysis

### Experimental Protocol

**For each skill in the evaluation set:**

1. **Preparation:**
   - Identify representative task set for skill domain
   - Define grading criteria (task success, efficiency, etc.)
   - Configure agent and model

2. **Baseline Run (WITHOUT skill):**
   - Run agent on task set without target skill
   - Record trajectories → ATIF
   - Compute baseline metrics

3. **Augmented Run (WITH skill):**
   - Add target skill to agent
   - Keep all other configurations identical
   - Run same task set
   - Record trajectories → ATIF

4. **Analysis:**
   - Normalize scores (handle task variance)
   - Compute Skill Lift = WITH - WITHOUT
   - Test statistical significance
   - Identify which tasks benefit from skill

### Dataset

**145 Enterprise Skills** evaluated across:
- **Retrieval Skills:** RAG implementations, vector search augmentations
- **Reasoning Skills:** Chain-of-thought prompts, structured reasoning workflows
- **Tool Skills:** Novel tool integrations, tool composition patterns
- **Workflow Skills:** Multi-step orchestration patterns

### Scoring

Metrics are normalized to 0-1 scale:
- Task success: binary (1 = success, 0 = failure)
- Steps to completion: normalized by max reasonable steps
- Tool efficiency: (useful_calls / total_calls)
- Error recovery: count / attempts
- Resource usage: normalized by median usage

**Skill Lift = Average(WITH metrics) - Average(WITHOUT metrics)**

## Results & Analysis

### Skill Effectiveness Distribution

**Key Finding:** Skill quality is highly variable; many skills show zero or negative lift

**Observed Distribution** [Exact figures unavailable — see full paper]:
- High-value skills (Skill Lift > 20%): [percentage]
- Neutral skills (Lift ≈ 0 ± 5%): [percentage]
- Negative skills (Lift < -10%): [percentage]

**Interpretation:**
- Not all published skills are production-ready
- Code review gates do not correlate with actual value
- Skills optimized for one domain may not transfer

### Correlation: Code Review vs. Skill Lift

**Critical Finding:** Code review pass rate does NOT strongly correlate with Skill Lift

This means:
- A skill passing style/security review may not help agent task completion
- Conversely, a skill with style issues might significantly improve performance
- Traditional gate criteria are insufficient for agent systems

### Skill Categories Performance

**Ranking by average Skill Lift** [Based on paper findings]:
1. **Workflow Orchestration Skills:** Highest average lift (structured task decomposition)
2. **Retrieval Skills:** Medium-high lift (context quality matters)
3. **Reasoning Skills:** Medium lift (inconsistent gains across models)
4. **Tool Skills:** Variable (depends on implementation quality)

### Statistical Significance

ACES provides confidence intervals for Skill Lift:
- Narrow CI: skill effect is reliable across tasks
- Wide CI: skill performance is task-dependent (conditional usefulness)

## Practical Applications & Use Cases

### 1. Skill Marketplace Quality Gates

**Current Process:** Manual code review + user feedback

**ACES-Enabled Process:**
- Code review (baseline)
- ACES evaluation on 3-5 representative tasks
- Skill Lift report guides approval decision
- Publish skills only with demonstrated positive lift (or clearly conditional lift)

**Impact:** Reduce production failures from low-quality skills

### 2. Skill Optimization & Ranking

**Use Case:** Organization has 20 similar code-review skills; which to recommend?

**Traditional Answer:** First available, author reputation

**ACES Answer:** Rank by Skill Lift on representative tasks

**Outcome:** Developers adopt highest-value skills; resource consolidation

### 3. Continuous Skill Degradation Detection

**Problem:** Skill quality changes as agent models update

**Solution:** Re-run ACES evaluation quarterly/per major model release

**Workflow:**
```
Agent model upgrade (v1 → v2)
  → Re-run ACES on all published skills
  → Identify skills with degraded Skill Lift
  → Alert maintainers or deprecate
  → Developers understand compatibility
```

### 4. Developer Feedback Loop

**Before ACES:**
- Skill author: "I built a code review skill"
- Developer: Uses it, finds it unhelpful
- Outcome: Orphaned skill, wasted effort

**With ACES:**
- Skill author: Runs ACES evaluation, gets Skill Lift report
- If Lift < 0: Iterate, improve, re-evaluate
- If Lift > 0: Publish with confidence metrics
- Developers: Choose skills with high, measured impact

## Insights & Implications

### 1. Skill Lift Matters More Than Code Quality

The paper's core insight: **a well-designed but informally-written skill that improves agent performance (high Skill Lift) is more valuable than a perfectly-formatted skill that degrades performance (negative Skill Lift)**.

This inversion of traditional software engineering values reflects agent systems' unique requirements: agent helpfulness > code style.

### 2. Production Readiness for Agent Skills

Proposed maturity model:
- **Level 1:** Code review pass (syntax, security)
- **Level 2:** ACES evaluation with positive Skill Lift
- **Level 3:** Replication across multiple agents/models (transfer validation)
- **Level 4:** Production monitoring with continuous Skill Lift tracking

### 3. Skill-Model Co-Evolution

Different models respond differently to skills:
- Gemini may show high Lift for reasoning skills
- Claude may show high Lift for retrieval skills
- Codex may show high Lift for code-specific tools

**Implication:** Skills should declare model compatibility based on ACES evaluation (e.g., "Tested on Gemini; untested on Codex")

### 4. Research Implications

ACES enables novel research directions:
- **Skill Composition:** Do skills combine additively or interact?
- **Skill Transfer:** Do skills learned on one task transfer to others?
- **Skill Design Patterns:** What design patterns yield high Skill Lift?
- **Skill Emergence:** Can agents automatically discover useful skills?

## Code & Resources

**NVIDIA SkillEvaluator Framework:**
- **Availability:** Open-source implementation of ACES
- **Tiers:** Tier 3 operationalizes paired evaluation protocol
- **Language:** Python-based, agent-agnostic
- **Link:** [Repository/documentation link — see full paper]

**ATIF Specification:**
- **Format:** JSON with standardized schema
- **Tools:** Libraries for trajectory capture and ATIF conversion
- **Extensibility:** Custom metrics can be computed from ATIF

**Evaluation Dataset:**
- 145 enterprise skills (internal + public)
- Benchmark task sets per domain
- Reference trajectories and scores

## Related Work & Context

### Related Multi-Agent & Skill-Based Agent Papers

1. **Skill-Based Agent Architectures:**
   - "Harnessing Agent Skills: Architectural Patterns and a Reference Architecture for Skill-Mediated LLM Agents" (arXiv 2606.20631)
   - "SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks" (arXiv 2602.12670)
   - "Not All Skills Help: Measuring and Repairing Agent Knowledge" (arXiv 2606.15390)

2. **Skill Optimization & Evaluation:**
   - "SkillAxe: Sharpening LLM-Authored Agent Skills Through Evaluation-Guided Self-Refinement" (arXiv 2606.10546)
   - "SkillFlow: Benchmarking Lifelong Skill Discovery and Evolution for Autonomous Agents" (arXiv 2604.17308)
   - "Trace2Skill: Verifier-Guided Skill Evolution for Long-Context EDA Agents" (arXiv 2605.21810)

3. **Agent Evaluation Frameworks:**
   - "Agent Skill Evaluation and Evolution: Frameworks and Benchmarks" (arXiv 2606.11435)
   - "A Framework for Evaluating Agentic Skills at Scale" (arXiv 2606.17819)
   - "Skill Use or Skill Theater? Evaluating the Reasoning Backroom in Skill-Augmented Language Agents" (arXiv 2607.27484)

### Foundational Concepts

- **A/B Testing for Software:** Traditional paired comparison methodology adapted to agent systems
- **Agent Evaluation:** Benchmarks like SWE-bench, HumanEval, etc. (measure agent capability, not skill value)
- **Contribution Analysis:** Statistical methods for isolating component effects in complex systems

### Future Research Directions

1. **Automatic Skill Discovery:** Can agents automatically generate high-Lift skills?
2. **Skill Composition Theory:** How do skills interact? Are there fundamental composition patterns?
3. **Zero-Shot Skill Transfer:** Can we predict Skill Lift without running full ACES evaluation?
4. **Skill-Model Compatibility:** Formal framework for predicting skill-model interactions
5. **Adversarial Skills:** Skills that degrade performance; understanding why

## Significance to Agentic Software Development

**ACES solves a critical problem in enterprise agent deployment:** the ability to objectively measure whether skills improve agent performance. Before ACES, skill value was measured subjectively (user feedback, anecdotes); now it can be quantified rigorously.

**For Enterprise Agents:**
- Provide objective skill selection guidance
- Enable confident skill deployment
- Support continuous quality monitoring
- Guide skill developers toward high-impact improvements

**For Agent Skill Developers:**
- Know whether your skill actually helps agents (quantified)
- Understand task- and model-specific effectiveness
- Iterate based on empirical Skill Lift data
- Build production-ready skills, not prototypes

**For Agent Framework Designers:**
- ATIF provides interoperable trajectory format
- Enable multi-agent skill portability
- Support ecosystem of evaluated skills
- Bridge gap between academia and production

**The bigger picture:** ACES is to agent skills as unit testing is to software: a foundational quality assurance practice that should become industry standard. Without it, enterprise agent deployments remain high-risk, skill-dependent, and difficult to optimize.
