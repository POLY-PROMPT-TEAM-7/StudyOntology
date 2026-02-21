from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )

    @model_serializer(mode='wrap', when_used='unless-none')
    def treat_empty_lists_as_none(
            self, handler: SerializerFunctionWrapHandler,
            info: SerializationInfo) -> dict[str, Any]:
        if info.exclude_none:
            _instance = self.model_copy()
            for field, field_info in type(_instance).model_fields.items():
                if getattr(_instance, field) == [] and not(
                        field_info.is_required()):
                    setattr(_instance, field, None)
        else:
            _instance = self
        return handler(_instance, info)



class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'study',
     'default_range': 'string',
     'description': 'LinkML schema for extracted knowledge entities and '
                    'relationships.',
     'id': 'https://w3id.org/study-ontology/',
     'imports': ['linkml:types'],
     'license': 'APACHE 2.0',
     'name': 'StudyOntology',
     'prefixes': {'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'study': {'prefix_prefix': 'study',
                            'prefix_reference': 'https://w3id.org/study-ontology/'}},
     'source_file': 'schema.yaml'} )

class RelationshipType(str, Enum):
    """
    Types of relationships between knowledge entities.
    """
    PREREQUISITE_OF = "PREREQUISITE_OF"
    """
    Subject must be learned before object.
    """
    EXAMPLE_OF = "EXAMPLE_OF"
    """
    Subject is a concrete instance or example of object.
    """
    CONTRASTS_WITH = "CONTRASTS_WITH"
    """
    Subject is similar to but meaningfully different from object.
    """
    LOCATED_IN = "LOCATED_IN"
    """
    Subject is found within or part of object.
    """
    PRODUCES = "PRODUCES"
    """
    Subject creates object as output.
    """
    CONSUMES = "CONSUMES"
    """
    Subject uses object as input.
    """
    APPLIES_TO = "APPLIES_TO"
    """
    Theory or method subject applies to domain or concept object.
    """
    ASSESSED_BY = "ASSESSED_BY"
    """
    Subject concept or theory is assessed by object assignment.
    """
    COVERS = "COVERS"
    """
    Subject assignment covers or tests object concept, theory, or method.
    """


class DifficultyLevel(str, Enum):
    """
    Difficulty level for learning a concept.
    """
    INTRODUCTORY = "INTRODUCTORY"
    """
    Suitable for beginners with no prerequisites.
    """
    INTERMEDIATE = "INTERMEDIATE"
    """
    Requires some foundational knowledge.
    """
    ADVANCED = "ADVANCED"
    """
    Requires significant prior knowledge.
    """
    EXPERT = "EXPERT"
    """
    Research-level or specialized content.
    """


class DocumentOrigin(str, Enum):
    """
    How the source document entered the system.
    """
    USER_UPLOAD = "USER_UPLOAD"
    """
    Manually uploaded by the user through the application UI.
    """
    CANVAS_API = "CANVAS_API"
    """
    Automatically fetched from the Canvas LMS API.
    """
    WEB_SCRAPE = "WEB_SCRAPE"
    """
    Scraped or downloaded from a web URL.
    """
    MANUAL_ENTRY = "MANUAL_ENTRY"
    """
    Content entered directly as text by the user.
    """


class AssignmentType(str, Enum):
    """
    Type of assignment from Canvas or user-defined.
    """
    HOMEWORK = "HOMEWORK"
    """
    Regular homework or problem set.
    """
    QUIZ = "QUIZ"
    """
    Quiz or short assessment.
    """
    EXAM = "EXAM"
    """
    Midterm, final, or other major exam.
    """
    PROJECT = "PROJECT"
    """
    Project or long-form deliverable.
    """
    DISCUSSION = "DISCUSSION"
    """
    Discussion board post or participation assignment.
    """
    LAB = "LAB"
    """
    Laboratory assignment or report.
    """
    ESSAY = "ESSAY"
    """
    Written essay or paper.
    """
    OTHER = "OTHER"
    """
    Any other assignment type.
    """



