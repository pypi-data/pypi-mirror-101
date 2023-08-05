# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, Optional
import copy
import platform
import uuid

from azureml import telemetry
from azureml.core import Run
from azureml.core import __version__ as version
from azureml.telemetry.contracts import (RequiredFields, StandardFields, Event)
from azureml.automl.core.shared._diagnostics.automl_events import AutoMLBaseEvent
from azureml.automl.core.shared._diagnostics.automl_event_extension_fields import AutoMLExtensionFields


class EventLogger:
    def __init__(self, extension_fields_dict: Dict[str, Any], run: Optional[Run] = None):
        """
        Init an event logger class. Event logger intends for using certain events in AutoML. The event name should be
        a strictly constant string without any user PII. Some of the standard fields are part B in cold path schema
        which will log only as allowed in the ColdPath DB for longer retention.

        :param extension_fields_dict: a list of the key/value pairs which will be logged in event extensions.
        :param run: An AzureML run.
        """
        if run is None:
            run = Run.get_context()
        if run.experiment is None or run.experiment.workspace is None:
            workspace_id = None
            subscription_id = None
            location = None
        else:
            workspace_id = run.experiment.workspace._workspace_id
            subscription_id = run.experiment.workspace.subscription_id
            location = run.experiment.workspace.location

        self._req = RequiredFields(
            client_type='SDK', client_version=version, component_name='automl', correlation_id=str(uuid.uuid4()),
            subscription_id=subscription_id, workspace_id=workspace_id)
        self._std = StandardFields(
            client_os=platform.system(), run_id=run.id,
            parent_run_id=run.parent.id if run.parent is not None else None,
            workspace_region=location)
        self._ext = AutoMLExtensionFields(
            **(extension_fields_dict if extension_fields_dict is not None else {})).sanitized_fields
        self._logger = telemetry.get_event_logger()

    def log_event(self, automl_event: AutoMLBaseEvent) -> None:
        """
        Log the automl event.

        :param automl_event: The AutoMLBaseEvent.
        """
        if not isinstance(automl_event, AutoMLBaseEvent):
            return

        ext = copy.deepcopy(self._ext)
        std = copy.deepcopy(self._std)
        std.task_result = automl_event.task_result
        std.failure_reason = automl_event.failure_reason
        ext.update(automl_event.extension_fields)
        event = Event(
            name=automl_event.event_name,
            required_fields=self._req,
            standard_fields=std,
            extension_fields=ext
        )
        self._logger.log_event(event)

    def flush(self):
        """Flush the logger."""
        self._logger.flush()
