# A Comparative Study of Machine Learning and Deep Learning for Out-of-Distribution Detection

**ArXiv ID:** 2605.10181  
**Submitted:** May 20, 2026  
**Categories:** Machine Learning  
**Application Domain:** Medical Imaging (Fundus Images)

## Executive Summary

This paper challenges the conventional assumption that deep learning uniformly outperforms traditional machine learning by demonstrating that for out-of-distribution (OOD) detection in medical imaging, traditional ML approaches achieve equivalent detection performance to deep learning while requiring substantially lower computational resources. Evaluated on over 60,000 fundus and non-fundus images, both approaches achieved perfect AUROC (1.000) and near-perfect accuracy (0.999-1.000), but the ML approach exhibited significantly lower end-to-end latency, suggesting profound implications for practical deployment in resource-constrained medical settings.

## Problem Statement

Out-of-distribution detection is critical for building reliable AI systems, as models that confidently produce outputs for invalid or unexpected inputs cannot be trusted in safety-critical applications like medical diagnosis. Traditional deep learning is often assumed to be superior to machine learning for complex vision tasks, but this assumption may not hold when:

1. **Domain-Specific Constraints:** Medical imaging data are acquired under standardized protocols
2. **Limited Visual Complexity:** Fundus images have relatively constrained variations within distribution
3. **Computational Constraints:** Medical deployment environments often have limited computational resources

**Research Gap:** There is insufficient empirical evidence comparing ML and DL approaches specifically for OOD detection in medical imaging, where standardized acquisition protocols may reduce the complexity advantage that DL typically provides.

## Core Concepts & Theory

### Out-of-Distribution Detection
OOD detection aims to identify inputs that differ significantly from the training distribution. Unlike standard classification, OOD detection must:
- Distinguish in-distribution (ID) samples from OOD samples
- Assign low confidence to OOD samples
- Avoid false positives (classifying OOD as ID)
- Minimize false negatives (classifying ID as OOD)

### Medical Imaging Context: Fundus Images
Fundus images are photographs of the retina taken through the eye's lens, standardly used for diabetic retinopathy screening and other ophthalmologic conditions. Advantages for OOD detection:
- Standardized acquisition protocols
- Constrained field-of-view
- Consistent lighting and resolution
- Limited natural variation between healthy retinas

### Deep Learning for OOD Detection
Traditional DL approaches use:
- **Confidence-based methods:** Using model uncertainty/softmax scores
- **Reconstruction-based:** Detecting anomalies via reconstruction error
- **Embedding-based:** Distance in latent space from known classes
- **Ensemble methods:** Disagreement among multiple models

### Traditional Machine Learning Approaches
Classical ML methods leverage:
- **Feature extraction:** Carefully engineered or automatically extracted features
- **Statistical classifiers:** Support Vector Machines (SVM), Random Forests, Isolation Forests
- **Anomaly detection:** One-class SVM, Local Outlier Factor (LOF)
- **Ensemble methods:** Gradient boosting, bagging

### Why ML Might Succeed in Constrained Domains
1. **Reduced Complexity:** Standardized acquisition reduces need for learning invariances
2. **Limited Variation:** Constrained visual space reduces generalization requirements
3. **Computational Efficiency:** Classical ML has lower overhead
4. **Interpretability:** Feature-based ML provides more transparent decision-making
5. **Data Efficiency:** ML may require fewer samples to reach performance plateaus

## Main Ideas & Contributions

### 1. Systematic Comparison Framework
The paper establishes a rigorous comparison between:
- **Traditional ML:** Algorithms like SVM, Random Forests, Isolation Forests
- **Deep Learning:** Convolutional neural networks and feature-based DL classifiers
- **Fair Evaluation:** Identical datasets, metrics, and validation protocols

### 2. Perfect Performance on Fundus OOD Detection
**Key Finding:** Both ML and DL achieve near-perfect performance:
- AUROC: 1.000 for both approaches
- Accuracy: 0.999-1.000 on internal validation
- External validation: Consistent performance across test sets
- Sensitivity/Specificity: Both near 100%

This suggests the OOD detection task on fundus images has relatively low inherent complexity.

### 3. Substantial Latency Difference
**Critical Discovery:** ML approach exhibits significantly lower end-to-end latency:
- **ML latency:** Substantially reduced compared to DL
- **DL latency:** Includes feature extraction, inference, postprocessing overhead
- **Practical Implication:** ML enables real-time deployment in time-sensitive clinical settings

### 4. Computational Efficiency Advantage
The ML approach demonstrates:
- Lower memory requirements
- Reduced model size
- No GPU requirement
- Faster inference on standard hardware
- Suitable for edge deployment and resource-constrained environments

