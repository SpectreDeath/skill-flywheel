(defn solve-strategy [clauses variables current-strategy]
  "Recommend SAT solving strategy based on clause structure and variable count"
  (let [clause-count (count clauses)
        var-count (count variables)
        avg-clause-len (if (> clause-count 0)
                        (/ (reduce + (map count clauses)) clause-count)
                        0)
        var-to-occurrence (map (fn [v]
                               [v (count (filter (fn [c]
                                                (some (fn [lit] 
                                                      (or (= lit v) 
                                                          (= (str \- v) (str lit)))) 
                                                      c))
                                             clauses))])
                            variables)]
    (cond
      ;; For small problems, use brute force
      (< var-count 10) {:strategy "brute-force" :reason "Small variable set"}
      
      ;; For highly constrained problems, use unit propagation first
      (> (/ clause-count var-count) 4) {:strategy "unit-propagation-first" :reason "High clause-to-variable ratio"}
      
      ;; For clauses with long averages, look for pure literals
      (> avg-clause-len 3) {:strategy "pure-literal-heuristic" :reason "Long average clause length"}
      
      ;; Default: use DLIS (Dynamic Largest Individual Sum)
      :else {:strategy "dlis" :reason "Default heuristic"}))))

(defn calculate-heuristic [features]
  "Legacy heuristic function for compatibility"
  (if (> (.count features "peer_reviewed") 0)
      0.9
      0.5))