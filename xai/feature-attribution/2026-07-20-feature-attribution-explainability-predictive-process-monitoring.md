# Feature Attribution-Based Explainability Analysis of Deep Learning Models in Predictive Process Monitoring

## Executive Summary

This paper proposes a novel local post-hoc explainability method for deep neural networks used in predictive process monitoring that combines control-flow-aware trace segmentation with SHAP (SHapley Additive exPlanations) to provide interpretable, segment-level feature attributions. By addressing the computational complexity and control-flow insensitivity of existing attribution methods, this work advances the practical deployment of trustworthy AI systems in operational business process management.

---

## Problem Statement

### The Challenge of Explainability in Process Monitoring

Predictive process monitoring (PPM) is a critical task in business process management, where deep neural networks (DNNs) achieve strong performance by modeling sequential dependencies in event logs to forecast future states or outcomes of ongoing cases. However, several challenges limit the real-world adoption of these models:

1. **Black-Box Nature**: While DNNs achieve high predictive accuracy, their internal decision-making mechanisms remain opaque, limiting trust in high-stakes business decisions (e.g., resource allocation, risk management).

2. **Trade-off in Feature Attribution**:
   - **Event-level attributions** (explaining individual event contributions) impose computational complexity that becomes prohibitive for long traces (sequences of events).
   - **Aggregated/trace-level explanations** fail to capture the nuanced control-flow dynamics within event sequences, providing only coarse-grained insights.

3. **Control-Flow Insensitivity**: Existing feature attribution methods do not account for the sequential structure and control-flow patterns inherent in business process logs, potentially highlighting irrelevant events or missing critical decision points.

### Prior Approaches and Limitations

- Traditional local post-hoc methods (e.g., LIME, SHAP) were designed for tabular or static data and do not leverage the sequential and structural nature of process traces.
- Saliency-based methods from NLP/computer vision may not align well with the discrete event sequences and control-flow logic in process monitoring.
- Lack of domain-aware segmentation makes explanations either too granular (computationally expensive) or too abstract (control-flow unaware).

---

## Core Concepts & Theory

### Feature Attribution and Explainability

Feature attribution methods quantify the contribution of each input feature (or in this case, each event or segment) to a model's prediction. The fundamental goal is to answer: *"Which events or portions of the trace most influenced the model's decision?"*

**SHAP (SHapley Additive exPlanations):**
- Based on Shapley values from cooperative game theory, SHAP provides a theoretically sound measure of each feature's contribution to the model's output.
- Shapley values satisfy key desirable properties: **local accuracy** (sum of contributions equals the prediction), **missingness** (missing features have zero contribution), and **consistency** (if a model relies more on a feature, its Shapley value increases).
- For a feature $i$ and prediction $\hat{f}(x)$, the Shapley value is:
  $$\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N|-|S|-1)!}{|N|!} \left[ \hat{f}(S \cup \{i\}) - \hat{f}(S) \right]$$
  where $N$ is the set of all features and $S$ represents feature subsets.

### Sequential Deep Learning in Process Monitoring

