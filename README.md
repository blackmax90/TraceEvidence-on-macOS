# Supplementary information
## Introduction
Discovering spoliation of evidence through identifying traces on deleted files in macOS systems

## Analysis
  - White paper - Spoliation Trace 		(MS Word)
  - Spoliation trace analysis result sheet 	(MS Excel)

## Experiments
 - Dataset (https://drive.google.com/drive/folders/1uHfDYvFLguRIe_juv6ScgNhLD-QnNX_3?usp=sharing)
	- No deletion				(Clean image)
	- File deletion				(Ordinary User image)
	- High-level anti forensics		(Specialist image)
 - Experiment Dataset & Result			(MS Excel)



# TEFT (Trace Evidence Forensics Tool)

## Building - Windows & macOS
 - The Python 3.7 or above must be registered in the system environment variable
 - No additional install is necessary

## Run
### Input data selection
![image](https://user-images.githubusercontent.com/17299107/196356121-066a4800-fb8a-4582-baa3-b3ffca226664.png)

TEFT show a list of methods in two categories.
1. Live System		- Automatically extract and analyze files in the system
2. Directory (Root)	- Automatically extract and analyze trace evidence in folder
(Unfortunally, disk image as a input file is not available for now)

### Directory path
![image](https://user-images.githubusercontent.com/17299107/196356537-c7a5fe44-4700-4537-92a3-2170fa2dd82b.png)

For direcotry as input, type the absolute path of the directory.

### Username
![image](https://user-images.githubusercontent.com/17299107/196356771-2c44c534-5111-4943-8a96-545e77d3e667.png)

Type target username. If you don't have information about the user, type 'x'.

## Output
TEFT collect and store the trace evidence data in the './extractedfiles' folder.
The deleted file list (MS Excel) is saved in './result' folder.
