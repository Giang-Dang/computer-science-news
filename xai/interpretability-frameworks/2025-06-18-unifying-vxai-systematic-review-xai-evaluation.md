# Unifying VXAI: A Systematic Review and Framework for the Evaluation of Explainable AI

**ArXiv ID:** [2506.15408](https://arxiv.org/abs/2506.15408)

## Executive Summary

This comprehensive systematic review consolidates 362 explainable AI research papers to address a critical standardization gap in XAI evaluation. The authors propose a unified framework (VXAI) with seven desiderata—parsimony, plausibility, coverage, fidelity, continuity, consistency, and efficiency—that organize 41 metric groups across three dimensions of XAI evaluation. This framework enables consistent, reproducible assessment of explainability methods and provides a shared vocabulary for the field.

## Problem Statement

The explainable AI field faces significant challenges in evaluation and standardization:

- **Fragmented evaluation landscape:** The XAI community lacks consensus on which metrics best evaluate explanations, leading to inconsistent evaluation practices across publications
- **Proliferation of metrics:** Hundreds of different evaluation metrics exist, many with overlapping or ambiguous purposes
- **Lack of standardization:** Different papers use different terminology for similar concepts, making it difficult to compare results across studies
- **Unclear metric relationships:** The connections between computational XAI metrics and human understanding of explanations remain poorly understood
- **No unified framework:** Prior work lacked a systematic, comprehensive organization of evaluation approaches

These challenges undermine reproducibility, make it difficult to select appropriate evaluation methods for new XAI research, and hinder the adoption of XAI methods in practice where consistent evaluation is critical for high-stakes applications.

## Core Concepts & Theory

### Three-Dimensional Categorization Scheme

The VXAI framework organizes XAI evaluation across three orthogonal dimensions:

1. **Explanation Type:** Differentiates between local (instance-specific), semi-local (pattern-level), and global (model-level) explanations
   - Local: Explains individual predictions (e.g., feature importance for a single sample)
   - Semi-local: Explains decision patterns (e.g., prototypes, archetypes)
   - Global: Explains the entire model's behavior and learned representations

2. **Evaluation Contextuality:** Categorizes the context in which explanations are evaluated
   - Context 0: Isolated evaluation (no ground truth, based on desiderata properties alone)
   - Context I: Evaluation with respect to model behavior (how well the explanation reflects what the model actually learned)
   - Context II: Evaluation with respect to human understanding (how well humans understand the model through the explanation)
   - Context III: Evaluation in realistic downstream application scenarios

3. **Explanation Quality Desiderata:** Seven core properties that high-quality explanations should satisfy
   - **Parsimony:** Explanations should be concise and contain only essential information
   - **Plausibility:** Explanations should be understandable to the target audience
   - **Coverage:** Every prediction or decision should receive an explanation
   - **Fidelity:** Explanations should accurately reflect the model's actual decision-making process
   - **Continuity:** Small changes in input should result in correspondingly small changes in explanation
   - **Consistency:** Similar inputs should receive similar explanations
   - **Efficiency:** Explanations should be computationally efficient to generate and communicate

### Metric Classification

The framework consolidates 362 papers into 41 functionally similar metric groups, each mapped to specific desiderata and contextuality levels:
- Metrics targeting parsimony and plausibility are found almost exclusively in Contextuality I and II
- Fidelity metrics dominate Context I evaluations (model-behavior alignment)
- Different metric groups serve different aspects of explanation quality

## Main Ideas & Key Contributions

### 1. Systematic Literature Review

**Scope:** Followed PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) guidelines to systematically identify and analyze 362 relevant publications on XAI evaluation

**Consolidation:** Reduced the fragmented landscape to 41 core metric groups, showing that many seemingly different metrics actually serve the same evaluation purposes

**Significance:** Provides the most comprehensive meta-analysis of XAI evaluation metrics to date, offering empirical evidence of the field's fragmentation and overlaps

### 2. Unified VXAI Framework

**Innovation:** Proposes the first comprehensive three-dimensional framework organizing XAI evaluation:
- Transcends individual metric types and brings coherence to diverse evaluation approaches
- Provides a shared conceptual vocabulary for discussing and comparing XAI methods
- Enables practitioners to identify appropriate evaluation methods for their specific context

**Practical utility:** The framework can serve as a:
- Checklist for evaluating new XAI methods
- Reference for selecting evaluation metrics in research papers
- Blueprint for designing comprehensive XAI evaluation studies
- Educational tool for understanding XAI evaluation landscape

### 3. Desiderata-Based Organization

**Philosophical foundation:** Rather than organizing metrics by method type (e.g., attention mechanisms, gradient-based methods), the framework organizes by *what* we want to measure: the fundamental properties of good explanations

