---
name: classdiagram-image-to-json
description: Convert hand-drawn or modeling tool-created UML class diagrams (JPEG, PNG, PDF) into domain-model.json format with multi-language OCR support (Japanese/English text recognition). Enables modelers to create/edit class diagrams visually and integrate them into the UML workflow. Supports merging with existing models. Automatically detects and processes Japanese entity names.
---

# Class Diagram Image to JSON Converter

Convert visual UML class diagrams (from images or PDFs) into structured domain-model.json format for integration with uml-workflow-v2.

## Overview

This skill enables modelers to:
1. Create or edit UML class diagrams using their preferred modeling tool (Eclipse Papyrus, Draw.io, Lucidchart, etc.)
2. Export the diagram as an image (JPEG, PNG) or PDF
3. Convert it to domain-model.json format
4. Integrate with the UML workflow pipeline

### Key Features

- **Multi-format support**: JPEG, PNG, PDF
- **Comprehensive extraction**: Classes, attributes, methods, relationships
- **Merge capability**: Update existing domain-model.json or create new
- **Validation**: Ensures JSON structure compliance
- **UML workflow integration**: Seamless Step 5.5 addition
- **Multi-language OCR**: Japanese and English text recognition ⭐ NEW!
- **Automatic japanese_name generation**: Detected Japanese names preserved ⭐ NEW!

---

## Language Support ⭐ NEW!

### Overview

Recognizes both Japanese and English text in class diagrams using advanced OCR. Automatically generates appropriate entity names and japanese_name attributes.

**Supported Text:**
- **Japanese**: Hiragana, Katakana, Kanji
- **English**: Latin characters
- **Mixed**: Japanese + English in same diagram

### OCR Processing

**When Japanese text detected:**
```json
{
  "name": "ReceivedOrder",           // Auto-romanized
  "japanese_name": "受注",           // Original detected text
  "original_text": "受注"            // Raw OCR result
}
```

**When English text detected:**
```json
{
  "name": "ReceivedOrder",
  "japanese_name": "ReceivedOrder",  // Same as name
  "original_text": "ReceivedOrder"
}
```

**Best practice**: Use English for class names even in Japanese diagrams for code compatibility.

---

## When to Use This Skill

### Primary Use Cases

1. **Manual class diagram creation**
   - User prefers visual modeling tools over code
   - Complex domain requires visual design
   - Team collaboration via shared diagram tools

2. **Model refinement workflow**
   - Auto-generated class diagram needs visual editing
   - After Step 5 (usecase-to-class-v1), refine diagram manually
   - Re-import refined diagram to update JSON

3. **Legacy model migration**
   - Existing class diagrams from previous projects
   - Need to convert to uml-workflow-v2 format

4. **Educational scenarios**
   - Students learn by drawing diagrams
   - Convert hand-drawn sketches to formal models

### Trigger Patterns

Use this skill when user says:
- "I've created a class diagram in [tool], can you convert it to JSON?"
- "Here's a screenshot of my class diagram, update the domain model"
- "I edited the class diagram manually, please update domain-model.json"
- "Convert this PDF class diagram to the workflow format"

---

## Workflow Integration

### Position in uml-workflow-v2

```
Step 5: usecase-to-class-v1
  ↓ (generates domain-model.json automatically)
Step 5.5: classdiagram-image-to-json ⭐ (OPTIONAL)
  ↓ (if user wants to manually edit and re-import)
Step 6: usecase-to-sequence-v1
  ↓ (continues normal workflow)
```

### Integration Patterns

**Pattern A: Replace Step 5**
```
User provides class diagram directly
  ↓ classdiagram-image-to-json
domain-model.json created
  ↓ Continue to Step 6
```

**Pattern B: Refine after Step 5**
```
Step 5: Auto-generate domain-model.json
  ↓ Export diagram, edit in modeling tool
User uploads refined diagram
  ↓ classdiagram-image-to-json (merge mode)
domain-model.json updated
  ↓ Continue to Step 6
```

**Pattern C: Start from existing diagram**
```
User has legacy class diagram
  ↓ classdiagram-image-to-json
domain-model.json created
  ↓ Start workflow from Step 6
```

---

## Execution Process

### Step 1: Input Validation

1. **Confirm file is uploaded**
   - Check file exists in /mnt/user-data/uploads
   - Verify format: JPEG, PNG, or PDF

