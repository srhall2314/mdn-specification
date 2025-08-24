# MDN AI Prompt Section Options

## Overview

The AI Prompt section is an **optional** addition to MDN files that helps AI systems understand the MDN format when they encounter it for the first time. This section can be removed once the MDN format becomes widely known and recognized by AI systems.

## Purpose

- **Format Education**: Teaches AI systems what MDN is and how to process it
- **Adoption Helper**: Reduces friction for AI tools encountering MDN for the first time
- **Self-Documenting**: Makes MDN files immediately understandable to new AI systems
- **Future-Proof**: Becomes less critical as MDN adoption grows

## Section Structure

```markdown
--- MDN:AI_PROMPT
# AI guidance content goes here
---
```

## Token Efficiency Options

### Option 1: Comprehensive (Recommended for Early Adoption)
**Token Count**: ~80-100 tokens
```markdown
--- MDN:AI_PROMPT
MDN: AI-optimized spreadsheet format
Structure: YAML header + CSV sheets + JSON formulas + optional format
Process: Parse YAML→extract CSV→apply formulas→apply format
Preserves: Excel business logic, relationships, calculations
Cell refs: SheetName!A1, ranges A1:B10, columns A:A
Linear: Top-to-bottom parsing, no nested structures
Version: 0.8.0
---
```

### Option 2: Standard (Balanced Information)
**Token Count**: ~50-60 tokens
```markdown
--- MDN:AI_PROMPT
MDN: AI spreadsheet format. YAML+CSV+JSON. Parse YAML→CSV→formulas→format. 
Cell refs: SheetName!A1, ranges A1:B10. Linear parsing, no nesting.
---
```

### Option 3: Minimal (Maximum Token Efficiency)
**Token Count**: ~25-30 tokens
```markdown
--- MDN:AI_PROMPT
MDN: AI spreadsheet. YAML→CSV→formulas→format. SheetName!A1 refs. Linear parse.
---
```

### Option 4: Ultra-Minimal (Extreme Token Efficiency)
**Token Count**: ~15-20 tokens
```markdown
--- MDN:AI_PROMPT
MDN: AI spreadsheet. YAML→CSV→formulas→format. SheetName!A1 refs. Linear.
---
```

## Token Efficiency Strategies

### 1. Remove Articles
- ❌ "the YAML header" → ✅ "YAML header"
- ❌ "a CSV sheet" → ✅ "CSV sheet"

### 2. Use Symbols
- ❌ "then" → ✅ "→"
- ❌ "plus" → ✅ "+"

### 3. Abbreviate Words
- ❌ "formatting" → ✅ "format"
- ❌ "business logic" → ✅ "logic"
- ❌ "relationships" → ✅ "rel"

### 4. Concise Verbs
- ❌ "How to process" → ✅ "Process"
- ❌ "Extract data from" → ✅ "Extract"

### 5. Eliminate Redundancy
- ❌ "Parse the YAML section, then extract CSV data from sheet sections" → ✅ "Parse YAML→CSV"

## Key Concepts for AI Systems

### Cell References
- **Sheet-specific**: `SheetName!A1` refers to cell A1 on specific sheet
- **Ranges**: `A1:B10` for rectangular ranges, `A:A` for entire columns
- **No ambiguity**: Multiple sheets can have same cell coordinates (e.g., A1 on Revenue vs A1 on Costs)

### Linear Parsing
- **Top-to-bottom**: Process sections in order: Header → Sheets → Formulas → Format → AI Prompt
- **No nesting**: Each section is self-contained, no complex hierarchical structures
- **Sequential access**: Can parse without jumping around or building complex data structures

### Section Processing Order
1. **YAML Header**: Extract metadata, sheet names, context
2. **CSV Sheets**: Parse tabular data for each sheet
3. **JSON Formulas**: Apply business logic to specific cells
4. **JSON Format**: Apply visual styling (optional)
5. **AI Prompt**: Understand format context (optional)

## Implementation Guidelines

### When to Include
- **New MDN files**: Include to help AI systems understand the format
- **Public repositories**: Include for broader AI accessibility
- **Documentation**: Include in examples and templates

### When to Omit
- **Internal use**: Once your AI tools recognize MDN
- **Known environments**: When working with familiar AI systems
- **Token optimization**: When maximum efficiency is needed

### Placement
- **Location**: After all other sections, before `END DOCUMENT`
- **Order**: Header → Sheets → Formulas → Format (optional) → AI Prompt (optional) → END

## Example Complete File

```markdown
--- MDN:HEADER YAML
source: budget.xlsx
version: 1.0
created: 2025-01-15T12:00:00Z
sheets:
  - Budget
---
--- MDN:SHEET CSV name=Budget
Category,Planned,Actual,Variance
Revenue,100000,95000,-5000
Expenses,80000,82000,2000
---
--- MDN:FORMULAS JSON
{
  "Budget!D2": "=C2-B2",
  "Budget!D3": "=C3-B3"
}
---
--- MDN:AI_PROMPT
MDN: AI spreadsheet. YAML→CSV→formulas→format. Excel logic preserved.
---
END DOCUMENT
```

## Future Considerations

### Auto-Removal
AI tools could automatically suggest removing this section once they:
- Recognize MDN format consistently
- Have built-in MDN processing capabilities
- No longer need format education

### Dynamic Content
The section could be customized based on:
- **Complexity**: More complex files get more detailed prompts
- **Use case**: Business vs. technical analysis prompts
- **Audience**: AI system type and capabilities

### Version Awareness
Include format version information to help AI systems:
- Use appropriate parsing logic
- Apply correct validation rules
- Handle format evolution gracefully

## Benefits

1. **Immediate Understanding**: AI systems can process MDN files without prior knowledge
2. **Reduced Friction**: Lower barrier to adoption for new AI tools
3. **Self-Documenting**: Files explain themselves to AI systems
4. **Token Efficient**: Minimal overhead while providing essential information
5. **Future-Proof**: Can be removed as format becomes standard

---

*This document outlines options for the optional AI Prompt section in the MDN format specification. Choose the option that best balances information needs with token efficiency requirements.*
