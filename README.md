# StudyOntology

Extract concepts and relationships from course materials to build interactive knowledge graphs.

## Overview

StudyOntology transforms scattered course materials (PDFs, slides, notes) into connected knowledge graphs. Upload your documents to see how concepts, theories, methods, and people relate to each other across your entire course.

## Features

- Schema-constrained AI extraction using LinkML ontology
- Support for PDF, PowerPoint, and DOCX documents
- Entity resolution to merge duplicate concepts
- Interactive graph visualization with d3.js
- Click nodes to jump to source material
- Study path generation based on prerequisite chains
- Export graphs as PNG or PDF

## Knowledge Graph Schema

### Entity Types
- **Concept**: Core ideas and topics
- **Theory**: Scientific frameworks and paradigms
- **Person**: Researchers and notable figures
- **Method**: Techniques and procedures

### Relationship Types
- prerequisite_of: Must learn A before B
- example_of: A is a concrete instance of B
- contrasts_with: A is similar but different from B
- located_in: A is found within or part of B
- produces: A creates B as output
- consumes: A uses B as input
- applies_to: Theory or method applies to a domain

## Technology Stack

- Schema Definition: LinkML + YAML
- Model Generation: LinkML to Pydantic
- Document Parsing: PyPDF2, python-docx, pdfplumber
- AI Extraction: OpenAI GPT-4o Function Calling
- Validation: Pydantic Models
- Graph Storage: NetworkX + DuckDB
- Visualization: d3.js + React
- Backend: FastAPI + Python
- DevOps: Nix + GitHub Actions

## Getting Started

### Prerequisites

- Nix package manager
- Python 3.13+

### Development Environment

```bash
# Enter the development shell
nix develop
```

This provides the `study-ontology` package, `flake8` linter, and `pyright` type checker.

### Building the Package

```bash
nix build
```

### Code Quality

```bash
# Linting
flake8 lib/

# Type checking
pyright lib/
```

## Project Structure

```
lib/StudyOntology/     # Main package code
  __init__.py           # Package exports
  core.py               # Core functionality
nix/                    # Nix configuration
  shell.nix             # Dev shell (flake8, pyright)
  overlay.nix           # Build overlay
pyproject.toml          # Python project config
flake.nix              # Nix flake entry point
schema.yaml            # LinkML schema definition
```

## License

Apache 2.0
