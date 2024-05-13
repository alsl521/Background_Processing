def SWMMFlow(cell, efdccol, efdcrow, EFDCValue, SWMMValue):
    TotalValue = 0
    for k in range(len(efdccol)):
        count = 0
        k = 0
        if efdccol[k] < 100:
            start_j = 0
        else:
            start_j = efdccol[k] - 100
        if efdccol[k] + 100 >= len(cell[0]):
            start_j = efdccol[k] - 100 - (100 - len(cell[0]) + efdccol[k])
            end_j = len(cell[0]) - 1
        else:
            end_j = efdccol[k] + 100
        for j in range(start_j, end_j + 1):
            for i in range(len(cell)):
                if cell[i, j] == 1:
                    count += 1
        flow = SWMMValue[k] / count
        for j in range(start_j, end_j + 1):
            for i in range(len(cell)):
                if cell[i, j] == 1:
                    EFDCValue[i, j] += flow
    return EFDCValue
