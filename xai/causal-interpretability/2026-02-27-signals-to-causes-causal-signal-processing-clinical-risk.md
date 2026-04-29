# From Signals to Causes: A Causal Signal Processing Framework for Robust and Interpretable Clinical Risk Prediction

**ArXiv ID:** [2602.23977](https://arxiv.org/abs/2602.23977)  
**Authors:** Surajit Das (Lab Infochemistry Scientific Center, ITMO University), Maxine Tan (School of Engineering, Monash University Malaysia)  
**Submitted:** February 27, 2026  
**Subfield:** Causal Interpretability  

---

## Executive Summary

Clinical AI systems routinely exploit spurious statistical correlations in biomedical signals — correlations that appear predictively strong within a study cohort but evaporate when the model is deployed across different hospitals, devices, or patient populations. This paper argues that the root cause of this fragility is a fundamental misalignment between statistical learning objectives and causal structure: models are trained to predict, not to understand *why* a signal predicts. Das and Tan propose a **causal signal processing (CSP) framework** in which biomedical signals (ECG, EHR time series, MRI) are treated as *effects of latent generative causes* rather than as isolated predictors, enabling models that are simultaneously more robust to distribution shift and more interpretable through genuine causal explanations rather than post-hoc correlation summaries.

---

## Problem Statement

### The Clinical AI Robustness Crisis

A disturbing pattern has emerged in clinical AI: models trained with impressive AUROC scores on academic cohorts often fail catastrophically in deployment. Well-documented examples include:

- **Pneumonia risk models** that learned to associate asthma with *lower* pneumonia mortality — because asthmatic patients receive more aggressive treatment in the training hospital
- **COVID-19 severity models** that learned to use scanner brand and hospital-specific imaging protocols as "risk factors" because specific hospitals treated sicker patients
- **ECG-based age prediction models** that generalize poorly across acquisition equipment

In each case, the model learned **confounded statistical correlations** — patterns that predict well within the training distribution but reflect hospital logistics, equipment differences, or selection biases rather than genuine clinical mechanisms.

### Why XAI Doesn't Fix This

Standard XAI approaches (SHAP, GradCAM for ECG/imaging) reveal *which features the model uses*, but they cannot distinguish:
- Features used because they causally influence the outcome (clinically meaningful)
- Features used because they correlate with the outcome through confounders (spurious)

Explaining a biased model does not de-bias it; it makes the bias legible. A physician told "the model assigned high importance to left bundle branch block pattern" cannot determine from this explanation alone whether that pattern genuinely predicts the outcome in their patient population or is a hospital-specific artifact.

### The Need for Causal Signal Processing

The paper advocates for treating biomedical signals through the lens of causal generative models:

- A patient's ECG is not just a waveform to be correlated with outcomes — it is the *observed effect* of underlying electrophysiological mechanisms (ion channel dynamics, conduction system geometry, autonomic tone)
- A chest X-ray is not just an image — it is the *observable projection* of underlying anatomical and pathophysiological states
- Clinical risk prediction should model the causal pathway from biological causes to observed signals to clinical outcomes, not just the statistical mapping from signal features to outcomes

---

## Core Concepts & Theory

### Causal Graphical Models for Clinical Signals

The paper formalizes clinical signal generation using **Structural Causal Models (SCMs)** (Pearl, 2009):

$$X_i := f_i(\text{Pa}(X_i), U_i)$$

where $X_i$ are observed variables, $\text{Pa}(X_i)$ are causal parents in the directed acyclic graph (DAG), $f_i$ are structural functions, and $U_i$ are exogenous noise variables.

For clinical prediction:
- **Latent causes $Z$:** Underlying pathophysiological states (e.g., myocardial ischemia, electrolyte imbalance)
- **Observed signals $X$:** Biomedical measurements (ECG waveform, lab values, vitals)
- **Outcome $Y$:** Clinical event (mortality, readmission, adverse event)
- **Confounders $C$:** Hospital protocols, device calibration, acquisition settings

The causal DAG:
$$Z \rightarrow X, \quad Z \rightarrow Y, \quad C \rightarrow X$$

The statistical correlation between $X$ and $Y$ includes both:
1. **Causal paths:** $X \leftarrow Z \rightarrow Y$ (valid, generalizable)
2. **Confounded paths:** $X \leftarrow C \rightarrow \text{Treatment} \rightarrow Y$ (spurious, non-generalizable)

### The Causal Signal Processing Framework

**Step 1: Signal decomposition into causal components**

Biomedical signals are decomposed into:
- **Causal component $X^{(c)}$:** Signal variation attributable to latent causal variables $Z$
- **Nuisance component $X^{(n)}$:** Signal variation attributable to confounders $C$ (equipment, patient demographics used as proxies)

For ECG: cardiac rhythm features (PR interval, QRS morphology) are causal components; baseline wander, electrode impedance artifacts, and device gain calibration are nuisance components.

Mathematically, this is framed as a **causal disentanglement** problem:
$$p(X) = \int p(X | Z, C) \, p(Z) \, p(C) \, dZ \, dC$$

The goal is to learn representations $\phi(X)$ such that:
- $I(\phi(X); Z) \approx I(X; Z)$ (preserves causal information)
- $I(\phi(X); C) \approx 0$ (discards confound information)

**Step 2: Neuro-symbolic causal reasoning**

Rather than learning a single end-to-end predictor, the CSP framework uses a **neuro-symbolic architecture**:
- **Neural component:** Extracts uncertain evidence from raw signals, producing posterior distributions over latent causal variables $q(Z | X)$
- **Symbolic causal component:** Takes causal variable posteriors $q(Z | X)$ and applies a causal model to produce the risk prediction, enforcing domain constraints and supporting counterfactual queries

The symbolic component is a **probabilistic causal program** — a structured generative model encoding clinical domain knowledge:

```
# Example: Sepsis Risk Causal Program
if SOFA_score > 2 and MAP < 65:
    bacteremia_risk = high
if WBC > 12 or WBC < 4:
    infection_evidence = high
sepsis_risk = f(bacteremia_risk, infection_evidence, organ_dysfunction)
```

**Step 3: Counterfactual inference**

The causal model supports **counterfactual queries** (Pearl's $do$-calculus):

- *Interventional:* "What would the risk be if we had administered antibiotics 2 hours earlier?" — requires $p(Y | do(X = x'))$
- *Counterfactual:* "Would this patient have survived if admitted to the ICU instead of the ward?" — requires $p(Y_{do(A=1)} | X = x, A = 0)$

These queries are not answerable from observational data alone without a causal model, which is why standard XAI (SHAP, LIME) cannot provide them.

### Identifiability and Distribution Shift Robustness

A key theoretical result in the paper concerns **invariant risk minimization (IRM)** (Arjovsky et al., 2020) and causal models:

**Theorem (Informal):** If a predictor relies only on causally valid features (those in the causal component $X^{(c)}$) and the causal structure is correctly specified, then the predictor achieves **optimal performance across all environments** that share the same causal structure but differ in confounder distributions.

This formalizes the intuition that causal models generalize across hospitals: the causal relationship between ventricular fibrillation and cardiac arrest is invariant across hospitals, while the correlation between QT-prolonging medication prescriptions and cardiac arrest is institution-specific.

---

## Main Ideas & Key Contributions

### Contribution 1: Causal Formalization of Biomedical Signal Generation

The paper provides a rigorous SCM-based formalization of how biomedical signals are generated, which is lacking in the standard signal processing and clinical AI literatures. This formalization clarifies:
- What it means for a feature to be "clinically interpretable" (it must correspond to a causal variable or causal path)
- Why distribution shift occurs (it is a consequence of confounder distribution shift, not signal distribution shift)
- What level of explanations are genuine vs. post-hoc rationalizations

### Contribution 2: Neuro-Symbolic Architecture for Causal Risk Prediction

The hybrid architecture combining neural evidence extraction with symbolic causal reasoning is a novel architectural contribution. Prior work on neuro-symbolic reasoning applied to NLP and visual QA; this paper extends it to clinical time series.

### Contribution 3: Causal Attribution vs. Statistical Attribution

The paper introduces a distinction between:
- **Statistical attribution:** SHAP/GradCAM tells you "feature $j$ contributed $+0.3$ to this prediction"
- **Causal attribution:** CSP tells you "the model believes the signal variation in $X_j$ is caused by latent state $Z_k$ (myocardial ischemia), and this causal state contributes $+0.3$ to mortality risk"

The causal attribution is clinically interpretable in a way that statistical attribution is not: it identifies *why* a feature is predictive, not just *that* it is predictive.

### Contribution 4: Counterfactual Clinical Reasoning

The CSP framework is one of the first clinical AI architectures to support genuine counterfactual reasoning (as opposed to counterfactual SHAP, which is a misleading name for a correlation-based method). This enables:
- Treatment effect estimation from observational data
- Patient-specific "what if" queries for clinical decision support
- Causal attribution of risk factors with statistical rigor

### Intuition: Why Treating Signals as Effects Matters

The key shift in perspective: instead of asking "which features of the ECG predict mortality?", the CSP framework asks "which latent pathophysiological states explain the observed ECG features, and which of those states cause mortality?" This is the difference between:
- "The QRS duration predicts mortality" (statistical)
- "Left ventricular dysfunction explains the widened QRS, and left ventricular dysfunction causes mortality" (causal)

The first statement is fragile across environments (QRS duration may be artificially wide due to bundle branch block from a pacemaker, which doesn't predict mortality the same way); the second is robust.

---

## Methodology & Implementation

### Framework Architecture

```
Raw Signal (ECG/EHR/imaging)
         │
         ▼
  ┌─────────────────┐
  │  Neural Encoder │  ──► q(Z | X): posterior over latent causes
  │  (CNN/Transformer)│
  └─────────────────┘
         │
         ▼
  ┌─────────────────┐
  │ Signal Decomp.  │  ──► X^(c) (causal), X^(n) (nuisance)
  │  (IRM-based)    │
  └─────────────────┘
         │
         ▼
  ┌─────────────────────────────┐
  │ Causal Probabilistic Program │  ──► Risk predictions + counterfactuals
  │ (Domain Knowledge DAG)       │
  └─────────────────────────────┘
```

### Datasets

**MIMIC-IV** (ICU time series):
- 40,000+ ICU admissions
- Vital signs, lab values, medication orders
- Task: 30-day mortality prediction
- Multi-hospital validation across 2 academic medical centers

**PhysioNet Challenge 2021** (ECG classification):
- 88,253 ECGs from 6 countries, 10 acquisition systems
- Task: 12-lead ECG classification (27 rhythm classes)
- Confounders: acquisition device, lead configuration, patient demographics

**UK Biobank** (imaging + genetics):
- 100,000 cardiac MRI scans
- Task: Cardiovascular disease risk prediction
- Confounders: MRI scanner model, site-specific acquisition protocols

### Evaluation Metrics

**Predictive performance:**
- AUROC on in-distribution test set
- AUROC on out-of-distribution test sets (different hospitals/devices)

**Distribution shift robustness:**
- **Worst-case performance gap:** Max performance drop across held-out environments
- **AUROC vs. environment correlation:** Lower correlation = better robustness

**Causal interpretability quality:**
- **Counterfactual validity:** % of generated counterfactuals that satisfy causal constraints
- **Clinical expert agreement:** Proportion of causal attributions agreed upon by cardiologists (blinded evaluation)
- **Confounder independence:** Mutual information between predictions and known confounders

### Results

**ECG Classification (PhysioNet):**

| Method | In-dist AUROC | Out-of-dist AUROC | Worst-case Drop |
|--------|---------------|-------------------|-----------------|
| Standard CNN | 0.923 | 0.847 | −8.2% |
| Invariant Risk Min. | 0.908 | 0.878 | −5.2% |
| CSP Framework (ours) | 0.912 | 0.901 | −2.4% |

**Clinical expert agreement on causal attributions:** 78% vs. 43% for SHAP attributions in a blinded evaluation with 5 cardiologists.

**Counterfactual validity:** 91% of generated counterfactuals satisfy the specified causal constraints, vs. 34% for DiCE (counterfactual SHAP).

### Limitations

- **Causal structure specification:** The framework requires a domain-expert-specified causal DAG. Errors in the DAG propagate directly to causal attributions. Automated causal discovery is partially addressed but remains challenging.
- **Scalability of symbolic reasoning:** Probabilistic causal programs do not scale to highly complex causal structures; this limits applicability to well-understood clinical domains.
- **Latent variable identifiability:** Learning $q(Z|X)$ from observational data requires strong assumptions (functional form, noise distribution) that may not hold in all settings.
- **Evaluation circularity:** Clinical expert agreement is valuable but experts may agree with each other rather than with ground truth.

---

## Practical Applications & Real-World Use Cases

### ICU Sepsis Early Warning

A CSP-based sepsis warning system provides:
- **Robust risk scores** that generalize across ICU types (MICU, SICU, CCU) without re-calibration
- **Causal explanations:** "Elevated lactate (causal: tissue hypoperfusion) → increased sepsis risk" rather than "lactate was an important feature"
- **Counterfactual decision support:** "If vasopressors were administered 2 hours ago, predicted mortality would decrease by 12%"

### ECG Interpretation for Rural/Low-Resource Settings

ECG devices in low-resource settings differ substantially from academic hospital equipment. A CSP-based ECG interpreter:
- Disentangles true cardiac abnormalities from device-specific acquisition artifacts
- Provides robust rhythm classification across device types without device-specific fine-tuning
- Explains predictions in terms of physiological mechanisms (conduction system abnormalities, ischemic patterns) that are meaningful to non-cardiologist clinicians

### FDA SaMD Approval

The FDA requires Software as a Medical Device to demonstrate performance across intended use environments. CSP's multi-environment validation protocol and invariance guarantees provide stronger evidence of generalizability than single-cohort AUROC:
- Pre-specification of causal structure provides auditable reasoning
- Counterfactual queries support clinical validation studies ("does the model correctly identify that intervention X reduces risk in the predicted direction?")

### GDPR and EU AI Act Compliance

The EU AI Act requires high-risk healthcare AI to:
- Provide technical explanations of decision logic
- Demonstrate performance across demographic groups
- Support human oversight through interpretable decision processes

CSP's causal attributions satisfy the "technical explanation" requirement more genuinely than statistical SHAP values: the model's decision logic is literally encoded in the causal DAG, which can be presented to regulators.

---

## Insights & Implications

### Broader Implications for Trustworthy Clinical AI

This paper makes the case that **causal interpretability is not optional for clinical AI — it is necessary for robustness**. The failure modes of statistical AI in clinical settings are precisely the failure modes predicted by causal analysis: confounders, distribution shift, and spurious correlations. The paper establishes a principled path from the current fragile statistical paradigm to a more robust causal paradigm.

### State-of-the-Art Advancement

The CSP framework is one of the first full architectures that integrates:
- Signal processing (decomposition of signals into causal/nuisance components)
- Causal inference (SCMs, invariant risk minimization)
- Neuro-symbolic AI (neural evidence extraction + symbolic causal reasoning)

This integration is novel and positions the work at the intersection of three active communities.

### Open Questions

1. **Automated causal discovery for clinical signals:** Can clinical causal DAGs be learned from data rather than specified by experts? This would lower the barrier to adoption substantially.
2. **Causal disentanglement guarantees:** Under what conditions on the data generating process can causal disentanglement be reliably achieved?
3. **Computational efficiency:** Probabilistic causal programs are slower than standard neural networks; runtime optimization is needed for real-time ICU monitoring.
4. **Cross-modal causal models:** How should causal structure be represented for multimodal clinical data (ECG + imaging + EHR)?

### Future Research Directions

- **Foundation models with causal inductive biases:** Pre-training clinical foundation models with causal constraints built into the objective
- **Causal federated learning:** Sharing causal model structure across hospitals while keeping patient data local
- **Causal biomarker discovery:** Using CSP framework to identify novel biomarkers that are causally (not just statistically) associated with clinical outcomes

---

## Code & Resources

- **ArXiv Paper:** [https://arxiv.org/abs/2602.23977](https://arxiv.org/abs/2602.23977)

### Key Dependencies

```bash
pip install torch torchvision
pip install dowhy          # causal inference with Python
pip install pgmpy          # probabilistic graphical models
pip install lifelines      # survival analysis
pip install wfdb           # PhysioNet ECG data loading
pip install pyhealth       # clinical ML preprocessing
```

### Conceptual Architecture

```python
import torch
import torch.nn as nn
from dowhy import CausalModel

class CausalSignalProcessor(nn.Module):
    def __init__(self, signal_dim, latent_dim, n_confounders, causal_dag):
        super().__init__()
        # Neural encoder: signal -> latent cause posteriors
        self.encoder = nn.Sequential(
            nn.Linear(signal_dim, 256),
            nn.ReLU(),
            nn.Linear(256, latent_dim * 2)  # mean + log_var
        )
        # Confounder disentanglement
        self.confounder_proj = nn.Linear(latent_dim, n_confounders)
        # Causal DAG (specified by domain expert)
        self.causal_model = CausalModel(graph=causal_dag)
    
    def encode(self, x):
        h = self.encoder(x)
        mu, log_var = h.chunk(2, dim=-1)
        z = self.reparameterize(mu, log_var)
        return z, mu, log_var
    
    def reparameterize(self, mu, log_var):
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def causal_disentangle(self, z):
        # Project out confounder directions
        c_hat = self.confounder_proj(z)
        c_dir = self.confounder_proj.weight / self.confounder_proj.weight.norm(dim=1, keepdim=True)
        z_causal = z - (z @ c_dir.T).unsqueeze(-1) * c_dir
        return z_causal, c_hat
    
    def forward(self, x):
        z, mu, log_var = self.encode(x)
        z_causal, c_hat = self.causal_disentangle(z)
        # Pass z_causal to symbolic causal program for risk prediction
        risk = self.symbolic_causal_predict(z_causal)
        return risk, z_causal, c_hat, mu, log_var

# Causal attribution (counterfactual query)
def causal_attribution(model, x, intervention_target, intervention_value):
    """Compute counterfactual risk under do(X_j = intervention_value)."""
    with torch.no_grad():
        # Factual prediction
        risk_factual, _, _, _, _ = model(x)
        # Interventional prediction
        x_intervened = x.clone()
        x_intervened[:, intervention_target] = intervention_value
        risk_counterfactual, _, _, _, _ = model(x_intervened)
    return (risk_counterfactual - risk_factual).item()
```

---

## Related Work & Context

### Building On

- **Structural Causal Models (Pearl, 2009):** The foundational causal inference framework used throughout
- **Invariant Risk Minimization (Arjovsky et al., 2020):** The distributional robustness objective that motivates causal disentanglement
- **Neuro-symbolic AI (Garcez & Lamb, 2023):** The architectural paradigm combining neural and symbolic components
- **Causal Representation Learning (Schölkopf et al., 2021):** The theoretical framework for learning causal latent variables
- **PhysioNet ECG datasets:** Benchmark data enabling multi-environment clinical AI evaluation

### Relation to Papers in This Repository

- **DANCE: Counterfactual Explanations with Causal Constraints (2025-11-25):** Generates counterfactual explanations for predictions; complementary to CSP which generates counterfactuals for causal reasoning. DANCE operates post-hoc; CSP bakes causality into the model architecture.
- **XAI as Causality in Disguise (2026-03-30):** Argues XAI methods implicitly assume causal structure; CSP makes this explicit and rigorous.
- **Causality Key for Interpretability Claims (2026-02-18):** Argues causal structure is necessary to validate interpretability claims; CSP provides a concrete architecture implementing this principle.

### Future Directions

- **Clinical causal discovery:** Automating the specification of causal DAGs from observational clinical data and domain knowledge knowledge bases (e.g., UMLS, clinical guidelines)
- **Causal foundation models:** Pre-training on massive clinical corpora with causal inductive biases
- **Regulatory causal AI frameworks:** Working with FDA, EMA, and other regulators to establish causal interpretability as a standard for clinical AI approval
- **Multi-site causal transfer:** Using causal models to enable certified transfer of clinical AI across healthcare systems with different patient populations and practices

### Connection to Broader xAI Communities

This paper connects:
- **Causal inference community** (Pearl, Rubin potential outcomes): Provides the causal reasoning framework
- **Clinical AI community** (MIMIC, PhysioNet): The application domain driving the robustness requirements
- **Mechanistic interpretability community:** Both seek to understand *why* models predict, not just *what* they predict
- **AI safety community:** Distribution shift robustness and causal reasoning are both central concerns for safe deployment of AI in high-stakes settings
