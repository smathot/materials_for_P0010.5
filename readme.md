# P0010.5 Cross-experimental analysis

Resources for Mathôt, S., Siebold, A., Donk, M., & Vitu, F., (in preparation). *Large Pupils Predict Goal-driven Eye Movements*.

## Usage

To run the full analysis, execute:

	./fullAnalysis.sh

## Input files

Every experiment has the following input files:

- `exp[X].data.csv` which contains trial info, with one trial per row.
- `exp[X].fixdur.csv` which is a list of fixation durations.
- `exp[x].fix.csv` contains the main input. This corresponds to `saccLog-processed.csv` from the original parser.
