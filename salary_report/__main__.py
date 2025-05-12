import logging
import argparse
from salary_report.cvs_reader import read_employee_data
from salary_report.reports.payout import PayoutReport

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--report", required=True)
    parser.add_argument("--output", required=False)

    args = parser.parse_args()

    if args.report != "payout":
        logger.error("Неподдерживаемый тип отчета: %s", args.report)
        return

    all_employees = []
    for file in args.files:
        employees = read_employee_data(file)
        all_employees.extend(employees)

    report = PayoutReport()
    report.create_payout_report(all_employees)

    print(report)

    if args.output:
        logger.info("Сохранение отчета в файл: %s", args.output)
        result = report.save_report_as_json(args.output)
        if result and "error" in result:
            logger.error("Ошибка при сохранении отчета: %s", result["error"])


if __name__ == "__main__":
    main()
