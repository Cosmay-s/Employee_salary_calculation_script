# Employee_salary_calculation_script
Скрипт для генерации отчета по зарплатам сотрудников из CSV-файлов.

## Запуск

```bash
python -m salary_report file1.csv file2.csv --report payout --output report.json
Поддерживаемый тип отчета: payout

Вход — один или несколько CSV-файлов с данными сотрудников.

Выход — отчет в консоль или в JSON-файл (--output).

