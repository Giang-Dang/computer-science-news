# Metis: Memory Foundation Model

**ArXiv ID:** 2607.26760  
**Authors:** Multiple institutions including MemTensor (Shanghai) Technology Co., Ltd., Renmin University of China, National University of Singapore, Shanghai Jiao Tong University, and Tongji University  
**Submitted:** July 29, 2026

## Executive Summary

Metis introduces the first prototype of a **memory foundation model**, equipping foundation models with **native memory capabilities** that operate autonomously within the model backbone. Rather than relying on external memory modules, Metis implements persistent, dynamically evolving memory states through optimized attention mechanisms and specialized memory procedures. This represents a paradigm shift in how foundation models internalize and utilize information, moving beyond stateless token-to-token processing toward agents with intrinsic memory capacity—a critical capability for building more capable and efficient autonomous systems.

## Problem Statement

Current foundation models face fundamental limitations regarding memory:

1. **Stateless Processing:** Standard transformers process each forward pass independently, with no persistent memory of previous interactions or learned information

2. **External Memory Overhead:** Current agent systems rely on external memory modules (vector databases, caching systems), introducing:
   - Increased latency from external I/O
   - Memory consistency challenges
   - Complexity in integration and management
   - Architectural inflexibility

3. **Limited Long-Context Capability:** While attention is O(n²) complexity, practical context windows remain limited, constraining ability to leverage long-term patterns

4. **Inefficient Information Reuse:** Each forward pass must recompute understanding; learned patterns cannot be stored efficiently in model weights

5. **Agent Scalability:** Multi-turn interactions require managing growing context windows, limiting practical agent deployment

6. **Knowledge Update:** Current models cannot efficiently internalize new information during deployment without retraining

Previous approaches attempted to address these through:
- Recurrent mechanisms (RNNs) — limited to short-term dependencies
- Caching strategies — external to model backbone
- Fine-tuning procedures — expensive and batch-based
- Prompt engineering — inefficient and limited

Metis directly internalizes these capabilities into the foundation model architecture itself.

## Core Concepts & Theory

### Native Memory Definition

Native memory is formalized from two perspectives:

**1. Persistent Memory State:**
```
A dynamically evolving memory representation:
M_t = compress(M_{t-1}, x_t)

Where:
- M_t: Memory state at time t
- x_t: Current input
- compress(): Learned compression function
```

The memory state persists across forward passes, accumulating information from previous interactions.

**2. Native Memory Procedures:**

Autonomous mechanisms within the model that:
- **Store:** Automatically extract and store relevant information
- **Retrieve:** Query and retrieve stored information
- **Update:** Maintain memory consistency and freshness
- **Forget:** Selectively prune irrelevant information

### Memory Architecture Overview

```
                Input x_t
                    │
                    ▼
        ┌─────────────────────┐
        │   Token Embedding   │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Hyper Memory Block  │ ← Long-term pattern storage
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Local Memory Block  │ ← Short-term interaction context
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   Memory Attention   │ ← Query memory state
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   Standard Layers    │
        └──────────┬──────────┘
                   │
                   ▼
        Output + Updated Memory
```

### Fast Weight Programming (FWP) Inspiration

Metis builds on Fast Weight Programming concepts:

**Core Idea:** Parameters that change at the speed of learning (fast weights) can express computation that standard parameters cannot.

**Metis Application:**
- Combines slow weights (frozen model parameters) with fast weights (memory states)
- Memory states transform through learning rules, not backpropagation
- Gradient-free update enables online learning

### Memory Components

**1. Hyper Memory Block:**
- Stores long-term patterns and learned abstractions
- Updated through specialized optimization objectives
- Remains relatively stable, changes gradually
- Capacity: [Exact figures unavailable — see full paper]

**2. Local Memory Block:**
- Maintains short-term interaction context
- Updated more frequently, responds to immediate input
- Provides current session context
- Capacity: [Exact figures unavailable — see full paper]

**3. Memory Attention Mechanism:**
- Queries both memory blocks: `Query(x_t) → [Hyper, Local]`
- Weighted retrieval: `Retrieved = α·Hyper + (1-α)·Local`
- Integrates retrieved information into standard forward pass
- Dynamically balances long-term and short-term memory

### Memory Update Mechanisms

**Training Phase:**

Multiple specialized optimization objectives:

```
L_total = L_reconstruction + L_operation + L_regularization

Where:
- L_reconstruction: Ensures memory can reconstruct past information
- L_operation: Trains memory manipulation procedures (store/retrieve/update)
- L_regularization: Maintains memory robustness and prevents degeneration
```

**Inference Phase (Gradient-Free):**

```
For each forward pass:
1. Query memory: r_t = MemoryAttention(x_t, Memory)
2. Update memory: Memory ← UpdateRule(Memory, x_t)
   (No backpropagation needed)
3. Use retrieved info: output = Decoder(x_t, r_t)
4. Memory weights frozen, only state updates
```

### Optimization Objectives Explained

**1. Memory Reconstruction Loss:**

Ensures memory efficiently compresses past information:

```
L_recon = ||Memory_reconstructed - Information_from_history||²
```

