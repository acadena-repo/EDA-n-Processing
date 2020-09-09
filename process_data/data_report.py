# -*- coding: utf-8 -*-
# PROGRAMMER: Alejandro Cadena
# DATE CREATED: 09.08.2020                   
# REVISED DATE: 
# PURPOSE: The Process Data Report are a set of functions that run on any Dataset imported as pandas Dataframe.
#The functions retrieve a comprenhensive report and a basic set of plots that can lead the process of Exploratory Data Analysis and Feature Engineering.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

def process_sugg(var):
    '''
    argument:
        > var: pandas series
    returns:
        > string with suggestions regarding further processing on the variable
    '''
    val = ('Variable','Missing %','Cardinality')
    sugg = ''
    
    ##CHECK FOR MISSING DATA ...
    if var[val[1]] > 0.0:
        if var[val[1]] <= 3.0:
            sugg += 'DLR/' #DELETE RECORDS WITH MISSING VALUES
        else:
            sugg += 'IMP/' #DATA IMPUTATION
        
    if var[val[0]] == 'Categorical':
        ##CHECK FOR CARDINALITY ...
        if var[val[2]] < 5:
            sugg += 'OHE/' #LOW CARDINALITY ONE HOT ENCODING
        elif var[val[2]] < 20:
            sugg += 'ENC/' #MEDIUM CARDINALITY ENCODING
        else:
            sugg += 'DPE/' #HIGH CARDINALITY DISCRETIZATION PLUS ENCODING
            
    if var[val[0]] == 'Numerical':
        sugg += 'TRM/'
        ##CHECK FOR CARDINALITY ...
        if var[val[2]] < 5:
            sugg += 'OHE/' #LOW CARDINALITY ONE HOT ENCODING
        elif var[val[2]] < 20:
            sugg += 'DPE/' #MEDIUM CARDINALITY DISCRETIZATION PLUS ENCODING
        else:
            sugg += 'BIN/' #HIGH CARDINALITY BINNING
        
    return sugg

def report(df):
    '''
    argument:
        > pandas dataframe
    returns:
        > pandas dataframe as a report of each feature with:
            - missing data (sort by default)
            - total unique values
            - type of variable
            - minimum, maximum values
            - suggestion on further processing
    '''
    ##AUXILIAR STRUCTURES ....
    card = []
    var = []
    vmax = []
    vmin = []
    psugg = []
    columns = ['Missing No.','Missing %','Cardinality','Variable','Max Value','Min Value']
    
    ##MISSING DATA CALCULATION ....
    na_num = df.isnull().sum()
    na_prc = round((df.isnull().mean()*100),2)
    ##CARDINALITY CALCULATION ....
    for col in df.columns:
        ##CARDINALITY CALCULATION ....
        card.append(df[col].nunique())
        ##GETTING FEATURE TYPE AND MAX & MIN VALUES ....
        if df[col].dtype == 'O':
            var.append('Categorical')
            vmax.append(df[col].value_counts().idxmax())
            vmin.append(df[col].value_counts().idxmin())
        else:
            var.append('Numerical')
            vmax.append(df[col].max())
            vmin.append(df[col].min())
        
    ##CREATING THE DATAFRAMES ....
    df_card = pd.DataFrame(card,index=df.columns)    
    df_var = pd.DataFrame(var,index=df.columns)
    df_max = pd.DataFrame(vmax,index=df.columns)
    df_min = pd.DataFrame(vmin,index=df.columns)
    ##GENERETING THE REPORT ....
    report = pd.concat([na_num,na_prc,df_card,df_var,df_max,df_min], axis=1,keys=columns,ignore_index=True)
    report.columns=columns
    report.sort_values(by='Missing %',ascending=False,inplace=True)
    ##GENERATING VARIABLE PROCESS SUGGESTIONS ....
    for i in report.index:
        variable = report.loc[i]
        psugg.append(process_sugg(variable))
        
    df_sugg = pd.DataFrame(psugg,index=report.index,columns=['Suggesting'])    
    report = pd.concat([report,df_sugg],axis = 1)
    
    return report

def sta_description(df,idx):
    '''
    arguments:
        > df: pandas dataframe
        > idx: pandas index
    returns:
        > pandas dataframe with statistical description for each feature
    '''
    return df[idx].describe()
    
def variable_type(df):
    '''
    argument:
        > df: pandas dataframe
    returns:
        > pandas index with all the freatures/columns that contain a numeric value
        > pandas index with all the features/columns that contain a categorical value
    '''
    return df.select_dtypes(include='number').columns, df.select_dtypes(include='object').columns

def corr_matrix(df):
    '''
    argument:
        > df: pandas dataframe
    returns:
        > Plot a correlation matrix as a heatmap
    '''
    corrmat = df.corr()
    plt.figure(figsize=(20,9))
    sns.heatmap(corrmat, vmin=0.0, vmax=1.0, center=0, annot=True, square=True, cmap='magma', fmt='.2f');
    
def univar_plot(variable,bins=30):
    '''
    arguments:
        > variable: pandas series
        > bins: integer with the number of bins (defalut: 30)
    returns:
        > Histogram and QQ plot for the specified variable
    '''
    plt.figure(figsize=(13,5))
    ##HISTOGRAM AND DENSITY FUNCTION PLOT ....
    plt.subplot(121,title = 'Histogram and Kde',ylabel = 'Frequency')
    sns.distplot(variable, bins = bins)
    ##PROBABILITY PLOT ....
    plt.subplot(122)
    stats.probplot(variable, dist= "norm",plot = plt)

    plt.show();

def multivar_plot(df):
    '''
    argument:
        > df: pandas dataframe
    returns:
        > Pairwise plot showing the relationships in the dataset
    '''
    sns.pairplot(df,diag_kws={'alpha':0.5})
    
def codes(code):
    '''
    argument:
        > code: string with suggestion code
    returns:
        > print a description of the processing suggestion
    '''
    sgg_codes = ['DLR','IMP','OHE','ENC','DPE','TRM','BIN']
    sgg_dic = {'DLR':'''Delete Records. It is assumed data is missing at random and missing data is less than 3%''',
               'IMP':'''Imputation. Missing data is greather that 3% so an imputation technique should be applied''',
               'OHE':'''One-Hot-Encoding. Categorical variable encoding with a set of boolean variables due to cardinality is low''',
               'ENC':'''Categorical Encoding. Categorical variable presents medium or high cardinality so an encoding technique other that OHE should be used''',
               'DPE':'''Discretisation Plus Encoding. Variable presents a high cardinality so a discretisation and encoding technique should be used''',
               'TRM':'''Transformation. Variable has been detected as continues so a mathematical transformation is suggested if distribution is not normal''',
               'BIN':'''Binning. Variable has been detected as continues so a discretisation technique is suggested'''}
    
    for sgg in sgg_codes:
        if sgg == code:
            print(sgg_dic[sgg])
            
            