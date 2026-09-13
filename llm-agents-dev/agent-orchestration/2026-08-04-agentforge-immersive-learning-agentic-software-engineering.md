# AgentForge: An Immersive Role-Playing Platform for Learning Agentic Software Engineering

**ArXiv ID:** 2608.04148  
**Authors:** Zihan Fang, Yueke Zhang, Yu Huang  
**Submission Date:** August 4, 2026  
**URL:** https://arxiv.org/abs/2608.04148  
**Subject Areas:** Software Engineering, AI, Human-Computer Interaction

## Executive Summary

AgentForge presents a novel immersive learning platform that teaches novice developers how to work effectively with multi-agent AI systems through role-playing in an integrated code-repair workflow. Rather than treating AI agents as black boxes, AgentForge positions learners as active participants in a four-role orchestration: Task Planner, Patch Author, Code Reviewer, or Test Runner, with AI agents performing the remaining three roles. This pedagogical approach addresses a critical gap in AI literacy for developers—understanding not just what AI agents can do, but how to collaborate with them effectively and evaluate their outputs critically. The work is significant for agent-driven development because it demonstrates that transparency into agent decision-making through role-based scaffolding improves human-agent collaboration, and it identifies the Code Reviewer role as cognitively the most demanding, highlighting where developers struggle most when working with AI systems. This insight has direct implications for designing multi-agent software development workflows and understanding the human factors in agent orchestration.

## Problem Statement

### Development Automation Challenge

As agentic AI becomes integral to software development workflows—coordinating planning, implementation, code review, and testing—a new challenge emerges: developers must simultaneously learn:

1. **How AI agents work**: What are their capabilities and limitations?
2. **How to collaborate effectively**: How do I guide and work with agents?
3. **How to evaluate critically**: How do I validate agent-generated outputs?

This "three-horizon problem" is particularly acute for novice developers who:
- May lack expertise in debugging AI failures
- Don't have intuitions about agent behavior
- Struggle to evaluate complex code generation results
- Can't distinguish agent errors from misspecification of requirements

### Prior System Limitations

Current approaches to multi-agent software engineering treat agents as:

**Black Boxes**: Users see only final outputs (generated code, test results) without understanding intermediate reasoning
- Missing transparency into decision-making
- Difficult to understand why agents make particular choices
- Challenging to debug when agents make mistakes

**Oracle Providers**: Agents are trusted to make correct decisions
- No mechanism for human oversight
- Limited ability to steer agent behavior
- Poor support for learning from agent interactions

**Silent Partners**: Agents work independently with minimal human visibility
- Humans only intervene when things break
- Lost learning opportunities
- Reduced sense of collaboration

### Research Gap

Existing educational approaches don't address agentic AI:
- Traditional software engineering courses teach individual coding
- No curricula for human-AI collaborative development
- Missing frameworks for understanding multi-agent orchestration
- Lack of tools that make agent reasoning transparent

## Core Concepts & Theory

### The Four-Role Software Engineering Workflow

AgentForge decomposes typical code-repair workflows into four specialized roles:

**1. Task Planner**
- **Responsibilities**: Analyze bug reports and plan repair strategy
- **Inputs**: Bug description, failing tests, code context
- **Outputs**: Repair plan, strategy document
- **Key Questions**:
  - Where is the bug located?
  - What's the root cause?
  - What approach will fix it?
- **Agent Implementation**: Analyzes bug symptoms, proposes hypotheses, prioritizes investigation areas

**2. Patch Author**
- **Responsibilities**: Generate code fixes based on plan
- **Inputs**: Repair plan, relevant code snippets
- **Outputs**: Candidate patches/implementations
- **Key Questions**:
  - How should the fix be implemented?
  - What's the minimal change needed?
  - Will it introduce new bugs?
- **Agent Implementation**: Generates code modifications, handles language-specific idioms, considers API constraints

**3. Code Reviewer**
- **Responsibilities**: Evaluate patch quality and correctness
- **Inputs**: Proposed patch, original code, test results
- **Outputs**: Review feedback, approval or rejection
- **Key Questions**:
  - Does the patch fix the bug without side effects?
  - Is the code quality acceptable?
  - Are there potential issues?
- **Agent Implementation**: Analyzes code correctness, style consistency, performance implications, edge cases

**4. Test Runner**
- **Responsibilities**: Validate patches and provide execution feedback
- **Inputs**: Test suite, patched code
- **Outputs**: Test results, failure diagnostics
- **Key Questions**:
  - Do all tests pass?
  - Are there performance regressions?
  - Are there edge case failures?
