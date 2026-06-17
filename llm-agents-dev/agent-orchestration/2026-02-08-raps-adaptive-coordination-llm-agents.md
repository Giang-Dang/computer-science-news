# Towards Adaptive, Scalable, and Robust Coordination of LLM Agents: A Dynamic Ad-Hoc Networking Perspective

**Paper ID:** arXiv:2602.08009  
**Submitted:** February 8, 2026  
**Authors:** Multiple authors from collaborative institutions

---

## Executive Summary

RAPS (Reputation-Aware Publish-Subscribe) introduces a paradigm for dynamically coordinating multiple LLM-based agents without static orchestration templates. By adapting principles from distributed ad-hoc networking, RAPS enables agents to declare intents, discover capabilities, and collaborate through decentralized communication while maintaining trustworthiness through Bayesian reputation tracking. The framework addresses a critical operational challenge: **manual orchestration of multi-agent workflows does not scale** as agent populations grow and task complexity evolves.

---

## Problem Statement

Traditional multi-agent orchestration relies on **static organizational structures** defined before execution:
- Hierarchical coordination with fixed agent roles
- Predefined message-passing patterns
- Centralized orchestrator making routing decisions
- Rigid topologies that cannot adapt to task complexity changes

**Limitations of Static Orchestration:**
1. **Scalability Bottleneck:** Centralized orchestrator becomes performance bottleneck with many agents
2. **Adaptivity Constraints:** Predefined topologies cannot adjust as task complexity changes
3. **Agent Heterogeneity:** Cannot accommodate agents with varying capabilities and reliability
4. **Communication Overhead:** Static topologies may route messages inefficiently
5. **Robustness Issues:** Single point of failure in centralized orchestrator; no graceful degradation

**The Coordination Challenge:**

```
Problem Scenario:
- 100+ specialized agents available
- Distributed across geographic locations
- Varying capabilities, reliability, and latency
- Complex multi-step tasks requiring agent composition
- Task characteristics may not be known in advance

Traditional Solution (Static Orchestrator):
├─ Hardcode routing: Agent A → Agent B → Agent C → ...
├─ Expected at design time: What agents are available?
├─ Expected at design time: What capabilities they possess?
├─ Expected at design time: Which are trustworthy?
└─ Result: Inflexible, cannot adapt

Desired Solution (RAPS):
├─ Agents declare intents dynamically
├─ Runtime discovery of capabilities
├─ Trust-based routing (reputation-aware)
└─ Adaptive patterns based on agent behavior
```

**Research Gap:** No existing framework provides adaptive, decentralized coordination of heterogeneous LLM agents while maintaining robustness under agent failures.

---

## Core Concepts & Theory

### Distributed Publish-Subscribe Paradigm

RAPS builds on the **Distributed Publish-Subscribe Protocol**, a well-established pattern in distributed systems. The key insight: agents exchange messages based on **declared intents** rather than predefined static routings.

#### Publish-Subscribe Communication Model

```
TRADITIONAL POINT-TO-POINT:
Agent A ---hardcoded---> Agent B
         (fixed routing)

PUBLISH-SUBSCRIBE:
Agent A publishes intent     Agent B subscribes to intent
"I need code review"      ← connects to → "I provide code review"
                          at runtime
         ↓
     Message Queue
         ↓
    Agent B receives message
```

**Key Advantages:**
- **Decoupling:** Publishers don't know subscribers; subscribers don't know publishers
- **Scalability:** Message brokers handle fan-out without central bottleneck
- **Adaptivity:** New agents can subscribe/publish without system reconfiguration
- **Robustness:** Multiple agents can provide same service (fault tolerance)

### Reactive Subscription

**Problem:** Agents' intents may change as tasks evolve. A code generation agent might request code review after generating code, but not all code generation tasks require review.

**Solution: Reactive Subscription**

Agents can dynamically subscribe to intents in response to task execution:

```
Agent Flow with Reactive Subscription:
┌──────────────────────────┐
│ 1. Code Generation Task  │
│    Subscribe to:         │
│    "code.generation"     │
└──────────────────────────┘
           ↓
┌──────────────────────────┐
│ 2. Generate Code        │
│    Evaluate quality      │
└──────────────────────────┘
           ↓
      ┌─────────────┐
      │ Quality OK? │
      └─────────────┘
         /        \
      YES          NO
      /              \
    End          Subscribe to:
                 "code.review"
                      ↓
                  Publish review
                     request
```

