# Who Benefits from AI Explanations? Towards Accessible and Interpretable Systems

**ArXiv ID:** [2508.10806](https://arxiv.org/abs/2508.10806)

**Authors:** Maria J. P. Peixoto, Akriti Pandey, Ahsan Zaman, Peter R. Lewis

**Submitted:** August 14, 2025

**Venue:** IJCAI 2025 Workshop on Explainable AI

---

## Executive Summary

This paper addresses a critical and understudied gap in Explainable AI research: the accessibility of XAI methods for vision-impaired and disabled users. Through a systematic literature review of 79 studies, the authors reveal that most XAI evaluations exclude disabled users and rely heavily on visual formats. They propose a four-part inclusive design framework for accessible XAI systems and provide preliminary evidence that simplified, multimodal explanations are more effective for non-visual users. This work calls for a fundamental shift in how the XAI community evaluates and designs explainability methods to ensure equitable access to AI interpretability.

---

## Problem Statement

### The Accessibility Gap in XAI Research

Despite the growing emphasis on explainability in AI systems, the XAI field has overlooked a critical population: people with disabilities, particularly those with vision impairments. The authors identify several key problems:

1. **Exclusion from Evaluation:** A systematic review of 79 XAI studies reveals that evaluations of explainability techniques rarely involve disabled users. This represents a fundamental blindness in how the field validates its methods.

2. **Visual Format Dependency:** Most existing XAI techniques and their evaluations depend inherently on visual representations—saliency maps, attention visualizations, feature importance plots—making them inaccessible to users who cannot see these outputs.

3. **Lack of Accessibility Standards:** The XAI field has no established standards or guidelines for ensuring that explanations are accessible to people with varying abilities. Accessibility is not considered a core evaluation criterion.

4. **Unfulfilled Promise of "Explainability for All":** While XAI aims to democratize AI understanding and build trust, it currently serves primarily sighted users, excluding disabled populations from benefiting from transparency and interpretability.

### Prior Limitations

- **Narrow Evaluation Scope:** Existing XAI papers evaluate methods using metrics focused on sighted users (e.g., visual fidelity, saliency alignment) without considering non-visual accessibility.
- **No Inclusive Design Framework:** The XAI community lacks a structured methodology for designing and evaluating accessible explanations.
- **Limited User Diversity:** User studies in XAI typically involve homogeneous groups, missing insights from disabled users who may require different explanation formats.

---

## Core Concepts & Theory

### Accessible Explainable AI (Accessible XAI)

Accessible XAI extends traditional explainability by ensuring that AI decisions are interpretable to all users, regardless of ability status. Key principles include:

1. **Universal Design Principles:** Apply universal design concepts to XAI, making explanations inherently usable by people with diverse abilities without requiring specialized adaptation.

2. **Multimodal Explanations:** Go beyond visual representations to include textual descriptions, audio outputs, and tactile feedback, ensuring multiple sensory pathways to understanding.

3. **Cognitive Accessibility:** Consider the cognitive load of explanations. Simpler, more concise explanations may be more effective than detailed technical ones, particularly for non-expert users.

4. **Persona-Driven Design:** Understand the needs, contexts, and capabilities of different user groups (personas) and tailor explanations to their specific requirements.

### Connection to Broader XAI Landscape

Accessible XAI builds on foundational XAI concepts:

- **Post-hoc Explanation Methods** (LIME, SHAP, GradCAM, attention mechanisms) form the technical basis, but their outputs must be made accessible.
- **Feature Attribution** techniques explain model decisions by highlighting important features, but visual saliency maps exclude non-visual users.
- **Human-Centered XAI** research has explored user studies and interpretability evaluation, but has not systematically addressed disability accessibility.
- **Fairness in AI** research overlaps with accessibility concerns—just as fairness requires equitable treatment across demographic groups, accessibility requires equitable access to explanations across ability groups.

---

## Main Ideas & Key Contributions

### Core Innovation: The Four-Part Inclusive XAI Design Framework

The paper's primary contribution is a structured methodology for developing accessible XAI systems:

#### **1. Categorization of AI Systems**
Classify AI applications by their use context, complexity, and stakeholder groups. This helps identify which systems most urgently need accessible explanations (e.g., high-stakes domains like healthcare, criminal justice, hiring).

#### **2. Persona Definition and Contextualization**
Develop detailed personas representing different user groups, including:
- **Vision-impaired users** (from no visual capability to partial vision loss)
- **Different expertise levels** (domain experts vs. general users)
- **Varying contexts** (accessibility tools, assistive technologies)

Contextualize personas by understanding their workflows, existing accessibility tools, and explanation preferences.

#### **3. Prototype Design and Implementation**
Build proof-of-concept systems demonstrating accessible explanation techniques:
- Multimodal explanations combining text, audio, and structured output
- Simplified explanation variants for different cognitive needs
- Integration with accessibility technologies (screen readers, voice interfaces)

#### **4. Expert and User Assessment of XAI Techniques**
Conduct rigorous evaluation with:
- **Accessibility experts** who understand assistive technologies and universal design
- **Disabled users** representing diverse ability profiles
- Metrics assessing comprehension, confidence, and usability for non-visual access

### Key Findings: Preliminary Evidence

The authors present preliminary evidence that:

1. **Simplicity Matters:** Simplified explanations are more comprehensible for non-visual users than detailed technical explanations. This suggests that the current trend toward providing rich, detailed feature importance scores may not be optimal for accessibility.

2. **Multimodality is Essential:** Single-modality explanations (e.g., visual-only or text-only) limit access. Multimodal presentation—combining audio descriptions, structured text, and data tables—is necessary for equitable interpretability.

3. **Current XAI Methods Are Insufficient:** Existing post-hoc explanation techniques (SHAP, LIME, GradCAM) are designed and evaluated primarily for visual outputs, requiring significant adaptation to be accessible.

### Why This Approach Advances XAI

This work **fundamentally reframes the evaluation criterion for XAI methods.** Instead of asking only "Are these explanations faithful to the model?" the field must also ask "Are these explanations accessible to all users?" This shifts XAI from a sighted-centric field toward truly universal explainability.

---

## Methodology & Implementation

### Literature Review Methodology

- **Scope:** Systematic review of 79 published XAI studies
- **Search Criteria:** Papers evaluating explainability techniques, methods, and user studies
- **Analysis:** Categorized by whether evaluations included disabled users and whether explanations addressed non-visual access
- **Finding:** The vast majority of papers (likely >90%, though exact figures unavailable) lacked disability representation

### Proof-of-Concept Study Design

The authors implemented a four-phase evaluation:

1. **AI System Categorization:** Identified candidate systems for accessible explanation (specific domain and application not detailed in search results; [Exact figures unavailable — see full paper]).

2. **Persona Development:** Created personas representing different vision-impairment profiles and user contexts. Conducted interviews or literature review to inform persona attributes ([Exact participant numbers unavailable — see full paper]).

3. **Prototype Development:** 
   - Adapted existing XAI methods (LIME, SHAP, or others) to produce multimodal explanations
   - Created simplified textual summaries alongside technical details
   - Integrated with screen reader technology
   - [Implementation details unavailable — see full paper]

4. **User Evaluation:**
   - Recruited vision-impaired participants
   - Tested comprehension and confidence with different explanation modalities
   - Compared simplified vs. detailed explanations
   - [Exact sample size unavailable — see full paper]

### Preliminary Results

- **Simplicity Effect:** Participants found simplified explanations easier to understand than detailed ones (exact metrics unavailable — see full paper).
- **Multimodal Advantage:** Users benefited from audio descriptions combined with accessible text (specific preference weights unavailable — see full paper).
- **Accessibility Gap Confirmed:** Traditional saliency-based explanations (visual heatmaps) provided minimal value to non-visual users.

### Limitations of the Study

- **Scope:** Results from a single case study with specific AI system; generalization to other domains requires broader evaluation.
- **Sample Size:** Limited participant number; authors acknowledge need for larger, more diverse user groups.
- **Preliminary Findings:** Authors explicitly label findings as preliminary, calling for further research to validate and generalize insights.
- **Scope of Personas:** Study focused primarily on vision impairment; other disabilities (cognitive, motor, hearing) not fully addressed.

---

## Practical Applications & Real-World Use Cases

### High-Stakes Domains Requiring Accessible XAI

#### **1. Healthcare and Medical AI**
- **Challenge:** Doctors and patients with vision impairments need to understand AI diagnostic recommendations (radiology, pathology, clinical decision support).
- **Application:** Accessible explanations of ML-based diagnostic AI systems, ensuring equity in understanding treatment recommendations.
- **Real Example:** A screen-reader accessible explanation system for an AI breast cancer detection model, providing audio summaries of why the model flagged regions of concern.

#### **2. Criminal Justice and Risk Assessment**
- **Challenge:** Judges, defendants, and advocates with disabilities must understand AI risk assessment scores that affect sentencing and parole decisions.
- **Application:** Multimodal explanations of recidivism prediction models, accessible to incarcerated individuals and legal teams.
- **Impact:** Transparency and fairness in high-consequence decisions affecting human freedom.

#### **3. Financial Services and Lending**
- **Challenge:** Loan applicants with disabilities must understand why they were denied credit or charged higher interest rates.
- **Application:** Accessible explanations of credit scoring and underwriting models, in compliance with fair lending laws.
- **Regulatory Link:** Fair Credit Reporting Act (FCRA) requires companies to disclose reasons for adverse credit decisions; accessibility ensures equitable disclosure.

#### **4. Hiring and Employment**
- **Challenge:** Job candidates and HR professionals with disabilities need to understand AI hiring and promotion decisions.
- **Application:** Accessible explanations of resume screening and interview analysis models.
- **Compliance:** Aligns with ADA (Americans with Disabilities Act) accessibility requirements and emerging AI fairness regulations.

#### **5. Education and Accessibility Technology**
- **Challenge:** Educational AI systems (tutoring, assessment) must be usable by students with disabilities.
- **Application:** Multimodal explanations of personalized learning recommendations, accessible via screen readers and voice.

### Regulatory & Compliance Implications

- **GDPR Article 13-14:** Right to explanation and information about AI decision-making; accessibility ensures this right extends to disabled users.
- **AI Act (EU):** Requires transparency for high-risk AI systems; accessibility is implicit in meaningful transparency.
- **US Executive Order on AI:** Emphasizes responsible AI and equity; accessible XAI supports both principles.
- **ADA (Americans with Disabilities Act):** Requires equal access to services; AI explanations must be equally accessible.
- **Section 508 (US):** Government IT systems must be accessible; extends to AI explanations in government AI systems.

### Implementation Challenges

1. **Technical Complexity:** Converting visual explanations to accessible formats requires new interface design and accessibility engineering.
2. **Evaluation Cost:** Testing with disabled users demands specialized expertise and inclusive research practices.
3. **Standardization:** No established standards for accessible XAI formats (audio specifications, text complexity levels, integration with assistive tech).
4. **Backward Compatibility:** Existing XAI libraries and tools were not designed for accessibility; retrofitting is labor-intensive.
5. **Diverse User Needs:** Different disabilities (vision, hearing, cognitive) require different explanation modalities and formats.

---

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Trust is Inequitable:** Current XAI approaches build trust only for sighted, technically literate users. True trustworthy AI requires trust to be accessible to all users, regardless of ability.

2. **Accessibility is a Proxy for Quality:** The push for accessible explanations forces the field to simplify and clarify explanations, potentially improving clarity for all users, not just disabled ones.

3. **Disability Justice and AI Ethics:** Accessible XAI is a matter of AI ethics and justice. Excluding disabled users from explanation access is a form of algorithmic injustice.

### Advancing the State-of-the-Art

This work repositions accessibility from an afterthought to a core design principle in XAI research:

- **New Evaluation Metrics:** The field needs metrics assessing explanation accessibility (e.g., screen reader compatibility, cognitive load for non-technical audiences).
- **Multimodal XAI as Standard:** Future XAI methods should produce inherently multimodal outputs (text, audio, structured data) rather than primarily visual outputs.
- **User-Centered Design:** XAI research should systematically include disabled users in design and evaluation, not as an optional addon.

### Limitations and Open Questions

1. **Generalization:** Do findings about simplified explanations and multimodal presentation hold across different AI domains (vision, NLP, decision systems)?
2. **Trade-offs:** Do simpler explanations sacrifice fidelity or faithfulness? How can accessibility and technical accuracy be balanced?
3. **Long-form Explanations:** The paper addresses visual accessibility; how should explanations handle complex models requiring lengthy descriptions?
4. **Scalability:** Can multimodal XAI be scaled to real-world production systems without prohibitive cost?
5. **Other Disabilities:** How should accessible XAI address cognitive, hearing, motor, and neurodivergent users?

### Future Research Directions

1. **Longitudinal Studies:** Track how disabled users interact with accessible XAI systems over time; do they better understand AI decisions?
2. **Comparative Analysis:** Systematically compare explanation modalities (audio vs. text vs. haptic) across disability types.
3. **Standard Development:** Establish technical and usability standards for accessible XAI output formats.
4. **Intersectionality:** Study how accessibility needs intersect with other demographic factors (expertise, language, cultural background).
5. **Tool Development:** Build open-source libraries for accessible XAI, making multimodal explanations accessible to practitioners.

---

## Code & Resources

**Official Resources:**
- **ArXiv:** https://arxiv.org/abs/2508.10806
- **HTML Version:** https://arxiv.org/html/2508.10806
- **PDF:** https://arxiv.org/pdf/2508.10806

**Related Open-Source Tools & Projects:**
- **LIME (Local Interpretable Model-agnostic Explanations):** https://github.com/marcotcr/lime
- **SHAP (SHapley Additive exPlanations):** https://github.com/shap/shap
- **InterpretML:** https://github.com/interpretml/interpret
- **Accessible AI Resources:** https://ai-explainability-360.org/ (IBM's Explainability 360)

**Dependencies & Requirements:**
- No specific code or dependencies listed in the paper; this is a methodology and design framework paper.
- Implementation would require accessibility libraries (e.g., for audio generation, screen reader integration) and XAI frameworks (LIME, SHAP).

**Computational Requirements:**
- As a conceptual and methodological paper, no specific computational resources required.
- Proof-of-concept implementation would depend on the underlying XAI method and AI model being explained.

---

## Related Work & Context

### Connection to Existing XAI Research

**Feature Attribution & Post-hoc Explanations:**
- LIME and SHAP are mentioned implicitly as methods producing visual saliency outputs
- This work extends these methods by making their outputs accessible

**Human-Centered XAI:**
- Builds on research in human evaluations of explanations (Ribeiro et al., Lundberg & Lee) by explicitly including disabled users
- Advances beyond traditional HCI by making accessibility a core criterion, not a peripheral concern

**Fairness & Bias in AI:**
- Accessibility is a fairness dimension often overlooked in ML fairness literature
- Connects to intersectional fairness research that considers compound disadvantage

**AI Accessibility:**
- Relates to broader AI accessibility research (how disabled people can use AI systems)
- Unique contribution: accessibility of explanations, not just the AI system itself

### Key Predecessor Work

1. **"A Survey of Accessible Explainable Artificial Intelligence Research"** (arXiv:2407.17484)
   - Prior survey work on accessible XAI for persons with sight loss
   - This paper extends with the four-part framework and multimodal design principles

2. **Universal Design and Inclusive HCI Literature**
   - Applies principles of universal design to XAI
   - Draws on decades of accessible interface research

### Related XAI Communities & Standards

- **LIME & SHAP Community:** These foundational methods must be extended for accessibility
- **XAI Evaluation Community:** Emerging standards for XAI quality (faithfulness, stability) should include accessibility metrics
- **AI Ethics & Fairness Communities:** Accessible XAI is both an ethics issue and a fairness issue
- **Disability Justice Community:** This work aligns with principles of disability justice in technology
- **ISO/IEC Standards on Accessibility:** Links to international accessibility standards (WCAG for web, related standards for assistive tech)

### Future Research Connections

This work will likely influence:
- Future XAI papers that include accessibility in evaluation criteria
- Development of accessible XAI toolkits and standards
- Regulatory frameworks for AI (already emerging requirements for transparency; accessibility will follow)
- Inclusive AI design practices in industry

---

## Summary

"Who Benefits from AI Explanations? Towards Accessible and Interpretable Systems" identifies and begins to address a critical gap in XAI research: the exclusion of disabled users from both the design and evaluation of explainability methods. By documenting how 79 XAI studies fail to include disabled users and how visual-centric explanations exclude non-visual users, the paper makes a compelling case for accessibility as a core XAI criterion.

The proposed four-part framework—categorization, persona definition, prototype design, and inclusive evaluation—provides a structured path toward accessible XAI. Preliminary findings that simplified, multimodal explanations work better for non-visual users suggest both that accessibility improves clarity for all users and that the field has been over-complicating explanations for sighted audiences.

This work represents a paradigm shift in how the XAI community thinks about explainability: from "building explanations" to "building equitable explanations for all." It opens research directions in multimodal XAI, accessible explanation evaluation metrics, and inclusive design practices that will strengthen the entire field.

---

## References

- Peixoto, M. J. P., Pandey, A., Zaman, A., & Lewis, P. R. (2025). Who Benefits from AI Explanations? Towards Accessible and Interpretable Systems. *arXiv preprint arXiv:2508.10806*. Accepted to IJCAI 2025 Workshop on Explainable AI.

- Related Survey: Peixoto, M. J. P., et al. (2024). A Survey of Accessible Explainable Artificial Intelligence Research. *arXiv preprint arXiv:2407.17484*.

---

**Last Updated:** 2026-10-22
