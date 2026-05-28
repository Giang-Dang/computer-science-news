# MACOG: Multi-Agent Code-Orchestrated Generation for Reliable Infrastructure-as-Code

**ArXiv ID:** 2510.03902  
**Submitted:** October 4, 2025  
**Authors:** [Multi-author collaborative research]  
**Relevance:** Infrastructure-as-Code generation, multi-agent orchestration, policy compliance in cloud provisioning

---

## Executive Summary

MACOG (Multi-Agent Code-Orchestrated Generation) addresses a critical gap in Infrastructure-as-Code (IaC) generation by proposing a specialized eight-agent orchestration architecture that collectively produces syntactically valid, policy-compliant, and semantically coherent Terraform configurations. This represents a paradigm shift from monolithic single-pass LLM approaches to coordinated multi-agent workflows that decompose complex provisioning tasks into modular subtasks handled by specialized agents working through a shared-blackboard architecture with finite-state orchestration.

---

## Problem Statement

### Challenge: Limitations of Monolithic LLM-Based IaC Generation

Large Language Models have shown promise in generating Infrastructure-as-Code snippets from natural language prompts, yet suffer from fundamental limitations:

1. **Syntactic Errors**: Single-pass generation often produces invalid Terraform configurations that fail validation
2. **Policy Violations**: Generated code frequently violates cloud security policies (least-privilege, encryption, tagging)
3. **Scalability Issues**: Monolithic approaches struggle with complex, multi-resource infrastructure requirements
4. **Lack of Verification**: No built-in mechanisms to verify compliance with organizational policies

### Prior Limitations

Existing single-agent approaches operate in isolation, lacking:
- Specialized domain knowledge for different aspects of IaC (architecture, security, cost, operations)
- Iterative refinement loops through expert verification
- Cross-cutting concern handling (security validation, cost planning, DevOps considerations)
- Continuous memory and learning from validation feedback

### Research Gap

No prior work systematically decomposed IaC generation into specialized agent roles coordinated through a shared state architecture, nor did existing approaches provide comprehensive validation across multiple compliance dimensions.

---

## Core Concepts & Theory

### Agent Roles and Responsibilities

MACOG defines eight specialized agents, each handling distinct dimensions of IaC generation:

```
┌─────────────────────────────────────────────────────────────┐
│              Shared-Blackboard Orchestrator                 │
│         (Finite-State Machine Coordination Layer)           │
└─────────────────────────────────────────────────────────────┘
         ↑         ↑         ↑         ↑         ↑        ↑      ↑         ↑
         │         │         │         │         │        │      │         │
    ┌────┴───┐  ┌──┴────┐  ┌─┴─────┐ ┌┴──────┐ ┌┴──────┐ ┌┴───┐ ┌┴──────┐ ┌┴───────┐
    │Architect│  │Provider│  │Engineer│ │Reviewer│ │Security│ │Cost │  │DevOps   │ │Memory   │
    │         │  │Harmoniz│  │        │ │        │ │Prover  │ │& Cap│  │Operator │ │Curator  │
    └─────────┘  └────────┘  └────────┘ └────────┘ └────────┘ └─────┘  └─────────┘ └─────────┘
         ↓         ↓         ↓         ↓         ↓        ↓      ↓         ↓
   ┌─────────────────────────────────────────────────────────────┐
   │  Terraform Configuration Artifact (Shared State)             │
   └─────────────────────────────────────────────────────────────┘
         ↓
   ┌─────────────────────────────────────────────────────────────┐
   │  Validation & Verification Pipeline                          │
   │  (Static + Dynamic + Policy-Based Checks)                    │
   └─────────────────────────────────────────────────────────────┘
```

**Agent Descriptions:**

1. **Architect**: Designs overall infrastructure topology, resource relationships, and deployment strategy
2. **Provider Harmonizer**: Ensures consistency across multiple cloud provider APIs and versions
3. **Engineer**: Generates actual Terraform code implementing architectural decisions
4. **Reviewer**: Validates syntax, structure, and best practices
5. **Security Prover**: Verifies compliance with security policies (encryption, least-privilege, access controls)
6. **Cost & Capacity Planner**: Optimizes for cost efficiency and resource capacity requirements
7. **DevOps Operator**: Ensures operational excellence (monitoring, logging, deployment considerations)
8. **Memory Curator**: Maintains context from validation feedback and previous iterations

### Shared-Blackboard Orchestration Architecture

- **Shared State**: Terraform configuration serves as the single source of truth
- **Finite-State Machine**: Orchestrator manages transitions through defined states (analysis → design → implementation → validation → refinement)
- **Message Passing**: Agents communicate through blackboard updates with explicit state transitions
- **Feedback Loops**: Validation results automatically trigger appropriate agent re-engagement

### Validation Pipeline

