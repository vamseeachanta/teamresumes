# CV Recommendations — Power Generation Controls Design Engineer
**Candidate:** Geeta | **Date:** 2026-03-08
**Role family:** Power Generation Controls / Microgrid / Data Center Electrical

---

## 1. Gap Analysis

| JD Requirement | Current Resume | Rating |
|---|---|---|
| Generator controls & sequencing | Listed as competency; no platform names (ComAp, Woodward) | Partial |
| Paralleling logic / load-shed | Competency only — no project narrative | Partial |
| Microgrid control systems | Competency only — no design/commissioning narrative | Partial |
| MV switchgear controls | "high-voltage facilities" mentioned; no control philosophy | Partial |
| EPMS/BMS integration | Competency listed; zero supporting project evidence | Partial |
| Data center topologies (UPS, STS, N+1) | Not mentioned anywhere | **No** |
| Named PLC platforms (Allen-Bradley, Schneider, Woodward, ComAp) | "PLC Programming" only — no named platforms | Partial |
| Protocols: Modbus, DNP3, IEC 61850, GOOSE, OPC UA | Not mentioned anywhere | **No** |
| Black-start requirements | Absent | **No** |
| FAT/SAT/IST commissioning | "through commissioning" — no methodology detail | **No** |
| Cross-functional coordination (OEM/EPC/OE) | Strong — multiple roles confirm this | Yes |
| Python / automation | Strong — multiple concrete projects | Yes |
| Remote work + technical writing | Independent consulting confirms this | Yes |
| PE credential | In-progress | Partial |

**Critical gaps that will fail a technical screen:** communication protocols (Modbus/DNP3/IEC 61850),
data center topology knowledge, black-start requirements, FAT/SAT/IST commissioning detail,
and named PLC/controller platforms.

---

## 2. Resume Edit Recommendations

### 2.1 Professional Summary — Full Rewrite

**BEFORE:**
> Multidisciplinary electrical engineer with 16+ years of experience in power systems, controls design, and
> mission-critical infrastructure. Proven expertise in generator controls, microgrid systems, electrical
> design coordination, with cross-functional project management. Strong background with deep technical
> knowledge of protection systems, control platforms, and communication protocols for large-scale power
> generation facilities.

**AFTER:**
> Electrical engineer with 16+ years of experience in power generation controls, mission-critical
> infrastructure design, and industrial automation, specializing in generator sequencing, microgrid
> control systems, and EPMS/BMS integration for large-scale facilities. Proven delivery record
> coordinating multi-discipline electrical design across OEM, EPC, and consulting interfaces — from
> control philosophy development and I/O list generation through FAT/SAT/IST commissioning support.
> Technical depth spans PLC-based control systems, SCADA integration, Modbus/DNP3/IEC 61850
> communication architectures, and DER asset coordination including BESS and inverter-based generation.
> PE certification in progress; open-source engineering tools portfolio demonstrating applied generator
> paralleling logic, microgrid island-mode transition modeling, and EPMS data architecture.

*(Add GitHub link once repo projects are publicly visible)*

---

### 2.2 Core Competencies — Replace Entirely

**BEFORE:**
> Technical Documentation & Standards Development | Cross-Functional Design Coordination |
> Microgrid Control Systems | Generator Controls & Paralleling Logic | Switchgear Controls |
> EPMS/BMS Integration | PLC Programming | Interconnection Design | Protection Systems & Sequencing |
> Power Distribution Infrastructure

**AFTER:**
> Generator Controls & Paralleling Logic | Microgrid Control Systems & DER Integration |
> MV Switchgear Control Philosophy | Load-Shed & Black-Start Sequencing | EPMS/BMS Integration |
> Utility Interconnection & Protection Systems | Control Narratives & Standards Documentation |
> PLC/SCADA Design (Allen-Bradley, Schneider, SEL RTAC) | Communication Protocols (Modbus, DNP3, IEC 61850) |
> Cross-Functional Design Coordination (OEM/EPC/OE) | FAT/SAT/IST Commissioning Support |
> Mission-Critical Power Infrastructure

---

### 2.3 Technical Skills — Add Protocols Line

Add a new line under Technical Skills:

> **Power Controls & Protocols:** Modbus RTU/TCP, DNP3, OPC UA, IEC 61850/GOOSE, SEL RTAC,
> ComAp InteliGen, Woodward easYgen, Allen-Bradley ControlLogix, Schneider EcoStruxure

*Only list platforms where there is genuine familiarity — exposure-level is better than silence,
but do not claim deep hands-on where it does not exist.*

---

### 2.4 Specific Bullet Rewrites

#### Rig Project — Coordination Detail

**BEFORE:**
> Coordinated integration with existing high-voltage facilities including VFDs, transformers,
> and modernized control systems and instrumentation.

