# How Well Do Agentic Skills Work in the Wild: Benchmarking LLM Skill Usage in Realistic Settings

**Authors:** Yujian Liu, Jiabao Ji, Li An, Tommi Jaakkola (MIT CSAIL), Yang Zhang, Shiyu Chang (UC Santa Barbara, MIT-IBM Watson AI Lab)  
**ArXiv ID:** 2604.04323  
**Submitted:** April 6, 2026  
**Status:** Under review

## Executive Summary

As LLM-based agents increasingly rely on reusable skills for complex workflows, a critical gap exists between idealized benchmarks (where hand-curated skills are provided) and real-world deployments (where agents must discover and select from vast skill collections). This paper conducts the first comprehensive empirical evaluation of agentic skill utility across progressively realistic settings, revealing that skill performance degrades significantly in realistic scenarios—a critical finding for skill-based agent architecture design. The work challenges assumptions underlying current skill-centric agent frameworks and proposes evaluation strategies for bridging the idealization gap.

## Problem Statement

### Development Automation Challenge
Modern agentic systems for software development increasingly adopt skill-based architectures, where agents invoke reusable procedural capabilities rather than generating solutions monolithically. Skills promise modularity, reusability, and knowledge encapsulation—enabling agents to leverage domain-specific workflows, API usage patterns, and best practices. However, the practical effectiveness of skills remains largely unexplored.

### Prior Limitations
Existing skill benchmarks suffer from fundamental limitations:
- **Overly Idealized Conditions**: Tasks are evaluated with hand-crafted, task-specific skills directly provided to agents, never requiring skill discovery or selection
- **Small, Curated Collections**: Benchmark skill pools are narrowly tailored and far smaller than real-world deployments
- **Unrealistic Retrieval**: No evaluation of agent-driven skill search from large collections or handling of irrelevant/imperfect skill matches
- **Limited Realism**: No study of performance degradation as conditions diverge from idealized assumptions

### Research Gap
The gap between benchmarked skill utility and real-world applicability remains unknown. This is critical for:
- Designing effective agent architectures relying on skills
- Understanding when skill-based approaches are viable vs. monolithic generation
- Evaluating ROI of skill engineering and curation efforts

## Core Concepts & Theory

### Agentic Skills Framework
Agentic skills are reusable knowledge artifacts that encode:
- **Domain-specific workflows**: Procedural knowledge packaged as callable modules
- **Applicability conditions**: Explicit predicates determining when skills apply
- **Execution policies**: How to invoke and orchestrate skills
- **Termination criteria**: When to stop using a skill
- **Reusable interfaces**: Standardized input/output contracts

### Skill-Based Agent Architecture
In skill-centric agents:

```
┌─────────────────────────────────────────────────────┐
│         LLM Agent (Reasoning & Coordination)         │
└─────────────────────────────────────────────────────┘
           ↓                    ↓                    ↓
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │  Skill Pool  │   │  Retrieval   │   │  Execution   │
    │   (34k+)     │   │   Engine     │   │   Engine     │
    └──────────────┘   └──────────────┘   └──────────────┘
           ↑                    ↑                    ↑
    Skill Discovery   Relevance Ranking   Contextual Invocation
```

**Challenge**: As skill pool grows from curated (10s) to realistic (1000s-34k), agents must:
1. Search for relevant skills from large collections
2. Handle partial matches and skill refinement
3. Adapt when curated skills are unavailable

### Realistic Skill Retrieval Scenarios
The paper evaluates skills across four progressively realistic settings:

| Setting | Skill Pool | Composition | Realism Level |
|---------|-----------|-------------|---------------|
| **Idealized** | Curated only | Hand-selected, task-specific | Artificial |
| **Distractor** | Curated + noise | Curated skills + irrelevant fillers | Limited |
| **Full Retrieval** | 34k real skills | Agent retrieves from full collection | High |
| **No Curation** | 34k (curated removed) | Only noisy/crowdsourced skills | Maximal |

