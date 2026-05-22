# What Do Agents Communicate? Characterizing Information Exchange in Multi-Agent Systems

**ArXiv ID:** 2605.20548  
**Submitted:** May 19, 2026  
**Authors:** Yong Jin Chun, Iftekhar Ahmed  
**Institution:** Department of Informatics, University of California, Irvine

---

## Executive Summary

This paper addresses a critical vulnerability in collaborative multi-agent LLM systems: error propagation through inter-agent communication. Through systematic analysis, the authors identify that agents fail to communicate essential reasoning and verification information, degrading downstream performance. They propose Category-Aware Recovery Augmentation (CARA), which enforces critical information presence in agent communication, improving multi-agent system reliability and performance while maintaining computational efficiency.

---

## Problem Statement

### Current Limitations

Modern multi-agent LLM systems leverage agent collaboration to improve performance through diverse reasoning and iterative refinement. However, these systems suffer from a fundamental information loss problem:

1. **Error Propagation**: Early-stage information degradation cascades through agent chains
2. **Missing Verification**: Agents often fail to communicate verification results and confidence scores
3. **Incomplete Reasoning**: Critical reasoning steps are omitted in inter-agent communication
4. **Information Bottlenecks**: Dense communication often loses nuance and context

### Research Gap

While multi-agent systems show promise for complex reasoning, we lack systematic understanding of:
- What information is most critical for agent-to-agent communication?
- How do communication patterns affect downstream performance?
- Which information loss points create the most damage?
- How can we ensure critical information flows between agents?

### Motivating Observation

Consider a three-agent system:
- **Agent A** (Retriever): Gathers relevant documents
- **Agent B** (Analyzer): Synthesizes information
- **Agent C** (Responder): Generates final answer

If Agent A only communicates "relevant documents found" without their relevance scores or confidence levels, Agent B cannot properly weight information, leading to poor synthesis. Agent C then inherits flawed analysis, compounding the error.

**Key Insight:** Multi-agent performance is not just about individual agent quality but about information flow between agents.

---

## Core Concepts & Theory

### 1. **Multi-Agent Communication Taxonomy**

The paper categorizes information exchanged between agents:

**Information Categories:**

```
Communication Content
├─ Raw Data: Facts, documents, retrieved items
├─ Reasoning Steps: Intermediate conclusions, logic chains
├─ Confidence/Verification: Trust scores, validation results
├─ Constraints: Requirements, limitations discovered
├─ Context: Problem background, execution status
└─ Error Information: Failure modes, alternatives explored
```

### 2. **Error Propagation Mechanisms**

**Cascade Effect:**
```
Agent A Error/Omission
        ↓
Misinterpretation by Agent B
        ↓
Suboptimal synthesis
        ↓
Poor input to Agent C
        ↓
Degraded final output
```

**Information Loss Points:**
1. **Filtering**: Agents discard seemingly irrelevant information
2. **Summarization**: Compression loses nuance
3. **Abstraction**: High-level communication misses details
4. **Selection Bias**: Agents communicate what they think is important, not what recipients need

### 3. **Reasoning Quality in Communication**

Communication quality depends on:

**a) Explicit Reasoning:**
- Showing work and logic chains
- Explaining decision-making process
- Clarifying assumptions

**b) Verification Evidence:**
- Confidence scores
- Supporting evidence strength
- Alternative hypotheses considered
- Uncertainty acknowledgment

**c) Context Preservation:**
- Why certain information was selected
- What alternatives were rejected
- Edge cases and limitations
- Execution constraints encountered

### 4. **Information Criticality Framework**

Not all information has equal importance:

**High-Criticality Information:**
- Primary reasoning conclusions
- Verification success/failure
- Data quality assessments
- Constraint violations

**Medium-Criticality Information:**
- Secondary findings
- Reasoning step details
- Confidence levels
- Complexity assessments

**Low-Criticality Information:**
- Exact document text (if summarized well)
- Intermediate computations
- Process details
- Metadata

### 5. **Multi-Agent System Dynamics**

**Sequential vs. Parallel Processing:**

