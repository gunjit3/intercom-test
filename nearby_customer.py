import argparse
import json
from math import sin, cos, asin, sqrt, radians, pow
from constants import INTERCOM_OFFICE_LAT, INTERCOM_OFFICE_LONG, EARTH_RADIUS, DISTANCE_LIMIT_KMS


def load_customers(input_file):
    """
    Reads in a file line by line to build a list of customers.
    :param input_file: File handle to input file
    :return: List of python dicts denoting a customer
    """
    with input_file:
        try:
            customers = [json.loads(line) for line in input_file]
        except ValueError:
            print("Incorrect json format. Please provide a valid customer json")
            raise

    return customers


def compute_distance(source_latitude, source_longitude, destination_latitude, destination_longitude):
    """
    Function to compute distance between source and destination on the globe. The points are identified by
    longitudes and latitudes in degrees.
    Function uses haversine formula described in https://en.wikipedia.org/wiki/Great-circle_distance

    :param source_latitude: Source latitude in degrees
    :param source_longitude: Source longitude in degrees
    :param destination_latitude: Destination latitude in degrees
    :param destination_longitude: Destination Longitude in degrees
    :return: Distance between source and destination in Kilometers
    """
    source_lat_rad, source_long_rad = radians(source_latitude), radians(source_longitude)
    dest_lat_rad, dest_long_rad = radians(destination_latitude), radians(destination_longitude)

    delta_latitudes = source_lat_rad - dest_lat_rad
    delta_longitudes = source_long_rad - dest_long_rad

    sine_term = pow(sin(delta_latitudes / 2), 2)
    cosine_term = cos(source_lat_rad) * cos(dest_lat_rad) * pow(sin(delta_longitudes / 2), 2)

    central_angle = 2 * asin(sqrt(sine_term + cosine_term))
    distance = round(central_angle * EARTH_RADIUS, 2)

    return distance


def get_customers_within_distance(customers, distance_limit_km=DISTANCE_LIMIT_KMS):
    """
    Function to return customers who are within a threshold limit from intercom office.

    :param customers: List of customers
    :param distance_limit_km: Limit threshold from intercom office in kilometers
    :return:List of customers who are within limit distance
    """
    nearby_customers = dict()
    for customer in customers:
        customer_lat = float(customer['latitude'])
        customer_long = float(customer['longitude'])

        if compute_distance(INTERCOM_OFFICE_LAT, INTERCOM_OFFICE_LONG, customer_lat,
                            customer_long) < distance_limit_km:
            nearby_customers[customer['user_id']] = customer

    return nearby_customers.values()


def sort_customers_by_id(customers):
    """
    Sorts customers based on customer id
    :param customers: List of customers
    :return: Sorted list of customers based on customer id
    """
    return sorted(customers, key=lambda x: x['user_id'])


def write_output(output_file, customers):
    """
    Function to write customers to output file, one line per customer.

    :param output_file: Path of output file to be generated
    :param customers: List of customers to be written into output file
    :return: Does not return anything
    """
    with open(output_file, 'w') as outfile:
        for customer in customers:
            json.dump(customer, outfile)
            outfile.write("\n")


def parse_args():
    """
    Function to parse arguments
    :return: Namespace object with parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=argparse.FileType("r"), help='path to customers file')
    parser.add_argument('output_file', type=str, help='path to output file')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    valid_customers = sort_customers_by_id(get_customers_within_distance(load_customers(args.input_file)))
    write_output(args.output_file, valid_customers)
