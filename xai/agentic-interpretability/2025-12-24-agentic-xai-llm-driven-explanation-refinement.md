# Agentic Explainable Artificial Intelligence (Agentic XAI): LLM-Driven Iterative Refinement for Enhanced Explanations

**ArXiv ID:** 2512.21066  
**Authors:** Tomoaki Yamaguchi, Yutong Zhou, Masahiro Ryo, Keisuke Katsura  
**Submitted:** December 24, 2025  
**Latest Version:** March 12, 2026 (v3)  
**Subjects:** Artificial Intelligence (cs.AI); Human-Computer Interaction (cs.HC)

## Executive Summary

Explainable AI (XAI) systems like SHAP provide technical insights into model predictions but often communicate poorly with non-technical stakeholders. This paper introduces Agentic XAI, a novel framework that combines SHAP-based explainability with multimodal large language model (MLLM) agents for iterative refinement, progressively enhancing explanation quality. Tested on an agricultural rice yield recommendation system, the framework achieved 30-33% improvement in explanation quality over baseline SHAP explanations, demonstrating significant potential for bridging the gap between technical explanations and human understanding in mission-critical domains.

## Problem Statement

While Explainable AI techniques have advanced significantly in recent years, a critical gap remains between what these methods can explain and how effectively those explanations communicate with end-users. Traditional XAI approaches face several challenges:

1. **Communication Gap**: SHAP outputs and feature importance visualizations are often too technical for domain experts and stakeholders without machine learning backgrounds
2. **Accessibility**: Non-technical users struggle to extract actionable insights from quantitative explanations
3. **Trust Building**: Complex technical explanations may not effectively build user trust in AI-based predictions
4. **Context Awareness**: Standard explanations lack domain-specific context and real-world applicability

The paper addresses a fundamental question: How can we iteratively enhance XAI explanations to make them more understandable and actionable for real-world users while maintaining fidelity to the underlying model behavior?

## Core Concepts & Theory

### Foundation: SHAP (SHapley Additive exPlanations)

SHAP is a game-theoretic approach to model interpretability that assigns each feature a value based on how much that feature contributes to a prediction. SHAP values are grounded in Shapley values from cooperative game theory and provide:

- **Local explanations**: Understanding individual predictions
- **Feature importance rankings**: Which features matter most
- **Contribution magnitude**: How much each feature contributes (positive or negative)

**Limitation of Traditional SHAP**: While mathematically rigorous, SHAP visualizations (waterfall plots, force plots, dependence plots) are often incomprehensible to non-technical users.

### Multimodal Large Language Models (MLLMs)

Modern large language models (GPT-4, Claude, LLaMA) can process and generate natural language at scale. When combined with vision capabilities, MLLMs can:

- Interpret visual representations (charts, plots, diagrams)
- Generate natural language descriptions
- Perform iterative refinement through agent-like feedback loops
- Adapt explanations to different audiences

### Agentic AI Architecture

The paper leverages an agentic approach where LLMs act as autonomous agents that:

1. **Perceive**: Analyze SHAP visualizations and data
2. **Reason**: Generate analytical hypotheses and code
3. **Act**: Create supplementary analyses and refined explanations
4. **Learn**: Iteratively improve explanations based on evaluation feedback

This creates a feedback loop: Initial SHAP → LLM Analysis → Refined Explanation → Evaluation → Next Iteration

## Main Ideas & Key Contributions

### 1. Novel Integration: SHAP + Agentic LLM Refinement

The paper's primary innovation is the systematic combination of:
- **Deterministic XAI (SHAP)**: Ensuring explanation fidelity to model behavior
- **Generative XAI (MLLM agents)**: Enhancing understandability and accessibility

This hybrid approach preserves mathematical rigor while improving practical usability.

### 2. Iterative Refinement Framework

The framework operates through 11 refinement rounds (0-10):

**Round 0 (Baseline):** SHAP explanation of the prediction
- Standard SHAP waterfall plot showing feature contributions
- Direct output from the trained model