class KnowledgeEntity(ConfiguredBaseModel):
    """
    Abstract base for all knowledge graph entities.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'schema:Thing',
         'close_mappings': ['skos:Concept'],
         'from_schema': 'https://w3id.org/study-ontology/'})

    id: str = Field(default=..., description="""Unique identifier for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument']} })
    name: str = Field(default=..., description="""Human-readable name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'], 'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'],
         'slot_uri': 'schema:description'} })
    aliases: Optional[list[str]] = Field(default=[], description="""Alternative names or synonyms.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity'], 'exact_mappings': ['schema:alternateName']} })
    sources: Optional[list[ExtractionProvenance]] = Field(default=[], description="""Provenance records for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity']} })


class Concept(KnowledgeEntity):
    """
    A core idea, principle, or topic within a subject domain.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept', 'from_schema': 'https://w3id.org/study-ontology/'})

    domain: Optional[str] = Field(default=None, description="""Academic domain this concept belongs to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept', 'Theory', 'Method']} })
    difficulty_level: Optional[DifficultyLevel] = Field(default=None, description="""How advanced this concept is.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept']} })
    field: Optional[str] = Field(default=None, description="""Specific field within the domain.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept', 'Person']} })
    prerequisites: Optional[list[str]] = Field(default=[], description="""Concepts that should be learned before this one.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept']} })
    prerequisite_of: Optional[list[str]] = Field(default=[], description="""Concepts that depend on this concept.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept']} })
    related_theories: Optional[list[str]] = Field(default=[], description="""Theories that explain or involve this concept.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept']} })
    related_methods: Optional[list[str]] = Field(default=[], description="""Methods that apply to or use this concept.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept']} })
    id: str = Field(default=..., description="""Unique identifier for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument']} })
    name: str = Field(default=..., description="""Human-readable name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'], 'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'],
         'slot_uri': 'schema:description'} })
    aliases: Optional[list[str]] = Field(default=[], description="""Alternative names or synonyms.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity'], 'exact_mappings': ['schema:alternateName']} })
    sources: Optional[list[ExtractionProvenance]] = Field(default=[], description="""Provenance records for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity']} })


class Theory(KnowledgeEntity):
    """
    A scientific or academic framework, model, or paradigm.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:ScholarlyArticle',
         'close_mappings': ['schema:Theory'],
         'from_schema': 'https://w3id.org/study-ontology/'})

    domain: Optional[str] = Field(default=None, description="""Academic domain of this theory.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept', 'Theory', 'Method']} })
    key_figures: Optional[list[str]] = Field(default=[], description="""People who developed or contributed to this theory.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Theory']} })
    year_proposed: Optional[int] = Field(default=None, description="""Year the theory was first proposed or published.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Theory']} })
    key_concepts: Optional[list[str]] = Field(default=[], description="""Core concepts explained by this theory.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Theory']} })
    id: str = Field(default=..., description="""Unique identifier for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument']} })
    name: str = Field(default=..., description="""Human-readable name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'], 'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'],
         'slot_uri': 'schema:description'} })
    aliases: Optional[list[str]] = Field(default=[], description="""Alternative names or synonyms.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity'], 'exact_mappings': ['schema:alternateName']} })
    sources: Optional[list[ExtractionProvenance]] = Field(default=[], description="""Provenance records for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity']} })


class Person(KnowledgeEntity):
    """
    A researcher, scientist, or notable figure in an academic domain.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Person',
         'from_schema': 'https://w3id.org/study-ontology/'})

    birth_year: Optional[int] = Field(default=None, description="""Year of birth.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person']} })
    death_year: Optional[int] = Field(default=None, description="""Year of death if applicable.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person']} })
    field: Optional[str] = Field(default=None, description="""Primary academic field of the person.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept', 'Person']} })
    affiliation: Optional[str] = Field(default=None, description="""Institution or organization the person is associated with.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'schema:affiliation'} })
    notable_contributions: Optional[list[str]] = Field(default=[], description="""Key theories or concepts this person contributed to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person']} })
    id: str = Field(default=..., description="""Unique identifier for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument']} })
    name: str = Field(default=..., description="""Human-readable name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'], 'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'],
         'slot_uri': 'schema:description'} })
    aliases: Optional[list[str]] = Field(default=[], description="""Alternative names or synonyms.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity'], 'exact_mappings': ['schema:alternateName']} })
    sources: Optional[list[ExtractionProvenance]] = Field(default=[], description="""Provenance records for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity']} })


class Method(KnowledgeEntity):
    """
    A technique, process, or procedure used in academic practice.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/study-ontology/'})

    domain: Optional[str] = Field(default=None, description="""Academic domain where this method is used.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Concept', 'Theory', 'Method']} })
    inputs: Optional[list[str]] = Field(default=[], description="""What this method requires as input.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Method']} })
    outputs: Optional[list[str]] = Field(default=[], description="""What this method produces as output.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Method']} })
    equipment: Optional[list[str]] = Field(default=[], description="""Equipment or tools needed for this method.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Method']} })
    related_concepts: Optional[list[str]] = Field(default=[], description="""Concepts this method operates on or produces.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Method']} })
    id: str = Field(default=..., description="""Unique identifier for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument']} })
    name: str = Field(default=..., description="""Human-readable name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'], 'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'],
         'slot_uri': 'schema:description'} })
    aliases: Optional[list[str]] = Field(default=[], description="""Alternative names or synonyms.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity'], 'exact_mappings': ['schema:alternateName']} })
    sources: Optional[list[ExtractionProvenance]] = Field(default=[], description="""Provenance records for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity']} })


class Assignment(KnowledgeEntity):
    """
    A coursework assignment, exam, quiz, or project — typically sourced from Canvas LMS.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/study-ontology/'})

    assignment_type: Optional[AssignmentType] = Field(default=None, description="""The category of assignment.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    course_name: Optional[str] = Field(default=None, description="""Name of the course this assignment belongs to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    course_id: Optional[str] = Field(default=None, description="""Canvas course ID or other LMS identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    canvas_assignment_id: Optional[int] = Field(default=None, description="""The assignment ID from the Canvas API.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    due_date: Optional[datetime ] = Field(default=None, description="""When the assignment is due.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    points_possible: Optional[float] = Field(default=None, description="""Maximum points available for this assignment.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    submission_types: Optional[list[str]] = Field(default=[], description="""Allowed submission formats (e.g., online_upload, online_text_entry).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    is_published: Optional[bool] = Field(default=None, description="""Whether the assignment is visible to students in Canvas.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    html_url: Optional[str] = Field(default=None, description="""Direct link to the assignment in Canvas.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    covers_concepts: Optional[list[str]] = Field(default=[], description="""Concepts that this assignment tests or covers.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    covers_theories: Optional[list[str]] = Field(default=[], description="""Theories that this assignment tests or covers.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    covers_methods: Optional[list[str]] = Field(default=[], description="""Methods that this assignment tests or covers.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assignment']} })
    id: str = Field(default=..., description="""Unique identifier for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument']} })
    name: str = Field(default=..., description="""Human-readable name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'], 'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'],
         'slot_uri': 'schema:description'} })
    aliases: Optional[list[str]] = Field(default=[], description="""Alternative names or synonyms.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity'], 'exact_mappings': ['schema:alternateName']} })
    sources: Optional[list[ExtractionProvenance]] = Field(default=[], description="""Provenance records for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity']} })


class SourceDocument(ConfiguredBaseModel):
    """
    A source document from which knowledge was extracted.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:DigitalDocument',
         'from_schema': 'https://w3id.org/study-ontology/'})

    id: str = Field(default=..., description="""Unique identifier for the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument']} })
    name: str = Field(default=..., description="""Human-readable name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'], 'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Detailed description of the entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeEntity', 'SourceDocument'],
         'slot_uri': 'schema:description'} })
    document_type: Optional[str] = Field(default=None, description="""Type of document such as PDF, slides, notes, textbook.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SourceDocument']} })
    file_path: Optional[str] = Field(default=None, description="""Path or URL to the source document.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SourceDocument']} })
    upload_date: Optional[datetime ] = Field(default=None, description="""When the document was added to the system.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SourceDocument']} })
    page_count: Optional[int] = Field(default=None, description="""Total number of pages in the document.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['SourceDocument']} })
    origin: DocumentOrigin = Field(default=..., description="""How this document entered the system (user upload, Canvas API, etc.).""", json_schema_extra = { "linkml_meta": {'domain_of': ['SourceDocument']} })
    canvas_file_id: Optional[int] = Field(default=None, description="""File ID from the Canvas API, if sourced from Canvas.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SourceDocument']} })
    canvas_course_id: Optional[str] = Field(default=None, description="""Canvas course ID this document belongs to, if sourced from Canvas.""", json_schema_extra = { "linkml_meta": {'domain_of': ['SourceDocument']} })


class ExtractionProvenance(ConfiguredBaseModel):
    """
    Provenance record tracking where and how knowledge was extracted.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dcterms:ProvenanceStatement',
         'from_schema': 'https://w3id.org/study-ontology/'})

    source_document: str = Field(default=..., description="""Reference to the source document.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionProvenance', 'ExtractionResult']} })
    section_title: Optional[str] = Field(default=None, description="""Title of the section where the knowledge was found.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionProvenance']} })
    page_number: Optional[int] = Field(default=None, description="""Page number in the source document.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionProvenance']} })
    extraction_timestamp: Optional[datetime ] = Field(default=None, description="""When this extraction was performed.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionProvenance', 'ExtractionResult']} })
    extraction_method: Optional[str] = Field(default=None, description="""Method used for extraction.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionProvenance']} })
    raw_text: Optional[str] = Field(default=None, description="""Original text snippet from which knowledge was extracted.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionProvenance']} })


class KnowledgeRelationship(ConfiguredBaseModel):
    """
    A directed relationship between two knowledge entities as a triple with metadata.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/study-ontology/'})

    subject: str = Field(default=..., description="""The source entity in the relationship.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeRelationship']} })
    predicate: RelationshipType = Field(default=..., description="""The type of relationship.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeRelationship']} })
    object: str = Field(default=..., description="""The target entity in the relationship.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeRelationship']} })
    confidence: float = Field(default=..., description="""Confidence score from 0.0 to 1.0.""", ge=0.0, le=1.0, json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeRelationship']} })
    provenance: Optional[ExtractionProvenance] = Field(default=None, description="""Where and how this relationship was extracted.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeRelationship']} })
    notes: Optional[str] = Field(default=None, description="""Additional context or explanation for this relationship.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeRelationship']} })


class ExtractionResult(ConfiguredBaseModel):
    """
    Container for the output of a single extraction run from a source document.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/study-ontology/'})

    source_document: SourceDocument = Field(default=..., description="""The document that was processed.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionProvenance', 'ExtractionResult']} })
    extracted_entities: Optional[list[KnowledgeEntity]] = Field(default=[], description="""Entities extracted in this run.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionResult']} })
    extracted_relationships: Optional[list[KnowledgeRelationship]] = Field(default=[], description="""Relationships extracted in this run.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionResult']} })
    extraction_timestamp: Optional[datetime ] = Field(default=None, description="""When this extraction was performed.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionProvenance', 'ExtractionResult']} })
    model_version: Optional[str] = Field(default=None, description="""Version of the model used for extraction.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExtractionResult']} })


class KnowledgeGraph(ConfiguredBaseModel):
    """
    Root container for the entire knowledge graph.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/study-ontology/', 'tree_root': True})

    concepts: Optional[list[Concept]] = Field(default=[], description="""Concept entities in the graph.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeGraph']} })
    theories: Optional[list[Theory]] = Field(default=[], description="""Theory entities in the graph.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeGraph']} })
    persons: Optional[list[Person]] = Field(default=[], description="""Person entities in the graph.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeGraph']} })
    methods: Optional[list[Method]] = Field(default=[], description="""Method entities in the graph.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeGraph']} })
    assignments: Optional[list[Assignment]] = Field(default=[], description="""Assignment entities in the graph.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeGraph']} })
    relationships: Optional[list[KnowledgeRelationship]] = Field(default=[], description="""Relationship triples in the graph.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeGraph']} })
    source_documents: Optional[list[SourceDocument]] = Field(default=[], description="""Source documents referenced by extracted knowledge.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KnowledgeGraph']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
KnowledgeEntity.model_rebuild()
Concept.model_rebuild()
Theory.model_rebuild()
Person.model_rebuild()
Method.model_rebuild()
Assignment.model_rebuild()
SourceDocument.model_rebuild()
ExtractionProvenance.model_rebuild()
KnowledgeRelationship.model_rebuild()
ExtractionResult.model_rebuild()
KnowledgeGraph.model_rebuild()
