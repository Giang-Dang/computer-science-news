# Agentic Environment Engineering for Large Language Models: A Survey of Environment Modeling, Synthesis, Evaluation, and Application

**ArXiv ID:** 2606.12191  
**Authors:** Jiachun Li et al. (15 co-authors)  
**Submitted:** June 10, 2026  
**URL:** https://arxiv.org/abs/2606.12191  
**Type:** Comprehensive Survey (63 pages, 10+ figures)

## Executive Summary

This seminal 63-page survey provides the first comprehensive framework for understanding **agentic environment engineering**—the systematic design, construction, and optimization of environments where LLM agents operate. The survey categorizes environment modeling approaches, synthesizes environments using symbolic and neural methods, establishes evaluation paradigms, and surveys applications across 8 domains (simulated, virtual, physical, digital, web, knowledge, social, hybrid). By establishing foundational concepts and taxonomies, this work enables practitioners to design effective environments that maximize agent capability while providing researchers a unified vocabulary for environment-agent co-design.

## Problem Statement

LLM-based autonomous agents operate within **environments** that determine what agents can perceive, what actions they can take, what consequences follow their actions, and how they receive feedback. Yet the field lacks principled frameworks for:

1. **Environment Specification**: How do we formally define what constitutes an "environment" for LLM agents?
2. **Environment Synthesis**: How do we efficiently create realistic environments for agent training, testing, and deployment?
3. **Environment-Agent Co-design**: How do agent capabilities and environment design interact? Which should we optimize first?
4. **Evaluation in Environments**: How do we compare agents fairly across different environments?
5. **Domain Specificity**: How do environment requirements differ across software development vs. robotics vs. scientific discovery?
6. **Scalability**: How do we create diverse, complex environments at scale without prohibitive manual effort?
7. **Realism-Efficiency Trade-off**: How do we balance environment realism (which improves transfer to real deployments) with computational efficiency?

Prior work either:
- Treats environments as fixed/given (not engineered)
- Focuses on single-domain environments (not generalizable)
- Lacks systematic evaluation methodologies
- Provides no guidance on symbolic vs. neural synthesis trade-offs

This survey addresses these gaps by establishing **environment engineering as a first-class research and engineering problem**.

## Core Concepts & Theory

### Dimensional Framework for Agentic Environments

The survey identifies **8 key environmental attributes** that characterize how environments enable/constrain agent operation:

#### **1. Observability**
- **Fully Observable**: Agent perceives complete environment state
- **Partially Observable**: Agent has incomplete information
- **Observation Noise**: Sensor errors, uncertainty
- **Observation Lag**: Delayed information reception
- **Multi-Modal Observation**: Text, images, structured data

**Trade-off**: Full observability aids learning but reduces realism
- Use: Training phases, algorithm development
- Real deployment: Partial observability is norm

#### **2. Action Space**
- **Discrete**: Predefined set of actions (e.g., {click, type, scroll})
- **Continuous**: Infinite action space (e.g., pixel coordinates)
- **Hybrid**: Mix of discrete and continuous actions
- **Action Validation**: Does environment enforce constraints?
- **Action Abstraction Level**: Low (raw pixels) vs. High (domain-specific skills)

**Trade-off**: Larger action spaces increase expressiveness but complexity
- Web agents: Discrete high-level actions (click button, enter text)
- Robotics agents: Continuous controls (joint angles)
- Code agents: Discrete high-level actions (edit file, run test)

#### **3. Determinism**
- **Deterministic**: Same action always produces same outcome
- **Stochastic**: Outcomes probabilistic
- **Adversarial**: Environment actively opposes agent
- **Multi-Agent**: Other agents affect outcomes

**Trade-off**: Deterministic environments easier to debug but less realistic
- Training: Often start deterministic for debugging
- Deployment: Introduce stochasticity to test robustness

#### **4. State Complexity**
- **State Dimensionality**: How many variables define state?
- **State Transitions**: Linear vs. non-linear dynamics
- **Long-Horizon**: How long is history? (affects planning horizon)
- **State Redundancy**: Compressed vs. verbose state representation

**Impact**: Complexity determines computational cost and learning difficulty

#### **5. Reward/Feedback Structure**
- **Sparse Rewards**: Feedback only at end
- **Dense Rewards**: Frequent feedback (e.g., per-step)
- **Feedback Delay**: Immediate vs. delayed
- **Ambiguous Rewards**: Conflicts between objectives
- **Human Judgment**: Requires human evaluation of quality

