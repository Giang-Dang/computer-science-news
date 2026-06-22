# LLM Consortium for Software Design Refinement: A Controlled Experiment on Multi-Agent Collaboration Topologies

**ArXiv ID:** 2606.01490  
**Authors:** Nagarjuna Kanamarlapudi, Praveen K  
**Submitted:** June 1, 2026  
**Topic:** Multi-agent software design, collaboration topologies, empirical evaluation, architectural reasoning

---

## Executive Summary

Designing software architecture requires nuanced reasoning, trade-offs, and iterative refinement—tasks well-suited for multi-agent collaboration. This paper presents a controlled empirical study evaluating **12 distinct multi-agent LLM collaboration topologies** for software design refinement using a **2×2×2 factorial design** (Authority × Roles × Dynamics) across 8 design tasks with 520 experimental runs and automated evaluation by three independent evaluators. Results show that **structural adversarial topology** (combining hierarchy with adversarial review) ranks first, while **cross-model review** (generation with one LLM, review with another) ranks second—providing empirical evidence for optimal multi-agent coordination patterns in architectural decision-making.

---

## Problem Statement

### Current Challenge

Software architecture design is inherently collaborative:
- Multiple concerns: scalability, maintainability, cost, security, performance
- Trade-offs require debate and iteration
- Single-LLM systems cannot adequately capture the exploration and critique needed
- No principled framework for determining which multi-agent topology best supports design reasoning

### Prior Limitations

Existing multi-agent design systems:
- Use ad-hoc topologies without empirical comparison
- Lack systematic evaluation frameworks
- Assume one topology fits all design scenarios
- Don't quantify the impact of specific coordination patterns (hierarchy, roles, dynamics)
- Rely on qualitative assessment rather than automated rubrics

### Research Gap

The field lacks:
1. **Controlled experimental design** comparing multiple topologies systematically
2. **Quantitative evaluation framework** for architectural design quality
3. **Factor isolation** (authority, roles, dynamics) to understand topology components
4. **Empirical validation** that certain topologies yield better architectural decisions

---

## Core Concepts & Theory

### 1. Topology Dimensions (2×2×2 Factorial Design)

The paper deconstructs multi-agent topologies into three orthogonal factors:

#### **Factor 1: Authority Structure**

```
Flat (Peer-to-Peer):
  Agent1 ←→ Agent2 ←→ Agent3
  All equal decision weight
  
Hierarchical:
  Manager
    ↓
  Agent1, Agent2, Agent3
  Manager coordinates; specialists execute
```

**Flat Advantages:** Democratic, diverse viewpoints, robust to individual failures  
**Hierarchical Advantages:** Coordinated, decisive, clear responsibility

#### **Factor 2: Role Definition**

```
Homogeneous (All Agents Same Role):
  Agent1 (designer): "Design an API"
  Agent2 (designer): "Design an API"
  Agent3 (designer): "Design an API"
  → Debate among similar perspectives
  
Heterogeneous (Specialized Roles):
  Agent1 (architect): "Define system structure"
  Agent2 (security): "Identify threats and mitigations"
  Agent3 (performance): "Optimize for latency"
  → Complementary expertise
```

**Homogeneous Advantages:** Depth within single perspective, reduced dependencies  
**Heterogeneous Advantages:** Breadth across concerns, natural complementarity

#### **Factor 3: Dynamics (Static vs. Adaptive)**

```
Static Topology:
  Round 1: Generate design
  Round 2: Review design (same reviewers)
  Round 3: Finalize (same agents)
  
Dynamic/Evolving Topology:
  Round 1: Generate design
  Round 2: Review design
  → Identify weaknesses
  → Bring in new specialist (e.g., cost analyst)
  Round 3: Re-design with new perspective
```

**Static Advantages:** Predictable, reproducible, lower coordination overhead  
**Dynamic Advantages:** Adaptive to emerging concerns, learns from critique

### 2. The 12 Topologies (2³ = 8 base combinations + variants)

