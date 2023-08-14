import datetime, os, sys

from osprey.server.lib.globus_compute import register_function
from globus_sdk import TimerClient
from globus_sdk import TimerJob
from globus_sdk.utils import slash_join
from osprey.server.lib.error import ServiceError, FLOW_TIMER_ERROR
from globus_sdk import SpecificFlowClient
from osprey.server.lib.globus_flow import create_authorizer
from enum import IntEnum
from osprey.server.config import Config

class FlowEnum(IntEnum):
    NONE              = 0
    VERIFY_OR_MODIFY  = 1
    VERIFY_AND_MODIFY = 2

# PERMANENT
FLOW_IDS = {
    FlowEnum.NONE: 'ad25e819-ec70-4d30-aaad-a828447da332',
    FlowEnum.VERIFY_OR_MODIFY: ''
}

def set_timer(interval_in_sec: int, id: int, flow_type: FlowEnum) -> None:
    """Set a Globus Timer for daily retrieval of updated tables from sources.

    Arguments:
        func_uuid: The Globus Compute registered function UUID.
    """
    flow_id       = FLOW_IDS[flow_type]

    # client, sfc, timer_scope = create_context(_FLOW_UUID)
    sfc = SpecificFlowClient(flow_id=flow_id)
    authorizer, specific_flow_scope = create_authorizer(flow_id)
    timer_client = TimerClient(authorizer=authorizer, app_name="osprey-prototype")

    run_input = {
                    "osprey-worker-endpoint": Config.GLOBUS_WORKER_UUID,
                    "download-function": Config.GLOBUS_FLOW_DOWNLOAD_FUNCTION, 
                    "database-commit-function": Config.GLOBUS_FLOW_COMMIT_FUNCTION,
                    "tasks": [{
                        "endpoint": Config.GLOBUS_WORKER_UUID,
                        "function": Config.GLOBUS_FLOW_DOWNLOAD_FUNCTION,
                        "kwargs": {
                        "source_id": id
                        }}]
                    }

    run_label = f"Osprey Demo | Source {id}"

    url = slash_join(sfc.base_url, f"/flows/{flow_id}/run")

    job = TimerJob(
        callback_url=url,
        callback_body={"body": run_input, "label": run_label},
        start=datetime.datetime.utcnow(),
        interval=datetime.timedelta(seconds=interval_in_sec),
        name=f"osprey-demo-source-{id}",
        scope=specific_flow_scope,
    )

    response = timer_client.create_job(job)
    assert response.http_status == 201
    job_id = response["job_id"]
    return job_id

if __name__ == "__main__":
    flow_id = FLOW_IDS[FlowEnum.NONE]
    create_authorizer(flow_id)