from salary_report.models import Employee


def test_employee_payout():
    employee = Employee(id=1, email="test@example.com", name="Test",
                        department="IT", hours=160, rate=50)
    assert employee.calculate_payout() == 8000