**Trade-off**: Dense rewards aid learning but may be hard to specify
- Software tasks: Often sparse (test pass/fail)
- Web interaction: Can provide dense feedback (action success)

#### **6. Communication & Grounding**
- **Symbolic Communication**: Natural language, structured formats
- **Semantic Grounding**: Symbols map to concrete entities
- **Ambiguity**: Intentionally ambiguous to test robustness
- **Dialogue**: Interactive back-and-forth with environment

**Critical for LLM agents**: Natural language grounding is essential

#### **7. Reproducibility & Debuggability**
- **Determinism**: Can executions be replayed?
- **Logging**: What information is captured?
- **Interpretability**: Why did action have this effect?
- **Breakpoints**: Can we pause and inspect?

**Production impact**: High reproducibility essential for deployment

#### **8. Scalability & Diversity**
- **Instance Count**: How many environment instances available?
- **Task Diversity**: How varied are evaluation tasks?
- **Curriculum Capability**: Can difficulty increase gradually?
- **Procedural Generation**: Can environments be synthesized programmatically?

---

### Environment Domain Taxonomy

The survey categorizes **8 major environment types** and their characteristics:

```
┌──────────────────────────────────────────────────────────────────┐
│           Agentic Environment Domain Taxonomy                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ 1. SIMULATED ENVIRONMENTS                                         │
│    • Purpose: Research, training, testing                         │
│    • Examples: CARLA (autonomous driving), OpenAI Gym (RL)      │
│    • Characteristics:                                             │
│      - Full control over dynamics                                 │
│      - Computationally efficient                                  │
│      - May not transfer to real world                             │
│    • Agent fit: RL agents, planning-heavy agents                  │
│                                                                   │
│ 2. VIRTUAL ENVIRONMENTS                                           │
│    • Purpose: Complex interaction, visual grounding              │
│    • Examples: Minecraft, VirtualHome, THOR                       │
│    • Characteristics:                                             │
│      - Visually realistic                                         │
│      - Large action spaces                                        │
│      - Supports research on embodiment                            │
│    • Agent fit: Vision+language agents, embodied reasoning        │
│                                                                   │
│ 3. PHYSICAL ENVIRONMENTS                                          │
│    • Purpose: Real-world robotics, IoT control                   │
│    • Examples: Real robots, lab equipment, manufacturing          │
│    • Characteristics:                                             │
│      - High realism, high risk                                    │
│      - Slow feedback loops                                        │
│      - Expensive experimentation                                  │
│    • Agent fit: Cautious, sample-efficient agents                 │
│                                                                   │
│ 4. DIGITAL ENVIRONMENTS                                           │
│    • Purpose: Software development automation                     │
│    • Examples: Code repositories, terminal/CLI, IDEs              │
│    • Characteristics:                                             │
│      - Deterministic (usually)                                    │
│      - Fast feedback (test results)                               │
│      - Rich symbolic structure (code)                             │
│    • Agent fit: Code-reasoning agents, planning-heavy             │
│                                                                   │
│ 5. WEB ENVIRONMENTS                                               │
│    • Purpose: Web browsing, interaction, automation               │
│    • Examples: Real websites, instrumented browsers               │
│    • Characteristics:                                             │
│      - Diverse, complex interfaces                                │
│      - Visual+symbolic information                                │
│      - Real-time feedback (page loads)                            │
│    • Agent fit: Vision+language agents, grounding agents          │
│                                                                   │
│ 6. KNOWLEDGE ENVIRONMENTS                                         │
│    • Purpose: Information retrieval, reasoning, synthesis         │
│    • Examples: Knowledge graphs, document corpora, QA systems     │
│    • Characteristics:                                             │
│      - Symbolic, structured information                           │
│      - Search/query interface                                     │
│      - Large-scale knowledge bases                                │
│    • Agent fit: Information-seeking agents, reasoning agents      │
│                                                                   │
│ 7. SOCIAL ENVIRONMENTS                                            │
│    • Purpose: Multi-agent interaction, negotiation, collaboration │
│    • Examples: Game scenarios, conversation systems, simulations  │
│    • Characteristics:                                             │
│      - Multi-agent dynamics                                       │
│      - Dialogue-based interaction                                 │
│      - Emergent behaviors from agent interactions                 │
│    • Agent fit: Collaborative agents, negotiating agents          │
│                                                                   │
│ 8. HYBRID ENVIRONMENTS                                            │
│    • Purpose: Realistic compound domains                          │
│    • Examples: Manufacturing floors (physical + digital), smart   │
│      homes (IoT + web), autonomous vehicles (physical + web)      │
│    • Characteristics:                                             │
│      - Multiple modalities and domains                            │
│      - Complex inter-system dependencies                          │
│      - Highest complexity and realism                             │
│    • Agent fit: Agents with multi-modal reasoning                 │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Environment Synthesis Approaches

**How are environments created?** The survey categorizes two major synthesis paradigms:

#### **Paradigm 1: Symbolic/Procedural Synthesis**

Environments defined through **explicit rules and procedures**:

```
Domain Rules & Logic
    ↓
