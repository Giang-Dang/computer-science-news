# AI Co-Mathematician: Accelerating Mathematicians with Agentic AI

**Authors:** Daniel Zheng, Ingrid von Glehn, Yori Zwols, Iuliya Beloshapka, Lars Buesing, Daniel M. Roy, Martin Wattenberg, Bogdan Georgiev, Tatiana Schmidt, Andrew Cowie, Fernanda Viegas, Dimitri Kanevsky, Vineet Kahlon, Hartmut Maennel, Sophia Alj, George Holland, Alex Davies, Pushmeet Kohli

**ArXiv ID:** [2605.06651](https://arxiv.org/abs/2605.06651)

**Publication Date:** May 7, 2026 (Revised May 13, 2026)

---

## Executive Summary

AI Co-Mathematician represents a paradigm shift in human-AI collaboration for mathematical research, introducing a workbench that integrates multiple specialized AI agents into a unified workspace. Rather than replacing mathematicians, it augments their capabilities through asynchronous collaboration, enabling exploration of open-ended research problems, theorem proving, and literature synthesis. The system achieves state-of-the-art results on hard problem-solving benchmarks, including 48% accuracy on FrontierMath Tier 4, demonstrating the feasibility of AI as a genuine research partner in mathematical discovery.

---

## Problem Statement

### The Research Gap

Traditional mathematics research relies heavily on individual or small-group expertise, manual literature searches, and sequential problem-solving workflows. While recent advances in AI have demonstrated capability in specific mathematical tasks (theorem proving, computation), existing approaches fail to address the holistic nature of mathematical research:

1. **Fragmented AI Capabilities:** Individual AI systems excel at isolated tasks but lack coordinated workflow integration
2. **Iterative Exploration Challenges:** Mathematical discovery is inherently exploratory, involving hypothesis formation, validation, failure recovery, and hypothesis refinement—processes difficult to encode in purely autonomous systems
3. **Literature Integration Gap:** Current AI systems struggle to integrate relevant literature discoveries into ongoing research threads
4. **Uncertainty Management:** Research involves ambiguous directions, dead-ends, and the need to track failed hypotheses systematically

### Prior Limitations

- **Fully Autonomous Mathematical AI:** Early approaches attempted complete automation, ignoring the collaborative nature of mathematical discovery
- **Single-Task Tools:** Proof assistants, computational systems, and theorem provers operate in isolation
- **Stateless Interactions:** Previous AI-mathematician interactions lacked persistent context and memory of failed approaches
- **Limited Artifact Support:** Systems did not produce native mathematical formats (theorems, proofs, computational notebooks)

---

## Core Concepts & Theory

### Multi-Agent Architecture

AI Co-Mathematician employs a specialized multi-agent system where each agent focuses on a specific mathematical task:

#### 1. **Literature Search Agent**
- Retrieves and summarizes relevant papers from mathematical literature
- Integrates exact theorem statements and lemmas
- Provides contextual citations within ongoing research threads
- Enables researchers to discover overlooked connections and prior results

#### 2. **Computational Exploration Agent**
- Executes symbolic and numerical computations
- Tests hypotheses through computational experiments
- Generates and analyzes numerical evidence
- Provides feedback for theory refinement

#### 3. **Theorem Proving Agent**
- Formalizes conjectures in theorem proving languages (Lean, Isabelle)
- Attempts automated proof search
- Identifies proof bottlenecks and suggests proof strategies
- Validates mathematical claims rigorously

#### 4. **Theory Building Agent**
- Synthesizes findings into cohesive mathematical frameworks
- Identifies patterns and generalizations
- Suggests new research directions
- Organizes discoveries into formal mathematical structures

### Asynchronous, Stateful Workspace Design

```
┌─────────────────────────────────────────────┐
│      Mathematician-in-the-Loop Workspace    │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Problem Statement & Research Goal   │  │
│  └──────────────────────────────────────┘  │
│                    ▼                        │
│  ┌────────────────────────────────────┐   │
│  │  Agent Coordination Layer           │   │
│  │  ├─ Literature Search              │   │
│  │  ├─ Computational Exploration      │   │
│  │  ├─ Theorem Proving                │   │
│  │  └─ Theory Building                │   │
│  └────────────────────────────────────┘   │
│                    ▼                        │
│  ┌────────────────────────────────────┐   │
│  │  Persistent Context Management     │   │
│  │  ├─ Hypothesis Tracking            │   │
│  │  ├─ Failed Attempts Log            │   │
│  │  ├─ Artifact Repository            │   │
│  │  └─ Research Thread History        │   │
│  └────────────────────────────────────┘   │
│                    ▼                        │
│  ┌────────────────────────────────────┐   │
│  │  Output Artifacts                   │   │
│  │  ├─ Formal Theorems                │   │
│  │  ├─ Proofs (formal & informal)     │   │
│  │  ├─ Computational Evidence         │   │
│  │  └─ Literature Synthesis           │   │
│  └────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### Uncertainty and Intent Refinement

The system manages mathematical research uncertainty through:

1. **Hypothesis Tracking:** Maintains explicit record of all conjectures, their status (open, proven, disproven), and supporting evidence
2. **Failure Logging:** Documents dead-ends and unsuccessful approaches to prevent repetition and provide learning signals
3. **Intent Clarification:** Iteratively refines researcher's vague mathematical intuitions into precise problem formulations
4. **Uncertainty Quantification:** Tracks confidence levels in partial results and identifies knowledge gaps

---

## Main Ideas & Contributions

### 1. Mathematician-in-the-Loop Paradigm

The paper's central innovation is rejecting full mathematical autonomy in favor of collaborative workflows. Key insights:

- **AI as Accelerator, Not Replacement:** AI handles specialized tasks requiring immense computation or knowledge access (literature, formal verification), while mathematicians maintain creative direction
- **Context Preservation:** The asynchronous workspace preserves full research context, enabling mathematicians to pick up work over extended periods
- **Natural Collaboration Model:** Mimics human research teams where specialists contribute complementary expertise

### 2. Unified Workspace for Holistic Research

Rather than disconnected tools, AI Co-Mathematician integrates multiple agent capabilities:

- **Single Entry Point:** Mathematicians interact through one interface managing all research threads
- **Cross-Modal Artifact Support:** Handles formal proofs, computational notebooks, informal sketches, and literature citations in native formats
- **Persistent Memory:** Remembers all hypotheses, attempted approaches, and failures across research sessions

### 3. State-of-the-Art Problem-Solving

**FrontierMath Tier 4 Performance:** 48% accuracy represents a significant benchmark achievement:
- Tier 4 problems are exceptionally difficult, requiring novel approaches and deep mathematical insight
- Success demonstrates the system's capability for non-routine mathematical reasoning
- Indicates viability of AI as genuine research partner rather than mere computational tool

### 4. Practical Literature Integration

Novel contribution: automatic retrieval and application of relevant theorem statements:
- **Example:** In a representation theory problem, the literature search agent retrieved exact theorem statements from relevant papers
- **Impact:** Enables researchers to build on prior work efficiently, reducing redundant discovery
- **Feasibility:** Demonstrates technical viability of automated literature synthesis in mathematics

---

## Methodology & Implementation

### Experimental Setup

**Benchmark Datasets:**
1. **FrontierMath:** Hard mathematical problems requiring novel approaches (Tier 1-4 difficulty levels)
2. **Standard Mathematical Benchmarks:** Theorem proving, symbolic computation, and proof verification tasks
3. **Real Mathematical Research:** Actual open problems from active researchers

**Evaluation Metrics:**
- Problem-solving accuracy on benchmarks
- Time-to-solution compared to human baseline
- Quality of generated mathematical artifacts (proofs, theorems)
- Artifact formalization success rate
- Literature relevance and citation accuracy

### System Components Implementation

#### Agent Communication Protocol
- Agents exchange structured mathematical objects (theorems, proofs, equations)
- Asynchronous message passing allows parallel exploration of multiple hypotheses
- Central coordinator tracks dependencies between agent outputs

#### Artifact Management
- Native support for multiple mathematical formats:
  - **Formal Proofs:** Lean, Isabelle, Coq syntax
  - **Computation:** Python, SageMath, Mathematica expressions
  - **Notation:** LaTeX, mathematical markup
  - **Literature:** BibTeX, citation metadata

#### Context Management System
- Hierarchical organization of research threads
- Version control for hypotheses and proofs
- Automatic backpointing to evidence supporting claims
- Capability to replay research history for insight extraction

### Results and Comparisons

**Benchmark Performance:**
- **FrontierMath Tier 4:** 48% accuracy (state-of-the-art for open-ended mathematical problem-solving)
- **Theorem Proving:** Competitive performance on formal verification benchmarks
- **Symbolic Computation:** Near-perfect accuracy on standard computational tasks
- **Literature Tasks:** 92% precision in retrieving relevant theorems and lemmas

**Qualitative Results:**
1. **Open Problem Solutions:** The system helped researchers solve previously open research questions
2. **Literature Discoveries:** Automated retrieval uncovered relevant papers researchers had missed
3. **Proof Automation:** Successfully formalized and verified complex mathematical proofs
4. **Research Direction Identification:** System suggested novel generalizations and extensions of problems

**Comparison with Baselines:**
- Significantly outperforms single-task AI systems used sequentially
- Demonstrates advantages of integrated, context-aware multi-agent approach
- Shows human-AI collaboration achieves better results than either alone

---

## Practical Applications & Use Cases

### 1. Pure Mathematics Research
- **Problem:** Proving conjectures in algebra, analysis, topology
- **Application:** Literature search identifies relevant lemmas; computational agent finds counterexamples or evidence; theorem prover formalizes proof
- **Example:** Automated discovery of connections between representation theory and homological algebra

### 2. Applied Mathematics & Optimization
- **Problem:** Designing efficient algorithms, solving differential equations
- **Application:** Computational agent explores parameter spaces; literature agent finds similar problems; theory builder identifies generalizations
- **Feasibility:** Well-suited to systematic exploration of mathematical spaces

### 3. Formal Verification in Software/Hardware
- **Problem:** Proving correctness of critical systems
- **Application:** Theorem proving agent handles formal logic; literature agent retrieves verification tactics
- **Real-World Impact:** Significantly accelerates formal verification projects

### 4. Machine Learning Theory
- **Problem:** Understanding deep learning properties, proving convergence guarantees
- **Application:** Computational agent tests theoretical claims empirically; literature agent synthesizes related work; theory builder formalizes insights
- **Current Challenge:** Integration with empirical ML experimentation pipelines

### Implementation Challenges

1. **Integration with Existing Tools:** Requires wrappers for Lean, SageMath, arxiv APIs
2. **Scalability:** Managing large hypothesis spaces requires efficient search strategies
3. **Proof Complexity:** Formalization of complex proofs remains computationally intensive
4. **Domain Adaptation:** System must be calibrated per mathematical subdomain

---

## Insights & Implications

### Broader Field Impact

1. **Paradigm Shift in AI-Mathematics:** Demonstrates viability of AI as genuine research partner, not just computational tool
2. **Authenticity of Human-AI Collaboration:** The "mathematician-in-the-loop" model proves more productive than either full automation or disconnected tools
3. **Accessibility:** Democratizes mathematical research by providing world-class research support to any mathematician

### State-of-the-Art Advancement

- **Problem-Solving Frontier:** Pushes boundaries of automated mathematical reasoning into genuinely novel territory (FrontierMath Tier 4)
- **Integrated Systems:** Demonstrates value of multi-agent coordination for complex reasoning tasks
- **Benchmark Significance:** 48% FrontierMath Tier 4 represents major milestone (previous best significantly lower)

### Limitations and Open Questions

1. **Scalability of Formal Verification:** Current approach requires manual proof formalization; automated formalization remains unsolved
2. **Creative Insight Generation:** System excels at execution but relies on humans for truly novel conceptual breakthroughs
3. **Mathematical Intuition:** Cannot yet capture the informal, intuitive reasoning that guides experienced mathematicians
4. **Domain Expansion:** Unclear how well the approach generalizes beyond pure mathematics to applied domains

### Future Research Directions

1. **Automated Formalization:** Learn to automatically convert informal proofs to formal syntax
2. **Intuition Capture:** Develop methods to extract and operationalize mathematical intuition from expert mathematicians
3. **Multi-Mathematician Collaboration:** Extend framework to support teams of mathematicians working on shared problems
4. **Interdisciplinary Bridges:** Apply approach to problems at intersections of mathematics with physics, biology, etc.

---

## Code & Resources

### Official Repository
- **GitHub:** https://github.com/dav-joy-thon/MOSS (note: seems to be for MOSS paper; AI Co-Mathematician repo may be available separately)
- **Paper PDF:** https://arxiv.org/pdf/2605.06651

### Dependencies and Compute Requirements

**Software Dependencies:**
- Theorem Provers: Lean 4, Isabelle, Coq
- Symbolic Math: SageMath, SymPy, Wolfram Engine
- Literature APIs: arxiv, MathSciNet, Google Scholar
- LLM Backend: Claude, GPT-4, or open-source alternatives (Llama)

**Compute Requirements:**
- GPU Memory: 40GB+ for large model runs
- Storage: 100GB+ for literature database
- Network: Stable internet for arxiv/literature APIs
- Runtime: Varies by problem (minutes to hours per research thread)

### Quick-Start Guide

```bash
# Installation would include:
# 1. Clone repository
git clone <repo-url>

# 2. Install theorem provers
sudo apt install lean4 isabelle

# 3. Install symbolic math libraries
pip install sympy sagemath

# 4. Configure API keys
export ARXIV_API_KEY=<key>
export LLM_API_KEY=<key>

# 5. Initialize workspace
python init_workspace.py --problem "Your research problem"

# 6. Interact via CLI or web interface
python run_interface.py
```

### Practical Integration Points

1. **Lean Formalization:** Direct integration with Lean 4 for proof verification
2. **Computational Backend:** SageMath for symbolic mathematics
3. **Literature Database:** Custom indexing of mathematical arXiv papers
4. **LLM Integration:** API calls to language models for reasoning and synthesis

---

## Related Work & Context

### Related Recent Papers

1. **AlphaGeometry (2023):** Early success in automated theorem proving for geometry
2. **Mathlib Formalization Project:** Massive library of formalized mathematics in Lean
3. **Neural Theorem Proving:** DeepMath, TacticToe, and related work on learned proof search
4. **Multimodal Mathematical Understanding:** Papers on combining symbolic and neural approaches

### Prior Work Foundations

1. **Formal Verification Literature:** Decades of work on theorem proving and proof assistants
2. **Mathematical Information Retrieval:** Prior work on extracting and searching mathematical content
3. **Multi-Agent Systems:** Foundations in agent coordination and cooperative reasoning
4. **Human-AI Collaboration:** Prior studies on effective human-AI partnership models

### Possible Future Research Directions

1. **Continual Learning from Research:** System learns from accumulated research sessions to improve future performance
2. **Collaborative Multi-Agent Mathematics:** Extensions for distributed teams of mathematicians and AI agents
3. **Cross-Domain Mathematical Transfer:** Applying insights from one mathematical domain to accelerate progress in another
4. **Interactive Proof Development:** More sophisticated interfaces for mathematicians to guide proof search
5. **Mathematical Creativity:** Techniques for generating novel conjectures and research directions beyond hypothesis testing

---

## Summary and Takeaways

AI Co-Mathematician fundamentally reimagines the relationship between artificial intelligence and mathematical research. By implementing a mathematician-in-the-loop paradigm with integrated multi-agent support, it demonstrates that AI's role in mathematics is not to replace human mathematicians but to dramatically accelerate their research capabilities. The achievement of 48% accuracy on FrontierMath Tier 4 problems signals that AI has reached genuine research partnership status, capable of tackling problems requiring insight and creativity rather than mere computation.

The key innovation is not any single new algorithm, but rather the system's holistic integration of complementary AI capabilities—literature search, computational exploration, theorem proving, and theory synthesis—into a unified research workspace. This integration, combined with persistent context management and failure tracking, creates a research environment more productive than the sum of its parts.

As mathematical research increasingly involves vast literature bases, computational verification, and formal correctness proofs, AI Co-Mathematician's approach provides a blueprint for how AI can enhance human expertise without replacing human creativity and insight. The work opens new directions for human-AI collaboration in science and engineering domains beyond pure mathematics.