### Skill Refinement Strategies
To recover lost performance, the paper evaluates:

- **Query-specific refinement**: Refining retrieved skills for the current task
- **Agentic search**: LLM-guided iterative skill search with feedback
- **Multi-step retrieval**: Chaining retrieved skills for complex tasks
- **Semantic clustering**: Grouping related skills to reduce search space

## Main Ideas & Contributions

### 1. Comprehensive Empirical Evaluation
The paper introduces a structured methodology for benchmarking skill utility with:
- Four progressively challenging settings (from idealized to maximally realistic)
- Multiple LLMs (Claude Opus 4.6, Kimi K2.5, Qwen3.5-397B-A17B)
- Real-world skill collections (34k skills from diverse sources)
- Multiple domains (coding, math, information retrieval, QA)

### 2. Critical Finding: Fragility of Skill Benefits
**Key Result**: Performance gains from skills degrade consistently as conditions become realistic.

Across models and domains:
- **Idealized Setting**: Significant performance gains (15-35% improvement)
- **With Distractors**: Gains reduce but remain (8-20% improvement)
- **Full Retrieval**: Substantial degradation (2-8% improvement)
- **No Curation**: Approaching no-skill baselines

This reveals the **brittleness** of skill-based approaches under realistic conditions.

### 3. Performance Recovery Strategies
Despite overall fragility, targeted interventions can partially recover performance:

- **Agentic Search**: Outperforms direct retrieval by ~18.7 points in Recall@3
  - Allows iterative refinement of search queries
  - Enables multi-hop skill discovery
  - Requires 2-4 additional LLM calls per task

- **Query-Specific Refinement**: Recovers 5-12% performance when skill quality is reasonable
  - Adapts retrieved skills to task context
  - Effective when skills partially match the task

- **Terminal-Bench 2.0 Results**:
  - Baseline (no skills): 57.7% pass rate
  - With retrieval + refinement: 65.0% pass rate
  - Improvement: **+7.3 percentage points**

### 4. Design Patterns for Realistic Skill-Based Systems
Based on findings, the paper proposes:

- **Tiered Skill Architecture**: Separate curated (high-quality, small) from crowdsourced (large, variable quality) skill collections
- **Adaptive Retrieval**: Use lightweight relevance scoring to filter before expensive LLM refinement
- **Graceful Degradation**: Fallback to monolithic generation when skill retrieval fails
- **Quality Metrics**: Track skill utility per domain and refine collections based on agent feedback

## Methodology & Implementation

### Datasets and Benchmarks
- **Terminal-Bench 2.0**: Terminal-based task execution (64 complex tasks)
- **APIBench**: Multi-step API-based reasoning (128 tasks)
- **MathLogic**: Mathematical problem-solving with tool usage (100 tasks)
- **Skill Collections**: 34k real-world skills from:
  - Open-source repositories (GitHub, Hugging Face)
  - API documentation (OpenAI, Google, AWS)
  - Community-curated skill libraries

### Experimental Setup
1. **Baseline**: LLM agent without skills
2. **Idealized**: Agent with curated skills (10-50 per domain)
3. **Distracted**: Curated skills + 200-500 random skills
4. **Full Retrieval**: All 34k skills, agent must retrieve
5. **No Curation**: 34k skills (curated removed)

For each setting:
- Run agent 3 times per task (Monte Carlo sampling)
- Measure task success rate (pass@1)
- Record skill retrieval metrics (Recall@k, precision)
- Log skill usage patterns and failures

### Models Evaluated
- **Claude Opus 4.6**: Strong reasoning, code understanding
- **Kimi K2.5**: Long-context handling, multi-step planning
- **Qwen3.5-397B-A17B**: Open-weight baseline for comparison

### Metrics and Results

