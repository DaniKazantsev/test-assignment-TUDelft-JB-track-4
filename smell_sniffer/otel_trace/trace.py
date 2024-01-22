from otel_trace.span import Span
import typing as tp
import json

def get_main_span(spans: tp.Dict[str, tp.Dict]) -> str:
    """
    Identify the main span in a collection of spans.

    The main span is assumed to be the one that has no parent.

    Args:
    spans (Dict[str, Dict]): A dictionary of spans with span IDs as keys and span data as values.

    Returns:
    str: The ID of the main span.
    """
    for span_id, span_data in spans.items():
        if not any(ref.get('spanID') == span_id for ref in span_data.get('references', [])):
            return span_id
    return None

def get_children_by_parent(spans: tp.Dict[str, tp.Dict]) -> tp.Dict[str, tp.List[str]]:
    """
    Create a mapping of parent spans to their child spans.

    Args:
    spans (Dict[str, Dict]): A dictionary of spans with span IDs as keys and span data as values.

    Returns:
    Dict[str, List[str]]: A dictionary mapping parent span IDs to lists of their child span IDs.
    """
    child_by_parent = {}
    for span_id, span_data in spans.items():
        for ref in span_data.get('references', []):
            if ref.get('refType') == 'CHILD_OF':
                parent_id = ref.get('spanID')
                if parent_id not in child_by_parent:
                    child_by_parent[parent_id] = []
                child_by_parent[parent_id].append(span_id)
    return child_by_parent    

class Trace:
    """
    Represents a trace consisting of multiple spans.

    Attributes:
    main_span (Span): The main span of the trace.
    """
    def __init__(self, json_string):
        """
            Initialize a Trace object from a JSON string.

            This method parses the JSON string, validates its structure, and initializes the Trace object
            with the main span and a mapping of parent spans to their child spans.

            Args:
            json_string (str): A JSON-formatted string representing the trace data.

            Raises:
            ValueError: If the JSON string does not contain the expected structure.
            AssertionError: If the 'data' field in the JSON string does not contain exactly one trace.
        """
        trace = json.loads(json_string)
        
        def get_value(input_trace, value, where='trace'):
            if value not in input_trace:
                raise ValueError(f"No {value} in input {where}.")
            
            return input_trace[value]
        
        self.total = get_value(trace, 'total')
        self.limit = get_value(trace, 'limit')
        self.offset = get_value(trace, 'offset')
        self.errors = get_value(trace, 'errors')

        data = get_value(trace, 'data')
        
        assert len(data) == 1, "Data lenght is not equal to 1"
        
        trace = data[0]
        self.trace_id = get_value(trace, 'traceID', 'trace/data')
        spans = get_value(trace, 'spans', 'trace/data')
        
        spans = {get_value(span, 'spanID', 'span'): span for span in spans}
        
        parent_span: str = get_main_span(spans)
        child_by_parent: tp.Dict[str, tp.List[str]] = get_children_by_parent(spans)
        self.main_span = Span(spans, parent_span, child_by_parent)
    
    @property
    def get_main_span(self):
        return self.main_span
