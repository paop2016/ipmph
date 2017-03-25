from bs4 import BeautifulSoup
import json,re
class Parser():
    def __init__(self):
        pass
    def parserChapter(self,html):
        ids=[]
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div',class_='item-hd clearfix'):
            id=item.a['onclick']
            text=item.a.text[:-1]
            if len(id)==12 and text!='超纲':
                ids.append([id[8:11],text])
        return ids
    # def parserChapter1(self,html):
    #     soup = BeautifulSoup(html, 'html.parser')
    #     for item in soup.find_all('div',class_=re.compile('list-group-item')):
    #         print(re.search(r'\'(\d)+\'',item.contents[1].name).group()[1:-1])
    #         print(item.text.split(' ')[1])
    #         # id=item.a['onclick']
    #         # text=item.a['col-sm-7']
    #         # print(id)
    #         # print(text)
    def parserSection(self,data):
        sections=[]
        for item in data:
            chapterName=item[0]
            html=item[1]
            soup = BeautifulSoup(json.loads(html)['HTML'], 'html.parser')
            for item1 in soup.find_all('div', class_='item'):
                # 节名
                sectionName=item1.span.text
                b=item1.find('span',class_="pull-right")
                # 节题量
                sectionSum=b.contents[4].strip()
                if sectionName=='超纲' and sectionSum=='题量：0 道':
                    continue
                # 节id
                sectionId=b.a['onclick'][11:-1]
                sections.append([chapterName,sectionId,sectionName,sectionSum])
        return sections
    def parseHtmls(self,htmls):
        # 无答案
        contentNo=''
        # 有答案
        contentYes=''
        soup=BeautifulSoup(htmls,'html.parser')
        for item in soup.find_all('div',class_='well wells'):
            # 题号
            num=item['name']
            num='#'+num
            # 问题
            question=item.find_all('h2')
            if len(question)==1:
                question=question[0].text
                index = question.find('【')
                if index != -1:
                    question = question[index:]
                question=question.replace(' 题型','')
                question=question.replace('  ',' ')
            elif len(question)==2:
                question0=question[0].text
                question1=question[1].text
                question1= question1.replace(' 题型', '')
                question1=question1.replace('  ',' ')
                index=question1.find('【')
                if index!=-1:
                    question1=question1[index:]
                question=question0+'\n'+question1
            question=question+'：'
            # 备选答案
            answers=''
            answerss=item.find_all('input',type='radio')
            for answer in answerss:
                ansNum=answer['value']
                ansContent=answer.text[3:]
                answers+=ansNum+'、'+ansContent+'\n'
            # 正确答案
            right=item.find('span',class_='fcb m-l-sm').text
            a='%s %s\n%s\n'%(num,question,answers)
            contentNo+=a
            b='%s %s\n%s%s\n\n'%(num,question,answers,right)
            contentYes+=b
        print(contentYes)
        return contentNo,contentYes