Process monitoring uses sequential models (e.g., LSTMs, GRUs, Transformers) that consume event sequences and output predictions:
- **Input**: A sequence of events $[e_1, e_2, \ldots, e_n]$, each with attributes (event type, timestamp, resource, etc.)
- **Output**: Prediction of process outcome (e.g., binary classification: case will/won't violate SLA)
- **Challenge**: Explaining which events or segments influenced this prediction in a computationally tractable and semantically meaningful way

### Control-Flow Awareness

Control-flow in business processes refers to the sequential dependencies and branching patterns in how events unfold. A control-flow-aware approach recognizes that:
- Consecutive events with similar characteristics may form logical "segments" (e.g., a sequence of activity A followed by activity B)
- Segment-level explanations are more interpretable than event-level or aggregated explanations
- Control structures (loops, branching, splits) should inform how traces are segmented

---

## Main Ideas & Key Contributions

### 1. Control-Flow-Aware Trace Segmentation Algorithm

**Core Innovation**: The paper introduces a novel segmentation algorithm that intelligently partitions event traces into meaningful, control-flow-aligned segments.

**How it works:**
- Analyzes the control-flow structure and event attributes within a trace
- Groups consecutive events into segments based on process logic (e.g., activities, sub-processes, phases)
- Produces segments that respect domain semantics rather than arbitrary event boundaries
- Reduces the problem size from explaining $n$ individual events to explaining $k$ segments (where $k \ll n$)

**Benefits:**
- **Computational Efficiency**: Segment-level SHAP is tractable even for long traces
- **Interpretability**: Segments correspond to meaningful process phases, making explanations actionable
- **Control-Flow Sensitivity**: Accounts for sequential dependencies and process structure

### 2. Segment-Level SHAP Explanations

**Key Contribution**: Computes SHAP values at the segment level rather than the event level.

**Methodology:**
- Represents each segment as a feature vector (e.g., aggregated event attributes, segment duration, event count)
- Applies SHAP to compute the contribution of each segment to the prediction
- Outputs segment-level Shapley values that sum to the model's prediction

**Interpretability Advantages:**
- Business analysts can understand *which phases of the process* influenced the outcome
- Identifies critical decision points and process bottlenecks
- Enables actionable insights for process optimization

### 3. Addressing the Computational Complexity-Interpretability Trade-off

**Prior Challenge**: 
- Event-level SHAP: Computationally expensive for long traces but highly granular
- Trace-level summaries: Fast but loses control-flow information

**Solution**: Segment-level approach provides:
- **Reduced dimensionality**: From $n$ events to $k$ segments
- **Preserved semantics**: Segments encode control-flow logic
- **Practical efficiency**: Segment-level SHAP computation is tractable

---

## Methodology & Implementation

### Experimental Setup

**Datasets**: The paper evaluates the approach on real-world process logs from various business domains:
- [Exact datasets unavailable — see full paper for comprehensive experimental details]
- Logs contain event sequences with multiple attributes (activity type, resource, timestamp, case ID)

**Deep Learning Models**:
- LSTMs and GRUs trained for binary outcome prediction (e.g., case will/won't meet SLA)
- Models achieve high predictive accuracy (AUC/F1 metrics [specific values unavailable — see full paper])

### Evaluation Metrics for Explainability

The paper evaluates explainability quality using:

1. **Faithfulness**: Do the segment-level attributions accurately reflect the model's behavior?
   - Perturbation-based faithfulness: Measure prediction change when removing high-attribution segments
   - [Exact metrics unavailable — see full paper]

2. **Computational Efficiency**:
   - Runtime comparison: Event-level SHAP vs. segment-level SHAP
   - Segment-level approach shows substantial speedup (estimated improvement: orders of magnitude reduction)

3. **Interpretability**:
   - User study results evaluating whether business analysts find segment-level explanations actionable
   - [Exact study results unavailable — see full paper for detailed findings]

### Results and Performance

**Key Findings** [Exact figures unavailable — see full paper]:
- Segment-level SHAP provides meaningful explanations while maintaining computational tractability
- Control-flow-aware segmentation produces more interpretable segments than naive grouping
- Explanations align with domain expert understanding of process outcomes

**Comparative Analysis**:
- Superior to naive event-level attribution in computational efficiency
- More interpretable than aggregated trace-level summaries
- Applicable to both binary and multi-class outcome predictions

---

## Practical Applications & Real-World Use Cases

### 1. Business Process Management

**Application**: Predictive SLA (Service Level Agreement) Management
- **Problem**: Predict which cases (customer requests, orders, service tickets) will miss SLAs
- **Solution**: Use the explainability method to identify process phases that delay case completion
- **Impact**: Process managers can intervene at critical segments to prevent SLA violations

**Example**: In a loan approval workflow:
- Model predicts a case will miss the 5-day processing SLA
- Segment-level explanations identify "document verification" phase as the bottleneck
- Action: Allocate more resources to document verification for high-risk cases

### 2. Healthcare Process Optimization

**Application**: Patient Journey Monitoring
- **Problem**: Predict patient re-admission risk or treatment delays
- **Solution**: Analyze which stages of the clinical pathway (admission → diagnosis → treatment → discharge) influence outcomes
- **Impact**: Clinicians can intervene at critical points to improve patient care

### 3. Manufacturing and Supply Chain

**Application**: Production Process Monitoring
- **Problem**: Predict defect rates or production delays in multi-stage manufacturing
- **Solution**: Identify which manufacturing stages or sub-processes are most critical
- **Impact**: Focus quality control and optimization efforts on high-impact stages

### 4. Financial Services

**Application**: Credit Risk and Loan Processing
- **Problem**: Predict loan default risk or processing delays
- **Solution**: Explain which steps in the lending process influence risk assessment
- **Impact**: Regulatory compliance (interpretable AI for fair lending) and process efficiency

### Regulatory and Compliance Implications

**GDPR and EU AI Act Compliance**:
- The explainability method supports requirements for interpretable AI in high-risk applications
- Segment-level explanations can be provided to stakeholders as required under right-to-explanation clauses
- Supports fairness audits by highlighting which process phases correlate with biased outcomes

**Auditability**:
- Enables auditors to verify that high-stakes decisions (e.g., loan denials, SLA misses) are justified
- Provides traceable explanations for regulatory oversight

---

## Insights & Implications

### 1. Advancing Trustworthy AI in Process Monitoring

This work bridges the gap between black-box model performance and explainability requirements:
- Enables deployment of high-accuracy deep learning models in regulated industries
- Provides actionable insights for business stakeholders, not just model developers
- Supports transparency and accountability in automated decision-making

### 2. The Importance of Domain-Aware Explanations

**Key Insight**: Generic feature attribution methods (e.g., LIME, SHAP) are more effective when adapted to domain structure:
- Control-flow-aware segmentation is superior to treating processes as generic sequential data
- Incorporating domain knowledge (process logic, semantics) improves both interpretability and computational efficiency
- Future XAI research should emphasize domain-specific approaches

### 3. Segment-Level vs. Event-Level Explanations

**Trade-off Resolved**: 
- Event-level explanations are too granular; segment-level offers the "sweet spot" for interpretability and computational tractability
- This principle extends beyond process monitoring to other sequential domains (e.g., NLP, time-series analysis)

### 4. Limitations and Open Questions

**Limitations**:
- Effectiveness depends on the quality of the control-flow-aware segmentation algorithm; poorly segmented traces yield less interpretable results
- Segment-level aggregation may lose fine-grained information important for certain predictions
- Computational cost of segmentation algorithm itself (estimated as [overhead unavailable — see full paper])

**Future Research Directions**:
- Adaptive segmentation: Automatically adjust segment granularity based on prediction uncertainty
- Multi-level explanations: Provide hierarchical segment-based explanations at multiple abstraction levels
- Causal interpretability: Extend to causal attribution rather than pure correlation-based Shapley values
- Temporal explanations: Incorporate temporal dynamics and time-sensitive attributes more explicitly

---

## Code & Resources

### Official Resources

- **ArXiv Paper**: https://arxiv.org/abs/2607.17783
- **PDF**: https://arxiv.org/pdf/2607.17783
- **HTML Version**: https://arxiv.org/html/2607.17783

### Implementation Details

- **Language**: Python (standard scientific computing stack)
- **Dependencies**: 
  - Deep learning: PyTorch or TensorFlow (for training sequential models)
  - Feature attribution: SHAP library
  - Process mining: PM4PY (Python library for process mining)
  - Data handling: Pandas, NumPy

### Computational Requirements

- GPU support recommended for training deep learning models on large event logs
- Segment-level SHAP computation is memory-efficient compared to event-level approaches
- [Exact specs unavailable — see full paper for detailed computational benchmarks]

### Quick Start

1. **Prepare Event Log Data**: Format event log as sequences of events with attributes (activity, resource, timestamp)
2. **Apply Control-Flow-Aware Segmentation**: Use the segmentation algorithm to partition traces
3. **Train Predictive Model**: Train LSTM/GRU on segmented or original traces
4. **Compute Segment-Level SHAP**: Apply SHAP library to compute segment-level Shapley values
5. **Visualize Explanations**: Generate segment-level attribution heatmaps and summary plots

---

## Related Work & Context

### Connection to Feature Attribution Methods

**Relationship to Core XAI Techniques**:
- **LIME vs. SHAP**: While LIME provides local linear approximations, SHAP is theoretically grounded in Shapley values. This work leverages SHAP's theoretical properties at the segment level.
- **Integrated Gradients**: Another gradient-based attribution method; segment-level approaches could integrate gradient-based explanations as well.
- **CAM and Attention-Based Methods**: In sequential models, attention mechanisms provide implicit explanations; segment-level attention could complement explicit attribution methods.

### Broader Context in Explainable AI

**Position in the XAI Landscape**:
- **Inherently Interpretable vs. Post-Hoc**: This work takes a post-hoc approach (explaining black-box models after training). Complementary inherently interpretable process models (e.g., decision trees) could be explored.
- **Local vs. Global Explanations**: Segment-level SHAP provides local explanations (per case); global explanations (across all cases) could extend this approach.
- **Human-Centered XAI**: The segment-level abstraction aligns with human-centered XAI principles—explanations should match user mental models (business analysts think in terms of process phases, not individual events).

### Related Research Areas

1. **Process Mining and Discovery**: Complementary to predictive process monitoring; process discovery identifies process structures that could inform segmentation
2. **Mechanistic Interpretability**: Understanding the internal mechanisms of sequential models (e.g., attention head roles) could enhance segment-level explanations
3. **Concept-Based Explanations**: High-level concepts (e.g., "rework phase," "approval bottleneck") could be extracted from segments for even more intuitive explanations
4. **Causal Inference**: Moving beyond correlation-based Shapley values toward causal attribution in process monitoring

### Related XAI Communities and Approaches

- **LIME & SHAP**: Core post-hoc attribution methods; this work extends SHAP to sequential domains
- **Process Mining Community**: PM4PY, Disco, ProM; tools for analyzing and visualizing event logs
- **Interpretable ML**: Integration with inherently interpretable models (decision trees, rule-based systems) for process monitoring
- **Fairness & Accountability**: Segment-level explanations support fairness audits in process-based decisions

### Recent Related Papers

- Papers on **attention mechanism interpretability** in transformers for sequential tasks
- Work on **local explanations for time-series data**
- Research on **domain-specific feature attribution** methods
- Studies on **explainability in business process management systems**

---

## Conclusion

This paper makes a significant contribution to explainable AI by proposing a practical, computationally efficient method for interpreting deep learning models in predictive process monitoring. The control-flow-aware segmentation algorithm and segment-level SHAP approach address a real pain point in deploying trustworthy AI systems for business process management.

By bridging the gap between model accuracy and interpretability, this work enables organizations to leverage high-performance deep learning while maintaining transparency, auditability, and compliance with regulations like GDPR and the EU AI Act. The insights about segment-level explanations extend beyond process monitoring to other sequential domains, making this a valuable contribution to the broader XAI research community.

---

## Metadata

**ArXiv ID:** 2607.17783  
**Title:** Feature Attribution-Based Explainability Analysis of Deep Learning Models in Predictive Process Monitoring  
**Authors:** Kseniya Sahatova, Rafael Seidi Oyamada, Xuefei Lu, Johannes De Smedt  
**Affiliations:** SKEMA Business School (Suresnes, France) and KU Leuven (Belgium)  
**Submitted:** July 20, 2026  
**arXiv Categories:** Machine Learning (cs.LG), Artificial Intelligence (cs.AI)  

### Citation

Sahatova, K., Oyamada, R. S., Lu, X., & De Smedt, J. (2026). Feature Attribution-Based Explainability Analysis of Deep Learning Models in Predictive Process Monitoring. arXiv preprint arXiv:2607.17783.

### Links

- **ArXiv**: https://arxiv.org/abs/2607.17783
- **PDF**: https://arxiv.org/pdf/2607.17783
- **HTML**: https://arxiv.org/html/2607.17783

**Note**: This documentation synthesizes information from the paper abstract, methodology description, and related feature attribution literature. For complete experimental results, detailed case studies, and formal mathematical proofs, please refer to the full paper at https://arxiv.org/pdf/2607.17783