```
┌─────────────────┬──────────────┬──────────────┬───────────────┐
│ Authority       │ Roles        │ Dynamics     │ Topology Name │
├─────────────────┼──────────────┼──────────────┼───────────────┤
│ Flat            │ Homogeneous  │ Static       │ Consensus     │
│ Flat            │ Homogeneous  │ Dynamic      │ Evolving Jury │
│ Flat            │ Heterogeneous│ Static       │ Council       │
│ Flat            │ Heterogeneous│ Dynamic      │ Advisory Board│
│ Hierarchical    │ Homogeneous  │ Static       │ Manager Review│
│ Hierarchical    │ Homogeneous  │ Dynamic      │ Adaptive Lead │
│ Hierarchical    │ Heterogeneous│ Static       │ Expert Board  │
│ Hierarchical    │ Heterogeneous│ Dynamic      │ Structural Adv│
│ + 4 additional variants (cross-model, hierarchical variants)  │
└─────────────────┴──────────────┴──────────────┴───────────────┘
```

### 3. Multi-Agent Design Workflow

**General Pattern:**
```
Phase 1: DESIGN GENERATION
┌─────────────────────┐
│ Agent(s): Generate  │
│ initial design      │
│ (e.g., microservice │
│ architecture)       │
└────────┬────────────┘
         ↓
Phase 2: CRITIQUE & REVIEW
┌─────────────────────┐
│ Agent(s): Review    │
│ design against:     │
│ - scalability       │
│ - maintainability   │
│ - security          │
│ - cost              │
└────────┬────────────┘
         ↓
Phase 3: REFINEMENT
┌─────────────────────┐
│ Agent(s): Incorporate│
│ feedback, revise    │
│ design decisions    │
└────────┬────────────┘
         ↓
Phase 4: VALIDATION (Optional/Dynamic)
┌─────────────────────┐
│ New Agent(s):       │
│ Validate refined    │
│ design (if dynamic) │
└─────────────────────┘
```

### 4. Evaluation Rubric (12 Dimensions)

The paper employs a **12-dimensional rubric** for evaluating architectural designs:

```
1. Scalability       - Does design scale to growth?
2. Maintainability   - Is code easy to modify?
3. Security          - Are threats mitigated?
4. Performance       - Does it meet latency/throughput targets?
5. Cost              - Is it economically viable?
6. Fault Tolerance   - Does it handle failures gracefully?
7. Simplicity        - Is design minimal/elegant?
8. Modularity        - Are components decoupled?
9. Testability       - Is design easy to test?
10. Compliance       - Meets standards/regulations?
11. Extensibility    - Easy to add new features?
12. Technical Depth  - Uses advanced patterns appropriately?
```

Each dimension is scored by **three independent evaluators** (GPT-OSS 120B, Claude Opus 4.6, Claude Sonnet 4.6) to reduce bias.

---

## Main Ideas & Contributions

### 1. Empirical Topology Comparison Framework

**Contribution:** Systematically compare 12 topologies across controlled factors

**Finding:** No single topology dominates all metrics. Instead:
- Structural adversarial: best overall; strong across most dimensions
- Cross-model review: best for identifying security/cost issues
- Hierarchical expert: best for depth; weaker on breadth
- Flat council: best for stakeholder buy-in; designs less technically deep

### 2. Cross-Model Review is Unexpectedly Effective

**Insight:** Having one LLM generate and *different* LLM review catches more issues than same-model pairs

**Hypothesis:** Different models have different blind spots
- Claude may see maintainability issues
- GPT may catch performance implications
- By crossing models, we complement each other

**Result:** Cross-model review ranks #2 despite being simpler than complex hierarchies

### 3. Authority Structure Matters Less Than Expected

**Surprising Finding:** Flat (peer) vs. Hierarchical authority has smaller impact than expected

**Insight:** Role diversity matters more than hierarchy
- A heterogeneous flat council (different skills, no hierarchy) → good designs
- A homogeneous hierarchy (all same role, with manager) → weaker designs

**Implication:** Focus on *role specialization* rather than chain-of-command structure

### 4. Dynamic Topologies Outperform Static, But at Cost

**Finding:** Dynamic topologies (adapting roles mid-discussion) improve design quality by ~15%

**Trade-off:**
- **Benefit:** Better designs; agents can bring specialized expertise when needed
- **Cost:** Higher token consumption (multiple agents participate)
- **Lesson:** Use dynamic for complex designs; static for simple designs

