# Usable Agent Discovery for Decentralized AI Systems

## Executive Summary

This paper addresses a critical infrastructure challenge for large-scale decentralized multi-agent systems: how agents efficiently discover and locate one another in peer-to-peer networks with high churn (agents and nodes frequently joining/leaving). The authors evaluate two discovery paradigms—structured overlays (Kademlia-based) and gossip-based mechanisms (Cyclon with Vicinity heuristics)—across realistic failure scenarios. The findings demonstrate that gossip-based discovery with local proximity optimization achieves superior trade-offs between routing efficiency, resilience, and service readiness, establishing practical foundations for deploying autonomous AI systems on distributed, unreliable infrastructure without centralized coordination.

## Problem Statement

Building decentralized multi-agent AI systems at scale requires solving a fundamental infrastructure problem: **agent discovery**—enabling agents to locate and communicate with relevant peers in networks where:

- **Participants are dynamic**: Agents and nodes join/leave frequently (network churn)
- **No centralized authority exists**: No DNS, no service registry, no centralized broker
- **Scale is large**: Potentially millions of agents across distributed nodes
- **Resources are heterogeneous**: Variable latency, bandwidth, and computational capabilities
- **Trust is distributed**: Agents may not have pre-established relationships

Traditional centralized approaches (service meshes, registry servers like Consul/Eureka) become bottlenecks and single points of failure. Peer-to-peer overlays (like BitTorrent/IPFS) exist but were not designed for agent-specific requirements: semantic understanding of agent capabilities, real-time discovery latency requirements, and support for multi-dimensional agent properties (skills, availability, reliability).

Prior distributed systems research addressed this for generic network services. However, LLM agents have unique requirements:
- Need to discover agents with specific **capabilities** (language models, tools, reasoning abilities)
- May need to verify agent **availability** before attempting remote calls (not just existence)
- Benefit from **reputation tracking** and quality-of-service metrics
- Require low **discovery latency** to enable responsive multi-step reasoning

This paper is the first to systematically evaluate agent discovery mechanisms under realistic agent churn scenarios.

## Core Concepts & Theory

### Network Churn and Its Impact

**Churn** refers to the rate at which participants leave and rejoin the network. The paper identifies two types:

1. **Node-level churn**: Physical machines or containers hosting agents go down/restart
2. **Agent-level churn**: Individual agents shutdown or migrate (while their hosting node persists)

Churn affects overlay network stability in several ways:
- **Routing table staleness**: Nodes in your routing table may have left, requiring re-discovery
- **Service availability**: Locating an agent is not enough; it must be reachable and responsive
- **Cascading failures**: If an important hub node leaves, many discovery paths become invalid

### Discovery Mechanism Categories

#### A. Structured Overlays (DHT-Based)

**Kademlia**, used in BitTorrent and Ethereum, organizes nodes in a tree-like structure based on XOR distance in keyspace.

**Core mechanism:**
```
Agent A wants to find agent B (target key)
1. Compute XOR(A_id, B_id)
2. Route toward B through intermediate nodes that share 
   increasingly long bit prefixes with B
3. Converge on B's location after log(N) hops
```

**Advantages:**
- Guaranteed convergence (if target exists)
- Logarithmic lookup latency O(log N)
- Deterministic routing enables caching and optimization
- Proven at scale (billions of nodes in Ethereum)

**Disadvantages:**
- High maintenance cost under churn (routing tables must be continuously updated)
- Delayed detection of failures (stale entries point to dead nodes)
- Poor performance under concentrated churn patterns
- Uneven load distribution

#### B. Gossip-Based Overlays

Gossip protocols (also called epidemic protocols or rumor-spreading) operate through random peer-to-peer sampling:

**Basic gossip mechanism:**
```
Every Δt seconds, node A:
1. Randomly selects peer B
2. Exchanges state (e.g., list of seen agents)
3. Both nodes update their local views
```

**Cyclon Protocol** (analyzed in this paper):
- Maintains a small **view** (list of peer descriptors)
- Periodically swaps partial views with random peers
- Uses **ageing** to naturally evict stale entries

**Vicinity Heuristic** (proposed for agent discovery):
- Prioritize gossip with agents that have low latency
- Preference for agents with desired capabilities
- Trade-off: Locality bias vs. network coverage

**Advantages:**
- Adaptive to churn (stale entries naturally evicted through randomness)
- High resilience (no critical paths or hubs to fail)
- Simple to implement and reason about
- Fair load distribution