**Rounds 1-10 (Agentic Refinement):**
- MLLM analyzes previous explanation and output
- Generates supplementary analyses (e.g., correlation studies, sensitivity analyses)
- Creates visualization code (Python/matplotlib) for additional plots
- Produces refined natural language explanation incorporating new insights
- Updates farmer recommendations with domain-specific context

### 3. Bias-Variance Tradeoff in Iterative Refinement

A critical finding is the bias-variance tradeoff observed during refinement:

- **Early rounds (0-2)**: High bias, low variance. SHAP explanation lacks depth and context. Limited actionable insights.
- **Optimal rounds (3-4)**: Balanced bias-variance. Peak explanation quality at 30-33% improvement over baseline. Maximum practical utility.
- **Late rounds (5-10)**: Low bias, high variance. Excessive refinement introduces:
  - Verbosity and redundancy
  - Ungrounded abstractions
  - Contradictions between refined explanations
  - Decreased practical usefulness
  - Degraded recommendation quality

**Key Insight**: More refinement is not always better. Optimal stopping around rounds 3-4 achieves the best balance between explanation depth (reducing bias) and clarity (controlling variance).

### 4. Evaluation Methodology

Explanations were evaluated across 7 quantitative and qualitative metrics:

1. **Specificity**: How specific and targeted is the explanation?
2. **Clarity**: How easy is it to understand?
3. **Conciseness**: Is the explanation appropriately brief?
4. **Practicality**: How actionable are the recommendations?
5. **Contextual Relevance**: Does it address domain-specific concerns?
6. **Cost Consideration**: Does it account for practical constraints?
7. **Crop Science Credibility**: Does it align with agricultural expertise?

Evaluators: 
- 12 human crop scientists (domain experts)
- 14 LLM-based evaluators (automated consistency checks)

This dual evaluation approach provides both human validation and systematic consistency checking.

## Methodology & Implementation

### System Architecture

```
Input Data
    ↓
Random Forest Model
    ↓
SHAP Analysis
    ↓
MLLM Agent (Agentic Refinement Loop)
    ├─ Perceive: Analyze SHAP & visualizations
    ├─ Reason: Generate analytical hypotheses
    ├─ Act: Create supplementary analyses & code
    └─ Generate refined explanations
    ↓
Evaluation (Rounds 0-10)
    ├─ Human experts (crop scientists)
    └─ LLM evaluators
    ↓
Farmer Recommendations
```

### Dataset & Experimental Setup

**Agricultural Use Case: Rice Yield Prediction**

**Dataset:**
- 26 rice fields in Japan
- Data collected from multiple growing seasons
- Features included:
  - Soil properties (pH, nitrogen content, organic matter)
  - Rice varieties and cultivation practices
  - Planting dates and transplanting schedules
  - Fertilization strategies
  - Pesticide/herbicide application timing
  - Meteorological data (temperature, precipitation, solar radiation)

**Model:**
- Random Forest regressor for rice yield prediction
- Trained to predict yield based on soil and cultivation factors
- Provides baseline predictions with SHAP explanations

### Results & Performance

**Quantitative Findings:**

- **Baseline (Round 0)**: SHAP waterfall plot - raw feature contribution values
- **Peak Performance (Rounds 3-4)**: 
  - Average score increase: **30-33% improvement** over baseline
  - Both human experts and LLM evaluators confirmed quality improvement
  - Optimal recommendation quality achieved
- **Degradation (Rounds 5-10)**:
  - Continued refinement decreased explanation quality
  - Verbosity increased without proportional increase in insight
  - Contradiction rates increased (estimated variance > bias reduction)

**Qualitative Observations:**

1. **Human Expert Feedback (n=12 crop scientists)**:
   - Rounds 0-1: Too technical, difficult to apply in practice
   - Rounds 2-4: Balanced technical depth with practical applicability
   - Rounds 5-10: Increasingly verbose and sometimes contradictory

