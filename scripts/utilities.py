#this function helps to print 
#some stats for the processing of a 
#maxquant dataset
def print_result(start_df_shape, shape_before, df, what):
    removed = shape_before[0]- df.shape[0]
    removed_from_beginning = start_df_shape[0]-df.shape[0]
    if removed > 0:
        print 'removed ',removed, what   
        print 'tot ', removed_from_beginning, ' entries removed' 
        print '---------------'
    else:
        print what
        print 'nothing removed'
        print '---------------'


#this function remove rubbish entries from a 
#maxquant dataset
def clean(df):  
    #remove Only identified by site
    before,start = df.shape,df.shape
    col = 'Only identified by site'
    df = df[df[col] != '+'] 
    print_result(start, before, df, col)
    
    #remove hits from reverse database
    before = df.shape
    col = 'Reverse'
    df = df[df[col] != '+']
    print_result(start, before, df, col)
        
    #remove contaminants (mainly keratine and bsa)
    before = df.shape
    col = 'Potential contaminant'
    df = df[df[col] != '+']
    print_result(start, before, df, col)
    
    #remove protein groups with less thatn 2 unique peptides
    before = df.shape
    col = 'Peptide counts (unique)'
    df['unique'] = [int(n.split(';')[0]) for n in df[col]]
    df = df[df['unique'] >= 2]
    print_result(start, before, df, col)
    return df

#this function extract a dataset from
#a maxquant output file
def get_data(df, quant_method, experiment, fractions):
    cols_to_select = [ quant_method+str(experiment)+str(f) for f in fractions]
    df = df[cols_to_select]
    print 'got: ', df.shape[0], 'protein now'
    #remove raws with all zeros entries in the data
    df = df[(df.T != 0).any()]
    return df

#function to normalise the raw of a dataframe
#by its maximum value
def norm_max(X):
    X = X/X.max()
    return X