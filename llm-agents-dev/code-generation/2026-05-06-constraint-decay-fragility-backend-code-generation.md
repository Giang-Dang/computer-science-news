# Constraint Decay: The Fragility of LLM Agents in Backend Code Generation

**ArXiv**: 2605.06445  
**Published**: May 7, 2026  
**Authors**: Francesco Dente (EURECOM), Dario Satriani (University of Basilicata), Paolo Papotti (EURECOM)

## Executive Summary

LLM agents demonstrate impressive capabilities in code generation, yet current evaluation focuses primarily on functional correctness (does the code run?). Production-grade software, however, requires strict adherence to architectural patterns, database choices, framework conventions, and object-relational mappings. This paper reveals **constraint decay**—a substantial and systematic performance degradation as structural requirements accumulate. Through evaluation on 80 greenfield generation tasks and 20 feature-implementation tasks spanning eight popular web frameworks (Flask, Django, FastAPI, Express, Fastify, etc.), the study demonstrates that capable LLM configurations lose approximately **30 percentage points in assertion pass rate** when constraints increase from baseline (functional spec only) to fully specified (framework + architecture + database + ORM). The findings expose a critical gap between research benchmarks and production software requirements, with implications for practical deployment of agentic code generation.

## Problem Statement

### The Research-to-Production Gap

The code generation community has achieved remarkable progress on functional correctness:

**Research Achievement**:
- Models pass 40-60% of functional test cases on HumanEval, MBPP
- Can generate syntactically valid, runnable code
- Handle multi-file generation and integration tests
- Demonstrate competence on simplified task formulations

**Production Reality**:
- Functional correctness is table stakes, not differentiator
- Real systems must satisfy dozens of non-functional constraints simultaneously
- Architectural patterns must be maintained across entire codebase
- Framework-specific conventions must be respected
- ORM usage must be consistent across files
- Database schemas must be respected throughout

### Constraint Types in Real Software

Production backend systems operate under four independent constraint dimensions:

1. **Framework Choice** (e.g., Flask, Django, Express, FastAPI)
   - Each framework has conventions and implicit assumptions
   - Auto-discovery mechanisms vs. explicit configuration
   - Type-hint-driven validation (FastAPI) vs. convention-based (Flask)
   - Routing patterns and handler signatures vary

2. **Architectural Pattern** (e.g., Clean Architecture, Layered Architecture)
   - Enforced separation of concerns
   - Layer-specific responsibilities
   - Dependency rules (only lower layers depend on higher)
   - Cross-layer consistency
   - Naming conventions reflecting structure

3. **Database Backend** (e.g., PostgreSQL)
   - Schema constraints (column types, nullable fields)
   - Relationship definitions
   - Data integrity rules
   - Query efficiency patterns

4. **ORM Integration** (e.g., SQLAlchemy, Sequelize)
   - Model definitions must match database schema
   - Repository pattern for data access
   - Lazy vs. eager loading decisions
   - Query method conformance
   - Relationship mapping accuracy

### The Constraint Decay Phenomenon

The paper's key finding: **constraint decay** is not linear or additive, but multiplicative.

**Example Performance Trajectory**:

| Constraint Level | Flask | Django | FastAPI | Express |
|---|---|---|---|---|
| Level 0 (None) | 68% | 70% | 72% | 71% |
| Level 1 (+Framework) | 55% | 52% | 48% | 59% |
| Level 2 (+Architecture) | 42% | 28% | 21% | 45% |
| Level 3 (All constraints) | 33% | 12% | 6% | 32% |

**Decay Pattern**:
- Capable configurations lose ~30 percentage points overall (~40% relative decline)
- Some configurations approach zero performance with all constraints
- Performance is non-uniform: convention-heavy frameworks penalize more
- Multi-file consistency failures compound constraint violations

### Root Cause: Cross-File Consistency

The fundamental challenge is maintaining consistency across files:

**Example Failure**:

Specification: "Create a user management system with Clean Architecture"

Agent generates:
```
routes/
  user_routes.py    → User.find_by_id()      # ORM model access
  
services/
  user_service.py   → UserRepository.get()   # Repository pattern
  
models/
  user.py           → SQLAlchemy definition
  
database/
  schema.py         → Column definitions
```

