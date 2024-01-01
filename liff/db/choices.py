from enum import IntEnum, StrEnum


class AttendanceType(IntEnum):
    leave = 1
    exchange = 2
    overtime = 3
    parent_leave = 4


class LeaveType(StrEnum):
    annual = "annual"
    sick = "sick"
    personal = "personal"
