import os
import tempfile

class InvalidRecord(Exception):
    """Raised when an attendance record is invalid."""
    pass


def parse_line(line):
    parts = line.strip().split(",")

    if len(parts) != 3:
        raise InvalidRecord(
            f"expected 3 fields, found {len(parts)}"
        )

    roll, date, status = parts

    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")

    return roll, date, status


def summarise(path):
    present, absent, errors = 0, 0, []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                try:
                    roll, date, status = parse_line(line)

                    if status == "P":
                        present += 1
                    else:
                        absent += 1

                except InvalidRecord as e:
                    errors.append((line_no, str(e)))

    except FileNotFoundError as e:
        raise RuntimeError("Attendance file not found") from e

    except PermissionError as e:
        raise RuntimeError("Permission denied") from e

    except UnicodeDecodeError as e:
        raise RuntimeError("Wrong file encoding") from e

    except OSError as e:
        raise RuntimeError("File reading error") from e

    else:
        print("File processed successfully")

    finally:
        print("Attendance processing completed")

    return present, absent, errors


# Test data
data = (
    "192311001,2026-10-08,P\n"
    "192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n"
    "192311004,2026-10-08,L\n"
)

with tempfile.NamedTemporaryFile(
    mode="w", suffix=".csv", delete=False, encoding="utf-8"
) as tmp:
    tmp.write(data)
    filename = tmp.name

try:
    print(summarise(filename))

except RuntimeError as e:
    print(e)

finally:
    os.remove(filename)