**Constraint Violations**:
- `routes/` should not call ORM directly (architecture violation)
- `services/` calls repository, but repository doesn't exist
- `user.py` model doesn't match `schema.py` column definitions
- `user.py` uses nullable field, but schema has NOT NULL
- Naming conventions not followed (service_name.py vs. user_service.py)

### Why Constraints Matter

Architects and senior engineers spend 40-60% of their time on non-functional constraints:

1. **Maintainability**: Code must be understandable years later
2. **Consistency**: New developers must understand patterns
3. **Scalability**: Architecture must support growth
4. **Testability**: Components must be testable in isolation
5. **Deployment**: Framework-specific deployment patterns
6. **Database Efficiency**: ORM usage impacts query performance

Current LLM code generation ignores most of this expertise.

## Core Concepts & Theory

### Four Non-Functional Constraint Dimensions

**1. Framework Selection Constraints**

Different frameworks impose different constraints:

| Dimension | Flask | Django | FastAPI | Express |
|---|---|---|---|---|
| Type Hints | Optional | Optional | Required | Optional |
| Configuration | Explicit | Implicit (auto-discovery) | Explicit (decorators) | Explicit |
| Template Engine | Jinja2 | Django templates | Jinja2 | EJS |
| ORM | SQLAlchemy (external) | Django ORM (built-in) | SQLAlchemy (external) | Sequelize (external) |
| Authentication | Passport/custom | Django auth | FastAPI Security | Passport |

**Type-Hint Implications**:
- FastAPI leverages type hints for validation (breaking consistency → errors)
- Flask/Express don't require type hints (missing hints → no validation)
- Inconsistent typing causes silent failures in FastAPI

**2. Architectural Constraints**

Clean Architecture (Four-Tier Model):

```
┌─────────────────────────────────────┐
│ Presentation Layer (Routes, Views)  │
│ Can depend on: none                 │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Application/Service Layer           │
│ Can depend on: Domain               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Domain/Business Logic Layer         │
│ Can depend on: Infrastructure       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Infrastructure/Database Layer       │
│ Can depend on: nothing              │
└─────────────────────────────────────┘
```

**Constraints Enforced**:
- Presentation CANNOT directly call Infrastructure
- Services must mediate all data access
- Domain entities must be isolated from ORM models
- Dependency direction is unidirectional (must never cycle)

**Naming Convention Impact**:
- Route handlers: `routes/user_routes.py` or `routes/users.py`?
- Service classes: `UserService` vs. `UserManager` vs. `UserHandler`?
- Repository classes: `UserRepository` vs. `UserDao`?
- Model files: `models/user.py` vs. `user_model.py`?

**3. Database Backend Constraints**

PostgreSQL imposes schema constraints:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  title VARCHAR(500) NOT NULL,
  content TEXT
);
```

**Agent Must Ensure**:
- All column names match exactly
- Type mismatches caught (VARCHAR vs TEXT, SERIAL vs INTEGER)
- NOT NULL constraints respected (no nullable fields where schema forbids)
- Foreign keys declared (user_id in posts must reference users.id)
- Default values match schema

**4. ORM Integration Constraints**

Correct ORM model definition:

```python
# Correct: Matches schema
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    user = relationship("User", back_populates="posts")
```

**Common Violations**:
- Column type mismatch (String(100) vs VARCHAR(255))
- Missing nullable constraint (nullable=True vs False)
- Foreign key missing or incorrect
- relationship() definition missing (breaks querying)
- Table name case mismatch (_users vs users)

### Constraint Interactions and Multiplicative Failure

Why doesn't constraint decay simply add?

**Hypothesis 1: Context Window**
- Each file adds 100-500 tokens of context
- Multi-file specification exceeds context limits
- Agent forgets consistency requirements across files

**Hypothesis 2: Conflicting Conventions**
- Framework F1 uses convention C1
- Architecture A1 uses convention C2 (incompatible)
- ORM O1 expects convention C3
- Agent cannot satisfy all simultaneously

**Hypothesis 3: Weak Constraint Reasoning**
- Agents don't reason about constraint satisfaction
- Learning is pattern-based, not rule-based
- Constraints not explicitly modeled in prompts/training
- Agent can't verify its own constraint adherence

**Multiplicative Effect**:

If single constraint violations occur with probability p₁, p₂, p₃, p₄, then:
- No constraints: pass rate ≈ 90% (functional correctness)
- One constraint: pass rate ≈ 90% × (1-p₁) ≈ 70-80%
- Two constraints: pass rate ≈ 90% × (1-p₁) × (1-p₂) ≈ 50-60%
- Three constraints: pass rate ≈ 90% × (1-p₁) × (1-p₂) × (1-p₃) ≈ 30-40%
- Four constraints: pass rate ≈ 90% × (1-p₁) × (1-p₂) × (1-p₃) × (1-p₄) ≈ 5-15%

## Main Ideas & Contributions

### 1. First Systematic Characterization of Constraint Decay

This paper is the first to:
- Isolate constraint dimensions independently
- Measure performance degradation per constraint
- Evaluate across multiple frameworks and architectures
- Characterize multiplicative vs. additive effects
- Provide empirical evidence of the problem

**Key Finding**: Constraint decay is **substantial and systematic**, not an edge case.

### 2. Comprehensive Evaluation Framework

**Two Complementary Task Types**:

**Greenfield Generation** (80 tasks):
- Fresh backend implementation from specification
- Fixes API contract across all tasks
- Controlled constraint specification
- Tests "from scratch" code generation

**Feature Implementation** (20 tasks):
- Integration with existing RealWorld repositories
- Read and understand existing code
- Infer conventions from codebase
- Implement missing functionality (164-2,604 LOC)
- Tests consistency with existing patterns

**Constraint Progression**:
```
Level 0: Functional spec
         ↓
