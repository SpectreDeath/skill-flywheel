;; Computational Creativity Heuristics in Hy
;; Creative solution generation and optimization

(import hy)
(import [random [random choice sample]])
(import [collections [Counter]])

;; Creative solution generation
(defn generate-creative-solutions [problem constraints inspiration n-solutions]
  "Generate diverse creative solutions using heuristics"

  ;; Solution diversity heuristic
  (defn ensure-diversity [solutions]
    (let [types (list-comp s.type [s solutions])
          type-counts (Counter types)]
      (if (> (max type-counts.values) (* 0.6 (len solutions)))
          (regenerate-solutions solutions)  ;; Too homogeneous
          solutions)))

  ;; Inspiration integration
  (defn integrate-inspiration [solution inspiration]
    (let [inspired-elements (sample inspiration (min 2 (len inspiration)))]
      (merge-dicts solution {"inspired_by" inspired-elements})))

  ;; Constraint satisfaction check
  (defn satisfies-constraints [solution constraints]
    (all (fn [c] (check-constraint solution c)) constraints))

  ;; Generate initial solutions
  (let [initial-solutions (list-comp (create-solution i) [i (range n-solutions)])]
    (ensure-diversity (list-comp (integrate-inspiration s inspiration)
                                [s initial-solutions]
                                (satisfies-constraints s constraints)))))

(defn create-solution [idx]
  "Create a single creative solution"
  {"id" idx "type" (choice ["design" "process" "strategy"])
   "novelty" (random) "feasibility" (random) "impact" (random)})

(defn regenerate-solutions [solutions]
  "Regenerate solutions for better diversity"
  (generate-creative-solutions "problem" [] [] (len solutions)))

(defn check-constraint [solution constraint]
  "Check if solution satisfies a constraint"
  True)  ;; Simplified

(defn merge-dicts [&rest dicts]
  "Merge multiple dictionaries"
  (let [result {}]
    (for [d dicts]
      (for [k v] d.items]
        (assoc result k v)))
    result))

;; Solution optimization
(defn optimize-creative-solutions [solutions criteria weights]
  "Optimize creative solutions using multi-criteria heuristics"

  ;; Pareto front identification
  (defn identify-pareto-front [solutions criteria]
    (let [pareto-set []]
      (for [s solutions]
        (when (not (dominated-by-any s solutions criteria))
          (.append pareto-set s)))
      pareto-set))

  (defn dominated-by-any [solution all-solutions criteria]
    (any (fn [other] (dominates other solution criteria))
         (list-comp o [o all-solutions] (!= o solution))))

  (defn dominates [s1 s2 criteria]
    (let [all-better (all (fn [c] (>= (get s1 c 0) (get s2 c 0))) criteria)
          some-better (any (fn [c] (> (get s1 c 0) (get s2 c 0))) criteria)]
      (and all-better some-better)))

  ;; Weighted scoring
  (defn calculate-weighted-score [solution criteria weights]
    (sum (list-comp (* (get solution c 0) (get weights c 1)) [c criteria])))

  ;; Optimize
  (let [pareto-solutions (identify-pareto-front solutions criteria)
        scored-solutions (list-comp {"solution" s "score" (calculate-weighted-score s criteria weights)}
                                   [s pareto-solutions])]
    (sorted scored-solutions :key (fn [x] x.score) :reverse True)))

;; Creative evaluation
(defn evaluate-creativity [solutions baseline-solutions]
  "Evaluate creativity using novelty and quality metrics"

  ;; Novelty assessment
  (defn assess-novelty [solution baseline]
    (let [similarities (list-comp (solution-similarity solution b) [b baseline])
          avg-similarity (mean similarities)]
      (- 1 avg-similarity)))

  ;; Quality assessment
  (defn assess-quality [solution]
    (let [feasibility (get solution "feasibility" 0.5)
          impact (get solution "impact" 0.5)]
      (mean [feasibility impact])))

  ;; Overall creativity
  (let [creativity-scores (list-comp {"novelty" (assess-novelty s baseline-solutions)
                                     "quality" (assess-quality s)
                                     "overall" (* (assess-novelty s baseline-solutions)
                                                (assess-quality s))}
                                    [s solutions])]
    {"creativity_scores" creativity-scores
     "average_novelty" (mean (list-comp cs.novelty [cs creativity-scores]))
     "average_quality" (mean (list-comp cs.quality [cs creativity-scores]))
     "creativity_distribution" (analyze-distribution creativity-scores)}))

(defn solution-similarity [s1 s2]
  "Calculate similarity between solutions"
  0.5)  ;; Placeholder

(defn mean [values]
  "Calculate mean of values"
  (/ (sum values) (len values)))

(defn analyze-distribution [scores]
  "Analyze distribution of creativity scores"
  {"high_creativity" (len (list-comp s [s scores] (> s.overall 0.7)))
   "medium_creativity" (len (list-comp s [s scores] (and (>= s.overall 0.4) (<= s.overall 0.7))))
   "low_creativity" (len (list-comp s [s scores] (< s.overall 0.4)))})