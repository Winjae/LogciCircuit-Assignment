import copy


def rowDominance(table):
    for i in range(len(table) - 1):
        for k in range(i + 1, len(table)):
            pd = []
            dd = []
            for j in range(1, len(table[i])):
                if table[i][j] == 1:
                    pd.append(j)
                if table[k][j] == 1:
                    dd.append(j)
            if len(pd) == 0:
                break
            elif len(dd) == 0:
                continue
            elif sorted(list(set(pd + dd))) == dd:  # dd가 pd를 지배할 때
                for j in range(1, len(table[i])):
                    table[i][j] = 0
                break
            elif sorted(list(set(pd + dd))) == pd:  # pd가 dd를 지배할 때
                for j in range(1, len(table[i])):
                    table[k][j] = 0
    return table


def columnDominance(table):
    for i in range(1, len(table[0]) - 1):
        for k in range(i + 1, len(table[0])):
            pd = []
            dd = []
            for j in range(len(table)):
                if table[j][i] == 1:
                    pd.append(j)  # table[j][i] 가 pd
                if table[j][k] == 1:
                    dd.append(j)  # table[j][k] 가 dd
            if len(pd) == 0:
                break
            elif len(dd) == 0:
                continue
            elif sorted(list(set(pd + dd))) == dd:  # dd가 pd를 지배할 때
                for j in range(len(table)):  # dd를 다 지운다
                    table[j][k] = 0
                break
            elif sorted(list(set(pd + dd))) == pd:  # pd가 dd를 지배할 때
                for j in range(len(table)):  # pd를 다 지운다
                    table[j][i] = 0

    return table


def minimumCover(PItable):
    NEPI = []
    BeforeTable = copy.deepcopy(PItable)
    AfterTable = copy.deepcopy(BeforeTable)
    while not isEmpty(BeforeTable):
        for j in range(1, len(BeforeTable[0])):  # EPI 찾기
            checkEPI = [0]
            epi = []
            for i in range(len(BeforeTable)):
                if BeforeTable[i][j] == 1:
                    checkEPI[0] += 1
                    checkEPI.append(BeforeTable[i][0])
                    epi = BeforeTable[i].copy()
            if checkEPI[0] == 1 and (checkEPI[1] not in NEPI):
                NEPI.append(checkEPI[1])
                print(checkEPI[1])
                for i in range(1, len(BeforeTable[0])):
                    for k in range(len(BeforeTable)):
                        if epi[i] == 1:
                            AfterTable[k][i] = 0

        AfterTable = columnDominance(AfterTable)  # Column Dominance 진행
        AfterTable = rowDominance(AfterTable)  # Row Dominance 진행

        print("Before Table")
        for l in BeforeTable:
            print(l)
        print("After Table")
        for l in AfterTable:
            print(l)



        if BeforeTable == AfterTable:
            NEPI.append("Petrick's Method")
            break

        BeforeTable = copy.deepcopy(AfterTable)  # 차이가 있으면 Before에다가 After를 복사

    for i in range(len(NEPI)):
        NEPI[i] = NEPI[i].replace("2","-")
    return NEPI


def isEmpty(table):
    for list in table:
        for data in list[1:]:
            if data != 0:
                return False
    return True


def findEPI(minterm):
    result = []
    size = minterm[0]
    temp = []
    for p in minterm[2:]:
        temp.append(("{0:0" + str(size) + "b}").format(p))
    answer = findPI(temp)
    answer = sorted(answer)

    EPITable = []
    for i in range(len(answer)):
        EPITable.append([answer[i]])
        n = answer[i].count("2")
        for num in range(len(minterm[2:])):
            count = pow(2, n) - 1
            included = 0
            while (count >= 0):
                compA = ("{0:0" + str(n) + "b}").format(count)
                k = len(compA) - 1
                compB = answer[i]
                for j in range(len(compB), 0, -1):
                    if compB[j - 1] == "2":
                        compB = compB[:j - 1] + compA[k] + compB[j:]
                        k -= 1
                bin_num = ("{0:0" + str(size) + "b}").format(minterm[2 + num])
                if compB == bin_num:
                    included = 1
                count -= 1
            EPITable[i].append(included)
    answer.append("EPI")
    for j in range(1, len(EPITable[0])):
        checkEPI = [0]
        for i in range(len(EPITable)):
            if EPITable[i][j] == 1:
                checkEPI[0] += 1
                checkEPI.append(EPITable[i][0])
        if checkEPI[0] == 1 and (checkEPI[1] not in result):
            result.append(checkEPI[1])

    result = sorted(result)
    result = answer + result

    for i in range(len(result)):
        result[i] = result[i].replace("2", "-")
    return result, EPITable


def findPI(bin_minterm):
    count = max = 0
    result = []

    for binNum in bin_minterm:
        for i in range(len(binNum)):
            if binNum[i] == '1':
                count += 1
        if max < count:
            max = count

    table = []
    com = []
    for i in range(max + 1):
        table.append([])
        com.append([])

    for p in bin_minterm:
        num = 0
        for i in range(len(p)):
            if p[i] == '1':
                num += 1
        table[num].append(p)
        com[num].append(0)

    next_binary = []
    for a in range(len(table) - 1):
        for i in range(len(table[a])):
            for j in range(len(table[a + 1])):
                twin = compare(table[a][i], table[a + 1][j])
                if twin[0] == 1:
                    com[a][i] = 1
                    com[a + 1][j] = 1
                    if twin[1] not in next_binary:
                        next_binary.append(twin[1])

    for i in range(len(com)):
        for j in range(len(com[i])):
            if com[i][j] == 0:
                result.append(table[i][j])
    if len(next_binary) > 0:
        result += findPI(next_binary)
    return result


def compare(a, b):
    count = 0
    pis = ""
    result = []
    for i in range(len(a)):
        if a[i] != b[i]:
            count += 1
            pis += "2"
        else:
            pis += a[i]
    result.append(count)
    result.append(pis)

    return result


def solution(minterm):
    answer, PItable = findEPI(minterm)

    list = minimumCover(PItable)

    print(list)
    return answer


a = [4, 13, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
print(solution(a))
