# AI Maintenance Invoices Tracker Application

A smart web application that helps car owners organize, track, and manage all their vehicle maintenance invoices in a centralized digital platform.

## Overview

Paper invoices are easy to lose, or the ink may fade from them. This project solves that by allowing users to register multiple vehicles and digitally log every maintenance record. In the future, the system will leverage AI and OCR to extract invoice data and estimate upcoming maintenance costs automatically.

## Key Features

- Multi-Vehicle Management: Register and switch between multiple cars (Track Make, Model, Year, VIN, and Mileage).

- Digital Invoices: Log services, replaced parts, total costs, and upload photos/PDFs of the actual receipts.

- Cost Calculation: Automatically calculate the total maintenance cost per vehicle.

- Smart Reminders: Get notified about upcoming maintenance (e.g., oil changes) based on mileage or date.

## Technology Stack

| Tool   | Purpose   |
| ------ | --------- |
| Python | Backend   |
| SQLite | Database  |
| React  | Interface |

## Getting Started
Coming soon.

## Current Status

This project is currently under active development as an MVP.

## Project Structure

```
C:.
│   README.md
│
├───docs/      # Project documentation
|   |
│   ├───validation/
│   │   └── iteration_01.md
│   │
│   ├───context.md        # Context provided to AI agents
│   ├───project_idea.md   # Original project concept
│   ├───spec.md           # Detailed implementation specification
│   └───system_prompt.md  # AI assistant instructions
│
├───src/
│   ├───backend/    # Python & SQLite code
│   └───frontend/   # React application
|
└── tests/     # Unit and integration tests

```

## Documentation

| File | Purpose |
|------|---------|
| project_idea.md | Original project idea |
| context.md | Context for AI agents |
| spec.md | Project specification |
| system_prompt.md | AI assistant behavior |