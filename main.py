import pandas
import time
import os
#各料件耗損狀況
UnCostKeyWords=["更改","重","重裝","重新","清潔","重焊","修正"]
ConsumablesCostKeyWords=["更換"]
#異常狀況描述
ErrorConditionKeyWords=["異音","接觸不良","損","未","未裝","斷","沒鎖","Err","無法","異常","閉鎖","鬆脫","脫落"]

def GetDeviceHistoryResult(RepairHistoryData):
    RepairTimes = 0
    f = open('FixHistory.html', 'w+', encoding='utf8')
    f.write('<h2>{}</h2>\n<table border="1" cellpadding="10">'.format(DeviceSN))

    #欄位建立
    f.write('<tr style="background-color:#DCE6F1;">\n')
    f.write('<th>{}</th>\n'.format('返修次數'))
    for DeviceHistoryColumns in DeviceHistoryResult.columns:
        f.write('<th>{}</th>\n'.format(DeviceHistoryColumns))
    f.write('</tr>\n')

    #輸出設備相關資料
    for DeviceHistoryIndexNumber in DeviceHistoryResult.index:
        #返修次數計算
        RepairTimes+=1
        f.write('<tr>\n')
        ColumnPosition=0
        DeviceHistoryInfoString = '<th>{}</th>\n'.format(RepairTimes)
        f.write(DeviceHistoryInfoString)

        for DeviceHistoryInfo in DeviceHistoryResult.loc[DeviceHistoryIndexNumber]:
            ColumnPosition+=1
            DeviceHistoryInfoString = '<th>{}</th>'.format(DeviceHistoryInfo)
            DeviceHistoryInfoString=DeviceHistoryInfoString.replace('\n', '<br>')
            f.write(DeviceHistoryInfoString)

        f.write('</tr>')
    f.write('</table>')
    f.close()

def DisplayRepairinfo(RepairDeviceInfo):
    #顯示目前設備資料
    ItemNumber = 0
    for DeviceInfo in RepairDeviceInfo.keys():
        ItemNumber+=1
        print('{}.{}:{}'.format(ItemNumber, DeviceInfo, RepairDeviceInfo[DeviceInfo]))

def SaveorTmp(RepairDeviceInfo):
    #資料無"維修結果",則將其存於暫存檔案中
    if RepairDeviceInfo['維修結果']=='':
        df = pandas.DataFrame.from_dict([RepairDeviceInfo])
        # 將DataFrame寫入CSV檔案
        df.to_csv('./TmpFiles/{}.csv'.format(DeviceSN), index=False,encoding='utf-8')
    else:
        f=open('BV2RepairHistory.csv','a',encoding='utf-8')
        RepairDeviceInfoList=[]
        for DeviceInfo in RepairDeviceInfo.values():
            RepairDeviceInfoList.append(DeviceInfo)

        for dataposition in range(len(RepairDeviceInfoList)-1):
            f.write('{},'.format(RepairDeviceInfoList[dataposition]))
        f.write(RepairDeviceInfoList[-1])
        f.close()

