import json
from urllib import response

import requests


class ApiPost():
    def __init__(self):
        self.base_url_post = 'https://api.judge0.com/submissions?base64_encoded=false&wait=false'
        self.base_url_get = 'https://api.judge0.com/submissions/'


    def __getReponse(self, token):
        s = requests.get(self.base_url_get+token+'?base64_encoded=false')
        status = s.status_code
        reponse = s.text
        reponse = json.loads(reponse)

        return status, reponse
    
    def postCode(self ,code, lang_id, result):
        datas = {
            "source_code": code,
            "language_id": lang_id,
            "expected_output": result
        }

        r = requests.post(self.base_url_post,json = datas)
        status = r.status_code
        reponse = r.text
        reponse = json.loads(reponse)
        
        token = reponse['token']

        print(reponse)

        print(status)

        status, data = self.__getReponse(token)

        while data['status']['id'] == 1 or data['status']['id'] == 2 :
            status, data = self.__getReponse(token)     
        return status, data

    def testCode(self ,code, lang_id):
        datas = {
            "source_code": code,
            "language_id": lang_id,
            
        }

        r = requests.post(self.base_url_post,json = datas)
        status = r.status_code
        reponse = r.text
        reponse = json.loads(reponse)
        
        token = reponse['token']

        print(reponse)

        print(status)

        status, data = self.__getReponse(token)

        while data['status']['id'] == 1 or data['status']['id'] == 2 :
            print(data['status']['id'])
            status, data = self.__getReponse(token)        
        return status, data


class DartAPI():
    
    def __init__(self):
        self.base_url = 'http://parserdjango.herokuapp.com/compile'  
        
    def postCodeDart(self,code, result):
        data = {
            'code':code,
            'excepted_result':result,
            'language':34,
            'apikey':"52ffd1375224c67b1bf9633699db9a8e8c59c64448fc5778bd465b33dad275105ec3997c49e2809bdf2ef9f264760c21c0a77aee6a42ff0325216449a9b643f4"
        }
        req = requests.post(self.base_url,data)
        status = req.status_code
        reponse = req.text
        response = json.loads(reponse)
        return response
    
    def postCodeTestDart(self,code):
        
        data = {
            'code':code,
            'language':34,
            'excepted_result':'',
            'apikey':"52ffd1375224c67b1bf9633699db9a8e8c59c64448fc5778bd465b33dad275105ec3997c49e2809bdf2ef9f264760c21c0a77aee6a42ff0325216449a9b643f4"
        }
        req = requests.post(self.base_url,data)
        status = req.status_code
        reponse = req.text
        response = json.loads(reponse)
        return response
                
                


class Note():

    def CalCpourcentage(self,levelUser,totalTentativeUser,totalLevel):
            if totalTentativeUser < levelUser:    
                return 0 
            if levelUser > totalLevel:
                return 0
            else:
                return (levelUser*100)/totalLevel - ((totalTentativeUser-levelUser)/totalTentativeUser)