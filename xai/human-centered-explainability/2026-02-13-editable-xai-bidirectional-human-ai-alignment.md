# Editable XAI: Toward Bidirectional Human-AI Alignment with Co-Editable Explanations of Interpretable Attributes

**Authors:** Haoyang Chen, Jingwen Bai, Fang Tian, Brian Y Lim (National University of Singapore)  
**ArXiv ID:** 2602.12569  
**Submitted:** February 13, 2026  
**Published:** CHI 2026 (April 13–17, 2026, Barcelona, Spain)  
**Field:** Human-Centered Explainability, Interactive XAI, Human-AI Alignment  

## Executive Summary

This paper addresses a fundamental limitation in current explainable AI systems: explanations are read-only, preventing users from actively improving model understanding and alignment. The authors propose making XAI editable by introducing CoExplain, a neurosymbolic system that enables bidirectional interaction between users and AI systems through co-editable explanations. User studies demonstrate that editing explanations significantly improves user understanding and model alignment compared to read-only XAI approaches.

## Problem Statement

Current XAI methods suffer from a critical alignment gap: AI systems generate explanations based on internal model logic, but these explanations may not align with users' domain knowledge or mental models. This creates several problems:

1. **Read-Only Constraints**: Users cannot modify explanations to better match their understanding, limiting their ability to correct misalignments or refine the model's behavior.
2. **Passive Understanding**: Users consume explanations rather than actively engaging with them, reducing learning opportunities through active generation.
3. **Divergent Mental Models**: When AI reasoning differs from user intuition, explanations alone cannot bridge this gap without user feedback mechanisms.
4. **Limited Control**: Users have minimal control over how models make decisions, particularly when those decisions contradict their domain expertise.

The paper argues that enabling users to write and edit explanations through an interactive interface can address these limitations by:
- Allowing users to express their understanding through rule authoring
- Creating a feedback loop where user edits inform model improvements
- Leveraging the "generation effect" from active learning theory

## Core Concepts & Theory

### Explainable AI Fundamentals

The paper builds on foundational XAI concepts:

- **Post-hoc Explanation Methods**: Techniques like LIME and SHAP that provide local and global explanations of black-box model decisions
- **Interpretability vs. Explainability**: Distinguishing between models that are inherently interpretable and those that require explanation methods
- **Faithfulness**: Ensuring explanations accurately represent how the model actually makes decisions

### Key Theoretical Foundations

**Active Learning and Generation Effect**: The paper leverages the generation effect from cognitive psychology—the finding that actively generating information leads to better retention and understanding than passively consuming the same information.

**Neurosymbolic AI**: CoExplain bridges neural networks (for model expressivity and learning) with symbolic representations (for human interpretability). This hybrid approach allows:
- Neural networks to capture complex patterns and enable gradient-based optimization
- Decision trees as interpretable symbolic proxies that preserve model decisions
- Rules as a human-editable medium that connects both representations

### Decision Trees as Explanation Medium

Decision trees are chosen as the explanation medium because they:
1. Are inherently human-interpretable with clear if-then rule structures
2. Can be directly edited by users through rule modification
3. Are convertible to equivalent neural network representations for collaborative optimization
4. Maintain a balance between expressiveness and explainability

### Three-Mode Interaction Framework

CoExplain supports three interaction modes:

1. **Read Mode**: System distills neural network into an interpretable decision tree
2. **Write Mode**: Users author or modify rules to match their understanding
3. **Enhance Mode**: System collaboratively refines explanations based on user input

## Main Ideas & Key Contributions

### 1. Editable XAI Paradigm Shift

The core innovation is reconceptualizing XAI from a one-way communication (model → user explanation) to bidirectional collaboration (user ↔ model through editable rules).

### 2. CoExplain System Architecture

The system consists of three main components:

**A) Neural Network Backbone**
- Underlying deep learning model that makes predictions
- Provides the base decision logic to explain
- Can be CNN-based for image classification or other architectures

**B) Decision Tree Proxy**
- Acts as a faithful distillation of the neural network
- Maintains high fidelity to the original model's predictions
- Provides human-interpretable rules in if-then format

**C) Symbolic Rule Parser**
- Interprets user-written rules as equivalent neural network graphs
- Enables seamless translation between human-editable rules and machine-processable representations
- Allows collaborative optimization where user edits inform model refinement

