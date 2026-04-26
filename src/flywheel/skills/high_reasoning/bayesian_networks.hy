(defn optimize-bayesian-network [variables edges evidence query current-algorithm]
  "Recommend Bayesian network structure and inference optimization strategies
  
  Uses heuristics to:
  1. Suggest optimal elimination order for variable elimination
  2. Recommend simplifications based on network structure
  3. Choose appropriate inference algorithm
  4. Identify computational bottlenecks"
  (let [var-count (count variables)
        edge-count (count edges)
        evidence-count (count evidence)
        query-count (count query)
        density (/ (* 100 edge-count) (max 1 (* var-count (dec var-count))))  ; percentage
        avg-parents (if (> var-count 0) (/ edge-count var-count) 0)]
    (cond
      ;; Small networks: brute force or exact inference feasible
      (and (< var-count 10)
           (< density 20))
      {:recommended_algorithm "variable_elimination"
       :variable_elimination_order (min-fill-elimination-order variables edges)
       :reason "Small, sparse network: VE is optimal"
       :simplifications ["prune-unobserved-leaf-nodes"]
       :complexity "O(t) where t = max factor size"}
      
      ;; Large, sparse networks: good for belief propagation
      (and (> var-count 20)
           (< density 10))
      {:recommended_algorithm "belief_propagation"
       :variable_elimination-order (min-degree-elimination-order variables edges)
       :reason "Large sparse network: BP converges faster"
       :simplifications ["cluster-variables"
                        "min-fill-heuristic"]
       :complexity "O(n * d^w) where w = treewidth, d = domain size"}
      
      ;; Very dense networks: sampling methods often best
      (> density 50)
      {:recommended_algorithm "gibbs-sampling"
       :variable-elimination-order variables  ; Default order, sampling doesn't need VE order
       :reason "Dense network: approximate inference via sampling more efficient"
       :simplifications ["remove-deterministic-variables"
                        "collapse-multinomial-variables"]
       :complexity "O(n) where n = number of samples"}
      
      ;; Lots of evidence: factor in evidence early
      (> evidence-count (/ var-count 2))
      {:recommended_algorithm "factorization-with-evidence"
       :variable-elimination-order (evidence-first-order variables edges evidence)
       :reason "Many observed variables: reduce network early"
       :simplifications ["absorb-evidence-into-factors"
                        "prune-irrelevant-subtrees"]
       :complexity "O(m * t) where m = unobserved variables"}
      
      ;; Default: balance between approaches
      :else
      {:recommended_algorithm current-algorithm
       :variable-elimination-order (balanced-elimination-order variables edges)
       :reason "Mixed strategy for balanced performance"
       :simplifications ["standard-min-fill"]
       :complexity "O(n * 2^w) typical"})))

(defn calculate-heuristic [features]
  "Legacy heuristic function for compatibility"
  (if (> (.count features "peer_reviewed") 0)
      0.9
      0.5))

(defn min-fill-elimination-order [variables edges]
  "Heuristic: repeatedly eliminate the variable that creates
   the fewest new edges (minimizes fill-in)"
  (let [var-set (atom (set variables))
        edge-set (atom (set edges))
        order (atom [])]
    (while (seq @var-set)
      (let [best-var (apply min-key
                           #(count-new-edges % @var-set @edge-set)
                           @var-set)
            new-edges (edges-created-by-eliminating best-var @var-set @edge-set)]
        (swap! order conj best-var)
        (swap! var-set disj best-var)
        (swap! edge-set into new-edges)
        ;; Remove edges to/from eliminated variable
        (swap! edge-set (fn [es]
                         (set (filter #(and (not= (first %) best-var)
                                           (not= (second %) best-var)) es))))))
    @order))

(defn count-new-edges [var vars edges]
  "Count new edges created by eliminating var"
  (let [parents (filter #(= (second %) var) edges)
        children (filter #(= (first %) var) edges)]
    ;; Each parent will connect to each child (creating a clique)
    (count parents) ; Simplified: just use number of connections
    ))

(defn edges-created-by-eliminating [var vars edges]
  "Determine edges that would be created by eliminating var"
  (let [parents (map first (filter #(= (second %) var) edges))
        children (map second (filter #(= (first %) var) edges))]
    ;; Create edges from parents to children (completing the moral graph)
    (for [p parents
          c children
          :when (not= p c)]
      [p c])))

(defn min-degree-elimination-order [variables edges]
  "Heuristic: eliminate variable with minimum degree first"
  (let [var-set (atom (set variables))]
    (repeatedly (count variables)
                (fn []
                  (let [var (apply min-key #(degree % @var-set edges) @var-set)]
                    (swap! var-set disj var)
                    var)))))

(defn degree [var vars edges]
  "Count undirected edges incident to var among remaining vars"
  (count (filter #(and (vars (first %)) (vars (second %))
                       (or (= (first %) var) (= (second %) var)))
                 edges)))

(defn balanced-elimination-order [variables edges]
  "Balanced heuristic: combination of min-degree and min-fill"
  (let [min-fill (take (int (/ (count variables) 2))
                       (min-fill-elimination-order variables edges))
        remaining (filter #(not (some #{%} min-fill)) variables)]
    (concat min-fill (min-degree-elimination-order remaining edges))))

(defn evidence-first-order [variables edges evidence]
  "Prioritize eliminating variables with evidence first"
  (let [evidence-vars (map first evidence)
        remaining (filter #(not (some #{%} evidence-vars)) variables)]
    (concat evidence-vars remaining))))
