# Supplementary information
## Introduction
Discovering spoliation of evidence through identifying traces on deleted files in macOS systems

## Analysis
  - White paper - Spoliation Trace 		(MS Word)
  - Spoliation trace analysis result sheet 	(MS Excel)

## Experiments
 - Dataset
	- No deletion				(Clean image)
	- File deletion				(Ordinary User image)
	- High-level anti forensics		(Specialist image)
 - SampleDataSet for the tool test
 - Experiment Dataset & Result			(MS Excel)

# TEFT (Trace Evidence Forensics Tool)

## Building - Windows
 - The Python 3.7 or above must be registered in the system environment variable
 - No additional install is necessary
 
## Git

To get the source using git run:
<pre><code>git clone https://github.com/blackmax90/TraceEvidence-on-macOS.git</code></pre>

## Install/Dependency

To run TEFT, please change Powershell Execution Policy.

Execute Powershell as administrator:
```
Set-ExecutionPolicy Unrestricted
```

And enter
```
A
```

Installing the Requirements Library to Run in PowerShell:
```
.\build.ps1
```

## Run
Open Folder:
```
cd TraceEvidence-on-macOS
```

Activate venv(if not activated):
```
cd venv\Scripts
Activate.bat
```

Run TEFT:
```
python TEFT_core.py
```

## Building - macOS
 - The Python 3.7 or above must be registered in the system environment variable
 - No additional install is necessary
 
## Git

To get the source using git run:
<pre><code>git clone https://github.com/blackmax90/TraceEvidence-on-macOS.git</code></pre>

## Install/Dependency

To run TEFT, please change the Full Disk Access permissions.
```
System Preferences -> Security & Privacy -> Privacy -> Full Disk Access '+' -> Terminal
```

changing file permission to Run:
```
sudo chmod 755 ./build.sh
```

Installing the Requirements Library to Run:
```
./build.sh
```

## Run
Open Folder:
```
cd TraceEvidence-on-macOS
```

Activate venv(if not activated):
```
source ./venv/bin/activate
```

Run TEFT:
```
python3 ./TEFT_core.py
```


## USAGE
### Input data selection

To test the tool with our sample data, download 'SampleDataSet' from
(https://drive.google.com/drive/folders/1uHfDYvFLguRIe_juv6ScgNhLD-QnNX_3?usp=sharing)

<img width="478" alt="image" src="https://user-images.githubusercontent.com/17299107/198842642-17023951-e151-472c-9fdb-e5214dcf796d.png">

TEFT show a list of methods in two categories.
1. Live System			- Automatically extract and analyze files in the system (macOS)
2. Disk Image			- Not available for now
3. Directory (or for test)	- Automatically extract and analyze trace evidence in folder

(To test the tool with our sample data, select '3')

### Directory path
<img width="476" alt="2" src="https://user-images.githubusercontent.com/17299107/198843016-126c3e16-6832-4f7d-8d89-8cef5ce6c7bd.png">

For direcotry as input, type the absolute path of the directory.

(To test the tool with our sample data, type 'SampleDataSet')

### Username
<img width="479" alt="3" src="https://user-images.githubusercontent.com/17299107/198843234-6644600a-c49a-48bd-85a5-3812147c3156.png">

Type target username. If you don't have information about the user, type 'x'.

(To test the tool with our sample data, type 'x' or 'max')

## Output
TEFT collect and store the trace evidence data in the './extractedfiles - [user account]' folder.

The deleted file list (MS Excel) is saved in './result/[user account]' folder.
