# Project Spec: AI Maintenance Invoices Tracker Application

---

## Objective

Build a web application helps car owners organize all maintenance invoices in one place because paper invoices are easy to lose.

---

## Technology Stack

| Tool   | Purpose   |
| ------ | --------- |
| Python | Backend   |
| SQLite | Database  |
| React  | Interface |

### Framework Selection

The implementation framework is intentionally left unspecified.

The development team may select the most appropriate Python backend framework
and React tooling during implementation based on project needs.

---

## Project Structure

- `src/` - Application source code
- `tests/` - Unit test
- `docs/` - Documentation

## Project Scope

### In Scope

- Build an MVP to validate the project idea.
- Register and manage multiple vehicles.
- Store maintenance invoices and service history.
- Upload invoice images or PDF files.
- Calculate the total maintenance cost for each vehicle.
- Display maintenance history in chronological order.

### Out of Scope (Future Improvements)

- OCR-based invoice scanning.
- LLM-based vehicle condition evaluation.
- Automatic information extraction using VLM.
- Maintenance type classification.
- Future maintenance cost prediction.


---

## Functional Requirements

**The ability to register multiple cars, each with its:**

- make
- model
- year
- VIN
- current mileage

**Each maintenance invoice should include:**

- Service
  - Date
  - Center
- Total cost
- Performed services
- Replaced parts
- Upload the invoice as a PDF or image.
- Uploaded files are stored locally, while the database stores only the file path.

---

## Features

**The system should:**

1. Automatically calculate the total maintenance cost for each vehicle
2. Display the maintenance history in chronological order
3. Remind users about upcoming maintenance based on mileage or date, _such as oil changes or tire replacement_

---

## Validation Rules

**Users should not be allowed:**

- Save invoices without selecting a vehicle

**The system must validate:**

- Total cost should always be greater than zero

---

## Constraints 

- The MVP is designed as a single-user application.
- User authentication is out of scope for this version.
- If the implementation communicates with an external LLM service, any sensitive
application data (such as VINs or other private information) must be sanitized
before being sent outside the system.
- After you finished the task write your changes into `/CHANGELOG.md`