2. **Analyze image quality**
   - Ensure diagram is readable
   - Check for text clarity
   - Warn if quality is poor

### Step 2: Diagram Analysis

Extract the following UML elements:

#### 2.1 Classes
```
For each class box:
- Class name
- Stereotype (if any): <<entity>>, <<service>>, <<value object>>
- Modifiers: abstract, interface
```

#### 2.2 Attributes
```
For each attribute:
- Name
- Type
- Visibility: + (public), - (private), # (protected), ~ (package)
- Multiplicity: [0..1], [0..*], etc.
- Default value (if shown)
- Constraints: {unique}, {required}, etc.
```

#### 2.3 Methods
```
For each method:
- Name
- Return type
- Parameters: name, type
- Visibility
- Stereotype: <<constructor>>, <<query>>, <<command>>
```

#### 2.4 Relationships
```
For each relationship:
- Type: association, aggregation, composition, generalization, realization
- Source class
- Target class
- Source multiplicity
- Target multiplicity
- Role names (if shown)
- Association name (if shown)
- Direction: unidirectional, bidirectional
```

### Step 3: JSON Structure Generation

#### 3.1 Standard domain-model.json Format

```json
{
  "entities": [
    {
      "name": "ClassName",
      "description": "Description from notes or comments",
      "attributes": [
        {
          "name": "attributeName",
          "type": "String",
          "description": "Attribute description",
          "required": true,
          "unique": false,
          "defaultValue": null
        }
      ],
      "methods": [
        {
          "name": "methodName",
          "returnType": "void",
          "parameters": [
            {
              "name": "paramName",
              "type": "String"
            }
          ],
          "description": "Method description"
        }
      ]
    }
  ],
  "relationships": [
    {
      "type": "association|aggregation|composition|generalization|realization",
      "source": "SourceClass",
      "target": "TargetClass",
      "sourceMultiplicity": "1",
      "targetMultiplicity": "0..*",
      "sourceName": "role1",
      "targetName": "role2",
      "description": "Relationship description"
    }
  ],
  "enums": [
    {
      "name": "EnumName",
      "values": ["VALUE1", "VALUE2"],
      "description": "Enum description"
    }
  ],
  "valueObjects": [
    {
      "name": "ValueObjectName",
      "attributes": [...],
      "description": "Value object description"
    }
  ]
}
```

#### 3.2 Mapping Rules

**Class Types:**
- `<<entity>>` → entities array
- `<<value object>>` → valueObjects array
- `<<enumeration>>` → enums array
- `<<interface>>` or `<<abstract>>` → include in entities with metadata

**Attribute Types:**
- Map UML types to JSON-compatible types
- Preserve constraints: {unique}, {required}, {id}
- Handle composite types: Address, Money, etc.

**Relationship Types:**
- `─────>` → association (unidirectional)
- `<────>` → association (bidirectional)
- `◇─────>` → aggregation
- `◆─────>` → composition
- `─────▷` → generalization (inheritance)
- `- - - ▷` → realization (interface implementation)

**Multiplicity:**
- `1` → exactly one
- `0..1` → optional
- `*` or `0..*` → many
- `1..*` → one or more
- `n..m` → specific range

### Step 4: Merge or Create

#### 4.1 Create Mode (No existing JSON)

```bash
# Save as new domain-model.json
/home/claude/domain-model.json
```

#### 4.2 Merge Mode (Existing JSON found)

Ask user:
```
Found existing domain-model.json. How to proceed?
1. Replace entirely (discard existing)
2. Merge (add new, update existing, keep unchanged)
3. Review changes first (show diff)
```

**Merge Logic:**
```
For each entity in new diagram:
  If entity exists in old JSON:
    Update attributes/methods
  Else:
    Add as new entity

For relationships:
  Replace all (relationships are structural)

Preserve metadata:
  - Creation timestamp
  - Version info
  - Custom annotations
```

### Step 5: Validation

Check JSON structure:
1. Valid JSON syntax
2. Required fields present
3. Type consistency
4. Relationship references valid
5. No circular generalization

### Step 6: Output Generation

1. **Save JSON**
   ```bash
   cp /home/claude/domain-model.json /mnt/user-data/outputs/domain-model.json
   ```

