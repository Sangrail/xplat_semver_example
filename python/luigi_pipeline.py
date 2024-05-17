import luigi
import subprocess
from version import __version__
from opentelemetry_setup import setup_opentelemetry

tracer = setup_opentelemetry()

class RunCppProgram(luigi.Task):
    def output(self):
        return luigi.LocalTarget('/app/output.txt')

    def run(self):
        with tracer.start_as_current_span("RunCppProgram"):
            result = subprocess.run(["/app/hello_cpp"], capture_output=True, text=True)
            with self.output().open('w') as f:
                f.write(result.stdout)

class PrintCppOutput(luigi.Task):
    def requires(self):
        return RunCppProgram()

    def run(self):
        with tracer.start_as_current_span("PrintCppOutput"):
            with self.input().open('r') as f:
                output = f.read()
                print(output)
                print(f"Python Version: {__version__}")

    def output(self):
        return luigi.LocalTarget('/app/print_done.txt')

if __name__ == "__main__":
    with tracer.start_as_current_span("LuigiPipeline"):
        luigi.build([PrintCppOutput()], local_scheduler=True)