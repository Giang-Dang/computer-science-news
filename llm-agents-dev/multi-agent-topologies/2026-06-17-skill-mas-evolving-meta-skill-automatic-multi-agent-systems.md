# Skill-MAS: Evolving Meta-Skill for Automatic Multi-Agent Systems

**ArXiv ID:** 2606.18837  
**Submitted:** June 17, 2026  
**Authors:** Hehai Lin, Qi Yang, Chengwei Qin  
**Affiliations:** Ant Group; The Hong Kong University of Science and Technology (Guangzhou)  
**Domain:** Multi-Agent Systems (cs.MA), Artificial Intelligence (cs.AI)

## Abstract

Skill-MAS proposes a novel third path to bridging the dilemma between model capability and experience retention in LLM-based automatic Multi-Agent Systems (MAS). Existing methods face a fundamental trade-off:

- **Inference-time MAS** leverages frozen frontier LLMs (maximum capability) but repeats identical searches without learning from past experience
- **Training-time MAS** internalizes experience via gradient updates but is constrained by smaller models' lower capability ceiling and doesn't scale to large frontier LLMs

**Skill-MAS decouples experience retention from parametric updates** by conceptualizing the high-level orchestration capability as an evolvable Meta-Skill. This approach enables frontier LLMs to continuously learn from experience while maintaining their full reasoning capabilities.

## Key Research Questions and Solutions

1. **How to retain experience without fine-tuning frontier models?**
   - Answer: Evolve the orchestration strategy (Meta-Skill) in prompt space, not model parameters

2. **How to achieve strong performance across diverse task types?**
   - Answer: Use hierarchical contrastive analysis to distill generalizable principles from task-specific experiences

3. **How to ensure transferability to unseen tasks?**
   - Answer: Learn strategy-level principles rather than task-specific policies

## Core Methodology

### Problem Formulation
Skill-MAS addresses automatic MAS generation for complex tasks requiring:
- Deep reasoning (research questions, mathematical proofs)
- Expert-level problem-solving (competitions, code generation)
- Multi-hop reasoning (question answering across documents)
- Real-world interaction (interactive scenarios, web navigation)

### Closed-Loop Optimization Framework

**Two main components:**

#### 1. Multi-Trajectory Rollout
- Samples a behavioral distribution for each task under the current Meta-Skill
- Generates multiple solution attempts from the frontier LLM
- Captures diverse reasoning paths and failure modes
- Explores the solution space while maintaining model capability

#### 2. Selective Reflection (Adaptive Learning)
- **Priority Task Selection:** Identifies which tasks to learn from
  - Focuses on high-loss, high-impact tasks
  - Avoids redundant re-learning from easy tasks
  - Allocates learning budget strategically

- **Hierarchical Contrastive Analysis:**
  - Contrasts successful vs. failed trajectories at multiple levels:
    - **Task-level:** What worked for this specific problem type?
    - **Strategy-level:** What are the generalizable principles?
    - **System-level:** How do tasks relate to broader patterns?
  - Extracts systemic insights that transfer across domains

### Meta-Skill Representation
- Expressed as prompt-level instructions and orchestration patterns
- Encodes the high-level reasoning strategy for multi-agent coordination
- Evolves through language-based optimization
- Remains independent of underlying LLM parameters

## Key Innovations

1. **Decoupled Learning:** Separates experience retention (Meta-Skill evolution) from parametric updates (LLM capability preservation), enabling use of frontier models like GPT-4o or Claude

2. **Hierarchical Extraction:** Multi-level contrastive analysis captures both task-specific insights and generalizable principles, improving transfer learning

3. **Selective Reflection:** Adaptive task selection prevents overfitting to easy tasks and focuses learning effort where it matters most

4. **Prompt-Space Evolution:** Meta-Skill optimization in prompt space enables rapid iteration and interpretability compared to parameter updates

## Experimental Evaluation

### Benchmarks
Skill-MAS was validated across four challenging, diverse benchmarks:

1. **Deep Research Tasks**
   - Complex information retrieval and synthesis
   - Requires planning and multi-step reasoning

2. **Expert-Level Mathematics**
   - Competition-style problem-solving
   - Rigorous proof verification

3. **Multi-Hop Question Answering** (HotpotQA-style)
   - Multi-document reasoning
   - Requires synthesis across sources

4. **Real-World Interactive Scenarios** (WebShop-style)
   - Dynamic environment interaction
   - Requires adaptation and planning

### Performance Results

