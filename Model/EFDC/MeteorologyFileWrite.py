def WindFileWrite(windspeed, TimeEvery, StationHeight, winddirection, backpath, runingpath):
    WserFile = open(backpath + "\\wser1.inp", "r+")
    WserFileLists = WserFile.readlines()
    WserFile.close()
    WserFile = open(runingpath + "\\wser.inp", "w+")
    for i in range(19):
        if WserFileLists[i].find('\n') == -1:
            WserFileLists[i] = WserFileLists[i] + "\n"
        WserFile.write(WserFileLists[i])
    WserFile.write(str(len(windspeed)) + "       " + str(TimeEvery) + "     0         1         0     " + str(
        StationHeight) + "     ! WIND\n")
    for i in range(len(windspeed)):
        WserFile.write(str(i + 1) + "       " + str(windspeed[i]) + "          " + str(winddirection[i]) + "\n")
    WserFile.close()


def TserFileWrite(WaterTemperature, TimeEvery, VerLay, backpath, runingpath):
    TserFile = open(backpath + "\\tser1.inp", "r+")
    TserFileLists = TserFile.readlines()
    TserFile.close()
    TserFile = open(runingpath + "\\tser.inp", "w+")
    for i in range(19):
        if TserFileLists[i].find('\n') == -1:
            TserFileLists[i] = TserFileLists[i] + "\n"
        TserFile.write(TserFileLists[i])
    TserFile.write("1        " + str(10 * len(WaterTemperature)) + "       " + str(
        TimeEvery) + "    0.0000    1.0000    0.0000 ! Temp Inflow\n")
    for i in range(VerLay):
        if i == VerLay - 1:
            TserFile.write("          " + str(1 - (1 / VerLay) * (VerLay - 1)) + "\n")
        else:
            TserFile.write("          " + str(1 / VerLay))
    for i in range(len(WaterTemperature)):
        for j in range(1, 10):
            TserFile.write(str(i + j * 0.1))
            TserFile.write("     ")
            TserFile.write(str(WaterTemperature[i]))
            TserFile.write("\n")
        TserFile.write(str(i + 1))
        TserFile.write("     ")
        TserFile.write(str(WaterTemperature[i]))
        TserFile.write("\n")
    TserFile.close()


def AserFileWrite(TimeEvery, Atmosphere, Rain, Eva, Solar, Cloud, backpath, runingpath):
    AserFile = open(backpath + "\\aser1.inp", "r+")
    AserFileLists = AserFile.readlines()
    AserFile.close()
    AserFile = open(runingpath + "\\aser.inp", "w+")
    for i in range(27):
        if AserFileLists[i].find('\n') == -1:
            AserFileLists[i] = AserFileLists[i] + "\n"
        AserFile.write(AserFileLists[i])
    AserFile.write(str(len(Atmosphere)) + "      " + str(
        TimeEvery) + "     0.000         1    1.15740e-5      1.15741e-5     1.000     1.000 ! SERIES 0\n")
    for i in range(len(Atmosphere)):
        AserFile.write(str(i + 1) + "       " + str(Atmosphere[i]) + "      9.400      0.930      " + str(
            Rain[i]) + "      " + str(Eva[i]) + "      " + str(Solar[i]) + "      " + str(Cloud[i]) + "\n")
    AserFile.close()
