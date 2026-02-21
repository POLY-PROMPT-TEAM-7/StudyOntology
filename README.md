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

The schema is defined in LinkML (YAML) and automatically generates Pydantic models for validation and type safety.

### Core Entity Types

All entities extend `KnowledgeEntity` with these base fields:
 `id`: Unique identifier
 `name`: Display name
 `description`: Optional detailed description
 `aliases`: Alternative names
 `sources`: Extraction provenance information

#### Concept
Core ideas and topics with academic metadata:
 `domain`: Subject area (e.g., "psychology", "neuroscience")
 `difficulty_level`: INTRODUCTORY, INTERMEDIATE, ADVANCED, or EXPERT
 `field`: Academic field
 `prerequisites`: List of prerequisite concept IDs
 `prerequisite_of`: List of concepts that depend on this one
 `related_theories`: Associated theoretical frameworks
 `related_methods`: Applicable research methods

#### Theory
Scientific frameworks and paradigms:
 `domain`: Subject area
 `key_figures`: Researchers who developed/advanced the theory
 `year_proposed`: Year of initial proposal
 `key_concepts`: Core concepts within the theory

#### Person
Researchers and notable figures:
 `birth_year`: Year of birth
 `death_year`: Year of death (if applicable)
 `field`: Primary research domain
 `affiliation`: Institution or organization
 `notable_contributions`: Key achievements

#### Method
Research techniques and procedures:
 `domain`: Applicable field
 `inputs`: Required inputs or materials
 `outputs`: Expected results or data
 `equipment`: Tools or apparatus needed
 `related_concepts`: Relevant theoretical concepts

#### Assignment
Course assignments linked to knowledge entities:
 `assignment_type`: HOMEWORK, QUIZ, EXAM, PROJECT, DISCUSSION, LAB, ESSAY, OTHER
 `course_name`, `course_id`: Course identification
 `canvas_assignment_id`: LMS integration ID
 `due_date`, `points_possible`: Assignment metadata
 `covers_concepts`, `covers_theories`, `covers_methods`: Knowledge coverage

### Relationship Types

Relationships connect entities through typed predicates:
 **prerequisite_of**: Must learn A before B
 **example_of**: A is a concrete instance of B
 **contrasts_with**: A is similar but different from B
 **located_in**: A is found within or part of B
 **produces**: A creates B as output
 **consumes**: A uses B as input
 **applies_to**: Theory or method applies to a domain
 **assessed_by**: Entity is evaluated through assignment
 **covers**: Assignment includes this entity

### Graph Structure

The `KnowledgeGraph` container holds:
 Collections: `concepts`, `theories`, `persons`, `methods`, `assignments`
 `relationships`: All entity connections
 `source_documents`: Original materials with provenance
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
lib/StudyOntology/
  __init__.py           # Package exports
  lib.py                # Generated Pydantic models from LinkML
  core.py               # Core functionality (TODO)
nix/                    # Nix configuration
  shell.nix             # Dev shell (flake8, pyright)
  overlay.nix           # Build overlay
pyproject.toml          # Python project config
flake.nix              # Nix flake entry point
schema.yaml            # LinkML schema definition
```

## Using the Pydantic Models

The Pydantic models are automatically generated from `schema.yaml` using LinkML:

```python
from lib.StudyOntology.lib import (
    Concept,
    Theory,
    Person,
    Method,
    Assignment,
    KnowledgeGraph,
    KnowledgeRelationship,
    RelationshipType,
    DifficultyLevel,
)

# Create a concept
working_memory = Concept(
    id="wm_001",
    name="Working Memory",
    description="Temporary storage system for cognitive processing",
    domain="cognitive_psychology",
    difficulty_level=DifficultyLevel.INTERMEDIATE,
    field="psychology",
    prerequisites=["attention_001", "stm_001"],
)

# Create a relationship
rel = KnowledgeRelationship(
    subject="wm_001",
    predicate=RelationshipType.PREREQUISITE_OF,
    object="executive_function_001",
    confidence=0.95,
)

# Build a knowledge graph
graph = KnowledgeGraph(
    concepts=[working_memory],
    relationships=[rel],
)
```

All models include:
- **Type safety**: Full type hints with Pyright validation
- **Validation**: Pydantic validation on instantiation
- **LinkML metadata**: Class URIs and slot URIs for semantic web integration
- **JSON schema**: Auto-generated schemas for API validation

## License

Apache 2.0
