# Machine Unlearning: A Comprehensive Survey

**arXiv ID:** 2405.07406  
**Original Submission:** May 13, 2024  
**Latest Version:** April 20, 2026 (v3)  
**Authors:** Weiqi Wang, Zhiyi Tian, Chenhan Zhang, Shui Yu  
**Field:** Machine Learning / Privacy and Security  

## Executive Summary

This comprehensive survey covers machine unlearning—the emerging field dedicated to enabling trained models to "forget" the influence of specified data samples. Driven by global "right to be forgotten" regulations and privacy concerns, machine unlearning has evolved from a theoretical concept to a practical necessity. The survey systematizes knowledge across four dimensions: centralized unlearning (exact and approximate approaches), distributed and irregular data unlearning (federated and graph variants), unlearning verification methods, and critical privacy-security considerations, providing researchers and practitioners with a complete roadmap for implementing privacy-preserving machine learning systems.

## Problem Statement

### The Privacy Challenge in Machine Learning

As machine learning systems become ubiquitous across critical applications—healthcare, finance, autonomous systems—the privacy implications of training data become increasingly serious:

1. **Right to Be Forgotten (RTBF):** Legislated in GDPR (Europe), CCPA (California), and similar regulations worldwide, users have legal rights to request removal of their data and its influence from trained systems

2. **Model Inversion and Membership Inference Attacks:** Trained models can leak information about their training data, enabling attackers to:
   - Recover sensitive training samples
   - Determine if specific individuals were in training data
   - Extract proprietary or private information

3. **Data Breach Scenarios:** When training data is compromised, organizations need mechanisms to quickly remove the influence of exposed data without full model retraining

4. **Changing Consent:** Users may withdraw consent for their data usage after models have been trained

5. **Competitive Intelligence:** Companies may want to remove the influence of specific competitors' data or strategies

### Limitations of Existing Approaches

**Full Retraining:** While retraining from scratch with dataset D\{d} is the most straightforward "unlearning" method, it is computationally prohibitive:
- Cost scales with dataset size and model complexity
- For large models (LLMs with billions of parameters) and massive datasets, retraining can take months and consume enormous computational resources
- Makes privacy-preserving updates impractical in production systems

**Naive Deletion:** Simply removing data records without updating model parameters leaves the data's influence intact, failing to provide meaningful privacy guarantees.

## Core Concepts & Theory

### Formal Definition of Machine Unlearning

Machine unlearning is formally defined as the process of removing the influence of a sample (or subset of samples) from a trained model, such that:

1. **Membership Removal:** The model's parameters change as if the removed sample(s) were never part of the training set
2. **Influence Removal:** All learned associations with the sample are eliminated
3. **Privacy Guarantee:** Provides provable bounds on information leakage about removed samples

### Key Theoretical Concepts

#### 1. Exact Unlearning

**Definition:** The model after unlearning is indistinguishable from a model trained from scratch without the data to be forgotten.

**Mathematical Formulation:**
- Original model: θ = Train(D)
- Unlearned model: θ' = Unlearn(θ, d)
- Exact unlearning requires: θ' ≈ Train(D \ {d})

**Advantages:**
- Provides strongest privacy guarantees
- Theoretically sound

**Disadvantages:**
- Computationally expensive
- Often requires retraining or near-complete recalculation

#### 2. Approximate Unlearning

**Definition:** The model after unlearning is "close enough" to a model trained without the data, providing probabilistic privacy guarantees.

**Differential Privacy Framework:**
- Mechanisms ensure that unlearning satisfies (ε, δ)-differential privacy
- ε controls privacy budget (smaller = stronger privacy)
- δ allows for failure probability

**Advantages:**
- Computationally efficient
- Enables practical privacy-utility tradeoffs
- Amenable to formal analysis

**Disadvantages:**
- Probabilistic rather than absolute guarantees
- May require parameter adjustments affecting model utility

#### 3. Machine Unlearning in Different Settings

**Centralized Unlearning:**
- Single monolithic model
- Full access to model parameters
- Can apply gradient-based or parameter adjustment methods

**Federated Unlearning:**
- Models distributed across multiple clients
- Data never centralized
- Must unlearn without exposing client data

**Graph Unlearning:**
- Specialized for graph neural networks
- Must account for structural dependencies
- Nodes/edges may have complex interdependencies

## Main Ideas & Key Contributions

### 1. Systematic Taxonomy of Unlearning Methods

The survey provides comprehensive categorization:

**Exact Unlearning Approaches:**
- **Retraining-based:** Full or incremental retraining
- **Influence-based:** Computing data influence on predictions
- **Certified approaches:** With formal privacy guarantees