**AFTER:**
> Coordinated electrical integration across high-voltage distribution architecture including VFDs,
> step-down transformers, MCC panels, and generator control interfaces; defined control philosophy
> for sequenced load transfer and fault isolation aligned with facility uptime requirements.

---

#### Rig Project — Commissioning Methodology

**BEFORE:**
> Led electrical motor replacement and refurbishment for TESCO drilling rig in Houston, managing
> full project lifecycle from requirements definition through commissioning.

**AFTER:**
> Led full lifecycle delivery of electrical motor replacement — from requirements definition and
> vendor coordination through factory acceptance testing (FAT), site acceptance testing (SAT),
> and commissioning — ensuring integrated control system operability under live production conditions.

---

#### Instrumentation — Add Protocol Reference

**BEFORE:**
> Designed and implemented centralized instrumentation system for oil and gas drilling land rig
> with 10Hz data acquisition.

**AFTER:**
> Designed centralized SCADA-linked instrumentation system for a land drilling rig, integrating
> real-time 10Hz data acquisition with PLC-based control loops; architected Modbus RTU
> communications between field instruments and the supervisory layer.

*Only apply if Modbus (or another named protocol) was actually used — substitute the correct protocol.*

---

#### Digital Twin Platform — Reframe for EPMS Audience

**BEFORE:**
> Implemented automated FEA analysis platform for subsea assets using Python-driven workflows
> and ASCII data integration.

**AFTER:**
> Developed Python-based automated engineering analysis platform with modular plug-and-play
> architecture for near real-time data processing — demonstrating the configuration-driven I/O
> design patterns used in EPMS/BMS integration layers (Pandas, SciPy, SQLAlchemy,
> configurable processing engines and output interfaces).

---

#### Wind Turbine Role — Sharpen to DER/Interconnection

**BEFORE:**
> Consulting engineer supporting commercial, tender, and supply chain activities for offshore
> wind turbine lifecycle.

**AFTER:**
> Consulting engineer supporting commercial and technical activities for offshore wind turbine
> lifecycle, including evaluation of grid interconnection requirements, inverter-based DER asset
> specifications, and supplier qualification for BESS and power conversion systems across US
> offshore wind markets.

---

## 3. Repo Project Proposals

Build these modules in `digitalmodel/power/` to create verifiable, open-source technical evidence
directly aligned to the JD. Each module should include ≥10 unit tests and docstrings referencing
the applicable standard.

### Project 1 — `digitalmodel/power/protocols/scada_integration.py` *(Priority: Build First)*

**What it models:** Protocol simulation and data-mapping toolkit covering Modbus TCP/RTU,
DNP3 point mapping, OPC UA node modeling, and an EPMS data model with I/O list export.
Does not require live hardware — models the register maps, data types, scaling, and polling
architecture used in real SCADA/EPMS integrations.

**Key classes:**
```python
class ModbusRegisterMap:
    # from_csv(path) -> ModbusRegisterMap
    # get_holding_register(address: int) -> RegisterDefinition
    # scale_raw_to_engineering(raw: int, reg: RegisterDefinition) -> float
    # validate_map_consistency() -> list[ValidationError]

class DNP3PointList:
    # analog_inputs: list[DNP3Point]
    # binary_inputs: list[DNP3Point]
    # from_excel(path) -> DNP3PointList
    # export_to_ied_config_format() -> str  # SEL RTAC compatible

class OPCUANodeModel:
    # build_namespace(device_tree: dict) -> NodeSpace
    # export_to_xml() -> str  # importable to Ignition/Wonderware

class EPMSDataModel:
    # generator_points, switchgear_points, bms_points: list[EPMSPoint]
    # validate_against_template(template_path: str) -> ComplianceReport
    # generate_io_list(format: str) -> pd.DataFrame  # Excel-ready I/O list
```

**JD skills demonstrated:** Modbus, DNP3, OPC UA, EPMS/BMS integration, I/O list generation
(explicit JD deliverable), SCADA integration architecture.

**Estimated effort:** 15–20 hours | **Interview value:** High

---

### Project 2 — `digitalmodel/power/controls/generator_sequencing.py`

**What it models:** Deterministic state-machine for multi-generator paralleling and sequencing
logic per IEEE 1547 / NFPA 110. Models: crank → idle → rated → synchronization check →
breaker close → load transfer. Computes synchronization window compliance, dead-bus vs.
live-bus transfer logic, and priority-based load-shed thresholds.

**Key classes:**
```python
class GeneratorUnit:
    # State: OFFLINE | CRANKING | IDLE | RATED | SYNCHRONIZED | ONLINE
    # Parameters: rated_kw, rated_kva, pf, voltage_setpoint, freq_setpoint

class SynchronizationChecker:
    # check_voltage_match(v1, v2, tolerance_pct) -> bool
    # check_frequency_match(f1, f2, tolerance_hz) -> bool
    # check_phase_angle(angle_deg, window_deg) -> bool
    # is_synchronization_permissive() -> bool

class ParallelBusController:
    # add_generator(unit: GeneratorUnit)
    # compute_load_share(total_load_kw: float) -> dict[str, float]
    # execute_load_shed(priority_order: list, shed_threshold_kw: float)

class BlackStartSequencer:
    # define_critical_loads(load_list: list[Load])
    # run_black_start_sequence() -> SequenceLog
    # validate_sequence_against_nfpa110() -> ComplianceResult
```

