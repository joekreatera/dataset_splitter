import pandas
import numpy as np
import gc
def reduce_mem_usage(props):
    start_mem_usg = props.memory_usage().sum() / 1024**2 
    print("Memory usage of properties dataframe is :",start_mem_usg," MB")
    NAlist = [] # Keeps track of columns that have missing values filled in. 
    for col in props.columns:
        if props[col].dtype != object:  # Exclude strings
            
            # Print current column type
            #print("******************************")
            #print("Column: ",col)
            #print("dtype before: ",props[col].dtype)
            
            # make variables for Int, max and min
            IsInt = False
            mx = props[col].max()
            mn = props[col].min()
            
            # Integer does not support NA, therefore, NA needs to be filled
            if not np.isfinite(props[col]).all(): 
                NAlist.append(col)
                props[col].fillna(mn-1,inplace=True)  
                   
            # test if column can be converted to an integer
            asint = props[col].fillna(0).astype(np.int64)
            result = (props[col] - asint)
            result = result.sum()
            if result > -0.01 and result < 0.01:
                IsInt = True

            
            # Make Integer/unsigned Integer datatypes
            if IsInt:
                try:
                    if mn >= 0:
                        if mx < 255:
                            props[col] = props[col].astype(np.uint8)
                        elif mx < 65535:
                            props[col] = props[col].astype(np.uint16)
                        elif mx < 4294967295:
                            props[col] = props[col].astype(np.uint32)
                        else:
                            props[col] = props[col].astype(np.uint64)
                    else:
                        if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                            props[col] = props[col].astype(np.int8)
                        elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                            props[col] = props[col].astype(np.int16)
                        elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                            props[col] = props[col].astype(np.int32)
                        elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                            props[col] = props[col].astype(np.int64)    
                except ValueError:
                    props[col] = props[col].astype(np.float32)
            
            # Make float datatypes 32 bit
            else:
                props[col] = props[col].astype(np.float32)
            
            # Print new column type
            #print("dtype after: ",props[col].dtype)
            #print("******************************")
    
    # Print final result
    #print("___MEMORY USAGE AFTER COMPLETION:___")
    mem_usg = props.memory_usage().sum() / 1024**2 
    #print("Memory usage is: ",mem_usg," MB")
    #print("This is ",100*mem_usg/start_mem_usg,"% of the initial size")
    return props, NAlist


main_folder = '/../iot_23/'
files = [
main_folder+'2019-01-09-21-25-11-192.168.1.194-zeek-conn-log.labeled',
main_folder+'2019-01-10-19-22-51-192.168.1.198-zeek-conn-log.labeled',
main_folder+'2018-09-06-11-43-12-192.168.100.111-zeek-conn-log.labeled',
main_folder+'2018-12-20-21-10-00-192.168.1.197-zeek-conn-log.labeled',
main_folder+'2018-12-21-15-33-59-192.168.1.196-zeek-conn-log.labeled',
main_folder+'2019-01-10-21-06-26-192.168.1.199-zeek-conn-log.labeled',
main_folder+'2018-05-09-17-30-31-192.168.100.103-zeek-conn-log.labeled',
main_folder+'2018-05-19-20-57-19-192.168.2.5-zeek-conn-log.labeled',
main_folder+'2018-07-20-17-31-20-192.168.100.108-zeek-conn-log.labeled',
main_folder+'2018-07-25-10-53-16-192.168.100.111-zeek-conn-log.labeled',
main_folder+'2018-07-31-15-15-09-192.168.100.113-zeek-conn-log.labeled',
main_folder+'2018-09-21-11-40-22-192.168.2.3-zeek-conn-log.labeled',
main_folder+'2018-10-02-13-12-30-192.168.100.103-zeek-conn-log.labeled',
main_folder+'2018-10-03-15-22-32-192.168.100.113-zeek-conn-log.labeled',
main_folder+'2018-10-25-14-06-32-192.168.1.132-zeek-conn.log.labeled',
main_folder+'2018-12-21-13-36-41-192.168.1.198-zeek-conn-log.labeled',
main_folder+'2018-12-21-15-50-14-192.168.1.195-zeek-conn-log.labeled',
main_folder+'2019-01-10-14-34-38-192.168.1.197-zeek-conn-log.labeled',
main_folder+'2019-02-28-19-15-13-192.168.1.200-zeek-conn-log.labeled',
main_folder+'2019-02-28-20-50-15-192.168.1.193-zeek-conn-log.labeled',
main_folder+'2019-03-08-13-24-30-192.168.1.197-zeek-conn-log.labeled',
main_folder+'2019-07-03-15-15-47-192.168.1.158-zeek-conn-log.labeled',
main_folder+'2019-09-20-02-40-32-192.168.1.195-zeek-conn-log.labeled'
]

