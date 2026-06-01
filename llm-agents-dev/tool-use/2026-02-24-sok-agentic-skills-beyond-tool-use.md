# SoK: Agentic Skills -- Beyond Tool Use in LLM Agents

**Paper:** [SoK: Agentic Skills -- Beyond Tool Use in LLM Agents](https://arxiv.org/abs/2602.20867)  
**ArXiv ID:** 2602.20867  
**Submission Date:** February 24, 2026  
**Authors:** Yanna Jiang, Delong Li, Haiyu Deng, Baihe Ma, Xu Wang, Qin Wang, Guangsheng Yu  
**Affiliations:** University of Technology Sydney, CSIRO Data61, Macquarie University, Westlake University  

## Executive Summary

This systematization of knowledge (SoK) paper shifts the conceptual foundation for agent-augmented systems from simple "tool use" to reusable, composable "agentic skills." Agentic skills are callable modules that package procedural knowledge with explicit applicability conditions, execution policies, termination criteria, and reusable interfaces. The paper identifies seven design patterns for skill lifecycle management (discovery, practice, distillation, storage, composition, evaluation, and update), provides a comprehensive taxonomy of skill representations and scopes, and surfaces security implications through the lens of the ClawHavoc campaign, in which nearly 1,200 malicious skills infiltrated a major agent marketplace. This work establishes foundational vocabulary and architectural guidance for skill-based agent systems at enterprise scale.

## Problem Statement

**The Tool Use Limitation:**
Traditional agent frameworks treat tool access as atomic function calls (e.g., "call file_read(path)"). This model:
- Doesn't support abstraction: agents cannot compose atomic tools into recurring patterns
- Creates duplication: agents re-solve the same subtasks repeatedly (e.g., "find files matching pattern")
- Lacks governance: no way to enforce organizational constraints (security policies, cost controls)
- Scales poorly: adding new tools requires retraining or rewriting agent prompts

**Why "Agentic Skills" Matter:**
In large organizations, teams accumulate domain expertise—patterns for deployment, testing, debugging, compliance. This knowledge exists as:
- Runbooks (human procedures, not executable)
- Code libraries (static, not adaptive)
- Tribal knowledge (documentation, Slack archives, nobody remembers)

**Research Gap:**
No systematic understanding of:
1. How skills differ from tools or APIs
2. What lifecycle stages skills pass through
3. How to package skills for reuse and governance
4. What security risks emerge in skill-based systems
5. How skills scale from individual agents to enterprise marketplaces

## Core Concepts & Theory

### What are Agentic Skills?

**Definition:** A skill is a callable, reusable procedural module that encodes *what* to do, *when* to apply it, *how* to execute safely, and *when* to stop.

**Skill vs. Tool vs. API:**

| Aspect | Tool | API | Skill |
|--------|------|-----|-------|
| **Scope** | Single action (e.g., read file) | Set of related functions | Procedural strategy (e.g., find-and-migrate) |
| **Preconditions** | Implicit (docs) | Implicit | Explicit (applicability conditions) |
| **Error handling** | Caller's responsibility | Caller's responsibility | Skill-managed (fallback, retry) |
| **Composition** | Via orchestration | Via client code | Via skill chaining |
| **Governance** | Basic | Basic | Rich (cost limits, approval chains) |
| **Learning** | Static | Static | Can evolve (self-improving) |

### Skill Lifecycle (Seven Stages)

```
Discovery → Practice → Distillation → Storage → Composition → Evaluation → Update
    ↓           ↓           ↓          ↓          ↓             ↓          ↓
   Identify    Execute   Extract    Archive   Chain with    Measure    Learn
   problems   repeatedly  patterns   formally   other skills performance from
   needing                 into                              and adapt  failures
   skills                  skill                            outcomes
```

#### 1. **Discovery:** Problem Recognition
- Agents encounter recurring subtasks
- Example: "find files matching regex" appears 5+ times across issues
- Trigger: performance plateau, repeated failures, high token usage

#### 2. **Practice:** Repeated Execution
- Agents execute the same procedural pattern multiple times
- Feedback accumulates (success cases, edge cases, failure modes)
- In-context learning: prompt examples grow more sophisticated

#### 3. **Distillation:** Pattern Extraction
- Generalize from specific examples to reusable procedure
- Abstract away concrete values (file paths) into parameters
- Identify termination conditions (when to stop iterating)

#### 4. **Storage & Formalization:** Persistent Representation
- Encode in format suitable for reuse:
  - Natural language description (for discoverability)
  - Executable code (Python, REST endpoint)
  - Formal policy (preconditions, cost limits, approval chains)
- Register in skill library or marketplace

#### 5. **Composition:** Skill Chaining
- Combine skills into larger workflows
- Example: "migrate-function" skill uses "find-calls" and "update-signature" as sub-skills
- Agents dynamically select composition strategy based on context

#### 6. **Evaluation:** Measurement & Benchmarking
- Measure quality: correctness, latency, cost
- A/B test against alternatives
- Identify performance gaps (when skill fails systematically)

#### 7. **Update:** Continuous Improvement
- Self-evolving skills: learn from execution feedback
- Versioning: manage breaking changes
- Deprecation: retire skills as better alternatives emerge

### Design Patterns for Skill Implementation

The paper identifies seven design patterns capturing how skills are packaged in practice:

#### 1. **Metadata-Driven Progressive Disclosure**
Skill represented as metadata + handler:
```json
{
  "name": "find-files",
  "description": "Recursively find files matching pattern",
  "preconditions": ["directory exists", "read permission"],
  "parameters": [
    {"name": "root_path", "type": "string", "description": "..."},
    {"name": "pattern", "type": "regex", "required": true}
  ],
  "cost_limit": {"tokens": 500, "time_sec": 10},
  "handler": "functions.find_files"
}
```
Agent discovers available skills via metadata without parsing code.

#### 2. **Executable Code Skills**
Skills as executable Python/JavaScript:
- Pro: full expressiveness, easy to test
- Con: security risk (arbitrary code execution), no static analysis
- Mitigation: sandboxing, static analysis, signed code

#### 3. **Formal Policies & Guards**
Skills with explicit governance:
```
Permission: can invoke "deploy-to-production"
Only if: approval_count >= 2 AND cost_estimate <= $1000
Retry policy: exponential backoff, max 3 attempts
Timeout: 5 minutes
Audit: log all invocations with context
```

#### 4. **Skill Composition Graphs**
Skills as nodes, dependencies as edges:
```
request-review → approve-changes → merge-pr → deploy
                       ↑              ↓
                  assign-reviewer  run-tests
                       ↓              ↓
                   notify-team   report-status
```

#### 5. **Self-Evolving Skill Libraries**
Skills that update their own prompts/parameters based on success/failure:
- Pattern: track success rate per parameter setting
- Adapt: update prompts if success rate drops
- Versions: maintain multiple versions, agents A/B test

#### 6. **Marketplace Distribution**
Skills published to centralized or decentralized marketplaces:
- **Centralized:** GitHub Marketplace, AWS Bedrock Tools
- **Decentralized:** blockchain-based registries, peer-to-peer
- Challenge: discovery, authentication, version management

#### 7. **Hybrid Representations**
Skills combining multiple patterns:
- NL description + code + formal policy + marketplace metadata
- Enables multiple use cases: human discovery, agent invocation, governance audit

### Taxonomy: What Skills Are (Representation × Scope)

**Representation Axis (How is the skill encoded?):**
1. **Natural Language:** descriptive text, runbook-style
2. **Code:** Python, JavaScript, SQL
3. **Policy:** formal specifications, constraint languages
4. **Hybrid:** combination of above

**Scope Axis (What domain does the skill operate in?):**
1. **Web:** browser automation, API interactions
2. **OS:** file system, shell commands
3. **Software Engineering:** code analysis, testing, deployment
4. **Robotics:** physical tasks, sensor integration
5. **Domain-Specific:** tax code, medical diagnosis, legal research

**Example Positions in the Taxonomy:**

| Domain | NL | Code | Policy | Hybrid |
|--------|----|----|--------|--------|
| **Web** | "Query this web API" | Selenium script | Rate limits | NL + Policy |
| **OS** | "Find files" | bash find command | File ACLs | Code + Policy |
| **SoftEng** | "Run tests" | pytest runner | Cost budget | All three |

## Main Ideas & Contributions

### 1. Agentic Skills as a Distinct Abstraction Layer

Skills are neither tools nor libraries—they represent a new abstraction layer with:
- **Applicability conditions:** skills know when they're applicable
- **Execution semantics:** skills manage their own error handling, retries, timeouts
- **Governance policies:** skills encode organizational constraints
- **Composability:** skills can invoke other skills without orchestrator intervention

**Impact:** Enables enterprise agents to operate autonomously within governance bounds, reducing the need for human oversight on routine decisions.

### 2. Skill Lifecycle as an Architecture Pattern

The seven-stage lifecycle (discovery → practice → distillation → storage → composition → evaluation → update) mirrors how human organizations evolve procedural knowledge:
- **Before:** Runbook in Confluence, nobody reads it
- **With Skills:** Executable, versioned, auditable, continuously improving

**Implication:** The path from "repeated task" to "trusted organizational skill" is well-understood; frameworks can support this path explicitly.

### 3. Security and Governance at Marketplace Scale

The ClawHavoc case study revealed:
- **1,200+ malicious skills** infiltrated a major agent marketplace
- **Attack vectors:**
  - Skill payload contains injected prompt (prompt injection)
  - Skill code exfiltrates API keys, cryptocurrency wallets
  - Skill masquerades as legitimate (typosquatting: "deploy_securely" vs "deploy-securely")
- **Damage:** API keys stolen, wallets emptied, credentials exfiltrated at scale

**Security Principles for Skill Marketplaces:**
1. **Code signing and verification:** cryptographic attestation
2. **Sandboxing:** skill code runs in restricted containers
3. **Trust tiers:** skills vetted by organization vs. community
4. **Supply-chain attestation:** verify provenance of dependencies
5. **Dynamic analysis:** audit skills in test environments before deployment

### 4. Skill Composition as Orchestration Simplification

Instead of agents invoking 50+ tools, skills reduce to 5-10 high-level capabilities:
- **Agents become simpler:** focus on planning, not implementation details
- **Orchestration becomes easier:** skill composition graphs replace complex prompts
- **Reuse increases:** teams share skills across projects
- **Cost decreases:** skills abstract away low-level inefficiencies

## Methodology & Implementation

### Empirical Grounding

The paper is primarily a systematization of knowledge (SoK) survey, grounded in:

1. **Literature Review:**
   - 150+ papers on agent systems, tools, orchestration
   - Analysis of industrial frameworks (AWS Bedrock, Microsoft Copilot Agents)
   - Study of open-source implementations (LangChain, AutoGPT)

2. **Architectural Analysis:**
   - Six design patterns identified from deployed systems
   - Lifecycle stages derived from qualitative interviews with practitioners
   - Security taxonomy based on ClawHavoc incident post-mortem

3. **Case Studies:**
   - **ClawHavoc:** nearly 1,200 malicious skills in marketplace
     - Attack patterns: prompt injection, code obfuscation, credential exfiltration
     - Root causes: insufficient vetting, no code signing, trust propagation
   - **Enterprise Deployments:** companies using skills for deployment, testing, compliance
     - Success factors: clear governance policies, version management, audit logging
     - Failure modes: skills with side effects, circular dependencies, unclear preconditions

### Framework Validation

No formal benchmarks (SoK paper), but patterns validated against:
- **Existing systems:** how well do the seven design patterns explain real implementations?
- **Security incidents:** does the threat taxonomy cover known attacks?
- **Practitioner feedback:** do teams find the lifecycle stages useful?

## Practical Applications & Use Cases

### 1. Enterprise Software Deployment

**Scenario:** Deploy microservice changes to production

**Skill Composition:**
```
deploy-service = [
  validate-code,
  run-integration-tests,
  create-deployment-plan,
  request-approval,
  execute-blue-green-deployment,
  monitor-service-health
]
```

**Governance:**
- validate-code: can run without approval
- request-approval: requires 2 approvals for production
- execute-blue-green-deployment: logs all changes to audit trail

**Benefit:** agents can orchestrate complex deployments without hardcoding approval chains; governance evolves independently.

### 2. Data Pipeline Orchestration

**Scenario:** ETL pipeline that adapts based on data quality

**Skills:**
- extract: pull data from source
- validate: check for anomalies
- alert-on-quality: trigger if data quality below threshold
- transform-with-fallback: apply transformation or fallback logic
- load: persist to warehouse

**Self-Evolving:** if transform-with-fallback success rate drops, agent requests updated parameters.

### 3. Security Compliance and Auditing

**Scenario:** Ensure all deployments meet regulatory requirements

**Skills:**
- scan-for-secrets: detect hardcoded credentials
- verify-ssl-certificates: check certificate validity and pinning
- audit-access-controls: verify IAM policies
- generate-compliance-report: document findings

**Composable:** agents combine for different regulations (SOC2, HIPAA, GDPR).

### 4. Bug Triage and Root Cause Analysis

**Scenario:** Incoming bug reports, prioritize and route to teams

**Skills:**
- parse-bug-report: extract components, symptoms, environment
- reproduce-issue: attempt to reproduce in test environment
- search-similar-issues: find related past issues
- assign-priority: determine severity and urgency
- route-to-team: send to appropriate team based on component

## Insights & Implications

### 1. From Tool Calls to Skill-Driven Autonomy

**Current State:** agents call tools, orchestrator coordinates
**Future State:** agents invoke skills, skills self-manage error handling and governance

This shift enables:
- Agents to be smarter (less orchestration code)
- Governance to be automated (policies embedded in skills)
- Reuse to be systematic (skills versioned and discoverable)

### 2. Skills Enable Organizational Learning

When a team solves a problem (e.g., "deploy without downtime"), encoding it as a skill:
- Captures domain expertise
- Makes it reusable across projects
- Allows continuous improvement (A/B test variants)
- Auditable (who ran which version when?)

**Implication:** Over time, organizations shift from "humans are the bottleneck" to "skill quality is the bottleneck."

### 3. Marketplace Security is Critical

ClawHavoc showed that even with governance intentions, marketplaces can be exploited at scale. Essential protections:
- Code signing (authors cryptographically attest skills)
- Sandboxing (skills can't access arbitrary files or network)
- Attestation (skills declare dependencies; dependencies verified)
- Rate limiting (prevent mass-deployment of malicious skills)
- Community review (reputation systems, flagging)

### 4. Cost and Latency Trade-offs

Skills can be optimized for cost or latency:
- **Cost-optimized:** batch operations, use cheaper APIs
- **Latency-optimized:** parallelize, use premium APIs

**Governance:** skills expose these trade-offs; agents choose based on context (urgent fix vs. routine task).

### 5. Limitations and Open Questions

- **Skill Versioning Complexity:** How do agents handle breaking changes in skill APIs?
- **Circular Dependencies:** Can skill composition graphs have safe circular patterns?
- **Skill Discovery:** How do agents find applicable skills in a large marketplace?
- **Performance Isolation:** Slow skills can cascade; how to prevent performance anti-patterns?
- **Human Understandability:** Can non-experts understand and trust skill behavior?

## Skill Lifecycle Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  DISCOVERY: Recognize Recurring Pattern                      │
│  "Agents solve 'find-files' 5+ times, 50+ token each"       │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│  PRACTICE: Execute Pattern Repeatedly                        │
│  Agents solve it 10+ times, examples accumulate              │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│  DISTILLATION: Extract Generalizable Logic                   │
│  Identify: parameters, preconditions, termination criteria   │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│  STORAGE: Formalize & Register                               │
│  Code + Metadata + Policy → Skill Library                    │
└─────────────────────────┬──────────────────────────────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
        ┌─────────┐ ┌──────────┐ ┌────────┐
        │Compose  │ │ Evaluate │ │ Update │
        │(Skill   │ │(Measure  │ │(Learn  │
        │Chaining)│ │Quality)  │ │& Adapt)│
        └────┬────┘ └────┬─────┘ └───┬────┘
             │           │           │
             └───────────┼───────────┘
                         │
                  ┌──────▼───────┐
                  │ Skill Ready  │
                  │ for Production
                  │ Use
                  └──────────────┘
```

## Code & Resources

### Reference Implementations

**Open-Source Frameworks Supporting Skills:**

1. **LangChain:** Provides `BaseTool` abstraction, extensible for skill-like behavior
   - GitHub: [langchain-ai/langchain](https://github.com/langchain-ai/langchain)
   - Skill pattern: custom Tool classes with error handling

2. **AutoGPT:** Skill-like abstraction through command registries
   - GitHub: [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)

3. **AWS Bedrock Agent Skills:** Industry implementation
   - Docs: [AWS Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/)
   - Pattern: declarative skill definitions + handler functions

4. **OpenAPI-based Skill Definition**
   - Tools can be defined via OpenAPI, automatically discoverable
   - Simplifies marketplace publishing

### Skill Definition Template

```yaml
name: "find-files"
version: "1.0.0"
author: "platform-team@company.com"

description: |
  Recursively find files matching a glob pattern.
  Returns list of matching file paths.

preconditions:
  - "directory_path exists"
  - "caller has read permission on directory_path"

parameters:
  directory_path:
    type: string
    description: "Root directory to search"
  pattern:
    type: string
    description: "Glob pattern (e.g., '*.py', 'test_*.js')"
  max_results:
    type: integer
    default: 1000
    description: "Maximum number of results to return"

cost_policy:
  timeout_seconds: 10
  max_token_cost: 500

error_handling:
  - condition: "path not found"
    action: "retry_with_parent_directory"
  - condition: "permission denied"
    action: "log_and_continue"
  - condition: "timeout"
    action: "return_partial_results"

dependencies:
  - name: "os-file-system-access"
    version: "1.0"

returns:
  type: "list"
  items:
    type: "string"
    description: "Paths to matching files"

audit_logging: true
governance_approval_required: false
```

## Related Work & Context

### Foundational Concepts

- **Tool Use in LLMs:** Gorilla, ToolLLaMA (atomic tool invocation)
- **Procedural Knowledge:** Soar cognitive architecture (procedural vs. declarative memory)
- **Component-Based Systems:** Unix philosophy (small, composable, reusable tools)

### Contemporary Work on Agent Skill Systems

- **Agent Frameworks:** LangChain tools, Anthropic MCP (Modular Capabilities Protocol)
- **Code Agents:** AgentForge (execution-grounded skills), OpenHands
- **Orchestration:** DAG-based workflow engines (Airflow, Prefect)

### Security and Governance

- **Supply Chain Security:** SLSA framework, software bill of materials (SBOM)
- **Marketplace Security:** npm security, PyPI security incidents
- **Sandboxing:** OCI containers, WebAssembly for skill isolation

### Future Directions

1. **Automated Skill Generation:** Can agents synthesize new skills from examples?
2. **Skill Composition Planning:** How do agents optimally order skills in workflows?
3. **Cross-Domain Skill Transfer:** Can a skill learned in one domain transfer to another?
4. **Skill Interpretability:** How to explain to users what a skill does and its failure modes?
5. **Distributed Skill Execution:** Executing skills across multiple systems (federated agents)

## References and Further Reading

- **ArXiv Paper:** [SoK: Agentic Skills -- Beyond Tool Use in LLM Agents](https://arxiv.org/abs/2602.20867)
- **Related SoK Papers:** 
  - [SoK: LLM-Based Agent Architectures](https://arxiv.org/abs/2402.11066)
  - [Agentic AI Frameworks: Architectures, Protocols, and Design Challenges](https://arxiv.org/abs/2508.10146)
- **Agent Security:** [SkillProbe: Security Auditing for Emerging Agent Skill Marketplaces](https://arxiv.org/abs/2603.21019)
