from flask import Flask, request
import sys
from datetime import datetime, timedelta, timezone
import os
import requests
import json


# 시간 설정

datetime_utc = datetime.utcnow()
timezone_kst = timezone(timedelta(hours=9))
datetime_kst = datetime_utc.astimezone(timezone_kst)
day = datetime_kst.strftime("%Y%m%d")
date = str(int(datetime_kst.strftime("%m"))) + "월 "+ str(int(datetime_kst.strftime("%d"))) + "일"
week = int(datetime_kst.strftime("%w"))

# 환경변수/시간표 설정
# table1 - 시간표
NEISurl = "https://open.neis.go.kr/hub/mealServiceDietInfo"
service_key = os.environ.get('NEIS_Key')
edu_code = 'H10'
school_codeE = '7480188'
school_codeS = '7501030'
weeklist = {'0':'일','1':'월','2':'화','3':'수','4':'목','5':'금','6':'토'}
timetabledict = {'월1사회2': '박경환 | 2301(1-5)', '월2체육': '강정현 | 6201(강당)', '월3미술': '이창열 | 3202(미술실)', '월4영어2': '이은정 | 2301(1-5)', '월5수학': '김효정 | 2301(1-5)', '월6한국사1': '윤선희 | 2301(1-5)', '월7정보': '이상옥 | 4201(SW융합실)', '화1한국사2': '김태경 | 2301(1-5)', '화2과학2': '이정미 | 2402(생물과학실)', '화3국어2': '남원정 | 2301(1-5)', '화4사회1': '권민호 | 2301(1-5)', '화5국어1': '김성은 | 2301(1-5)', '화6영어2': '이은정 | 2301(1-5)', '화7체육': '강정현 | 6201(강당)', '수1미술': '이창열 | 3202(미술실)', '수2수학': '김효정 | 2301(1-5)', '수3과학3': '이정미 | 2402(생물과학실)', '수4국어2': '남원정 | 2301(1-5)', '수5직업': '장지연 | 2404(진로실)', '수6진로': '남원정 | 2301(1-5)', '수7오늘은 7교시가 없어요':'','목1사회3': '박정호 | 2301(1-5)', '목2정보': '이상옥 | 4201(SW융합실)', '목3과학실험': '김명귀 | 2403(화학실험실)', '목4영어1': '신지현 | 2301(1-5)', '목5예술1': '이창열 | 3202(미술실)', '목6수학': '김효정 | 2301(1-5)', '목7국어1': '김성은 | 2301(1-5)', '금1수학': '김효정 | 2301(1-5)', '금2한국사2': '김태경 | 2301(1-5)', '금3영어1': '신지현 | 2301(1-5)', '금4과학1': '김명귀 | 2301(1-5)', '금5자율': '', '금6동아리': '', '금7여유': ''}
timetablelist = []
teacherlist = []

#

# @app.route('/service', methods = ["POST"])
# 	body = request.get_json()
# 	userTimezone = body['userRequest']['timezone']

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello, World!'

@app.route('/time')
def time():
	return str(datetime_kst) + "  " + str(day)

@app.route('/test')
def test():
	return 'test'


@app.route('/timetable', methods = ["POST"])
def timetable():
	weekstr = str(week)
	weekday = weeklist.get(weekstr, "월")
	passing_timetable = {timetab: teacher for timetab, teacher in timetabledict.items() if not(timetab.find(weekday) == -1)}
	for key in passing_timetable:
		timetablelist.append(key[2:])

	for value in passing_timetable.values():
		teacherlist.append(value)
	responseBody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"itemCard":{
		  "items": [
			{
			  "imageTitle": {
				"title": date + " 시간표" 
			  },
			  "itemList": [
				{
				  "title": '1교시',
				  "description": timetablelist[1] + ' | ' + teacherlist[1]
				 },
		{
				  "title": '2교시',
				  "description": timetablelist[2] + ' | ' + teacherlist[2]
				 },
		{
				  "title": '3교시',
				  "description": timetablelist[3] + ' | ' + teacherlist[3]
				 },
		{
				  "title": '4교시',
				  "description": timetablelist[4] + ' | ' + teacherlist[4]
				 },
		{
				  "title": '5교시',
				  "description": timetablelist[5] + ' | ' + teacherlist[5]
				 },
		{
				  "title": '6교시',
				  "description": timetablelist[6] + ' | ' + teacherlist[6]
				 },
				 {
				  "title": '7교시',
				  "description": timetablelist[7] + ' | ' + teacherlist[7]
				 }
			  ],
			  "itemListAlignment": "left"
		}
	  ]
	}
	  }
	]
  }
	}
	return responseBody
	   

@app.route('/service', methods = ["POST"])
def service():
	params = {
		'KEY' : service_key,
		'Type' : 'json',
		'pIndex' : '1',
		'pSize' : '100',
		'ATPT_OFCDC_SC_CODE' : edu_code,
		'SD_SCHUL_CODE' : school_codeE,
		'MLSV_YMD' : day
		}

	response = requests.get(NEISurl, params=params)
	contents = response.text

	#급식 미제공 날짜 구별
	find = contents.find('해당하는 데이터가 없습니다.')
	
	if find == -1:
		findstart = contents.find('DDISH_NM') + 11
		findend = contents.find('ORPLC_INFO') - 3
		content = contents[findstart:findend]
		meal ="\n".join(content.split('<br/>'))
	else:
		meal = "오늘은 급식이 없습니다!"

		responseBody = {
		"version": "2.0",
		"template": {
			"outputs": [
				{
					"textCard": {
		  				"title": date + " 오늘의 급식",
		  				"description": meal ,
		  				"buttons": [
							{
			  					"action": "webLink",
			  					"label": "온라인 건의함",
			  					"webLinkUrl": "https://m.site.naver.com/1k4Sj"
							}
									]
								}
				}
						]
		}
	}
	return responseBody
