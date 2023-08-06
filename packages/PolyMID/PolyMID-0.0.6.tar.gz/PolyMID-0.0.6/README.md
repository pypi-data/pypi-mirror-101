# PolyMID

PolyMID is a software package of functions that can be used to analyze data collected in stable-isotope tracing experiments.

PolyMID.Correct() is a function that removes the influence of naturally occurring heavy isotopes from stable-isotope tracing experiments
If it is called without any inputs, the user will be prompted to navigate to a text file where the inputs can be read. The text file must be formatted as follows:

FragmentName: TryptophanProtonated
FragmentFormula: C11H13N2O2
CanAcquireLabel: C11H13N2O2
MIDm: 0.88885 0.106829 0.004322
LabeledElement: C
TracerEnrichment: 1
LabelEnrichment: 1
HighRes: N O H

FragmentName and FragmentFormula specify the name and formula of the metabolite fragment. For analyses on LCMS systems using electrospray ionization, the fragment will generally be the whole metabolite. For analyses on GCMS systems using electron ionization, the fragment will generally be a portion of the derivatized form of the whole metabolite. The value, CanAcquireLabel, specifies which atoms of the fragment can possibly acquire label from the tracer. Only the atoms that are of the same element as the tracer are considered. If the fragment formula is identical to the metabolite formula, then this input could be the same as the input Formula. However, in cases where the fragment is a derivatized version of the metabolite, atoms of the derivatizing agent cannot acquire label from the tracer and should be excluded from this input. The value, MIDm, is the mass isotopomer distribution of the metabolite fragment as it is measured. The value, LabeledElement, is the chemical symbol of the heavy isotope-labeled element on the tracer molecule. The value, TracerEnrichment, is the percent of the chemical species of the tracer molecule that is labeled. The value, LabelEnrichment, is the fraction of atoms in labeled positions on the tracer that are labeled as heavy isotopes. Finally, HighRes is a series of element chemical symbols, separated by spaces, whose mass shifts due to incorporation of heavy isotopes are distinguished from those of the labeled element. HighRes can also take on values of none and all to indicate mass shifts due to incorporation of heavy isotopes of all or no chemical species, respectively, can be distinguished from those of the labeled element.

Open the Terminal (MacOS or Linux) or Cmd (Windows) window and type the command, Python3, to start the Python3 interpreter. The Python3 interpreter is now running in the Terminal or Cmd window. Type the command, Import PolyMID, to load the PolyMID software. PolyMID-Correct is part of the PolyMID software package. To run Poly-MID-Correct, type the command, Output = PolyMID.Correct(). A window accessing the operating system's directories will open. Navigate and select the text file specifying the input values as formatted according to instructions in the previous section. The program will run and print the corrected MID when finished. In the event that the printed output is truncated, the corrected MID can be accessed with the command, Output.MIDc.

Inputs can also be specified directly from the python interpreter command line as follows:
>>> FragmentName = 'TryptophanProtonated'
>>> FragmentFormula = 'C11H13N2O2'
>>> CanAcquireLabel = 'C11H13N2O2'
>>> MIDm = [0.88885, 0.106829, 0.004322]
>>> LabeledElement = 'C'
>>> TracerEnrichment = 1
>>> LabelEnrichment = 1
>>> HighRes = ['N', 'O', 'H']

Next, curate the variables into a single "Fragment" object, Input:
>>> Input = PolyMID.Fragment(FragmentName, FragmentFormula, CanAcquireLabel, MIDm, LabeledElement, TracerEnrichment, LabelEnrichment, HighRes)

Finally, run PolyMID-Correct passing it the Input variable:
>>> Output = PolyMID.Correct(Input)

The program will run and print the corrected MID when finished. In the event that the printed output is truncated, the corrected MID can be accessed with the command, Output.MIDc.