Level 1: +Framework choice
         ↓
Level 2: +Architectural pattern
         ↓
Level 3: +Database schema + ORM
```

### 3. Framework-Specific Analysis

**Top Performers** (Explicit APIs):
- **Express**: 51.4% pass rate (explicit routing, optional conventions)
- **Koa**: 50.7% pass rate (similar to Express)
- **Flask**: 49.3% pass rate (simple, explicit)

**Penalized** (Convention-Heavy):
- **Django**: Heavy implicit configuration and auto-discovery
- **FastAPI**: Type-hint-driven validation
- Consistency violations break immediately

**Insight**: Frameworks with explicit, minimal conventions are easier for agents to handle. Convention-heavy frameworks penalize more because violations are harder to detect and accumulate.

### 4. Architectural Impact Quantification

Clean Architecture enforcement reduces performance by 15-25 percentage points depending on framework. Major failures:

- Routes calling ORM directly instead of through services
- Services calling database layer directly instead of repositories
- Data models mixed between layers
- Naming convention mismatches (route_name.py vs. routeName.py)

**Key Insight**: Architectural patterns are not surface-level formatting; they require deep structural reasoning about data flow and dependencies.

## Methodology & Implementation

### Task Design and Evaluation

**Greenfield Task Example**:

**Specification**:
```
Create a blog API with:
- POST /users: Create user (email, password)
- GET /users/{id}: Get user by ID
- POST /posts: Create post (user_id, title, content)
- GET /posts: List posts with pagination
- DELETE /posts/{id}: Delete post

Constraints:
- Framework: FastAPI
- Architecture: Clean Architecture (4-tier)
- Database: PostgreSQL
- ORM: SQLAlchemy
```

**Output Evaluation**:

1. **Functional Assertions**:
   - Endpoints exist and have correct signatures
   - POST /users creates a user in database
   - GET /users/{id} retrieves the correct user
   - Pagination works correctly

2. **Structural Assertions**:
   - Files are organized in expected layers (routes/, services/, models/, database/)
   - Routes do NOT import from database layer
   - Services import from domain layer
   - ORM models are in models/ layer
   - No circular dependencies

3. **ORM Consistency**:
   - Model columns match database schema
   - Foreign keys defined correctly
   - Relationships are bidirectional and consistent
   - Lazy vs. eager loading aligns with usage patterns

4. **Naming Convention**:
   - File names follow pattern (singular or plural)
   - Class names follow pattern (User vs. UserModel)
   - Function names follow pattern (get_user vs. getUser)

### Architecture Verification Algorithm

```python
def verify_clean_architecture(codebase):
    """Verify Clean Architecture constraints"""
    
    layers = {
        'routes': [],
        'services': [],
        'domain': [],
        'infrastructure': []
    }
    
    # Detect layer membership
    for file in codebase:
        layer = detect_layer(file)
        layers[layer].append(file)
    
    # Check dependency constraints
    violations = []
    for source_file in codebase:
        source_layer = detect_layer(source_file)
        imports = parse_imports(source_file)
        
        for target_module in imports:
            target_layer = detect_layer(target_module)
            
            # Enforce dependency rules
            allowed = get_allowed_dependencies(source_layer)
            if target_layer not in allowed:
                violations.append({
                    'file': source_file,
                    'violates': f"{source_layer} cannot import {target_layer}",
                    'import': target_module
                })
    
    # Check naming conventions
    naming_violations = check_naming_conventions(layers)
    violations.extend(naming_violations)
    
    return len(violations) == 0, violations
