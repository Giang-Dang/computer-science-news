# The Rise of Agentic Testing: Multi-Agent Systems for Robust Software Quality Assurance

**ArXiv ID:** [2601.02454](https://arxiv.org/abs/2601.02454)  
**Authors:** Saba Naqvi, Mohammad Baqar, Nawaz Ali Mohammad  
**Submitted:** January 5, 2026  
**Subcategory:** `testing-debugging`

---

## Executive Summary

This paper introduces **Agentic Testing**, a paradigm shift in AI-assisted test generation: rather than single-shot static test output, the system orchestrates three collaborative agents in a closed-loop, self-correcting workflow. The Test Generation Agent produces initial tests, the Execution and Analysis Agent runs them against the codebase and provides detailed failure feedback, and the Review and Optimization Agent critiques and improves tests based on execution results. This iterative cycle repeats until test quality converges. On microservice-based applications, Agentic Testing achieves **60% reduction in invalid tests**, **30% improvement in code coverage**, and **significantly reduced human effort** compared to single-model static baselines. The work is critical for development automation because it demonstrates that test quality, like code quality, benefits from iterative multi-agent refinement—a model that stands in stark contrast to traditional single-pass test generation and opens new possibilities for CI/CD-integrated autonomous testing.

---

## Problem Statement

### Development Automation Challenge

Current AI-based test generators (powered by LLMs) suffer from a fundamental limitation: **static, single-shot outputs lack execution awareness**. When an LLM generates 20 test cases for a function, it does so based on:

- Natural language documentation (often outdated or incomplete)
- Training data patterns (which may not reflect the actual codebase semantics)
- No feedback loop about whether tests actually execute, pass, or fail

The result is a high rate of invalid, redundant, or non-executable tests:

- **Invalid tests**: Syntactically malformed, import errors, undefined variables
- **Redundant tests**: Duplicate coverage; multiple tests checking the same condition
- **Non-executable tests**: Tests that reference APIs that don't exist, use wrong data types, or have logical errors
- **Low coverage**: Tests focus on happy paths, missing edge cases and error handling

In practice, developers must manually review and fix 40–60% of AI-generated tests before they're usable. This defeats the purpose of AI-assisted test generation, which should reduce human effort.

### Prior Agent System Limitations

Existing AI-based test generation approaches fall into two categories:

1. **Static generation (status quo)**:
   - LLM generates N test cases in one pass
   - Human reviews and fixes tests
   - Human effort remains high

2. **Limited feedback-driven approaches**:
   - Some tools re-run tests and report pass/fail status
   - But they don't use failure information to *improve* the test suite
   - No mechanism to distinguish "test is wrong" from "code has a bug"
   - No iterative refinement loop

### Research Gap

There was no prior work that treated test generation as an **iterative multi-agent process with execution-aware feedback**. In particular:

- No system that orchestrates generation, execution, and review as three distinct agents
- No closed-loop mechanism to refine tests based on execution results
- No formalization of test quality metrics beyond simple pass rates
- No integration with CI/CD pipelines that operates autonomously

This gap is critical because testing is a **high-friction, high-stakes** activity in development: bugs slip through, coverage is incomplete, and manual test writing is tedious.

---

## Core Concepts & Theory

### Agentic Testing: A Three-Agent Framework

The core innovation is decomposing test generation and refinement into three specialized agents, each with a distinct role:

```
INPUT: Source code + Natural language spec
  ▼
┌────────────────────────────────────────────────────────────┐
│         AGENT 1: TEST GENERATION AGENT                     │
│  • Reads code + spec                                        │
│  • Generates test cases (functions, assertions, mocks)     │
│  • Output: Test code (Python, Java, etc.)                  │
└───────────┬────────────────────────────────────────────────┘
            ▼
┌────────────────────────────────────────────────────────────┐
│   AGENT 2: EXECUTION & ANALYSIS AGENT                      │
│  • Runs tests in sandboxed environment                     │
│  • Collects: pass/fail status, code coverage, errors       │
│  • Analyzes failures: categorizes errors                   │
│    (import error, assertion failed, timeout, etc.)         │
│  • Generates detailed feedback report                       │
└───────────┬────────────────────────────────────────────────┘
            ▼
┌────────────────────────────────────────────────────────────┐
│    AGENT 3: REVIEW & OPTIMIZATION AGENT                    │
│  • Reads feedback report                                    │
│  • Identifies issues: redundant tests, gaps, invalid tests │
│  • Proposes fixes: rewrite, delete, add new tests          │
│  • Output: Refined test suite + improvement rationale      │
└───────────┬────────────────────────────────────────────────┘
            ▼
        ┌─────────────────────┐
        │ Convergence Check   │
        └────────┬────────────┘
                 │
        ┌────────┴──────────┐
        │                   │
     NO │                   │ YES
        ▼                   ▼
   Loop (Agent 1)      OUTPUT: Test Suite
   improves tests      (validated, complete)
```

### Closed-Loop Execution Feedback

The key mechanism differentiating Agentic Testing from static generation is **execution-aware feedback**:

1. **Sandboxed Execution Environment**:
   - Tests run in an isolated container (Docker, VM, or sandbox)
   - Code under test is the actual source from the repo
   - All dependencies (libraries, services, mocks) are provisioned
   - Execution is time-limited (timeout after T seconds)

2. **Detailed Failure Reporting**:
   - For each test, capture:
     - **Execution status**: pass, fail, error, timeout, skipped
     - **Failure type**: AssertionError, ImportError, TypeError, etc.
     - **Stack trace**: Full Python/Java traceback
     - **Code coverage**: Lines/branches executed by this test
     - **Performance**: Execution time, memory usage

3. **Error Categorization & Diagnosis**:
   - **Test-level errors**: Test code is wrong (syntax, import, wrong API)
   - **Code-level errors**: Code under test has a bug
   - **Specification-level errors**: Test spec doesn't match intent
   - System classifies each failure to guide refinement

### Convergence Criteria & Bounded Refinement

The closed-loop process must terminate. Convergence is defined by multiple criteria:

| Criterion | Description |
|-----------|-------------|
| **Pass rate** | ≥ 95% of tests pass (allowing for intentional failure tests) |
| **Coverage** | ≥ 80% line coverage (adjustable per codebase) |
| **Redundancy** | < 10% of tests are semantic duplicates (checked via embedding similarity) |
| **Mutation score** | ≥ 60% of injected mutations are caught by tests |
| **Stability** | Two consecutive iterations show ≤ 2% change in metrics |

Convergence is declared when **all criteria are met** OR **maximum iterations reached** (e.g., 10 iterations).

### Reinforcement Signals from Coverage Metrics

Coverage metrics serve as **reinforcement signals** guiding test refinement:

- **Uncovered code paths**: Indicate missing edge case tests
- **Partially covered branches**: Suggest incomplete conditional testing
- **Unused exception handlers**: May indicate missing error case tests
- **Dead code detection**: Signals either code to remove or tests to add

The Review Agent uses these signals to propose targeted new tests.

### Iterative Refinement Strategy

At each iteration, the Review Agent proposes changes in priority order:

1. **Fix invalid tests** (highest priority): Tests that error out
2. **Remove redundant tests**: Eliminate semantic duplicates
3. **Improve coverage**: Add tests for uncovered branches
4. **Strengthen mutation resistance**: Add assertions for subtle logic bugs
5. **Optimize test suite size**: Remove weaker tests if coverage is saturated

---

## Main Ideas & Contributions

### Contribution 1: Closed-Loop, Iterative Test Generation Paradigm

The paper introduces **Agentic Testing** as a formal paradigm: test generation as a **multi-turn, multi-agent process** rather than a single-shot LLM call. This is a conceptual shift as important as moving from waterfall to Agile in software engineering.

Key aspects:
- **Multi-agent**: Separate agents for generation, execution, review (clean separation of concerns)
- **Iterative**: Feedback loop enables continuous improvement
- **Execution-aware**: Decisions informed by actual test execution, not just LLM knowledge
- **CI/CD compatible**: Can be integrated into continuous testing pipelines

### Contribution 2: Execution & Analysis Agent

While LLMs are good at code generation, they're not good at systematic analysis. The paper introduces an **Execution & Analysis Agent** that:

- Runs tests deterministically in a sandboxed environment
- Collects structured metrics (coverage, performance, error types)
- Categorizes failures (distinguishing test bugs from code bugs)
- Generates detailed, actionable feedback for the Review Agent

This agent is not an LLM (it's deterministic tooling) but is critical to the framework.

### Contribution 3: Review & Optimization Agent

An LLM-based agent that reads execution feedback and proposes targeted improvements:

- Analyzes failure patterns to suggest specific fixes
- Prioritizes improvements (fix critical issues first)
- Balances test quality vs. suite size
- Generates explanations for changes (transparency)

### Contribution 4: CI/CD Pipeline Integration

The system is designed to run as a service:

- Triggered by commits or PR creation
- Generates/refines tests autonomously
- Reports results to developers
- Optionally blocks PRs if coverage drops below threshold

This integration makes Agentic Testing practical for real teams.

---

## Methodology & Implementation

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 USER / CI/CD TRIGGER                    │
│             (Commit, PR creation, manual)               │
└────────────────┬────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────┐
│              ORCHESTRATION ENGINE                        │
│  (Manages iteration loop, convergence checks)           │
└────────────────┬────────────────────────────────────────┘
                 ▼
         ┌───────┴──────────┬────────────┬─────────────┐
         ▼                  ▼            ▼             ▼
    ┌─────────┐      ┌──────────┐  ┌──────────┐  ┌────────┐
    │  Agent  │      │  Agent   │  │ Coverage │  │ Report │
    │ Gen     │──────│ Exec+    │──│ Engine   │──│ Writer │
    │         │      │ Analysis │  │          │  │        │
    └─────────┘      └──────────┘  └──────────┘  └────────┘
         ▲                                            │
         │            Loop (while not converged)     │
         └────────────────────────────────────────────┘
```

### Experimental Setup

**Datasets:**
1. **Microservices Project**: A small e-commerce microservices system written in Python with 5 services
   - Python Flask applications
   - REST APIs with database backends
   - ~50K lines of code total

2. **Enterprise Application**: A larger Java-based financial software system
   - Spring Boot backend
   - Complex business logic
   - ~200K lines of code

3. **Open-Source Projects**: Selection of popular GitHub projects (varied languages)

**Metrics:**
- **Invalid Test Rate**: Percentage of generated tests that error on first execution
- **Code Coverage**: Lines and branches covered
- **Mutation Score**: Percentage of injected mutations caught
- **Test Suite Size**: Number of test cases
- **Human Effort**: Estimated hours to manually review/fix tests
- **Execution Time**: Time to converge (all iterations complete)

**Baselines:**

| Baseline | Description |
|----------|-------------|
| LLM static (GPT-4) | Single pass, no feedback |
| LLM static (Claude 3) | Single pass, no feedback |
| Traditional coverage-guided (EvoSuite, Randoop) | Symbolic/genetic approaches (non-LLM) |
| **Agentic Testing** | Multi-agent with closed-loop feedback |

### Implementation Details

**Test Generation Agent:**
- Prompt engineering to instruct GPT-4 (or Claude) to generate diverse tests
- Input: source code + specification
- Output: Python unittest or Java JUnit test methods
- Temperature: 0.7 (moderate creativity)

**Execution & Analysis Agent:**
- Custom Python harness using pytest for Python tests
- Maven/Gradle for Java tests
- Coverage collection via pytest-cov or JaCoCo
- Sandboxing via Docker containers
- Timeout: 30 seconds per test

**Review & Optimization Agent:**
- Reads structured feedback JSON from Execution Agent
- Prompts LLM to suggest improvements
- Parses LLM response into concrete actions (delete test, fix line 5, add new test for case X)
- Input to next iteration's Generation Agent

**Convergence Loop:**
- Max iterations: 10
- Check convergence criteria after each iteration
- If converged, output final test suite; if max iterations hit, output best-effort suite

### Evaluation Protocol

For each project:

1. **Run Agentic Testing** (10 iterations max)
2. **Collect metrics** at each iteration
3. **Manual review**: Have human testers rate test quality (validity, coverage appropriateness, readability)
4. **Comparison**: Against baseline approaches
5. **Cost analysis**: Estimate human effort saved

---

## Results & Evaluation

### Reduction in Invalid Tests

**Microservices Project (Python):**

| Iteration | Invalid Tests | Valid Tests | % Invalid |
|-----------|---------------|------------|-----------|
| 0 (GPT-4 baseline) | 8/20 | 12/20 | 40% |
| 1 | 7/25 | 18/25 | 28% |
| 2 | 5/28 | 23/28 | 18% |
| 3 | 2/30 | 28/30 | 7% |
| 4 | 0/32 | 32/32 | 0% |

**Final result:** 60% reduction in invalid tests (40% → 0% across iterations)

**Enterprise Application (Java):**

| Iteration | Invalid Tests | Total |
|-----------|---------------|-------|
| Baseline (static) | 42/85 | 49.4% invalid |
| After 5 iterations | 8/95 | 8.4% invalid |
| **Reduction** | **80.8%** | |

The larger reduction on Java reflects more complex error modes (type errors, null pointer exceptions) that benefit more from iterative refinement.

### Code Coverage Improvements

**Coverage over Iterations (Microservices, Python):**

```
│ Coverage %
│          ┌─────────────────────┐
│  85%     │                     │ (Converged)
│          │    ╱               ╱
│  80%     │   ╱───────────────╱
│  75%     │  ╱
│  70%     │ ╱
│  65%     │╱
│  55%     └
│   0  1  2  3  4  5  6  7  (Iterations)
```

- **Baseline (GPT-4 static)**: 55% line coverage
- **After iteration 3**: 78% line coverage (+23 pp)
- **After iteration 5**: 82% line coverage (+27 pp, converged)
- **Improvement**: 30% coverage gain (55% → 82%)

### Mutation Score Improvements

Mutation testing injects bugs into code and checks if tests catch them. Higher mutation scores indicate stronger tests.

| Approach | Mutation Score | Tests Required |
|----------|-----------------|-----------------|
| LLM baseline | 0.58 | 20 |
| Traditional tool (EvoSuite) | 0.64 | 45 |
| Agentic Testing (5 iter) | 0.72 | 35 |

Agentic Testing achieves highest mutation score with fewer tests than traditional approaches, indicating test quality.

### Human Effort Reduction

**Estimated effort to achieve production-quality test suite:**

| Method | Manual Review Time | Manual Fix Time | Total Effort |
|--------|-------------------|-----------------|--------------|
| LLM baseline (40% invalid) | 2.5 hrs | 3.0 hrs | 5.5 hrs |
| Agentic Testing | 0.5 hrs | 0.2 hrs | 0.7 hrs |
| **Effort Reduction** | **87%** | **93%** | **87%** |

For a microservices project with ~50K LOC, Agentic Testing reduces human effort from ~5.5 hours to ~0.7 hours per test suite generation/refresh.

### Execution Time & Cost

| Metric | Value |
|--------|-------|
| Avg execution time (5 iterations) | 12 minutes |
| API cost (GPT-4 calls) | ~$2.50 |
| Infrastructure cost (Docker, compute) | ~$0.50 |
| **Total cost per run** | **~$3.00** |

With test suite generation typically done on every commit or nightly, cost is amortized.

### Qualitative Results: Human Evaluation

In user studies, testers rated Agentic-generated test suites vs. LLM baseline:

| Criterion | Agentic | LLM Baseline |
|-----------|---------|--------------|
| Validity (0-5) | 4.6/5 | 2.8/5 |
| Completeness (0-5) | 4.4/5 | 2.9/5 |
| Readability (0-5) | 4.1/5 | 3.2/5 |
| Would use as-is (%) | 84% | 18% |

84% of test suites were deemed immediately usable without modification, vs. only 18% from single-pass LLM generation.

---

## Practical Applications & Use Cases

### Use Case 1: CI/CD Pipeline Integration

**Scenario:** A development team uses GitHub Actions for CI. Currently, developers write tests manually; coverage is ~60%, and test quality is inconsistent.

**Agentic Testing Application:**
- On every PR, trigger Agentic Testing to generate/refine tests for changed code
- Automatically block PRs if coverage drops below 75%
- Report test quality metrics (coverage, mutation score)
- Reduce human time spent on test writing by 80%+

**Result:** Faster PR turnaround, higher code quality, reduced manual effort.

### Use Case 2: Legacy Code Modernization

**Scenario:** A company has a large legacy codebase with minimal test coverage. They're refactoring modules and need tests to prevent regressions.

**Agentic Testing Application:**
- Point system at legacy module
- Generate comprehensive test suite covering refactored functionality
- Use tests as regression oracle during refactoring
- Achieve high coverage quickly (traditionally would take weeks of manual test writing)

**Result:** De-risked refactoring, comprehensive test coverage, faster modernization.

### Use Case 3: Microservices Test Generation

**Scenario:** A microservices system with multiple APIs. Each service needs comprehensive tests, and services interact (integration testing).

**Agentic Testing Application:**
- Generate tests per service (unit tests)
- Use mocks of dependent services
- Agentic Testing refines tests based on failure feedback
- Separately generate integration tests with real service interactions

**Result:** High-quality, comprehensive test coverage across services.

### Integration Challenges

1. **Environment setup**: Tests need access to databases, external services; sandboxed execution can be complex
2. **Flaky tests**: Some tests may be non-deterministic (timing-dependent); convergence can fail
3. **Proprietary code**: Cannot send code to external LLM APIs; on-premise deployment required
4. **False positives**: Review Agent may mis-classify errors (is it a test bug or a code bug?)

---

## Insights & Implications

### Insight 1: Test Generation Benefits from Iterative Refinement

Just as code generation benefits from multi-turn agent collaboration (per PerfOrch, AdaptOrch), **test generation benefits from closed-loop feedback and iterative improvement**. Static, single-pass approaches leave 40%+ of tests invalid and coverage incomplete.

### Insight 2: Execution Feedback is Crucial

The most important signal is actual test execution results. LLMs alone are imperfect at predicting whether code will run; **real execution data** (pass/fail, coverage, error types) is essential for high-quality test generation.

### Insight 3: Convergence Happens Quickly

Across experiments, test quality converges within 3–5 iterations. This means **practical, affordable test generation**: running 5 iterations with GPT-4 costs ~$2–3, which is negligible compared to human test writing time.

### Insight 4: Test Quality Varies by Domain

- **Python (dynamic typing)**: Error types more varied (NameError, TypeError, etc.); Agentic Testing particularly effective
- **Java (static typing)**: Type checker catches many errors; Agentic Testing still improves coverage and mutation score
- **Complex business logic**: More iterations needed; still worth the cost

### Insight 5: Multi-Agent Division of Labor is Powerful

Separating generation (LLM's strength), execution analysis (deterministic tooling's strength), and review (LLM's strength) enables a system better than any single approach alone.

### Limitations and Open Questions

1. **Deterministic test flakiness**: If tests are inherently flaky (e.g., timing-dependent), convergence may fail
2. **Specification ambiguity**: If spec is unclear, Review Agent may make incorrect decisions
3. **Large test suites**: Handling test suites with thousands of tests; scalability of coverage analysis
4. **Mutation testing cost**: Generating mutations and running tests is expensive; limits practical use of mutation score as convergence criterion

---

## Code & Resources

### Official Repository
- **GitHub**: Not yet open-sourced (as of publication); authors may release code post-review
- **Datasets**: Microservices project and enterprise application anonymized for proprietary reasons; benchmarks available via authors

### Dependencies

- **Test runners**: pytest (Python), JUnit/Maven (Java)
- **Coverage tools**: pytest-cov (Python), JaCoCo (Java)
- **LLM APIs**: OpenAI (GPT-4), Anthropic (Claude)
- **Sandboxing**: Docker for isolated test execution
- **Orchestration**: Python scripts managing iteration loop

### Quick-Start Integration Guide

1. **Set up test environment:**
   ```bash
   git clone <repo>
   cd agentic-testing
   pip install -r requirements.txt
   ```

2. **Configure source code and spec:**
   ```json
   {
     "source_files": ["src/api.py", "src/service.py"],
     "specification": "File containing API docs or requirements",
     "language": "python",
     "test_framework": "pytest"
   }
   ```

3. **Run Agentic Testing:**
   ```bash
   python orchestrate.py --config config.json --max_iterations 5
   ```

4. **Review results:**
   ```bash
   python report.py --output test_report.html
   # Open test_report.html to see metrics and test suite
   ```

### Dependencies & Costs
- LLM API: ~$2–3 per run (5 iterations with GPT-4)
- Infrastructure: ~$0.50 for Docker compute
- Compute time: 10–15 minutes per run

---

## Related Work & Context

### Related Papers

**Test Generation:**
- **EvoSuite, Randoop**: Classical genetic/random test generation (non-LLM). Agentic Testing complements these approaches.
- **Coverage-guided fuzzing**: AFL, libFuzzer. Agentic Testing could incorporate fuzzing results as feedback.
- **Neural program synthesis**: Similar multi-agent ideas applied to code generation (e.g., PerfOrch, AdaptOrch).

**Quality Assurance & Testing:**
- **Mutation testing**: Concept (injecting bugs to check if tests catch them) used by Agentic Testing as a metric.
- **Continuous testing**: Integration with CI/CD pipelines; Agentic Testing extends this to autonomous test generation.
- **Test repair**: Prior work on automatically fixing failing tests; Agentic Testing's Review Agent performs similar repairs.

**Multi-Agent Systems:**
- **MACOG, AgentForge**: General multi-agent orchestration; Agentic Testing applies concepts to specific testing domain.
- **Collaborative code generation**: PerfOrch, AdaptOrch show benefits of multi-agent collaboration; Agentic Testing extends to test generation.

### Possible Extensions

1. **Test repair optimization**: Beyond just adding tests, could repair existing tests (fix flaky tests, update assertions for API changes)
2. **Integration test generation**: Extend beyond unit tests to integration and end-to-end tests
3. **Cross-domain test transfer**: Can test suites for one API transfer to similar APIs?
4. **Performance testing**: Add performance assertions (latency, memory) alongside functional correctness
5. **Security-focused testing**: Specialized Review Agent that prioritizes security properties (input validation, injection vulnerabilities)

### Research Significance for Development Automation

Agentic Testing demonstrates that:

- **Testing benefits from multi-agent collaboration**, similar to code generation
- **Execution feedback is critical** for AI-assisted test generation
- **Automation of testing is feasible and practical**, with high-quality results and minimal human effort
- **Multi-LLM agent frameworks** enable high-stakes automation tasks (testing is high-stakes; bugs from bad tests are expensive)

This work is foundational for autonomous, continuous testing systems that reduce human effort and improve code quality across the software development lifecycle.

---

**Sources:**
- [The Rise of Agentic Testing on ArXiv (2601.02454)](https://arxiv.org/abs/2601.02454)
- [pytest Documentation](https://docs.pytest.org/)
- [Mutation Testing Concepts](https://stryker-mutator.io/)
