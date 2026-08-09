# Forage V2: Knowledge Evolution and Transfer in Autonomous Agent Organizations

**Authors:** [Team from ArXiv submission]

**ArXiv ID:** 2604.19837

**Submitted:** April 2026

**Source:** https://arxiv.org/abs/2604.19837

## Executive Summary

Autonomous agents operating in open-world tasks—where task boundaries are not predefined—face a fundamental problem: denominator blindness, the systematic underestimation of task scope. Forage V2 extends the Forage V1 architecture from a single-run system to a learning organization where experience accumulates across runs, transfers across model capabilities, and institutional safeguards prevent knowledge degradation. Demonstrated across web scraping, API querying, and mathematical reasoning, the system shows knowledge accumulation over six runs (growing from 0 to 54 entries) and successful knowledge transfer, where weaker agents seeded with stronger agent knowledge narrow performance gaps from 6.6 percentage points to 1.1 percentage points.

## Problem Statement

### Denominator Blindness

Autonomous agents in open-world tasks face a critical challenge:

- **Unbounded Problem Spaces:** Tasks don't come with predefined completion criteria
- **Denominator Blindness:** Agents systematically underestimate how much work remains to be done
- **Coverage Plateaus:** Agents reach a coverage ceiling and fail to explore remaining solution space
- **Efficiency Loss:** Inefficient exploration patterns lead to wasted computational resources
- **Model Degradation:** Multi-run systems without knowledge preservation fail to improve over time

### Forage V1 Limitations

