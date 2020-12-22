import pandas as pd

class dataTreatment(object):
    """
    Test Data를 Tensorflow에 적용하기 위해 Treat하는 Class
    """

    def __init__(self, filenames):
        """
        dataTreatment Class 생성자
        """
        self.filenames = filenames

    def dataRead(self):
        """
        Make the dataframe into dictionary using excel file.
        """
        data = dict()

        # dataframe restore용 Dictionary setting
        for filename in self.filenames:
            # xl = pd.ExcelFile('./data/'+filename)
            xl = pd.ExcelFile(filename)
            for name in xl.sheet_names:
                if name in data.keys():
                    pass
                else:
                    data[name] = pd.DataFrame()

        # dataframe restore in dictionary
        for filename in self.filenames:
            xl = pd.ExcelFile(filename)
            for name in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=name, header=0)
                data[name] = data[name].append(df)

        # NaN 제거 및 reindexing 진행
        for name in data.keys():
            data[name] = data[name].dropna(axis=0)
            data[name] = data[name].reset_index(drop=True)

        return data

