# Beyond Test Presence: Assessing the Quality and Robustness of Agent-Generated Tests in Open-Source Projects

**Authors:** Preet Jhanglani, Zeel Kaushal Desai, Vidhi Kansara, Eman Abdullah AlOmar

**ArXiv ID:** 2607.12068

**Submission Date:** July 13, 2026

---

## Executive Summary

As AI-powered coding agents become integrated into continuous integration/continuous deployment (CI/CD) pipelines, their capability to automatically generate tests creates a new quality assurance challenge: test suites that pass execution metrics but lack comprehensive coverage. This research reveals a critical gap between test presence (whether tests exist and pass) and test quality (whether tests actually catch bugs and edge cases). The paper introduces metrics for evaluating agent-generated test robustness, identifying patterns of "stealth technical debt" where agents produce tests that execute successfully but fail to detect real defects, creating long-term maintenance liabilities for open-source projects.

## Problem Statement

### Development Automation Challenge

The integration of AI agents into software development workflows has transformed test automation:
- **Before:** Manual test writing by developers, focus on coverage and edge cases
- **After:** AI-generated tests integrated directly into CI/CD pipelines

However, current evaluation benchmarks (CodeXGLUE, HumanEval, etc.) and CI/CD systems measure only:
- **Pass Rate:** Do tests execute without error?
- **Coverage:** What percentage of code lines are touched?

They do NOT measure:
- **Mutation Score:** Do tests catch injected bugs?
- **Edge Case Handling:** Do tests validate boundary conditions?
- **Semantic Correctness:** Do tests verify actual requirements?

### Research Gap

Existing work on agent-generated tests assumes that automated test generation produces acceptable quality. Studies focus on:
- Whether agents can generate tests at all
- Test code coverage metrics

But critically overlook:
- Actual defect detection capability
- Test robustness under code mutations
- Test reliability across diverse codebases

The result: AI-generated tests that have high pass rates but poor mutation detection, creating a false sense of code quality assurance.

## Core Concepts & Theory

### Test Quality Dimensions

**Traditional Quality Metrics (Commonly Measured):**
- **Test Count:** Number of tests generated
- **Pass Rate:** Percentage of tests that pass
- **Code Coverage:** Lines/branches/functions covered by tests

**Advanced Quality Metrics (Often Neglected):**
- **Mutation Score:** Percentage of injected mutations caught by tests
- **Defect Detection Rate:** Ability to catch real bugs from issue trackers
- **Robustness Score:** Test resilience to minor code changes
- **Edge Case Coverage:** Tests for boundary conditions, error cases

### Mutation Testing Framework

**Concept:** Introduce controlled bugs (mutations) into code and measure if tests catch them.

```
Original Code:
    if (count > 0):
        process()

Mutant 1: if (count >= 0):  # Changed > to >=
Mutant 2: if (count > 1):   # Changed 0 to 1
Mutant 3: if (count > 0):
           # process() removed (deletion mutation)

Test Suite Goal: Catch as many mutants as possible
```

**Mutation Killing Rate:**
- **Excellent:** 85-100% of mutants caught
- **Good:** 70-85%
- **Fair:** 50-70%
- **Poor:** <50%

### Stealth Technical Debt

**Definition:** Test suites that satisfy traditional metrics (high pass rate, good coverage) but fail to detect real defects.

**Manifestation Pattern:**
1. AI agent generates tests that pass current code
2. Code mutates/evolves over time
3. Tests still pass but no longer validate critical properties
4. Real bugs slip through undetected
5. Technical debt accumulates silently until discovered in production

## Main Ideas & Contributions

### Novel Evaluation Framework

The paper introduces a comprehensive test quality evaluation framework encompassing:

1. **Mutation Testing:** Generate diverse mutants of the source code
2. **Defect Detection:** Test ability to catch known bugs from project issue trackers
3. **Robustness Assessment:** Evaluate test stability under refactoring and minor code changes
4. **Coverage-Quality Correlation Analysis:** Examine whether high coverage correlates with high mutation scores

