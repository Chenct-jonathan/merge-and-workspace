from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Tuple, List, Union
from pprint import pprint
import uuid
import re

from ArticutAPI import Articut
articut=Articut()

# Typings for Syntactic Objects (SOs)
# We should but havn't specify that FrozenSet['SyntacticObject'] should be binary.
SyntacticObject = Union['LexicalItem', FrozenSet['SyntacticObject']]

@dataclass(frozen=True)
class LexicalItem:
    form: str
    phase_head: bool = False
    formal_feature: FrozenSet[str] = field(default_factory=frozenset)
    semantic_feature: FrozenSet[str] = field(default_factory=frozenset)
    id: uuid.UUID = field(default_factory=uuid.uuid4, compare=True, hash=True)

    def __str__(self) -> str:
        return self.form

    def __repr__(self) -> str:
        syntax_driven = sorted([f for f in self.formal_feature if f.startswith('u')])
        feature_suffix = f"[{','.join(syntax_driven)}]" if syntax_driven else ""
        phase_marker = "+PHASE" if self.phase_head else ""
        return f"LI('{self.form}'{feature_suffix})"

pattern = re.compile(r"<([^>]+)>([^<]+)</\1>")

def articut_parse(raw_input: str) -> List[Tuple[str, str]]:
    return [(word, tag) for tag, word in pattern.findall(str(articut.parse(raw_input)['result_pos']))]

CDHEAD_CONFIG: Dict[str, dict] = {
    "ENTITY": {
        "head_form": "n",
        "phase_head": True,
        "formal_features": frozenset({"+n", "uΦ", "Φ"}),
    },
    "ACTION": {
        "head_form": "V",
        "phase_head": True,
        "formal_features": frozenset({"+v", "ACC"}),
    }
}

def externalization_to_interface(articut_pos: List[Tuple[str, str]]) -> List[FrozenSet[SyntacticObject]]:
    lexical_array = ["v*", "T"]
    
    for word, pos_tag in articut_pos:
        category = pos_tag.split("_")[0]
        if category not in CDHEAD_CONFIG:
            continue
            
        config = CDHEAD_CONFIG[category]
        
        sem_features = {f"+{pos_tag.lower()}"}
        if category == "ENTITY":
            sem_features.add("+animate" if "person" in pos_tag else "-animate")
            
        root_item = LexicalItem(form=f"√{word}", semantic_feature=frozenset(sem_features))
        head_item = LexicalItem(
            form=config["head_form"], 
            phase_head=config["phase_head"], 
            formal_feature=config["formal_features"]
        )
        
        # Perform Local Categorization Merge: {√Root, Category-Head}
        categorized_set = merge(root_item, head_item)
        lexical_array.append(categorized_set)
        
    return lexical_array

def merge(so1: SyntacticObject, so2: SyntacticObject) -> FrozenSet[SyntacticObject]:
    """The core operational engine of Narrow Syntax: Binary Unordered Set Formation."""
    if so1 == so2:
        raise ValueError("SMT Constraint: Cannot Merge an object with its identical self.")
    new_set = frozenset({so1, so2})
    assert len(new_set) == 2, "Parser Error: Generated a non-binary branching node."
    return new_set

def minimal_search(workspace: List[FrozenSet[SyntacticObject]], target_feature: str) -> Tuple[FrozenSet[SyntacticObject], int]:
    """
     LINGUISTIC PRIMITIVE: Minimal Search
    Scans the given workspace domain linearly to locate the first Syntactic Object 
    containing a LexicalItem that bears the target_feature.
    
    Returns:
        Tuple[FrozenSet, int]: The matched Syntactic Object and its workspace index.
    """
    for idx, syntactic_set in enumerate(workspace):
        for item in syntactic_set:
            if isinstance(item, LexicalItem) and target_feature in item.formal_feature:
                return syntactic_set, idx
                
    raise ValueError(f"Syntactic Crash: Minimal Search failed to find feature '{target_feature}' in workspace.")

def reconstruct_i_language(lexical_array: List[FrozenSet[SyntacticObject]]) -> SyntacticObject:
    """
    Step 3: Build the final hierarchal representation using Minimal Search primitives.
    """
    # 1. Execute Minimal Search to locate the verbal probe anchoring the phase
    v_head, v_idx = minimal_search(lexical_array, target_feature="ACC")

    # 2. Identify the Complement (IA) - The immediate subsequent domain object
    if v_idx + 1 < len(lexical_array):
        internal_argument = lexical_array[v_idx + 1]
    else:
        raise ValueError("Syntactic Crash: v* Phase head lacks a structural Complement (IA).")

    # Step A: First Merge (creates the core predicate relation)
    v_prime = merge(v_head, internal_argument)

    # 3. Identify the Specifier (EA) - Look back for the closest nominal expression
    # We slice the workspace to restrict Minimal Search to elements preceding the verb
    pre_verbal_domain = lexical_array[:v_idx]
    
    try:
        # Re-apply Minimal Search over the restricted pre-verbal domain to find the subject
        external_argument, _ = minimal_search(pre_verbal_domain, target_feature="Φ")
    except ValueError:
        raise ValueError("Syntactic Crash: No nominal External Argument found preceding v*P.")

    # Step B: Second Merge (specifier insertion)
    v_star_p = merge(external_argument, v_prime)
    
    return v_star_p

def pprint_SO(so: SyntacticObject) -> str:
    """Recursively stringifies the derived binary structure into standard linguistic set notation."""
    if isinstance(so, LexicalItem):
        # Strip structural functional syntax tokens out for pure surface semantics
        return re.sub(r"(√|Ø_v\*|Ø_n)", "", so.form).strip()

    if isinstance(so, frozenset):
        parts = [pprint_SO(elem) for elem in so]
        parts = [p for p in parts if p]  # Clear structural emptiness blanks
        
        if len(parts) == 1:
            return parts[0]
        return f"{{{parts[0]}, {parts[1]}}}" if len(parts) == 2 else ""
        
    return ""

# --- Driver Execution ---
if __name__ == "__main__":
    print("## Running Chomskyan I-Language Syntactic Parser Demo\n" + "-"*50)
    
    raw_sentence = "張三吃牛排"
    
    # 1. Articut Output Step
    articut_res = articut_parse(raw_sentence)
    print("\n[Step 1] Articut Token & Part of Speech Realization:")
    pprint(articut_res)
    
    # 2. C-I Interface Lexical Array Formation
    workspace_la = externalization_to_interface(articut_res)
    print("\n[Step 2] Workspace Lexical Array Primitives (Representational Objects):")
    pprint(workspace_la)
    
    # 3. Structural Derivation Execution
    i_language_tree = reconstruct_i_language(workspace_la)
    print("\n[Step 3] Computed Binary Heirarchal Derivation Object:")
    pprint(i_language_tree)
    
    # Final Visual Output Form
    surface_brackets = pprint_SO(i_language_tree)
    print(f"\n[Final Product] I-Language Set Format:{surface_brackets}")