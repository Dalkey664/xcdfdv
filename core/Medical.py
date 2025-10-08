from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Tuple
from functools import reduce
#DOMAIN ENTITIES (IMMUTABLE)
@dataclass(frozen=True)
class Patient:
    id: int
    name: str
    age: int
@dataclass(frozen=True)
class Doctor:
    id: int
    name: str
    specialty: str
@dataclass(frozen=True)
class Appointment:
    id: int
    patient: Patient
    doctor: Doctor
    start: datetime
    duration_minutes: int
    category: str
    @property
    def end(self) -> datetime:
        return self.start + timedelta(minutes=self.duration_minutes)
@dataclass(frozen=True)
class Service:
    id: int
    name: str
    price: int  # cents
@dataclass(frozen=True)
class InvoiceLine:
    service: Service
    qty: int
@dataclass(frozen=True)
class Invoice:
    id: int
    patient: Patient
    lines: Tuple[InvoiceLine, ...]
    @property
    def total(self) -> int:
        return sum(l.service.price * l.qty for l in self.lines)
#PURE FUNCTIONS + MAP/FILTER/REDUCE


def overlapping(a1: Appointment, a2: Appointment) -> bool:
    return a1.start < a2.end and a2.start < a1.end
def total_income(invoices: List[Invoice]) -> int:
    return reduce(lambda acc, i: acc + i.total, invoices, 0)
def filter_expensive_services(services: List[Service], min_price: int) -> List[Service]:
    return list(filter(lambda s: s.price >= min_price, services))
def map_discount(services: List[Service], percent: float) -> List[Service]:
    factor = 1 - percent / 100
    return [Service(s.id, s.name, int(s.price * factor)) for s in services]
#LAMBDAS + CLOSURES
def make_filter_by_category(cat: str):
    return lambda appt: appt.category == cat
def make_filter_by_date_range(start: datetime, end: datetime):
    return lambda appt: start <= appt.start <= end
def make_filter_by_patient_name(part: str):
    part_low = part.lower()
    return lambda appt: part_low in appt.patient.name.lower()

#RECURSION
@dataclass(frozen=True)
class Department:
    name: str
    subdepartments: List["Department"]
def find_department(root: Department, name: str) -> Department | None:
    if root.name == name:
        return root
    for sub in root.subdepartments:
        found = find_department(sub, name)
        if found:
            return found
    return None
def count_total_departments(root: Department) -> int:
    if not root.subdepartments:
        return 1
    return 1 + sum(count_total_departments(sub) for sub in root.subdepartments)
def nested_sum(structure):
    if isinstance(structure, (int, float)):
        return structure
    if isinstance(structure, dict):
        return sum(nested_sum(v) for v in structure.values())
    if isinstance(structure, (list, tuple)):
        return sum(nested_sum(x) for x in structure)
    return 0
#DEMO PIPELINE
def demo():
    patient1 = Patient(1, "Alice", 35)
    patient2 = Patient(2, "Bob", 28)
    doctor = Doctor(1, "Dr. House", "Therapy")
    s1 = Service(1, "Consultation", 10000)
    s2 = Service(2, "X-ray", 5000)
    services = [s1, s2]
    invoice = Invoice(1, patient1, (InvoiceLine(s1, 1), InvoiceLine(s2, 2)))
    invoices = [invoice]
    now = datetime(2025, 10, 8)
    appts = [
        Appointment(1, patient1, doctor, now, 30, "checkup"),
        Appointment(2, patient2, doctor, now + timedelta(days=1), 45, "surgery"),
        Appointment(3, patient1, doctor, now + timedelta(days=2), 20, "checkup"),
    ]
    discounted = map_discount(services, 10)
    expensive = filter_expensive_services(discounted, 6000)
    total = total_income(invoices)
    print("Discounted:", discounted)
    print("Expensive only:", expensive)
    print("Total income:", total)
    checkup_filter = make_filter_by_category("checkup")
    name_filter = make_filter_by_patient_name("bob")
    print("Checkups:", [a.id for a in filter(checkup_filter, appts)])
    print("By patient 'bob':", [a.id for a in filter(name_filter, appts)])
    dep_tree = Department(
        "Hospital",
        [
            Department("Reception", []),
            Department("Diagnostics", [Department("X-Ray", []), Department("MRI", [])]),
            Department("Surgery", [Department("Cardio", []), Department("Neuro", [])]),
        ],
    )
    print("Find 'MRI':", find_department(dep_tree, "MRI"))
    print("Total departments:", count_total_departments(dep_tree))
    print("Nested sum:", nested_sum([10, [20, {"x": 5, "y": [15, 5]}]]))
if __name__ == "__main__":
    demo()
