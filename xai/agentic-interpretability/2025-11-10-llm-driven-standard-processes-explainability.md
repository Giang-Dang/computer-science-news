# Increasing AI Explainability by LLM Driven Standard Processes

**Paper ID:** arXiv:2511.07083  
**Submitted:** November 10, 2025  
**Authors:** Marc Jansen, Marcel Pehlke  
**Institution:** Computer Science Institute, University of Applied Sciences Ruhr West, Bottrop, Germany

---

## Executive Summary

This paper introduces a novel paradigm for explainable AI that embeds Large Language Models within standardized analytical decision-making frameworks—specifically Question-Option-Criteria (QOC), Sensitivity Analysis, Game Theory, and Risk Management. Rather than relying on post-hoc explanation methods that attempt to interpret opaque neural network decisions, this approach makes AI systems explainable by design: LLMs execute well-established, human-understandable analytical processes whose reasoning pathways remain transparent and auditable throughout. Empirical evaluation on real-world logistics case studies demonstrates that LLMs can reproduce human-level decision logic while maintaining interpretability, offering a promising alternative to black-box AI systems.

---

## Problem Statement

The field of explainable AI faces a fundamental tension: sophisticated AI systems like large language models demonstrate impressive capabilities but remain largely opaque in their decision-making processes. Traditional XAI approaches attempt to retrofit explainability through post-hoc methods:

- **Feature attribution methods** (LIME, SHAP) provide local explanations but sacrifice model fidelity
- **Attention visualization** offers windows into model computation but doesn't guarantee interpretability
- **Mechanistic interpretability** aims to reverse-engineer neural computations but remains labor-intensive and model-specific
- **Concept-based methods** introduce human-interpretable concepts but add layers of indirection

**Core limitation:** All these approaches treat explainability as a secondary concern, attempting to extract explanations from systems designed for pure performance rather than interpretability.

**A different perspective:** What if we designed AI systems around interpretability from the ground up? Instead of asking "how can we explain this black-box model?", we ask "how can we harness LLM capabilities to execute inherently transparent reasoning processes?"

**Specific challenges addressed:**

1. **Trustworthiness gap:** Even with post-hoc explanations, users cannot fully trust AI systems if the reasoning process itself is opaque
2. **Auditability requirements:** Regulated domains (finance, healthcare, legal) require decision traces that can be audited and verified
3. **Human alignment:** LLMs often make decisions users struggle to understand; structured processes could improve human-AI cognitive alignment
4. **Scalability of human understanding:** Post-hoc explanation methods don't scale well to high-stakes decisions where human understanding is critical

---

## Core Concepts & Theory

### Explainability Through Structured Processes

The paper's core insight is that **explainability emerges from structure, not from post-processing**. By embedding LLMs within well-established analytical frameworks, the paper creates systems that are inherently explainable because their reasoning follows transparent, human-understandable processes.

#### Key Analytical Frameworks

**1. Question-Option-Criteria (QOC) Framework**
- A decision analysis method where options are evaluated against explicit criteria
- Each criterion receives an explicit score or assessment
- The reasoning becomes transparent through the systematic evaluation of each option-criterion pair
- Unlike black-box ranking, QOC produces a human-verifiable decision trace

