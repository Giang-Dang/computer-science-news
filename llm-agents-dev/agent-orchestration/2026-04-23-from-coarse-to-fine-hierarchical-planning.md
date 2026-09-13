# From Coarse to Fine: Self-Adaptive Hierarchical Planning for LLM Agents

**ArXiv ID:** [2604.23194](https://arxiv.org/abs/2604.23194)  
**Authors:** Haoran Tan, Zeyu Zhang, Chen Ma, Tianze Liu, Quanyu Dai, Xu Chen  
**Affiliations:** Renmin University of China, Huawei Noah's Ark Lab  
**Submission Date:** April 23, 2026  
**Last Updated:** April 23, 2026  

## Executive Summary

Current LLM agent planning approaches operate at a fixed granularity level—providing either excessive detail for simple tasks or insufficient detail for complex ones. This paper proposes AdaPlan-H (Adaptive Hierarchical Planning), a self-adaptive hierarchical planning mechanism inspired by human cognitive science that starts with coarse-grained macro plans and progressively refines them based on task complexity. The approach significantly improves task success rates while mitigating overplanning, offering practical flexibility for diverse multi-step decision-making challenges in software development automation.

## Problem Statement

### Fixed Granularity Limitations

Traditional LLM agent planning approaches suffer from a fundamental limitation:

- **Excessive Detail for Simple Tasks:** Over-planning leads to token waste, slower execution, and unnecessary complexity
- **Insufficient Detail for Complex Tasks:** Under-planning causes agents to miss critical dependencies, skip validation steps, and fail on complex reasoning

### Granularity Mismatch Challenge

```
Simple Task: "Write a hello world program"
├─ Fixed Coarse Plan: Too vague, missing execution details
├─ Fixed Fine Plan: Over-detailed, wastes tokens on unnecessary steps
└─ Adaptive Plan: Coarse → refines to fine as needed

Complex Task: "Implement a distributed caching system"
├─ Fixed Coarse Plan: Missing critical design decisions
├─ Fixed Fine Plan: Manageable, but token-expensive
└─ Adaptive Plan: Progressive refinement at optimal granularity
```

### Cognitive Science Foundation

Human planning exhibits self-adaptive hierarchical structure:

1. **Initial Phase:** High-level goal decomposition (coarse)
2. **Complexity Assessment:** Evaluate which subtasks need refinement
3. **Progressive Refinement:** Expand selected branches to fine-grained details
4. **Execution:** Interleave planning with execution, re-refining as needed

## Core Concepts & Theory

### Hierarchical Planning Architecture

AdaPlan-H operates on a three-level hierarchy:

**Level 1 - Macro Plan:** Abstract high-level goal decomposition
```
Goal: Implement user authentication module
├─ Design database schema
├─ Implement authentication API
├─ Create frontend login interface
└─ Integrate with main application
```

**Level 2 - Intermediate Plan:** Task-specific detail expansion
```
Implement authentication API
├─ Define API endpoints (login, logout, register)
├─ Implement JWT token generation
├─ Add password hashing mechanism
├─ Implement session management
└─ Add rate limiting
```

**Level 3 - Micro Plan:** Fine-grained execution steps
```
Implement JWT token generation
├─ Choose JWT library and version
├─ Define token payload structure
├─ Set expiration time policy
├─ Implement token refresh mechanism
├─ Add signature verification logic
└─ Handle token validation errors
```

### Self-Adaptive Refinement Mechanism

The key innovation is the **Complexity-Triggered Refinement** policy:

```
For each task in current plan:
  1. Estimate complexity:
     - Historical precedent (have we solved similar tasks?)
     - Information density (missing dependencies?)
     - Uncertainty level (known unknowns vs. unknown unknowns?)
  
  2. Decision rule:
     IF complexity > threshold:
       THEN expand to next level
       ELSE execute with current granularity
  
  3. Adaptive threshold:
     - Learned from successful/failed past trajectories
     - Adjusted per agent capabilities
     - Domain-specific calibration
```

### Theoretical Foundations

The approach combines:

1. **Hierarchical Task Networks (HTN):** Decomposing goals into subgoals
2. **Curiosity-Driven Learning:** Identifying high-uncertainty components
3. **Progressive Disclosure:** Gradually expanding details as needed
4. **Meta-Cognitive Loop:** Learning from success/failure patterns

## Main Ideas & Contributions

### Novel Adaptive Planning Framework

1. **Coarse-to-Fine Progression:** Starting simple, adding detail only when necessary
2. **Complexity-Driven Expansion:** Using task characteristics to determine refinement
3. **Interleaved Learning:** Improving the refinement policy through execution

### Key Mechanisms

**Complexity Scoring:**
- Lexical metrics: number of distinct entities, action vocabulary size
- Structural metrics: dependency graph complexity, branching factor
- Semantic metrics: alignment with known patterns vs. novelty

**Refinement Strategy:**
- Greedy expansion of highest-complexity tasks first
- Beam search over refinement decisions (explore alternative decompositions)
- Backtracking and re-planning when initial refinement proves insufficient

### Practical Benefits

For software engineering tasks:

| Task Type | Benefit |
|-----------|---------|
| Simple implementation (CRUD) | 40-60% reduction in planning tokens |
| Complex system design | 25-35% improvement in plan completeness |
| Multi-component integration | 20-30% better handling of edge cases |
| Debugging workflows | 35-45% faster root cause identification |

## Methodology & Implementation

### Experimental Setup

**Environments:**
- Code generation tasks (LeetCode-style programming)
- Software engineering tasks (system design, refactoring)
- Interactive instruction following (WebShop, AlfWorld)
- Complex planning (multi-step reasoning tasks)

**Baseline Comparisons:**
- Fixed coarse-grained planning
- Fixed fine-grained planning
- Chain-of-Thought without hierarchical structure
- Existing hierarchical planning (non-adaptive)

### Datasets and Benchmarks

**Code Generation:**
- LeetCode problems (various complexity levels)
- Real-world GitHub issues requiring code fixes
- Algorithm implementation tasks

**Software Engineering:**
- System design scenarios (design requirements → architecture)
- Codebase refactoring tasks
- Cross-module integration challenges

**Interactive Tasks:**
- WebShop: E-commerce task completion
- AlfWorld: Text-based household tasks
- Custom multi-step planning benchmarks

### Results and Analysis

**Task Success Rate Improvements:**

| Task Category | Fixed Coarse | Fixed Fine | AdaPlan-H | Improvement |
|----------------|-------------|-----------|-----------|-------------|
| Simple (5-10 steps) | 62% | 78% | 81% | +3-19pp vs baselines |
| Medium (10-20 steps) | 71% | 85% | 89% | +4-18pp |
| Complex (20+ steps) | 53% | 74% | 82% | +8-29pp |
| Very Complex (30+ steps) | 41% | 68% | 78% | +10-37pp |

**Token Efficiency:**

- Simple tasks: 35% reduction in planning tokens compared to fixed fine-grained
- Complex tasks: 15% increase in planning tokens but 25% increase in overall success rate
- Optimal token-efficiency ratio achieved at medium complexity levels

**Overplanning Mitigation:**

- Unnecessary refinement steps reduced by 45-60%
- False-positive refinements (refining tasks that don't need it) reduced from 28% to 8%
- Appropriate refinement rate increased from baseline 15% to 68-75%

### Qualitative Analysis

**Planning Quality Metrics:**

```
Plan Completeness (0-1 scale):
  Fixed Coarse:   0.54 ± 0.18
  Fixed Fine:     0.88 ± 0.12
  AdaPlan-H:      0.91 ± 0.10

Plan Efficiency (tokens/success):
  Fixed Coarse:   287 ± 95
  Fixed Fine:     402 ± 118
  AdaPlan-H:      321 ± 89 (best efficiency-quality tradeoff)
```

**Failure Mode Analysis:**

- Fixed coarse: 38% under-planning failures, 0% over-planning failures
- Fixed fine: 12% under-planning failures, 28% over-planning failures
- AdaPlan-H: 8% under-planning failures, 6% over-planning failures

## Practical Applications & Use Cases

### Software Development Automation

**Bug Fix Planning:**
```
Initial (Coarse): "Fix the bug in authentication module"
├─ Reproduce the issue
├─ Identify root cause
├─ Implement fix
└─ Verify solution

Adaptive Refinement (Medium): 
├─ Reproduce the issue
│  ├─ Run minimal test case
│  └─ Check error logs
├─ Identify root cause
│  ├─ Analyze stack trace
│  ├─ Check recent commits
│  └─ Review related code
├─ Implement fix
│  ├─ Update relevant functions
│  ├─ Add error handling
│  └─ Update tests
└─ Verify solution
   ├─ Run test suite
   ├─ Manual smoke tests
   └─ Performance regression check
```

**Code Refactoring:** Self-adaptive planning naturally fits refactoring workflows where complexity varies dramatically

**Testing Automation:** Test plan generation that automatically expands coverage requirements based on code complexity

### Integration Challenges

1. **Real-world Codebase Complexity:** Token budgets may exceed with complex systems
2. **Domain Knowledge:** Complexity scoring needs tuning per domain
3. **Interleaved Execution:** Coordination with actual code execution and feedback loops
4. **LLM Consistency:** Different models have varying planning capabilities

## Insights & Implications

### Impact on Agent Development

1. **Efficiency:** Reduced token consumption enables larger systems and longer horizons
2. **Quality:** Better balance between planning completeness and efficiency
3. **Robustness:** Adaptive approach handles diverse task types naturally
4. **Scalability:** Mechanism scales gracefully from simple to very complex tasks

### Cognitive Science Connection

The work validates the hypothesis that hierarchical, task-complexity-responsive planning mirrors human problem-solving effectiveness. This suggests LLM agents can benefit from mimicking cognitive science principles.

### Limitations

1. **Complexity Estimation:** Predicting task complexity remains challenging
2. **Domain Transfer:** Learned refinement policies may not transfer across domains
3. **Emergent Complexity:** Some tasks only reveal complexity during execution
4. **Optimization Trade-offs:** Optimal granularity may depend on LLM size/capability

## Future Research Directions

1. **Learning-Based Complexity Prediction:** Meta-learning complexity scoring from trajectories
2. **Online Refinement:** Adjusting granularity based on execution feedback
3. **Multi-LLM Hierarchies:** Different LLMs for different levels of the hierarchy
4. **Theoretical Analysis:** Formal guarantees on planning quality vs. efficiency
5. **Cross-Domain Adaptation:** Transfer learning for refinement policies

## Code & Resources

- **ArXiv Paper:** https://arxiv.org/abs/2604.23194
- **Paper PDF:** https://arxiv.org/pdf/2604.23194
- **GitHub Repository:** https://github.com/import-myself/AHP
- **Code Status:** Publicly available with Apache 2.0 license

**Citation:**
```bibtex
@article{tan2026coarse,
  title={From Coarse to Fine: Self-Adaptive Hierarchical Planning for LLM Agents},
  author={Tan, Haoran and Zhang, Zeyu and Ma, Chen and Liu, Tianze and Dai, Quanyu and Chen, Xu},
  journal={arXiv preprint arXiv:2604.23194},
  year={2026}
}
```

## Related Work & Context

### Related Papers on Planning

- **Hierarchical Planning:** [Learning and Reusing Policy Decompositions for Hierarchical Generalized Planning with LLM Agents](https://arxiv.org/abs/2605.07145)
- **Task Decomposition:** [Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory](https://arxiv.org/abs/2606.08247)
- **Long-Horizon Reasoning:** [Think Anywhere in Code Generation: Interleaved Reasoning for Adaptive LLM Problem-Solving](https://arxiv.org/abs/2603.26198)
- **Self-Correction:** [Self-Corrective Task Planning by Inverse Prompting with Large Language Models](https://arxiv.org/abs/2503.07317)

### Foundational Concepts

- Hierarchical Task Networks (HTN Planning)
- Progressive disclosure UI patterns
- Cognitive science of hierarchical planning
- Meta-learning and learning-to-learn

## References & Further Reading

1. Tan, H., et al. (2026). "From Coarse to Fine: Self-Adaptive Hierarchical Planning for LLM Agents," arXiv:2604.23194
2. Sacerdoti, E. D. (1974). "Planning in a hierarchy of abstraction spaces"
3. Cognitive science literature on hierarchical problem-solving
4. Related work on decomposition and abstraction in AI planning
