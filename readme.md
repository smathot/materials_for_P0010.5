# P0010.5 Cross-experimental analysis

Resources for Mathôt, S., Siebold, A., Donk, M., & Vitu, F., (in preparation). *Large Pupils Predict Goal-driven Eye Movements*.

## Analysis

To run the full analysis, execute:

	./fullAnalysis.sh
	
In addition to the standard Python modules for data processing (NumPy etc.), the analysis requires [`exparser`](https://github.com/smathot/exparser).

## Data

Every experiment has the following input files:

- `exp[X].data.csv` which contains trial info, with one trial per row.
- `exp[X].fixdur.csv` which is a list of fixation durations.
- `exp[x].fix.csv` contains the main input. This corresponds to `saccLog-processed.csv` from the original parser.

## Stimuli

Images, saliency maps, and luminance maps (as described in the manuscript) can be found in the folder `/stimuli/`. Due to license restrictions, for Exp. 2, only the fractals are provided. The scenes can be obtained from:

- <http://natural-scenes.cps.utexas.edu/>

## Manuscript

Manuscript source files can be found under `/manuscript/`.

## License and credits

- Experimental scripts (i.e. `*.py`) are available under the [GNU General Public License v3](http://www.gnu.org/licenses/gpl.html).
- `/stimuli/exp1-3/*` are taken (or derived) from the [UPenn natural image database](http://tofu.psych.upenn.edu/~upennidb/) and are available under a [Creative Commons Attribution-NonCommercial Unported License](https://creativecommons.org/licenses/by-nc/3.0/).
- All other files are original materials and available under a [Creative Commons Attribution Unported License](https://creativecommons.org/licenses/by/3.0/).
