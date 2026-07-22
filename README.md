# merge-and-workspace
A python library dedicated to visualize the mathematical structure of syntactic merge.

Parser Demo
---
=========================
      Articut Result
=========================
[('張三', 'ENTITY_person'), ('吃', 'ACTION_verb'), ('牛排', 'ENTITY_noun')]

=========================
           LEX
=========================
frozenset({'V'[uθ]*, 'n'[D,Φ]*, 'v'[uθ,uθ]*, 'C'[C]*, '√吃', 'INFL'[uEPP,uΦ], '√牛排', '√張三', 'n'[D,Φ]*})

=========================
           WS0
=========================

C,
  INFL,
  v,
  吃,
  張三,
  牛排


=========================
      NARROW SYNTAX
=========================

[LAYER 0] Active WS: 1
Current WS: 6 SOs remaining.
-> Combinations: 15

[LAYER 1] Active WS: 15
Current WS: 5 SOs remaining.
-> Combinations: 105

[LAYER 2] Active WS: 105
Current WS: 4 SOs remaining.
-> Combinations: 420

[LAYER 3] Active WS: 420
Current WS: 3 SOs remaining.
-> Combinations: 945

[LAYER 4] Active WS: 945
Current WS: 2 SOs remaining.
-> Combinations: 945

[LAYER 5] Active WS: 945
Current WS: 1 SOs remaining.

MERGE terminated at Layer 5!

=========================
Some Possible Derivations
=========================

{{{{C, {INFL, v}}, 張三}, 吃}, 牛排}


{C, {{v, 張三}, {{INFL, 牛排}, 吃}}}


{v, {{{C, {INFL, 吃}}, 張三}, 牛排}}


{{v, {C, {{INFL, 牛排}, 張三}}}, 吃}


{v, {{C, 吃}, {{INFL, 牛排}, 張三}}}
