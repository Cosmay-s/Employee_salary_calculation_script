import re
import logging
from typing import List, Optional
from salary_report.models import Employee
from salary_report.header_aliases import HEADER_ALIASES


logger = logging.getLogger(__name__)


def normalize_header(header: str) -> str:
    cleaned = re.sub(r'[^a-z0-9_]', '', header.strip().lower())
    return HEADER_ALIASES.get(cleaned, cleaned)


def parse_employee_data(headers: List[str],
                        values: List[str],
                        raw_headers: List[str]) -> Optional[Employee]:
    row = dict(zip(headers, values))

    try:
        hours = int(row.get('hours', 0))
        rate_value = float(row.get('rate', 0))

        employee = Employee(
            id=int(row['id']),
            email=row['email'].strip(),
            name=row['name'].strip(),
            department=row['department'].strip(),
            hours=hours,
            rate=rate_value
        )
        return employee
    except (ValueError, KeyError) as e:
        logger.exception("Ошибка при обработке строки данных. Ошибка: %s",
                          str(e))
        return None

def read_employee_data(filepath: str) -> List[Employee]:
    employees = []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.readlines()

            if not lines:
                return employees
            headers = [normalize_header(header)
                       for header in lines[0].strip().split(",")]
            raw_headers = lines[0].strip().split(",")

            for line in lines[1:]:
                values = line.strip().split(",")
                employee = parse_employee_data(headers, values, raw_headers)
                if employee:
                    employees.append(employee)

    except Exception as e:
        logger.exception("Ошибка при чтении файла %s. Ошибка: %s",
                          filepath, str(e))
    
    return employees