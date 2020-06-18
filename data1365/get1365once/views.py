
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse

sdate = datetime.now()
edate = datetime.now() + timedelta(days=31)
cntPage = 1
url_Main = "https://www.1365.go.kr/vols/P9210/partcptn/timeCptn.do"

#postㄹ
search_info = {
    "cPage": 1
    , "searchFlag": "search"
    , "requstSe": ""
    , "firstSearch": ""
    , "flag": "A01"
    , "searchHopeArea1": "6410000"
    , "searchHopeArea2": "4060000"
    , "searchHopeSrvc1": ""
    , "searchHopeSrvc2": ""
    , "searchSrvcTarget": ""
    , "searchRequstSe": "on"
    , "searchProgrmBgnde": sdate
    , "searchProgrmEndde": edate
    , "yngbgsPosblAt": "Y"        #청소년
    , "adultPosblAt": "Y"        #성인
    , "searchSrvcStts": "0"
    , "searchKeyword": ""
}



def MakeBasicHtml():
    strHtml = '''<html><head>
                <link rel="shortcut icon" href="https://www.1365.go.kr/web/vols/images/ico/favicon.ico" type="images/x-ico" />
                <link rel="stylesheet" type="text/css" href="https://www.1365.go.kr/web/vols/css/base.css?v=20180426">
                <link rel="stylesheet" type="text/css" href="https://www.1365.go.kr/web/vols/css/common.css?v=20180509">
                <link rel="stylesheet" type="text/css" href="https://www.1365.go.kr/web/vols/css/slick.css">
                <script type="text/javascript" src="https://www.1365.go.kr/web/vols/js/jquery-1.12.4.min.js"></script>
                <script type="text/javascript" src="https://www.1365.go.kr/web/vols/js/common.js"></script>
                <script type="text/javascript" src="https://www.1365.go.kr/web/vols/js/vols_common.js"></script>
                <script type="text/javascript" src="https://www.1365.go.kr/web/vols/js/frontUi.js"></script>	
                <script type="text/javascript" src="https://www.1365.go.kr/web/vols/js/modules/calendar.js"></script>
                <script type="text/javascript" src="https://www.1365.go.kr/web/cmmn/js/miya_validator.js"></script>
                <script type="text/javascript" src="https://www.1365.go.kr/js/prtl/netfunnel.js"></script>
            </head>
	
            <body> 
                <script type = "text/javascript" >
                    function show(No){
                        var no = No;
                        $('#firstSearch').val('N');
                        //접근성관련 수정
                        //$('#progrmRegistNo').val(no);
                        $('#progrmRegistNo_'+no).val(no);
                        $('#cPage').val('1');
                        var flag = $('#flag').val();

                        if(flag == 'A01'){ 
                            returnUrl="https://www.1365.go.kr/vols/P9210/partcptn/timeCptn.do;jsessionid=a2cgAbx7sRQL9XmXnQ71tpVJ.node10?titleNm=상세보기&type=show&progrmRegistNo="+no+"";
                        }
                        else if(flag == 'A02'){                            returnUrl="https://www.1365.go.kr/vols/P9220/partcptn/partCptn.do;jsessionid=a2cgAbx7sRQL9XmXnQ71tpVJ.node10?titleNm=상세보기&type=show&progrmRegistNo="+no+"";
                        }
                        else{                            returnUrl="https://www.1365.go.kr/vols/P9230/partcptn/grpCptn.do;jsessionid=a2cgAbx7sRQL9XmXnQ71tpVJ.node10?titleNm=상세보기&type=show&progrmRegistNo="+no+"";
                        }
                        document.frm.action = returnUrl;
                        document.frm.target = "_top";
                        //document.frm.target = "_blank";
                        document.frm.submit();
                    }
                </script>

                <form method="post" name="frm" id="frm" action="">
                <input type="hidden" id="jsonUrl" name="jsonUrl" value="''' +url_Main+ '''" />
                <input type="hidden" id="cPage"    name="cPage"  value="1" />
                <input type="hidden" id="searchFlag" name="searchFlag" value="search" />
                <input type="hidden" id="requstSe" name="requstSe" value="" />
                <input type="hidden" id="firstSearch" name="firstSearch" value="" />
                <input type="hidden" id="flag"     name="flag"   value="A01"/>
    '''

    return strHtml


def GetData(url, info):
    rtnVal = ""

    session = requests.session()
    res = session.post(url, data=info)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")    
    tag_list = soup.find('div',{'class':'board_list board_list2 non_sub'})
    

    if info["cPage"] == 1:
        ## 페이지 갯수 찾기
        ## [전체 13건, 현재페이지 1/2] 에서 2 갖고 오기 (2020.6.15)
        countInfo = soup.find('div',{'class':'search_result'}).text
        
        global cntPage
        cntPage = int(countInfo.split("]")[0].split("/")[1])

    
    return str(tag_list)



def main(request):
    global cntPage
    result = ""
    #기본(head정보, link html)
    result += MakeBasicHtml()
    
    ## 첫페이지
    result += GetData(url_Main, search_info)

    ## 페이지 수 만큼 자료 갖고 오기
    if cntPage >= 2:
        for i in range(2, cntPage + 1):
            search_info["cPage"] = i
            result += GetData(url_Main, search_info)

    result+="</body> </html>"
    
    return HttpResponse(result)
    #################################################
    
