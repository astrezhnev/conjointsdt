# Conjoint Survey Design Tool

The Conjoint Survey Design Tool assists researchers in creating multi-dimensional choice experiments that can be readily incorporated into any pre-existing web survey software (such as Qualtrics). Conjoint analysis is a type of survey experiment often used by market researchers to measure consumer preferences over a variety of product attributes. Hainmueller, Hopkins and Yamamoto (2014) demonstrate the value of this design for political science applications. Conjoint experiments present respondents with a choice among set of profiles composed of multiple randomly assigned attributes. This approach allows researchers to estimate the effect of each individual component on the probability that the respondent will choose a profile. This software tool is designed as a companion to Hainmueller, Hopkins and Yamamoto (2014), providing a graphical user interface for generating conjoint experiments.

## Citation 

Hainmueller, Jens., Hopkins, Daniel J., Yamamoto, Teppei. (2014). Causal Inference in Conjoint Analysis: Understanding Multidimensional Choices Via Stated Preference Experiments. *Political Analysis* 22(1), 1-30

## Installation

The Conjoint Survey Design Tool (SDT) runs from the Python source on Windows, Mac OSX and Linux. It is written for Python 3 and requires Python 3.6 or greater. To obtain the most recent release of Python 3, visit https://www.python.org/downloads/

Windows users should install Python using the installer from python.org and leave the "tcl/tk and IDLE" option checked (it is on by default), as the SDT's interface requires the TCL/TK library.

Mac OSX users should make sure that they have the most recent version of the TCL/TK library installed. Consult https://www.python.org/download/mac/tcltk/ for more information.

To run the Conjoint SDT from Python source, download the `conjointSDT.py` to the desired directory and run the file through the Python interpreter (this can be done through the command line by calling `python conjointSDT.py` or `python3 conjointSDT.py` if your installation distinguishes between versions 2 and 3 of python).

A sample survey file, `immigrant_demo.sdt`, is included in the Demos folder.
  
## Instructions

Please consult the `conjoint_sdt_manual.pdf` file located in the Manual folder for detailed instructions on how to use the GUI design tool.
  
## Companion R package

After implementing the experiment and collecting the result, researchers can use the `cjoint` R package for analysis and visualization of the results. This package can be installed directly from CRAN. The most current documentation can be found at `https://cran.r-project.org/web/packages/cjoint/index.html`.
  
## Version History

Version 3.1 - October 21, 2026

Removed the PHP randomizer. The JavaScript randomizer for Qualtrics is now the only export format, as it runs entirely within Qualtrics and does not require hosting a script on a separate server. Users who need a randomizer for a different survey platform can adapt the exported JavaScript.

Discontinued the standalone Windows executable. Windows users should run the SDT from the Python source.

Version 3.0 - January 10, 2022

Added a JavaScript randomizer to supplement the existing PHP randomizer. Users can now export JavaScript snippet that can be placed directly within a Qualtrics question to generate the conjoint tasks for a respondent. This no longer requires users to have a second server to host the PHP script and allows the randomization be carried out entirely within Qualtrics.

Added a feature to allow users to generate designs that prevent identical profiles from appearing in a single task (off by default).

Version 2.0 - July 24, 2019

Ported over to Python 3. Fixed various compatability issues that had accumulated over the last several years.

Version 1.3 (BETA) - May 16, 2014

Fixed significant bug in Qualtrics question templates. Qualtrics template files will not longer include choice radio buttons. Do NOT use radio buttons within a Descriptive Text item to obtain responses as Qualtrics will not record any data passed through a Descriptive Text item. Instead, use a Multiple Choice item and create choices that correspond to each profile.

Version 1.2 (BETA) - May 5, 2014

Added "Export to R" feature to allow designs to be exported to the (forthcoming) conjoint R package for estimating component effects

Version 1.1 (BETA) - November 16, 2013

Added automatic question templates for use in Qualtrics

Version 1.0 (BETA) - September 23, 2013

First release

## Contact

If you have further questions about using the Conjoint SDT or wish to report a bug, please do not hesitate to contact Anton Strezhnev at [strezhnev@wisc.edu](mailto:strezhnev@wisc.edu).

## License

GNU General Public License 3.0 

## Acknowledgments

Special thanks to Katarina Jensen for assistance in porting the old Python 2 code to be compatible with Python 3. Thanks to everyone who has contributed with bug reports and feature suggestions.