**Approximate Unlearning Approaches:**
- **Gradient-based:** Modifying gradients to remove data influence
- **Parameter update:** Direct parameter adjustments
- **Perturbation-based:** Adding noise or perturbations
- **Sketching methods:** Compact data summaries for efficient updates

### 2. Domain-Specific Unlearning

The survey identifies and covers domain-specific variants:

**Graph Unlearning:**
- Challenges: Interdependent node/edge deletions
- Methods: Adaptive aggregation, node sampling
- Applications: Social networks, recommendation systems

**Federated Unlearning:**
- Challenge: Distributed optimization without centralizing data
- Methods: Client-side unlearning, secure aggregation
- Applications: Healthcare, financial services

**Diffusion Model Unlearning:**
- Challenge: Unlearning in generative models
- Methods: Classifier guidance, noise injection
- Applications: Safe generative AI, copyright protection

**Large Language Model Unlearning:**
- Challenge: Unlearning from massive parameter models
- Methods: Adapter-based, prompt-based approaches
- Applications: Data privacy, reducing harmful outputs

### 3. Unlearning Verification and Validation

A critical component often overlooked: How do we verify unlearning actually worked?

**Verification Methods:**
- **Membership Inference Tests:** Quantify remaining membership signals
- **Model Inversion Attacks:** Attempt to recover original data
- **Influence Estimation:** Compute remaining data influence
- **Statistical Testing:** Formal hypothesis testing for unlearning effectiveness

### 4. Privacy-Security Considerations

The survey highlights often-overlooked privacy risks in unlearning:

**New Attack Vectors:**
- **Unlearning Attacks:** Exploiting unlearning process itself to infer information
- **Timing Attacks:** Using unlearning latency to infer data presence
- **Gradient Leakage:** Unlearning process may leak information through gradients

**Security Recommendations:**
- Combine unlearning with differential privacy
- Use secure multi-party computation for sensitive unlearning
- Implement auditing and logging of unlearning operations

## Methodology & Implementation

### Exact Unlearning: Influence Function Approach

The influence function quantifies how much a training sample affects model parameters:

**Mathematical Foundation:**
```
I(d) = -∇θL(θ, d)^T H^{-1} ∇θL(θ_f)
```

Where:
- H is the Hessian matrix of the loss function
- ∇θL(θ, d) is the gradient of loss for sample d
- θ_f are final model parameters

**Implementation Steps:**
1. Compute Hessian-vector products (computationally expensive)
2. Apply influence estimates to identify sensitive samples
3. Reweight or adjust parameters based on influence
4. Validate through membership inference tests

**Computational Complexity:** O(n) where n is dataset size; prohibitive for large models

### Approximate Unlearning: Gradient-Based Methods

**Algorithm: Gradient Unlearning**

```python
def unlearn_sample(model, sample, learning_rate):
    # Compute negative gradient for the sample to unlearn
    loss = compute_loss(model, sample)
    neg_gradient = -gradient(loss, model.parameters())
    
    # Update model parameters in opposite direction
    for param, grad in zip(model.parameters(), neg_gradient):
        param.data -= learning_rate * grad
    
    return model
```

**Properties:**
- Single-pass update: O(1) complexity per sample
- Probabilistic guarantee: Satisfies approximate unlearning
- Trade-off: May slightly reduce model accuracy

**Advantages:**
- Practical computational complexity
- Scales to large models
- Can be applied to already-deployed models

**Limitations:**
- Requires carefully tuned learning rates
- Privacy guarantee degrades with number of unlearning requests
- May need multiple rounds for strong privacy

### Federated Unlearning: Distributed Approach

**Architecture:**
```
Client 1      Client 2      Client 3
  |              |              |
  ---- Local Unlearning ----
        |           |           |
        --- Secure Aggregation ---
                  |
            Global Update
```

**Process:**
1. **Local Unlearning:** Each client removes data influence locally
2. **Secure Aggregation:** Combine updates without revealing individual client updates
3. **Global Synchronization:** Distribute global model updates

**Privacy Properties:**
- Individual client data never leaves device
- Secure aggregation prevents server from seeing individual updates
- Composition: Privacy degrades with number of unlearning rounds

### Graph Unlearning: Node/Edge Deletion

**Challenge:** When removing a node, must recalculate influences through connected edges

**Method: Adaptive Aggregation**
```
1. Identify node to remove
2. Collect neighbor embeddings (cached from last forward pass)
3. Recompute node's influence on neighbors
4. Update neighbor embeddings to remove influence
5. Propagate updates through graph layers
```

**Computational Efficiency:**
- Only affects local subgraph
- Complexity: O(degree × layers) instead of O(n)

## Practical Applications & Real-World Use Cases

### 1. Healthcare and Medical Records
**Application:** Patient data deletion from AI diagnostic models

