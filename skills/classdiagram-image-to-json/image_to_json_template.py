#!/usr/bin/env python3
"""
Class Diagram Image to JSON Converter - Reference Template

This script provides a template for converting class diagram images to domain-model.json.
Claude AI will use this as a reference when analyzing images.
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# ============================================================================
# Data Classes for Domain Model
# ============================================================================

@dataclass
class Attribute:
    """Represents a class attribute"""
    name: str
    type: str
    description: str = ""
    required: bool = False
    unique: bool = False
    defaultValue: Optional[Any] = None
    
    def to_dict(self) -> Dict:
        result = {
            "name": self.name,
            "type": self.type,
            "required": self.required
        }
        if self.description:
            result["description"] = self.description
        if self.unique:
            result["unique"] = self.unique
        if self.defaultValue is not None:
            result["defaultValue"] = self.defaultValue
        return result


@dataclass
class Parameter:
    """Represents a method parameter"""
    name: str
    type: str
    
    def to_dict(self) -> Dict:
        return {"name": self.name, "type": self.type}


@dataclass
class Method:
    """Represents a class method"""
    name: str
    returnType: str
    parameters: List[Parameter]
    description: str = ""
    
    def to_dict(self) -> Dict:
        result = {
            "name": self.name,
            "returnType": self.returnType,
            "parameters": [p.to_dict() for p in self.parameters]
        }
        if self.description:
            result["description"] = self.description
        return result


@dataclass
class Entity:
    """Represents a domain entity (class)"""
    name: str
    description: str = ""
    attributes: List[Attribute] = None
    methods: List[Method] = None
    stereotype: str = ""
    isAbstract: bool = False
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = []
        if self.methods is None:
            self.methods = []
    
    def to_dict(self) -> Dict:
        result = {
            "name": self.name,
            "attributes": [a.to_dict() for a in self.attributes]
        }
        if self.description:
            result["description"] = self.description
        if self.methods:
            result["methods"] = [m.to_dict() for m in self.methods]
        if self.stereotype:
            result["stereotype"] = self.stereotype
        if self.isAbstract:
            result["isAbstract"] = self.isAbstract
        return result


@dataclass
class Relationship:
    """Represents a relationship between entities"""
    type: str  # association, aggregation, composition, generalization, realization
    source: str
    target: str
    sourceMultiplicity: str = "1"
    targetMultiplicity: str = "1"
    sourceName: str = ""
    targetName: str = ""
    description: str = ""
    
    def to_dict(self) -> Dict:
        result = {
            "type": self.type,
            "source": self.source,
            "target": self.target,
            "sourceMultiplicity": self.sourceMultiplicity,
            "targetMultiplicity": self.targetMultiplicity
        }
        if self.sourceName:
            result["sourceName"] = self.sourceName
        if self.targetName:
            result["targetName"] = self.targetName
        if self.description:
            result["description"] = self.description
        return result


@dataclass
class Enum:
    """Represents an enumeration"""
    name: str
    values: List[str]
    description: str = ""
    
    def to_dict(self) -> Dict:
        result = {
            "name": self.name,
            "values": self.values
        }
        if self.description:
            result["description"] = self.description
        return result


@dataclass
class ValueObject:
    """Represents a value object"""
    name: str
    attributes: List[Attribute]
    description: str = ""
    
    def to_dict(self) -> Dict:
        result = {
            "name": self.name,
            "attributes": [a.to_dict() for a in self.attributes]
        }
        if self.description:
            result["description"] = self.description
        return result


@dataclass
class DomainModel:
    """Complete domain model"""
    entities: List[Entity] = None
    relationships: List[Relationship] = None
    enums: List[Enum] = None
    valueObjects: List[ValueObject] = None
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = []
        if self.relationships is None:
            self.relationships = []
        if self.enums is None:
            self.enums = []
        if self.valueObjects is None:
            self.valueObjects = []
    
    def to_dict(self) -> Dict:
        result = {}
        if self.entities:
            result["entities"] = [e.to_dict() for e in self.entities]
        if self.relationships:
            result["relationships"] = [r.to_dict() for r in self.relationships]
        if self.enums:
            result["enums"] = [e.to_dict() for e in self.enums]
        if self.valueObjects:
            result["valueObjects"] = [v.to_dict() for v in self.valueObjects]
        return result


# ============================================================================
# Image Analysis Guidelines (for Claude AI reference)
# ============================================================================

IMAGE_ANALYSIS_GUIDE = """
When analyzing class diagram images, follow these steps:

1. IDENTIFY CLASSES
   - Look for rectangular boxes
   - Top section contains class name
   - Optional stereotype in <<...>> notation above class name
   - Abstract classes may be in italic or have {abstract} tag

