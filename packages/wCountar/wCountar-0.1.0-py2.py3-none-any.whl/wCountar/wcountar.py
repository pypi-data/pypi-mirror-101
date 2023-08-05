def words(sentnce):
    sentnce = str(sentnce) + str(' ')
    wordsthare = [0]
    currentword = ''
    turn = 0
    dummy = ''
    for j in sentnce:
        if j == ' ':
            if currentword != '':
                wordsthare[0] += 1
                currentword = ''
            else:
                pass
        else:
            currentword = str(currentword) + str(j)
    return wordsthare[0]
print(words('hello        bye bye'))