### Key Findings on Agent-Generated Tests

**Comparison: Agent-Generated vs. Human-Written Tests**

| Metric | Agent-Generated | Human-Written | Gap |
|--------|-----------------|---------------|----|
| Pass Rate | 94% | 96% | -2% |
| Line Coverage | 82% | 85% | -3% |
| **Mutation Kill Rate** | **58%** | **79%** | **-21%** |
| Edge Cases Covered | 31% | 64% | -33% |
| Defect Detection Rate | 42% | 71% | -29% |

**Critical Finding:** Agent-generated tests appear high-quality (high pass rates, good coverage) but perform 20-33% worse on mutation scores and defect detection.

### Coverage-Quality Paradox

**Surprising Discovery:** High code coverage does NOT guarantee high mutation detection.

- **Agent tests:** 82% coverage, 58% mutation score
- **Reason:** Tests verify that code executes but don't validate logic correctness

**Example:**

```python
def calculate_discount(price, customer_type):
    if customer_type == "premium":
        discount = 0.20  # 20% discount
    else:
        discount = 0.10  # 10% discount
    return price * (1 - discount)

# Agent-Generated Test (Coverage-Focused)
def test_calculate_discount():
    assert calculate_discount(100, "premium") == 80.0  # Covers line
    assert calculate_discount(100, "normal") == 90.0   # Covers line

# BUT agent test misses:
# - What if price is 0? (boundary)
# - What if customer_type is None? (error case)
# - Mutation: if discount = 0.15 instead of 0.20
#   Test still passes! (Logic not verified, just coverage)

# Human-Derived Test (Quality-Focused)
def test_calculate_discount_edge_cases():
    # Boundary conditions
    assert calculate_discount(0, "premium") == 0.0
    assert calculate_discount(0, "normal") == 0.0
    # Actual logic validation
    assert calculate_discount(100, "premium") == 80.0  # Validates 20%
    assert calculate_discount(50, "premium") == 40.0   # Confirms ratio
    # Error conditions
    with pytest.raises(ValueError):
        calculate_discount(-10, "premium")
    with pytest.raises(TypeError):
        calculate_discount(100, None)
```

### Root Causes of Quality Gaps

1. **Coverage-Driven Generation:** Agent optimization for coverage rather than correctness
2. **Shallow Logic Validation:** Tests often verify execution paths without validating business logic
3. **Limited Context:** Agents may not understand nuanced requirements from documentation
4. **No Multi-Assertion Testing:** Single assertions per test path rather than multi-faceted validation

## Methodology & Implementation

### Dataset

**Scope:**
- 50 open-source Python projects (diverse domains)
- Sample size: 10,000+ agent-generated test cases
- Comparison baseline: Human-written tests from same projects

**Project Categories:**
- Web frameworks (Django, Flask)
- Data processing (Pandas, NumPy)
- Utilities (requests, loguru)
- Scientific computing (SciPy)

### Experimental Protocol

**Phase 1: Test Generation**
- Prompt AI agents (Claude, GPT-4) to generate test suites
- Extract tests from generated code
- Filter for valid, executable test cases

**Phase 2: Quality Evaluation**

1. **Mutation Testing:**
   - Generate mutants using PIT (Python Mutation Testing)
   - Run test suites against mutants
   - Calculate mutation kill rate

2. **Defect Detection:**
   - Extract known bugs from project issue history
   - Apply bug reproducer code snippets
   - Measure test detection rate

3. **Robustness Analysis:**
   - Apply minor refactorings (variable rename, method extract)
   - Re-run tests
   - Track pass/fail transitions

### Key Metrics Computed

**Test Quality Indicators:**

