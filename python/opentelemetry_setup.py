import logging
import os
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Load environment variables from .env file
load_dotenv()

def setup_opentelemetry():
    resource = Resource(attributes={
        "service.name": "jasons_test_service",
        "service.version": "1.0.0"
    })

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

    return tracer

tracer = setup_opentelemetry()
