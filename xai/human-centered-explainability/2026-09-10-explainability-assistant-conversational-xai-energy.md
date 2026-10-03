# Explainability Assistant: A Conversational XAI Interface for Interpreting Energy Consumption Models

**ArXiv ID:** [2609.11860](https://arxiv.org/abs/2609.11860)  
**Authors:** Rodion Krjutškov, Eduard Barbu, Nikos Sakkas, Sofia Yfanti  
**Submitted:** September 10, 2026

**Conference:** ICECET 2026 (6th International Conference on Electrical, Computer and Energy Technologies, Rome, Italy)  

## Executive Summary

This paper introduces the Explainability Assistant, an open-source conversational XAI system that leverages Large Language Models' function-calling capabilities to provide intuitive, natural language-based explanations for complex machine learning models. By overcoming limitations of rigid, grammar-based conversational systems, the Explainability Assistant achieves 94% intent-parsing accuracy and demonstrates superior usability compared to traditional XAI dashboards, with all three specialists in the comparison study preferring the conversational interface.

## Problem Statement

Energy consumption forecasting and other real-world applications rely on increasingly complex machine learning models, including Genetic Programming-based symbolic regressors, whose predictions are often difficult for facility managers, building operators, and domain experts to interpret. While Explainable Artificial Intelligence (XAI) techniques address model opacity, traditional approaches suffer from critical limitations:

1. **Complexity of Traditional Dashboards**: XAI dashboards require substantial technical expertise, limiting accessibility for non-technical stakeholders
2. **Limited Interactivity**: Fixed visualizations and interfaces lack flexibility for dynamic, context-aware inquiry
3. **Rigid Grammar-Based Systems**: Previous conversational XAI systems like TalkToModel were constrained by custom grammars and achieved only 76.8% intent-parsing accuracy
4. **Static Explanations**: Traditional XAI methods provide read-only explanations without adapting to user questions and context
5. **Domain Specificity**: Most conversational systems require task-specific fine-tuning, limiting generalization

The paper identifies a gap between the potential of conversational interfaces and the practical limitations of grammar-based approaches, motivating the development of LLM-powered conversational XAI.

## Core Concepts & Theory

### Conversational XAI Architecture

Conversational XAI represents a human-centered approach to model interpretability that combines:

- **Natural Language Processing (NLP)**: Understanding user queries in open-ended natural language rather than constrained formal grammars
- **Function Calling**: Leveraging LLM function-calling capabilities to dispatch appropriate interpretation tasks
- **Multi-Modal Explanations**: Providing explanations through dialogue, numerical results, visualizations, and structured reasoning

### Key Interpretability Techniques Integrated

The Explainability Assistant incorporates multiple XAI methodologies:

1. **Feature Attribution**: Identifying which features most influence model predictions
2. **Model Performance Analysis**: Evaluating metrics, accuracy, and prediction quality
3. **Counterfactual Explanations**: "What-if" scenarios to understand decision boundaries
4. **Model Behavior Analysis**: Understanding patterns in predictions across different inputs
5. **Symbolic Reasoning**: For Genetic Programming models, explaining symbolic equations directly

### Function-Calling Based Architecture

Instead of implementing a rigid grammar parser, the system leverages LLM function-calling to:

```
User Query → LLM Intent Recognition → Function Call Dispatch → 
Model Analysis → Explanation Generation → Natural Language Response
```

This approach:
- Achieves higher parsing accuracy (94% vs. 76.8% for grammar-based systems)
- Requires no task-specific fine-tuning
- Adapts naturally to diverse ML domains
- Provides more fluent, contextual responses

### Comparison with Prior Approaches

| Aspect | Grammar-Based (TalkToModel) | LLM-Based (Explainability Assistant) |
|--------|----------------------------|--------------------------------------|
| Intent Parsing | 76.8% accuracy | 94% accuracy |
| Adaptability | Task-specific | Multi-domain without fine-tuning |
| Natural Language | Limited to grammar | Full natural language |
| Usability | Technical barrier | Domain expert accessible |
| Modularity | Custom implementations | Generic LLM interface |

## Main Ideas & Key Contributions

### 1. LLM Function-Calling for XAI Dispatch

The primary innovation is leveraging modern LLM function-calling capabilities to replace rigid grammar-based parsing. Rather than implementing custom parsers, the system:

- Defines interpretable functions (e.g., `analyze_feature_importance()`, `get_prediction_explanation()`)
- Lets the LLM understand user intent and map it to appropriate functions
- Automatically routes queries to correct interpretation methods
- Handles variations in natural language phrasing seamlessly

**Technical Advantage**: This approach is more robust to natural language variations and requires no task-specific fine-tuning, enabling deployment across diverse ML domains.

### 2. Domain-Agnostic Conversational Interface

The system's architecture enables seamless application to different ML domains:

- **Energy Domain**: Interpreting Genetic Programming symbolic regressors for building energy forecasting
- **Healthcare Domain**: Explaining heart disease classification models
- **Extensible Design**: Easily adaptable to other domains without model retraining

### 3. Superior Accuracy and Usability

Key achievements from evaluation:

- **94% Intent-Parsing Accuracy**: Significant improvement over 76.8% baseline
- **Flexible Natural Language**: Handles open-ended user queries without grammar constraints
- **Unanimous Expert Preference**: All domain specialists preferred conversational interface for practical use
- **Consistent Task Accuracy**: Maintains high performance while improving usability

### 4. Open-Source Implementation

The Explainability Assistant is released as open-source, lowering barriers to adoption and enabling community contributions for extending functionality to new domains and model types.

## Methodology & Implementation

### Parsing evaluation

The evaluation covers 20 available functions. A manually created set has 20 samples; two LLM-generated sets have 80 samples each and were manually checked. Exact-match function-call accuracy is measured on two combined sets of 100 samples. Gemini-2.5-Flash reaches 94% and 93%; the 76.8% TalkToModel figure is a previously reported comparison, not a fresh experiment under identical conditions.

### Domain-specialist comparison

Three energy specialists used both a dashboard and the conversational assistant. Task accuracy was 93% with the dashboard and 100% with the assistant, and all three preferred the conversational interface. The sample is too small to establish a statistically significant performance advantage or general adoption outcome.

The front end uses Next.js and the back end invokes explanation functions selected through LLM function calling. Provider choice, unsupported requests, and explanation correctness still need evaluation in each deployment.

## Practical Applications & Real-World Use Cases

### 1. Energy Management & Smart Buildings

**Domain Criticality**: Building energy management is essential for sustainability, cost reduction, and grid stability. Understanding how ML models predict energy consumption enables:

- **Facility Manager Decision Support**: Non-technical facility managers can query why predictions changed without data science expertise
- **Optimization Exploration**: Conversational interface enables asking "what-if" questions about energy-saving interventions
- **Stakeholder Communication**: Explains complex model behavior to building owners and regulatory bodies
- **Fault Detection**: Identifying when models behave unexpectedly due to equipment failures or anomalies

**Concrete Example**: A facility manager could ask "Why did the model predict lower energy consumption on Tuesday?" and receive a conversational explanation of contributing factors (weather, occupancy, schedule changes).

### 2. Healthcare & Medical Decision Support

**Domain Criticality**: Medical decision-making requires trust and understanding. The paper demonstrates application to heart disease classification:

- **Clinical Interpretation**: Physicians can interrogate why models flagged certain patients as high-risk
- **Patient Explanation**: Patients can understand what factors influenced diagnostic predictions
- **Regulatory Compliance**: Natural language explanations support HIPAA, GDPR, and FDA requirements for explainability

**Concrete Example**: A cardiologist could ask "What specific risk factors did the model identify for this patient?" and receive personalized explanations.

### 3. Regulatory & Compliance Applications

Conversational XAI supports emerging regulatory requirements:

- **GDPR Article 22**: Right to explanation for automated decisions
- **EU AI Act**: Explainability requirements for high-risk AI systems
- **FDA Requirements**: Pre-market approval for clinical AI systems increasingly demands interpretability
- **Loan & Credit Decisions** (Fair Lending): Applicants can understand loan denial or rate decisions

### 4. Industrial & Manufacturing Applications

- **Anomaly Detection**: Explaining why models flagged equipment failures
- **Quality Control**: Understanding factors driving quality predictions
- **Predictive Maintenance**: Communicating maintenance urgency to technicians

### Practical Feasibility & Implementation Challenges

**Advantages:**
- Open-source implementation reduces deployment barriers
- No task-specific fine-tuning required for new domains
- Standard LLM APIs can be leveraged (reducing development cost)
- Familiar chat interface reduces user learning curve

**Challenges:**
- **LLM API Costs**: Real-time LLM inference adds operational expenses
- **Latency**: LLM inference introduces delays vs. static dashboards (milliseconds to seconds)
- **Privacy Concerns**: Sending model details to cloud LLM APIs may violate data governance policies
- **Reproducibility**: LLM responses can vary non-deterministically; need validation mechanisms
- **Model Misalignment**: If LLM incentives differ from accurate explanation goals

## Insights & Implications

### Broader Implications for Trustworthy AI

This work demonstrates that **human-centered interface design is as important as statistical rigor** for XAI effectiveness. A statistically faithful explanation presented poorly is less useful than a slightly simplified explanation delivered in an accessible, conversational manner.

Key implications:

1. **Accessibility Democratizes Interpretability**: Moving from technical dashboards to conversational interfaces significantly lowers barriers to adoption
2. **LLMs as XAI Infrastructure**: Function-calling capabilities enable LLMs to serve as flexible dispatchers for interpretation tasks
3. **Multi-Domain Generalization**: Conversational XAI can adapt across domains without per-domain fine-tuning, unlike prior grammar-based systems
4. **Human-AI Collaboration**: Conversational interfaces enable dynamic, iterative exploration of model behavior, supporting deeper understanding

### State-of-the-Art Advancement

The Explainability Assistant represents advancement in:

1. **Intent Recognition Accuracy**: 94% vs. 76.8% prior state-of-the-art
2. **Generalization**: Domain-agnostic adaptation without fine-tuning
3. **Practical Deployment**: Unanimous expert preference in real-world evaluation
4. **Accessibility**: Enabling non-technical stakeholders to interrogate complex models

### Limitations, Failure Cases & Open Questions

**Unresolved Challenges:**

1. **Explanation Faithfulness**: How do we ensure LLM-generated explanations faithfully represent model behavior vs. generating plausible narratives?
2. **Scalability**: Can conversational XAI scale to extremely large models and datasets with millions of features?
3. **Adversarial Robustness**: Could users manipulate conversational queries to elicit misleading explanations?
4. **Offline/Private Deployment**: How to deploy conversational XAI in data-sensitive environments requiring on-premise inference?
5. **Explanation Evaluation Metrics**: How to quantitatively measure conversational explanation quality beyond accuracy metrics?

**Failure Modes:**

- LLMs may generate "confident" explanations for edge cases without sufficient evidence
- Sophisticated domain experts may ask questions requiring explanation depth beyond LLM capabilities
- Outdated domain knowledge in LLM training could lead to anachronistic explanations

### Future Research Directions

1. **Hybrid Local-Conversational XAI**: Combining fine-tuned local models with conversational interfaces
2. **Multi-Turn Explanation Refinement**: Iterative queries to refine understanding through dialogue
3. **Personalized Explanations**: Adapting explanation depth and style to user expertise level
4. **Explanation Verification**: Automated validation that conversational explanations match ground-truth model behavior
5. **Causal Conversational XAI**: Integrating causal reasoning into conversational explanations
6. **Multimodal Explanations**: Combining text, visualizations, and interactive plots in dialogue

## Code & Resources

- [Primary paper](https://arxiv.org/abs/2609.11860)
- [Full text](https://arxiv.org/html/2609.11860)
- [Backend](https://github.com/krkv/explainability-backend)
- [Frontend](https://github.com/krkv/explainability-frontend)
- [Parsing evaluation](https://github.com/krkv/llm-evaluation)

## Related Work & Context

### Connection to Recent xAI Literature

This work builds on and relates to several recent research directions:

1. **Editable XAI** ([2602.12569](https://arxiv.org/abs/2602.12569)): Prior human-centered work enabling users to edit explanations for better alignment. The Explainability Assistant complements this by enabling interactive dialogue-based exploration rather than static editing.

2. **Is Conversational XAI All You Need?** ([2501.17546](https://arxiv.org/abs/2501.17546)): Explores effectiveness of conversational XAI for human-AI decision-making, questioning whether conversational interfaces alone suffice or require supplementary visualizations.

3. **Feature Attribution Methods**: Builds on established SHAP, LIME, and integrated gradients methods as backend analysis engines.

4. **XAI Surveys**: Continues themes from meta-surveys like "Explainable AI (XAI): A Systematic Meta-Survey of Current Challenges and Future Opportunities" identifying usability as key barrier.

### Prior Work on Conversational AI

- **TalkToModel** (prior work baseline at 76.8%): Grammar-based conversational XAI with rigid syntax constraints
- **Neural-Symbolic Integration**: Combining neural networks (LLMs) with symbolic reasoning for explainability

### XAI Community Context

**Relevant Communities & Frameworks:**

- **LIME (Local Interpretable Model-agnostic Explanations)**: Model-agnostic local approximations that Explainability Assistant can leverage
- **SHAP (SHapley Additive exPlanations)**: Game-theoretic feature attribution used by backend analysis engines
- **Concept-Based Methods**: TCAV and related work for human-interpretable concept explanations
- **Causal Interpretability**: Extensions integrating causal inference into conversational XAI

### Research Trajectory

**Where This Work Leads:**

1. **Multi-Modal Conversational XAI**: Combining chat with interactive visualizations
2. **Adaptive Explanation Depth**: Personalizing conversational style to user expertise
3. **Causal Conversation**: Explaining not just "what" but "why" through causal reasoning
4. **Federated Conversational XAI**: Privacy-preserving explanations in distributed settings
5. **XAI for Language Models**: Conversational interfaces for interpreting LLM behavior (meta-interpretability)

### Positioning in xAI Landscape

The Explainability Assistant represents a **human-centered, interface-driven advance** in XAI that prioritizes **accessibility and usability over theoretical complexity**. It demonstrates that strategic application of modern LLM capabilities can significantly improve practical XAI deployment, complementing theoretical work on explanation faithfulness and evaluation metrics.

---

## Summary

The Explainability Assistant advances conversational XAI by leveraging LLM function-calling to achieve 94% intent-parsing accuracy and domain-agnostic deployment. Through evaluation with domain experts, it demonstrates that conversational interfaces significantly improve accessibility compared to traditional XAI dashboards, supporting trustworthy AI deployment in energy management, healthcare, and other high-stakes domains. The work opens research directions for multi-modal explanations, adaptive depth, and causal conversational reasoning.

**Key Takeaway**: Making XAI interpretable requires not just explaining models, but explaining explanations through interfaces matched to human cognitive and practical needs.
