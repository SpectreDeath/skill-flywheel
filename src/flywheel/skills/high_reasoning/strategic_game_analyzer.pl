% Strategic Game Theory Analysis in Prolog
% Nash equilibria, Pareto optimality, and strategic reasoning

% Game types and their properties
game_type(prisoners_dilemma).
game_type(chicken).
game_type(staghunt).
game_type(battle_of_sexes).

% Nash equilibrium detection
nash_equilibrium('cooperate_cooperate') :- game_type(prisoners_dilemma), false.  % No mutual cooperation
nash_equilibrium('defect_defect') :- game_type(prisoners_dilemma).  % Dominant equilibrium

nash_equilibrium('swerve_swerve') :- game_type(chicken).  % Risk-dominant equilibrium
nash_equilibrium('straight_straight') :- game_type(chicken).  % Payoff-dominant equilibrium

nash_equilibrium('stag_stag') :- game_type(staghunt).  % Both equilibria
nash_equilibrium('hare_hare') :- game_type(staghunt).

% Pareto optimality
pareto_optimal('cooperate_cooperate') :- game_type(prisoners_dilemma).  % Best for both
pareto_optimal('stag_stag') :- game_type(staghunt).  % Best outcome

% Strategy dominance
strictly_dominates(S1, S2, Player) :-
    game_type(_),
    forall(other_player_strategy(S2, OtherStrat),
           payoff_better(S1, OtherStrat, Player, S2, OtherStrat, Player)).

weakly_dominates(S1, S2, Player) :-
    game_type(_),
    not(strictly_dominates(S2, S1, Player)),
    exists(other_player_strategy(S2, OtherStrat),
           payoff_better(S1, OtherStrat, Player, S2, OtherStrat, Player)).

% Payoff comparison
payoff_better(Strat1, OtherStrat1, Player, Strat2, OtherStrat2, Player) :-
    payoff(Player, Strat1, OtherStrat1, Payoff1),
    payoff(Player, Strat2, OtherStrat2, Payoff2),
    Payoff1 > Payoff2.

% Game-specific payoff definitions (simplified)
payoff(alice, cooperate, cooperate, 3) :- game_type(prisoners_dilemma).
payoff(alice, cooperate, defect, 0) :- game_type(prisoners_dilemma).
payoff(alice, defect, cooperate, 5) :- game_type(prisoners_dilemma).
payoff(alice, defect, defect, 1) :- game_type(prisoners_dilemma).

payoff(bob, cooperate, cooperate, 3) :- game_type(prisoners_dilemma).
payoff(bob, defect, cooperate, 5) :- game_type(prisoners_dilemma).
payoff(bob, cooperate, defect, 0) :- game_type(prisoners_dilemma).
payoff(bob, defect, defect, 1) :- game_type(prisoners_dilemma).

% Cooperative advantages
cooperative_advantage('mutual_benefit') :- game_type(prisoners_dilemma), false.  % No cooperation advantage
cooperative_advantage('trust_building') :- game_type(staghunt).
cooperative_advantage('risk_sharing') :- game_type(chicken).

% Repeated game considerations
repeated_game_advantage('tit_for_tat') :- game_type(prisoners_dilemma).
repeated_game_advantage('trigger_strategies') :- game_type(_).

% Evolutionary stability
evolutionarily_stable('defect_defect') :- game_type(prisoners_dilemma).  % Tit-for-tat in repeated games
evolutionarily_stable('stag_stag') :- game_type(staghunt).

% Bargaining and negotiation
bargaining_solution('nash_bargaining') :- game_type(battle_of_sexes).
bargaining_solution('kalai_smorodinsky') :- game_type(_).

% Coalition formation
stable_coalition(C) :- coalition(C), not(blocked_by(C, _)).

% Fairness considerations
fair_outcome(Outcome) :- pareto_optimal(Outcome), envy_free(Outcome).

% Risk analysis
risk_dominant('defect_defect') :- game_type(prisoners_dilemma).
payoff_dominant('cooperate_cooperate') :- game_type(prisoners_dilemma).