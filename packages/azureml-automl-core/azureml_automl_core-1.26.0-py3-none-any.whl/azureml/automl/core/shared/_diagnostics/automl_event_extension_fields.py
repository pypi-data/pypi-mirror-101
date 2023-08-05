# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""All the allowlist for AutoML extension fields dict."""
from typing import Any, Dict, List, cast
from collections import defaultdict
import re

from azureml.telemetry.contracts._extension_fields import ExtensionFieldKeys, ExtensionFields


class AutoMLExtensionFieldKeys(ExtensionFieldKeys):
    """All the allowed keys in AutoML events extension fields are defined here."""
    SESSION_ID_KEY = "SessionId"

    @classmethod
    def keys(cls) -> List[str]:
        keys_list = super(AutoMLExtensionFieldKeys, cls).keys()
        keys_list.extend([AutoMLExtensionFieldKeys.SESSION_ID_KEY])
        return cast(List[str], keys_list)


class AutoMLExtensionFieldValueValidators:
    """ALl the extension field values validator holds here."""
    VALIDATORS_MAPPING = {
        AutoMLExtensionFieldKeys.MEMORY_USED_KEY: lambda x: isinstance(x, int) or isinstance(x, float),
        AutoMLExtensionFieldKeys.SESSION_ID_KEY: lambda x: AutoMLExtensionFieldValueValidators.is_guid_str(x)
    }

    @staticmethod
    def is_guid_str(input_id: Any) -> bool:
        """Check whether the input is a guid string."""
        if not isinstance(input_id, str):
            return False

        guid_pattern = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
        return guid_pattern.match(input_id) is not None


class AutoMLExtensionFields(ExtensionFields):
    """Defines Part C of the logging event schema in AutoML, keys that can be customized for telemetry data."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a new instance of the ExtensionFields."""
        super(AutoMLExtensionFields, self).__init__(*args, **kwargs)

    @property
    def sanitized_fields(self) -> Dict[str, Any]:
        """Get all the fields with values that allowed for the event logger."""
        return {
            k: v for k, v in self.items()
            if AutoMLExtensionFieldValueValidators.VALIDATORS_MAPPING.get(k, lambda x: False)(v)
        }
