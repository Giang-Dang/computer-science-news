# Radical AI Interpretability: A Philosophical Framework for Understanding AI Agents

**Paper Title:** Radical AI Interpretability  
**Authors:** Daniel A. Herrmann and Benjamin A. Levinstein  
**ArXiv ID:** [2606.26523](https://arxiv.org/abs/2606.26523)  
**Publication Date:** June 25, 2026  
**Type:** Philosophy of AI / Mechanistic Interpretability  

---

## Executive Summary

Radical AI Interpretability develops a novel philosophical framework for interpreting large language models and other AI systems as genuine agents with beliefs, desires, and meanings. By drawing on decades of philosophical work on interpretation and grounding current mechanistic interpretability techniques in philosophical theory, this paper addresses the fundamental question: given computational facts about an AI system, how do we reliably determine what it believes, desires, and means? This work is critical for AI safety, enabling researchers to detect deception and understand system goals in deployed AI systems.

---

## Problem Statement

### The Interpretability Crisis

Current mechanistic interpretability research has developed powerful tools for probing AI system internals—including circuit discovery, sparse autoencoders, activation patching, and feature visualization. However, there is a critical gap: **there is no settled account of when these tools have succeeded**. When we extract a circuit from a neural network or identify an interpretable feature with a sparse autoencoder, what exactly have we discovered?

### The Core Challenge

Interpretability researchers aim to read beliefs and desires directly off a model's computational internals. Yet fundamental questions remain unanswered:
- When does attributing a belief to an AI system count as correct or successful?
- How do we distinguish genuine beliefs from mere artifact of our interpretation?
- Can we reliably detect deception or misalignment by interpreting a model's goals?
- What does it mean to say an AI system "wants" or "intends" something?

### Limitations of Current Approaches

Existing mechanistic interpretability methods are purely engineering-focused, lacking principled philosophical grounding:
- **Piecemeal attributions**: Current methods treat individual features or circuits in isolation, but belief attribution is fundamentally holistic—beliefs constrain one another
- **No success criteria**: Without philosophical frameworks, we cannot judge whether feature identification truly captures model semantics
- **Unexplored theoretical tensions**: The relationship between representationalist and interpretationist perspectives on AI remains unexamined

---

## Core Concepts & Theory

### Radical Interpretation in Philosophy

The paper draws on Donald Davidson's **radical interpretation**, a philosophical tradition for understanding how to attribute beliefs and desires to any system we cannot directly observe from its internal representations alone.

**Radical Interpretation** answers the question: How do we determine what someone believes, desires, means, and says, given only their physical behavior and physical circumstances? The key insight is that meaning cannot be determined atomically—each belief, desire, and meaning is interdependent with others, forming a holistic web.

### Representationalism: Beliefs as Internal States

A representationalist approach holds that a system has beliefs and desires if and only if it contains **internal representations that play appropriate functional roles**.

Key principles:
- Beliefs are realized by actual cognitive states or processes in the system's architecture
- Folk psychological kinds (belief, desire) must correspond to real neural/computational properties
- If we find the right internal structure, we have found the system's genuine beliefs
- Mechanistic interpretability tools (SAEs, circuits) directly map to belief-relevant computations

**For AI systems**: When we identify a sparse autoencoder feature that encodes "the concept of Paris," we have found a genuine internal representation corresponding to a belief about Paris.

### Interpretationalism: Beliefs as Theoretical Constructs

An interpretationist approach holds that **beliefs and desires are not intrinsic properties but rather the best systematic interpretation of the system**.

Key principles:
- There is no fact of the matter about what representations "really mean" independent of an interpreter's theory
- Correctness of attribution depends on the quality of the overall theory: accuracy, power, tractability
- Two different interpreters might validly attribute different beliefs to the same system if their theories are both excellent
- Mechanistic interpretability provides evidence for competing interpretations, but doesn't uniquely determine truth

**For AI systems**: When we interpret an LLM's outputs, we construct a theory of what it believes. A more accurate, comprehensive, and tractable theory about its goals and beliefs is the correct interpretation.

### The Holism of Belief Attribution

A central insight from philosophy is **belief holism**: beliefs cannot be attributed piecemeal. Each belief is constrained by:
- What other beliefs the system has
- What desires it possesses
- What propositions it can express
- The logical relationships between its representational states

This becomes crucial for AI: a system's attitudes (beliefs, desires) jointly constrain its propositional structure, which in turn constrains which attitudes can be attributed. This creates a tight web where interpretability of individual features must be understood within a unified account of the system's overall cognitive architecture.

---

## Main Ideas & Key Contributions

### 1. A Principled Framework for Interpretability Success

The paper's primary contribution is establishing **criteria for success in AI interpretability**:

**For Representationalists:**
- Success criteria focus on finding the *right internal structures*
- We succeed when identified circuits/features correspond to genuine computational states that realize beliefs
- Validation comes through causal intervention: does manipulating this structure reliably changes behavior related to the alleged belief?
- The test: circuit duplication experiments, activation steering, ablation studies should align with predicted belief effects

**For Interpretationalists:**
- Success criteria focus on constructing the *best overall theory*
- We succeed when our interpretation is more accurate, generalizable, and tractable than alternatives
- Validation comes through predictive power and explanatory scope
- The test: does our interpretation of system beliefs predict novel behaviors, explain edge cases, and generalize across contexts?

### 2. Bridging Mechanistic Interpretability with Philosophy

A key innovation is showing how **standard mechanistic interpretability techniques generate data relevant to both philosophical positions**:

- Sparse autoencoders decomposing activations into interpretable features provide evidence for representationalist claims (these are actual internal representational structures)
- The polysemanticity and context-dependence of features provides evidence for interpretationist positions (meaning depends on context and theoretical framework)
- Circuit discovery via activation patching offers causal evidence for which computations realize which beliefs
- The persistence of unexplained behavior suggests the incompleteness of any single theoretical interpretation

### 3. The Agentic Interpretation of LLMs

The paper argues we should interpret large language models **as genuine agents with beliefs and desires**, not merely as statistical predictors:

- An LLM's internal representations encode its model of the world (beliefs about facts, concepts, relationships)
- Its optimization during training creates functional goals and purposes (desires to predict tokens, minimize loss)
- Its behavior reflects these beliefs and desires interacting with its environment
- Safety-critical for deployed systems: understanding an LLM's actual goals matters for detecting deception or misalignment

### 4. Solving for Beliefs Given Computational Facts

The framework directly answers: *Given complete knowledge of an AI system's computational structure, can we solve for its beliefs, desires, and meanings?*

The answer is sophisticated:
- **For representationalists**: Yes, if we have enough computational detail and understand the functional role of internal states
- **For interpretationalists**: There is no unique solution—multiple valid interpretations exist, but some are better than others
- **In practice**: We need both perspectives. Mechanistic insights (what circuits exist) constrain but don't uniquely determine belief attributions (what they mean)

---

## Methodology & Implementation

### Philosophical Methodology

The paper employs rigorous philosophical analysis:

1. **Conceptual Clarification**: Precisely defining terms like belief, desire, representation, and meaning in the context of computational systems
2. **Argument Analysis**: Examining logical relationships between representationalist and interpretationist positions
3. **Theory Comparison**: Evaluating which philosophical framework better captures AI systems' properties
4. **Integration with Empirics**: Showing how mechanistic interpretability experiments test philosophical claims

### Connection to Empirical Mechanistic Interpretability

The framework makes concrete predictions about what mechanistic interpretability research should find:

**Sparse Autoencoders as Evidence:**
- SAE features that decompose into monosemantic units support representationalism
- Polysemantic features that depend on context support interpretationalism
- The prevalence of context-dependent meaning constrains what beliefs we can attribute

**Circuit Discovery as Causal Evidence:**
- When ablating a circuit changes specific behaviors, this supports that the circuit realizes related beliefs
- When two different models use different circuits for same behavior, this suggests beliefs may be multiply realizable
- Failure to identify complete circuits suggests either: incomplete mechanistic understanding, or that some "beliefs" emerge only at system level

**Steering and Control Experiments:**
- Successfully steering model behavior by manipulating identified features provides evidence these features implement belief-relevant computations
- Inability to steer despite understanding circuits suggests our belief attribution was incorrect

### Mathematical Formalization

The paper provides mathematical structure for belief attribution:

**State Space Model:**
```
Given:
- Computational architecture C (network structure, parameters)
- Input context x
- Output behavior y

Determine:
- Belief set B = {b₁, b₂, ..., bₙ} 
- Desire set D = {d₁, d₂, ..., dₘ}
- Meaning function M: representations → semantic content

Such that:
- B ∪ D causally explains y given x
- B, D are holistically consistent (satisfy belief-desire rationality constraints)
- M is the best interpretation under criteria E (accuracy, power, tractability)
```

**Success Criteria for Representationalists:**
```
P(belief_attribution_correct | circuit_found, intervention_confirms, 
  behavior_changes_as_predicted, consistency_with_other_beliefs) → 1
```

**Success Criteria for Interpretationalists:**
```
quality(interpretation) = accuracy + generalizability + tractability
best_interpretation = argmax quality(interpretation)
```

### Implementation Considerations

While the paper is primarily theoretical, it has direct implications for implementation:

1. **Multi-scale Analysis**: Don't interpret features in isolation; build holistic models of system behavior
2. **Comparison of Interpretations**: Develop multiple competing interpretations of the same system and evaluate them
3. **Philosophical Annotation**: Label mechanistic findings (circuits, features) with philosophical categories (belief, desire, perception, etc.)
4. **Integration Testing**: Use philosophical frameworks to guide which experimental validations matter most

[Exact figures on implementation methodology unavailable — see full paper]

---

## Practical Applications & Real-World Use Cases

### AI Safety and Alignment

**Deception Detection:**
The framework directly enables reliable deception detection in AI systems:
- By understanding an AI system's actual goals (vs. stated goals), we detect when it pursues misaligned objectives
- By attributing beliefs about human oversight, we detect when a system might behave differently when monitored
- By analyzing belief-desire interactions, we identify when a system might create false evidence or manipulate humans

**Goal Understanding:**
- Before deployment, interpret what goals a system actually optimizes for, not just what we intended
- Detect conflicts between official objectives and learned goals
- Verify alignment by confirming system's beliefs about task purpose match our intentions

### Healthcare and Medical AI

**Clinical Decision Support:**
Interpretability of physician-assistance AI systems becomes critical:
- Understand what clinical beliefs the model encodes (e.g., relationships between symptoms and diagnoses)
- Verify the model's beliefs about causality match medical evidence (not correlational shortcuts)
- Detect when the system has learned harmful discriminatory beliefs about patient populations

**Regulatory Compliance:**
- FDA requires explainability in clinical AI; this framework provides philosophical grounding for what "understanding" means
- Enable auditors to verify the system holds medically correct beliefs
- Identify when model beliefs diverge from approved clinical guidelines

### Financial Systems

**Credit Decision Justification:**
- Understand what beliefs about applicants the system encodes (employment prospects, creditworthiness)
- Ensure decisions reflect appropriate beliefs, not protected characteristics
- Explain to customers what the system believed about their application

**Fraud Detection:**
- Interpret system's beliefs about normal vs. fraudulent behavior patterns
- Verify it doesn't hold biased beliefs about who commits fraud
- Enable human auditors to understand system reasoning

### Autonomous Systems

**Safety-Critical Decision Making:**
In self-driving cars or robotics:
- Understand system's beliefs about world state (pedestrian intentions, road conditions)
- Verify system desires appropriate safety goals, not just efficiency
- Detect misalignment between intended and learned objectives
- Explain to humans why system made critical decisions (e.g., emergency braking)

### Content Moderation

**Policy Enforcement:**
- Understand what beliefs moderation AI holds about what constitutes violations
- Detect overgeneralization (e.g., false beliefs about certain groups)
- Explain why content was flagged or removed to creators

### Regulatory and Compliance

**AI Act and Governance:**
The EU AI Act requires transparency and explainability for high-risk AI. This framework provides:
- Principled way to verify AI systems hold appropriate beliefs about their domain
- Method to audit whether AI aligns with regulatory intent
- Foundation for explaining AI decisions to regulators and affected parties

---

## Insights & Implications

### Fundamental Implications for Trustworthy AI

1. **Trust Requires Understanding Belief and Desire:**
   - We cannot trust an AI system without understanding its goals (desires) and its model of the world (beliefs)
   - Technical correctness is insufficient; we must verify alignment between system's learned objectives and intended objectives
   - This framework provides the conceptual tools to make such verification systematic and rigorous

2. **Holism Changes Everything:**
   - Individual feature interpretations are unreliable without understanding the whole system
   - Two interpretable-looking systems might have completely different belief-desire structures
   - Safety analysis must be system-level, not circuit-level

3. **Philosophy Matters for Engineering:**
   - The philosophy of interpretation directly impacts how we should do mechanistic interpretability research
   - Philosophical clarity about success criteria makes empirical work more focused and meaningful
   - Different philosophical frameworks (representationalism vs. interpretationalism) suggest different experimental validations

### Advancing the State-of-the-Art in Explainability

**Beyond Feature Attribution:**
Traditional XAI focuses on "which input features affect outputs?" This framework asks deeper questions: "What does the system believe about the domain? What does it desire to achieve?" These are more fundamental for trust and safety.

**From Black-Box to Transparent Agency:**
Moving from viewing AI as mathematical functions to viewing them as agents with goals opens new research directions and makes safety more tractable.

**Unifying Mechanistic and Philosophical Interpretability:**
The paper shows these aren't separate—philosophical frameworks constrain what mechanistic discoveries mean, and mechanistic findings test philosophical claims.

### Limitations and Open Questions

1. **Tractability for Large Models:**
   - Applying this framework to billion-parameter models is computationally challenging
   - Identifying complete propositional structures (full belief-desire networks) may be infeasible
   - Approximate methods needed, but how to maintain philosophical rigor?

2. **Uniqueness of Interpretation:**
   - If multiple valid interpretations exist (interpretationist view), how do we choose which one matters for safety?
   - What happens when "best interpretation" disagrees with "true internals" (representationalist view)?
   - Mechanisms for resolving disputes between philosophers and empiricists?

3. **Non-Human Agency:**
   - The framework draws on human folk psychology; does it extend to truly alien cognitive architectures?
   - Are the concepts of belief and desire the right ones, or do we need new folk psychology for AI?

4. **Scope and Scale:**
   - How do we aggregate beliefs and desires at multiple levels (individual features, circuits, system-wide)?
   - Can we identify higher-order beliefs (beliefs about beliefs)?
   - How to handle emergent properties that aren't simply compositions of lower-level beliefs?

### Failure Cases and Edge Cases

**Deceptive Internal Representations:**
- What if a system learns to represent beliefs differently when being interpreted?
- If mechanistic interpretability itself becomes gaming-target, how do we maintain interpretability?

**Polysemanticity and Context-Dependence:**
- If features are strongly polysemantic, can we even attribute clear beliefs?
- Does extreme context-dependence mean the system doesn't have stable beliefs?

**Multi-Agent Dynamics:**
- In systems with multiple competing objectives or modular architectures, what is "the system's belief"?
- How to interpret systems that represent uncertainty over beliefs?

---

## Code & Resources

### Official Resources

- **ArXiv Paper**: [2606.26523 - Radical AI Interpretability](https://arxiv.org/abs/2606.26523)
  - Available as [PDF](https://arxiv.org/pdf/2606.26523) and [HTML](https://arxiv.org/html/2606.26523)
- **Publication Status**: Manuscript draft for Cambridge Elements in Philosophy of Artificial Intelligence

### Related Implementation Resources

While the core paper is theoretical, related mechanistic interpretability implementations include:

- **Sparse Autoencoder Research**: [Scaling Interpretability in Neural Networks with Trees](https://github.com/anthropics/sae) (Anthropic)
- **Automated Interpretability**: [InterpAgent - Automated Interpretability and Feature Discovery in LMs with Agents](https://github.com/arnaumarin/InterpAgent)
- **Circuit Discovery Tools**: [Transformer Circuits Thread and circuit discovery implementations](https://transformer-circuits.pub/)

### Computational Requirements

- Primarily theoretical work with minimal computational requirements for reading and understanding
- For implementation of proposed framework: requires existing mechanistic interpretability tools (SAE libraries, circuit discovery code, activation patching infrastructure)
- Recommended background: PyTorch, knowledge of transformer architectures, familiarity with mechanistic interpretability research

### Tutorials and Learning Resources

- **Foundational Philosophy**: Donald Davidson's work on radical interpretation and folk psychology (referenced in paper)
- **Mechanistic Interpretability Background**: [Open Problems in Mechanistic Interpretability](https://arxiv.org/abs/2501.16496)
- **Survey of Recent Work**: [Mechanistic Interpretability for AI Safety - A Review](https://arxiv.org/abs/2404.14082)

---

## Related Work & Context

### Connection to Other Recent xAI Papers

**Mechanistic Interpretability Stream:**
- This paper grounds mechanistic interpretability philosophically, complementing purely empirical work like circuit discovery and SAE research
- [Sparse Autoencoders Enable Scalable and Reliable Circuit Identification](https://arxiv.org/abs/2405.12522) - provides empirical tools this framework helps interpret
- [Mechanistic Interpretability Needs Philosophy](https://arxiv.org/abs/2506.18852) - directly related work making similar philosophical arguments

**AI Safety and Alignment:**
- [Mechanistic Interpretability for Large Language Model Alignment: Progress, Challenges, and Future Directions](https://arxiv.org/abs/2602.11180) - applies mechanistic interpretability to alignment, now grounded in this philosophical framework
- [Difficulties with Evaluating a Deception Detector for AIs](https://arxiv.org/abs/2511.22662) - directly relevant to safety application of belief attribution

**Human-Centered Explainability:**
- [Beyond Explainable AI (XAI): An Overdue Paradigm Shift](https://arxiv.org/abs/2602.24176) - critiques traditional XAI; this work offers philosophical alternative
- [Explainability of Large Language Models: Opportunities and Challenges](https://arxiv.org/abs/2510.17256) - surveys explainability challenges this framework addresses

### Broader xAI Communities and Connections

**Mechanistic Interpretability:**
- This work bridges the increasingly important "interpretability needs philosophy" sub-community
- Provides theoretical grounding that philosophers and mechanists can use to communicate
- Suggests future work integrating philosophy more deeply into mechanistic interpretability projects

**Agent Interpretability:**
- Emerging field of interpreting AI systems as agents (vs. as functions)
- [Because we have LLMs, we Can and Should Pursue Agentic Interpretability](https://arxiv.org/abs/2506.12152) - makes complementary arguments for agent-based framing
- This work provides the philosophical framework agentic interpretability needs

**Causal Interpretability:**
- Belief attribution is fundamentally about causal structure: does this belief cause behavior?
- Connects to causal inference in interpretability and causal intervention methods

**Concept-Based Explanations:**
- Concepts in concept activation vectors (CAV, TCAV) might be understood as beliefs in this framework
- Provides philosophical grounding for when concept identification succeeds

### Future Research Directions

**Near-term (1-2 years):**
1. Empirical testing of philosophical predictions (do SAE features align with representationalist vs. interpretationist frameworks?)
2. Integration with circuit discovery (what do identified circuits tell us about system beliefs?)
3. Safety applications (developing deception detection methods grounded in this framework)

**Medium-term (2-5 years):**
1. Scaling interpretability framework to larger models
2. Developing approximate belief-attribution methods for practical deployment
3. Creating interpretability tools that output philosophical categories (beliefs, desires) not just features

**Long-term (5+ years):**
1. Complete mapping of LLM belief-desire spaces
2. Automated verification of AI alignment via belief attribution
3. Integration with formal methods for certified interpretability
4. Extending framework to multimodal and embodied AI systems

### Integration with Broader Research Agenda

This paper positions at the intersection of:
- **Mechanistic interpretability research** (tools for understanding neural internals)
- **AI safety and alignment** (ensuring systems have appropriate goals)
- **Philosophy of mind and interpretation** (understanding what beliefs and desires are)
- **Explainable AI** (making AI decisions understandable to humans)

The synthesis suggests an emerging consensus: **trustworthy AI requires philosophically grounded approaches to understanding system internals**, not just engineering tools for feature extraction.

---

## Summary

"Radical AI Interpretability" represents a paradigm shift in how we should approach explaining AI systems. By grounding mechanistic interpretability in rigorous philosophical frameworks about belief and interpretation, Herrmann and Levinstein provide the conceptual tools necessary to answer whether we truly understand what an AI system believes, desires, and means—questions critical for safety, trust, and alignment in deployed AI systems.

The paper's key insight—that belief attribution is fundamentally holistic and constrained by both system internals and interpretive frameworks—suggests both the power and limitations of mechanistic interpretability. We can probe neural networks' internals with increasing sophistication, but converting computational facts into understanding requires philosophical rigor about what counts as success.

For researchers working on AI interpretability, safety, and alignment, this work provides essential theoretical grounding. For practitioners deploying AI systems, it offers frameworks for understanding whether we truly understand the systems we're deploying. For AI policy and regulation, it clarifies what "explainability" and "transparency" should mean in practice.

