import pandas as pd
import json


def read_traces(file):
    with open(file) as f:
        trace_data = json.load(f)
        return pd.DataFrame(trace_data['data'][0]['spans'])


if __name__ == "__main__":
    df = read_traces("./traces/trace_generate_pairs_with_error.json")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df.head())
