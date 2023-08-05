# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The base class to hold all the AutoML events."""
from typing import Any, Dict, Optional

from azureml.telemetry.contracts._standard_fields import TaskResult, FailureReason
from azureml.automl.core.shared._diagnostics.automl_event_extension_fields import AutoMLExtensionFields
from azureml.automl.core.shared._diagnostics.automl_event_names import AutoMLEventNames
from azureml.automl.core.shared._error_response_constants import ErrorCodes
from azureml.automl.core.shared.utilities import get_error_code


class AutoMLBaseEvent:
    """Base class for all automl events."""
    def __init__(
            self,
            event_name: str,
            task_result: Optional[str] = None,
            extension_fields_dict: Optional[Dict[str, Any]] = None,
            exception: Optional[Exception] = None
    ):
        """
        :param event_name: Name of the event.
        :param task_result: The task result.
        :param extension_fields_dict: Extension fields dict.
        :param exception: The exception for the failure event.
        """
        self._event_name = event_name if event_name in AutoMLEventNames.ALL_EVENT_NAMES \
            else AutoMLEventNames.AUTOML_BASE_EVENT
        self._extension_fields = AutoMLExtensionFields(
            **(extension_fields_dict if extension_fields_dict is not None else {}))

        self._task_result = task_result if task_result in TaskResult else TaskResult.Others

        self._failure_reason = None
        if exception is not None and ErrorCodes.USER_ERROR in get_error_code(exception, as_hierarchy=True):
            self._failure_reason = FailureReason.UserError
        elif self._task_result == TaskResult.Failure:
            self._failure_reason = FailureReason.SystemError

    @property
    def event_name(self) -> str:
        """
        The event name which should be defined in azureml.automl.core.shared._diagnostics.automl_event_names.
        """
        return self._event_name

    @property
    def task_result(self) -> Optional[str]:
        """
        The task result which can be None or defined in azureml.telemetry.contracts._standard_fields.TaskResult.
        """
        return self._task_result

    @property
    def failure_reason(self) -> Optional[str]:
        """
        The task result which can be None or defined in azureml.telemetry.contracts._standard_fields.FailureReason.
        """
        return self._failure_reason

    @property
    def extension_fields(self) -> Dict[str, Any]:
        """
        The extension fields for this event which are defined in
            azureml.automl.core.shared._diagnostics.automl_event_extension_fields.
        """
        return self._extension_fields.sanitized_fields
