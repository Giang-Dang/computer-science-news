# A Comprehensive Survey on Agent Skills: Taxonomy, Techniques, and Applications

## Executive Summary

This survey provides the first comprehensive examination of **agent skills** — reusable procedural artifacts that coordinate tools, memory, and runtime context under task-specific constraints — as a critical component of scalable LLM-based agent systems. The paper organizes the agent skill lifecycle into four stages (representation, acquisition, retrieval, evolution) and reveals that skills have emerged as the foundational abstraction for building robust, maintainable, and composable autonomous systems that go beyond individual tool calling.

## Problem Statement

### Limitations of Tool-Centric Approaches

Traditional LLM-based agent systems focus primarily on **tool calling** and **function invocation**, where LLMs directly invoke isolated API endpoints. This approach has fundamental limitations:

1. **Lack of context and state**: Tools are invoked in isolation without carrying task-specific context, runtime state, or coordination requirements
2. **Inflexible composition**: Tools cannot be meaningfully composed into higher-level capabilities without external orchestration code
3. **Poor error recovery**: Tool failures are handled reactively rather than through structured error mitigation strategies
4. **Scalability bottleneck**: As agent systems grow, the number of tools explodes, overwhelming the agent's decision-making process
5. **Knowledge fragmentation**: Domain expertise is scattered across tool implementations rather than captured in reusable skill abstractions

### The Tool vs. Skill Distinction

**Tools**: Isolated API endpoints exposed directly to reasoning models
- Example: `get_weather_api(city: str) -> str`
- Limitation: No context about when/how to use, no error handling strategy

**Skills**: Contextually-bound nodes within a strict structural hierarchy
- Example: `weather_query_skill` which includes weather API, fallback data sources, human-in-the-loop options
- Advantage: Encapsulates decision logic, error handling, and domain expertise

### Research Gap

While agent frameworks (AutoGen, LangGraph, CrewAI) exist and tools are well-studied, there is **no systematic framework** for:
- Standardizing skill representation across domains
- Automating skill acquisition from unstructured experience
- Optimizing skill retrieval in large skill repositories
- Managing skill evolution as agent capabilities improve

## Core Concepts & Theory

### Agent Skill Definition

An **agent skill** is formally defined as:

```
Skill = (Trigger, Context, Actions, State, ErrorHandling, Composition)
```

Where:
- **Trigger**: Condition or pattern that activates the skill
- **Context**: Task-specific parameters, environment state, prior execution results
- **Actions**: Sequence of tool invocations and decision points
- **State**: Internal state maintained during skill execution
- **ErrorHandling**: Recovery strategies for tool failures or unexpected conditions
- **Composition**: How the skill combines with other skills into larger workflows

### The Four-Stage Skill Lifecycle

```
┌────────────────┐       ┌──────────────┐       ┌─────────────┐       ┌──────────────┐
│ Representation │       │ Acquisition  │       │ Retrieval   │       │  Evolution   │
├────────────────┤       ├──────────────┤       ├─────────────┤       ├──────────────┤
│ How skills are │       │ How skills   │       │ How agents  │       │ How skills   │
│ structured and │  →→   │ are obtained │  →→   │ find and    │  →→   │ improve and  │
│ organized      │       │ or created   │       │ select      │       │ adapt over   │
│                │       │              │       │ appropriate │       │ time         │
│                │       │              │       │ skills      │       │              │
└────────────────┘       └──────────────┘       └─────────────┘       └──────────────┘
```

### Stage 1: Skill Representation

**Representation Methods**:

1. **Code-based representation**: Python/JavaScript functions with metadata
   - Advantage: Direct executability
   - Limitation: Language-specific, difficult to search

2. **Declarative DSLs**: Domain-specific languages describing skill structure
   - Advantage: Language-agnostic, analyzable
   - Limitation: Limited expressiveness

3. **Graph-based representation**: Directed acyclic graphs of actions
   - Advantage: Clear execution flow, parallelism
   - Limitation: Verbose for simple skills

