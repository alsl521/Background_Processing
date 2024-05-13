import math
import os


def CellFileWrite(cell, backpath, runingpath):
    CellFile = open(backpath + "\\cell1.inp", "r+")
    CellFileLists = CellFile.readlines()
    CellFile.close()
    CellFile1 = open(runingpath + "\\cell.inp", "w+")
    CellFile2 = open(runingpath + "\\cell2.inp", "w+")
    for i in range(4):
        if CellFileLists[i].find('\n') == -1:
            CellFileLists[i] = CellFileLists[i] + "\n"
        CellFile1.write(CellFileLists[i])
        CellFile2.write(CellFileLists[i])
    for i in range(len(cell)):
        CellFile2.write("{0:<4}".format(len(cell) - i))
        CellFile2.write(" ")
        for j in range(len(cell[i])):
            CellFile2.write(str(int(cell[i, j])))
        CellFile2.write("\n")
    CellFile2.close()
    if len(cell[0]) <= 640:
        for i in range(len(cell)):
            CellFile1.write("{0:<4}".format(len(cell) - i))
            CellFile1.write(" ")
            for j in range(len(cell[i])):
                CellFile1.write(str(int(cell[i, j])))
            CellFile1.write("\n")
        CellFile1.close()
    else:
        for k in range(int(len(cell[0]) / 640) + 1):
            for i in range(len(cell)):
                CellFile1.write("{0:<4}".format(len(cell) - i))
                CellFile1.write(" ")
                max_temp = (k + 1) * 640
                if max_temp > len(cell[0]):
                    max_temp = len(cell[0])
                for j in range(k * 640, max_temp):
                    CellFile1.write(str(int(cell[i, j])))
                CellFile1.write("\n")
    CellFile1.close()
    CellFile2.close()


def ShowFileWrite(cell, backpath, runingpath):
    i = int(len(cell) / 2)
    j = int(len(cell[0]) / 2)
    flag = True
    count = 1
    while flag and cell[i, j] != 1:
        i_top = i - 1
        while flag and i_top >= 0:
            if cell[i_top, j] == 1:
                i = i_top
                flag = False
                break
            i_top -= 1
        i_bot = i + 1
        while flag and i_bot < len(cell[0]):
            if cell[i_bot, j] == 1:
                i = i_bot
                flag = False
                break
            i_bot += 1
        if flag:
            if count > 0:
                j += count
                count = -count
            else:
                j += 2 * count
                count = -count
                count += 1
    print("show.inp     " + str(cell[i, j]))
    ShowFile = open(backpath + "\\show1.inp", "r+")
    ShowFileLists = ShowFile.readlines()
    ShowFile.close()
    ShowFile = open(runingpath + "\\show.inp", "w+")
    for k in range(6):
        if ShowFileLists[k].find('\n') == -1:
            ShowFileLists[k] = ShowFileLists[k] + "\n"
        ShowFile.write(ShowFileLists[k])
    print("show.inp     " + str(cell[i, j]))
    ShowFile.write("         3     20000        " + str(j + 1) + "       " + str(len(cell) - i) + "      5000\n")
    ShowFile.write("  100.000  1000.000  500.000\n")
    ShowFile.close()


def LxlyFileWrite(cell, efdccollon, efdcrowlon, Originx, Originy, backpath, runingpath):
    LxlyFile = open(backpath + "\\lxly1.inp", "r+")
    LxlyFileLists = LxlyFile.readlines()
    LxlyFile.close()
    LxlyFile = open(runingpath + "\\lxly.inp", "w+")
    for i in range(4):
        if LxlyFileLists[i].find('\n') == -1:
            LxlyFileLists[i] = LxlyFileLists[i] + "\n"
        LxlyFile.write(LxlyFileLists[i])
    for i in range(len(cell)):
        for j in range(len(cell[0])):
            if cell[i, j] != 0:
                x = Originx + j * efdcrowlon + efdcrowlon / 2
                y = Originy + (len(cell) - i - 1) * efdccollon + efdccollon / 2
                LxlyFile.write(str(j + 1) + "      " + str(len(cell) - i) + "     " + str(x) + "       " + str(
                    y) + "         1.000          0.000          0.000          1.000          1.000\n")
    LxlyFile.close()


def DecompFileWrite(cell, backpath, runingpath):
    DecompFile = open(backpath + "\\decomp1.jnp", "r+")
    DecompFileLists = DecompFile.readlines()
    DecompFile.close()
    j = 0
    flag = False
    while j < len(DecompFileLists[4]):
        while j < len(DecompFileLists[4]) and DecompFileLists[4][j] >= '0' and DecompFileLists[4][j] <= '9':
            line = DecompFileLists[4][:j]
            DecompFileLists[4] = line + str(len(cell[0])) + "],"
            flag = True
            break
        if flag:
            break
        j += 1
    flag = False
    j = 0
    while j < len(DecompFileLists[5]):
        while j < len(DecompFileLists[5]) and DecompFileLists[5][j] >= '0' and DecompFileLists[5][j] <= '9':
            line = DecompFileLists[5][:j]
            DecompFileLists[5] = line + str(len(cell)) + "],"
            flag = True
            break
        if flag:
            break
        j += 1
    DecompFile = open(runingpath + "\\decomp.jnp", "w+")
    for i in range(len(DecompFileLists)):
        if DecompFileLists[i].find('\n') == -1:
            DecompFileLists[i] = DecompFileLists[i] + "\n"
        DecompFile.write(DecompFileLists[i])
    DecompFile.close()


def DxdyFileWrite(cell, WaterLevel_cell, Underwatertopography_cell, efdccollon, efdcrowlon, backpath, runingpath):
    DxdyFile = open(backpath + "\\dxdy1.inp", "r+")
    DxdyFileLists = DxdyFile.readlines()
    DxdyFile.close()
    DxdyFile = open(runingpath + "\\dxdy.inp", "w+")
    for i in range(4):
        if DxdyFileLists[i].find('\n') == -1:
            DxdyFileLists[i] = DxdyFileLists[i] + "\n"
        DxdyFile.write(DxdyFileLists[i])
    for i in range(len(cell)):
        for j in range(len(cell[i])):
            if cell[i, j] != 0:
                DxdyFile.write(str(j + 1) + "      " + str(len(cell) - i) + "     " + str(efdcrowlon) + "     " + str(
                    efdccollon) + "      " + str(
                    WaterLevel_cell[i, j] - Underwatertopography_cell[i, j]) + "      " + str(
                    Underwatertopography_cell[i, j]) + "      0.010\n")
    DxdyFile.close()
