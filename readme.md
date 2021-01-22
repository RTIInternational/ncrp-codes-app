# NCRP Auto-Coder

## ℹ️ Intro

This application uses machine learning to assign NCRP codes to offense descriptions. Using [publicly available data](https://web.archive.org/web/20201021001250/https://www.icpsr.umich.edu/web/pages/NACJD/guides/ncrp.html) from a crosswalk, we used examples of offenses from all 50 states to train an algorithm to identify which patterns of text are associated with each code.

There are 3 outputs available, in increasing order of granularity: `Broad Category`, `BJS Category`, `BJS Descrption`. These are listed in the original crosswalk file.