The predecessor addressed some issues through:
- Co-evolving evaluation (Evaluator discovers completion criteria)
- Method isolation (Evaluator and Planner cannot see each other's code)

However, Forage V1 operated on a per-run basis—learning didn't accumulate or transfer across runs.

### Knowledge Transfer Gap

Current agent systems lack:
- **Persistent Organizational Memory:** No mechanism to accumulate insights across runs
- **Cross-Model Knowledge Transfer:** Insights from capable models don't benefit weaker models
- **Institutional Learning:** Organizations don't learn from experience like human teams do
- **Adaptive Strategies:** Agents cannot leverage learned patterns to improve future runs

## Core Concepts & Theory

### The Forage V2 Architecture

**Three Core Components:**

1. **Knowledge Base**
   - Persistent storage of task-domain insights
   - Structured entries capturing successful strategies, failure modes, and domain patterns
   - Versioning and quality control mechanisms

2. **Evaluator Agent**
   - Continuously discovers task completion boundaries
   - Identifies when Planner has reached current capability limits
   - Isolated from Planner code to prevent collusion

3. **Planner Agent**
   - Executes task completion steps
   - Learns from Knowledge Base entries
   - Accesses institutional memory to guide exploration

### Knowledge Base Structure

**Entry Components:**

- **Task Domain:** Categorization of the knowledge (web scraping, API interaction, mathematical reasoning)
- **Pattern:** Description of discovered pattern or strategy
- **Conditions:** When this knowledge applies
- **Success Rate:** Empirical success metrics across historical uses
- **Refinements:** Evolution of understanding as new evidence emerges

**Quality Control Mechanisms:**

- **Verification:** Knowledge entries validated before addition to base
- **Deprecation:** Outdated or failed approaches marked and de-prioritized
- **Provenance Tracking:** Recording which agent/model discovered each insight
- **Version Management:** Tracking evolution of knowledge over time

### Knowledge Transfer Mechanism

**Cross-Model Seeding:**

The paper demonstrates transfer from stronger models (Opus) to weaker models (Sonnet):

1. **Knowledge Extraction:** Distill Opus-discovered knowledge into Knowledge Base format
2. **Seeding:** Initialize Sonnet's context with relevant Knowledge Base entries
3. **Task Execution:** Sonnet uses seeded knowledge for improved exploration
4. **Coverage Improvement:** Weaker agent approximates stronger agent's performance

**Mathematical Formulation:** [Exact transfer functions unavailable — see full paper]

### Institutional Safeguards

**Preventing Knowledge Degradation:**

- **Conservative Addition:** Threshold for adding new entries prevents noise accumulation
- **Decay Functions:** Outdated knowledge gradually deprioritized
- **Consensus Validation:** Multiple runs must confirm pattern before canonical storage
- **Expert Curation:** Human oversight for critical domains

## Main Ideas & Contributions

1. **Organizational Learning Framework:**
   - Extends agent systems from single-run to multi-run learning organizations
   - Enables persistent accumulation of institutional knowledge
   - Demonstrates measurable performance improvement from organization-level learning

2. **Knowledge Transfer Protocol:**
   - Proposes concrete mechanism for transferring insights across model boundaries
   - Shows significant performance improvements from seeding (6.6pp → 1.1pp coverage gap)
   - Demonstrates transfer works across different model capabilities

3. **Denominator Problem Resolution:**
   - Shows that with proper knowledge accumulation, agents overcome underestimation
   - Knowledge base grows from 0 to 54 entries over six runs
   - Denominator estimates stabilize as domain understanding deepens

4. **Empirical Validation Across Domains:**
   - Tests in three distinct domains (web scraping, API queries, mathematical reasoning)
   - Shows consistency of approach across diverse task types
   - Demonstrates domain-specific knowledge doesn't harm generalization

5. **Architectural Safeguards:**
   - Method isolation prevents agent coordination shortcuts
   - Institutional safeguards maintain knowledge quality over time
   - Convergence mechanisms prevent oscillation or divergence

## Methodology & Implementation

### Experimental Setup

**Three Task Domains:**

1. **Web Scraping:** Extracting structured data from websites
   - Complex DOM navigation
   - Handling anti-scraping measures
   - Identifying relevant content patterns

2. **API Interaction:** Querying and manipulating remote APIs
   - Understanding API documentation
   - Handling authentication and rate limits
   - Extracting relevant information from responses

3. **Mathematical Reasoning:** Solving mathematical problems
   - Symbolic manipulation
   - Proof strategies
   - Pattern recognition in problem structure

### Experimental Protocol

**Run Sequence (6 total runs):**

1. **Initial Setup:** Empty Knowledge Base, single agent system
2. **Runs 2-6:** Accumulate insights, test transfer mechanisms

**Metrics Tracked:**
- Knowledge Base size (number of entries)
- Coverage percentage (portion of task space explored)
- Denominator estimates (agent's estimate of task size vs. actual)
- Transfer effectiveness (performance improvement from seeding)

### Results Summary

**Knowledge Accumulation:**
- Initial state: 0 knowledge entries
- After 6 runs: 54 verified knowledge entries
- Stabilization: Denominator estimates converge as understanding deepens

**Knowledge Transfer (Sonnet seeded with Opus knowledge):**
- Baseline coverage gap: 6.6 percentage points
- After seeding: Coverage gap narrows to 1.1 percentage points
- Improvement: ~83% reduction in performance gap

**Domain Performance:** [Specific per-domain metrics unavailable — see full paper]

### Implementation Details

**Knowledge Base Management:**
- Storage: [Exact storage format unavailable — see full paper]
- Update protocol: Vetted entries added via consensus
- Query optimization: Efficient retrieval of relevant knowledge for current task

**Agent Architecture:**
- Planner: LLM with retrieval-augmented context
- Evaluator: Independent assessment of task completion
- Communication: Structured protocol preventing hidden state sharing

**Scaling Considerations:**
- Knowledge base size management for long-running organizations
- Query efficiency as entries accumulate
- Computational cost of transfer operations

## Practical Applications & Use Cases

### Autonomous Research

- **Literature Discovery:** Agents learning systematic search strategies for scientific literature
- **Hypothesis Generation:** Accumulating patterns in successful hypothesis formulation
- **Experiment Design:** Learning experimental design principles across multiple domains

### Software Engineering

- **Code Search and Navigation:** Agents learning to efficiently explore large codebases
- **Bug Finding:** Accumulating bug patterns and search strategies
- **API Mastery:** Learning API behavior through systematic exploration

### Knowledge Work Automation

- **Document Analysis:** Learning patterns in document structure and extraction
- **Data Integration:** Accumulating knowledge of data source peculiarities
- **Information Synthesis:** Learning to combine information from multiple sources

### Scientific Discovery

- **Biological Research:** Agents learning systematic exploration of parameter spaces
- **Material Science:** Learning synthesis and characterization strategies
- **Drug Discovery:** Accumulating knowledge of molecular properties and interactions

### Practical Challenges

- **Knowledge Stagnation:** System might converge to local optima without exploration
- **Negative Transfer:** Incorrect or domain-specific knowledge might harm transfer
- **Scalability:** Knowledge management complexity increases with organization size
- **Quality Control:** Maintaining knowledge base accuracy at scale
- **Transparency:** Understanding which knowledge entries drive decisions

## Insights & Implications

1. **Organizations Learn Differently from Individuals:**
   - Multi-run learning dynamics differ fundamentally from single-run agent optimization
   - Organizational memory enables emergent capabilities not possible for individual agents
   - Institutional safeguards become critical as scale increases

2. **Knowledge Transfer as Capability Amplifier:**
   - Weak agents can approximate strong agent capabilities with proper knowledge seeding
   - Transfer effectiveness depends critically on knowledge quality and relevance
   - Successful transfer suggests generalizable insights within and across domains

3. **Denominator Problem is Solvable:**
   - Proper epistemological frameworks (separate evaluation) help overcome systematic biases
   - Knowledge accumulation provides empirical ground truth for problem size
   - Convergence validates correctness of approach

4. **Institutional Dynamics Matter:**
   - Preventing knowledge degradation requires active curation, not passive accumulation
   - Quality control mechanisms essential for long-term performance
   - Institutional memory becomes asset but can become liability if corrupted

5. **Scalability Lessons:**
   - Systems that learn organizational memory require different design than single-agent systems
   - Separation of concerns (Planner/Evaluator) proves effective for maintaining quality
   - Scaling requires proportional investment in knowledge management infrastructure

## State-of-the-Art Advancement

Forage V2 advances the field by:
- Introducing the first framework demonstrating sustained organizational learning in autonomous agents
- Quantifying knowledge transfer effectiveness across model capabilities
- Solving the denominator blindness problem through institutional epistemology
- Showing that autonomous systems can overcome systematic biases through proper architecture
- Demonstrating scalable mechanisms for multi-run agent coordination

The work establishes organizational learning as a key capability for autonomous systems, with significant implications for deployment in complex, open-ended domains.

## Code & Resources

**Official Materials:**
- Paper PDF: https://arxiv.org/pdf/2604.19837
- ArXiv Webpage: https://arxiv.org/abs/2604.19837

**System Components:**
- Knowledge Base implementation
- Planner agent framework
- Evaluator agent implementation
- Transfer mechanism implementation

**Dependencies:**
- LLM API access (OpenAI or compatible)
- Knowledge store (database or vector store)
- Task execution environment
- Evaluation framework

**Compute Requirements:**
- Multiple LLM API calls per run
- Storage for growing Knowledge Base
- Transfer operations require retrieval and re-ranking

## Related Work & Context

### Foundational Work

- **Lifelong Learning:** Continuous learning over multiple tasks and time periods
- **Transfer Learning:** Leveraging knowledge from one domain to another
- **Multi-Agent Systems:** Coordination mechanisms for agent teams
- **Knowledge Representation:** Structured approaches to encoding domain knowledge
- **Organizational Theory:** How institutions learn and evolve

### Related Recent Papers

- Few-shot learning and in-context adaptation for agents
- World models and simulation for agent learning
- Curriculum learning for autonomous systems
- Reinforcement learning from human feedback and oversight
- Agent teams and swarms with emergent properties

### Future Research Directions

1. **Negative Transfer Mitigation:** Mechanisms to detect and prevent harmful knowledge transfer
2. **Automated Knowledge Curation:** Learning which knowledge entries to keep, deprecate, or refine
3. **Cross-Domain Learning:** Transferring insights between seemingly unrelated domains
4. **Agent Specialization:** Organizations where agents develop specialized roles based on knowledge
5. **Distributed Organizations:** Forage V2 applied to geographically or computationally distributed agents
6. **Human-in-the-Loop Curation:** Combining autonomous learning with human expert guidance
7. **Meta-Learning Organizations:** Organizations that learn how to learn more effectively
8. **Long-Horizon Learning:** Forage V2 applied to problems requiring years of accumulated learning
