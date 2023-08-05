import pandas
import pkg_resources


def read_resource_csv(relative_name):
    stream = pkg_resources.resource_stream(__name__, relative_name)
    df = pandas.read_csv(stream)
    return df


def passengers():
    return read_resource_csv("res/passengers.csv")

def family_info():
    return read_resource_csv("res/family_info.csv")

def tickets():
    return read_resource_csv("res/tickets.csv")


def test_passengers():
    return read_resource_csv("res/test_passengers.csv")

def test_family_info():
    return read_resource_csv("res/test_family_info.csv")

def test_tickets():
    return read_resource_csv("res/test_tickets.csv")