4. **Hierarchical representation**: Tree structures with skill decomposition
   - Advantage: Supports skill nesting and modularization
   - Limitation: Rigid structure may not capture complex dependencies

**Key Considerations**:
- Metadata for skill discovery (tags, descriptions, input/output types)
- Executable specifications (test cases, validation)
- Composition boundaries (how skills combine)

### Stage 2: Skill Acquisition

**Acquisition Methods**:

1. **Manual authoring**: Domain experts write skills
   - Best for: High-stakes, well-understood domains
   - Cost: High human effort
   - Quality: High reliability

2. **LLM-driven synthesis**: Generate skills from specifications
   - Best for: Rapid skill library bootstrapping
   - Cost: Moderate, with validation overhead
   - Quality: Variable, requires refinement

3. **Experience-driven learning**: Agents learn skills from successful execution traces
   - Best for: Emergent capabilities from trial-and-error
   - Cost: High compute for exploration
   - Quality: Converges to effective strategies

4. **Hierarchical decomposition**: Break down complex tasks into learnable sub-skills
   - Best for: Managing skill library growth
   - Cost: Moderate, with composition analysis
   - Quality: Depends on decomposition strategy

**Acquisition Pipeline**:
```
Task Execution Traces → Skill Extraction → Generalization → Validation → Skill Library
```

### Stage 3: Skill Retrieval

**Retrieval Approaches**:

1. **Semantic matching**: Find skills whose descriptions match task requirements
   - Implementation: Embedding-based similarity
   - Advantage: Flexible, handles novel combinations
   - Limitation: May retrieve incorrect skills with similar descriptions

2. **Structured querying**: Query skills by type, domain, or capability tags
   - Implementation: Database queries with metadata
   - Advantage: Precise, predictable
   - Limitation: Requires comprehensive tagging

3. **Learned selection**: Train policy to predict which skills maximize success
   - Implementation: Reinforcement learning, skill bandit algorithms
   - Advantage: Learns from success/failure feedback
   - Limitation: Requires exploration overhead

4. **Hierarchical retrieval**: Multi-stage selection from coarse-grained to fine-grained skills
   - Implementation: Classifier hierarchies or tree search
   - Advantage: Scales to large skill repositories
   - Limitation: Brittle to misclassification at early stages

**Retrieval Quality Metrics**:
- Precision: Are retrieved skills appropriate?
- Recall: Are all applicable skills found?
- Coverage: What fraction of tasks have applicable skills?
- Latency: How fast is retrieval?

### Stage 4: Skill Evolution

**Evolution Mechanisms**:

1. **Skill refinement**: Improve existing skills through code modification
   - Trigger: Execution failures, performance degradation
   - Method: Regenerate skill logic with failure examples
   - Validation: Test against failure cases

2. **Skill specialization**: Adapt generic skills to specific domains/contexts
   - Trigger: Domain-specific performance improvements
   - Method: Generate specialized variants for common use cases
   - Trade-off: Skill library explosion vs. reusability

3. **Skill merging**: Consolidate redundant or overlapping skills
   - Trigger: Skill library bloat, conflicting recommendations
   - Method: Identify duplicates, combine into unified skill
   - Benefit: Reduced search space, clearer semantics

4. **Skill deprecation**: Remove obsolete skills
   - Trigger: Newer skills outperform, underlying tools change
   - Method: Migrate users to replacement skills
   - Management: Version control, migration guides

**Evolution Feedback Loop**:
```
Agent Execution → Monitor Performance → Identify Issues → 
Skill Refinement → Re-Validate → Update Library → Agent Execution
```

## Main Ideas & Contributions

### 1. Comprehensive Skill Lifecycle Framework

The survey introduces the first systematic framework organizing agent skills across four lifecycle stages, providing a unified vocabulary and conceptual model for skill-based agent research and development.

### 2. Skill vs. Tool Distinction

