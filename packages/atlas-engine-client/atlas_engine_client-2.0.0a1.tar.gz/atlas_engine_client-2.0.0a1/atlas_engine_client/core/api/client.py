
from typing import Callable, List

from requests.models import Response

from .helpers.application_info import ApplicationInfo, ApplicationInfoHandler
from .helpers.external_tasks import FetchAndLockRequestPayload, ExternalTask, ExternalTaskHandler, FinishExternalTaskRequestPayload
from .helpers.process_instances import ProcessInstanceHandler
from .helpers.process_models import ProcessStartRequest, ProcessStartResponse, ProcessModelHandler

class Client(object):

    def __init__(self, url: str, identity: Callable=None):
        self._url = url
        self._identity = identity

    def info(self) -> ApplicationInfo:
        handler = ApplicationInfoHandler(self._url, self._identity)

        application_info = handler.info()

        return application_info

    def authority(self) -> str:
        handler = ApplicationInfoHandler(self._url, self._identity)

        authority = handler.authority()

        return authority

    def process_model_start(self, process_model_id: str, request: ProcessStartRequest, options: dict={}) -> ProcessStartResponse:
        handler = ProcessModelHandler(self._url, self._identity)

        response = handler.start(process_model_id, request)

        return response

    def external_task_fetch_and_lock(self, request: FetchAndLockRequestPayload) -> List[ExternalTask]:
        handler = ExternalTaskHandler(self._url, self._identity)

        reponse = handler.fetch_and_lock(request)

        return reponse

    def external_task_finish(self, external_task_id: str, request: FinishExternalTaskRequestPayload, options: dict={}):
        handler = ExternalTaskHandler(self._url, self._identity)

        response = handler.finish(external_task_id, request, options)

        return response
    
    def process_instance_terminate(self, process_instance_id: str, options: dict={}):
        handler = ProcessInstanceHandler(self._url, self._identity)

        response = handler.terminate(process_instance_id, options)

        return response 
