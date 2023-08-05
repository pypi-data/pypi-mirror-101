from typing import List, Optional, Dict, Set
from broccoli_server.content import ContentStore
from .pipeline_state import PipelineState
from .pipeline_worker import PipelineWorkerInstance, StateKey
from .pipeline_mod_view import PipelineModView


class Pipeline(object):
    def __init__(self, name: str):
        self.name = name
        self.states = []  # type: List[PipelineState]
        self.starting_state = None  # type: Optional[PipelineState]
        self.worker_instances = []  # type: List[PipelineWorkerInstance]
        self.mod_views = []  # type: List[PipelineModView]
        self._graph_adj_list = {}  # type: Dict[str, List[str]]

    def add_state(self, state: PipelineState, is_starting: bool = False):
        if state in self._get_state_names():
            raise RuntimeError(f"For pipeline {self.name} state {state.name} already exists")
        if is_starting:
            if self.starting_state:
                raise RuntimeError(f"For pipeline {self.name} starting state is already set")
            self.starting_state = state
        self.states.append(state)

    def _get_state_names(self) -> List[str]:
        return list(map(lambda s: s.name, self.states))

    def add_worker_instance(self, worker_instance: PipelineWorkerInstance):
        from_state = worker_instance.from_state
        to_states = worker_instance.to_states
        if from_state not in self._get_state_names():
            raise RuntimeError(f"For pipeline {self.name} {from_state} is not (yet) a valid state")
        for to_state in to_states:
            if to_state not in self._get_state_names():
                raise RuntimeError(f"For pipeline {self.name} {to_state} is not (yet) a valid state")
        self.worker_instances.append(worker_instance)
        if from_state not in self._graph_adj_list:
            self._graph_adj_list[from_state] = []
        self._graph_adj_list[from_state] += list(to_states)

    def add_mod_view(self, mod_view: PipelineModView):
        from_state = mod_view.from_state
        to_states = mod_view.to_states
        if from_state not in self._get_state_names():
            raise RuntimeError(f"For pipeline {self.name} {from_state} is not (yet) a valid state")
        for to_state in to_states:
            if to_state not in self._get_state_names():
                raise RuntimeError(f"For pipeline {self.name} {to_state} is not (yet) a valid state")
        self.mod_views.append(mod_view)
        if from_state not in self._graph_adj_list:
            self._graph_adj_list[from_state] = []
        self._graph_adj_list[from_state] += list(to_states)

    def assert_pipeline_is_dag(self):
        discovered = set()  # type: Set[str]
        visiting = set()  # type: Set[str]

        def has_cycle(state_name: str) -> bool:
            discovered.add(state_name)
            visiting.add(state_name)
            for to_state in self._graph_adj_list.get(state_name, []):
                if to_state not in discovered:
                    if has_cycle(to_state):
                        return True
                elif to_state in visiting:
                    return True
            visiting.remove(state_name)
            return False

        if not self.starting_state:
            raise RuntimeError(f"Pipeline {self.name} does not have a starting state")
        if has_cycle(self.starting_state.name):
            raise RuntimeError(f"Pipeline {self.name} has a cycle")

        undiscovered = set(self._get_state_names()) - discovered
        if undiscovered:
            raise RuntimeError(f"States {', '.join(undiscovered)} are undiscovered")

    def assert_valid_state_migrations(self, content_store: ContentStore, migration_batch: int = 50):
        # quickly check count first
        # if sum of all state docs doesn't match total count then it has to be invalid
        sum_migrated_count = 0
        for state in self.states:
            sum_migrated_count += content_store.count(state.migrate_q)
        if sum_migrated_count != content_store.count({}):
            raise RuntimeError("Sum of all state docs does not match total count")

        # check if there is overlap in state docs
        # combined with the check that count matches, it means
        # every item in content store belongs to one and only one state
        # and all items in content store are accounted for
        doc_ids = set()
        for state in self.states:
            state_name = state.name
            migrate_q = state.migrate_q
            migrated_count = content_store.count(state.migrate_q)
            migration_batches = migrated_count // migration_batch

            for i in range(migration_batches):
                print(f"Checking pipeline {self.name} state {state_name} migration batch {i + 1}/{migration_batches}")
                for doc in content_store.query(migrate_q, skip=i * migration_batch, limit=migration_batch):
                    doc_id = doc['_id']
                    if doc_id in doc_ids:
                        raise RuntimeError(f"Document with id {doc_id} is duplicated across state migrations")
                    doc_ids.add(doc_id)

            print(f"Checking pipeline {self.name} state {state_name} last migration batch")
            for doc in content_store.query(migrate_q, skip=migration_batches * migration_batch):
                doc_id = doc['_id']
                if doc_id in doc_ids:
                    raise RuntimeError(f"Document with id {doc_id} is duplicated across state migrations")
                doc_ids.add(doc_id)

    def perform_state_migrations(self, content_store: ContentStore):
        for state in self.states:
            print(f"Migrating pipeline {self.name} state {state}")
            filter_q = {**state.migrate_q, **{
                StateKey: {
                    "$exists": False
                }
            }}
            content_store.update_many(
                filter_q=filter_q,
                update_doc={
                    "$set": {
                        StateKey: state.name
                    }
                }
            )
