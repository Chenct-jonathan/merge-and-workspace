# A python library dedicated to visualize the mathematical structure of syntactic merge.
# Project based mainly on Chomsky 2019a, Chomsky 2019b, Fong et al. 2024 and Marcolli et al. 2023. 

from typing import List, Optional, Set, Tuple, Union
from mathematical_structure import SyntacticObject, LexicalItem, ComplexSO, Workspace
from IPython.display import display, Math
from pprint import pprint
from vis import visualize

def merge(alpha: SyntacticObject, beta: SyntacticObject) -> ComplexSO:
    """M(α, β) := {α, β} (Marcolli et al. 2023: 1.1)"""
    """Opertation on Workspace: M_S,S' = ⊔◦(B+⊗id)◦δ_S,S'◦∆"""
    """Summation_v,w:T_v=S,T_w=S' (M(Tv,Tw)⊔(T/Tv)⊔(T/Tw))"""
    return ComplexSO(alpha, beta)

def external_merge(ws: Workspace, alpha: SyntacticObject, beta: SyntacticObject) -> Workspace:
    """
    External Merge (EM): Joins two distinct trees from the workspace.
    Effect: b0 decreases by 1, #Acc increases by 2, sigma increases by 1.
    (Marcolli et al. 2023: Lemma 2.11 / Proposition 2.17)
    """
    # ∆ = ws.items
    
    
    # δ_S,S' : V(F_SO0)⊗V(F_SO0)→V(F_SO0)⊗V(F_SO0) (Marcolli et al. 2023: Section 2.3)
    # In cases where no matching terms for S and S' are found, δ_S,S′(Fv⊗F/Fv) = 1⊗F. (Marcolli et al. 2023: (2.20))
    if alpha not in ws.items or beta not in ws.items:
        print()
        print("No matching terms for S and S'.")
        print("δ₍S,S'₎(Fᵥ ⊗ F/Fᵥ) = 1 ⊗ F")
        print("                         (Marcolli et al. 2023: (2.20))")
        return ws
    
    # B+⊗id, where B+ : V(F_N_SO0)→V(T_N_SO0) (Marcolli et al. 2023: Definition 2.8)
    new_items = list(ws.items)
    new_items.remove(alpha)
    new_items.remove(beta)
    new_items.append(merge(alpha, beta))
    
    # ⊔
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
    
    print("tree")
    pprint(tree)
    print("term")
    pprint(term)

    # Cancellation of the deeper copy via the quotient map T/term.
    # (Marcolli et al. 2023: Section 2.5.2)
    quotient_tree = tree.quotient(term)
    print()
    print()
    print("quotient_tree")
    pprint(quotient_tree)
    
    # here, problem: the "tree" ver should be replaced with quotient tree. not yet done
    
    pprint(merge(term, quotient_tree))
    # copy_item = list(ws.items)
    #pprint(copy_item)
    #copy_item.append(term)
    #copy_ws = Workspace(tuple(copy_item))
    #pprint(copy_ws)    
    
    # Internal Merge results in M(term, tree/term).
    #new_so = external_merge(copy_ws, term, quotient_tree)

    #new_items = list(ws.items)
    #new_items.remove(tree)
    #new_items.append(new_so)
    #pprint(new_items)
    #return Workspace(tuple(new_items))
    return Workspace(merge(term, quotient_tree))


if __name__ == "__main__":
    a, b, c, d = LexicalItem("a"), LexicalItem("b"), LexicalItem("c"), LexicalItem("d")
    ws0 = Workspace((a, b, c))
    print(ws0)
    
    # External Merge
    ws1 = external_merge(ws0, b, c)
    print()
    print()    
    print("ws1:")
    pprint(ws1)
    
    # External Merge
    ws2 = external_merge(ws1, a, ComplexSO(b, c))
    print()
    print()
    print("ws2:")
    pprint(ws2)
    visualize([ws0, ws1, ws2])
    
    # External Merge
    ws3 = external_merge(ws2, a, ComplexSO(b,ComplexSO(c, d)))
    print()
    print()
    print("ws3:")
    pprint(ws3)
    visualize([ws0, ws1, ws2, ws3])

    # Internal Merge
    ws4 = internal_merge(ws3, ComplexSO(a, ComplexSO(b,ComplexSO(c, d))), ComplexSO(c, d))
    print()
    print()
    print("ws4:")
    pprint(ws4)
    visualize([ws3, ws4])
    #print(f"Internal Merge Result: {ws3.items}")
    #print(f"Sigma conservation check: {ws2.sigma} == {ws3.sigma}")