# Explainable AI Isn't Enough! Rethinking Algorithmic Contestability

**ArXiv ID:** 2605.16041  
**Submission Date:** May 15, 2026  
**Subfield:** Algorithmic Contestability, Human-Centered XAI, Fairness & Accountability  

---

## Executive Summary

This paper fundamentally reframes how we think about explainability in high-stakes algorithmic decision systems. While explainable AI has focused on algorithmic recourse—helping individuals modify their features to obtain desired outcomes—this work argues that algorithmic **contestability**—the ability to challenge and overturn erroneous algorithmic decisions—deserves equal or greater attention despite receiving far less research focus. The paper provides an operational framework identifying three types of evidence that warrant decision reversal: predictive multiplicity, incorrect feature values, and neglected overruling evidence. This work bridges critical gaps between technical XAI methods and the legal/ethical requirements for trustworthy AI systems.

---

## Problem Statement

### The Recourse vs. Contestability Divide

Current explainability research has primarily focused on **algorithmic recourse**—enabling individuals to change their circumstances (e.g., improving credit scores, adjusting loan application features) to obtain favorable decisions from algorithmic systems. However, this approach operates under a fundamental assumption: *the system's decision logic is sound, and individuals need to adapt to it*.

In reality, algorithmic decisions are frequently **erroneous**. High-stakes domains like lending, employment, criminal justice, healthcare triage, and insurance involve systems that can make mistakes due to:
- Incorrect or outdated input data about individuals
- Model biases that the decision maker (judge, loan officer, HR manager) considers ethically unacceptable
- Conflicting predictions from equally valid models trained on the same data (predictive multiplicity)
- Overlooked or systematically suppressed evidence that should override the algorithmic recommendation

### The Legal and Ethical Imperative

Recent regulations and human rights frameworks—including the EU AI Act, the US AI Bill of Rights, and evolving case law—increasingly recognize that affected individuals have:
1. **The right to explanation** (notice of how decisions are made)
2. **The right to contestation** (the ability to challenge decisions they believe are unjust)
3. **The right to human review** (meaningful appeal processes)

Yet current XAI methods fail to adequately support contestation. Standard techniques like counterfactual explanations, LIME, and anchor explanations show what *could* change a decision, but they don't establish grounds for believing a specific decision *should* be reversed.

### Limitations of Existing XAI Methods

The paper demonstrates that even sophisticated explanation methods struggle to support contestability:

- **Counterfactual explanations** (e.g., "If your income were $10K higher, you'd be approved") suggest conditions under which the decision would change, but don't establish that these conditions apply to the individual.
- **LIME and Anchors** work locally around an individual's data point, identifying minimal feature sets that preserve the decision, but can't detect when the model's behavior is problematic beyond the immediate neighborhood.
- **Standard fairness audits** reveal aggregate disparities but don't provide individual-level evidence of unfair treatment in specific cases.
- **Model explanations** (feature importance, attention weights) don't validate whether the features being used are even correct in the individual's case.

---

## Core Concepts & Theory

### 1. Defining Algorithmic Contestability

**Algorithmic contestability** is defined as the ability of an affected individual to obtain and present evidence that warrants overturning an algorithmic decision according to the decision maker's own ethical standards and institutional rules.

This contrasts with recourse in a crucial way:

| Aspect | Recourse | Contestability |
|--------|----------|-----------------|
| **Underlying Assumption** | Decision is valid; individual should adapt | Decision may be invalid; system should reconsider |
| **Goal** | Change decision through behavioral change | Overturn decision through evidence of error |
| **Actionability** | Individual modifies their circumstances | System revises its assessment |
| **Burden of Proof** | Individual demonstrates improved qualification | Individual demonstrates decision error |

### 2. The Three Types of Contestation Evidence

The paper identifies three categories of evidence that warrant decision reversal, grounded in ethical reasoning and legal precedent:

#### Evidence Type 1: Predictive Multiplicity

