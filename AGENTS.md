# Syntagmax VS Code Extension

## Project Overview
This project is a VS Code extension for the **Syntagmax DSL**. It provides syntax highlighting and language intelligence (completions, linting) using a Language Server Protocol (LSP) architecture.

### Architecture
- **Client**: TypeScript-based VS Code extension (`src/extension.ts`).
- **Server**: Python-based Language Server (`server/server.py`) using `pygls` and `lark`.
- **Syntax Highlighting**: TextMate grammar defined in `syntagmax.tmLanguage.json`.

## Building and Running

### Prerequisites
- [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/)
- [Python 3.x](https://www.python.org/)
- [VS Code](https://code.visualstudio.com/)

### Installation
1.  Navigate to the extension directory:
    ```bash
    cd syntagmax-vscode
    ```
2.  Install Node dependencies:
    ```bash
    npm install
    ```
3.  Install Python dependencies:
    ```bash
    pip install pygls lark
    ```

### Compilation
Compile the TypeScript code:
```bash
npm run compile
```
Or use the watch mode:
```bash
npm run watch
```

### Launching the Extension
1.  Open the `syntagmax-vscode` folder in VS Code.
2.  Press `F5` (or go to the **Run and Debug** view and select **Launch Extension**).
3.  A new **Extension Development Host** window will open with the extension loaded.

## Development Conventions

### Language Definition
- **Language ID**: `syntagmax`
- **Extensions**: `.stmx`, `.syntagmax`
- **Grammar Scope**: `source.syntagmax`

### Coding Style
- **Client**: TypeScript with strict typing. Follow standard VS Code extension patterns.
- **Server**: Python using `pygls`. Ensure the Lark grammar in `server.py` stays in sync with the official Syntagmax metamodel.

### Key Files
- `package.json`: Extension manifest and configuration.
- `syntagmax.tmLanguage.json`: Syntax highlighting rules.
- `language-configuration.json`: Brackets, comments, and indentation rules.
- `src/extension.ts`: Client-side activation and LSP client setup.
- `server/server.py`: Python LSP implementation (Diagnostics & Completion).
- `tsconfig.json`: TypeScript compiler configuration.
