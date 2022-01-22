from monosi.monitors.analyzer import Analyzer
from monosi.config.configuration import Configuration
from monosi.monitors.compiler import Compiler

class Runner:
    def __init__(self, config: Configuration):
        self.config = config
        self.driver = None

    def _initialize(self):
        try:
            from monosi.drivers.factory import load_driver
            driver_config = self.config.config
            driver_cls = load_driver(driver_config)

            self.driver = driver_cls(self.config)
        except:
            raise Exception("Could not initialize connection to database in runner.")

    def execute(self, sql: str):
        if self.driver is None:
            raise Exception("Initialize runner before execution.")

        results = self.driver.execute_sql(sql)
        return results

    def run(self, sql: str):
        self._initialize()

        return self.execute(sql)

