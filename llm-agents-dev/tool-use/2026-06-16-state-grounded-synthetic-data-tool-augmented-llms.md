# State-Grounded Multi-Agent Synthetic Data Generation for Tool-Augmented LLMs

**ArXiv**: 2606.16307  
**Published**: June 15, 2026  
**Authors**: Rahul Khedar, Eshita, Sneha Teja Sree Reddy Thondapu, Mayank Malhotra, Arup Das, Jitesh Chandra, Yun-Shiuan Chuang, Chaitanya Kulkarni, Arun Menon, Linsey Pang, Avinash Karn, Mouli V, Prakhar Mehrotra  
**Affiliation**: PayPal AI

## Executive Summary

Training effective tool-augmented LLM agents requires large-scale, high-quality multi-turn conversational data that is grounded in real tool interactions—but manual annotation is expensive and privacy-sensitive in production systems. This paper presents **StateGen**, a novel synthetic data generation platform that orchestrates a four-role LLM loop with an **authoritative state manager** to produce reasoning-trace-rich training conversations while eliminating the dominant class of tool-call hallucinations by architectural design rather than post-hoc filtering. Evaluated on three production corpora spanning PayPal's real-world tool ecosystem, StateGen demonstrates its effectiveness for training robust, production-grade tool-augmented agents at scale.

## Problem Statement

### The Challenge of Training Tool-Augmented Agents

Training LLM agents to reliably use external tools is one of the most critical challenges in autonomous systems development. The fundamental problem lies in the data requirement:

1. **Data Scarcity**: Production-quality tool-augmented agent training requires massive corpora of multi-turn conversational data where:
   - Each turn contains realistic user behavior
   - Agent reasoning and tool selections are interpretable
   - Tool calls are grounded in actual backend responses
   - Conversations span multiple interaction patterns

2. **Annotation Expense**: Manual annotation of tool-use conversations is prohibitively expensive because annotators must:
   - Understand complex tool APIs and their preconditions
   - Verify correctness of tool calls against backend logic
   - Trace reasoning chains across multi-turn interactions
   - Maintain consistency across thousands of conversations

3. **Privacy Constraints**: In production systems like PayPal, using real customer data for training is infeasible due to:
   - PII and financial data sensitivity
   - Regulatory compliance requirements (GDPR, financial regulations)
   - Customer privacy concerns
   - Operational risk of data exposure

4. **Tool-Call Hallucinations**: A critical failure mode in tool-augmented agents is the generation of tool calls that:
   - Reference non-existent functions or parameters
   - Use incorrect argument formats
   - Violate preconditions (e.g., calling delete before checking existence)
   - Become inconsistent with the actual state of the backend

### State-of-the-Art Limitations

Existing approaches fall short in several ways:

- **Manual data**: Expensive, limited scale, privacy-risky
- **Rule-based generation**: Lacks naturalness, poor reasoning traces, brittle
- **Simple synthetic approaches**: Generate tool calls without backend state grounding, leading to hallucinations
- **Public datasets**: Insufficient tool coverage, limited to simple scenarios, don't reflect production complexity

## Core Concepts & Theory

### The Four-Role LLM Loop Architecture

StateGen's innovation rests on orchestrating four specialized LLM roles in a coordinated loop:

```
┌─────────────────────────────────────────────────────────────┐
│                Four-Role LLM Loop Pattern                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. User Simulator (Persona-Driven)                          │
│     └─> Generates realistic user requests with personality    │
│                          │                                     │
│                          ▼                                     │
│  2. Agent Under Test (Action Generation)                     │
│     └─> Produces tool calls and reasoning                     │
│                          │                                     │
│                          ▼                                     │
│  3. Tool Simulator (State Management)                        │
│     └─> Authoritative backend state executor                 │
│                          │                                     │
│                          ▼                                     │
│  4. Multi-Axis Judge (Conversation Scoring)                  │
│     └─> Evaluates quality across multiple dimensions          │
│                          │                                     │
│                          ▼ (cycle continues)                  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### The Authoritative State Manager

The core innovation is the **authoritative state manager**, which maintains a structured world-state object that all tools and the agent reference. This achieves:

1. **Backend-is-Truth Invariant**: The actual state object is the single source of truth. When the agent makes a tool call, the state manager:
   - Validates preconditions against current state
   - Executes the operation on the state object
   - Returns authoritative results
   - Updates state deterministically

2. **Hallucination Elimination by Design**: By grounding all tool calls in actual state, the system eliminates hallucinations structurally:
   - Non-existent operations cannot succeed (caught at validation)
   - State-dependent operations receive real state
   - Results are always consistent with backend logic
   - Impossible sequences are prevented

3. **Persona-Driven Variation**: User diversity is encoded through a 23-dimensional persona trait vector:
   - Communication style (formal, casual, technical)
   - Domain expertise level
   - Decision-making preferences
   - Interaction frequency and patterns
   - Error tolerance and recovery preferences

### Multi-Agent Orchestration for Hierarchical Systems

StateGen naturally extends to hierarchical multi-agent settings through a key architectural pattern:

- Sub-agents are declared as tools callable by higher-level agents
- All agents share a single authoritative state object
- Enables complex multi-level reasoning chains
- Maintains state consistency across hierarchical levels

```
┌──────────────────────────────────┐
│   Master Orchestrator Agent       │
├──────────────────────────────────┤
│  Calls Tool: Invoke-SubAgent-A   │
│  Calls Tool: Invoke-SubAgent-B   │
│  Calls Tool: Invoke-SubAgent-C   │
└──────────┬───────────────────────┘
           │
      Shared State Object
      (Authoritative)
           ▲
           │
    ┌──────┴──────┬──────────┬──────────┐
    │             │          │          │
    ▼             ▼          ▼          ▼