Procedural Generation System
    ↓
Environment Instance
```

**Advantages**:
- Full control and transparency
- Computationally efficient
- Easy to verify correctness
- Interpretable failure modes

**Disadvantages**:
- Requires domain expertise to encode
- May lack realism (brittle assumptions)
- Hard to add stochasticity naturally

**Examples**:
- BabyAI (grid-world rules for language grounding)
- Program synthesis benchmarks (formal grammars for code generation)
- Manufacturing simulations (explicit plant models)

#### **Paradigm 2: Neural/Learned Synthesis**

Environments **learned from data or trained generatively**:

```
Real-world data / Demonstrations
    ↓
Neural Environment Model (e.g., World Model, Simulator)
    ↓
Generated Environment Instance
```

**Advantages**:
- Can capture complex, realistic dynamics
- Automatic from data (less manual engineering)
- Can handle stochasticity naturally
- Better transfer to real systems

**Disadvantages**:
- "Sim-to-real gap" (imperfect simulation)
- Less interpretable (black-box)
- Requires substantial training data
- Harder to guarantee correctness

**Examples**:
- Learned video models for visual simulation
- World models trained on trajectories
- Generative models for code environments

**Hybrid Approach**: Combine symbolic structure (rules) with learned components (dynamics) for balance.

---

### Agent Evolution Pathways in Environments

The survey identifies **4 key mechanisms** through which agents evolve within environments:

#### **Pathway 1: Memory-Centric Evolution**

Agents improve by building and refining internal memory representations:

```
[Interaction with Environment]
         ↓
[Update Memory/Knowledge]
         ↓
[Subsequent Actions Better Informed]
```

**Mechanisms**:
- Episodic memory: Recall specific past interactions
- Semantic memory: Extract general patterns
- Procedural memory: Learn efficient action sequences

**Examples in software dev**:
- Learn common bug patterns
- Remember successful refactoring strategies
- Build understanding of codebase structure

#### **Pathway 2: Orchestration-Centric Evolution**

Agents improve by better coordinating sub-systems/tools:

```
[Observe Outcomes of Tool Calls]
         ↓
[Learn Tool Effectiveness Patterns]
         ↓
[Improve Tool Selection & Sequencing]
```

**Mechanisms**:
- Tool proficiency: Understand what each tool does well
- Sequencing: Learn effective tool chains
- Failure recovery: Know when to switch tools

**Examples in software dev**:
- Learn which testing approach finds bugs fastest
- Understand when static analysis is most valuable
- Build efficient debugging workflows

#### **Pathway 3: Trajectory-Centric Evolution**

Agents improve by analyzing their own action sequences:

```
[Complete Task with Multi-Step Trajectory]
         ↓
[Analyze Trajectory for Efficiency]
         ↓
[Learn Better Planning Strategies]
```

**Mechanisms**:
- Path optimization: Find shorter solutions
- Redundancy elimination: Remove unnecessary steps
- Alternative discovery: Find different valid paths

**Examples in software dev**:
- Recognize overly-complex debugging approaches
- Simplify implementation paths
- Learn architectural patterns

#### **Pathway 4: Exploration-Centric Evolution**

Agents improve by strategic exploration of action space:

```
[Unknown Situation]
         ↓
[Strategic Exploration of Options]
         ↓
[Build Model of Situation]
         ↓