**Scenario:** A patient requests deletion of their medical records from a hospital's AI system used for disease diagnosis

**Implementation:**
- Hospital trains deep learning models on patient data
- Patient exercises GDPR right to deletion
- System unlearns that patient's influence from diagnostic model
- Model remains useful for other patients

**Challenge:** Ensuring unlearning doesn't degrade diagnostic accuracy for remaining patients

**Real Impact:** Enables HIPAA and GDPR compliance in medical AI systems

### 2. Financial Services and Credit Scoring
**Application:** Removing individual financial records from credit scoring models

**Scenario:** Consumer requests removal from credit risk assessment models

**Implementation:**
- Banks train risk models on historical credit data
- Consumer invokes CCPA deletion right
- System unlearns consumer's credit history influence
- Model updates credit scores for remaining customers

**Challenge:** Maintaining model fairness while unlearning specific demographic groups

### 3. Recommendation Systems
**Application:** Removing user interaction data from personalized recommenders

**Scenario:** Social media platform must remove user's interaction history

**Implementation:**
- Federated training: Each user device trains local recommendation model
- When user deletes account, local model is erased
- Federated unlearning removes aggregate influence from global model
- Personalization is removed for that user across platform

**Challenge:** Unlearning without harming recommendations for other users

### 4. Autonomous Vehicles and Driving Data
**Application:** Removing vehicle trajectory data from navigation models

**Scenario:** Dashcam/GPS data collected during driving must be unlearned

**Implementation:**
- Vehicles contribute trajectory data to shared navigation models
- Vehicle owner requests data deletion
- System unlearns that vehicle's trajectory influence
- Navigation model maintains utility for other vehicles

**Challenge:** Ensuring routes still optimal after removing historical data

### 5. Large Language Models and Copyright Protection
**Application:** Unlearning copyrighted content or specific author works

**Scenario:** Author requests removal of their copyrighted material from LLM training

**Implementation:**
- Identify training samples containing copyrighted material
- Apply LLM-specific unlearning (e.g., adapter-based)
- Verify through generation tests that model no longer reproduces protected content

**Challenge:** Determining which parameters encode specific training data

### 6. Social Media and Sensitive Content
**Application:** Removing sensitive personal or harmful content from trained models

**Scenario:** Revenge porn or harassment content must be unlearned

**Implementation:**
- Identify problematic content in training data
- Apply targeted unlearning to remove its influence
- Implement safeguards to prevent regeneration

**Challenge:** Scale—social platforms train on millions of hours of content

## Insights & Implications

### 1. Privacy-Utility Tradeoff

The survey emphasizes a fundamental tension:

**The Privacy-Utility Frontier:**
```
Privacy (%)
100 |     .....
    |   ...       ......
 50 | ...             ....
    |...                 .......
  0 |                         100 (Utility %)
```

- **Perfect Unlearning (100% privacy):** Requires retraining; zero utility gains
- **No Unlearning (0% privacy):** Maximum utility but privacy violations
- **Practical Unlearning:** Balances both through approximate methods

### 2. Scalability Challenges

The survey identifies critical scalability issues:

- **Linear in model size:** Influence functions scale poorly with parameter count
- **Linear in data size:** Verification methods require dataset size computation
- **LLM Unlearning:** Billions of parameters make traditional approaches infeasible

**Implication:** New paradigms needed for modern large-scale systems

### 3. The Verification Problem

A central insight: **Unlearning is only as good as verification methods**

Current verification approaches:
- **Membership Inference:** Imperfect and computationally expensive
- **Model Inversion:** May not fully capture influence
- **Empirical Testing:** No formal guarantees

**Research Need:** Stronger verification methods with formal foundations

### 4. Regulatory Compliance Implications

The survey points out:

1. **Technical Gap:** Regulations assume deletion is possible; unlearning is technically subtle
2. **Audit Requirements:** Regulations demand proof of deletion; verification is weak
3. **Liability Questions:** Who's responsible if unlearning fails? Unclear legal framework

### 5. Adversarial Robustness

Unlearning introduces new attack surfaces:

**Attack Scenarios:**
- Adversary manipulates unlearning process to learn about training data
- Timing analysis of unlearning to infer data membership
- Iterative requests to extract information

**Defense:** Combine unlearning with differential privacy for formal guarantees

### 6. Future Research Directions

The survey identifies key open problems:

1. **Efficient Exact Unlearning:** Methods matching approximate unlearning speed
2. **Multi-Party Unlearning:** Handling data from multiple stakeholders
3. **Time-Dependent Unlearning:** Handling data with temporal properties
4. **Unlearning Composition:** Theoretical framework for sequential unlearning
5. **Generative Model Unlearning:** Specialized methods for diffusion models and VAEs

