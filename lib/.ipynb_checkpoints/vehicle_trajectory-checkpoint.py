from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r



def calculate_speed_from_gps(lon1, lat1, lon2, lat2, time_between):
    distance = haversine(lon1, lat1, lon2, lat2)
    speed = distance/time_between*3600
    return speed


def create_gps_speed_df(latlong):
    latlong['deltaT_to_gps_before'] = latlong.Timestamp.diff().dt.seconds#.div(60, fill_value=0)
    latlong['speed'] = 0
    for i in range(1, latlong.shape[0]):
        latlong.loc[i, 'speed'] = calculate_speed_from_gps(lon1 = latlong.loc[i-1, 'Longitude'], lat1 = latlong.loc[i-1, 'Latitude'],
                                                   lon2 = latlong.loc[i, 'Longitude'], lat2 = latlong.loc[i, 'Latitude'], 
                                                   time_between = latlong.loc[i, 'deltaT_to_gps_before'])
    return latlong

def calculate_acceleration_from_speed(vehicle_speed_before, vehicle_speed_after, time_between_seconds):
    acc = (vehicle_speed_after - vehicle_speed_before) / time_between_seconds
    return acc


def create_acceleration_series(data_gps):
    acc_ = list()
    for i in range(data_gps.shape[0]-1):
        
        v0 = data_gps.vehicle_speed[i]
        v1 = data_gps.vehicle_speed[i+1]
        time_between = data_gps.Timestamp[i+1] - data_gps.Timestamp[i]
        time_between = time_between.total_seconds()
        #check if change in participant
        p0 = data_gps.participant_id[i]
        p1 = data_gps.participant_id[i+1]
        if p0 != p1:#if time_between > 100:
            acc = np.nan
        else:
            acc = calculate_acceleration_from_speed(vehicle_speed_before = v0,vehicle_speed_after = v1, time_between_seconds = time_between)
        acc_.append(acc)
    
    #last element acceleration is constant -> acceleration stays the same
    acc_.append(acc)
    return pd.Series(data = acc_, index = data_gps.index)



def calculate_acceleration_from_speed(vehicle_speed_before, vehicle_speed_after, time_between_seconds):
    acc = (vehicle_speed_after - vehicle_speed_before) / time_between_seconds
    return acc


def create_acceleration_series(data_gps):
    acc_ = list()
    for i in range(data_gps.shape[0]-1):
        
        v0 = data_gps.vehicle_speed[i]
        v1 = data_gps.vehicle_speed[i+1]
        time_between = data_gps.Timestamp[i+1] - data_gps.Timestamp[i]
        time_between = time_between.total_seconds()
        #check if change in participant
        p0 = data_gps.participant_id[i]
        p1 = data_gps.participant_id[i+1]
        if p0 != p1:#if time_between > 100:
            acc = 0
        else:
            acc = calculate_acceleration_from_speed(vehicle_speed_before = v0,vehicle_speed_after = v1, time_between_seconds = time_between)
        acc_.append(acc)
    
    #last element acceleration is constant -> acceleration stays the same
    acc_.append(acc)
    return pd.Series(data = acc_, index = data_gps.index)


