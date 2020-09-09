## PROCESS DATA REPORT

The `Process Data Report` is composed of a set of functions that run on a pandas Dataframe.
The functions retrieve a comprenhensive report and a basic set of plots that can lead the process of Exploratory Data Analysis and Feature Engineering.

The functions provided by the `Process Data Report` are listed next:
   - report: **data process report generator**
   - codes: **description of codes regarding with process suggestion**
   - corr_matrix: **correlation matrix plot as heatmap**
   - univar_plot: **histogram and QQ-plot for a single variable**
   - multivar_plot: **pairwise plot showing the relationship of the variables**
   - sta_description: **statistical description of a set of variables**
   - variable_type: **separates the variables in the dataset as Numerical / Categorical**
   
##DEPENDENCIES
The libraries dependencies of the `Process Data Report` are:
- pandas                    0.24.2
- seaborn                   0.9.0
- matplotlib                3.0.3
- scipy                     1.2.1

In the repository a jupyter notebook is provided where it shows some examples on how to use the `Process Data Report`