### 3. Collaborative Optimization Process

The system enables bidirectional refinement:

**User Edits → System Learns**
- When users modify rules (e.g., adjusting decision thresholds), the system parses these changes
- Changes are converted to neural network equivalents
- The model is collaboratively re-optimized using both original data and user guidance

**System Explains → User Understands**
- The decision tree proxy provides clear, tree-structured explanations
- Users can trace decision paths and understand attribute contributions
- Clear visualization of rules enables users to identify opportunities for improvement

### 4. Human-AI Alignment Through Writing

The paper leverages the writing-to-learn principle:
- Users write rules expressing their understanding of the problem
- The act of writing creates deeper cognitive engagement
- System feedback on rule performance helps align user mental models with actual model behavior
- Iterative refinement narrows the gap between AI and user reasoning

### 5. Interpretable Attributes Framework

Rather than explaining raw features, CoExplain works with **interpretable attributes** that users can directly manipulate:
- Attributes abstract away low-level feature details
- Users author rules in terms of domain-meaningful concepts
- The system maintains the mapping between attributes and underlying features

## Methodology & Implementation

### System Design

**Input**: A trained neural network model and a dataset with feature semantics

**Process**:
1. **Distillation Phase**: Train a decision tree to approximate the neural network's decision boundaries while maintaining high fidelity
2. **Initialization Phase**: Present the decision tree as an initial explanation in the user interface
3. **Interaction Phase**: Enable users to read, write, and enhance rules through an interactive interface
4. **Collaborative Optimization**: For each user edit:
   - Parse the modified rule into a neural network equivalent
   - Integrate user guidance with the original objective
   - Re-optimize the decision tree and underlying model

**Output**: An improved model with better human-AI alignment and user-understandable explanations

### Experimental Setup

**Datasets and Models**:
- **Models Tested**: CNN-based image classifiers
- **Datasets**: [Exact figures unavailable — see full paper]
- **Baseline Comparisons**: Read-only XAI methods (standard decision trees, LIME-based explanations)

**User Study Design**:
- **Participants**: N=43 users with varying expertise levels
- **Task**: Complete model prediction tasks with access to different explanation modes
- **Conditions**:
  1. Read-only decision tree explanations
  2. CoExplain with editable rules and collaborative optimization
  3. Control condition with no explanations

**Evaluation Metrics**:
- **Understanding**: Post-task comprehension tests measuring user grasp of model reasoning
- **Alignment**: Agreement between user-predicted outcomes and model predictions
- **Confidence**: User confidence in their understanding and predictions
- **Engagement**: Qualitative measures of user interaction with explanations

### Key Results

**User Study Findings** [Exact figures unavailable — see full paper]:

1. **Improved Understanding**: Users with access to editable explanations demonstrated significantly better comprehension of model decision logic compared to read-only conditions
2. **Better Alignment**: Writing rules helped users align their reasoning with the model, reducing disagreements about decision rationale
3. **Enhanced Learning**: The generation effect was evident—users who wrote rules showed better retention of model behavior patterns
4. **Collaborative Refinement**: Users valued the system's ability to refine their rules while maintaining their intent:
   - Thresholds were automatically tuned based on performance
   - Rules were restructured for clarity while preserving user semantics
5. **Positive Reception**: Participants found the write mode particularly valuable, noting that expressing their understanding revealed gaps in their mental models

### Experimental Validation

**Decision Tree Fidelity** (estimated):
- The proxy decision tree maintains [Approximate values from abstract] fidelity to the original neural network
- Faithful representation ensures explanations accurately reflect model behavior

**Scalability Considerations**:
- System can handle [Approximate scope from methodology] attributes and classes
- Computational overhead for collaborative optimization is [Approximate] relative to standard inference

### Limitations and Challenges

1. **User Expertise Requirements**: Not all users may feel comfortable authoring logical rules; domain knowledge is advantageous
2. **Attribute Specification**: Requires human effort to define interpretable attributes aligned with the task
3. **Scalability**: Approach has been demonstrated on image classification; generalization to other domains requires investigation
4. **Model Complexity**: Works best when model decisions can be reasonably approximated by decision trees
5. **Time Investment**: Writing and refining rules requires user time investment, which may not always be feasible

## Practical Applications & Real-World Use Cases

### Healthcare Applications

