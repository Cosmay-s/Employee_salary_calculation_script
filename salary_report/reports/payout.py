import logging
import json
from typing import List
from salary_report.models import Employee

logger = logging.getLogger(__name__)


class PayoutReport:
    def __init__(self):
        self._report_data = {}

    def create_payout_report(self, employees: List[Employee]):
        logger.info("Начало создания отчета по зарплатам сотрудников.")
        try:
            for employee in employees:
                payout = employee.calculate_payout()
                entry = {
                    "employee_name": employee.name,
                    "worked_hours": employee.hours,
                    "hourly_rate": employee.rate,
                    "payout": payout
                }
                self._report_data.setdefault(employee.department,
                                             []).append(entry)
            logger.info("Отчет успешно создан.")
        except Exception as e:
            logger.exception("Ошибка создания отчета по зарплатам: %s", str(e))

    def __str__(self):
        logger.info("Начало форматирования отчета для вывода.")
        try:
            lines = []
            for department, entries in self._report_data.items():
                lines.append(department)
                total_hours = total_payout = 0
                for employee_data in entries:
                    lines.append(
                        "-------------- {0:<20} {1:<6} {2:<6} ${3:<10}".format(
                            employee_data["employee_name"],
                            int(employee_data["worked_hours"]),
                            int(employee_data["hourly_rate"]),
                            int(employee_data["payout"])
                        )
                    )
                    total_hours += employee_data["worked_hours"]
                    total_payout += employee_data["payout"]
                lines.append("{:>36}{:<13} ${:<10}".format("", total_hours,
                                                           int(total_payout)))
                lines.append("")
            logger.info("Форматирование завершено.")
            return "\n".join(lines)
        except Exception as e:
            logger.exception("Ошибка при форматировании отчета: %s", str(e))
            return "Ошибка формирования отчета."

    def prepare_report_data(self):
        logger.info("Начало подготовки данных отчета в формате JSON.")
        try:
            report_data = {"departments": []}

            for department, employees in self._report_data.items():
                employees_data = [
                    {
                        "name": employee["employee_name"],
                        "worked_hours": int(employee["worked_hours"]),
                        "hourly_rate": int(employee["hourly_rate"]),
                        "payout": int(employee["payout"])
                    }
                    for employee in employees
                ]

                report_data["departments"].append({
                    "department_name": department,
                    "employees": employees_data,
                    "total_hours": sum(e["worked_hours"] 
                                       for e in employees_data),
                    "total_payout": sum(e["payout"] for e in employees_data)
                })

            logger.info("Данные для отчета подготовлены успешно.")
            return report_data
        except Exception as e:
            logger.exception("Ошибка подготовки данных для отчета: %s", str(e))
            return {"error": "Ошибка подготовки данных отчета."}

    def save_report_as_json(self, filepath: str):
        logger.info("Начало сохранения отчета в формате JSON.")
        try:
            report_data = self.prepare_report_data()

            if "error" in report_data:
                return report_data

            with open(filepath, 'w', encoding='utf-8') as json_file:
                json.dump(report_data, json_file, ensure_ascii=False, indent=4)

            logger.info(f"Отчет успешно сохранен в файл: {filepath}")
        except Exception as e:
            logger.exception("Ошибка при сохранении JSON-отчета: %s", str(e))
            return {"error": "Ошибка при сохранении JSON отчета."}
