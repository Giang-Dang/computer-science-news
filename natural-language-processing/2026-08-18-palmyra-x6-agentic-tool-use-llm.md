# Palmyra x6 Technical Report: An Agentic, Tool-Use Model Post-Trained via Anchored Supervised Fine-Tuning

**Authors:** Peng Du, Kiran Kamble, Rakshith Vasudev, Zhizhuo Yang, Rohith Nadimpally, Arjun Krishna, Waseem Alshikh, Daniel M. Bikel  
**Affiliation:** Scale AI  
**ArXiv ID:** 2608.16620  
**Submitted:** August 17-18, 2026

## Executive Summary

Palmyra x6 is a large language model purpose-built for enterprise-oriented agentic applications and tool-use scenarios. Through a carefully controlled post-training approach using Anchored Supervised Fine-Tuning (SFT) on a compact corpus of verified synthetic tool-use trajectories, the model demonstrates substantial improvements in agent capabilities and tool-use performance. Achieving the highest BFCL Core benchmark score (0.785) and leading six-benchmark mean performance, Palmyra x6 represents a practical advancement in agentic LLM development.

## Problem Statement

**Research Gap:**  
While large language models have demonstrated impressive general capabilities, adapting them for reliable tool-use and agentic reasoning presents distinct challenges:

1. **Tool-Use Complexity:** Effective tool-use requires understanding when to call tools, with what arguments, and how to interpret results—nuances not well-captured in generic language modeling
2. **Agent Behavior:** Agentic reasoning involves sequential decision-making, recovery from errors, and iterative refinement—different from single-turn prediction
3. **Enterprise Requirements:** Production systems require safety, bias mitigation, and predictable behavior beyond standard benchmarks
4. **Data Scarcity:** High-quality tool-use trajectories are expensive to generate and validate
5. **Trade-offs:** Naive fine-tuning risks catastrophic forgetting of general capabilities

**Prior Limitations:**
- Generic LLMs struggle with consistent tool-use patterns
- Standard fine-tuning can degrade performance on non-tool tasks
- Existing agent benchmarks don't correlate well with enterprise requirements
- Few models are explicitly optimized for tool-use reliability
- Limited transparency on training methodology for agentic models

## Core Concepts & Theory

### Anchored Supervised Fine-Tuning

**Key Innovation:** Anchored SFT combines controlled fine-tuning with KL regularization to the frozen base model, preventing catastrophic forgetting while enabling targeted improvement.

```
Traditional SFT:
Base Model → Standard SGD → Specialized Model (potential forgetting)

Anchored SFT:
Base Model → SGD + KL(P_fine-tune || P_base) → Specialized Model (controlled change)
```

**Mathematical Framework:**

The training objective combines task loss with KL regularization:

```
L_total = L_task + β * KL(P_fine-tune || P_base)

where:
- L_task: Cross-entropy loss on tool-use trajectories
- KL divergence: Constrains how far fine-tuned distribution diverges from base
- β: Regularization strength (controls update magnitude)
```

This ensures the model remains capable on general tasks while specializing for tool-use.

### Mixture-of-Experts Base Model

Palmyra x6 is based on a Mixture-of-Experts (MoE) architecture:
- **Sparse routing:** Only subset of experts activated per token
- **Efficient scaling:** Increases capacity without proportional compute increase
- **Specialization potential:** Different experts can specialize for different tasks
- **Tool-use fit:** Expert sparsity maps naturally to decision-making (which tool to use?)

### Tool-Use Trajectory Format

Training data consists of structured interactions:

```
User Request → Model Reasoning → Tool Selection → Tool Call → Tool Result → Result Interpretation → Response

Each trajectory includes:
1. Initial user query
2. Model's reasoning about which tools to use
3. Structured tool calls with arguments
4. Tool execution results (simulated or real)
5. Model's interpretation of results
6. Final response to user
```

## Main Ideas & Contributions

