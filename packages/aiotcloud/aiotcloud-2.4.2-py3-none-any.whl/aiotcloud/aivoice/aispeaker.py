# -*- coding: UTF-8 -*-
from aip import AipSpeech
from aiotcloud.aivoice.playsound import playsound
import threading
from queue import Queue
import os
import shutil

class AiSpeaker(threading.Thread):
    def __init__(self,queue=Queue(),app_id='15421757',app_key='QIAal5mst7QLGY8NGgWCXkuD',secret_key='PK3aFSGffuS3UMtxd1IXN96jyo69HZUV',person=3,speed=5,voice=5,pit=5,launguage='zh'):
        '''
        description: 
        param {*} self
        param {*} queue
        param {*} app_id 你所申请的百度appid
        param {*} app_key 对应的key
        param {*} secret_key key所对应的secret
        param {*} person发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
        param {*} voice音量，取值0-15，默认为5中音量
        return {*}
        使用方法：
        a = AiSpeaker()
        a.speech("我是王二狗",speed=1,person=3)
        '''
        threading.Thread.__init__(self)
        self.client = AipSpeech(app_id, app_key, secret_key)
        self.queue = queue
        self.launguage = launguage
        self.speed = speed
        self.vol = voice
        self.person = person
        self.pit = pit
        if os.path.exists('''.audio/'''):
            shutil.rmtree(".audio/")
        os.mkdir(".audio/")
        self.start()

    def speech(self,text,person=3,speed=5,voice=5,pit=5,launguage='zh'):
        """
        异步播放文字语音
        speed	String	语速，取值0-9，默认为5中语速	否
        pit	    String	音调，取值0-9，默认为5中语调	否
        voice	String	音量，取值0-15，默认为5中音量	否
        person	String	发音人选择, 0为女声，1为男声，
        3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女	否
        """
        self.launguage = launguage
        self.speed = speed
        self.vol = voice
        self.person = person
        self.pit = pit
        self.queue.put(text)

    def speech_sync(self,text,voice=5,speed=5,person=3,pit=5):
        """
        同步语音合成
        speed	String	语速，取值0-9，默认为5中语速	否
        pit	String	音调，取值0-9，默认为5中语调	否
        voice	String	音量，取值0-15，默认为5中音量	否
        person	String	发音人选择, 0为女声，1为男声，
        3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女	否
        """
        result = self.client.synthesis(text, 'zh', 1, {
                'vol': voice,'per':person,
                "spd":speed,"pit":pit
        })
        if not isinstance(result, dict):
            with open('.audio/auido_sync.mp3', 'wb') as f:
                f.write(result)
        playsound('.audio/auido_sync.mp3')

    def run(self):
        while True:
            text = self.queue.get()
            result = self.client.synthesis(text, self.launguage, 2, {
                'vol': self.vol,'per':self.person,
                "spd":self.speed,"pit":self.pit
            })
            if not isinstance(result, dict):
                with open('.audio/auido.mp3', 'wb') as f:
                    f.write(result)
            playsound('.audio/auido.mp3')


