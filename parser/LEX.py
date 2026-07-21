# LEXICON

# from __future__ import annotations
from typing import Dict

LEXICON: Dict[str, dict] = {
    "ENTITY": {
        "form": "n",   
        "phase_head": True,
        "formal_feature": frozenset({"D", "Φ"}),
    },
    "ACTION": {
        "form": "V",
        "phase_head": True,
        "formal_feature": frozenset({"uθ"}),
    },
    "v": {
        "form": "v",
        "phase_head": True,
        "formal_feature": frozenset({"uθ,uθ"}) # a bit of a trick here, set cllapse identical elements.
    },
    "INFL": {
        "form": "INFL",
        "phase_head": False,
        "formal_feature": frozenset({"uEPP", "uΦ"})
    },
    "C": {
        "form": "C",
        "phase_head": True,
        "formal_feature": frozenset({"C"})
    }    
}