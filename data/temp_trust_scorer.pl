
% Disqualify if source is on a known banned list
disqualified(Source) :- banned(Source).
% Disqualify if source has zero reputation
disqualified(Source) :- reputation(Source, 0).

% Example data (could be dynamic)
banned(malicious_actor_01).
banned(shadow_node_42).
reputation(anonymous_proxy, 0).
reputation(verified_expert, 100).
