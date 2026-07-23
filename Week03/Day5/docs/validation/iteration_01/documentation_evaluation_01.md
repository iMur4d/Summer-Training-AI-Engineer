# Evaluation of Project Documentation for AI Maintenance Invoices Tracker

This document provides a senior engineer's review of the project documentation located in `docs/` and `README.md`. It outlines our understanding, highlights ambiguities and inconsistencies, defines the assumptions required to start implementation, and proposes concrete specification improvements.

---

## 1. Project Understanding

The goal is to build an MVP for an **AI Maintenance Invoices Tracker Application**. This web app helps car owners organize and manage vehicle maintenance history in a centralized database instead of keeping physical paper invoices.

### Core Architectural Structure
*   **Backend (Python + SQLite)**: Relational database to persist vehicle metadata and service logs. Provides REST APIs for CRUD operations and logic for total cost calculation, upcoming service reminders, and invoice storage links.
*   **Frontend (React)**: A user-friendly dashboard to manage multiple cars, log detailed maintenance bills, view chronologically ordered history, upload files, and check maintenance alerts.
*   **File Storage**: Uploaded files (receipt photos, PDFs) stored outside the database.

---

## 2. Inconsistencies, Ambiguities, and Missing Requirements

### A. Inconsistencies
*   **OCR and AI Scope Discrepancy (Critical)**:
    *   [spec.md](file:///c:/Users/Dvs/Desktop/AI-Engineering-Training/coding/Week03/Day5/docs/spec.md#L28-L36) lists **"Using OpenCV to scan invoices and traditional OCR"** and **"Integrate LLM to evaluate the car state"** as **In Scope** for the MVP.
    *   [context.md](file:///c:/Users/Dvs/Desktop/AI-Engineering-Training/coding/Week03/Day5/docs/context.md#L63-L66) and [project_idea.md](file:///c:/Users/Dvs/Desktop/AI-Engineering-Training/coding/Week03/Day5/docs/project_idea.md#L7-L8) categorize **OCR and AI info extraction** under **Future Improvements** (Out of Scope for the initial MVP).
    *   There is no clarity on whether LLM evaluation/OpenCV OCR must be built now.

### B. Ambiguities
*   **Reminders Logic**:
    *   *Specification*: "Remind users about upcoming maintenance based on mileage or date, such as oil changes or tire replacement."
    *   *Ambiguity*: There is no math or frequency rule set. Are service intervals hardcoded (e.g., oil changes every 5,000 miles / 6 months) or customizable?
*   **File Upload & Storage details**:
    *   *Specification*: "Uploaded files are stored outside the database."
    *   *Ambiguity*: Should files be stored on the local backend filesystem (e.g. `/uploads`) or in a cloud storage service (AWS S3)? How should files be associated with records (e.g., storing the filepath string)? What are the max size/type limits?
*   **Schema Normalization**:
    *   *Specification*: "The schema is normalized."
    *   *Ambiguity*: Does this mean "Performed services" and "Replaced parts" must have their own tables relationally linked to the invoice (e.g., `invoice_items`), or can they be stored as JSON arrays / text lists within the main invoice table?
*   **User Identity**:
    *   *Specification*: "Register multiple cars... switch between multiple cars."
    *   *Ambiguity*: Is user authentication (login/signup, multi-tenancy) in-scope, or is this a single-user local MVP?

### C. Missing Requirements
*   **Specific Python & React Frameworks**:
    *   The tech stack specifies "Python" and "React", but does not prescribe the framework (FastAPI vs Flask vs Django; Vite vs Next.js vs Create React App).
*   **LLM Details & API Secrets**:
    *   If LLM is in-scope, there are no specs on which LLM provider to use (Gemini, OpenAI), nor instructions on the prompt behavior.
    *   No details on how to fulfill: *"Before using LLM with private schema data, must be clean it before you call it."* (What constitutes private schema data? VIN? Mileage? Service Center names?)
*   **Data Validation Details**:
    *   Besides `total_cost > 0`, are there constraints on VIN formats, year limits, or mileage boundaries (e.g. cannot be negative)?
*   **Edit/Delete Capabilities (CRUD)**:
    *   Can users edit or delete vehicles and invoices, or is this read/write only?

---

## 3. Required Assumptions Before Implementation

If implementation were to proceed immediately without further clarification, we would have to make the following assumptions:

1.  **Single-User / No Auth**: The system has no user authentication or sessions. Any user visiting the page sees the same vehicles.
2.  **Selected Tech Stack**:
    *   **Backend**: Python with **FastAPI** (for typing, speed, and automatic Swagger docs) and **SQLAlchemy** ORM.
    *   **Frontend**: React built with **Vite** and styled with **Vanilla CSS** (premium dark mode theme with rich animations as per UI instructions).
3.  **Local File Storage**: Uploaded receipt PDFs and images will be saved under a local folder (e.g. `src/backend/static/uploads/`). The database will store the relative static file path.
4.  **Relational Database Schema (Normalized)**:
    *   `vehicles` table: `id` (PK), `make`, `model`, `year`, `vin`, `current_mileage`
    *   `invoices` table: `id` (PK), `vehicle_id` (FK), `service_date`, `service_center`, `total_cost`, `receipt_file_path`
    *   `invoice_services` table: `id` (PK), `invoice_id` (FK), `service_name`
    *   `invoice_parts` table: `id` (PK), `invoice_id` (FK), `part_name`
5.  **Reminder Engine Rules**:
    *   *Oil Change*: 6 months or 5,000 miles from the most recent invoice date or mileage.
    *   *Tire Replacement*: 36 months or 30,000 miles from the most recent tire service.
6.  **LLM/OCR Scope**:
    *   Since OCR and LLM integration are conflicting, they are treated as **mocked endpoints** in the backend or stubbed on the frontend for the initial MVP. No real OCR binaries (e.g., Tesseract) or paid LLM API calls are required unless credentials and API endpoints are provided.
7.  **VIN Validation**: Minimal length validation (17 characters) without strict checksum verification.
8.  **Changelog**: All changes will be recorded in a `/CHANGELOG.md` file at the project root.

---

## 4. Suggested Improvements to the Specification

To make the documentation robust and direct for an AI developer agent, we suggest updating the specifications with:

1.  **Unified Scope Definition**: Reconcile the discrepancy between `spec.md` and `context.md` on OCR/AI. Either explicitly exclude OpenCV/LLM from MVP, or provide a defined API endpoint/key config for them.
2.  **Concrete DB Diagram or DDL**: Provide the exact tables and field types expected (SQLite DDL schema).
3.  **API Endpoint Table**: Provide a spec list of REST endpoints, query parameters, and payload types.
4.  **Framework Directives**: Specify FastAPI and Vite React explicitly to maintain framework consistency.
5.  **Defined Maintenance Rules**: Include a clear reference table for default upcoming maintenance intervals.
6.  **Allowed File Formats and Sizes**: Specify maximum file upload size (e.g. 5MB) and accepted MIME types (e.g., `.png`, `.jpg`, `.pdf`).