```
Sequential (Pipeline):
Agent A → (output) → Agent B → (output) → Agent C
- Error amplification with each step
- Cannot recover from early errors
- Total output quality = product of individual qualities

Parallel (Voting/Ensemble):
     ↙ Agent A
Problem ← Agent B (consensus)
     ↘ Agent C
- More robust to individual agent failures
- Can detect and correct errors
- Output quality ≈ maximum of individual qualities (better)
```

**Hierarchical Processing:**
```
         Agent Z (Supervisor)
        /    |    \
    Agent A Agent B Agent C (Specialized)
    
Supervisor coordinates and validates communication,
reduces error propagation through validation layer
```

---

## Main Ideas & Contributions

### 1. **Core Innovation: Systematic Communication Analysis**

The paper provides the first systematic characterization of what information drives multi-agent performance:

**Key Findings:**

1. **Reasoning Presence Matters:**
   - Systems with explicit reasoning in communication: 18% higher accuracy
   - Loss of reasoning steps cascades through agent chain
   - Even informal reasoning sketches help downstream agents

2. **Verification is Critical:**
   - Agents that communicate verification results improve performance by 22%
   - Confidence scores essential for error detection
   - Validation information enables adaptive responses

3. **Redundancy is Beneficial:**
   - Strategic information repetition improves robustness
   - Slight overhead worth the reliability gain
   - ~15% extra tokens, but 20%+ performance improvement

4. **Communication Structure Matters:**
   - Explicit structure outperforms natural language by 12%
   - Consistent formatting reduces misinterpretation
   - Templated communication enables better parsing

### 2. **Technical Contribution: Category-Aware Recovery Augmentation (CARA)**

CARA is a communication protocol that ensures critical information presence:

**Protocol Components:**

```
CARA Communication Structure:

[TASK_CONTEXT]
- Original problem statement
- Constraints and requirements

[PRIMARY_FINDINGS]
- Main conclusions (reasoning + evidence)
- Confidence levels
- Key supporting facts

[VERIFICATION_RESULTS]
- What was verified/validated
- Success/failure indicators
- Uncertainty acknowledgment

[ALTERNATIVES_CONSIDERED]
- Other interpretations
- Paths not taken
- Why primary choice was selected

[CONSTRAINTS_IDENTIFIED]
- Limitations discovered
- Assumptions made
- Edge cases noted

[QUALITY_METRICS]
- Data quality assessment
- Information completeness
- Recommendation confidence
```

**Implementation:**
- Template-based structure guides agent communication
- Enforces presence of critical information categories
- Natural language filled into structured categories
- Downstream agents parse structured information more effectively

### 3. **Design Intuitions**

**Why Structure Helps:**
1. Enforces complete information transmission
2. Reduces ambiguity in interpretation
3. Enables systematic error detection
4. Facilitates multi-agent coordination

**Why Category-Awareness Helps:**
1. Different information types serve different purposes
2. Explicit categorization improves routing and use
3. Makes information provenance clear
4. Enables selective information filtering when needed

**Why Recovery Matters:**
1. Some communication will still fail or be incomplete
2. Recovery mechanisms (fallbacks, re-querying) improve robustness
3. Error detection + recovery > error prevention
4. Real-world systems need graceful degradation

### 4. **Comparison with Baselines**

| Approach | Communication Structure | Information Loss | Robustness | Accuracy |
|----------|------------------------|-----------------|-----------|----------|
| Free-form Natural Language | Unstructured | High | Low | Baseline |
| Templated Communication | Loose structure | Medium | Medium | +8% |
| Dense Summarization | Compressed | Very High | Low | -5% |
| **CARA** | **Structured + Complete** | **Low** | **High** | **+22%** |
| CARA + Verification | Structured + Complete | Very Low | Very High | +25% |

---

## Methodology & Implementation

### 1. **Experimental Setup**

**Multi-Agent System Configurations Tested:**

a) **Three-Agent Sequential Pipeline (Retrieval → Analysis → Response)**
   - Agent A: Document retrieval with keyword matching
   - Agent B: Information synthesis and analysis
   - Agent C: Answer generation and formatting
   - Task: Multi-document question answering (musique, HotpotQA variants)

b) **Multi-Agent Parallel Voting (Ensemble)**
   - Agents A, B, C: Independent reasoning paths
   - Supervisor: Consensus aggregation
   - Task: Fact verification, confidence estimation
   - Dataset: FEVER, natural questions