**Interconnected properties:** The seven desiderata are not independent:
- Parsimony and plausibility are often interrelated (brief explanations may be more understandable)
- Fidelity and continuity relate to explanation quality and robustness
- Coverage and consistency ensure explanations are comprehensive and reliable
- Efficiency enables practical deployment

### 4. Applicability Across Modalities and Domains

The framework accommodates:
- **Modalities:** Vision (saliency maps, attention visualizations, concept-based explanations), NLP (token attribution, rationale extraction), structured data (decision trees, rule lists)
- **Model types:** Deep neural networks, tree-based models, linear models, symbolic AI
- **Application domains:** Healthcare, finance, autonomous systems, content moderation, scientific discovery

## Methodology & Implementation

### Systematic Review Process

**Search strategy:**
- Comprehensive database searches across major AI/ML venues and archives
- Inclusion/exclusion criteria applied consistently
- PRISMA guidelines followed for rigor and reproducibility

**Data extraction:**
- For each paper: identified proposed metrics, evaluation contexts, explanation types supported
- Categorized metrics according to desiderata
- Mapped papers to the three-dimensional framework

**Quality assessment:**
- Evaluated clarity and completeness of metric definitions
- Assessed reproducibility of proposed evaluation methods
- Checked consistency in terminology usage

### Framework Construction

**Metric grouping:** Authors identified 41 core metric groups by analyzing:
- Conceptual definitions (what the metric measures)
- Mathematical formulations where provided
- Practical usage patterns across literature

**Dimension specification:**
- Explanation types mapped to categories (local/semi-local/global)
- Contextuality levels defined based on what metrics compare against
- Desiderata assigned based on metric purposes and properties

**Validation:** Cross-referenced the framework against:
- Seminal XAI papers to ensure coverage of major approaches
- Evaluation practices in recent work to verify real-world applicability
- Downstream citation patterns to confirm framework utility

### Results Summary

**Metric distribution:**
- Coverage: Metrics addressing model behavior and computational properties dominate (Context I)
- Coverage: Fewer metrics directly measure human understanding (Context II) — [Exact figures unavailable — see full paper]
- Distribution: Parsimony and plausibility metrics concentrated in specific contextuality levels
- Efficiency: Most XAI methods report computational costs, but efficiency metrics remain understudied

**Framework adoption:**
- Subsequent work cites the VXAI framework as a principled approach to XAI evaluation
- Other papers apply the seven desiderata as evaluation checklists for their own XAI methods
- The framework has been used in multiple domains (healthcare, finance, computer vision)

## Practical Applications & Real-World Use Cases

### 1. Healthcare & Medical Diagnosis

**Use case:** Evaluating AI-assisted diagnostic systems
- **Fidelity requirement:** Explanations must reflect which imaging features (tumors, lesions, anatomical variants) drive the model's diagnosis
- **Plausibility requirement:** Clinicians must understand the explanation without extensive AI training
- **Coverage requirement:** Every patient case requires a diagnosis, therefore an explanation
- **Regulatory compliance:** EU AI Act and FDA regulations mandate explainability for high-stakes medical AI

### 2. Financial Risk Assessment

**Use case:** Credit scoring and loan approval systems
- **Fidelity & consistency:** Explanations must accurately reflect decision criteria and treat similar applicants similarly (fairness requirement)
- **Parsimony:** Financial institutions need concise explanations for communicating decisions to applicants
- **Continuity:** Small changes in credit history should produce proportional explanation changes
- **Contestability:** Applicants must understand why they were denied to have meaningful recourse

### 3. Autonomous Vehicle Safety

**Use case:** Explaining critical driving decisions
- **Continuity:** Trajectory planning explanations must be consistent; abrupt explanation changes could indicate model instability
- **Coverage:** Every safety-critical decision requires explanation (e.g., emergency braking)
- **Efficiency:** Real-time constraints require explanations to be computed rapidly
- **Plausibility:** Safety-critical human overseers need to understand and quickly evaluate model decisions

### 4. Content Moderation & Social Media

**Use case:** Explaining content removal decisions
- **Plausibility:** Transparency for both content creators and users regarding policy enforcement
- **Consistency:** Similar content should receive similar explanations and treatment
- **Parsimony:** Concise explanations suitable for public communication
- **Fidelity:** Explanations must accurately reflect detection criteria, not post-hoc rationalizations

### 5. Scientific Discovery & Model Interpretation

**Use case:** Understanding learned representations in scientific ML
- **Fidelity:** Explanations should reveal true scientific mechanisms discovered by the model
- **Plausibility:** Scientists need interpretable explanations to validate biological/physical insights
- **Continuity:** Smooth explanation landscapes help identify robust learned patterns
- **Efficiency:** Scientific workflows require rapid model interpretation