2. **LLM Evaluator Consistency (n=14 models)**:
   - High consistency in identifying Rounds 3-4 as optimal
   - Detected inconsistencies and self-contradictions in later rounds
   - Flagged ungrounded claims and speculative statements

**Statistical Details:**
- [Exact figures unavailable — see full paper]
- Score distributions across evaluation metrics show clear peak at Rounds 3-4
- Variance in later rounds suggests model instability

### Implementation Considerations

**Computational Requirements:**
- SHAP calculation: Depends on Random Forest complexity and feature dimensionality
- MLLM inference: Requires modern GPU or cloud API (GPT-4, Claude)
- Total time per refinement cycle: [Estimated] 2-5 minutes per cycle with API-based MLLMs
- Cost: Dominated by MLLM API calls in later rounds (multiple supplementary analyses)

**Key Implementation Details:**

1. **Prompt Engineering**: The quality of agentic refinement depends heavily on prompt design for:
   - Initial SHAP interpretation
   - Analytical hypothesis generation
   - Natural language explanation generation
   - Domain-specific adaptation

2. **Context Management**: Early refinement rounds benefit from providing:
   - Domain context (agricultural knowledge base)
   - User expertise level assumptions
   - Specific decision constraints

3. **Stopping Criteria**: Implementing early stopping around Round 3-4 is critical:
   - Reduces computational cost
   - Prevents quality degradation
   - Improves user experience

## Practical Applications & Real-World Use Cases

### 1. Agricultural Advisory Systems

**Primary Use Case (Paper):**
- Rice cultivation optimization
- Farmer decision support systems
- Agronomic recommendations based on soil and climate data

**Broader Agricultural Applications:**
- Crop yield prediction across multiple crop types
- Fertilizer recommendation systems
- Pest and disease risk prediction
- Climate adaptation advisory

**Domain Criticality**: Agriculture faces increasing pressure from climate change, resource constraints, and population growth. Explainable predictions that farmers can trust and understand are essential for adoption of data-driven practices.

### 2. Healthcare & Medical Diagnosis

**Application**: Clinical decision support systems
- Diagnostic predictions with physician-friendly explanations
- Treatment recommendations with evidence summaries
- Risk stratification with actionable interventions

**Regulatory Relevance**: FDA's guidance on clinical decision support systems increasingly emphasizes the need for interpretable and explainable AI.

### 3. Financial Services & Risk Management

**Application**: Credit risk assessment, fraud detection
- Loan approval decisions with clear explanations for applicants
- Regulatory compliance with explainability requirements (GDPR, Fair Lending regulations)
- Trust building through transparent decision processes

### 4. Autonomous Systems & Robotics

**Application**: Robotic decision-making for mission-critical operations
- Explainable path planning and navigation decisions
- Transparent sensor interpretation and anomaly detection
- Accountability in safety-critical failures

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **XAI is not enough**: Technical explanations alone cannot bridge the human-AI understanding gap. Active intervention through LLM-based communication is necessary.

2. **Iterative refinement has limits**: The bias-variance tradeoff suggests that more sophisticated explanations can become counterproductive. This challenges the implicit assumption that "more explanation = better understanding."

3. **Hybrid approaches are promising**: Combining rigorous quantitative XAI (SHAP) with generative AI (LLM) leverages strengths of both paradigms:
   - SHAP ensures fidelity to model behavior
   - LLM ensures human comprehensibility

4. **Domain adaptation matters**: The framework's success depends on incorporating domain-specific knowledge and constraints. One-size-fits-all explanations are inadequate.

### Advancement of XAI State-of-the-Art

**Previous XAI Paradigm:**
- Focus on what models do (local/global feature importance)
- Technical accuracy as primary goal
- Limited user studies validating understandability

**Agentic XAI Contribution:**
- Shifts focus to how users understand model behavior
- Combines technical rigor with communication effectiveness
- Empirically demonstrates iterative improvement with quantifiable limits