c) **Hierarchical Multi-Agent Architecture**
   - Specialist agents: Retrieval, analysis, verification
   - Supervisor agent: Orchestration and validation
   - Task: Complex research questions
   - Dataset: Long-form QA, research synthesis

d) **Task Categories Evaluated:**
   - Multi-hop reasoning: Chains of 3-5 inference steps
   - Long-context processing: 50k-100k token inputs
   - Fact verification: Claim validation against sources
   - Synthesis: Combining information from multiple sources
   - Error recovery: Robustness under noise/failures

### 2. **Evaluation Metrics**

**Performance Metrics:**
- **Accuracy**: Exact match and F1 scores
- **Reasoning Quality**: Human evaluation of reasoning clarity
- **Error Propagation Rate**: Percentage of errors traced to communication failures
- **Recovery Rate**: Successfully recovered from bad intermediate results

**Communication Metrics:**
- **Information Completeness**: Coverage of critical information categories
- **Redundancy Level**: Proportion of repeated information
- **Compression Ratio**: Tokens used vs. original information
- **Misinterpretation Rate**: Downstream agent misunderstanding percentage

**System-Level Metrics:**
- **Throughput**: Problems solved per unit time
- **Token Efficiency**: Total tokens for multi-agent reasoning
- **Latency**: End-to-end response time
- **Robustness**: Performance under agent failures/delays

### 3. **Baselines and Comparisons**

**Baseline Systems:**
1. **Single Agent**: Unified model handling entire task
2. **Basic Multi-Agent**: Free-form communication between agents
3. **Supervised Multi-Agent**: Agents trained with communication supervision
4. **Retrieval-Augmented**: RAG pipeline with no structured communication
5. **Standard Ensemble**: Voting without communication protocol

### 4. **Results Summary**

**Key Quantitative Results:**

1. **Communication Content Analysis:**
   - Agents in unstructured systems omit 30-40% of critical information
   - Reasoning steps omitted in 25% of communications
   - Verification results communicated in only 15% of baseline agents
   - CARA enforces 95%+ presence of critical categories

2. **Performance Impact:**
   - Baseline multi-agent vs. single agent: +8% (small gain, high variance)
   - Baseline + CARA: +18% improvement over single agent
   - CARA + error detection: +22% improvement
   - CARA + verification layer: +25% improvement

3. **Error Analysis:**
   - 45% of multi-agent failures traceable to communication gaps
   - Reasoning omission causes 18% accuracy drop
   - Verification absence enables error propagation (15% additional errors)
   - CARA reduces communication-induced errors by 80%

4. **Computational Trade-offs:**
   - Structured communication overhead: 10-15% extra tokens
   - Parsing structured output: <50ms additional latency
   - ROI: 22% accuracy gain for 15% token increase (highly favorable)

5. **Robustness Results:**
   - Baseline: Degrades 30% with agent failures
   - CARA: Degrades only 8% with same failures
   - Better error detection enables automatic fallbacks
   - System continues functioning with graceful degradation

### 5. **Qualitative Findings**

**Agent Communication Patterns:**

**Worst Performing (Baseline):**
```
Agent A → Agent B: "Found relevant documents"
(Missing: Which documents, relevance scores, why selected)

Agent B → Agent C: "Analysis complete"  
(Missing: Key findings, confidence, methodology)

Agent C: Low quality response due to insufficient information
```

**Best Performing (CARA):**
```
Agent A → Agent B:
[PRIMARY_FINDINGS]
- Documents X, Y, Z retrieved (relevance: 0.92, 0.87, 0.81)
- Focus on climate change policy from 2020-2026

[VERIFICATION_RESULTS]
- All sources verified as reputable publications
- Coverage: Comprehensive on policy, moderate on implementation

[CONSTRAINTS_IDENTIFIED]
- Limited recent economic impact analysis
- Recommend supplementary research in economics

Agent B Successfully synthesizes with full context → Agent C generates high-quality response
```

---

## Practical Applications & Use Cases

### 1. **Multi-Agent Research Systems**
- Literature review: Retriever → Analyzer → Synthesizer
- Problem: Many papers missed or wrongly prioritized
- CARA Solution: Structured communication of document relevance and analysis confidence
- Impact: More complete, better-contextualized literature reviews

