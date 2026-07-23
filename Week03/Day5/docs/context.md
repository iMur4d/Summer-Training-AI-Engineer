# Context Project for AI Agent
> This document provides the minimum context required for an AI agent to understand the project, its current state, and the assigned task before implementation.
## Background
The project aims to help car owners manage maintenance invoices digitally instead of relying on paper documents that are easily lost.
Understanding common vehicle maintenance workflows and invoice structures will help produce a more practical solution. 

### Rule
You are a software engineer responsible for designing practical, maintainable, and scalable solutions for this project.

### Behavioral Guidelines
Stay focused on the application requirements.
If you identify useful real-world improvements, suggest them separately without changing the original project requirements.

## Current State
The project is currently in the planning phase.

Only the project description has been defined.

No architecture, database schema, or implementation has been created yet.

## Current Task
Prepare the project for implementation based on the provided specification.

## Success Criteria
The solution is considered complete if:

- One vehicle can own multiple invoices.

- Uploaded files are stored outside the database.

- Cost validation exists.

- The schema is normalized.

## Project Requirements

### Functional Requirements

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

### Features
**The system should:**
1. Automatically calculate the total maintenance cost for each vehicle
2. Display the maintenance history in chronological order
3. Remind users about upcoming maintenance based on mileage or date, *such as oil changes or tire replacement*
---

#### Future Improvements

- OCR-based invoice scanning.
- LLM-based vehicle condition evaluation.
- Automatic information extraction using VLM.
- Maintenance type classification.
- Future maintenance cost prediction.