**Implementation:**
- Agents monitor their own execution progress
- On conditional outcomes, agents subscribe/unsubscribe from intents
- Subscription changes are propagated to pub-sub broker
- No central coordinator aware of these runtime decisions

### Bayesian Reputation System

**Problem:** Not all agents are equally reliable. Some agents may:
- Fail intermittently
- Produce low-quality results
- Have higher latency than others
- Be untrustworthy or malicious

**Solution: Trust-Based Routing via Reputation**

The framework maintains a **Bayesian reputation model** for each agent:

```
Agent Reputation Model:
├─ Prior belief: P(reliable)
├─ Evidence: outcome of interactions
│  ├─ Success → update belief upward
│  ├─ Failure → update belief downward
│  └─ Timeout → moderate downward update
└─ Posterior: Updated trust score
```

**Bayesian Update Formula (Conceptual):**

```
P(agent_reliable | observations) 
  ∝ P(observations | agent_reliable) × P(agent_reliable)
```

**Reputation State:**
- Starts as neutral (weak prior)
- Accumulates evidence from successful/failed interactions
- Decays over time (recent evidence weighted more)
- Used to rank available agents when multiple candidates exist

**Application to Routing:**

```
Task: "Code review needed"
Available agents: 
  - Agent_X (reputation: 0.95)
  - Agent_Y (reputation: 0.60)
  - Agent_Z (reputation: 0.40)

Routing decision: Route to Agent_X
(highest reputation)

Alternative: Risk-aware routing
  - Route to Agent_X with 95% confidence
  - Route to Agent_Y with 5% confidence (for learning)
  - Rarely route to Agent_Z (low trust)
```

### Multi-Layer Coordination Architecture

RAPS proposes a multi-layer coordination topology:

```
Coordination Architecture:

Layer 1: Task Layer (Application-Level)
├─ Task specification
├─ Goal definition
└─ Success criteria

Layer 2: Intent Declaration Layer
├─ Agents declare capabilities
├─ Agents declare intent requirements
└─ Pub-Sub broker maintains mappings

Layer 3: Routing & Reputation Layer
├─ Reputation tracking
├─ Intelligent routing decisions
├─ Load balancing
└─ Failure recovery

Layer 4: Communication Layer
├─ Message passing
├─ Acknowledgments
└─ Timeout handling
```

---

## Main Ideas & Contributions

### 1. Decentralized Agent Coordination

**Key Innovation:** Moving from centralized orchestrator to decentralized publish-subscribe coordination

**Benefits:**
- No single point of failure
- Linear scalability with agent count (not bottleneck at central orchestrator)
- Agents can join/leave without system reconfiguration
- Automatic load balancing (multiple agents provide same service)

**Example - Code Generation Pipeline:**

```
CENTRALIZED (Traditional):
┌──────────────┐
│  Orchestrator│ (single point of failure)
│   (decides   │
│   routing)   │
└──────────────┘
     ↙    ↘
  Plan   Code Gen    Reviews
  Agent   Agent      Agent

DECENTRALIZED (RAPS):
┌─────────────────────────────────────┐
│    Pub-Sub Broker (distributed)     │
└─────────────────────────────────────┘
    ↙        ↓        ↓      ↘
 Plan       Code      Reviews  Test
 Agent      Gen       Agent   Agent
(subscribes (publishes (subscribes (subscribes
 to "plan.  to        to "review. to
 request")  "plan")   request")   "test.request")
```

### 2. Intent-Based Service Discovery

**Traditional:** Hardcode which agent provides which service

**RAPS:** Agents declare capabilities through intent subscriptions

```
Agent Capability Declaration (at startup):
├─ Code Generation Agent:
│  ├─ Publishes to: "code.generation"
│  └─ Subscribes to: "code.generation.request"
├─ Code Review Agent:
│  ├─ Publishes to: "code.review"
│  └─ Subscribes to: "code.review.request"
└─ Testing Agent:
   ├─ Publishes to: "test.execution"
   └─ Subscribes to: "test.execution.request"
```

**Runtime Service Discovery:**
- Task manager queries broker: "Who can do code review?"
- Broker returns all agents subscribing to "code.review.request"
- Task manager selects based on reputation and load
- Completely dynamic; no hardcoding required

### 3. Trustworthy Decentralized Collaboration

**Challenge:** How to maintain system integrity when agents are autonomous and potentially unreliable?

**RAPS Solution:** Reputation-aware routing + validation

