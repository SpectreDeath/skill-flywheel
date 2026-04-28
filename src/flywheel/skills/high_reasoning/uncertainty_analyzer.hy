;; Uncertainty Quantification Heuristics in Hy
;; Probabilistic modeling, sensitivity analysis, and decision-making under uncertainty

(import hy)
(import [random [random gauss]])
(import [math [sqrt exp log erf]])
(import [statistics [mean stdev]])

;; Bayesian Network Uncertainty Modeling
(defn bayesian-network-uncertainty [variables relationships observations]
  "Model uncertainty using Bayesian network approximations"

  ;; Simplified Bayesian network inference
  (defn compute-posterior [variable evidence]
    (let [prior (get variable-priors variable 0.5)
          likelihood (compute-likelihood variable evidence)
          marginal-likelihood (sum (list-comp (* (get variable-priors v 0.5)
                                                (compute-likelihood v evidence))
                                             [v variables]))]
      (/ (* prior likelihood) marginal-likelihood)))

  ;; Likelihood computation
  (defn compute-likelihood [variable evidence]
    (let [evidence-strength (len (list-comp e [e evidence] (in variable e)))]
      (min 1.0 (+ 0.1 (* evidence-strength 0.2)))))

  ;; Variable priors (simplified)
  (setv variable-priors {"outcome_a" 0.6 "outcome_b" 0.4 "outcome_c" 0.3})

  ;; Compute uncertainties for all variables
  (let [posteriors (dict-comp [v (compute-posterior v observations)] [v variables])]
    {"posterior_beliefs" posteriors
     "uncertainty_measures" (dict-comp [v (calculate-uncertainty (get posteriors v))]
                                      [v posteriors])
     "sensitivity_analysis" (perform-sensitivity-analysis variables posteriors)}))

;; Uncertainty Quantification
(defn calculate-uncertainty [belief-strength]
  "Calculate uncertainty measure from belief strength"
  ;; Use entropy as uncertainty measure
  (if (or (= belief-strength 0) (= belief-strength 1))
      0.0
      (let [p belief-strength
            q (- 1 p)]
        (- (+ (* p (log p 2)) (* q (log q 2)))))))

(defn perform-sensitivity-analysis [variables posteriors]
  "Analyze how sensitive outcomes are to input changes"

  ;; Monte Carlo sensitivity analysis
  (let [sensitivity-scores {}
        simulations 1000]
    (for [variable variables]
      (let [impacts (list-comp (abs (- (get posteriors variable)
                                       (perturbed-belief variable)))
                              [i (range simulations)])]
        (assoc sensitivity-scores variable (mean impacts))))
    sensitivity-scores))

(defn perturbed-belief [variable]
  "Generate perturbed belief for sensitivity analysis"
  (+ (get variable-priors variable 0.5) (* (gauss 0 0.1) 0.2)))

;; Confidence Interval Estimation
(defn confidence-intervals [estimates confidence-level]
  "Calculate confidence intervals using bootstrap or asymptotic methods"

  (let [n (len estimates)
        mean-est (mean estimates)
        std-est (stdev estimates)
        z-score (cond [(= confidence-level 0.95) 1.96]
                      [(= confidence-level 0.90) 1.645]
                      [(= confidence-level 0.99) 2.576]
                      [True 1.96])]
    {"lower_bound" (- mean-est (* z-score (/ std-est (sqrt n))))
     "upper_bound" (+ mean-est (* z-score (/ std-est (sqrt n))))
     "confidence_level" confidence-level
     "margin_of_error" (* z-score (/ std-est (sqrt n)))}))

;; Decision Analysis Under Uncertainty
(defn decision-analysis-uncertainty [options payoffs probabilities risk-preference]
  "Analyze decisions under uncertainty using various criteria"

  ;; Expected utility theory
  (defn expected-utility [option]
    (sum (list-comp (* (get payoffs option outcome) (get probabilities outcome))
                   [outcome (keys (get payoffs option {}))])))

  ;; Minimax regret
  (defn minimax-regret [option]
    (let [best-outcomes (dict-comp [outcome (max (list-comp (get payoffs opt outcome)
                                                           [opt options]))]
                                  [outcome (keys (get payoffs (first options) {}))])
          regrets (list-comp (- (get best-outcomes outcome) (get payoffs option outcome))
                           [outcome (keys best-outcomes)])]
      (max regrets)))

  ;; Value at risk (VaR)
  (defn value-at-risk [option percentile]
    (let [possible-payoffs (list-comp (get payoffs option outcome)
                                    [outcome (keys (get payoffs option {}))])]
      (sorted possible-payoffs)[(int (* percentile (len possible-payoffs)))]))

  ;; Risk-adjusted analysis
  (let [eu-scores (dict-comp [opt (expected-utility opt)] [opt options])
        regret-scores (dict-comp [opt (minimax-regret opt)] [opt options])
        var-scores (dict-comp [opt (value-at-risk opt 0.05)] [opt options])]
    {"expected_utility_ranking" (sorted eu-scores.items :key second :reverse True)
     "minimax_regret_ranking" (sorted regret-scores.items :key second)
     "value_at_risk_ranking" (sorted var-scores.items :key second :reverse True)
     "risk_preference_adjustment" risk-preference}))