2. **Generate PlantUML** (optional)
   ```bash
   # Call json-to-models to regenerate diagrams
   python /home/claude/json_to_plantuml.py
   ```

3. **Create summary report**
   - Entities extracted: X
   - Relationships: Y
   - Changes made (if merge)

---

## Detailed Analysis Guidelines

### Image Reading Best Practices

1. **Text Extraction**
   ```
   Look for:
   - Class names in box headers
   - Attribute declarations: visibility name : Type
   - Method signatures: visibility name(params) : ReturnType
   - Relationship labels and multiplicities
   ```

2. **Relationship Direction**
   ```
   Arrow indicators:
   - Solid line: association
   - Diamond (hollow): aggregation
   - Diamond (filled): composition
   - Triangle (hollow): generalization
   - Triangle (hollow, dashed line): realization
   ```

3. **Stereotype Recognition**
   ```
   Common stereotypes:
   <<entity>>, <<service>>, <<repository>>, <<controller>>
   <<value object>>, <<aggregate root>>, <<factory>>
   <<interface>>, <<abstract>>, <<enumeration>>
   ```

4. **Constraint Notation**
   ```
   Look for:
   {unique}, {id}, {required}, {immutable}
   {ordered}, {sorted}, {readonly}
   OCL constraints: context, inv, pre, post
   ```

### Handling Ambiguity

**If unclear:**
1. Make reasonable assumptions based on UML conventions
2. Add `"note"` field to JSON with assumptions made
3. Ask user for clarification on critical elements
4. Provide confidence level for extracted information

**Priority ranking:**
1. Class names (must be correct)
2. Relationships (structural integrity)
3. Attribute names and types (business logic)
4. Method signatures (implementation detail)
5. Descriptions/comments (documentation)

---

## Error Handling

### Common Issues

1. **Poor image quality**
   ```
   Solution: Request higher resolution image
   Fallback: Extract what's readable, mark unclear items
   ```

2. **Inconsistent notation**
   ```
   Solution: Interpret based on standard UML 2.5
   Note: Document non-standard notation used
   ```

3. **Incomplete diagram**
   ```
   Solution: Extract available information
   Warning: Indicate missing elements
   ```

4. **Conflicting relationships**
   ```
   Solution: Ask user which interpretation is correct
   Default: Choose most restrictive interpretation
   ```

### Validation Errors

If JSON validation fails:
1. Report specific errors
2. Provide corrected JSON
3. Explain what was fixed
4. Ask user to verify

---

## Examples

### Example 1: Simple Domain Model

**Input:** PNG screenshot from Draw.io

**Extracted:**
```json
{
  "entities": [
    {
      "name": "Customer",
      "description": "Represents a customer in the system",
      "attributes": [
        {
          "name": "customerId",
          "type": "String",
          "required": true,
          "unique": true
        },
        {
          "name": "name",
          "type": "String",
          "required": true
        },
        {
          "name": "email",
          "type": "String",
          "required": true,
          "unique": true
        }
      ]
    },
    {
      "name": "Order",
      "description": "Represents a customer order",
      "attributes": [
        {
          "name": "orderId",
          "type": "String",
          "required": true,
          "unique": true
        },
        {
          "name": "orderDate",
          "type": "Date",
          "required": true
        },
        {
          "name": "totalAmount",
          "type": "Number",
          "required": true
        }
      ]
    }
  ],
  "relationships": [
    {
      "type": "association",
      "source": "Customer",
      "target": "Order",
      "sourceMultiplicity": "1",
      "targetMultiplicity": "0..*",
      "targetName": "orders",
      "description": "A customer can place multiple orders"
    }
  ]
}
```

### Example 2: Merge with Existing Model

**Scenario:**
- Existing domain-model.json has Customer, Order
- User adds Product class in diagram
- User modifies Order to add productItems relationship

**Merge result:**
```
Added:
- Product entity
- Order-Product relationship

Modified:
- Order.attributes (added productItems)

Preserved:
- Existing Customer definition
- Original metadata
```

---

## Integration with json-to-models

After generating domain-model.json, optionally call json-to-models to:
1. Generate PlantUML diagrams
2. Create XMI for Eclipse Papyrus
3. Generate Markdown documentation

```bash
# Regenerate all model artifacts
python /home/claude/json_to_models.py
```

---

## Best Practices

### For Users

