# A python library dedicated to visualize the mathematical structure of syntactic merge.
# Project based mainly on Chomsky 2019a, Chomsky 2019b, Fong et al. 2024 and Marcolli et al. 2023. 

from dataclasses import dataclass
from typing import List, Set, Union

@dataclass(frozen=True)
class SyntacticObject:
    """
    Base class for Syntactic Objects (SO).
    Mathematically identified as binary, non-planar, rooted trees.
    (Marcolli et al. 2023 : Remark 2.2/(2.3))
    """
    pass

@dataclass(frozen=True, order=True)
class LexicalItem(SyntacticObject):
    """
    Initial set SO_0 consisting of lexical items and syntactic features.
    (Marcolli et al. : 1.1 / Section 2.1)
    """
    label: str

@dataclass(frozen=True)
class ComplexSO(SyntacticObject):
    """
    A complex SO formed by the binary Merge operation M(α, β) = {α, β}.
    This represents an element in a free, non-associative, commutative magma.
    (Marcolli et al. : Definition 2.1 / (2.1) / (2.2))
    """
    left: SyntacticObject
    right: SyntacticObject

    def __post_init__(self):
        """
        Implements commutativity (non-planarity).
        The unordered set {α, β} is identical to {β, α}.
        (Marcolli et al. : Section 2.1.1 / Remark 2.2)
        """
        # Ensure a canonical order to represent an unordered set {left, right}
        if self.left > self.right:
            object.__setattr__(self, 'left', self.right)
            object.__setattr__(self, 'right', self.left)

    def get_accessible_terms(self) -> Set[SyntacticObject]:
        """
        Accessible terms are proper nonempty subsets of the SO.
        In tree terms, these are subtrees rooted at internal (non-root) vertices.
        Acc(T) = {L_v = L(T_v) |v ∈ V_int(T)}.
        (Marcolli et al. : Definition 2.4 / (2.5))
        """
        terms = set()
        # For a binary tree {α, β}, α and β are the primary accessible terms
        terms.add(self.left)
        terms.add(self.right)
        
        # Recursively collect terms from deeper internal nodes
        if isinstance(self.left, ComplexSO):
            terms.update(self.left.get_accessible_terms())
        if isinstance(self.right, ComplexSO):
            terms.update(self.right.get_accessible_terms())
        return terms

@dataclass
class Workspace:
    """
    A Workspace (WS) is a finite multiset of Syntactic Objects.
    Mathematically identified as a binary non-planar forest.
    (Marcolli et al. : Definition 2.3 / (2.4))
    """
    items: List[SyntacticObject]

    @property
    def b0(self) -> int:
        """
        The number of connected components (trees) in the forest.
        (Marcolli et al. : (2.7))
        """
        return len(self.items)

    @property
    def num_acc(self) -> int:
        """
        The total number of accessible terms in the workspace.
        (Marcolli et al. : (2.6) / (2.7))
        """
        total = 0
        for item in self.items:
            if isinstance(item, ComplexSO):
                total += len(item.get_accessible_terms())
        return total

    @property
    def sigma(self) -> int:
        """
        Workspace size σ(F), defined as the sum of SOs and accessible terms.
        σ(F) := b0(F) + #Acc(F) = #V(F) (total vertices).
        (Marcolli et al. : (2.8))
        """
        return self.b0 + self.num_acc

    @property
    def sigma_hat(self) -> int:
        """
        The conserved counting function σ̂(F).
        σ̂(F) := b0(F) + σ(F)
        (Marcolli et al. : (2.9))
        """
        return self.b0 + self.sigma

def external_merge(ws: Workspace, alpha: SyntacticObject, beta: SyntacticObject) -> Workspace:
    """
    Implements External Merge (EM) as a forest-level operation.
    Mathematically: F' = {alpha, beta} ⊔ (F \ {alpha, beta}).
    (Marcolli et al. : Section 2.4.1 / Lemma 2.11)
    """
    # 1. Verification of EM Condition:
    # Alpha and beta must be distinct connected components (trees) of the forest.
    # Marcolli et al. : Case (1) Section 2.4.1 / Lemma 2.11
    if alpha not in ws.items or beta not in ws.items:
        raise ValueError("Both alpha and beta must be independent trees in the workspace.")

    # 2. Forest Manipulation:
    # Create a new list (multiset) of trees.
    # The forest structure allows repeated copies (repetitions).
    # Marcolli et al. : Definition 2.3 / [3]
    new_items = list(ws.items)
    
    # 3. Removal of Components:
    # Removing two trees decreases the component count (b0) by 2.
    # Marcolli et al. : Proposition 2.17 / [4]
    new_items.remove(alpha)
    new_items.remove(beta)
    
    # 4. Binary Set Formation:
    # Creating M(alpha, beta) = {alpha, beta} as a single tree component.
    # This adds 1 back to b0, resulting in a net change of -1.
    # Marcolli et al. : (1.1) / (2.2) / [4]
    merged_object = ComplexSO(alpha, beta)
    new_items.append(merged_object)
    
    return Workspace(new_items)