[Execute Optimally from Model]
```

**Mechanisms**:
- Active learning: Strategic query selection
- Uncertainty quantification: Know what's unknown
- Risk management: Balance exploration vs. exploitation

**Examples in software dev**:
- Systematically test edge cases
- Probe API behavior uncertainties
- Discover undocumented behaviors

---

## Main Ideas & Contributions

### Contribution 1: First Comprehensive Environment Taxonomy for LLM Agents

This survey establishes the first systematic framework for categorizing agentic environments across multiple dimensions:
- **8 environmental attributes** (observability, action space, etc.)
- **8 environment domains** (simulated through hybrid)
- **2 synthesis paradigms** (symbolic vs. neural)
- **4 agent evolution pathways**

This taxonomy enables:
- Principled discussion of environment design choices
- Identification of gaps (underexplored environment types)
- Better matching of agents to appropriate environments

### Contribution 2: Environment Synthesis Methodology

Systematic guidance on building environments:

**Symbolic Synthesis**:
- When to use (high-control, high-clarity requirements)
- How to implement (rule engines, procedural generation)
- Limitations and workarounds

**Neural Synthesis**:
- When to use (real-world realism, data available)
- How to implement (training approaches)
- Sim-to-real gap mitigation strategies

**Hybrid Approaches**:
- Combining symbolic clarity with neural realism
- Best practices from real-world deployments

### Contribution 3: Evaluation Frameworks for Environments

The survey proposes methodologies for evaluating whether an environment is suitable for agent research:

**Environment Quality Metrics**:
- Reproducibility: Can results be replicated?
- Interpretability: Can we understand why agents fail?
- Scalability: How many diverse tasks can we generate?
- Realism: How well does environment reflect real deployment?
- Efficiency: What's the computational cost?

**Agent-Environment Fit Metrics**:
- Coverage: What fraction of agent capabilities are tested?
- Challenge: How difficult are tasks for the agent?
- Transfer: Do insights transfer to other domains?

### Contribution 4: Domain-Specific Insights

The survey provides detailed guidance for **8 major application domains**:

**Software Development Environments**:
- Requirements: Test oracle, deterministic execution, fast feedback
- Challenges: Codebase complexity, tool diversity
- Best practices: Containerized execution, comprehensive logging

**Robotics Environments**:
- Requirements: Physical realism, safety constraints, sample efficiency
- Challenges: Sim-to-real gap, cost of real experiments
- Best practices: Transfer learning from simulation, careful validation

**Knowledge Work Environments**:
- Requirements: Large knowledge bases, search interfaces, semantic grounding
- Challenges: Ambiguity, incomplete information
- Best practices: Knowledge structure representation, uncertainty handling

[Similar sections for other 5 domains]

## Methodology & Implementation

### Survey Construction

**Scope**: 63-page comprehensive survey covering literature 2020-2026
**Analysis approach**:
1. Identify major agent system publications
2. Characterize their environment choices
3. Extract common patterns and divergences
4. Synthesize into taxonomy and frameworks

**Key papers analyzed**: 100+ publications spanning:
- RL and simulation environments
- Language-based agent systems
- Vision+language agent research
- Real-world robotic systems
- Web automation systems

### Environment Design Checklist

The survey provides practical guidance as a **design checklist**:

```
ENVIRONMENT DESIGN CHECKLIST
───────────────────────────────

□ Specify observability level
  □ Full vs. partial?
  □ Noise level?
  □ Multi-modal?

□ Define action space
  □ Discrete, continuous, or hybrid?
  □ Action validation rules?
  □ Abstraction level?

□ Choose dynamics model
  □ Symbolic rules or learned?
  □ Deterministic or stochastic?
  □ Validation approach?

□ Design reward structure
  □ Sparse or dense feedback?
  □ Delay in feedback?
  □ Multi-objective or single?

□ Select synthesis method
  □ Symbolic procedural generation?
  □ Neural learned models?
  □ Hybrid combination?

□ Plan evaluation
  □ Reproducibility mechanisms?
  □ Logging and debugging support?
  □ Metrics for environment quality?

□ Consider scaling
  □ How many tasks/instances?
  □ Curriculum progression?
  □ Diversity of tasks?

□ Test agent-environment fit
  □ Does environment match agent capabilities?
  □ Is difficulty appropriately calibrated?
  □ Will insights transfer?
