import pytest
from salary_report.models import Employee


@pytest.fixture
def employee():
    return Employee(id=1, email="test@example.com", name="Test Employee",
                    department="IT", hours=160, rate=50.0)


def test_employee_payout(employee):
    expected_payout = 160 * 50
    assert employee.calculate_payout() == expected_payout


def test_employee_repr(employee):
    expected_repr = (
        "Employee(\n"
        "  id=1,\n"
        "  email=test@example.com,\n"
        "  name=Test Employee,\n"
        "  department=IT,\n"
        "  hours=160,\n"
        "  rate=50.0\n"
        ")"
    )
    assert repr(employee) == expected_repr
