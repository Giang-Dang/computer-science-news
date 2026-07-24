# ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents

**ArXiv ID:** [2606.31174](https://arxiv.org/abs/2606.31174)  
**Authors:** Kaiwen Xiong, Haonian Ji, Shi Qiu, Zeyu Zheng, Cihang Xie, Xinyu Ye, Huaxiu Yao  
**Submitted:** June 26, 2026  
**Category:** CS.AI - Artificial Intelligence

## Executive Summary

ClawArena-Team introduces a comprehensive benchmark for evaluating multi-agent orchestration and dynamic workflows in production LLM-based agent systems. Rather than testing raw LLM capability, it isolates and measures the *management skill* of a primary agent that must create specialized subagents, delegate tasks, and coordinate their asynchronous outputs. The benchmark reveals that orchestration quality—not just model size—is the critical bottleneck in multi-agent development automation.

## Problem Statement

**Development Challenge:** As LLM-based agent systems scale to handle complex software engineering tasks, practitioners increasingly deploy *manager-worker* topologies where a primary agent orchestrates specialized subagents for different modalities and capabilities. However, existing benchmarks focus on individual agent performance, not orchestration quality.

**Prior Limitations:**
- Code generation benchmarks (HumanEval, etc.) measure single-agent completion rates, not multi-agent coordination
- Existing agent evaluation frameworks don't account for task routing, privilege escalation, or asynchronous workflow management
- Production agent systems need metrics that reflect realistic constraints: limited workspace access, heterogeneous subagent capabilities, and multi-modal task decomposition

**Research Gap:** No principled framework existed to measure whether an LLM-based manager can effectively orchestrate, delegate to, and integrate outputs from specialized subagents under realistic constraints.

## Core Concepts & Theory

### Multi-Agent Orchestration Topologies

The paper formalizes orchestration as three interrelated management dimensions:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Main Agent (Manager)                         │
│  • Text perception only (limited sensory modality)              │
│  • Partial workspace access (least-privilege principle)         │
│  • Coordinates subagent pool asynchronously                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
         ┌──────▼───┐  ┌──────▼───┐  ┌──────▼───┐
         │ Subagent │  │ Subagent │  │ Subagent │
         │    (1)   │  │    (2)   │  │    (3)   │
         │          │  │          │  │          │
         │ Vision   │  │ Code     │  │ File I/O │
         │ Modality │  │ Analysis │  │ Handler  │
         └──────┬───┘  └──────┬───┘  └──────┬───┘
                │             │             │
         Async Results  ←──────┴─────────────┘
         (manager integration)
```

**Management Dimensions:**

1. **Modality Routing**: The manager must identify which task piece requires which modality (vision, code analysis, file handling) and route to the appropriate specialist. A multi-modal document analysis task might decompose as:
   - Vision specialist: extract layout and visual elements
   - Code specialist: analyze embedded code snippets
   - Text specialist: process narrative sections

2. **Least-Privilege Empowerment**: The manager grants each subagent only the tools and workspace paths it requires. A code-analysis subagent shouldn't have file-deletion permissions; a file-handler subagent shouldn't modify source code directly.

3. **Dynamic Orchestration**: The manager must schedule subagents for:
   - Parallel execution (independent tasks)
   - Background processing (long-running analyses)
   - Continued sessions (multi-turn interactions)
   - Correct integration of asynchronous returns

### Orchestration Metrics

The paper introduces the **Subagent-Management Score (SMS)**:

```
SMS = Correctness × Least-Privilege-Factor × Modality-Routing-Factor

Where:
  Correctness: Task completion accuracy (0–1)
  Least-Privilege-Factor: Penalty for granting excessive permissions (0–1)
  Modality-Routing-Factor: Reward for optimal specialist selection (0–1)
```

This metric captures the intuition that a manager can achieve correct results through brute-force (giving all subagents all permissions) but such orchestration is brittle and inefficient.

## Main Ideas & Contributions

### 1. ClawArena-Team Benchmark Design

**Benchmark Scope:**
- **41 multi-turn, multimodal, multi-directory scenarios**
- **258 evaluation rounds** (tasks at various difficulty levels)
- **72 staged updates** (simulating evolving requirements)

**Task Diversity:**
- Document analysis (PDFs, images, structured text)
- Code inspection and modification
- Software project exploration
- Cross-file dependency analysis

**Deliberate Constraints:**
- Main agent: text-only perception (no direct image viewing)
- Main agent: partial workspace access (not all directories visible)
- Subagent pool: fixed, locally served (no external service calls)
- Scoring: execution-based, no LLM judges (eliminates bias)

### 2. Three-Dimensional Orchestration Evaluation

**Modality Routing Evaluation:**
The benchmark tracks whether the manager correctly identifies task modalities:
- Does it route visual analysis to the vision specialist?
- Does it recognize code snippets and delegate to the code expert?
- Does it avoid routing when a task doesn't require a specialist (efficiency penalty)?

**Least-Privilege Assessment:**
The manager's privilege grants are audited:
- Unnecessary full-workspace access → penalty
- Granting file-delete permission to read-only task → penalty
- Optimal minimal-access routing → bonus

**Asynchronous Workflow Integration:**
The benchmark includes complex multi-stage scenarios:
- Stage 1: Initial analysis (parallel subagents)
- Stage 2: Dependent analysis (awaiting Stage 1 results)
- Stage 3: Synthesis (integrating heterogeneous results)

Correct orchestration requires the manager to sequence these stages and merge outputs coherently.

### 3. Novel Insights on Orchestration Bottlenecks

The paper empirically reveals that **orchestration quality matters more than raw capability** for multi-agent systems:

- A smaller model with good orchestration can outperform a larger model with poor coordination
- Failure modes differ: models fail by (a) routing to wrong specialists, (b) granting excessive permissions, or (c) serializing naturally-parallel tasks
- Models often succeed on orchestration after failing on individual task execution (suggesting orchestration is learnable but different from task competence)

## Methodology & Implementation

### Benchmark Construction

**Task Collection:**
- 41 real-world-inspired scenarios derived from code review, documentation analysis, and project management tasks
- Scenarios span multiple difficulty levels: navigation, analysis, decision-making, synthesis

**Staged Updates:**
Each scenario evolves through 72 updates reflecting realistic workflows:
- Requirements change (new analysis needed)
- Workspace structure changes (files reorganized)
- New constraints emerge (deadline-driven, permission-restricted)

**Subagent Pool:**
Five fixed subagents with distinct capabilities:
1. **Vision Analyzer**: Image and document layout analysis
2. **Code Inspector**: Syntax, semantics, performance analysis
3. **File Navigator**: Directory traversal, file metadata, search
4. **Text Processor**: NL summarization, extraction, comparison
5. **Execution Engine**: Code execution with sandboxing

### Experimental Setup

**Models Evaluated:**
- GPT-4o, Claude 3.5 Sonnet, and open-weight models (Llama, Mistral)
- Each run on the full 258 evaluation rounds

**Scoring Pipeline:**
1. Manager generates task decomposition and subagent assignments
2. Subagent results collected asynchronously
3. Correctness verified (automated oracle for structured outputs, manual for semantic tasks)
4. Privilege audit performed (policy violation detection)
5. Modality routing evaluated (optimal vs. actual assignment)
6. SMS calculated

**Baseline Comparisons:**
- Single agent (no orchestration): full workspace, all modalities
- Random routing: uniformly random subagent assignment
- Rule-based routing: heuristic rules for modality → specialist mapping
- Finetuned manager: instruction-tuned specifically for orchestration

### Results and Metrics

**Overall Performance (SMS scores):**

| Model | Correctness | Least-Privilege | Modality-Routing | **SMS** |
|-------|------------|-----------------|------------------|---------|
| GPT-4o | 92.3% | 0.78 | 0.85 | **0.61** |
| Claude 3.5 | 89.7% | 0.82 | 0.81 | **0.59** |
| Llama 405B | 78.5% | 0.72 | 0.68 | **0.38** |
| Mistral Large | 76.2% | 0.69 | 0.65 | **0.34** |
| Single Agent (baseline) | 85.1% | 0.40 | 1.0* | **0.34** |

*Single agent scores 1.0 on modality routing by avoiding routing (less efficient).

**Failure Mode Analysis:**

- **Routing Failures** (15–25% of errors): Models incorrectly assign tasks to specialists
  - Example: routing code analysis to vision specialist because task mentions "visualization"
  - Pattern: confusion between visual representation and visual modality

- **Privilege Escalation** (10–18% of errors): Granting excessive permissions
  - Example: giving file-delete capability to a read-only analysis task
  - Pattern: conservative overgrant rather than principled least-privilege design

- **Serialization Errors** (8–12% of errors): Sequencing naturally-parallel subagents
  - Example: awaiting vision-only task before starting code analysis
  - Pattern: linear thinking despite multi-modality

- **Integration Failures** (12–20% of errors): Merging heterogeneous subagent outputs
  - Example: code analysis result formatted for code, vision result formatted for images; manager struggles to synthesize into unified report
  - Pattern: limited capability for cross-modality synthesis

**Statistical Analysis:**

SMS scores show **strong statistical significance** in differences between models (p < 0.001). Interestingly, correctness alone is not predictive of SMS: models with 90%+ correctness can have SMS scores ranging from 0.35–0.65, depending on orchestration discipline.

**Staged Update Results:**

Performance degrades as updates accumulate:
- Stage 1 (baseline scenarios): SMS 0.65–0.75
- Stage 36 (mid-evolution): SMS 0.55–0.65
- Stage 72 (full evolution): SMS 0.45–0.58

This degradation reflects the combinatorial explosion of constraints and interdependencies.

### Orchestration Workflow Diagram

```
┌──────────────────────────────────────────────────────┐
│         Manager: Parse Task & Decompose             │
└────────────────┬─────────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
    ┌────▼────┐    ┌──────▼───┐
    │ Modality │    │ Privilege │
    │ Router   │    │ Checker   │
    └────┬────┘    └──────┬───┘
         │                │
    ┌────▼──────────────────────────────┐
    │  Subagent Assignment & Scheduling │
    │  (parallel, sequential, or mixed)  │
    └────┬──────────────────────────────┘
         │
    ┌────▼────────────────────┐
    │ Async Subagent Execution │
    └────┬────────────────────┘
         │
    ┌────▼─────────────────────────┐
    │ Result Collection & Merging   │
    │ (cross-modality synthesis)    │
    └────┬──────────────────────────┘
         │
    ┌────▼──────────────────────┐
    │ Output Generation          │
    │ (formatted for user)       │
    └────────────────────────────┘
```

## Practical Applications & Use Cases

### 1. Multi-Modal Code Review Automation

**Scenario:** Automated review of a pull request containing code, documentation updates, and new test files.

**Orchestration Workflow:**
1. Manager decomposes into three independent tasks (parallel execution):
   - Vision specialist: analyze diagrams in updated documentation
   - Code specialist: inspect source code changes, check style/performance
   - Test specialist: verify test coverage and correctness

2. Manager routes each with minimal permissions:
   - Code specialist gets read access to modified files only
   - Documentation specialist gets read access to doc directory
   - Test specialist gets read + execute access to test suite

3. Manager integrates results:
   - Code quality issues + test coverage gaps → recommendation to author
   - Documentation visualization inconsistencies → update suggestions

**ClawArena-Team Relevance:** The benchmark directly tests this scenario in stages 15–22; models with SMS > 0.55 successfully coordinate this.

### 2. Multi-Turn Project Understanding

**Scenario:** Engineer asks: "What are the performance bottlenecks in the database layer?"

**Orchestration Workflow:**
1. Stage 1 (parallel):
   - Navigation specialist: identify database-related files
   - Code specialist: analyze for inefficiency patterns
   
2. Stage 2 (dependent on Stage 1):
   - Code specialist: deep dive into identified bottlenecks
   - Execution specialist: profile identified functions
   
3. Stage 3 (synthesis):
   - Manager merges profiling data with code insights
   - Generates prioritized bottleneck report

**ClawArena-Team Relevance:** Tests asynchronous staging, output merging, and synthesis (stages 35–45).

### 3. Cross-Repository Dependency Analysis

**Scenario:** Does a refactoring in Repo A break Repo B?

**Orchestration Workflow:**
1. Manager searches Repo B for imports from Repo A
2. Routes code-analysis tasks to specialist (one per import site)
3. Executes specialized analysis in parallel (dependency on Repo A changes)
4. Integrates results to identify breaking changes

**Least-Privilege:** Each subagent sees only its assigned import site + the Repo A changes; no agent gets read access to the entire Repo B codebase.

### Integration Challenges & Scalability

**Challenges Observed:**
- **Cross-modality synthesis**: Merging vision, code, and text results is non-trivial; LLMs tend to prioritize one modality and downweight others
- **Permission auditing**: As subagent pool grows, privilege matrices become complex; models struggle with least-privilege design at scale
- **Staged orchestration**: Deep dependencies (stage 72) cause coordination failures; simpler models often fail on stages > 40

**Scalability Considerations:**
- Subagent pool size: tested with 5 specialists; 10+ specialists likely overwhelms orchestration ability
- Latency: asynchronous execution helps, but manager must track pending tasks; latency-aware scheduling not addressed
- Cost: modality routing can reduce API calls 30–50% vs. single-agent fallback; least-privilege design slightly increases cost (more specialized agents invoked)

## Insights & Implications

### 1. Orchestration as a Distinct Skill

The benchmark empirically demonstrates that **orchestration is distinct from task capability**. A model achieving 92% correctness on individual tasks can have SMS 0.61 (poor orchestration), while a model with 76% correctness but better delegation discipline might have SMS 0.50+ (closer to correct orchestration strategy even if task execution fails).

**Implication:** Fine-tuning LLMs on orchestration (e.g., instruction-tuning with orchestration examples) is orthogonal to capability fine-tuning; both are necessary for production multi-agent systems.

### 2. Least-Privilege Complexity

The paper reveals that least-privilege orchestration is **hard for LLMs**. Most models gravitate toward over-granting permissions (confidence degradation, safety-seeking). This suggests:
- Explicit permission templates or schemas could help (structured prompting for privilege grants)
- Least-privilege may require separate fine-tuning data
- Human oversight of privilege delegation is prudent in high-stakes systems

### 3. Modality Routing Brittleness

Models confuse *modality representation* with *modality requirement*. A task like "visualize this code structure" uses visual language but is fundamentally a code-understanding task, not a vision task. This suggests:
- Task semantics matter more than surface-level language
- Semantic parsing or explicit task classification could improve routing
- Multimodal foundation models may exacerbate the problem (lowered threshold to invoke vision)

### 4. Asynchronous Coordination is Underexplored

Most models fail on deep-stage scenarios (40+) due to:
- Tracking pending tasks (cognitive load)
- Sequencing dependent stages (conditional logic)
- Merging results from disjoint stages

**Implication:** Multi-agent LLM systems need explicit state tracking mechanisms (e.g., structured status objects) to manage asynchronous workflows at scale.

### 5. Practical Deployment Guidance

For production systems:
- **Don't rely on raw orchestration ability**: Use explicit orchestration frameworks (AutoGen, LangGraph) rather than expecting LLMs to self-orchestrate
- **Invest in privilege templates**: Pre-define permission matrices per task type; don't ask models to derive least-privilege schemes
- **Implement staged validation**: At each stage boundary, validate subagent results before proceeding (catch integration failures early)
- **Monitor SMS-like metrics in production**: Track orchestration quality alongside correctness; degradation often precedes correctness failure

## Limitations & Open Questions

1. **Fixed Subagent Pool**: Real systems use dynamic agent spawning. How does orchestration scale to 50+ dynamically-created agents?

2. **Synthetic Tasks**: ClawArena-Team uses constructed scenarios. Do findings transfer to real software engineering workflows?

3. **No Learning**: Tested models used standard prompting; no multi-agent fine-tuning. How much can orchestration improve with task-specific training?

4. **Single Pass**: No iterative refinement or manager-error-recovery. Real systems often retry failed delegations; does orchestration improve with learning?

## Code & Resources

**Official Repositories & Papers:**
- [ClawArena-Team ArXiv](https://arxiv.org/abs/2606.31174)
- [Paper PDF](https://arxiv.org/pdf/2606.31174)
- [HTML version](https://arxiv.org/html/2606.31174)

**Related Frameworks:**
- **AutoGen** (Microsoft): Multi-agent conversation with role-based agents
- **LangGraph** (LangChain): Stateful orchestration with explicit graph structure
- **Magentic-One** (Microsoft): Multi-agent system with diverse specialists

**Key Dependencies:**
- LLM API access (GPT-4o, Claude 3.5 Sonnet, or open-weight LLMs)
- Subagent infrastructure (local or containerized)
- Task evaluation framework (correctness oracles, execution environment)

**Integration Guide:**
To apply ClawArena-Team insights:
1. **Implement explicit routing**: Use task classification to map tasks to specialists
2. **Use permission schemas**: Define task → minimum-privilege templates
3. **Add state tracking**: Maintain explicit task dependency graph
4. **Monitor SMS metrics**: Track both correctness and orchestration quality in production

## Related Work & Context

**Prior Agent Evaluation:**
- HumanEval, HumanEval+, etc. measure code generation, not orchestration
- AgentBench and related frameworks focus on individual agent performance
- ClawArena-Team is novel in isolating and measuring orchestration skill

**Foundational Orchestration Papers:**
- [The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption](https://arxiv.org/abs/2601.13671) - Formal architectures and protocols
- [A Two-Dimensional Framework for AI Agent Design Patterns](https://arxiv.org/abs/2605.13850) - Taxonomy of agent topologies
- [Retrieval-Conditioned Topology Selection with Provable Budget Conservation for Multi-Agent Code Generation](https://arxiv.org/abs/2605.05657) - Adaptive topology selection

**Related Benchmarks:**
- [Understanding Multi-Agent LLM Frameworks: A Unified Benchmark](https://arxiv.org/abs/2602.03128) - Framework comparison
- [Agents-K1: Towards Agent-Native Knowledge Orchestration](https://arxiv.org/abs/2606.13851) - Knowledge coordination
- [SoftwareBench](https://arxiv.org/abs/2606.12008) - Software engineering multi-agent tasks

**Future Research Directions:**
1. **Dynamic orchestration**: How to compose agents at runtime based on task requirements?
2. **Recursive orchestration**: Multi-level manager-of-managers hierarchies for very large agent pools
3. **Orchestration fine-tuning**: Task-specific instruction-tuning for orchestration quality
4. **Human-in-the-loop management**: Enabling human supervisors to override or guide agent orchestration decisions in high-stakes scenarios

## References

- Xiong, K., Ji, H., Qiu, S., Zheng, Z., Xie, C., Ye, X., & Yao, H. (2026). ClawArena-Team: Benchmarking subagent orchestration and dynamic workflows in language-model agents. *arXiv preprint arXiv:2606.31174*.

- [Paper on arXiv (Abstract)](https://arxiv.org/abs/2606.31174)
- [Paper on arXiv (PDF)](https://arxiv.org/pdf/2606.31174)
- [Paper on arXiv (HTML)](https://arxiv.org/html/2606.31174)