**JD skills demonstrated:** Generator controls, paralleling logic, load-shed schemes,
black-start requirements, protection system integration — covers 5 of the JD's core
design coordination items directly.

**Estimated effort:** 20–30 hours | **Interview value:** High

---

### Project 3 — `digitalmodel/power/microgrid/microgrid_controller.py`

**What it models:** Rule-based microgrid energy management controller for grid-connected and
island-mode operation. Implements: mode switching logic, DER dispatch prioritization
(PV → BESS → genset merit order), BESS state-of-charge management, frequency/voltage droop
response, and island detection using ROCOF and vector shift thresholds.

**Key classes:**
```python
class MicrogridMode(Enum):
    GRID_CONNECTED | ISLANDED | TRANSITIONING | BLACK_START

class DERAsset:
    # Types: PV, BESS, GENSET, FUEL_CELL
    # dispatch_priority: int, rated_power_kw: float

class BESSController:
    # soc_pct: float
    # charge_rate_kw(target_soc, available_pv_kw) -> float
    # discharge_rate_kw(load_demand_kw, min_soc_pct) -> float

class IslandDetector:
    # compute_rocof(freq_history: list[float], window_s: float) -> float
    # check_vector_shift(phase_before, phase_after, threshold_deg) -> bool
    # anti_islanding_trip_required() -> bool

class MicrogridEMS:
    # dispatch_merit_order(load_kw: float) -> list[DERDispatch]
    # transition_to_island_mode() -> TransitionLog
    # transition_to_grid_connected() -> TransitionLog
```

**JD skills demonstrated:** Microgrid controller design, DER asset integration (BESS, PV,
fuel cells), inverter-based power systems, islanding detection (IEEE 1547.4), seamless
transfer logic.

**Estimated effort:** 25–35 hours | **Interview value:** High

---

### Project 4 — `digitalmodel/power/commissioning/test_sequence_validator.py`

**What it models:** FAT/SAT/IST test procedure generator and results validator for generator
and switchgear commissioning. Takes system configuration and outputs structured test steps
with pass/fail criteria, inter-step dependencies, safety interlocks, and punch list export.

**Key classes:**
```python
class CommissioningPhase(Enum):
    FAT | SAT | IST

class TestStep:
    # step_id, description, preconditions, action, acceptance_criteria
    # dependencies: list[str]

class GeneratorCommissioningSequence:
    # build_fat_sequence(gen_config) -> list[TestStep]
    # build_sat_sequence(site_config) -> list[TestStep]
    # build_ist_sequence(system_config) -> list[TestStep]

class TestResultsValidator:
    # load_results(csv_path) -> TestResults
    # validate_against_sequence(sequence) -> ValidationReport
    # export_punch_list(output_path)
```

**JD skills demonstrated:** FAT/SAT/IST commissioning support, testability design,
system verification methodology, technical documentation.

**Estimated effort:** 15–20 hours | **Interview value:** Medium-High

---

## 4. Priority Ranking

| Rank | Module | Est. Hours | Rationale |
|---|---|---|---|
| 1 | `scada_integration.py` (Protocols/EPMS) | 15–20 | Closes hardest gap at lowest effort; I/O list = literal JD deliverable |
| 2 | `generator_sequencing.py` | 20–30 | Primary JD responsibility — every technical screen will ask for sequencing evidence |
| 3 | `microgrid_controller.py` (DER/Island) | 25–35 | Differentiating — BESS/islanding elevates candidate above O&G-only engineers |
| 4 | `test_sequence_validator.py` | 15–20 | Rounds out commissioning gap; build last or optionally |

**Total effort:** 60–85 hours over 3–4 weeks to build a portfolio that directly answers every
technical screen question for this role family.

**Recommended build order:** Protocol toolkit → Generator sequencing → Microgrid EMS

Once Proposals 1–3 are publicly visible, add the GitHub link to the Professional Summary and
LinkedIn About section before applying to additional postings.

---

## 5. Additional Notes

- **PE credential:** If there is a projected completion date, state it explicitly
  ("PE certification expected [Month Year]") rather than "in progress" — it reads as more credible.
- **Data center exposure:** If any consulting work touched UPS systems, ATS, or generator-backed
  critical loads even indirectly, add a bullet — any data center topology language strengthens ATS scoring.
- **LinkedIn:** Mirror the updated Core Competencies as LinkedIn Skills. Recruiters for this
  role filter on "IEC 61850", "Microgrid", "EPMS", and "ComAp" — none currently appear in the profile.