**Disadvantages:**
- Slower convergence (search time is O(log² N) or higher)
- "Push-based" gossip is unreliable (message loss accepted)
- Difficult to guarantee hard constraints (e.g., must find agent within 5 seconds)

### Hybrid Approaches

The paper also explores **structured + gossip hybrids**:
- Use Kademlia for core routing efficiency
- Augment with gossip to repair and maintain overlay under churn
- Balance of guaranteed performance with robustness

### Service Readiness vs. Discovery

A critical insight: **Finding an agent is not enough; it must be reachable and responsive.**

The paper defines **Service Readiness** metrics:
- **Reachability**: Network path exists and agent is online
- **Responsiveness**: Agent responds to discovery pings within SLA
- **Capability Match**: Agent has required skills/features

Discovery mechanisms that optimize for discovery latency alone may return agents that are:
- No longer running (network partition, crash)
- Overloaded (high latency responses)
- Incompatible with your requirements

## Methodology & Implementation

### Experimental Setup

**Simulation Environment:**
- Custom discrete-event simulator built in Python
- Implemented Kademlia (structured) and Cyclon+Vicinity (gossip)
- Modeled network conditions: latency distributions, packet loss

**Agent Population:**
- Simulated 1,000 to 100,000 agents
- Agents organized in a 2D capability space (simulating diverse skills)
- Random and Zipfian churn distributions

**Churn Scenarios:**

| Scenario | Node Churn Rate | Agent Churn Rate | Description |
|---|---|---|---|
| **Stable** | 0.1% per minute | 0.05% per minute | Enterprise data center |
| **Moderate** | 1% per minute | 0.5% per minute | Cloud with auto-scaling |
| **High** | 5% per minute | 2% per minute | Mobile/edge networks |
| **Bursty** | 20% in 10 seconds | 10% in 10 seconds | Cascading failures |

### Metrics Evaluated

1. **Discovery Latency**: Time to locate target agent (median, 95th percentile)
2. **Success Rate**: Percentage of lookups that successfully find a reachable agent
3. **Maintenance Overhead**: Network traffic for protocol housekeeping
4. **Service Readiness**: Fraction of discovered agents that respond within timeout

### Key Findings

#### Finding 1: Structured Overlays Break Under Moderate Churn
- Kademlia performance degrades sharply when node churn exceeds 1% per minute
- Lookup success drops from 99.9% (stable) to 65% (moderate churn) within 30 seconds
- Routing table corruption requires expensive repairs

**Reason**: Kademlia assumes stable network topology; churn invalidates routing assumptions.

#### Finding 2: Gossip-Based Discovery is Resilient but Slower
- Cyclon + Vicinity maintains >95% success rate even under 5% node churn
- Discovery latency increases from 200ms (stable) to 2-5 seconds (high churn)
- Gossip overhead scales poorly with agent count (linear memory per node)

**Insight**: Acceptable latency trade-off for systems where occasional delays are tolerable.

#### Finding 3: Hybrid Approach Achieves Best Trade-Off
- Kademlia core routing for known peers + gossip-based repair
- Maintains 99%+ success rate under 2% node churn
- Latency: ~300ms stable, ~800ms under churn
- Memory overhead: 10% higher than pure Kademlia

#### Finding 4: Vicinity Heuristic Significantly Improves Performance
- Adding capability and latency awareness to gossip increases "useful discovery" by 40%
- Reduced cascading lookups (agents need fewer re-searches for failing peers)
- Trade-off: Slightly reduced network coverage (agents in distant regions discovered slower)

#### Finding 5: Service Readiness is Often Overlooked
- 15-20% of discovered agents fail to respond within timeout
- Likely caused by temporary overload or transient network issues
- Active probing / heartbeating could improve this, but adds overhead

## Practical Applications & Use Cases

### 1. **Decentralized LLM Agent Networks**

**Scenario**: Open-source LLM agent framework where independent developers deploy agents to solve problems collaboratively.

**Application**:
- Agents discover specialized peers (e.g., "SQL expert", "vision model", "document processor")
- Use gossip-based discovery with Vicinity heuristics prioritizing recent/responsive agents
- Agents form dynamic teams without centralized orchestration

**Benefits**:
- No single point of failure (no central registry)
- Natural inclusion of new agents (they receive gossip about the network)
- Graceful handling of agent failures (alternatives discovered through gossip)

