# Day 1 Data Quality Summary

- Fund master unique AMFI codes: **40**
- Supplied NAV history unique scheme codes: **1**
- Codes matched: **1**
- Fund master codes absent from supplied NAV history: **39**
- Match rate: **2.5%**

## Interpretation
Missing means no matching code was present in the supplied NAV history file; it does not prove that the AMFI code is invalid.

## Data anomaly
The supplied NAV history file contains scheme code 125497 with the name `SBI SMALL CAP FUND - Direct Plan - Growth`. The assignment labels 125497 as HDFC Top 100 Direct. Verify the code/name mapping against MFAPI metadata before treating it as HDFC data.

## Important scope note
The supplied NAV history contains only the scheme codes present in that file. This check tests presence in the supplied file; it is not a complete live-AMFI validity check.