```

### Multi-File Consistency Testing

```python
def verify_orm_consistency(codebase, schema):
    """Verify ORM models match database schema"""
    
    inconsistencies = []
    
    # Parse ORM models
    models = parse_orm_models(codebase)
    
    # Parse database schema
    db_tables = parse_schema(schema)
    
    for model_name, model in models.items():
        table_name = model.get_table_name()
        
        if table_name not in db_tables:
            inconsistencies.append(f"ORM model {model_name} has no table {table_name}")
            continue
        
        table = db_tables[table_name]
        
        # Check columns
        for col_name, column in model.columns.items():
            if col_name not in table.columns:
                inconsistencies.append(
                    f"Model {model_name} has undefined column {col_name}"
                )
            else:
                # Check type match
                model_type = column.type
                schema_type = table.columns[col_name].type
                if not compatible_types(model_type, schema_type):
                    inconsistencies.append(
                        f"Column type mismatch: {model_name}.{col_name} "
                        f"({model_type} vs {schema_type})"
                    )
        
        # Check foreign keys
        for fk in model.foreign_keys:
            if not valid_foreign_key(fk, table, db_tables):
                inconsistencies.append(f"Invalid FK in {model_name}: {fk}")
    
    return len(inconsistencies) == 0, inconsistencies
```

### Evaluation Metrics

**Primary Metric: Assertion Pass Rate**
```
pass_rate = (assertions_passed) / (total_assertions) × 100%
```

**Breakdown**:
- Functional assertions: Does it work?
- Architectural assertions: Is it structured correctly?
- ORM consistency: Do models match schema?
- Naming conventions: Are patterns followed?

**Constraint Decay Metric**:
```
decay = (pass_rate_baseline - pass_rate_full) / pass_rate_baseline × 100%
```

Example: Flask goes from 68% → 33%, so decay = 51%

## Practical Applications & Use Cases

### 1. Agent Code Generation System Design

**Understanding Constraint Limitations**:

Instead of: "Use agent to generate entire backend from spec"

Better: "Use agent for code generation in constrained scenarios"

**Practical Approach**:

1. **Specification-Driven Architecture**:
   - Human architect defines architecture (layers, patterns, naming conventions)
   - Store as formal specification (AST, constraints)
   - Agent generates code within constrained space
   - Violations detected and corrected automatically

2. **Incremental Generation with Feedback**:
   - Generate one file at a time
   - Test for constraint violations
   - Show violations to agent with corrections
   - Agent learns constraints through iteration

3. **Hybrid Human-Agent Workflow**:
   - Humans design architecture and define constraints
   - Agent generates implementation
   - Humans review and validate
   - Agent refines based on feedback

### 2. Constraint Specification and Enforcement

**Formal Constraint Language**:

```yaml
constraints:
  architecture:
    pattern: clean_architecture
    layers:
      - name: routes
        can_import: [services, shared]
        naming: "*_routes.py"
      - name: services
        can_import: [domain, infrastructure, shared]
        naming: "*_service.py"
      - name: domain
        can_import: [shared]
        naming: "*.py"
      - name: infrastructure
        can_import: []
        naming: "*_repository.py"
  
  framework:
    type: fastapi
    requirements:
      - all_routes_have_type_hints
      - dependency_injection_used
  
  database:
    type: postgresql
    schema: "./schema.sql"
    orm: sqlalchemy
    requirements:
      - model_columns_match_schema
      - foreign_keys_defined
```

**Automated Validation**:

```python
validator = ConstraintValidator(constraints_yaml)
violations = validator.validate(generated_codebase)

for violation in violations:
    print(f"CONSTRAINT VIOLATION: {violation.constraint}")
    print(f"FILE: {violation.file}")
    print(f"REMEDIATION: {violation.suggestion}")