### 2. **Enterprise Decision Support**
- Multi-department analysis: Finance → Operations → Strategy
- Problem: Departments misunderstand each other's constraints and findings
- CARA Solution: Structured information exchange with explicit constraints and confidence
- Impact: Better decisions reflecting all perspectives

### 3. **Real-Time Monitoring and Response**
- Sensor fusion: Multiple sensors → Data analyzer → Decision maker
- Problem: Critical information lost in data compression
- CARA Solution: Structured sensor data with confidence and quality metrics
- Impact: More reliable automated decisions, fewer false alarms

### 4. **Medical Diagnosis Assistants**
- Multi-specialist consultation: Lab → Imaging → Clinic → Diagnosis
- Problem: Specialists miss context from other specialties
- CARA Solution: Structured sharing of findings, confidence, and limitations
- Impact: More accurate diagnoses, better treatment plans

### 5. **Open-Domain Question Answering**
- Search → Retrieval → Summarization → Answering
- Problem: Noise propagates through pipeline
- CARA Solution: Structured information quality and verification at each stage
- Impact: Higher accuracy, better handling of unanswerable questions

### 6. **Implementation Challenges**

**Technical Challenges:**
1. **Parsing Complexity**: Agents must generate well-formed structured output
2. **Flexibility**: Overly rigid templates limit agent expressiveness
3. **Scalability**: Structured communication overhead grows with agent count
4. **Compatibility**: Existing agents not designed for structured output

**Practical Challenges:**
1. **Training Overhead**: Agents need supervision to follow CARA protocol
2. **Error Handling**: Malformed output can break downstream parsing
3. **Debugging**: Harder to understand agent behavior with structured output
4. **Customization**: Different tasks may need different information categories

---

## Insights & Implications

### 1. **Broader Field Impact**

**Communication as First-Class Concern:**
- Multi-agent systems need explicit attention to communication
- Communication design is as important as agent design
- Structured communication enables more reliable systems

**Information Theory in Practice:**
- Information preservation is more important than compression
- Redundancy (up to 15%) is beneficial, not wasteful
- Context and metadata carry high information density

**Reliability Through Structure:**
- Structured systems more resilient to component failures
- Error detection and recovery possible with good communication
- Transparency in communication enables better debugging

### 2. **State-of-the-Art Advancement**

**Previous SOTA:**
- Ad-hoc multi-agent systems: 50-65% accuracy on complex tasks
- Challenges with information loss and error propagation
- Difficulty in scaling beyond 3-4 agents

**New Insights:**
- 22-25% improvement with proper communication structure
- Scales to larger agent networks with structured protocols
- Enables reliable multi-agent systems for high-stakes applications
- Shows information architecture matters as much as agent capability

### 3. **Limitations and Open Questions**

**Current Limitations:**
1. **Scope**: Tested primarily on text-based reasoning tasks
2. **Scalability**: Not tested with 10+ agent systems
3. **Generalization**: CARA protocol may need adjustment per task type
4. **Overhead**: Structured communication has computational costs

**Open Questions:**

1. **Optimal Communication Structure:**
   - Can we learn communication protocols from data?
   - What is the minimal sufficient structure?
   - How much redundancy is truly necessary?

2. **Scalability:**
   - How does CARA scale to larger agent teams?
   - Communication graph optimization?
   - Compression techniques for large teams?

3. **Adaptation:**
   - Can agents learn to adjust communication style per partner?
   - Dynamic protocol adjustment based on task?
   - Meta-learning of communication strategies?

4. **Robustness:**
   - Adversarial agent communication?
   - Information poisoning resistance?
   - Byzantine-tolerant multi-agent systems?

5. **Generalization:**
   - Transfer of communication protocols across domains?
   - Foundation models for agent communication?
   - Cross-domain communication standards?

---

## Code & Resources

### Official Resources
- **ArXiv Paper**: https://arxiv.org/abs/2605.20548
- **Paper HTML**: https://arxiv.org/html/2605.20548v1

### Expected Implementation Components
Based on the nature of the work:

**Core Components:**
- Multi-agent orchestration framework
- Communication protocol parser/generator
- Information categorization module
- Error detection and recovery mechanism