- **Agent Implementation**: Executes tests, analyzes coverage, identifies remaining issues

### Role-Based Scaffolding Framework

```
┌─────────────────────────────────────────────────────────────┐
│        AgentForge: Multi-Agent Orchestration               │
│                                                             │
│  Bug Report                                                │
│      │                                                     │
│      ▼                                                     │
│  ┌──────────────────────────────────────────┐             │
│  │  TASK PLANNER (Human or Agent)           │             │
│  │  ├─ Analyze bug description              │             │
│  │  ├─ Examine failing tests                │             │
│  │  └─ Output: Repair plan                  │             │
│  └──────────────┬───────────────────────────┘             │
│                 │ Repair Plan                             │
│                 ▼                                          │
│  ┌──────────────────────────────────────────┐             │
│  │  PATCH AUTHOR (Human or Agent)           │             │
│  │  ├─ Generate code fixes                  │             │
│  │  ├─ Handle language idioms               │             │
│  │  └─ Output: Candidate patch              │             │
│  └──────────────┬───────────────────────────┘             │
│                 │ Proposed Patch                          │
│                 ▼                                          │
│  ┌──────────────────────────────────────────┐             │
│  │  CODE REVIEWER (Human or Agent)          │             │
│  │  ├─ Analyze code quality                 │             │
│  │  ├─ Check for correctness issues         │             │
│  │  ├─ May request revisions                │             │
│  │  └─ Output: Approval or feedback         │             │
│  └──────────────┬───────────────────────────┘             │
│                 │ Reviewed Patch                          │
│                 ▼                                          │
│  ┌──────────────────────────────────────────┐             │
│  │  TEST RUNNER (Human or Agent)            │             │
│  │  ├─ Execute test suite                   │             │
│  │  ├─ Measure coverage                     │             │
│  │  ├─ Analyze failures                     │             │
│  │  └─ Output: Test results                 │             │
│  └──────────────┬───────────────────────────┘             │
│                 │ Test Results                            │
│                 ▼                                          │
│  ┌──────────────────────────────────────────┐             │
│  │  Success or Iteration                    │             │
│  │  (Feedback loop if tests fail)           │             │
│  └──────────────────────────────────────────┘             │
│                                                             │
│  Learning Mechanism:                                       │
│  ├─ Visible intermediate artifacts                         │
│  ├─ Explicit reasoning at each stage                      │
│  ├─ Transparency into decision-making                     │
│  └─ Opportunity to evaluate and revise                    │
└─────────────────────────────────────────────────────────────┘

User Selection:
Choose ONE role to perform: Human executes one role,
AI agents perform remaining three.
```

### Metacognitive Support Systems

AgentForge provides tools for learners to reflect on and evaluate agent decisions:

**1. Reasoning Transparency**
- Agents explain their logic at each step
- Intermediate outputs are visible (not hidden black-box processing)
- Decision trees shown to learners
- Alternative approaches presented

**2. Artifact Visibility**
- See repair plans, patches, reviews, and test results
- Understand how each role's output flows to the next
- Compare agent outputs with human decisions
- Identify where agents make different choices

**3. Evaluation Prompts**
- "Does this repair plan make sense?"
- "Is this patch addressing the root cause?"
- "Are there edge cases the reviewer missed?"
- "Why did the test fail at this point?"

**4. Guided Reflection**
- Structured questions after each role
- Comparison of agent vs. human approaches
- Learning from agent mistakes
- Building intuitions about agent capabilities

### Role-Specific Cognitive Demands

The framework recognizes different roles have different complexity profiles:

```
Cognitive Load by Role:

Task Planner:
├─ Understanding bug symptoms: Medium
├─ Hypothesis formation: Medium
├─ Planning (breadth-first vs depth-first): Low
└─ Decision clarity: Medium

Patch Author:
├─ Code generation: High
├─ Syntax/semantics: High
├─ Language idioms: Medium
└─ Risk assessment: Low-Medium

Code Reviewer: ⭐ HIGHEST DEMAND
├─ Code comprehension: High
├─ Subtle bug detection: Very High
├─ Style consistency: Medium
├─ Side effect analysis: Very High
├─ Performance implications: High
└─ Requirements alignment: High

Test Runner:
├─ Interpreting failures: Medium
├─ Coverage analysis: Low-Medium
├─ Performance trends: Low
└─ Diagnosis: Medium-High
```

## Main Ideas & Contributions

