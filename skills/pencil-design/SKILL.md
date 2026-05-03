---
name: pencil-design
description: Use when the user asks to "design in pencil", "create a pencil.dev design", "open a .pen file", "work with pencil MCP", "generate UI in pencil", "edit a pencil design", "sketch a screen in pencil", "update a pencil component", or any task involving pencil.dev's design tool, the .pen file format, or the Pencil MCP server tools. Also use when the user asks you to read, inspect, or modify any file with a .pen extension.
version: 0.1.0
license: MIT
compatibility: Any AI coding tool with the Pencil MCP server configured (Claude Code, Codex, Gemini CLI, Copilot CLI, Cursor)
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
