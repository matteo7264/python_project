# Python Educational Reverse Shell

**Strictly educational project** – Demonstration and learning of how a reverse shell works in Python.

This project is **NOT** intended to be used on systems without explicit permission. Any malicious use is illegal and unethical.

## ⚠️ IMPORTANT DISCLAIMER

This code is provided **SOLELY for educational purposes** and to understand the mechanisms of client-server communication, remote command execution, and post-exploitation techniques in an educational or authorized security research context (authorized pentest, CTF, personal lab, etc.).

**It is strictly forbidden** to use this program:

- on a machine that does not belong to you
- without the written and explicit consent of the owner
- in any illegal, malicious or unauthorized context

I decline all responsibility in case of misuse of this code.

## Project Goal

This project was created to help you:

- Deeply understand how a **reverse shell** works
- Learn TCP socket programming in Python
- Discover bidirectional client-server communication
- Explore remote system command execution
- Practice error handling and code robustness
- Improve skills in Python network programming and security

## General Architecture

The project consists of two parts:

1. **Server** (`server_reverseshell.py`)  
   → Listens on a given IP address and port  
   → Waits for a client to connect

2. **Client** (`client_reverseshell.py`)  
   → Executed on the target/victim machine (e.g. via educational phishing demo, malicious USB demo, etc.)  
   → Actively initiates the connection to the server  
   → Executes received commands and sends back the results

### Implemented features (server side)

- Arbitrary shell command execution
- Basic system information retrieval (OS, version, current directory)
- File download from the remote machine
- Screenshot capture (if Pillow dependency is installed)
- Custom commands (e.g. `infos`, `capture`, `download`, etc.)

## Requirements

**Server** (the listening machine):

- Python 3.8+
- No mandatory extra dependencies

**Client** (the "victim" machine in the demo):

- Python 3.8+
- Optional modules for `capture` features:

  ```bash
  pip install Pillow