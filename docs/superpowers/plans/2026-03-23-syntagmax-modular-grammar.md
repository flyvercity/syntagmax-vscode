# Syntagmax Modular DSL Grammar Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the Syntagmax VS Code extension to use a modular grammar architecture and support new DSL features (id rule, as schema, multiple attributes).

**Architecture:** Move the Lark grammar definition to a separate file (`server/syntagmax.lark`) and update the LSP server (`server/server.py`) to load it dynamically. Update syntax highlighting and test samples.

**Tech Stack:** Python (pygls, Lark), JSON (TextMate Grammar).

---

### Task 1: Create Modular Grammar File

**Files:**
- Create: `server/syntagmax.lark`

- [ ] **Step 1: Create the grammar file**
Create `server/syntagmax.lark` with the following content:
```lark
start: (artifact | trace | _NL)+

artifact: ARTIFACT name ":" _NL _INDENT (rule | _NL)* _DEDENT
rule: "attribute" name "is" PRESENCE [MULTIPLE] type _NL
    | "id" "is" type ["as" schema_value] _NL

trace: "trace" "from" name "to" target_list "is" PRESENCE ["via" TRACE_MODE] _NL
target_list: name ("or" name)*

?type: "string" -> type_string
     | "integer" -> type_integer
     | "boolean" -> type_boolean
     | "reference" to_parent? -> type_reference
     | "enum" "[" value ("," value)* "]" -> type_enum

to_parent: "to" "parent"

?schema_value: ESCAPED_STRING | SCHEMA
ARTIFACT: "artifact"
MULTIPLE: "multiple"
SCHEMA: /[^ \t\n\r"]+/
?name: WORD
PRESENCE: "mandatory" | "optional"
TRACE_MODE: "commit" | "timestamp"
?value: ESCAPED_STRING | WORD

%import common.WORD
%import common.ESCAPED_STRING
%import common.WS_INLINE
%import common.SH_COMMENT
%ignore WS_INLINE
%ignore SH_COMMENT

%declare _INDENT _DEDENT
_NL: /(\r?\n[\t ]*)+/
```

- [ ] **Step 2: Verify grammar file exists**
Run: `ls server/syntagmax.lark`
Expected: `server/syntagmax.lark`

### Task 2: Update LSP Server to Load Grammar

**Files:**
- Modify: `server/server.py`

- [ ] **Step 1: Modify `server/server.py` to load grammar from file**
Update `server/server.py` to import `Path` and load the grammar:

```python
import os
from pathlib import Path

# ... existing imports ...

# Load grammar from file
GRAMMAR_PATH = Path(__file__).parent / "syntagmax.lark"
with open(GRAMMAR_PATH, "r") as f:
    GRAMMAR = f.read()

# ... existing parser initialization ...
```

- [ ] **Step 2: Update `completions` function**
Add `id` and `as` to the `items` list in `completions` function:
```python
@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(ls, params: CompletionParams):
    items = [
        # ... existing items ...
        CompletionItem(label="id"),
        CompletionItem(label="as"),
        # ... other items ...
    ]
```

- [ ] **Step 3: Verify server parses correctly**
Run: `python -m server.server` (just to check if it starts without syntax/grammar errors)
Expected: No immediate crash (it will wait for IO)

### Task 3: Update Syntax Highlighting

**Files:**
- Modify: `syntagmax.tmLanguage.json`

- [ ] **Step 1: Add new keywords to TextMate grammar**
Update `syntagmax.tmLanguage.json` to include `id` and `as` in the keywords list.

```json
{
    "name": "keyword.control.syntagmax",
    "match": "\\b(artifact|attribute|is|trace|from|to|or|via|id|as)\\b"
}
```

- [ ] **Step 2: Verify JSON syntax**
Run: `python -c "import json; json.load(open('syntagmax.tmLanguage.json'))"`
Expected: No errors.

### Task 4: Update Test Sample and Verify

**Files:**
- Modify: `test.stmx`
- Run: `test_parser.py`

- [ ] **Step 1: Update `test.stmx`**
Change `attribute id is mandatory string` to `id is string` in `test.stmx`.

- [ ] **Step 2: Run parser test**
Run: `python test_parser.py`
Expected: `Parsing successful!`

- [ ] **Step 3: Cleanup any temporary files**
Expected: `test_parser.py` passes.
