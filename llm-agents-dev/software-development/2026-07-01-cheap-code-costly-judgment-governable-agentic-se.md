# Cheap Code, Costly Judgment: A Case Study on Governable Agentic Software Engineering

**Paper:** [Cheap Code, Costly Judgment: A Case Study on Governable Agentic Software Engineering](https://arxiv.org/abs/2607.01087)  
**ArXiv ID:** 2607.01087  
**Submission Date:** July 1, 2026 (Revised: July 4, 2026)  
**Authors:** James C. Davis, Paschal C. Amusuo, Tanmay Singla, Berk Çakar, Kirsten A. Davis  
**Affiliations:** Purdue University

## Executive Summary

As generative AI makes code production abundant and inexpensive, software engineering faces a fundamental shift in what remains scarce: not implementation effort, but engineering judgment. This first-person longitudinal case study documents a 12-week journey building a production document accessibility system using frontier AI coding agents. Through 88 field notes and production metrics (420 KLOC code, 1.16 MLOC tests/docs/tooling), the authors develop a "governance conversion" theory explaining how high-velocity agentic work surfaces recurring structural failures that must be converted into durable governance mechanisms. The paper's central insight—"cheap code, costly judgment"—reframes the challenge of agentic software engineering: the bottleneck is no longer generating code, but creating the architecture, tools, evidence, and feedback systems that keep AI-mediated development inspectable, correctable, and maintainable.

## Problem Statement

### Development Automation Challenge

The arrival of capable AI coding agents has inverted the software engineering economic model:
- **Before**: Implementation effort was scarce; code generation was the bottleneck
- **Now**: Code generation is abundant and low-cost; judgment and governance are the bottleneck

This creates new engineering challenges:
- How do teams maintain control and visibility over high-velocity AI-generated code?
- How do they discover and fix systematic failures before they compound?
- How do they maintain long-term maintainability when agents generate vast quantities of code?
- How do they create feedback loops that improve agent performance over time?
- How do teams organize work so that human expertise focuses on high-value judgment?

### Prior Limitations

Traditional software engineering research assumes human implementation capacity is the constraint:
- **Traditional concern**: How to help developers code faster (tools, templates, assistance)
- **AI-era concern**: How to keep high-velocity agentic code production governable
- **Prior work** on AI-assisted development focuses on capability (can agents generate correct code?)
- **Overlooked gap**: governance (how do we maintain control over abundant code production?)

Literature on software governance (architectural decisions, code review, testing strategies) was developed in a regime of human-paced development:
- Code review processes assume manageable volume (10-100 LOC per review)
- Architectural review assumes humans understand and approve changes
- Testing assumes comprehensive human oversight
- All these break down when an agent generates 420 KLOC in 12 weeks

### Research Gap

No empirical research systematically documents:
1. **How expert engineers actually use AI agents** (what worked, what failed, lessons learned)
2. **What governance mechanisms emerge** from high-velocity agentic development
3. **How failure patterns surface and get addressed** in real projects
4. **What architectural and organizational changes** become necessary
5. **How judgment converts from human decision-making into durable controls**

This paper fills that gap through a longitudinal case study grounded in field notes and production metrics.

## Core Concepts & Theory

### The Economics of AI-Mediated Development

```
TRADITIONAL SOFTWARE ECONOMICS (Human-paced):
┌──────────────────────────────────────┐
│ Scarce Resource: Implementation       │
│ Abundant Resource: Human judgment     │
│ Engineering Focus: Help devs code     │
│ Rate-limiting factor: Person-hours    │
└──────────────────────────────────────┘

AI-ERA SOFTWARE ECONOMICS (Agentic):
┌──────────────────────────────────────┐
│ Scarce Resource: Judgment & control   │
│ Abundant Resource: Generated code     │
│ Engineering Focus: Governable systems │
│ Rate-limiting factor: System design   │
└──────────────────────────────────────┘
```

**Key Realization**: The cost structure of software engineering fundamentally changes:
- Code generation cost → near-zero (agent + compute)
- Testing cost → low (automated)
- Judgment cost → high (requires expert humans)
- Governance cost → high (must design for high velocity)
- Maintenance cost → potentially high (code not written by maintainers)

### Governance Conversion: From Failure to Control

The paper introduces **governance conversion** as the core process by which agentic high-velocity development becomes governable:

```
GOVERNANCE CONVERSION PROCESS:

1. Agent Exploration (High Velocity)
   └─ Agent rapidly generates implementations
      └─ Produces 420 KLOC in 12 weeks
         └─ Introduces variants, attempts, dead-ends

2. Structural Failure Emergence
   └─ Patterns of recurring failures surface
      └─ File organization issues appear
      └─ Interface inconsistencies emerge
      └─ Testing gaps become visible
         └─ Maintainability concerns crystallize

3. Engineering Judgment (Reflection)
   └─ Expert engineer analyzes failure patterns
      └─ Distinguishes systematic issues from accidents
      └─ Identifies root causes
         └─ "This failure type keeps recurring because..."

4. Governance Mechanism Creation (Institutionalization)
   └─ Convert insights into durable controls
      └─ Architectural decisions (enforce via code structure)
      └─ Linting rules (enforce via automation)
      └─ Testing requirements (enforce via CI/CD)
      └─ Code review guidelines (enforce via human gates)
         └─ Feedback loops in agent prompt design

5. Control Embedding (Prevention)
   └─ Mechanism prevents future failures
      └─ Agent prompts updated to avoid patterns
      └─ Architecture enforces constraints
      └─ Tests catch regressions
         └─ Cycle repeats at higher level of sophistication
```

**Key Insight**: Governance emerges from observed failures, not from pre-specified requirements. You cannot anticipate all control needs before development; instead, failures guide governance design.

### The "Cheap Code, Costly Judgment" Model

The paper's central metaphor captures the economic transformation:

**Code Production** (now cheap):
- Frontier AI agents generate correct, working code at ~0.5-2.0 USD per 1000 LOC
- Production: 420 KLOC cost ~$210-840 in compute (order of $1000)
- Human coding would cost $200,000+

**Judgment & Governance** (increasingly expensive):
- Engineer time analyzing failures: weeks of expert attention
- Designing governance mechanisms: architectural expertise required
- Testing/verification: must scale with code volume
- Maintenance planning: addressing long-term maintainability
- Cost: tens of thousands of dollars in expertise

**Net Economics**: Developer time shifts from implementation toward governance, architecture, judgment.

### Agent Failure Patterns & Categories

Through 88 field notes, five categories of recurring failures emerged:

#### 1. **Structural Inconsistency Failures**
- **Nature**: Agent generates code that violates project architecture
- **Example**: Component structure differs across modules; breaks expected patterns
- **Failure symptom**: Unexpected API, unclear interfaces, inconsistent abstractions
- **Conversion to control**: Architectural guidelines → linting rules → agent prompt constraints

#### 2. **Interface Boundary Failures**
- **Nature**: Agent generates code at module boundaries that doesn't match expectations
- **Example**: Function signatures incomplete; return types underdefined; error handling inconsistent
- **Failure symptom**: Integration tests fail; APIs don't compose as expected
- **Conversion to control**: Interface specifications → type system enforcement → testing requirements

#### 3. **Testing Gap Failures**
- **Nature**: Agent generates code with insufficient test coverage or wrong test focus
- **Example**: Happy path tested; edge cases untested; error conditions not validated
- **Failure symptom**: Tests pass locally; production finds new failure modes
- **Conversion to control**: Explicit test coverage requirements → automated checkers → code review gates

#### 4. **Maintenance Burden Failures**
- **Nature**: Code is correct but difficult to maintain (unclear intent, poor naming, missing documentation)
- **Example**: Algorithm implementation works but is hard for others to modify; shortcuts reduce readability
- **Failure symptom**: Future engineers struggle to understand/extend code
- **Conversion to control**: Maintainability guidelines → documentation requirements → review processes

#### 5. **Domain Knowledge Gaps**
- **Nature**: Agent generates code that works in simple cases but misses domain complexities
- **Example**: Accessibility remediation logic incorrect for specific disability categories; doesn't account for regulatory nuances
- **Failure symptom**: Works for obvious cases; fails for edge cases requiring domain expertise
- **Conversion to control**: Domain specification → test cases → expert review gates

## Main Ideas & Contributions

### 1. **Governance Conversion Theory**

First systematic theory explaining how high-velocity agentic development becomes governable:
- **Empirical grounding**: 12 weeks of field observations
- **Process model**: Failure → Analysis → Mechanism → Prevention
- **Practical insight**: Don't try to pre-specify all controls; let failures guide governance design
- **Scalability implication**: Control mechanisms grow organically as agent activities expand

### 2. **Inversion of Software Economics**

Reframes the engineering challenge:
- **Old frame**: Code generation is expensive; help developers code faster
- **New frame**: Code generation is cheap; make abundant code governable
- **Implication**: Future software engineering invests in judgment, architecture, governance
- **Prediction**: Individual contributor skill ≠ code generation speed; = design/judgment quality

### 3. **Empirical Longitudinal Documentation**

Unprecedented level of detail on real agentic development:
- 88 field notes capturing decision points
- 420 KLOC of production code (actual working system)
- 1.16 MLOC of supporting artifacts (tests, tooling, documentation)
- 12-week continuous project (enough time to see patterns repeat)

### 4. **Architectural Patterns for Agentic Development**

Identifies specific patterns that emerged during the project:
- **Pattern 1**: Separate agent concerns from human judgment (agent generates → human reviews)
- **Pattern 2**: Make control mechanisms discoverable (governance via code structure, not just process)
- **Pattern 3**: Use tests as specifications (tests define expected behavior; agent implements)
- **Pattern 4**: Iterative refinement of prompts (failures guide prompt improvement)
- **Pattern 5**: Maintain durable documentation (agent forgets; documentation captures decisions)

## Methodology & Implementation

### 12-Week Case Study Design

**Project Description**:
- **Domain**: Document accessibility remediation (real-world application, non-trivial)
- **Scale**: 420 KLOC production code
- **Supporting code**: 1.16 MLOC (tests, lints, docs, tooling)
- **Duration**: 12 consecutive weeks
- **Team**: Single expert engineer + frontier AI agents
- **Goal**: Build production-quality accessibility remediation system

**Why this design?**
- Single engineer ensures consistent perspective
- Accessibility domain is rigorous (regulatory requirements, accessibility standards, testing frameworks)
- 12 weeks is long enough to see failure patterns repeat and governance mechanisms mature
- Production-quality mandate forces dealing with real challenges, not toy examples

### Data Collection Methods

**Field Notes (88 total)**:
- Contemporaneous observations, not retrospective analysis
- Capture decision points: "Why did I choose this architecture?"
- Document failures: "This test failed; here's why..."
- Record governance decisions: "I added this linting rule because..."
- Preserve the messiness of real development

**Code Artifacts**:
- Production code: The actual working system (420 KLOC)
- Test code: Automated testing (included in 1.16 MLOC)
- Linting/formatting rules: Enforced code style (included in 1.16 MLOC)
- Documentation: Architectural decisions, patterns, lessons (included in 1.16 MLOC)
- Agent prompts: Instructions guiding agent behavior (documented)

**Metrics**:
- Lines of code generated: 420 KLOC production
- Lines of supporting code: 1.16 MLOC (tests, tooling, docs)
- Code velocity: ~35 KLOC per week of production code
- Time to detect failure patterns: typically 2-3 occurrences
- Time from failure detection to governance implementation: 1-3 days

### Failure Analysis & Governance Conversion Examples

**Example 1: Structural Inconsistency → Architectural Linting**

**Observed Failure**: Agent generated accessibility check functions with inconsistent signatures:
```
// File A: accessibility/validators.js
function validateColor(element) { /* returns { pass: bool, reason: string } */ }

// File B: accessibility/auditor.js  
function auditFont(element) { /* returns { errors: string[] } */ }

// File C: accessibility/checker.js
function checkContrast(element) { /* returns bool */ }
```

**Problem**: Inconsistent return types; callers can't use validators in uniform way

**Governance Conversion**:
1. **Recognition**: After seeing 8th inconsistent signature, pattern became obvious
2. **Root cause analysis**: Agent wasn't given explicit interface specification
3. **Mechanism design**: Define canonical interface specification document
4. **Control implementation**: Add linting rule to enforce signature consistency; update agent prompt with interface specification
5. **Result**: No further structural inconsistencies in this category

**Example 2: Testing Gap → Explicit Coverage Requirements**

**Observed Failure**: Agent generated happy-path tests; production hit edge case:
```
// Test: colorContrast('white', 'black') ✓
// Test: colorContrast('red', 'green') ✓
// Production bug: colorContrast('#FFF', '#000') ✗ (didn't handle hex format)
```

**Problem**: Tests didn't specify all input format requirements

**Governance Conversion**:
1. **Recognition**: Third testing gap incident
2. **Root cause analysis**: Agent tests only obvious cases; edge cases need explicit specification
3. **Mechanism design**: Create formal specification of test cases for each function (input domains, edge cases, error conditions)
4. **Control implementation**: Code review enforces test case coverage; CI/CD checks test counts against specification
5. **Result**: Subsequent functions include comprehensive test coverage

**Example 3: Domain Knowledge Gap → Domain Review Gate**

**Observed Failure**: Accessibility remediation logic missed nuance in WCAG compliance:
```
// Agent's logic: If contrast ratio > 4.5, accessible
// But: WCAG has different thresholds for different font sizes
// And: Different requirements for graphics vs. text
```

**Problem**: Agent doesn't understand domain-specific regulatory nuances

**Governance Conversion**:
1. **Recognition**: First error review by accessibility specialist
2. **Root cause analysis**: Agent needs explicit domain knowledge, not inferrable from code patterns
3. **Mechanism design**: Create domain specification document; create domain expert review checklist
4. **Control implementation**: Domain expert reviews all accessibility logic before deployment
5. **Result**: Subsequent implementations correctly handle regulatory nuances

### Supporting Systems & Tools

**Agents Used**:
- Frontier code generation model (Claude, GPT-4, similar)
- Multi-tool orchestration via agent harness
- Iterative planning and error recovery

**Testing Infrastructure**:
- Unit tests: Automated function-level testing
- Integration tests: Component interaction validation
- Accessibility testing: Automated + manual checks
- Performance testing: Scalability verification

**Governance Tools**:
- Linting frameworks: ESLint with custom rules
- Code review process: GitHub PRs with human review gates
- CI/CD pipeline: Automated testing + deployment gates
- Documentation system: Markdown + versioned decision logs

**Metrics & Monitoring**:
- Code quality metrics: Coverage, complexity, duplication
- Velocity metrics: KLOC per week, time per feature
- Quality metrics: Bug rates, test passage rates
- Governance metrics: Governance mechanism coverage, enforcement effectiveness

## Practical Applications & Use Cases

### 1. **Enterprise Development Teams**

**Scenario**: Large organization adopting AI coding agents
- **Challenge**: Velocity increases 5x; existing governance cannot scale
- **Application**: Use governance conversion to evolve controls organically
- **Outcome**: Maintain code quality + maintainability despite high velocity

**Process**:
```
Week 1-2: Agents generate rapidly; failures surface
Week 3-4: Analyze failure patterns; design governance
Week 5-6: Implement controls; retrain agents on new constraints
Week 7+: Mature governance; velocity remains high, quality maintained
```

### 2. **Startups with Limited Engineering Resources**

**Scenario**: Small team needs to move fast; limited expertise
- **Challenge**: Can't review all code; need quality + speed
- **Application**: Use structured governance to scale team beyond human capacity
- **Outcome**: Small team + agents produce output of large team

**Key pattern**: Governance becomes the multiplier:
- Architect designs system; agents implement
- Architect specifies tests; agents pass them
- Architect reviews critical paths; agents handle the rest

### 3. **Legacy Modernization**

**Scenario**: Refactoring large old codebase
- **Challenge**: Refactoring is boring, error-prone; hard to coordinate across team
- **Application**: Agents do refactoring; governance ensures no regressions
- **Outcome**: Modernize faster; improve code quality; reduce human effort

### 4. **Cross-Functional Development**

**Scenario**: Product feature requires backend + frontend + infrastructure
- **Challenge**: Coordination overhead; integration points error-prone
- **Application**: Agents implement components; governance ensures compatibility
- **Outcome**: Faster feature delivery; fewer integration bugs

### Integration Challenges & Scalability

**Challenge 1: Governance Lag**
- As agent velocity increases, governance discovery can lag
- Solution: Proactive pattern monitoring; predictive governance design
- Time investment: Small team watching for patterns

**Challenge 2: Expertise Requirements**
- Governance design requires domain + engineering expertise
- Solution: Codify expertise in specifications, tests, review checklists
- Time investment: Initial investment in specification; payoff over time

**Challenge 3: Control Brittleness**
- Controls can be overly rigid; block useful agent adaptations
- Solution: Regular governance review; adjust controls as agent capability improves
- Time investment: Quarterly governance audit

**Challenge 4: Testing Coverage**
- High-velocity development can outpace test writing
- Solution: Automated test generation; agent-assisted testing
- Time investment: Investment in testing infrastructure

### Cost & Latency Implications

**Code Production Cost**: ~$1000 for 420 KLOC
- Agent compute: $500-800
- API costs: $200-400
- Verification/testing: $100-300

**Judgment/Governance Cost**: ~$50,000-100,000
- Engineer time analyzing failures: $20,000-30,000
- Designing governance mechanisms: $15,000-25,000
- Testing/verification infrastructure: $10,000-25,000
- Documentation/knowledge capture: $5,000-10,000

**Total Development Cost**: ~$50,000-100,000 (vastly cheaper than hand-coded equivalent)
- Hand-coding equivalent: $400,000-600,000
- **Savings**: 80-90% reduction in development cost

**Latency Trade-offs**:
- Agent generation: fast (~hours for 420 KLOC)
- Governance design: moderate (~weeks to mature)
- Total project time: 12 weeks (faster than traditional development)

## Insights & Implications

### 1. **The Death of "Cheap" Code**

Counterintuitive finding: As code becomes abundant (cheap), total project costs don't decrease linearly:
- **Code generation cost**: ↓ dramatically (near-zero)
- **Judgment cost**: ↑ (becomes bottleneck)
- **Governance cost**: ↑ (scales with volume)
- **Net effect**: Total cost may decrease, but the composition changes

**Implication**: Optimize for judgment, not for code generation speed.

### 2. **Governance is Discovered, Not Designed**

Traditional software engineering tries to specify all controls upfront (architecture, process, rules). In agentic development:
- Controls emerge from observed failures
- Governance design is iterative
- The first attempt at governance is always wrong
- Success requires reflecting on failures and refining

**Implication**: Expect and budget for governance evolution.

### 3. **Human Expertise Shifts, Not Disappears**

The paper disproves "agents replace humans" narrative:
- Humans shift from code implementation to code judgment
- Human expertise becomes more, not less, valuable
- The bottleneck moves from "can we generate code?" to "can we govern high-velocity code?"

**Implication**: Future demand for architecture, design, and judgment skills will increase.

### 4. **Maintainability Requires Intentionality**

Code generated at high velocity is at risk for maintainability crisis:
- Agents lack context for future modifications
- Code volume makes understanding cost
- Solutions: explicit documentation, maintainability governance, knowledge capture

**Implication**: Maintainability investment must scale with velocity.

### 5. **Limitations & Open Questions**

The paper acknowledges limitations:
- **Single case study**: Generalization to other domains/teams unclear
- **Single engineer perspective**: Team dynamics not captured
- **12-week horizon**: Long-term maintainability patterns unknown
- **Domain specificity**: Accessibility remediation may not generalize
- **Specific models**: Findings may be specific to frontier models used

**Open questions**:
- How do governance mechanisms scale to multiple teams?
- What governance patterns generalize across domains?
- How do governance mechanisms evolve as agent capability improves?
- What organizational structures enable effective governance?

## Code & Resources

### Artifacts & Availability
- Production system: Document accessibility remediation system (domain-specific)
- Code metrics: 420 KLOC production, 1.16 MLOC supporting code
- Field notes: 88 contemporaneous observations
- Governance mechanisms: Linting rules, test specifications, review checklists

### Dependencies & Tools
- Code generation: Frontier LLM (Claude, GPT-4, similar)
- Testing: Standard testing frameworks (Jest, pytest, etc.)
- Linting: ESLint with custom rules
- CI/CD: GitHub Actions or similar
- Documentation: Markdown with version control

### Quick-Start Integration Guide

**Step 1: Establish Baseline**
```
1. Define project scope
2. Set up agent + human workflow
3. Begin development; collect observations
4. Record decisions in field notes
```

**Step 2: Monitor for Failure Patterns**
```
1. Watch for recurring issues
2. After 2-3 occurrences, begin failure analysis
3. Identify root cause; design mechanism
4. Implement control (linting rule, test spec, review gate)
```

**Step 3: Evolve Governance**
```
1. Quarterly review of failure patterns
2. Identify new governance gaps
3. Update agent prompts based on learnings
4. Relax overly restrictive controls
5. Mature governance incrementally
```

**Step 4: Scale Carefully**
```
1. Document proven governance mechanisms
2. Extend to new domains/teams carefully
3. Adapt mechanisms to local context
4. Monitor effectiveness in new context
5. Share learnings across organization
```

## Related Work & Context

### Foundational Software Engineering Research
- **Software architecture**: Design patterns, architectural decisions documentation
- **Software process**: Agile, DevOps, continuous integration
- **Code review**: Research on review effectiveness, scaling review
- **Testing**: Test-driven development, test coverage, mutation testing

### Complementary Approaches
- **Agent capability research**: Improving model reasoning, planning, tool use
- **Harness engineering** (see related paper): Runtime substrate for agent reliability
- **Formal verification**: Mathematical proofs of code correctness
- **DevOps automation**: CI/CD pipelines, deployment automation

### Future Research Directions

1. **Multi-Engineer Teams**: How do governance mechanisms evolve in team settings?
2. **Cross-Domain Generalization**: What governance patterns transfer across domains?
3. **Organizational Scale**: How do teams manage governance across 100+ agents?
4. **Dynamic Governance**: Can we learn optimal governance policies from failure data?
5. **Long-Term Maintainability**: How do AI-generated systems age? What's the technical debt trajectory?
6. **Governance Automation**: Can systems automatically discover and implement governance mechanisms?

## Key Takeaways

1. **Economics Inversion**: Code is now cheap; judgment is expensive
2. **Governance Conversion**: High-velocity development surfaces failures; judgment converts them to durable controls
3. **Empirical Evidence**: 420 KLOC production system demonstrates viability + challenges
4. **Pattern Discovery**: Failures guide governance design; don't try to pre-specify all controls
5. **Scalability Path**: Governance mechanisms discovered organically; can scale to teams/domains incrementally
6. **Human Future**: Expertise doesn't disappear; shifts from implementation to architecture/judgment

## References

- **Paper**: [Cheap Code, Costly Judgment: A Case Study on Governable Agentic Software Engineering](https://arxiv.org/abs/2607.01087)
- **ArXiv**: 2607.01087
- **Citation**: Davis, J. C., Amusuo, P. C., Singla, T., Çakar, B., & Davis, K. A. (2026). Cheap Code, Costly Judgment: A Case Study on Governable Agentic Software Engineering. arXiv preprint arXiv:2607.01087.
