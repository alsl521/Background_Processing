import numpy as np


def EFDCFileWrite(paramter, cell, RiverValue, ModflowCol, ModflowRow, EFDCCol, EFDCRow, EFDCBoundaryValue, Verlay,
                  IsActivite,
                  IsHumid, Isboundary, TimeEvery, TimeStep, CurrentTime, backpath, runingpath):
    ModflowToEFDC = 0
    EFDCToModflow = 0
    EFDCFile = open(backpath + "\\efdc1.inp", "r+", encoding="ISO-8859-1")
    EFDCFileLists = EFDCFile.readlines()
    EFDCFile.close()
    i = 0
    FlowCount = 0
    EFDCCount = np.zeros((len(cell), len(cell[0])))
    EFDCValue = np.zeros((len(cell), len(cell[0])))
    while i < len(EFDCFileLists):
        if str(EFDCFileLists[i]).find(
                "C2  ISRESTI ISRESTO ISRESTR ISGREGOR  ISLOG ISDIVEX  ISNEGH   ISMMC   ISBAL ICONTINUE ISHOW") != -1:
            if CurrentTime == 1:
                i += 1
                EFDCFileLists[
                    i] = "          0       1       1       1       0       0       0       0       1       0       1\n"
            else:
                i += 1
                EFDCFileLists[
                    i] = "          1       1       1       1       0       0       0       0       1       0       1\n"
        elif str(EFDCFileLists[i]).find(
                "C7      NTC  NTSPTC    NLTC    NTTC   NTCPP  NTSTBC   NTCNB   NTCVB  NTSMMT  NFLTMT NDRYSTPP NRAMPUP NUPSTEP") != -1:
            i += 1
            EFDCFileLists[i] = "         1   " + str(
                int(TimeEvery / TimeStep)) + "      0       0       1       4       0       0        " + str(
                int(TimeEvery / TimeStep)) + "       1      20    1000       2\n"
        elif str(EFDCFileLists[i]).find(
                "C8       TCON    TBEGIN      TREF    CORIOLIS  ISCORV   ISCCA   ISCFL  ISCFLM   DTSSFAC  DTSSDHDT     DTMAX") != -1:
            i += 1
            EFDCFileLists[i] = "        86400       " + str(CurrentTime - 1) + "     " + str(
                TimeEvery) + "   6.842E-05       0       0       0       0         0       0.3      3600\n"
        elif str(EFDCFileLists[i]).find(
                "C9       IC      JC      LC     LVC    ISCO     NDM     LDM  ISMASK NBLCKED CONNECT  NSHMAX  NSBMAX    WSMH    WSMB") != -1:
            i += 1
            EFDCFileLists[i] = str(len(cell[0])) + "   " + str(len(cell)) + "   " + str(IsActivite + 2) + "     " + str(
                IsActivite) + "       1       1    " + str(
                IsActivite) + "       0       0       0       0       0       0       0\n"
        elif str(EFDCFileLists[i]).find("C9A  KC  KSIG  ISETGVC  SELVREF  BELVREF  ISGVCCK") != -1:
            i += 1
            EFDCFileLists[i] = str(Verlay) + "     1        1        0       -1        0\n"
        elif str(EFDCFileLists[i]).find("C10  K   DZC") != -1:
            for varlay in range(Verlay):
                i += 1
                if varlay == Verlay - 1:
                    EFDCFileLists.insert(i, str(Verlay) + "     " + str(1 - round(((Verlay - 1) / Verlay), 3)) + "\n")
                else:
                    EFDCFileLists.insert(i, str(varlay + 1) + "      " + str(round(1 / Verlay, 3)) + "\n")
            i += 1
            while EFDCFileLists[i].find("-----------------") == -1:
                EFDCFileLists.pop(i)
        # 水位边界部分
        elif str(EFDCFileLists[i]).find("C16    NPBS    NPBW    NPBE    NPBN   NPFOR  NPFORT   NPSER PDGINIT") != -1:
            i += 1
            if Isboundary == 2:
                EFDCFileLists[i] = " 0       50       50      0       0       0       0       0\n"
            else:
                EFDCFileLists[i] = " 0       0       0      0       0       0       0       0\n"
        # ...
        # 流量边界部分
        elif str(EFDCFileLists[i]).find(
                "C23   NQSIJ  NQJPIJ   NQSER   NQCTL  NQCTLT  NHYDST    NQWR  NQWRSR   ISDIQ NQCTLSER  NQCTRULES") != -1:
            i += 1
            for k in range(len(EFDCRow)):
                if cell[EFDCRow[k] - 1, EFDCCol[k] - 1] == 1:
                    EFDCCount[EFDCRow[k] - 1, EFDCCol[k] - 1] += 1
            for k in range(len(EFDCRow)):
                if cell[EFDCRow[k] - 1, EFDCCol[k] - 1] == 1:
                    EFDCValue[EFDCRow[k] - 1, EFDCCol[k] - 1] = RiverValue[ModflowRow[k] - 1, ModflowCol[k] - 1] / \
                                                                EFDCCount[EFDCRow[k] - 1, EFDCCol[k] - 1]

                    # 水均衡Modflow与EFDC的模型
                    if RiverValue[ModflowRow[k] - 1, ModflowCol[k] - 1] / EFDCCount[EFDCRow[k] - 1, EFDCCol[k] - 1] > 0:
                        ModflowToEFDC += RiverValue[ModflowRow[k] - 1, ModflowCol[k] - 1] / EFDCCount[
                            EFDCRow[k] - 1, EFDCCol[k] - 1]
                    else:
                        EFDCToModflow += RiverValue[ModflowRow[k] - 1, ModflowCol[k] - 1] / EFDCCount[
                            EFDCRow[k] - 1, EFDCCol[k] - 1]

            for row in range(len(EFDCBoundaryValue)):
                for col in range(len(EFDCBoundaryValue[0])):
                    EFDCValue[row, col] += EFDCBoundaryValue[row, col]
            for m in range(len(EFDCValue)):
                for n in range(len(EFDCValue[0])):
                    if EFDCValue[m, n] != 0:
                        FlowCount += 1
            EFDCFileLists[i] = str(
                FlowCount) + "      0       0       0       0       0       0       0       0       0       0\n"
        elif str(EFDCFileLists[i]).find(
                "C24     IQS     JQS        QSSE  NQSMUL   NQSMF  IQSERQ  ICSER1  ICSER2  ICSER3  ICSER4  ICSER5  ICSER6  ICSER7   QWIDTH    QSFACTOR    GRPID ! ID") != -1:
            i += 1
            # 水均衡文件部分没写
            for k in range(FlowCount):
                EFDCFileLists.insert(i, str(EFDCCol[k]) + "    " + str(len(cell) - EFDCRow[k] + 1) + "      " + str(
                    round(EFDCValue[EFDCRow[k] - 1, EFDCCol[k] - 1],
                          3)) + "        0       0       0       0       0       0       0       0       0       0   0.0000 1.000000E+0        1\n")
                i += 1
            while str(EFDCFileLists[i]).find("-------") == -1:
                EFDCFileLists.pop(i)
        elif str(EFDCFileLists[i]).find("C25       SAL       TEM      DYE1       SFL      GRPID ! ID") != -1:
            i += 1
            for k in range(IsActivite):
                EFDCFileLists.insert(i, "            0         0         0         0          1\n")
                i += 1
            while str(EFDCFileLists[i]).find("------------------") == -1:
                EFDCFileLists.pop(i)
        elif str(EFDCFileLists[i]).find("C26      GRPID ! ID (0 SEDS + 0 SNDS)") != -1:
            i += 1
            for k in range(IsActivite):
                EFDCFileLists.insert(i, "             1\n")
                i += 1
            while str(EFDCFileLists[i]).find("-----------------") == -1:
                EFDCFileLists.pop(i)
        elif str(EFDCFileLists[i]).find("C12") != -1 and str(EFDCFileLists[i]).find("AHO") != -1 and str(
                EFDCFileLists[i]).find("AHD") != -1:
            i += 1
            EFDCFileLists[i] = " " + str(paramter[0]) + " " + str(paramter[1]) + " " + str(
                paramter[2]) + " 1E-06 " + str(paramter[3]) + " " + str(paramter[4]) + " 0.0001 1 " + str(paramter[5])
            i += 1
            while str(EFDCFileLists[i]).find("------------") == -1:
                EFDCFileLists.pop(i)
        # 水位边界C53-C59
        i += 1

    EFDCFile = open(runingpath + "\\efdc.inp", "w+", encoding="utf-8")
    for i in range(len(EFDCFileLists)):
        if EFDCFileLists[i].find('\n') == -1:
            EFDCFileLists[i] = EFDCFileLists[i] + "\n"
        EFDCFile.write(EFDCFileLists[i])
    EFDCFile.close()
    return ModflowToEFDC, EFDCToModflow,