```

### Reference Environment Implementations

The survey catalogs and compares **15+ reference environment systems**:

| Environment | Domain | Synthesis | Observability | Agent Type |
|---|---|---|---|---|
| CARLA | Autonomous Driving | Symbolic | Visual + Symbolic | Vision+RL |
| THOR | Virtual Embodied | Neural (Unity) | Visual | Vision+Language |
| BabyAI | Language Grounding | Symbolic | Symbolic | Language |
| SWE-bench | Code Development | Real (repo snapshot) | Symbolic | Code reasoning |
| WebArena | Web Interaction | Real websites | Visual | Vision+Language |
| [others] | [various] | [mixed] | [mixed] | [mixed] |

## Practical Applications & Use Cases

### Application 1: Software Development Agent Environments

**Goal**: Develop agents that write code, fix bugs, review PRs

**Environment Requirements**:
- **Observability**: Code text, test results, error messages
- **Action space**: Edit file, run test, check syntax
- **Dynamics**: Deterministic (code execution)
- **Reward**: Test pass/fail, code quality metrics

**Design choices**:
- Synthetic: GitHub-like repositories (procedurally generated)
- Real: Actual open-source repositories (real data)
- Hybrid: Real code with synthetic task definitions

**Current systems**: SWE-bench, BeyondSWE, Repo-Benchmark

### Application 2: Web Automation Agent Environments

**Goal**: Build agents that interact with web interfaces

**Environment Requirements**:
- **Observability**: HTML, screenshots, structured elements
- **Action space**: Click, type, scroll, navigate
- **Dynamics**: Stochastic (page loads, animations)
- **Reward**: Goal completion (e.g., find information)

**Design choices**:
- Real websites (realism but instability)
- Instrumented sandboxes (control with realism)
- Synthetic websites (full control)

**Current systems**: WebArena, VisualWebBench, MindAct

### Application 3: Multi-Agent Collaboration Environments

**Goal**: Develop agents that work together

**Environment Requirements**:
- **Observability**: Partial (each agent sees subset)
- **Action space**: Agent-specific actions plus communication
- **Dynamics**: Multi-agent interactions
- **Reward**: Collaborative objectives

**Design choices**:
- Explicit communication (agents send messages)
- Implicit communication (agents observe each other)
- Hybrid (some explicit, some implicit)

**Current systems**: Multi-agent simulations, dialogue systems

### Application 4: Continuous Learning Environments

**Goal**: Agents that improve over time in deployment

**Environment Requirements**:
- **Feedback mechanism**: Human or automatic evaluation
- **Learning signal**: Clear, frequent feedback
- **Scalability**: New tasks available continuously
- **Safety**: Failures don't cause harm

**Design choices**:
- Supervised: Human annotates agent outputs
- Unsupervised: Agent self-evaluates
- Hybrid: Combination approach

**Current systems**: Production agent deployments with logging

## Insights & Implications

### Key Findings

1. **Environment Design Determines Agent Capability**: The environment shapes what agents can learn and achieve—equal attention should be paid to environment and agent design

2. **Domain Specificity Matters**: No single environment design works for all domains; each domain imposes unique constraints and opportunities

3. **Hybrid Synthesis Wins**: Pure symbolic or pure neural approaches each have drawbacks; hybrid approaches combining symbolic structure with learned dynamics are most promising

4. **Reproducibility is Essential for Adoption**: Reproducible environments with comprehensive logging are adopted faster than black-box systems, even if the latter are more realistic

5. **Evolution Pathways Differ by Domain**: Some domains benefit most from memory-centric evolution (learning patterns), others from exploration-centric evolution (strategic testing)

### Research Implications

- **Environment engineering as first-class problem**: Deserves dedicated research effort, not ancillary to agent research

- **Standardized environment benchmarks needed**: Industry needs agreed-upon reference environments similar to ImageNet for vision

- **Sim-to-real gap is fundamental**: Theory needed to predict and mitigate transfer failures from simulated to real environments

- **Human-AI co-design of environments**: Environments should be designed through human-AI collaboration, not purely by either alone

### Limitations of Current Work

- **Limited real-world deployment analysis**: Most environments are research systems; fewer insights from production deployments
- **Scalability questions**: How do environments scale to handle millions of agents simultaneously?
- **Standardization gap**: No agreed-upon environment specification format or interchange protocol
- **Evaluation metric gaps**: Unclear how to compare agents across different environments fairly

## Code & Resources

### Environment Implementation Frameworks

**Python-based frameworks for building agentic environments**:

1. **Gymnasium (formerly OpenAI Gym)**
   - Standard RL environment interface
   - Used by: Researchers building custom environments
   - GitHub: https://github.com/Farama-Foundation/Gymnasium

2. **Langchain Environment Integration**
   - Tools for connecting LLM agents to external systems
   - Used by: LLM agent developers
   - GitHub: https://github.com/langchain-ai/langchain

3. **LLM-Compiler / Isaac Sim**
   - Robot simulation environments
   - Used by: Embodied agent researchers
   - Key for: Physical agent research

4. **Custom Frameworks**
   - SWE-bench environment (code development)
   - WebArena (web automation)
   - THOR (virtual embodied)

### Quick-Start Environment Building

```python
# Minimal agentic environment implementation
class AgentEnvironment:
    def __init__(self):
        self.state = self.reset()
    
    def reset(self):
        """Initialize environment state"""
        return initial_state
    
    def step(self, action):
        """Execute action, return new state and feedback"""
        new_state = self.dynamics(self.state, action)
        feedback = self.evaluate(new_state)
        done = self.is_terminal(new_state)
        return new_state, feedback, done
    
    def observe(self):
        """Return agent's partial observation of state"""
        return self.observation_function(self.state)
    
    def get_available_actions(self):
        """Return actions valid in current state"""
        return self.action_set