```

### 3. Curriculum Learning for Code Generation

**Staged Constraint Introduction**:

**Phase 1**: Learn basic generation (no constraints)
**Phase 2**: Add framework constraints
**Phase 3**: Add architectural patterns
**Phase 4**: Add database schema consistency
**Phase 5**: Add ORM consistency

Training improves at each stage rather than overwhelming agent with all constraints simultaneously.

### 4. Production Deployment Strategies

**Strategy 1: Agent-Assisted Code Review**
- Agent generates code
- Human architect reviews against constraints
- Violations are clear and actionable

**Strategy 2: Constraint Scaffolding**
- Generate code templates matching architecture
- Agent fills in implementation details within template
- Violations impossible (structure enforced)

**Strategy 3: Interactive Agent**
- Agent generates incrementally
- System provides constraint feedback
- Agent adjusts generation based on feedback

## Insights & Implications

### 1. Constraint Decay is Fundamental, Not Edge Case

The finding that capable agents lose 30+ percentage points under full constraints shows:

**This is not**:
- A problem with specific models (affects all tested configs)
- A prompt engineering issue (affects all tested prompts)
- A dataset issue (affects both greenfield and feature tasks)

**This is**:
- A fundamental limitation of current agent architecture
- A systematic property of multi-file code generation
- A critical gap between research and production

**Implication**: Agents cannot be deployed for production code generation without constraint-awareness architecture changes.

### 2. Framework Choice Materially Impacts Feasibility

**Range of difficulty**:
- Easy (Flask, Express): 50%+ pass rate even with constraints
- Hard (Django, FastAPI): <10% pass rate with constraints

**Root cause**: Convention density
- Explicit frameworks have small constraint surface
- Convention-heavy frameworks have large constraint surface

**Implication**: Framework selection should consider agent-friendly conventions. Industries standardizing on convention-heavy frameworks should expect lower agent effectiveness.

### 3. Multi-File Consistency is the Fundamental Challenge

Most failures are not "agent can't generate valid code" but "agent can't generate consistent code across files."

**Examples**:
- Model definition in File A doesn't match schema in File B
- Service in File A calls repository method undefined in File B
- Route in File A imports from infrastructure in File B (violates architecture)

**Implication**: Constraint-guided generation must focus on multi-file consistency mechanisms, not just single-file quality.

### 4. Context Window is Likely a Binding Constraint

Multi-file specifications exceed typical context windows:
- Specification: 500-1000 tokens
- Architecture constraints: 200-300 tokens
- Database schema: 300-500 tokens
- Framework conventions: 200-300 tokens
- Previous code (context): 2000-4000 tokens

Total: 3200-6100 tokens before generation even starts.

**Implication**: Addressing constraint decay likely requires new architectures for maintaining consistency across extended contexts (e.g., memory augmentation, retrieval-augmented generation).

### 5. Architecture is Not Just a Best Practice

Current research treats architecture as a "nice to have." The data shows:

**Without architecture constraint**: 68% pass rate (Flask)
**With architecture constraint**: 33% pass rate

This is not a 5% penalty; it's a 50% penalty. Architecture fundamentally affects the problem difficulty.

**Implication**: Production code generation systems must treat architecture as a first-class concern, not an afterthought.

## Code & Resources

### Benchmark Implementation

**Public Benchmark Code**:
- Repository: [Constraint Decay Benchmark](https://github.com/dente/constraint-decay)
- Tasks: 80 greenfield + 20 feature implementation
- Evaluation: Full architectural and ORM consistency checking

### Task Specification Format

```json
{
  "task_id": "blog_api_001",
  "task_type": "greenfield",
  "specification": {
    "description": "Create a blog API...",
    "endpoints": [
      {
        "method": "POST",
        "path": "/users",
        "params": ["email", "password"],
        "response": "user_id"
      }
    ]
  },
  "constraints": {
    "framework": "fastapi",
    "architecture": "clean_architecture",
    "database": {
      "type": "postgresql",
      "schema_file": "schema.sql"
    },
    "orm": "sqlalchemy"
  },
  "evaluation": {
    "functional": [
      "POST /users creates user in database",
      "GET /users/{id} returns correct user"
    ],
    "structural": [
      "Routes in routes/ layer",
      "Routes only import services",
      "Services import domain"
    ],
    "consistency": [
      "ORM models match schema",
      "Foreign keys defined",
      "No circular dependencies"
    ]
  }
}
```

### Evaluation Script

```python
from constraint_decay_benchmark import BenchmarkTask, Evaluator

