from dataclasses import dataclass
from typing import Any, List
from monosi.config.configuration import Configuration
from monosi.drivers.column import Table

from monosi.monitors.types.table import TableMonitor
from monosi.drivers.dialect import Dialect
from monosi.monitors.types.base import Monitor
from monosi.monitors.types.metrics import MetricBase
from monosi.monitors.types.custom import CustomMetric
from monosi.monitors.types.table import ColumnMetric, ColumnMetricType

@dataclass
class Compiler:
    dialect: Dialect
    metadata: Any

    def compile_metric(self, metric: MetricBase):
        return metric.compile(self.dialect)

    def compile_select(self, metrics: List[MetricBase]):
        select_body = []
        for metric in metrics:
            metric_sql = self.compile_metric(metric)
            select_body.append(metric_sql)

        return ",\n\t".join(select_body)

    def _add_cols(self, monitor: TableMonitor):
        tables = Table.from_metadata(self.metadata)
        for table in tables:
            if table.name.lower() in monitor.table:
                monitor.columns = table.columns

    def compile(self, monitor: Monitor):
        if isinstance(monitor, TableMonitor):
            self._add_cols(monitor)

        select_sql = self.compile_select(monitor.retrieve_metrics())
        sql = monitor.base_sql_statement(select_sql)
        
        return sql

