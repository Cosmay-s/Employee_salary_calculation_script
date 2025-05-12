import pytest
import json
from salary_report.reports.payout import PayoutReport
from salary_report.models import Employee


@pytest.fixture
def employees():
    return [
        Employee(id=1, email="a@example.com", name="Alice",
                 department="Design", hours=100, rate=40),
        Employee(id=2, email="b@example.com", name="Bob",
                 department="Design", hours=120, rate=50),
        Employee(id=3, email="c@example.com", name="Carol",
                 department="HR", hours=90, rate=60)
    ]


def test_create_payout_report(employees):
    report = PayoutReport()
    report.create_payout_report(employees)

    assert "Design" in report._report_data
    assert len(report._report_data["Design"]) == 2
    assert report._report_data["Design"][0]["payout"] == 4000


def test_report_str_output(employees):
    report = PayoutReport()
    report.create_payout_report(employees)
    output = str(report)
    assert "Design" in output
    assert "Alice" in output
    assert "$4000" in output


def test_prepare_report_data(employees):
    report = PayoutReport()
    report.create_payout_report(employees)
    data = report.prepare_report_data()

    assert "departments" in data
    assert any(dep["department_name"] == "Design" for dep in data["departments"])
    assert data["departments"][0]["employees"][0]["name"] == "Alice"


def test_save_report_as_json(employees, tmp_path):
    report = PayoutReport()
    report.create_payout_report(employees)

    output_file = tmp_path / "output.json"
    report.save_report_as_json(str(output_file))

    assert output_file.exists()
    with open(output_file, "r", encoding="utf-8") as f:
        content = json.load(f)
        assert "departments" in content
        assert any(dep["department_name"] == "HR" for
                   dep in content["departments"])