**Implementation**: Could be used by frameworks like:
- Open-source agent networks (CrewAI or AutoGen deployments)
- Blockchain-integrated AI (agents as smart contracts)

### 2. **Edge/Mobile Agent Networks**

**Scenario**: Agents deployed on mobile devices, edge servers, or IoT devices with frequent connectivity changes.

**Application**:
- Hybrid gossip + structured approach tolerates device churn
- Gossip-based discovery accommodates brief connectivity windows
- Local agent clustering (Vicinity heuristic) reduces cross-region traffic

**Use Case Example - Smart City**:
- Traffic optimization: Vehicle agents, traffic light agents, navigation agents
- High churn: Vehicles enter/leave constantly
- Requirement: Discover nearest traffic agent in <500ms
- Solution: Gossip-based discovery with geolocation Vicinity

### 3. **Federated Learning with Agent Collaboration**

**Scenario**: ML training across organizations where agents (representing datasets, models, compute resources) must discover each other.

**Application**:
- Privacy-preserving discovery (agents advertise capabilities without revealing identity)
- Structured discovery for trusted partners (intra-organization)
- Gossip for inter-organization discovery (less trusted paths)
- Service readiness verification prevents wasted transfers to failed partners

### 4. **Large-Scale RL Agent Training**

**Scenario**: Thousands of agents training in parallel, occasionally failing and restarting.

**Application**:
- Agents use discovery to locate experience replay partners
- Hybrid approach: Structured core (coordinating RL algorithm) + gossip (fault tolerance)
- Vicinity heuristic matches agents with similar experience distributions

## Insights & Implications

### Broader Field Impact

1. **Establishes Baselines for Decentralized Agent Systems**
   - Before this work: Practitioners chose gossip vs. structured ad-hoc
   - After this work: Data-driven comparison enables informed decisions
   - Likely to become reference for edge computing + AI research

2. **Challenges Centralized Assumptions in Cloud-Native Agent Development**
   - Many agent frameworks (AutoGen, Crew AI) assume centralized orchestration
   - This work demonstrates decentralized alternatives are viable
   - May drive development of "cloud-native" agent frameworks

3. **Informs Standardization** 
   - As decentralized AI becomes strategic (sovereign AI, resilient systems), standardized agent discovery becomes essential
   - Taxonomy of mechanisms in this paper could inform standards development

### State-of-the-Art Advancement

**Before**: Decentralized agent systems were viewed as impractical; industry defaulted to centralized service meshes (Kubernetes, Consul).

**After**: Decentralized discovery is practical and often preferable for resilience and avoiding single points of failure. Expected to accelerate adoption of peer-to-peer agent architectures.

### Limitations and Open Questions

1. **Byzantine Adversaries**: Analysis assumes honest agents; doesn't address malicious agents providing false discovery information.

2. **Quality-of-Service Guarantees**: No probabilistic latency bounds (e.g., "99th percentile latency < 1 second with probability 0.95").

3. **Heterogeneous Capability Spaces**: Current simulation uses simple 2D capability space; real agents have high-dimensional, semantic capability descriptions.

4. **Integration with Agent Reasoning**: Discovery mechanisms are studied independently from agent decision-making; tight coupling might enable better results.

5. **Privacy-Preserving Discovery**: Current approaches leak information about agent presence/capabilities; privacy-preserving variants unexplored.

6. **Recovery from Network Partitions**: Behavior when the agent network splits into isolated components not thoroughly analyzed.

## Code & Resources

### Official Paper & Repository
- **ArXiv**: https://arxiv.org/abs/2604.23080
- **PDF**: https://arxiv.org/pdf/2604.23080
- **Publication Date**: April 25, 2026

### Relevant Open-Source Implementations

**Structured Overlays (Kademlia)**:
- **libp2p**: https://github.com/libp2p/go-libp2p (IPFS/Ethereum foundation)
- **Chord Implementation**: https://github.com/go-chord/chord
- **Pastry/Bamboo**: Historical implementations

**Gossip Protocols**:
- **Cyclon**: https://github.com/pfouto/cyclon-java (reference implementation)
- **HyParView**: https://github.com/pfouto/hyparview (hierarchical gossip)
- **Serf**: https://github.com/hashicorp/serf (real-world gossip system)

**Hybrid Approaches**:
- **SWIM Protocol**: https://github.com/hashicorp/memberlist
- **Cassandra's Gossip**: https://cassandra.apache.org/ (production system)

