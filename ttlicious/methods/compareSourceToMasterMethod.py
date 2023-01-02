from .. import classes


def compareSourceToMaster(XLSSource: classes.XLSSource, XLSMaster: classes.XLSMaster, settings: classes.XMLSettings) -> classes.XLSUpdate:
    """
    Return XLScompare after comparing sheets in source with the master
    """

    # Get the return variable
    XLSCompare = XLSSource
    XLSCompare.convertClass(classes.XLSCompare)

    sheetList = XLSSource.getSheetList()
    for sheetName in sheetList:

        # Get the sheets manually
        source = XLSSource.getSheet(sheetName)
        master = XLSMaster.getSheet(sheetName)

        # Display to screen
        print("Compare Sheet: {}".format(source.name))

        # Get list of columns that match the compare from settings
        compareList = list()
        settingsCompareList = settings.getItemListFromName(sheetName, "compare")
        tempList = source.dataColumnsToList()
        for i, listValue in enumerate(tempList):
            listValueOriginal = source.columnMap.convertToOriginal(listValue)
            if listValueOriginal[0] in settingsCompareList:
                compareList.append(listValue)

        for SP, sourceLine in source.data.iterrows():
            # Get the search terms
            searchTerm = source.data.at[SP, 'searchIndex']

            # get the pointer to the master
            MP = master.data.index[master.data['searchIndex'] == searchTerm].values

            if len(MP) > 1:
                # check for duplicates in master
                raise Exception("Write code here")
            elif len(MP) == 0:
                # check for data which is not in master
                source.data.at[SP, 'status'] = 'new'
                print("  {} New Line   : {}".format(SP, searchTerm))
                XLSCompare.modificationFound = True
                continue
            else:
                MP = int(MP)

            for compareColumn in compareList:
                tempSource = str(source.data.at[SP, compareColumn])
                tempMaster = str(master.data.at[MP, compareColumn])
                if tempSource != tempMaster:
                    source.data.at[SP, 'status'] = 'change'
                    print("  {} Line Change: {} {}".format(
                        SP, searchTerm, compareColumn))
                    rowToInsert = master.data.loc[MP]
                    source.data.loc[SP+0.5] = rowToInsert
                    XLSCompare.modificationFound = True

        # Reorder the index
        source.data = source.data.sort_index().reset_index(drop=True)

        # Add changed source data to XLSreturn
        XLSCompare.setSheet(sheetName, source)

    return XLSCompare
