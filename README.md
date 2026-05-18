# rr-lyrae-animations
Various visualizations for RR Lyrae stars (like the opacity bump as a driving mechanism, observations of the Blazhko effect, etc.)


**kappa_mechanism.py**
- uses [MESA-RSP](https://ui.adsabs.harvard.edu/abs/2019ApJS..243...10P/abstract) LOGS to show work integral + opacity in star during a pulsation cycle
- creates gif of stellar envelope structure (ionization zone, convective regions, work + opacity) during a pulsation, matched with the position in the lightcurve and position in the HR diagram


**blazhko_2d3d.py**
- given: i) lightcurve, manually cropped to a single lightcurve phase:
- creates gif of folded lightcurve showing the blazhko modulations from phase to phase, as well as 3d gif of blazhko modulations, highlighting the folded lightcurve in each step of the 2d gif; side-by-side


**blazhko_effect.py**
- given: i) dataset (e.g., times and magnitudes) ii) fundamental pulsation period, iii) blazhko period (approximately):
- creates gif of folded lightcurve showing the blazhko modulations from phase to phase
- note: if dataset is in flux, need to comment you the y-axis inversion
- inspired by [OGLE Atlas of Variable Star Light Curves: RR Lyrae](https://ogle.astrouw.edu.pl/atlas/RR_Lyr.html) info page