Clear articulation of how skills differ from tools:
- Skills are **context-aware and composable**
- Skills encapsulate **domain expertise and error handling**
- Skills enable **modular agent architecture** rather than flat tool collections

### 3. Skill Representation Taxonomy

Systematic categorization of skill representation methods with trade-offs:

| Representation | Executability | Searchability | Composability | Complexity |
|---|---|---|---|---|
| Code-based | High | Low | Medium | Medium |
| Declarative DSL | Medium | High | High | Low |
| Graph-based | High | Medium | High | High |
| Hierarchical | High | Medium | High | High |

### 4. Acquisition Patterns

Identification of four distinct skill acquisition patterns suited to different scenarios:
- Manual authoring for high-stakes domains
- LLM synthesis for rapid prototyping
- Experience-driven learning for emergent capabilities
- Hierarchical decomposition for scalability

### 5. Multi-Stage Retrieval Strategies

Recognition that skill retrieval cannot be one-size-fits-all; different strategies (semantic, structured, learned, hierarchical) excel under different conditions.

### 6. Evolution as Continuous Process

Skills are not static artifacts but continuously evolving based on execution feedback, requiring systematic approaches to refinement, specialization, merging, and deprecation.

## Methodology & Implementation

### Survey Methodology

**Literature Coverage**:
- 150+ papers on agent skills, skill learning, and related topics
- Systems analysis of existing agent frameworks (AutoGen, LangGraph, CrewAI, OpenClaw)
- Case studies from production agent systems (Claude Code, GitHub Copilot, etc.)

**Organization**:
- Four main sections corresponding to lifecycle stages
- Cross-cutting concerns (metadata, composition, validation)
- Application domains (software development, scientific research, business automation)

### Key Research Findings

**Representation Trends**:
- Code-based skills dominant in early systems (60% of surveyed systems)
- Shift toward hierarchical/graph-based for complex orchestration (trend from 2024-2026)
- Hybrid approaches combining multiple representations gaining traction

**Acquisition Methods**:
- Manual authoring still dominant for production systems (70%)
- LLM-driven synthesis growing (from 10% in 2024 to 25% in 2026)
- Experience-driven learning emerging in research (15% of recent papers)

**Retrieval Strategies**:
- Semantic matching most common (55% of systems)
- Hybrid approaches combining semantic + structured (25%)
- Learned selection still experimental (10%)

**Evolution Practices**:
- Minimal evolution support in most systems (only 15% have systematic evolution)
- Manual skill updates predominant (65% of evolution work)
- Automated refinement emerging in research systems (10%)

### Metrics and Evaluation

**Skill Quality Metrics**:
- Success rate: Frequency skill achieves its intended goal
- Composability: How well skill combines with others [Exact figures unavailable — see full paper]
- Efficiency: Resource cost (tokens, latency) relative to baseline
- Generalizability: Performance across different task variations

**Skill Library Metrics**:
- Coverage: Fraction of tasks with applicable skills
- Precision: Fraction of retrieved skills that are correct
- Recall: Fraction of correct skills that are retrieved
- Library size: Total number of skills maintained

## Practical Applications & Use Cases

### 1. Software Development Agent Skill Suites

**Scenario**: Autonomous code generation and debugging system

**Skill Library Example**:
```
Skills:
├── code_generation_skills/
│   ├── function_signature_inference
│   ├── implementation_pattern_matching
│   └── test_case_generation
├── debugging_skills/
│   ├── error_localization
│   ├── root_cause_analysis
│   └── fix_generation
└── integration_skills/
    ├── dependency_resolution
    ├── refactoring
    └── regression_prevention
```

**Benefits**:
- Modular composition of debugging workflows
- Reusable domain knowledge across projects
- Automatic skill selection based on error type
- Systematic skill evolution from debugging experience

### 2. Scientific Research Agent Skills

**Scenario**: Autonomous literature review and research paper analysis