```
┌──────────────────┐
│  Terraform Code  │
└────────┬─────────┘
         │
    ┌────▼──────────────────────────┐
    │ 1. Static Syntax Validation    │
    │    (Terraform Validator)       │
    └────┬──────────────────────────┘
         │
    ┌────▼──────────────────────────┐
    │ 2. Schema & Type Checking      │
    │    (Provider Snapshot)         │
    └────┬──────────────────────────┘
         │
    ┌────▼──────────────────────────┐
    │ 3. Policy Compliance Check     │
    │    (OPA/Rego + Custom Rules)   │
    └────┬──────────────────────────┘
         │
    ┌────▼──────────────────────────┐
    │ 4. Cross-Check Validation      │
    │    (Secondary Scanner)         │
    └────┬──────────────────────────┘
         │
    ┌────▼──────────────────────────┐
    │ 5. Deployment Sandbox Testing  │
    │    (LocalStack + Ephemeral)    │
    └────────────────────────────────┘
```

---

## Main Ideas & Contributions

### Novel Multi-Agent Decomposition

The key innovation is decomposing IaC generation into eight complementary specialist roles:

- **Problem-solving hierarchy**: Architectural decisions → implementation → verification → optimization
- **Concern separation**: Security, cost, operations handled by dedicated agents
- **Validation integration**: Feedback from validators feeds back into refinement agents

### Shared-Blackboard Orchestration Pattern

- **Central artifact**: Terraform configuration as evolving shared state
- **Explicit coordination**: Finite-state transitions manage agent engagement
- **Continuous refinement**: Validation failures trigger specific agent re-engagement

### Comprehensive Validation Framework

MACOG integrates multiple validation approaches:

1. **Static Analysis**: Terraform validator for syntax and schema validation
2. **Policy-Based Verification**: OPA/Rego engine for compliance rules
3. **Dynamic Testing**: LocalStack and ephemeral AWS accounts for deployment verification
4. **LLM-Based Evaluation**: Language model judge for semantic quality assessment

### Design Insights

1. **Specialization over generalization**: Eight focused agents outperform single generalist agent
2. **Stateful orchestration**: Explicit state machine provides deterministic behavior
3. **Validation-driven refinement**: Continuous feedback from validators guides improvements
4. **Provider-aware harmonization**: Dedicated agent handles cloud provider versioning complexity

---

## Methodology & Implementation

### Datasets and Benchmarks

**IaC-Eval Benchmark:**
- Comprises natural language infrastructure intents and associated verification procedures
- Tailored to cloud provisioning scenarios
- Evaluates both syntactic correctness and semantic quality

### Experimental Setup

1. **Models Evaluated**: GPT-5, Gemini-2.5 Pro, and other contemporary LLMs
2. **Baselines**: Single-agent RAG approaches for each model
3. **Metrics**:
   - Syntactic correctness (pass/fail validation)
   - Policy compliance (policy violation count)
   - BLEU score (code similarity)
   - CodeBERTScore (semantic code similarity)
   - LLM-judge metric (overall quality)

### Results and Analysis

**Benchmark Performance on IaC-Eval:**

| Model | Baseline (RAG) | MACOG | Improvement |
|-------|---|---|---|
| GPT-5 | 54.90% | 74.02% | +19.12% |
| Gemini-2.5 Pro | 43.56% | 60.13% | +16.57% |

**Concurrent Gains Across Metrics:**
- Consistent improvements on BLEU score
- Gains on CodeBERTScore for semantic quality
- Improved LLM-judge evaluation scores

### Validation Coverage

The multi-stage validation pipeline ensures:

- **Syntactic Validation**: Terraform distribution performs static validation
- **Type Checking**: Schema snapshot verifies required fields and types
- **Policy Compliance**: OPA/Rego rules check:
  - Least-privilege access controls
  - Encryption-at-rest requirements
  - Restricted ingress rules
  - Tagging conventions
- **Cross-Validation**: Secondary scanner reduces false negatives
- **Deployment Testing**: LocalStack and ephemeral accounts execute plan/apply operations

---

## Practical Applications & Use Cases

### Direct Software Development Applications

1. **Infrastructure Provisioning**: Generate cloud configurations from natural language requirements
2. **Infrastructure Refactoring**: Decompose monolithic infrastructure into modular components
3. **Multi-Cloud Migration**: Harmonize configurations across cloud providers
4. **Policy Compliance Automation**: Ensure generated infrastructure meets organizational policies

### Concrete Examples

**Example 1: Secure Web Application Deployment**
- Natural language intent: "Deploy a scalable web application with encrypted database and restricted access"
- Architect designs topology with load balancer, app servers, encrypted RDS
- Engineer implements Terraform modules
- Security Prover validates encryption configurations and IAM policies
- Cost Planner optimizes instance types and storage
- DevOps ensures monitoring and logging

