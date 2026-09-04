# Hexastorm: Open-Hardware High-Resolution Laser Scanner

Hexastorm is an open-hardware high-resolution laser direct imager (LDI) and polygon laser scanner. It enables ultra-fast, high-precision scanning for direct laser lithography, PCB exposure, and precision optical inspection.

* **Technical Specification & Design Theory**: [Open hardware fast high resolution laser (RepRap Wiki)](https://reprap.org/wiki/Open_hardware_fast_high_resolution_LASER)
* **Control Electronics & Driver PCBs**: [firestarter (GitHub)](https://github.com/hstarmans/firestarter)
* **FreeCAD Workbench**: [freecad_hexastorm (GitHub)](https://github.com/hstarmans/freecad_hexastorm)
* **Optical Simulation Engine**: [opticaldesign (GitHub)](https://github.com/hstarmans/opticaldesign)

<p align="center">
  <img src="./Images/freecadpic.jpg" width="80%" alt="Hexastorm FreeCAD Assembly">
</p>

---

## Key Architecture & Features

* **High-Speed Rotating Polygon Prism**:
  * Precision multifaceted prism mirror driven by a compact integrated PCB motor (`mirrormotor.FCStd`).
* **Anamorphic Beam Conditioning Optics**:
  * Laser diode collimator mount with fine focus.
  * Astigmatic correction / wobble-compensating sagittal cylinder lens (CL1).
  * Field-flattening cylinder lens 2 (CL2).
* **Maxwell Kinematic Coupling (Detachable Toolhead)**:
  * A true 6-DOF athermal kinematic dock using 3 radial V-grooves on the scanhead PCB mating with 3 captive Ø 8.0 mm chrome steel spheres on the receiver dock.
  * 3 pairs of N52 neodymium magnets (Ø 8.0 mm × 1.0 mm) providing ~17 N of clamping force with a 0.40 mm non-contact air gap.
  * Universal 4x M2 bolt pattern (40.0 mm × 36.0 mm) allowing easy mounting to 3D-printed machine adapters (CNC 3018 Pro, Voron, 2020 extrusion, or spindle clamps).

---

## Repository Structure

```text
├── FreeCAD files/
│   ├── assembly_compact_new.FCStd   # Master optomechanical assembly
│   ├── mirrormotor.FCStd            # Polygon prism and PCB motor assembly
│   └── ArducamUC621/                # Camera calibration & beam profiling fixtures
├── Images/
│   └── freecadpic.jpg               # CAD overview render
├── pyproject.toml                   # Python environment dependencies (managed via uv)
├── AGENTS.md                        # CAD assistant & pair-programming guidelines
└── README.md
```

---

## CAD Environment & Requirements

### 1. Git LFS Requirement
This repository stores `.FCStd` CAD files and images using **Git Large File Storage (Git LFS)**. Ensure Git LFS is installed before cloning:

```bash
git lfs install
git clone https://github.com/hstarmans/hexastorm_design.git
```

*(If you already cloned without LFS, run `git lfs pull` inside the repository).*

### 2. FreeCAD Version & Workbenches
* **FreeCAD**: Version 1.0 or higher.
* **Workbenches / Addons**:
  * **Assembly** (FreeCAD 1.0 built-in)
  * **PartDesign**
  * **Fasteners Workbench**
  * **KiCad StepUp** (for PCB 3D integration)

### 3. Python Environment
Python tools and dependencies are managed using [`uv`](https://docs.astral.sh/uv/):

```bash
# Run any script with uv
uv run python <script.py>

# Add dependencies
uv add <package>
```

---

## Optical Simulation & Ray Tracing
Creating and tracing rays in FreeCAD is accomplished with `pyoptools` and the following libraries:
* **FreeCAD Workbench**: [freecad_hexastorm](https://github.com/hstarmans/freecad_hexastorm)
* **Prism & Polygon Simulation Library**: [opticaldesign](https://github.com/hstarmans/opticaldesign)

---

## Reference Videos
* [Assembly 4 Design Overview (Legacy)](https://youtu.be/jhr6iEazbQk)
* [Optical Simulation Walkthrough](https://youtu.be/kekMkjqzRjE)
