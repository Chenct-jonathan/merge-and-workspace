# I_Language.py

# from __future__ import annotations
import itertools
from pprint import pprint
from typing import Set, Tuple, Optional, List

from syntax_types import *
from EXT import articut_parse, EXT_to_LA, linearize

def MERGE(so1: SyntacticObject, so2: SyntacticObject, ws: Workspace) -> Workspace:
    if so1 not in ws or so2 not in ws:
        raise ValueError("Cannot MERGE items that are not active in the current WS.")
        
    new_so: SyntacticObject = frozenset({so1, so2})
    return (ws - {so1, so2}) | {new_so}

def MINIMAL_SEARCH(so: SyntacticObject) -> Optional[LexicalItem]:
    '''
    Not used currently.
    Definition to be updated (Chomsky 2021 a.o.)
    '''
    if isinstance(so, LexicalItem):
        return so

    left, right = so
    left_head = MINIMAL_SEARCH(left)
    right_head = MINIMAL_SEARCH(right)
    
    if not left_head:
        return right_head
    if not right_head:
        return left_head

    left_active = any(f.startswith('u') for f in left_head.formal_feature)
    right_active = any(f.startswith('u') for f in right_head.formal_feature)
    
    if left_active and not right_active:
        return left_head
    elif right_active and not left_active:
        return right_head
    
    return left_head

def LA_to_WS0(la: LexicalArray) -> Workspace:
    """
    Maps Lexical Array (LA) into Workspace 0 (WS0).
    Additionally identifies uncategorized roots (√) and MERGEs them with their matching
    category-determining heads (e.g., n, V, A). Functional heads (C, INFL, v) bypass this step.
    """
    print("\n=========================")
    print("           WS0")
    print("=========================")    
    ws_elements: Set[SyntacticObject] = set()
    
    # Currently, the categories are fixed, but we are looking forward to better design.
    roots: Set[LexicalItem] = {item for item in la if item.form.startswith('√')}
    categorizers: Set[LexicalItem] = {item for item in la if item.form in ('n', 'V','A','appl')}
    functional_heads: Set[LexicalItem] = {item for item in la if item.form in ('C', 'INFL', 'v')}
    
    # Track available categorizing heads to avoid duplicate
    available_categorizers = list(categorizers)
    
    for root in roots:
        # just to make the operations cleaner so we jump start with all categorizers MERGEd
        # reads aritcut tags/semantic feature and map to available categorizer. (n and Vs only currently)  
        is_entity = any("entity" in sem for sem in root.semantic_feature)
        target_form = 'n' if is_entity else 'V'
        match_idx = next((i for i, h in enumerate(available_categorizers) if h.form == target_form), None)
        
        if match_idx is not None:
            head = available_categorizers.pop(match_idx)
            # local categorization MERGE: (√Root, Head)
            categorized_constituent = (root, head)
            ws_elements.add(categorized_constituent)
        else:
            ws_elements.add(root)
            
    # Keep functional heads flat in the active WS
    ws_elements.update(functional_heads)
    return frozenset(ws_elements)


def derivation(initial_ws: Workspace) -> List[Workspace]:
    """
    Narrow Syntax, free MERGE
    """
    print("\n=========================")
    print("      NARROW SYNTAX")
    print("=========================")
    
    current_layer_ws: Set[Workspace] = {initial_ws}
    layer_idx = 0
    
    # MERGE, works until 1 SO is present in WS.
    while True:
        # Check #SO in WS
        any_ws = next(iter(current_layer_ws))
        so_count = len(any_ws)
        
        print(f"\n[LAYER {layer_idx}] Active WS: {len(current_layer_ws)}")
        print(f"Current WS: {so_count} SOs remaining.")
        
        # Terminal condition: 1 SO remaining
        if so_count == 1:
            print(f"\nMERGE terminated at Layer {layer_idx}!")
            break
            
        next_layer_ws: Set[Workspace] = set()
        possible_ws: Set[Workspace] = set()
        
        for ws in current_layer_ws:
            possible_pairs = list(itertools.combinations(ws, 2))
            
            for so1, so2 in possible_pairs:
                candidate_ws = MERGE(so1, so2, ws)
                possible_ws.add(candidate_ws)
                merged = (so1, so2)
                
                next_layer_ws.add(candidate_ws)
                
                # INT(). We put PHASE aside for now.
                #from CI import INT
                #if INT(candidate_ws):
                    #next_layer_ws.add(candidate_ws)
        
        print(f"-> Combinations: {len(next_layer_ws)}")
        #print(f"-> Approved by INT/EXT: {len(next_layer_ws)}")
            
        current_layer_ws = next_layer_ws
        layer_idx += 1
        
    return list(current_layer_ws)

if __name__ == "__main__":
    raw="張三吃牛排"
    at=articut_parse(raw)
    print(at)
    la=EXT_to_LA(at)
    print(la)
    WS0=LA_to_WS0(la)
    print(repr_ws(WS0, False))    
    mergemerge=derivation(WS0)
    
    print("\n=========================")
    print("Some Possible Derivations")
    print("=========================")    
    for ws in mergemerge[:5]:
        print(repr_ws(ws, False))
    