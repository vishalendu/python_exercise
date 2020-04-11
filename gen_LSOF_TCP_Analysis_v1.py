import pandas as pd
import resource

def getCurrentMemoryUsage():
    return(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

def generateTCPSummary(infile,outfile):
    # Read lsof
    cols=['COMMAND' ,'PID','TID', 'USER', 'FD' ,'TYPE' ,'DEVICE' \
                   ,'SIZE/OFF' ,'NODE', 'NETWORK_INFO' ,'CONN_STATUS']
    dt = {'PID':'object','TID':'category','USER':'category','FD':'category',\
          'TYPE':'category','DEVICE':'category','SIZE/OFF':'category','CONN_STATUS':'category',\
          'NODE':'category','COMMAND':'object','NETWORK_INFO':'object'}
    lsof1 = pd.read_csv(infile,sep="\s+",\
                        header=None,skiprows=1,names=cols,dtype=dt)
    print(f'After loading file Memory = {getCurrentMemoryUsage()/(1024*1024)} MB')

    # Filter by TCP and extract TO/FROM IP/PORTS
    tcp = lsof1[(lsof1['CONN_STATUS']!='(LISTEN)') & (lsof1['NODE']=='TCP')]
    tcp = pd.concat([tcp,tcp['NETWORK_INFO'].str.extract(r'(.+?):(.+?)->(.+?):(.+?)$')],axis=1).\
    rename(columns={0:'FROM_IP',1:'FROM_PORT',2:'TO_IP',3:'TO_PORT'})
    for i in ['FROM_IP','FROM_PORT','TO_IP','TO_PORT']:
        tcp[i]=tcp[i].astype('category')
    tcp['COUNT'] = 1
    print(f'After formatting dataframe Memory = {getCurrentMemoryUsage()/(1024*1024)} MB')

    # Generate summary
    pd.crosstab([tcp.PID,tcp.COMMAND,tcp.FROM_IP,tcp.TO_IP,tcp.CONN_STATUS,tcp.TYPE],tcp.COUNT).sort_values(1,ascending=False).to_csv(outfile)
    print(f'Final Memory = {getCurrentMemoryUsage()/(1024*1024)} MB')

infile = '/Users/vishalendupandey/Downloads/lsof/lsof.txt'
outfile = '/Users/vishalendupandey/Downloads/lsof/analysis.csv'
generateTCPSummary(infile,outfile)