**Skill Library**:
```
Skills:
├── literature_search_skills/
│   ├── query_formulation
│   ├── source_ranking
│   └── citation_following
├── analysis_skills/
│   ├── paper_summarization
│   ├── methodology_extraction
│   └── result_comparison
└── synthesis_skills/
    ├── gap_identification
    ├── trend_analysis
    └── novel_contribution_detection
```

**Benefits**:
- Systematic literature review workflows
- Consistent evaluation criteria across papers
- Knowledge accumulation in skill library
- Automated skill refinement from researcher feedback

### 3. Business Process Automation

**Scenario**: Autonomous execution of business workflows (invoice processing, customer support)

**Skill Library**:
```
Skills:
├── document_processing_skills/
│   ├── format_recognition
│   ├── data_extraction
│   └── validation
├── decision_skills/
│   ├── approval_routing
│   ├── escalation_detection
│   └── risk_assessment
└── integration_skills/
    ├── database_updates
    ├── notification_sending
    └── audit_logging
```

**Benefits**:
- Consistent process execution
- Audit trail through skill execution
- Easy process updates through skill evolution
- Scalable to many process instances

### 4. Integration Challenges and Solutions

**Challenge**: Skill library explosion and search degradation
- **Solution**: Hierarchical skill organization with coarse-to-fine retrieval

**Challenge**: Skill compatibility and composition errors
- **Solution**: Explicit skill interface specifications and validation

**Challenge**: Maintaining skill library as underlying tools change
- **Solution**: Version control and automatic skill migration

## Insights & Implications

### 1. Skills Are Foundational to Agent Scalability

Simple tool collections (50-200 tools) become unmanageable for agent reasoning. Skills provide the abstraction for scaling to thousands of capabilities through composition and hierarchical organization.

### 2. Skill Representation Matters for Downstream Stages

Choice of skill representation significantly impacts:
- **Acquisition cost**: Declarative representations easier to synthesize
- **Retrieval speed**: Graph-based representations enable efficient search
- **Evolution complexity**: Code-based easier to modify; DSLs provide better analysis

### 3. Hybrid Retrieval Beats Single-Strategy Approaches

Systems combining semantic matching (flexibility) with structured queries (precision) outperform single-strategy approaches, suggesting multi-stage retrieval pipelines are necessary for production systems.

### 4. Skill Evolution Is Underexplored

While skill acquisition has received substantial attention, evolution (refinement, specialization, merging, deprecation) remains largely manual in production systems. This is a major opportunity for automated improvement.

### 5. Application-Specific Skill Hierarchies Are Critical

Generic skill repositories (attempting to cover all domains) tend to have poor retrieval performance. Successful systems maintain application-specific skill hierarchies that capture domain structure.

### Limitations and Open Questions

1. **Skill composability**: How can we guarantee that composed skills will work correctly together? Current approaches rely on testing rather than formal verification.

2. **Skill discovery**: How can agents discover the need for new skills during execution rather than requiring pre-defined skill libraries?

3. **Cross-domain transfer**: Can skills from one domain (e.g., debugging) transfer to other domains? What makes skills transferable?

4. **Skill naming and organization**: How should skill taxonomies be structured? Are there universal organizational principles or must each domain define its own?

5. **Skill accountability**: When a composed skill fails, how do we attribute failure to specific component skills or their composition?

## Code & Resources

### Official Resources

- **ArXiv Paper**: https://arxiv.org/abs/2605.07358
- **PDF**: https://arxiv.org/pdf/2605.07358
- **HTML Version**: https://arxiv.org/html/2605.07358v1

### Key Frameworks and Libraries

**Agent Frameworks with Skill Support**:
- **AutoGen** (Microsoft): Flexible multi-agent framework with skill abstractions
- **LangGraph**: Stateful orchestration with composable nodes (skills)
- **CrewAI**: Role-based multi-agent framework with skill definitions
- **Claude Code**: Hierarchical skill-based agent architecture

**Skill Management Tools**:
- **SkillCAT**: Contrastive, assessment-augmented skill evolution
- **SkillRevise**: Skill refinement through trace-conditioned revision
- **AutoSkill**: Experience-driven lifelong skill learning
- **Search2Skill**: Skill distillation via reinforcement learning

