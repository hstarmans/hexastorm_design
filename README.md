# Hexastorm: Laser Scanner CAD

FreeCAD design files for **Hexastorm**, an open-hardware polygon laser direct imager (LDI) for PCB lithography and laser scanning.

* **Documentation & Theory**: [Open hardware fast high resolution laser (RepRap Wiki)](https://reprap.org/wiki/Open_hardware_fast_high_resolution_LASER)
* **Electronics & Firmware**: [firestarter (GitHub)](https://github.com/hstarmans/firestarter)
* **Optical Simulation**: [opticaldesign (GitHub)](https://github.com/hstarmans/opticaldesign)

<p align="center">
  <img src="./Images/freecadpic_base.png" width="48%" alt="Hexastorm Base Configuration (without cylinder lenses)">
  <img src="./Images/freecadpic.png" width="48%" alt="Hexastorm with Cylinder Lenses">
  <br>
  <em>Left: Base configuration (no cylinder lenses). Right: Configuration with CL1 saddle bridge and CL2 lens.</em>
</p>

---

## Design Overview

* **Optical Configurations (Base vs. Cylinder Lens Upgrade)**:

  * **Base (no cylinder lenses)**: Focussed beam goes directly from the laser diode through the polygon prism into a small spot. Lower component count, but results in an elliptical beam spot.
  * **With Cylinder Lenses**: Adding CL1 (mounted in saddle bridge `sk_bridge_pcb`) and CL2 circularizes the beam spot and optically cancels facet tilt errors from the rotating prism. The beam is collimated when it leaves the laserdiode.
* **Prism Drive & Motor Support**:

  * Typically, a refurbished sharp AR160 polygon mirror motor is used.
  * However, a  PCB motor (`mirrormotor.FCStd` / `pcbmotorasm`) with stator coils etched into PCB copper (driven by [firestarter](https://github.com/hstarmans/firestarter)) can also be used for laser scanning.

<p align="center">
  <img src="./Images/pcb_motor_view.png" width="75%" alt="Hexastorm Planar PCB Motor and Internal Layout">
</p>

* **Chassis**: Tab-and-slot FR4 PCB panels soldered at the seams.
* **Maxwell Kinematic Dock**:
  * Toolhead mount using 3 radial V-grooves on the scanhead PCB mating with 3 captive Ø 8.0 mm steel bearing balls on the dock base.
  * Clamped by 3 pairs of Ø 8.0 mm × 1.0 mm N52 magnets (~17 N pull, 0.40 mm magnet air gap).
  * PCB separation is 2.40 mm when docked.
  * Mates with [maxwell_dock.kicad_pcb](file:///home/hexastorm/Documents/hardware/firestarter/lasermodule/maxwell_dock/maxwell_dock/maxwell_dock.kicad_pcb). Mounting to a CNC 3018 or extrusion frame requires an adapter plate.

<p align="center">
  <img src="./Images/kinematic_dock_view.png" width="75%" alt="Hexastorm Maxwell Kinematic Dock Interface">
</p>

* **KiCad Integration**: Board outlines and aperture cutouts in FreeCAD sync directly to KiCad `Edge.Cuts` via KiCad StepUp.

---

## Repository Structure

```text
├── FreeCAD files/
│   ├── assembly_compact_new.FCStd   # Main assembly (FreeCAD 1.0)
│   ├── mirrormotor.FCStd            # Polygon prism and PCB motor assembly
│   └── ArducamUC621/                # Calibration & profiling fixtures
├── Images/
│   ├── freecadpic_base.png          # Base configuration (no cylinder lenses)
│   ├── freecadpic.png               # Configuration with cylinder lenses
│   ├── pcb_motor_view.png           # Internal layout with planar PCB motor and rotor
│   └── kinematic_dock_view.png      # Kinematic dock underside view
├── AGENTS.md                        # CAD assistant & pair-programming guidelines
└── README.md
```

---

## CAD Environment

### 1. Git LFS

This repository stores `.FCStd` files and images in Git LFS. Run before cloning:

```bash
git lfs install
git clone https://github.com/hstarmans/hexastorm_design.git
```

*(If cloned without LFS, run `git lfs pull` inside the repository).*

### 2. FreeCAD Requirements

* **FreeCAD**: 1.0 or higher.
* **Workbenches**:
  * Assembly (built-in FreeCAD 1.0)
  * PartDesign
  * Fasteners Workbench
  * KiCad StepUp

---

## Optical Simulation & Ray Tracing

Ray tracing and optical verification are handled by [opticaldesign](https://github.com/hstarmans/opticaldesign) (`pyoptools` and `prisms.cad_verifier`).

Run with FreeCAD open:

```bash
cd path/to/opticaldesign
uv run python -m prisms.cad_verifier
```

This traces rays through the diode, lenses, polygon facets, and mirror, and writes rays into FreeCAD under `Simulation/Rays`.

---

## Reference Videos

* [Assembly 4 Design Overview (Legacy)](https://youtu.be/jhr6iEazbQk)
* [Optical Simulation Walkthrough](https://youtu.be/kekMkjqzRjE)