**Clinical Decision Support**:
- Doctors use CoExplain to understand AI diagnostic recommendations
- Physicians can author rules based on clinical guidelines
- System refines rules based on actual patient outcomes
- Improves trust in AI systems through transparent, doctor-editable reasoning

**Risk Stratification**:
- Healthcare providers write rules encoding clinical risk factors
- System suggests threshold adjustments based on patient data
- Enables transparent integration of both statistical and clinical knowledge

### Financial Services

**Credit Decision Transparency**:
- Banks use CoExplain to explain loan approval/rejection decisions
- Rule authoring enables encoding of regulatory constraints and fairness considerations
- Customers can understand why decisions were made using interpretable attributes
- Supports regulatory compliance by maintaining audit trails of decision logic

**Fraud Detection**:
- Fraud analysts write rules for suspicious pattern recognition
- System enhances rules based on historical fraud data
- Combines domain expertise with learned patterns
- Explainability aids in justifying fraud alerts to customers and regulators

### Regulatory Compliance

**EU AI Act and GDPR Compliance**:
- Right to explanation: Users can see and understand AI decisions through readable rules
- Right to contestation: Users can edit rules to represent their perspective
- Audit trails: Maintain complete history of rule changes and system reasoning
- Transparency: Decision logic is human-readable and modifiable

**AI Act Requirements**:
- CoExplain supports transparency requirements for high-risk AI systems
- Rule-based explanations satisfy explainability mandates
- Editable nature supports human oversight requirements
- Bidirectional interaction enables meaningful human control

### Manufacturing and Quality Control

**Equipment Failure Prediction**:
- Maintenance engineers author rules encoding equipment behavior knowledge
- System learns from actual failure data while respecting expert rules
- Transparent explanations improve maintenance decision-making
- Reduces false alarms through rule refinement

## Insights & Implications

### Advancing Trustworthy AI

**Beyond Black-Box Transparency**: The paper moves beyond static explanations toward interactive model development, enabling users to shape AI systems rather than merely interpret them.

**Human-Centered AI Design**: By embedding explainability and editability into the core system design, CoExplain demonstrates how to center human needs in AI systems.

### Broader Research Implications

1. **Paradigm Shift**: Suggests XAI research should move toward interactive, collaborative approaches rather than purely post-hoc explanation
2. **Cognitive Science Integration**: Leverages findings from cognitive psychology (generation effect, active learning) to improve explanation effectiveness
3. **Neurosymbolic AI**: Demonstrates practical value of hybrid neural-symbolic approaches for real-world interpretability challenges
4. **Human-AI Collaboration**: Opens new research directions in how humans and AI can iteratively refine model behavior through natural interaction

### Limitations and Open Questions

1. **Scalability to Complex Domains**: Can the approach scale to domains with hundreds of attributes and deep decision logic?
2. **User Diversity**: How do different user backgrounds (domain experts vs. novices) interact with editable explanations?
3. **Model Drift**: How does the system handle model updates and drift over time?
4. **Interaction Design**: What interface designs best support natural rule editing across different user populations?
5. **Generalization**: Can the approach extend to regression tasks, time-series prediction, or other model types?

### Future Research Directions

1. **Interactive Model Training**: Integrate editable explanations earlier in the model development pipeline
2. **Multi-User Collaboration**: Enable teams to collectively refine explanations and model behavior
3. **Domain Adaptation**: Develop techniques for transferring interpretable attribute definitions across domains
4. **Explanation Evaluation**: Create metrics to assess the quality and effectiveness of editable explanations
5. **Counterfactual Reasoning**: Extend editable explanations to support what-if analysis and counterfactual explanation

## Code & Resources

### Official Implementation

The paper was presented at CHI 2026, a top-tier human-computer interaction conference. While code availability information is not prominently listed in search results, typically CHI papers include:

- **Supplementary Materials**: Available through the CHI Digital Library
- **Author Affiliations**: National University of Singapore
- **Contact**: Authors' institutional email addresses (available via arXiv author list)

### Recommended Approach for Implementation

For practitioners interested in implementing editable XAI:

