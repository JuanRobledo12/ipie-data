import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import time

def epoch_to_date(epoch_date):
    epoch_date = epoch_date / 1000
    my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch_date))
    #print(my_time)
    return(my_time)
def spacing():
    print('*\n*\n*')
def select_pollutls(sensor_type):
    if (sensor_type == 'pm'):
        item_ls = ['PM1', 'PM25','PM4', 'PM10']
    elif (sensor_type == 'co2'):
        item_ls = ['CO2']
    elif (sensor_type == 'cov'):
        item_ls = ['TCOV']
    elif (sensor_type == 'hum'):
        item_ls = ['HR', 'Temp']
    return item_ls
def select_unit(measure):
    if(measure == 'CO2'):
        unit_t = 'ppm'
    elif(measure == 'TCOV'):
        unit_t = 'ppb'
    elif(measure == 'HR'):
        unit_t = '%'
    elif(measure == 'Temp'):
        unit_t = 'C°'
    elif(measure == 'PM1' or measure == 'PM25' or measure == 'PM4' or measure == 'PM10'):
        unit_t = 'ug/m3'
    return unit_t
print('Welcome to get_graphs from IPIestacion data program!\n')
time.sleep(1)

#Variables
x_val = []
y_val = []
ipie_id_ls = []
pollut_ls = []
sensor_ls = ['pm', 'co2', 'cov', 'hum']
usr_input = None
event_name = input('Input the event or experiment name for the csv files you want to plot: \n')

while True:
    usr_input = input("Please input IPIE ID (2 digits MAX), input 'no' when done: ")
    if(usr_input == 'no'):
        break
    try:
        int(usr_input)
    except:
        print("IPIE ID must be ONLY numbers")
        continue
    if (len(usr_input) > 2):
        print("IPIE ID must be MAX 2 digits")
        continue

    ipie_id_ls.append(usr_input)
spacing()
print("The following IDs' data will be plotted and saved: ", ipie_id_ls, '\n')

for id in ipie_id_ls:
    for sensor in sensor_ls:
        print('-------------')
        print('Processing data for ', sensor ,' in IPIE',id)
        try:
            df = pd.read_csv('/home/tony/ipie_python/ipie_csv/'+ event_name +'_IPIE' + id + '_' + sensor + '.csv')
        except:
            print('======== Error: No data was found for ', sensor, 'in IPIE ', id, ' ========')
            continue
        for epoch in df['Tiempo']:
                x_val.append(epoch_to_date(float(epoch)))
        datenum = md.date2num(x_val)
        pollut_ls = select_pollutls(sensor)
        for pollut in pollut_ls:
            for pollutval in df[pollut]:
                y_val.append(float(pollutval))
            print(pollut,' data items: ',len(y_val))
            plt.figure(figsize=(20,10)) #width, height
            plt.title('IPIE ' + id + ': ' + pollut.upper() + ' vs Time') #CHECK FOR HR, TEMP
            plt.xlabel("fecha y hora")
            plt.ylabel(select_unit(pollut))
            plt.xticks(rotation=25)
            plt.grid()
            ax = plt.gca()
            xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
            ax.xaxis.set_major_formatter(xfmt)
            plt.plot(datenum, y_val)
            plt.savefig('/home/tony/ipie_python/ipie_fig/'+ event_name + '_' + pollut +'_IPIE' + id + '.png', bbox_inches = 'tight')
            time.sleep(1)
            plt.close()
            y_val.clear()
        print('-------------')
        x_val.clear()
        pollut_ls.clear()
print("\nThe figures where saved succesfully!!!")
print("Quitting...")
exit()
