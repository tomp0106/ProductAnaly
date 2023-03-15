a='F0002-000002$SOM板$1\nF0002-000002$SOM板$1'

f=open('test.html','w+',encoding='utf8')

def MaterialFormFill(MaterialColumInfo):
    #建立欄位名稱
    FirstColums='''
    <table border="1" cellpadding="10">
        <tr style="background-color:#DCE6F1;">
            <th>料號</th><th>料件名稱</th><th>更換數量</th>
        </tr>
    '''

    f.write(FirstColums)

    #填入料件內容
    #分割項目
    MaterialItems=a.split('\n')
    #逐項寫入表格
    for x in MaterialItems:
        f.write('<tr>\n')
        y=x.split('$')
        f.write('   <th>{}</th><th>{}</th><th>{}</th>'.format(y[0],y[1],y[2]))
        f.write('</tr>\n')
    f.write('</table>')