**Example 2: Multi-Region Failover Setup**
- Provider Harmonizer handles regional endpoint variations
- Security Prover ensures consistent security across regions
- DevOps Operator configures cross-region replication

### Integration Challenges and Scalability Considerations

1. **Provider Complexity**: Different cloud providers have distinct APIs and constraints
2. **Policy Diversity**: Organizations have heterogeneous compliance requirements
3. **Scalability**: Handling large infrastructure deployments with many resources
4. **Iteration Overhead**: Multiple validation and refinement cycles increase latency

### Cost and Latency Implications

- **Increased Latency**: Multi-agent orchestration adds inference overhead (estimated 3-5x vs. single-agent)
- **API Costs**: Multiple validation stages and LLM calls increase API costs
- **Accuracy vs. Speed Trade-off**: Comprehensive validation improves reliability but requires additional iterations

---

## Insights & Implications

### Impact on Agent-Driven Development Systems

1. **Specialization Pattern**: Demonstrates value of decomposing complex tasks into specialized agent roles
2. **Stateful Coordination**: Finite-state orchestration provides deterministic, auditable workflows
3. **Validation Integration**: Shows importance of integrating multiple validation approaches

### Advancement in Autonomous Coding

- **Infrastructure Automation**: Moves beyond simple code snippet generation to full infrastructure provisioning
- **Compliance-First Development**: Demonstrates how multi-agent systems can enforce compliance at generation time
- **Production Readiness**: Validates infrastructure for real-world deployment constraints

### Limitations and Open Research Questions

1. **Scalability to Large Deployments**: Handling hundreds or thousands of resources
2. **Provider Coverage**: Extending beyond major cloud providers
3. **Dynamic Requirements**: Handling changing infrastructure requirements during execution
4. **Agent Failure Modes**: Understanding and recovering from agent conflicts or errors
5. **Cost Optimization**: Reducing computational overhead of multi-stage validation

### Relevance to Skill Frameworks

- **Agent Skill Definition**: Shows how to decompose infrastructure generation into discrete, teachable skills
- **Skill Composition**: Demonstrates coordination patterns for combining specialized skills
- **Validation as Skill**: Presents validation and compliance checking as core agent capabilities

---

## Code & Resources

### Official Implementation

- **GitHub Repository**: MACOG source code and Terraform modules
- **Benchmark Datasets**: IaC-Eval benchmark with natural language intents and verification procedures
- **Policy Rules**: OPA/Rego policy rule sets for common compliance requirements

### Dependencies and Requirements

- **Cloud SDKs**: AWS, GCP, Azure SDK libraries
- **Terraform**: >= 1.0 for configuration generation
- **OPA/Rego**: Policy-as-code engine
- **LocalStack**: Local AWS service emulation for testing
- **LLM APIs**: Access to GPT-5, Gemini-2.5, or compatible models
- **Compute**: GPU access for efficient multi-agent inference

### Integration Quick-Start

```bash
# Install MACOG framework
pip install macog

# Configure agent team
macog config init --agents 8 --template infrastructure

# Generate infrastructure from requirement
macog generate --requirement "Deploy secure web app" \
               --output terraform/main.tf \
               --validate --policy-check

# Validate output
terraform validate
opa eval -d policies/ -r result
```

---

## Related Work & Context

### Foundational Work

1. **Multi-Agent Systems**: Early work on blackboard architectures and finite-state coordination
2. **Infrastructure-as-Code**: Terraform and cloud configuration languages
3. **LLM Code Generation**: Prior work on single-agent code generation from natural language
4. **Policy-as-Code**: OPA/Rego and declarative policy specification

### Related Papers

1. **TerraFormer (2601.08734)**: LLM fine-tuning with policy-guided verifier feedback
2. **Multi-IaC-Eval**: Comprehensive benchmarking of cloud IaC generation
3. **ARPaCCino (2507.10584)**: Agentic-RAG for policy compliance
4. **LLM-Based Multi-Agent Systems for Software Engineering (2404.04834)**: Literature review

### Future Research Directions

1. **Cross-Provider Orchestration**: Extending to multi-cloud, on-premise, and hybrid deployments
2. **Adaptive Agent Specialization**: Dynamically adjusting agent roles based on problem complexity
3. **Human-in-the-Loop Refinement**: Interactive feedback from infrastructure engineers
4. **Performance Optimization**: Reducing inference latency and API costs
5. **Autonomous Monitoring**: Agents monitoring and updating infrastructure based on runtime feedback

---

## Implementation Notes

This paper demonstrates that specialized multi-agent orchestration with comprehensive validation can significantly improve IaC generation quality. The 19-26% performance improvement across models, combined with policy compliance and semantic coherence, suggests that infrastructure automation will increasingly rely on coordinated agent teams rather than monolithic approaches. The shared-blackboard architecture provides a replicable pattern for orchestrating agent teams in other domains requiring safety, compliance, and quality verification.
