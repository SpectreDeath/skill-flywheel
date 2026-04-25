(defn calculate-suitability-score [description]
  (let [keywords ["logic" "heuristic" "rules" "reliability" "trust" 
                  "verification" "optimization" "orchestration" 
                  "reasoning" "epistemic" "validation" "consensus"
                  "formal" "mathematical" "truth" "inference" "engine"]
        score 0.1
        desc-lower (.lower description)]
    (for [kw keywords]
      (if (> (.count desc-lower kw) 0)
          (setv score (+ score 0.15))))
    (min 1.0 score)))
