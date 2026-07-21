# Syntax types and some representation tools for convenience
#from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Union, TypeAlias, Tuple
import uuid

@dataclass(frozen=True)
class LexicalItem:
    '''
    Lexical Item bears formal features and semantic features. Chomsky (1995)
    '''
    form: str
    phase_head: bool = False
    formal_feature: FrozenSet[str] = field(default_factory=frozenset)
    semantic_feature: FrozenSet[str] = field(default_factory=frozenset)
    id: uuid.UUID = field(default_factory=uuid.uuid4, compare=True, hash=True)

    def __str__(self) -> str:
        return self.form

    def __repr__(self) -> str:
        '''
        Semantic features are not visible in Narrow Syntax.
        '''
        syntax_driven = sorted(list(self.formal_feature))
        feature_suffix = f"[{','.join(syntax_driven)}]" if syntax_driven else ""
        phase_marker = "*" if self.phase_head else ""
        return f"'{self.form}'{feature_suffix}{phase_marker}"
    
SyntacticObject: TypeAlias = Union[LexicalItem, Tuple['SyntacticObject', 'SyntacticObject']] # maybe we have to figure out a way to not use Tuple and use Set.
LexicalArray: TypeAlias = FrozenSet[LexicalItem]
Workspace: TypeAlias = FrozenSet[SyntacticObject]

def format_so(so, show_features: bool = True) -> str:
    '''
    To avoid non-reader-friendly representations of examples invloving category-determining heads. (Marantz 2006)
    We just show the root with the formal features for convenience.
    e.g.,  {'√張三', 'n'[D,Φ]*} will be represented as 張三[D,Φ].
    '''    
    # Lexical Items
    if isinstance(so, LexicalItem):
        word = so.form.strip("√")
        if show_features and so.formal_feature:
            feats = f"[{','.join(sorted(so.formal_feature))}]"
            return f"{word}{feats}"
        return word

    # Root + Categorizer
    if isinstance(so, tuple):
        if show_features:
            return "".join(format_so(x, show_features) for x in so if x is not None)
        else:
            root = next((x for x in so if isinstance(x, LexicalItem) and x.form.startswith('√')), None)
            return format_so(root, show_features) if root else ""

    # MERGEd Nodes (Frozenset)
    if isinstance(so, frozenset):
        # Sorted for consistent representation
        items = sorted([format_so(item, show_features) for item in so])
        return f"{{{', '.join(items)}}}"

    return str(so)


def repr_ws(ws: Workspace, show_features: bool = True) -> str:
    items = sorted([format_so(item, show_features) for item in ws])
    return "\n" + ",\n  ".join(items) + "\n"