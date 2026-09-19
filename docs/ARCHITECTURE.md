# JOCKY Architecture

## 1. Project Purpose

JOCKY is a cross-platform defensive forensic investigation
proof-of-concept for SIH Problem Statement 26148.

The Round-1 prototype supports the JOCKY command:

    INVESTIGATE HOST01 {
        CHECK PROCESSES
        CHECK NETWORK
        CHECK DNS
        CHECK LOGS
    }

The same JOCKY source must be usable on Windows and Kali Linux.

---

## 2. High-Level Pipeline

JOCKY Source
    ↓
Lexer
    ↓
Parser
    ↓
AST
    ↓
IR
    ↓
Executor
    ↓
Platform Adapter
    ↓
Common Evidence Model
    ↓
Forensic Analysis
    ↓
Correlation
    ↓
Risk
    ↓
Result
    ↓
Dashboard

---

## 3. Major Components

### Compiler

Location:

    compiler/

Responsibilities:

- lexical analysis
- parsing
- AST construction
- intermediate representation

The compiler is platform-independent.

---

### Runtime

Location:

    runtime/

Responsibilities:

- execute platform-neutral IR
- dispatch operations through platform interfaces

The runtime must not contain hard-coded
Windows or Linux commands.

---

### Platform Adapters

Location:

    platform/

Structure:

    platform/
    ├── windows/
    └── linux/

Responsibilities:

- interact with the operating system
- collect processes
- collect network information
- collect DNS information
- collect logs
- convert platform-specific information into
  the common evidence model

---

### Forensics

Location:

    forensics/

Responsibilities:

- analyze collected evidence
- identify suspicious activity
- correlate evidence
- calculate risk
- generate findings

---

### Backend

Location:

    backend/

Responsibilities:

- expose JOCKY functionality through an API
- accept investigation requests
- return investigation results
- expose findings, timelines, and evidence

---

### Frontend

Location:

    frontend/

Responsibilities:

- provide JOCKY editor
- show compiler pipeline
- show execution status
- display findings
- display timeline
- display evidence

---

## 4. Platform Independence

The following components must remain platform-independent:

- JOCKY syntax
- lexer
- parser
- AST
- IR
- executor interface
- evidence schema
- finding schema
- correlation format
- API contracts

Platform-specific implementation belongs inside:

    platform/windows/

and:

    platform/linux/

---

## 5. Platform Provider Concept

The executor communicates with a platform provider.

Conceptually:

    Executor
        ↓
    Platform Provider
        ↓
    Windows or Linux implementation

The executor must not directly execute operating-system-specific
commands.

---

## 6. Evidence Flow

Platform-specific collectors produce normalized evidence.

Conceptually:

    Windows/Linux Collector
             ↓
       Common Evidence
             ↓
       Forensic Analysis
             ↓
          Findings

Windows and Linux may collect information differently,
but their normalized output must follow the same contract.

---

## 7. Round-1 Scope

The Round-1 proof-of-concept focuses on:

- JOCKY language
- compiler pipeline
- platform abstraction
- Windows implementation
- Linux/Kali implementation
- forensic analysis
- correlation
- risk
- backend
- dashboard

The project does not implement:

- EDR disabling
- BYOVD exploitation
- kernel subversion
- API unhooking
- process hollowing
- reflective injection
- real malware
- antivirus bypass
- stealth persistence
- offensive payloads

Advanced techniques may only be represented through
safe detection or simulation.

---

## 8. Team Ownership

### Person 1 — Windows / Team Lead

Owns:

- architecture
- JOCKY language
- compiler
- runtime
- Windows adapter
- common contracts
- backend foundation
- dashboard foundation
- testing
- documentation
- integration

### Person 2 — Kali Linux

Owns:

- Kali/Linux environment
- Linux adapter
- Linux collectors
- forensic analysis
- correlation
- risk engine
- Kali testing

Person 2 must implement the Linux side using
the interfaces established by Person 1.

---

## 9. One JOCKY Project

Windows and Linux are not separate projects.

There is one JOCKY language and one architecture.

The operating-system-specific implementation is isolated
behind the platform abstraction.