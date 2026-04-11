# Syntagmax DSL Grammar Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the Syntagmax DSL grammar to support conditions, placeholders in schema values, and new rules.

**Architecture:** Update the Lark grammar file, then propagate keywords to the LSP server for completions and to the VS Code extension for syntax highlighting.

**Tech Stack:** Lark (grammar), pygls (LSP), VS Code TextMate (syntax highlighting).

---

### Task 1: Create Reproduction Test Case

**Files:**
- Create: `reproduce_new_features.stmx`
- Test: `test_parser.py`

- [ ] **Step 1: Create a test file with new DSL features**

```syntagmax
artifact SRC:
    id is string as "{atype}/{num}"
    attribute title is mandatory string if anchor
    attribute desc is optional string if not anchor

artifact REQ:
    id is string as "{atype}/{num:5}"
    attribute contents is mandatory string

trace from SRC to REQ is mandatory if anchor
trace from SRC to REQ or OTHER is optional if not anchor
```

- [ ] **Step 2: Run `test_parser.py` to verify it fails**

Run: `python test_parser.py` (ensure you're using the correct python environment)
Expected: FAIL with Lark parsing error.

- [ ] **Step 3: Commit**

```bash
git add reproduce_new_features.stmx
git commit -m "test: add reproduction case for new grammar features"
```

### Task 2: Update Grammar

**Files:**
- Modify: `server/syntagmax.lark`

- [ ] **Step 1: Apply the new grammar provided by the user**

```lark
start: (artifact | trace | _NL)+

artifact: ARTIFACT name ":" _NL _INDENT (rule | _NL)* _DEDENT
rule: "attribute" name "is" PRESENCE [MULTIPLE] type [condition] _NL
    | "id" "is" type ["as" schema_value] _NL

trace: "trace" "from" name "to" target_list "is" PRESENCE ["via" TRACE_MODE] [condition] _NL
target_list: name ("or" name)*

condition: "if" [NOT] anchor
anchor: WORD
NOT: "not"

?type: "string" -> type_string
     | "integer" -> type_integer
     | "boolean" -> type_boolean
     | "reference" to_parent? -> type_reference
     | "enum" "[" value ("," value)* "]" -> type_enum

to_parent: "to" "parent"

?schema_value: unquoted_items | quoted_items

unquoted_items: (SCHEMA_PART | PLACEHOLDER | INVALID_PLACEHOLDER)+
quoted_items: "\"" (QUOTED_PART | PLACEHOLDER | INVALID_PLACEHOLDER)* "\""

PLACEHOLDER: /\{(atype|num(:\d+)?)\}/
INVALID_PLACEHOLDER: /\{[^}]+\}/

SCHEMA_PART: /[^ \t\n\r"{]+/
QUOTED_PART: /[^"{]+/

ARTIFACT: "artifact"
MULTIPLE: "multiple"
%import common.INT
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

- [ ] **Step 2: Run `test_parser.py` with `reproduce_new_features.stmx`**

Run: `python test_parser.py`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add server/syntagmax.lark
git commit -m "feat(grammar): update DSL grammar to support conditions and placeholders"
```

### Task 3: Update LSP Completions

**Files:**
- Modify: `server/server.py`

- [ ] **Step 1: Add `if` and `not` to completions**

```python
# In completions function in server/server.py
    items = [
        # ... existing items
        CompletionItem(label="if"),
        CompletionItem(label="not"),
    ]
```

- [ ] **Step 2: Commit**

```bash
git add server/server.py
git commit -m "feat(lsp): add 'if' and 'not' to auto-completions"
```

### Task 4: Update Syntax Highlighting

**Files:**
- Modify: `syntagmax.tmLanguage.json`

- [ ] **Step 1: Add `if` and `not` to keywords**

```json
{
    "name": "keyword.control.syntagmax",
    "match": "\\b(artifact|attribute|is|trace|from|to|or|via|id|as|if|not)\\b"
}
```

- [ ] **Step 2: Add placeholder highlighting in strings and schema values**

```json
// Add to patterns or repository
{
    "name": "variable.other.placeholder.syntagmax",
    "match": "\\{(atype|num(:\\d+)?)\\}"
},
{
    "name": "invalid.illegal.placeholder.syntagmax",
    "match": "\\{[^}]+\\}"
}
```

- [ ] **Step 3: Commit**

```bash
git add syntagmax.tmLanguage.json
git commit -m "feat(syntax): update highlighting for conditions and placeholders"
```

### Task 5: Final Cleanup and Verification

**Files:**
- Modify: `test.stmx`
- Delete: `reproduce_new_features.stmx`

- [ ] **Step 1: Update `test.stmx` with representative examples of new features**

- [ ] **Step 2: Run final test**

Run: `python test_parser.py`
Expected: PASS

- [ ] **Step 3: Commit and Cleanup**

```bash
rm reproduce_new_features.stmx
git add test.stmx
git commit -m "test: update test.stmx with new DSL features"
```
