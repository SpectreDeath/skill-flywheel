(defn revise-beliefs [beliefs new-evidence current-strategy]
  "Recommend belief revision strategy based on evidence strength and current beliefs"
  (let [belief-count (count beliefs)
        evidence-count (count new-evidence)
        avg-belief-conf (if (> belief-count 0)
                         (/ (reduce + (map (fn [[_ conf]] conf) beliefs)) belief-count)
                         0)
        avg-evidence-strength (if (> evidence-count 0)
                               (/ (reduce + (map (fn [[_ strength]] strength) new-evidence)) evidence-count)
                               0)
        high-conf-beliefs (filter (fn [[_ conf]] (> conf 0.7)) beliefs)
        low-conf-beliefs (filter (fn [[_ conf]] (< conf 0.3)) beliefs)
        strong-evidence (filter (fn [[_ strength]] (> strength 0.7)) new-evidence)
        weak-evidence (filter (fn [[_ strength]] (< strength 0.3)) new-evidence)]
    (cond
      ;; If we have strong evidence and low confidence beliefs, be aggressive
      (and (> (count strong-evidence) 0) (> (count low-conf-beliefs) 0))
      {:strategy "aggressive" :reason "Strong evidence contradicts low-confidence beliefs"}
      
      ;; If beliefs are highly confident but we have conflicting evidence, be conservative
      (and (> (count high-conf-beliefs) 0) (> (count weak-evidence) 0))
      {:strategy "conservative" :reason "High-confidence beliefs with weak contradictory evidence"}
      
      ;; If we have much more evidence than beliefs, favor evidence
      (> evidence-count (* belief-count 2))
      {:strategy "evidence-favored" :reason "Significantly more evidence than prior beliefs"}
      
      ;; If we have much more belief than evidence, be conservative with belief changes
      (> belief-count (* evidence-count 2))
      {:strategy "belief-favored" :reason "Significantly more beliefs than new evidence"}
      
      ;; If confidence levels are similar, use balanced approach
      (and (< (math:abs (- avg-belief-conf avg-evidence-strength)) 0.2)
           (> belief-count 2)
           (> evidence-count 2))
      {:strategy "balanced" :reason "Similar confidence levels in beliefs and evidence"}
      
      ;; Default to current strategy if no clear pattern
      :else {:strategy current-strategy :reason "No strong heuristic signal detected"}))))

(defn calculate-heuristic [features]
  "Legacy heuristic function for compatibility"
  (if (> (.count features "peer_reviewed") 0)
      0.9
      0.5))