## Code & Resources

### Implementation Frameworks

**SISA (Sharded, Isolated, Sliced, Aggregated):**
```python
# Partition training data into shards
models = [train(data[i:i+shard_size]) for i in range(0, len(data), shard_size)]

# To unlearn sample, retrain only affected shard
affected_shard = find_shard(sample)
models[affected_shard] = train(data[affected_shard] - {sample})

# Aggregate predictions
final_prediction = aggregate([model.predict(x) for model in models])
```

**Gradient-Based Unlearning:**
```python
import torch

def unlearn_gradient_ascent(model, sample, lr=0.01, steps=5):
    """Remove sample influence using gradient ascent"""
    model.train()
    for _ in range(steps):
        # Compute loss for the sample
        loss = compute_loss(model, sample)
        
        # Gradient ascent (maximize loss for sample)
        grad = torch.autograd.grad(loss, model.parameters())
        
        # Update parameters to increase loss (opposite of training)
        with torch.no_grad():
            for param, g in zip(model.parameters(), grad):
                param -= lr * g
    
    return model
```

### Verification Tools

**Membership Inference Attack:**
```python
def membership_inference_test(model, sample, shadow_models):
    """Test if sample was in training data"""
    # Collect losses from models trained with/without sample
    losses_with = [m(sample) for m in shadow_models if sample in m.training_data]
    losses_without = [m(sample) for m in shadow_models if sample not in m.training_data]
    
    # Use statistical test to determine membership
    return statistical_test(losses_with, losses_without)
```

### Key Libraries and Tools

1. **PyTorch:** For gradient-based unlearning implementation
2. **TensorFlow Privacy:** Differential privacy integration
3. **Membership Inference Library:** https://github.com/privacytrustlab/ml_privacy_meter
4. **Unlearning Benchmarks:** SISA framework implementations

### Computational Requirements

- **Baseline Unlearning:** GPU with 8GB+ VRAM
- **LLM Unlearning:** Multi-GPU setup with 80GB+ aggregate memory
- **Verification:** Similar to training dataset once

## Related Work & Context

### Evolution of Machine Unlearning

**Timeline:**
- **2019:** "Machine Unlearning" formally introduced by Bourtoule et al.
- **2021-2022:** Rapid expansion into federated learning and graphs
- **2023-2024:** Focus on large models (LLMs, diffusion models)
- **2025-2026:** Integration with regulatory compliance, practical deployments

### Relationship to Privacy-Preserving ML

**Differential Privacy:**
- **DP:** Adds noise during training to guarantee privacy
- **Unlearning:** Removes data after training
- **Relationship:** Can be combined for stronger guarantees

**Federated Learning:**
- **FL:** Trains models without centralizing data
- **Unlearning:** Removes data influence from trained models
- **Relationship:** Unlearning is critical for FL privacy

### Foundational Concepts

Machine unlearning builds on:
- **Influence Functions:** Measuring data impact on models (Koh & Liang, 2017)
- **Differential Privacy:** Formal privacy framework (Dwork et al., 2006)
- **Secure Multi-Party Computation:** Privacy-preserving computation
- **Cryptographic Protocols:** Enabling distributed unlearning

### Contemporary Related Work

**Recent Advances (2025-2026):**
- **LLM-Specific Unlearning:** Adapter-based and prompt-based methods
- **Certified Unlearning:** Formal guarantees for unlearning
- **Efficient Graph Unlearning:** Linear-time algorithms
- **Multimodal Unlearning:** Unlearning in vision-language models

## References and Further Reading

```bibtex
@article{wang2024unlearning,
  title={Machine Unlearning: A Comprehensive Survey},
  author={Wang, Weiqi and Tian, Zhiyi and Zhang, Chenhan and Yu, Shui},
  journal={arXiv preprint arXiv:2405.07406},
  year={2024}
}
```

**Key Related Papers:**
- Bourtoule et al. (2021): "Machine Unlearning" (ICLR 2021)
- Koh & Liang (2017): "Understanding Black-box Predictions via Influence Functions"
- Dwork et al. (2006): "Differential Privacy: A Survey of Results"

## Conclusion

Machine unlearning has evolved from a theoretical curiosity to a practical necessity in the age of privacy regulation. This survey provides comprehensive coverage of the state-of-the-art across exact and approximate approaches, domain-specific variants, and verification methods. Key insights include the fundamental privacy-utility tradeoff, scalability challenges for large models, and the critical importance of verification. As regulatory pressure increases and models grow larger, unlearning research will be essential for building trustworthy, privacy-preserving machine learning systems. The field remains wide open with opportunities for fundamental algorithmic innovations, particularly in efficient exact unlearning and formal verification methods.
