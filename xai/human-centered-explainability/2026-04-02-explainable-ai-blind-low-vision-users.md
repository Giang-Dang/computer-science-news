# Explainable AI for Blind and Low-Vision Users: Navigating Trust, Modality, and Interpretability in the Agentic Era

**Authors:** Abu Noman Md Sakib, Protik Dey, Zijie Zhang, Taslima Akter  
**ArXiv ID:** [2604.00187](https://arxiv.org/abs/2604.00187)  
**Published:** April 2, 2026 (Latest Revision: May 2, 2026)  
**Institution:** University of Texas at San Antonio

---

## Executive Summary

This paper investigates the critical accessibility gap in explainable AI (xAI) systems, specifically examining the unique needs and challenges faced by blind and low-vision (BLV) users when interacting with AI-powered assistive technologies and autonomous agents. Through comprehensive user studies and empirical analysis, the work identifies key barriers to xAI accessibility, including modality mismatches and the phenomenon of self-blame in AI failures, while providing design recommendations for more equitable and trustworthy AI systems for this underserved population.

---

## Problem Statement

As AI systems transition from single-query tools to autonomous agents capable of multi-step decision-making and real-world actions, the absence of accessible explanations creates a fundamental barrier for blind and low-vision (BLV) users. This problem is especially acute because:

1. **Accessibility Gap in XAI Research:** While explainable AI has become increasingly important across domains, research specifically addressing the needs of users with visual impairments remains sparse and often overlooked.

2. **Agentic AI Complexity:** Traditional xAI methods designed for single-prediction explanations are insufficient for autonomous agents that operate over extended task horizons. In such systems, a single undetected error or misunderstanding can propagate irreversibly before any corrective feedback is available.

3. **Modality Mismatch:** Most xAI explanations are designed for visual presentation (saliency maps, feature importance plots, decision trees visualized as graphs), making them inaccessible to BLV users without significant adaptation.

4. **Trust and Verification Challenges:** BLV users face unique challenges in verifying AI outputs and understanding failure modes when they cannot directly perceive the results of AI decisions (e.g., in image recognition tasks, environmental perception, or autonomous decision-making).

5. **Self-Blame Attribution:** BLV users frequently internalize responsibility for AI failures, assuming they took a poor-quality input (e.g., a blurry photo) rather than recognizing that the AI system made an error—a phenomenon termed "self-blame bias."

---

## Core Concepts & Theory

### 1. Explainable AI (XAI) for Accessibility

Explainability in AI traditionally involves making model decisions transparent through post-hoc interpretability techniques such as:
- **Feature attribution methods** (SHAP, LIME, Integrated Gradients)
- **Saliency maps and attention visualizations**
- **Decision rules and concept-based explanations**
- **Rule extraction and surrogate models**

However, these methods presume visual or text-based modalities that are not naturally accessible to BLV users without conversion to alternative modalities (e.g., audio descriptions, haptic feedback, or conversational explanations).

### 2. Modality in Human-Computer Interaction

**Modality** refers to the sensory channels through which information is conveyed:
- **Visual:** Graphs, charts, saliency maps, highlighted features
- **Auditory:** Verbal descriptions, text-to-speech, tone-based feedback
- **Tactile/Haptic:** Vibration patterns, texture feedback, spatial information through haptic interfaces
- **Conversational:** Natural language dialogue for exploratory and confirmatory explanation

For BLV users, conversational and auditory modalities are often more natural and effective, but many xAI systems are designed with visual-first approaches.

### 3. Trust Calibration in Human-AI Interaction

Trust in AI systems is not a static property but a **dynamic negotiation** between:
- **User perception of system capability and reliability**
- **Risk assessment of the task and potential failure modes**
- **System communication style and transparency level**
- **User experience with system successes and failures**

For BLV users, this dynamic is further complicated by:
- **Reduced ability to independently verify outputs** when they cannot directly observe results
- **Higher stakes for trust miscalibration** (underestimating risk can lead to dangerous decisions, overestimating risk reduces system usefulness)
- **Reliance on system explanations as primary mechanism for trust building**

### 4. Autonomous Agents and Extended Horizons

Traditional xAI research focuses on **local explanations** (why did the model make *this* prediction?) for individual decisions. However, autonomous agents operate over **extended task horizons** with multiple decision points:
- Agent A → Agent B → Agent C → Final Outcome

In such systems:
- Errors can compound across steps
- Responsibility for failures becomes diffuse
- Accountability requires understanding not just individual decisions but their cumulative effects
- Explanation needs shift from understanding single predictions to understanding agent behavior over time

---

## Main Ideas & Key Contributions

### 1. Identifying the "Self-Blame Bias" in BLV Users

The paper documents a critical phenomenon where BLV users frequently attribute AI failures to their own actions (e.g., taking a blurry photo) rather than recognizing system failures. This bias:
- **Undermines appropriate distrust:** Users may trust systems too readily if they blame themselves for failures
- **Reduces error reporting:** BLV users may not report system errors if they believe they caused them
- **Affects system improvement:** Systems that don't receive accurate failure feedback cannot improve
- **Impacts user autonomy:** Persistent self-blame reduces users' confidence in using AI systems independently

### 2. Discovering the "Modality Gap" in XAI

The research empirically demonstrates that there is a significant gap between:
- **Preferred explanation modalities for BLV users:** Conversational, auditory, and natural language explanations
- **Common XAI implementation modalities:** Visual representations, graphs, and attention visualizations

This modality gap means many state-of-the-art xAI techniques are inherently inaccessible to BLV users, creating an equity problem in AI accessibility.

### 3. Characterizing Trust Dynamics Across Three Dimensions

The paper structures trust in AI systems for BLV users along three key dimensions:

#### Dimension 1: Risk Calibration
- BLV users must maintain accurate mental models of when AI systems are reliable vs. unreliable
- Explanation quality directly impacts calibration accuracy
- Misaligned explanations can lead to either over-confidence (dangerous) or under-confidence (wasteful)

#### Dimension 2: Modality Preference
- BLV users consistently prefer conversational and dialogue-based explanations
- Natural language explanations support iterative clarification and verification
- Conversational modality enables users to ask follow-up questions and explore ambiguities
- Visual explanations (without accessible alternatives) are fundamentally inaccessible

#### Dimension 3: Verification Strategies
- BLV users employ various strategies to verify non-interpretable outputs:
  - **Logical consistency checks:** Ensuring explanations are internally coherent
  - **Cross-validation with domain knowledge:** Comparing AI outputs to their own expertise
  - **Incremental testing:** Using small, low-stakes decisions to test system reliability before high-stakes use
  - **Human consultation:** Seeking verification from sighted individuals or domain experts

### 4. Requirements for Accessible and Equitable XAI in Agentic Systems

The paper articulates specific requirements for xAI systems serving BLV users:

1. **Accessible modalities:** Explanations must be available in auditory and conversational formats, not solely visual representations

2. **Blame-aware design:** Explanations should help users distinguish between user error (e.g., input quality) and system error (e.g., model failure)

3. **Agent transparency:** For autonomous systems, explanations must address not just individual decisions but agent behavior patterns over extended interactions

4. **Verification support:** Systems should enable users to independently verify outputs and assess reliability without requiring sighted assistance

5. **Iterative dialogue:** Conversational interfaces that support follow-up questions and exploratory clarification

6. **Bias awareness:** Recognition that certain user populations (BLV users) may be underserved and require different explanation approaches

---

## Methodology & Implementation

### Research Approach

The paper employs a **mixed-methods qualitative research design** combining:

1. **User Interviews:** Semi-structured interviews with BLV users to understand their:
   - Current use of AI-powered assistive technologies
   - Information needs and preferences
   - Trust dynamics and verification strategies
   - Pain points and failures they've experienced

2. **Literature Review:** Comprehensive analysis of existing xAI research to identify:
   - What accessibility considerations exist in current xAI literature
   - How well existing techniques address BLV needs
   - Gaps and underexplored areas

3. **Case Study Analysis:** Examination of specific AI systems and xAI approaches used or relevant to BLV users, such as:
   - Image recognition assistants for environmental perception
   - Decision support systems for information access
   - Autonomous agents in assistive technology contexts

### Key Research Questions

1. What are the unique xAI requirements of BLV users?
2. How do BLV users currently interact with and verify AI outputs?
3. What modalities and explanation formats are most effective for BLV users?
4. How do trust dynamics differ for BLV users compared to sighted users?
5. What design principles should guide accessible xAI systems?

### Datasets and User Population

- **Participants:** BLV individuals with varying degrees of visual impairment and experience with AI assistive technologies
- **Domains:** Environmental perception, information access, decision support, and autonomous agent interaction

### Evaluation Metrics

Rather than traditional interpretability metrics (faithfulness, stability), the paper evaluates xAI systems on:

1. **Accessibility:** Can BLV users perceive and understand explanations without additional assistance?

2. **Verification capability:** Do explanations enable users to independently verify AI outputs?

3. **Self-blame reduction:** Do blame-aware explanations help users correctly attribute errors?

4. **Trust calibration:** Do explanations support accurate mental models of system reliability?

5. **User autonomy:** Do explanations enable independent decision-making without requiring sighted intermediaries?

### Key Findings

1. **Conversational explanations are strongly preferred** by BLV users over visual or complex textual descriptions

2. **Self-blame is a pervasive phenomenon** even among experienced AI users, suggesting it's a systemic design issue rather than user knowledge gap

3. **Extended task horizons complicate trust:** BLV users struggle to maintain appropriate trust over long interaction sequences with autonomous agents

4. **Verification strategies are cognitively demanding:** Current verification approaches require significant user effort and domain expertise

5. **Existing xAI research largely ignores accessibility:** Most papers don't consider how explanations would be presented to users with different sensory capabilities

---

## Practical Applications & Real-World Use Cases

### 1. Assistive Technology for Environmental Perception

**Application:** Image recognition systems for environment navigation (e.g., object detection, scene understanding, obstacle avoidance)

**Concrete Example:**
- A blind user uses their smartphone with an AI vision system to navigate an unfamiliar building
- The system encounters an ambiguous object and provides either a wrong identification or admits uncertainty
- **Without accessible explanation:** User can only guess whether the system failed or they provided a poor input
- **With accessible xAI:** Conversational system explains "I detected a shape with characteristics of X, but my confidence is only 60%. The image quality was good, but the lighting was dim, which affects my accuracy on similar objects"
- **Outcome:** User understands it's a system limitation (not user error) and can adjust their approach (increase lighting, try different angles)

### 2. Decision Support Systems for Healthcare

**Application:** AI-assisted diagnosis and treatment recommendations in healthcare systems accessed by BLV healthcare workers or patients

**Concrete Example:**
- A BLV physician uses an AI diagnostic system to suggest treatment options
- The system recommends a treatment that conflicts with the physician's clinical judgment
- **Accessible explanation via dialogue:** 
  - "I recommended this based on patient age (40), symptom profile X, and lab results Y, which matched patterns in 87% of similar cases"
  - "Would you like me to explain which specific symptoms most influenced this recommendation?"
  - "Should I consider the additional context you mentioned about patient medication history?"
- **Outcome:** Physician can understand reasoning and make informed decisions about whether to follow AI recommendation

### 3. Autonomous Agents for Task Automation

**Application:** AI agents that autonomously perform multi-step tasks (e.g., scheduling, information retrieval, task planning) for BLV users

**Concrete Example:**
- An AI agent autonomously schedules a medical appointment, reserves transportation, and books a hotel
- One step fails (no available appointments on requested date)
- **Accessible explanation:** Rather than just failing, agent explains "I could not find appointments on June 15, but found options on June 16 (same doctor, morning slot) and June 17 (different doctor, afternoon slot). Should I proceed with either of these, or would you like me to continue searching?"
- **Outcome:** User maintains agency over task and understands why the agent made particular decisions

### 4. Regulatory and Compliance Applications

**Scenario:** FDA approval for medical AI devices, EU AI Act compliance

**Requirements:**
- Explainability requirements (e.g., EU AI Act) apply to high-risk systems
- These systems must be usable by diverse populations, including people with disabilities
- Accessible explanation mechanisms become a regulatory requirement for compliance
- BLV users should be able to independently understand AI recommendations in healthcare, lending, hiring, and other high-stakes domains

### 5. Educational Technology and Content Accessibility

**Application:** AI tutoring systems and automated content generation for educational platforms serving BLV students

**Use Case:** AI generates explanations for student errors but must do so in accessible formats
- "You answered 42, but the correct answer is 45. You made an error in the multiplication step (6×7 should be 42... wait, that's actually correct. Let me reconsider... You had the right calculation but likely made an error in carrying from a previous step.)"
- Conversational explanation allows student to ask clarifying questions

---

## Insights & Implications

### 1. Advancing Trustworthy AI for Underserved Populations

This work contributes to broader goals of **trustworthy and equitable AI** by highlighting how xAI research often inadvertently creates barriers for users with disabilities. Key implications:

- **Accessibility is not an afterthought:** Designing xAI systems without considering diverse user populations (including people with disabilities) fundamentally undermines trustworthiness
- **Universal design benefits everyone:** Conversational explanations are not just better for BLV users—they're often more useful for everyone (sighted users also benefit from natural language dialogue vs. visual plots alone)
- **Equity in high-stakes decisions:** In critical domains like healthcare, criminal justice, and lending, explainability must be equitable; denying BLV users accessible explanations denies them agency in decisions affecting their lives

### 2. State-of-the-Art in Accessible XAI

Current state-of-the-art advances in accessible xAI include:

- **Large Language Model-based explanations:** LLMs can generate natural language explanations from model internals, enabling accessible explanations
- **Conversational explanation interfaces:** Dialogue systems that support iterative clarification
- **Multimodal explanation generation:** Systems that produce explanations in multiple modalities (visual, auditory, tactile)
- **Participatory design:** Involving BLV users in the design of xAI systems from the start

This paper advances the field by systematizing what types of explanations work best and identifying specific design principles.

### 3. Limitations and Open Questions

**Limitations:**
1. **Generalizability:** Findings based on specific user cohort; needs validation across diverse BLV populations with different backgrounds and experiences
2. **Technical feasibility:** Some recommendations (e.g., real-time conversational explanations for complex models) face computational constraints
3. **Scalability:** Implementing accessible xAI at scale across many systems and domains requires significant investment
4. **User training:** Some accessible xAI approaches require users to learn new interaction paradigms

**Open Questions:**
1. How can we design autonomous agents that maintain user agency and understanding over extended task horizons?
2. What are the cognitive load and performance implications of different explanation modalities for BLV users?
3. How do we measure and ensure sufficient explanation quality for xAI systems serving BLV users?
4. What role should participatory design play in developing accessible xAI?
5. How can we incentivize industry to prioritize accessibility in xAI research and development?

### 4. Future Research Directions

**Near-term (1-2 years):**
- Develop and validate accessible xAI interfaces for specific domains (healthcare, education, assistive technology)
- Create benchmarks and datasets for evaluating accessible xAI systems
- Study cognitive and interaction patterns of BLV users with different explanation modalities

**Medium-term (2-5 years):**
- Design autonomous agents that maintain user understanding and agency over extended interactions
- Develop standardized guidelines for accessible xAI implementation
- Conduct longitudinal studies on how accessible explanations affect user trust and decision-making

**Long-term (5+ years):**
- Integrate accessibility as a core design principle across AI and ML research communities
- Develop xAI systems that dynamically adapt explanations to individual user needs and preferences
- Create regulatory frameworks that enforce xAI accessibility requirements
- Establish interdisciplinary communities connecting HCI, accessibility research, and explainable AI

### 5. Impact on Broader XAI Research

This work has implications for the entire xAI community:

1. **Highlights blind spot in current research:** XAI research's focus on visual and technical explanations has inadvertently excluded users with visual impairments

2. **Demonstrates importance of human-centered XAI:** Effective explanations must be centered on actual user needs and contexts, not just technical metrics

3. **Advocates for participatory design:** Involving affected communities (here, BLV users) from the start leads to more equitable and effective systems

4. **Influences research methodology:** Future xAI evaluations should include diverse user populations and measure real-world utility, not just technical faithfulness

---

## Code & Resources

### Official Implementations

The paper does not appear to have released official code, but related resources include:

- **Related Projects:** The authors reference work from the User-Centered AI Lab at University of Texas at San Antonio
- **Inseq Library:** For attribution extraction in NLP: https://github.com/inseq-team/inseq
- **Accessible AI research community:** https://hcxai.jimdosite.com/

### Dependencies and Computational Requirements

For implementing accessible xAI systems as described in the paper:

- **LLM-based explanation generation:** Requires access to large language models (GPT-4, Claude, open-source alternatives like Llama)
- **Conversational interfaces:** Can leverage existing dialogue frameworks (Rasa, Microsoft Bot Framework)
- **Text-to-speech:** Accessibility tools like JAWS, NVDA, or built-in OS text-to-speech
- **Computational cost:** Modest for most proposed approaches; conversational explanations via LLMs have standard API costs

### Quick Start for Implementing Accessible XAI

1. **Audit current xAI system:**
   - List all explanations and their modalities
   - Test with screen reader or accessibility tool
   - Identify visual-only explanations

2. **Generate alternative modalities:**
   - Convert visual explanations (saliency maps) to textual descriptions
   - Implement text-to-speech for all textual explanations
   - Add conversational interface for exploratory explanation needs

3. **Evaluate with diverse users:**
   - Conduct usability testing with BLV participants
   - Measure verification capability and trust calibration
   - Iterate based on feedback

### Interactive Demos and Visualizations

The paper references several related papers with interactive components:
- Papers on conversational AI for accessibility
- Demos of dialogue-based explanation systems
- Tools for generating accessible data visualizations

---

## Related Work & Context

### How This Paper Connects to Prior XAI Work

**Building upon:**
1. **XAI for Trust:** Prior work (Lipton 2016; Ribeiro et al. 2016) established that explanations affect user trust; this paper applies that to a specific underserved population

2. **Conversational AI:** Related to work on dialogue-based explanations and interactive xAI (Lakkaraju & Bastani 2020; Sap et al. 2019)

3. **Accessibility in AI:** Builds on growing research in accessible machine learning (Branham & Kane 2015; Kaur et al. 2022)

4. **Human-Centered AI:** Part of the broader movement toward human-centered, participatory AI design (Shneiderman 2022)

### Critiquing and Extending Prior Work

The paper identifies gaps in prior xAI research:

1. **Most xAI research assumes visual communication:** LIME, SHAP, saliency maps, and attention visualization are all visual-first methods

2. **Accessibility is rarely considered:** Only a handful of prior papers specifically address accessible xAI

3. **User studies often use limited populations:** Few xAI papers include diverse user populations in evaluation

4. **Agentic systems are underexplored:** Most xAI research focuses on single-prediction explanations, not extended agent behavior

### Connections to Broader XAI Communities

This work connects to multiple xAI research threads:

1. **Feature Attribution Methods** (SHAP, LIME, Integrated Gradients)
   - Shows how to present these results accessibly
   - Suggests conversational interfaces as alternatives to visual attribution plots

2. **Concept-Based Explanations**
   - Argues that high-level concepts (rather than raw features) may be more accessible
   - Supports natural language concept descriptions

3. **Causal Interpretability**
   - Relevant for explaining "why" certain decisions were made
   - Supports causal reasoning in conversational format

4. **Human-Centered XAI**
   - Directly part of this research community
   - Exemplifies importance of centering actual user needs in xAI design

5. **Fairness and Accountability in AI**
   - Accessibility is a fairness issue: denying BLV users explanations is inequitable
   - Supports broader movements toward fair and accountable AI

### Future Research Directions in Related Areas

**In Accessible Assistive Technology:**
- How to design AI agents that maintain user agency and understanding over long task sequences

**In Human-Computer Interaction:**
- Best practices for conversational interfaces delivering complex technical information

**In AI Ethics and Fairness:**
- How to systematically identify and address accessibility barriers in AI systems

**In XAI Evaluation:**
- Metrics and benchmarks for evaluating xAI systems with diverse user populations

---

## Discussion: Implications for XAI Research

### The Accessibility Imperative

This paper makes a compelling case that **accessibility is not a niche concern in xAI research**—it's foundational to trustworthy and equitable AI systems. Key takeaways:

1. **Explainability and accessibility are inseparable:** An explanation that's incomprehensible due to inaccessible presentation is not actually an explanation

2. **Universal design benefits everyone:** Conversational explanations, blame-aware messaging, and iterative verification help not just BLV users but all users

3. **Current xAI research has a blind spot:** By focusing on visual representations, the field has inadvertently excluded users with visual impairments

### Methodological Insights

The paper demonstrates the value of **participatory, human-centered research** in xAI:
- Direct engagement with BLV users reveals needs that would be missed in purely technical research
- Qualitative methods complement quantitative metrics in understanding explanation effectiveness
- Real-world context matters: Explanations for assistive technology have different requirements than for model debugging

### Systemic Issues Revealed

The research surface several systemic problems in current AI development:

1. **Self-blame bias** is a design issue, not a user knowledge issue—systems could reduce this through careful explanation design

2. **Trust miscalibration** is common among BLV users but is addressable through better explanations

3. **Verification barriers** limit user agency—accessible xAI must support independent verification without requiring sighted intermediaries

### Call to Action

For the XAI research community:

1. **Involve diverse users** in xAI research, including people with disabilities
2. **Design for accessibility from the start**, not as an afterthought
3. **Adopt human-centered evaluation metrics** beyond technical faithfulness
4. **Collaborate with accessibility researchers** to apply inclusive design principles
5. **Advocate for regulatory requirements** that ensure xAI accessibility

---

## Summary

This paper makes critical contributions to accessible and equitable xAI by:

1. **Identifying specific accessibility gaps** in current xAI research and practice
2. **Documenting self-blame bias** as a systematic issue in AI explanation design
3. **Characterizing trust dynamics** for BLV users across three key dimensions
4. **Providing concrete design recommendations** for accessible xAI systems
5. **Advancing human-centered XAI** by centering underserved populations
6. **Making the case for participatory design** in AI system development

The work demonstrates that effective explainability requires not just technical sophistication but also accessibility, usability, and genuine engagement with the diverse humans who will interact with these systems.