┌─────────┐  ┌─────────┐ ┌─────────┐ ┌─────────┐
│SubAgent │  │SubAgent │ │SubAgent │ │SubAgent │
│   A     │  │   B     │ │   C     │ │   D     │
└─────────┘  └─────────┘ └─────────┘ └─────────┘
```

## Main Ideas & Contributions

### 1. Structured Synthetic Data Generation Platform

StateGen provides a complete platform for generating production-quality training data:

**User Simulation with Persona Control**:
- Generates diverse, natural user requests
- 23-dimensional persona trait space enables controlled variation
- Personas control conversation style, domain knowledge, preferences
- Enables curriculum learning (start with simple personas, increase complexity)

**Agent Evaluation Under Diverse Conditions**:
- Tests agent behavior across persona variations
- Identifies robustness gaps against different interaction styles
- Enables persona-specific fine-tuning

**Reasoning-Trace Richness**:
- Generated conversations include explicit reasoning traces
- Multi-step reasoning chains captured for training
- Enables learning of reasoning patterns alongside tool use

### 2. Authoritative State Management

The state manager eliminates the most prevalent failure mode:

**Tool-Call Hallucination Scoring**: 9.66/10 indicates near-perfect elimination through structural design

**How It Works**:
1. Every tool call receives the current state object
2. Preconditions are checked against actual state
3. Operations execute on the state deterministically
4. Results reflect actual state transitions
5. Agent learns that hallucinated calls fail immediately

**Learning Effect**:
- Agents trained on StateGen data avoid hallucinations
- Policy learns valid preconditions from examples
- Tool-use patterns become state-aware
- Generalization to unseen states improves

### 3. Production-Scale Evaluation

Evaluation on three PayPal production corpora demonstrates real-world applicability:

- **64,698 evaluated conversations** across production systems
- **Separate train and golden sets** prevent memorization
- **Real tool patterns** from production usage
- **Cross-validation** on production metrics

## Methodology & Implementation

### Data Generation Process

**Step 1: Four-Role Configuration**
```
Persona-driven user simulator:    temp=0.7
Agent under test:                 temp=0.8
State-grounded tool simulator:    temp=0.0 (deterministic)
Multi-axis judge:                 temp=0.6
```

**Step 2: Turn-Taking Loop**
1. User simulator generates request with persona context
2. Agent generates reasoning and tool calls
3. Tool simulator:
   - Validates calls against state
   - Executes on authoritative state
   - Returns results
4. Judge scores conversation across axes
5. Loop continues until termination condition

**Step 3: Conversation Extraction**
- Collect all turns in structured format
- Extract reasoning traces for supervision
- Separate into train and evaluation sets
- Compute quality metrics

### Persona Engineering

The persona system uses a 23-dimensional trait vector:

```json
{
  "communication_style": "formal|neutral|casual",
  "domain_expertise": 0.0-1.0,
  "decision_speed": 0.0-1.0,
  "risk_tolerance": 0.0-1.0,
  "interaction_frequency": 0.0-1.0,
  "error_recovery_preference": "immediate|delayed|manual",
  "language_complexity": 0.0-1.0,
  "task_planning_style": "detail_first|goal_first|iterative",
  ...
}
```

### State Object Representation

The authoritative state tracks:
- Account information (when applicable)
- Transaction history
- Permission state
- Resource availability
- Constraint satisfaction

### Production Integration

**Architecture**:
```
Data Generation Pipeline:
  Raw Persona Specs → Four-Role Loop → Quality Filtering → Train/Eval Split
                        ▲                    │
                        │                    ▼
                   Authoritative         Conversational
                   State Manager         Data (64,698 examples)
                                             │
                                             ▼
                                        Agent Training
                                             │
                                             ▼
                                        Production Deployment