### Simulation Code

The paper's experimental setup (simulator, protocols, scenarios) is likely to be released or could be reimplemented:

**Dependencies**:
- Python 3.8+
- Simpy (discrete-event simulation)
- NetworkX (graph algorithms)
- Numpy/Matplotlib (analysis/visualization)

**Quick-Start for Evaluation**:

```bash
# (Conceptual - exact code to be confirmed from paper)
pip install simpy networkx

# Run simulation comparing discovery mechanisms
python simulate_discovery.py --churn-rate 0.01 --num-agents 10000 \
  --mechanisms kademlia gossip hybrid

# Analyze results
python analyze_results.py results/simulation_*.json
```

### Dependencies and Compute Requirements

- **No specialized hardware required**: CPU-only simulation feasible on commodity laptops
- **Execution time**: Simulating 10,000 agents for 1 hour of virtual time: ~5-30 minutes wall-clock (depending on fidelity)
- **Memory**: ~500MB-2GB for large agent population simulations

### Quick-Start Guide for Application

1. **Assess your churn rate**: Monitor how often agents/nodes fail in your deployment
2. **Determine latency requirements**: What discovery latency is acceptable?
3. **Select mechanism**:
   - Stable network (<0.1% churn): Kademlia or hybrid
   - Moderate churn (1-5%): Hybrid approach
   - High churn (>5%): Gossip-based with Vicinity
4. **Implement pilot**: Use libp2p (structured) or Serf (gossip) for production deployment
5. **Monitor metrics**: Track discovery success rate and latency in production
6. **Iterate**: Adjust parameters (gossip frequency, view size, timeout) based on observations

## Related Work & Context

### Distributed Systems Foundations

- **Kademlia** (Maymounkov & Mazières, 2002): Structured peer-to-peer overlays, used in BitTorrent/Ethereum
- **Chord** (Stoica et al., 2003): Simpler DHT design, proven theoretical analysis
- **Pastry** (Rowstron & Druschel, 2001): Hybrid structured overlay with network locality
- **Gossip Algorithms** (Demers et al., 1987): Foundational epidemic protocols
- **Cyclon** (Voulgaris et al., 2005): Gossip-based overlay optimized for dynamic networks

### Agent System Architecture

- **FIPA Standards** (Foundation for Intelligent Physical Agents): Formal agent communication specifications (predates modern LLM agents)
- **BDI Agent Model** (Rao & Georgeff): Belief-Desire-Intention architecture, influenced agent design
- **Multi-Agent Reinforcement Learning**: Studies agent coordination but typically in centralized settings

### Recent Related Work (2024-2026)

- **A Technical Taxonomy of LLM Agent Communication Protocols** (this session): Complements discovery research by classifying communication paradigms
- **ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration** (2026): Demonstrates need for scalable agent coordination
- **Self-Organizing Multi-Agent Systems for Continuous Software Development** (2026): Applies self-organization to decentralized agent systems

### Possible Future Research Directions

1. **Byzantine-Tolerant Agent Discovery**: Agents may lie about capabilities or availability; develop discovery mechanisms robust to up to f < n/3 malicious agents.

2. **Privacy-Preserving Capability Advertising**: Agents reveal capabilities without leaking identity or sensitive information; use differential privacy or cryptographic commitments.

3. **Dynamic Capability Routing**: Instead of just "find agent X", systems that route based on required computation: "find any agent capable of SQL + vector search near me".

4. **Adaptive Mechanism Selection**: Agents or networks dynamically switch between gossip/structured discovery based on observed churn and performance.

5. **Discovery + Incentive Alignment**: Mechanism design ensuring agents are incentivized to report accurate availability and capability information.

6. **Integration with LLM Reasoning**: Agents use discovery information to actively plan which peers to connect with for specific tasks (not just reactively follow discovery results).

## Summary

"Usable Agent Discovery for Decentralized AI Systems" provides practical, empirically-grounded guidance for building large-scale multi-agent systems without centralized coordination. By systematically comparing structured overlays (Kademlia), gossip-based mechanisms (Cyclon + Vicinity), and hybrid approaches across realistic churn scenarios, the paper demonstrates that decentralized discovery is viable and often preferable for resilience. The findings establish a foundation for the next generation of distributed AI systems that can scale across organizational and geographical boundaries without single points of failure, with significant implications for sovereign AI, edge computing, and peer-to-peer agent networks.