### 1. Controlled Fine-Tuning Recipe

The paper presents a deliberately conservative and reproducible recipe:
- **626 verified synthetic trajectories** (small, high-quality dataset)
- **Single training epoch** (avoids overfitting on small data)
- **Low learning rate** (conservative parameter updates)
- **KL anchor to base** (explicit forgetting prevention)
- **Muon + Adam hybrid optimizer** (stable convergence)

This conservative approach prioritizes reliability over aggressive optimization.

### 2. Synthetic Data Quality

Trajectories are:
- **Verified:** Human validation of tool-use patterns
- **Diverse:** Cover multiple tool-use scenarios and domains
- **Realistic:** Based on actual enterprise use cases
- **Recoverable:** Include error cases and recovery patterns

Quality over quantity enables effective learning from minimal data.

### 3. Benchmark Performance

Palmyra x6 achieves:
- **BFCL Core: 0.785** (highest in benchmark)
- **Six-benchmark mean: Leading performance** across evaluated benchmarks
- **Competitive or leading** in bias and safety evaluations

Demonstrates strength across multiple evaluation dimensions.

### 4. Enterprise Suitability

The model shows:
- **Tool-use reliability:** Consistent, correct tool invocation
- **Safety:** Competitive performance on bias/safety metrics
- **Predictability:** Controlled training enables reproducible behavior
- **Transparency:** Clear methodology and training procedure

### 5. Practical Deployment

Design enables:
- **Clear reproducibility:** Recipe can be replicated
- **Efficiency:** Modest fine-tuning on limited compute
- **Integration:** Works with standard LLM serving infrastructure
- **Monitoring:** Conservative training permits confidence intervals

## Methodology & Implementation

### Base Model Selection

**MoE Architecture Rationale:**
- Sparse routing naturally fits tool-selection decisions
- Efficient scaling enables larger context windows
- Expert specialization can encode task-specific knowledge
- Practical for inference (only subset of weights active)

### Dataset Construction

**Trajectory Generation:**
1. Define tool set (APIs, functions available to agent)
2. Generate user intents (what task should agent accomplish?)
3. Create tool-use sequences (reasoning + calls + results)
4. Include error cases and recovery patterns
5. Human verification of trajectory quality

**626 Trajectory Corpus:**
- Multiple domains (customer service, coding, data analysis)
- Varying complexity (simple single calls to complex sequences)
- Error scenarios (incorrect arguments, tool failures, retries)
- Recovery examples (how agent handles failures)

### Training Procedure

**Hyperparameter Configuration:**
- Learning rate: Conservative (low, tuned for stability)
- Batch size: Moderate (balances memory and gradient variance)
- Optimizer: Muon + Adam hybrid
  - Muon: For second-moment estimation (efficient)
  - Adam: For per-parameter learning rates (adaptive)
- KL regularization: β value chosen to preserve base model

**Training Loop:**
1. Initialize from frozen base model
2. Prepare 626 trajectories as single epoch
3. Apply Anchored SFT training
4. Validate on tool-use benchmarks
5. Verify no catastrophic forgetting on general tasks

**Validation Strategy:**
- Tool-use performance on BFCL
- General capability preservation
- Bias and safety metrics
- Inference speed/cost analysis

### Evaluation Benchmarks

**BFCL (Berkeley Function Calling Leaderboard):**
- Evaluates accuracy of tool-use function calls
- Multiple benchmark suites (Core, Extended, etc.)
- BFCL Core: 0.785 (highest score)

**Additional Evaluations:**
- General knowledge benchmarks (preservation check)
- Bias and safety metrics (fairness, toxicity)
- Task-specific tool-use scenarios
- Real-world enterprise use cases

### Results Summary

[Exact figures unavailable — see full paper]

Key findings:
- **Tool-Use Strength:** Highest BFCL Core score among evaluated models
- **General Capability:** Preserved on general knowledge tasks
- **Safety/Bias:** Competitive or leading on bias and safety metrics
- **Reliability:** Consistent behavior across multiple evaluation runs
- **Efficiency:** Modest compute requirements for fine-tuning

