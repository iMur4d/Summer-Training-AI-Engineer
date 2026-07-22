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

---

## Project Structure

- `src/` - Application source code
- `tests/` - Unit test
- `docs/` - Documentation

## Project Scope
### In Scope 
 - Building a MVP to prove the idea concept
 - Integrate LLM to evaluate the car state
 - Using OpenCV to scan invoices and traditional OCR

### Out of scope (Features Improvements)
- Using VLM to extract information automatically and retrieve stucture data
- Classify maintenance types and estimate future maintenance costs


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
- Upload it as PDF or image

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
- Before using LLM with private schema data , must be clean it before you call it.

- After you finished the task write your changes into `/CHANGELOG.md`

