from monosi.monitors.analyzer import Analyzer
from monosi.monitors.compiler import Compiler
from monosi.monitors.runner import Runner
from .base import ProjectTask, TaskBase

class RunMonitorTask(TaskBase):
    def __init__(self, args, config, monitor, compiler, runner, analyzer):
        super().__init__(args, config)
        self.monitor = monitor
        self.compiler = compiler
        self.runner = runner
        self.analyzer = analyzer

    def _run_monitor(self):
        sql_stmt = self.compiler.compile(self.monitor)
        sql_results = self.runner.run(sql_stmt)
        analysis = self.analyzer.analyze(monitor=self.monitor, results=sql_results)

        return (sql_results, analysis)

    def run(self, *args, **kwargs):
        reporter = self.config.reporter

        reporter.monitor_started(self.monitor)
        (sql_results, analysis) = self._run_monitor()
        reporter.monitor_finished(self.monitor)

        return (sql_results, analysis)

class MonitorsTask(ProjectTask):
    def __init__(self, args, config):
        super().__init__(args, config)

    def _driver(self):
        try:
            from monosi.drivers.factory import load_driver
            driver_config = self.config.config
            driver_cls = load_driver(driver_config)

            return driver_cls(self.config)
        except:
            raise Exception("Could not initialize connection to database in runner.")
        
    def _create_tasks(self):
        if self.project is None:
            raise Exception("Project was not loaded before running monitors.")

        driver = self._driver()
        compiler = Compiler(
            dialect=driver.dialect, 
            metadata=driver.metadata()
        )
        runner = Runner(self.config)
        analyzer = Analyzer(self.config.reporter)

        tasks = []
        for monitor in self.project.monitors:
            task = RunMonitorTask(
                args=self.args,
                config=self.config,
                monitor=monitor,
                compiler=compiler,
                runner=runner,
                analyzer=analyzer,
            )
            tasks.append(task)

        return tasks

    def _process_tasks(self):
        results = [task.run() for task in self.task_queue]
        return results