```

## Practical Applications & Use Cases

### 1. Tool-Augmented Agent Training

StateGen directly enables training of robust agent systems:

**Use Case: Customer Service Agents**
- Generate conversations between simulated customers and service agents
- Service agents learn to use backend tools (account lookup, payment processing)
- Train on diverse customer personas
- Evaluate agent robustness across interaction styles

**Use Case: Developer Assistant Agents**
- Generate interactions with code repositories, CI/CD tools, deployment systems
- Training data reflects realistic developer behavior and tool patterns
- Enables safe autonomous deployment and infrastructure agents

### 2. Multi-Agent Orchestration Training

StateGen's hierarchical extension enables complex multi-agent training:

**Use Case: Hierarchical Planning Agents**
- Master agent orchestrates sub-agents for different domains
- All agents share authoritative state
- Training ensures consistent multi-level decision-making
- Enables curriculum learning from simple to complex hierarchies

**Use Case: Multi-Skill Agent Systems**
- Each skill is a callable tool with state effect
- Master agent learns to sequence skills effectively
- Sub-agent interaction data generated naturally
- Hierarchical reasoning patterns captured in training

### 3. Privacy-Preserving Data Collection

StateGen solves the privacy problem for production systems:

**Production Deployment Benefits**:
- No real customer data needed for training
- Compliant with GDPR, financial regulations
- Faster iteration (generate data instantly vs. waiting for production patterns)
- Enables sharing of training data across teams

**Data Governance**:
- Synthetic data has clear non-sensitive origin
- Audit trail of generation process
- Reproducible data creation
- Clean separation from production data

## Insights & Implications

### 1. Structural Solutions Beat Post-Hoc Filtering

StateGen achieves 9.66/10 tool-call correctness through architectural design:
- Authoritative state manager prevents invalid calls by construction
- Not via filtering or ranking of bad outputs
- Agents learn valid patterns because hallucinated calls consistently fail
- Transfer to real systems is strong because learned patterns are robust

**Implication**: For agent systems, structural constraints on outputs are more reliable than training-based solutions. The tool environment itself should enforce correctness.

### 2. Persona Variation Improves Generalization

The 23-dimensional persona space enables:
- Agents trained on diverse personas generalize better
- Curriculum learning (simple→complex personas) improves sample efficiency
- Persona-specific fine-tuning addresses niche behaviors
- Cross-persona robustness becomes measurable

**Implication**: Variation in synthetic data is as important as volume. Controllable variation improves generalization.

### 3. Reasoning Traces Enable Better Learning

By capturing explicit reasoning in synthetic conversations:
- Agents learn to reason about state and tool preconditions
- Multi-step reasoning patterns transfer to new domains
- Interpretable policies emerge from supervised learning
- Generalization beyond seen tool patterns improves

**Implication**: Tool-augmented agent training should explicitly supervise reasoning, not just outputs. Intermediate reasoning steps guide policy learning.

### 4. Hierarchical Multi-Agent Training Requires Shared State

The shared state mechanism enables:
- Consistent multi-level decision-making
- Clear interfaces between agents
- Deterministic composition of behaviors
- Compositional reasoning about multi-agent systems

**Implication**: Hierarchical agent systems need explicit state objects, not implicit communication. Shared authoritative state is the key to correct composition.

## Code & Resources

### Implementation Components

**State Manager Core**:
```python
class AuthoritativeStateManager:
    def __init__(self):
        self.state = {}  # Current authoritative state
    
    def validate_precondition(self, operation, args):
        # Check if operation can execute with current state
        pass
    
    def execute_operation(self, operation, args):
        # Execute on state and return result
        result = self._apply_operation(operation, args)
        self.state = self._update_state(operation, args, result)
        return result
    
    def get_state_snapshot(self):
        # Return view of state for agent decision-making
        return self.state.copy()
```

**Persona System**:
```python
class PersonaSimulator:
    def __init__(self, trait_vector):
        self.traits = trait_vector  # 23-dimensional vector
    
    def generate_user_message(self, context):
        # Generate request respecting persona traits
        pass
