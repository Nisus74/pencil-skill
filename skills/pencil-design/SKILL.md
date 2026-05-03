---
name: pencil-design
description: Use this skill for any pencil.dev work — designing UI in a .pen file, editing an open Pencil canvas, sketching or mocking screens, instantiating components from a .lib.pen library, scaffolding a project's design-system/ folder, fixing batch_design schema errors, or recovering from Pencil MCP host-not-connected issues. Pick it on any mention of pencil.dev, .pen, .lib.pen, "the Pencil MCP", "the Pencil canvas", or a design-system/ folder in a Pencil context — even when the user phrases it casually, mid-sentence, or doesn't name the tool. This is the canonical skill for all Pencil tasks; reach for it before any general design or frontend skill when Pencil signals are present.
license: MIT
compatibility: Any AI coding tool with the Pencil MCP server configured (Claude Code, Codex, Gemini CLI, Copilot CLI, Cursor)
metadata:
  version: "1.1.0"
permissions:
  mcp:
    - pencil:get_editor_state
    - pencil:open_document
    - pencil:get_guidelines
    - pencil:batch_get
    - pencil:batch_design
    - pencil:snapshot_layout
    - pencil:get_screenshot
    - pencil:get_variables
    - pencil:set_variables
    - pencil:find_empty_space_on_canvas
    - pencil:search_all_unique_properties
    - pencil:replace_all_matching_properties
    - pencil:export_nodes
  shell: none
  filesystem: project-only  # reads ./design-system/ and writes scaffolded templates from skill assets
  network: none
---

# Pencil.dev Design Skill

<!-- PLACEHOLDER: Full skill content to be written in a future session. -->

## Platform Note

This skill is platform-agnostic. Tool names below use Claude Code conventions by default.
For tool-name mappings on other platforms, see:

- **OpenAI Codex**: `references/codex-tools.md`
- **Google Gemini CLI**: `references/gemini-tools.md`
- **GitHub Copilot CLI**: `references/copilot-tools.md`

Cursor uses the Pencil MCP server directly — the MCP tool names are identical across all platforms.

## Prerequisites

- Pencil MCP server must be configured in your AI coding tool's environment
- A `.pen` file must be open or accessible via the Pencil MCP tools

## Core Principle

`.pen` files are encrypted. **Never use generic file-read tools (`Read`, `Grep`, `cat`, etc.)
on `.pen` files.** Always use the Pencil MCP tools listed below.

## Available Pencil MCP Tools

| Tool | Purpose |
|------|---------|
| `get_editor_state` | Get current state of the open document |
| `open_document` | Open a `.pen` file |
| `get_guidelines` | Retrieve design guidelines for the document |
| `batch_get` | Read multiple nodes at once |
| `batch_design` | Write or modify design nodes |
| `snapshot_layout` | Capture a layout snapshot |
| `get_screenshot` | Get a visual screenshot of the current design |
| `get_variables` | Read design tokens / variables |
| `set_variables` | Update design tokens / variables |
| `find_empty_space_on_canvas` | Locate available space on the canvas |
| `search_all_unique_properties` | Search across all design properties |
| `replace_all_matching_properties` | Bulk-replace a property across nodes |
| `export_nodes` | Export nodes to an external format |

## Workflow

<!-- TODO: Step-by-step design workflow to be written. -->

## Tool Sequencing

<!-- TODO: Document required tool order (e.g., always call get_editor_state before batch_design). -->