### 5. Domain-Specific Success Factor
The paper identifies why ML succeeds where it might fail elsewhere:
- **Standardization:** Medical acquisition protocols reduce variation
- **Consistency:** Controlled imaging conditions limit edge cases
- **Specificity:** Task-specific feature engineering proves effective
- **Stability:** Limited distribution shift within domain

## Methodology & Implementation

### Dataset Description
- **Total Size:** Over 60,000 fundus and non-fundus images
- **In-Distribution (ID):** Fundus images (retinal photographs) from standard protocols
- **Out-of-Distribution (OOD):** Non-fundus images (other eye photos, unrelated medical images, natural images)
- **Data Splits:** Internal validation set and external test set
- **Resolution:** Multiple resolutions tested

### Experimental Setup

#### Machine Learning Approach
1. **Feature Extraction:**
   - Manual feature engineering (morphological features, statistical descriptors)
   - Texture analysis (LBP, SIFT, SURF)
   - Color histogram features
   - Handcrafted medical imaging features

2. **Classifier Training:**
   - Support Vector Machine (SVM) with RBF kernel
   - Random Forest
   - Isolation Forest for anomaly detection
   - Ensemble combination

3. **OOD Decision:**
   - Anomaly score threshold
   - Distance from known class distribution
   - Ensemble voting

#### Deep Learning Approach
1. **Architecture:**
   - Pre-trained CNNs (ResNet, VGG, etc.)
   - Fine-tuning on ID data
   - Extraction of penultimate layer features
   - Uncertainty estimation

2. **Training:**
   - Cross-entropy loss on classification
   - Confidence calibration
   - Dropout/temperature scaling for uncertainty

3. **OOD Detection:**
   - Maximum softmax confidence
   - Feature distance in latent space
   - Model uncertainty estimation

### Evaluation Metrics
- **AUROC:** Area under receiver operating characteristic curve
- **Accuracy:** Overall correct classification rate
- **Sensitivity/Recall:** True positive rate (detecting OOD)
- **Specificity:** True negative rate (accepting ID)
- **Precision:** Positive predictive value
- **F1-Score:** Harmonic mean of precision and recall
- **End-to-End Latency:** Total inference time including preprocessing
- **Memory Usage:** Model and runtime memory requirements

### Key Results

| Metric | ML Approach | DL Approach |
|--------|------------|------------|
| Internal AUROC | 1.000 | 1.000 |
| External AUROC | 0.999-1.000 | 0.999-1.000 |
| Accuracy | 0.999-1.000 | 0.999-1.000 |
| End-to-End Latency | [Substantial Reduction] | [Baseline] |
| Memory Usage | [Low] | [High] |
| Training Time | [Fast] | [Slow] |

[Exact figures unavailable — see full paper]

## Practical Applications & Use Cases

### 1. Clinical Deployment
- **Retinopathy Screening:** Automated detection of invalid/non-fundus images in screening programs
- **Quality Control:** Real-time validation of image acquisition
- **Point-of-Care Deployment:** Resource-constrained clinic settings with limited computing
- **Mobile Health:** Integration into mobile screening platforms

### 2. Hospital Information Systems
- **HIS Integration:** Fast processing compatible with existing workflows
- **Real-Time Validation:** Detect invalid images during acquisition
- **Batch Processing:** Efficient processing of large image archives
- **Low-Cost Infrastructure:** Minimal hardware requirements

### 3. Medical Imaging QA
- **Automated QA:** Detect corrupted, mis-acquired, or out-of-domain images
- **Pipeline Monitoring:** Continuous quality assurance in imaging pipelines
- **Data Curation:** Efficient filtering of large image databases
- **Cost Reduction:** Eliminates expensive manual review for many cases

### 4. Telehealth and Remote Screening
- **Bandwidth Efficiency:** ML models require less processing power
- **Latency Reduction:** Critical for real-time telemedicine
- **Edge Processing:** Deploy on local devices without cloud connectivity
- **Robustness:** Simpler models less affected by compression artifacts

### 5. Feasibility and Implementation Challenges

**Advantages of ML Deployment:**
- Simple integration with legacy systems
- Minimal training requirements
- Interpretable decision-making
- Easy model updates

**Challenges:**
- Feature engineering is task-specific
- Transfer to other imaging modalities requires retraining
- May not generalize to different acquisition protocols
- Limited by handcrafted features

## Insights & Implications

### Broader Field Impact