### Implementation Patterns

**Skill Representation Template** (Python):
```python
@skill(
    name="error_diagnosis",
    domain="debugging",
    input_types={"error_msg": str, "stack_trace": str},
    output_types={"diagnosis": str, "solutions": List[str]}
)
def diagnose_error(error_msg: str, stack_trace: str) -> Dict:
    # Skill logic here
    return {"diagnosis": ..., "solutions": [...]}
```

**Skill Composition Pattern**:
```python
workflow = (
    skill("code_analysis") 
    >> skill("error_detection") 
    >> skill("fix_generation")
    >> skill("validation")
)
```

### Quick-Start Integration Guide

1. **Define Skill Library**:
   - Identify domain-specific capabilities
   - Choose representation (code, DSL, or hierarchical)
   - Create skill specifications with input/output types

2. **Implement Skill Acquisition**:
   - Start with manual authoring for critical skills
   - Use LLM synthesis for prototyping
   - Integrate experience-driven learning

3. **Deploy Skill Retrieval**:
   - Implement semantic matching (embedding-based)
   - Add structured metadata and queries
   - Monitor retrieval accuracy and refine

4. **Enable Skill Evolution**:
   - Instrument skill execution for feedback collection
   - Implement automated skill refinement on failures
   - Set up skill deprecation pipeline for old versions

5. **Monitor and Improve**:
   - Track success rates by skill
   - Identify retrieval failures and improve taxonomy
   - Continuously refine skills based on execution data

## Related Work & Context

### Foundational Concepts

**Tool Use in LLMs**: Function calling (OpenAI, Claude, Anthropic APIs) provides the basic mechanism for tool invocation, which skills build upon.

**Hierarchical Abstraction**: Classical software engineering principles of modularity and abstraction inform skill organization.

**Workflow Automation**: Business process automation and workflow management systems (BPM) provide proven approaches to skill composition and orchestration.

### Related Agent Research

- **Agent Orchestration Patterns**: Phillips et al. identify five coordination patterns, each utilizing different skill architectures
- **Agentic Software Architecture**: Evolution from tools to skills represents a paradigm shift in agent system design
- **Skill Learning and Adaptation**: Papers on automated skill discovery, specialization, and evolution

### Contemporary Work on Specific Skill Aspects

- **Skill Representation**: Papers on code-based, DSL-based, and graph-based approaches to skill definition
- **Skill Acquisition**: LLM-driven synthesis, reinforcement learning approaches, human-in-the-loop skill creation
- **Skill Retrieval**: Semantic retrieval methods, learned selection policies, hierarchical search
- **Skill Evolution**: Automated refinement, in-context learning, feedback-driven improvement

### Future Research Directions

1. **Formal Verification of Skill Composition**: Can we prove properties about composed skills without runtime testing?

2. **Skill Transfer Learning**: How can skills learned in one domain transfer to other domains?

3. **Emergent Skill Hierarchies**: Can agents automatically discover optimal skill hierarchies during execution?

4. **Skill Versioning and Compatibility**: How to manage skill evolution while maintaining compatibility with existing workflows?

5. **Multi-Agent Skill Sharing**: How can multiple agents collaboratively maintain and improve shared skill libraries?

6. **Interpretability of Skills**: How can we make skill behavior more interpretable and debuggable?

---

**Survey Information**:
- **Title**: A Comprehensive Survey on Agent Skills: Taxonomy, Techniques, and Applications
- **Authors**: Yingli Zhou, Shu Wang, Yaodong Su, Wenchuan Du, Yixiang Fang, Xuemin Lin
- **Institution**: The Chinese University of Hong Kong, Shenzhen
- **Submission Date**: May 8, 2026
- **Final Revision**: May 26, 2026 (v3)
- **ArXiv ID**: [2605.07358](https://arxiv.org/abs/2605.07358)