```
Mutation Kill Rate = (Mutants Caught) / (Total Mutants)

Defect Detection Rate = (Known Bugs Caught) / (Total Known Bugs)

Robustness Score = (Tests Passing After Refactor) / (Initial Passing Tests)

Coverage-Quality Ratio = (Mutation Kill Rate) / (Coverage %)
  [Ratio > 1.0 = High quality per unit coverage]
  [Ratio < 0.7 = Low quality despite coverage]
```

### Results

**Aggregate Statistics Across 50 Projects:**

| Test Type | Avg. Pass Rate | Avg. Coverage | Mutation Score | Defect Detection |
|-----------|---|---|---|---|
| Agent-Generated | 94% | 82% | 58% | 42% |
| Human-Written | 96% | 85% | 79% | 71% |

**Worst-Performing Domains (Agents):**
- Complex business logic: 35% mutation score
- Error handling: 40% mutation score
- Boundary conditions: 45% mutation score

**Best-Performing Domains (Agents):**
- Simple CRUD operations: 75% mutation score
- Basic I/O: 72% mutation score

**Statistical Significance:**
- Mutation score gap: Statistically significant (p < 0.01)
- Defect detection gap: Statistically significant (p < 0.001)
- Coverage gap: Small but consistent (3% average)

## Practical Applications & Use Cases

### Real-World Impact Scenarios

1. **CI/CD Pipeline Integration:**
   - **Current State:** Tests pass, metrics look good, code merged
   - **Reality:** Test quality gaps go undetected until production
   - **Implication:** False confidence in code quality

2. **Open-Source Project Maintenance:**
   - **Problem:** Agent-generated tests create ongoing liability
   - **Manifestation:** Future regressions slip through "passing" tests
   - **Cost:** Delayed bug discovery, user-facing issues

3. **Test Automation ROI:**
   - **Expected:** Reduced manual testing burden
   - **Reality:** Tests pass but don't catch real defects
   - **Risk:** Complete replacement of human testing creates gaps

### Concrete Example Workflow

**Scenario: Web API Agent-Generated Tests**

```python
# API Endpoint: GET /users/<id>
def get_user(user_id):
    if user_id <= 0:
        raise ValueError("Invalid ID")
    return db.query(User).filter(id=user_id).first()

# Agent-Generated Test (92% coverage, 45% mutation score)
class TestGetUser:
    def test_get_existing_user(self):
        result = get_user(1)
        assert result is not None  # Only checks execution

# Mutations that PASS despite being wrong:
#   Mutation 1: if user_id < 0:  (← test doesn't catch!)
#   Mutation 2: if user_id == 0:
#   Mutation 3: db.query(User).filter(id=user_id).all()  (← test doesn't catch!)

# Human-Written Test (85% coverage, 79% mutation score)
class TestGetUser:
    def test_get_existing_user(self):
        result = get_user(1)
        assert result.id == 1  # Validates actual data
        assert result.name == "Test User"

    def test_invalid_user_id_zero(self):
        with pytest.raises(ValueError):
            get_user(0)

    def test_invalid_user_id_negative(self):
        with pytest.raises(ValueError):
            get_user(-1)

    def test_nonexistent_user(self):
        result = get_user(999999)
        assert result is None  # Validates absence
```

### Integration Best Practices

1. **Hybrid Approach:** Use agent-generated tests for boilerplate + human review for quality
2. **Mutation Score Gates:** Require minimum mutation scores in CI/CD
3. **Defect Detection Validation:** Regularly test against known bugs
4. **Coverage Quality Ratio:** Monitor tests per percentage coverage

## Insights & Implications

### Impact on Autonomous Testing & Development

1. **Test Automation Limitations:** Current agents can generate syntactically correct tests but not necessarily semantically robust tests

2. **Quality Assurance Challenge:** As agents become more prevalent in development, ensuring test quality becomes critical before relying on agent-generated tests in production

3. **Educational Opportunity:** Understanding test quality gaps can guide better prompt engineering and agent design

### Limitations & Caveats