**2. Memory Operation Loss:**

Trains the model to effectively use memory procedures:

```
L_operation = combined_loss_for(
    store_operation,   # Can new info be stored?
    retrieve_operation, # Can old info be retrieved?
    update_operation    # Can memory be effectively updated?
)
```

**3. Regularization Loss:**

Maintains memory stability and prevents collapse:

```
L_reg = ||Memory||²  (L2 regularization)
      + entropy_penalty(memory_distribution)
      + stability_constraint(memory_change_rate)
```

## Main Ideas & Contributions

### 1. **First Native Memory Foundation Model**

Metis is the first foundation model to internalize memory capabilities:
- **Not an External Add-on:** Memory is integral to backbone computation
- **Learned Procedures:** Memory operations (store, retrieve, update) are learned during pre-training
- **Efficient Update:** Gradient-free updates enable fast online memory adjustment
- **Scalable Design:** Memory can scale with model size

This contrasts with:
- Vector databases (external, high latency)
- Cache-based approaches (no learning, limited adaptation)
- Fine-tuning (expensive, batch-based)

### 2. **Gradient-Free Memory Update**

Online learning without backpropagation:

**Key Innovation:**
- Memory state transforms through learned rules that don't require gradient computation
- Only forward pass needed for memory update
- Reduces computational overhead significantly
- Enables truly online learning during deployment

**Advantages:**
- **Efficiency:** Single forward pass updates both output and memory
- **Scalability:** No additional backward pass overhead
- **Flexibility:** Can be applied at any inference step

### 3. **Unified Long-term and Short-term Memory**

Hyper and Local memory blocks work together:

**Hyper Memory (Long-term):**
- Captures patterns that persist across many interactions
- Learned through pre-training objectives
- Relatively stable across sessions

**Local Memory (Short-term):**
- Captures recent conversation/session context
- Quickly updated based on current input
- Session-specific, reset appropriately

**Integration:** Memory attention mechanism dynamically weights both, enabling flexible use of temporal information.

### 4. **Comprehensive Memory-Specific Training**

Three complementary training objectives ensure:
- **Capacity:** Memory can store sufficient information
- **Operability:** Memory procedures function correctly
- **Robustness:** Memory doesn't degrade under various conditions

This multi-objective approach ensures memory is not just capacity but also operationally sound.

## Methodology & Implementation

### Large-Scale Memory Training

**Training Data Construction:**
- Memory-specific datasets designed to emphasize memory operations
- Diverse scenarios: knowledge retention, context recall, multi-turn understanding
- [Exact composition unavailable — see full paper]

**Training Procedure:**

```
For each batch:
1. Forward pass through standard transformer
2. Compute memory update based on input
3. Evaluate all three loss components
4. Backpropagate through model weights (not memory states)
5. Memory state transforms occur independently
```

**Optimization:**
- Large-scale training: [Exact scale unavailable — see full paper]
- Multi-objective optimization with loss weighting
- Convergence criteria for memory stability
- Computational requirements: [Figures unavailable — see full paper]

### Experimental Setup

**Evaluation Dimensions:**

1. **Memory Capacity:** How much information can be stored and retrieved?
2. **Memory Operations:** Effectiveness of store, retrieve, update procedures
3. **Online Learning:** Speed and accuracy of learning new information
4. **Multi-turn Interactions:** Handling extended conversations
5. **Real-world Tasks:** Practical agent applications
6. **Robustness:** Performance under distribution shift and edge cases

**Baseline Comparisons:**
- Standard transformers (no native memory)
- RNNs (recurrent memory baseline)
- Transformer + external vector DB
- Other memory-augmented approaches

**Domains Tested:**
- Conversational AI (multi-turn dialogue)
- Question answering with context accumulation
- Knowledge-based reasoning
- Long-horizon task execution
- Interactive learning scenarios

### Results

**Memory Functionality:**

Comprehensive experiments demonstrate that Metis exhibits native memory capabilities:
- **Stores** information through learned procedures
- **Retrieves** past information effectively
- **Updates** memory with new experiences
- **Forgets** selectively when appropriate

**Quantitative Results:**

[Exact figures unavailable — see full paper] for:
- Memory capacity (bits/tokens)
- Operation success rates (store/retrieve/update)
- Multi-turn conversation accuracy
- Online learning speed
- Computational overhead
- Comparison with baseline approaches

**Qualitative Analysis:**

- Detailed investigation of when/why memory succeeds or fails
- Analysis of learned memory procedures
- Behavior under different task types
- Edge cases and limitations

## Practical Applications & Use Cases

### 1. **Conversational AI Agents**

- **Multi-turn Memory:** Remember context across extended conversations
- **Personalization:** Internalize user preferences and history
- **Consistency:** Maintain coherent behavior across sessions
- **Example:** Customer support agents that recall previous interactions without explicit history

### 2. **Autonomous Agents**

- **Task State:** Track ongoing task progress and intermediate results
- **Learning:** Internalize feedback from environment interactions
- **Adaptation:** Online adaptation to new environments
- **Example:** Robotic agents that learn from experience without retraining

### 3. **Knowledge Management Systems**

