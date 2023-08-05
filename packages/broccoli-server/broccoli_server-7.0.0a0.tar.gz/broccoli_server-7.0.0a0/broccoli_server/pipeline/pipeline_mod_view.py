import dataclasses
from typing import List, Optional, Dict, Set
from broccoli_server.mod_view import NamedModViewColumn


@dataclasses.dataclass
class PipelineModView:
    from_state: str
    to_states: Set[str]
    projections: List[NamedModViewColumn]
    filter_q_key: str
    limit: Optional[int] = None
    sort: Optional[Dict] = None