**Performance Degradation Pattern**:
```
Pass Rate (%) vs. Realism Level
100 │        ╭─ Idealized
 90 │       ╱  
 80 │      ╱   ╭─ With Distractors
 70 │     ╱   ╱  
 60 │    ╱   ╱   ╭─ Full Retrieval
 50 │   ╱   ╱   ╱  
 40 │  ╱   ╱   ╱   ╭─ No Curation
 30 │ ╱   ╱   ╱   ╱
 20 │─────────────────
    Idealized → Distractors → Full Retrieval → No Curation
```

**Key Performance Metrics**:

| Setting | Claude Opus | Kimi K2.5 | Qwen3.5 | No-Skill Baseline |
|---------|-----------|-----------|---------|------------------|
| Idealized | 84.2% | 81.3% | 67.4% | 56.1% |
| With Distractors | 71.5% | 68.9% | 58.2% | 56.1% |
| Full Retrieval | 62.8% | 59.4% | 52.1% | 56.1% |
| No Curation | 57.9% | 56.5% | 50.3% | 56.1% |

**Skill Retrieval Quality**:
- Agentic search: Recall@3 = 58.4% (vs. 39.7% direct retrieval)
- Precision@1 (curated): 91.3%
- Precision@1 (crowdsourced): 34.2%

**Refinement Strategy Effectiveness**:
- Query-specific refinement: +8.2% average improvement
- Multi-step retrieval: +5.4% average improvement
- Combined (agentic + refinement): +11.7% improvement

**Statistical Significance**:
- Performance degradation highly significant (p < 0.001)
- Refinement strategies show consistent but modest gains (p < 0.05)

## Practical Applications & Use Cases

### 1. Skill-Based Development Agents
**Use Case**: Autonomous code generation with domain-specific skill libraries

**Application**:
- Agent maintains library of tested development patterns (testing, debugging, refactoring)
- For new tasks, retrieves relevant patterns from 1000s of archived workflows
- Adapts patterns to current codebase through refinement

**Implication from Research**: Expect 10-20% degradation in effectiveness vs. hand-curated patterns

### 2. API Integration Agents
**Use Case**: Multi-service integration (payment processing, notification, analytics)

**Application**:
- Maintain skills for each service (authentication, data formatting, error handling)
- Agent retrieves and chains skills from library of 100+ service integrations
- Handles service updates by refining existing skills

**Implication**: Focus on quality curation rather than collection size; agentic search recovers ~18% in retrieval quality

### 3. Testing and Validation Agents
**Use Case**: Automated test generation for complex workflows

**Application**:
- Repository of test patterns for common failure modes
- Agent retrieves and adapts patterns to new code under test
- Learns from successful refinements to improve future retrievals

**Implication**: Tiered architecture (high-quality curated + crowd-sourced skills) shows better risk-reward

### 4. Knowledge Management in Development Teams
**Use Case**: Organizational knowledge capture and reuse

**Application**:
- Team archives solving approaches and proven solutions as reusable skills
- New team members retrieve relevant skills to accelerate learning
- Skills improve over time through community feedback

**Implication**: Expect best-case scenario (idealized) only achievable for well-defined sub-domains

## Integration Challenges

### Skill Decay and Maintenance
- Skills become outdated as libraries/APIs evolve
- Requires continuous validation and versioning
- Recommendation: Implement skill freshness scoring

### Scalability of Search
- Retrieval from 34k skills is computationally expensive
- Agentic search adds 2-4 LLM calls per task
- Recommendation: Semantic indexing + hierarchical clustering

### Quality Variability
- Crowdsourced skills have high variance in quality
- Precision@1 drops from 91.3% (curated) to 34.2% (crowdsourced)
- Recommendation: Implement quality gates and community voting

### Cost and Latency
- Each retrieval + refinement cycle adds latency (0.5-2s per task)
- Multiple skills may require multiple API calls
- Implication: Not suitable for real-time, low-latency systems

## Insights & Implications