```
Interaction Flow with Reputation:
1. Task manager needs code review
2. Query broker for code review agents
3. Broker returns available agents with reputations
4. Select top-reputation agent
5. Submit code for review
6. Validate result (code review quality)
7. Update agent reputation based on outcome
8. Future tasks will use updated reputation
```

**Cascading Benefits:**
- Poor-performing agents naturally receive fewer tasks
- Good agents build reputation and receive more work
- System self-corrects without human intervention
- Incentivizes agents to perform well

### 4. Adaptive Workflow Topology

**Traditional Workflow:**
```
Task → Plan (Agent A) → Code Gen (Agent B) → Review (Agent C) → Test (Agent D)
```

**RAPS Adaptive Workflow:**

```
Task → Available Planning Agents
            ↓
     Select Top Reputation
            ↓
       Generate Plan
            ↓
    Evaluate Plan Quality
            ↓
  Branch on Complexity Score:
    ├─ Simple: Direct to Code Gen
    ├─ Medium: Plan → Design Review → Code Gen
    └─ Complex: Plan → Design → Implementation Stages
            ↓
     Code Generation Phase
            ↓
   Available Code Gen Agents
            ↓
   Route to Top Reputation
            ↓
   (continue adaptively...)
```

---

## Methodology & Implementation

### System Architecture

**Components:**

```
RAPS System Components:

┌─────────────────────────────────┐
│  Pub-Sub Message Broker         │
│  (Central communication hub)     │
│  ├─ Intent registry             │
│  ├─ Message queue               │
│  └─ Routing table               │
└─────────────────────────────────┘
         ↑ ↓ ↑ ↓ ↑ ↓
    ┌─────────────────────┐
    │   Reputation Store  │
    │  (Trust tracking)   │
    └─────────────────────┘
         ↑ ↓ ↑ ↓ ↑ ↓
    [Agent 1] [Agent 2] ... [Agent N]
    (LLM-based specialized agents)
```

### Pub-Sub Protocol Implementation

**Message Format:**

```json
{
  "type": "intent_subscription",
  "agent_id": "code_review_agent_1",
  "intent": "code.review.request",
  "capabilities": {
    "max_files": 10,
    "max_loc": 5000,
    "supported_languages": ["Python", "Java", "Go"]
  },
  "timestamp": "2026-02-08T10:30:00Z"
}
```

**Pub-Sub Operations:**

1. **Subscribe:** Agent declares ability to handle intent
2. **Publish:** Agent requests service from available subscribers
3. **Route:** Broker selects best subscriber based on reputation
4. **Deliver:** Broker sends message to selected agent
5. **Acknowledge:** Agent confirms receipt
6. **Validate:** Task manager validates outcome
7. **Update Reputation:** Broker updates agent's reputation

### Reputation Model Implementation

**Bayesian Reputation Update:**

```
For each interaction outcome:
  If SUCCESS:
    reputation ← reputation + alpha × (1 - reputation)
  Else If FAILURE:
    reputation ← reputation - beta × reputation
  Else If TIMEOUT:
    reputation ← reputation - gamma × reputation

Where:
  alpha = reward factor for success (e.g., 0.1)
  beta = penalty factor for failure (e.g., 0.3)
  gamma = penalty factor for timeout (e.g., 0.15)
```

**Decay Over Time:**

```
reputation(t) ← reputation(t-1) × decay_factor
Where:
  decay_factor = 0.99^(hours_since_last_update)
```

### Experimental Setup & Evaluation

**Benchmarks Tested (illustrative):**

[Exact figures unavailable — see full paper]

**Five Diverse Benchmark Domains:**
1. Code generation and review (software development)
2. Mathematical reasoning (proof verification)
3. Multi-step planning (task orchestration)
4. Information retrieval and synthesis
5. Creative content generation (requiring subjective quality assessment)

**Evaluation Metrics:**

| Metric | Measures | Importance |
|--------|----------|-----------|
| Task Success Rate | % tasks completed successfully | Primary |
| Latency | Mean time from task to completion | Operational |
| Scalability | Performance with increasing agents | Infrastructure |
| Robustness | Handling of agent failures | Reliability |
| Resource Efficiency | Message overhead, routing efficiency | Cost |
| Reputation Accuracy | How well reputation reflects actual agent quality | System Health |

**Results Summary:**

[Exact figures unavailable — see full paper]

