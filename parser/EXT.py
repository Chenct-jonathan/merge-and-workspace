# Externalization.py
# from __future__ import annotations
import re
from typing import Any, List, Tuple, Set

from ArticutAPI import Articut
articut = Articut()

from syntax_types import LexicalItem, LexicalArray
from LEX import LEXICON
from pprint import pprint

pattern = re.compile(r"<([^>]+)>([^<]+)</\1>")

def articut_parse(raw_input: str) -> List[Tuple[str, str]]:
    '''
    The result of articut.parse() looks like <ENTITY_person>張三</ENTITY_person>. (Wang et al. 2019)
    We take (張三, ENTITY_person) instead.
    '''
    print("=========================")
    print("      Articut Result")
    print("=========================")    
    parsed = articut.parse(raw_input)
    result_pos_list = parsed.get('result_pos', [])
    raw_pos = result_pos_list[0] if result_pos_list else ""
    return [(word, tag) for tag, word in pattern.findall(raw_pos)]

def EXT_to_LA(articut_pos: List[Tuple[str, str]]) -> LexicalArray:
    '''
    Maps the parsed sequence to the Lexical Array.
    e.g., 
    input: [('張三', 'ENTITY_person'), ('吃', 'ACTION_verb'), ('牛排', 'ENTITY_noun')] -> 
    output: 
    frozenset({'C'[C]*,
           'V'[uθ]*,
           '√張三',
           'n'[D,Φ]*,
           'v'[uθ,uθ]*,
           'INFL'[uEPP,uΦ],
           'n'[D,Φ]*,
           '√牛排',
           '√吃'})
    '''
    print("\n=========================")
    print("           LEX")
    print("=========================")    
    la_elements = set()
    
    # We the input sentence is a grammatical sentence for now.
    # We therefore add C and INFL automatically. (Chomsky 2000, 2001)
    la_elements.add(LexicalItem(**LEXICON["C"]))
    la_elements.add(LexicalItem(**LEXICON["INFL"]))
    
    has_action = False

    for word, pos_tag in articut_pos:
        category = pos_tag.split("_")[0]
        if category not in LEXICON:
            continue
            
        config = LEXICON[category]
        
        # Semantic features, just for demonstration, not used in Narrow Syntax.
        sem_features = {f"+{pos_tag.lower()}"}
        if category == "ENTITY":
            sem_features.add("+animate" if "person" in pos_tag else "-animate")
        
        # All LEX are category-less roots at Lexical Array.    
        root_item = LexicalItem(form=f"√{word}", semantic_feature=frozenset(sem_features))
        la_elements.add(root_item)
        
        head_item = LexicalItem(**config)
        la_elements.add(head_item)
        
        # the v head for the shell-like structure of the predicate. (Larson 1988 a.o.)
        if category == "ACTION":
            has_action = True
            
    if has_action:
        la_elements.add(LexicalItem(**LEXICON["v"]))
        
    return frozenset(la_elements)

def linearize(so):
    pass

if __name__ == "__main__":
    pass