# merge-and-workspace
A Python Library dedicated to build (i) visualization tools for the mathematical structure of syntactic merge (ii) a parser that constructs binary hierarchical structures and syntactic derivations from raw sentences (result of INT/EXT). 

## Parser Output
Below is an example of the processing pipeline output, covering linguistic categorization, lexical initialization, and syntactic derivation.

### 1. Linear Processing: EXT -> LA -> WS0
| Phase | Data |
| --- | --- |
| **Articut Result** | `[('張三', 'ENTITY_person'), ('吃', 'ACTION_verb'), ('牛排', 'ENTITY_noun')]` |
| **LEX** | `frozenset({'V'[uθ]*, 'n'[D,Φ]*, 'v'[uθ,uθ]*, 'C'[C]*, '√吃', 'INFL'[uEPP,uΦ], '√牛排', '√張三', 'n'[D,Φ]*})` |
| **WS0** | `C`, `INFL`, `v`, `吃`, `張三`, `牛排` |

---

### 2. Narrow Syntax (free MERGE)

```text
[LAYER 0] Active WS: 1    | 6 SOs remaining -> 15 Combinations
[LAYER 1] Active WS: 15   | 5 SOs remaining -> 105 Combinations
[LAYER 2] Active WS: 105  | 4 SOs remaining -> 420 Combinations
[LAYER 3] Active WS: 420  | 3 SOs remaining -> 945 Combinations
[LAYER 4] Active WS: 945  | 2 SOs remaining -> 945 Combinations
[LAYER 5] Active WS: 945  | 1 SOs remaining

MERGE terminated at Layer 5!

```

---

### 3. Some Possible Derivations

* `{{{{C, {INFL, v}}, 張三}, 吃}, 牛排}`
* `{C, {{v, 張三}, {{INFL, 牛排}, 吃}}}`
* `{v, {{{C, {INFL, 吃}}, 張三}, 牛排}}`
* `{{v, {C, {{INFL, 牛排}, 張三}}}, 吃}`
* `{v, {{C, 吃}, {{INFL, 牛排}, 張三}}}`

---

### 4. C-I Interface, INT() act as a filter, theta-configuration, feature checking. 

* `{{{{C, {INFL, v}}, 張三}, 吃}, 牛排}` --> blocked
* `{C, {{v, 張三}, {{INFL, 牛排}, 吃}}}` --> blocked
* `{v, {{{C, {INFL, 吃}}, 張三}, 牛排}}` --> blocked
* `{{v, {C, {{INFL, 牛排}, 張三}}}, 吃}` --> blocked
* `{v, {{C, 吃}, {{INFL, 牛排}, 張三}}}` --> blocked

--- 

### 5. Externalization, EXT() (currently) checks with the input sentence.
* `{C, {INFL, {張三, {v, {吃, 牛排}}}}}`
* `{C, {INFL, {牛排, {v, {吃, 張三}}}}}` --> blocked

