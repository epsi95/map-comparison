from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
import csv
import random
import string
import requests
import threading
from kivy.clock import Clock
import time
import json


mmi_key = 't2uaa6hi5u31edzll3j361ugrr2xm45r'
APP_ID = '0INBjWlPQChfUSn13p4b'
APP_CODE = 'H9io3_9HVYbAv2nnhndrhQ'
google_key = 'AIzaSyBFG_9Kim0fZCZHC2xxe1N-z8Q_OQQxF20'


Window.clearcolor = (219/255, 219/255, 192/255, 0.4)

zoom_level_mmi = 15
zoom_level_google = 15
zoom_level_here = 15
lat = 28.4950116
lon = 77.0641847

data_mmi = {}
data_google = {}
data_here = {}

flag = 3

mmi_google = 0
here_google = 0
mmi_here = 0
row_len = 0
co_ordinate_list = []
index = 0
report = []

class MainWindow(BoxLayout):
    mmi_id = ObjectProperty()
    google_id = ObjectProperty()
    here_id = ObjectProperty()
    lat_ = ObjectProperty()
    lon_ = ObjectProperty()
    mmi_dtls = ObjectProperty()
    google_dtls = ObjectProperty()
    here_dtls = ObjectProperty()
    csv_path = ObjectProperty()
    comment = ObjectProperty()
    mmi_gogl = ObjectProperty()
    mmi_google_ = ObjectProperty()
    here_gogl = ObjectProperty()
    here_google_ = ObjectProperty()
    mmi_hre = ObjectProperty()
    here_mmi_ = ObjectProperty()

    def stop(self):
        Clock.unschedule(self.auto_wm)
        Clock.unschedule(self.auto_wtm)

    def auto_wm(self, dt):
        global index, row_len
        if(index + 1 == row_len):
            index += 1
        self.next('NaN')
        if (index+1 > row_len):
            self.gen_rep()
            exit()

    def automate_wm(self):
        Clock.schedule_interval(self.auto_wm, 7)


    def auto_wtm(self, dt):
        global index, row_len
        if(index + 1 == row_len):
            index += 1
        self.next_new('NaN')
        if (index+1 > row_len):
            self.gen_rep()
            exit()

    def automate_wtm(self):
        Clock.schedule_interval(self.auto_wtm, 3)


    def report_manager(self,tp):
        global report, mmi_google, here_google, mmi_here
        #mmi_google =
        #here_google =
        #mmi_here =
        try:
            if(len(report)>0):
                #print('$$', report[len(report)-1][0], co_ordinate_list[index][0])
                #print('$$', report[len(report)-1][1], co_ordinate_list[index][1])
                if(report[len(report)-1][0] == co_ordinate_list[index][0]):
                    if (report[len(report)-1][1] == co_ordinate_list[index][1]):
                        return
                    else:
                        temp = [co_ordinate_list[index][0], co_ordinate_list[index][1], tp, mmi_google, here_google, mmi_here]
                        report.append(temp)
                        #print(report)
                else:
                    temp = [co_ordinate_list[index][0], co_ordinate_list[index][1], tp, mmi_google, here_google, mmi_here]
                    report.append(temp)
                    #print('$$',report)
            else:
                temp = [co_ordinate_list[index][0], co_ordinate_list[index][1], tp, mmi_google, here_google, mmi_here]
                report.append(temp)
                #print(report)
        except:
            #print('error')
            self.comment.text = '<previous Error!>    No more Latitude, Longitude left'

    def mmi_mat(self):
        global data_mmi
        mmi_cont = []
        dump = []
        try:
            for item in data_mmi['results'][0]:
                if (item != 'formatted_address'):
                    mmi_cont.append(data_mmi['results'][0][item])
        except:
            mmi_cont = 'NaN'
        mmi_cont = list(filter(None, mmi_cont))
        for item in mmi_cont:
            for items in [x.strip() for x in item.split(' ')]:
                dump.append(items)

        #print('$$$', dump)
        return(set(dump))

    def google_mat(self):
        global data_google
        dump = []
        try:
            my_string = data_google['results'][0]['formatted_address']
        except:
            my_string = 'NaN'
        google_cont = [x.strip() for x in my_string.split(',')]

        for item in google_cont:
            for items in [x.strip() for x in item.split(' ')]:
                dump.append(items)
        return(set(dump))

    def here_mat(self):
        global data_here
        dump = []
        a = data_here['Response']['View'][0]['Result'][0]['Location']['Address']['Label']
        a_cont = [x.strip() for x in a.split(',')]
        for item in a_cont:
            for items in [x.strip() for x in item.split(' ')]:
                dump.append(items)
        dump.append(data_here['Response']['View'][0]['Result'][0]['Location']['Address']['PostalCode'])
        for item in (data_here['Response']['View'][0]['Result'][0]['Location']['Address']['AdditionalData']):
            dump.append(item['value'])

        return(set(dump))

    def mmi_google(self):
        global mmi_google
        global flag
        flag = 3
        temp = ''
        mmi = self.mmi_mat()
        google = self.google_mat()
        here = self.here_mat()
        a = (len(mmi)+len(google)+len(here))/3
        #print(len(mmi & google), min(len(mmi),len(google)))
        mmi_google = int((len(mmi & google)/a)*100)
        self.mmi_gogl.text = str(mmi_google)+' %'
        for i in mmi & google:
            temp = temp +i + ', '
        #print(temp)
        self.mmi_google_.text = str(temp)
        #print(mmi & google)

    def here_google(self):
        global flag
        global here_google
        flag = 3
        temp = ''
        mmi = self.mmi_mat()
        google = self.google_mat()
        here = self.here_mat()
        a = (len(mmi) + len(google) + len(here)) / 3

        #print(len(here & google), min(len(here),len(google)))
        here_google = int((len(here & google)/a)*100)
        self.here_gogl.text = str(here_google)+' %'
        for i in here & google:
            temp = temp +i + ', '
        #print(temp)
        self.here_google_.text = str(temp)
        #print(here & google)

    def here_mmi(self):
        global flag
        global mmi_here
        flag = 3
        temp = ''
        mmi = self.mmi_mat()
        google = self.google_mat()
        here = self.here_mat()
        a = (len(mmi) + len(google) + len(here)) / 3

        #print(len(here & google), min(len(here),len(google)))
        mmi_here = int((len(here & mmi)/a)*100)
        self.mmi_hre.text = str(mmi_here)+' %'
        for i in here & mmi:
            temp = temp +i + ', '
        #print(temp)
        self.here_mmi_.text = str(temp)
        #print(here & mmi)



    def gen_rep(self):
        global report
        #print(report)
        fields = ['Lat', 'Long', 'Status', 'MMI_GOOGLE', 'HERE_GOOGLE', 'MMI_HERE']
        filename = 'report_'+''.join(random.choices(string.ascii_uppercase + string.digits, k=5))+'.csv'
        with open(filename, 'w', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(fields)

            # writing the data rows
            csvwriter.writerows(report)
        self.comment.text = '<Info!>'+'    Report generated successfully'

        #print(report)



    def next_new(self, tp):
        global row_len
        global co_ordinate_list
        global lat
        global lon
        global index
        global report

        if (len(report) >= 100):
            self.gen_rep()
            report = []
        if(index+1 < row_len):
            self.report_manager(tp)
            index += 1
            #print('***',co_ordinate_list, index)
            lat = co_ordinate_list[index][0]
            lon = co_ordinate_list[index][1]
            #print(lat, lon)
            self.adress_put()
            self.lat_.text = str(lat)
            self.lon_.text = str(lon)
            self.comment.text = '<Info!>    Co-ordinate: ' + str(index + 1) + ' of ' + str(row_len)
        else:
            self.report_manager(tp)
            #print('list exhausted')
            self.comment.text = '<previous Error!>    No more Latitude, Longitude left'



    def next(self, tp):

        global row_len
        global co_ordinate_list
        global lat
        global lon
        global index
        global report

        if(len(report) >= 100):
            self.gen_rep()
            report = []
        if(index+1 < row_len):
            self.report_manager(tp)
            index += 1
            #print('***',co_ordinate_list, index)
            lat = co_ordinate_list[index][0]
            lon = co_ordinate_list[index][1]
            #print(lat, lon)
            self.set_image()
        else:
            self.report_manager(tp)
            #print('list exhausted')
            self.comment.text = '<previous Error!>    No more Latitude, Longitude left'

    def set_image(self):

        self.adress_put()
        self.lat_.text = str(lat)
        self.lon_.text = str(lon)
        self.set_mmi()
        self.set_google()
        self.set_here()
        self.comment.text = '<Info!>    Co-ordinate: ' + str(index+1) + ' of ' + str(row_len)



    def adress_put(self):
        global lat, lon
        #print('###', 'address put initiated')
        lat_long = str(lat) + ',' + str(lon)
        """url_mmi = 'https://apis.mapmyindia.com/advancedmaps/v1/e95rvnlk1luizrbr9nqqvzbaqmqmi2gw/rev_geocode?lat='+str(lat)+'&lng='+str(lon)
        url_google = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+lat_long+'&key=AIzaSyBFG_9Kim0fZCZHC2xxe1N-z8Q_OQQxF20'
        url_here = 'https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?prox='+lat_long+'&mode=retrieveAddresses&maxresults=1&gen=9&app_id=0INBjWlPQChfUSn13p4b&app_code=H9io3_9HVYbAv2nnhndrhQ'"""
        url_mmi = ('https://apis.mapmyindia.com/advancedmaps/v1/{}/rev_geocode?lat=' + str(lat) + '&lng=' + str(lon)).format(mmi_key)
        url_google = ('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + lat_long + '&key={}').format(google_key)
        url_here = ('https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?prox=' + lat_long + '&mode=retrieveAddresses&maxresults=1&gen=9&app_id={}&app_code={}').format(APP_ID, APP_CODE)

        '''request1 = UrlRequest(url_mmi, self.mmi_adress_put, print('redirect'), print('failed'), print('error'), print('progress'))
        request2 = UrlRequest(url_google, self.google_adress_put)
        request3 = UrlRequest(url_here, self.here_adress_put)'''

        t1 = threading.Thread(target=self.mmi_adress_put, args=(url_mmi,))
        t2 = threading.Thread(target=self.google_adress_put, args=(url_google,))
        t3 = threading.Thread(target=self.here_adress_put, args=(url_here,))
        '''self.mmi_adress_put(url_mmi)
        self.google_adress_put(url_google)
        self.here_adress_put(url_here)'''
        t1.start()
        t2.start()
        t3.start()

        #t1.join()
        #t2.join()
        #t3.join()


    def mmi_adress_put(self, url):
        #print('###', 'got mmi dada')
        data = requests.get(url).json()
        try:
            data = json.loads(data.decode()) if not isinstance(data, dict) else data
        except:
            exit()

        global data_mmi
        data_mmi = data
        global flag
        flag += -1
        if(flag == 0):
            self.mmi_google()
            self.here_google()
            self.here_mmi()

        #print(data['results'][0]['formatted_address'])
        self.mmi_dtls.text = data['results'][0]['formatted_address']

    def google_adress_put(self, url):
        data2 = requests.get(url).json()
        try:
            data2 = json.loads(data2.decode()) if not isinstance(data2, dict) else data2
        except:
            exit()

        global data_google
        data_google = data2
        global flag
        flag += -1
        if (flag == 0):
            self.mmi_google()
            self.here_google()
            self.here_mmi()
        #print(data2['results'][0]['formatted_address'])
        #print(data2)

        self.google_dtls.text = data2['results'][0]['formatted_address']

    def here_adress_put(self, url):
        data = requests.get(url).json()
        try:
            data = json.loads(data.decode()) if not isinstance(data, dict) else data
        except:
            exit()


        global data_here
        data_here = data
        global flag
        flag += -1
        if (flag == 0):
            self.mmi_google()
            self.here_google()
            self.here_mmi()
        #print(data)
        self.here_dtls.text = data['Response']['View'][0]['Result'][0]['Location']['Address']['Label'] +' pin - '+ data['Response']['View'][0]['Result'][0]['Location']['Address']['PostalCode']




    def set_mmi(self):
        global zoom_level_mmi
        global lat, lon
        lat_long = str(lat) + ',' + str(lon)
        #self.mmi_id.source = 'https://apis.mapmyindia.com/advancedmaps/v1/juj6ynf5u5f9x99oon962pmuzk2tkz64/still_image?center=' + lat_long + '&zoom=' + str(zoom_level_mmi) + '&size=800x480&ssf=&markers=' + lat_long
        self.mmi_id.source = ('https://apis.mapmyindia.com/advancedmaps/v1/{}/still_image?center=' + lat_long + '&zoom=' + str(zoom_level_mmi) + '&size=800x480&ssf=&markers=' + lat_long).format(mmi_key)
    def set_google(self):
        global zoom_level_google
        global lat, lon
        lat_long = str(lat) + ',' + str(lon)
        #self.google_id.source = 'https://maps.googleapis.com/maps/api/staticmap?center=' + lat_long + '&zoom=' + str(zoom_level_google) + '&size=800x480&maptype=roadmap&markers=color:red%7Clabel:O%7C' + lat_long + '&key=AIzaSyBFG_9Kim0fZCZHC2xxe1N-z8Q_OQQxF20'
        self.google_id.source = ('https://maps.googleapis.com/maps/api/staticmap?center=' + lat_long + '&zoom=' + str(zoom_level_google) + '&size=800x480&maptype=roadmap&markers=color:red%7Clabel:O%7C' + lat_long + '&key={}').format(google_key)
    def set_here(self):
        global lat, lon
        lat_long = str(lat) + ',' + str(lon)
        global zoom_level_here
        #self.here_id.source = 'https://image.maps.api.here.com/mia/1.6/mapview?app_id=0INBjWlPQChfUSn13p4b&app_code=H9io3_9HVYbAv2nnhndrhQ&poi=' + lat_long + '&ctr=' + lat_long + '&poithm=1&f=0&z=' + str(zoom_level_here) + '&poifc=red&w=800&h=480&ppi=250'
        self.here_id.source = ('https://image.maps.api.here.com/mia/1.6/mapview?app_id={}&app_code={}&poi=' + lat_long + '&ctr=' + lat_long + '&poithm=1&f=0&z=' + str(zoom_level_here) + '&poifc=red&w=800&h=480&ppi=250').format(APP_ID, APP_CODE)
    def mmi_zoom(self,val):
        global zoom_level_mmi

        if (val == 1):
            if (zoom_level_mmi <= 17):
                zoom_level_mmi+=1
                #print(zoom_level_mmi)
                self.set_mmi()
        if (val == 0):
            if (5<=zoom_level_mmi <= 18):
                zoom_level_mmi+=-1
                #print(zoom_level_mmi)
                self.set_mmi()

    def here_zoom(self,val):
        global zoom_level_here

        if (val == 1):
            if (zoom_level_here <= 19):
                zoom_level_here+=1
                #print(zoom_level_here)
                self.set_here()
        if (val == 0):
            if (1<=zoom_level_here <= 20):
                zoom_level_here+=-1
                #print(zoom_level_here)
                self.set_here()

    def google_zoom(self,val):
        global zoom_level_google

        if (val == 1):
            if (zoom_level_google <= 19):
                zoom_level_google+=1
                #print(zoom_level_google)
                self.set_google()
        if (val == 0):
            if (1<=zoom_level_google <= 20):
                zoom_level_google+=-1
                #print(zoom_level_google)
                self.set_google()

    def load_csv(self):
        global row_len
        global co_ordinate_list
        global lat
        global lon
        global index
        global report



        path = self.csv_path.text.strip()
        #print(path)
        fields = []
        rows = []
        try:
            with open(path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                fields = next(csvreader)
                for row in csvreader:
                    rows.append(row)
            row_len = csvreader.line_num -1
            self.comment.text = '<Info!>    Co-ordinate: '+str(index+1)+' of '+str(row_len)
            co_ordinate_list.clear()
            report.clear()
            #print(row_len)
            for row in rows:
                co_ordinate_list.append(row)
            #print(co_ordinate_list)
            lat = co_ordinate_list[index][0]
            lon = co_ordinate_list[index][1]
            #print(lat,lon)
            self.set_image()
        except:
            self.comment.text = '<previous Error!>    Unable to load .csv file'


class navigation(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    navigation().run()