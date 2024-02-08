import json
import os
import boto3
from datetime import datetime, time

def load_rds_details(file_name='/Users/yaminidhulipalla/CoreSecOps - tool /rdsstop_start/rds_details.json'):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Using default values.")
        return {
            'name': 'your-default-rds-instance-name',
            'region': 'your-default-region',
            'start_time': '08:00',
            'stop_time': '18:00'
        }

def check_cluster_status(rds_client, rds_name):
    try:
        response = rds_client.describe_db_clusters(DBClusterIdentifier=rds_name)
        cluster_status = response['DBClusters'][0]['Status']
        # print(f"RDS Cluster Status: {cluster_status}")
        return cluster_status
    except Exception as e:
        print(f"Error: {str(e)}")

def start_rds(rds_client, rds_name):
    try:
        rds_client.start_db_cluster(DBClusterIdentifier=rds_name)
        print(f"Starting RDS {rds_name}")
    except Exception as e:
        print(f"Error starting RDS {rds_name}: {str(e)}")

def stop_rds(rds_client, rds_name):
    try:
        rds_client.stop_db_cluster(DBClusterIdentifier=rds_name)
        print(f"Stopping RDS {rds_name}")
    except Exception as e:
        print(f"Error stopping RDS {rds_name}: {str(e)}")

def is_within_time_range(start_time, stop_time):
    current_time = datetime.now().time()
    print(current_time)
    return start_time <= current_time <= stop_time

def main():
    rds_details = load_rds_details()
    for cluster in rds_details:
        region = cluster['region']
        rds_name = cluster['name']
        start_time = datetime.strptime(cluster['start_time'], '%H:%M').time()
        stop_time = datetime.strptime(cluster['stop_time'], '%H:%M').time()
        current_time = datetime.now().time()
        rds_client = boto3.client('rds', region_name=region,aws_access_key_id="AKIAWVSRUQCJOK2TZ4MC",aws_secret_access_key="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")
        if current_time >= start_time:
            cluster_status = check_cluster_status(rds_client, rds_name)
            if cluster_status == 'stopped':
                print(f"RDS {rds_name} is currently Stopped status. Starting the cluster.")
                start_rds(rds_client, rds_name)
            elif cluster_status == 'available':
                print(f"RDS {rds_name} is already available. Current Time: {current_time}, Start Time: {start_time}, Stop Start: {stop_time}")
            else:
                print(f"Unexpected status of RDS {rds_name}. Status: {cluster_status}")
        else:
            print(f"It's not yet time to start RDS {rds_name}. Current Time: {current_time}, Start Time: {start_time}, Stop Start: {stop_time}")
        if current_time >= stop_time:
            cluster_status = check_cluster_status(rds_client, rds_name)
            if cluster_status == 'available':
                print(f"RDS {rds_name} is currently available. stopped the cluster.")
                stop_rds(rds_client, rds_name)
            elif cluster_status == 'stopped':
                print(f"RDS {rds_name} is already stopped. Current Time: {current_time}, Start Time: {start_time}, Stop Start: {stop_time}")
            else:
                print(f"Unexpected status of RDS {rds_name}. Status: {cluster_status}")
                

        # if is_within_time_range(start_time, stop_time):
        #     cluster_status = check_cluster_status(rds_client, rds_name)

        #     # print(f"hello doctor hurt miss {cluster_status}")
        #     # If the cluster isn't running and it should be, then start it up!
        #     if cluster_status == 'available':
        #         print(f"RDS {rds_name} is currently available. Stopping the cluster.")
        #         stop_rds(rds_client, rds_name)
        #     elif cluster_status == 'stopped':
        #         print(f"RDS {rds_name} is already stopped.")
        #     else:
        #         print(f"RDS {rds_name} is in {cluster_status} state. Taking appropriate action.")
        # else:
        #     current_time = datetime.now().time()
        #     if current_time > start_time and current_time < stop_time:
        #         cluster_status = check_cluster_status(rds_client, rds_name)

        #         if cluster_status == 'available':
        #             print(f"RDS {rds_name} is currently available. Starting the cluster.")
        #             # start_rds(rds_client, rds_name)
        #         elif cluster_status == 'stopped':
        #             print(f"RDS {rds_name} is stopped.")
        #             start_rds(rds_client, rds_name)
        #         else:
        #             print(f"RDS {rds_name} is in {cluster_status} state. Taking appropriate action.")
            # if cluster_status == 'available':
            #     print(f"Stopping {rds_name}")
            #     start_rds(rds_client, rds_name)
            # elif cluster_status == 'stopped':
            #     print(f"Starting {rds_name} - currently stopped")
            #     stop_rds(rds_client, rds_name)
            # else:
            #     stop_rds(rds_client, rds_name)

if __name__ == '__main__':
    main()