1. **Challenging Deep Learning Dominance:**
   The paper provides empirical evidence that deep learning's superiority is not universal. In domains with:
   - Standardized data acquisition
   - Limited visual complexity
   - Constrained variation
   - Strong need for computational efficiency
   Traditional ML remains competitive or superior.

2. **Rediscovering Classical Methods:**
   With resource constraints and deployment challenges becoming critical, classical ML deserves renewed attention in practical applications, particularly in medical imaging.

3. **Task-Specific Optimization:**
   The paper emphasizes the importance of choosing architectures matched to task complexity rather than always defaulting to state-of-the-art DL approaches.

### State-of-the-Art Advancement

1. **Efficiency Paradigm:**
   Shifts focus from model capacity to computational efficiency and practical deployment constraints.

2. **Medical AI Best Practices:**
   Suggests OOD detection in standardized medical imaging should consider ML approaches, particularly when:
   - Real-time performance is required
   - Computational resources are limited
   - Interpretability is important

3. **Comparative Analysis Framework:**
   Establishes methodology for fair comparison between ML and DL in medical applications.

### Limitations and Open Questions

1. **Domain Specificity:**
   - Results specific to fundus imaging; unclear if generalizable to other modalities
   - Different imaging protocols (ultra-wide-field, etc.) may require retraining
   - Cross-domain transfer untested

2. **Task Complexity:**
   - OOD detection is simpler than classification; results may not transfer to more complex tasks
   - Multi-class classification with OOD may show different patterns

3. **Data Availability:**
   - Assumes standardized acquisition protocols (not always true in practice)
   - Results may not hold for naturally variable data

4. **Generalization:**
   - ML features are hand-engineered; unclear if results generalize to other medical domains
   - DL may still excel when task complexity increases

### Future Research Directions

1. **Extension to Other Modalities:** Apply framework to other standardized imaging (chest X-ray, CT, MRI)
2. **Multi-Domain Analysis:** Investigate where ML/DL trade-off points occur
3. **Hybrid Approaches:** Combine ML and DL strengths
4. **Interpretability Analysis:** Compare explainability of ML vs. DL predictions
5. **Resource-Aware Design:** Formalize framework for efficiency-accuracy trade-offs

## Code & Resources

### Availability
- Paper: https://arxiv.org/abs/2605.10181
- HTML Version: https://arxiv.org/html/2605.10181
- PDF: https://arxiv.org/pdf/2605.10181

### Dependencies
- **ML Stack:**
  - scikit-learn (SVM, Random Forest, Isolation Forest)
  - scipy, numpy (numerical computation)
  - OpenCV (feature extraction)

- **DL Stack:**
  - PyTorch or TensorFlow
  - Pre-trained model zoo
  - CUDA (optional, for GPU acceleration)

### Compute Requirements
- **ML:** CPU only, minimal GPU memory
- **DL:** GPU acceleration beneficial but not required

### Quick-Start Guide
1. Prepare fundus and non-fundus image datasets
2. Implement both ML and DL feature extractors
3. Train classifiers on ID data
4. Evaluate OOD detection on test sets
5. Compare latency and accuracy metrics
6. Analyze performance-efficiency trade-offs

## Related Work & Context

### Related Papers
- [A Benchmark of Medical Out of Distribution Detection](https://arxiv.org/abs/2007.04250) - Medical OOD detection benchmarks
- Medical imaging OOD detection methods
- Classical ML for medical imaging analysis
- Recent deep learning medical imaging papers

### Prior Work Foundations
- Fundamental OOD detection methods
- Medical imaging AI benchmarks
- Traditional machine learning for healthcare
- Clinical deployment requirements

### Future Research Directions
1. **Hybrid ML-DL Systems:** Combine strengths of both approaches
2. **Domain Adaptation:** Adapt to different imaging protocols
3. **Few-Shot OOD:** Learning with limited OOD examples
4. **Interpretable OOD Detection:** Explaining why images are OOD
5. **Federated OOD Detection:** Privacy-preserving deployment

## Summary

This paper provides important evidence that traditional machine learning can match or exceed deep learning performance for out-of-distribution detection in standardized medical imaging domains, particularly when computational efficiency is a priority. By evaluating on over 60,000 fundus and non-fundus images, the authors demonstrate that both approaches achieve near-perfect detection (AUROC 1.000), but the ML approach offers substantially lower latency and computational requirements. The findings challenge the assumption that deep learning universally dominates and suggest that task-specific characteristics—particularly standardized data acquisition and limited visual complexity—should guide architecture selection. For clinical deployment, point-of-care screening, and resource-constrained settings, traditional ML approaches merit serious consideration alongside state-of-the-art deep learning methods.
