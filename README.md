<div align="center">
  <img src="https://raw.githubusercontent.com/joinsnipe/SPE_TRACE/main/public/apple-touch-icon.png" width="120" alt="TRACE Logo">
  <h1>TRACE™ Structural Extractor</h1>
  <p><b>Zero-Trust Codebase Topology Extractor for Enterprise Audits</b></p>
</div>

---

## What is this?

This is the official open-source extraction tool for **TRACE™ Structural Audits**. 

When undergoing a technical due diligence or codebase audit with TRACE, we measure the structural resilience of your software architecture (identifying God Nodes, single points of failure, and community fragmentation).

However, **we do not want your source code.**

This script allows you to extract the mathematical topology of your codebase (how functions and classes connect) without ever exposing a single line of business logic, hardcoded strings, or API keys.

## 🛡️ The Zero-Trust Guarantee

You can review `trace_extractor.py` (it's less than 100 lines). You will see that it uses Abstract Syntax Tree (AST) parsing to:
- **EXTRACT**: Class names, function names, and function call targets.
- **IGNORE**: Variables, strings, comments, loops, conditions, and any inner logic.
- **OFFLINE**: The script does not make any network requests. It saves a `.json` file locally on your machine.

## How to use it

1. Download the script:
   ```bash
   curl -O https://raw.githubusercontent.com/joinsnipe/SPE_TRACE./main/trace_extractor.py
   ```

2. Run it against your project folder (requires Python 3.8+):
   ```bash
   python trace_extractor.py /path/to/your/project
   ```

3. **Verify the output**:
   The script will generate a file called `trace_topology_export.json`. Open it with any text editor to verify that absolutely no sensitive code was captured.

4. **Send it to TRACE**:
   Send the `trace_topology_export.json` file to your TRACE Structural Auditor to generate your architectural health report.

---
*Maintained by TRACE™ - Forensic Intelligence & Structural Diagnostics.*
