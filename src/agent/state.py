from typing import List, Dict, Any, Optional


class AgentState:
    """
    State object passed between pipeline nodes.
    """

    def __init__(
            self,
            question: str,
            queries: Optional[List[str]] = None,
            docs: Optional[List[Dict[str, Any]]] = None,
            reflections: Optional[List[Dict[str, Any]]] = None,
            max_iter: int = 2,
            iter_count: int = 0,
            slots: Optional[List[str]] = None,
            filled: Optional[List[str]] = None,
    ):
        self.question = question
        self.queries = queries if queries is not None else []
        self.docs = docs if docs is not None else []
        self.reflections = reflections if reflections is not None else []
        self.max_iter = max_iter
        self.iter_count = iter_count
        self.slots = slots if slots is not None else []
        self.filled = filled if filled is not None else []

    def to_dict(self):
        return {
            "question": self.question,
            "queries": self.queries,
            "docs": self.docs,
            "reflections": self.reflections,
            "max_iter": self.max_iter,
            "iter_count": self.iter_count,
            "slots": self.slots,
            "filled": self.filled,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            question=d.get("question"),
            queries=d.get("queries"),
            docs=d.get("docs"),
            reflections=d.get("reflections"),
            max_iter=d.get("max_iter", 2),
            iter_count=d.get("iter_count", 0),
            slots=d.get("slots", []),
            filled=d.get("filled", []),
        )
