# NarupaTools Package

This package contains code to help interact with molecular dynamics simulations running within
the [Narupa framework](https://gitlab.com/intangiblerealities/narupa-protocol) and being viewed
with [Scivana](https://alexjbinnie.itch.io/scivana)

## Conversion Functions

Conversion functions from various MD packages to a Narupa FrameData are provided. These all take a set of fields, which
indicate which fields should be populated if available. This gives fine control over what is added to your frames, and
can help to avoid expensive calls such as accessing velocities or forces when not required.

|  | ASE Atoms | OpenMM State/Topology | MDTraj Trajectory/Topology | MDAnalysis Universe |
| --- | --- | --- | --- | --- | 
| Particle Positions | ✔ | ✔ | ✔ | ✔ |
| Particle Velocities | ✔ | ✔ | ❌ | ✔ |
| Particle Forces | ✔ | ✔ | ❌ | ✔ |
| Particle Masses | ✔ | ❌ | ❌ | ✔ |
| Particle Elements | ✔ | ✔ | ✔ | ✔ |
| Particle Names | ✔ | ✔ | ✔ | ✔ |
| Particle Residues | ✔ | ✔ | ✔ | ✔ |
| Particle Charges | ✔ | ❌ | ❌ | ✔ |
| Particle Count | ✔ | ✔ | ✔ | ✔ |
| Residue Names | ✔ | ✔ | ✔ | ✔ |
| Residue Chains | ❌ | ✔ | ✔ | ✔ |
| Residue Count | ✔ | ✔ | ✔ | ✔ |
| Chain Names | ❌ | ✔ | ✔ | ✔ |
| Chain Count | ❌ | ✔ | ✔ | ✔ |
| Bond Pairs | ❌ | ✔ | ✔ | ✔ |
| Bond Count | ❌ | ✔ | ✔ | ✔ |
| Potential Energy | ✔ | ✔ | ❌ | ❌ |
| Kinetic Energy | ✔ | ✔ | ❌ | ❌ |
| Box Vectors | ✔ | ✔ | ✔ | ✔ |