### Limitations & Open Questions

1. **Computational Complexity**: 
   - Iterative refinement requires multiple MLLM inference calls
   - Scalability to real-time systems unclear
   - Cost implications for large-scale deployment

2. **Generalization**:
   - Primary evaluation on single domain (agriculture)
   - Transferability to healthcare, finance, other domains uncertain
   - Different domains may have different optimal stopping points

3. **Evaluation Challenges**:
   - Human expert evaluation limited to 12 crop scientists
   - LLM evaluator reliability not independently validated
   - No comparison to other XAI communication strategies (e.g., natural language explanations from scratch)

4. **Theoretical Understanding**:
   - Why does variance increase after Round 4? Mechanism unclear
   - How to predict optimal stopping point a priori?
   - What prompt structures lead to explanation quality improvements?

5. **User Study Gaps**:
   - No direct measurement of user understanding improvement
   - No assessment of decision quality when using refined vs. baseline explanations
   - Limited analysis of user trust evolution across refinement rounds

### Future Research Directions

1. **Theoretical Framework**: Develop formal model of explanation quality vs. refinement round relationship

2. **Multi-Domain Validation**: Test framework across healthcare, finance, autonomous systems with corresponding user populations

3. **Adaptive Stopping**: Develop algorithms to predict optimal stopping point without running full refinement cycle

4. **Prompt Optimization**: Systematic study of prompt engineering impact on explanation quality

5. **Real-World Deployment**: Longitudinal studies on farmer adoption, decision quality, and trust in production systems

6. **Alternative Refinement Strategies**: Explore other agentic architectures, including multi-agent systems and structured reasoning approaches

## Code & Resources

### Official Implementation
- **GitHub Repository**: Not yet publicly available (as of paper publication)
- **Contact**: Authors at [institutional affiliations in paper]

### Dependencies & Requirements

**Core Libraries:**
- SHAP (for Shapley value calculations and visualizations)
- scikit-learn (Random Forest implementation)
- LangChain or similar (agentic LLM orchestration)
- OpenAI/Anthropic API (for MLLM inference)
- pandas, numpy (data processing)

**Optional Dependencies:**
- matplotlib, plotly (visualization)
- jupyter (interactive notebooks)

### Computational Requirements
- **Minimum**: CPU-based testing (slow inference)
- **Recommended**: 
  - GPU for local MLLM hosting (A100 or better)
  - OR cloud API access to GPT-4/Claude (recommended for production)
- **Storage**: Minimal (explanations are generated on-demand)

### Quick Start Guide

1. **Install Dependencies**:
   ```bash
   pip install shap scikit-learn langchain openai pandas numpy
   ```

2. **Prepare Data**:
   - Load tabular dataset with features and target variable
   - Train Random Forest model on training data

3. **Generate SHAP Explanations**:
   ```python
   import shap
   explainer = shap.TreeExplainer(model)
   shap_values = explainer.shap_values(X_test)
   ```

4. **Initialize Agentic Refinement**:
   - Set up LLM client (OpenAI/Anthropic)
   - Create SHAP visualization
   - Initialize agentic refinement loop

5. **Run Refinement Cycles**:
   - Execute Rounds 0-10
   - Evaluate at each round using your metrics
   - Identify optimal stopping point (likely Rounds 3-4)

### Interactive Demos & Visualizations
- [To be published]: Paper authors may release interactive demos showing refinement progression
- Potential platforms: Hugging Face Spaces, Streamlit applications

## Related Work & Context

### Related XAI Approaches

**Feature Attribution Methods:**
- LIME (Local Interpretable Model-agnostic Explanations): Rule-based local approximations
- Integrated Gradients: Gradient-based feature importance for deep learning
- Attention visualization: Interpretability for transformer models

