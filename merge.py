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
    Marcolli et al. : 1.1 / Section 2.1
    """
    label: str

@dataclass(frozen=True)
class ComplexSO(SyntacticObject):
    """
    A complex SO formed by the binary Merge operation M(α, β) = {α, β}.
    This represents an element in a free, non-associative, commutative magma.
    Marcolli et al. : Definition 2.1 / (2.1) / (2.2)
    """
    left: SyntacticObject
    right: SyntacticObject

    def __post_init__(self):
        """
        Implements commutativity (non-planarity).
        The unordered set {α, β} is identical to {β, α}.
        Marcolli et al. : Section 2.1.1 / Remark 2.2
        """
        # Ensure a canonical order to represent an unordered set {left, right}
        if self.left > self.right:
            object.__setattr__(self, 'left', self.right)
            object.__setattr__(self, 'right', self.left)

    def get_accessible_terms(self) -> Set[SyntacticObject]:
        """
        Accessible terms are proper nonempty subsets of the SO.
        In tree terms, these are subtrees rooted at internal (non-root) vertices.
        Marcolli et al. : Definition 2.4 / (2.5)
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
    Marcolli et al. : Definition 2.3 / (2.4)
    """
    items: List[SyntacticObject]

    @property
    def b0(self) -> int:
        """
        The number of connected components (trees) in the forest.
        Marcolli et al. : (2.7)
        """
        return len(self.items)

    @property
    def num_acc(self) -> int:
        """
        The total number of accessible terms in the workspace.
        Marcolli et al. : (2.6) / (2.7)
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
        Marcolli et al. : (2.8)
        """
        return self.b0 + self.num_acc

    @property
    def sigma_hat(self) -> int:
        """
        The conserved counting function σ̂(F).
        σ̂(F) := b0(F) + σ(F)
        Marcolli et al. : (2.9)
        """
        return self.b0 + self.sigma

def external_merge(ws: Workspace, alpha: SyntacticObject, beta: SyntacticObject) -> Workspace:
    """
    External Merge (EM) combines two separate trees into one.
    Results: b0 decreases by 1, #Acc increases by 2, σ increases by 1, σ̂ is conserved.
    Marcolli et al. : Lemma 2.11 / Proposition 2.17
    """
    new_items = list(ws.items)
    new_items.remove(alpha)
    new_items.remove(beta)
    new_items.append(ComplexSO(alpha, beta))
    return Workspace(new_items)