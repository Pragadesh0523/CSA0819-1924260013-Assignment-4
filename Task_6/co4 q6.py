
import os

INPUT = "input"
OUTPUT = "output"

def valid_email(email):
    email = email.strip().lower()

    if email.count("@") != 1 or " " in email:
        return False

    name, domain = email.split("@")
    return bool(name) and "." in domain and not domain.startswith(".") and not domain.endswith(".")

def process():
    os.makedirs(OUTPUT, exist_ok=True)

    master = []
    seen = set()
    events = {}
    errors = []
    total = 0
    duplicates = 0
    invalid = 0

    files = ["cse.txt", "aids.txt", "ece.txt",
             "eee.txt", "mech.txt"]

    for filename in files:
        path = os.path.join(INPUT, filename)

        try:
            with open(path, "r") as f:

                for line_no, line in enumerate(f, 1):
                    total += 1

                    try:
                        data = line.strip().split("|")

                        if len(data) != 5:
                            raise ValueError("Damaged line")

                        reg, name, dept, email, choices = data

                        reg = reg.strip()
                        name = name.strip()
                        dept = dept.strip()
                        email = email.strip().lower()

                        if not all([reg, name, dept, choices.strip()]):
                            raise ValueError("Missing field")

                        if not valid_email(email):
                            raise ValueError("Invalid email")

                        if reg in seen:
                            duplicates += 1
                            raise ValueError("Duplicate registration")

                        seen.add(reg)

                        student = (
                            f"{reg}|{name}|{dept}|{email}|{choices}"
                        )
                        master.append(student)

                        for event in choices.split(";"):
                            event = event.strip()
                            if event:
                                events.setdefault(event, []).append(student)

                    except ValueError as e:
                        invalid += 1
                        errors.append(
                            f"{filename} Line {line_no}: {e} - {line.strip()}"
                        )

        except FileNotFoundError:
            errors.append(f"Missing file: {filename}")

        except OSError as e:
            errors.append(f"File error {filename}: {e}")

    # Write master list
    with open(f"{OUTPUT}/master_list.txt", "w") as f:
        f.write("\n".join(master))

    # Write event-wise files
    for event, students in events.items():
        safe_name = "".join(
            c if c.isalnum() else "_" for c in event
        ).lower()

        with open(f"{OUTPUT}/event_{safe_name}.txt", "w") as f:
            f.write("\n".join(students))

    # Write summary
    with open(f"{OUTPUT}/summary.txt", "w") as f:
        f.write(f"Total records: {total}\n")
        f.write(f"Valid registrations: {len(master)}\n")
        f.write(f"Duplicates: {duplicates}\n")
        f.write(f"Invalid records: {invalid}\n")
        f.write(f"Missing/error files: {len(errors)}\n")
        f.write(f"Total events: {len(events)}\n")

    # Write error log
    with open(f"{OUTPUT}/error_log.txt", "w") as f:
        f.write("\n".join(errors))

    print("Fest Registration Processing Completed!")
    print("Valid registrations:", len(master))
    print("Duplicates:", duplicates)
    print("Errors:", len(errors))


if __name__ == "__main__":
    process()
