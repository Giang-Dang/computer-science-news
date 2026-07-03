# Agentic Environment Engineering for Large Language Models: A Comprehensive Survey

## Executive Summary

This comprehensive 63-page survey synthesizes foundational work in environment engineering for LLM-based agents, providing a unified taxonomy covering modeling, synthesis, and evaluation paradigms. Through a novel 8-attribute classification framework (symbolic vs. neural, open-loop vs. closed-loop, online vs. offline, MDP vs. POMDP, deterministic vs. nondeterministic, discrete vs. continuous, unimodal vs. multimodal, single vs. multi-agent), the survey organizes 400+ papers across 8 application domains—from web automation and QA systems to software engineering and embodied AI—establishing the critical infrastructure perspective that agent quality depends as much on environment design as on model capability.

## Problem Statement

The rapid advancement of LLM agents has created a critical blind spot: **systematic study of agent environments**. Existing literature treats environments as afterthoughts—simple simulators or APIs—missing that:

1. **Environment Design Bottleneck**: The gap between agent capability and deployment success often stems not from model weakness but from poor environment specification (unclear state representation, noisy observations, ambiguous action effects).

2. **Synthesis Challenge**: Building realistic environments for agent training is expensive. Rule-based simulation requires domain expertise; data-driven approaches require massive corpora. No unified framework guides practitioners.

3. **Evaluation-Deployment Gap**: Lab environments reward simple heuristics; real-world environments penalize them. Evaluation metrics don't transfer across environments (success rate on WebShop ≠ success rate on real e-commerce APIs).

4. **Heterogeneity Across Domains**: Web automation, question-answering, code generation, and robotics each require different environment abstractions—no common vocabulary.

5. **Multi-Agent Coordination Ignored**: Most environments assume single-agent control. Real systems require orchestrating multiple agents in shared environments (competing resources, information sharing, credit assignment).

The research gap is the lack of a unifying framework for conceptualizing, designing, synthesizing, and evaluating agent environments across diverse domains.

## Core Concepts & Theory

### 8-Attribute Environment Taxonomy

UniToolCall defines environments through 8 orthogonal dimensions:

#### 1. **Representation: Symbolic vs. Neural**

**Symbolic Environments**:
- State: Structured (JSON, ASTs, knowledge graphs)
- Transition rules: Explicit (if-then, constraints)
- Observation: Deterministic ground truth
- Example: WebShop (HTML DOM as state, API calls as actions)

**Neural Environments**:
- State: Implicit (learned embeddings, vision)
- Transition rules: Learned (neural networks)
- Observation: Stochastic approximations
- Example: Complex vision-based robotics (agent sees pixels, infers object state)

**Trade-offs**:
```
Symbolic                          Neural
Interpretable ←→ Flexible
Requires engineering ←→ Data-driven
Fast simulation ←→ Realistic dynamics
Easy to verify ←→ Emergent properties
```

#### 2. **Interaction: Open-Loop vs. Closed-Loop**

**Open-Loop**: Agent commits to action sequence without feedback
- Action: "Buy iPhone 13" (commit to order)
- No intermediate observation before purchase

**Closed-Loop**: Agent observes outcome after each action
- Action: "Search for iPhones"
- Observation: [matching results]
- Next action: "Filter by price < $500"

Most practical environments are closed-loop; open-loop is rare (e.g., batch processing, offline RL).

#### 3. **Execution: Online vs. Offline**

**Online Environments**:
- State evolves independently of agent actions
- Agent must respond in real-time
- Example: Live chat support (customers arrive, agent must respond timely)

**Offline Environments**:
- Agent has batch of queries/tasks
- No time pressure
- Agent can reason as long as needed
- Example: Batch code review, document summarization

#### 4. **Uncertainty: MDP vs. POMDP**

**MDP (Fully Observable)**:
- Agent observes complete state
- Transition is deterministic or known
- Example: Board game (agent sees all pieces)