Extensive experiments across five diverse benchmarks demonstrate:
- Superior performance compared to static orchestration
- Effective adaptation to agent failures and varying capabilities
- Consistent improvement with increased agent specialization
- Reputation system accurately identifies high-quality agents
- Graceful degradation when agents fail (alternative agents engaged)

---

## Practical Applications & Use Cases

### 1. Large-Scale Code Generation and Testing

**Scenario:** Enterprise needs code generation, testing, and review across 50+ specialized agents

```
Traditional Approach:
├─ Hardcode routing rules for each task type
├─ Predict which agents will be available
├─ No adaptation if agent fails
└─ Central orchestrator becomes bottleneck

RAPS Approach:
├─ Each agent declares capabilities
├─ Task router queries available agents
├─ Routes to highest-reputation agents
├─ Automatically falls back if agent fails
└─ Reputation system identifies poor performers
```

**Operational Benefits:**
- Agents can be added/removed without system reconfiguration
- New agent types automatically discovered via intent declarations
- Poor-performing agents naturally receive fewer tasks
- System self-optimizes task routing over time

### 2. Multi-Domain Problem Solving

**Scenario:** Complex task requiring diverse agent types (research, coding, analysis, writing)

```
Task: "Implement new algorithm and write research paper"

RAPS Workflow:
1. Query broker: "Which agents can research algorithms?"
   → Returns [Researcher_A, Researcher_B, Researcher_C]
   → Select Researcher_A (highest reputation)
2. Research phase completes
3. Query broker: "Which agents can implement in Python?"
   → Returns [Coder_1, Coder_2, Coder_3, Coder_4]
   → Select Coder_1 (high reputation, lower latency)
4. Implementation completes
5. Query broker: "Which agents can write research papers?"
   → Returns [Writer_1, Writer_2]
   → Select Writer_1 if reputation good, else Writer_2
6. Paper completed

All decisions made adaptively based on:
- Current agent availability
- Reputation scores
- Estimated latency
- Task complexity
```

### 3. Fault-Tolerant Long-Running Workflows

**Scenario:** Multi-day task requiring multiple agents, with potential for agent failures

```
Without RAPS (Static Orchestrator):
Day 1: Agent_X handles phase 1
Day 2: Agent_X fails
       → Entire workflow fails
       → Manual intervention needed to reconfigure

With RAPS (Adaptive Routing):
Day 1: Agent_X handles phase 1
Day 2: Agent_X fails, but:
       → Broker detects failure
       → Routes to Agent_Y (next highest reputation)
       → Phase 2 continues without interruption
       → Agent_X reputation decreases (less future use)
```

### 4. Heterogeneous Agent Populations

**Scenario:** Mix of fast/slow, reliable/flaky, specialized/generalist agents

```
Agent Registry:
├─ Fast code generators (high latency variance)
│  └─ Good for: exploratory generation, quick iterations
├─ Slow code generators (low latency variance)
│  └─ Good for: production code, critical paths
├─ Reliable reviewers (high reputation)
│  └─ Good for: high-stakes review
├─ Experimental agents (low reputation initially)
│  └─ Good for: learning, low-risk tasks
└─ Specialized agents (niche capabilities)
   └─ Good for: domain-specific tasks

RAPS Routing:
Quick task: Route to fast agent (accept variance)
Critical task: Route to reliable agent (worth latency cost)
Learning: Route to experimental agent (build reputation)
Specialized domain: Route to domain expert (highest reputation)
```

---

## Insights & Implications

### 1. Decentralization as Scalability Strategy

The paper demonstrates that **decentralized coordination scales better than centralized** for autonomous agent systems:
- Centralized orchestrator I/O becomes bottleneck at ~100 agents
- Decentralized pub-sub avoids bottleneck (scales to 1000s)
- Trade-off: increased message overhead, but acceptable for most use cases

### 2. Reputation as the Coordination Currency

In large agent populations, **reputation becomes the primary coordination mechanism**:
- Agents with high reputation receive more work
- Poor performers naturally receive less work
- System self-balances without explicit load distribution
- Incentive structure aligns agent performance with system health

### 3. Adaptivity Through Reactive Subscription

The framework shows that **agents can control their own engagement**:
- Agents subscribe/unsubscribe based on task progress
- No central coordinator decides workflow topology
- Enables complex adaptive workflows without hardcoding
- Particularly powerful for multi-step tasks with branching

### 4. Intent-Based Service Discovery

Declaring capabilities through **intent subscription** enables:
- New agents added without system reconfiguration
- Dynamic capability discovery at runtime
- Automatic balancing across agents with same capability
- Natural evolution of agent populations