## Practical Applications & Use Cases

### 1. Customer Service Automation

- Routing customer queries to appropriate tools (FAQs, ticketing systems, refunds)
- Retrieving customer information from databases
- Processing refunds and account changes
- Escalating to human agents when needed

### 2. Software Development Assistance

- Calling code search tools to find relevant snippets
- Invoking test runners to validate code
- Accessing documentation systems
- Interacting with version control systems

### 3. Data Analysis and Reporting

- Querying databases for analysis
- Invoking statistical tools
- Generating visualizations
- Automating report generation

### 4. IT Operations and Troubleshooting

- Querying system logs and monitoring tools
- Executing diagnostic commands
- Resolving common issues automatically
- Escalating complex problems

### 5. Business Process Automation

- Scheduling meetings (calendar integration)
- Drafting communications
- Updating CRM systems
- Processing transactions

### 6. Healthcare Support

- Querying patient records (with privacy safeguards)
- Retrieving medical literature
- Scheduling appointments
- Drafting clinical communications

## Insights & Implications

### Paradigm Shift in Agentic LLMs

1. **Quality Over Scale:** 626 verified trajectories outperform naive fine-tuning on massive datasets; curation matters more than volume.

2. **Conservative Post-Training:** Anchored SFT with KL regularization provides better real-world results than aggressive fine-tuning; forgetting prevention is crucial.

3. **MoE Natural Fit:** Sparse routing in MoE models aligns naturally with tool-selection and decision-making.

4. **Transparent Methodology:** Reproducible recipes enable trust and deployment; black-box fine-tuning undermines enterprise confidence.

### Theoretical Insights

- **Trade-off Navigation:** KL regularization provides principled way to balance specialization and generalization
- **Optimizer Hybrid:** Muon + Adam combination provides stable convergence on tool-use trajectories
- **Single Epoch Sufficiency:** High-quality trajectories enable single-epoch training, reducing overfitting risk

### Practical Deployment Lessons

1. **Data Quality Critical:** Verified, diverse trajectories are more valuable than raw size
2. **Conservative Learning:** Low learning rates and KL anchoring improve reliability
3. **Reproducibility Essential:** Controlled recipes enable production deployment
4. **Multi-Metric Evaluation:** Tool-use + safety + general capability assessment needed

### Limitations and Open Questions

1. **Limited Scale:** Only 626 trajectories; unclear how approach scales to millions
2. **Tool Set Specificity:** Different applications need different tool sets; generalization uncertain
3. **Error Handling:** Limited detail on trajectory diversity for error cases
4. **Domain Transfer:** Performance on out-of-distribution tool sets unknown
5. **Inference Cost:** No detailed latency/throughput analysis provided

### Future Research Directions

1. **Scaling Trajectories:**
   - Efficient trajectory generation and validation
   - Active learning to select high-value trajectories
   - Mixture of automatic and human-verified data

2. **Tool Set Generalization:**
   - Transfer learning across different tool sets
   - Meta-learning for new tools with few examples
   - Tool description language for rapid adaptation

3. **Advanced Agentic Behaviors:**
   - Planning and decomposition of complex tasks
   - Uncertainty estimation and confidence scores
   - Multi-step reasoning with backtracking

4. **Production Optimization:**
   - Inference speed optimization
   - Cost-efficient serving
   - Monitoring and fallback mechanisms

## Code & Resources

**Paper Resources:**
- ArXiv: https://arxiv.org/abs/2608.16620
- HTML Version: https://arxiv.org/html/2608.16620
- Technical Report: Full methodology details available in paper

**Base Technologies:**
- Mixture-of-Experts LLM backbone
- Standard transformer inference engines
- Tool-use evaluation benchmarks (BFCL)

