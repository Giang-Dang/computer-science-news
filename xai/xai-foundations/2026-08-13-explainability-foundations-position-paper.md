# Position: Explainability Research Must Prioritize Foundations over Ad-hoc Methods

**Authors:** Michal Moshkovitz, Suraj Srinivas, Lesia Semenova, Nave Frost, Cyrus Rashtchian, Valentyn Boreiko, Shichang Zhang, Himabindu Lakkaraju, Cynthia Rudin, Jennifer Wortman Vaughan

**ArXiv ID:** [2607.14123](https://arxiv.org/abs/2607.14123)

**Publication:** ICML 2026 Position Paper Track (July 2026)

**Paper:** https://arxiv.org/pdf/2607.14123

**HTML Version:** https://arxiv.org/html/2607.14123v1

---

## Executive Summary

This position paper challenges the current trajectory of Explainable AI (XAI) research, arguing that despite the proliferation of explanation techniques, the field has prioritized method development over foundational principles. The authors present empirical evidence that explanations rarely influence real-world decision-making workflows because XAI research lacks clear problem formulations, rigorous evaluation frameworks, and systematic methods for integrating explanations into human-in-the-loop systems. The paper calls for a paradigm shift in XAI research toward addressing these foundational challenges and provides a checklist to guide future work.

---

## Problem Statement

### The XAI Paradox: Method Proliferation Without Impact

Despite the explosion of explainable AI techniques over the past decade—including LIME, SHAP, attention mechanisms, saliency maps, concept-based methods, and countless others—there is minimal empirical evidence that these explanations actually improve human decision-making or system outcomes in practice. This constitutes a fundamental disconnect between research output and practical impact.

### Key Issues in Current XAI Research

**1. Explanations Are Generated and Discarded**
In real-world workflows, explanations are often produced but never actually consulted or acted upon by end users. Analysis of recent research papers and practitioner surveys reveals that:
- Explanations lack clear relevance to user decision-making processes
- There is no established pipeline for explanation-driven feedback loops
- System design does not integrate explanations as active components

**2. Unclear Problem Formulations**
XAI papers typically define explainability vaguely:
- What aspect of the model should be explained (predictions, features, behaviors, fairness)?
- Who is the intended audience (data scientists, domain experts, non-technical stakeholders)?
- What specific decision or action should the explanation support?
- How should explanation success be measured?

**3. Underspecified Evaluation Objectives**
Current evaluation methodologies are often ad-hoc:
- Explanations are evaluated in isolation rather than in the context of end-to-end human-in-the-loop workflows
- Metrics focus on technical properties (faithfulness, stability, local accuracy) rather than actual utility to users
- Few studies validate that explanations meaningfully improve user decision-making or system performance

**4. Absence of Integration Methodologies**
The field lacks systematic approaches for:
- Embedding explanations into interactive systems where users can iteratively refine their understanding
- Closing feedback loops where explanation insights inform model improvements
- Designing human-centered workflows where explanations drive actionable changes

### Historical Context

The XAI research community has adopted an implicit assumption: *better explanations → more trustworthy AI → improved outcomes*. However, empirical evidence increasingly suggests this causal chain is not automatic and requires deliberate system design.

---

## Core Concepts & Theory

### Foundational Concepts in Explainability

**Explainability vs. Transparency:**
- **Transparency** refers to the inherent interpretability of a model's structure and parameters
- **Explainability** refers to the generation of human-understandable descriptions of model behavior
- The paper argues that XAI research conflates these concepts, leading to solutions that are neither transparent nor effectively explain

**The Explanation-Action Gap:**
The central theoretical insight is that explanations alone do not guarantee actionable insights. An explanation is only useful if it:
1. Accurately describes the model's behavior (faithfulness)
2. Is comprehensible to the intended audience (interpretability)
3. Identifies actionable aspects the user can control or modify (agency)
4. Integrates into the decision-making workflow (integration)

**Types of Stakeholders and Their Explanation Needs:**

| Stakeholder | Primary Need | Example Use Case |
|---|---|---|
| Model Developer | Debugging model errors | "Why did my model fail on this input?" |
| Data Scientist | Hyperparameter tuning | "Which features matter most for predictions?" |
| Domain Expert | Domain validation | "Does the model's reasoning align with domain knowledge?" |
| Regulatory/Compliance | Demonstrating fairness/legality | "Is the model fair across demographic groups?" |
| End User | Understanding AI decisions | "Why did the system recommend this action?" |

Each stakeholder has fundamentally different explanation needs, yet XAI methods are often evaluated as if they serve universal purposes.

### Theoretical Frameworks for Evaluation

The paper argues that XAI research must adopt more rigorous theoretical frameworks:

**1. Human-in-the-Loop Systems Theory**
- Explanations should be evaluated within the context of interactive human-AI systems
- Metrics should measure the quality of human-AI collaboration, not just explanation properties
- Research should study how explanations affect human decision-making over time

**2. User-Centered Design Principles**
- Explanation design should begin with clear user needs and tasks
- Evaluation should involve actual users performing realistic tasks
- Iterative refinement should incorporate user feedback

**3. End-to-End System Evaluation**
- Explanations should be evaluated in the context of the full decision pipeline
- Metrics should measure downstream impact (e.g., improved decisions, faster workflows, better outcomes)
- Explanations should close feedback loops enabling model improvement

---

## Main Ideas & Key Contributions

### 1. Empirical Evidence of the Explanation-Action Gap

The authors conducted systematic analysis of:

**ICML, NeurIPS, and ICLR XAI Papers (2020-2026):**
- Most papers focus on explanation method development
- Few papers include user studies validating explanation utility
- Rare papers demonstrate explanations actually improving real-world outcomes
- Evaluation is predominantly computational, not human-centered

**Practitioner Survey Results:**
- XAI practitioners report that explanations rarely influence production systems
- Common pain point: "We generate explanations, but nobody uses them"
- Explanations are often generated for compliance rather than actionable insight
- Integration with existing workflows is cited as a major challenge

### 2. Root Causes of the Explanation-Action Gap

**Foundational Shortcomings:**

**A. Unclear Problem Formulation**
- Researchers develop explanation methods without specifying what problem they solve
- The "who, what, why" of explanations is rarely articulated
- Methods are evaluated against synthetic benchmarks rather than real user needs

**B. Fragmented Stakeholder Landscape**
- XAI methods treat all users as identical
- No systematic approach to designing explanations for specific stakeholders
- Research ignores that different stakeholders have fundamentally different information needs

**C. Isolated Evaluation**
- Explanations are evaluated in laboratories with synthetic tasks
- Evaluation rarely involves representative users performing realistic workflows
- Human studies are rare and often limited in scale

**D. Missing Integration Infrastructure**
- No standardized pipelines for incorporating explanations into production systems
- Lack of best practices for human-AI interaction design
- No frameworks for closing feedback loops where explanations drive model improvement

### 3. A Call for Foundational Research

Rather than developing yet another explanation method, the field must prioritize:

**Problem Definition and Scoping**
- Clearly specify WHO needs explanations (specific stakeholder roles)
- Define WHAT aspects of the system require explanation (outputs, features, behaviors, fairness)
- Articulate WHY explanations are needed (debugging, compliance, user trust, model improvement)
- Specify the CONTEXT in which explanations will be used

**Rigorous Evaluation Methodologies**
- Conduct human-subject studies with representative users
- Measure downstream impact on decision quality and system performance
- Evaluate explanations in realistic, end-to-end workflows
- Report quantitative metrics on explanation utility, not just technical properties

**System Integration**
- Design human-in-the-loop systems where explanations actively guide decisions
- Implement feedback mechanisms where user insights from explanations improve models
- Create interaction patterns where explanations are naturally incorporated into workflows
- Develop platforms that make it easy to deploy explanation-integrated systems

### 4. A Checklist for Future XAI Research

The paper proposes a practical checklist for XAI researchers to ensure foundational rigor:

**Before Developing Your Explanation Method, Ask:**

1. **Problem Formulation**
   - [ ] Who specifically needs this explanation? (role, expertise level)
   - [ ] What decision or action does this explanation support?
   - [ ] How is explanation success measured in your use case?
   - [ ] Why is this explanation better than existing alternatives?

2. **User and Stakeholder Considerations**
   - [ ] Have you identified and involved representative stakeholders?
   - [ ] Do you understand their current workflow and information needs?
   - [ ] Have you validated that your explanation addresses their needs?
   - [ ] How does explanation design differ across stakeholder types?

3. **Evaluation and Validation**
   - [ ] Does your evaluation include human-subject studies?
   - [ ] Are participants representative of actual users?
   - [ ] Do users perform realistic tasks with the explanation?
   - [ ] Do you measure downstream impact on decision quality?
   - [ ] Can you quantify the value of the explanation?

4. **System Integration**
   - [ ] How will explanations integrate into existing workflows?
   - [ ] What infrastructure is needed to deploy explanations in production?
   - [ ] How do explanations close feedback loops for model improvement?
   - [ ] Can users act on the explanation to modify outcomes?

5. **Reproducibility and Generalization**
   - [ ] Can your approach generalize beyond your specific use case?
   - [ ] Have you tested on multiple datasets and model types?
   - [ ] Are your results reproducible by other researchers?
   - [ ] What are the limitations and failure modes?

---

## Methodology & Implementation

### Research Approach

The paper employs multiple methodologies:

**1. Systematic Literature Review**
- Analyzed 200+ XAI papers from top-tier venues (ICML, NeurIPS, ICLR)
- Categorized papers by research type (method development, evaluation, application)
- Quantified fraction of papers including human evaluation

**2. Practitioner Survey**
- Surveyed machine learning practitioners deployed AI systems in production
- Identified common challenges in deploying explanations
- Documented actual use cases and integration patterns

**3. Case Study Analysis**
- Examined real-world deployments where explanations succeeded vs. failed
- Identified patterns in successful explanation-integrated systems
- Documented lessons learned from production experiences

### Key Findings

**Finding 1: Rare Human Evaluation**
- Only ~15% of XAI papers from ICML/NeurIPS include human-subject studies
- Of those, most involve brief studies with limited participants
- Few measure downstream impact on actual decision outcomes

**Finding 2: Stakeholder Mismatch**
- XAI methods often serve one stakeholder (e.g., model developers)
- Deployed systems require explanations for different stakeholders (e.g., end users)
- This mismatch leads to explanations being generated but not used

**Finding 3: Integration is Underestimated**
- Practitioners identify system integration as the primary barrier to explanation adoption
- Infrastructure for deploying explanations in production is immature
- Feedback loops where explanations improve models are rare

### Implementation Considerations

**For Practitioners Adopting Explanations:**

1. **Stakeholder Analysis First**
   - Map all stakeholders who interact with your AI system
   - Interview each group about their information needs and decisions
   - Design explanations specifically for each stakeholder type
   - Example: healthcare system needs different explanations for clinicians vs. patients vs. hospital administrators

2. **User Study Integration**
   - Before deploying explanations, conduct user studies with representative stakeholders
   - Use realistic tasks and datasets, not synthetic benchmarks
   - Measure whether explanations improve decision quality
   - Iterate on design based on user feedback

3. **Feedback Loop Design**
   - Design mechanisms for users to communicate insights from explanations back to data science teams
   - Implement processes where explanation-derived insights improve models
   - Track metrics on explanation value over time
   - Example: radiologists using explanations to identify systematic model weaknesses

4. **Workflow Integration**
   - Embed explanations directly into tools practitioners already use
   - Design explanation UX that doesn't disrupt existing workflows
   - Make it easy for users to act on explanation insights
   - Monitor adoption rates and iterate on design

---

## Practical Applications & Real-World Use Cases

### Healthcare: Diagnosis Support Systems

**Challenge:** Clinicians must trust AI recommendations to integrate them into patient care workflows.

**Current XAI Approach (Failing):**
- Hospitals deploy explainability methods (saliency maps, attention visualizations)
- Clinicians report explanations don't match their clinical reasoning
- Explanations often identify non-clinical features (e.g., artifacts) that don't inform decisions
- Result: explanations are generated but ignored

**Foundational Approach (Succeeding):**
- Interview clinicians to understand their diagnostic reasoning and information needs
- Design explanations to highlight clinically relevant features
- User study with clinicians on realistic cases to validate explanation quality
- Implement feedback loop: clinicians report when explanations disagree with clinical knowledge
- Use feedback to refine model and explanation method
- Result: explanations become trusted clinical decision support

### Finance: Loan Approval Systems

**Challenge:** Regulatory compliance requires explainability; fairness auditing requires identifying disparities.

**Current XAI Approach (Failing):**
- Deploy SHAP or similar to generate feature importance explanations
- Explanations show which features influenced decisions but don't explain *why* features matter
- Compliance teams struggle to audit for fairness
- Result: regulatory box-checking without meaningful fairness improvement

**Foundational Approach (Succeeding):**
- Identify stakeholders: loan officers, compliance teams, applicants, regulators
- Design different explanations for each: loan officers need decision rationale; compliance teams need fairness audit info; applicants need clear, understandable reasons
- User studies with loan officers to validate explanations improve lending decisions
- Fairness audit: explicitly test whether explanations reveal discriminatory patterns
- Feedback loop: compliance team reports disparities → model team investigates → model improved
- Result: explanations enable both better decisions and genuine fairness improvement

### Autonomous Systems: Safety-Critical Decisions

**Challenge:** Autonomous vehicles, robots, and medical devices must make critical decisions; explanations are essential for safety validation.

**Current XAI Approach (Failing):**
- Complex explanation methods (attention, concept activation vectors) overwhelm safety engineers
- Explanations often don't match system's actual decision logic
- Safety teams can't audit whether explanation algorithms are faithful
- Result: explanations inspire false confidence rather than genuine understanding

**Foundational Approach (Succeeding):**
- Interview safety engineers about their needs: can they audit the system? Can they identify failure modes? Can they improve safety?
- Design simple, interpretable explanations that can be rigorously validated
- Formal verification: prove that explanation method is faithful to model
- Safety-critical evaluation: can safety engineers use explanations to identify dangerous edge cases?
- Feedback loop: safety issues discovered via explanations → immediate model updates
- Result: explanations genuinely improve system safety

### Content Moderation: Platform Safety

**Challenge:** Platforms must moderate content at scale while respecting user rights; users need to understand moderation decisions.

**Current XAI Approach (Failing):**
- Systems generate explanations but don't explain clearly enough for appeals
- Users don't understand *why* content was removed
- No feedback mechanism for users to dispute incorrect decisions
- Result: frustrated users, potential discriminatory moderation patterns

**Foundational Approach (Succeeding):**
- Design explanations for users: why was this specific content flagged?
- Design explanations for auditors: systematic fairness analysis across demographics
- User study: do explanations help users understand and accept moderation decisions?
- Appeal process: users can contest decisions and provide feedback
- Feedback loop: contentious decisions analyzed; patterns inform model improvements
- Result: transparent moderation, fair outcomes, improved user trust

### Regulatory Compliance: EU AI Act, FDA

**Challenge:** Regulators require explainability evidence; compliance requires documenting system behavior.

**Current XAI Approach (Failing):**
- Companies deploy explanation methods and claim compliance
- Regulators question whether explanations are actually faithful
- No standardized criteria for what constitutes "sufficient" explanation
- Result: regulatory uncertainty, potential compliance failures

**Foundational Approach (Succeeding):**
- Clearly document *why* explanations are required (specific regulatory requirement)
- Specify *what* must be explained (model decisions, fairness properties, failure modes)
- Define *who* needs explanations (regulators, auditors, affected users)
- Provide *rigorous evidence* that explanations are faithful and useful
- Regular third-party audits: independent verification that explanations meet standards
- Result: genuine regulatory compliance, defensible explanations

---

## Insights & Implications

### For the Research Community

**1. The Time for Method Development Has Passed**
While innovative explanation methods are intellectually interesting, the field has reached a point of diminishing returns on new algorithms. The bottleneck is not method innovation but rather:
- Understanding user needs
- Designing explanations for specific stakeholders and use cases
- Rigorously evaluating explanation utility
- Integrating explanations into production systems

**2. Human-Centered Research Is Essential**
The future of XAI lies in rigorous human-computer interaction research, not better statistical methods. This requires:
- Conducting substantial user studies with representative participants
- Measuring downstream impact on decision quality, fairness, and trust
- Iteratively refining explanations based on user feedback
- Publishing negative results and failures (currently underrepresented)

**3. Interdisciplinary Collaboration is Necessary**
Solving the XAI problem requires expertise beyond machine learning:
- Human-computer interaction (HCI) for interface design
- Cognitive science for understanding how humans process explanations
- Organizational behavior for understanding workflow integration
- Domain expertise (medicine, law, finance) for stakeholder needs
- Social science for understanding fairness and accountability

**4. Evaluation Standards Must Evolve**
Venues like ICML, NeurIPS, and ICLR should establish standards for XAI research:
- Require clear problem formulation and stakeholder identification
- Mandate human evaluation for papers claiming user-facing benefits
- Encourage publication of negative results and failed approaches
- Recognize that good XAI research may not be as novel as new methods

### For Practitioners

**1. Start with Stakeholder Analysis, Not Methods**
Before selecting or developing an explanation method:
- Interview stakeholders to understand their needs and decisions
- Map the workflow where explanations will operate
- Define success metrics (improved decisions? regulatory compliance? user trust?)
- Only then select methods

**2. Invest in User Research**
- Conduct formative user studies to validate explanation design
- Run pilot deployments with real users before full rollout
- Measure whether explanations actually improve outcomes
- Iterate based on user feedback

**3. Design for Integration**
- Build explanations into tools practitioners already use
- Make explanations easy to act on
- Implement feedback loops where insights improve models
- Monitor adoption and iterate on design

**4. Plan for Maintenance**
- Explanations can become outdated as models evolve
- Maintain processes for validating that explanations remain faithful
- Update explanations when model behavior changes significantly
- Communicate changes to users

### Broader Implications for AI Trust and Governance

**The Trust Paradox:**
Explanations can inspire false confidence. A well-designed explanation method can make a flawed model *seem* trustworthy, actually *reducing* appropriate skepticism. Solutions:
- Combine explanations with rigorous model auditing
- Use explanations to identify model weaknesses, not just justify decisions
- Maintain human oversight and critical judgment

**Accountability Requires Explainability:**
As AI systems make consequential decisions (hiring, lending, criminal justice), explainability becomes essential for accountability. However:
- Explanations must be faithful to actual decision logic, not post-hoc justifications
- Users must have agency to act on explanations (approve/appeal decisions)
- Feedback mechanisms must close loops where explanation insights improve decisions

**The Role of Transparency:**
True system transparency—clear documentation of model architecture, training data, design choices—may be more valuable than complex explanation methods. Solutions:
- Prioritize transparency over complex explainability methods
- When complex models are necessary, ensure explanations are validated against transparent baselines
- Build increasingly interpretable models rather than explaining uninterpretable ones

---

## Code & Resources

### Official Paper and Materials

- **ArXiv Paper:** [https://arxiv.org/abs/2607.14123](https://arxiv.org/abs/2607.14123)
- **PDF Full Text:** [https://arxiv.org/pdf/2607.14123](https://arxiv.org/pdf/2607.14123)
- **HTML Version:** [https://arxiv.org/html/2607.14123v1](https://arxiv.org/html/2607.14123v1)
- **ICML 2026 Proceedings:** Position Paper Track, Seoul, South Korea

### Referenced XAI Methods and Frameworks

The paper references and critiques numerous XAI approaches:

**Classic Feature Attribution Methods:**
- [LIME (Local Interpretable Model-agnostic Explanations)](https://arxiv.org/abs/1602.04938) - Ribeiro, Singh, Guestrin (2016)
- [SHAP (SHapley Additive exPlanations)](https://arxiv.org/abs/1705.07874) - Lundberg & Lee (2017)
- [Integrated Gradients](https://arxiv.org/abs/1703.01365) - Sundararajan et al. (2017)

**Attention-Based Explanations:**
- Attention Visualization in Transformers
- Saliency Maps for CNNs
- Concept Activation Vectors (TCAV) - [Kim et al. (2018)](https://arxiv.org/abs/1711.11572)

**Counterfactual and Causal Explanations:**
- Counterfactual Explanations - [Wachter et al. (2017)](https://arxiv.org/abs/1706.07552)
- Causal Inference approaches for explainability

### Related Position Papers and Critical Reviews

**Complementary Critical Perspectives:**
- "Beyond Explainable AI: An Overdue Paradigm Shift" (2602.24176) - Examines fundamental limitations and proposes post-XAI research directions
- "In Defence of Post-hoc Explainability" (2412.17883) - Counterargument defending post-hoc explanation methods
- [Explainability Needs Formalization](https://arxiv.org/abs/2409.14590) - Formal theoretical frameworks for explainability

### Practical Tools and Frameworks

**For Implementing Explanation Systems:**
- [LIME Python library](https://github.com/marcotcr/lime) - GitHub
- [SHAP Python library](https://github.com/slundberg/shap) - GitHub
- [Captum (PyTorch model interpretability)](https://captum.ai/) - Facebook Research
- [InterpretML](https://interpret.ml/) - Microsoft

**For User Study Design:**
- Nielsen Norman Group: UX Research methods for explanation evaluation
- ACM CHI guidelines for human-computer interaction research
- Guidelines for conducting user studies in explainable systems

**For System Integration:**
- [Explainability requirements by domain](https://www.iso.org/standard/78626.html) - ISO standards on AI transparency
- EU AI Act compliance documentation
- FDA guidance on software as a medical device (SaMD) explainability

### Recommended Reading List

**Foundational Papers on XAI:**
- [The Mythos of Model Interpretability](https://arxiv.org/abs/1606.03490) - Lipton (2016)
- [Definitions, methods, and applications in interpretable machine learning](https://arxiv.org/abs/1901.04592) - Murdoch et al. (2019)
- [Towards A Rigorous Science of Interpretable Machine Learning](https://arxiv.org/abs/1702.08608) - Doshi-Velez & Kim (2017)

**Human-Centered Explainability:**
- "Towards Human-centered Design of Explainable AI" (2410.21183) - Survey of empirical XAI studies
- "Beyond Technocratic XAI: The Who, What & How in Explanation Design" (2508.09231) - Design thinking for explanations

**Evaluation Methodologies:**
- "Evaluating Feature Importance Estimates" - Comparison of explanation method properties
- "How Much Should I Trust You?" - Validation methods for local explanations

### Computational Requirements

This is a position paper focused on critique and framework proposal rather than computationally intensive methods. However, implementing the recommended research directions requires:

- **User Study Infrastructure:** Platforms for conducting human-subject studies (e.g., Prolific, MTurk, lab-based studies)
- **Workflow Integration:** Engineering effort to embed explanations in production systems
- **Evaluation Frameworks:** Custom evaluation scripts to measure explanation utility in context

---

## Related Work & Context

### How This Paper Connects to the Broader XAI Landscape

**Relationship to Major XAI Communities:**

**1. Feature Attribution Methods (LIME, SHAP, Integrated Gradients)**
- **Critique:** These methods are technically sound but their real-world utility is unclear
- **Finding:** They are often deployed without clear stakeholder needs or integration strategy
- **Implication:** Method improvements won't solve the fundamental problem; focus must shift to deployment and human factors

**2. Attention-Based Interpretability**
- **Critique:** Attention weights are often not faithful to model behavior
- **Finding:** Explanations based on attention don't necessarily improve user understanding
- **Implication:** Need rigorous validation that attention-based explanations are useful

**3. Mechanistic Interpretability (Circuits, Sparse Autoencoders)**
- **Complement:** This work on model internals is valuable but addresses a different problem
- **Note:** Circuit analysis helps researchers understand models but may not directly serve end-user explanation needs
- **Implication:** Mechanistic insights should inform explanation design, not replace stakeholder-centered approaches

**4. Fairness and Algorithmic Accountability**
- **Strong Connection:** This paper argues explainability must serve fairness auditing and accountability
- **Key Insight:** Generic explanations often fail at revealing fairness issues; must be designed for audit purposes
- **Implication:** XAI research should collaborate with fairness research to design explanations that detect bias

**5. Regulatory and Legal Perspectives on AI**
- **Compliance Focus:** EU AI Act, FDA guidance, SEC transparency rules all demand explainability
- **Gap:** Regulatory requirements are specific (fairness, safety, legality) but XAI methods are generic
- **Implication:** Explainability methods must be designed for regulatory needs, not vice versa

### Recent Developments in the Field (2025-2026)

**Emerging Trends Supporting This Position:**

1. **Increased Focus on Human-in-the-Loop AI (2025-2026)**
   - Growing recognition that explanation quality depends on system integration
   - More papers incorporating human evaluation
   - Growing interest in explanation user interfaces and interaction design

2. **Regulatory Pressure (2024-2026)**
   - EU AI Act enforcement creating real-world explainability requirements
   - FDA guidance on AI/ML transparency for medical devices
   - SEC regulations on algorithmic trading transparency
   - These regulations demand *specific* types of explanations, not generic ones

3. **Practitioner Feedback (2025-2026)**
   - Industry reports documenting the "explanation-action gap"
   - Companies investing in explanation deployment infrastructure
   - Recognition that method innovation alone doesn't solve deployment challenges

4. **Meta-Research on XAI (2025-2026)**
   - Systematic reviews questioning XAI method effectiveness
   - Studies showing human studies rare in top-tier venues
   - Analysis of whether explanations improve decision quality

### Connections to Other Foundational XAI Critiques

**"Beyond Explainable AI: An Overdue Paradigm Shift" (2602.24176)**
- Similar critique of XAI limitations but more philosophical/theoretical
- Proposes post-XAI paradigm rather than foundational improvements to XAI
- This paper argues foundational improvements to XAI research are necessary before moving beyond XAI

**"In Defence of Post-hoc Explainability" (2412.17883)**
- Counter-argument defending post-hoc explanations as useful
- Argues explainability is inherently a posteriori and that's acceptable
- This paper acknowledges post-hoc explanations can work if properly integrated and evaluated

**"Explainability Needs Formalization" (2409.14590)**
- Focuses on theoretical formalization of explainability concepts
- Complementary to this paper's focus on practical methodology
- Together, argue for both theoretical rigor and practical validation

### Where XAI Research Should Go Next

**According to This Paper:**

1. **Move Beyond Method Development**
   - Shift resources from new explanation algorithms to human-centered research
   - Prioritize user studies over novel mathematical methods
   - Recognize that best XAI paper might not propose new algorithm

2. **Invest in Integration Infrastructure**
   - Develop platforms for easily deploying explanations in production
   - Create open standards for explanation formats
   - Build tools for human-in-the-loop feedback loops

3. **Establish Evaluation Standards**
   - Venues should require human evaluation for user-facing XAI work
   - Metric should include downstream impact, not just technical properties
   - Encourage negative results and failure analysis

4. **Interdisciplinary Collaboration**
   - HCI researchers should lead explanation design
   - Domain experts should guide stakeholder requirements
   - Practitioners should validate approaches in real deployments

### Open Research Questions

Raised by This Position Paper:

1. **How can we systematically design explanations for different stakeholders?**
   - What frameworks guide stakeholder-specific explanation design?
   - How do explanation needs differ across roles and domains?

2. **How can we evaluate explanation utility rigorously?**
   - What metrics capture whether explanations improve decisions?
   - How do we measure downstream impact vs. technical properties?

3. **How can we integrate explanations into workflows?**
   - What UX patterns make explanations actionable?
   - How do we design for adoption and avoid explanation avoidance?

4. **How can explanations improve AI systems?**
   - What feedback mechanisms allow explanations to drive model improvements?
   - How do we close the loop between explanation insights and model updates?

5. **Can simple explanations be sufficient?**
   - Are complex explanation methods necessary, or do simpler approaches work better?
   - When is transparency (model simplicity) preferable to explainability (post-hoc explanation)?

---

## Conclusion

This position paper represents a significant inflection point in XAI research. After years of focus on explanation method development, the field must recognize that **having better algorithms is not the bottleneck—having systematic approaches to understanding user needs, designing explanations for specific stakeholders, rigorously evaluating utility, and integrating into production systems is.**

The paper's core contribution is not proposing a new explanation method but rather proposing a new research agenda: foundational work on XAI integration, human-in-the-loop systems, and practical deployment. This shift from method innovation to foundational rigor will ultimately determine whether XAI succeeds in its central promise: making AI systems genuinely more trustworthy and understandable.

The checklist provided offers a practical tool for researchers and practitioners to ensure future XAI work addresses foundational concerns. The case studies demonstrate that when XAI is designed with clear stakeholder needs and rigorously evaluated in context, it can generate real value. The call to action is clear: **the future of XAI lies not in more sophisticated algorithms, but in more rigorous, human-centered, integrated approaches to explanation.**

---

## Citation

```bibtex
@inproceedings{moshkovitz2026position,
  title={Position: Explainability Research Must Prioritize Foundations over Ad-hoc Methods},
  author={Moshkovitz, Michal and Srinivas, Suraj and Semenova, Lesia and Frost, Nave and Rashtchian, Cyrus and Boreiko, Valentyn and Zhang, Shichang and Lakkaraju, Himabindu and Rudin, Cynthia and Wortman Vaughan, Jennifer},
  journal={arXiv preprint arXiv:2607.14123},
  year={2026}
}
```
