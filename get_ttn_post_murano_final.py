'''
    Title: TTN REST API node data to Exosite Murano
    Author: Marco Sanchez
    Description:
            This program was written to retrieve node data sent by the user to the TTN REST API.
            The data is available here:https://www.thethingsnetwork.org/api/v0/nodes/<your_node_eui>/
            Essentially, we use a GET request to obtain the data, and then we use a POST request to send
            the desired data up to the Exosite Murano application where you are then able to create a
            visualization for your node data.
'''
import requests
import json
import time

#Defining parameters to use in GET request
url = 'https://www.thethingsnetwork.org/api/v0/nodes/21426384/?limit=1'
headers1 = {'Content-Type':'application/json'}

#Send a GET request to the defined url. Print results
r = requests.get(url, headers=headers1)
node_data = r.text
print '***************************************************************************************************'
print '                                     INITIALIZING GET REQUEST'
print '***************************************************************************************************'
print ''

print 'GET request sent to the follwoing URL:'
print r.url
print ''
print 'Status code:'
status_code = r.status_code
print status_code
if (status_code == 200):
    print 'OK'
else:
    print 'ERROR'
print ''
print 'Any Errors?'
print r.raise_for_status()
print ''
print 'Original data from TTN REST API:'
print ''
print node_data
print ''

#Remove the brackets from var string to format into a proper json string.
#This allows us to successfully use the json.loads

remv = "[]"  #character to be removed

for char in remv:               #Replace charater with ""....basically a delete
    node_data = node_data.replace(char,"")
    
print 'Modified data after removing unwanted characters [ ]'
print ''
print node_data           #Verify unwanted characters were removed
print ''
print ''
print '---------------------------------------------------------------------------------------------------'
print '                                 PARSED DATA PARAMETERS AVAILABLE'
print '---------------------------------------------------------------------------------------------------'
print ''

#Parse for desired values in json string
j = json.loads(node_data)
gateway_eui = j['gateway_eui']
tiempo_old = j['time']
datarate = j['datarate']
rssi = j['rssi']
data_plain = j['data_plain']
data = j['data']
node_eui = j['node_eui']
frequency = j['frequency']
data_raw = j['data_raw']
snr = j['snr']

print 'Gateway EUI:'
print gateway_eui
print ''
print 'Node EUI:'
print node_eui
print ''
print 'Time:'
print tiempo_old
print ''
print 'Datarate:'
print datarate
print ''
print 'Frequency:'
print frequency
print ''
print 'Received Signal Strength Indicator:'
print rssi
print ''
print 'Signal to Noise Ratio:'
print snr
print ''
print 'Data in ASCII:'
print data_plain
print ''
print 'Data in Base 64:'
print data
print ''
print 'Raw Data:'
print data_raw
print ''
print ''
print '///////////////////////////////////////////////////////////////////////////////////////////////////'
print '                                     END OF GET REQUEST'
print '///////////////////////////////////////////////////////////////////////////////////////////////////' 
print ''
print ''
print '***************************************************************************************************'
print '                                     INITIALIZING POST REQUEST'
print '***************************************************************************************************'
print ''

#Initializing variables for POST request
cik = 'YOUR DEVICE UNIQUE CIK' #Unique CIK given for each device
url = 'http://m2.exosite.com/onep:v1/stack/alias?state'
headers2 = {'X-Exosite-CIK': cik, 'content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
payload = {'Message' : data_plain , 'Frequency' : frequency , 'Datarate': datarate ,
           'Gateway_EUI': gateway_eui ,'snr': snr , 'raw_data': data_raw ,
           'rssi': rssi ,'Time': tiempo_old ,'Node_EUI': node_eui , 'Data64': data}
#data to be sent to Exosite Portals
#'message' & 'number' are alias in Exosite
                                                        
r1 = requests.post(url, data=payload, headers=headers2) #POST request
print 'POST request sent to the following URL:'
print r1.url
print ''
print 'Status Code:'
status2_code = r1.status_code
print status2_code
if (status2_code == 204):
    print 'No Content'
else:
    print 'ERROR'
print ''
print 'Any Errors?'
print r1.raise_for_status()
print ''
print ''
print '///////////////////////////////////////////////////////////////////////////////////////////////////'
print '                                     END OF POST REQUEST'
print '///////////////////////////////////////////////////////////////////////////////////////////////////'
print ''
print ''

if (status_code == 200 and status2_code == 204):
    print '==================================================================================================='
    print '                                GET & POST REQUESTS WERE SUCCESSFUL! :]'
    print '==================================================================================================='

else:
    print '==================================================================================================='
    print '                                GET & POST REQUESTS WERE UNSUCCESSFUL...  :['
    print '===================================================================================================' 
time.sleep(5)  # Delay for 5 seconds

while True:
    url = 'https://www.thethingsnetwork.org/api/v0/nodes/21426384/?limit=1'
    headers1 = {'Content-Type':'application/json'}
    r = requests.get(url, headers=headers1)
    node_data = r.text
    print ''
    print '                                    ----------------------------'
    print '                                     CHECKING FOR NEW TIMESTAMP'
    print '                                    ----------------------------'
    print ''

    #Remove the brackets from var string to format into a proper json string.
    #This allows us to successfully use the json.loads

    remv = "[]"  #character to be removed

    for char in remv:               #Replace charater with ""....basically a delete
        node_data = node_data.replace(char,"")

    #Parse for desired values in json string
    j = json.loads(node_data)
    gateway_eui = j['gateway_eui']
    tiempo_new = j['time']
    datarate = j['datarate']
    rssi = j['rssi']
    data_plain = j['data_plain']
    data = j['data']
    node_eui = j['node_eui']
    frequency = j['frequency']
    data_raw = j['data_raw']
    snr = j['snr']

    if tiempo_new != tiempo_old :
        print "Different timestamp, will POST now!"
        print tiempo_old
        print ''
        print ''
        print '                                     POSTING...'
        print ''

        cik = 'YOUR DEVICE UNIQUE CIK' #Unique CIK given for each device
        url = 'http://m2.exosite.com/onep:v1/stack/alias?state'
        headers2 = {'X-Exosite-CIK': cik, 'content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
        payload = {'Message' : data_plain , 'Frequency' : frequency , 'Datarate': datarate ,
           'Gateway_EUI': gateway_eui ,'snr': snr , 'raw_data': data_raw ,
           'rssi': rssi ,'Time': tiempo_new ,'Node_EUI': node_eui , 'Data64': data}
        #data to be sent to Exosite Portals
        #'message' & 'number' are alias in Exosite
        r1 = requests.post(url, data=payload, headers=headers2) #POST request

        status2_code = r1.status_code
        print status2_code
        if status2_code == 204 :
            print "                                 POST WAS SUCCESSFUL!"
        else:
            print "                                 POST WAS UNSUCCESSFUL.."

        print ''
        tiempo_old = tiempo_new
    else:
        print "Same timestamp, will not POST!"
        
        tiempo_old = tiempo_new
        print tiempo_old
        print ''
        
    time.sleep(7)  # Delay for 7 seconds

