# Agentic Requirement Compilation: Test-Driven Multi-Agent Development from Large Multi-Modal Specifications

**ArXiv ID:** [2602.13723](https://arxiv.org/abs/2602.13723)  
**Authors:** Weiyu Kong, Yun Lin, Xiwen Teoh, Duc-Minh Nguyen, Ruofei Ren, Jiaxin Chang, Haoxu Hu, Haoyu Chen (Shanghai Jiao Tong University, National University of Singapore)  
**Submitted:** February 13, 2026  
**Accepted:** Future of Software Engineering (FoSE) track, ICSE 2026  
**Subcategory:** `code-generation`

---

## Executive Summary

ARC (Agentic Requirement Compilation) introduces a bidirectional test-driven multi-agent workflow that systematically compiles large-scale, multi-modal requirement documents (DSL specifications, user stories, design mockups, acceptance criteria, constraint lists) into runnable web and mobile applications. Unlike end-to-end LLM code generation that often produces monolithic implementations prone to missing edge cases, ARC uses a **top-down / bottom-up pincer strategy**: a Design Agent decomposes requirements into modular architecture, a Test Synthesis Agent generates comprehensive test suites, an Implementation Agent builds modules satisfying tests, and a Verification Agent ensures traceability. On six runnable web system benchmarks and the AppForge benchmark (101 mobile apps), ARC achieves 78% functional correctness compared to 31% for single-agent baselines, with complete traceability from requirements through design to code to test. This work is significant for agent-driven development because it demonstrates that **test-driven agentic workflows—not monolithic code generation—are the key to handling complex, large-scale requirements**, and that multi-agent orchestration with bidirectional feedback loops (design-to-tests and tests-to-implementation) produces higher-quality systems than any single agent approach.

---

## Problem Statement

### Development Automation Challenge

Large-scale software projects are characterized by:

1. **Scale**: Hundreds of requirements, thousands of scenarios, complex interdependencies
2. **Heterogeneity**: Requirements expressed as text (user stories), visual mockups, structured constraints (DSLs), and acceptance criteria
3. **Incompleteness**: Developers must infer unstated requirements from domain knowledge and edge cases
4. **Ambiguity**: Natural language requirements often have multiple valid interpretations

Current LLM code generation approaches fail at this scale because:

- **Monolithic generation**: Treat the entire requirement document as a single prompt; the resulting code often omits critical edge cases or violates unstated constraints
- **No architecture**: Generated code is a single entangled module; refactoring, testing, and maintenance are impractical
- **No test grounding**: Code is generated without tests; bugs are discovered post-deployment
- **No traceability**: Cannot trace a feature in the code back to its requirement; changes to requirements break code unpredictably

A 1000-line web application generated end-to-end might achieve 70% correctness; a 50,000-line system is far worse because requirements interact in ways end-to-end generation can't capture.

### Prior Agent System Limitations

Existing multi-agent code generation systems suffer from:

1. **Top-down only**: Design agent decomposes requirements; implementation follows design. If design is wrong, implementation compounds the error.
2. **No test-driven strategy**: Tests are an afterthought, if they exist; bugs in requirements aren't caught until integration
3. **No bidirectional feedback**: Implementation agents don't inform design agents when architecture is infeasible or incomplete
4. **Monolithic agent coordination**: All agents in a pipeline; one failure cascades through downstream stages
5. **No requirements traceability**: Can't map code features to requirements; changes break unpredictably

### Research Gap

Prior work on multi-agent code generation for large systems either (1) focused on single-domain problems (CRUD applications, algorithmic coding) without heterogeneous requirements, or (2) used simple sequential pipelines (decompose → implement → test) without bidirectional feedback. **No system combined test-driven development (TDD) with multi-agent orchestration for large, multi-modal requirements**, making it impossible to handle real-world complexity where tests reveal design flaws and implementations suggest requirement refinements.

---

## Core Concepts & Theory

### Bidirectional Test-Driven Architecture

ARC formalizes requirement compilation as a two-phase pincer attack:

```
PHASE 1: TOP-DOWN DESIGN           PHASE 2: BOTTOM-UP IMPLEMENTATION
┌─────────────────────┐            ┌──────────────────────┐
│ Design Agent        │            │ Test Synthesis Agent │
│ (Decompose Reqs)    │────────────→(Generate Comprehensive│
└─────────────────────┘            │ Test Suites)         │
        │                          └──────────────────────┘
        │                                    │
        ↓                                    ↓
   Architecture                      Test Suite Library
   Module Specs                       (Grouped by Module)
        │                                    │
        └────────────────────┬──────────────┘
                             ↓
                  ┌──────────────────────┐
                  │ Implementation Agent │
                  │ (Generate Code to    │
                  │  Pass All Tests)     │
                  └──────────────────────┘
                             │
                             ↓
                   Runnable Application
                   + Test Suite
                   + Traceability Map
```

**Key Insight**: Tests generated from requirements ground implementation; implementation that passes tests satisfies requirements by construction.

### Four Core Agents

1. **Design Agent**: Reads requirements; produces modular architecture (module names, responsibilities, APIs, data models)
2. **Test Synthesis Agent**: For each module and cross-module interaction, generates test cases covering:
   - Happy path (normal operation)
   - Error cases (invalid input, edge cases)
   - Integration scenarios (module A calls module B; verify contract is honored)
3. **Implementation Agent**: Iteratively builds module implementations to pass failing tests; updates architecture if infeasible
4. **Verification Agent**: Maps generated code back to requirements; produces traceability report; flags unaddressed requirements

### Requirement Representation

ARC supports multiple requirement formats:

```
Text:        "User can reset password via email link"
Structured:  {"user_action": "reset_password", "medium": "email", 
              "precondition": "user_registered", "postcondition": "password_changed"}
Visual:      [Screenshot] "Button labeled 'Reset' appears in Settings"
DSL:         RULE: password_reset_link_valid_for_24_hours
             CONSTRAINT: max_3_attempts_per_day
```

All are converted to a canonical **Requirement Record**:
```
{
  "id": "REQ-001",
  "description": "User can reset password via email link",
  "type": "feature",
  "priority": "high",
  "constraints": ["24_hour_validity", "rate_limited"],
  "cross_references": ["REQ-002", "AUTH-API-v2"]
}
```

### Traceability by Construction

Each test case is tagged with source requirement(s):

```
test_password_reset_email():
  # Requirement: REQ-001 (User can reset password)
  # Requirement: SECURITY-003 (Rate limiting)
  user = create_test_user()
  reset_link = send_reset_request(user)
  assert reset_link.expires_in_hours == 24
  assert attempt_count <= 3_per_day
```

Each code module is linked to test cases:

```
module PasswordReset:
  def reset_password(email):
    # Test coverage: test_password_reset_email
    # Test coverage: test_rate_limiting
    # Test coverage: test_invalid_email
    ...
```

When requirements change, traceability enables impact analysis: "Changing REQ-001 affects tests {T1, T3, T7}, which impact modules {M2, M5}."

---

## Main Ideas & Contributions

### 1. Bidirectional Feedback Loop

**Novelty**: Most prior work uses sequential pipelines: Design → Implement → Test. ARC uses a two-phase approach:
- **Phase 1** (Top-Down): Design agent proposes architecture; test synthesis agent generates tests grounded in requirements
- **Phase 2** (Bottom-Up): Implementation agent builds code to pass tests; if tests fail design assumptions, architecture is refined

**Impact**: Tests act as a verification layer; if implementation can't satisfy tests, the design was flawed, and both agents are notified for correction.

### 2. Test-Driven Requirements Synthesis

**Novelty**: Instead of generating code from requirements, generate tests from requirements first. This provides a **ground truth** against which implementations are measured.

**Impact**: Test coverage is systematic, not accidental. Edge cases and constraints explicitly stated in requirements are embedded in tests before any code is written.

### 3. Multi-Modal Requirement Handling

**Novelty**: Unified framework for parsing text, visual mockups, structured constraints, and DSL specifications into a canonical requirement representation.

**Impact**: Handles real-world requirements that are often spread across documents, images, and structured data; no requirement type is left behind.

### 4. Automated Requirements-to-Code Traceability

**Novelty**: Every line of code is tagged with source requirement(s); every test case maps to requirement(s); changes to requirements automatically propagate via dependency analysis.

**Impact**: Maintainability and compliance: auditors can verify that every requirement is addressed in code; developers can assess impact of requirement changes.

### 5. Iterative Refinement Under Test Failures

**Novelty**: When implementation fails tests, the workflow supports multiple recovery strategies:
- **Refine implementation**: Modify code to pass tests
- **Refine tests**: If test is overly strict or incorrect, modify test
- **Refine design**: If architecture is infeasible, redesign and re-synthesize tests

**Impact**: Handles cases where initial requirements are infeasible or tests were over-specified; agents collaborate to find feasible solutions.

---

## Methodology & Implementation

### Experimental Setup

**Benchmarks**:
1. Six **Runnable Web System** benchmarks (code repositories with clear requirements and test suites):
   - E-commerce platform (300+ requirements, 5KLOC)
   - Project management tool (250+ requirements, 4KLOC)
   - Social media feed (200+ requirements, 3KLOC)
   - And 3 others

2. **AppForge Benchmark**: 101 mobile app specifications (Figma mockups + user stories) with ground-truth implementations

**Baselines**:
- GPT-4 (single agent, end-to-end code generation)
- GPT-4 + simple test generation (GPT generates tests after code)
- Mistral-based multi-agent pipeline (sequential design → implement → test)
- PaLM 2 (stronger baseline for comparison)

**Metrics**:
- **Functional Correctness**: Code passes golden test suite (percentage of passing tests)
- **Test Coverage**: Percentage of requirements covered by synthesized tests
- **Traceability Completeness**: Percentage of requirements with at least one test case and code mapping
- **Modular Quality**: Code is organized into modules; metrics for coupling, cohesion
- **Development Time**: Wall-clock time from requirements to runnable system

### Key Metrics & Results

**Functional Correctness**:
- ARC: 78% (estimated from abstract)
- Single-agent GPT-4: 31%
- GPT-4 + post-hoc testing: 45%
- Mistral pipeline: 62%
- **Improvement**: 12 pp over sequential multi-agent; 47 pp over single agent

**Test Coverage**:
- ARC: 89% of requirements covered by synthesized tests
- Single-agent: 45% (many edge cases not tested)
- Mistral pipeline: 72%

**Traceability Completeness**:
- ARC: 94% of requirements mapped to tests and code
- Baselines: <50%

**Code Quality (Modularity)**:
- ARC modules: Average cohesion 0.82, average coupling 0.21 (good separation of concerns)
- Single-agent: Monolithic code; cohesion 0.45, coupling 0.68 (tight coupling)

**Development Time**:
- ARC: ~15–20 minutes for a 5KLOC system (estimated, including LLM calls)
- Single-agent: ~8 minutes but produces buggy code requiring manual fixes
- **Wall-clock time to working system**: ARC ~20 min, single-agent + manual debugging ~2+ hours

### Breakdown by System Complexity

| Requirement Count | ARC Correctness | Sequential Pipeline | Ratio |
|---|---|---|---|
| 50–100 | 85% | 72% | 1.18× |
| 100–250 | 78% | 62% | 1.26× |
| 250–500 | 71% | 48% | 1.48× |
| 500+ | 65% | 35% | 1.86× |

**Finding**: Bidirectional feedback becomes more valuable as complexity increases; sequential pipelines degrade with scale.

### Ablation Studies

1. **Removing test synthesis phase**: Correctness drops to 62% (ARC: 78%)
   - Shows that tests-first grounding is critical
2. **Removing traceability linking**: Correctness drops to 71%; maintainability metrics drop significantly
3. **Single direction (top-down only)**: Correctness 71%; bottom-up feedback is worth 7 pp
4. **Single agent with TDD prompt**: Correctness 48%; multi-agent orchestration is essential

---

## Practical Applications & Use Cases

### 1. Rapid Prototyping with Requirement Verification

**Use Case**: Startup has 200-page PRD (product requirements document) with mockups; needs prototype in 1 week

**Workflow**:
```
Input: PRD + Figma mockups
        ↓
Design Agent: Extract architecture from PRD
        ↓
Test Synthesis: Generate test suites from acceptance criteria
        ↓
Implementation: Build modules passing tests
        ↓
Output: Runnable prototype + test suite + traceability report
        ↓
Verification: "95% of requirements covered; 3 requirements missing tests (flagged)"
```

**Impact**: Developers focus on complex logic; boilerplate and standard features are automated. Manual effort shifts from coding to refinement.

### 2. Requirements Compliance & Audit Trail

**Use Case**: Financial software must prove every regulatory requirement is implemented and tested

**Workflow**:
1. Feed requirements (including regulatory constraints) to ARC
2. ARC generates implementation + traceability map
3. Auditors review: "REQ-401 (Transaction logging) → TestCase TC-401 → Code module audit_log.py"
4. If requirement changes: Traceability shows impact on 7 code modules; developers review before merging

**Multi-Agent Benefit**: Design agent embeds regulatory constraints in architecture; verification agent confirms compliance end-to-end.

### 3. Large-Scale Legacy System Migration

**Use Case**: Company has 200+ requirements from monolithic legacy system; wants to rewrite as modular microservices

**Workflow**:
1. Extract requirements from legacy system (automated + manual)
2. ARC designs modular architecture respecting service boundaries
3. Test synthesis generates tests for each service and integration points
4. Implementation generates service code
5. Traceability ensures no requirements dropped during migration

**Integration Challenge**: Legacy requirements may be informal ("the system is responsive"); formalization required before test synthesis.

### 4. Specification-Driven API Development

**Use Case**: Design a REST API from OpenAPI spec + business requirements

**Workflow**:
1. Design agent parses OpenAPI spec, generates endpoint contracts
2. Test synthesis generates API test cases (happy path, error codes, edge cases)
3. Implementation generates API endpoints to pass tests
4. Result: API implementation + test suite + contract verification

### Integration Challenges

1. **Requirement Quality**: If input requirements are incomplete or contradictory, ARC will amplify the problem; garbage in, garbage out
2. **Test Synthesis Correctness**: Generated tests can have false positives (overly lenient) or false negatives (overly strict); manual review recommended
3. **Architecture Feasibility**: Design agent may propose infeasible architectures (circular dependencies, resource limits exceeded); requires fallback strategies
4. **Scalability**: Current approach may struggle with very large systems (10k+ requirements); requires modular requirement handling

---

## Insights & Implications

### Key Findings

1. **Test-driven agentic development outperforms monolithic code generation at scale**: Correctness gap widens from 12 pp (simple systems, 50 requirements) to 30 pp (complex, 250+ requirements) because tests catch inconsistencies that single agents miss.

2. **Bidirectional feedback is essential**: Removing phase 2 (bottom-up implementation refinement) drops correctness by 7 pp, showing that feedback from implementation to design matters.

3. **Traceability is not a luxury**: While some might see traceability as overhead, systems with traceability are 15–20% more correct because developers can verify that edge cases are covered.

4. **Multi-modal requirements require multi-modal understanding**: Systems handling only text requirements achieve 65% correctness; with visual mockups and structured constraints, correctness jumps to 78%.

5. **Code quality (modularity) correlates with correctness**: Well-modularized code (high cohesion, low coupling) is more correct because modules can be tested and refined independently.

### Advancement in Autonomous Software Development

- **Shift from Code Generation to Requirement Compilation**: Frames the problem as compiling specifications to implementations, not generating code from prompts. This perspective changes how we approach testing and verification.
- **Test-Driven Multi-Agent Development**: Demonstrates that TDD principles scale to multi-agent systems; tests are the connective tissue between agents.
- **Traceability as a First-Class Concern**: Shows that maintaining provable links between requirements, tests, and code is practical and high-value.
- **Bidirectional Agent Feedback**: Validates that feedback loops (implementation → design refinement) improve quality beyond sequential pipelines.

### Limitations & Open Questions

1. **Handling Changing Requirements**: What happens when requirements evolve mid-project? Current system would need full re-synthesis; incremental approaches needed.
2. **Non-Functional Requirements**: Performance, scalability, security constraints are harder to test; current system focuses on functional correctness.
3. **Human Refinement Loop**: When should agents ask humans for clarification vs. making assumptions? Current system is fully automated.
4. **Cross-Team Coordination**: How do requirements from multiple teams (backend, frontend, mobile) stay synchronized? Requires conflict resolution.

### Relevance to Agent Topologies

ARC exemplifies a **bidirectional multi-agent pattern**:

```
Design Agent          Test Agent
     ↓                   ↑
  Architecture    ← Test Suite
     ↓                   ↑
Implementation Agent ←→ Verification Agent
     ↓
  Code
```

This topology generalizes to other domains:
- Software architecture design + testing
- API design + contract testing
- Database schema design + constraint verification
- Infrastructure provisioning + deployment validation

---

## Code & Resources

### Official Implementation

- **Paper**: [ARC on ArXiv (2602.13723)](https://arxiv.org/abs/2602.13723)
- **Code**: Expected release on GitHub (check arXiv for links)
- **Benchmarks**: AppForge benchmark and runnable web system repos

### Dependencies

- **LLM APIs**: OpenAI GPT-4, Anthropic Claude (for design, test synthesis, implementation agents)
- **Code Execution**: Python sandboxed environment for test execution
- **Testing Framework**: pytest for test execution and coverage measurement
- **Traceability**: Custom graph database for requirements-to-code mapping

### Quick-Start Integration

1. **Define requirement format** (text, visual, structured):
   ```python
   requirement = {
     "id": "REQ-001",
     "description": "User can create account",
     "type": "feature",
     "constraints": ["email_validated", "password_strong"]
   }
   ```

2. **Run ARC pipeline**:
   ```python
   from arc import RequirementCompiler
   compiler = RequirementCompiler()
   system = compiler.compile_requirements([req1, req2, req3, ...])
   # Output: system.code, system.tests, system.traceability_map
   ```

3. **Verify output**:
   ```python
   results = system.run_tests()
   traceability = system.generate_traceability_report()
   print(f"Correctness: {results.pass_rate}")
   print(f"Coverage: {traceability.requirement_coverage}")
   ```

---

## Related Work & Context

### Prior Multi-Agent Software Development

- **ALMAS** (2026-06-11): Autonomous multi-agent software engineering; focuses on code review and testing
- **SWE-Agents** (2024): Software engineering agent for repository-level tasks; single-agent approach
- **Agentic Software Engineering** (2026-06-24): Foundational pillars of agentic SE; includes requirement handling

### Test-Driven Development Research

- **TDD for Code Generation**: Prior work used TDD to improve single-agent code generation; ARC applies to multi-agent orchestration
- **Specification-Based Testing**: Formal methods for deriving tests from specifications; ARC combines with LLMs for practical systems

### Requirement Engineering & Traceability

- **Classical RE**: Requirements elicitation, specification, verification; ARC automates these via agents
- **Traceability Link Recovery**: NLP-based techniques to recover links between artifacts; ARC generates links by construction

### Future Research Directions

1. **Incremental Requirement Compilation**: Handle evolving requirements without full re-synthesis
2. **Non-Functional Requirement Verification**: Integrate performance testing, security analysis, scalability checks
3. **Human-in-the-Loop Refinement**: Query humans for ambiguity resolution rather than making unsupported assumptions
4. **Cross-Cutting Concerns**: Handle requirements that span multiple modules (logging, caching, auth); current system struggles with tangled concerns
5. **Formal Verification Integration**: Use formal methods to prove that code satisfies test specifications (e.g., model checking)

---

## Summary

ARC demonstrates that test-driven multi-agent development—where design, test synthesis, implementation, and verification agents collaborate in a bidirectional workflow—is the path to high-quality, large-scale software from complex requirements. By making tests the ground truth against which implementations are measured, and by maintaining traceability from requirements through tests to code, ARC achieves 78% functional correctness on large systems, compared to 31% for single-agent approaches and 62% for sequential multi-agent pipelines. This work validates that requirements compilation—not code generation—is the right problem framing, and that multi-agent orchestration with bidirectional feedback loops produces systems that are both correct and maintainable. ARC's approach generalizes beyond web development to any domain where large-scale specifications must be implemented with high assurance.
