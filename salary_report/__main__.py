import logging
import argparse
from salary_report.cvs_reader import read_employee_data
from salary_report.reports.payout import PayoutReport

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Генерация отчета по зарплатам сотрудников")
    parser.add_argument("files", nargs="+", help="Пути к CSV-файлам")
    parser.add_argument("--report", required=True, help="Тип отчета (только 'payout' поддерживается)")
    parser.add_argument("--output", required=False, help="Файл для сохранения отчета в формате JSON")

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

    if args.output:
        result = report.save_report_as_json(args.output)
        if result and "error" in result:
            logger.error("Ошибка при сохранении отчета: %s", result["error"])
        else:
            logger.info("Отчет успешно сохранен в файл: %s", args.output)
    else:
        print(report)


if __name__ == "__main__":
    main()
