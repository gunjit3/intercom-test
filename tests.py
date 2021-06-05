from nearby_customer import compute_distance, load_customers, write_output, get_customers_within_distance, \
    sort_customers_by_id
from constants import INTERCOM_OFFICE_LAT, INTERCOM_OFFICE_LONG
import pytest


def test_compute_distance_same_spot():
    dist = compute_distance(INTERCOM_OFFICE_LAT, INTERCOM_OFFICE_LONG, INTERCOM_OFFICE_LAT, INTERCOM_OFFICE_LONG)
    assert dist == 0


def test_compute_distance_same_spot():
    dist = compute_distance(INTERCOM_OFFICE_LAT, INTERCOM_OFFICE_LONG, INTERCOM_OFFICE_LAT+0.5, INTERCOM_OFFICE_LONG+1)
    print(dist)
    assert dist == 86.3


def test_get_customers_within_distance():
    customers = load_customers(open("./customers.txt"))
    customers = get_customers_within_distance(customers)
    assert len(customers) == 16


def test_sort_customers_by_id():
    customers = load_customers(open("./test_resources/valid.txt"))
    customers = sort_customers_by_id(customers)
    assert customers[0]["user_id"] == 1


def test_read_file():
    customers = load_customers(open("./test_resources/valid.txt"))
    assert len(customers) == 2


def test_read_empty_file():
    customers = load_customers(open("./test_resources/empty.txt"))
    assert len(customers) == 0


def test_read_invalid_file():
    with pytest.raises(ValueError):
        customers = load_customers(open("./test_resources/invalid.txt"))


def test_write_to_file():
    import os
    customers = load_customers(open("./test_resources/valid.txt"))
    write_output("./test_write.txt", customers)
    assert os.path.exists("./test_write.txt")
    os.remove("./test_write.txt")
