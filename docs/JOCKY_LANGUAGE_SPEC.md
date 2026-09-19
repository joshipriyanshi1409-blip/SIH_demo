# JOCKY Language Specification

## 1. Purpose

JOCKY is a small domain-specific language for expressing
cross-platform forensic investigation operations.

The Round-1 prototype intentionally supports a very small
language surface.

---

## 2. Example Program

```text
INVESTIGATE HOST01 {
    CHECK PROCESSES
    CHECK NETWORK
    CHECK DNS
    CHECK LOGS
} 