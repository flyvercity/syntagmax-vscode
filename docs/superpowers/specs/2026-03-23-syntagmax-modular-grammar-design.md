# Design Spec: Syntagmax Modular DSL Grammar Update (v2)

## 1. Overview
The Syntagmax Domain Specific Language (DSL) is being updated to a more modular architecture. The grammar is being separated into a dedicated `.lark` file to improve maintainability and support the new features, including a dedicated `id` rule and trace modes.

## 2. Goals
- Move grammar to a separate `server/syntagmax.lark` file.
- Update `server/server.py` to load from this file.
- Implement the new DSL features (`id` rule, `as` schema, `multiple` attributes).
- Update TextMate grammar for correct syntax highlighting.
- Update `test.stmx` to demonstrate new syntax.

## 3. Architecture
- **Grammar Definition:** `server/syntagmax.lark` (Lark format).
- **LSP Server:** `server/server.py` (Python, loading from `server/syntagmax.lark`).
- **Syntax Highlighting:** `syntagmax.tmLanguage.json` (JSON).

## 4. Proposed Changes

### 4.1. Grammar (`server/syntagmax.lark`)
The grammar will be:
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

### 4.2. LSP Server (`server/server.py`)
- Load `GRAMMAR` from `server/syntagmax.lark`.
- Update `completions` to include `id`, `as`.

### 4.3. Syntax Highlighting (`syntagmax.tmLanguage.json`)
- Add `id`, `as` to `keyword.control.syntagmax`.

### 4.4. Test File (`test.stmx`)
- Update `attribute id is mandatory string` to `id is string`.
- Update `trace from TEST to REQ or SRC is mandatory via commit`.

## 5. Verification Plan
- **Test Script:** `test_parser.py` will verify that `test.stmx` parses correctly with the new modular grammar.
- **Diagnostics:** Manually verify diagnostics in VS Code using the Extension Development Host.
- **Completions:** Verify `id` and `as` appear in the completions list.