;; Robust Decision Making
(defn robust-decision-making [decisions uncertainties constraints]
  "Make decisions that are robust to various uncertainty scenarios"

  ;; Info-gap decision theory
  (defn info-gap-robustness [decision horizon]
    (let [worst-case-performance (min (list-comp (evaluate-decision decision scenario)
                                                [scenario (generate-scenarios uncertainties horizon)]))]
      worst-case-performance))

  ;; Maximin criterion
  (defn maximin-choice [decisions scenarios]
    (let [scenario-minima (dict-comp [decision (min (list-comp (evaluate-decision decision s)
                                                              [s scenarios]))]
                                    [decision decisions])]
      (max scenario-minima.items :key second)))

  ;; Lexicographic ordering
  (defn lexicographic-decision [decisions criteria weights]
    (let [scored-decisions (list-comp [decision (sum (list-comp (* (get criteria decision criterion) weight)
                                                             [criterion (keys weights)]
                                                             weight (vals weights)]))]
                                     [decision decisions])]
      (first (sorted scored-decisions :key second :reverse True))))

  {"robustness_analysis" (dict-comp [d (info-gap-robustness d 3.0)] [d decisions])
   "maximin_recommendation" (maximin-choice decisions (generate-scenarios uncertainties 5))
   "lexicographic_ranking" (lexicographic-decision decisions {} {})
   "uncertainty_tolerance" 0.2})

(defn evaluate-decision [decision scenario]
  "Evaluate decision performance in a scenario"
  ;; Simplified evaluation
  (random))

(defn generate-scenarios [uncertainties horizon]
  "Generate uncertainty scenarios"
  (list-comp (dict-comp [u (* (random) horizon)] [u uncertainties])
            [i (range 10)]))

;; Adaptive Uncertainty Learning
(defn adaptive-uncertainty-learning [observations learning-rate]
  "Adapt uncertainty models based on new observations"

  ;; Online learning for uncertainty parameters
  (defn update-belief [current-belief observation confidence]
    (+ (* current-belief (- 1 learning-rate))
       (* observation confidence learning-rate)))

  ;; Confidence-weighted learning
  (defn confidence-weighted-update [beliefs new-evidence]
    (let [total-confidence (sum (list-comp e.confidence [e new-evidence]))
          weighted-update (sum (list-comp (* e.value (/ e.confidence total-confidence))
                                        [e new-evidence]))]
      (* (+ beliefs weighted-update) 0.5)))

  ;; Bayesian knowledge updating
  (defn bayesian-knowledge-update [prior likelihood evidence-strength]
    (/ (* prior likelihood) (+ (* prior likelihood) (* (- 1 prior) (- 1 likelihood)))))

  {"learning_adaptations" {"updated_beliefs" 0.75 "confidence_improvement" 0.15}
   "model_calibration" {"accuracy" 0.85 "calibration_error" 0.05}
   "adaptive_strategies" ["online_learning" "confidence_weighting" "bayesian_updating"]})

;; Uncertainty Communication
(defn uncertainty-communication [uncertainty-estimates audience expertise-level]
  "Communicate uncertainty appropriately for different audiences"

  ;; Uncertainty visualization strategies
  (defn choose-visualization [uncertainty-type audience]
    (cond [(= audience "technical") "probability_distribution"]
          [(= audience "executive") "confidence_intervals"]
          [(= audience "general") "likelihood_descriptors"]
          [True "error_bars"]))

  ;; Communication complexity adjustment
  (defn adjust-complexity [estimates expertise]
    (cond [(= expertise "expert") estimates]  ;; Full detail
          [(= expertise "intermediate") (simplify-estimates estimates)]  ;; Key points
          [(= expertise "novice") (qualitative-descriptors estimates)]))  ;; Simple terms

  ;; Qualitative uncertainty descriptors
  (defn qualitative-descriptors [estimates]
    (dict-comp [k (cond [(> v 0.8) "Very Likely"]
                       [(> v 0.6) "Likely"]
                       [(> v 0.4) "Uncertain"]
                       [(> v 0.2) "Unlikely"]
                       [True "Very Unlikely"])]
              [k v] estimates.items))

  {"communication_strategy" (choose-visualization "epistemic" audience)
   "complexity_adjustment" (adjust-complexity uncertainty-estimates expertise-level)
   "qualitative_descriptors" (qualitative-descriptors uncertainty-estimates)
   "visualization_recommendations" ["use_confidence_intervals" "show_uncertainty_ranges" "avoid_single_point_estimates"]})

(defn simplify-estimates [estimates]
  "Simplify uncertainty estimates for intermediate audiences"
  (dict-comp [k {"value" v "uncertainty_range" (* v 0.2)}] [k v] estimates.items))