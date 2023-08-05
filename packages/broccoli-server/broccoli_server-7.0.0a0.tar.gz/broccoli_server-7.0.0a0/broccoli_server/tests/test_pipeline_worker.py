import datetime
from bson import ObjectId
from typing import List, Dict, Set
from broccoli_server.interface.worker import WorkContext
from broccoli_server.worker.work_context import WorkContextImpl
from broccoli_server.pipeline import PipelineWorker
from .testcase_with_mongomock import TestCaseWithMongoMock


class TestPipelineWorker(TestCaseWithMongoMock):
    def create_demo_worker(self, process, from_state: str, to_states: Set[str]):
        worker_id = "demo_worker"

        class Worker(PipelineWorker):
            def get_id(self) -> str:
                return worker_id

            def pre_work(self, context: WorkContext):
                pass

            def process(self, context: WorkContext, documents: List[Dict]) -> Dict[str, List[str]]:
                return process(context, documents)

        demo_work_context = WorkContextImpl(worker_id, self.content_store, self.metadata_store_factory)
        return Worker("demo", from_state, to_states, None, None), demo_work_context

    def test_all_valid_single_transitions(self):
        now = datetime.datetime.now()
        oid_a = ObjectId.from_datetime(now)
        oid_b = ObjectId.from_datetime(now - datetime.timedelta(seconds=1))
        oid_c = ObjectId.from_datetime(now - datetime.timedelta(seconds=2))
        self.content_store.append({"_id": oid_a, "_state": "state1"}, "_id")
        self.content_store.append({"_id": oid_b, "_state": "state1"}, "_id")
        self.content_store.append({"_id": oid_c, "_state": "state1"}, "_id")

        def process(context, documents):
            return {"state2": [oid_a, oid_b, oid_c]}
        demo_worker, demo_work_context = self.create_demo_worker(process, "state1", {"state2"})
        demo_worker.work(demo_work_context)

        assert self.actual_documents_by_id_desc() == [
            {"_id": oid_a, "_state": "state2"},
            {"_id": oid_b, "_state": "state2"},
            {"_id": oid_c, "_state": "state2"},
        ]

    def test_all_valid_multiple_transitions(self):
        now = datetime.datetime.now()
        oid_a = ObjectId.from_datetime(now)
        oid_b = ObjectId.from_datetime(now - datetime.timedelta(seconds=1))
        oid_c = ObjectId.from_datetime(now - datetime.timedelta(seconds=2))
        self.content_store.append({"_id": oid_a, "_state": "state1"}, "_id")
        self.content_store.append({"_id": oid_b, "_state": "state1"}, "_id")
        self.content_store.append({"_id": oid_c, "_state": "state1"}, "_id")

        def process(context, documents):
            return {"state2": [oid_a, oid_b], "state3": [oid_c]}

        demo_worker, demo_work_context = self.create_demo_worker(process, "state1", {"state2", "state3"})
        demo_worker.work(demo_work_context)

        assert self.actual_documents_by_id_desc() == [
            {"_id": oid_a, "_state": "state2"},
            {"_id": oid_b, "_state": "state2"},
            {"_id": oid_c, "_state": "state3"},
        ]

    def test_invalid_transition(self):
        now = datetime.datetime.now()
        oid_a = ObjectId.from_datetime(now)
        oid_b = ObjectId.from_datetime(now - datetime.timedelta(seconds=1))
        oid_c = ObjectId.from_datetime(now - datetime.timedelta(seconds=2))
        self.content_store.append({"_id": oid_a, "_state": "state1"}, "_id")
        self.content_store.append({"_id": oid_b, "_state": "state1"}, "_id")
        self.content_store.append({"_id": oid_c, "_state": "state1"}, "_id")

        def process(context, documents):
            return {"state2": [oid_a, oid_b], "state3": [oid_c]}

        demo_worker, demo_work_context = self.create_demo_worker(process, "state1", {"state2"})
        demo_worker.work(demo_work_context)

        assert self.actual_documents_by_id_desc() == [
            {"_id": oid_a, "_state": "state2"},
            {"_id": oid_b, "_state": "state2"},
            {"_id": oid_c, "_state": "state1"},
        ]

    def test_no_transition(self):
        now = datetime.datetime.now()
        oid_a = ObjectId.from_datetime(now)
        oid_b = ObjectId.from_datetime(now - datetime.timedelta(seconds=1))
        oid_c = ObjectId.from_datetime(now - datetime.timedelta(seconds=2))
        self.content_store.append({"_id": oid_a}, "_id")
        self.content_store.append({"_id": oid_b}, "_id")
        self.content_store.append({"_id": oid_c}, "_id")

        def process(context, documents):
            return {"state2": [oid_a, oid_b, oid_c]}

        demo_worker, demo_work_context = self.create_demo_worker(process, "state1", {"state2"})
        demo_worker.work(demo_work_context)

        assert self.actual_documents_by_id_desc() == [
            {"_id": oid_a},
            {"_id": oid_b},
            {"_id": oid_c},
        ]
