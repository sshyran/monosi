import os
from monosi.drivers.column import Table

from monosi.monitors.types.schema import SchemaMonitor
from monosi.monitors.types.table import TableMonitor
import monosi.utils.yaml as yaml

BOOTSTRAPPED_MONITOR_PATH = './bootstrapped-monitors'
class Profiler:
    def __init__(self, config):
        self.config = config

    def _retrieve_tables(self):
        from monosi.drivers.factory import load_driver
        driver_cls = load_driver(self.config.config)
        driver = driver_cls(self.config)

        metadata = driver.metadata()
        return Table.from_metadata(metadata)

    def _create_definitions(self):
        definitions = []

        tables = self._retrieve_tables()
        for table in tables:
            try:
                table_monitor = TableMonitor(
                    table=table.name,
                    timestamp_field=table.timestamp().name,
                )
                schema_monitor = SchemaMonitor(
                    table=table.name,
                    columns=table.columns
                )
                definition = {
                    'monosi': {
                        'monitors': [
                            table_monitor.to_dict(),
                            schema_monitor.to_dict(),
                        ]
                    }
                }
                definitions.append(definition)
            except:
                pass
                # logging.warn("Timestamp field could not be found for table")

        return definitions

    def _write_definition(self, definition, monitors_dir=BOOTSTRAPPED_MONITOR_PATH):
        database = definition['monosi']['monitors'][0]['table'].split('.')[0]
        schema = definition['monosi']['monitors'][0]['table'].split('.')[1]
        table = definition['monosi']['monitors'][0]['table'].split('.')[2]

        monitor_path = os.path.join(monitors_dir, database, schema)
        if not os.path.exists(monitor_path):
            os.makedirs(monitor_path)

        path = os.path.join(monitor_path, table + '.yml')
        if not os.path.exists(path):
            yaml.write_file(path, definition)

    def _persist_definitions(self, definitions):
        if not os.path.exists(BOOTSTRAPPED_MONITOR_PATH):
            os.makedirs(BOOTSTRAPPED_MONITOR_PATH)
        self.config.add_monitor_path(BOOTSTRAPPED_MONITOR_PATH)

        for definition in definitions:
            self._write_definition(definition)

    def profile(self):
        definitions = self._create_definitions()
        # TODO: validate definitions
        self._persist_definitions(definitions)


