# Conjoint Survey Design Tool

The Conjoint Survey Design Tool assists researchers in creating multi-dimensional choice experiments that can be readily incorporated into any pre-existing web survey software (such as Qualtrics). Conjoint analysis is a type of survey experiment often used by market researchers to measure consumer preferences over a variety of product attributes. Hainmueller, Hopkins and Yamamoto (2013) demonstrate the value of this design for political science applications. Conjoint experiments present respondents with a choice among set of profiles composed of multiple randomly assigned attributes. This approach allows researchers to estimate the effect of each individual component on the probability that the respondent will choose a profile. This software tool is designed as a companion to Hainmueller, Hopkins and Yamamoto (2013), providing a graphical user interface for generating conjoint experiments.

## Installation

Currently the Windows executable version is unavailable. Please follow the PDF manual located in the Manual folder for instructions on how to install the Python source. The current version uses Python 2. A Python 3.0 version will be made available shortly.

## Version History

Version 1.3 (BETA) - May 16, 2014

Fixed significant bug in Qualtrics question templates. Qualtrics template files will not longer include choice radio buttons. Do NOT use radio buttons within a Descriptive Text item to obtain responses as Qualtrics will not record any data passed through a Descriptive Text item. Instead, use a Multiple Choice item and create choices that correspond to each profile.

Version 1.2 (BETA) - May 5, 2014

Added "Export to R" feature to allow designs to be exported to the (forthcoming) conjoint R package for estimating component effects

Version 1.1 (BETA) - November 16, 2013

Added automatic question templates for use in Qualtrics

Version 1.0 (BETA) - September 23, 2013

First release

## License

GNU General Public License 3.0 


