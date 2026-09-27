# Synthetic source record

All content below is fictional original-material stand-ins, not a real publication. These are the supplied excerpts; the full proof and other sections are not supplied.

## Identity

- Identifier: SYN-READ-03
- Title: Sparse estimators under structured observations
- Authors: Example Methods Group
- Year/version: 2025, version of record
- No DOI is assigned.

## Publisher abstract

We establish recovery guarantees for sparse estimators under covariate shift and evaluate the method on simulated shifted datasets. The method achieved a median held-out F1 score of 0.87, supporting robust use when training and deployment distributions differ.

## Theorem 2 — page 4

Let the training and evaluation covariates be independently drawn from the same sub-Gaussian distribution with covariance matrix Sigma. If the support size is at most s, the restricted-eigenvalue condition holds, and the stated sample-size bound is met, then the estimator's prediction error is bounded as specified in Equation 6.

This theorem does not cover a changed covariate distribution between training and evaluation. Equation 6 and the proof are outside the supplied excerpts.

## Experiments 3.2 — page 7

We simulated one training distribution and two shifted deployment distributions. The shifted deployment settings change the covariance structure while preserving the response-generation rule. Table 3 reports held-out F1 across five random seeds, with the covariance-shift row summarizing those prespecified shifts. The experiment is a finite simulation result and does not extend Theorem 2 to covariate shift.

## Table 3 — page 7

| Evaluation setting | Median held-out F1 | Range across five seeds |
|---|---:|---:|
| Matched distribution | 91.2% | 90.1% to 92.0% |
| Covariance-shift simulation | 86.6% | 82.4% to 88.1% |

Footnote: F1 is reported as a percentage. The ranges summarize the observed seeds; they are not confidence intervals.

## Appendix A — Generation settings

The covariance-shift simulation uses two prespecified covariance perturbations. It retains the same response-generation rule, sparsity level, sample size, and noise distribution as training. No experiment changes the response mechanism, missing-data process, or support size. No empirical result tests arbitrary covariate shift.

## Discussion — page 9

The shifted simulations suggest that performance may remain useful for the tested shifts. They do not prove a distribution-shift guarantee, and the evaluated shifts do not represent arbitrary deployment changes.
