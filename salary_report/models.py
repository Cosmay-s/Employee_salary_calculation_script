from dataclasses import dataclass


@dataclass
class Employee:
    id: int
    email: str
    name: str
    department: str
    hours: int
    rate: float

    def calculate_payout(self) -> float:
        return self.hours * self.rate

    def __repr__(self) -> str:
        return (
            f"Employee(\n"
            f"  id={self.id},\n"
            f"  email={self.email},\n"
            f"  name={self.name},\n"
            f"  department={self.department},\n"
            f"  hours={self.hours},\n"
            f"  rate={self.rate}\n"
            f")")
