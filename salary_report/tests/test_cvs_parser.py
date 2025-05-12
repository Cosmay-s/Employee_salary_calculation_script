import pytest
from unittest.mock import mock_open, patch
from salary_report.cvs_reader import normalize_header, parse_employee_data, read_employee_data
from salary_report.models import Employee

HEADERS = ['id', 'email', 'name', 'department', 'hours', 'rate']
RAW_HEADERS = ['id', 'email', 'name', 'department', 'hours_worked', 'salary']
VALID_VALUES = ['1', 'alice@example.com', 'Alice Johnson', 'Marketing', '160', '50']


@pytest.mark.parametrize("raw,expected", [
    ("hourlyRate", "rate"),
    ("Salary", "rate"),
    ("Hours_Worked", "hours"),
    ("unknownHeader", "unknownheader"),
])
def test_normalize_header(raw, expected):
    assert normalize_header(raw) == expected


def test_parse_employee_data_valid():
    emp = parse_employee_data(HEADERS, VALID_VALUES, RAW_HEADERS)
    assert isinstance(emp, Employee)
    assert emp.name == "Alice Johnson"
    assert emp.rate == 50.0


def test_parse_employee_data_invalid():
    bad_values = VALID_VALUES.copy()
    bad_values[4] = "invalid"
    assert parse_employee_data(HEADERS, bad_values, RAW_HEADERS) is None


def test_read_employee_data_valid():
    csv = "id,email,name,department,hours_worked,salary\n1,alice@example.com,Alice Johnson,Marketing,160,50\n"
    with patch("builtins.open", mock_open(read_data=csv)):
        emps = read_employee_data("fake.csv")
        assert len(emps) == 1
        assert emps[0].email == "alice@example.com"


def test_read_employee_data_invalid_row():
    csv = "id,email,name,department,hours_worked,salary\n1,alice@example.com,Alice Johnson,Marketing,notanumber,50\n"
    with patch("builtins.open", mock_open(read_data=csv)):
        assert read_employee_data("fake.csv") == []


def test_read_employee_data_empty():
    with patch("builtins.open", mock_open(read_data="")):
        assert read_employee_data("fake.csv") == []