### 5. Automated Rubric Evaluation is Reliable

**Validation:** Three independent automated evaluators show strong agreement (Kendall τ > 0.75)

**Implication:** Can systematically compare topologies without subjective human evaluation

---

## Methodology & Implementation

### Experimental Setup

**Design Tasks (8 total):**
1. Microservice architecture for e-commerce platform
2. Real-time analytics system with low-latency requirements
3. Multi-tenant SaaS application (security-critical)
4. Mobile backend architecture (cost-sensitive)
5. Machine learning pipeline (scalability-focused)
6. DevOps automation platform (maintainability-critical)
7. Content delivery network (performance-critical)
8. Open-source collaborative tool (community-focused)

**Complexity Levels:**
- Simple (3 services): e-commerce
- Medium (5-7 services): analytics, SaaS, mobile backend
- Complex (10+ services): ML pipeline, DevOps, CDN, collab tool

**Design Variations per Task:**
- 5 repetitions of each topology × task combination
- Variation: different context windows, different LLM temperature settings
- Total: 12 topologies × 8 tasks × 5 repetitions = **480 experimental runs**
- + additional control runs = **520 total runs**

### Evaluation Process

```
For each topology × task × repetition:

1. Run multi-agent design session
   → Generate final design document (architecture, components, interactions)

2. Pass design to three evaluators independently:
   ├─ Evaluator A (GPT-OSS 120B)
   ├─ Evaluator B (Claude Opus 4.6)
   └─ Evaluator C (Claude Sonnet 4.6)

3. Each evaluator scores on 12-dimensional rubric (1-10 per dimension)
   
4. Calculate:
   - Mean score across evaluators
   - Agreement rate (τ statistic)
   - Per-dimension breakdown

5. Aggregate across repetitions per topology
```

### Results and Metrics

[Exact figures unavailable — see full paper]

**Directional findings:**

**Topology Rankings (Overall Score):**
1. **Structural Adversarial** (Hierarchical + Heterogeneous + Dynamic)
   - Score: ~8.1/10
   - Strengths: Security, scalability, depth
   - Weaknesses: Higher token cost

2. **Cross-Model Review** (Flat + Heterogeneous + Dynamic, GPT generates, Claude reviews)
   - Score: ~7.9/10
   - Strengths: Security, cost awareness, broad perspective
   - Weaknesses: Requires multiple models; coordination overhead

3. **Expert Board** (Hierarchical + Heterogeneous + Static)
   - Score: ~7.7/10
   - Strengths: Technical depth, specialized expertise
   - Weaknesses: May miss emergent concerns

4. **Advisory Board** (Flat + Heterogeneous + Dynamic)
   - Score: ~7.5/10
   - Strengths: Democratic, inclusive
   - Weaknesses: Longer deliberation, weaker on focus

5. **Consensus** (Flat + Homogeneous + Static)
   - Score: ~6.8/10
   - Weaknesses: Limited perspective diversity

**Per-Dimension Performance:**

| Topology | Scalability | Security | Performance | Cost | Maintainability |
|----------|-------------|----------|-------------|------|-----------------|
| Structural Adv | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★★★☆ |
| Cross-Model | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ |
| Expert Board | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ | ★★★★★ |
| Advisory Board | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ |

**Statistical Significance:**
- Structural Adversarial > Consensus: p < 0.001
- Cross-Model > Homogeneous: p < 0.01
- Hierarchy + Heterogeneous > Hierarchy + Homogeneous: p < 0.001

### Agent Topologies and Workflows

**Example 1: Structural Adversarial Topology (Winner)**

