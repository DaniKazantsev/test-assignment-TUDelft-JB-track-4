import typing as tp
from otel_trace.trace import Trace
from otel_trace.span import Span

from detectors.issue_detector_base import IssueBase, IssueDetectorBase


class NPlusOneQueryIssue(IssueBase):
    """
    Represents an N+1 query issue identified within a span.

    This issue indicates that a large number of similar database queries were made in a short period,
    potentially indicating inefficient querying patterns.

    Attributes:
    duration_involved_spans (float): The total duration of all spans involved in the N+1 issue.
    count_involved_spans (int): The count of spans involved in the N+1 issue.
    """
    def __init__(self, span, duration_involved_spans, count_involved_spans, name):
        super().__init__(span, name)
        self.duration_involved_spans = duration_involved_spans
        self.count_involved_spans = count_involved_spans

    def __str__(self):
        return f"{self.name} found with duration: {self.duration_involved_spans}ms and count {self.count_involved_spans} in {super().__str__()}"

class NPlusOneQueryDetector(IssueDetectorBase):
    """
    Detector class for identifying N+1 query issues in traces.

    This detector looks for patterns where a large number of similar database queries are executed 
    in a short period, which is a common performance anti-pattern.

    Attributes:
    duration_involved_spans_thrsh (float): Threshold for total duration of spans to consider as an N+1 issue.
    count_involved_spans_thrsh (int): Threshold for the count of spans to consider as an N+1 issue.
    """
    def __init__(self, name: str, duration_involved_spans_thrsh, count_involved_spans_thrsh):
        super().__init__(name)
        self.duration_involved_spans_thrsh = duration_involved_spans_thrsh
        self.count_involved_spans_thrsh = count_involved_spans_thrsh
        
    def check_trace(self, trace: Trace):
        self.check_span(trace.get_main_span)
        return self.issues
        
    def check_span(self, span: Span):
        if span.is_tags_key_eq_to_statment("db.statement"):
            return span.get('duration'), 1
        
        children_info = [self.check_span(child_span) for child_span in span.children] # (danik) use multiprocessing here
        total_duration, total_count = sum(pair[0] for pair in children_info) or 0, sum(pair[1] for pair in children_info) or 0

        if (total_duration > self.duration_involved_spans_thrsh
            and total_count > self.count_involved_spans_thrsh):
            self.issues.append(NPlusOneQueryIssue(span, total_duration, total_count, self.name))
            return 0, 0

        return total_duration, total_count