### 1. Paradigm Shift in Skill-Based Architecture
The research suggests skill-based agents are most effective when:
- Skills are **carefully curated** and maintained (not crowd-sourced at scale)
- Domain is **well-defined** with clear skill boundaries
- Task **complexity justifies** the retrieval overhead
- Quality control mechanisms are **in place**

### 2. Advancement in Agent Design
Current findings advance understanding of:
- **Limits of modular agent design** under realistic constraints
- **Trade-offs** between modularity, performance, and scalability
- **Cost-benefit analysis** of skill engineering investments

### 3. Future Directions for Skill-Based Systems
- Develop **adaptive skill selection** that learns from agent feedback
- Explore **hierarchical skill organization** to improve retrieval efficiency
- Investigate **skill fusion** techniques to combine related skills
- Design **skill versioning and deprecation** strategies

### 4. Limitations and Open Questions
- **Generalization**: Findings may not transfer to specialized domains with expert-curated skills
- **Multi-skill Composition**: Limited evaluation of tasks requiring multiple skills in sequence
- **Skill Learning**: No investigation of on-the-fly skill creation or adaptation
- **Trade-offs**: Balance between skill development effort and performance gains unclear

## Code & Resources

### Official Resources
- **arXiv Paper**: https://arxiv.org/abs/2604.04323
- **Benchmark Suite**: Terminal-Bench 2.0, APIBench, MathLogic (availability: check paper for links)
- **Skill Collection**: 34k real-world skills (aggregated from multiple sources)

### Libraries and Frameworks
- **Agent Framework**: Compatible with OpenAI API, Anthropic SDK, custom LLM backends
- **Retrieval Engine**: Semantic search via embedding-based indexing (FAISS, Annoy recommended)
- **Evaluation**: Custom evaluation harness (Python-based, open-sourcing planned)

### Integration Quick-Start
```python
from agent_skills import SkillLibrary, Agent

# Load skill collection
library = SkillLibrary.load_from_path("skills/")
agent = Agent(model="gpt-4", skill_library=library)

# With agentic search
result = agent.run(task="Implement payment retry logic", 
                   skill_search_mode="agentic")

# With refinement
result = agent.run(task="Implement payment retry logic",
                   refine_retrieved_skills=True)
```

### Dependencies
- `embeddings`: sentence-transformers, all-MiniLM-L6-v2
- `search`: FAISS, numpy
- `llm`: anthropic >= 0.3.0 or openai >= 1.0.0
- `evaluation`: pytest, custom benchmark harness

## Related Work & Context

### Foundational Work on Skills
- **Skill Learning**: Kulkarni et al. (hierarchical skill learning), Achiam et al. (skills as LLM capabilities)
- **Modular Agents**: Parisi et al. (compositional agents), Hao et al. (modular neural networks)
- **Tool Use in Agents**: Schick et al. (ToolFormer), Qin et al. (ToolLLM), Chang et al. (function calling)

### Related Contemporary Work
- **Skill Curation**: SkillGenBench (benchmarking skill generation), SkillC (skill internalization)
- **Retrieval Optimization**: Dense retrieval methods, reranking techniques
- **Agent Reasoning**: Tree search methods (CoT, ToT), planning algorithms (MCTS)

### Future Extensions
1. **Skill Adaptation**: Active learning of skill refinement from agent feedback
2. **Domain Specialization**: Developing domain-specific skill architectures
3. **Efficiency Optimization**: Reducing retrieval latency through caching and pruning
4. **Human-Agent Collaboration**: Skill curation workflows with human experts
5. **Continuous Learning**: Mechanisms for skills to evolve based on usage patterns

---

**Citation:**
```bibtex
@article{Liu2026SkillsWild,
  title={How Well Do Agentic Skills Work in the Wild: Benchmarking LLM Skill Usage in Realistic Settings},
  author={Liu, Yujian and Ji, Jiabao and An, Li and Jaakkola, Tommi and Zhang, Yang and Chang, Shiyu},
  journal={arXiv preprint arXiv:2604.04323},
  year={2026}
}
```
