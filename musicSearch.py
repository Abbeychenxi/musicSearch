# -*- coding: UTF-8 -*-
import sys,os,codecs
sys.path.append("../")
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer

class Search():
    def GetFileList(self, FindPath):
        FileNames = os.listdir(FindPath)
        return FileNames

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=self.analyzer))
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        ix = create_in("tmp", schema) # for create new index
        #ix = open_dir("tmp") # for read only
        writer = ix.writer()
        self.init(writer, ix)

    def init(self, writer, ix):
        FindPath = u'./static/bag/bag/'
        temp = self.GetFileList(FindPath)
        musicList = []
        for index in temp:
            # print index
            if index[-3:] == 'txt':
                musicList.append(index)
        self.buildIndex(writer, musicList, FindPath)
        self.searcher = ix.searcher()
        self.parser = QueryParser("content", schema=ix.schema)


    def buildIndex(self, writer, musicList, FindPath):
        for index in musicList:
            music_title = index
            music_path = FindPath + index
            # print music_path
            with open(music_path, 'r') as f:
                music_content = f.read().decode('utf-8')
            writer.add_document(
                title = music_title,
                path = music_path,
                content = music_content
            )
        writer.commit()



if __name__ == '__main__':
    ms = Search()
    with codecs.open('./songinput.txt', 'r', 'utf-8') as f:
        test = f.readlines()

    f_out = open('./out.txt', 'a')
    for index in test:
        f_out.write('Input: ')
        f_out.write(index)

        q_acc = ms.parser.parse(index)
        res_acc = ms.searcher.search(q_acc)
        if len(res_acc) > 0:
            f_out.write('Result: ')
            for res in res_acc:
                f_out.write(res['title'])
                f_out.write('\n')
            f_out.write('*'*20)
            f_out.write('\n'*2)
        else:
            cx = {}
            s = ms.analyzer(index)
            for t in s:
                q = ms.parser.parse(t.text)
                results = ms.searcher.search(q)
                for res in results:
                    if cx.has_key(res['title']):
                        cx[res['title']] += 1
                    else:
                        cx[res['title']] = 1
            cx = sorted(cx.iteritems(), key=lambda d:d[1], reverse = True)
            r = []
            for i, index in enumerate(cx):
                if i > 0:
                    if index[1] < cx[i-1][1]:
                        f_out.write('Result: ')
                        f_out.write("%s>>>出现次数: %d" % (index[0], index[1]))
                        f_out.write('\n')
                        break
                    else:
                        r.append(index)
                else:
                    r.append(index)
            if len(r) > 1:
                for index in r:
                    f_out.write('Result: ')
                    f_out.write("%s>>>出现次数: %d" % (index[0], index[1]))
                    f_out.write('\n')
            f_out.write('*'*20)
            f_out.write('\n'*2)
    f_out.close()