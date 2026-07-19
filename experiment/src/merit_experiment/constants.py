"""Shared enums and markers for the experiment skeleton."""

USER_APPROVAL_REQUIRED = "USER_APPROVAL_REQUIRED"

RUN_STATUSES = frozenset(
    {
        "PLANNED",
        "READY",
        "RUNNING",
        "SUCCEEDED",
        "FAILED",
        "ABORTED",
        "INVALID",
        "BLOCKED",
    }
)

FAILURE_TYPES = frozenset(
    {
        "NONE",
        "CONFIGURATION",
        "DATA_INTEGRITY",
        "ROLE_LEAKAGE",
        "ENVIRONMENT",
        "IMPLEMENTATION",
        "RESOURCE",
        "METRIC",
        "EXTERNAL",
        USER_APPROVAL_REQUIRED,
        "UNKNOWN",
    }
)

PILOT_ROLES = frozenset({"pilot_train", "pilot_audit"})
CONFIRMATORY_ROLES = frozenset(
    {"fit", "calibration", "development", "sealed_final_audit"}
)

EXECUTABLE_STATUSES = frozenset({"READY", "RUNNING", "SUCCEEDED", "FAILED", "ABORTED"})

