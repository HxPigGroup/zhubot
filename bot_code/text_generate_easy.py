import re
import random
import jieba
import jieba.analyse as analyse
import emoji
import pickle

class Dialog:
    def __init__(self):
        self.lines = []
        self.max_length = 100
        self.min_length = 30
        self.wordict = {}
        self.wordict_re = {}
        self.wordict_two = {}
        self.nums = 0
    
    def load(self, filename):
        if filename.endswith(".txt") == True:
            self.load_txt(filename)
            self.get_generator()
            self.get_generator_re()
            self.get_generator_two()
        else:
            self.wordict = pickle.load(open(filename, 'rb'))
            self.wordict_re = pickle.load(open(filename + '_re', 'rb'))
            self.wordict_two = pickle.load(open(filename + '_two', 'rb'))
            
    def load_txt(self, filename):
        file = open(filename, 'r', encoding='UTF-8')
        for i in file.readlines():
            if i[0] == '\n':
                continue
            if len(i) >= 17 and i[4] == '-' and i[7] == '-' and i[10] == ' ' and \
             ((i[13] == ':' and i[16] == ':') or (i[12] == ':' and i[15] == ':')):
                continue
            if i[-1] != '\n':
                self.lines.append(i + "。")
            else:
                self.lines.append(i)
    
    def save_data(self):
        pickle.dump(self.wordict, open('./save/dict', 'wb'))
        pickle.dump(self.wordict_re, open('./save/dict_re', 'wb'))
        pickle.dump(self.wordict_two, open('./save/dict_two', 'wb'))
    #def special_token(self)
    def wordLen(self, dictsub):
        sum = 0
        for key, value in dictsub.items():
            sum += value
        return sum

    def retriveRandomWord(self, dictsub):
        randindex = random.randint(1, self.wordLen(dictsub))
        for key, value in dictsub.items():
            randindex -= value
            if randindex <= 0:
                return key
        return "，"
    
    def get_generator_two(self):
        text = "".join(self.lines)
        text = text.replace('\n', '。')
        text = text.replace('[图片]', '')
        text = text.replace('[表情]', '')
        text = text.replace('[表情弹射]', '')
        text = text.replace('[QQ红包]', 'QQ红包')
        text = text.replace(' ', '，')
        text = text.replace('}', '')
        text = text.replace('{', '')
        words = [word for word in text if word != '']
        wordict = {}
        for i in range(2, len(text)):
            preTwo = words[i-2] + words[i-1]
            if preTwo not in wordict:
                wordict[preTwo] = {}
            if words[i] not in wordict[preTwo]:
                wordict[preTwo][words[i]] = 0
            wordict[preTwo][words[i]] += 1
        
        self.wordict_two = wordict
        return wordict

    def get_generator_re(self):
        text = "".join(self.lines)
        text = text.replace('\n', '。')
        text = text.replace('[图片]', '')
        text = text.replace('[表情]', '')
        text = text.replace('[表情弹射]', '')
        text = text.replace('[QQ红包]', 'QQ红包')
        text = text.replace(' ', '，')
        text = text.replace('}', '')
        text = text.replace('{', '')
        words = [word for word in text if word != '']
        words = words[::-1]
        wordict = {}
        for i in range(1, len(text)):
            if words[i-1] not in wordict:
                wordict[words[i-1]] = {}
            if words[i] not in wordict[words[i-1]]:
                wordict[words[i-1]][words[i]] = 0
            wordict[words[i-1]][words[i]] += 1
        
        self.wordict_re = wordict
        return wordict

    def get_generator(self):
        text = "".join(self.lines)
        text = text.replace('\n', '。')
        text = text.replace('[图片]', '')
        text = text.replace('[表情]', '')
        text = text.replace('[表情弹射]', '')
        text = text.replace('[QQ红包]', 'QQ红包')
        text = text.replace(' ', '，')
        text = text.replace('}', '')
        text = text.replace('{', '')
        #punc = ['，', '。', '？', '；', ':', '!']
        #for symbol in punc:
        #    text = text.replace(symbol, ' '+symbol+' ')
        words = [word for word in text if word != '']
        wordict = {}
        for i in range(1, len(text)):
            if words[i-1] not in wordict:
                wordict[words[i-1]] = {}
            if words[i] not in wordict[words[i-1]]:
                wordict[words[i-1]][words[i]] = 0
            wordict[words[i-1]][words[i]] += 1
        
        self.wordict = wordict
        return wordict
    
    def add_new_line(self, text):
        text = text.replace('\n', '。')
        text = text.replace('[图片]', '')
        text = text.replace(' ', '，')
        text = text.replace('}', '')
        text = text.replace('{', '')
        text = "。"+text
        if text[-1] != '。':
            text = text + "。"
        words = [word for word in text if word != '']
        print(text)
        for i in range(1, len(text)):
            if words[i-1] not in self.wordict:
                self.wordict[words[i-1]] = {}
            if words[i] not in self.wordict[words[i-1]]:
                self.wordict[words[i-1]][words[i]] = 0
            self.wordict[words[i-1]][words[i]] += 1
        
        for i in range(2, len(text)):
            preTwo = words[i-2] + words[i-1]
            if preTwo not in self.wordict_two:
                self.wordict_two[preTwo] = {}
            if words[i] not in self.wordict_two[preTwo]:
                self.wordict_two[preTwo][words[i]] = 0
            self.wordict_two[preTwo][words[i]] += 1

        words = words[::-1]
        for i in range(1, len(text)):
            if words[i-1] not in self.wordict_re:
                self.wordict_re[words[i-1]] = {}
            if words[i] not in self.wordict_re[words[i-1]]:
                self.wordict_re[words[i-1]][words[i]] = 0
            self.wordict_re[words[i-1]][words[i]] += 1
        
        
    def hou_one(self, currentword, chain, sens, nowi, i):
        if currentword not in self.wordict:
            chain += currentword
            if nowi < len(sens) - 1:
                nowi += 1
                currentword = sens[nowi][-1]
                chain += sens[nowi]
                senti = chain
            elif i > self.min_length:
                chain += '。'
                return "Finish", chain, nowi
        currentword = self.retriveRandomWord(self.wordict[currentword])
        if currentword == '。':
            if nowi < len(sens) - 1:
                chain += '，'
                nowi += 1
                currentword = sens[nowi][-1]
                chain += sens[nowi]
                senti = chain
            elif i > self.min_length:
                chain += '。'
                return "Finish", chain, nowi
        else:
            chain += currentword
            chain = chain.replace(' ', '')
        return currentword, chain, nowi
    
    def hou_two(self, currentword, chain, sens, nowi, i):
        if currentword not in self.wordict_two:
            chain += currentword[-1]
            if nowi < len(sens) - 1:
                nowi += 1
                if len(sens[nowi]) > 1:
                    currentword = sens[nowi][-2:]
                else:
                    currentword = sens[nowi][-1]
                chain += sens[nowi]
                senti = chain
            elif i > self.min_length:
                chain += '。'
                return "Finish", chain, nowi
        else:
            currentword = currentword[-1] + self.retriveRandomWord(self.wordict_two[currentword])
            if currentword[-1] == '。':
                if nowi < len(sens) - 1:
                    chain += '，'
                    nowi += 1
                    if len(sens[nowi]) > 1:
                        currentword = sens[nowi][-2:]
                    else:
                        currentword = sens[nowi][-1]
                    chain += sens[nowi]
                elif i > self.min_length:
                    chain += '。'
                    return "Finish", chain, nowi
            else:
                chain += currentword[-1]
                chain = chain.replace(' ', '')
        return currentword, chain, nowi
    def cheng(self, sentence):
        sens = jieba.lcut(sentence)
        nowi = 0
        currentword = sens[nowi][-1]
        chain = sens[nowi]
        senti = chain
        print(sens)
        #tou
        preword = sens[nowi][0]
        while True:
            if preword not in self.wordict_re:
                print(preword)
                break
            preword = self.retriveRandomWord(self.wordict_re[preword])
            if preword == '。':
                break
            else:
                chain = preword + chain
                chain = chain.replace(' ', '')
        if len(sens[nowi]) > 1:
            currentword = sens[nowi][-2:]
        else:
            currentword = sens[nowi][-1]
        for i in range(0, self.max_length):
            if len(currentword) > 1:
                currentword, chain, nowi = self.hou_two(currentword, chain, sens, nowi, i)
            else:
                currentword, chain, nowi = self.hou_one(currentword, chain, sens, nowi, i)
            if currentword == "Finish":
                break
        """for i in range(0, self.max_length):
            if currentword not in self.wordict:
                chain += currentword
                if nowi < len(sens) - 1:
                    nowi += 1
                    currentword = sens[nowi][-1]
                    chain += sens[nowi]
                    senti = chain
                elif i > self.min_length:
                    chain += '。'
                    break
            currentword = self.retriveRandomWord(self.wordict[currentword])
            if currentword == '。':
                if nowi < len(sens) - 1:

                    chain += '，'
                    nowi += 1
                    currentword = sens[nowi][-1]
                    chain += sens[nowi]
                    senti = chain
                elif i > self.min_length:
                    chain += '。'
                    break
            else:
                chain += currentword
                senti += currentword
                chain = chain.replace(' ', '')
"""
        print(chain)
        return chain


if __name__ == '__main__':
    D = Dialog()
    D.load(r'./data/猪群.txt')
    #D.get_generator()
    #D.zhuhua('猪哥爱大爷')

    D.cheng('猪')
            