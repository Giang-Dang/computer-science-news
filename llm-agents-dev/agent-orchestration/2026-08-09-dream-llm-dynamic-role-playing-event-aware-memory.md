# DREAM: LLM-based Dynamic Role-playing via Event-Aware Memory Graph

## Executive Summary

DREAM is a structured memory framework for role-playing agents that transforms unstructured character narratives into Event-aware Memory Graphs (EMGs). Published at KDD 2026, the paper demonstrates that capturing character experiences as temporally ordered and causally linked event graphs enables LLMs to generate contextually accurate, emotionally resonant interactions while maintaining long-term narrative and personality coherence. This approach significantly advances conversational AI by grounding character behavior in temporal context and causal relationships.

## Problem Statement

Existing role-playing agents face critical limitations in maintaining character authenticity across long narratives:

- **Static character representations**: Current systems rely on static character descriptions and unstructured memory, failing to capture dynamic personality evolution
- **Lack of temporal reasoning**: Agents cannot reason about how past events shape current behavior and emotional states
- **Limited causal understanding**: Missing connections between events and behavioral changes leads to inconsistent character portrayals
- **Narrative coherence breakdown**: Long-term character consistency deteriorates without structured representations of character history

The paper addresses these gaps by recognizing that accurate role-playing requires not just stylistic imitation but temporally consistent and causally grounded behavioral reasoning inspired by cognitive psychology.

## Core Concepts & Theory

### Foundational Framework: ABC Model

DREAM builds on the Activating Event-Belief-Consequence (ABC) cognitive model from psychology:
- **Activating Event (A)**: A situation or event that occurs
- **Belief (B)**: Internal interpretation and emotional reaction
- **Consequence (C)**: Resulting behavioral response

This framework ensures character actions are grounded in internal states and causal relationships, mimicking human psychological processes.

### Event-Aware Memory Graph (EMG)

The EMG is a directed acyclic graph representing character experiences:

```
EMG Structure:
┌─────────────────────────────────────────────────┐
│ Event₁ (Temporal: t₁) ─→ Event₂ (Temporal: t₂) │
│    ↓ (causal link)            ↓ (causal link)   │
│ Consequence₁              Consequence₂           │
│    ↓ (belief impact)          ↓ (belief impact) │
│ Character State₁          Character State₂       │
└─────────────────────────────────────────────────┘
```

Key properties:
- **Temporal ordering**: Events are chronologically organized
- **Causal links**: Edges represent how events influence subsequent character beliefs and actions
- **Dual-granularity profiles**: Captures both stable personality traits and event-driven behavioral changes
- **State tracking**: Maintains character emotional and psychological states across the narrative

### Memory Graph Construction

The transformation process:
1. **Extract events** from unstructured literary text using LLM-guided parsing
2. **Identify causal links** between events (what caused what)
3. **Map to ABC model** - connect events to beliefs and behavioral consequences
4. **Build temporal structure** - order events chronologically with temporal annotations
5. **Construct profiles** - aggregate events to build dynamic character representations

## Main Ideas & Contributions

### Primary Innovation: Event-Aware Memory Graph

1. **Structured character memory**: Novel representation that bridges cognitive psychology and NLP
   - Transforms narrative into formal event graphs
   - Enables reasoning about cause-and-effect in character development
   - Supports long-horizon behavioral consistency

2. **Dual-granularity character profiles**:
   - **Stable traits** (e.g., "compassionate," "ambitious"): extracted from aggregate patterns
   - **Event-driven states** (e.g., "angry after betrayal," "hopeful after success"): extracted from specific events
   - Dynamic update: profiles evolve based on experienced events

3. **Temporal filtering mechanism**:
   - Applies temporal relevance weighting to memory retrieval
   - Recent events have higher influence on current behavior
   - Older, less relevant events fade in influence while maintaining narrative consistency

### Technical Contributions

- **Event extraction pipeline** using LLMs with minimal manual annotation
- **Causal reasoning framework** for modeling event dependencies
- **Memory retrieval strategy** that balances temporal recency with causal relevance
- **Profile generation algorithm** that automatically constructs character descriptors from EMGs

## Methodology & Implementation

### Experimental Setup

**Datasets**:
- Literary narratives from classic and contemporary fiction
- Multi-character scenarios with complex relationships and evolving dynamics
- Long-form interactions (100+ turns) to test coherence over extended conversations

**Evaluation Metrics**:
- **Behavioral consistency**: Human evaluation of character trait consistency across turns
- **Emotional authenticity**: Assessment of whether emotional responses match historical context
- **Narrative coherence**: Evaluation of logical flow and causal consistency
- **Long-term consistency**: Measurement of trait preservation over extended interactions

**Baseline comparisons**:
- Static prompt-based character description methods
- Unstructured memory systems (traditional retrieval-augmented generation)
- Random event sampling approaches

### Implementation Details

**Core Components**:
1. **Event extraction module**: Parses narrative text to identify key events
2. **Graph construction**: Builds temporal and causal relationships
3. **Memory encoder**: Encodes EMG into dense representations for LLM conditioning
4. **Retrieval module**: Selects relevant events using temporal and causal filtering
5. **Generation module**: Conditions LLM on retrieved memory for coherent responses

**Integration with LLMs**:
- EMG information provided as structured context before generation
- Temporal filtering ensures recency without losing important causal information
- Character profile embeddings guide generation toward consistent behaviors

