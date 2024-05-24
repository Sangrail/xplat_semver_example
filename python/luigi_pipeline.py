import atexit
import logging
import os
import subprocess
import time
import luigi
from dotenv import load_dotenv

from version import __version__

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter

load_dotenv()

def setup_opentelemetry():
    resource = Resource(attributes={
        "service.name": "jasons_test_service",
        "service.version": "1.0.0"
    })

    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter(insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    logging.getLogger().addHandler(handler)

    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer = trace.get_tracer(__name__)

    # Console exporter for local debugging
    console_exporter = ConsoleSpanExporter()
    trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(console_exporter))

    # Remote OTEL exporter setup for New Relic
    api_key = os.getenv("OTEL_API_KEY")
    headers = (
        ("api-key", api_key),
    )

    endpoint = os.getenv("OTEL_ENDPOINT")

    otlp_exporter = OTLPSpanExporter(
        endpoint=endpoint,
        headers=headers,
        insecure=False
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

    return tracer, logging

tracer, logging = setup_opentelemetry()

class RunCppProgram(luigi.Task):
    def output(self):
        return luigi.LocalTarget('/app/output.txt')

    def run(self):
        with tracer.start_as_current_span("RunCppProgram") as span:
            span.add_event("Calling a c++ executable")

            result = subprocess.run(["/app/hello_cpp"], capture_output=True, text=True)
            with self.output().open('w') as f:
                f.write(result.stdout)

            time.sleep(10)

            span.add_event("Called a c++ executable")
            logging.error("Failed too complete RunnCppProgram")

class PrintCppOutput(luigi.Task):
    def requires(self):
        return RunCppProgram()

    def run(self):
        with tracer.start_as_current_span("PrintCppOutput") as span:
            span.add_event("PrintFile")
            with self.input().open('r') as f:
                span.add_event("ReadFile")
                output = f.read()
                print(output)
                print(f"Python Version: {__version__}")

            time.sleep(30)

            span.add_event("PrintedFile")

        logging.info("Completed PrintCppOutput")

    def output(self):
        return luigi.LocalTarget('/app/print_done.txt')
    
def main():

    with tracer.start_as_current_span("LuigiPipeline") as span:
        span.set_attribute("luigi.version", luigi.__version__)
        span.set_attribute("python.app.version", __version__)
        span.set_attribute("app.name", "luigi-pipeline")

        span.add_event("Pipeline started")
        
        luigi.build([PrintCppOutput()], local_scheduler=True)

        span.add_event("Pipeline completed")

if __name__ == "__main__":
    main()