**POMDP (Partially Observable)**:
- Agent observes partial state
- Must maintain belief state (uncertainty)
- Transition may be nondeterministic
- Example: Web search (agent doesn't see full search results, only top-10)

#### 5. **Dynamics: Deterministic vs. Nondeterministic**

**Deterministic**: Same action always produces same outcome
- Example: Code execution (given code and input, output is fixed)

**Nondeterministic**: Action produces stochastic outcomes
- Example: Web search (query returns different results over time)
- Example: Multi-agent environments (other agents' actions affect state)

#### 6. **State Space: Discrete vs. Continuous**

**Discrete**: Finite action/state set
- Example: WebShop (click button → discrete next state)

**Continuous**: Infinite action/state space
- Example: Robotic manipulation (joint angles in ℝ³)
- Example: Text generation (embedding space)

#### 7. **Modality: Unimodal vs. Multimodal**

**Unimodal**: Single modality (text, vision, audio)
- Example: API-based QA (text only)

**Multimodal**: Multiple modalities
- Example: Embodied AI (visual + force feedback + proprioception)
- Example: Web automation (vision + text)

#### 8. **Agency: Single-Agent vs. Multi-Agent**

**Single-Agent**:
- Agent operates in fixed environment
- Example: Solo code writing

**Multi-Agent**:
- Multiple agents in shared environment
- Cooperation (agents work toward shared goal)
- Competition (agents have conflicting goals)
- Mixed (some cooperation, some competition)

### Unified Environment Formalism

```
E = (S, A, O, T, R, I)

S:  State space (infinite for neural, finite for symbolic)
A:  Action space (agent's capabilities)
O:  Observation space (what agent perceives)
T:  Transition function s' = T(s, a, ω) where ω ~ P(ω|s,a)
R:  Reward/success criterion
I:  Initial state distribution

Meta-parameters:
  - Symbolic/Neural representation
  - Open/Closed loop interaction
  - Online/Offline execution
  - Observable/Partial observability
  - Deterministic/Stochastic dynamics
  - Discrete/Continuous state-action
  - Unimodal/Multimodal observations
  - Single/Multi-agent
```

### Environment Lifecycle

```
┌────────────────────────────────────────────────────────┐
│              Environment Engineering Lifecycle         │
└────────────────────────────────────────────────────────┘

1. Specification Phase
   ├─ Define task (goal specification)
   ├─ Identify domain constraints
   ├─ Choose taxonomy attributes
   └─ Document environment contract

2. Synthesis Phase
   ├─ Symbolic synthesis: Rule-based simulators
   ├─ Neural synthesis: Data-driven learning
   └─ Hybrid: Combine symbolic + neural

3. Validation Phase
   ├─ Test state transitions
   ├─ Verify observation correctness
   ├─ Check reward signal alignment
   └─ Measure sim-to-real gap (if applicable)

4. Integration Phase
   ├─ Deploy with agent training pipeline
   ├─ Monitor agent-environment interaction
   └─ Iterate based on agent performance

5. Evaluation Phase
   ├─ Benchmark agent on environment
   ├─ Compare to human baselines
   ├─ Analyze failure modes
   └─ Publish results + release environment
```

## Main Ideas & Contributions

### 1. Unified Taxonomy Across Heterogeneous Domains

The paper's core contribution is the 8-attribute taxonomy that enables comparing environments across domains:

**Example Classification**:

| Domain | Symbolic | Closed | Online | POMDP | Stochastic | Discrete | Multimodal | Multi-Agent |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| WebShop | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ |
| API-Bank | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ |
| Code Gen | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Text-SQL | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Embodied AI | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| Game Playing | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Web Automation | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |

This matrix reveals that no two domains are identical; agent researchers must understand their environment's position in taxonomy space.

### 2. Synthesis Paradigm Classification

The survey identifies two complementary synthesis approaches:

**A. Symbolic Synthesis (Rule-Based)**

```
Domain Knowledge
    ↓
Specify Rules & Constraints
    ↓
Build Simulator
    ├─ State representation (structs, APIs)
    ├─ Transition logic (if-then rules)
    ├─ Observation function (deterministic rendering)
    └─ Reward function (explicit metrics)
    ↓
Validate Against Real Data
```

**Strengths**:
- Interpretable, auditable rules
- Fast simulation (no learning overhead)
- Can guarantee properties (correctness, completeness)

**Weaknesses**:
- Requires domain expertise
- Brittle to distribution shift
- Cannot capture complex emergent behaviors

**Examples**: WebShop simulator, Text-to-SQL evaluators, API stubs

**B. Neural Synthesis (Learning-Based)**

```
Real-World or High-Fidelity Data
    ↓
Learn Environment Model
    ├─ State encoder (images → embeddings)
    ├─ Transition model (next state predictor)
    ├─ Observation model (perceptual encoder)
    └─ Reward model (outcome prediction)
    ↓
Validate Prediction Accuracy
    ├─ State prediction error
    ├─ Transition fidelity
    └─ Reward correlation
```

**Strengths**:
- Data-driven, captures real-world complexity
- Generalizes to distribution shift
- Can learn surprising patterns

**Weaknesses**:
- Requires large corpora (expensive to collect)
- Prediction errors compound (distribution shift in agent actions)
- Black-box (hard to debug failures)

**Examples**: World models for video prediction, learned reward models, neural simulators for robotics

**Hybrid Synthesis**:

Combine symbolic rules (correctness guarantees) with neural components (flexibility):

```
Symbolic Rules for Core Logic
    +
Neural Component for Uncertainty
    =
Robust, Verifiable Environment

Example: Text-SQL evaluation
├─ Symbolic: SQL parser, schema validator
├─ Neural: Semantic equivalence checker (learned from data)
└─ Result: Handles both syntactic and semantic correctness
```

### 3. Eight Application Domains

The survey comprehensively covers:

#### a) **Web Automation**
- **Environment**: Browser, HTML DOM, JavaScript execution
- **Key Challenge**: Partial observability (agent doesn't see below-the-fold content)
- **Notable Systems**: WebShop, Mind2Web, ScreenAgent
- **Synthesis Approach**: Symbolic simulator + neural vision model

#### b) **Question Answering**
- **Environment**: Knowledge bases, retrieval indices, documents
- **Key Challenge**: Determining when sufficient evidence gathered
- **Notable Systems**: HotpotQA, 2WikiMultiHopQA, Natural Questions
- **Synthesis Approach**: Symbolic retrieval engine + neural ranking

#### c) **Text-to-SQL**
- **Environment**: Database schema, SQL executor
- **Key Challenge**: Schema understanding, bridging natural language to SQL
- **Notable Systems**: Spider, WikiSQL, BIRD
- **Synthesis Approach**: Symbolic schema validation + neural semantic matching

#### d) **Software Engineering**
- **Environment**: Code repository, test runner, linter, debugger
- **Key Challenge**: Long-horizon planning (understanding entire codebase)
- **Notable Systems**: SWE-Bench, HumanEval, GitHub Issues
- **Synthesis Approach**: Symbolic code analyzer + neural program synthesis

#### e) **Gaming**
- **Environment**: Game engine (Atari, Minecraft, StarCraft)
- **Key Challenge**: High-dimensional state, stochastic opponents
- **Notable Systems**: ALE (Arcade Learning Environment), MineDojo, AlphaStar
- **Synthesis Approach**: Neural environment model (learned from game engine)

#### f) **Embodied AI (Robotics)**
- **Environment**: Physical world (or high-fidelity simulator like Mujoco)
- **Key Challenge**: Reality gap (sim-to-real transfer)
- **Notable Systems**: AI2-THOR, Habitat, SAPIEN
- **Synthesis Approach**: Neural dynamics model + symbolic physics engine

#### g) **Dialogue & Multi-Turn Interaction**
- **Environment**: Conversation partner (human or agent)
- **Key Challenge**: Long-term coherence, user satisfaction
- **Notable Systems**: ConvAI, ParaNMT-50M, Wizard of Wikipedia
- **Synthesis Approach**: Symbolic dialogue state tracker + neural response model

#### h) **Tool-Use Environments (APIs, Code, Commands)**
- **Environment**: API specifications, code execution, CLI tools
- **Key Challenge**: Handling diverse tool schemas, error recovery
- **Notable Systems**: ToolBench, APIBench, UniToolCall
- **Synthesis Approach**: Symbolic tool registry + neural parameter prediction

### 4. Evaluation Across Environments

**Challenge**: Different domains use different success metrics, making it impossible to compare agents.

**Solution**: Propose unified evaluation framework:

```
Universal Evaluation Framework:

1. Task Specification
   ├─ Goal clarity (is goal well-defined?)
   ├─ Goal achievability (is it solvable?)
   └─ Goal uniqueness (one solution or multiple?)

2. Execution Metrics
   ├─ Success rate (task completed?)
   ├─ Sample efficiency (queries/actions needed)
   ├─ Time efficiency (real-world wall-clock)
   └─ Cost efficiency (API calls, compute used)

3. Robustness Metrics
   ├─ Distribution shift (performance on OOD data)
   ├─ Noise tolerance (robustness to observation errors)
   └─ Adversarial robustness (against adversarial inputs)

4. Interpretability Metrics
   ├─ Action explanation (can agent justify action?)
   ├─ State understanding (does agent understand state?)
   └─ Failure diagnostics (clear error messages?)
```

## Methodology & Implementation

### Coverage Analysis

The survey reviews 400+ papers across synthesis and evaluation literature:

**Synthesis Papers**:
- Symbolic simulators: 120+ papers
- Neural environment models: 150+ papers
- Hybrid approaches: 60+ papers
- Validation methods: 70+ papers

**Evaluation Papers**:
- Benchmarks: 95+ papers
- Metrics & analysis: 85+ papers
- Comparative studies: 50+ papers

### Key Findings by Domain

**Software Engineering** (most mature):
- Synthesis: Symbolic AST analyzers + neural code models
- Benchmarks: SWE-Bench, SWE-gym (1000s of real tasks)
- Evaluation: Task completion + code quality metrics

**Web Automation** (growing):
- Synthesis: HTML DOM simulator + vision models for rendering
- Benchmarks: Mind2Web (10K web interactions), WebShop
- Evaluation: User-centric metrics (task success, page coverage)

**Embodied AI** (frontier):
- Synthesis: Physics-based simulators (Mujoco) + learned dynamics
- Benchmarks: Habitat (1000s of scenes), AI2-THOR (real 3D scans)
- Evaluation: Sim-to-real gap (real robot performance vs simulator)

**Game Playing** (established):
- Synthesis: Game engine + neural models (for partially observable games)
- Benchmarks: ALE (57 Atari games), Minecraft (open-ended)
- Evaluation: Win rate, game score, speedrun records

### Architectural Patterns

**Pattern 1: Symbolic Core + Neural Perception**

```
User Input → LLM Planning → Symbolic Executor → State
                               ↓
                        Neural Perception
                        (e.g., vision model)
                               ↓
                        Observation to Agent
```

**Example**: Web automation (LLM plans actions, symbolic executor clicks, neural model interprets visual feedback)

**Pattern 2: Neural Dynamics + Symbolic Constraints**

```
Agent Action → Neural Dynamics Model → Predicted Next State
                       ↓
              Symbolic Constraint Checker
              (ensure feasibility)
                       ↓
              Filtered/Adjusted State → Observation
```

**Example**: Embodied AI (learned dynamics model respects physical constraints)

**Pattern 3: Ensemble Environments**

```
Agent → Environment 1 (Conservative/Pessimistic)
      → Environment 2 (Optimistic)
      → Environment 3 (Medium)
         ↓
      Ensemble Vote
      (majority-rule success)
```

**Use Case**: When ground-truth environment is unavailable; use ensemble for robust evaluation.

## Practical Applications & Use Cases

### 1. Building a Web Automation Environment

**Scenario**: Create environment for e-commerce agents.

**Steps**:
1. **Specification**: Identify partial observability (agent sees viewport, not full page)
2. **Symbolic Core**: Build simulator with HTML DOM, JavaScript engine
3. **Neural Component**: Train vision model on real website screenshots
4. **Validation**: Compare agent behavior on simulator vs. real site
5. **Iteration**: Refine simulator based on simulation-reality gap

**Result**: Agents trained on environment transfer to real websites with >80% success rate.

### 2. Evaluating Dialogue Systems

**Scenario**: Benchmark conversational agents.

**Challenge**: Dialogue success is subjective; hard to define ground truth.

**Solution**:
1. **Symbolic Specification**: Define conversation goals (answer user question, complete task)
2. **Evaluation Framework**: Multi-dimensional metrics (task success + coherence + user satisfaction)
3. **Baseline Comparison**: Compare agent to human performance

**Benefit**: Evaluation becomes standardized across papers; enables fair comparison.

### 3. Sim-to-Real Transfer for Robotics

**Scenario**: Train robot in simulation, deploy in real world.

**Environment Engineering**:
1. **Neural Dynamics**: Learn to predict real-world physics
2. **Domain Randomization**: Vary simulator parameters (friction, dynamics) to improve transfer
3. **Validation**: Test policy on real robot, measure success rate

**Challenge**: Even with good environment, sim-to-real gap remains (~20% performance drop typical).

### 4. Multi-Agent Coordination in Shared Environments

**Scenario**: Multiple coding agents collaborating on large codebase.

**Environment Design**:
1. **Shared State**: Version control system, shared code repository
2. **Communication**: Agents can read git history, leave comments
3. **Coordination Mechanism**: Explicit task assignment, conflict resolution

**Benefit**: Formalized environment enables analyzing agent collaboration patterns.

## Insights & Implications

### 1. Environment Quality Determines Agent Quality

A major finding: **Agent capabilities are bottlenecked by environment specification**, not just model size.

Examples:
- Poor partial observability modeling → agents fail on real-world tasks even if model is strong
- Unrealistic reward signal → agents learn spurious heuristics
- Stochastic environment underspecified → agents overfit to training distribution

**Implication**: Before scaling to larger models, invest in environment engineering.

### 2. Synthesis Approach Should Match Task Characteristics

**Symbolic is better for**:
- Well-specified domains (code, databases)
- Tasks requiring interpretability/auditability
- Offline, planning-heavy tasks

**Neural is better for**:
- Perceptual/unstructured domains (vision, dialogue)
- Tasks with complex emergent properties
- Online, reactive tasks

**Hybrid is best for**:
- High-stakes applications (medical, finance)
- Real-world deployment (needs both interpretability + flexibility)

### 3. Generalization Requires Diverse Environments

Agents trained on single environment overfit. Paper shows:

**Training Domain vs. Test Domain**:
- Same domain, same data distribution: 92% success
- Same domain, different data distribution: 78% success (19% drop)
- Different domain, even if semantically similar: 45% success (47% drop)

**Implication**: Benchmark environments must include diverse data distributions and domain variants.

### 4. Multi-Agent Environments Are Underexplored

Most agent research focuses on single-agent control. Real-world systems are multi-agent:
- Web applications (multiple users)
- Code repositories (multiple developers)
- Robotics (multiple robots)

The survey identifies only ~50 multi-agent environment papers vs. 400+ single-agent. This is a frontier.

### 5. Evaluation Metrics Don't Transfer

Success metric meaningful in one domain is meaningless in another:
- Task completion rate (good for Q&A)
- Path efficiency (good for navigation)
- Code quality (good for programming)
- User satisfaction (good for dialogue)

**Solution**: Adopt unified framework with multi-dimensional metrics per domain.

## Code & Resources

### Environment Engineering Toolkit

The survey references 400+ open-source environments:

**Symbolic Simulators**:
- WebShop: https://webshop-pnlp.github.io/
- Text-SQL databases: Spider (huggingface.co/datasets/spider), BIRD
- Code environments: SWE-bench (https://www.swebench.com/), HumanEval

**Neural Environments**:
- Habitat (embodied AI): https://github.com/facebookresearch/habitat3
- AI2-THOR (3D environments): https://ai2thor.allenai.org/
- MinecraftRL: https://github.com/openai/minecraft-rl

**Hybrid Environments**:
- WebArena (web automation): https://github.com/web-arena-x/webarena
- AnyTool (tool-use): https://github.com/bilevel-icer/anytool

### Implementation Patterns

**Template for Symbolic Environment**:

```python
class SymbolicEnvironment:
    def __init__(self, task_spec):
        self.state = self.initialize_state(task_spec)
        self.reward_fn = task_spec.reward_function
    
    def step(self, action):
        # Validate action against environment schema
        assert action in self.valid_actions(), "Invalid action"
        
        # Apply transition function
        self.state = self.transition(self.state, action)
        
        # Generate observation
        observation = self.observe()
        
        # Compute reward
        reward = self.reward_fn(self.state)
        done = self.is_terminal(self.state)
        
        return observation, reward, done
    
    def observe(self):
        # Render state for agent perception
        return self.render_observation(self.state)
```

**Template for Neural Environment**:

```python
class NeuralEnvironment:
    def __init__(self, dynamics_model, perception_model):
        self.dynamics = dynamics_model  # Neural network
        self.perception = perception_model
    
    def step(self, action):
        # Predict next state using learned model
        action_embedding = self.encode_action(action)
        state_embedding = self.encode_state(self.state)
        
        next_state_embedding = self.dynamics(
            state_embedding, action_embedding
        )
        self.state = self.decode_state(next_state_embedding)
        
        # Generate observation via perception model
        observation = self.perception(self.state)
        
        # Reward from learned model or symbolic function
        reward = self.reward_model(self.state)
        
        return observation, reward, done
```

### Evaluation Harness

```python
class EnvironmentEvaluator:
    def __init__(self, environment, agent, metrics):
        self.env = environment
        self.agent = agent
        self.metrics = metrics  # task_success, sample_efficiency, etc.
    
    def evaluate(self, n_trials=100):
        results = defaultdict(list)
        
        for _ in range(n_trials):
            obs = self.env.reset()
            trajectory = []
            
            while not obs['done']:
                action = self.agent.act(obs)
                obs, reward, done = self.env.step(action)
                trajectory.append((obs, action, reward))
            
            # Compute metrics
            for metric_fn in self.metrics:
                score = metric_fn(trajectory)
                results[metric_fn.name].append(score)
        
        # Aggregate statistics
        summary = {
            name: {
                'mean': np.mean(scores),
                'std': np.std(scores),
            }
            for name, scores in results.items()
        }
        return summary
```

## Related Work & Context

### Prior Surveys on Agent Environments

- **Wu et al. (2023)**: Towards a Generalizable Agent for Vision-and-Language Navigation
- **Bridge et al. (2024)**: Benchmarking Procedurally Generated Agents in the Open Web
- **Zhou et al. (2024)**: A Survey on Language Agents: Foundations, Development, and Opportunities

**UniToolCall Contribution**: First comprehensive taxonomy + synthesis + evaluation framework specifically for LLM agents.

### Foundational Work

- **Markov Decision Processes** (Bellman, 1957): Formalism for modeling sequential decision-making
- **POMDP Theory** (Kaelbling et al., 1998): Handling partial observability
- **Environment Design in RL** (Berner et al., 2019): Work on environment-agent co-design
- **Sim-to-Real Transfer** (Tobin et al., 2017): Domain randomization for robustness

### Related Research Themes

- **Benchmark Design**: How to design benchmarks that measure real-world capabilities (not spurious correlations)
- **Distribution Shift**: Agents must generalize to environments not seen during training
- **Safe Agent Deployment**: Environment design for safe exploration and failure recovery
- **Human-AI Collaboration**: Designing environments where humans and AI agents work together

## Future Research Directions

1. **Automated Environment Synthesis**: Can agents learn to generate environments that train better agents (meta-learning)?

2. **Environment Calibration**: How to tune environment parameters (difficulty, realism) to match agent capability?

3. **Multi-Modal Integration**: How to design environments that seamlessly integrate vision, text, and action?

4. **Distributed Environments**: How to scale environments for distributed multi-agent training?

5. **Formal Verification**: Can we formally verify that environment satisfies desired properties?

---

**Survey Details**:
- **ArXiv ID**: 2606.12191
- **Published**: June 2026
- **Authors**: 15 researchers (comprehensive collaboration across institutions)
- **Pages**: 63
- **Scope**: 400+ papers across 8 domains, 8 taxonomy dimensions
- **GitHub**: https://github.com/agentic-env-eng/survey-resources
- **Dataset of Environments**: https://huggingface.co/datasets/agentic-environments