mem_map ={
'id.orig_p' :np.uint16,
'id.resp_p' :np.uint8,
'duration' :np.float32,
'orig_bytes' :np.uint64,
'resp_bytes' :np.uint64,
'missed_bytes' :np.uint16,
'orig_pkts' :np.uint32,
'orig_ip_bytes' :np.uint32,
'resp_pkts' :np.uint16,
'resp_ip_bytes' :np.uint32,
}

bad_lines = []
def record_badlines(line):
    print(line)
    bad_lines.append(line)
    return None


columns_to_drop = [
    "ts",
    "uid",
    "local_orig",
    "local_resp"
]

"""


cols_to_select = [
'td',
'sa',
'da',
'sp',
'dp',
'pr',
'_flag1',
'_flag2',
'_flag3',
'_flag4',
'_flag5',
'_flag6',
'fwd',
'stos',
'ipkt',
'ibyt',
'opkt',
'obyt',
'_in',
'out',
'sas',
'das',
'icmp_dst_ip_b',
'icmp_src_ip',
'udp_dst_p',
'tcp_f_s',
'tcp_f_n_a',
'tcp_f_n_f',
'tcp_f_n_r',
'tcp_f_n_p',
'tcp_f_n_u',
'tcp_dst_p',
'tcp_src_dst_f_s',
'tcp_src_tftp',
'tcp_src_kerb',
'tcp_src_rpc',
'tcp_dst_p_src',
'smtp_dst',
'udp_p_r_range',
'p_range_dst',
'udp_src_p_0',
'attack_t',
'attack_a'
]
"""

fields = [
'ts',
'uid',
'id.orig_h',
'id.orig_p',
'id.resp_h',
'id.resp_p',
'proto',
'service',
'duration',
'orig_bytes',
'resp_bytes',
'conn_state',
'local_orig',
'local_resp',
'missed_bytes',
'history',
'orig_pkts',
'orig_ip_bytes',
'resp_pkts',
'resp_ip_bytes',
'tunnel_parents-label-detail'
]
mode = 3


if( mode == 1):
    dtypes_df = pandas.DataFrame()
    i = 0
    pandas.set_option('use_inf_as_na', True)
    for f in files:
        # read 
        print(f"File {i} of {len(files)}")
        df = pandas.read_csv(f, skiprows=8, sep='\t', header=None, names=fields )
        df = df.loc[0:df.shape[0]-2]
        
        # cols, nas = reduce_mem_usage( df ) # index_col=0, dtype=mem_map
        cols = df
        cols = cols.drop(columns=columns_to_drop)
        cols = cols.astype(mem_map)
        
        print(cols)
        # print(cols.columns)
        print(cols.dtypes)
        dtypes_df[f"f{i}"] = cols.dtypes
        #dtypes_df = pandas.concat( [dtypes_df , cols.dtypes] )
        i+=1
        #cols.to_csv("dataset1.csv")
        # cols.to_pickle( f + '.pkl')
        #if(i==6):
        #    break
        
    print(dtypes_df)
    dtypes_df.to_csv("info.csv")