**Implementation Stack:**
- Training framework: PyTorch
- Optimizer: Muon + Adam implementation
- Evaluation: BFCL benchmark suite
- Deployment: Standard LLM serving (vLLM, TGI, etc.)

**Key Dependencies:**
- PyTorch >= 1.13
- Transformers library (HuggingFace)
- Custom MoE routing code
- Tool-use trajectory dataset

**Quick-Start Deployment:**
1. Load pretrained Palmyra x6 base model
2. Prepare tool-use trajectory corpus
3. Configure Anchored SFT training
4. Apply post-training to MoE model
5. Evaluate on BFCL and domain-specific benchmarks
6. Deploy with standard inference engine

## Related Work & Context

### Tool-Use in LLMs

1. **Early Tool-Use Work:** Chain-of-Thought, ReAct frameworks
   - Prompt-based approaches without fine-tuning
   - Limited reliability for production

2. **Tool-Use Fine-Tuning:** ToolFormer, TaskLaw
   - Task-specific fine-tuning
   - Requires more data, less general

3. **Function Calling APIs:** GPT-4 turbo, Claude tool-use
   - Proprietary implementations
   - Limited transparency on methodology

4. **Open Tool-Use Models:** Gorilla, Orca-Math
   - Earlier work on open-source tool-use
   - Palmyra x6 advances through controlled post-training

### Post-Training Methodologies

1. **SFT (Supervised Fine-Tuning):** Standard fine-tuning
   - Simple but risk of catastrophic forgetting

2. **RLHF (Reinforcement Learning from Human Feedback):** PPO-based
   - More complex, less stable
   - Harder to reproduce

3. **DPO (Direct Preference Optimization):** Preference-based
   - Simpler than RLHF but for pairwise preferences

4. **Anchored SFT:** Palmyra x6's approach
   - Combines SFT with KL regularization
   - Balances specialization and preservation

### MoE Architecture Development

1. **Sparse MoE:** GShard, Switch Transformers
   - Foundational work on sparse routing

2. **Dense Expert Retrieval:** Mixtral, Grok
   - Modern MoE implementations

3. **Expert Specialization:** Task-specific expert activation
   - Theoretical work on expert differentiation

### Safety and Bias in Agentic Systems

1. **AI Safety in Agents:** Alignment, goal specification
   - Ensuring agents behave as intended

2. **Bias Measurement:** Different frameworks for assessment
   - Fairness across demographics

3. **Tool-Use Safety:** Constraining tool arguments, access control
   - Preventing misuse of available tools

### Benchmark Landscape

**BFCL (Berkeley Function Calling Leaderboard):**
- Comprehensive tool-use evaluation
- Multiple benchmark suites
- Real-world tool scenarios

**Other Evaluation Frameworks:**
- General knowledge benchmarks (MMLU, etc.)
- Bias/safety metrics
- Domain-specific evaluations

## Broader Impact

**Positive Implications:**
- Enables reliable automation of routine tasks
- Reduces need for manual interventions
- Improves accessibility through AI assistance
- Democratizes advanced AI capabilities

**Potential Risks:**
- Job displacement in customer service and routine tasks
- Misuse for deceptive automation
- Over-reliance on automated decisions
- Privacy concerns with data access through tools

**Mitigation Strategies:**
- Transparent tool-use and decision logging
- Human oversight and review mechanisms
- Clear limitation communication
- Privacy-preserving tool interactions

## Discussion

Palmyra x6 demonstrates that thoughtful post-training methodology—emphasizing data quality, controlled learning, and preservation of base capabilities—yields practical, production-ready agentic models. The transparent, reproducible approach enables enterprise adoption while maintaining the flexibility of large language models. This work provides a blueprint for developing specialized models without sacrificing general capability, an important lesson as AI systems become increasingly task-specific.

The achievement of leading performance on BFCL while maintaining competitive bias/safety metrics suggests that agentic capability and safety need not be in tension—proper training methodology can advance both simultaneously.
