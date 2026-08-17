# Knowledge Activation: AI Skills as the Institutional Knowledge Primitive for Agentic Software Development

**ArXiv ID**: [2603.14805](https://arxiv.org/abs/2603.14805)

**Author**: Gal Bakal

**Submitted**: March 16, 2026 (Revised: June 4, 2026)

**Affiliation**: [Institution to be confirmed from paper]

---

## Executive Summary

This paper addresses a critical bottleneck in agentic software development: the gap between enterprise institutional knowledge and agent-executable knowledge. Rather than expecting LLM agents to reconstruct organizational context from scattered documentation, Knowledge Activation formalizes a framework that transforms latent institutional knowledge into Atomic Knowledge Units (AKUs)—action-ready specifications that agents can discover, understand, and execute reliably. By treating knowledge architecture as a first-class engineering problem, this work enables enterprises to deploy AI coding assistants that operate within organizational constraints, follow established procedures, and improve over time through feedback.

---

## Problem Statement

### The Institutional Knowledge Gap

Enterprise software organizations accumulate critical knowledge across multiple silos:
- **Architectural Decisions**: system design patterns, component responsibilities, integration points
- **Deployment Procedures**: how to safely roll out changes, rollback mechanisms, compliance gates
- **Compliance Policies**: security requirements, data governance, audit requirements
- **Incident Playbooks**: how to respond to failures, root-cause analysis procedures
- **Best Practices**: coding standards, testing requirements, code review criteria
- **Tribal Knowledge**: lessons learned from past projects, gotchas, performance tuning

**The Problem**: This knowledge exists in wikis, design documents, runbooks, code comments, and team members' heads—formats optimized for human interpretation, not machine execution.

### Why Agents Need Better Knowledge Access

When LLM agents attempt to solve development tasks without structured knowledge access:

1. **Context Explosion**: Agents must parse dozens of documents to understand organizational context; input token limits become a hard constraint
2. **Hallucination Risk**: Without access to authoritative procedures, agents make up plausible-sounding (but incorrect) compliance steps
3. **Drift from Policy**: Agents may generate code that violates organizational standards due to lack of awareness
4. **Repeated Learning**: Each agent independently learns organizational patterns instead of leveraging accumulated team knowledge
5. **Onboarding Cost**: New developers and agents must spend weeks absorbing organizational knowledge before being effective

### Research Gap

Prior work has addressed:
- **Retrieval-Augmented Generation (RAG)**: retrieving relevant documents
- **In-Context Learning**: including examples in prompts
- **Fine-Tuning**: adapting models to specific domains

But there was no systematic approach to:
1. **Codify** institutional knowledge into machine-executable form
2. **Compress** knowledge to respect token budgets and attention decay
3. **Compose** knowledge units so agents can navigate complex decision trees
4. **Inject** knowledge into agents at runtime with minimal context overhead

This paper fills that gap.

---

## Core Concepts & Theory

### Atomic Knowledge Units (AKUs)

The core innovation is the **Atomic Knowledge Unit (AKU)**—a machine-executable knowledge artifact:

```
Atomic Knowledge Unit (AKU) = {
  specification: what to do (goal, constraints),
  procedures: step-by-step instructions,
  tool_bindings: which tools/skills to use,
  constraints: compliance rules, resource limits,
  context: preconditions, decision points,
  navigation: links to related AKUs,
  metadata: owner, version, applicable_domains
}
```

**Example AKU for Safe Deployment**:

```yaml
name: "Deploy to Production"
goal: "Safely deploy code changes with zero-downtime"

procedures:
  1. Run security scanning (invoke SecurityScan skill)
  2. Run integration tests (invoke TestSuite skill)
  3. Create canary deployment (invoke CanaryDeploy skill)
  4. Monitor error rate for 5 minutes
     - If error rate < 0.1%: proceed to full rollout
     - If error rate > 0.1%: invoke Rollback skill, notify team
  5. Verify downstream dependencies (invoke DependencyCheck skill)
  6. Update DNS/load balancer (invoke TrafficSwitch skill)

constraints:
  - Pre-deployment security scan must pass
  - Code review approval required
  - Rollback procedure must be tested in staging
  - Data migration must be reversible
  - PII access logging must be enabled

tool_bindings:
  SecurityScan: "s3://org-tools/security-scanner"
  TestSuite: "s3://org-tools/integration-tests"
  CanaryDeploy: "k8s-api://staging-cluster"
  TrafficSwitch: "dns-api://prod"

context:
  preconditions:
    - Main branch is green
    - All required approvals obtained
  decision_points:
    - Canary error rate threshold (configurable)
    - Rollback if dependency check fails
  related_AKUs:
    - "Incident Response: Production Outage"
    - "Rollback Procedures"
    - "Compliance Audit: Deployment Logs"
```

### Knowledge Activation Framework: Three Stages

The paper defines a formal pipeline for transforming latent knowledge into agent-executable form:

```
┌──────────────────────────────────────────────────────────────┐
│ KNOWLEDGE ACTIVATION PIPELINE                                │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  INPUT: Institutional Knowledge (scattered, unstructured)    │
│  ↓                                                             │
│                                                                │
│  ╔════════════════════════════════════════════════════════╗  │
│  ║ STAGE 1: CODIFICATION                                  ║  │
│  ║                                                          ║  │
│  ║ Transform domain knowledge into structured form         ║  │
│  ║ Input: Design docs, runbooks, code comments,           ║  │
│  ║         tribal knowledge (interviews)                  ║  │
│  ║ Output: Specification documents with clear goals,      ║  │
│  ║         procedures, constraints, decision trees        ║  │
│  ║                                                          ║  │
│  ║ Question Answered: "What should agents do and why?"    ║  │
│  ╚════════════════════════════════════════════════════════╝  │
│  ↓                                                             │
│                                                                │
│  ╔════════════════════════════════════════════════════════╗  │
│  ║ STAGE 2: COMPRESSION                                   ║  │
│  ║                                                          ║  │
│  ║ Reduce knowledge to respect token budgets and          ║  │
│  ║ attention decay in LLM context windows                  ║  │
│  ║                                                          ║  │
│  ║ Techniques:                                             ║  │
│  ║ - Summarize: keep essential facts, remove verbosity    ║  │
│  ║ - Index: create retrieval keys for efficient access    ║  │
│  ║ - Prune: remove rarely-used decision branches          ║  │
│  ║ - Abstract: replace verbose examples with patterns     ║  │
│  ║                                                          ║  │
│  ║ Constraint: |AKU| < context_window/10 (leave room      ║  │
│  ║ for agent reasoning and tool outputs)                  ║  │
│  ║                                                          ║  │
│  ║ Question Answered: "How do we express this compactly?" ║  │
│  ╚════════════════════════════════════════════════════════╝  │
│  ↓                                                             │
│                                                                │
│  ╔════════════════════════════════════════════════════════╗  │
│  ║ STAGE 3: INJECTION                                     ║  │
│  ║                                                          ║  │
│  ║ Integrate AKUs into agent reasoning at runtime          ║  │
│  ║ without exploding token usage                           ║  │
│  ║                                                          ║  │
│  ║ Strategies:                                             ║  │
│  ║ - Dynamic Retrieval: query relevant AKU only when      ║  │
│  ║   agent needs guidance                                  ║  │
│  ║ - Layered Disclosure: start with summary, expose       ║  │
│  ║   details on-demand                                     ║  │
│  ║ - Prompt Injection: embed AKU context in system        ║  │
│  ║   prompt at startup                                     ║  │
│  ║ - Skill Binding: translate AKU procedures into         ║  │
│  ║   callable skills                                       ║  │
│  ║                                                          ║  │
│  ║ Question Answered: "How do we make this accessible?"   ║  │
│  ╚════════════════════════════════════════════════════════╝  │
│  ↓                                                             │
│                                                                │
│  OUTPUT: Agents with knowledge-grounded decision-making     │
│
└──────────────────────────────────────────────────────────────┘
```

### Knowledge Graph Architecture

AKUs are not isolated artifacts. Instead, they form a **composable knowledge graph**:

```
                  ┌─────────────────────────┐
                  │ Deploy to Production     │
                  │ (primary AKU)           │
                  └────────┬────────────────┘
                           │
                ┌──────────┼──────────┐
                │          │          │
                ▼          ▼          ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Security │ │Canary    │ │Rollback  │
        │ Scanning │ │Deployment│ │Procedures│
        └──────────┘ └──────────┘ └──────────┘
             │            │            │
             ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Compliance  │ Monitoring  │ Incident  │
        │ Policies  │ Procedures  │ Response  │
        └──────────┘ └──────────┘ └──────────┘
```

**Key Property**: Agents navigate this graph at runtime, pulling in related AKUs as they encounter decision points. This enables **progressive disclosure**: show the summary, then reveal details only when needed.

### Formal Definition: Context Window Economy

The paper formalizes knowledge activation as an optimization problem:

```
Maximize: Σ(information_density(AKU_i) × utility(AKU_i))

Subject to:
  - Σ(tokens(AKU_i)) ≤ context_budget  [token constraint]
  - retrieval_latency(AKU_i) ≤ latency_budget  [latency constraint]
  - Σ(cost(AKU_i)) ≤ cost_budget  [cost constraint]

Where:
  - information_density = essential_facts / token_count
  - utility = probability_of_use × impact_on_decision
  - context_budget = 0.1 × context_window_size (leave room for reasoning)
```

This formalization helps organizations decide:
- Which AKUs to include in the prompt vs. retrieve dynamically
- What level of detail to encode in each AKU
- When to decompose large AKUs into smaller ones

---

## Main Ideas & Contributions

### 1. Institutional Knowledge as a First-Class Problem

**Key Insight**: Treating knowledge as an afterthought (e.g., RAG over PDFs) doesn't scale. Organizations need to:
- Codify knowledge explicitly (make implicit assumptions explicit)
- Maintain knowledge rigorously (version, audit, update)
- Compose knowledge for specific agent tasks (not just retrieve all matching documents)

### 2. AKUs as Actionable Artifacts

Unlike documents (which require interpretation) or simple prompts (which lack structure), AKUs are:
- **Executable**: Specify exactly what agents should do (not just educate them)
- **Composable**: Agents chain AKUs to solve complex tasks
- **Auditable**: Each AKU decision is logged with source (which AKU guided the decision)
- **Versionable**: Teams track evolution of knowledge over time

### 3. Knowledge Graph Navigation

Rather than flooding agents with all knowledge upfront, let agents **navigate** the knowledge graph:
- Start with high-level summaries
- Agents ask questions or encounter decision points
- System retrieves relevant child AKUs in context
- Dramatically reduces token usage vs. flat RAG

### 4. Context Window Economy

**Novel Framework**: Formalizing knowledge injection as a resource allocation problem. This enables:
- Predictable token budgets (knowledge + reasoning + tool outputs fits in context)
- Trade-off analysis (more detail for critical AKUs, summaries for others)
- Cost optimization (avoid expensive LLM calls by embedding low-cost knowledge)

---

## Methodology & Implementation

### Knowledge Codification Process

The paper proposes a structured process for organizations to codify institutional knowledge:

**Stage 1: Inventory & Analysis**
1. Identify critical knowledge domains (deployment, security, compliance, etc.)
2. Gather existing documentation, interview domain experts
3. Extract decision trees and procedures from actual systems
4. Identify gaps and contradictions

**Stage 2: Specification**
1. Write specifications in structured format (templates, decision trees)
2. Include pre-conditions, procedures, constraints, related knowledge
3. Define retrieval metadata (tags, applicability rules)
4. Review with domain experts for accuracy and completeness

**Stage 3: Compression & Optimization**
1. Measure information density (facts per token)
2. Identify opportunities to compress (summarize verbose sections, remove examples, abstract patterns)
3. Test with agents: does compressed AKU lead to correct decisions?
4. Iterate until token budget met without losing essential information

**Stage 4: Integration & Validation**
1. Deploy AKUs to agent runtime
2. Monitor: do agents use AKUs as intended?
3. Collect feedback: did agents make decisions consistent with AKU guidance?
4. Update AKUs based on feedback

### Case Study: Software Deployment

The paper includes a detailed case study of codifying deployment knowledge:

**Before Knowledge Activation**:
- Deployment procedures scattered across 47 wiki pages, 12 runbooks, countless Slack conversations
- Agents hallucinate deployment steps; miss compliance checks
- Human review required before every deployment
- Deployment mistakes lead to incidents once per month

**After Knowledge Activation**:
- Single AKU hierarchy for "Safe Production Deployment" with 7 decision points
- Related AKUs for "Incident Response", "Rollback", "Compliance Audit"
- Agents follow AKU guidance; decisions are auditable
- Deployment success rate improves (estimated based on pilot)

**Metrics** (from pilot program, not full validation):
- Deployment time: 45 min → 15 min (3x faster)
- Human review time: 30 min → 5 min (6x faster)
- Compliance violations: 1/month → 0 (in 3-month pilot)
- Incident rate: ~1/month → 0 (in 3-month pilot)

**Note**: Full paper contains more detailed results; [Exact figures unavailable — see full paper] for production-scale validation.

---

## Practical Applications & Use Cases

### 1. Agentic Software Development Lifecycle

**Use Case: Autonomous Code Review and Refactoring**

AKU hierarchy:
```
Code Review Standards (top-level AKU)
├─ Readability Guidelines
├─ Performance Criteria
├─ Security Checklist
│  ├─ Input Validation
│  ├─ Authentication Handling
│  └─ Data Privacy
└─ Testing Requirements
   ├─ Unit Test Coverage (>80%)
   ├─ Integration Tests
   └─ E2E Tests for Changed Features
```

Agent uses this AKU graph:
1. Agent reviews code changes
2. For each change, queries relevant sub-AKU (e.g., "Security Checklist")
3. Verifies that code meets AKU criteria
4. Documents findings with source AKU reference
5. If violations found, suggests fixes per AKU guidance

**Benefit**: Code review is consistent with organizational standards; decisions are fully auditable.

### 2. Multi-Stage Deployment & Incident Response

**Use Case: Autonomous Incident Triage and Resolution**

AKU hierarchy:
```
Production Incident Response (top-level)
├─ Incident Triage
│  ├─ Severity Assessment
│  ├─ Impact Analysis
│  └─ Communication Plan
├─ Investigation & Root Cause
│  ├─ Log Analysis Procedures
│  ├─ Metrics Query Procedures
│  └─ Database Query Safe Practices
└─ Remediation
   ├─ Feature Rollback Procedures
   ├─ Data Consistency Restoration
   └─ Post-Incident Review
```

Agent workflow:
1. Incident alert received
2. Agent retrieves "Incident Triage" AKU
3. Runs assessment procedures (query metrics, analyze logs)
4. Determines severity; follows appropriate sub-AKU
5. Executes remediation with full governance (audit logs, approval gates)

**Benefit**: Incidents are handled consistently; post-incident reviews are automated.

### 3. Enterprise Compliance & Governance

**Use Case: Autonomous Compliance Verification**

AKU hierarchy:
```
Data Privacy Compliance (e.g., GDPR)
├─ PII Data Handling
│  ├─ What constitutes PII in our org
│  ├─ Where PII can be stored
│  ├─ Data retention policies
│  └─ Access control requirements
├─ Data Subject Rights
│  ├─ Right to Access Procedure
│  ├─ Right to Deletion Procedure
│  └─ Data Portability Procedure
└─ Breach Notification
   ├─ Detection & Assessment
   ├─ Internal Escalation
   └─ Regulatory Reporting
```

Agent workflow:
1. Agent generating data handling code
2. Retrieves "PII Data Handling" AKU
3. Verifies code compliance with AKU constraints
4. Suggests modifications if violations found
5. Records decision and AKU reference in audit log

**Benefit**: Compliance is automated; audit trail is automatically generated.

---

## Insights & Implications

### Advancement in Agentic Software Development

1. **Knowledge-Grounded Reasoning**: Agents can make decisions that respect organizational constraints without extensive fine-tuning
2. **Onboarding Acceleration**: New developers and agents access codified knowledge immediately (vs. weeks of learning)
3. **Scaling Without Specialization**: Organizations can deploy agents to new domains by codifying domain-specific knowledge into AKUs

### Impact on Enterprise AI Adoption

- **Governance Enabled**: Knowledge activation patterns align with enterprise governance requirements (auditability, compliance, version control)
- **Risk Reduction**: Agents follow established procedures; incidents due to agent decisions are dramatically reduced
- **Knowledge Preservation**: Organizational knowledge is explicitly captured; retiring experts doesn't mean losing knowledge

### Limitations & Open Questions

1. **Codification Effort**: How much manual effort is required to codify institutional knowledge? Can this be automated?
2. **Knowledge Drift**: How do we detect when AKUs become outdated as organizational practices evolve?
3. **Cross-Organizational Knowledge**: How can organizations share AKUs while respecting confidentiality and competitive differences?
4. **Handling Uncertainty**: How do AKUs express conditional knowledge (e.g., "this procedure only applies if X, Y, or Z")?
5. **Multi-Language Support**: How do AKUs integrate with multilingual development environments?

### Relevance to Skill Frameworks

This work complements the SoK on Agentic Skills by answering: "Where does the knowledge to guide skills come from?" Skills are the execution mechanism; AKUs are the knowledge source.

---

## Code & Resources

### Official Resources

- **ArXiv Paper**: [Knowledge Activation: AI Skills as the Institutional Knowledge Primitive for Agentic Software Development](https://arxiv.org/abs/2603.14805)
- **Paper PDF**: [https://arxiv.org/pdf/2603.14805](https://arxiv.org/pdf/2603.14805)
- **HTML Version**: [https://arxiv.org/html/2603.14805](https://arxiv.org/html/2603.14805)

### Related Tools & Frameworks

- **LangChain RAG**: [Retrieval-augmented generation](https://python.langchain.com/docs/use_cases/question_answering/) (foundation for knowledge retrieval)
- **LangGraph**: [Graph-based workflows](https://langchain-ai.github.io/langgraph/) (can structure knowledge as graphs)
- **Vector Databases**: Weaviate, Pinecone, Chroma (store and retrieve AKU embeddings)
- **Documentation Tools**: Confluence, GitBook, Notion (store AKU specifications)

### Recommended Tools for AKU Implementation

```yaml
Codification:
  - Confluence/GitBook: Write AKU specifications
  - GitHub Issues: Track knowledge gaps and updates

Compression:
  - Tokenizer APIs: Measure tokens in AKU candidates
  - Text summarization: Identify verbose sections

Injection:
  - LangChain: Templates for injecting AKUs into prompts
  - Redis/DynamoDB: Caching layer for frequently-accessed AKUs
  - OpenAI Assistants: Knowledge files for semantic search
```

---

## Related Work & Context

### Foundational Work

1. **Retrieval-Augmented Generation (RAG)**
   - [Lewis et al., 2020](https://arxiv.org/abs/2005.11401): Retrieving documents for generation
   - This work extends RAG to actionable, structured knowledge

2. **Knowledge Graphs in AI Systems**
   - [Hogan et al., 2021](https://arxiv.org/abs/1808.07304): Comprehensive survey
   - This work applies knowledge graphs specifically to agent guidance

3. **Agent Prompting & In-Context Learning**
   - [Wei et al., 2022](https://arxiv.org/abs/2201.11903): Chain-of-thought prompting
   - [Brown et al., 2020](https://arxiv.org/abs/2005.14165): In-context learning in GPT-3
   - This work formalizes in-context knowledge delivery

### Related Recent Work

- **[Harnessing Agent Skills: Architectural Patterns](https://arxiv.org/abs/2606.20631)** - Complementary work on skill execution
- **[SoK: Agentic Skills](https://arxiv.org/abs/2602.20867)** - Systematization of skill design patterns
- **[AIP: A Graph Representation for Learning and Governing Agent Skills](https://arxiv.org/abs/2606.04781)** - Graph-based skill governance
- **[Is Progressive Disclosure All You Need for Long-Context Agents?](https://arxiv.org/abs/2607.17598)** - Progressive AKU revelation strategies

### Future Research Directions

1. **Automated AKU Extraction**: Extract AKUs from existing codebases and documentation
2. **AKU Composition Verification**: Formally verify that composed AKUs produce correct behavior
3. **Multi-Agent AKU Reasoning**: How do multiple agents navigate the same knowledge graph?
4. **Federated Knowledge Graphs**: Share AKUs across organizations while respecting privacy
5. **Self-Updating AKUs**: AKUs that evolve based on agent feedback and execution outcomes

---

## Summary

**Knowledge Activation** formalizes how enterprises can transform institutional knowledge into machine-executable form suitable for AI-driven development. By introducing Atomic Knowledge Units and a systematic three-stage pipeline (codification, compression, injection), this work enables organizations to:

1. Capture organizational wisdom explicitly (reducing loss when experts leave)
2. Scale agent deployment across new domains (by codifying domain knowledge)
3. Ensure compliance and governance (by grounding agent decisions in organizational policy)
4. Reduce human review overhead (by automating knowledge-guided decision-making)

For teams deploying agentic AI coding assistants, this paper provides both the conceptual framework and practical methodologies needed to move from prototype to production, where agents operate with full organizational context and make decisions that respect institutional constraints.
