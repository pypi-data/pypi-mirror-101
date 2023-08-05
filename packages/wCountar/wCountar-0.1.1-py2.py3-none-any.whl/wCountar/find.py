def findw(sents):
    dummy = ''
    wordsta = []
    i = 0
    cw = ''
    a = i
    sents = str(sents) + str(' ')
    for l in range(int(sents.__len__() / 2)):
        wordsta += ' '
    for j in sents:
        if j == ' ' and cw != '':
            wordsta[i] = str(cw)
            cw = ''
            i += 1
        else:
            if j == ' ':
                j = ''
            cw = str(cw) + str(j)
    a = i
    for j in range(wordsta.__len__()):
        if j in range(i):
            pass
        else:
            wordsta[j] = ''
        a += 1
    return wordsta
