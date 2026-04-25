(defn calculate-heuristic [features]
  (if (> (.count features "peer_reviewed") 0)
      0.9
      0.5))
