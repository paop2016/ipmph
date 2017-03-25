import os
class Outputer():
    def __init__(self):
        os.chdir('/users/tong/desktop/章节练习')
    def __call__(self, sectionDic,result):
        try:
            if result:
                with open(self._FileName(sectionDic),'w',encoding='GB18030') as f:
                    f.write(result[0])
                with open(self._FileNameYes(sectionDic),'w',encoding='GB18030') as f:
                    f.write(result[1])
            # else:
            #     with open(self._FileName(sectionDic),'w',encoding='GB18030') as f:
            #         f.write(result)
        except IOError as e:
            print(e)
    def _FileName(self,sectionDic):

        chapterName=sectionDic['chapterName']
        index = chapterName.find('章')
        chapterName = '【' + chapterName[0:index + 1] + '】' + chapterName[index + 1:]

        sum=sectionDic['sectionSum'][3:5]+'道'
        sectionName=sectionDic['sectionName']

        if '中医基础知识' in chapterName:
            index=sectionName.find('、')
            if index != -1:
                sectionName = '【第' + sectionName[0:index] + '节】' + sectionName[index + 1:]
        else:
            index=sectionName.find('节')
            if index!=-1:
                sectionName='【'+sectionName[0:index+1]+'】'+sectionName[index+1:]
        return chapterName+'/'+sectionName+' '+sum+'.doc'
    def _FileNameYes(self,sectionDic):

        chapterName=sectionDic['chapterName']
        index = chapterName.find('章')
        chapterName = '【' + chapterName[0:index + 1] + '】' + chapterName[index + 1:]

        sum=sectionDic['sectionSum'][3:5]+'道'
        sectionName=sectionDic['sectionName']

        if '中医基础知识' in chapterName:
            index=sectionName.find('、')
            if index != -1:
                sectionName = '【第' + sectionName[0:index] + '节】' +'【答案】'+ sectionName[index + 1:]
        else:
            index=sectionName.find('节')
            if index!=-1:
                sectionName='【'+sectionName[0:index+1]+'】'+'【答案】'+sectionName[index+1:]
            else:
                sectionName =sectionName+'【答案】'
        return chapterName+'/'+sectionName+' '+sum+'.doc'