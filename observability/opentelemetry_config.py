import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource.create(attributes={SERVICE_NAME: os.environ.get("TRACES_SERVICE_NAME", "crewforge-api")})


tracerProvider = TracerProvider(resource=resource)
traces_endpoint = os.environ.get("TRACES_ENDPOINT", "http://otel-collector:4318")
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{traces_endpoint}/v1/traces"))
tracerProvider.add_span_processor(processor)
trace.set_tracer_provider(tracerProvider)

instrumentor = DjangoInstrumentor().instrument()
