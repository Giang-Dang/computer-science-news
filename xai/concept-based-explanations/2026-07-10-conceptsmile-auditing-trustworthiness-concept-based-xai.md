# ConceptSMILE: Auditing the Trustworthiness of Concept-Based Explainable AI

**ArXiv ID:** [2607.09649](https://arxiv.org/abs/2607.09649)

**Authors:** Mohadeseh Mollapour, Koorosh Aslansefat, Zeinab Dehghani, Bhupesh Kumar Mishra, Tejal Shah, Zhibao Mian

**Submission Date:** July 10, 2026

## Executive Summary

ConceptSMILE introduces a model-agnostic, perturbation-based auditing framework for evaluating the reliability and trustworthiness of concept-based explainable AI systems. By extending the SMILE (Symbolic Manipulation of Interpretable Linear Explanations) approach from region-level to concept-level explanations, the paper addresses a critical gap in XAI evaluation: many concept-based explanation methods lack rigorous reliability assessment. The framework enables practitioners to audit whether concepts extracted by explanation systems are actually faithful to model behavior, faithful to ground truth, stable under perturbations, and generalizable across contexts.

## Problem Statement

Concept-based explainable AI methods have become increasingly popular for interpreting machine learning models in sensitive domains like medical imaging. However, there is a significant gap between the promise of concept-level explanations and their actual reliability. Key challenges include:

1. **Lack of Rigorous Auditing:** Most concept-based explanation methods (e.g., TCAV, ACE, LACE) lack comprehensive evaluation frameworks that assess multiple reliability dimensions simultaneously.

2. **Unknown Faithfulness:** Concepts may not faithfully represent what the model actually learns or what humans understand, leading to misleading explanations that give false confidence to domain experts.

3. **Stability Under Perturbations:** Concept-level explanations may be fragile to small input perturbations or distribution shifts, undermining their utility in high-stakes applications.

4. **Inconsistency Across Pathways:** Different explanation pathways (e.g., visual features vs. semantic embeddings) may produce conflicting concepts for the same input, creating confusion about which explanation to trust.

5. **Limited Domain Applicability Assessment:** Existing frameworks don't systematically evaluate how concepts transfer across different domain conditions or how they degrade under adversarial or corrupted inputs.

## Core Concepts & Theory

### Concept-Based Explanations Overview

Concept-based explainability methods aim to interpret neural networks by extracting human-understandable concepts (e.g., "vessel," "exudate," "hemorrhage" in retinal imaging) and explaining predictions through these concepts. Unlike feature-based attributions (saliency maps, SHAP), concept-based methods operate at a higher semantic level, making explanations more interpretable to domain experts.

**Key interpretability concepts:**
- **Concepts:** Abstract, human-understandable units (often semantic or visual) that summarize model behavior
- **Attribution:** Measuring how much each concept contributes to a model's prediction
- **Faithfulness:** Whether the explanation accurately reflects the model's decision-making process
- **Stability:** Whether explanations remain consistent under small input perturbations

### SMILE Framework Foundation

ConceptSMILE extends SMILE (Symbolic Manipulation of Interpretable Linear Explanations), which operates through:

1. **Perturbation:** Systematically corrupt input regions (e.g., superpixels, patches)
2. **Measurement:** Track how the model's output changes
3. **Locality Weighting:** Weight perturbations by proximity to maintain local linearity assumptions
4. **Surrogate Fitting:** Fit a simple, interpretable model (e.g., XGBoost) to approximate local behavior
5. **Attribution:** Extract how much each feature/concept contributes locally

### Concept-Level Extension

ConceptSMILE adapts this framework to concepts by:

1. **Extracting Concept Representations:** Use a pre-trained concept extractor (e.g., MedSAM for visual concepts, CLIP for semantic concepts) to produce concept embeddings from the model's latent space
2. **Perturbation Pipeline:** Apply input perturbations and track changes in concept activations (not just final predictions)
3. **Concept Attribution:** Use perturbation responses to determine which input regions most affect each concept's activation
4. **Reliability Metrics:** Measure concept reliability across multiple dimensions

### Reliability Dimensions

The framework assesses concepts across five key dimensions:

1. **Attribution Accuracy (Spatial Fidelity):** Do the input regions highlighted for a concept align with human-understandable definitions of that concept?

2. **Surrogate Fidelity:** How well can a simple surrogate model (XGBoost) approximate the concept's behavior? High R² indicates the concept behaves locally linearly.

3. **Faithfulness:** Do the identified concept attributions explain the model's actual decision-making process? Low fidelity suggests concepts may be artifacts rather than genuine model components.

4. **Stability:** Do concept attributions remain consistent under adversarial perturbations (e.g., noise, blur, artifacts)?

5. **Consistency:** Do different explanation pathways (e.g., visual vs. semantic) agree on concept importance?

## Main Ideas & Key Contributions

### Primary Innovation: Multi-Dimensional Reliability Audit Framework

The core contribution is a systematic, model-agnostic framework that audits concept-based explanations on multiple dimensions. Unlike prior work that evaluates single properties (e.g., faithfulness alone), ConceptSMILE provides a holistic audit checklist.

**Key advantages:**
- **Model-Agnostic:** Works with any model and concept extraction method
- **Comprehensive:** Evaluates multiple reliability aspects simultaneously
- **Practical:** Designed for real-world deployment in medical imaging and other sensitive domains
- **Interpretable:** Uses human-understandable metrics (R², perturbation responses) rather than abstract measures

### Insights from Medical Imaging Evaluation

The paper evaluates two concept extraction pathways on retinal fundus images:

1. **MedSAM Pathway:** Uses visual segmentation masks (vessel, optic disc, exudates)
2. **VLM Pathway:** Uses CLIP embeddings (semantic concepts like "vessel," "pathology")

**Key finding:** Different pathways have different strengths:
- MedSAM excels at spatial attribution accuracy and surrogate fidelity (R² = 0.8503)
- VLM excels at semantic faithfulness and stability under some artifact conditions

This suggests practitioners need multiple explanation pathways to gain full confidence in concept-based systems.

### Addressing Concept Reliability in Practice

The framework highlights that concept reliability varies by concept and pathway, not uniformly. Some concepts (e.g., "vessel") are reliably extracted, while others (e.g., fine-grained pathological features) may be unstable or unfaithful. This enables:

- **Selective Trust:** Domain experts can identify which concepts to trust for decision-making
- **Targeted Improvement:** Practitioners can focus reliability improvements on unreliable concepts
- **Risk Quantification:** Provide confidence scores for each concept's explanations

## Methodology & Implementation

### Auditing Pipeline

1. **Input Perturbation:**
   - Segment input into superpixels or patches
   - Systematically corrupt each region (e.g., replace with mean color, blur, or mask)
   - Generate a perturbation dataset

2. **Concept Extraction:**
   - For each perturbation, extract concept embeddings from the explanation pathway
   - Record concept activation changes

3. **Locality Weighting:**
   - Weight each perturbation by distance to the original input
   - Maintains local linearity assumption for surrogate fitting

4. **Surrogate Model Training:**
   - Fit XGBoost to predict concept activations from perturbation binary indicators
   - XGBoost feature importances encode which input regions affect concepts

5. **Reliability Metric Computation:**
   - Attribution Accuracy: Compare extracted regions to human-annotated concept definitions
   - Surrogate Fidelity: R² score of XGBoost fit to concept responses
   - Faithfulness: Measure via downstream model agreement (predictions remain consistent)
   - Stability: Re-run pipeline under adversarial perturbations (noise, blur, artifacts)
   - Consistency: Compare concept importances across pathways

### Experimental Setup

**Dataset:** Retinal fundus images (diabetic retinopathy, age-related macular degeneration)

**Models:**
- Target model: Diabetic retinopathy classifier
- Concept pathways:
  - MedSAM: Medical image segmentation model producing spatial masks
  - CLIP: Vision-language model producing semantic embeddings

**Evaluation:**
- Attribution accuracy: Intersection over union (IoU) with domain expert annotations
- Surrogate fidelity: R² on held-out test perturbations
- Faithfulness: Prediction agreement under concept ablation
- Stability: Metric retention under Gaussian noise, blur, and compression artifacts
- Consistency: Correlation of concept importances across pathways

### Results [Exact figures unavailable — see full paper]

**MedSAM Pathway:**
- Spatial attribution accuracy (IoU): Strong alignment with expert-annotated vessel and exudate regions
- Surrogate fidelity: R² = 0.8503, weighted R² = 0.8465 (indicates high local linearity)
- Stability: Moderate robustness to noise; degrades under severe blur

**VLM (CLIP) Pathway:**
- Semantic concept accuracy: Good alignment with high-level pathological concepts
- Surrogate fidelity: R² = 0.78–0.82 (lower than MedSAM but still respectable)
- Faithfulness: Stronger vessel-related concept reliability
- Stability: Superior robustness to artifact conditions compared to MedSAM

**Key observation:** Concept reliability is heterogeneous. Vessel concepts are highly reliable in both pathways, while fine-grained pathology concepts show variable reliability.

### Limitations

1. **Limited Test Set:** Initial evaluation on retinal images; generalization to other medical domains or natural images not yet fully established
2. **Perturbation Methodology:** Superpixel masks are coarse; finer perturbations may reveal different reliability characteristics
3. **Concept Definitions:** Human-annotated ground truth for concept accuracy is labor-intensive; scaling to many concepts is challenging
4. **Computational Cost:** Full pipeline evaluation requires multiple model forward passes; scalability to large models or datasets is unclear

## Practical Applications & Real-World Use Cases

### Medical Imaging & Diagnosis Support

**Healthcare:** Radiologists and pathologists using AI for:
- Diabetic retinopathy detection in retinal fundus images
- Tumor detection and characterization in CT/MRI scans
- ECG interpretation in cardiology

**Value:** ConceptSMILE audit framework enables clinicians to understand which AI-extracted concepts (vessel patterns, hemorrhages, exudates) are trustworthy explanations of the model's decisions, rather than relying blindly on unvalidated concept systems.

**Example:** A retinal AI system identifies "vessel abnormality" as a risk factor. Using ConceptSMILE:
- Audit whether "vessel abnormality" actually corresponds to regions the model attends to
- Verify stability under different imaging protocols or devices
- Compare visual vs. semantic pathways to gain confidence

### Regulatory & Compliance

**FDA & Medical Device Approval:**
- Regulatory agencies increasingly require explainability evidence for AI diagnostic systems
- ConceptSMILE provides systematic, auditable evidence that explanations are faithful
- Supports validation documentation for FDA 510(k) or approval pathways

**GDPR & Data Privacy:**
- Right to explanation requires transparent decision-making
- Concept-based explanations satisfy transparency requirements
- ConceptSMILE auditing ensures explanations are not "false transparency" (explanations that look right but aren't faithful)

**AI Act (EU) Compliance:**
- High-risk AI systems must demonstrate explainability
- ConceptSMILE audit results can substantiate XAI compliance claims

### Finance & Risk Management

**Loan & Credit Decisions:**
- Banks use AI to evaluate creditworthiness
- Concept-based explanations (e.g., "debt-to-income ratio," "payment history") are expected by regulators
- ConceptSMILE auditing ensures these concepts genuinely drive model decisions

**Anomaly Detection:**
- Concept auditing helps detect whether a system's reported anomaly concepts are stable/reliable or artifacts of the detection process

### Autonomous Systems

**Self-Driving Cars:**
- Critical for understanding whether vehicle's decision concepts (pedestrian detection, traffic light recognition) are robust to distribution shift
- Stability metrics help identify which concepts degrade under adverse weather or novel scenarios

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Beyond Post-Hoc Auditing:** ConceptSMILE demonstrates that post-hoc explanation auditing is essential. Practitioners cannot assume concept-based explanations are faithful; systematic evaluation is mandatory.

2. **Reliability is Heterogeneous:** Different concepts have different reliability profiles. A single "concept fidelity" score is insufficient; per-concept auditing is necessary.

3. **Pathway Matters:** The mechanism for concept extraction (visual segmentation vs. semantic embeddings) significantly affects reliability. Practitioners benefit from multiple explanation pathways.

4. **Stability Under Perturbations:** Explanations must be robust to input variations. ConceptSMILE's perturbation-based approach aligns with recent trends in adversarial robustness and distribution shift research.

### Advances in Explainability

This work contributes to:

1. **Operationalizing XAI:** Bridges the gap between theoretical explainability research and practical deployment by providing measurable audit criteria.

2. **Standardizing Concept Evaluation:** Establishes a framework that could become a standard auditing process for concept-based systems (analogous to fairness auditing for bias in ML).

3. **Integration with Human-in-the-Loop Systems:** Enables systems to flag unreliable concepts and request human oversight, supporting effective human-AI collaboration.

### Limitations & Open Questions

1. **Scalability:** How does the framework scale to models with thousands of concepts or very high-dimensional input spaces?

2. **Concept Definition Mismatch:** What if human-defined concepts don't align with model-learned concepts? ConceptSMILE assumes concept definitions are available; discovering concepts remains challenging.

3. **Dynamic Concepts:** Real-world concept meanings may evolve over time or vary across populations. Does auditing need to be repeated periodically?

4. **Fairness-Trustworthiness Trade-offs:** Can concept-based explanations be audited for both trustworthiness and fairness simultaneously?

### Future Research Directions

1. **Automated Concept Discovery + Auditing:** Combine ConceptSMILE with unsupervised concept discovery methods to enable fully automated auditing pipelines.

2. **Cross-Domain Concept Transfer:** Investigate how concepts learned in one domain transfer to others and how auditing results generalize.

3. **Interactive Refinement:** Use audit results to iteratively improve concept extractors, creating a feedback loop for more reliable explanations.

4. **Integration with Model Improvement:** Beyond auditing, use ConceptSMILE insights to steer model retraining toward more interpretable, reliable features.

5. **Benchmark Datasets:** Develop standardized evaluation datasets for concept-based XAI auditing, similar to fairness benchmarks.

## Code & Resources

### Official Implementation

**Repository:** [GitHub - ConceptSMILE](https://github.com/MohadesehMollpour/ConceptSMILE)
- Python implementation of the auditing framework
- Example notebooks for retinal fundus image evaluation
- Pre-trained concept extractors (MedSAM, CLIP wrappers)

### Dependencies & Requirements

- **Python:** 3.8+
- **Core Libraries:** PyTorch, NumPy, Scikit-learn, XGBoost
- **Medical Imaging:** OpenCV, PIL
- **Vision Models:** Transformers (HuggingFace), CLIP
- **Evaluation:** Matplotlib for visualization

### Quick Start

1. Clone the repository and install dependencies
2. Load a target model and concept extraction pathway
3. Define a perturbation strategy (superpixels or patches)
4. Run the auditing pipeline on your dataset
5. Interpret results across five reliability dimensions

### Computational Requirements

[Exact requirements unavailable — see full paper] - Estimated moderate computational cost for medical imaging (CNN-scale models); scales with dataset size and number of concepts.

## Related Work & Context

### Concept-Based XAI Methods

ConceptSMILE builds on and complements existing concept-based explanation methods:

- **TCAV (Testing with Concept Activation Vectors):** Seminal work enabling concept-based explanations by testing linear sensitivity to concept activations. ConceptSMILE addresses TCAV's lack of reliability assessment.

- **ACE (Automated Concept Extraction):** Discovers concepts unsupervised. ConceptSMILE assumes given concepts but audits their reliability.

- **LACE (Latent Concept Explanations):** Learns concepts via contrastive learning. ConceptSMILE's framework applies to LACE-extracted concepts.

- **ConceptSHAP & Concept Attribution:** Recent methods for concept-level feature attribution. ConceptSMILE provides complementary auditing.

### Connection to Feature Attribution & Perturbation-Based XAI

- **LIME & SHAP:** Established perturbation-based frameworks for local explanations. ConceptSMILE applies similar principles to concept level.

- **Perturbation-Based Attribution:** ConceptSMILE's methodology aligns with growing consensus that perturbation-based approaches are more reliable than gradient-based ones.

### Fairness & Robustness in Explanations

- **Stability of Explanations:** Related to work on adversarial robustness of saliency maps and explanations.
- **Concept Fairness:** Connects to research on whether concept-based explanations perpetuate biases.

### Recent Concept-Based XAI Papers (2025-2026)

- **"Concept frustration: Aligning human concepts and machine representations"** (2026): Addresses misalignment between human and model concepts.

- **"Measuring What Matters: Synthetic Benchmarks for Concept Bottleneck Models"** (2026): Proposes evaluation metrics for concept bottleneck architectures.

- **"An Explainable Biomedical Foundation Model via Large-Scale Concept-Enhanced Vision-Language Pre-training"** (2026): Scales concept-based approaches to large biomedical models.

### Broader XAI Community

ConceptSMILE contributes to ongoing debates in the XAI community:

1. **Post-Hoc vs. Intrinsic Interpretability:** Shows that even model-agnostic post-hoc explanations can be rigorously audited.

2. **Faithfulness as a Requirement:** Aligns with the growing recognition that faithfulness is non-negotiable for high-stakes applications.

3. **Towards Standardized XAI Auditing:** Analogous to fairness and robustness auditing, contributes to making XAI evaluation systematic and reproducible.

## Conclusion

ConceptSMILE addresses a critical gap in the trustworthiness of concept-based explainable AI systems. By providing a systematic, model-agnostic framework for auditing concepts across multiple reliability dimensions, it enables practitioners to:

- Assess whether concept-based explanations are actually faithful to model behavior
- Identify concepts that can be trusted for high-stakes decision support
- Detect when explanations may be misleading
- Build confidence in AI systems deployed in regulated domains like healthcare

The medical imaging evaluation demonstrates practical value, showing that different explanation pathways have different reliability profiles and require complementary auditing. As AI systems become increasingly prevalent in high-stakes domains, ConceptSMILE represents an important step toward trustworthy, auditable explanations that users can confidently rely on.