**Concept-Based Explanations:**
- TCAV (Testing with Concept Activation Vectors): Human-interpretable concept-level explanations
- CBMs (Concept Bottleneck Models): Models explicitly trained on interpretable concepts

**Natural Language Explanations:**
- NLX (Natural Language eXplanations): Free-form text explanations from models
- Counterfactual explanations: "What would need to change for different prediction"

### Relationship to Prior Work

**Agentic XAI extends:**
1. **SHAP**: Uses SHAP as foundation but addresses its communication limitations
2. **LLM-based XAI**: Builds on work using LLMs for explanation generation (e.g., "An Agentic Approach to Generating XAI-Narratives", 2603.20003)
3. **Human-Centered XAI**: Contributes empirical evidence to human-centered XAI research about what makes explanations effective

**Key Distinctions:**
- Unlike pure LLM explanation generation, maintains fidelity through SHAP grounding
- Unlike traditional XAI, explicitly addresses human comprehensibility
- Unlike prior agentic approaches, quantifies quality with evaluation metrics

### Connection to Broader XAI Community

**Standardization & Tools:**
- Part of growing ecosystem of XAI evaluation frameworks
- Complements initiatives like "Explainability & Accountability" (EA) frameworks
- Relevant to NIST AI Risk Management Framework's explainability pillar

**Research Communities:**
- Human-Computer Interaction (HCI) in AI: User studies, trust, communication
- Responsible AI: Trustworthiness, transparency, accountability
- Mechanistic Interpretability: Understanding model internals (complementary approach)
- Fairness & Bias: Using explanations to detect and mitigate bias

### Relevant Contemporary Papers

**Directly Related (2025-2026):**
1. "Fewer Than 1% of Explainable AI Papers Validate Explainability with Humans" (2503.16507): Motivates the need for human evaluation
2. "VirtualXAI: A User-Centric Framework for Explainability Assessment Leveraging GPT-Generated Personas" (2503.04261): Complementary approach to XAI evaluation
3. "Beyond Explainable AI: An Overdue Paradigm Shift and Post-XAI Research Directions" (2602.24176): Critiques XAI limitations that Agentic XAI helps address

**Foundational Work:**
- SHAP (Lundberg & Lee, 2017): Original Shapley value explanation method
- LIME (Ribeiro et al., 2016): Local interpretable model-agnostic explanations
- Attention is All You Need (Vaswani et al., 2017): Transformer architecture underlying modern LLMs

## Significance & Future Impact

### Why This Paper Matters

1. **Practical Solution**: Addresses a real gap between XAI methods and user comprehension
2. **Quantified Improvement**: Demonstrates 30-33% quality improvement with clear evaluation metrics
3. **Replicable Framework**: Provides systematic methodology applicable across domains
4. **Empirical Rigor**: Combines human expert evaluation with automated consistency checking

### Potential for Influence

- **Immediate**: Adoption in agricultural AI systems for farmer advisory
- **Medium-term**: Deployment in healthcare and finance as regulatory pressure increases
- **Long-term**: May become standard practice for explaining AI predictions in mission-critical domains

### Call to Action for Researchers

1. Replicate in other domains (healthcare, finance, autonomous systems)
2. Investigate theoretical foundations of bias-variance tradeoff
3. Develop algorithms for predicting optimal stopping point
4. Study impact on user decision-making and trust evolution
5. Explore multi-agent refinement strategies

---

## References & Sources

- ArXiv Paper: [Agentic Explainable Artificial Intelligence (Agentic XAI)](https://arxiv.org/abs/2512.21066)
- SHAP Documentation: https://shap.readthedocs.io/
- Related XAI Papers:
  - "Fewer Than 1% of Explainable AI Papers Validate Explainability with Humans" (2503.16507)
  - "VirtualXAI: A User-Centric Framework for Explainability Assessment" (2503.04261)
  - "Beyond Explainable AI: An Overdue Paradigm Shift" (2602.24176)
  - "An Agentic Approach to Generating XAI-Narratives" (2603.20003)