## Practical Applications & Use Cases

### Entertainment & Gaming

- **Interactive fiction**: Dynamic characters that evolve realistically based on player choices
- **RPG systems**: Non-player characters (NPCs) with consistent, believable personality arcs
- **Narrative games**: Story-driven experiences where character consistency enhances immersion

### Conversational AI

- **Advanced chatbots**: Personalized assistants with consistent personality across sessions
- **Therapy and coaching bots**: Systems that remember and respond to personal growth narratives
- **Customer service agents**: Representatives with consistent brand persona and memory of customer history

### Content Creation

- **Screenwriting assistance**: Tools that help maintain character consistency across scripts
- **Novel writing**: AI-assisted character development and dialogue generation
- **Podcast/audiobook production**: Consistent voice and personality for recurring characters

### Social Applications

- **Virtual companions**: AI characters with evolving relationships and shared history
- **Educational simulations**: Historical or fictional characters with authentic behavioral patterns
- **Mental health support**: Empathetic AI that remembers and responds to user narratives

## Insights & Implications

### Broader Field Impact

1. **Cognitive-grounded NLP**: Demonstrates value of incorporating psychological models into NLP systems
   - Bridges gap between human cognition and machine learning
   - Opens new research directions in psychologically-informed AI

2. **Structured knowledge for LLMs**: Shows that structured representations significantly improve reasoning
   - EMGs provide explicit causal chains that LLMs can reason over
   - Suggests broader applicability to other structured memory problems

3. **Long-context coherence**: Addresses critical challenge in long-horizon reasoning
   - Provides mechanism for maintaining consistency over hundreds of interactions
   - Relevant to general problems of long-context language understanding

4. **Character representation learning**: Advances in how AI systems model and reason about entities
   - Applicable beyond character modeling to any entity with evolving state
   - Potential applications in knowledge graphs and semantic representation

### Limitations & Open Questions

- **Scalability**: Construction of EMGs requires parsing and understanding narrative structure at scale
- **Event granularity**: Optimal level of event specification remains an open question
- **Cross-narrative transfer**: Whether EMGs can transfer between different character portrayals
- **Real-world application**: Performance on completely unstructured, real-world conversational data
- **Computational overhead**: Trade-offs between memory complexity and retrieval efficiency

### Future Research Directions

1. **Automatic event extraction**: Improve robustness of unsupervised event identification
2. **Multi-agent scenarios**: Extend to systems with multiple interacting characters
3. **Real-time learning**: Enable EMGs to evolve during conversations, not just from pre-existing narratives
4. **Cross-modal integration**: Incorporate visual and audio information into event representations
5. **Transfer learning**: Pre-train EMG construction on diverse narrative corpora

## Code & Resources

**Repository Status**: 
- Authors: Zhihao Xiao, Mengting Li, Xintao Wang, and collaborators
- Published at: KDD 2026 (ACM SIGKDD Conference, Jeju Island, August 9-13, 2026)

**Available Resources**:
- arXiv preprint: [https://arxiv.org/abs/2608.05170](https://arxiv.org/abs/2608.05170)
- HTML version: [https://arxiv.org/html/2608.05170](https://arxiv.org/html/2608.05170)

**Dependencies**:
- PyTorch or similar deep learning framework
- Large language model API or local LLM
- Graph processing libraries (NetworkX or similar)
- Text processing libraries (spaCy, NLTK)

**Quick-Start Implementation**:
1. Parse narrative text to extract events (manual annotation or LLM-guided)
2. Identify causal relationships using LLM reasoning or structured annotation
3. Build temporal graph structure with event ordering
4. Generate character profiles from aggregate event patterns
5. Integrate EMG into LLM prompt context for generation

## Related Work & Context

### Prior Work Foundations

- **Cognitive psychology**: ABC model of behavior (Albert Ellis, 1962) - foundational framework
- **Memory systems in NLP**: Work on memory-augmented transformers and retrieval-augmented generation
- **Character modeling**: Prior work on static character cards and persona-based prompting
- **Event representation**: Research on event extraction and temporal reasoning in NLP

### Recent Related Papers

- [PersonaArena: Dynamic Simulation for Evaluating and Enhancing Persona-Level Role-Playing in Large Language Models](https://arxiv.org/pdf/2605.17044) - Evaluating persona consistency in LLMs
- [From Role-Play to Drama-Interaction: An LLM Solution](https://arxiv.org/html/2405.14231v1) - Interactive drama systems with LLMs
- [Memory-Driven Role-Playing: Evaluation and Enhancement of Persona Knowledge Utilization in LLMs](https://arxiv.org/abs/2603.19313) - Memory mechanisms for persona preservation

### Possible Future Research Directions

1. **Integration with broader knowledge graphs**: Connect character EMGs to world-state representations
2. **Multi-agent interaction graphs**: Model how characters influence each other's event experiences
3. **Causal abstraction**: Learn hierarchical abstractions of events for more efficient reasoning
4. **Cross-narrative consistency**: Enable characters to maintain consistency across different story contexts
5. **Uncertainty handling**: Explicitly model uncertainty in event interpretation and causal relationships

**Paper ID:** arXiv:2608.05170  
**Submission Date:** May 27, 2026  
**Publication:** KDD 2026 (August 9-13, 2026)  
**Conference:** 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining
