from enum import IntEnum


class AttendanceType(IntEnum):
    leave = 1
    exchange = 2
    overtime = 3
    parent_leave = 4


class LeaveType(IntEnum):
    annual = 1
    sick = 2
    personal = 3
