# Conjoint Survey Design Tool

The Conjoint Survey Design Tool assists researchers in creating multi-dimensional choice experiments that can be readily incorporated into any pre-existing web survey software (such as Qualtrics). Conjoint analysis is a type of survey experiment often used by market researchers to measure consumer preferences over a variety of product attributes. Hainmueller, Hopkins and Yamamoto (2013) demonstrate the value of this design for political science applications. Conjoint experiments present respondents with a choice among set of profiles composed of multiple randomly assigned attributes. This approach allows researchers to estimate the effect of each individual component on the probability that the respondent will choose a profile. This software tool is designed as a companion to Hainmueller, Hopkins and Yamamoto (2013), providing a graphical user interface for generating conjoint experiments.

## Installation

There are two ways to run the Conjoint Survey Design Tool (SDT). 

### Windows Binary

For Windows users, an executable binary is available for download. This is a self-contained package that requires no additional libraries to function. To use the SDT, download the `conjointSDT.exe` file to the desired location and run the executable.

A sample survey file, `immigrant_demo.sdt`, is included in the Demos folder. 

### Source Package
Mac OSX and Linux users do not have standalone executables and need to use the Python source files. Windows users with a Python installation can also use the source package. This is advisable as the binary package is much larger than the source since it includes the necessary Python libraries and interpreter. 

The Conjoint SDT is written for Python 3 and requires Python 3.6 or greater. To obtain the most recent release of Python 3, visit https://www.python.org/downloads/

Mac OSX users should make sure that they have the most recent version of the TCL/TK library installed. If you installed Python. Consult https://www.python.org/download/mac/tcltk/ for more information.

To run the Conjoint SDT from Python source, download the `conjointSDT.py` to the desired directory and run the file through the Python interpreter (this can be done through the command line by calling `python conjointSDT.py` or `python3 conjointSDT.py` if your installation distinguishes between versions 2 and 3 of python).

A sample survey file, `immigrant_demo.sdt`, is included in the Demos folder.
  
## Instructions

Please consult the `conjoint_sdt_manual.pdf` file located in the Manual folder for detailed instructions on how to use the GUI design tool.
  
## Version History

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

If you have further questions about using the Conjoint SDT or wish to report a bug, please do not hesitate to contact Anton Strezhnev at [as6672@nyu.edu](mailto:as6672@nyu.edu).

## License

GNU General Public License 3.0 

## Acknowledgments

Special thanks to Katarina Jensen for assistance in porting the old Python 2 code to be compatible with Python 3. Thanks to everyone who has contributed with bug reports and feature suggestions.