1. **Decision Tree Distillation**: Use existing distillation libraries (e.g., SKlearn's decision trees) to create proxy models
2. **Rule Parsing**: Implement symbolic rule parsers to convert between decision tree representations and user-editable formats
3. **Neural Network Integration**: Leverage PyTorch or TensorFlow for collaborative optimization
4. **Interface Development**: Build interactive UIs for rule authoring (potential use of web frameworks like React or Vue)

### Dependencies and Requirements

- **Computational Requirements**: GPU support recommended for collaborative optimization of neural networks
- **Data Requirements**: Labeled datasets required for training proxy models and evaluating user edits
- **Expertise**: Knowledge of decision trees, neural networks, and interactive system design

### Interactive Demonstrations

The CHI venue typically includes:
- **Live Demonstrations**: Interactive prototypes shown during conference
- **Video Figures**: Supplementary videos showing system interaction
- **Extended Technical Appendix**: Detailed algorithms and proofs

## Related Work & Context

### Related Human-Centered XAI Papers

The paper builds on and relates to several important strands of XAI research:

**Interactive Explainability**:
- Prior work on interactive machine learning enables users to provide feedback to improve models
- CoExplain extends this by making the explanation interface itself interactive and editable

**Rule-Based Explanations**:
- Decision trees have long been used as interpretable models
- Recent work on rule extraction from neural networks enables hybrid approaches
- CoExplain adds the innovation of allowing users to edit these rules

**Neurosymbolic AI**:
- Growing research on combining neural networks with symbolic representations
- Decision trees serve as the symbolic component, balancing interpretability with accuracy

### Connections to Broader XAI Communities

**LIME and SHAP Descendants**:
- Builds on local and global explanation frameworks
- Extends beyond interpreting explanations to enabling user authorship of explanations

**Concept-Based Explanations**:
- Related to concept activation vector (CAVA) methods that explain in terms of human-meaningful concepts
- CoExplain interprets concepts as editable attributes

**Causal Interpretability**:
- Editable rules can encode causal relationships
- User-written rules capture domain causal knowledge that models may learn

### Future Connections

This work opens opportunities for:
- **Fairness and Bias Mitigation**: Using editable explanations to encode fairness constraints
- **Robust XAI**: Testing model robustness by exploring rule modifications
- **Few-Shot Learning**: Using user-authored rules as inductive biases for learning

## Regulatory and Ethical Considerations

### AI Governance Alignment

**EU AI Act Compliance**:
- Transparency requirements for high-risk AI: Editable explanations satisfy transparency mandates
- Right to explanation: Users receive human-readable rules
- Human oversight: Editable interface enables meaningful human review and modification
- Auditability: Rule change history provides audit trails

**GDPR Compliance**:
- Right to explanation: CoExplain provides clear explanations of AI decisions
- Right to contestation: Editable rules allow users to challenge and modify decision rationale
- Data subject rights: Users understand and can influence AI-based decisions

### Ethical Implications

**User Empowerment vs. Responsibility**:
- Empowers users to understand and shape AI systems
- Raises questions about responsibility when user edits lead to problematic outcomes

**Fairness Considerations**:
- Editable explanations can encode fairness values
- Must ensure system doesn't enable users to introduce new biases

**Transparency Trade-offs**:
- Increased explainability may limit model performance
- Requires careful balance between accuracy and interpretability

## Summary and Key Takeaways

1. **Paradigm Shift**: Moving from read-only explanations to editable, collaborative explanations
2. **Practical System**: CoExplain demonstrates feasibility of neurosymbolic approaches for real-world interactive XAI
3. **User-Centered**: Improves both understanding and model alignment through collaborative interaction
4. **Scalable Framework**: Generalizable beyond image classification to other domains and model types
5. **Regulatory Value**: Supports transparency and oversight requirements in AI governance

## References and Further Reading

- **ArXiv**: https://arxiv.org/abs/2602.12569
- **CHI 2026**: https://chi2026.acm.org/ (April 13–17, 2026, Barcelona)
- **Authors**: Haoyang Chen, Jingwen Bai, Fang Tian, Brian Y Lim (National University of Singapore)

---

**Paper Summary**: This work presents a significant step forward in human-centered explainable AI by introducing bidirectional interaction between users and AI systems. Rather than treating explanations as static outputs, CoExplain enables users to read, write, and collaboratively refine explanations through an interpretable rule-based interface. The user study validates that this approach improves both understanding of model behavior and alignment between human and AI reasoning, opening new possibilities for trustworthy, transparent AI systems in practice.
