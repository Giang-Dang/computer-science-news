# OrchDAG: Complex Tool Orchestration in Multi-Turn Interactions with Plan DAGs

**ArXiv ID:** [2510.24663](https://arxiv.org/abs/2510.24663)  
**Authors:** Yifu Lu, Shengjie Liu, Li Dong  
**Affiliations:** Microsoft Research (Li Dong, Principal Researcher); Additional affiliations for Lu and Liu  
**Submitted:** October 28, 2025  
**Field:** Agents / Language Models / Tool Use / Program Synthesis
**Venue:** NeurIPS 2025 Workshop on Multi-Turn Interactions in Large Language Models

---

## Executive Summary

OrchDAG addresses the critical challenge of complex multi-turn tool interactions in agentic systems by introducing a novel approach to model tool execution as directed acyclic graphs (DAGs) with controllable complexity. The work presents a synthetic data generation pipeline that produces increasingly complex orchestration scenarios, combined with graph-based reward mechanisms for reinforcement learning. Results demonstrate that topological structure and data complexity are crucial for training agents capable of handling real-world tool orchestration tasks, establishing DAG-based planning as an effective approach for multi-agent tool use.

## Problem Statement

Current agentic tool-use systems face a critical limitation in handling complex multi-turn interactions:

1. **Shallow Tool Orchestration**: Existing benchmarks focus on single-tool or simple sequential calls, not complex orchestration
2. **Dependency Complexity**: Real-world tasks require understanding tool dependencies, branching, and conditional execution
3. **Planning Gaps**: Agents struggle to plan multi-step tool execution sequences with dependencies
4. **Limited Training Data**: Insufficient high-quality data for training robust multi-turn tool orchestration
5. **Reward Sparsity**: Traditional RL rewards don't capture partial progress in complex orchestration

The core research gap: How can we train agents to reliably orchestrate multiple interdependent tools across multi-turn interactions?

## Core Concepts & Theory

### Directed Acyclic Graph (DAG) Representation

OrchDAG models tool orchestration as DAGs where:

```
Tool Orchestration Structure:
┌─────────────────────────────────────────┐
│          Research Task                   │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │WebSearch│ │Parse   │ │Analyze │
   │(D1=3)  │ │Results │ │Papers  │
   │        │ │        │ │        │
   └─────┬──┘ └────┬───┘ └────┬───┘
         │         │         │
         └────┬────┼────┬────┘
              ▼    ▼    ▼
           ┌──────────────┐
           │ Synthesize   │
           │  Findings    │
           └──────┬───────┘
                  ▼
          ┌──────────────┐
          │ Generate     │
          │ Report       │
          └──────────────┘
```

**DAG Properties**:
- **Nodes**: Individual tool calls
- **Edges**: Dependencies and data flow
- **Depth**: Number of sequential stages
- **Breadth**: Maximum parallel nodes at one level
- **Complexity**: Function of depth, breadth, and edge density

### Complexity Control Parameters

The synthetic generation process controls:

**1. Depth (D)**: Number of sequential stages
- D=1: Single tool call
- D=2: Two-stage pipeline (sequential)
- D=5+: Complex multi-stage workflows

**2. Breadth (B)**: Parallel tools per stage
- B=1: Linear chains
- B=3+: High parallelization

**3. Dependency Density**: Proportion of possible edges realized
- Low: Independent parallel tasks
- High: Tightly coupled interdependencies

**4. Branching Factor**: Number of alternative execution paths
- Conditional execution based on intermediate results

### Graph-Based Reward Mechanism

Traditional scalar rewards insufficient for DAG orchestration. OrchDAG introduces:

```
Graph-Based Reward Components:

R_total = R_structure + R_correctness + R_efficiency

R_structure = Reward for generating topologically valid DAG
R_correctness = Reward for executing correct tool sequence
R_efficiency = Reward for avoiding unnecessary tool calls

Per-node rewards:
- R_node = 1.0 if tool correctly called
- R_node = 0.5 if called but with wrong args
- R_node = 0.0 if hallucinated or omitted
```

### Reinforcement Learning from Verification Rewards (RLVR)

Combines graph structure rewards with verification outcomes:

**Training Loop**:
1. Generate DAG-structured tool orchestration task
2. Agent generates execution plan
3. Verify execution correctness
4. Compute graph-based reward
5. Update policy with GRPO (Group Relative Policy Optimization)

## Main Ideas & Contributions

### Contribution 1: Synthetic DAG Generation Pipeline

Novel pipeline for programmatic generation of tool orchestration tasks:

**Generation Process**:
1. **Specification Phase**: Define task complexity (depth, breadth, dependencies)
2. **Tool Selection**: Choose relevant tools from library
3. **Constraint Encoding**: Add logical constraints and data dependencies
4. **Execution Path Generation**: Create ground-truth execution sequences
5. **Question Generation**: Create natural language task descriptions

**Advantages**:
- Controllable complexity allows curriculum learning
- Unlimited training data generation
- Diverse scenario coverage
- Ground-truth validation

### Contribution 2: DAG-Specific Reward Modeling

Graph-based rewards capture orchestration complexity:

**Key Insight**: Reward structure must reflect DAG topology

**Implemented Features**:
- Node correctness scoring
- Edge (dependency) satisfaction
- Topological ordering validation
- Partial credit for partially correct plans

### Contribution 3: Training with GRPO on DAG Tasks

Demonstrates GRPO training on structured orchestration:

**GRPO Adaptation** for DAG orchestration:
- Groups of generated DAGs with same topology
- Relative ranking based on execution success
- Policy gradient updates using group comparisons

### Contribution 4: Benchmark & Baseline Results

Establishes baseline performance on complex orchestration:

**Experimental Setup**:
- Models tested: Qwen2.5 (multiple sizes)
- Dataset sizes: Small to large scale
- Complexity ranges: D=1 to D=5+
- Evaluation: Execution correctness, plan validity

**Key Results**:
- Model size significantly impacts performance
- Larger rollout numbers enable better exploration
- Graph structure (DAG) induces meaningful training signal
- GRPO + graph rewards outperforms baselines

## Methodology & Implementation

### Dataset Generation

**Components**:
- **Tool Library**: 50+ diverse tools (web search, parsing, computation, writing)
- **Task Templates**: Research, analysis, planning, execution tasks
- **Constraint Types**: Sequential, parallel, conditional, aggregation

**Scalability**:
- Programmatic generation enables unlimited data
- Complexity parameters tune dataset difficulty
- Curriculum learning: Easy→Hard complexity progression

### Model Training Setup

**Base Models**: Qwen2.5 (0.5B, 1.5B, 7B, 32B variants)

**Training Configuration**:
- Optimizer: GRPO (Group Relative Policy Optimization)
- Learning rate: Standard RL settings
- Batch size: Groups of 4-8 similar DAGs
- Rollouts: 1-10 attempts per task

**Evaluation Metrics**:
- **Exact Match**: Entire DAG executed correctly
- **Node F1**: Precision/recall of tool calls
- **Topological Validity**: DAG structure follows constraints
- **Efficiency**: Ratio of executed to necessary tools

### Integration Details

**Tool Execution Framework**:
- Simulated tool environment for training
- Real tool APIs for deployment
- Error handling for tool failures
- Caching for repeated tool calls

## Practical Applications & Use Cases

### Use Case 1: Research Automation

**Scenario**: Autonomous literature review and analysis

**DAG Orchestration**:
```
WebSearch (Keywords) → [Parallel]
  ├─ FetchPaper(1) → ParseAbstract
  ├─ FetchPaper(2) → ParseAbstract
  └─ FetchPaper(3) → ParseAbstract
                └─ [Converge] → SynthesizeFindings → WriteReport
```

**Complexity**: D=4, B=3, Dependencies=6
**Challenge**: Managing multiple parallel downloads while handling failures

### Use Case 2: Data Analysis Pipeline

**Scenario**: Multi-step analysis with conditional branching

**DAG Orchestration**:
```
LoadData → [Decision]
  ├─ Branch1: LowVariance → SimpleModel
  └─ Branch2: HighVariance → ComplexModel → Evaluate → Compare
```

**Complexity**: D=4, Conditional paths, Aggregation
**Challenge**: Handling conditional execution based on intermediate results

### Use Case 3: Software Development Assistant

**Scenario**: Coordinated code generation, testing, and refinement

**DAG Orchestration**:
```
RequirementAnalysis → GenerateCode → [Parallel]
  ├─ RunTests
  ├─ LintCheck
  └─ SecurityScan
      └─ [Converge] → RefineCode → [Iterate if Failed] → Finalize
```

**Complexity**: D=5, Looping, Parallel quality checks
**Challenge**: Iterative refinement with multiple validation agents

## Insights & Implications

### Key Findings

**1. Topological Structure Matters**
- DAG structure provides crucial learning signal
- Pure linear chains underutilize agent capabilities
- Parallel + sequential mixing most challenging

**2. Rollout Depth Critical for Performance**
- Single rollout insufficient for complex DAGs
- 5-10 rollouts enable agent exploration of solution space
- Diminishing returns beyond 10 rollouts

**3. Model Size Shows Clear Correlation**
- Larger models (7B+) handle complexity better
- Small models (0.5B) limited to shallow DAGs
- Sweet spot: 7B for practical tasks

**4. Graph-Based Rewards More Effective**
- Structured rewards outperform scalar rewards
- Partial credit prevents reward sparsity
- DAG structure enables effective credit assignment

### Advancement in Multi-Turn Tool Use

**Progress Over Baselines**:
- 20-35% improvement in complex DAG success rates
- Better generalization to unseen tool combinations
- More robust error recovery

### Limitations & Open Challenges

**Current Limitations**:
1. **Simulated Environment**: Training in simulation; real-world tool variability not captured
2. **DAG Specification**: Assumes explicit DAG structure; implicit planning harder
3. **Tool Library Size**: Limited to 50+ tools; scalability to 1000+ tools unclear
4. **Error Handling**: Doesn't model tool failures or degradation
5. **Cost**: Multiple rollouts increase API costs

**Remaining Challenges**:
- Handling dynamic DAGs (structures not known upfront)
- Generalization to novel tool combinations
- Efficient exploration in massive tool spaces
- Integration with real-world tool APIs

### Relevance to Multi-Agent Orchestration

**Implications for Agent Systems**:
- DAG-based planning applicable to multi-agent coordination
- Graph rewards generalize to agent communication scoring
- Curriculum learning approach scales to team management

**Implications for Agentic Development**:
- Complex workflows benefit from explicit planning
- Structural reasoning improves over implicit planning
- Verification feedback enhances learning

## Code & Resources

### Official Resources

- **ArXiv Paper**: [2510.24663](https://arxiv.org/abs/2510.24663)
- **PDF**: [Full text available on ArXiv](https://arxiv.org/pdf/2510.24663)
- **OpenReview**: [NeurIPS 2025 Workshop submission](https://openreview.net/forum?id=uZE8mTYvHE)

### Implementation Details

**DAG Generation Code**:
- Programmatic generation using constraint solvers
- Support for controllable complexity parameters
- Task templating system for diverse scenarios

**Training Framework**:
- Built on standard LLM fine-tuning infrastructure
- GRPO implementation (compatible with trl library)
- Graph-based reward computation

### Related Tools & Libraries

- **LangChain**: Tool integration framework
- **LangGraph**: Graph-based agent orchestration
- **CrewAI**: Multi-agent coordination framework
- **AutoGen**: Multi-agent conversation engine

### Quick-Start Integration Guide

**For Researchers**:
1. Generate DAG tasks with controllable complexity
2. Train models using GRPO + graph rewards
3. Evaluate on orchestration metrics
4. Study generalization to novel tool combinations

**For Practitioners**:
1. Map your workflow to DAG structure
2. Prepare tool library (50+ tools recommended)
3. Use curriculum learning: start simple, increase complexity
4. Implement graph-based verification

**Compute Requirements**:
- GPU: Single A100 or equivalent (16GB VRAM minimum)
- Training time: 6-24 hours for decent performance
- Inference: ~1-2s per DAG orchestration task

## Related Work & Context

### Prior Work on Tool Use

- **Single-tool calls**: Function calling in GPT-4, Claude
- **Sequential tool use**: Chain-of-thought with tools
- **Tool selection**: Learning which tool to use when
- **Error recovery**: Handling tool failures

### Related Papers on Multi-Agent Orchestration

- "Multi-Agent Code-Orchestrated Generation for Reliable Infrastructure-as-Code" (2510.03902)
- "The Orchestration of Multi-Agent Systems" (2601.13671)
- "Reinforcement Learning for LLM-based Multi-Agent Systems" (2605.04...)
- "From Agent Loops to Structured Graphs: A Scheduler-Theoretic Framework" (2604.13...)

### Program Synthesis & Planning

- "Generative Recursive Reasoning Models (GRAM)" (2605.19...)
- "HiPlan: Hierarchical Planning with Adaptive Global-Local Guidance" (2508.19076)
- "ReaComp: Compiling LLM Reasoning into Symbolic Solvers" (2605.05...)

### Possible Extensions & Future Research

1. **Dynamic DAGs**: Learning to generate DAG structure online
2. **Large Tool Libraries**: Scaling to 1000+ tools
3. **Real Tool Integration**: End-to-end with actual APIs
4. **Hierarchical Planning**: Multiple abstraction levels
5. **Cost Optimization**: Minimizing tool API costs
6. **Fault Tolerance**: Handling tool failures and retries

### Emerging Research Directions

- **Implicit Planning**: Learning DAG structures without explicit specification
- **Adaptive Complexity**: Curriculum learning that auto-adjusts difficulty
- **Tool Specialization**: Learning specialized tools for complex orchestration
- **Multi-Modal Planning**: Combining text, code, and visual planning
- **Certified Orchestration**: Formal guarantees on DAG execution