# Load task
task = BenchmarkTask.from_json("blog_api_001.json")

# Generate code (with agent)
generated_code = agent.generate(
    task.specification,
    constraints=task.constraints
)

# Evaluate
evaluator = Evaluator(task)
results = evaluator.evaluate(generated_code)

print(f"Functional pass rate: {results.functional_pass_rate:.1%}")
print(f"Structural pass rate: {results.structural_pass_rate:.1%}")
print(f"Consistency pass rate: {results.consistency_pass_rate:.1%}")
print(f"Overall: {results.overall_pass_rate:.1%}")

# Show violations
for violation in results.violations:
    print(f"\nVIOLATION: {violation.type}")
    print(f"File: {violation.file}")
    print(f"Description: {violation.description}")
```

### Frameworks Evaluated

**Python**:
- Flask
- FastAPI
- Django
- aiohttp

**JavaScript/Node.js**:
- Express
- Fastify
- Hono
- Koa

**Extending the Benchmark**:

```python
# Add new framework
class NewFrameworkEvaluator(FrameworkEvaluator):
    def __init__(self):
        self.framework_name = "new_framework"
        self.convention_rules = {
            "routing_file": r"routes/.*\.py$",
            "handler_name_pattern": r".*_handler$"
        }
    
    def check_framework_constraints(self, codebase):
        """Check framework-specific constraints"""
        violations = []
        # ... implementation
        return violations
```

## Related Work & Context

### Code Generation Benchmarks

Prior work focuses on functional correctness:

- **HumanEval**: Single-file functions, no constraints
- **MBPP**: Multi-file, but minimal architectural requirements
- **SWE-bench**: Real GitHub issues, but evaluates on final correctness not process

**Constraint Decay** fills the gap by evaluating non-functional properties explicitly.

### LLM Agent Capabilities

Current research shows agents excel at:
- Single-file generation (HumanEval: 40-60%)
- Functional correctness (MBPP: 50-70%)
- Simple, unstructured tasks

Current research shows agents struggle with:
- Multi-file consistency (new finding: 30% overall vs. 70% single-file)
- Architectural patterns (new finding: -25pp penalty)
- Framework conventions (new finding: -20pp penalty)
- ORM consistency (new finding: -15pp penalty)

### Production Requirements vs. Benchmarks

**Current Benchmarks**:
- Focused on functional correctness
- Limited multi-file scenarios
- Minimal architectural requirements
- No cross-file consistency checks

**Production Reality**:
- Functional correctness is minimum requirement
- Extensive multi-file systems (20-50 files typical)
- Strict architectural enforcement
- Multiple constraint dimensions simultaneously

**Implication**: Benchmarks must evolve to include realistic production constraints.

### Future Research Directions

**Immediate Needs**:
1. **Constraint-Aware Generation**: Architectures that reason about constraint satisfaction
2. **Memory Augmentation**: Handle large specifications without context loss
3. **Iterative Refinement**: Agent learns constraints through feedback loops
4. **Formal Verification**: Check constraint satisfaction mathematically

**Long-Term**:
1. **Neuro-Symbolic Approaches**: Combine neural generation with symbolic constraint checking
2. **Program Synthesis**: Constraint-based program synthesis (Rosette, etc.)
3. **Executable Specifications**: Run constraints as automated tests during generation

## Summary

Constraint Decay reveals a fundamental limitation in current LLM agent code generation: **agents cannot reliably generate code satisfying multiple non-functional constraints simultaneously**. The systematic 30+ percentage point performance loss from baseline to fully-constrained scenarios demonstrates that:

1. **Non-functional constraints are critical** for production software
2. **Multi-file consistency** is the binding constraint, not single-file quality
3. **Framework choice matters** (convention-heavy frameworks penalize more)
4. **Constraint decay is multiplicative**, not additive
5. **Current agents are insufficient** for production deployment without architectural changes

For the research community, the implications are:

- **Benchmark evolution**: Evaluation must include realistic non-functional constraints
- **Architectural innovation**: Agents need new approaches to constraint satisfaction
- **Deployment strategy**: Production use requires constraint-aware systems
- **Training approaches**: Curriculum learning and constraint specification formalism needed

These findings establish constraint handling as a critical challenge in autonomous code generation and a key area for future research in agentic software engineering.
