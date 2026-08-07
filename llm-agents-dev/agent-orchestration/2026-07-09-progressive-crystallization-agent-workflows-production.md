# Progressive Crystallization: Turning Agent Exploration into Deterministic, Lower-Cost Workflows in Production

**ArXiv ID:** [2607.07052](https://arxiv.org/abs/2607.07052)  
**Authors:** Arun Malik (Microsoft Azure, AIOps)  
**Submitted:** July 9, 2026  
**Field:** Artificial Intelligence, Operations Research, Software Engineering  

---

## Executive Summary

AI agents deployed for IT operations become permanent cost centers when every execution requires full LLM inference, even for previously solved problems. Progressive Crystallization introduces a three-stage execution model that systematically converts agentic exploration into deterministic, lower-cost workflows. The approach captures successfully validated agent behaviors as reusable playbooks while demoting workflows that regress. Evaluated on a production cloud networking AIOps system processing tens of thousands of incidents monthly, Progressive Crystallization achieves up to **3x cost reduction** while maintaining or improving resolution quality through evidence-based promotion of agent-discovered solutions into deterministic automation.

---

## Problem Statement

### Development Automation Challenge

Today's approach to agent-based IT operations creates unsustainable economics:

1. **Perpetual inference costs** - Every incident (even recurring ones) triggers full LLM inference
2. **Exploration overhead** - Agents re-explore solution space for incidents they've previously solved
3. **Decision paralysis** - Approval gates slow down well-understood operational changes
4. **Knowledge loss** - Successful agent behaviors aren't captured for future use

### Prior System Limitations

- **Static playbooks:** Traditional IT automation requires humans to write procedures; can't adapt to novel situations
- **Agent-only approaches:** Agents handle novel incidents well but waste resources on known problems
- **No learning pipeline:** Successful agent behaviors disappear after execution; no mechanism to extract lessons
- **Binary automation:** Systems choose between "full agent" (expensive) or "full automation" (brittle)

### Research Gap

The field lacks a principled framework for converting agentic exploration into deterministic automation. How do we systematically capture agent-discovered solutions? When is automation safe vs. requiring approval? How do we handle regression without losing all automation gains?

---

## Core Concepts & Theory

### Three-Stage Execution Taxonomy

Progressive Crystallization introduces three execution stages representing increasing levels of determinism:

```
Stage 1: Type 1 - Fully Agent-Orchestrated (Most Flexible)
├─ Scenario: Novel problem with no matching playbook
├─ Execution: Agent investigates using all available tools
├─ Decision-making: Agent chooses all actions autonomously
├─ Write operations: All require human approval
├─ Cost: Highest (full inference + human review)
└─ Resolution guarantee: Medium-high (agent quality dependent)

Stage 2: Type 2 - Hybrid (Balanced)
├─ Scenario: Partially known problem (some playbook coverage)
├─ Execution: Agent uses playbook for known steps, explores novel areas
├─ Decision-making: Deterministic for playbook paths, agentic otherwise
├─ Write operations: Approved playbook actions auto-execute, novel actions require review
├─ Cost: Medium (partial inference + selective review)
└─ Resolution guarantee: High (deterministic baseline + agent augmentation)

Stage 3: Type 3 - Fully Deterministic (Most Economical)
├─ Scenario: Completely solved problem (full playbook coverage)
├─ Execution: Pure playbook-driven automation
├─ Decision-making: No LLM required; follow predetermined steps
├─ Write operations: Auto-execute with safety guardrails
├─ Cost: Lowest (computation only, no inference)
└─ Resolution guarantee: Highest (tested, proven playbook)
```

### Execution Taxonomy Visualization

```
Cost vs. Determinism Trade-off:

Cost
(Inference + Human)
      ▲
      │                  Type 1 (Agentic)
      │                      ●
      │                     /│\
      │                    / │ \
      │                   /  │  \
      │                  /   │   \
      │                 /    │    \
      │                /     │     \
      │          Type 2      │      \  (Hybrid)
      │        (Hybrid)      │        ●
      │           ●          │       /│\
      │            \         │      / │ \
      │             \        │     /  │  \
      │              \       │    /   │   \
      │               \      │   /    │    \
      │                \     │  /     │     \
      │                 \    │ /      │      \
      │                  \   │/   Type 3      \
      │                   \  ●        (Deterministic)
      │                    \(Playbook-driven automation)
      │
      └──────────────────────────────────────► Determinism
         Low                                  (Repeatability)
```

### Evidence-Based Promotion Mechanism

```
Promotion Pipeline (Agentic → Deterministic):

Stage 1: Agent Exploration
  ├─ Agent encounters novel incident
  ├─ Performs investigation and root-cause diagnosis
  ├─ Selects and executes remediation actions
  ├─ All write operations require human approval
  └─ Actions recorded in execution trace

Stage 2: Success Validation
  ├─ Verify incident is resolved
  ├─ Confirm no regressions or side effects
  ├─ Analyze solution path (sequence of actions)
  └─ Score solution quality and applicability

Stage 3: Pattern Extraction
  ├─ Identify repeatable patterns in solution
  ├─ Generalize from specific incident to class of incidents
  ├─ Extract decision points and branches
  ├─ Define applicability conditions
  └─ Create Type 2 hybrid playbook template

Stage 4: Validation & Testing
  ├─ Validate playbook against historical incidents
  ├─ Run simulations on test scenarios
  ├─ Verify deterministic version produces correct outcomes
  └─ Get expert approval before deployment

Stage 5: Deployment as Type 2
  ├─ Deploy hybrid playbook to production
  ├─ Pre-determined steps execute automatically
  ├─ Novel steps still routed to agent
  ├─ Monitor for correctness and regression
  └─ Collect feedback for Type 3 promotion

Stage 6: Continuous Refinement
  ├─ Type 2 execution generates more data
  ├─ As coverage approaches 100%, consider Type 3
  ├─ Extract full deterministic playbook (Type 3)
  ├─ Deploy with maximum automation
  └─ Monitor for regressions and update applicability conditions

Stage 7: Regression Handling
  ├─ If Type 3 playbook fails on new incident variant
  ├─ Demote back to Type 2 or Type 1
  ├─ Investigate failure cause
  ├─ Update applicability conditions or decision logic
  └─ Promote again when fixed and validated
```

### Incident Classification for Playbook Matching

```
Incident Feature Space for Playbook Retrieval:

Features extracted from incident:
├─ Symptom category (latency, error rate, unavailability)
├─ Affected service/component
├─ Scope (single instance, region, global)
├─ Time characteristics (sudden vs. gradual onset)
├─ Related alert patterns
├─ Historical similarity metrics
└─ Causal context (related to recent deployment, etc.)

Matching Algorithm:
├─ Exact match → Use Type 3 playbook
├─ Partial match → Use Type 2 hybrid playbook
├─ No match → Invoke Type 1 agent exploration
└─ Confidence score determines execution stage
```

---

## Main Ideas & Contributions

### 1. Three-Stage Execution Model

**Contribution:** Formal taxonomy moving from fully agentic to deterministic execution.

- **Flexibility spectrum:** Type 1 (full exploration) → Type 2 (hybrid) → Type 3 (automation)
- **Cost progression:** High → Medium → Low
- **Determinism progression:** Low → Medium → High
- **Economic sustainability:** Enables amortization of LLM costs across incident types

### 2. Evidence-Based Promotion Mechanism

**Contribution:** Principled approach to converting agentic behaviors into deterministic automation.

- **Execution trace capture:** Record all agent actions and decisions for analysis
- **Pattern extraction:** Identify repeatable sequences in successful resolutions
- **Generalization:** Abstract specific incidents into generalizable playbook
- **Validation pipeline:** Rigorous testing before promotion to deterministic automation
- **Regression detection:** Automatic demotion when deterministic playbooks fail

### 3. Production Deployment Validation

**Contribution:** Grounded evaluation on production AIOps system with tens of thousands of incidents.

- **Real incident patterns:** Not synthetic test cases; actual customer incidents
- **At-scale performance:** Measured on production infrastructure with 200+ services
- **Cost impact:** Quantified savings from automation vs. agentic execution
- **Reliability analysis:** Regression rates and mitigation strategies

### 4. Smart Playbook Matching

**Contribution:** ML-based incident-to-playbook matching enabling efficient exploration + exploitation.

- **Feature-based retrieval:** Match incidents to applicable playbooks using incident features
- **Confidence scoring:** Calibrated confidence in playbook applicability
- **Fallback mechanisms:** Graceful degradation from Type 3 → Type 2 → Type 1
- **Continuous learning:** Improve matching accuracy from historical matches

### 5. Hybrid Type 2 Execution Model

**Contribution:** Balanced approach combining deterministic automation with agentic flexibility.

- **Playbook guidance:** Follow predetermined steps for known problem aspects
- **Agent augmentation:** Agents handle novel problem aspects not covered by playbook
- **Selective approval:** Human approval only for agent-chosen actions, not playbook steps
- **Smooth transition:** Type 2 naturally progresses toward Type 3 as coverage improves

---

## Methodology & Implementation

### Experimental Setup

**Deployment Environment:** Production Microsoft Azure Networking AIOps system

- **Incident volume:** 50,000+ incidents/month across infrastructure
- **Service scope:** 200+ network services and infrastructure components
- **Incident types:** Latency anomalies, reachability issues, configuration problems, capacity limits

**Baseline Comparison:**

1. **Type 1 Only (baseline):** All incidents handled by agent exploration
2. **Playbook Only (naive):** All incidents attempted with deterministic playbooks regardless of match
3. **Progressive Crystallization (proposed):** Adaptive three-stage execution with intelligent matching

### Metrics & Evaluation Protocol

**Primary Metrics:**

- **Mean Time to Resolution (MTTR):** Time from incident detection to resolution
- **Resolution Success Rate:** % of incidents with correct resolution
- **Cost per incident:** LLM inference + human review costs
- **Regression rate:** % of incidents where automated playbook failed

**Efficiency Metrics:**

- **Cost reduction ratio:** Cost of deterministic vs. agentic execution
- **Automation coverage:** % of incidents handled by Type 2/3 (not requiring agent reasoning)
- **Human review burden:** Number of incidents requiring human approval

### Results and Analysis

**Overall Cost Impact:**

```
Cost Reduction by Execution Type

Incident Category    Type 1 (Agent)  Type 2 (Hybrid)  Type 3 (Deterministic)  Savings
─────────────────────────────────────────────────────────────────────────────────────
DNS failures         $50/incident    $15/incident    $2/incident            96%
Connection issues    $45/incident    $18/incident    $3/incident            93%
Performance issues   $80/incident    $35/incident    $8/incident            90%
Config problems      $60/incident    $20/incident    $5/incident            92%

Organization Average: $60/incident → $20/incident (Type 2 hybrid)
                    → $5/incident (Type 3 deterministic)
                    = 67% → 92% cost reduction
```

**Progression Stages Over Time:**

```
Incident Resolution Distribution (Over 6 Months)

Month 1: Initial deployment (mostly Type 1)
  Type 1: 92%  | Type 2: 6%   | Type 3: 2%
  
Month 2: First playbooks automated (Type 2 emergence)
  Type 1: 75%  | Type 2: 20%  | Type 3: 5%
  
Month 3: Common incidents automated (Type 3 growth)
  Type 1: 60%  | Type 2: 25%  | Type 3: 15%
  
Month 4: Playbook refinement (increased Type 3)
  Type 1: 45%  | Type 2: 28%  | Type 3: 27%
  
Month 5: Mature automation (Type 3 dominance)
  Type 1: 38%  | Type 2: 25%  | Type 3: 37%
  
Month 6: Equilibrium (new incident types drive Type 1)
  Type 1: 35%  | Type 2: 22%  | Type 3: 43%

Key Finding: Reaches equilibrium where 35-40% of incidents
benefit from deterministic automation, reducing overall costs by 3x
```

**Regression Analysis:**

```
Regression Rate by Playbook Age

Playbook Age    Type 2 Regression    Type 3 Regression
─────────────────────────────────────────────────────
< 1 week        0.2%                 1.5%
1-4 weeks       0.5%                 2.1%
1-3 months      1.2%                 3.8%
3+ months       2.5%                 6.2%

Mitigation:
├─ Weekly playbook validation: catch 70% of emerging regressions
├─ Automatic demotion: prevent cascading failures
├─ ML anomaly detection: flag unusual patterns in Type 3
└─ Monthly playbook refresh: update for environmental changes
```

**Type 2 vs. Type 3 Effectiveness:**

```
Execution Quality Metrics

Metric                          Type 2 Hybrid    Type 3 Deterministic
─────────────────────────────────────────────────────────────────────
Avg Resolution Time             8 min            4 min
Success Rate                     94%              92%
Human Review Rate                18%              0%
Regression Rate                  1.8%             4.2%
Cost per incident                $20              $5
User Satisfaction                4.1/5            3.9/5

Trade-off: Type 3 cheaper but higher regression; Type 2 balances
cost savings with quality. Hybrid Type 2 often optimal choice.
```

### Agent Topologies and Workflows

**Playbook Extraction Workflow:**

```
Agent-Discovered Solution → Crystallized Playbook

1. Agent Execution (Type 1)
   ├─ Identify root cause: [service X degradation due to resource leak]
   ├─ Perform investigation: [trace logs, metrics analysis]
   ├─ Execute remediation: [restart service, trigger garbage collection]
   └─ Record all actions in execution trace

2. Pattern Recognition
   ├─ Analyze trace: [sequence of diagnostic commands]
   ├─ Identify decision points: [IF high memory THEN restart]
   ├─ Extract generalizable conditions: [memory > 80% AND response_time > 2s]
   └─ Create playbook template

3. Validation
   ├─ Test against 100 similar historical incidents
   ├─ Simulate against synthetic test data
   ├─ Expert review and approval
   └─ Define applicability scope

4. Type 2 Deployment
   ├─ Predetermined steps: [check service health, gather metrics, restart]
   ├─ Agent-driven: [root cause analysis for novel scenarios]
   ├─ Approval required: [agent-chosen restart actions]
   └─ Monitor outcomes

5. Type 3 Promotion
   ├─ After Type 2 covers 95%+ of cases
   ├─ Fully deterministic: [automatic restart + verification]
   ├─ No approval needed: [well-tested, proven safe]
   └─ Monitor regression rates
```

**Three-Stage Runtime Decision Tree:**

```
Incident Detection
    ↓
Search Playbooks
    ├─ High Confidence Match (>90%)
    │  └─ Type 3 Execution: Use deterministic playbook
    │
    ├─ Medium Confidence Match (60-90%)
    │  └─ Type 2 Execution: Hybrid (playbook + agent)
    │
    └─ Low Confidence Match (<60%)
       └─ Type 1 Execution: Full agent exploration
```

---

## Practical Applications & Use Cases

### IT Operations at Scale

1. **Database Performance Issues**
   - Discovery (Type 1): Agent diagnoses slow queries, missing indexes
   - Crystallization (Type 2): Playbook for common slow queries; agent for novel ones
   - Maturity (Type 3): Automatic index creation with confidence scoring

2. **Service Degradation**
   - Discovery: Agent traces cascade failures, identifies root service
   - Crystallization: Playbook for known cascade patterns; agent for anomalies
   - Maturity: Automatic circuit breaker engagement, request shedding

3. **Configuration Drift**
   - Discovery: Agent detects config mismatches, proposes corrections
   - Crystallization: Playbook for common drift patterns
   - Maturity: Automatic config reconciliation with human audit logs

### Cost-Benefit Analysis

**Example: DNS Failure Incidents**

```
Scenario: 50 DNS failure incidents per month

Type 1 Only (Pure Agent):
  Cost: 50 × $50/incident = $2,500/month
  MTTR: 12 min average
  Success: 92%

Type 3 Crystallized (After learning):
  Cost: 50 × $2/incident = $100/month  (98% reduction!)
  MTTR: 2 min average
  Success: 89%

Type 2 Hybrid (Balanced approach):
  Cost: 50 × $15/incident = $750/month  (70% reduction)
  MTTR: 6 min average
  Success: 94%

Recommendation: Start with Type 2 to balance cost savings and reliability
```

### Integration Challenges

**Playbook Fragility:**
- Environmental changes break deterministic assumptions
- Mitigation: Weekly validation, automated regression detection, graceful demotion

**Coverage Gaps:**
- Not all incidents fit existing playbooks
- Mitigation: Type 1 always available as fallback; Type 2 bridges gap

**Skill Evolution:**
- Agents improve over time; older playbooks become suboptimal
- Mitigation: Periodic playbook refresh, A/B testing of new versions

**Scalability Considerations:**

| Phase | Total Incidents | Type 1 | Type 2 | Type 3 | Total Cost | Cost Trend |
|-------|-----------------|--------|--------|---------|-----------|-----------|
| Month 1 | 1000 | 900 | 80 | 20 | $51,000 | Baseline |
| Month 3 | 1200 | 720 | 300 | 180 | $28,000 | -45% |
| Month 6 | 1500 | 525 | 330 | 645 | $15,000 | -71% |
| Month 12 | 1800 | 630 | 396 | 774 | $16,000 | -69% |

---

## Insights & Implications

### Impact on Agent-Driven Development Systems

1. **Economic sustainability:** Agents become viable for production only if costs decrease over time
2. **Hybrid future:** Pure agentic systems insufficient; hybrid Type 2 is likely production norm
3. **Automation taxonomy:** Organizations need framework for reasoning about automation levels

### Advancement in Autonomous Software Engineering

- **CI/CD automation:** Agents explore novel test/deploy strategies; crystallize successful patterns
- **Code generation:** Agents explore alternative implementations; convert best-performing to templates
- **Monitoring:** Agents explore novel detection rules; automate proven rules with guardrails

### Limitations and Open Questions

1. **Generalization:** Do findings hold across different operational domains?
2. **Agent quality:** How does agent error rate affect crystallization success?
3. **Behavioral drift:** How to detect when agents' behavior has drifted from original playbooks?
4. **Playbook conflicts:** How to handle conflicting playbooks in overlapping incident domains?

### Relevance to Skill Frameworks

- **Skill crystallization:** Agents develop skills through exploration; successful skills crystallized into reusable procedures
- **Skill versioning:** Different skill versions (Types 1-3) coexist with intelligent selection
- **Skill evolution:** Continuous feedback enables skill improvement and promotion

---

## Code & Resources

### Official Repository & Libraries

- **ArXiv Paper:** https://arxiv.org/abs/2607.07052
- **Implementation:** Microsoft Azure AIOps (production system details in paper)

### Playbook Format & Template

```yaml
name: "DNS Failure Playbook"
id: "playbook_dns_failure_v2"
type: "hybrid"  # Type 2 (agent-augmentable)
applicability:
  symptom: "DNS resolution failures"
  affected_service: "DNS resolver"
  confidence_threshold: 0.75

deterministic_steps:
  - step: 1
    action: "Check DNS service health"
    command: "systemctl status dns-resolver"
    expected_output: "active (running)"
  
  - step: 2
    action: "Verify DNS server reachability"
    command: "nslookup google.com @localhost"
    expected_output: "successfully resolved"
  
  - step: 3
    action: "Gather diagnostic metrics"
    commands:
      - "dns-query-latency-over-5m"
      - "dns-failure-rate-over-5m"

agentic_steps:
  - step: 4
    trigger: "If DNS service is down"
    agent_task: "Diagnose why DNS service crashed (logs, recent changes)"
    approval_required: true
    action_options:
      - "Restart DNS service"
      - "Rollback recent config change"
      - "Increase DNS service resources"

verification:
  - "DNS queries succeed from multiple test clients"
  - "DNS query latency returns to baseline (<10ms)"
  - "Error rate drops below 0.1%"

rollback:
  - "If verification fails: revert all changes"
  - "Escalate to Type 1 agent for investigation"
```

### Dependencies & Requirements

- **Compute:** Production AIOps infrastructure
- **Storage:** Incident history, playbook versions, execution traces
- **Agent:** Full reasoning agent for Type 1 exploration
- **Testing:** Simulation environment for playbook validation

### Quick-Start Integration Guide

1. **Instrument agent execution:** Capture traces from all agent operations
2. **Build playbook extraction:** ML pipeline to extract patterns from successful resolutions
3. **Implement three-stage dispatch:** Route incidents based on playbook confidence
4. **Deploy Type 2 hybrids:** Start with low-confidence playbooks requiring agent augmentation
5. **Monitor and promote:** Track Type 2 performance; promote to Type 3 when ready
6. **Handle regressions:** Automatic demotion and retraining when deterministic playbooks fail

---

## Related Work & Context

### Related Papers on Automation Crystallization

- **Progressive Formalization:** Converting implicit knowledge into explicit procedures
- **Hybrid Automation:** Combining deterministic and agentic approaches
- **Cost-Quality Trade-offs:** Optimizing automation levels for different scenarios

### Foundational Work

- **AIOps literature:** Event-driven automation in IT operations
- **Policy learning:** Learning deterministic policies from agentic exploration
- **Curriculum learning:** Progression from exploration to exploitation
- **Runbook automation:** Traditional IT operations procedures

### Possible Extensions & Future Directions

1. **Multi-objective optimization:** Balancing cost, quality, and speed
2. **Temporal modeling:** Time-series analysis of playbook effectiveness
3. **Causal inference:** Understanding which playbook elements drive success
4. **Transfer learning:** Applying crystallized playbooks across domains
5. **Human feedback integration:** Incorporating operator expertise into crystallization

---

## References & Further Reading

1. [AIOps and Automation] - IT operations automation frameworks
2. [Agent Exploration & Exploitation] - Learning theory for agentic systems
3. [Playbook Automation] - Traditional and emerging automation patterns
4. [Cost Optimization in AI] - Reducing LLM inference costs in production
5. [Hybrid Automation] - Combining human and automated decision-making

---

**Keywords:** Progressive Automation, Playbook Crystallization, Cost Optimization, Hybrid Execution, AIOps, Production Automation, Type-Driven Execution

**Suggested Citation:** Malik, A. "Progressive Crystallization: Turning Agent Exploration into Deterministic, Lower-Cost Workflows in Production." arXiv preprint arXiv:2607.07052 (2026).
