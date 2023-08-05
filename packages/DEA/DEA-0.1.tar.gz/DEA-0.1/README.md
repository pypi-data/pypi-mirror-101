# DEA

DEA stands for differential expression analysis, a common analysis in bioinformatics done to explore the most significantly differentially expressed genes between 2 predefined groups. DEA is a simple python package that implements related-tools for differential expression analysis as well as visualizing the output on a volcano plot.

### Download Package

Download the DEA package by:
```
pip install git+https://github.com/jeffliu6068/DEA.git
```
or 
```
pip install DEA
```

### Import

Once installed, import the package by: 

```
import DEA
```
## Intuition: How DEA Works to Identify Differentially Expressed Genes

During DEA, the input group of samples will be compared to the rest of the samples. The degree of difference is measured in fold change which is the mean(group1) divided by the mean(group2) and the significance of the difference is measured using a Student t-test with Bonferroni multiplicity correction as an option. This returns a dataframe with the p-value and fold change of each differentially expressed gene. P-value > 0.05 are removed. This output is then plotted onto a volcano plot for easy visualization.

# Available Tools in the GMMchi_scs_pipeline Package

## Differentially Expressed Genes

```
import DEA

dea_df = DEA.compare_clusters(df, X_label, correction=False) 
```
df is the input dataframe with genes (row) x samples (columns) and X_label is a list of samples part of df that is compared to the rest of the df

## Volcano Plot

```
DEA.volcano_plot(dea_df, 5,2)
```
Volcano plots the log2(fold change) on the x-axis and -log10(p-value) on the y-axis. The last 2 parameters 5, 2 in this case are the -log10(p-value) threshold and log2(fold change) threshold used to define the points that will be annotated on the graph. 

## Authors

* **Ta-Chun (Jeff) Liu** - [jeffliu6068](https://github.com/jeffliu6068)
* **Sir Walter Fred Bodmer FRS FRSE** - *Supervision*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration: Thank you for all that has contributed ideas and expertise to make this possible. Let's advance science together. 

