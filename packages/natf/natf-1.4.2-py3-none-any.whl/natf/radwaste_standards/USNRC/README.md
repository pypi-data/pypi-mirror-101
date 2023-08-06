This folder contains two files about US NRC radwaste classification.
See NRC website and '10CFR61' for more information.
- USNRC_LL.csv: Long live nuclides table.
- USNRC_SL.csv: Short live nuclides table.

Data in USNRC_LL.csv have two units:
- Ci/g: for Pu241 and Cm242
- Ci/m3: for the rest
- There is not class B in orignal USNRC_LL, to keep the format of table LL
  and SL are the same, I set the limit of class A and B to be the same.
  Therefore, if the radwaste exceed the class A, it automatically exceed the
  limit of calss B.
  

Data in USNRC_SL.csv ara in unit of: Ci/m3.
- The nuclide with half life less than 5 year, is hard coded, not present in the csv.