**2. Sensitivity Analysis (Vester's Sensitivity Model)**
- Identifies systemic factors and their interactions
- Maps factor relationships using signed impact matrices: `+` (positive influence), `-` (negative influence), `0` (no influence)
- Categorizes factors by their systemic roles:
  - **Active factors:** High influence on the system
  - **Passive factors:** Influenced but exert little influence
  - **Critical factors:** High influence and high sensitivity
  - **Buffering factors:** Stabilizing the system
- Creates feedback loops explicitly, making causal relationships transparent
- Enables "what-if" analysis by adjusting factor impacts

**3. Game Theory (Normal and Sequential Forms)**
- **Normal-form games:** Model strategic interactions with payoff matrices
  - Agents simultaneously choose strategies
  - Equilibria can be computed (Nash equilibria, dominant strategies)
  - Reasoning is transparent: "Agent A chose strategy X because it maximizes payoff given Agent B's expected response"
- **Sequential games:** Model dynamic decision-making with explicit trees
  - Decisions are made in sequence
  - Backward induction determines optimal strategies
  - Decision trees remain visible, making the reasoning auditable

**4. Risk Management Frameworks**
- Systematic identification of risks and mitigation strategies
- Risk assessment using explicit criteria (likelihood, impact)
- Mitigation strategies linked to specific risks
- Reasoning becomes transparent: "We mitigate risk X through strategy Y because..."

### Layered Architecture: Separating Reasoning from Process

The paper proposes a layered architecture that separates:

**Layer 1: Opaque Reasoning Space**
- The LLM's internal computations remain opaque
- LLM processes information, generates assessments, suggests options

**Layer 2: Explainable Process Space**
- Standardized frameworks structure the LLM's output
- Reasoning is routed through transparent analytical processes
- Each step remains auditable and human-verifiable

**Key advantage:** This separation allows leveraging LLM capabilities (language understanding, reasoning, creativity) while constraining the final decision-making to transparent processes. The LLM's "reasoning" feeds into human-understandable frameworks rather than directly determining outcomes.

### Swappable Modular Architecture

The paper emphasizes modularity:
- Each analytical framework (QOC, sensitivity analysis, game theory, risk management) can be instantiated independently
- Components are swappable: different frameworks can be combined for different problem types
- Enables customization for domain-specific needs without sacrificing explainability

---

## Main Ideas & Key Contributions

### 1. Process-First Explainability Paradigm

**Core contribution:** The paper argues for inverting the typical XAI approach. Instead of:
```
Opaque Model → Post-Hoc Explanation
```

Propose:
```
LLM Reasoning → Structured Process → Transparent Decision
```

This paradigm shift has profound implications:
- **Explainability is inherent:** Not an afterthought or approximation
- **Reasoning is traceable:** Each step follows known, human-understandable logic
- **Auditability is built-in:** No need for interpretation; the process itself is transparent

### 2. Integration of LLMs with Decision Frameworks

**Technical innovation:** The paper demonstrates how to integrate LLM capabilities (language understanding, reasoning, information synthesis) with formal decision-making frameworks (QOC, game theory, etc.).

**Key integration points:**
- LLM generates options to be evaluated in QOC framework
- LLM assesses factor impacts for sensitivity analysis
- LLM strategizes in game-theoretic models
- LLM identifies and evaluates risks in risk management

**Advantage:** Leverages LLM strengths (natural language, creative reasoning) while using formal frameworks to constrain and structure the final decision.

### 3. Vester Sensitivity Model Implementation

**Specific contribution:** Detailed implementation of Vester's Sensitivity Model with LLM reasoning:
- LLM identifies factors relevant to the decision problem
- LLM assesses impact relationships (signed matrix: -1, 0, +1)
- Algorithms compute systemic roles (active, passive, critical, buffering)
- Feedback loops are explicitly identified and visualized

**Evaluation results:**
- Mean factor alignment with human baseline: 55.5% over 26 factors
- Improved alignment on core factors: 62.9% on transport-core subset
- Role agreement: 57% on role classification
- LLM judge evaluation: scoring against 8-criterion rubric (max score 100)

### 4. Game-Theoretic Decision Making

The paper applies both normal-form and sequential game theory:

**Normal-form games:** Model strategic interactions between agents
- LLMs assign payoffs based on decision criteria
- Equilibria computation provides justifiable decisions
- Agents' strategies are transparent: each agent's choice is explained by payoff maximization

**Sequential games:** Model dynamic, multi-stage decision processes
- LLMs reason about future outcomes at each decision node
- Backward induction provides optimal strategies
- Decision trees remain visible and auditable

### 5. Real-World Validation: Logistics Case Study

**Empirical evaluation on real-world logistics problem** (100 runs):
- **Setup:** Multi-factor system with 26 factors affecting logistics operations
- **Comparison:** LLM-driven decisions vs. human expert baseline
- **Metrics:**
  - Factor identification and alignment: 55.5% mean agreement
  - Core factor alignment: 62.9% (improved over non-core factors)
  - Systemic role agreement: 57%
  - Overall decision quality: evaluated by LLM judge on 8-criterion rubric

**Key finding:** LLMs can reproduce human-level decision logic while maintaining full transparency of the reasoning process.

### 6. Auditability and Compliance

**Practical contribution:** The paper addresses compliance and auditability needs:
- Every decision step remains explicitly logged
- The reasoning pathway is traceable from inputs through decision process to outputs
- This enables:
  - Post-hoc verification of decisions
  - Compliance audits (GDPR right to explanation, AI Act requirements)
  - Root cause analysis of decisions
  - Correction of individual decisions without retraining

---

## Methodology & Implementation

### System Architecture

**Components:**
1. **Problem formulation module:** Converts domain-specific problems into framework-appropriate representations
2. **LLM reasoning module:** Executes reasoning within each framework
3. **Framework instantiation module:** Implements specific analytical frameworks (QOC, sensitivity analysis, game theory, risk management)
4. **Decision module:** Computes final decisions based on framework outputs
5. **Audit trail module:** Logs all reasoning steps for transparency

### Vester Sensitivity Model Implementation

**Step-by-step process:**

1. **Factor Identification:**
   - LLM identifies factors affecting the system (e.g., "transportation cost", "delivery time", "weather patterns")
   - Factors represent variables that can influence outcomes

2. **Impact Matrix Construction:**
   - LLM assesses how each factor influences every other factor
   - Creates signed matrix: +1 (positive influence), -1 (negative influence), 0 (no direct influence)
   - Matrix dimensions: number of factors × number of factors

3. **Systemic Role Computation:**
   - **Activity index:** Sum of positive influences a factor exerts
   - **Passivity index:** Sum of influences a factor receives
   - Classification into roles:
     - Active: High activity, low passivity (drivers)
     - Passive: Low activity, high passivity (consequences)
     - Critical: High activity and high passivity (critical nodes)
     - Buffering: Low activity and low passivity (stabilizers)

4. **Feedback Loop Identification:**
   - Algorithms detect feedback cycles in the impact matrix
   - Explicit representation: "Factor A → Factor B → Factor A"

### Game-Theoretic Implementation

**Normal-form games:**
```
Payoff Matrix Construction:
- LLM identifies agents and their strategies
- LLM assigns payoffs based on decision criteria
- Equilibrium computation (Nash equilibrium, dominant strategies)
- Strategy selection based on equilibrium analysis
```

**Sequential games:**
```
Game Tree Construction:
- Nodes represent decision points
- Edges represent actions/choices
- Payoffs assigned at terminal nodes
- Backward induction: optimal strategy at each node
- Decision path made explicit
```

### Evaluation Methodology

**Real-world logistics case study:**
- Problem: Multi-factor logistics network optimization
- 26 interdependent factors
- 100 simulation runs
- Comparison metric: Alignment with human expert decisions

**Evaluation metrics:**

1. **Factor Alignment:** Percentage of factors identified by LLM matching expert identification
   - Result: 55.5% mean agreement
   - Subset result: 62.9% on transport-core factors

2. **Role Agreement:** Percentage of factors assigned correct systemic roles
   - Result: 57% agreement

3. **Decision Quality:** LLM-based judge scores decisions on rubric
   - Rubric: 8 criteria for decision quality
   - Scale: 0-100

4. **Human Evaluation:** [Exact figures unavailable — see full paper]
   - Whether human experts found LLM-driven decisions understandable
   - Whether decision reasoning was auditable

### Limitations

1. **Scalability:** Sensitivity analysis works well for ~20-30 factors; scaling to hundreds of factors may become challenging
2. **Framework selection:** Choosing appropriate framework for different problem types requires domain expertise
3. **Factor identification:** Reliance on LLM's factor identification may miss domain-specific factors
4. **Factor relationships:** Simple signed relationships (-1, 0, +1) may oversimplify complex interactions
5. **Evaluation scope:** Real-world evaluation on single domain (logistics); generalization to other domains needs validation

---

## Practical Applications & Real-World Use Cases

### 1. Supply Chain and Logistics

**Application:** Network optimization, route planning, inventory management

**Example:** A logistics company needs to optimize its delivery network considering:
- Transportation costs
- Delivery times
- Vehicle capacity
- Weather patterns
- Driver availability
- Customer demand patterns

**How the approach works:**
- Sensitivity analysis identifies which factors most influence delivery performance
- Game theory models strategic interactions between warehouses, drivers, and customer demands
- QOC framework evaluates different routing options against explicit criteria
- Decision remains fully auditable: "We chose route X because the sensitivity analysis showed Y factors are critical, and X optimizes these"

**Benefit:** Decision-makers understand the reasoning; if assumptions change, the decision framework can be quickly adapted

### 2. Healthcare and Clinical Decision Support

**Application:** Treatment planning, resource allocation, patient triage

**Example:** A hospital needs to allocate limited ICU beds considering:
- Patient severity
- Treatment prognosis
- Resource availability
- Staff expertise
- Ethical constraints

**How the approach works:**
- QOC framework scores each patient against allocation criteria
- Sensitivity analysis identifies which factors most influence patient outcomes
- Risk management framework identifies potential complications
- Decision reasoning is completely transparent: "Patient A received the bed because their criteria score is highest and sensitivity analysis shows patient severity is the critical factor"

**Benefit:** 
- Clinicians can verify decisions align with medical guidelines
- Patients/families can understand allocation rationale
- Regulators can audit compliance

### 3. Financial Services and Credit Decisions

**Application:** Loan approval, credit scoring, investment decisions

**Example:** A bank needs to approve/deny loan applications considering:
- Applicant creditworthiness
- Income stability
- Loan-to-value ratio
- Market conditions
- Regulatory capital requirements

**How the approach works:**
- QOC framework evaluates each application against defined criteria
- Sensitivity analysis identifies which factors most influence default risk
- Game theory models strategic responses to interest rate changes
- Applicants receive fully transparent decisions: "Your application was denied because criteria X, Y, Z were not met, and sensitivity analysis shows these factors determine creditworthiness"

**Benefit:**
- Compliance with fair lending regulations (ability to explain decisions)
- Applicant recourse (can address specific failing criteria)
- Reduced regulatory risk

### 4. Legal and Regulatory Compliance

**Application:** Compliance monitoring, risk assessment, audit

**Example:** An organization needs to assess regulatory compliance considering:
- Regulatory requirements
- Organizational capabilities
- Risk severity
- Remediation costs
- Timeline constraints

**How the approach works:**
- Risk management framework identifies compliance gaps
- Sensitivity analysis determines which requirements are critical
- QOC framework evaluates remediation options
- Compliance decisions are fully auditable: "We prioritized remediation of risk X because sensitivity analysis shows it affects Y regulatory areas"

**Benefit:**
- Audit trails for regulators
- Clear prioritization of compliance efforts
- Evidence of reasonable decision-making

### 5. Autonomous Systems and Robotics

**Application:** Task planning, resource allocation, safety verification

**Example:** An autonomous robot needs to plan tasks considering:
- Task priority
- Resource availability
- Safety constraints
- Time windows
- Power/energy limits

**How the approach works:**
- Game theory models interactions between concurrent tasks
- Sensitivity analysis identifies safety-critical factors
- Sequential game tree structures task scheduling
- Safety engineers can verify decisions: "The robot prioritized safety check X over task Y because sensitivity analysis shows safety factors are critical"

**Benefit:**
- Safety verification is built into decision reasoning
- Engineers can understand and approve robot decisions
- Failure analysis is easier when reasoning is transparent

### 6. Emergency Management and Disaster Response

**Application:** Resource allocation, evacuation planning, incident command

**Example:** Emergency management needs to coordinate response considering:
- Incident severity
- Resource availability
- Population at risk
- Weather conditions
- Evacuation routes

**How the approach works:**
- Sensitivity analysis identifies critical factors affecting safety
- QOC framework evaluates resource allocation options
- Game theory models coordination between agencies
- Incident commanders receive fully transparent recommendations: "We prioritized evacuation from zone A because sensitivity analysis shows wind patterns and population density are critical factors"

**Benefit:**
- Rapid decision-making with full transparency
- Coordination between agencies based on shared reasoning
- Post-incident analysis is straightforward

### Implementation Challenges

1. **Framework selection expertise:** Selecting appropriate frameworks requires domain knowledge
2. **Factor identification:** Ensuring LLMs identify all relevant domain factors
3. **Relationship modeling:** Accurately capturing complex causal relationships
4. **Validation overhead:** Requires expert validation of framework setup and results
5. **Domain adaptation:** Frameworks may need customization for different domains

---

## Insights & Implications

### Paradigm Shift in Explainable AI

This paper proposes a fundamental rethinking of how to achieve explainability:

**Traditional approach:** Make black-box models explainable through post-hoc methods
- Advantages: Can apply to existing powerful models
- Disadvantages: Explanations are approximate; trust remains fragile

**Proposed approach:** Design systems around explainability from the start
- Advantages: Explainability is inherent, not approximated; reasoning is truly transparent
- Disadvantages: May sacrifice some model flexibility; requires upfront framework selection

### The Value of Structured Reasoning

The paper demonstrates that structure is a key to explainability. By constraining LLM reasoning to follow well-established decision frameworks:
- Outputs become verifiable
- Reasoning becomes auditable
- Decisions can be understood by domain experts
- Systems can be debugged and improved systematically

### Human-AI Cognitive Alignment

A key insight: When AI systems reason through human-understandable processes, users can:
- Follow the reasoning
- Verify it makes sense
- Catch errors
- Suggest improvements
- Build appropriate trust (not blind trust, but informed trust)

This contrasts with attention heatmaps or LIME explanations that humans struggle to connect to their own reasoning.

### Scalability of Transparent AI

Traditional XAI methods don't scale well:
- Computing SHAP values becomes expensive for large models
- Attention visualization becomes unintelligible with many attention heads
- Mechanistic interpretability is labor-intensive

This approach offers better scalability:
- Structured reasoning is inherently scalable
- Frameworks can be instantiated quickly
- Transparency is maintained regardless of model size

### Limitations and Open Questions

1. **Expressiveness vs. Transparency Trade-off:** Do structured frameworks limit what problems can be solved effectively?

2. **Framework Selection:** How do we systematically select appropriate frameworks for new problem domains?

3. **Human Understanding:** Are users actually better able to understand and act on structured reasoning compared to post-hoc explanations? (Requires human studies)

4. **Complex Relationships:** Can signed impact matrices (-1, 0, +1) adequately represent real-world complexity?

5. **Automation vs. Human Oversight:** How much of the framework instantiation and interpretation should be automated vs. human-guided?

### Future Research Directions

1. **Extended Frameworks:** Applying structured reasoning to more domains (healthcare, legal, finance)

2. **Hybrid Approaches:** Combining structured reasoning with LLM capabilities (e.g., using LLM to generate candidates that QOC framework evaluates)

3. **Comparative Studies:** Head-to-head evaluation: structured reasoning vs. post-hoc explanations in terms of human understanding

4. **Learning Frameworks:** Can systems learn optimal frameworks for specific domains?

5. **Verification and Validation:** How to systematically verify that structured reasoning is correct and complete?

6. **Integration with Existing Systems:** Applying structured reasoning to explain decisions from existing black-box models

---

## Code & Resources

### Accessing the Paper

- **arXiv Webpage:** [Increasing AI Explainability by LLM Driven Standard Processes](https://arxiv.org/abs/2511.07083)
- **HTML Version:** https://arxiv.org/html/2511.07083
- **PDF Version:** https://arxiv.org/pdf/2511.07083

### Related Paper by Same Authors

- **2511.07086:** "LLM Driven Processes to Foster Explainable AI" (same authors, closely related)

### Framework References

**Vester's Sensitivity Model:**
- Classic systems analysis framework for factor impact analysis
- Useful for understanding complex systems with many interdependent factors
- Publicly documented methodology

**Game Theory Resources:**
- Game theory provides formal framework for modeling strategic interactions
- Nash equilibrium concept for finding stable solutions
- Sequential game trees for dynamic decision-making

**Question-Option-Criteria Framework:**
- Multi-criteria decision analysis (MCDA) method
- Systematic evaluation of options against explicit criteria
- Transparent ranking and justification

### Implementation Guidance

**For implementing LLM-driven structured processes:**

1. **Problem Formulation:**
   - Clearly define decision problem
   - Identify agents/stakeholders
   - Specify decision criteria

2. **Framework Selection:**
   - Choose appropriate analytical framework (QOC, sensitivity analysis, game theory, risk management)
   - May require domain expertise to select
   - Consider combining multiple frameworks

3. **LLM Integration:**
   - Design prompts that ask LLM to identify factors, assess relationships, evaluate options
   - Constrain LLM outputs to fit framework requirements
   - Implement validation of LLM reasoning

4. **Implementation:**
   - Instantiate chosen framework
   - Feed LLM reasoning into framework
   - Compute decisions through framework logic

5. **Evaluation:**
   - Validate decisions against domain expert judgment
   - Measure alignment with known ground truth
   - Gather human feedback on reasoning transparency

### Computational Requirements

The paper does not specify detailed computational requirements, but framework-based reasoning is generally efficient:
- Sensitivity analysis: O(n²) for n factors (matrix-based)
- Game theory: Depends on game size (exponential for very large games)
- QOC: Linear in number of options × criteria
- Not compute-intensive compared to large LLM inference

---

## Related Work & Context

### How This Paper Relates to Other XAI Research

**Relationship to Post-Hoc Explainability:**
- **LIME (Local Interpretable Model-Agnostic Explanations):** Creates local linear approximations
- **SHAP (SHapley Additive exPlanations):** Computes feature attribution based on game theory
- **This paper's approach:** Uses game theory directly for decision-making, not as a post-hoc tool

**Relationship to Mechanistic Interpretability:**
- **Circuit analysis, sparse autoencoders:** Attempt to reverse-engineer model internals
- **Attention visualization:** Shows which inputs influence outputs
- **This paper's approach:** Doesn't try to interpret model internals; constrains reasoning to transparent processes

**Relationship to Inherently Interpretable Models:**
- **Decision trees, linear models, rule-based systems:** Interpretable by design but limited expressiveness
- **This paper's approach:** Combines LLM expressiveness with framework interpretability

### Building on Prior Work

The paper synthesizes research from multiple fields:

1. **Decision Analysis (QOC Framework):**
   - Multi-criteria decision analysis has decades of research
   - QOC is an established framework
   - Paper applies it with LLM reasoning

2. **Systems Thinking (Sensitivity Analysis):**
   - Vester's sensitivity model is from 1999
   - Systemic analysis of complex systems
   - Paper demonstrates LLM effectiveness for factor identification and relationship assessment

3. **Game Theory:**
   - Formal mathematical framework for strategic interaction
   - Nash equilibrium and backward induction are classical concepts
   - Paper shows LLMs can reason within game-theoretic frameworks

4. **Risk Management:**
   - Well-established frameworks for risk identification and mitigation
   - Paper integrates LLM reasoning into risk management processes

### Connections to Agentic AI

This paper relates to the broader field of agentic AI and multi-agent systems:

**Agent Reasoning and Planning:**
- Structured reasoning frameworks provide principled approaches to agent planning
- Game theory naturally models multi-agent interactions
- Decision frameworks help agents justify and explain decisions

**Relationship to LLM Agents:**
- Recent work on LLM agents shows they can follow structured reasoning
- This paper provides frameworks specifically designed for transparency
- Suggests path toward truly explainable agentic AI

**Multi-Agent Collaboration:**
- Game theory and QOC framework naturally support multi-agent coordination
- Each agent's reasoning remains transparent
- Enables collaborative decision-making with full auditability

### XAI Subfields Affected

This paper impacts multiple XAI research communities:

1. **Human-Centered XAI:** Structured reasoning may be more understandable to users
2. **Mechanistic Interpretability:** Alternative to reverse-engineering internal mechanisms
3. **Fairness and Interpretability:** Transparent reasoning can help identify bias
4. **Causal Interpretability:** Game theory and sensitivity analysis naturally model causality
5. **Agentic XAI:** Provides frameworks for explaining agent decisions
6. **Regulatory Compliance:** Structured reasoning may better meet regulatory requirements

### Where This Research Leads

The paper opens several research directions:

1. **Empirical Validation:** Do users actually find structured reasoning more understandable? (Requires human studies)

2. **Domain Extension:** How to apply structured reasoning to other domains?

3. **Hybrid Systems:** Combining structured reasoning with other XAI methods?

4. **Theoretical Analysis:** What formal guarantees can we provide about explanation quality?

5. **Learning Frameworks:** Can systems learn to select and instantiate appropriate frameworks?

6. **Integration with Existing AI:** How to apply structured reasoning to explain decisions from existing black-box models?

---

## Conclusion

"Increasing AI Explainability by LLM Driven Standard Processes" proposes a paradigm shift in how to achieve explainable AI. Rather than trying to explain opaque models post-hoc, the paper demonstrates that by embedding LLM reasoning within well-established analytical frameworks—Question-Option-Criteria, Sensitivity Analysis, Game Theory, and Risk Management—we can create AI systems that are interpretable by design.

The key insight is that **structure enables explainability**. By constraining LLM reasoning to follow transparent decision processes, the system maintains full auditability while leveraging LLM capabilities for reasoning, language understanding, and information synthesis.

Empirical evaluation on real-world logistics problems shows that LLMs can reproduce human-level decision logic while maintaining transparency. This suggests a promising path toward truly explainable AI that doesn't require post-hoc interpretation or rely on approximations—the reasoning itself is transparent.

For practitioners in regulated domains (healthcare, finance, legal, regulatory compliance) where decision transparency is critical, this approach offers a concrete methodology for creating AI systems that are not just powerful but also genuinely understandable.

---

## References

- Jansen, M., & Pehlke, M. (2025). "Increasing AI Explainability by LLM Driven Standard Processes." arXiv preprint arXiv:2511.07083.

**Paper Links:**
- arXiv Page: https://arxiv.org/abs/2511.07083
- PDF: https://arxiv.org/pdf/2511.07083
- HTML: https://arxiv.org/html/2511.07083

**Related Work by Same Authors:**
- arXiv:2511.07086 - "LLM Driven Processes to Foster Explainable AI"

