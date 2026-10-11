# Seeing through the Eyes of AI: Situated Explainability in Augmented Reality

**ArXiv ID:** [2610.03232](https://arxiv.org/abs/2610.03232)

**Authors:** Ana Stanescu, Lucchas Ribeiro Skreinig, Tobias Langlotz, Stefanie Zollmann, Peter Mohr, Dieter Schmalstieg, Mark Billinghurst, Denis Kalkofen

**Submitted:** 2 October 2026

## Executive Summary

This paper proposes **situated explainability**, a novel human-centered approach to presenting AI explanations directly in the user's physical workspace using Augmented Reality (AR) rather than on traditional 2D screens. By overlaying real-time saliency maps and activation heatmaps on objects in the user's environment, the work addresses a critical gap in XAI: eliminating the cognitive burden of mentally mapping abstract explanations back to real-world objects. A user study demonstrates that AR-based situated explainability significantly enhances user engagement and preference compared to traditional explainability tools, advancing the intersection of human-computer interaction and interpretable AI.

## Problem Statement

Traditional explainable AI approaches face a critical usability challenge: explanations are typically presented on 2D displays using pre-recorded or static data, forcing users to mentally construct a mapping between the explanation artifacts and real-world objects or scenes. This creates several problems:

1. **Cognitive overhead**: Users must cognitively match explanations (often abstract heatmaps or saliency maps) back to physical objects they're observing
2. **Context loss**: Pre-recorded data lacks the dynamic, real-time context of an active exploration scenario
3. **Reduced engagement**: Static, screen-based explanations feel disconnected from the actual decision-making process
4. **Limited practical applicability**: Many real-world use cases (quality control, medical diagnostics, autonomous systems) benefit from understanding AI decisions *in situ*

Existing XAI methods (LIME, SHAP, saliency maps, attention visualizations) are sophisticated but remain bound to post-hoc, offline presentation paradigms. The paper argues that the next evolution in XAI should move beyond explaining post-hoc and instead integrate explanations into the user's immediate visual environment.

## Core Concepts & Theory

### Situated Cognition and Explainability

The paper grounds its approach in **situated cognition** — the principle that learning and understanding are anchored in the physical and social context in which they occur. Applying this to XAI:

- **Grounded explanations**: Explanations are anchored directly to the objects they describe, eliminating abstract-to-reality mapping
- **Real-time interactivity**: Users can explore objects and immediately see how the AI model perceives them, enabling dynamic understanding
- **Context-aware presentation**: The spatial context of the AR environment naturally conveys relationships and dependencies

### Explainability Methods in AR

The authors apply established XAI techniques to AR rendering:

1. **Saliency Maps**: Visualize which image regions most influence the model's decision
   - Rendered as heat maps overlaid on detected objects
   - Color intensity corresponds to feature importance (e.g., red for high importance, blue for low)

2. **Activation Heatmaps**: Show where the model's internal feature detectors activate
   - Reveal which object regions trigger the network's neurons
   - Useful for understanding what the model "sees" versus what humans see

3. **Comparative Visualization**: Overlay explanations across multiple objects to reveal confusion patterns
   - Example: when a detector confuses a can of beans with pet food, display both objects side-by-side with their respective activation weights
   - Reveals model biases and brittleness

### Technical Architecture

The implemented system uses:
- **AR Headset** (Microsoft HoloLens-style): Captures live video, displays overlaid visualizations
- **Desktop Server**: Runs real-time deep learning inference using standard frameworks
- **Streaming Pipeline**: Headset streams frames to the server; server computes explanations (saliency maps, heatmaps) and sends visualizations back to the headset
- **Visualization Layer**: AR app renders heat maps and saliency overlays directly on detected objects in the user's workspace

The architecture ensures real-time responsiveness, a critical requirement for user engagement in interactive AR exploration.

## Main Ideas & Key Contributions

### 1. **Situated Explainability Paradigm**

The paper's central contribution is articulating and demonstrating **situated explainability** — a new paradigm for presenting AI explanations that:
- Places explanations in the user's immediate spatial context (not on a separate screen)
- Updates explanations in real time as the user explores their environment
- Leverages the physicality of AR to eliminate abstract-to-reality cognitive mapping

This represents a conceptual shift: from "here's the explanation for the decision" (offline, post-hoc) to "here's what the AI sees as you explore" (online, situated).

### 2. **Practical Implementation & Real-time Integration**

The authors demonstrate that established XAI methods can be integrated into an AR workflow without fundamentally changing the methods themselves. The key innovation is architectural (real-time inference on a server, streaming back visualizations) and presentational (overlaying explanations on objects in situ).

### 3. **User Experience Insights**

The user study reveals nuanced findings:
- **Engagement**: AR-based situated explainability is significantly more engaging than traditional screen-based approaches
- **Preference**: Participants strongly preferred situated explainability, finding it more intuitive and aligned with their exploration process
- **Cognitive Workload Trade-off**: While participants found AR explanations more engaging, they also reported higher cognitive workload compared to traditional tools. This trade-off suggests that situated explainability demands more active interpretation but yields deeper understanding and stronger preference.

### 4. **Connection to Trustworthy AI**

By presenting explanations in context, situated explainability can contribute to building trust:
- Users can directly observe the model's behavior and reasoning in real-world scenarios
- The situated presentation makes explanation faithfulness more apparent (users see if the heatmap aligns with actual object features)
- Interactive exploration enables discovery of failure modes and biases in situ

## Methodology & Implementation

### Experimental Setup

- **Platform**: Augmented Reality headset (similar to Microsoft HoloLens)
- **Models tested**: Vision models trained for object detection (specifics: [Exact figures unavailable — see full paper])
- **XAI methods applied**:
  - Saliency maps (gradient-based, e.g., Integrated Gradients or similar)
  - Activation heatmaps (feature visualization)
  - Comparative overlays for confusion analysis

### Evaluation Metrics & User Study

The paper includes a user study with AI-background participants to evaluate situated explainability. Key findings:

| Metric | Finding |
|--------|---------|
| **Engagement** | AR-based approach significantly more engaging than traditional 2D tools |
| **User Preference** | Participants strongly preferred situated explainability |
| **Cognitive Workload** | Higher cognitive workload in AR (estimated/approximate) but justified by preference and engagement |
| **Understanding** | Participants reported better intuitive understanding of model decisions when explanations were situated |

Sample size and detailed statistical analysis: [Exact figures unavailable — see full paper]

### Key Results & Observations

1. **Visualization Clarity**: Heat maps and saliency overlays are clearly visible and interpretable when placed directly on objects
2. **Real-time Performance**: The streaming architecture maintains acceptable latency for real-time exploration
3. **Confusion Detection**: The comparative visualization approach effectively reveals which objects the model confuses (e.g., beans vs. pet food cans)
4. **Participant Feedback**: Qualitative feedback emphasized the naturalness of exploring explanations in context

### Limitations

1. **Cognitive Workload**: The situated approach increases cognitive load, which may not suit all use cases
2. **Scalability**: Real-time server-side inference may not scale to very large models or high video frame rates
3. **AR Hardware Requirements**: Requires AR headset hardware, limiting accessibility compared to screen-based tools
4. **Participant Demographics**: User study involved AI-background participants; generalization to non-technical users unclear
5. **Model Coverage**: Evaluation focused on vision tasks; applicability to other domains (NLP, time series) requires further research

## Practical Applications & Real-World Use Cases

### 1. **Manufacturing & Quality Control**
- AR operators inspect products on assembly lines while AI flags defects
- Real-time saliency maps show exactly which features triggered defect detection
- Enables rapid verification and corrects of false positives

### 2. **Medical Imaging & Diagnostics**
- Radiologists use AR to view medical scans (X-ray, CT) with AI-detected abnormalities highlighted in situ
- Real-time explanations show which image regions the AI model found suspicious
- Supports collaborative human-AI decision-making in high-stakes diagnostics

### 3. **Autonomous Systems & Robotics**
- AR headsets for robot operators overlay the robot's visual perception and decision reasoning
- Operators see in real-time what the robot perceives and why it's making decisions
- Critical for understanding and trusting autonomous systems in safety-critical scenarios

### 4. **Security & Surveillance**
- Security operators use AR displays to see real-time AI alerts (person detection, anomaly detection, etc.)
- Heat maps show exactly which video regions triggered alerts
- Reduces false alarms and improves operator confidence

### 5. **Accessible AI for Non-Technical Users**
- Situated explainability can make AI reasoning more intuitive for non-experts
- Instead of abstract saliency maps, users see direct visual feedback on objects they're observing

### Regulatory & Compliance Implications

- **GDPR & AI Act**: EU regulations increasingly require explainability. Situated explainability provides transparent, verifiable explanations in context
- **FDA Requirements**: Medical device developers may leverage AR explanations to demonstrate AI interpretability in regulatory submissions
- **Workplace Safety**: AR-based explanations can satisfy transparency requirements in safety-critical industries (autonomous systems, industrial automation)

### Implementation Challenges

1. **Hardware accessibility**: AR headsets remain expensive and not ubiquitous; adoption depends on infrastructure investment
2. **Real-time inference**: Requires backend compute resources; may not be feasible for extremely large models
3. **User training**: Operators need training to effectively interpret AR visualizations
4. **Privacy concerns**: Streaming video to a backend server raises privacy questions; local inference or edge computing mitigates this
5. **Standardization**: AR visualization conventions for XAI are not yet standardized; each application must design custom visualizations

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Context as a Foundation for Trust**: This work demonstrates that context fundamentally shapes how users interpret and trust explanations. Situated explanations reduce the gap between model behavior and human understanding.

2. **Redefining "Interpretability"**: Rather than asking "can we explain a model's decision?" (post-hoc), situated explainability asks "can we help users understand what the model sees as it operates?" This reframing is more aligned with real-world use cases.

3. **The Role of Interaction**: By enabling real-time, exploratory interaction with explanations, the work highlights that interpretability is not just about passive consumption of explanations but active exploration and discovery.

4. **Human-AI Collaboration**: Situated explainability supports genuine human-AI collaboration by making the AI's reasoning visible and interrogable in the moment.

### State-of-the-Art Advancement

This paper advances the intersection of:
- **Human-Centered XAI**: Moving from passive explanation consumption to active, situated understanding
- **AR/VR for AI**: Demonstrating practical use of immersive technologies for AI transparency
- **Real-time XAI**: Showing that real-time, on-the-fly explanations are feasible and valuable

### Limitations & Open Questions

1. **Cognitive Workload Trade-off**: Higher cognitive workload in AR may limit adoption; future work should optimize this trade-off
2. **Generalization**: Does situated explainability work equally well for all types of AI models (e.g., LLMs, time-series models)?
3. **Long-term Effectiveness**: Does the preference for AR explanations persist over extended use, or does novelty wear off?
4. **Accessibility**: How can situated explainability be designed to be accessible to users with disabilities?

### Future Research Directions

1. **Extended Reality (XR) Integration**: Explore VR and mixed reality for even richer explanation experiences
2. **Multi-modal Explanations**: Combine visual explanations with audio, haptic, or textual cues for different user preferences
3. **Intelligent Visualization Adaptation**: Use user feedback to automatically adjust visualization complexity and presentation style
4. **Longitudinal Studies**: Study how situated explainability affects trust and decision-making over extended periods
5. **Cross-domain Applications**: Extend to NLP (e.g., AR-based explanation of language model decisions), audio (e.g., speech recognition), and other domains

## Code & Resources

### Official Implementation

- **GitHub**: [Exact repository link unavailable — see full paper]
- **ArXiv Version**: [arXiv:2610.03232](https://arxiv.org/abs/2610.03232)
  - HTML version: [https://arxiv.org/html/2610.03232](https://arxiv.org/html/2610.03232)
  - PDF version: [https://arxiv.org/pdf/2610.03232](https://arxiv.org/pdf/2610.03232)

### Dependencies & Requirements

- **AR Hardware**: Microsoft HoloLens or compatible AR headset
- **Deep Learning Framework**: PyTorch or TensorFlow (for inference)
- **Vision Models**: Pre-trained object detection models (YOLO, Faster R-CNN, or similar)
- **XAI Libraries**: 
  - For saliency maps: Captum, TensorFlow XAI, or custom gradient-based methods
  - For activation visualizations: Feature visualization libraries
- **AR Development**: Unity or similar AR development platform for headset integration
- **Server**: Backend server capable of running real-time inference (GPU-accelerated recommended)

### Quick Start (Conceptual)

1. **Set up AR headset** with webcam streaming capability
2. **Deploy inference server** with vision model and XAI methods
3. **Implement streaming pipeline**: Headset → server (video frames) → explanations → headset (visualizations)
4. **Configure visualization layer**: Map saliency/activation heatmaps to detected objects in AR space
5. **Optimize latency**: Tune model and server performance for real-time responsiveness

### Interactive Visualizations & Demos

- [Exact demo link unavailable — see full paper for supplementary materials]
- The paper includes video examples of AR visualization in action (embedded in HTML version)

## Related Work & Context

### Related Explainability Papers

1. **[Beyond Explainable AI (XAI): An Overdue Paradigm Shift](https://arxiv.org/abs/2602.24176)** (arXiv:2602.24176)
   - Critiques traditional post-hoc XAI approaches; this work aligns with the call for new paradigms by demonstrating a practical alternative

2. **[Radical AI Interpretability](https://arxiv.org/abs/2606.26523)** (arXiv:2606.26523)
   - Proposes philosophical frameworks for AI interpretation; this work applies interpretability in practical AR contexts

3. **[Explainable AI: Learning from the Learners](https://arxiv.org/abs/2601.05525)** (arXiv:2601.05525)
   - Emphasizes causal reasoning in explainability; situated explanations enable direct observation of causality

### Human-Centered XAI Context

This work builds on growing literature in human-centered XAI:
- User studies on saliency map effectiveness (Evaluating saliency-based XAI methods)
- HCI perspectives on explanation design
- Interactive visualization for machine learning understanding

### AR/XR for AI

The paper extends early work on using immersive technologies for AI understanding and sits at the intersection of:
- **Augmented Reality for Visualization**: AR for data visualization and exploration
- **Explainable Human-Robot Interaction**: AR for understanding robot decisions
- **Immersive Analytics**: Using VR/AR to explore high-dimensional data and model behavior

### Connection to Broader XAI Communities

1. **LIME & SHAP Community**: This work applies these local explanation methods in a new (situated AR) presentation paradigm
2. **Saliency Map Research**: Extends the practical utility of saliency maps by embedding them in real-time, spatial contexts
3. **Mechanistic Interpretability**: While focused on post-hoc methods, the work's emphasis on real-time, interactive exploration aligns with mechanistic interpretability's goals of understanding model internals
4. **Fairness & Transparency**: AR-based situated explanations support fairness auditing and transparency in high-stakes AI applications

### Where This Research Leads Next

1. **Multimodal Explainability**: Extend to NLP, audio, and other modalities using equivalent immersive presentation paradigms
2. **Automated Explanation Design**: Use machine learning to optimize how explanations are visualized and presented in AR
3. **Collaborative AI Systems**: Design AR interfaces that support collaborative decision-making between humans and AI
4. **Trustworthiness at Scale**: Study how situated explainability scales to very large, complex models (foundation models, multi-modal transformers)

## Related ArXiv Papers

- [Situated Brushing and Linking in Virtual and Augmented Reality](https://arxiv.org/abs/2602.02023) — Interactive visualization in AR
- [Explainable Human-Robot Training and Cooperation with Augmented Reality](https://arxiv.org/abs/2302.01039) — AR for robot interpretability
- [TOM: A Development Platform For Wearable Intelligent Assistants](https://arxiv.org/abs/2407.15523) — AR platforms for AI assistants
- [See What I Mean? Mobile Eye-Perspective Rendering for Optical See-through Head-mounted Displays](https://arxiv.org/abs/2509.11653) — AR display technologies

## Key Takeaways

1. **Situated explainability** is a promising new paradigm for presenting XAI in real-world contexts
2. **AR provides a natural medium** for integrating AI explanations into users' physical environment
3. **Real-time interactivity** enhances engagement and preference, though with a cognitive workload trade-off
4. **Practical feasibility** is demonstrated through a working system and user study
5. **Broad applicability** across quality control, medical imaging, robotics, security, and other domains where AI decisions require transparency in situ
6. **Future directions** include multimodal extensions, automated visualization design, and integration into collaborative AI systems