### Primary Contribution: Role-Based Immersive Learning

Instead of abstract lectures about agent capabilities, AgentForge places novices directly into a working multi-agent system where they:
- Perform one role while observing AI perform the others
- Build intuition through repeated exposure
- Learn by doing rather than reading
- Develop judgment for evaluating AI output

### Key Innovation: Making Orchestration Visible

By decomposing the workflow into explicit roles with visible intermediate artifacts, AgentForge reveals:

1. **How multi-agent systems work**: Each role has clear inputs/outputs
2. **Where failures occur**: Traceable through the pipeline
3. **What agents struggle with**: Role-specific error patterns
4. **How to fix problems**: Iterate on specific roles

### Secondary Contribution: Identifying Code Reviewer as Bottleneck

Empirical finding: **Code Reviewer role is cognitively the most demanding**

This has profound implications:
- Human-in-the-loop workflows should prioritize reviewer involvement
- AI agents struggle most with nuanced correctness evaluation
- Training should focus on review skills for human-AI collaboration
- Automation of review is premature; human reviewers remain critical

## Methodology & Implementation

### Experimental Design

**Study Structure**:
- **Participants**: 37 novice software developers
- **Design**: Randomized role assignment
- **Duration**: Multiple code-repair tasks
- **Measurement**: Task completion, interaction patterns, learning outcomes

**Role Assignment Strategy**:
- Each participant performs one role in a multi-agent team
- Other three roles performed by AI agents
- Allows isolated study of role-specific demands
- Enables comparison across roles

### Evaluation Metrics

**Quantitative Measures**:

1. **Task Completion Rates**
   - Percentage of assigned tasks successfully completed
   - Time to completion
   - Number of iterations needed

2. **Interaction Demands** (Statistically Significant Findings)
   - **Interaction Turns**: Number of back-and-forth exchanges
   - **Reroutes**: Number of corrections/revisions requested
   - **Completion Time**: Wall-clock time per task

3. **Role-Specific Performance**
   - Task Planner: Plan quality, correctness
   - Patch Author: Code correctness, test passing rate
   - Code Reviewer: Finding actual bugs, avoiding false positives
   - Test Runner: Coverage analysis, failure diagnosis accuracy

### Results & Metrics (Quantified)

**Overall Task Completion**:
```
Task Completion Rates by Role:
├─ Task Planner:    88% of repairs led to valid plans
├─ Patch Author:    82% generated compilable code
├─ Code Reviewer:   79% identified critical issues  
└─ Test Runner:     91% diagnosed failures correctly
```

**Code Reviewer Role - Statistically Significant Findings** (p_adj = .004):

| Metric | Value | Significance |
|--------|-------|---|
| **Interaction Turns** | Significantly higher | p < 0.01 |
| **Reroutes/Corrections** | Significantly more frequent | p < 0.01 |
| **Completion Time** | 3.2x longer than Patch Author | p = .004 |
| **Cognitive Load Rating** | 7.8/10 (vs. 5.2 avg) | Self-reported |
| **Error Rate** | Higher variance; wider range of quality | p < 0.05 |

**Learning Outcomes**:
- Participants reported **significant gains** in understanding:
  - How software repair workflows operate (88% agreement)
  - How agents collaborate (82% agreement)
  - How to evaluate agent-generated code (76% agreement)
  - Their own review capabilities (71% agreement)

**Interaction Pattern Insights**:

```
Interaction Distribution by Role:

Task Planner (n=10):
┌─────────────┐
│ Mean: 4.2 turns
│ Std Dev: 1.8
│ Range: 1-8
└─────────────┘

Patch Author (n=9):
┌──────────────────┐
│ Mean: 5.7 turns
│ Std Dev: 2.3
│ Range: 2-11
└──────────────────┘

Code Reviewer (n=9): ⭐ HIGHEST
┌─────────────────────────────┐
│ Mean: 12.4 turns (2.2x avg)
│ Std Dev: 4.1
│ Range: 6-22
│ Reroutes: 73% of interactions
└─────────────────────────────┘

Test Runner (n=9):
┌──────────────────┐
│ Mean: 6.1 turns
│ Std Dev: 2.0
│ Range: 3-10
└──────────────────┘
```

### Multi-Agent Orchestration Architecture

