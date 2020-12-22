import read_data as rd
import linear_regression as lr
import os


if __name__ == '__main__':
    fileNames = os.listdir('./data')
    # filenames = ['20201111_AUT_EB#3_10K_OTA_Loopback_V3.xlsx']

    rfData = rd.dataTreatment(fileNames).dataRead()
    print(rfData)

    