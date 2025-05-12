from dataclasses import dataclass


@dataclass
class Employee:
    id: int
    email: str
    name: str
    department: str
    hours_worked: float
    hourly_rate: float