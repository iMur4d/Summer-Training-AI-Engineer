# Idea Analysis Agent

## Objecetive
- Transform a submitted idea into structured organizational knowledge.

## Input
- `/Idea` command
- Idea text
- Telegram sender information
- Timestamp

## Brain
- LLM

## Available Tools
- Supabase
- Validation Logic
- Search Similar Ideas
- Save Knowledge (Supabase)

## Outputs
- Structured Knowledge
- Summary
- Tags
- Metadata
- Saved Record

## Decision Process


```mermaid
flowchart TD
    A["Receive /idea"] --> B["Validate Input"]
    B --> C{"Valid?"}
    C -- No --> D["Return Error"]
    C -- Yes --> E["Search Similar Knowledge"]
    E --> F["Analyze with LLM"]
    F --> G["Generate Structured Knowledge"]
    G --> H["Store in Supabase (SQLlite)"]
    H --> I["Reply to User"]
```


