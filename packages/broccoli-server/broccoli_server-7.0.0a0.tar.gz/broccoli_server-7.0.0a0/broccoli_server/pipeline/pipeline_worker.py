import abc
import dataclasses
from typing import List, Dict, Set, Optional, Callable
from bson import ObjectId
from broccoli_server.interface.worker import Worker, WorkContext

StateKey = '_state'


class PipelineWorker(Worker, abc.ABC):
    def __init__(self, pipeline_name: str, from_state: str, to_states: Set[str], limit: Optional[int],
                 sort: Optional[Dict]):
        self.pipeline_name = pipeline_name
        self.from_state = from_state
        self.to_states = to_states
        self.limit = limit
        self.sort = sort

    def get_id(self) -> str:
        return f"{self.pipeline_name}.{self.from_state}.{'|'.join(sorted(self.to_states))}"

    @abc.abstractmethod
    def pre_work(self, context: WorkContext):
        pass

    def work(self, context: WorkContext):
        from_state_documents = context.content_store().query(
            q={
                StateKey: self.from_state
            },
            limit=self.limit,
            sort=self.sort
        )
        if not from_state_documents:
            context.logger().info(f"No item in {self.from_state} state")
            return

        results = self.process(context, from_state_documents)
        for to_state, to_state_document_ids in results.items():
            self.transition_state(context, to_state, to_state_document_ids)

    def transition_state(self, context: WorkContext, to_state: str, to_state_document_ids: List[str]):
        if to_state not in self.to_states:
            context.logger().error(f"{to_state} is not a designated terminal state")
            return
        context.logger().info(f"Transitioning {len(to_state_document_ids)} item(s) to {to_state} state")
        context.content_store().update_many(
            filter_q={
                "_id": {"$in": list(map(lambda i: ObjectId(i), to_state_document_ids))}
            },
            update_doc={
                "$set": {
                    StateKey: to_state
                }
            }
        )

    @abc.abstractmethod
    def process(self, context: WorkContext, documents: List[Dict]) -> Dict[str, List[str]]:
        pass


@dataclasses.dataclass
class PipelineWorkerInstance:
    clazz: Callable
    extra_args: Dict
    from_state: str
    to_states: Set[str]
    limit: Optional[int] = None
    sort: Optional[Dict] = None
