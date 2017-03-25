import ipmph_downloader,ipmph_parser,ipmph_manager,ipmph_outputer,multiprocessing,threading,os
class Spider():
    def __init__(self):
        self.downloader=ipmph_downloader.Downloader()
        self.parser=ipmph_parser.Parser()
        self.manager=ipmph_manager.Manager()
        self.outputer=ipmph_outputer.Outputer()
        # 初始
        self.manager.init()
        # 进入首页
        self.downloader.downChapter(5)
    def downSectionId(self):
        result=self.parser.parserChapter(self.downloader.downChapter(5))
        result=self.parser.parserSection(self.downloader.downSections(result))
        self.manager.save(result)
    def start(self):
        while True:
            # 待下载节信息
            sectionDic=self.manager.getSection()
            # 结束
            if not sectionDic:
                break
            if sectionDic['sectionSum']=='题量：0 道':
                self.outputer(sectionDic,'')
                continue
            # 下载每节内容
            htmls=self.downloader(sectionDic)
            # 返回该节所有题
            result=self.parser.parseHtmls(htmls)
            # 输出到文档
            self.outputer(sectionDic,result)
    # def start2(self):
    #     self.parser.parserChapter1(self.downloader.downChapter1(5))
    def xixi(self):
        ps = []
        for a in range(2):
            p = threading.Thread(target=self.start())
            ps.append(p)
            p.start()
        for s in ps:
            s.join()
    def haha(self):
        ps=[]
        for a in range(7):
            p=multiprocessing.Process(target=self.xixi())
            ps.append(p)
            p.start()
        for s in ps:
            s.join()
def clear():
    data=['第一节','第二节','第三节','第四节','第五节','第六节','第七节',
          '第八节','第九节','第十节','第十一节','第十二节','第十三节',
          '第十四节','第十五节','第十六节','第十七节','第十八节','第十九节',
          '第二十节', '第二十一节', '第二十二节','第二十三节','第二十四节',"附："]
    os.chdir('/users/tong/desktop/章节练习')
    for file in os.listdir():
        if file=='.DS_Store':
            continue
        os.chdir(file)
        for name in data:
            for doc in os.listdir():
                if name in doc:
                    if '【答案】' in doc:
                        try:
                            with open(file+'（答案）.doc','a',encoding='GB18030') as f,open(doc,'r',encoding='GB18030') as f1:
                                sectionName=doc.replace('【答案】','').replace('.doc','\n')
                                f.write(sectionName)
                                f.write(f1.read())
                        except Exception as e:
                            print(e)
                    else:
                        try:
                            with open(file+'.doc','a',encoding='GB18030') as f,open(doc,'r',encoding='GB18030') as f1:
                                sectionName=doc.replace('.doc','\n')
                                f.write(sectionName)
                                f.write(f1.read())
                        except Exception as e:
                            print(e)
        os.chdir('..')
s=Spider()
# s.start2()
s.haha()
# clear()