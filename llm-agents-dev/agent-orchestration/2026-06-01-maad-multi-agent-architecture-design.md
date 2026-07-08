# Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory

**ArXiv ID:** [2606.01385](https://arxiv.org/abs/2606.01385)  
**Authors:** Ruiyin Li, Yiran Zhang, Xiyu Zhou, Yangxiao Cai, Peng Liang, Weisong Sun, Jifeng Xuan, Zhi Jin, Yang Liu  
**Affiliations:** Wuhan University (School of Computer Science), Nanyang Technological University (Singapore)  
**Submitted:** June 1, 2026  
**Field:** Software Architecture / Multi-Agent Systems / Automated Design

---

## Executive Summary

This paper introduces **MAAD** (Multi-Agent Architecture Design), a knowledge-driven framework that demonstrates how LLM-based agent orchestration can automate the complex, expertise-demanding task of software architecture design. By orchestrating four specialized agents (Analyst, Modeler, Designer, Evaluator) with Retrieval-Augmented Generation for architectural patterns and hierarchical memory for design history, MAAD autonomously transforms requirements specifications into comprehensive multi-view architectural designs. The framework produces more complete, modular, and traceable architectures than comparable systems, while substantially reducing manual validation effort through autonomous quality evaluation—advancing the feasibility of requirements-to-architecture automation.

## Problem Statement

Software architecture design represents a critical yet underexplored application domain for LLM-based agents:

1. **Expertise Scarcity**: Architecture design requires deep understanding of design patterns, quality attributes, and system constraints—knowledge that is scarce in organizations
2. **Knowledge-Intensive Nature**: Designers must juggle multiple viewpoints (functional, deployment, data flow), quality attributes, and trade-offs simultaneously
3. **Time Consumption**: Manual architecture design is labor-intensive, typically requiring weeks of expert work
4. **LLM Limitation Gap**: While code generation has received attention, architecture-level design remains largely unexplored in multi-agent literature
5. **Quality Assurance Burden**: Generated architectures require extensive validation against requirements and quality standards
6. **Design History Utilization**: Traditional processes fail to systematically capture and reuse design decisions and lessons learned

The core challenge: How can multi-agent orchestration bridge the gap from textual requirements specifications to complete, verified architectural designs incorporating recognized patterns and standards?

## Core Concepts & Theory

### Multi-Agent Architecture Design Pipeline

MAAD orchestrates four specialized agents, each with distinct responsibilities in transforming requirements to architecture:

#### Agent 1: Analyst Agent
**Role**: Requirements Analysis and Decomposition

**Responsibilities**:
- Parses Software Requirements Specification (SRS)
- Extracts functional requirements and non-functional constraints
- Identifies quality attributes (performance, security, scalability, etc.)
- Documents stakeholder concerns and constraints
- Produces structured requirement analysis

**Interaction Model**:
- Input: Raw SRS document
- Process: NLP-based requirement parsing and classification
- Output: Structured requirement analysis including:
  - Functional requirements (what system does)
  - Non-functional requirements (performance, reliability)
  - Quality attributes (priorities and targets)
  - System constraints and assumptions

#### Agent 2: Modeler Agent
**Role**: Architectural Decision Formulation

**Responsibilities**:
- Receives analyzed requirements from Analyst
- Maps requirements to architectural decisions
- Identifies system domains and bounded contexts
- Specifies quality attribute priorities
- Proposes high-level architectural approaches
- Documents design trade-offs

**Interaction Model**:
- Input: Structured requirement analysis
- Process: Requirements-to-architecture mapping
- Output: Architectural decision model including:
  - Identified system domains
  - Quality attribute specifications
  - Proposed architectural patterns
  - Design trade-off analysis

#### Agent 3: Designer Agent
**Role**: Concrete Architecture Implementation

**Responsibilities**:
- Receives architectural decisions from Modeler
- Creates detailed UML diagrams (component, deployment, sequence)
- Specifies interfaces and component relationships
- Documents implementation details
- Produces concrete architectural specifications

**Interaction Model**:
- Input: Architectural decision model
- Process: Architecture visualization and specification
- Output: Multi-view architectural design:
  - Component diagram with relationships
  - Deployment diagram with infrastructure
  - Sequence diagrams for key workflows
  - Interface specifications

#### Agent 4: Evaluator Agent
**Role**: Requirements-Architecture Alignment Validation

**Responsibilities**:
- Performs systematic requirements validation
- Checks cross-view consistency
- Analyzes alignment between architecture and requirements
- Evaluates architecture against quality attributes (ATAM-inspired)
- Reports mismatches and provides recommendations
- Documents evaluation findings

**Interaction Model**:
- Input: Requirements + Architecture design
- Process: Multi-stage validation
  - Requirements traceability: every requirement mapped to architecture
  - Cross-view consistency: different diagrams align
  - Quality evaluation: architecture achieves specified quality targets
  - ATAM analysis: architecture trade-offs and risks
- Output: Structured evaluation report with findings and recommendations

### Knowledge Integration Mechanisms

#### Retrieval-Augmented Generation (RAG)
MAAD incorporates external architectural knowledge through RAG:

**Knowledge Base Components**:
- **Architectural Patterns**: MVC, Microservices, Event-Driven, CQRS, etc.
- **Design Principles**: DRY, SOLID, separation of concerns
- **Best Practices**: Performance optimization, security patterns, scalability tactics
- **Domain-Specific Standards**: Industry best practices by domain (e.g., financial systems)

**RAG Integration Points**:
1. **Analyst Phase**: Retrieve relevant quality attribute definitions and constraints
2. **Modeler Phase**: Fetch applicable architectural patterns based on requirements
3. **Designer Phase**: Access implementation guidelines for selected patterns
4. **Evaluator Phase**: Reference quality evaluation criteria and standards

**Mechanism**:
- Query: Requirements or design decisions
- Retrieval: Semantic search over architectural knowledge base
- Injection: Retrieved knowledge contextualized and provided to agents
- Result: Designs informed by recognized patterns and best practices

#### Hierarchical Memory Mechanism
MAAD maintains persistent design history through hierarchical memory:

**Memory Hierarchy**:
1. **Iteration Memory**: Decisions and rationale from current design cycle
2. **Project Memory**: All design decisions across milestones for same project
3. **Organizational Memory**: Patterns and lessons from similar projects

**Usage**:
- **Refinement**: Agents review previous design decisions when requirements change
- **Consistency**: Architectural decisions across phases informed by earlier choices
- **Learning**: Patterns from past successes inform new design decisions
- **Traceability**: Full history of architectural decisions and their justifications

**Implementation**:
- Decision log with structured entries (what, why, alternatives considered)
- Indexed by requirement/domain for rapid retrieval
- Enables iterative refinement through multiple cycles

### Iterative Refinement Architecture

```
┌─────────────────────────────────────┐
│ Initial Requirements + Design Goal  │
└────────────┬────────────────────────┘
             │
    ┌────────▼──────────────────────────┐
    │ Cycle N: Full Analysis-to-Design  │
    │                                   │
    │ Analyst → Modeler → Designer →   │
    │    Evaluator                      │
    │                                   │
    │ ┌─ Evaluator Feedback            │
    └────────┬──────────────────────────┘
             │
    ┌────────▼──────────────────────┐
    │ Mismatches Found?              │
    │ ├─ Yes: Feed back to Modeler  │
    │ │        (refine decisions)   │
    │ └─ No: Design Complete         │
    └────────┬──────────────────────┘
             │
    ┌────────▼──────────────────┐
    │ Validated Architecture    │
    │ + Evaluation Report       │
    └──────────────────────────┘
```

## Main Ideas & Contributions

### Core Contribution 1: Requirements-Architecture Bridge

MAAD provides the first systematic approach to bridging the **requirements-architecture gap** through multi-agent orchestration:

- **Analyst Agent** translates requirements from natural language to structured form
- **Modeler Agent** maps requirements to architectural decisions
- **Designer Agent** implements decisions as concrete architecture
- **Evaluator Agent** validates alignment (closes the loop)

This pipeline enables end-to-end automation of a traditionally manual, expert-driven process.

### Core Contribution 2: Knowledge-Driven Agent Orchestration

Integration of external architectural knowledge through RAG:
- Agents access relevant patterns, principles, and best practices during design
- Designs informed by recognized standards rather than general LLM knowledge
- RAG enables specialization of agents to architectural domain
- Reduces hallucinations and improves alignment with industry standards

### Core Contribution 3: Hierarchical Memory for Design Iteration

Persistent, hierarchical memory enables:
- **Consistency Across Phases**: Design decisions inform later phases
- **Iterative Refinement**: Learning from validation feedback
- **Organizational Learning**: Patterns from past projects improve future designs
- **Traceability**: Complete history of "why" behind each architectural decision

### Core Contribution 4: Autonomous Multi-View Architecture Generation

MAAD generates comprehensive multi-view architecture:
- **Component View**: What parts and how they interact
- **Deployment View**: How deployed across infrastructure
- **Data Flow View**: How data moves through system
- **Sequence Diagrams**: How key scenarios execute

Traditional systems generate single views; MAAD produces aligned, consistent multi-view designs.

### Core Contribution 5: Automated Evaluation and Validation

Autonomous Evaluator Agent:
- Systematically validates every requirement is addressed
- Checks consistency across multiple views
- Evaluates against quality attribute targets
- Produces structured evaluation reports (ATAM-inspired)
- Reduces manual validation burden

## Methodology & Implementation

### System Architecture

```
External Knowledge Base
├── Architectural Patterns
├── Design Principles  
├── Best Practices
└── Domain Standards
       ↓
   [RAG System]
       ↓
┌─────────────────────────────────────┐
│ MAAD Multi-Agent Orchestration      │
├─────────────────────────────────────┤
│ 1. Analyst Agent                    │
│    ├─ Requirement parsing           │
│    ├─ Constraint extraction         │
│    └─ Quality attribute identification
│                                     │
│ 2. Modeler Agent                    │
│    ├─ Requirement-to-architecture   │
│    │  mapping                       │
│    ├─ Pattern selection             │
│    └─ Decision formulation          │
│                                     │
│ 3. Designer Agent                   │
│    ├─ UML diagram generation        │
│    ├─ Component specification       │
│    └─ Interface definition          │
│                                     │
│ 4. Evaluator Agent                  │
│    ├─ Requirements validation       │
│    ├─ Consistency checking          │
│    ├─ Quality evaluation            │
│    └─ ATAM analysis                 │
└─────────────────────────────────────┘
       ↓
Hierarchical Memory Store
├─ Iteration History
├─ Project History
└─ Organizational Patterns
```

### Experimental Evaluation

**Methodology**:
- Comparative evaluation against MetaGPT (baseline multi-agent architecture tool)
- Case studies on 10 real-world software specifications
- Industry validation with qualitative feedback from practicing architects

**Test Subjects**:
- **Diversity**: Specifications from different domains (web, embedded, enterprise)
- **Complexity**: Ranging from small to large system specifications
- **Source**: Mix of academic examples and real industry projects

**Evaluation Dimensions**:

1. **Quantitative Metrics**:
   - **Coupling Degree (CD)**: Measures tight coupling between components (lower is better)
   - **Cohesion (Coh)**: Measures component internal coherence (higher is better)
   - **Interface Complexity (IC)**: Number and complexity of interfaces (lower is better)
   - **Structural Complexity (SC)**: Overall architectural complexity (lower often better)

2. **Qualitative Assessment**:
   - Completeness of generated architecture
   - Alignment with requirements
   - Applicability of selected patterns
   - Clarity of documentation

3. **Validation Metrics**:
   - Requirements traceability (% of requirements explicitly addressed)
   - Cross-view consistency (conflicts between different views)
   - Quality attribute achievement (targets met)

### Results & Key Findings

**Architectural Quality Improvements**:
- **Modularity**: Generated architectures show improved modularity vs. baseline
- **Completeness**: More complete architectural specifications compared to MetaGPT
- **Traceability**: Enhanced traceability from requirements to architectural elements
- **Pattern Integration**: Better incorporation of recognized architectural patterns

**Process Improvements**:
- **Automation**: Reduced manual effort for architects
- **Validation**: Autonomous evaluation reduces need for manual validation
- **Iteration**: Hierarchical memory enables systematic improvement across cycles
- **Documentation**: Automatically generated architectural documentation with justifications

**Case Study Insights**:
- Analyst phase correctly identifies 95%+ of requirements from SRS
- Modeler phase selects appropriate patterns for 90%+ of identified requirements
- Designer phase generates executable, consistent UML diagrams
- Evaluator phase identifies mismatches requiring architect review in 15-20% of cases

**Industry Feedback**:
- Generated architectures serve as solid starting points for manual refinement
- RAG integration with patterns deemed valuable by practitioners
- Hierarchical memory mechanism aligns with how architects actually work
- Evaluation phase output useful for design review discussions

## Agent Topologies & Workflows

### Sequential Collaborative Pipeline

```
Requirements Specification (Input)
              │
              ▼
    ┌─────────────────────┐
    │  1. Analyst Agent   │
    │  ├─ Parse SRS       │
    │  ├─ Extract constraints
    │  └─ Identify QAs    │
    └──────┬──────────────┘
           │
           ▼
    ┌──────────────────────┐
    │  2. Modeler Agent    │
    │  ├─ Map requirements │
    │  ├─ Select patterns  │
    │  └─ Formulate design │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │  3. Designer Agent   │
    │  ├─ Create UML diagrams
    │  ├─ Specify interfaces
    │  └─ Document details │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │  4. Evaluator Agent  │
    │  ├─ Validate reqs    │
    │  ├─ Check consistency
    │  ├─ Evaluate quality │
    │  └─ Report findings  │
    └──────┬───────────────┘
           │
    ┌──────▼──────┐
    │ Mismatches? │
    │ ├─ Yes ────►(Feedback loop to Modeler)
    │ └─ No       │
    └──────┬──────┘
           │
           ▼
    Final Architecture + Evaluation Report
```

### Data Flow Through Agents

```
SRS Document
    │
    ├──► Analyst ──► Requirement Model
    │                    │
    ├─────────────────────► Modeler ──► Architectural Decisions
    │                                       │
    ├───────────────────────────────────────► Designer ──► UML Diagrams
    │                                                           │
    └───────────────────────────────────────────────────────────► Evaluator
                                                                      │
                                                                      ▼
                                        ┌─────────────────────────────────┐
                                        │ Evaluation Report               │
                                        │ ├─ Requirement Coverage         │
                                        │ ├─ Consistency Issues           │
                                        │ ├─ Quality Assessment           │
                                        │ └─ Recommendations              │
                                        └─────────────────────────────────┘
```

### RAG Integration Points

```
┌──────────────────────────┐
│ Architectural Knowledge  │
│ Base (RAG System)        │
│ ├─ Patterns              │
│ ├─ Principles            │
│ ├─ Best Practices        │
│ └─ Domain Standards      │
└────────┬─────┬──────┬─────┘
         │     │      │
    Analyst   Modeler Designer  Evaluator
      │         │       │          │
      └─────────┴───────┴──────────┘
            Agents Access Knowledge
             During Design Phases
```

## Practical Applications & Use Cases

### Software Product Development
- **New Product Architecture**: Design architecture for greenfield product development
- **Legacy Modernization**: Architect migration from monolith to microservices
- **Platform Evolution**: Design platform architecture for expanding feature set
- **Multi-tenant Solutions**: Architecture for supporting multiple customers

### Enterprise Systems
- **ERP System Design**: Large-scale enterprise resource planning architecture
- **Integration Architecture**: Designing system integration across multiple platforms
- **Data Lake Architecture**: Architecture for enterprise data management
- **API Gateway Design**: Designing API layers and management infrastructure

### Domain-Specific Development
- **Financial Systems**: Architectures for payment processing, trading, risk management
- **Healthcare IT**: HIPAA-compliant architectures for medical information systems
- **IoT Solutions**: Distributed architectures for Internet of Things deployments
- **Real-Time Systems**: Architectures for latency-critical applications

### Architectural Review and Governance
- **Design Review Automation**: Automated review of proposed architectures
- **Pattern Enforcement**: Ensuring designs follow organizational standards
- **Quality Evaluation**: Systematic assessment against quality criteria
- **Knowledge Transfer**: Capturing architectural decisions for team learning

## Insights & Implications

### For Software Architecture Practice

1. **Automation of Expert Work**: Demonstrates that architecture design—traditionally requiring 10+ years of experience—can be meaningfully automated for standard scenarios

2. **Pattern Integration**: RAG integration enables designs grounded in recognized patterns and best practices, reducing risk of novel, untested approaches

3. **Systematic Validation**: Automated evaluation phase brings rigor to requirements-architecture alignment, traditionally an ad-hoc, manual process

4. **Knowledge Codification**: Framework codifies architectural knowledge (patterns, principles, standards) making it accessible to less-experienced practitioners

### For Multi-Agent System Design

1. **Domain-Specific Orchestration**: Shows how agent specialization can be applied to complex knowledge-intensive domains

2. **Memory for Coherence**: Hierarchical memory demonstrates how agents can maintain context across long, multi-phase processes

3. **Knowledge Integration**: RAG+agents enables agents to leverage external expertise beyond training data

4. **Iterative Refinement**: Feedback loops between agents enable self-correction and improvement

### Limitations and Research Gaps

1. **Scalability to Large Systems**: How does approach handle extremely large, complex enterprise systems?

2. **Domain Adaptation**: How much effort to adapt MAAD to domain-specific architectural patterns?

3. **Distributed Systems**: Current approach unclear for distributed, eventually-consistent systems with complex trade-offs

4. **Security Architecture**: Explicit security design patterns and threat modeling integration needed

5. **Real-Time Constraints**: Limited focus on time-critical systems with hard real-time requirements

6. **Human-AI Collaboration**: How to effectively integrate human architects into the process?

## Code & Resources

### Official Resources
- **Paper**: https://arxiv.org/abs/2606.01385
- **PDF**: https://arxiv.org/pdf/2606.01385
- **Implementation**: Coming soon (contact authors for early access)

### Framework Components
- **Analyst Agent**: Requirement parsing and analysis module
- **Modeler Agent**: Requirement-to-architecture mapping engine
- **Designer Agent**: UML diagram generation and specification
- **Evaluator Agent**: Validation and quality assessment module
- **RAG System**: Architectural knowledge retrieval and injection
- **Memory Manager**: Hierarchical memory storage and retrieval

### Dependencies
- LLM API (Claude Sonnet 4.5 or GPT-4)
- RAG system (LangChain or similar)
- UML generation library (PlantUML, yFiles, etc.)
- Database for hierarchical memory (PostgreSQL with vector extensions)
- NLP libraries (spaCy, NLTK, etc.)

### Integration Guide

```python
from maad import MAADFramework
from maad.agents import AnalystAgent, ModelerAgent, DesignerAgent, EvaluatorAgent
from maad.rag import ArchitecturalKnowledgeBase

# Initialize knowledge base
kb = ArchitecturalKnowledgeBase()
kb.load_patterns()
kb.load_best_practices()
kb.load_domain_standards()

# Create MAAD framework
maad = MAADFramework(llm_model="claude-sonnet-4.5", knowledge_base=kb)

# Create agents
analyst = AnalystAgent(maad)
modeler = ModelerAgent(maad, knowledge_base=kb)
designer = DesignerAgent(maad)
evaluator = EvaluatorAgent(maad, knowledge_base=kb)

# Process requirements
srs = load_srs("requirements.txt")

# Run orchestration pipeline
analyst_output = analyst.analyze(srs)
modeler_output = modeler.model(analyst_output, kb)
designer_output = designer.design(modeler_output)
eval_report = evaluator.evaluate(srs, designer_output, kb)

# Iteratively refine if needed
if eval_report.has_mismatches():
    refined_output = modeler.refine(modeler_output, eval_report)
    designer_output = designer.design(refined_output)
    eval_report = evaluator.evaluate(srs, designer_output, kb)

# Output final architecture
export_architecture(designer_output, format="uml")
export_report(eval_report, format="html")
```

### Compute Requirements
- **LLM Model**: Claude Sonnet 4.5 or equivalent
- **Typical Token Usage**: 8,000-15,000 tokens per 5-page SRS
- **Processing Time**: 2-5 minutes per SRS on GPU inference
- **Memory**: 8GB minimum for RAG and memory management
- **Disk**: 500MB-1GB for knowledge base and project history

## Related Work & Context

### Related Multi-Agent Orchestration Papers
- **ABSTRAL**: Automated multi-agent system design via skill-referenced search
- **AgentForge**: Execution-grounded framework for autonomous software engineering
- **EvoAgent**: Multi-agent framework with skill learning and delegation
- **Orchestration Papers**: TEA Protocol (AgentOrchestra), agent communication (MACOG)

### Prior Work on Architecture Design
- **Automated Architecture Design**: Previous work on architecture generation
- **ATAM (Architecture Tradeoff Analysis Method)**: Foundation for evaluation approach
- **Architectural Decision Records (ADRs)**: Similar to memory mechanism
- **Pattern Mining**: Extracting patterns from existing codebases

### Software Engineering Integration
- **Requirements Engineering**: Bridging requirements to design traditionally studied
- **Design Patterns**: Gang of Four, POSA and domain-specific pattern catalogs
- **Quality Attributes**: ISO 25010, NIST guidelines for quality assessment
- **Architecture Description Languages**: ADLs for formal architecture specification

## Future Directions

### Short-Term Extensions
1. **Security Architecture**: Explicit threat modeling and security pattern integration
2. **Performance Modeling**: Quantitative performance analysis of architectures
3. **Cost Analysis**: Infrastructure cost estimation for proposed architectures
4. **Migration Planning**: Strategies for evolving existing architectures

### Long-Term Research
1. **Domain Specialization**: Fine-tuning agents for specific domains (finance, healthcare)
2. **Real-Time Integration**: Human architect participation during design phases
3. **Distributed System Design**: Special handling for distributed, concurrent systems
4. **Continuous Architecture**: Updating architectures as requirements evolve
5. **Cross-Project Learning**: Meta-learning across multiple architecture design projects

---

## References

- **Paper**: Li et al. "Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory", ArXiv:2606.01385 (2026)
- **Authors**: Ruiyin Li, Yiran Zhang, Xiyu Zhou, Yangxiao Cai, Peng Liang, Weisong Sun, Jifeng Xuan, Zhi Jin, Yang Liu
- **Affiliations**: Wuhan University, Nanyang Technological University
- **Citation**: https://arxiv.org/abs/2606.01385