def FillOutFormProcess(RepairDeviceInfo):
    # 將字典轉成清單
    RepairDeviceInfoKeyList = []
    RepairDeviceInfoValueList = []

    for DeviceInfo in RepairDeviceInfo.keys():
        RepairDeviceInfoKeyList.append(DeviceInfo)
        RepairDeviceInfoValueList.append(RepairDeviceInfo[DeviceInfo])


    SelectNumber = ''
    while (1):
        if SelectNumber.isnumeric()==True:
            SelectNumber = eval(SelectNumber) - 1
            print('目前填寫項目:{}\n'.format(RepairDeviceInfoKeyList[SelectNumber]))
            print('離開填寫請填q')
            context = ''
            contextList = []
            while (context != 'q'):
                context = input()
                if context != 'q':
                    contextList.append(context.strip())
                print(contextList)

            ContextWords = ''
            if len(contextList) > 1:
                for x in contextList:
                    ContextWords = ContextWords + x + '\n'
                ContextWords = '"{}"'.format(ContextWords)
            else:
                ContextWords = contextList[0]
            RepairDeviceInfoValueList[SelectNumber] = ContextWords.strip()
            # 存到字典裡
            RepairDeviceInfo[RepairDeviceInfoKeyList[SelectNumber]] = RepairDeviceInfoValueList[SelectNumber]
            # 顯示目前設備資料
            DisplayRepairinfo(RepairDeviceInfo)

        else:
            print('s.保存')
            SelectNumber = input('請選擇要填寫的項目')
            if SelectNumber == 's':
                print('已保存填寫資料~')
                print('===========================================\n')
                break
            #連續填寫
            if SelectNumber=='c':
                print('中斷填寫請填e')

    return RepairDeviceInfo

def DisplayFucmenu():
    fucs=['''
    h.help
    s.保存
    d.顯示/關閉目前設備已填寫資訊
    c.連續填寫未填資訊
    ''']




if __name__ == '__main__':
    DeviceSN=''
    RepairDeviceInfo = {'維修時間': '', '維修單號': '', '送修機台序號': '', '業者': '', '車號': '', '維修人員': '', '送修原因': '', '維修結果': '',
                        '燒機測試LOG': '', '更換料件項目':'','備註': ''}
    #取得維修歷史資料
    RepairHistoryData=pandas.read_csv("BV2RepairHistory.csv")
    while(1):
        #使用者輸入後設備編號後取得相關資料
        DeviceSN=input('請輸入設備編號:\n')
        # DeviceSN='BVORB1320003'

        #確認該編號是否有未填寫完成的紀錄
        TmpFileList = os.listdir('./TmpFiles')
        if '{}.csv'.format(DeviceSN) in TmpFileList:
            print('該設備尚未填寫完成~')
            #取得已填寫資訊
            ExRepairDeviceInfo = pandas.read_csv('./TmpFiles/{}.csv'.format(DeviceSN))
            RepairDeviceInfo = ExRepairDeviceInfo.fillna('').to_dict(orient='index')[0]

            # 刪除暫存檔案
            file_path = './TmpFiles/{}.csv'.format(DeviceSN)
            # 如果檔案存在，則刪除它
            if os.path.isfile(file_path):
                os.remove(file_path)
        else:
            filt = (RepairHistoryData['送修機台序號']==DeviceSN)
            DeviceHistoryResult = RepairHistoryData.loc[filt].sort_values(["維修時間"], ascending=True).fillna('')

            if DeviceHistoryResult.shape[0]==0:
                print('無該設備歷史資料!!')
            else:
                # 輸出歷史資料
                GetDeviceHistoryResult(DeviceHistoryResult)
                # 顯示設備歷史資料
                os.system('FixHistory.html')
                #取出最後一筆歷史資料對本次維修有要填寫的項目
                LastDeviceInfo=DeviceHistoryResult.loc[DeviceHistoryResult.index[-1]].fillna('').to_dict()
                #清空應填寫項目
                EmptyTargetList = ['維修單號', '送修原因', '維修結果', '燒機測試LOG','更換料件項目', '備註']
                for EmptyTarget in EmptyTargetList:
                    LastDeviceInfo[EmptyTarget] = ''
                RepairDeviceInfo=LastDeviceInfo

            #僅於新建資料程序導入
            current_time = time.localtime()
            formatted_time = time.strftime('%Y/%m/%d', current_time)
            RepairDeviceInfo['維修時間'] = '{}'.format(formatted_time)

        #顯示目前設備資料
        print(RepairDeviceInfo)
        DisplayRepairinfo(RepairDeviceInfo)

        #設備資料填寫流程
        RepairDeviceInfo=FillOutFormProcess(RepairDeviceInfo)
        SaveorTmp(RepairDeviceInfo)
