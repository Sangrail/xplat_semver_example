from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


def setup_opentelemetry():
    resource = Resource(attributes={
        "service.name": "jasons_test_service",
        "service.version": "1.0.0"
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer = trace.get_tracer(__name__)

    console_exporter = ConsoleSpanExporter()
    trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(console_exporter))

    return tracer

tracer = setup_opentelemetry()