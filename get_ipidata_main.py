import urllib.request, urllib.parse, urllib.error
import ssl
import time
import pandas as pd
import calendar

def date_to_epoch(h_date):
    time_format = '%Y-%m-%d %H:%M:%S'
    #IPIEstacion send actual data in GMT
    epoch_date = int(calendar.timegm(time.strptime(h_date,time_format))) * 1000
    return epoch_date
def epoch_to_date(epoch_var):
    epoch_var = float(epoch_var) / 1000
    my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch_var))
    return my_time
def spacing():
    print('*\n*\n*')

#API Parameters
service_url = 'http://youilab.ipicyt.edu.mx/ipiestacion/'
start_date = None
end_date = None

#Other
ipie_id_ls = list()
sensor_ls = ['pm', 'hum', 'cov', 'co2']
api_params = dict()
date_ls = list()

#Ignore SSL certification errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Welcome!
print('Welcome to the get_data program for the IPIestacion!\n')
time.sleep(1)
event_name = input('Please input the event or experiment name for the csv files (AVOID SPECIAL CHARACTERS): \n')

#Set IPIE ids you want to consult
while True:
    usr_input = input("Please input the IPIE ID (2 digits max), input 'no' when done: ")
    if(usr_input == 'no'):
        break
    try:
        int(usr_input)
        ipie_id_ls.append(usr_input)
    except:
        print("===== Error: IPIE ID must be ONLY numbers =====")
        continue
    if (len(usr_input) > 2):
        print("===== Error: IPIE ID must be MAX 2 digits =====")
        continue

#Set time range for query
while True:
    start_date = input('Input start date in the format yyyy-mm-dd hh:mm:ss\n')
    end_date = input('Input end date in format yyyy-mm-dd hh:mm:ss\n')
    try:
        start_date = date_to_epoch(start_date)
        end_date = date_to_epoch(end_date)
        spacing()
        break
    except:
        print("===== Error: time data does not match format '%Y-%m-%d %H:%M:%S' =====")
        continue
print("Getting data for the following IDs: ", ipie_id_ls)
print('Starting program...')
spacing()

#Main loop for retrieving data
for ipie_id in ipie_id_ls:
    for sensor_type in sensor_ls:
        api_params['start'] = start_date
        api_params['end'] = end_date
        new_url = service_url + ipie_id + '/' + sensor_type + '/csv?'
        req_url = new_url + urllib.parse.urlencode(api_params)
        print('Getting data from: ', req_url)
        spacing()
        try:
            data = pd.read_csv(req_url)
        except:
            print('======= Error: No data was found for '+ sensor_type +'in IPIE', ipie_id, ' =======')
            continue
        epoch_ls = data['Tiempo']
        for epoch_date in epoch_ls:
            date_ls.append(epoch_to_date(epoch_date))
    
        data['Date'] = date_ls
        #print(data)
        date_ls.clear()
        api_params.clear()
        data.to_csv('/home/tony/ipie_python/ipie_csv/'+ event_name +'_IPIE' + ipie_id + '_' + sensor_type + '.csv')
print('Succesfull creation of CSV files! \n Quitting progra...')
exit()