- **Dynamic Knowledge:** Update internal knowledge with new information
- **Long-term Retention:** Maintain knowledge across deployments
- **Selective Recall:** Retrieve relevant information on demand
- **Example:** Researcher assistant that accumulates knowledge over projects

### 4. **Interactive Learning**

- **Few-shot Learning:** Learn new tasks from small number of examples
- **Domain Adaptation:** Adapt to new domains through interaction
- **User Guidance:** Learn from user feedback without retraining
- **Example:** Educational AI that adapts to individual student needs

### 5. **Real-time Decision Making**

- **State Tracking:** Maintain understanding of current system state
- **Online Optimization:** Learn optimal policies during deployment
- **Emergency Response:** Quickly adapt to critical situations
- **Example:** Financial trading systems that adapt to market conditions

### Implementation Challenges

- **Memory Initialization:** Proper setup of memory states for new deployments
- **Memory Drift:** Preventing degradation of memory over long deployments
- **State Management:** Efficient serialization/deserialization of memory states
- **Integration:** Connecting with external systems that expect stateless APIs
- **Debugging:** Interpreting and troubleshooting memory behavior
- **Scaling:** Memory overhead for very large models

## Insights & Implications

### Theoretical Insights

1. **Foundation Models Need Memory:** Stateless processing fundamentally limits agent capabilities; internalized memory is essential for true autonomy

2. **Gradient-Free Updates:** Learning doesn't require backpropagation; learned rules can transform states efficiently

3. **Dual Memory Systems:** Long-term and short-term memory serve complementary roles; both are necessary for comprehensive memory

4. **Learned Procedures:** Memory operations (store/retrieve) can be learned through training objectives rather than hand-designed

### Field Impact

1. **Paradigm Shift in Agent Architecture:** Moves away from external memory systems toward integrated native memory

2. **Closer to Biological Inspiration:** Models memory more similarly to biological neural systems

3. **State-of-the-Art in Foundation Models:** First demonstration of native memory in foundation models

4. **Path to Autonomous AI:** Internalized memory is a necessary component of truly autonomous systems

### Limitations and Open Questions

1. **Memory Scaling:** How does memory capacity scale with model size? Are there fundamental limits?

2. **Memory Interference:** Do old and new memories interfere with each other? How to prevent catastrophic forgetting?

3. **Transfer Learning:** Can memory learned in one domain transfer to another?

4. **Interpretability:** How interpretable are the learned memory procedures? Can we understand what's being stored?

5. **Comparison with External Systems:** Under what conditions is native memory better than external vector databases?

6. **Extreme Scale:** Performance at very large model scales (10T+ parameters) is unexplored

7. **Multimodal Memory:** Extension to vision and multimodal domains needs investigation

## Code & Resources

**Official Repository:**
- GitHub: https://github.com/MemTensor/Metis

**Pre-trained Models:**
- HuggingFace Collections: https://huggingface.co/collections/IAAR-Shanghai/metis

**Code Availability:**
- Implementation of Metis blocks
- Training code for memory-specific objectives
- Evaluation benchmarks and metrics

**Dependencies:**
- PyTorch or compatible framework
- Large-scale training infrastructure
- Standard transformer libraries

**Quick-Start Guide:**

```python
# Basic usage
from metis import MetisModel

# Initialize model with memory
model = MetisModel.from_pretrained("metis-base")
memory_state = model.init_memory()

# Multi-turn interaction
for turn in conversation:
    output, memory_state = model(
        input_ids=turn,
        memory_state=memory_state
    )
    print(output)
```

## Related Work & Context

### Prior Memory-Augmented Approaches

**Neural Turing Machines (NTMs):** Early work on learnable external memory with attention mechanisms. Metis builds on these ideas but internalizes memory into model backbone.

**Transformer-XL:** Extends context through segment-level recurrence. Metis provides more structured memory mechanisms.

**Retrieval-Augmented Generation (RAG):** Uses external knowledge retrieval. Metis combines external-like capabilities with internal efficiency.

**RNNs and LSTMs:** Classical recurrent architectures with internal states. Metis combines RNN-like memory with transformer efficiency.

### Foundational Concepts

**Fast Weight Programming (FWP):** Theoretical foundation for learning memory updates that don't require backpropagation

**Episodic Memory in Neuroscience:** Biological inspiration for dual long-term/short-term memory systems

**Information Theory:** Theoretical framework for understanding memory compression and capacity

### Future Research Directions

1. **Memory Compression:** More efficient memory representations to reduce overhead

2. **Multi-Modal Memory:** Extending to vision, audio, and multimodal information

3. **Distributed Memory:** Memory systems for multi-agent collaborative scenarios

4. **Memory Interpretability:** Understanding what information is stored in memory

5. **Continual Learning:** Leveraging native memory for lifelong learning without catastrophic forgetting

6. **Hybrid Systems:** Combining native memory with external knowledge bases for maximum capability

7. **Neuro-symbolic Integration:** Combining learned memory with symbolic knowledge representations

---

**Keywords:** Memory Foundation Models, Native Memory, Autonomous Agents, Online Learning, Long-context Processing, Foundation Models, Gradient-free Learning
