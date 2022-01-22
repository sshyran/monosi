from typing import Type

from monosi.monitors.types.base import Monitor, MonitorType
from monosi.monitors.types.custom import CustomMonitor
from monosi.monitors.types.table import TableMonitor
from monosi.monitors.types.schema import SchemaMonitor

def load_monitor_cls(monitor_dict) -> Type[Monitor]:
    type_raw = monitor_dict.get('type')
    monitor_type = MonitorType(type_raw)

    if monitor_type == MonitorType.TABLE:
        return TableMonitor
    elif monitor_type == MonitorType.CUSTOM:
        return CustomMonitor
    elif monitor_type == MonitorType.SCHEMA:
        return SchemaMonitor

    # Note: Unreachable - we would error at MonitorType instantiation
    raise Exception("Could not find a moniotr with type: {}".format(type_raw))
