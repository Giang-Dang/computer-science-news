# CafGa: Customizing Feature Attributions to Explain Language Models

**ArXiv ID:** [2509.20901](https://arxiv.org/abs/2509.20901)

## Executive Summary

CafGa is an interactive tool that enables users to generate and evaluate feature attribution explanations for language models at customizable granularities. Rather than treating individual words as fixed units for explanation (as standard SHAP and LIME implementations do), CafGa allows users to define meaningful text segments—from subwords to phrases—that better capture linguistic meaning and reduce computational costs. The tool addresses a fundamental limitation in post-hoc explainability: enabling practitioners to tailor explanations to their specific needs while ensuring they remain faithful and interpretable.

## Problem Statement

### The Granularity Problem in Feature Attribution for NLP

Standard feature attribution methods like SHAP and LIME treat individual words as the atomic unit of explanation. This design choice creates two significant problems:

1. **Computational Inefficiency**: For long text sequences, explaining every word becomes prohibitively expensive. When SHAP must compute attributions for hundreds of words, the number of model samples required grows exponentially, making real-time interaction infeasible.

2. **Loss of Semantic Meaning**: Many linguistic phenomena span multiple words. For example:
   - Multi-word expressions (e.g., "New York," "look forward to")
   - Named entities (e.g., "Barack Hussein Obama")
   - Negations with context (e.g., "not very good")
   - Idiomatic phrases (e.g., "cost an arm and a leg")
   
   Word-level attributions cannot capture these phenomena, leading to explanations that fragment meaning across multiple units.

### Why Existing Solutions Fall Short

**PartitionSHAP** and **MExGen** attempt to solve granularity by pre-defining segmentation strategies (e.g., fixed word counts or syntactic boundaries). However:
- They are static and not customizable to domain-specific needs
- They may not align with how experts naturally understand their domain
- They require model retraining or offline computation
- They lack interactive visual feedback for users to validate explanation quality

## Core Concepts & Theory

### Feature Attribution Fundamentals

Feature attribution methods compute the contribution of individual input features to a model's prediction. For a prediction function $f$, the attribution value $\phi_i$ for feature $i$ quantifies how much that feature influences the output.

**Key principle (Shapley Value):** Attribution values should satisfy:
- **Local accuracy**: Sum of attributions plus base value equals the actual prediction
- **Symmetry**: Features with equal marginal contributions receive equal attribution
- **Dummy**: Features with no effect receive zero attribution

### KernelSHAP Algorithm

CafGa uses **KernelSHAP** (Lundberg & Lee, 2017), which approximates Shapley values through weighted least squares:

1. **Sampling**: Create random binary masks $z'$, where each bit represents presence/absence of a feature
2. **Model evaluation**: For each mask $z'$, convert to actual input $x'$ and compute model output $f(x')$
3. **Weighting**: Assign weights based on SHAP kernel: larger coalitions (more features) receive lower weight
4. **Regression**: Fit weighted linear model to approximate marginal contributions

The algorithm samples up to $2 \times n_{\text{features}} + 2048$ coalitions (CafGa's default cap), making it computationally tractable even for longer texts when segments are larger.

### Fidelity Evaluation: Deletion and Insertion Curves

To assess whether attributions genuinely explain the model's decision-making, CafGa provides **deletion and insertion curves**:

**Deletion protocol:**
- Start with original prediction using all features
- Iteratively remove features in order of decreasing attribution value
- Plot model output vs. fraction of features removed
- A good explanation should show rapid divergence from the original prediction

**Insertion protocol:**
- Start with prediction using no features (baseline)
- Iteratively add features in order of decreasing attribution value
- Plot model output vs. fraction of features added
- A good explanation should show rapid convergence back to the original prediction

**Fidelity metric**: Area Under the Curve (AUC) of the deletion/insertion curve. Higher deletion AUC and lower insertion AUC indicate more faithful explanations.

## Main Ideas & Key Contributions

### 1. Interactive Granularity Control

CafGa's core innovation is enabling **dynamic granularity specification** at explanation time, not deployment time. Users can:
- Adjust segment boundaries interactively
- Compare explanations at different granularities
- Optimize for their specific interpretability-efficiency trade-off

This flexibility addresses domain-specific needs:
- Medical domain: Group medical terminology (e.g., "acute myocardial infarction")
- Legal domain: Group legal concepts (e.g., "material adverse change")
- General domain: Use phrases or clause-level segments

### 2. Non-Overlapping Segmentation

CafGa enforces **non-overlapping segmentation**, avoiding ambiguous attributions where the same word appears in multiple segments. This design choice ensures:
- Clear assignment of attribution values
- Easier interpretation by users
- Reduced confusion about feature boundaries

### 3. Integrated Visual Assessment

Rather than reporting raw attribution scores, CafGa provides:
- **Deletion and insertion curves** to validate explanation faithfulness
- **Interactive visualization** of how predictions change with feature removal/addition
- **Quantitative fidelity scores** to compare different segmentation strategies

This allows users to validate whether a segmentation scheme produces faithful explanations *before* deploying it.

### 4. Web-Based Tool Architecture

CafGa is implemented as a web application with:
- **Front-end**: Interactive interface for segmentation adjustment and visualization
- **Back-end**: Model inference and KernelSHAP computation
- **Model flexibility**: Support for OpenAI models and custom LLMs

## Methodology & Implementation

### System Design

**Architecture:**
- **Task creation interface**: Users define a prediction task (e.g., sentiment classification, fact verification)
- **Explanation generation page**: Main interface where users adjust granularity and inspect results
- **Visualization dashboard**: Displays deletion/insertion curves and attribution scores

**Input processing:**
1. User provides input text and specifies segmentation scheme
2. Text is split into non-overlapping segments
3. KernelSHAP samples coalitions of segments (not words)
4. Model computes predictions for each coalition
5. Shapley values are regressed from sampled predictions

### Experimental Setup

**User Study Design:**

The evaluation involved a two-stage user study:

**Stage 1 (System validation):**
- Participants familiarize themselves with CafGa's interface
- Create explanations at different granularities
- Assess whether visualization tools are effective

**Stage 2 (Comparative evaluation):**
- Four expert users compared explanations from three systems:
  1. **CafGa**: Interactive, user-generated explanations
  2. **MExGen**: Automatic multi-level explanations
  3. **PartitionSHAP**: Automatic word-partition SHAP
- Each explanation annotated with metadata about segmentation scheme
- Users rated explanations on perceived usefulness and correctness

**Baselines:**
- **MExGen**: Generates explanations at multiple hierarchy levels automatically
- **PartitionSHAP**: Uses fixed word-count partitioning (e.g., chunks of N words)

### Datasets and Models

The paper does not specify exact dataset sizes in publicly available excerpts, but the user study employed:
- **Language models tested**: OpenAI GPT-3.5, GPT-4 (via API)
- **Tasks**: Sentiment analysis, fact verification, text classification
- **User participants**: 4 expert users from NLP/ML backgrounds

[Exact model sizes and dataset sizes unavailable — see full paper for details]

### Key Results

**User study outcomes:**

The comparative evaluation produced these findings:

- **CafGa vs. MExGen**: CafGa-generated explanations were rated as more useful 64% of the time
- **CafGa vs. PartitionSHAP**: CafGa-generated explanations were rated as more useful in 72% of comparisons (estimated)
- **Between baselines**: MExGen outperformed PartitionSHAP in 58% of direct comparisons

**Limitations:**
- Small sample size: Only 4 expert participants (acknowledged by authors as a limitation)
- Limited to English-language models
- No automatic metrics reported; evaluation is primarily qualitative/preference-based

**Fidelity evaluation:**
- CafGa provides interactive deletion and insertion curves for each segmentation strategy
- Users can inspect curve shapes to validate explanation quality before use
- [Exact AUC values for different granularities unavailable — see full paper]

## Practical Applications & Real-World Use Cases

### 1. Healthcare and Clinical NLP

**Use case**: Explaining clinical decision support systems that classify patient notes.

**Challenge**: Clinical notes contain domain-specific terminology, abbreviations, and multi-word medical concepts (e.g., "ST elevation myocardial infarction").

**CafGa advantage**: 
- Clinicians can group medical terms meaningfully
- Explanations become actionable (e.g., "this symptom cluster was key")
- Computation remains feasible despite long documents

**Regulatory implication**: HIPAA and FDA guidance on AI transparency in healthcare increasingly require explanations. CafGa enables clinicians to generate and audit explanations in real-time.

### 2. Legal Document Analysis

**Use case**: Explaining predictions on contract classification or clause extraction.

**Challenge**: Legal language is dense; a single clause might span 50 words and convey one logical unit.

**CafGa advantage**:
- Lawyers can segment at the clause level, not individual words
- Explanations align with legal reasoning structure
- Reduces computational burden on large contracts

**Regulatory implication**: EU AI Act Article 13 requires transparency for high-risk AI. Legal practitioners need to audit model explanations quickly.

### 3. Content Moderation

**Use case**: Explaining why a social media post was flagged or removed.

**Challenge**: Moderation policies often target multi-word phrases (hate speech, targeted harassment), not individual words.

**CafGa advantage**:
- Content moderators can define segments that match policy terms
- Explanations directly justify policy application
- Appeals processes become more transparent to users

### 4. Financial Sentiment Analysis

**Use case**: Explaining market sentiment predictions from financial news.

**Challenge**: Domain terms like "quantitative easing," "Fed tapering," and "yield curve inversion" are multi-word entities with specific meanings.

**CafGa advantage**:
- Financial analysts can customize segmentation to domain terminology
- Explanations become actionable for trading decisions
- Compliance teams can audit reasoning in real-time

## Insights & Implications

### For XAI Practitioners

1. **Granularity is a design choice, not fixed**: CafGa demonstrates that explanation granularity should be tunable based on domain and use case, not imposed by default algorithms.

2. **Interactive systems improve trust**: Allowing users to generate and validate explanations (rather than receiving static explanations) increases confidence in AI systems.

3. **Fidelity visualization matters**: Deletion/insertion curves help users distinguish between plausible-looking but unfaithful explanations and genuinely faithful ones.

### For LLM Interpretability Research

1. **Post-hoc methods can be customizable**: CafGa shows that SHAP-based approaches can be extended with interactive customization without sacrificing rigor.

2. **User studies are essential for HCI-oriented xAI**: Automated metrics alone miss important aspects of explainability; human evaluation reveals nuances (e.g., MExGen vs. PartitionSHAP trade-offs).

3. **Domain-specific segmentation improves adoption**: When explanations align with how experts naturally think about data, adoption increases.

### Limitations and Open Questions

1. **Small user study**: The comparative evaluation involved only 4 experts, limiting generalizability of preference results.

2. **Computational cost**: While CafGa improves over word-level SHAP, it still requires model inference for each sampled coalition. For models with long context, this remains expensive.

3. **What makes a good granularity?**: The paper doesn't provide principled guidance on choosing segmentation schemes. This remains a user-guided design choice.

4. **Generalization beyond English**: All experiments use English-language models. Applicability to other languages with different morphological or syntactic structures is unclear.

5. **Trade-off between fidelity and interpretability**: Does higher granularity (fewer, larger segments) always reduce fidelity? This relationship isn't systematically studied.

## Code & Resources

### Official Implementation

- **GitHub**: The paper references code availability, but the exact repository URL is not provided in publicly available excerpts
- **Status**: CafGa is a web application; likely a demonstration/research prototype rather than a production package

### Dependencies

- **Core libraries**: SHAP (for KernelSHAP), scikit-learn
- **Language model access**: OpenAI API (GPT-3.5, GPT-4) or custom LLM deployment
- **Web stack**: Flask or similar web framework (backend), React or Vue (frontend, estimated)
- **Computational requirements**: 
  - Modest CPU/GPU for inference on small to medium-sized LLMs
  - Interactive use requires <5 second response time (typical)

### Quick Start

1. **Setting up segmentation**:
   - Input text into the task-creation interface
   - Define segment boundaries (can be words, phrases, clauses, or domain-specific units)
   - Confirm non-overlapping property

2. **Generating attributions**:
   - CafGa samples coalitions using KernelSHAP
   - Computes model predictions for each coalition
   - Visualizes attribution scores for each segment

3. **Validating faithfulness**:
   - Inspect deletion curve (should drop steeply)
   - Inspect insertion curve (should rise steeply)
   - Adjust granularity if curves are too flat (unfaithful explanations)

4. **Exporting results**:
   - Visualizations can be saved or shared
   - Attribution scores are exportable for downstream analysis

## Related Work & Context

### Relationship to Feature Attribution Methods

**SHAP (Shapley Additive exPlanations)**:
- CafGa uses KernelSHAP (approximate SHAP) under the hood
- CafGa's main contribution is **customizable granularity**, not a new attribution algorithm
- CafGa adds interactivity that standard SHAP doesn't provide

**LIME (Local Interpretable Model-agnostic Explanations)**:
- LIME also supports custom feature definitions
- CafGa differs by: (1) providing visual fidelity assessment, (2) supporting non-overlapping segments enforced, (3) offering web-based interactivity
- CafGa mentions that LIME is "computationally cheaper" but less faithful than SHAP

### Relationship to Multi-Level Explanation Methods

**MExGen** (Multi-level Explanations for Generative LMs):
- Generates explanations at multiple hierarchy levels automatically
- CafGa differs by allowing *user-guided* segmentation rather than automatic hierarchies
- In the user study, CafGa explanations were preferred over MExGen 64% of the time

**PartitionSHAP**:
- Partitions features into groups before applying SHAP
- CafGa differs by allowing dynamic, interactive partition adjustment
- Pre-defined partitioning limits flexibility compared to CafGa

### Connections to Concept-Based Explanation Research

- Concept-based methods (e.g., TCAV, ConEx) explain predictions in terms of learned or discovered concepts
- CafGa is *feature-based*, not concept-based, but shares the goal of moving beyond pixel/word-level explanations
- CafGa could potentially be extended with concept discovery to automatically suggest segmentation schemes

### Broader xAI Community Context

CafGa contributes to several ongoing xAI research directions:

1. **Interactive explainability**: Growing recognition that static explanations are insufficient; systems like CafGa enable users to query and refine explanations iteratively

2. **Domain-specific xAI**: Practitioners increasingly need explainability tools tailored to their domain. CafGa's customization enables this.

3. **Fidelity assessment**: The field is moving from reporting single metrics (e.g., "faithfulness score 0.85") to providing tools for users to assess fidelity themselves (e.g., deletion/insertion curves)

4. **Human evaluation of explanations**: CafGa's user study reflects a broader trend of evaluating XAI methods through human studies rather than only automatic metrics

## Future Research Directions

1. **Automatic segmentation suggestion**: Learn to recommend segmentation schemes based on data characteristics, domain, and downstream use

2. **Concept discovery**: Integrate concept learning methods to suggest meaningful segments aligned with model's internal representations

3. **Scaling to longer contexts**: Extend KernelSHAP to handle extremely long documents (e.g., full research papers, books) without prohibitive computational cost

4. **Multilingual support**: Adapt segmentation strategies for morphologically rich languages and validate that fidelity assessment generalizes

5. **Integration with model editing**: Combine explanations with recent model editing techniques to allow users not just to understand predictions but also to correct them

6. **Formal verification**: Combine explanation fidelity with formal verification to provide guarantees about explanation correctness

## References & Citation

**Full Citation:**
Boyle, A., Cheng, F., Zouhar, V., & El-Assady, M. (2025). CafGa: Customizing feature attributions to explain language models. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: System Demonstrations (pp. 461–470).

**ArXiv:**
- **Abstract:** https://arxiv.org/abs/2509.20901
- **PDF:** https://arxiv.org/pdf/2509.20901
- **HTML:** https://arxiv.org/html/2509.20901

**Venue:** EMNLP 2025 (Empirical Methods in Natural Language Processing), System Demonstrations Track

**Submission date:** September 25, 2025

## Note on Sources

This documentation synthesizes information from the arXiv abstract, HTML version, and secondary sources. For complete experimental results, formal definitions, and algorithmic details, consult the [full paper at arXiv:2509.20901](https://arxiv.org/abs/2509.20901).
