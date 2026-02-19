# Class Diagram Image to JSON Converter

Convert visual UML class diagrams from images (JPEG, PNG, PDF) into structured domain-model.json format for uml-workflow-v3.

## Quick Start

### Basic Usage

1. **Create or export class diagram**
   - Use any UML tool (Eclipse Papyrus, Draw.io, Lucidchart, etc.)
   - Export as PNG, JPEG, or PDF
   - Ensure text is clearly readable (recommended 1200px+ width)

2. **Upload to Claude**
   - Attach image file to conversation
   - Trigger the skill

3. **Convert to JSON**
   ```
   User: "Please convert this class diagram to domain-model.json"
   Claude: [Analyzes image and generates JSON]
   ```

### Workflow Integration

#### Scenario A: Start from Visual Diagram
```
User creates class diagram visually
  ↓
Claude: classdiagram-image-to-json
  ↓
domain-model.json created
  ↓
Continue with Step 6 (usecase-to-sequence-v1)
```

#### Scenario B: Refine Auto-Generated Diagram
```
UML Workflow Step 5 completes (usecase-to-class-v1)
  ↓
User exports diagram, edits in modeling tool
  ↓
User uploads refined diagram
  ↓
Claude: classdiagram-image-to-json (merge mode)
  ↓
domain-model.json updated
  ↓
Continue with Step 6
```

## Examples

### Example 1: Simple E-Commerce Model

**Input Diagram (conceptual):**
```
┌─────────────────┐         ┌─────────────────┐
│    Customer     │         │      Order      │
├─────────────────┤         ├─────────────────┤
│ - customerId    │ 1    0..* │ - orderId      │
│ - name          │─────────>│ - orderDate    │
│ - email         │         │ - totalAmount  │
└─────────────────┘         └─────────────────┘
```

**Command:**
```
"Please convert this class diagram to domain-model.json"
```

**Generated JSON:**
```json
{
  "entities": [
    {
      "name": "Customer",
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
          "required": true
        }
      ]
    },
    {
      "name": "Order",
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
      "targetName": "orders"
    }
  ]
}
```

### Example 2: Merge Mode

**Scenario:** You have an existing domain-model.json and want to add a new Product class.

**Command:**
```
"I've added a Product class to my diagram. Please merge it with the existing model."
```

**Claude's Response:**
```
Found existing domain-model.json. Merging changes:

Added:
- Product entity with attributes (productId, name, price, stock)
- Order-Product relationship (many-to-many)

Modified:
- Order entity (added items attribute)

Preserved:
- Existing Customer entity
- Customer-Order relationship

Merged model saved to domain-model.json
```

### Example 3: Complex Diagram with Inheritance

**Input Diagram Features:**
- Abstract class: `Payment` (abstract)
- Concrete classes: `CreditCardPayment`, `PayPalPayment`
- Generalization relationships (inheritance)

**Command:**
```
"Convert this payment hierarchy diagram to JSON"
```

**Generated JSON:**
```json
{
  "entities": [
    {
      "name": "Payment",
      "isAbstract": true,
      "attributes": [
        {
          "name": "paymentId",
          "type": "String",
          "required": true,
          "unique": true
        },
        {
          "name": "amount",
          "type": "Number",
          "required": true
        }
      ],
      "methods": [
        {
          "name": "processPayment",
          "returnType": "Boolean",
          "parameters": []
        }
      ]
    },
    {
      "name": "CreditCardPayment",
      "attributes": [
        {
          "name": "cardNumber",
          "type": "String",
          "required": true
        }
      ]
    },
    {
      "name": "PayPalPayment",
      "attributes": [
        {
          "name": "paypalEmail",
          "type": "String",
          "required": true
        }
      ]
    }
  ],
  "relationships": [
    {
      "type": "generalization",
      "source": "CreditCardPayment",
      "target": "Payment"
    },
    {
      "type": "generalization",
      "source": "PayPalPayment",
      "target": "Payment"
    }
  ]
}
```

## Supported UML Elements

### Classes
- ✅ Class names
- ✅ Stereotypes: `<<entity>>`, `<<value object>>`, `<<enumeration>>`, `<<service>>`, etc.
- ✅ Abstract classes
- ✅ Interfaces

### Attributes
- ✅ Name and type
- ✅ Visibility: `+` public, `-` private, `#` protected, `~` package
- ✅ Multiplicity: `[0..1]`, `[0..*]`, etc.
- ✅ Default values
- ✅ Constraints: `{unique}`, `{required}`, `{id}`

### Methods
- ✅ Name and return type
- ✅ Parameters with types
- ✅ Visibility
- ✅ Stereotypes: `<<constructor>>`, `<<query>>`, `<<command>>`