```

**Four-Role Orchestration**:
```python
def generate_conversation(num_turns=10):
    user_sim = PersonaSimulator(random_persona_vector())
    agent = LLMAgent()
    state_mgr = AuthoritativeStateManager()
    judge = LLMJudge()
    
    conversation = []
    for _ in range(num_turns):
        user_msg = user_sim.generate_user_message()
        state_snapshot = state_mgr.get_state_snapshot()
        
        agent_output = agent.generate_response(user_msg, state_snapshot)
        tool_calls = parse_tool_calls(agent_output)
        
        tool_results = []
        for call in tool_calls:
            if state_mgr.validate_precondition(call):
                result = state_mgr.execute_operation(call)
                tool_results.append(result)
        
        turn_score = judge.score_turn(
            user_msg, agent_output, tool_results, state_mgr.state
        )
        conversation.append((user_msg, agent_output, tool_results, turn_score))
    
    return conversation
```

### Dependencies and Requirements

**Required Capabilities**:
- Multi-turn LLM inference (OpenAI, Anthropic, or open-source)
- State management and deterministic execution
- Tool API specification and validation

**Compute Requirements**:
- Per-conversation generation: 30-60 seconds
- 64,698 conversations: ~18-36k GPU-hours on efficient hardware
- Parallel generation across multiple workers

**Data Output Format**:
```json
{
  "conversation_id": "unique_id",
  "persona": {
    "traits": {...},
    "description": "..."
  },
  "turns": [
    {
      "user_message": "...",
      "agent_reasoning": "...",
      "agent_tool_calls": [...],
      "tool_results": [...],
      "turn_score": {
        "correctness": 0.95,
        "reasoning_quality": 0.88,
        "user_satisfaction": 0.92
      }
    }
  ],
  "conversation_score": {...},
  "hallucination_score": 9.66
}
```

### Integration with Agent Training

**Training Pipeline**:
1. Generate StateGen conversational data (64,698 conversations)
2. Extract (input, tool_call, result) triples for supervised learning
3. Fine-tune base LLM on tool-use prediction
4. Evaluate on held-out test set from StateGen
5. Deploy and monitor in production

**Curriculum Learning**:
```
Phase 1: Train on simple personas (10k conversations)
Phase 2: Add medium personas (15k conversations)
Phase 3: Add complex personas (20k conversations)
Phase 4: Add adversarial personas (5k conversations)
```

## Related Work & Context

### Synthetic Data Generation for LLMs

StateGen advances the state of synthetic data generation by addressing specific challenges:

**Previous Approaches**:
- Template-based generation: Rigid, unnatural, limited reasoning
- Paraphrasing real data: Privacy-risky, labor-intensive
- Simple prompting: Prone to hallucinations, inconsistent state

**StateGen Innovations**:
- Authoritative state management eliminates hallucinations structurally
- Persona variation enables controlled diversity
- Multi-agent coordination enables hierarchical systems
- Production-scale evaluation on real corpora

### Tool Use in LLMs

Tool-augmented LLMs are an active research area. StateGen contributes to:

- **Improving tool-call accuracy**: Hallucination elimination through state grounding
- **Training efficiency**: Synthetic data removes data collection bottleneck
- **Generalization**: Persona variation improves transfer to new users/scenarios
- **Hierarchical tool use**: Shared state enables multi-agent tool orchestration

### Multi-Agent Systems

StateGen's hierarchical extension connects to broader multi-agent research:

- **Coordination mechanisms**: Shared authoritative state as coordination primitive
- **Information sharing**: State snapshots provide agent observability
- **Consistency guarantees**: Deterministic state updates ensure consistency
- **Scalability**: State management patterns scale to larger agent hierarchies

### Future Directions

**Immediate Extensions**:
- Asynchronous multi-agent interactions with eventual consistency
- Tool API learning (agents discover tools dynamically)
- Adversarial data generation (test robustness)
- Real-time persona adaptation during conversation

**Research Opportunities**:
- Formal verification of tool-use correctness
- State abstraction learning (agents learn relevant state dimensions)
- Constraint satisfaction in multi-agent coordination
- Integration with reinforcement learning for tool-use optimization

## Summary

StateGen presents a novel approach to training tool-augmented LLM agents through structured synthetic data generation. By introducing an authoritative state manager and persona-driven user simulation, it achieves:

1. **Elimination of tool-call hallucinations** (9.66/10 score) through structural design
2. **Production-scale training data** (64,698 conversations) from private API simulators
3. **Persona-driven diversity** enabling robust generalization
4. **Hierarchical multi-agent support** through shared state patterns

For the broader community working on agent systems, StateGen demonstrates that:
- **Structural constraints** are more reliable than post-hoc filtering
- **Authoritative state management** is fundamental to multi-agent correctness
- **Synthetic data** can be production-grade when properly designed
- **Tool environments** should enforce correctness, not just agents

These insights are broadly applicable across autonomous systems, multi-agent coordination, and interactive LLM applications.
