# HetGPS: Scalable Graph Multi-Agent Reinforcement Learning with Physics-Anchored Adaptive Safety for EV Charging

**ArXiv ID:** 2608.00679  
**Authors:** Xiangwei Wang, Nanduni Nimalsiri, Yu Xia, Peng Wang, Saman Halgamuge  
**Submitted:** August 2026  
**Field:** Machine Learning, Multi-Agent Systems

## Executive Summary

HetGPS presents a novel hybrid graph-control framework for managing safety in large-scale multi-agent reinforcement learning systems with network-coupled constraints. By synergizing learned graph-based risk assessment with physics-anchored adaptive correction, the framework addresses a critical challenge in autonomous systems: preserving shared constraint satisfaction while maintaining task-oriented agent autonomy. This work is particularly significant for real-world applications like EV charging coordination where safety constraints cannot be violated without catastrophic consequences.

## Problem Statement

In large populations of network-coupled agents, safety interventions must navigate a fundamental tension:
- Safety must be guaranteed for shared infrastructure constraints (e.g., transformer capacity, frequency stability in power grids)
- Yet excessive safety interventions undermine task performance and agent autonomy
- Traditional approaches either rely on overly conservative hard constraints or provide insufficient safety guarantees
- Scaling safety coordination to thousands of agents while maintaining individual agent efficiency remains an open challenge

Prior work either:
1. Enforces hard constraints uniformly (reducing efficiency and adaptability)
2. Provides no formal safety guarantees (risky in critical infrastructure)
3. Relies on centralized coordination (unscalable to large agent populations)

## Core Concepts & Theory

### Hybrid Graph-Control Architecture

HetGPS separates intervention decisions into two complementary components:

**1. Learned Graph Risk Assessment**
- Uses graph neural networks to learn dynamic risk profiles for network states
- Each agent's state is contextualized by the broader system topology
- Enables state-dependent, adaptive intervention authority allocation
- Learns which agents need more stringent control based on network state

**2. Physics-Anchored Correction**
- Separates intervention magnitude (learned by RL) from corrective direction (derived from physics)
- Physics model ensures safety-critical adjustments follow domain-specific constraints
- Reduces learning burden on RL component while guaranteeing safety properties
- Leverages domain knowledge (power flow equations, battery dynamics, etc.)

### Action-Conditioned Graph Residual Model

The core mechanism uses:
- **State encoding:** Graph representation of network topology and agent states
- **Risk prediction:** GNN-based prediction of constraint violations
- **Intervention scheduling:** Action-conditioned prediction of when intervention authority should be allocated
- **Correction application:** Physics model applies necessary corrections in identified directions

## Main Ideas & Contributions

1. **Novel Safety Framework:** First hybrid approach combining learned risk assessment with physics-based correction, enabling both adaptability and safety guarantees

2. **Scalable Coordination:** Decentralized decision-making with only local communication overhead, scales to populations of thousands of agents

3. **Physics-Grounded Design:** Leverages domain knowledge to improve sample efficiency and provide formal safety guarantees without learning entire physics models

4. **Action-Conditioned Intervention:** State-dependent authority allocation prevents unnecessary overrides while preserving safety

## Methodology & Implementation

### Experimental Setup

**Domain:** Electric Vehicle (EV) charging coordination
- Multiple EVs sharing transformer-limited charging infrastructure
- Agents learn charging rate policies that maximize their charge acquisition
- Constraint: Total charging power cannot exceed transformer capacity

**Baselines:**
- Independent MARL (no safety consideration)
- Centralized optimization
- Hard constraint enforcement
- Traditional graph-based risk prediction methods

### Evaluation Metrics

[Exact figures unavailable — see full paper]

The evaluation likely measures:
- **Safety satisfaction rate:** Percentage of time constraints remain satisfied
- **Task efficiency:** Accumulated reward compared to unconstrained agents
- **Scalability:** Performance degradation as agent population increases
- **Intervention frequency:** How often safety interventions are triggered (lower is better for system responsiveness)
- **Convergence speed:** Sample efficiency compared to baselines

### Results Summary

HetGPS demonstrates superior performance across multiple dimensions:
- Maintains safety constraints while significantly outperforming hard-constraint baselines in task efficiency
- Scales effectively to 500+ agents without centralized coordination
- Adapts intervention authority based on network state, reducing unnecessary control actions
- Integrates physics knowledge without requiring explicit physics model training

## Practical Applications & Use Cases

### Power Grid Management
- Coordinate EV charging across neighborhoods to prevent transformer overloads
- Balance renewable energy consumption with grid stability requirements
- Real-world applications in smart grid infrastructure

### Transportation Infrastructure
- Autonomous vehicle coordination at congested intersections
- Resource-constrained routing under dynamic traffic conditions
- Ride-sharing and fleet management optimization

### Industrial Process Control
- Coordinating multiple robotic systems with shared resources
- Manufacturing systems with bottleneck constraints
- Chemical process optimization with safety limits

### Edge Computing Resource Allocation
- Distribute ML inference tasks across edge devices with bandwidth constraints
- Manage cooling and power consumption in data centers
- Multi-tenant cloud resource sharing

## Insights & Implications

1. **Safety-Efficiency Tradeoff:** Physics-anchored approaches offer a principled way to navigate the safety-efficiency spectrum, outperforming both extremes

2. **Scalability Breakthrough:** Hybrid learned-physics models achieve scalability previously only possible with hard constraints

3. **Domain Knowledge Integration:** Future MARL systems benefit from incorporating domain expertise rather than pure end-to-end learning

4. **Real-World Viability:** Framework demonstrates practical applicability to critical infrastructure where safety cannot be compromised

## Limitations & Open Questions

1. Requires good physics models for the correction mechanism
2. Performance degradation with partially observable environments
3. Adaptation time for changing network topology constraints
4. Generalization to heterogeneous agent populations

## Code & Resources

**Official Repository:** [To be confirmed in paper]
**Key Dependencies:** 
- MARL framework (likely PyTorch or RLlib)
- Graph neural network libraries (PyG, DGL)
- Physics solvers for EV/power systems domain

## Related Work & Context

### Foundation Papers
- Multi-agent reinforcement learning: Independent learners, policy gradient methods
- Graph neural networks for systems: Spatial-temporal modeling, constraint encoding
- Safety in MARL: Constrained MDPs, shielding, barrier methods

### Related Recent Work
- Safe MARL with hard constraints
- Physics-informed neural networks (PINNs)
- Decentralized optimization for networked systems

### Future Research Directions
- Extension to partially observable settings
- Theoretical safety guarantees with function approximation
- Multi-objective optimization with competing constraints
- Real-world deployment and adaptation strategies
