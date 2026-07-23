# Evaluation of Project Documentation for AI Maintenance Invoices Tracker (Iteration 2)

This document provides a senior engineer's review of the revised project documentation located in `docs/` and `README.md`. It outlines our updated understanding, highlights resolved and unresolved ambiguities/inconsistencies, defines the remaining assumptions required to start implementation, and proposes suggestions.

---

## 1. Project Understanding

The goal is to build an MVP for an **AI Maintenance Invoices Tracker Application**. This web app helps car owners organize and manage vehicle maintenance history in a centralized database instead of keeping physical paper invoices.

### Core Architectural Structure
*   **Backend (Python + SQLite)**: Relational database to persist vehicle metadata and service logs. Provides REST APIs for CRUD operations and logic for total cost calculation, upcoming service reminders, and invoice storage links. The specific backend framework (e.g. FastAPI, Flask) is left to the developer's discretion.
*   **Frontend (React)**: A user-friendly dashboard to manage multiple cars, log detailed maintenance bills, view chronologically ordered history, upload files, and check maintenance alerts. The frontend tooling (e.g. Vite, Next.js) is left to the developer's discretion.
*   **File Storage**: Uploaded files (receipt photos, PDFs) stored locally on the server filesystem, with their file paths persisted in the database.
*   **Scope & Tenancy**: A single-user MVP with no user authentication or multi-tenant separation.

---

## 2. Inconsistencies, Ambiguities, and Missing Requirements

### A. Inconsistencies
*   **None (Resolved)**: The previous discrepancy regarding OCR and LLM scope has been resolved. Both OCR scanning and LLM-based vehicle evaluation are now explicitly marked as **Out of Scope** for this MVP.
*   **Security Constraint Context (Resolved)**: The constraint regarding data sanitization when using LLM services is now conditional: *"If the implementation communicates with an external LLM service"*, aligning with the fact that LLM features are not part of the core MVP requirements.

### B. Ambiguities
*   **Reminders Logic**:
    *   *Specification*: "Remind users about upcoming maintenance based on mileage or date, such as oil changes or tire replacement."
    *   *Ambiguity*: There is no mathematical trigger or scheduling rule set in the specification.
*   **Schema Normalization**:
    *   *Specification*: "The schema is normalized."
    *   *Ambiguity*: It is unspecified whether "Performed services" and "Replaced parts" must have their own tables relationally linked to the invoice (e.g., `invoice_items`), or can be stored as JSON arrays / text lists within the main invoice table.
*   **File Storage Naming and Collision Resolution**:
    *   *Specification*: "Uploaded files are stored locally, while the database stores only the file path."
    *   *Ambiguity*: The exact folder structure, file name mapping, and duplicate file handling are left unspecified.

### C. Missing Requirements
*   **Data Validation Details**:
    *   Besides `total_cost > 0` and vehicle association checks, are there constraints on VIN formats (e.g. exactly 17 characters), year limits, or mileage boundaries (e.g. cannot be negative)?
*   **Edit/Delete Capabilities (CRUD)**:
    *   Can users edit or delete vehicles and invoices, or is the application read/write only?

---

## 3. Required Assumptions Before Implementation

If implementation were to proceed immediately, we would make the following assumptions based on the revised specification:

1.  **Single-User / No Auth**: The system has no user authentication. Any user visiting the app sees the same vehicles and invoices.
2.  **Selected Tech Stack**:
    *   **Backend**: Python with **FastAPI** (due to typing and automatic Swagger docs) and **SQLAlchemy** ORM.
    *   **Frontend**: React built with **Vite** and styled with **Vanilla CSS** (premium dark mode theme with rich animations as per UI instructions).
3.  **Local File Storage**: Uploaded receipt PDFs and images will be saved under a local folder (e.g., `src/backend/static/uploads/`). The database will store the relative static file path. File names will be prefixed with a UUID or timestamp to prevent name collisions.
4.  **Relational Database Schema (Normalized)**:
    *   `vehicles` table: `id` (PK), `make`, `model`, `year`, `vin`, `current_mileage`
    *   `invoices` table: `id` (PK), `vehicle_id` (FK), `service_date`, `service_center`, `total_cost`, `receipt_file_path`
    *   `invoice_services` table: `id` (PK), `invoice_id` (FK), `service_name`
    *   `invoice_parts` table: `id` (PK), `invoice_id` (FK), `part_name`
5.  **Reminder Engine Rules**:
    *   *Oil Change*: 6 months or 5,000 miles from the most recent invoice date or mileage.
    *   *Tire Replacement*: 36 months or 30,000 miles from the most recent tire service.
6.  **VIN Validation**: Minimal length validation (17 characters) without strict checksum verification.
7.  **Changelog**: All changes will be recorded in a `/CHANGELOG.md` file at the project root.

---

## 4. Suggested Improvements to the Specification

To make the documentation robust and direct for an AI developer agent, we suggest updating the specifications with:

1.  **Concrete DB Diagram or DDL**: Provide the exact tables and field types expected (SQLite DDL schema).
2.  **API Endpoint Table**: Provide a spec list of REST endpoints, query parameters, and payload types.
3.  **Defined Maintenance Rules**: Include a clear reference table for default upcoming maintenance intervals.
4.  **Allowed File Formats and Sizes**: Specify maximum file upload size (e.g. 5MB) and accepted MIME types (e.g., `.png`, `.jpg`, `.pdf`).