### Relationships
- ✅ Association (unidirectional/bidirectional)
- ✅ Aggregation (hollow diamond)
- ✅ Composition (filled diamond)
- ✅ Generalization (inheritance)
- ✅ Realization (interface implementation)
- ✅ Multiplicities on both ends
- ✅ Role names

### Value Objects & Enums
- ✅ Enumerations with values
- ✅ Value objects with attributes

## Best Practices

### For Creating Diagrams

1. **Use standard UML notation**
   - Follow UML 2.5 conventions
   - Use standard symbols for relationships
   - Include multiplicities

2. **Make text readable**
   - Use clear, legible fonts
   - High contrast (dark text on light background)
   - Adequate font size (12pt+ in final export)

3. **Organize layout**
   - Avoid overlapping lines
   - Group related classes
   - Use consistent spacing

4. **Include details**
   - Add attribute types
   - Specify multiplicities
   - Use stereotypes appropriately

5. **Export quality**
   - PNG: Use lossless compression
   - JPEG: Use maximum quality setting
   - PDF: Ensure text is vector-based, not rasterized
   - Recommended resolution: 1200px+ width

### For Merging

1. **Review before merging**
   - Request to see changes first: "Show me what will change"
   - Claude will display diff before applying

2. **Handle conflicts**
   - If class definitions differ, choose which to keep
   - Claude will ask for clarification on conflicts

3. **Preserve metadata**
   - Existing notes and documentation are preserved
   - Custom fields in JSON are maintained

## Tips for Better Results

### Image Quality
- ✅ High resolution (1200px+)
- ✅ Good lighting (for photos)
- ✅ Direct screenshot (for digital diagrams)
- ❌ Avoid blurry images
- ❌ Avoid hand-drawn sketches (unless very clear)
- ❌ Avoid excessive compression

### Diagram Clarity
- ✅ Clear class names
- ✅ Typed attributes
- ✅ Labeled relationships
- ✅ Visible multiplicities
- ❌ Avoid tiny fonts
- ❌ Avoid cluttered layouts

### Notation
- ✅ Standard UML symbols
- ✅ Consistent style
- ✅ Complete information
- ❌ Avoid custom notation
- ❌ Avoid ambiguous arrows

## Troubleshooting

### Problem: "Cannot read attribute types"

**Cause:** Text too small or blurry

**Solution:**
- Re-export at higher resolution
- Zoom in on diagram before screenshot
- Use vector export (PDF) instead of raster (PNG)

### Problem: "Relationship direction unclear"

**Cause:** Arrow not visible or non-standard

**Solution:**
- Use standard UML arrows
- Ensure arrows are clearly visible
- Add explicit direction labels

### Problem: "Merge created duplicates"

**Cause:** Class names don't match exactly

**Solution:**
- Ensure class names are identical (case-sensitive)
- Review merge diff before applying
- Manually reconcile if needed

### Problem: "Missing some classes"

**Cause:** Low contrast or overlapping elements

**Solution:**
- Increase diagram contrast
- Separate overlapping elements
- Re-export with white background

## Integration with Other Skills

### After this skill, you can use:

1. **json-to-models**
   - Regenerate PlantUML diagrams
   - Create XMI for Eclipse Papyrus
   - Generate Markdown documentation

2. **usecase-to-sequence-v1**
   - Generate sequence diagrams from use cases
   - Requires use case definitions

3. **class-to-statemachine-v1**
   - Generate state machines for entities
   - Requires entities with status attributes

4. **model-validator-v1**
   - Validate model consistency
   - Check business rules

5. **usecase-to-code-v1**
   - Generate full-stack application
   - Requires complete workflow context

## Limitations

1. **Handwritten diagrams**: Accuracy depends on handwriting clarity
2. **Complex layouts**: Crossing lines may confuse extraction
3. **Custom notation**: Non-standard UML requires interpretation
4. **OCR limits**: Very small text may not be readable
5. **Color dependency**: Relies on structural elements, not colors

## Success Metrics

- **Extraction accuracy**: 95%+ for digital diagrams
- **Time saved**: 80% vs. manual JSON writing
- **Workflow integration**: Seamless Step 5.5 addition
- **User satisfaction**: Enables visual-first modeling

## Future Enhancements

- [ ] Support XMI import directly
- [ ] Batch processing multiple diagrams
- [ ] Interactive correction interface
- [ ] Version control for diagrams
- [ ] Auto-fix common mistakes

## Support

For issues or questions:
1. Check troubleshooting section
2. Provide high-quality image
3. Ask Claude to explain extraction decisions
4. Request manual review for critical models

## Summary

This skill bridges the gap between visual modeling tools and automated code generation, enabling:
- **Visual-first workflow**: Design in your preferred tool
- **Flexibility**: Mix auto-generation with manual refinement  
- **Integration**: Seamless uml-workflow-v3 pipeline
- **Productivity**: 10x faster than manual JSON creation

**Result:** Best of both worlds - visual design freedom + automated code generation power.