2. EXTRACT ATTRIBUTES
   Format: [visibility] name : type [multiplicity] [= defaultValue]
   Visibility symbols:
   + public
   - private
   # protected
   ~ package
   
   Example: "- customerId : String {unique}"
   → name: "customerId", type: "String", unique: true, required: true

3. EXTRACT METHODS
   Format: [visibility] name([parameter : type, ...]) : returnType
   
   Example: "+ calculateTotal(items : OrderItem[]) : Number"
   → name: "calculateTotal"
     parameters: [{name: "items", type: "OrderItem[]"}]
     returnType: "Number"

4. IDENTIFY RELATIONSHIPS
   
   Association: ────────>
   - Solid line with optional arrow
   - Multiplicity on both ends: 1, 0..1, *, 0..*, 1..*
   - Role names near each end
   
   Aggregation: ◇────────>
   - Hollow diamond on "whole" side
   - Represents "has-a" relationship (weak)
   
   Composition: ◆────────>
   - Filled diamond on "whole" side
   - Represents "owns" relationship (strong)
   - Parts cannot exist independently
   
   Generalization: ────────▷
   - Hollow triangle points to parent/superclass
   - Represents inheritance (is-a)
   
   Realization: ─ ─ ─ ─ ▷
   - Dashed line with hollow triangle
   - Represents interface implementation

5. HANDLE STEREOTYPES
   Common stereotypes:
   - <<entity>> → Add to entities array
   - <<value object>> → Add to valueObjects array
   - <<enumeration>> → Add to enums array
   - <<interface>> → Mark as interface type
   - <<service>>, <<repository>>, <<controller>> → Include as metadata

6. EXTRACT CONSTRAINTS
   Look for text in curly braces:
   - {unique} → unique: true
   - {required} → required: true
   - {id} → indicates primary key
   - {readonly} → constant value
   - {ordered}, {sorted} → collection properties

7. HANDLE AMBIGUITIES
   If unclear:
   - Use standard UML interpretations
   - Make reasonable assumptions
   - Document in "note" field
   - Ask user for critical clarifications

8. TYPE MAPPINGS
   UML Type → JSON Type
   - String, Text → "String"
   - Integer, Int → "Number"
   - Float, Double, Decimal → "Number"
   - Boolean, Bool → "Boolean"
   - Date, DateTime → "Date"
   - Array<T>, T[] → "Array" or "T[]"
   - Custom types → Keep as-is

9. MULTIPLICITY MAPPINGS
   UML → Interpretation
   - 1 → Exactly one (required)
   - 0..1 → Optional (not required)
   - * or 0..* → Array, can be empty
   - 1..* → Array, at least one required
   - n..m → Array with min/max constraints
