import pandas as pd
import glob
import os

file_list = glob.glob("*.json")
for i in range(0, len(file_list)):
    file_list[i] = './' + file_list[i]


def read_file(path, file_number, count_files):
    result = pd.DataFrame(
        columns=['Item', 'SalePriceBeforePromo', 'SalePriceTimePromo', 'DatePriceBeforePromo', 'ObjCode',
                 'DiscountType', 'DiscountValue', 'DateBegin', 'DateEnd', 'PWCcode', 'Value', 'FirstValue',
                 'LessOrEqual', 'File'])
    json_data = pd.read_json(path)
    File = os.path.basename(path)
    if 'Information' not in json_data.keys() or \
            not isinstance(json_data['Information'], pd.Series) or \
            'QtyGoodsLists' not in json_data['Information'].keys() or \
            'GoodsLists' not in json_data['Information'].keys() or \
            'GeneralInfo' not in json_data.keys() \
            or not isinstance(json_data["GeneralInfo"], pd.Series):
        return

    QtyGoodsLists = json_data["Information"]["QtyGoodsLists"] if isinstance(json_data["Information"]["QtyGoodsLists"],
                                                                            int) else 0
    GoodsLists = json_data["Information"]["GoodsLists"] if isinstance(json_data["Information"]["GoodsLists"],
                                                                      list) else []
    if len(GoodsLists) != QtyGoodsLists:
        print('Warning: Len GoodsLists not equal QtyGoodsLists in file ' + File)
        if len(GoodsLists) < QtyGoodsLists:
            QtyGoodsLists = len(GoodsLists)
    print("Найдено списков товаров: " + str(QtyGoodsLists) + " в фаиле номер " + str(file_number) + " / " + str(
        count_files))
    GeneralInfo = json_data["GeneralInfo"]
    DateBegin = GeneralInfo["DateBegin"] if 'DateBegin' in GeneralInfo.keys() else None
    DateEnd = GeneralInfo["DateEnd"] if 'DateEnd' in GeneralInfo.keys() else None
    PWCcode = GeneralInfo["PWCcode"] if 'PWCcode' in GeneralInfo.keys() else None
    for IndexGoodsList in range(0, QtyGoodsLists):
        print("\nПроверяю список товаров номер " + str(IndexGoodsList + 1) + " / " + str(
            QtyGoodsLists) + " в фаиле номер " + str(file_number) + " / " + str(count_files))
        GoodsListItem = GoodsLists[IndexGoodsList]
        GoodsListItemIsDict = isinstance(GoodsListItem, dict)
        QtyPrices = GoodsListItem["QtyPrices"] if GoodsListItemIsDict and 'QtyPrices' in GoodsListItem.keys() else 0
        Prices = GoodsListItem["Prices"] if GoodsListItemIsDict and 'Prices' in GoodsListItem.keys() and isinstance(
            GoodsListItem["Prices"], list) else []
        DiscountType = GoodsListItem[
            "DiscountType"] if GoodsListItemIsDict and 'DiscountType' in GoodsListItem.keys() else None
        DiscountValue = GoodsListItem[
            "DiscountValue"] if GoodsListItemIsDict and 'DiscountValue' in GoodsListItem.keys() else None
        PriceOptionsList = GoodsListItem[
            "PriceOptions"] if GoodsListItemIsDict and 'PriceOptions' in GoodsListItem.keys() else None
        PriceOptions = PriceOptionsList[0] if isinstance(PriceOptionsList, list) and len(PriceOptionsList) > 0 else {}
        PriceOptionsIsDict = isinstance(PriceOptions, dict)
        LessOrEqual = PriceOptions["Operator"] if PriceOptionsIsDict and 'Operator' in PriceOptions.keys() else None
        FirstValue = PriceOptions["FirstValue"] if PriceOptionsIsDict and 'FirstValue' in PriceOptions.keys() else None
        Value = PriceOptions["Value"] if PriceOptionsIsDict and 'Value' in PriceOptions.keys() else None
        if QtyPrices != len(Prices):
            print(
                'Warning: Len Prices not equal QtyPrices in GoodsLists[' + str(IndexGoodsList) + '] in file ' +
                File
            )
            if len(Prices) < QtyPrices:
                QtyPrices = len(Prices)
        for PriceIndex in range(0, QtyPrices):
            PriceItem = Prices[PriceIndex]
            PriceItemIsDict = isinstance(Prices[PriceIndex], dict)
            QtyGoods = PriceItem["QtyGoods"] if PriceItemIsDict and 'QtyGoods' in PriceItem.keys() else 0
            Columns = PriceItem["ColumnsName"] if PriceItemIsDict and 'ColumnsName' in PriceItem.keys() and \
                                                  isinstance(PriceItem["ColumnsName"], list) else []
            ItemColumnIndex = Columns.index("Item")
            SalePriceBeforePromoColumnIndex = Columns.index("SalePriceBeforePromo")
            SalePriceTimePromoColumnIndex = Columns.index("SalePriceTimePromo")
            DatePriceBeforePromoColumnIndex = Columns.index("DatePriceBeforePromo")
            ObjCode = PriceItem["StoreCode"] if 'StoreCode' in PriceItem.keys() else None
            Data = PriceItem["Data"] if 'Data' in PriceItem.keys() and isinstance(PriceItem["Data"], list) else []
            if QtyGoods != len(Data):
                print(
                    'Warning: Len Prices not equal QtyPrices in GoodsLists[' + str(IndexGoodsList) + '][Prices][' +
                    str(PriceIndex) + '] in file ' + File
                )
                if len(Data) < QtyGoods:
                    QtyGoods = len(Data)
            ManyGoods = False
            if QtyGoods > 1000:
                print("Товаров много")
                ManyGoods = True
            for DataIndex in range(0, QtyGoods):
                if ManyGoods and DataIndex % 100 == 0:
                    print("Проверяю товар номер " + str(DataIndex + 1) + " / " + str(QtyGoods))
                DataItem = Data[DataIndex]
                Item = DataItem[ItemColumnIndex] if 0 <= ItemColumnIndex < len(DataItem) else None
                SalePriceBeforePromo = DataItem[
                    SalePriceBeforePromoColumnIndex] if 0 <= SalePriceBeforePromoColumnIndex < len(
                    DataItem) else None
                SalePriceTimePromo = DataItem[
                    SalePriceTimePromoColumnIndex] if 0 <= SalePriceTimePromoColumnIndex < len(DataItem) else None
                DatePriceBeforePromo = DataItem[
                    DatePriceBeforePromoColumnIndex] if 0 <= DatePriceBeforePromoColumnIndex < len(
                    DataItem) else None
                ResultRow = {'Item': Item,
                             'SalePriceBeforePromo': SalePriceBeforePromo,
                             'SalePriceTimePromo': SalePriceTimePromo,
                             'DatePriceBeforePromo': DatePriceBeforePromo,
                             'ObjCode': ObjCode,
                             'DiscountType': DiscountType,
                             'DiscountValue': DiscountValue,
                             'DateBegin': DateBegin,
                             'DateEnd': DateEnd,
                             'PWCcode': PWCcode,
                             'Value': Value,
                             'FirstValue': FirstValue,
                             'LessOrEqual': LessOrEqual,
                             'File': File}
                result = result.append(ResultRow, ignore_index=True)
    return result


datas = pd.DataFrame()
count_files = len(file_list)
# запись в файл
for file in file_list:
    file_number = file_list.index(file) + 1
    print("Начинаю разбор фаила " + file + " номер " + str(file_number) + " / " + str(count_files))
    datas = datas.append(read_file(file, file_number, count_files))
    print("Разбор фаила  номер " + str(file_number) + " / " + str(count_files) + " закончен! ")
datas.to_excel('./result.xlsx', index=False, na_rep='None')

# ObjCode = json_data["Information"]["GoodsLists"][0]["Prices"][0]["StoreCode"]
# DiscountType = json_data["Information"]["GoodsLists"][0]["DiscountType"]
# DiscountValue = json_data["Information"]["GoodsLists"][0]["DiscountValue"]
# Value = None
# FirstValue = None
# LessOrEqual = json_data["Information"]["GoodsLists"][0]["PriceOptions"][0]["Operator"]
# DateBegin = json_data["GeneralInfo"]["DateBegin"]
# DateEnd = json_data["GeneralInfo"]["DateEnd"]
# PWCcode = json_data["GeneralInfo"]["PWCcode"]
# File = path
