# NCRP Auto-Coder

## ℹ️ Intro

This application uses machine learning to assign NCRP codes to offense descriptions. Using [publicly available data](https://web.archive.org/web/20201021001250/https://www.icpsr.umich.edu/web/pages/NACJD/guides/ncrp.html) from a crosswalk combined with other hand-labeled offense text datasets, we used examples of offenses from all 50 states plus three specific jurisdictions to train an algorithm to identify which patterns of text are associated with each code.

This application predicts the *Charge Category*, which are the headings for offense codes in the [2009 NCRP Codebook: Appendix F](https://www.icpsr.umich.edu/web/NACJD/studies/30799/datadocumentation#).