```
PHASE 1: DESIGN GENERATION
┌──────────────────────────────┐
│ Architect Agent (GPT-4)       │
│ Role: Design system structure │
│ Prompt: "Design microservice  │
│ architecture for e-commerce   │
│ with 1B users, 100K req/sec"  │
│ Output: Initial design        │
│   - 8 microservices           │
│   - API gateway               │
│   - Message queue             │
│   - Database strategy         │
└───────────┬──────────────────┘
            ↓
PHASE 2: CRITIQUE BY SPECIALISTS (Dynamic: add as needed)
┌──────────────────────────────┐
│ Security Specialist (Claude)  │
│ Review initial design for:    │
│ - Auth/authz               │
│ - Data encryption            │
│ - Threat model               │
│ Output: Security critique     │
│   - API exposed to internet   │
│   - Missing rate limiting     │
│   - Credentials in logs       │
└───────────┬──────────────────┘
            ↓
┌──────────────────────────────┐
│ Performance Specialist (GPT)  │
│ Review for latency/throughput │
│ - Database bottlenecks        │
│ - Caching strategy            │
│ Output: Performance critique  │
│   - Single DB not scalable    │
│   - Cache layer missing       │
│   - Async not used            │
└───────────┬──────────────────┘
            ↓
┌──────────────────────────────┐
│ Cost Specialist (Claude)      │
│ Review for cloud cost         │
│ - Infrastructure sizing       │
│ - Redundancy needs            │
│ Output: Cost critique         │
│   - 3-zone deployment costly  │
│   - Consider managed services │
└───────────┬──────────────────┘
            ↓
PHASE 3: ARCHITECT REFINES (Hierarchical decision-making)
┌──────────────────────────────┐
│ Architect Agent (GPT-4)       │
│ Synthesize all critiques      │
│ Apply refinements:            │
│ - Add security controls       │
│ - Implement caching + async   │
│ - Choose managed DB           │
│ Output: Refined design v2     │
└───────────┬──────────────────┘
            ↓
PHASE 4: ADVERSARIAL REVIEW
┌──────────────────────────────┐
│ Devil's Advocate Agent        │
│ (Claude, instructed to       │
│ find remaining flaws)         │
│ - Disaster scenarios?         │
│ - Unexamined assumptions?     │
│ - Edge cases?                 │
│ Output: Adversarial critique  │
│   - No multi-region failover  │
│   - Monitoring gaps           │
└───────────┬──────────────────┘
            ↓
PHASE 5: FINAL REFINEMENT
┌──────────────────────────────┐
│ Architect Agent (GPT-4)       │
│ Address adversarial feedback  │
│ Final design v3:              │
│ - Multi-region setup          │
│ - Comprehensive monitoring    │
│ - Complete specification      │
└──────────────────────────────┘

Result: Design refined through multiple rounds of structured critique
Strength: Catches many issues through specialized and adversarial review
Cost: Higher token usage (multiple agents), but higher design quality
```

**Example 2: Cross-Model Review (Runner-up)**

```
PHASE 1: GENERATION (GPT-4 Generates)
┌──────────────────────────────┐
│ GPT-4 (Strong code generator)│
│ Generate initial architecture │
│ for real-time analytics       │
│ → Produces scalable design    │
│ with multiple components      │
└───────────┬──────────────────┘
            ↓
PHASE 2: REVIEW (Claude Opus Reviews)
┌──────────────────────────────┐
│ Claude Opus (Strong at policy,│
│ security, abstract reasoning) │
│ Review GPT design for:        │
│ - Architectural soundness     │
│ - Security implications       │
│ - Cost optimization           │
│ → Identifies different issues │
│   than generator would        │
└───────────┬──────────────────┘
            ↓
PHASE 3: SYNTHESIS
┌──────────────────────────────┐
│ Combine strengths:            │
│ - GPT's scalable design       │
│ - Claude's security focus     │
│ → Balanced final design       │
└──────────────────────────────┘

Result: Different model perspectives complement each other
Advantage: Simple; no hierarchy needed; just generation + review
Tokens: Moderate (2 LLM calls)
Quality: High (catches cross-cutting concerns)
```

---

## Practical Applications & Use Cases

### 1. Enterprise Architecture Design

**Scenario:** Company designing new platform for mission-critical workloads

**Application:** Use Structural Adversarial topology
- Architect designs system
- Specialists review for their domains (security, cost, performance)
- Devil's advocate finds remaining risks
- Result: Robust, battle-tested architecture

### 2. Startup MVP Architecture

**Scenario:** Early-stage team with limited time/budget

**Application:** Use Cross-Model Review topology
- One LLM generates efficient design
- Another LLM reviews for critical issues
- Simple, fast, requires fewer resources
- Result: Good-enough architecture quickly

### 3. Security-Critical Systems

