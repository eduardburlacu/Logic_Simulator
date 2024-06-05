---
title: Logic Simulator
labels: [Circuit Simulation, Python]
---

**Contributors:** Eduard Burlacu, Nikko ten Have, Dhanish Patel

 
**Note**: this coursework project has been developed starting with a partial implementation on top of which we built the compiler and GUI.

## About this software
**What's implemented:** Source code for a logic simulator with interaction either on terminal or a GUI.

**How to use:**
* install the dependencies(details next)
* create a .txt definition file for the circuit description
* run the source code

```bash
# To run in a terminal GUI
python final/src/logsim.py -c  (path_to_file)
# To run in a WxPython GUI
python final/src/logsim.py (path_to_file)
```

**Content:**
* `doc/EBNF` shows the EBNF used in the hardware description language
* `def_files` contains toy-examples of definition files used during testing
* `requirements.txt` contains the packages necessary to run in full functionality mode. If one intends to use it with the terminal only, the environment setup step can be skipped. The only requirement remains using Python 3.8+.

## Environment Setup
To run the code with the full GUI functionality you can install the dependencies by:
```bash
python -m pip install --upgrade pip
bash setup_env.sh
```

## Language Setup

```bash
# Enter the following command in the terminal to change the language e.g. if the system language is Chinese, enter:
LANG=zh_CN.utf8
```

## Usage Examples

```bash
# Run def file circtuit1
python final/src/logsim.py ../doc/net_definition/circuit1.txt
```

```bash
# Run def file circtuit2
python final/src/logsim.py ../doc/net_definition/circuit2.txt
```

```bash
# Run def file adder with carry
python final/src/logsim.py ../doc/net_definition/adder.txt
```

```bash
# Run def file rc3
python final/src/logsim.py ../doc/net_definition/rc3.txt
```
