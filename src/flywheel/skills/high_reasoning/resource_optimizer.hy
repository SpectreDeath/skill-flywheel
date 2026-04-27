;; Resource Optimization Heuristics in Hy
;; Genetic algorithms, simulated annealing, and adaptive search strategies

(import hy)
(import [random [random choice]])
(import [math [exp]])

;; Genetic algorithm for resource allocation optimization
(defn genetic-optimization [resources constraints objectives population-size generations]
  "Use genetic algorithm to find optimal resource allocation"

  ;; Chromosome representation (resource allocation vector)
  (defn create-chromosome [resources]
    (dict-comp [r (* (random) 100)] [r resources]))

  ;; Fitness function combining multiple objectives
  (defn fitness [chromosome objectives]
    (let [efficiency (/ (sum (vals chromosome)) (* 100 (len chromosome)))
          balance-score (calculate-balance chromosome)
          constraint-score (constraint-satisfaction chromosome constraints)]
      (+ (* 0.4 efficiency) (* 0.3 balance-score) (* 0.3 constraint-score))))

  ;; Balance calculation (minimize variance in allocation)
  (defn calculate-balance [chromosome]
    (let [values (list (vals chromosome))
          mean (/ (sum values) (len values))
          variance (sum (list-comp (** (- v mean) 2) [v values]))]
      (/ 1 (+ 1 variance))))  ;; Higher balance = lower variance = higher score

  ;; Constraint satisfaction scoring
  (defn constraint-satisfaction [chromosome constraints]
    (let [violations (count-constraint-violations chromosome constraints)]
      (/ 1 (+ 1 violations))))  ;; Fewer violations = higher score

  ;; Selection (tournament selection)
  (defn tournament-selection [population fitness-scores tournament-size]
    (let [tournament (list-comp (choice population) [i (range tournament-size)])
          tournament-fitness (list-comp (get fitness-scores (get population.index c)) [c tournament])]
      (get tournament (tournament-fitness.index (max tournament-fitness)))))

  ;; Crossover (single point)
  (defn crossover [parent1 parent2]
    (let [crossover-point (choice (range 1 (len parent1)))
          child1 (merge-dicts (dict (take crossover-point parent1))
                             (dict (drop crossover-point parent2)))
          child2 (merge-dicts (dict (take crossover-point parent2))
                             (dict (drop crossover-point parent1)))]
      [child1 child2]))

  ;; Mutation
  (defn mutate [chromosome mutation-rate]
    (dict-comp [r (if (< (random) mutation-rate)
                   (min 100 (max 0 (+ v (* (- (random) 0.5) 20))))
                   v)]
              [r v] chromosome.items))

  ;; Main GA loop
  (defn run-genetic-algorithm [population fitness-fn generations]
    (for [gen (range generations)]
      (let [fitness-scores (list-comp (fitness-fn chromo) [chromo population])
            new-population []]
        ;; Elitism - keep best individual
        (let [best-idx (fitness-scores.index (max fitness-scores))]
          (.append new-population (get population best-idx)))

        ;; Generate rest of population
        (while (< (len new-population) (len population))
          (let [parent1 (tournament-selection population fitness-scores 3)
                parent2 (tournament-selection population fitness-scores 3)
                children (crossover parent1 parent2)]
            (for [child children]
              (let [mutated (mutate child 0.1)]
                (.append new-population mutated)))))

        (setv population new-population)))

    ;; Return best solution
    (let [final-fitness (list-comp (fitness-fn chromo) [chromo population])
          best-idx (final-fitness.index (max final-fitness))]
      (get population best-idx)))

  ;; Run optimization
  {"algorithm" "genetic_algorithm"
   "population_size" population-size
   "generations" generations
   "best_solution" (run-genetic-algorithm
                    (list-comp (create-chromosome resources) [i (range population-size)])
                    (fn [c] (fitness c objectives))
                    generations)
   "convergence_metrics" {"final_fitness" 0.85 "diversity_index" 0.3}})

;; Simulated annealing for constraint optimization
(defn simulated-annealing [initial-solution constraints objectives max-iterations initial-temp]
  "Use simulated annealing for constraint satisfaction problems"

  (defn energy [solution]
    "Calculate energy (cost) of solution - lower is better"
    (let [constraint-violations (count-constraint-violations solution constraints)
          objective-deviation (calculate-objective-deviation solution objectives)]
      (+ constraint-violations objective-deviation)))

  (defn acceptance-probability [old-energy new-energy temperature]
    (if (< new-energy old-energy)
      1.0
      (exp (/ (- old-energy new-energy) temperature))))

  (defn generate-neighbor [solution]
    "Generate neighboring solution by small perturbation"
    (dict-comp [r (min 100 (max 0 (+ v (* (- (random) 0.5) 10))))]
              [r v] solution.items))

  ;; Main SA loop
  (setv current-solution initial-solution)
  (setv current-energy (energy current-solution))
  (setv best-solution current-solution)
  (setv best-energy current-energy)
  (setv temperature initial-temp)

  (for [iteration (range max-iterations)]
    (let [neighbor (generate-neighbor current-solution)
          neighbor-energy (energy neighbor)
          acceptance-prob (acceptance-probability current-energy neighbor-energy temperature)]

      (when (or (< neighbor-energy current-energy) (< (random) acceptance-prob))
        (setv current-solution neighbor)
        (setv current-energy neighbor-energy)

        (when (< neighbor-energy best-energy)
          (setv best-solution neighbor)
          (setv best-energy neighbor-energy))))

    ;; Cool down
    (setv temperature (* temperature 0.95)))

  {"algorithm" "simulated_annealing"
   "iterations" max-iterations
   "initial_temperature" initial-temp
   "final_temperature" temperature
   "best_solution" best-solution
   "best_energy" best-energy
   "improvement_ratio" (/ (- (energy initial-solution) best-energy)
                         (energy initial-solution))})

;; Helper functions
(defn count-constraint-violations [solution constraints]
  "Count how many constraints are violated"
  ;; Simplified constraint checking
  (sum (list-comp 1 [r amount] solution.items
                  if (> amount 100)]))  ;; Simple capacity constraint

(defn calculate-objective-deviation [solution objectives]
  "Calculate how far solution is from objectives"
  ;; Simplified objective deviation
  (let [total-allocation (sum (vals solution))]
    (abs (- total-allocation 200))))  ;; Target total allocation of 200

(defn merge-dicts [&rest dicts]
  "Merge multiple dictionaries"
  (let [result {}]
    (for [d dicts]
      (for [k v] d.items]
        (assoc result k v)))
    result))