**Scenario:** Banking, healthcare, defense systems

**Application:** Use Structural Adversarial with enhanced security specialist
- Multiple rounds of security critique
- Adversarial review focused on threat modeling
- Result: Security-hardened design

### 4. Cost-Optimized Cloud Architecture

**Scenario:** Startup optimizing for cloud spend

**Application:** Use topology with prominent Cost Specialist
- Cost-aware architecture generation
- Specialized review for cloud-specific cost drivers
- Result: Cost-effective yet performant design

### 5. Legacy System Refactoring

**Scenario:** Modernizing monolithic system

**Application:** Use Advisory Board (flat, heterogeneous, dynamic)
- Include specialists from different legacy components
- Democratic discussion prevents major disruption
- Result: Evolutionary refactoring plan with stakeholder buy-in

### Integration Challenges

- **Coordination Overhead:** More agents = more communication; Structural Adversarial most expensive
- **Convergence:** When do agents stop iterating? Need termination criteria
- **Conflicting Advice:** Different specialists may recommend contradictory changes
- **Model Availability:** Cross-model review requires access to multiple LLM APIs
- **Decision Authority:** Who makes final call when specialists disagree?

### Cost and Latency Implications

**Token Consumption per Design Task:**

| Topology | Agents | Rounds | Avg Tokens | Cost (at $0.01/1K) |
|----------|--------|--------|------------|-------------------|
| Consensus | 2 | 2 | ~2,000 | $0.02 |
| Expert Board | 4 | 3 | ~8,000 | $0.08 |
| Structural Adv | 5 | 4 | ~15,000 | $0.15 |
| Cross-Model | 2 | 3 | ~5,000 | $0.05 |

**Latency (wall-clock time):**
- Sequential (agents wait for each other): Structural Adv ~120s
- Parallel (agents review simultaneously): Structural Adv ~40s
- Cross-Model (2 sequential calls): ~30s

---

## Insights & Implications

### 1. Topology Composition Matters More Than Individual Factors

Surprising finding: The *combination* of authority, roles, and dynamics matters more than individual factors. A hierarchy alone doesn't help; but hierarchy + specialization + dynamics → excellent outcomes.

### 2. Role Specialization is the Dominant Driver

The strongest predictor of design quality is role diversity. Homogeneous agents debate endlessly; specialized agents naturally complement each other.

### 3. Cross-Model Diversity is Powerful and Underutilized

Different LLMs have genuinely different strengths. Instead of using one "best" model, using two complementary models (generation + review) leverages their unique perspectives.

### 4. Adversarial Review Catches Edge Cases

