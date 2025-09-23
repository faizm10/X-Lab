import json
import pandas as pd

# filepath to the trips data
TRIPS_FILEPATH = 'trips/trips.jsonl'
OUTPUT_FILEPATH = 'trips/summary.csv'

# this is just responsible for loading the trips from a JSONL file
def load_trips(filepath):
    """ we can load the trips from the JSONL file (trips.jsonl that we talked about on the train) """
    trips = []
    with open(filepath, 'r') as file:
        for line in file:
            trips.append(json.loads(line))
    return trips

# we need to process the trips into a dataframe and calculate some metrics
def process_trips(trips):
    """ process trips into a dataframe and calculate metrics"""
    df = pd.DataFrame(trips)
    df["total_cost"] = df["local_bus_cost"] + df["go_train_cost"] + df["go_bus_cost"]

    # now, calculate summary metrics
    summary = {
        "average_local_bus_cost": df["local_bus_cost"].mean(),
        "average_go_train_cost": df["go_train_cost"].mean(),
        "average_go_bus_cost": df["go_bus_cost"].mean(),
        "total_trips": len(df),
    }
    return df, summary

# this function basically just saves the processed dataframe and summary metrics to a CSV file
def save_summary(df, summary, output_filepath):
    """ save the processed dataframe and summary metrics to a CSV file """
    df.to_csv(output_filepath, index=False)
    print("Summary metrics:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
# this is the main execution block
if __name__ == "__main__":
    trips = load_trips(TRIPS_FILEPATH)
    df, summary = process_trips(trips)
    save_summary(df, summary, OUTPUT_FILEPATH)