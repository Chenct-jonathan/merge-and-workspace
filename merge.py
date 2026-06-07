# A python library dedicated to visualize the mathematical structure of syntactic merge.
# Project based mainly on Chomsky 2019a, Chomsky 2019b, Fong et al. 2024 and Marcolli et al. 2023. 

from typing import List, Optional, Set, Tuple, Union
from mathematical_structure import SyntacticObject, LexicalItem, ComplexSO, Workspace 
from pprint import pprint
from vis import visualize

def external_merge(ws: Workspace, alpha: SyntacticObject, beta: SyntacticObject) -> Workspace:
    """
    External Merge (EM): Joins two distinct trees from the workspace.
    Effect: b0 decreases by 1, #Acc increases by 2, sigma increases by 1.
    (Marcolli et al. 2023: Lemma 2.11 / Proposition 2.17)
    """
    if alpha not in ws.items or beta not in ws.items:
        raise ValueError("EM requires two distinct trees in the workspace.")

    new_items = list(ws.items)
    new_items.remove(alpha)
    new_items.remove(beta)
    new_items.append(ComplexSO(alpha, beta))
    return Workspace(tuple(new_items))
    
def internal_merge(ws: Workspace, tree: ComplexSO, term: SyntacticObject) -> Workspace:
    """
    Internal Merge (IM): Extracts an accessible term and merges it at the root.
    Implemented as the composition of extraction and re-merging with the quotient.
    Effect: All counting functions (b0, #Acc, sigma) remain constant.
    (Marcolli et al. 2023: Proposition 2.12 / Proposition 2.17)
    """
    if term not in tree.get_accessible_terms():
        raise ValueError("Term is not accessible within the selected tree.")

    # Cancellation of the deeper copy via the quotient map T/term.
    # (Marcolli et al. 2023: Section 2.5.2)
    quotient_tree = tree.quotient(term)
    pprint(quotient_tree)
    
    # Internal Merge results in M(term, tree/term).
    new_so = ComplexSO(term, quotient_tree)

    new_items = list(ws.items)
    new_items.remove(tree)
    new_items.append(new_so)
    #pprint(new_items)
    return Workspace(set(new_items))


if __name__ == "__main__":
    a, b, c = LexicalItem("a"), LexicalItem("b"), LexicalItem("c")
    ws0 = Workspace((a, b, c))
    
    # External Merge
    ws1 = external_merge(ws0, b, c)
    print()
    print()    
    print("ws1:")
    pprint(ws1)
    
    # External Merge
    ws2 = external_merge(ws1, a, ws1.items[-1])
    print()
    print()
    print("ws2:")
    pprint(ws2)
    visualize([ws0, ws1, ws2])

    # Internal Merge
    ws3 = internal_merge(ws2, ws2.items[0], ws1.items[-1])
    #pprint(ws3)
    #visualize_derivation([ws3])
    #print(f"Internal Merge Result: {ws3.items}")
    print(f"Sigma conservation check: {ws2.sigma} == {ws3.sigma}")