# AI Maintenance Invoices Tracker Application
---
## Objective
The application helps car owners organize all maintenance invoices in one place because paper invoices are easy to lose.

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
3. Remind users about upcoming maintenance based on mileage or date, *such as oil changes or tire replacement*
---

### Future Improvements
 - Using OCR and AI to extract information automatically
 - Classify maintenance types and estimate future maintenance costs
---

## Technology Stack
|Tool|Purpose|
|---|---|
|Python|Backend|
|SQLite|Database|
|Flutter|Interface|

---
## Validation Rules
**Users should not be allowed:**
- Save invoices without selecting a vehicle

**The system must validate:**
- Total cost should always be greater than zero
---

## Workflow
Simple workflow of app:

```mermaid
graph LR
User --> System
System --> Car
Car --> Invoices
Invoices --> Database
```
<!-- Note: This document was created by converting an unstructured project description into a structured Markdown document -->