1. **Image quality matters**
   - Use high resolution (at least 1200px width)
   - Ensure text is clearly readable
   - Avoid compression artifacts

2. **Follow UML conventions**
   - Use standard notation
   - Label relationships clearly
   - Include multiplicities

3. **Provide context**
   - Add notes or comments to diagram
   - Use stereotypes consistently
   - Group related classes

4. **Iterative refinement**
   - Start simple, add details incrementally
   - Validate each version
   - Keep diagram organized

### For Claude

1. **Be explicit about assumptions**
   - Document what was interpreted
   - Ask for clarification when needed
   - Provide confidence levels

2. **Preserve information**
   - Don't discard any visible details
   - Include notes in JSON metadata
   - Maintain relationship semantics

3. **Validate thoroughly**
   - Check JSON structure
   - Verify relationship consistency
   - Test with downstream tools

4. **Clear communication**
   - Explain what was extracted
   - Show before/after for merges
   - Warn about potential issues

---

## Advanced Features

### Handling Complex Diagrams

1. **Multiple inheritance**
   ```json
   {
     "relationships": [
       {
         "type": "generalization",
         "source": "ConcreteClass",
         "target": "Interface1"
       },
       {
         "type": "generalization",
         "source": "ConcreteClass",
         "target": "Interface2"
       }
     ]
   }
   ```

2. **Association classes**
   ```json
   {
     "entities": [
       {
         "name": "Enrollment",
         "stereotype": "association_class",
         "attributes": [...]
       }
     ],
     "relationships": [
       {
         "type": "association",
         "source": "Student",
         "target": "Course",
         "associationClass": "Enrollment"
       }
     ]
   }
   ```

3. **Qualified associations**
   ```json
   {
     "relationships": [
       {
         "type": "association",
         "source": "Bank",
         "target": "Account",
         "qualifier": {
           "name": "accountNumber",
           "type": "String"
         }
       }
     ]
   }
   ```

### OCL Constraints Support

If diagram includes OCL constraints:
```json
{
  "entities": [
    {
      "name": "Person",
      "attributes": [...],
      "constraints": [
        {
          "type": "invariant",
          "name": "validAge",
          "expression": "age >= 0 and age <= 150"
        }
      ]
    }
  ]
}
```

---

## Troubleshooting

### Issue: Cannot read text from image

**Cause:** Low resolution, compression artifacts, or handwriting

**Solutions:**
1. Request user to re-export at higher resolution
2. Ask user to re-create diagram in digital tool
3. Request typed list of classes/attributes if critical

### Issue: Ambiguous relationship type

**Cause:** Non-standard arrow notation

**Solutions:**
1. Interpret based on UML 2.5 standard
2. Ask user to clarify
3. Document assumption in JSON note

### Issue: Merge conflicts

**Cause:** Same entity with different definitions

**Solutions:**
1. Show diff to user
2. Ask which version to keep
3. Offer manual merge option

### Issue: Invalid JSON generated

**Cause:** Extraction errors, malformed structure

**Solutions:**
1. Fix automatically if possible
2. Report error location
3. Request user validation

---

## Success Metrics

**Quality indicators:**
- 100% of classes extracted correctly
- 95%+ of relationships captured accurately
- All multiplicities preserved
- Stereotypes and constraints included

**User satisfaction:**
- Reduces manual JSON writing time by 80%
- Enables visual-first modeling workflow
- Seamless integration with existing tools
- Minimal manual corrections needed

---

## Limitations

1. **Handwritten diagrams**: May have lower accuracy
2. **Complex layouts**: Crossing lines may confuse extraction
3. **Custom notation**: Non-standard UML may require interpretation
4. **Diagram quality**: Depends on image resolution and clarity

---

## Future Enhancements

1. **Support more formats**: XMI, MDJ (StarUML), VSDX (Visio)
2. **Interactive refinement**: Web interface for corrections
3. **Batch processing**: Multiple diagrams at once
4. **Version control**: Track diagram evolution
5. **AI-assisted cleanup**: Auto-fix common mistakes

---

## Summary

This skill bridges visual modeling and the uml-workflow-v2 pipeline, enabling:
- Modelers to work in their preferred tools
- Manual refinement of auto-generated diagrams
- Integration of legacy class diagrams
- Flexible, hybrid modeling workflows

**Result:** Best of both worlds - visual design tools + automated code generation.
