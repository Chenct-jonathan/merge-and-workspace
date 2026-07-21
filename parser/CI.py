# CI-Interface
import itertools
from pprint import pprint
from typing import Any, List, Optional, Set, Tuple

from EXT import *
from I_language import *
from syntax_types import *

def get_c_command_domain(head, so):
    if isinstance(so, frozenset) and head in so:
        domain = [item for item in so if item is not head]
        return domain[0] if domain else None
    
    # Recursive search for the head
    if isinstance(so, (tuple, frozenset)):
        for item in so:
            result = get_c_command_domain(head, item)
            if result: return result
    return None

def find_probe(so, target_feature: List[str]) -> list:
    probe = []
    if isinstance(so, LexicalItem):
        if any(feat in so.formal_feature for feat in target_feature):
            probe.append(so)
    elif isinstance(so, (tuple, frozenset)):
        for item in so:
            probe.extend(find_probe(item, target_feature))
    return probe

def count_goal(so) -> int:
    goal = 0
    if isinstance(so, LexicalItem):
        if 'D' in so.formal_feature:
            goal += 1
    elif isinstance(so, (tuple, frozenset)):
        for item in so:
            goal += count_goal(item)
    return goal

def INT(so) -> bool:
    # check θ-config
    theta_heads = find_probe(so, ["uθ,uθ"])
    
    for head in theta_heads:
        domain = get_c_command_domain(head, so)
        
        if domain is None:
            return False

        available = count_goal(domain)
        required = 2 if "uθ,uθ" in head.formal_feature else 1
        
        if available < required:
            return False
            
    return True

if __name__ == "__main__":
    raw="張三吃牛排"
    at=articut_parse(raw)
    print(at)
    la=EXT_to_LA(at)
    print(la)
    WS0=LA_to_WS0(la)
    print(repr_ws(WS0))    
    mergemerge=derivation(WS0)
    int_result=set()
    for ws in mergemerge:
        if INT(ws):
            int_result.add(ws)
            print(repr_ws(ws, False))
            
    print(f"total WS approved:{len(int_result)}")