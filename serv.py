import socketserver
#from http.server import BaseHTTPRequestHandler
#from model import *
import pickle
import simplejson
import numpy as np
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from sklearn.preprocessing import StandardScaler 
scaler = StandardScaler()

mlp = pickle.load(open("mlp.pkl","rb"))


class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/x-www-form-urlencoded')
        self.end_headers()
    
    def do_POST(self):
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))     #This can read the input request
        #print("in post method",self.data_string)        #now focus on converting the values in an array
        #********** data_string is bytes object array, which can be accessed as a normal array
        # Now lets convert all the bytes array values to appropriate integer values

        ####Lets convert to str, then split according to '&' and then split according to = then drop odd number of indexes
        str_data = str(self.data_string.decode('utf-8'))
        arr_data = str_data.split('&')
        #print(arr_data)     #Split accorrdingly
        #now let's convert to decoded string
        arr2=[]
        for i in arr_data:
            #i = i.decode('utf-8')
            #print(type(i))
            arr2.append(i.split("="))
            #print(arr2)
        
        arr3=[]
        for i in range(0,len(arr2)):
            arr3.append(arr2[i][1])
        
        #print(arr3)
        count =0
        arr_int=[]
        for i in arr3:
            #print(int(i))
            arr_int.append(int(i))
            count+=1
        #print(arr_int,type(arr_int))
        
        arrr = np.array(arr_int)
        
        #print(arrr,type(arrr))
        response = mlp.predict([arr_int]).tolist()#This is the Json response
        res(response)
        print("Returning response",response)
        return response
def res(response):
    if(response==[1]):
        print("Openness")
    elif(response==[2]):
        print("Conscientiousness")
    elif(response==[3]):
        print("Extraversion")
    elif(response==[4]):
        print("Agreeableness")
    elif(response==[5]):
        print("Neuroticism")
    return res
def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()

# httpd = socketserver.TCPServer(("",8000), MyHandler)
# httpd.serve_forever()
