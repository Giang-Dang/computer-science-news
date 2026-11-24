# XAI-Arena: Can LLMs Assess the Quality of XAI Explanations?

**ArXiv ID:** [2609.09428](https://arxiv.org/abs/2609.09428)  
**Authors:** Yanfei Hu Fleischhauer, Alona Zharova, Nadja Klein, Stefan Feuerriegel  
**Submitted:** September 2026  
**Field:** Explainable AI, Explanation Evaluation, LLM-as-a-Judge Framework

## Executive Summary

XAI-Arena introduces the first LLM-as-a-judge framework for scalable, reproducible, and multidimensional evaluation of explainable AI explanations. Rather than relying solely on subjective human judgment (which limits reproducibility and scalability), the paper proposes using large language models as automated judges to assess explanation quality across eight dimensions: perceived simplicity, clarity, task adequacy, trust calibration, actionability, transparency, faithfulness, and overall interpretability. The framework achieves strong agreement with human ratings (Spearman's rho = .693, p < .001), offering a practical solution for benchmarking diverse XAI methods at scale.

## Problem Statement

### Current Challenges in XAI Evaluation

Traditional evaluation of explanations in explainable AI relies on **subjective human judgment**, which creates significant limitations:

- **Reproducibility:** Human evaluators introduce subjectivity and inconsistency, making it difficult to reproduce results across studies and institutions
- **Scalability:** Conducting human studies is expensive, time-consuming, and limits the number of explanations that can be evaluated
- **Comparability:** Without standardized, automated evaluation procedures, comparing XAI methods across different papers and contexts is challenging
- **Dimensionality:** Explanations should be evaluated on multiple dimensions (simplicity, clarity, faithfulness, etc.), but human studies typically capture only a subset
- **Stakeholder Sensitivity:** Different stakeholders (domain experts, executives, regulators) may require explanations optimized for different purposes, but standard human evaluations cannot easily adapt to these differences

### Limitations of Existing Approaches

Prior work in XAI evaluation has focused on:
- Technical correctness (e.g., faithfulness scores based on model ablations)
- Simple metrics like sparsity or stability
- Limited-scale human studies that don't scale to comprehensive benchmarking
- Narrow evaluation criteria that don't capture the full spectrum of explanation quality

XAI-Arena addresses these gaps by proposing an automated, scalable framework that maintains strong alignment with human judgment while enabling comprehensive multidimensional evaluation.

## Core Concepts & Theory

### The XAI-Arena Framework

XAI-Arena operationalizes explanation evaluation through **eight key dimensions**:

1. **Perceived Simplicity:** How easy is the explanation to understand? Does it use accessible language and avoid jargon?
2. **Clarity:** How clearly does the explanation convey its main message? Is the structure logical and coherent?
3. **Task Adequacy:** Does the explanation address the specific prediction task at hand? Is it relevant and focused?
4. **Trust Calibration:** Does the explanation inspire appropriate levels of trust? Does it avoid over- or under-confidence?
5. **Actionability:** Can stakeholders take concrete actions based on the explanation? Is it practical and implementable?
6. **Transparency:** Does the explanation clearly describe the reasoning process? Can stakeholders understand why the model made this decision?
7. **Faithfulness:** Does the explanation accurately represent the model's internal decision-making process? Is it not misleading?
8. **Overall Interpretability:** Holistic assessment of the explanation's ability to make the model's behavior understandable to humans

### Foundational Concepts

**LLM-as-a-Judge Paradigm:** The framework leverages the natural language understanding capabilities of large language models to assess explanation quality. Rather than designing hand-crafted metrics, the LLM acts as a human-like judge that can evaluate explanations qualitatively across multiple dimensions.

**Multidimensional Evaluation:** Unlike single-metric approaches (e.g., "faithful" or "not faithful"), XAI-Arena evaluates explanations on a spectrum across multiple independent dimensions, recognizing that high-quality explanations must balance competing objectives (e.g., simplicity vs. thoroughness).

**Stakeholder-Aware Assessment:** The framework can be customized for different stakeholder personas (e.g., data scientists, business analysts, domain experts, regulators), recognizing that explanation needs vary by audience.

### Relationship to Prior XAI Evaluation Work

XAI-Arena builds on and extends:
- **Attribution Method Benchmarks:** Prior work benchmarked LIME, SHAP, and similar methods against ground truth on synthetic datasets (e.g., XAI-BENCH, XAI-Units). XAI-Arena complements this by evaluating explanations from a human-centric perspective.
- **Human-Centered Explanation Research:** Studies like those by Lipton and others emphasize the importance of explanations being understandable to humans, not just technically correct. XAI-Arena operationalizes these insights into automated metrics.
- **Explanation Quality Taxonomies:** Conceptual frameworks have categorized explanation qualities (e.g., completeness, accuracy, comprehensibility). XAI-Arena translates these into measurable dimensions.

The key novelty is the **combination** of LLM-based automation with multidimensional, stakeholder-aware evaluation at scale.

## Main Ideas & Key Contributions

### 1. First LLM-as-a-Judge Framework for XAI Explanations

XAI-Arena is the first framework to systematically apply the LLM-as-a-judge paradigm specifically to XAI explanation evaluation. The authors demonstrate that LLMs can reliably assess explanation quality across multiple dimensions, achieving strong correlation with human judgment without the cost and scalability limitations of traditional human studies.

### 2. Multidimensional Evaluation Protocol

Rather than reducing explanation quality to a single score, XAI-Arena evaluates across **eight independent but complementary dimensions**. This allows:
- Fine-grained understanding of explanation strengths and weaknesses
- Domain-specific selection of relevant dimensions based on use case
- Comparison of XAI methods on specific criteria of interest
- Recognition that "best" explanations depend on stakeholder priorities

### 3. Benchmarking of Major XAI Methods

The paper benchmarks five widely-used XAI explanation methods:
- **SHAP (SHapley Additive exPlanations):** State-of-the-art game-theoretic feature attribution
- **LIME (Local Interpretable Model-agnostic Explanations):** Local linear approximations
- **DiCE (Diverse Counterfactual Explanations):** Counterfactual-based explanations
- **Partial Dependence:** Global explanation of feature-outcome relationships
- **Permutation-based Methods:** Feature importance through random shuffling

The comparative analysis reveals which methods excel on different dimensions and identifies trade-offs (e.g., local methods often achieve higher clarity and actionability, but may sacrifice comprehensiveness).

### 4. Empirical Validation Against Human Judgment

The authors conducted human studies showing that LLM ratings correlate strongly with human judgment:
- **Overall Spearman's correlation: rho = .693 (p < .001)**
- **Per-dimension correlations vary:** Perfect rank correlation (rho = 1.000) for perceived simplicity; weaker correlations for dimensions requiring numerical or technical accuracy
- **Finding:** LLM judges reliably capture qualitative aspects of explanation quality but may be less reliable for technical accuracy dimensions

This validation demonstrates that XAI-Arena can serve as a practical surrogate for human evaluation in many contexts, though the authors note it should not entirely replace human judgment for critical applications.

### 5. Scalable, Reproducible Evaluation Workflow

The framework enables:
- **Reproducibility:** Fixed LLM models and seeds ensure consistent ratings across runs and research groups
- **Scalability:** Automated evaluation allows benchmarking hundreds or thousands of explanations without human resources
- **Comparability:** Standardized evaluation enables fair comparison of XAI methods across different papers and organizations
- **Customization:** Framework can be tailored to specific stakeholder personas or domain requirements

## Methodology & Implementation

### Experimental Setup

**Datasets:**
- **Synthetic Datasets:** Controlled environments for systematic evaluation of explanation dimensions
- **Wisconsin Diagnostic Breast Cancer (WDBC):** 569 samples, 30 numerical features; classification task predicting malignancy
- **Additional Tabular Datasets:** Multiple classification and regression tasks for real-world validation

**Machine Learning Models:**
- Gradient boosting models (XGBoost)
- Random forests
- Neural networks
- Other standard ML models commonly explained in practice

**XAI Methods Evaluated:**
1. SHAP (multiple variants)
2. LIME
3. DiCE (counterfactual explanations)
4. Partial Dependence
5. Permutation-based Feature Importance

### Evaluation Protocol

**Six-Step XAI-Arena Workflow:**
1. **Generate Explanations:** Apply XAI method to model predictions
2. **Prepare Prompts:** Structure explanations into LLM-readable format with context about the prediction task
3. **Invoke LLM Judge:** Query the LLM with standardized prompts requesting ratings on each of the eight dimensions
4. **Collect Ratings:** Obtain numerical ratings (typically on 1-5 or 1-7 scales) for each dimension
5. **Aggregate Scores:** Combine individual ratings into profile of explanation quality
6. **Comparative Analysis:** Compare XAI methods across dimensions and stakeholder personas

**LLM Judge Details:**
- Uses fixed LLM models (reported in appendix) with version control
- Fixed random seeds for reproducibility
- Standardized prompt engineering across all evaluations
- Anonymous 4open.science repository for validation notebook and reproducibility scripts

### Key Evaluation Metrics

[Exact figures unavailable — see full paper for detailed metric results]

**Per-Method Performance Patterns:**
- **SHAP:** Strong on transparency and faithfulness; variable on simplicity
- **LIME:** High on clarity and actionability due to interpretable local linear models
- **DiCE:** Excels on actionability (counterfactuals are inherently actionable)
- **Partial Dependence:** Good for comprehensiveness but may sacrifice clarity
- **Permutation-based:** Generally high on simplicity but potentially less faithful

**Correlation with Human Judgment (reported as [Exact figures unavailable]):**
- Overall Spearman's rho = .693 (p < .001)
- Strong rank correlation for some dimensions
- Weaker for dimensions requiring technical verification

### Statistical Analysis

The paper reports:
- Spearman rank correlations between LLM and human ratings
- Statistical significance testing (all results at p < .001 level)
- Per-dimension breakdowns
- Cross-dataset consistency checks

### Limitations of the Approach

1. **LLM Consistency:** LLMs may drift in behavior over time or across different versions; reproducibility depends on version pinning
2. **Dimension Weighting:** Framework evaluates eight dimensions equally; in practice, stakeholder-specific weighting may be needed
3. **Ground Truth:** For some dimensions (e.g., faithfulness), LLM assessment may not capture technical correctness; expert review still recommended
4. **Context Sensitivity:** LLM ratings may not fully capture domain-specific requirements of specialized fields (e.g., medical diagnosis, financial decisions)
5. **Stakeholder Representation:** While the framework claims stakeholder-awareness, actual personas tested were limited; generalization to new stakeholder types requires validation

## Practical Applications & Real-World Use Cases

### 1. Healthcare and Medical Diagnosis

**Use Case:** Explaining AI-based diagnostic recommendations to clinicians and patients

- **Challenge:** Clinicians need explanations they can verify against their clinical knowledge; patients need actionable, understandable guidance
- **XAI-Arena Application:** Evaluate whether explanations from different XAI methods achieve the right balance of technical accuracy (faithfulness/transparency) and interpretability for each audience
- **Regulatory Relevance:** FDA increasingly requires explainability for AI medical devices; XAI-Arena can standardize evaluation across submissions

### 2. Financial Services and Credit Decisions

**Use Case:** Explaining loan approval/denial decisions to applicants and regulators

- **Challenge:** Decisions must be legally defensible (transparency), actionable (what can the applicant improve?), and appropriate in confidence (trust calibration)
- **XAI-Arena Application:** Benchmark XAI methods across the actionability and trust calibration dimensions to ensure decisions are both understandable and appropriate
- **Regulatory Relevance:** Fair Lending laws require that explanation processes support contestability; XAI-Arena helps verify this

### 3. Hiring and Recruitment

**Use Case:** Explaining AI-assisted candidate screening and hiring recommendations

- **Challenge:** Candidates need to understand why they were rejected or screened out (transparency, actionability); HR teams need to identify potential algorithmic bias (faithfulness)
- **XAI-Arena Application:** Evaluate whether explanations support both candidate understanding and bias auditing
- **Regulatory Relevance:** Employment discrimination laws increasingly scrutinize algorithmic decision-making; systematic evaluation is critical

### 4. E-commerce and Recommendation Systems

**Use Case:** Explaining product recommendations to customers

- **Challenge:** Customers need simple, compelling reasons to trust recommendations (clarity, trust calibration); businesses want explanations that drive engagement and sales
- **XAI-Arena Application:** Use framework to find balance between simplicity/actionability (drive clicks) and faithfulness (maintain user trust)

### 5. Regulatory Compliance and Audit

**Use Case:** Demonstrating AI system explainability to regulators (GDPR Right to Explanation, AI Act, etc.)

- **Challenge:** Regulations require "explanations," but define this vaguely; organizations need standardized evidence of explanation quality
- **XAI-Arena Application:** Provide reproducible, systematic evaluation demonstrating that explanations meet regulatory standards across multiple dimensions
- **Implementation:** Organizations can run XAI-Arena to generate auditable reports of explanation quality before submission to regulators

### Implementation Challenges

1. **Prompt Engineering:** Requires careful design of prompts to elicit consistent, meaningful LLM responses
2. **Model Selection:** Different LLM versions produce different ratings; organizations must decide on specific models and versions for consistency
3. **Cost:** While more efficient than human studies, automated evaluation at scale still requires compute resources
4. **Integration:** Requires pipeline integration with existing ML systems and explanation generation workflows

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Automated, Scalable Evaluation:** XAI-Arena demonstrates that trustworthy AI doesn't require manual human oversight at every step; intelligent automation can complement human judgment at scale
2. **Multidimensional Assessment:** The finding that explanations should be evaluated across multiple dimensions (not reduced to single scores) has implications for XAI design—the "best" explanation depends on stakeholder needs
3. **LLM Trust:** The framework shows that LLMs can serve as useful proxies for human judgment in some domains, but their reliability varies by task; this has implications for broader LLM-as-a-judge approaches in AI safety and alignment

### Advancing the State-of-the-Art in Explainability

1. **Benchmarking Infrastructure:** XAI-Arena provides common infrastructure for standardized comparison of XAI methods, similar to how ImageNet and other benchmarks accelerated computer vision research
2. **Explanation Evaluation as a Field:** The framework legitimizes explanation evaluation as a research area with rigorous metrics and protocols, moving it beyond ad-hoc human studies
3. **Stakeholder-Aware Design:** Demonstrates that one-size-fits-all XAI is insufficient; methods should be evaluated and designed with specific stakeholders in mind

### Limitations, Failure Cases, and Open Questions

1. **LLM Hallucination:** Can LLMs accurately assess technical dimensions like faithfulness, or do they hallucinate plausible-sounding but incorrect ratings?
2. **Cultural and Linguistic Bias:** How do LLM ratings vary across languages, cultural contexts, and demographic groups? Do they reproduce human biases in explanation preferences?
3. **Dimension Independence:** Are the eight dimensions truly independent? Could they be reduced or reorganized? Do correlations between dimensions suggest a latent structure?
4. **Generalization to New Methods:** As new XAI methods emerge (e.g., causal inference, mechanistic interpretability), will the framework generalize or require adaptation?
5. **Domain Specificity:** The paper benchmarks on relatively standard ML tasks; how does XAI-Arena perform on domain-specific applications like scientific discovery or medical diagnosis?

### Future Research Directions

1. **Deeper LLM Analysis:** Investigate LLM internals to understand *why* they correlate with human judgment; use mechanistic interpretability to verify that LLM ratings reflect the intended dimensions
2. **Dynamic Evaluation:** As XAI methods evolve, continuously update benchmarks; build a living leaderboard similar to SuperGLUE for XAI explanations
3. **Causal Understanding:** Move beyond correlation to establish causal relationships: *what changes in an explanation cause human preferences to shift?*
4. **Cross-Domain Transfer:** Test whether XAI-Arena generalizes from tabular data to images, text, time series, and other modalities
5. **Interactive Evaluation:** Extend framework to interactive settings where stakeholders can query and refine explanations in real-time

## Code & Resources

### Official Implementation

- **Anonymous Repository:** 4open.science repository (details in paper)
- **Validation Notebook:** Reproducibility notebook included for verification of results
- **Version Control:** Fixed random seeds and model versions for reproducibility

### Datasets and Benchmarks

- **Wisconsin Diagnostic Breast Cancer (WDBC):** Publicly available; 569 samples, 30 features
- **Synthetic Datasets:** Generated for controlled experiments; described in paper appendix
- **Tabular Benchmark:** Multiple classification and regression datasets (details in full paper)

### Dependencies and Requirements

[Exact specifications unavailable — see full paper for environment setup]

- Large language model API access (specific models listed in paper)
- Python libraries for ML/explanation generation (scikit-learn, XGBoost, etc.)
- SHAP, LIME, and other XAI method libraries
- LLM API keys and rate limits for large-scale evaluation

### Quick Start Guide

1. Install XAI method libraries (SHAP, LIME, etc.)
2. Prepare dataset and train ML model
3. Generate explanations for model predictions
4. Format explanations into XAI-Arena input structure
5. Query LLM judge with standardized prompts
6. Collect ratings and aggregate into explanation quality profiles
7. Compare XAI methods across dimensions

For step-by-step implementation, refer to validation notebook in the anonymous repository.

## Related Work & Context

### Foundational XAI Methods

XAI-Arena evaluates implementations of:
- **SHAP:** Lundberg & Lee (2017), "A Unified Approach to Interpreting Model Predictions" — game-theoretic approach to feature attribution with proven theoretical properties
- **LIME:** Ribeiro et al. (2016), "Why Should I Trust You?" — foundational local interpretability method
- **Counterfactual Explanations (DiCE):** Mothilal et al. (2020) — actionable, contrastive explanations showing what would need to change for different outcomes

### Related Benchmarking and Evaluation Work

- **XAI-BENCH (arXiv:2106.12543):** Synthetic benchmarks with known ground truth for evaluating attribution methods
- **XAI-Units (arXiv:2506.01059):** Unit tests for explanation methods; finds LIME and KernelSHAP perform worse on significantly non-linear models
- **XAI-TRIS (arXiv:2306.12816):** Non-linear image benchmarks to quantify false positive attribution rates
- **Factorial Study of LLM-Generated Explanations (arXiv:2601.02224):** Human study comparing SHAP and LIME with no-XAI baseline (d ≈ 0.3 effect size)

### LLM-as-a-Judge Research

XAI-Arena contributes to growing body of work on using LLMs as evaluators:
- **G-Eval and Related Work:** Demonstrates LLMs can reliably assess text quality in some domains but show variation by task
- **Limitations of LLM Judges:** Related work notes that LLM judges replicate human conclusions on coarse-grained qualities but are weaker on numerical verification
- **Implications:** XAI-Arena demonstrates both capabilities and limitations of this paradigm when applied to XAI

### Explanation Quality Theory

Building on theoretical work by:
- **Lipton (2016, 2018):** Critiques of "interpretability" definitions; call for rigor in explanation research
- **Miller (2019):** "Explanation in Artificial Intelligence: Insights from the Social Sciences" — human-centered perspective on what makes good explanations
- **Mittelstadt et al. (2016):** European legal framework on the Right to Explanation; implications for XAI evaluation standards

### Regulatory and Ethical Frameworks

- **GDPR Article 22:** Right to explanation for automated decision-making; XAI-Arena provides tools for demonstrating compliance
- **AI Act (EU):** Increasing requirements for explainability; XAI-Arena enables standardized compliance assessment
- **FDA Guidance on AI/ML in Medical Devices:** Calls for explanation quality assessment; XAI-Arena could support this
- **Fairness Research:** Connections to work on fairness-aware explanations (do explanations support understanding of bias?)

### Connections to XAI Communities

- **LIME Community:** XAI-Arena provides systematic evaluation framework for LIME variants and improvements
- **SHAP Community:** Benchmarking across SHAP methods (kernel, tree, deep) enables identification of method trade-offs
- **Concept-Based Explanations:** While not explicitly benchmarked, framework extends to concept-based and prototype-based methods
- **Causal Interpretability:** Relationship to causal explanation work (counterfactuals are causal by nature)
- **Mechanistic Interpretability:** Orthogonal but complementary to circuit analysis and circuit discovery approaches; could evaluate circuit explanations

### Next Steps in the Field

1. **Community Adoption:** Building on XAI-Arena framework to create shared benchmarks and leaderboards for explanation methods
2. **Domain-Specific Adaptations:** Extending framework to specialized domains (medical, legal, financial) with domain-specific dimensions
3. **Explanation Design:** Using insights from XAI-Arena to inform design of better explanation interfaces and presentation formats
4. **Fairness and Transparency:** Investigating whether certain explanation methods better support fairness auditing and bias detection

## References and Further Reading

- **Paper:** XAI-Arena: Can LLMs Assess the Quality of XAI Explanations? (arXiv:2609.09428)
- **Anonymous Code Repository:** 4open.science (details in paper)
- **Related Surveys:** 
  - LLMs for Explainable AI: A Comprehensive Survey (arXiv:2504.00125)
  - Making Sense of the Unsensible (arXiv:2505.20305)
  - Beyond Explainable AI (arXiv:2602.24176)
- **Foundational Methods:**
  - SHAP: https://arxiv.org/abs/1705.07874
  - LIME: https://arxiv.org/abs/1602.04938
  - DiCE: https://arxiv.org/abs/1912.03277

---

*This summary synthesizes research from the XAI-Arena paper and related work in explainable AI evaluation. For complete details, methodology, and experimental results, refer to the full paper at arxiv.org/abs/2609.09428.*
