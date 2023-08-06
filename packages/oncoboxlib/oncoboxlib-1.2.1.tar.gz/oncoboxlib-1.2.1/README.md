# oncoboxlib

Oncobox library calculates Pathways Activation Levels (PAL) according to
Sorokin et al.(doi: 10.3389/fgene.2021.617059).
It takes a file that contains gene symbols in HGNC format (see genenames.org),
their expression levels for one or more samples (cases and/or controls)
and calculates PAL values for each pathway in each sample.

## Installation

```
pip install oncoboxlib
```

## How to run the example

1. Create any directory that will be used as a sandbox. Let's assume it is named `sandbox`.


2. Extract `resources/databases.zip` into `sandbox/databases/`.
  <br> (You may download the archive from 
  `https://gitlab.com/oncobox/oncoboxlib/-/blob/master/resources/databases.zip`)
  

3. Extract example data `resources/cyramza_normalized_counts.txt.zip` into `sandbox`.
  <br> (You may download the archive from 
  `https://gitlab.com/oncobox/oncoboxlib/-/blob/master/resources/cyramza_normalized_counts.txt.zip`)
  

What it looks like now:
```
   - sandbox
       - databases
           - Balanced 1.123
           - KEGG Adjusted 1.123
           ...
       - cyramza_normalized_counts.txt  
```

4. Change directory to `sandbox` and execute the command:
```
calculate_scores --databases-dir=databases/ --samples-file=cyramza_normalized_counts.txt
```
It will create a result file `sandbox\pal.csv`.


Alternatively, you can use it as a library in your source code.
For details please see `examples` directory.


## Input file format

Table that contains gene expression.
Allowed separators: comma, semicolon, tab, space.
Compressed (zipped) files are supported as well.

- First column - gene symbol in HGNC format, see genenames.org.
- Others columns - gene expression data for cases or controls.
- Names of case columns should contain "Case", "Tumour", or "Tumor", case insensitive.
- Names of control columns should contain "Control" or "Norm", case insensitive.

It is supposed that data is already normalized by DESeq2, quantile normalization or other methods.