### Implementation Challenges

1. **Contextuality trade-off:** Evaluating in Context II (human understanding) is expensive (user studies required) but essential for high-stakes applications
2. **Metric selection:** Organizations must decide which desiderata are most critical for their domain
3. **Resource constraints:** Comprehensive evaluation across all desiderata requires significant effort
4. **Stakeholder alignment:** Different stakeholders (regulators, users, developers) may prioritize different desiderata

## Insights & Implications

### Broader Implications for XAI Research

1. **Standardization path forward:** The VXAI framework provides a first step toward standardized XAI evaluation, enabling:
   - Reproducible XAI research with consistent evaluation methodology
   - Meaningful comparison across different XAI methods and papers
   - Evidence-based selection of evaluation metrics for new work

2. **Research gaps identified:**
   - **Under-explored Context II evaluation:** Most metrics focus on Context I (model behavior), while human understanding remains understudied despite being critical for interpretability
   - **Limited efficiency metrics:** Computational efficiency is rarely evaluated despite practical importance
   - **Insufficient cross-domain validation:** Many metrics designed for vision don't transfer to NLP or structured data
   - **Desiderata trade-offs:** Limited understanding of how different desiderata interact or conflict

3. **Measurement validity concerns:**
   - Computational metrics may not predict human understanding (as shown by [arXiv:2603.25251](https://arxiv.org/abs/2603.25251))
   - Proxy metrics (e.g., faithfulness) require validation against ground truth or human outcomes
   - Multiple measurements across desiderata needed for comprehensive evaluation

### Implications for XAI Practitioners

1. **Metric selection guidance:** The framework enables practitioners to:
   - Identify which desiderata matter most for their application domain
   - Select appropriate evaluation contextuality levels (model behavior vs. human understanding)
   - Choose metrics proven effective for their explanation type and domain

2. **Evaluation planning:** Framework provides a structured approach to comprehensive evaluation:
   - Ensures coverage of multiple desiderata rather than single-metric evaluation
   - Encourages Context II evaluation where feasible
   - Helps identify evaluation gaps in existing studies

3. **Interdisciplinary communication:** Shared vocabulary enables collaboration between:
   - XAI researchers and domain experts (medicine, finance, law)
   - Technical implementers and stakeholders requiring explainability
   - Regulators and industry on explainability requirements

### Limitations and Open Questions

1. **Framework limitations:**
   - Focused on taxonomy of existing metrics; standards for new metric proposals remain unclear
   - Three-dimensional framework may be incomplete or require evolution as field advances
   - Documentation standards for metrics are separate from this framework

2. **Unresolved research questions:**
   - How do desiderata optimally trade off against each other? (e.g., parsimony vs. completeness)
   - Which desiderata are essential vs. nice-to-have for different application domains?
   - How can Context II evaluation (human understanding) be scaled cost-effectively?
   - What are the cultural and domain-specific variations in explainability preferences?

3. **Metric validation gaps:**
   - Need for meta-studies validating whether currently-used metrics actually measure what they claim
   - Limited guidance on threshold values or pass/fail criteria for metric results
   - Unclear how to combine multiple metrics into holistic evaluation scores

## Code & Resources

### Official Resources

- **ArXiv Paper**: [https://arxiv.org/abs/2506.15408](https://arxiv.org/abs/2506.15408) (PDF: [https://arxiv.org/pdf/2506.15408](https://arxiv.org/pdf/2506.15408))
- **HTML Version**: [https://arxiv.org/html/2506.15408v1](https://arxiv.org/html/2506.15408v1)
- **Published at**: [Transactions on Machine Learning Research (TMLR) 2026](https://openreview.net/venue/tmlr)

### Implementation Notes

- The paper is primarily a review and framework proposal without associated code
- The framework is designed to be implemented as:
  - Evaluation checklists for XAI method papers
  - Reference tables for selecting metrics
  - Conceptual blueprint for XAI evaluation studies
- The 41 metric groups and their mappings to desiderata serve as a lookup table for practitioners

### Replicating the Framework

To apply the VXAI framework:

1. **Identify your explanation type:** local, semi-local, or global
2. **Determine evaluation context:** 
   - Context 0 if ground truth unavailable
   - Context I to evaluate model alignment
   - Context II to evaluate human understanding (preferred for interpretability claims)
   - Context III for end-to-end application evaluation
3. **Prioritize desiderata:** Select which of the seven properties matter most for your domain
4. **Select metrics:** Use the framework's 41 metric groups to find appropriate metrics
5. **Document comprehensively:** Report metrics across multiple desiderata, not just fidelity

### Computational Requirements

- Paper review and analysis: literature review methodology, no specific computational experiments
- Framework application: moderate computational cost depends on specific metrics chosen
- Most cited metrics have publicly available implementations or are available in XAI libraries (LIME, SHAP, captum, etc.)

## Related Work & Context

### How This Paper Advances the XAI Field

**Prior work landscape:**
- Individual XAI method papers typically use 1-3 evaluation metrics (often without justification)
- Previous surveys focused on explanation types (saliency maps, attention, prototypes) rather than evaluation criteria
- No comprehensive meta-analysis of XAI metrics existed before this work

**This paper's contribution:**
- First systematic PRISMA-guided review of 362 XAI papers
- Unique three-dimensional framework organizing metrics by type, context, and desiderata
- Empirical evidence of field fragmentation and metric overlap
- Actionable guidance for future evaluation in XAI research

### Connection to Broader XAI Trends

1. **From methods to evaluation:** The field is maturing from proposing new XAI methods to rigorously evaluating them
2. **Standardization movement:** This framework aligns with broader trends toward standardization in AI (ISO/IEC AI standards, NIST AI risk management framework)
3. **Human-centered focus:** Emphasis on Context II evaluation reflects growing recognition that explanations must serve human needs, not just satisfy computational metrics
4. **Regulatory drivers:** EU AI Act, FDA guidance on interpretability increasing demand for standardized evaluation approaches

### Related Recent Work

- **Evaluation methodology papers:** [arXiv:2603.25251](https://arxiv.org/abs/2603.25251) (Does Explanation Correctness Matter? - validating metrics against human understanding)
- **Specific domain evaluations:** Multiple papers apply VXAI framework to healthcare, finance, and computer vision
- **Metric documentation:** [arXiv:2605.04410](https://arxiv.org/abs/2605.04410) (Evaluation Cards for XAI Metrics - proposes documentation standards)
- **Fairness in explanations:** Research on how explainability intersects with fairness in ML systems
- **Causal interpretability:** Emerging work on using causal inference frameworks for more rigorous XAI evaluation

### Communities and Standards

- **XAI research community:** Conferences (FAccT, ICLR XAI workshops), journals publishing XAI work
- **Standards bodies:** ISO/IEC work on AI transparency; NIST AI risk management; EU AI Act implementation groups
- **Industrial practitioners:** Growing adoption of XAI methods in healthcare, finance, autonomous systems
- **Open-source XAI libraries:** LIME, SHAP, Captum, InterpretML that implement many metrics from this framework

## Conclusion

"Unifying VXAI" represents a significant milestone in XAI maturation by providing the first comprehensive, principled framework for evaluating explainable AI methods. By consolidating 362 papers into a coherent three-dimensional categorization with seven desiderata, the paper addresses the field's fragmentation and lack of standardization.

The framework's value lies not in proposing new metrics, but in organizing existing knowledge and establishing shared terminology for XAI evaluation. This enables researchers and practitioners to:
- Select appropriate evaluation methods based on principled criteria
- Compare results across different studies more meaningfully
- Design comprehensive evaluations addressing multiple quality dimensions
- Contribute to standardization efforts in AI trustworthiness

As XAI methods move from research prototypes to production systems in healthcare, finance, and autonomous systems, standardized evaluation becomes increasingly critical. This paper provides a foundational framework for that transition.

## Related ArXiv Papers

- [2603.25251](https://arxiv.org/abs/2603.25251) - Does Explanation Correctness Matter? Linking Computational XAI Evaluation to Human Understanding
- [2605.04410](https://arxiv.org/abs/2605.04410) - Evaluation Cards for XAI Metrics
- [2605.20081](https://arxiv.org/abs/2605.20081) - Bridging the Disciplinary Gap in Explainable AI: From Abstract Desiderata to Concrete Tasks
- [2607.07316](https://arxiv.org/abs/2607.07316) - Mechanistic Interpretability for Neural Networks: Circuits, Sparse Features and Symbolic Reasoning
- [2602.16823](https://arxiv.org/abs/2602.16823) - Formal Mechanistic Interpretability: Automated Circuit Discovery with Provable Guarantees

## Citation

**Bibtex:**
```
@article{dembinsky2025unifying,
  title={Unifying VXAI: A Systematic Review and Framework for the Evaluation of Explainable AI},
  author={Dembinsky, David and Lucieri, Adriano and Frolov, Stanislav and Najjar, Hiba and Watanabe, Ko and Dengel, Andreas},
  journal={Transactions on Machine Learning Research},
  year={2026},
  url={https://arxiv.org/abs/2506.15408}
}
```

---

**Publication:** Transactions on Machine Learning Research (TMLR), 2026  
**ArXiv Submission:** June 18, 2025 (v1), updated January 26, 2026 (v2)  
**Affiliations:** German Research Center for Artificial Intelligence (DFKI)
