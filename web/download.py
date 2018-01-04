#!/usr/bin/env python
#encoding=utf-8
import os
import xlwt
from django.http import StreamingHttpResponse


def createdownloadfile(table, table_info, filename):
    workbook=xlwt.Workbook(encoding='utf-8')
    booksheet=workbook.add_sheet("test1",cell_overwrite_ok=True)
    row_c=len(table)
    i=0
    while i<row_c:
        booksheet.write(0,i,table[i][1])
        i+=1
    i=1
    for info in table_info:
        j=0
        while j<row_c:
            booksheet.write(i,j,getattr(info,table[j][0]))
            j+=1
        i+=1
    tmpfile='/tmp/table.tmp'
    if os.path.exists(tmpfile):os.remove(tmpfile)
    workbook.save(tmpfile)
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:yield c
                else:
                    f.close()
                    break
    response=StreamingHttpResponse(file_iterator(tmpfile),content_type='application/vnd.ms-excel')
    response['Content-Disposition']='attachment; filename="'+filename+'"'
    return response
