% Tier 1 domains (Hard Rules)
is_tier1_domain(epistemology).
is_tier1_domain(logic).
is_tier1_domain(logic_programming).
is_tier1_domain(game_theory).
is_tier1_domain(formal_methods).
is_tier1_domain(reasoning).

% Rule: Recommended if it's a Tier 1 domain
recommendation(Skill, "Highly Recommended") :- 
    domain(Skill, Domain), 
    is_tier1_domain(Domain).

% Default recommendation
recommendation(Skill, "Consider for Enhancement") :- 
    not(recommendation(Skill, "Highly Recommended")).
