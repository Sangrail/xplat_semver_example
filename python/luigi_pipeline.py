import luigi
import subprocess
from version import __version__

class RunCppProgram(luigi.Task):
    def output(self):
        return luigi.LocalTarget('/app/output.txt')

    def run(self):
        result = subprocess.run(["/app/hello_cpp"], capture_output=True, text=True)
        with self.output().open('w') as f:
            f.write(result.stdout)

class PrintCppOutput(luigi.Task):
    def requires(self):
        return RunCppProgram()

    def run(self):
        with self.input().open('r') as f:
            output = f.read()
            print(output)
            print(f"Python Version: {__version__}")

    def output(self):
        return luigi.LocalTarget('/app/print_done.txt')

if __name__ == "__main__":
    luigi.build([PrintCppOutput()], local_scheduler=True)