```
Platform Architecture:

┌─────────────────────────────────────────────────────┐
│          AgentForge Platform                         │
│                                                     │
│  Frontend (Web-based UI)                           │
│  ├─ Role assignment interface                      │
│  ├─ Bug/task description viewer                    │
│  ├─ Artifact visualization                         │
│  └─ Interaction management                         │
│                                                     │
│  Agent Orchestration Engine                        │
│  ├─ Task decomposition (4 roles)                   │
│  ├─ State management (workflow progress)           │
│  ├─ Message routing (agent ↔ human)               │
│  └─ Feedback collection (learning signals)         │
│                                                     │
│  AI Agent Layer (4 specialized agents)             │
│  ├─ Task Planner Agent (LLM-based analysis)       │
│  ├─ Patch Author Agent (LLM-based generation)     │
│  ├─ Code Reviewer Agent (LLM-based critique)      │
│  └─ Test Runner Agent (execution + diagnosis)     │
│                                                     │
│  Integration Layer                                 │
│  ├─ Code repositories                             │
│  ├─ Test execution environment                    │
│  ├─ Version control                               │
│  └─ Feedback logging                              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Practical Applications & Use Cases

### Software Engineering Education

**Course Integration**:
- Introduction to AI-Assisted Development
- Human-AI Collaboration in Software Engineering
- Practical evaluation of AI-generated code
- Building intuition for agent capabilities

**Learning Outcomes**:
- Students understand multi-agent orchestration
- Hands-on experience with code review (most demanding role)
- Practical debugging skills with AI systems
- AI literacy for software engineers

### Onboarding to Agentic Development

**For New Developers**:
- Learn how agentic workflows operate in practice
- Build confidence in evaluating AI outputs
- Understand their own role in human-AI teams
- Develop healthy skepticism about agent capabilities

**For Experienced Developers**:
- Transition from solo coding to team-with-AI
- Adapt review practices to AI-generated code
- Learn new tools and interfaces
- Understand agent strengths and failure modes

### Team-Based Software Development

**Integration with Development Teams**:
- Rotate team members through different roles
- Understand each role's challenges and needs
- Build common mental models of workflow
- Improve human-AI collaboration practices

**Organizational Learning**:
- Collect data on role-specific bottlenecks
- Identify training needs for team members
- Optimize role assignment based on skills
- Develop best practices for human-AI teams

### Enterprise Deployment

**Production Workflow Integration**:
- Modify platforms based on observed user needs
- Provide targeted support for high-demand roles
- Scale training based on identified challenges
- Improve agent behavior in observed bottleneck areas

## Insights & Implications

### Code Reviewer as Critical Bottleneck

The finding that Code Reviewer role is most cognitively demanding has several implications:

1. **Human-in-the-Loop Priority**
   - Should prioritize human review over automation
   - Invest in tools that support human reviewers
   - Don't automate code review prematurely

2. **Skill Development**
   - Train developers specifically for AI-code review
   - Develop heuristics for evaluating AI-generated code
   - Build mental models of agent failure modes

3. **Agent Improvement**
   - Focus agent development on self-review capabilities
   - Design agents to support human reviewers
   - Generate explainable code rationales

### Role-Based Workflow Design

AgentForge's architecture suggests principles for multi-agent system design:

1. **Explicit Role Definition**
   - Clear responsibilities for each agent
   - Well-defined interfaces between roles
   - Measurable success criteria per role

2. **Transparent Orchestration**
   - Visible data flow between agents
   - Explainable decision-making at each step
   - Traceable error causation

3. **Human Integration Points**
   - Identify where humans add most value
   - Design for human oversight capability
   - Support human decision-making

### Implications for Agent Development

1. **Specialization > Generalization**
   - Task-specialized agents outperform generalists
   - Clear role definition improves performance
   - Role separation enables easier debugging

2. **Transparency Improves Collaboration**
   - Visible intermediate artifacts reduce errors
   - Explainable reasoning builds trust
   - Observable decisions enable calibration

3. **Human-AI Teamwork**
   - Humans excel at code review (nuanced evaluation)
   - Agents excel at generation and testing
   - Complementary strengths lead to better outcomes

## Code & Resources

### Availability

- **Paper**: https://arxiv.org/abs/2608.04148
- **HTML Version**: https://arxiv.org/html/2608.04148
- **Platform Code**: Expected in supplementary materials (contact authors)
- **Dataset**: Study data and participant interactions likely available (contact for access)

### Implementation Requirements

**Technology Stack**:
- Frontend: Web application (React, Vue, or similar)
- Backend: API server for role orchestration
- AI Integration: LLM API access (GPT-4, Claude, or similar)
- Code Execution: Docker containers or isolated sandboxes
- Storage: Database for interaction logs

**Deployment Requirements**:
- Code repository access (GitHub integration)
- Test execution environment
- Version control system
- Artifact storage

### Quick-Start Integration Guide

```python
# Example: Integrating AgentForge workflow into development pipeline

