# Agent Guidelines: Hexastorm FreeCAD Design Assistant

## Project Goal
Assist with the CAD modeling, assembly, and optical/mechanical design of **Hexastorm**, an open-hardware high-resolution laser scanner / laser direct imager.

## Primary Working File
- Main FreeCAD file: [FreeCAD files/assembly_compact_new.FCStd](file:///home/hexastorm/Documents/hardware/hexastorm_design/FreeCAD%20files/assembly_compact_new.FCStd)

## Collaboration & Workflow Guidelines
1. **Interactive User Editing in FreeCAD**:
   - The user actively opens, inspects, and edits the CAD model directly in FreeCAD.
   - The agent provides assistance on demand when the user requests help with design choices, dimensions, assembly constraints, troubleshooting, or Python scripting.
2. **MCP-Assisted Collaboration**:
   - Assist via the FreeCAD MCP (Model Context Protocol) connection to query object trees, inspect geometry, extract parameters, run FreeCAD Python snippets, or modify parts as requested.
   - Coordinate actions with the user's active FreeCAD session to ensure smooth interactive pair-designing without conflicting with unsaved local changes.
3. **Domain Context**:
   - **Mechanism**: High-speed optical scanning with a rotating polygon/prism mirror and compact optomechanics.
   - **Environment**: FreeCAD (v1.0+) with workbenches/plugins including Assembly4, PartDesign, Fasteners, KiCad StepUp, and pyoptools for optical simulation.
   - **Tooling & Environment**:
     - This repository is dedicated exclusively to FreeCAD CAD modeling and mechanical assets; do not create Python packages, venvs, or lockfiles here.
     - The FreeCAD MCP server runs standalone via `uvx freecad-mcp`.
     - Optical simulation, ray tracing, and Python tooling are maintained and run via `uv` in `opticaldesign`.
   - **Related Repositories & References**:
     - Open Hardware Wiki: [Open hardware fast high resolution laser](https://reprap.org/wiki/Open_hardware_fast_high_resolution_LASER)
     - PCB Electronics: [firestarter](https://github.com/hstarmans/firestarter)
     - Optical Simulation & CAD Verification: [opticaldesign](https://github.com/hstarmans/opticaldesign)

