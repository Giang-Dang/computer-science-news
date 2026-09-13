# CoRe-Code: Collaborative Reinforcement Learning for Code Generation

**Paper:** [CoRe-Code: Collaborative Reinforcement Learning for Code Generation](https://arxiv.org/abs/2605.24812)

**ArXiv ID:** 2605.24812

**Authors:** Zhihao Dou, Qinjian Zhao, Zhongwei Wan, Xiaoyu Xia, Sumon Biswas

**Submission Date:** May 24, 2026

**Research Focus:** Multi-agent code generation, reinforcement learning for agent coordination, role-specialized LLM agents, planner-coder paradigm, collaborative learning

---

## Executive Summary

CoRe-Code introduces a **role-specialized multi-agent framework** that enhances inter-agent coordination for more accurate and efficient code generation through collaborative reinforcement learning. The framework adopts a simple yet effective **Planner-Coder paradigm**, where the Planner produces high-level code architecture and plans, and the Coder executes plans to generate detailed code. CoRe-Code leverages **Group Relative Policy Optimization (GRPO)**—a collaborative RL stage—to refine role specialization and agent alignment, enabling agents to learn from each other's strengths.

**Key Results:**
- Outperforms single-agent baselines and existing RL-based multi-agent methods
- Generalizes to other multi-agent frameworks (with Retrieval agents, Debugging agents)
- Reduces locally coherent yet globally suboptimal solutions (e.g., failing tests, inefficient complexity)

**Significance to Agent-Driven Development:** This work demonstrates that multi-agent code generation benefits from **collaborative learning**—agents can improve through reinforcement learning feedback on inter-agent interactions, not just individual task performance. The framework is practical and adaptable, suggesting a path toward self-improving multi-agent development systems.

---

## Problem Statement

**Development Automation Challenge:**
Large language models (LLMs) have achieved strong performance in code generation, reaching high success rates on benchmarks like HumanEval and MBPP. However, most approaches rely on **autoregressive decoding without global planning**, leading to locally coherent yet globally suboptimal solutions. Examples:

- Generated code passes unit tests (local coherence) but uses inefficient algorithms (global suboptimality)
- Code is syntactically correct but fails edge cases because the planner didn't consider them
- Multi-step code generation produces sequential code without architectural coherence

**Prior Multi-Agent Limitations:**
- **Simple Multi-Agent Systems:** Round-robin agent composition (agent A does step 1, agent B does step 2) without learning to improve coordination
- **Existing RL-Based Methods:** Apply RL to individual agent actions, not to inter-agent coordination
- **Missing Collaborative Learning:** Agents operate independently; no mechanism for learning from each other's performance

**Research Gap:**
A collaborative multi-agent framework where agents with distinct roles (planner, coder, debugger, retriever) **learn from each other's performance** through reinforcement learning was needed to improve global code quality and architectural coherence.

---

## Core Concepts & Theory

### Role-Specialized Agent Paradigm

**Multi-Agent Decomposition:**
CoRe-Code decomposes code generation into specialized roles:

```
┌─────────────────────────────────────────┐
│          Planner Agent                  │
│  (High-level design, architecture)      │
│  Output: Code plan, algorithm choice    │
└────────────────┬────────────────────────┘
                 │ (Plan: "Use BST for O(log n) lookup")
                 ▼
┌─────────────────────────────────────────┐
│          Coder Agent                    │
│  (Detailed implementation)              │
│  Input: Plan from Planner               │
│  Output: Executable code                │
└────────────────┬────────────────────────┘
                 │
                 ▼
         [Test & Evaluation]
         Passes tests? ✓ → Submit
                      ✗ → Feedback to agents
```

**Role Differentiation:**

| Role | Specialization | Input | Output | Success Metric |
|------|---|---|---|---|
| **Planner** | Algorithm design, architecture selection | Problem specification | High-level plan, design decisions | Plan is feasible, optimal algorithm chosen |
| **Coder** | Syntax, implementation details | Plan from Planner | Clean, correct code | Code passes tests, efficient |
| **Debugger** (optional) | Error analysis, fix generation | Failed tests, error trace | Bug fixes | Fixed code passes tests |
| **Retriever** (optional) | Knowledge retrieval, context | Problem description | Relevant examples, patterns | Retrieved context aids generation |

### Collaborative Learning via Group Relative Policy Optimization (GRPO)

**Traditional RL for Single Agents:**
Individual agents learn to maximize reward for their own actions:
```
Reward = score(agent_output)
Agent learns: maximize individual score
```

**Collaborative RL for Multi-Agents:**
CoRe-Code uses **Group Relative Policy Optimization** to learn inter-agent alignment:

```
Reward = score(final_code)  // Evaluated on entire system output

Planner learns: "Does my plan help Coder generate good code?"
Coder learns: "Does following this plan produce correct code?"

Agents adjust policies collaboratively based on final code quality.
```

**GRPO Algorithm (Simplified):**
1. **Collect Trajectories:** Run Planner → Coder pipeline multiple times with different LLM samples
2. **Evaluate:** Test generated code against test cases; score each trajectory
3. **Group Reward:** Compare group performance: did this team of agents (at these policy settings) produce good code?
4. **Policy Update:** Update Planner and Coder policies to maximize group reward
5. **Iterate:** Repeat until convergence

**Key Property:** Agents learn to specialize—Planner focuses on feasible, optimal plans; Coder focuses on clean, efficient implementation—because coordinated specialization maximizes group reward.

### Architecture Coherence & Global Optimization

**Problem Addressed:**
Autoregressive code generation optimizes locally (each token conditioned on prior tokens) but not globally (overall code architecture). This produces:

```
Local coherence, global suboptimality:
- Each line is valid Python
- Code passes basic tests
- Algorithm is O(n³) instead of optimal O(n log n)
- No consideration of user requirements for efficiency
```

**Solution: Planning Stage:**
Planner **commits to an algorithm and architecture before Coder generates tokens**. This enforces global constraints:

```
PLANNER OUTPUT:
"Algorithm: Binary search tree for efficient lookup
Data structure: BST node with left, right pointers
Complexity target: O(log n) for search, insert"

CODER OUTPUT:
Generates code consistent with plan
All decisions aligned to architecture

RESULT: Global optimization (architecture reflects complexity target)
```

### GRPO-Based Refinement

**Reinforcement Learning Loop:**

```
Iteration 1:
├─ Planner generates plan for problem
├─ Coder implements plan
├─ Code tested: 60% pass rate
└─ GRPO: Reward = 0.6; agents update policies

Iteration 2 (with updated Planner policy):
├─ Planner generates improved plan (learned which plans lead to good code)
├─ Coder implements plan
├─ Code tested: 75% pass rate
└─ GRPO: Reward = 0.75; further policy refinement

... (iterate until convergence or diminishing returns)
```

**What Agents Learn:**
- **Planner learns:** Which algorithm choices, architectural patterns, and design decisions lead to code that Coder can implement successfully
- **Coder learns:** How to best implement diverse architectural plans with high quality
- **System learns:** Which (Planner, Coder) policy combinations generalize well across different problem types

---

## Main Ideas & Contributions

### 1. Multi-Agent Framework Outperforms Single-Agent Baselines

**Contribution:** CoRe-Code's Planner-Coder approach surpasses single-agent code generation, even with the same total model capacity.

**Why It Works:**
- **Separation of Concerns:** Planner specializes in high-level design (requires broad knowledge of algorithms, patterns)
- **Reduced Token Pressure:** Coder doesn't need to "think out loud" about architecture; can focus on clean implementation
- **Error Recovery:** If Plan is suboptimal, Coder has room to adapt; if implementation has issues, Plan can guide correction

**Empirical Results:**
[Exact figures unavailable — see full paper]

CoRe-Code outperforms:
- Single-agent baseline (same total model calls)
- Other multi-agent methods without collaborative learning (e.g., sequential agent composition)
- RL-based single-agent methods (e.g., PPO on individual agent policies)

### 2. Collaborative RL Improves Inter-Agent Coordination

**Key Insight:** Simply running agents sequentially (Planner → Coder) provides moderate benefits. **Collaborative RL dramatically improves performance** by training Planner and Coder to understand each other.

**GRPO Advantage:**
- **Without GRPO:** Planner and Coder have no feedback loop; Planner doesn't know which plans are implementable; Coder doesn't know how to handle unclear plans
- **With GRPO:** Agents learn from group performance; Planner learns to generate implementable plans; Coder learns to leverage high-level plans

**Mechanism:**
GRPO groups agent actions into trajectories (Planner step + Coder step) and assigns group reward (based on code quality). This creates:
- **Indirect learning:** Planner learns "this plan type works well with this Coder"
- **Specialization:** Agents develop complementary strengths (Planner gets good at planning; Coder gets good at implementation)

### 3. Generalization to Other Agent Roles

**Contribution:** CoRe-Code architecture generalizes beyond Planner-Coder. Experiments show gains when extending to:

```
Original:  Planner → Coder
Extended:  Planner → Coder → Debugger (debugs failed tests)
Extended:  Planner → Retriever → Coder (retriever provides examples)
Extended:  Planner → Coder → Coder (two coding passes)
```

**Generalization Result:** GRPO-based collaborative learning improves coordination for any multi-agent pipeline, not just Planner-Coder.

**Implication:** The framework is a general recipe for multi-agent code generation systems:
1. Decompose into specialized roles
2. Define role interfaces (Planner output → Coder input)
3. Apply GRPO to learn inter-agent policies
4. Extend with additional roles as needed

### 4. Efficient Code Generation with Global Optimization

**Result:** CoRe-Code generates **more efficient code** than autoregressive baselines, even on the same model size.

**Example Problem:** "Implement efficient search in a list of 1M items"

**Autoregressive Single-Agent:**
```python
def search(items, target):
    for item in items:  # ← O(n) without plan
        if item == target:
            return True
    return False
```

**CoRe-Code with Plan:**
```
PLAN: "Use binary search for O(log n) efficiency"

def search(items, target):
    left, right = 0, len(items) - 1
    while left <= right:  # ← O(log n) from plan
        mid = (left + right) // 2
        if items[mid] == target:
            return True
        elif items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False
```

**Performance Impact:**
- Single-agent: Correct but inefficient (O(n))
- CoRe-Code: Correct and efficient (O(log n)) due to planning stage

### 5. Scalability to Complex Architectures

**Finding:** CoRe-Code handles complex, multi-file code generation by having Planner design module structure and Coder implement modules collaboratively.

**Architecture Example:**
```
PLANNER OUTPUT:
"Architecture:
  - Module 1: Data layer (classes for storage)
  - Module 2: Business logic (processing functions)
  - Module 3: API layer (endpoints)
Dependencies: Module 1 → Module 2 → Module 3"

CODER IMPLEMENTATIONS:
  - Generate Module 1 code (data models)
  - Generate Module 2 code (logic using Module 1 interfaces)
  - Generate Module 3 code (API using Module 2 functions)
  - All modules integrate correctly due to plan
```

**Result:** Multi-file code generation maintains consistency and reduces integration bugs.

---

## Methodology & Implementation

### Framework Architecture

**Pipeline:**
```
Problem Specification
        ↓
   [Planner Agent]
   Generates Plan
        ↓
   [Coder Agent]
   Generates Code
        ↓
   [Test Suite]
   Evaluates Code
        ↓
   [GRPO Training]
   Updates Planner & Coder Policies
        ↓
   [Repeat for N iterations]
```

### GRPO Training Details

**Sampling Phase:**
1. Sample multiple (Planner, Coder) policy pairs
2. For each pair: generate plan + code for problem
3. Test code; record pass/fail

**Optimization Phase:**
1. Compute group reward: (# tests passed) / (total tests)
2. Estimate policy gradient: how much did each agent's action contribute to group reward?
3. Update Planner policy: maximize reward for plan generation
4. Update Coder policy: maximize reward for code generation given plan
5. Iterate

**Hyperparameters:**
[Exact values unavailable — see full paper]
- Learning rate, batch size, number of GRPO iterations
- Number of plan samples per problem
- Reward function (simple: pass rate, or complex: pass rate + code quality metrics)

### Experimental Setup

**Benchmarks:**
- **HumanEval:** Classic code generation benchmark (164 problems)
- **MBPP (Mostly Basic Programming Problems):** Harder benchmark (1000 problems)
- **Additional:** Custom benchmarks focusing on algorithm efficiency, multi-file code

**Baselines:**
1. Single-agent LLM (e.g., GPT-4, Claude)
2. Sequential multi-agent (Planner → Coder, no collaborative learning)
3. Existing RL-based code generation methods
4. Domain-specific code synthesis tools (if applicable)

### Metrics & Results

**Performance Metrics:**

[Exact figures unavailable — see full paper]

Likely evaluated on:
- **Pass@k:** Percentage of problems solved within k attempts
- **Time to Solution:** Agent runtime until correct code
- **Code Quality:** Efficiency (complexity analysis), readability (cyclomatic complexity), maintainability (lines of code)
- **Generalization:** Performance on out-of-distribution problems

**Key Results:**
- CoRe-Code achieves higher pass@k than baselines
- Pass@1 (single generation) may be lower, but pass@3 or pass@5 significantly higher due to GRPO iterations
- Efficiency (algorithmic complexity) improves notably
- Generalization to new problem types is better than pure RL-based single-agent methods

### Ablation Studies

Likely explored:
- **Effect of GRPO:** With GRPO vs. without (sequential agents, no collaborative learning)
- **Role Sensitivity:** Performance with different agent roles (Planner + Coder vs. Planner + Coder + Debugger)
- **Plan Quality:** Sensitivity to Planner quality (does a weak Planner hurt Coder?)
- **Training Data:** How much collaborative training is needed before convergence?

---

## Practical Applications & Use Cases

### 1. Self-Improving Code Generation Systems

**Use Case:** Build a code generation system that improves over time through collaborative RL.

**Deployment Architecture:**
```
┌────────────────────────────────────────┐
│ Code Generation Serving                │
│ ┌──────────────────────────────────┐   │
│ │ Planner Agent (v2.1)             │   │ (Real-time)
│ │ Coder Agent (v2.1)               │   │
│ │ Collaborative policies (v2.1)    │   │
│ └──────────────────────────────────┘   │
└────────────┬───────────────────────────┘
             │ (Collect generations & test results)
             ▼
┌────────────────────────────────────────┐
│ Offline GRPO Training Pipeline         │
│ ┌──────────────────────────────────┐   │ (Daily batch)
│ │ Aggregate 10k problem-solution   │   │
│ │ pairs from production            │   │
│ │ Run GRPO: update Planner & Coder │   │
│ │ policies                         │   │
│ │ Evaluate on test suite           │   │
│ └──────────────────────────────────┘   │
└────────────┬───────────────────────────┘
             │ (New policies v2.2)
             ▼
      [Deploy updated agents]
```

**Benefits:**
- System improves from real-world usage data
- Collaborative RL ensures agents specialize based on observed success
- Feedback loop: policy v2.1 generates code → test results → GRPO learns → policy v2.2 deployed

### 2. Multi-Agent Code Orchestration

**Application:** Build larger systems with specialized agents for different code domains.

```
Problem Specification
     ↓
Planner (general: architecture)
     ├─→ Retriever (fetch relevant examples)
     └─→ Coder_ML (if plan includes ML)
     └─→ Coder_Web (if plan includes web components)
     └─→ Coder_Systems (if plan includes systems code)
```

**Collaborative Learning Benefit:**
- Planner learns which plans align well with each specialized Coder
- Specialized Coders learn to work well with Planner's high-level designs
- Multi-agent orchestration becomes adaptive

### 3. Developer Workflow Integration

**Use Case:** IDE plugin that suggests code with explainable plans.

```
Developer: "Generate a function to find duplicates in O(n)"

SYSTEM OUTPUT:
Plan: "Use hash set for O(1) lookups; single pass through list"

def find_duplicates(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return duplicates

Developer can:
- Review plan before accepting code
- Reject plan and ask for alternative algorithm
- Accept code confident in algorithm choice (plan was explicit)
```

**Advantage Over Autoregressive:** Developer sees reasoning (plan) not just output (code), improving trust and editability.

### 4. Code Refactoring & Optimization

**Application:** Agent system to refactor and optimize existing code.

```
Input: Legacy code (e.g., O(n²) sort)
       Problem spec (refactor for O(n log n) performance)

Planner: "Replace bubble sort with quicksort architecture"
Coder:   "Implement quicksort based on plan"
Result:  Refactored, optimized code

GRPO learns: which refactoring plans (vs. specific algorithms) 
are most effective and easiest for Coder to implement
```

---

## Insights & Implications

### 1. Specialization Through Collaborative Learning

**Insight:** Multi-agent systems don't automatically specialize; they need collaborative learning. Without GRPO, Planner might generate poor plans, and Coder might waste effort adapting. With GRPO, both agents learn optimal specialization.

**Theoretical Implication:** In multi-agent systems, agent roles should be learned (via RL) not manually assigned. Collaborative RL discovers optimal role boundaries.

### 2. Architecture-Aware Code Generation

**Finding:** Planning stages enable global architectural optimization, not achievable through autoregressive token-by-token generation. Multi-agent code generation should include an explicit planning stage.

**Architectural Principle:** For complex code generation, decompose into:
```
Design Phase → Implementation Phase → Verification Phase
(Planner)       (Coder)                (Debugger/Tester)
   ↓                ↓                       ↓
  GRPO-trained collaborative agent team
```

### 3. Generalization & Extensibility

**Finding:** GRPO-based collaboration generalizes to new roles (Debugger, Retriever, Optimizer). This suggests a general framework for multi-agent code systems:
1. Define agent roles & interfaces
2. Apply GRPO to train collaboration
3. Extend with new roles as needed

**Implication for Agent Ecosystem:** Multi-agent code generation is not a one-off engineering problem but a learning problem. Agents should be trained collaboratively, not built sequentially.

### 4. Efficiency Gains from Global Planning

**Observation:** CoRe-Code generates more efficient algorithms (better time complexity) than autoregressive baselines. This is because Planner commits to algorithms before implementation. Coder must follow plan → enforces optimality goals.

**Practical Implication:** Agentic systems optimizing for code efficiency should include planning stages with explicit complexity budgets (e.g., "Target O(n log n) or better").

### 5. Scalability to Multi-Agent Ecosystems

**Insight:** As code generation systems expand (more agents for retrieval, debugging, optimization), collaborative RL (GRPO) becomes critical. Without it, agents might interfere with each other. With it, agents specialize and cooperate.

**Vision:** Future agentic development systems might look like:
```
10+ specialized agents (design, implement, test, optimize, deploy, monitor)
Each trained via GRPO to maximize system-level code quality
Agents adapt roles based on problem type & learned optimal configurations
```

---

## Code & Resources

### Paper Access
- **ArXiv:** https://arxiv.org/abs/2605.24812
- **PDF:** https://arxiv.org/pdf/2605.24812

### Framework Implementation

**Likely Components:**

```python
# Pseudo-code structure
class PlannerAgent:
    def generate_plan(problem_spec: str) -> Plan:
        # LLM call with planning prompt
        # Output: high-level algorithm, architecture, complexity target
        pass

class CoderAgent:
    def generate_code(plan: Plan, problem_spec: str) -> Code:
        # LLM call conditioned on plan
        # Output: executable code following plan
        pass

class CoReCodeSystem:
    def train_collaborative(problems, iterations=100):
        for _ in range(iterations):
            # Collect trajectories
            trajectories = []
            for problem in problems:
                plan = planner.generate_plan(problem)
                code = coder.generate_code(plan, problem)
                reward = test_code(code)
                trajectories.append((plan, code, reward))
            
            # GRPO: update both agents' policies
            self.grpo_update(trajectories)
    
    def generate_code(problem_spec: str) -> Code:
        plan = planner.generate_plan(problem_spec)
        code = coder.generate_code(plan, problem_spec)
        return code
```

### RL Library Integration

**Compatible Frameworks:**
- **Ray RLlib:** Multi-agent RL training; can implement GRPO for agent teams
- **Anthropic SDK / LangChain:** Multi-agent orchestration; can integrate CoRe-Code pipeline
- **Custom Training Loop:** Straightforward to implement GRPO: collect trajectories, compute group rewards, backprop through agent policies

### Prompt Design for Planner & Coder

**Planner Prompt Template:**
```
You are a code architect planning code generation.

Given this problem:
{problem_specification}

Generate a high-level plan including:
1. Algorithm choice (with complexity analysis)
2. Data structures to use
3. Module architecture (if multi-file)
4. Edge cases to handle

Plan format:
ALGORITHM: [name, complexity]
DATA_STRUCTURES: [list]
ARCHITECTURE: [module breakdown]
EDGE_CASES: [list]
```

**Coder Prompt Template:**
```
You are implementing code according to a plan.

Problem: {problem_specification}
Plan: {plan_from_planner}

Implement code that:
1. Follows the algorithm specified in the plan
2. Uses the data structures from the plan
3. Handles edge cases listed in the plan

Code:
[generate code]
```

### Integration Guidance

**For LLM-Based Development Systems:**
1. **Separate Planning from Implementation:** Design phase produces explicit plans; implementation phase follows plans
2. **Collaborative Training:** Use GRPO or similar collaborative RL to train agents to work well together
3. **Test Feedback Loop:** Route test results back to RL training; agents learn from failures
4. **Extensibility:** Add new agent roles (Debugger, Optimizer) and retrain collaboratively

**For Enterprise Deployment:**
1. **Offline Training:** Run GRPO training on accumulated code generation data (daily batch)
2. **A/B Testing:** Deploy new agent policies alongside old ones; measure improvement
3. **Monitoring:** Track pass rate, code efficiency, developer satisfaction; feed back to training
4. **Custom Specialization:** Fine-tune agents on domain-specific problems (e.g., infrastructure-as-code)

---

## Related Work & Context

### Multi-Agent Code Generation

- **AutoGen (Microsoft, 2023):** General multi-agent conversation framework; CoRe-Code specializes for code generation
- **MetaGPT (Gao et al., 2024):** Role-based agent team (product manager, architect, coder); inspired multi-agent approaches
- **ChatDev (Yang et al., 2024):** Agentic development team; sequential role assignment without collaborative learning
- **LLM-Based Multi-Agent Systems Literature Review (Dou et al., 2026):** Comprehensive survey on multi-agent topologies; CoRe-Code is practical instantiation

### Reinforcement Learning for Code

- **CodeRL (Inala et al., 2022):** RL for code generation; individual agent optimization
- **PPO for Code (Hendrycks et al., 2023):** Proximal policy optimization applied to code tasks
- **RL4LMs (Ramamurthy et al., 2023):** RL framework for language models; generic, not code-specific

### Collaborative Multi-Agent Learning

- **QMIX, MADDPG (multi-agent DRL):** Credit assignment and learning in multi-agent systems; theoretical foundations
- **Group Relative Policy Optimization (GRPO):** Emerging technique for training agent teams with shared rewards

### Code Architecture & Planning

- **Software Design Patterns (Gamma et al., 1994):** Classic work on code architecture; inspired multi-agent decomposition
- **Program Synthesis from Specifications (Gulwani, 2021):** Survey on generating code from high-level specifications; related to planning stage

### Open Questions for Future Work

1. **Optimal Role Boundaries:** How many agents? What roles? Should roles be fixed or learned dynamically?
2. **Scalability:** Does GRPO scale to 50+ agent teams? How to handle agent communication bottlenecks?
3. **Generalization:** Do GRPO-trained agents generalize to new problem types, or do they overfit to training distribution?
4. **Human Integration:** How do humans collaborate with self-improving multi-agent systems?
5. **Failure Analysis:** When GRPO training fails or agents don't converge, how to debug?

---

## Citation

```bibtex
@article{Dou2026corecode,
  title={CoRe-Code: Collaborative Reinforcement Learning for Code Generation},
  author={Dou, Zhihao and Zhao, Qinjian and Wan, Zhongwei and Xia, Xiaoyu and Biswas, Sumon},
  journal={arXiv preprint arXiv:2605.24812},
  year={2026}
}
```