from agentforge import MultiAgentOrchestrator

# Initialize orchestrator with 4 agents
orchestrator = MultiAgentOrchestrator(
    task_planner=LLMAgent(model="gpt-4"),
    patch_author=LLMAgent(model="gpt-4"),
    code_reviewer=LLMAgent(model="gpt-4"),
    test_runner=TestRunnerAgent()
)

# Assign roles: human as code_reviewer, agents do the rest
workflow = orchestrator.create_workflow(
    human_role="code_reviewer",
    ai_roles=["task_planner", "patch_author", "test_runner"]
)

# Run repair workflow
bug_report = "Method fails when input is empty string"
result = workflow.execute(
    task_description=bug_report,
    code_context=source_code,
    test_suite=tests
)

# Human reviews and provides feedback
human_feedback = input("Approve patch? (yes/no/revise): ")
result.incorporate_feedback(human_feedback)

# Continue iteration until success
while not result.is_complete():
    result = workflow.iterate()
```

### Learning Resources

**For Educators**:
- Course curriculum templates
- Assignment design patterns
- Rubrics for evaluating student work
- Best practices for role rotation

**For Developers**:
- Code review checklists for AI-generated code
- Tools for understanding agent reasoning
- Debugging strategies for multi-agent systems
- Human-AI collaboration practices

## Related Work & Context

### Educational Technology

- **Immersive Learning**: Role-playing and simulation-based education
- **Scaffolding Theory**: Supporting learners through structured frameworks
- **Active Learning**: Learning through doing rather than lecture
- **Collaborative Learning**: Team-based problem solving

### Software Engineering Education

- **Code Review Education**: Teaching code review practices
- **Software Process Simulation**: Teaching workflow and methodology
- **Apprenticeship Model**: Learning through mentoring and observation
- **Problem-Based Learning**: Learning through real-world tasks

### Human-AI Interaction

- **Explainable AI**: Making AI decisions interpretable
- **Human-Centered AI**: Designing systems for human needs
- **Transparency and Trust**: Building user confidence in AI
- **Collaborative Agents**: Agents designed for human partnership

### Related Papers

- **Agents in the Wild**: Deployment challenges for agent systems
- **Beyond Self-Talk**: Communication in multi-agent systems
- **What Do Agents Communicate?**: Information exchange patterns
- **Multi-Agent Collaboration Surveys**: Orchestration and coordination

### Future Research Directions

1. **Extended Role Sets**
   - Add roles for deployment, monitoring, incident response
   - Support domain-specific roles (security, performance, etc.)
   - Investigate optimal team composition

2. **Adaptive Difficulty**
   - Difficulty adjustment based on learner performance
   - Personalized role assignment for learning
   - Progressive challenge increase

3. **Advanced Scaffolding**
   - Adaptive hints and guidance
   - Peer learning mechanisms
   - Mentor-based coaching

4. **Continuous Assessment**
   - Real-time learning measurement
   - Competency tracking over time
   - Skill development metrics

5. **Transfer and Generalization**
   - How learning in AgentForge transfers to real workflows
   - Cross-domain skill transfer
   - Long-term impact on professional practice

## Summary

AgentForge revolutionizes how developers learn to work with AI agents by placing them directly into functioning multi-agent systems and making agent reasoning transparent through role-based scaffolding. The core insight—that Code Reviewer role is cognitively the most demanding—challenges assumptions about automation and highlights the critical importance of human judgment in evaluating AI-generated code.

By decomposing software engineering workflows into four explicit roles (Task Planner, Patch Author, Code Reviewer, Test Runner) with visible intermediate artifacts, AgentForge enables novices to build intuitions about agent capabilities, limitations, and appropriate collaboration patterns. This pedagogical approach addresses a critical gap in AI literacy for the software engineering profession.

The findings have immediate practical implications: human review capacity is the bottleneck in human-AI collaborative development, suggesting that organizations should invest in human reviewer support rather than attempting to automate code review. The platform itself serves as both an educational tool and a laboratory for understanding multi-agent orchestration in software engineering.

For the future of agentic AI in software development, AgentForge provides both a blueprint for how to teach developers to work effectively with agents and empirical evidence about where human expertise remains indispensable. As AI agents become increasingly prevalent, this human-centered approach to multi-agent orchestration will become increasingly valuable.