1. **Language Scope:** Study focuses on Python; results may differ for compiled languages
2. **Project Bias:** Open-source projects may have different testing patterns than enterprise code
3. **Agent Selection:** Evaluated popular LLMs; results depend on model and prompting strategy
4. **Mutation Realism:** Not all mutants represent realistic bugs

### Future Research Directions

1. **Quality-Aware Test Generation:** Design agents that optimize for mutation scores, not just coverage
2. **Defect Prediction Models:** Can we predict which agent-generated tests are low quality?
3. **Human-AI Test Synthesis:** Hybrid approaches where agents draft and humans refine
4. **Domain-Specific Testing:** Custom test generation for specific domains (finance, healthcare)
5. **Test Repair:** Can agents repair low-quality tests based on mutation analysis feedback?

## Code & Resources

### GitHub Repository

- **Project:** Open-Source Test Quality Analysis
- **Dataset:** 10,000+ agent-generated test cases from 50 projects
- **Evaluation Tools:** Mutation score calculators, defect detector

### Dependencies

- Python 3.10+
- **pytest** - Test execution framework
- **mutmut** or **cosmic-ray** - Mutation testing tools
- **coverage.py** - Code coverage measurement
- LLM APIs (OpenAI, Anthropic)

### Quick-Start Guide

```python
# Step 1: Generate tests
agent = CodeAgent(model="gpt-4")
generated_tests = agent.generate_tests(source_code)

# Step 2: Run initial tests
results = pytest.run_tests(generated_tests)
print(f"Pass rate: {results.pass_rate}")
print(f"Coverage: {results.coverage}")

# Step 3: Evaluate quality with mutation
from mutmut_adapter import MutationScorer
scorer = MutationScorer(source_code, generated_tests)
mutation_score = scorer.calculate()
print(f"Mutation score: {mutation_score}")  # Often 40-60% for agents

# Step 4: Check defect detection
defect_detector = DefectDetector(project_history)
defect_rate = defect_detector.measure(generated_tests)
print(f"Defect detection: {defect_rate}")  # Often 30-50% for agents
```

## Related Work & Context

### Prior Work on Test Generation

- **REINFORCE-based Test Generation:** Optimize test selection but often for coverage, not quality
- **Symbolic Execution:** Generates tests but for specific paths, not holistic quality
- **Property-Based Testing (Hypothesis):** Automatically finds edge cases but requires property specification

### Agent-Based Code Generation Context

- **Earlier test generation systems:** Often produced high coverage but low mutation scores
- **Mutation testing research:** Established that coverage ≠ quality, but not widely adopted in agent evaluation
- **Test smell detection:** Identifies low-quality tests but requires running tests

### Complementary Research Areas

1. **Prompt Engineering:** Better prompts for test generation quality
2. **Agent Fine-Tuning:** Training agents on test quality metrics rather than just coverage
3. **LLM Reasoning:** Understanding why agents generate low-quality tests despite good coverage
4. **Formal Methods:** Using formal verification to generate guaranteed-correct test suites

### Future Integration Opportunities

1. **Continuous Quality Monitoring:** Mutation scores as part of CI/CD gates
2. **Agent Feedback Loops:** Training agents on mutation score feedback
3. **Test Repair:** Automatically fixing low-quality tests
4. **Domain Knowledge Integration:** Embedding domain-specific testing practices into agents

---

## Summary

"Beyond Test Presence" reveals a critical gap in how we evaluate AI-generated tests: traditional metrics (pass rate, coverage) mask fundamental quality deficiencies. Agent-generated tests, while syntactically valid and coverage-complete, demonstrate 20-33% lower mutation scores and defect detection rates compared to human-written tests. This "stealth technical debt" creates long-term risks for projects that rely on agent-generated tests without quality assurance mechanisms. The paper establishes mutation testing as an essential evaluation criterion, motivating future research into quality-aware test generation and hybrid human-AI testing approaches.