**Definition:** Multiple models with equally strong empirical and theoretical support make conflicting predictions for the same individual.

**Why it matters:** When predictive multiplicity exists, the decision maker cannot credibly claim the decision is determined by the "correct" model. Different models might make contradictory recommendations despite being equally justified by available data.

**Example:** A credit approval model trained on historical lending data predicts default risk differently than a model trained on alternative credit bureau data, because the training sets have different demographic compositions. Both models fit their training data equally well, but they disagree on the individual applicant. This disagreement signals that the data itself—not model performance—is driving the divergence, suggesting the decision should not be deterministic.

**Contestability mechanism:** Predictive multiplicity evidence obligates the decision maker to explain which model they're using and why that particular model should override others, making the choice contestable.

#### Evidence Type 2: Incorrect Feature Values

**Definition:** The individual's input data used by the system is factually wrong.

**Why it matters:** Even perfectly accurate models cannot produce just decisions if fed incorrect information. Decisions based on false data are inherently contestable.

**Example:** A hiring algorithm rejects a candidate based on an incorrect employment history (the system's data shows a gap that never occurred, due to database errors). Alternatively, a credit score is low because of another person's fraud on the individual's account, and this fraudulent entry remains in their credit file.

**Contestability mechanism:** Evidence of data errors provides grounds for decision reversal without requiring the system to change its logic—just its inputs.

#### Evidence Type 3: Neglected Overruling Evidence

**Definition:** Evidence exists about the individual that, if considered by the system, would deterministically overturn the decision, but the system's design or training excluded this information.

**Why it matters:** Some information is ethically or legally overriding. A hiring system that ignores accommodation requests is making decisions without acknowledging legally protected information. A medical triage system that never sees recent test results is missing overriding evidence.

**Example:** A criminal justice risk assessment model doesn't account for evidence of rehabilitation (completed therapy, stable housing) because these variables weren't in the training data. A loan system ignores evidence of recent financial recovery because it only looks at historical defaults. A content moderation system removes speech without considering documented medical necessity (discussing medications, therapeutic resources).

**Contestability mechanism:** The decision maker can override the algorithmic recommendation by introducing evidence that the system architecturally cannot see.

---

## Main Ideas & Key Contributions

### 1. Reframing XAI's Purpose

The paper's central contribution is a **conceptual shift**: explainability is not just about understanding "how did the system decide?" but about enabling contestation—"why should this decision stand?".

This reframing suggests that XAI research has been optimizing for the wrong objective function. Instead of asking "Can we explain model predictions?" we should ask "Can we support individual agency to challenge unjust outcomes?"

### 2. Distinguishing Contestability from Explanation

The authors demonstrate that **explanation ≠ contestation**:
- A system can be fully explainable yet uncontestable (you understand why it rejected you, but you have no legitimate grounds to overturn that decision)
- A system can be contestable yet opaque (you have clear evidence it made an error, even if you don't fully understand its mechanisms)

This distinction suggests the XAI community has been conflating two separate requirements.

### 3. Grounding in Decision Maker Ethics

Rather than imposing external fairness definitions, the framework respects the decision maker's own ethical standards. The question becomes: "According to **your** values and institutional rules, does this evidence warrant reversal?" This is more practically implementable than enforcing contested fairness metrics.

### 4. Legal Alignment

The paper shows how the three evidence types align with emerging regulatory requirements:

- **EU AI Act** requires transparency about how decisions are made (supporting predictive multiplicity evidence)
- **GDPR** grants individuals the right to correct inaccurate personal data (supporting incorrect feature values evidence)
- **Fair lending laws** and **disability accommodation requirements** create legal obligations to consider overruling evidence

The framework thus provides a bridge between technical XAI and legal compliance.

---

## Methodology & Implementation

### Analytical Framework

The paper employs **conceptual analysis** grounded in:

1. **Legal review:** Analysis of EU AI Act, GDPR, fair lending regulations, disability laws, and case law
2. **Ethical theory:** Examination of procedural justice, epistemic rights, and accountability frameworks
3. **Technical review:** Critique of existing XAI methods against contestability requirements
4. **Case studies:** High-stakes domains where contestability is critical

### Domains Analyzed

The framework is applied to:
- **Lending and credit:** Loan applications, credit scoring, interest rate determination
- **Employment:** Hiring, promotion, termination decisions
- **Criminal justice:** Risk assessment, bail determination, parole decisions
- **Healthcare:** Triage, treatment recommendations, resource allocation
- **Content moderation:** Automated speech removal, account suspension
- **Insurance:** Coverage decisions, rate calculation

### Evaluation Approach

Rather than empirical experiments, the methodology involves:

1. **Scenario analysis:** Constructing realistic cases where each evidence type could warrant reversal
2. **Legal analysis:** Showing alignment with existing rights and regulations
3. **Stakeholder mapping:** Identifying who needs to provide/verify each evidence type
4. **Process design:** Proposing how decision makers could implement contestability procedures

### Key Results & Findings

#### Finding 1: Predictive Multiplicity is Common but Poorly Addressed
- Many ML systems in high-stakes domains exhibit predictive multiplicity
- Current XAI methods don't reveal or address this multiplicity
- Simple model ensembles or competing vendor systems often show contradictory predictions
- This is a feature, not a bug—it reveals genuine uncertainty, but systems typically hide it

#### Finding 2: Data Quality Issues Are Systemic
- Error rates in decision-making data (credit files, employment records, criminal histories) are 10-20% or higher
- Current systems have no mandatory feature-level data quality checks
- Individual-level data correction procedures are slow, opaque, and inaccessible
- This represents low-hanging fruit for contestability improvements

#### Finding 3: Overruling Evidence is Systematically Excluded
- In lending: recent financial recovery, disability accommodations, hardship circumstances
- In employment: evidence of rehabilitation, caregiving responsibilities, medical conditions
- In criminal justice: evidence of rehabilitation, mental health improvements, community support
- This exclusion is often by design, but sometimes accidental (unmeasured variables)

#### Finding 4: Current Appeal Processes are Inadequate
- Most affected individuals lack clear pathways to present contestability evidence
- Decision makers often cannot override system recommendations even when evidence warrants it
- Appeals processes are slow, opaque, and have low success rates
- There's a gap between legal rights on paper and practical ability to exercise them

---

## Practical Applications & Real-World Use Cases

### 1. Lending and Credit (High Impact)

**Scenario:** An individual is denied a mortgage because their credit score is low due to a fraudulent account in their credit file. The fraud has been documented but remains on their record while disputes proceed.

**Current XAI approach:** System explains that "Your credit score of 620 is below the threshold of 640. Key factors: delinquency history (30% influence), utilization ratio (25%), payment history (20%), account age (15%), hard inquiries (10%)."

**Contestability approach:** The system could provide:
- Evidence of predictive multiplicity: "Our credit-risk model predicts 3% default probability, but an alternative vendor model predicts 1.8%, suggesting genuine uncertainty about your risk level."
- Data correction pathway: "This fraudulent account can be disputed through [specific process]. If removed, your score would be 720, above the threshold."
- Overruling evidence: "Our model doesn't consider: hardship circumstances, evidence of dispute filed, recent income stability. A human underwriter can evaluate these factors."

**Regulatory alignment:** GDPR Article 22 (right to contest), Fair Credit Reporting Act (data correction rights), Fair Lending laws (non-discriminatory lending).

---

### 2. Employment Decisions (High Complexity)

**Scenario:** A candidate with a gap in employment history is rejected by an automated screening system. The gap was due to caregiving responsibilities for a family member (legally protected under disability accommodation laws in many jurisdictions).

**Current XAI approach:** System explains that "Candidate filtered out. Continuous employment history is a key positive signal (importance weight: 0.3). Your employment gap (8 months) is below the threshold of 6+ months of gaps tolerated."

**Contestability approach:**
- Incorrect feature values: "Employment history analysis shows a gap, but the system only knew the dates. The individual can document that this gap was for legally-recognized caregiving, which should be reclassified."
- Overruling evidence: "The system evaluated technical skills (CV match: 92%) as a positive signal, but didn't access: relevant project portfolio (not in CV), professional references (not submitted), language skills (not in CV). These could override the employment gap concern."
- Predictive multiplicity: "Different screening rubrics could prioritize: recent experience vs. total experience, specialized skills vs. general aptitude. These lead to different recommendations; none is objectively 'correct.'"

**Regulatory alignment:** EU Employment Directive (disability accommodation), Title VII (protected characteristics), Pregnant Workers Act (caregiving protections).

---

### 3. Criminal Justice Risk Assessment (Highest Stakes)

**Scenario:** An individual faces a higher bail amount or longer sentence recommendation due to a risk assessment algorithm flagging them as high-risk for reoffending.

**Current XAI approach:** System explains that "Risk assessment: High risk (73%). Key factors: Prior arrests (30% importance), Age at first arrest (25%), Post-release neighborhood crime rates (20%), etc."

**Contestability approach:**
- Neglected overruling evidence: "The system only considers historical factors. Recent evidence of rehabilitation (vocational training completed, mental health treatment, stable housing secured, family support) is not in the model. These legally overrule historical risk factors in many jurisdictions."
- Data errors: "Your prior arrests record includes a case that was expunged. The system is using outdated legal information."
- Predictive multiplicity: "Research shows predictive multiplicity in recidivism assessment: different validated instruments designed on different populations make conflicting predictions. This uncertainty should result in conservative bail recommendations, not high risk determinations."

**Regulatory alignment:** Due process rights, bail reform laws, rehabilitation principle in sentencing.

---

### 4. Healthcare Triage and Treatment Allocation (Emerging Domain)

**Scenario:** An algorithmic system recommends against aggressive treatment for a patient, or deprioritizes them in resource allocation queues, based on risk predictions.

**Current approach:** System explains mortality risk score.

**Contestability approach:**
- Neglected overruling evidence: "Recent diagnostic tests (not in model training data) show different prognosis than historical data suggested. These override the algorithmic assessment."
- Patient/clinician values: "The system predicted life expectancy based on average population outcomes, but the individual patient values quality of life, experimental treatment risks, and personal survival priorities differently. These subjective judgments override algorithmic optimization."
- Data errors: "Patient history was imported from prior hospital system with errors. If corrected, the risk profile changes."

**Regulatory alignment:** Medical ethics (informed consent, patient autonomy), healthcare fairness laws.

---

### 5. Content Moderation (Scale, Ambiguity)

**Scenario:** A social media user's post is removed by automated moderation, suspended their account, and they cannot obtain meaningful explanation or appeal.

**Current approach:** "Your content violated policy X. System detected: [feature importance]."

**Contestability approach:**
- Neglected overruling evidence: "The system detected language flagged as 'harmful,' but context indicates: medical discussion (legitimate), educational resource (legitimate), or parody of harmful speech (legitimate). These contexts override the surface-level classification."
- Predictive multiplicity: "Multiple equally-trained moderation models disagree on whether this content violates policy. This disagreement (itself evidence) should trigger human review."
- Data errors: "The system flagged you as a 'repeat violator' but this is a data error—prior removals were incorrectly attributed to you."

---

## Insights & Implications

### 1. Paradigm Shift: From Explanation to Contestation

The paper suggests that XAI as currently framed solves the wrong problem. The question isn't "How can I understand the algorithm?" but "On what grounds can I legitimately demand it reconsider?"

This reframing has implications for:
- **Research priorities:** More work on data quality, model disagreement, and decision override mechanisms; less on post-hoc explanation methods
- **Industry practice:** Shifting from "making algorithms more transparent" to "enabling effective appeals"
- **Regulation:** Formalizing contestability requirements (EU AI Act is moving in this direction)

### 2. Regulation is Ahead of Technology

Emerging regulations already grant contestability rights:
- EU AI Act mandates right to explanation and challenge for high-risk systems
- GDPR grants right to correct personal data
- Various labor laws grant right to accommodation and review

Yet technical infrastructure to support these rights is underdeveloped. The paper identifies this gap and suggests concrete technical solutions.

### 3. Procedural Justice Matters More Than Transparency

Individuals care about:
1. Having their voice heard (procedural justice)
2. Receiving a fair outcome (distributive justice)
3. Understanding why the outcome occurred (retributive justice)

Transparency supports only #3. Contestability directly supports #1 and #2, which research shows are more important for perceived fairness and trust.

### 4. The Role of Human Judgment

The framework doesn't eliminate human judgment; it preserves and structures it. Decision makers remain the authority, but with better information and clearer procedures:
- They see predictive multiplicity, forcing a choice among valid options
- They learn about data errors, allowing correction
- They can consider overruling evidence, exercising contextual judgment

This supports **human-in-the-loop AI**, a more realistic deployment model than fully autonomous decision-making.

### 5. Limitations and Open Questions

**What the framework doesn't address:**
- **Predictive multiplicity without consensus:** What if experts genuinely disagree on which model is better?
- **Multiple overruling evidence types:** How to resolve conflicts when different evidence types suggest different decisions?
- **Scale and efficiency:** Contestability procedures could create massive administrative burden; how to make them scalable?
- **Technical measurement:** How to measure whether a contestability implementation is actually effective (vs. performative)?

**Future research directions:**
- Developing technical methods to *detect* predictive multiplicity and surface it to decision makers
- Automating data quality audits to identify feature-level errors
- Building causal inference methods to identify genuinely overruling evidence vs. correlated proxies
- Designing contestability procedures that scale while remaining fair
- Studying which contestability mechanisms actually change outcomes (effectiveness research)

---

## Code & Resources

### Official Implementations & Papers

- **ArXiv:** https://arxiv.org/abs/2605.16041
- **HTML version:** https://arxiv.org/html/2605.16041
- **Author repository:** (To be updated if authors release code)

### Related Legal & Policy Resources

- **EU AI Act:** https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
- **GDPR Articles 22, 24:** https://gdpr-info.eu/articles/automated-individual-decision-making/
- **US AI Bill of Rights:** https://www.whitehouse.gov/ostp/ai-bill-of-rights/
- **Fair Lending Compliance Guides:** CFPB, OCC guidelines on algorithmic credit decisions

### Related Interpretability Frameworks

- **Predictive Multiplicity:** [Marx et al., ICML 2020](https://proceedings.mlr.press/v119/marx20a/marx20a.pdf)
- **Counterfactual explanations:** DICE, counterfactual recourse literature
- **LIME/SHAP:** For understanding model-level feature importance
- **Causal inference:** For determining overruling evidence

### Computational Resources

This paper is primarily conceptual and doesn't require significant computational resources to understand. However, implementation would require:
- **Data quality auditing tools:** Pandas, Great Expectations for feature-level error detection
- **Model ensembles:** Scikit-learn, TensorFlow for detecting predictive multiplicity
- **Causal inference:** DoWhy, EconML for causal discovery of overruling evidence
- **Legal compliance tracking:** Custom databases and workflow systems

### Interactive Visualizations & Demos

- **Coming soon:** Interactive decision reversal scenarios
- **Contestability assessment tools:** Organizations like AI Now, Data for Good, and regulatory bodies are developing frameworks

---

## Related Work & Context

### Prior Contestability Research

1. **"Beyond Explainability: Justifiability and Contestability of Algorithmic Decision Systems"** (2021, Springer AI & Society)
   - Early theoretical work distinguishing contestability from explainability
   - Identifies contestability as an independent requirement

2. **"Generating Process-Centric Explanations to Enable Contestability in Algorithmic Decision-Making"** (arXiv:2305.00739)
   - Proposes generating explanations that support contestability
   - Focuses on process transparency rather than just prediction explanation

3. **"Contestable AI needs Computational Argumentation"** (arXiv:2405.10729)
   - Proposes using computational argumentation frameworks to formalize contestability
   - Addresses how to structure evidence and counterarguments

4. **"Explainable AI Systems Must Be Contestable: Here's How to Make It Happen"** (arXiv:2506.01662, June 2026)
   - Companion paper proposing formal contestability frameworks and design patterns
   - Provides implementation guidelines aligned with this paper's conceptual work

### Connections to Broader XAI Communities

**Relationship to SHAP/LIME:**
- These methods explain predictions but don't support contestability
- Could be extended to highlight areas where alternative models disagree or data appears incorrect

**Relationship to concept-based explanations:**
- Concept-based methods might better surface overruling evidence if concepts map to actionable human judgments
- Could improve contestability if they identify non-technical evidence (e.g., rehabilitation, accommodations)

**Relationship to causal interpretability:**
- Causal methods could identify whether neglected features are genuinely overruling vs. spurious correlations
- Strong potential for identifying true overruling evidence

**Relationship to fairness research:**
- Traditional fairness (group-level metrics) doesn't ensure individual contestability
- This framework provides individual-level fairness procedures

**Relationship to legal AI:**
- Bridges gap between AI safety/fairness research and practical legal requirements
- Provides framework for implementing regulatory requirements technically

### Evolution of Regulatory Requirements

- **2015-2018:** Early GDPR focus on data access rights
- **2020-2022:** Fair lending lawsuits highlight need for explanation (CFPB actions)
- **2023-2024:** EU AI Act codifies transparency and contestability rights
- **2025-2026:** Industry moves toward implementing contestability procedures (this paper)
- **Future:** Expected standards for measuring and auditing contestability effectiveness

### Future Research Directions

This paper opens several research avenues:

1. **Technical contestability detection:** Methods to automatically detect when systems should be contestable (data quality issues, predictive multiplicity, overruling evidence patterns)

2. **Contestability measurement:** Metrics for evaluating whether contestability procedures are actually effective (appeal success rates, fairness improvement, trust indicators)

3. **Scalable appeal systems:** How to design contestability procedures that don't become administrative bottlenecks while remaining fair

4. **Causal methods for overruling evidence:** Using causal inference to distinguish genuine overruling evidence from spurious correlations

5. **Human-AI collaborative contestation:** How to design systems where humans and AI systems collaborate to evaluate evidence and make override decisions

6. **Domain-specific contestability:** Specializing contestability frameworks for healthcare, criminal justice, hiring, content moderation, etc.

---

## Summary

"Explainable AI Isn't Enough! Rethinking Algorithmic Contestability" makes a crucial conceptual contribution to XAI research: explaining decisions and enabling contestation are distinct requirements, and contestability has received insufficient attention despite greater ethical and legal importance.

The paper's three-category framework (predictive multiplicity, incorrect feature values, neglected overruling evidence) provides concrete grounds for decision reversal grounded in ethical reasoning and legal precedent. This bridges the gap between technical XAI methods and the practical human rights and regulatory requirements for trustworthy algorithmic systems.

By reframing XAI's purpose from "make algorithms understandable" to "enable legitimate challenges to erroneous decisions," the paper charts a new research direction for the field—one more aligned with how humans actually deploy these systems and the legal/ethical constraints that govern them.

**Key takeaway:** In high-stakes domains, the ability to overturn wrong decisions matters more than the ability to explain correct ones. XAI should be measured not by explanation quality, but by whether it enables legitimate contestation of errors.