**Dependencies:**
- LLM inference engine (GPT-4, Claude, Llama, etc.)
- Multi-agent framework (LangChain, AutoGen, CrewAI)
- Knowledge base (vector DB, document store)
- Monitoring/logging infrastructure

### Compute Requirements
- **Inference**: High (multiple agents per task)
  - 3-agent system: ~3x single-agent tokens
  - Overhead manageable for reasoning tasks
  - Latency: 5-15 seconds for complex queries

- **Hardware**: Single GPU usually sufficient
  - VRAM: 20-40GB for 70B+ models
  - CPU: Moderate (agent coordination)
  - Networking: Low bandwidth requirements

### Quick-Start Conceptual Implementation

```pseudocode
function multi_agent_with_CARA(task):
    context = parse_task(task)
    
    # Agent A: Retrieval
    findings_a = retrieve_documents(context)
    message_ab = format_CARA({
        task_context: context,
        primary_findings: findings_a,
        verification_results: verify(findings_a),
        constraints_identified: document_limitations(findings_a)
    })
    
    # Agent B: Analysis
    analysis_b = analyze(message_ab)
    message_bc = format_CARA({
        task_context: context,
        primary_findings: analysis_b,
        verification_results: verify(analysis_b),
        alternatives_considered: alternatives(analysis_b)
    })
    
    # Agent C: Response
    response = generate_response(message_bc)
    return response
```

---

## Related Work & Context

### 1. **Related Recent Papers**

**a) Multi-Agent Communication:**
- "A Survey of Multi-Agent Deep Reinforcement Learning with Communication" - MARL communication
- "Learning Multi-Agent Communication from Graph Modeling Perspective" - Graph-based communication
- "Communicating Activations Between Language Models" - Direct activation exchange

**b) Information Flow and Architecture:**
- "Beyond Message Passing: A Semantic View of Agent Communication Protocols" - Communication semantics
- "Information Bottlenecks in Deep Learning" - Information preservation
- "A Survey of LLM-Driven AI Agent Communication" - Comprehensive agent communication survey

**c) Error Propagation and Robustness:**
- "Robust Multi-Agent Reinforcement Learning" - Multi-agent robustness
- "Byzantine Robust Aggregation" - Adversarial communication
- "Error Cascades in Multi-Step Reasoning" - Error propagation analysis

### 2. **Prior Work Foundations**

**Communication Theory:**
- Information Theory (Shannon): Channel capacity, information loss
- Protocol Design: Network protocols, structured communication
- Human Teamwork: Coordination, explicit communication importance

**AI Foundations:**
- Ensemble Methods: Diversity and combination benefits
- Distributed Systems: Coordination and consensus algorithms
- Agent Theory: Agent communication protocols

### 3. **Future Research Directions**

1. **Learned Communication:**
   - Agents learning to communicate effectively
   - Meta-learning communication strategies
   - Emergent communication protocols

2. **Hybrid Communication:**
   - Combining structured and natural language
   - Multimodal agent communication (text + embeddings)
   - Adaptive communication based on partner capability

3. **Security and Trust:**
   - Verifying information authenticity in multi-agent systems
   - Byzantine fault tolerance for agent teams
   - Adversarial communication robustness

4. **Large-Scale Systems:**
   - Scaling to 10+ agent teams
   - Hierarchical agent communication
   - Network optimization for agent teams

5. **Domain-Specific Protocols:**
   - Communication standards for different domains
   - Scientific agent communication protocols
   - Business process automation communication standards

---

## References

1. Chun, Y.J., Ahmed, I. (2026). "What Do Agents Communicate? Characterizing Information Exchange in Multi-Agent Systems." ArXiv:2605.20548

2. Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." ArXiv:2201.11903

3. Yao, S., et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." ArXiv:2210.03629

4. Tullo, G., Colavolpe, G. (2020). "A Survey of Multi-Agent Deep Reinforcement Learning with Communication." ArXiv:2203.08975

---

**Last Updated:** May 22, 2026  
**Field:** Machine Learning / Multi-Agent Systems / Large Language Models  
**Key Tags:** Multi-Agent Systems, Agent Communication, Error Propagation, Information Flow, Collaborative Reasoning, System Reliability
