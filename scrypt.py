import pandas as pd
import numpy as np


def read_file(path):
    result = pd.DataFrame(columns=['Item', 'SalePriceBeforePromo', 'SalePriceTimePromo', 'DatePriceBeforePromo'])
    json_data = pd.read_json(path)
    QtyGoodsLists = json_data["Information"]["QtyGoodsLists"]
    for IndexGoodsList in range(0, QtyGoodsLists):
        GoodsListItem = json_data["Information"]["GoodsLists"][IndexGoodsList]
        QtyPrices = GoodsListItem["QtyPrices"]
        for PriceIndex in range(0, QtyPrices):
            PriceItem = GoodsListItem["Prices"][PriceIndex]
            QtyGoods = PriceItem["QtyGoods"]
            Columns = PriceItem["ColumnsName"]
            ItemColumnIndex = Columns.index("Item")
            SalePriceBeforePromoColumnIndex = Columns.index("SalePriceBeforePromo")
            SalePriceTimePromoColumnIndex = Columns.index("SalePriceTimePromo")
            DatePriceBeforePromoColumnIndex = Columns.index("DatePriceBeforePromo")
            Data = PriceItem["Data"]
            for DataIndex in range(0, QtyGoods):
                DataItem = Data[DataIndex]
                Item = DataItem[ItemColumnIndex]
                SalePriceBeforePromo = DataItem[SalePriceBeforePromoColumnIndex]
                SalePriceTimePromo = DataItem[SalePriceTimePromoColumnIndex]
                DatePriceBeforePromo = DataItem[DatePriceBeforePromoColumnIndex]
                ResultRow = {'Item': Item,
                             'SalePriceBeforePromo': SalePriceBeforePromo,
                             'SalePriceTimePromo': SalePriceTimePromo,
                             'DatePriceBeforePromo': DatePriceBeforePromo}
                result = result.append(ResultRow, ignore_index=True)
    return result

    # ObjCode = json_data["Information"]["GoodsLists"][0]["Prices"][0]["StoreCode"]
    # DiscountType = json_data["Information"]["GoodsLists"][0]["DiscountType"]
    # DiscountValue = json_data["Information"]["GoodsLists"][0]["DiscountValue"]
    # DateBegin = json_data["GeneralInfo"]["DateBegin"]
    # DateEnd = json_data["GeneralInfo"]["DateEnd"]
    # PWCcode = json_data["GeneralInfo"]["PWCcode"]
    # Value = None
    # FirstValue = None
    # LessOrEqual = json_data["Information"]["GoodsLists"][0]["PriceOptions"][0]["Operator"]
    # File = path


datas = read_file('./export_20210913-1649_435_7429.json')
