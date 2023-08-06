NIR pre-process

Function compare-preprocessing can be used on any NIR spectral data if Y values are available. 
Y can include one or several variables.

Function evaluates impact of different pre-processing techniques and combinations using multiblock partial least squares (MBPLS). 
Each block in MBPLS is pre-processed spectral. 

Different pre-processing techniques evaluated:
    - baseline
    - detrend
    - EMSC
    - MSC
    - SNV
    - Savitzky Golay derivatives
    (different polynomial and derivatives orders can be tested as well as the size of the mmoving window)
    
Pre-processing techniques can be combined (several techniques applied to data one after the other). 
Analyst can choose to only compare scatter corrections techniques or only derivatives or both.
Number of combinations to evaluate can also be defined. 
By the default, only single pre-processing techniques and combining 2 are tested.
    
Original spectral data is also used as a block to have a starting point.

20 blocks made of random noise called false signals are added before performing MBPLS to represent what would data
look like if relevant information is completely destroyed.

For MBPLS, analyst can choose: 
    - number of principal to calculate 
    - to autoscale or center each pre-processed spectral
    - to autoscale or center Y
    
Blocks are represented in superloadings plot.
Model performances (adjusted R2, RMSECV) and variable importance on projection (VIP) are calculated 
for each block by cross validation. Number of random picks for cross validation and number of lines 
predicted in each cross validation can be set by the analyst.
Effective rank for each block is calculated as well. 