# Usage
env = AgentEnvironment()
for task in tasks:
    obs = env.reset()
    while not done:
        action = agent.decide(obs)
        obs, reward, done = env.step(action)
```

### Domain-Specific Environment Resources

**Software Development**:
- SWE-bench: Real repository issues
- BeyondSWE: Out-of-distribution challenges

**Web Interaction**:
- WebArena: Real websites
- VisualWebBench: Synthetic websites

**Knowledge Domains**:
- FEVEROUS: Fact extraction and verification
- MultiHopQA: Multi-step reasoning

**Robotics**:
- Isaac Sim: Physics simulation
- SAPIEN: Interactive simulation

### Integration with Agent Frameworks

**With Anthropic SDK**:
```python
# Define environment for agent tools
@agent_environment
class CodeEnvironment:
    def __init__(self):
        self.repo = Repository()
    
    @action
    def read_file(self, path: str) -> str:
        """Read file from repository"""
        return self.repo.read(path)
    
    @action
    def run_tests(self, test_path: str = None) -> str:
        """Execute tests"""
        return self.repo.run_tests(test_path)
```

## Related Work & Context

### Foundational Environment Literature

- **Classic RL Environments**: Atari, MuJoCo, Procgen (shaped how we think about environment design)
- **Embodied AI Environments**: THOR, AI2-THOR, VirtualHome (visual agents)
- **Language-based Environments**: BabyAI, TextWorld, WebShop (grounding language)

### Complementary Survey Work

- **Agent Survey Papers** (2024-2026): Focus on agent architectures; this survey complements with environment perspective
- **Reinforcement Learning Surveys**: Cover RL environments; this survey extends to language-based agents
- **Benchmark Surveys**: Catalog specific benchmarks; this survey focuses on environment design principles

### Convergence with Related Fields

**Connections to**:
- **Systems Engineering**: Environment as critical infrastructure for agents
- **Game Design**: Rich game environments share principles with agentic environments
- **Simulation Engineering**: Sim-to-real transfer from robotics applicable to other domains
- **Human-Computer Interaction**: User interface design informs environment design

### Future Directions

1. **Standardized Environment Specification Language**: Like PDDL for planning, need specification language for environments
2. **Automated Environment Generation**: Meta-learning to generate optimal environments for specific agent types
3. **Environment Adaptation**: Environments that dynamically adjust difficulty and diversity
4. **Multi-Agent Environments at Scale**: Handling 100s of agents simultaneously
5. **Formal Verification of Environments**: Proving properties about environment behavior and agent-environment interactions

---

## Conclusion

The shift from **agent-centric** to **agent-environment co-centric** perspectives represents a maturation of the field. As LLM agents move from research labs to production deployments, environment engineering becomes a critical bottleneck. This survey establishes foundational frameworks and taxonomies for principled environment design, synthesis, and evaluation. By treating environment engineering as a first-class problem with dedicated methodologies, researchers and practitioners can build more capable, more reliable, and more deployable autonomous agents.

The 8-dimensional attribute framework, 8-domain taxonomy, synthesis paradigm guidance, and 4-pathway evolution analysis provide immediate actionable guidance for anyone designing environments for LLM agents in any domain.
