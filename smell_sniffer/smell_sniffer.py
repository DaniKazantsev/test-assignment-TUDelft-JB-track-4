import argparse
import typing as tp
import json

from otel_trace.trace import Trace
from detectors.issue_detector_base import IssueDetectorBase
from detectors.multiple_issues_detector import MultipleIssueDetector
from detectors.n_plus_one_query import NPlusOneQueryDetector
from detectors.http_error_detector import HTTPErrorDetector
from detectors.warning_detector import WarningDetector
from detectors.exception_detector import ExceptionDetector

USE_HTTP_ERROR_CHECKER_DEFAULT=True
USE_WARNINGS_CHECKER_DEFAULT=True
USE_EXCEPTIONS_CHECKER_DEFAULT=True

def build_checkers(n_plus_one_query_cfg_path: tp.Optional[str], 
                   use_http_error_checker=USE_HTTP_ERROR_CHECKER_DEFAULT, 
                   use_warnings_checker=USE_WARNINGS_CHECKER_DEFAULT,
                   use_exceptions_checker=USE_EXCEPTIONS_CHECKER_DEFAULT) -> IssueDetectorBase:
    checkers = []
    
    if n_plus_one_query_cfg_path is not None:
        with open(n_plus_one_query_cfg_path) as cfg_file:
            n_plus_one_query_cfg = json.loads(cfg_file.read())
        checkers.append(NPlusOneQueryDetector(**n_plus_one_query_cfg))
    
    if use_http_error_checker is True:
        checkers.append(HTTPErrorDetector("[HTTPERROR]"))
        
    if use_warnings_checker is True:
        checkers.append(WarningDetector("[WARNING]"))
        
    if use_exceptions_checker is True:
        checkers.append(ExceptionDetector("[EXCEPTION]"))
    
    return MultipleIssueDetector("[DETECTORS]", checkers)
        

def find_code_issues(traces_path: str, 
                     n_plus_one_query_cfg_path: tp.Optional[str],
                     use_http_error_detector: bool,
                     use_warnings_detector: bool,
                     use_exceptions_detector: bool) -> str:
    checkers = build_checkers(n_plus_one_query_cfg_path, 
                              use_http_error_detector,
                              use_warnings_detector,
                              use_exceptions_detector)
    
    with open(traces_path) as json_file:
        data = json_file.read()
        trace = Trace(data)
        
    return checkers.check_trace(trace)


if __name__ == '__main__':
    description = ('''Detect performance issues, anomalies, bugs, code or architectural smells using runtime information.
                   ''')
    parser = argparse.ArgumentParser(prog='Smell sniffer.',
                    description=description)
    parser.add_argument("traces_path", help="Path of traces.")
    parser.add_argument("--n-plus-one-query-cfg", help="Path for n plus one query detector configuration.", default=None, required=False)
    parser.add_argument("--use-http-error-detector", help="Use http error detector or not.", type=bool, default=True, required=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--use-warnings-detector", help="Use warning detector or not.", type=bool, default=True, required=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--use-exceptions-detector", help="Use exception detector or not.", type=bool, default=True, required=False, action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    result = find_code_issues(args.traces_path, 
                              args.n_plus_one_query_cfg, 
                              args.use_http_error_detector,
                              args.use_warnings_detector,
                              args.use_exceptions_detector
                              )
    
    for issues_by_type in result:
        for issue in issues_by_type:
            print(issue)