### 5. Limitations and Challenges

- **Message Overhead:** Pub-sub introduces network overhead compared to direct point-to-point
- **Consistency:** Distributed system must handle eventual consistency
- **Reputation Gaming:** Agents could potentially manipulate reputation (requires robust validation)
- **Warm-up Period:** New agents start with neutral reputation; building trust takes time
- **Privacy:** Pub-sub broker sees all agent intents and interactions

---

## Code & Resources

### Reference Implementation

**Key Technology Stack:**
- **Message Broker:** Apache Kafka, RabbitMQ, or NATS (distributed pub-sub)
- **Reputation Store:** Redis or similar for fast reputation lookups
- **Intent Registry:** Elasticsearch or similar for service discovery
- **Agent Framework:** LangChain, AutoGen, or custom agent orchestration framework

### Integration Points

**With Existing Agent Frameworks:**

```python
# Pseudo-code: RAPS integration with agent framework

class RAPSCoordinatedAgent:
    def __init__(self, agent_type, capabilities):
        self.agent_type = agent_type
        self.broker = PublishSubscribeBroker()
        
    def startup(self):
        # Declare capabilities
        self.broker.subscribe(f"{self.agent_type}.request")
        
    def handle_task(self, task):
        # Process task
        result = self.execute(task)
        
        # Reactive subscription: subscribe to next phase if needed
        if needs_review(result):
            self.broker.subscribe("code.review.request")
        
        # Publish result for next agent
        self.broker.publish("code.review.request", result)
        
        return result
```

### Deployment Considerations

**Operational Checklist:**
- Set up distributed pub-sub broker (Kafka, RabbitMQ)
- Deploy reputation tracking service
- Configure message serialization (JSON, Protobuf)
- Set up monitoring for message latency and delivery
- Implement fallback routing if broker fails
- Configure agent timeout thresholds
- Set up reputation decay schedule

### Quick-Start Integration Guide

1. **Select Message Broker:** Deploy Kafka or RabbitMQ
2. **Define Intent Taxonomy:** Specify intent names (e.g., "code.generation.request")
3. **Implement Reputation Service:** Track agent success/failure rates
4. **Update Agent Framework:** Add intent subscription/publishing capabilities
5. **Deploy Agents:** Have agents declare intents on startup
6. **Monitor and Tune:** Track reputation scores, message latency, routing decisions

---

## Related Work & Context

### Foundational Distributed Systems Work
- **Pub-Sub Systems:** Original publish-subscribe protocols and implementations
- **Ad-Hoc Networks:** Dynamic networking concepts applied to agents
- **Distributed Trust:** Reputation systems in peer-to-peer networks
- **Load Balancing:** Techniques for distributing work across heterogeneous resources

### Related Multi-Agent Research
- Static orchestration frameworks (AutoGen, LangChain orchestrators)
- Hierarchical multi-agent coordination
- Agent capability representation and discovery
- Multi-agent reinforcement learning for task allocation

### Complementary Papers in This Collection
- Multi-Agent Collaboration via Evolving Orchestration (2505.19591) - RL-based orchestrator
- Knowledge Activation (2603.14805) - Skill-based agent capabilities
- Orchestration of Multi-Agent Systems (2601.13671) - MCP-based coordination
- From Static Templates to Dynamic Runtime Graphs (2603.22386) - Workflow optimization

### Future Research Directions

1. **Byzantine-Robust Reputation:** Defense against reputation gaming
2. **Privacy-Preserving Pub-Sub:** Hiding agent intents from broker
3. **Optimal Reputation Decay:** Learn decay schedule from empirical data
4. **Cross-Organization Agent Markets:** RAPS for agents from different organizations
5. **Hybrid Hierarchical-Peer Coordination:** Combine RAPS with hierarchical layers
6. **Emergent Specialization:** Agents specialize in niches through reputation evolution
7. **Formal Guarantees:** Theoretical analysis of convergence and optimality

---

## References

- arXiv:2602.08009 - Towards Adaptive, Scalable, and Robust Coordination of LLM Agents: A Dynamic Ad-Hoc Networking Perspective
- arXiv:2601.13671 - The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption
- arXiv:2505.19591 - Multi-Agent Collaboration via Evolving Orchestration
- arXiv:2603.22386 - From Static Templates to Dynamic Runtime Graphs: A Survey of Workflow Optimization for LLM Agents
