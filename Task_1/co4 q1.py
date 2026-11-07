from decimal import Decimal, InvalidOperation
def process_file(filename):
    total = Decimal('0.00')
    report = []
    rejected = []
    with open(filename, 'r') as file:
        for line_no, line in enumerate(file, 1):
            try:
                parts = line.strip().split(',')
                if len(parts) != 3:
                    raise ValueError("Invalid fields")
                reg, name, amount = parts
                amount = Decimal(amount)
                if not reg or not name or not amount.is_finite():
                    raise ValueError("Invalid data")
                if amount < 0:
                    raise ValueError("Negative amount")
                total += amount
                report.append(f"{name} {amount}")
            except (ValueError, InvalidOperation) as e:
                rejected.append((line_no, line.strip(), str(e)))
    print("\nStudent Report:")
    print("\n".join(report))
    print("Total:", total)
    print("\nRejected Lines:")
    for item in rejected:
        print(item)
process_file("mess_oct.txt")
