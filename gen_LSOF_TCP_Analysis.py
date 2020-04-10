import pandas as pd

def generateTCPSummary(infile,outfile):
    # Read lsof
    cols=['COMMAND' ,'PID','TID', 'USER', 'FD' ,'TYPE' ,'DEVICE' \
                   ,'SIZE/OFF' ,'NODE', 'NETWORK_INFO' ,'CONN_STATUS']
    lsof1 = pd.read_csv(infile,sep="\s+",\
                        header=None,skiprows=1,names=cols)

    # Filter by TCP and extract TO/FROM IP/PORTS
    tcp = lsof1[(lsof1['CONN_STATUS']!='(LISTEN)') & (lsof1['NODE']=='TCP')]
    tcp = pd.concat([tcp,tcp['NETWORK_INFO'].str.extract(r'(.+?):(.+?)->(.+?):(.+?)$')],axis=1).\
    rename(columns={0:'FROM_IP',1:'FROM_PORT',2:'TO_IP',3:'TO_PORT'})

    # Generate summary
    ip_summary = pd.DataFrame(tcp.groupby(['PID','COMMAND','FROM_IP','TO_IP','CONN_STATUS','TYPE']).\
       COMMAND.count()).rename(columns={'COMMAND':'COUNT'}).sort_values('COUNT',ascending=False)
    ip_summary.to_csv(outfile)

infile = '/Users/vishalendupandey/Downloads/lsof/lsof.txt'
outfile = '/Users/vishalendupandey/Downloads/lsof/analysis.csv'
generateTCPSummary(infile,outfile)
