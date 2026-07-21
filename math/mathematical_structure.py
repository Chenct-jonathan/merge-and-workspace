from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple, Union
from pprint import pprint

@dataclass(frozen=True)
class SyntacticObject:
    """
    Base class for Syntactic Objects (SO).
    Mathematically identified as binary, non-planar, rooted trees.
    (Marcolli et al. 2023 : Remark 2.2 / (2.3))
    """
    pass

@dataclass(frozen=True, order=True)
class LexicalItem(SyntacticObject):
    """
    Initial set SO_0 consisting of lexical items and syntactic features.
    (Marcolli et al. 2023 : Section 1.1 / Section 2.1)
    """
    label: str # Should we call it label?
    # About the data type: Maybe even LIs should be set(), might come back later.
    
    def __str__(self):
        return self.label    

@dataclass(frozen=True)
class ComplexSO(SyntacticObject):
    """
    A complex SO formed by the binary Merge operation M(α, β) = {α, β}.
    This represents an element in a free, non-associative, commutative magma.
    (Marcolli et al. 2023 : Definition 2.1 / (2.1) / (2.2))
    """
    elements: Tuple[SyntacticObject, ...] = field(init=False)
    # set(), {} does not allow duplicates. For this specific technical reason, var elements is initilaized as a Tuple.    
    # Though standard Merge is strictly binary (Marcolli et al. 2023: Section 4),
    # I leave the possibility for n>2-ary SOs so we can see the over/under-generalization effects.
    # If this library is then implemented as a base for some sort of NL parser, we might just use α, β or something else.

    def __init__(self, *args: SyntacticObject):
        """ 
        Implements commutativity (non-planarity).
        The unordered set {α, β} is identical to {β, α}.
        (Marcolli et al. 2023 : Section 2.1.1 / Remark 2.2)
        """
        # Ensure a canonical order to represent an unordered set. 
        # We might not need this since set(), {} is already order=False.
        # I keep this for clearer correspondence with the paper. 
        sorted_elements = tuple(sorted(args, key=str))
        object.__setattr__(self, 'elements', sorted_elements)    
    
    def __str__(self):
        # Displays the SO as an unordered set.
        return "{" + ", ".join(map(str, self.elements)) + "}"    

    def get_accessible_terms(self) -> Set[SyntacticObject]:
        """
        Accessible terms are proper nonempty subsets of the SO.
        In tree terms, these are subtrees rooted at internal (non-root) vertices.
        Acc(T) = {L_v = L(T_v) |v ∈ V_int(T)}.
        (Marcolli et al. 2023 : Definition 2.4 / (2.5))
        """
        terms = set()
        # For a binary tree {α, β}, α and β are the primary accessible terms.
        for child in self.elements:
            terms.add(child)
            # Recursively collect terms from deeper internal nodes.
            if isinstance(child, ComplexSO):
                terms.update(child.get_accessible_terms())
        return terms
    
    def quotient(self, target: SyntacticObject) -> Optional[SyntacticObject]:
        """
        Implements the quotient tree T/T_v via edge contraction.
        This is the formal mechanism for the cancellation of deeper copies.
        (Marcolli et al. 2023: Definition 2.5)
        """
        if self == target:
            # T/T = 1, where 1 is the multiplicative unit (empty tree).
            # (Marcolli et al. 2023: Section 2.2)
            return None 

        # Edge Contraction: Removing a branch and maintaining binary structure.
        # For binary trees, the quotient of a child is its sibling (Marcolli et al. 2023: Lemma 2.6).
        if len(self.elements) == 2:
            if self.elements[0] == target: return self.elements[1]
            if self.elements[1] == target: return self.elements[0]

        # Recursive search and contraction for deeper copies.
        new_children = []
        found = False
        for child in self.elements:
            if isinstance(child, ComplexSO) and target in child.get_accessible_terms():
                res = child.quotient(target)
                if res is not None: new_children.append(res)
                found = True
            elif child == target:
                found = True # Cancel the deeper copy
            else:
                new_children.append(child)
        
        if not found: return self
            
        # If only one child remains after contraction, return it to maintain maximal structure.
        if len(new_children) == 1: return new_children
        return ComplexSO(*new_children)
    
@dataclass(frozen=True)
class Workspace:
    """
    Identified as a binary non-planar forest (disjoint union of trees).
    A workspace is a finite multiset where repetitions are allowed.
    (Marcolli et al. 2023: Definition 2.3)
    """
    # Using tuple to ensure immutability and state stability (Algebraic state).
    # set(), {} does not allow duplicates. For this specific technical reason, var item is initilaized as a Tuple.
    items: Tuple[SyntacticObject, ...]

    @property
    def b0(self) -> int:
        """Number of connected components (trees) in the forest: b0(F)"""
        return len(self.items)

    @property
    def num_acc(self) -> int:
        """Total number of accessible terms in the workspace forest: #ACC(F)"""
        total = 0
        for item in self.items:
            if isinstance(item, ComplexSO):
                total += len(item.get_accessible_terms())
        return total

    @property
    def sigma(self) -> int:
        """Workspace size σ(F) := #V(F)=b0(F)+#Acc(F) (Marcolli et al. 2023: (2.8))."""
        return self.b0 + self.num_acc

    @property
    def sigma_hat(self) -> int:
        """Conserved counting function under External Merge σ_hat(F) := b0(F)+#V(F) (Marcolli et al. 2023: (2.9))."""
        return self.b0 + self.sigma