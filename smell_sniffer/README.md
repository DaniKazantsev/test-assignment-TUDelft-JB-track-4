## 👋 About
Smell snifer is python3 tool for analytics of traces coolected by OpenTelemetry.

It can detect issues:
1. N+1 query issue
2. Exceptions
3. Warnings
4. Http errors

## Get started
Just run the ```smell_sniffer.py``` with the path of .json file with traces and with path to config of n+1 query detector. Then

```python3 smell_sniffer/smell_sniffer.py trace_exploration/traces/trace_generate_pairs_with_error.json  --n-plus-one-query-cfg smell_sniffer/configs/n_plus_one_query_cfg.json```

There is also possible to disables different detectors with kwargs.

## How to improve
1. Implement other issues detectors
2. Improve already written detectors. For example, Exception detector detects exception in parent span, already detected in child ones, because of percularities of OTel traces. It can be improved in the way like it is done in n+1 queries.

## What is with ML?
I have not found any pre-trained models for this task on the internet. However, I did try asking ChatGPT from OpenAI about issues in a .json file, and it provided the date in the requested format. Despite this, there were some inaccuracies, so I decided not to implement an API request to ChatGPT. Nonetheless, pursuing this path presents a good opportunity to develop the tool further.

## Joke 
While working on your task, I came across a joke and hope you might find it funny if you understand Russian: "Ты с какого района, check_span()?". This phrase is similar to a famous line from a popular TV series about teenagers in the USSR, and it means, "Where are you from, guy?"