"""

# ============================================================================
# Extraction Functions
# ============================================================================

def parse_attribute(attr_text: str) -> Attribute:
    """
    Parse attribute text into Attribute object.
    
    Format: [visibility] name : type [constraints]
    Example: "- email : String {unique, required}"
    """
    # This is a template - actual implementation would parse the text
    # Claude AI will analyze images directly and construct Attribute objects
    pass


def parse_method(method_text: str) -> Method:
    """
    Parse method text into Method object.
    
    Format: [visibility] name(params) : returnType
    Example: "+ calculateDiscount(amount : Number) : Number"
    """
    # This is a template - actual implementation would parse the text
    pass


def parse_relationship(rel_visual: str, rel_text: str) -> Relationship:
    """
    Parse relationship from visual elements and text.
    
    Visual indicators:
    - Arrow type (association, aggregation, composition, generalization)
    - Direction
    - Multiplicity labels
    - Role names
    """
    # This is a template - actual implementation would analyze visual elements
    pass


# ============================================================================
# Merge Functions
# ============================================================================

def merge_models(existing: DomainModel, new: DomainModel) -> DomainModel:
    """
    Merge new model into existing model.
    
    Rules:
    1. Add new entities not in existing
    2. Update existing entities with new definitions
    3. Replace all relationships (structural change)
    4. Merge enums and value objects
    """
    merged = DomainModel()
    
    # Create entity lookup for existing model
    existing_entities = {e.name: e for e in existing.entities}
    
    # Process new entities
    for new_entity in new.entities:
        if new_entity.name in existing_entities:
            # Update existing entity
            merged.entities.append(new_entity)
        else:
            # Add new entity
            merged.entities.append(new_entity)
    
    # Add entities that exist only in old model
    for old_entity in existing.entities:
        if not any(e.name == old_entity.name for e in new.entities):
            merged.entities.append(old_entity)
    
    # Replace relationships entirely (structural change)
    merged.relationships = new.relationships
    
    # Merge enums
    existing_enums = {e.name: e for e in existing.enums}
    for new_enum in new.enums:
        merged.enums.append(new_enum)
    for old_enum in existing.enums:
        if not any(e.name == old_enum.name for e in new.enums):
            merged.enums.append(old_enum)
    
    # Merge value objects
    existing_vos = {v.name: v for v in existing.valueObjects}
    for new_vo in new.valueObjects:
        merged.valueObjects.append(new_vo)
    for old_vo in existing.valueObjects:
        if not any(v.name == old_vo.name for v in new.valueObjects):
            merged.valueObjects.append(old_vo)
    
    return merged


# ============================================================================
# Validation Functions
# ============================================================================

def validate_model(model: DomainModel) -> List[str]:
    """
    Validate domain model for consistency.
    
    Returns list of validation errors (empty if valid).
    """
    errors = []
    
    # Check entity names are unique
    entity_names = [e.name for e in model.entities]
    duplicates = [name for name in entity_names if entity_names.count(name) > 1]
    if duplicates:
        errors.append(f"Duplicate entity names: {duplicates}")
    
    # Check relationship references
    all_names = entity_names + [e.name for e in model.enums] + [v.name for v in model.valueObjects]
    for rel in model.relationships:
        if rel.source not in all_names:
            errors.append(f"Relationship source '{rel.source}' not found in model")
        if rel.target not in all_names:
            errors.append(f"Relationship target '{rel.target}' not found in model")
    
    # Check for circular generalization
    # (Implementation would require graph traversal)
    
    return errors


# ============================================================================
# Main Conversion Function
# ============================================================================

def convert_image_to_json(
    image_path: str,
    output_path: str = "domain-model.json",
    merge_with_existing: bool = False,
    existing_path: str = None
) -> Dict:
    """
    Main function to convert class diagram image to domain-model.json.
    
    Args:
        image_path: Path to image file (JPEG, PNG, PDF)
        output_path: Path for output JSON file
        merge_with_existing: Whether to merge with existing model
        existing_path: Path to existing domain-model.json (if merging)
    
    Returns:
        Dictionary containing the domain model
    
    Note: This is a template. Claude AI will perform actual image analysis
    using its vision capabilities and construct the model directly.
    """
    
    # Step 1: Load and analyze image
    # (Claude AI will analyze image content directly)
    
    # Step 2: Extract model elements
    model = DomainModel()
    
    # Example extracted data (Claude will populate from actual image):
    """
    model.entities.append(Entity(
        name="Customer",
        description="Represents a customer",
        attributes=[
            Attribute("customerId", "String", required=True, unique=True),
            Attribute("name", "String", required=True),
            Attribute("email", "String", required=True, unique=True)
        ],
        methods=[
            Method("updateProfile", "void", [
                Parameter("newName", "String"),
                Parameter("newEmail", "String")
            ])
        ]
    ))
    """
    
    # Step 3: Merge if requested
    if merge_with_existing and existing_path:
        with open(existing_path, 'r') as f:
            existing_data = json.load(f)
        existing_model = DomainModel()  # Would populate from existing_data
        model = merge_models(existing_model, model)
    
    # Step 4: Validate
    errors = validate_model(model)
    if errors:
        print("Validation errors found:")
        for error in errors:
            print(f"  - {error}")
    
    # Step 5: Convert to JSON
    model_dict = model.to_dict()
    
    # Step 6: Save
    with open(output_path, 'w') as f:
        json.dump(model_dict, f, indent=2)
    
    return model_dict


# ============================================================================
# Example Usage (for reference)
# ============================================================================

if __name__ == "__main__":
    """
    Example usage - this shows how Claude would structure the conversion.
    
    Claude AI will:
    1. Analyze the uploaded image using vision capabilities
    2. Extract classes, attributes, methods, relationships
    3. Construct DomainModel object
    4. Convert to JSON format
    5. Save to domain-model.json
    """
    
    # Example 1: Create new model from image
    result = convert_image_to_json(
        image_path="/mnt/user-data/uploads/class-diagram.png",
        output_path="/home/claude/domain-model.json"
    )
    
    # Example 2: Merge with existing model
    result = convert_image_to_json(
        image_path="/mnt/user-data/uploads/updated-diagram.png",
        output_path="/home/claude/domain-model.json",
        merge_with_existing=True,
        existing_path="/home/claude/domain-model.json"
    )
    
    print(f"Domain model saved with {len(result.get('entities', []))} entities")
