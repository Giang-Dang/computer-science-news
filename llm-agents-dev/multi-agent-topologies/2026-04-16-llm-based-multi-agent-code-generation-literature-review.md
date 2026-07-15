# LLM-Based Multi-Agent Systems for Code Generation: A Multi-Vocal Literature Review

**ArXiv ID:** [2604.16321](https://arxiv.org/abs/2604.16321)  
**Authors:** Zeeshan Rasheed, Muhammad Waseem, Kai-Kristian Kemell, Mika Saari, Pekka Abrahamsson  
**Affiliations:** Faculty of Information Technology and Communication Sciences, Tampere University, Finland  
**Submitted:** April 2026  
**Field:** Software Engineering / AI Agents / Code Generation

---

## Executive Summary

This multi-vocal literature review synthesizes evidence from 114 peer-reviewed and grey literature sources to provide a comprehensive understanding of LLM-based multi-agent systems in code generation. The review identifies adoption motivations across 9 categories, systematically analyzes models and benchmarks, and synthesizes challenges into 6 main categories with 26 subcategories, alongside proposed solutions. This work establishes the state of the art in multi-agent code generation and identifies critical research gaps and future directions for autonomous software development systems.

## Problem Statement

The rapid adoption of LLM-based multi-agent systems for code generation across academia and industry has created a fragmented landscape where:

1. **Knowledge Fragmentation**: Understanding spans both academic research and industrial practice, with limited synthesis between domains
2. **Challenge Characterization**: Systematic understanding of failure modes, limitations, and open problems remains fragmented
3. **Best Practice Unclear**: Design patterns, architectural choices, and evaluation approaches are not well-established
4. **Orchestration Complexity**: Multi-agent coordination introduces new challenges distinct from single-agent systems
5. **Quality Assurance**: Code quality, correctness, and reliability metrics need systematic characterization

The core research gap: What are the motivations, state-of-the-art approaches, critical challenges, and future directions for multi-agent LLM-based code generation systems?

## Core Concepts & Theory

### Multi-Vocal Literature Review (MLR) Methodology

Unlike traditional systematic reviews limited to peer-reviewed literature, the MLR approach synthesizes:
- **Academic sources**: Peer-reviewed conference papers and journals
- **Grey literature**: Industry white papers, technical blogs, open-source documentation
- **Practitioner insights**: Real-world deployment experiences and lessons learned

This combined perspective captures both theoretical advances and practical constraints.

### Adoption Motivation Framework (9 Categories)

The review identifies distinct motivations driving multi-agent adoption:

1. **Scalability & Parallelization**: Multiple agents enable parallel task execution
2. **Specialization & Expertise**: Different agents excel at distinct code generation tasks
3. **Reasoning & Planning**: Hierarchical multi-agent systems improve decomposition
4. **Code Quality**: Ensemble approaches and verification agents improve correctness
5. **Tool Integration**: Multiple agents coordinate tool use for complex tasks
6. **Knowledge Management**: Agent teams leverage different knowledge bases
7. **Error Recovery**: Specialized debugging agents handle failures
8. **Performance**: Agent cooperation accelerates code generation
9. **Cost Optimization**: Intelligent routing reduces API costs

### Challenge Framework (6 Categories)

#### 1. Hallucination & Factual Correctness (8.77% of studies)
- Generated code references non-existent APIs/libraries
- Incorrect function signatures
- Fabricated algorithm implementations

#### 2. Low Accuracy & Quality (6.14%)
- Suboptimal algorithm choices
- Edge case mishandling
- Performance degradation in complex scenarios

#### 3. Orchestration Failures (4.39%)
- Deadlock between coordinating agents
- Communication breakdown
- Poor task allocation

#### 4. Lack of High-Level Planning (3.51%)
- Missing hierarchical decomposition
- Insufficient task structure
- Limited strategic reasoning

#### 5. Agent Dependency Issues (2.63%)
- Single points of failure
- Insufficient agent diversity
- Incomplete specialization

#### 6. Code Consistency Problems (1.75%)
- Divergent implementations across agents
- Style inconsistencies
- Architecture mismatch

### Solution Approaches Identified

**Iterative Human Feedback Loops**: Agents refined through human-in-the-loop processes

**Error-Checking Mechanisms**: Post-generation validation and verification agents

**Schema-Based Communication**: Structured message formats ensure agent interoperability

**Dynamic Communication Structures**: Adaptive topologies based on task requirements

**Verification Systems**: Additional agents dedicated to code correctness validation

## Main Ideas & Contributions

### Contribution 1: Comprehensive Evidence Synthesis (114 Studies)

The review systematically categorizes findings from:
- 80+ peer-reviewed academic sources
- 34+ grey literature and industry sources
- Spanning 2023-2026 (cutting-edge research)

### Contribution 2: Multi-Agent System Categorization

Distinct classes of multi-agent approaches:

**Hierarchical Topologies**: Manager-worker architectures with central coordination

**Collaborative Topologies**: Peer-based agent cooperation without central authority

**Specialist Topologies**: Task-specific agents orchestrated for code generation

**Ensemble Topologies**: Multiple agents generating competing solutions for selection

### Contribution 3: Model & Benchmark Analysis

Systematically analyzes:
- **Models Used**: GPT-4, Claude, Gemini, open-weight alternatives
- **Benchmarks Evaluated**: HumanEval, MBPP, CodeContests, real-world repositories
- **Evaluation Metrics**: Pass@k, execution success, code quality metrics

### Contribution 4: Systematic Challenge Identification

Prioritizes challenges by research coverage:
1. Hallucinations (most studied)
2. Low accuracy
3. Orchestration failures
4. Planning deficiencies
5. Agent dependencies
6. Code consistency

### Contribution 5: Future Research Directions (6 Categories, 18 Subcategories)

Identifies research gaps across:
- Agent design and specialization
- Communication protocols standardization
- Verification and correctness assurance
- Integration with development tools
- Enterprise deployment patterns
- Ethical and safety considerations

## Methodology & Implementation

### Literature Search Strategy

**Search Queries** across multiple databases:
- "LLM agent code generation"
- "multi-agent software engineering"
- "agent orchestration development"
- "autonomous coding systems"
- "collaborative AI programming"

**Search Scope**:
- Academic databases: Google Scholar, IEEE Xplore, ACM Digital Library
- Grey literature: ArXiv, technical blogs, GitHub discussions
- Time range: 2023-2026 (rapid growth period)

### Selection Criteria

**Inclusion Criteria**:
- Systems with ≥2 agents
- LLM-based approaches
- Code generation focus
- Empirical evaluation or framework design

**Exclusion Criteria**:
- Single-agent systems
- Non-code generation tasks
- Pure theoretical work without implementation

### Data Extraction & Analysis

**Extracted Data Points**:
- Publication type and venue
- Agent architecture (topology, roles)
- Coordination mechanisms
- Evaluation benchmarks
- Reported challenges and solutions
- Performance metrics

**Synthesis Method**:
- Thematic analysis for challenges
- Comparative analysis of topologies
- Evidence quality assessment

## Practical Applications & Use Cases

### Use Case 1: Large Codebase Refactoring

**Challenge**: Refactor complex legacy system spanning 100K+ lines

**Multi-Agent Solution**:
- Analyzer agent: Maps dependencies and architecture
- Planner agent: Designs refactoring strategy
- Implementer agents: Parallel implementation of modules
- Verifier agent: Ensures correctness and consistency

**Benefits**: Parallelization, specialization, automated verification

### Use Case 2: Open-Source Project Contribution

**Challenge**: Contributing to unfamiliar codebase with specific requirements

**Multi-Agent Solution**:
- Requirement analyzer: Understands feature request
- Code explorer: Maps relevant files and APIs
- Implementer: Writes implementation matching style
- Test generator: Creates comprehensive tests
- Documentation agent: Updates docs and comments

**Benefits**: Knowledge-assisted development, quality assurance, completeness

### Use Case 3: Bug Fixing at Scale

**Challenge**: Fix recurring bug pattern across multiple repositories

**Multi-Agent Solution**:
- Bug detector: Identifies pattern occurrences
- Root cause analyzer: Understands bug origin
- Fix generator: Creates targeted fixes
- Regression tester: Validates fixes don't break other code
- Patch orchestrator: Coordinates across repositories

**Benefits**: Systematic bug resolution, reduced manual effort, consistency

## Insights & Implications

### Key Findings

**1. Orchestration as Core Challenge**
- Multi-agent coordination is not just additive to single-agent systems
- Orchestration failures represent distinct problem class
- Future systems must prioritize coordination mechanisms

**2. Specialization Drives Quality**
- Purpose-built agents outperform generalists
- Task decomposition into specialist roles improves outcomes
- Role diversity enhances ensemble quality

**3. Verification is Essential**
- Code correctness cannot be assumed
- Dedicated verification agents improve reliability
- Human-in-the-loop loops remain valuable

**4. Planning Enables Reasoning**
- Hierarchical decomposition improves complex task solving
- Multi-turn planning outperforms single-pass generation
- Structure reduces hallucination and errors

### Advancement Over Single-Agent Systems

**Multi-Agent Advantages**:
- 15-40% improvement in code correctness (from reviewed studies)
- Parallel execution reduces latency
- Specialization improves domain-specific quality
- Ensemble diversity handles edge cases better
- Human feedback integration enhances outcomes

### Limitations & Research Gaps

**Remaining Challenges**:
1. **Reproducibility**: Many industrial systems not publicly evaluated
2. **Cost vs. Benefit**: Trade-off between coordination overhead and quality gains unclear
3. **Scalability**: Performance with 10+ agents not well-studied
4. **Standardization**: Lack of standard protocols hinders interoperability
5. **Evaluation**: Comprehensive benchmarks for orchestration quality missing

### Relevance to Agent Systems & Development Automation

**Implications for Agent Frameworks**:
- Next-generation frameworks must support flexible topologies
- Communication protocols need standardization
- Orchestration abstractions must hide complexity
- Verification integration should be built-in

**Implications for Development Automation**:
- Multi-agent approach is becoming standard practice
- Specialized agent roles reduce cognitive load
- Tool integration requires careful coordination
- Quality assurance demands verification strategies

## Code & Resources

### Official Resources

- **ArXiv Paper**: [2604.16321](https://arxiv.org/abs/2604.16321)
- **Paper PDF**: [Full text available on ArXiv](https://arxiv.org/pdf/2604.16321)

### Related Frameworks & Systems

- **CrewAI**: Multi-agent framework for collaborative workflows
- **AutoGen**: Microsoft's multi-agent conversation framework
- **LangGraph**: LangChain's agent orchestration library
- **MetaGPT**: Role-based agent system for software engineering

### Datasets & Benchmarks Referenced

- **HumanEval**: Function-level code generation (164 problems)
- **MBPP**: Medium/hard business problems (974 problems)
- **CodeContests**: Competitive programming problems
- **SWE-Bench**: Real software engineering tasks

### Quick-Start Integration Guide

**For Researchers**:
1. Review challenge categorization (6 categories, 26 subcategories)
2. Map your system against identified solutions
3. Use benchmark recommendations for evaluation
4. Adopt suggested performance metrics

**For Practitioners**:
1. Select topology matching your use case
2. Implement solution patterns for identified challenges
3. Integrate verification mechanisms early
4. Plan for human feedback loops

## Related Work & Context

### Prior Foundational Work

- **Single-agent code generation**: GPT-Codex, Copilot, CodeGen
- **Tool-using agents**: Function calling in LLMs (GPT-4, Claude)
- **Multi-turn planning**: Chain-of-thought, tree-of-thought reasoning
- **Verification systems**: Program synthesis with correctness guarantees

### Related Papers on Multi-Agent Systems

- "The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption" (2601.13671)
- "ABSTRAL: Automated Multi-Agent System Design via Skill-Referenced Adaptive Search" (2603.24...)
- "AgentForge: Execution-Grounded Multi-Agent LLM Framework" (2604.06...)
- "EvoAgent: An Evolvable Agent Framework with Skill Learning" (2604.22...)

### Possible Extensions & Future Research

1. **Real-Time Coordination**: Improving latency in multi-turn agent interactions
2. **Context Efficiency**: Reducing token usage in complex multi-agent workflows
3. **Failure Recovery**: Better handling of agent failures and cascading errors
4. **Enterprise Patterns**: Deployment patterns for production-grade systems
5. **Certification & Safety**: Formal methods for multi-agent system verification
6. **Cost Modeling**: Understanding efficiency trade-offs at scale

### Emerging Research Directions

- **Agent Specialization**: Learning distinct skills per agent role
- **Dynamic Topology**: Adaptive multi-agent structures based on task complexity
- **Standardized Protocols**: Industry-wide agent communication standards
- **Verification Integration**: Built-in correctness guarantees for generated code
- **Human-AI Collaboration**: Scalable feedback mechanisms for human-in-the-loop improvement