**Key Findings:**
- Achieves **remarkable performance gains** across all four benchmarks
- Maintains **favorable cost-performance trade-off** compared to:
  - Inference-time baselines (better experience retention)
  - Training-time approaches (better model capability)
  - Static orchestration patterns (better adaptation)

### Model Coverage
Extensive experiments across **four distinct LLMs:**
- GPT-4-based models
- Claude models
- Smaller capable models
- Ensures findings generalize across different model architectures

### Transfer Learning Results
- **Strong robustness:** Evolved Meta-Skills transfer effectively
- **Cross-task generalization:** Strategies learned on one benchmark transfer to unseen tasks
- **Cross-model generalization:** Meta-Skills developed with one LLM successfully apply to different models

## Technical Contributions

1. **Orthogonal Learning Paradigm:** Demonstrates a viable path to continuous learning without parametric updates to frontier models

2. **Strategy-Level Abstraction:** Shows that high-level orchestration strategies (not just individual tool calls) can be effectively optimized

3. **Empirical Validation at Scale:** Proves effectiveness across diverse task types and multiple models simultaneously

4. **Scalable Architecture:** Approach scales to frontier models without requiring fine-tuning infrastructure

## Relevance to Software Development

Skill-MAS has direct applications to LLM-based software engineering:

### 1. **Multi-Agent Code Generation Teams**
- Orchestration Meta-Skill can encode best practices for multi-agent collaboration on codebases
- Evolves as team learns from successful and failed code synthesis attempts
- Transfers learned strategies to new projects with different architectures

### 2. **Adaptive Development Strategies**
- Meta-Skill encodes when to use different coding approaches:
  - When to generate full functions vs. incremental refinement
  - When to invoke testing agents vs. code review
  - When to leverage external tools vs. internal reasoning
- Learns from past development sessions

### 3. **Cross-Project Generalization**
- Strategies learned on one codebase transfer to new projects
- Different task types (API design, refactoring, debugging) inform each other
- Selective reflection identifies which experiences matter most

### 4. **Scalable Multi-Agent Systems**
- Enables coordination of many specialized agents (testing, documentation, security review, etc.)
- No need to fine-tune models for each project or team
- Adapts to different project constraints and preferences

### 5. **Continuous Improvement**
- System improves over time without retraining
- Captures team practices and preferences in evolved Meta-Skill
- Can distribute learned strategies across teams and projects

## Comparison with Related Approaches

| Approach | Model Capability | Experience Retention | Learning Cost | Frontier Model Support |
|----------|------------------|----------------------|----------------|------------------------|
| Inference-time MAS | Excellent | None | Very Low | Yes |
| Training-time MAS | Poor | Excellent | High | No |
| **Skill-MAS** | **Excellent** | **Excellent** | **Low** | **Yes** |
| Static Orchestration | Excellent | None | None | Yes |

## Limitations and Future Work

1. **Meta-Skill Complexity:** More complex tasks may require more sophisticated Meta-Skill representations
2. **Generalization Boundaries:** Some task families may require task-specific tuning
3. **Interpretability:** Understanding why certain Meta-Skills work well for specific domains
4. **Large-Scale Application:** Testing on even more diverse and complex task distributions

## Code and Resources

- Full implementation available
- Benchmarks and evaluation suites documented
- Model configurations for GPT-4, Claude, and other frontier models
- Reproducible experimental setup

## Related Work

- **Multi-Agent Orchestration:** ABSTRAL, MACOG, AgentForge
- **Skill Learning:** EvoSkills, SkillFlow, SkillRL
- **RL for LLMs:** Reinforcement learning approaches to agent training
- **Prompt Optimization:** In-context learning and prompt-based adaptation
- **Transfer Learning:** Cross-task and cross-model generalization

## Publications and Links

- **ArXiv:** [2606.18837 - Skill-MAS: Evolving Meta-Skill for Automatic Multi-Agent Systems](https://arxiv.org/abs/2606.18837)
- **HTML Version:** [Full paper on ArXiv](https://arxiv.org/html/2606.18837)

## Conclusion

Skill-MAS presents a breakthrough approach to continuous learning in multi-agent LLM systems without the constraints of fine-tuning frontier models. By focusing on orchestration strategies rather than individual components, and by employing hierarchical contrastive analysis to extract generalizable principles, the approach achieves strong performance gains while maintaining model capability. The strong cross-task and cross-model transfer results suggest this is a promising path toward adaptive, scalable autonomous systems that improve over time while maintaining access to frontier models.