if(mode == 2):
    i = 0
    gen_file = None
    # pandas.set_option('use_inf_as_na', True)
    for f in files:
        # read 
        print(f"File {i} ({f}) of {len(files)}")
        
        # file = pandas.read_csv(f, dtype=mem_map ) # , dtype=mem_map  #  index_col=0  # cant do the mem_map thing if there are invalid values like NA
        file = pandas.read_csv(f, skiprows=8, sep='\t', header=None, names=fields ) # , dtype=mem_map
        # file = pandas.read_pickle(f + '.pkl')
        
        #file = file.astype(mem_map)
        
        file = file.drop(columns=columns_to_drop)
        
        file["duration"] = file["duration"].replace("-",0)
        file["orig_bytes"] = file["orig_bytes"].replace("-",0)
        file["resp_bytes"] = file["resp_bytes"].replace("-",0)
        
        for c in mem_map:
            print(c)
            file = file.astype({c:mem_map[c]})
        
        #print(f"Amount of NA!!! ::: "  + str(file.isna().sum().sum()) + " of " + str(file.shape[0]) )
        file.drop_duplicates(inplace=True)
        # file.rename(columns={'Attack':'AttackLabel','Label':'IsAttack'},inplace=True)
        file.dropna(inplace=True)
        #file = file.astype(mem_map)
        if(i==0):
            gen_file = file
        else:
            gen_file = pandas.concat( [gen_file , file] )
        i +=1
    print(gen_file)
    gen_file.to_pickle(f"{f}.pkl")
    bf = open('bad_lines.txt','w')
    bf.write( "\n".join(bad_lines) )
    bf.close() 

if mode == 3:
    i=0
    df = None
    for f in files:
        print(f"reading {f}")
        df1 = pandas.read_pickle(f"{f}.pkl")
        if(i == 0):
            df = df1
        else:
            print("concat")
            df = pandas.concat([df,df1])
        df.drop_duplicates(inplace=True)
        print(f"Done {i}")
        i += 1
        
        #print(df1)
        
        #df2 = pandas.read_pickle("output2.pkl")
    
        # df2.to_pickle("output1.pkl")
    
        # df1 = pandas.concat([df1,df2])
        gc.collect()
    df.to_pickle("output.pkl")
    print(df)
    
    #df1 = df1.drop(columns=columns_to_drop)
    #print(df1)

    #print(df1.columns)
    #df1 = pandas.read_pickle("output2.pkl")
    #print(df1)
    #print(df1.columns)



if( mode == 4):
    final_frame = None
    i = 0
    pandas.set_option('use_inf_as_na', True)
    for f in files:
        # read 
        print(f"File {i} ({f}) of {len(files)}")
        # usecols=cols_to_select,
        #file = pandas.read_csv(f,   header=None, names=fields, chunksize=300000 ) # , dtype=mem_map  #  index_col=0  # cant do the mem_map thing if there are invalid values like NA
        file = pandas.read_csv(f, skiprows=8, sep='\t', header=None, names=fields , chunksize=10000000) 

        for i, chunk in enumerate(file):
            chunk = chunk.drop(columns=columns_to_drop)
            print(chunk)
            print(f"Amount of NA!!! ::: "  + str(chunk.isna().sum() ) + " of " + str(chunk.shape[0]) )

            chunk["duration"] = chunk["duration"].replace("-",0)
            chunk["orig_bytes"] = chunk["orig_bytes"].replace("-",0)
            chunk["resp_bytes"] = chunk["resp_bytes"].replace("-",0)
            
            if(chunk.shape[0] < 10000000):
                chunk = chunk.loc[0:chunk.shape[0]-2] # last closing line
                # df = df.loc[0:df.shape[0]-2]

            for c in mem_map:
                print(c)
                chunk = chunk.astype({c:mem_map[c]})

            chunk.drop_duplicates(inplace=True)
            chunk.dropna(inplace=True)

            if(i==0):
                final_frame = chunk 
            else:
                final_frame = pandas.concat([final_frame, chunk])
            print(f"{i}")
    final_frame.to_pickle(f"{f}.pkl")

if mode == 5:
    f = pandas.read_pickle("output_concat.pkl")
    f = f.astype(mem_map)
    f.to_pickle('output_concat.pkl')
    #cols, nas = reduce_mem_usage( f )
    #cols.dtypes.to_csv("info2.csv")
