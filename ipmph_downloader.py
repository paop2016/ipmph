import urllib.parse,urllib.request,http.cookiejar,os,json
class Downloader():
    def __init__(self):
        os.chdir('/users/tong/desktop/章节练习')
        self._login()
    def _login(self):
        userInfo={'UserName':'HP024814',
              'Password':'512512',
              }
        cookie=http.cookiejar.CookieJar()
        self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        # 登入
        self.opener.open('http://sso.ipmph.com/doLogin?Referer=http%3A%2F%2Fexam.ipmph.com%2F',urllib.parse.urlencode(userInfo).encode('utf-8'))
    def downChapter(self,times):
        try:
            response=self.opener.open('http://exam.ipmph.com/learncenter/centre/chapterTraining.zhtml',timeout=3).read()
        except OSError as e:
            print(times)
            if times>0:
                return self.downChapter(times-1)
            return None
        return response
    # def downChapter1(self,times):
    #     try:
    #         data={'_ZVING_DATA':
    #                 '{"_ZVING_METHOD":"MyCourseCentre.listbind","_ZVING_SIZE":50,"_ZVING_AUTOFILL":"true","_ZVING_PAGE":true,"_ZVING_ID":"dl1","Login":"true","UserName":"HP024814","BranchInnerCode":"0001","ExamType":"Ehls00","ExamTypeName":"护士执业","ContextPath":"/learncenter/","_ZVING_TAGBODY":"centre/myCourse.zhtml#958539bc66bcb70980bde274899c6962","_ZVING_PAGEINDEX":0,"_ZVING_PAGETOTAL":-1,"FDBID":"1201","CourseID":"211"}',
    #               '_ZVING_METHOD':'com.zving.framework.ui.control.DataListUI.doWork',
    #               '_ZVING_URL':'%2Flearncenter%2Fcentre%2FmyCourse.zhtml',
    #               '_ZVING_DATA_FORMAT':'json'
    #               }
    #         response = self.opener.open('http://exam.ipmph.com/learncenter/ajax/invoke', urllib.parse.urlencode(data).encode('utf-8'))
    #         html=response.read()
    #         return html
    #     except OSError as e:
    #         print(times)
    #         if times>0:
    #             return self.downChapter1(times-1)
    #         return None
    def downSections(self,result):
        sectionId=[]
        for item in result:
            post1 = {'_ZVING_METHOD': 'com.zving.framework.ui.control.DataListUI.doWork',
                     '_ZVING_URL': '%2Flearncenter%2Fcentre%2FchapterTraining.zhtml',
                     '_ZVING_DATA': '{"_ZVING_METHOD":"TrainCentre.dyList",'
                                    '"_ZVING_AUTOFILL":"true",'
                                    '"_ZVING_ID":"list%s",'
                                    '"Login":"true",'
                                    '"UserName":"HP024814",'
                                    '"BranchInnerCode":"0001",'
                                    '"ExamType":"Ehls00",'
                                    '"ExamTypeName":"护士执业",'
                                    '"ContextPath":"/learncenter/",'
                                    '"_ZVING_PAGE":false,'
                                    '"_ZVING_TAGBODY":"null#6dc4b86bd6981f94c2408953e79f1f9d",'
                                    '"_ZVING_PAGEINDEX":0,'
                                    '"_ZVING_PAGETOTAL":-1,'
                                    '"_ZVING_SIZE":0,'
                                    '"ID":%s}'%(item[0],item[0]),
                     '_ZVING_DATA_FORMAT': 'json'
                     }
            response = self.opener.open('http://exam.ipmph.com/learncenter/ajax/invoke', urllib.parse.urlencode(post1).encode('utf-8'))
            html = response.read().decode('utf-8')
            sectionId.append([item[1],html])
        return sectionId
    def __call__(self, sectionDic):
        # 每一节的所有题
        htmls=''
        nowNum=0
        print(sectionDic)
        self._createFile(sectionDic)
        sectionData={'_ZVING_METHOD':'TrainCentre.load',
                     '_ZVING_URL':'%2Flearncenter%2Fcentre%2FrandomTraining.zhtml',
                     '_ZVING_DATA':'{"key":null,"id":"%s","cookieFlag":"ALL"}'%sectionDic['_id'],
                     '_ZVING_DATA_FORMAT':'json'}
        response=self.opener.open('http://exam.ipmph.com/learncenter/ajax/invoke',urllib.parse.urlencode(sectionData).encode('utf-8')).read().decode('utf-8')
        print(response)
        response=json.loads(response)['Content']
        # 双引号无法解析
        while True:
            htmls+=response
            # 20待定，应取最后一题,可能有bug待观察
            nowNum=nowNum+20
            if nowNum >= int(sectionDic['sectionSum'][3:-1]):
                break
            sectionData={'_ZVING_METHOD':'TrainCentre.load',
                         '_ZVING_URL':'%2Flearncenter%2Fcentre%2FrandomTraining.zhtml',
                         '_ZVING_DATA':'{"key":null,"id":"%s","cookieFlag":"ALL","page":%s,"buttonFlag":"next"}'%(sectionDic['_id'],nowNum),
                         '_ZVING_DATA_FORMAT':'json'}
            response = self.opener.open('http://exam.ipmph.com/learncenter/ajax/invoke', urllib.parse.urlencode(sectionData).encode('utf-8')).read().decode('utf-8')
            response = json.loads(response)['Content']
        # print(htmls)
        return htmls
    def _createFile(self,itemDic):
        chapterName=itemDic['chapterName']
        index=chapterName.find('章')
        chapterName='【'+chapterName[0:index+1]+'】'+chapterName[index+1:]
        if not os.path.exists(chapterName):
            os.mkdir(chapterName)