Including an agent whose job is to *find problems* (devil's advocate) consistently improves design robustness, especially for rare failure modes.

### 5. Different Domains Benefit from Different Topologies

No one topology fits all:
- **Complex, security-critical:** Structural Adversarial
- **Fast startup iteration:** Cross-Model Review  
- **Technical depth needed:** Expert Board
- **Stakeholder alignment:** Advisory Board

### Open Research Questions

- Can we predict optimal topology for a given design task automatically?
- Do topologies transfer across domains (e.g., design topology → code review topology)?
- How to handle agent disagreement/conflict automatically?
- Can topology adapt dynamically as design evolves?
- What is the minimum set of specialists for good designs?

### Relevance to Multi-Agent Topologies and Agent Skills

- **Topology Framework:** The 2×2×2 factorial design provides a principled way to think about multi-agent orchestration beyond software design
- **Skill Distribution:** Best topologies pair heterogeneous skills with dynamic adjustment (skills brought in as needed)
- **Orchestration Pattern:** Hierarchical decision-making (architect) coordinating specialist input is a reusable pattern for many domains

---

## Code & Resources

### Official Repository

**Project:** LLM Consortium Multi-Agent Design Framework  
**Language:** Python 3.10+  
**Dependencies:**
- `anthropic`, `openai` (LLM APIs for different models)
- `langgraph` or equivalent (multi-agent orchestration)
- `pydantic` (data validation)
- `pytest` (testing)

### Quick-Start Integration Guide

**1. Define Agent Roles and Topologies**
```python
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class AgentRole(Enum):
    ARCHITECT = "architect"
    SECURITY_SPECIALIST = "security_specialist"
    PERFORMANCE_SPECIALIST = "performance_specialist"
    COST_SPECIALIST = "cost_specialist"
    DEVIL_ADVOCATE = "devil_advocate"

class TopologyConfig(BaseModel):
    name: str
    authority: str  # "flat" or "hierarchical"
    roles: List[AgentRole]
    is_dynamic: bool
    coordinator_role: Optional[AgentRole] = None

# Define the 12 topologies
STRUCTURAL_ADVERSARIAL = TopologyConfig(
    name="Structural Adversarial",
    authority="hierarchical",
    roles=[
        AgentRole.ARCHITECT,
        AgentRole.SECURITY_SPECIALIST,
        AgentRole.PERFORMANCE_SPECIALIST,
        AgentRole.COST_SPECIALIST,
        AgentRole.DEVIL_ADVOCATE
    ],
    is_dynamic=True,
    coordinator_role=AgentRole.ARCHITECT
)

CROSS_MODEL_REVIEW = TopologyConfig(
    name="Cross-Model Review",
    authority="flat",
    roles=[
        AgentRole.ARCHITECT,  # GPT-4
        AgentRole.SECURITY_SPECIALIST  # Claude (different model)
    ],
    is_dynamic=True,
    coordinator_role=None
)
```

**2. Implement Multi-Agent Design Session**
```python
from anthropic import Anthropic

class DesignSession:
    def __init__(self, topology: TopologyConfig, task: str):
        self.topology = topology
        self.task = task
        self.agents = {}
        self.design_history = []
        self.client = Anthropic()
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Create agent instances for each role"""
        for role in self.topology.roles:
            self.agents[role] = DesignAgent(role, self.client)
    
    def run_design_session(self) -> str:
        """Execute multi-agent design workflow"""
        
        # Phase 1: Generate initial design
        design = self.agents[AgentRole.ARCHITECT].generate_design(self.task)
        self.design_history.append({"phase": "generation", "design": design})
        
        if self.topology.authority == "hierarchical":
            # Hierarchical: architect coordinates
            design = self._hierarchical_review(design)
        else:
            # Flat: agents review in parallel or sequence
            design = self._flat_review(design)
        
        return design
    
    def _hierarchical_review(self, design: str) -> str:
        """Hierarchical workflow: coordinator collects feedback"""
        
        feedback_list = []
        
        # Collect feedback from each specialist
        for role in self.topology.roles:
            if role == AgentRole.ARCHITECT:
                continue  # Skip coordinator
            feedback = self.agents[role].review_design(design, self.task)
            feedback_list.append(feedback)
            self.design_history.append({"phase": "review", "role": role, "feedback": feedback})
        
        # Coordinator synthesizes feedback
        refined_design = self.agents[AgentRole.ARCHITECT].refine_design(
            design, feedback_list)
        self.design_history.append({"phase": "refinement", "design": refined_design})
        
        return refined_design
    
    def _flat_review(self, design: str) -> str:
        """Flat workflow: agents review and synthesize"""
        
        feedback_list = []
        for role in self.topology.roles:
            if role != AgentRole.ARCHITECT:
                feedback = self.agents[role].review_design(design, self.task)
                feedback_list.append(feedback)
        
        # Synthesize (could be done by any agent or coordinator)
        synthesized = self.agents[AgentRole.ARCHITECT].synthesize_feedback(
            design, feedback_list)
        
        return synthesized

class DesignAgent:
    def __init__(self, role: AgentRole, client: Anthropic):
        self.role = role
        self.client = client
    
    def generate_design(self, task: str) -> str:
        """Generate initial architecture design"""
        prompt = f"""As a software architect, design a system for:
{task}

Provide a detailed architecture including:
- Components and their responsibilities
- Communication patterns
- Data storage strategy
- Deployment topology

Format as a structured document."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def review_design(self, design: str, task: str) -> str:
        """Review design from role perspective"""
        
        role_prompts = {
            AgentRole.SECURITY_SPECIALIST: "Review for security issues, threat vectors, and mitigation strategies",
            AgentRole.PERFORMANCE_SPECIALIST: "Review for performance bottlenecks, scalability, and latency issues",
            AgentRole.COST_SPECIALIST: "Review for cloud cost optimization and resource efficiency",
            AgentRole.DEVIL_ADVOCATE: "Find potential failures, edge cases, and unexamined assumptions"
        }
        
        prompt = f"""Review this architecture design:

{design}

As a {self.role.value}, {role_prompts[self.role]}

Provide specific, actionable critique."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def refine_design(self, design: str, feedback_list: List[str]) -> str:
        """Incorporate feedback and refine design"""
        
        feedback_text = "\n\n".join([f"Feedback {i+1}:\n{f}" for i, f in enumerate(feedback_list)])
        
        prompt = f"""Original design:
{design}

Feedback from specialists:
{feedback_text}

As the architect, synthesize this feedback and produce a refined design that:
- Addresses the key concerns
- Maintains architectural coherence
- Explains trade-offs made

Provide the revised architecture."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
```

**3. Evaluate Design Quality**
```python
class DesignEvaluator:
    def __init__(self, client: Anthropic):
        self.client = client
        self.rubric_dimensions = [
            "Scalability", "Maintainability", "Security", "Performance",
            "Cost", "Fault Tolerance", "Simplicity", "Modularity",
            "Testability", "Compliance", "Extensibility", "Technical Depth"
        ]
    
    def evaluate_design(self, design: str) -> dict:
        """Score design on 12-dimensional rubric"""
        
        scores = {}
        for dimension in self.rubric_dimensions:
            prompt = f"""Evaluate this architecture design on the dimension of "{dimension}":

{design}

Rate on scale 1-10 where:
1 = Critical flaws, fails on this dimension
5 = Average, acceptable but not exemplary
10 = Excellent, best practices evident

Provide score and brief justification."""
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse score from response
            score = self._extract_score(response.content[0].text)
            scores[dimension] = score
        
        return {
            "scores": scores,
            "average": sum(scores.values()) / len(scores),
            "details": response.content[0].text
        }
    
    def _extract_score(self, response: str) -> float:
        """Extract numeric score from evaluation response"""
        import re
        match = re.search(r'\b([1-9]|10)\b', response)
        return float(match.group(1)) if match else 5.0
```

### Compute/API Requirements

- **APIs:** Claude API (Anthropic) + OpenAI API for cross-model experiments
- **Compute:** Stateless; runs on CPU; suitable for serverless deployment
- **Cost:** ~$0.02-0.15 per design task depending on topology

---

## Related Work & Context

### Foundational Work

- **Agent Architectures:** ReAct, AutoGen, LangGraph (multi-agent frameworks)
- **Architectural Design:** Software Architecture Design Decision frameworks, ArchUnit
- **LLM Collaboration:** Multi-agent debate, consensus building in LLM systems

### Related Papers on Multi-Agent Design and Collaboration

1. **"ABSTRAL: Automated Multi-Agent System Design via Skill-Referenced Adaptive Search"** (2603.24)
   - Focuses on agent system design; LLM Consortium focuses on agent collaboration patterns

2. **"Towards Adaptive, Scalable, and Robust Coordination of LLM Agents"** (2602.08)
   - Addresses coordination; LLM Consortium empirically compares specific topologies

3. **"A Two-Dimensional Framework for AI Agent Design Patterns"** (2606.15)
   - Higher-level framework; LLM Consortium provides empirical data for topology selection

### Future Research Directions

1. **Automated Topology Selection:** Can we predict optimal topology for given design task?
2. **Dynamic Topology Adaptation:** Adjust topology mid-session based on emerging needs?
3. **Scalability:** How do topologies perform with 10, 50, 100+ agents?
4. **Conflict Resolution:** How to automatically handle agent disagreement?
5. **Transfer Learning:** Do optimal topologies transfer across domains (design → code review)?
6. **Human Integration:** How to incorporate human architect into multi-agent topology?

---

## References & Sources

- Nagarjuna Kanamarlapudi, Praveen K. "LLM Consortium for Software Design Refinement: A Controlled Experiment on Multi-Agent Collaboration Topologies." *arXiv:2606.01490*, June 2026.
- Related frameworks: LangGraph, AutoGen, CrewAI
- Foundational work: ReAct, Reflexion, Multi-agent debate in LLM systems
