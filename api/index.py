from flask import Flask, request
import sys
from datetime import datetime, timedelta, timezone
import os
import requests
import json
from pyairtable import Table, Base
from pyairtable.formulas import match

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
timetabledict = {'월1사회2': '박경환 | 2301(1-5)', '월2체육': '강정현 | 6201(강당)', '월3미술': '이창열 | 3202(미술실)', '월4영어2': '이은정 | 2301(1-5)', '월5수학': '김효정 | 2301(1-5)', '월6한국사1': '윤선희 | 2301(1-5)', '월7정보': '이상옥 | 4201(SW융합실)', '화1한국사2': '김태경 | 2301(1-5)', '화2과학2': '이정미 | 2402(생물과학실)', '화3국어2': '남원정 | 2301(1-5)', '화4사회1': '권민호 | 2301(1-5)', '화5국어1': '김성은 | 2301(1-5)', '화6영어2': '이은정 | 2301(1-5)', '화7체육': '강정현 | 6201(강당)', '수1미술': '이창열 | 3202(미술실)', '수2수학': '김효정 | 2301(1-5)', '수3과학3': '이정미 | 2402(생물과학실)', '수4국어2': '남원정 | 2301(1-5)', '수5직업': '장지연 | 2404(진로실)', '수6진로': '남원정 | 2301(1-5)', '수7오늘은 7교시가 없어요':' - ','목1사회3': '박정호 | 2301(1-5)', '목2정보': '이상옥 | 4201(SW융합실)', '목3과학실험': '김명귀 | 2403(화학실험실)', '목4영어1': '신지현 | 2301(1-5)', '목5예술1': '이창열 | 3202(미술실)', '목6수학': '김효정 | 2301(1-5)', '목7국어1': '김성은 | 2301(1-5)', '금1수학': '김효정 | 2301(1-5)', '금2한국사2': '김태경 | 2301(1-5)', '금3영어1': '신지현 | 2301(1-5)', '금4과학1': '김명귀 | 2301(1-5)', '금5자율': '', '금6동아리': '', '금7여유': ''}
timetablelist = []
teacherlist = []


airtable_token = os.environ.get('Airtable_Key')
BASE_ID = 'appehbq0HhoF3Rk62'
TABLE_NAME = 'tblnxuLnQ0t4qPlox'
userIdData = Table(airtable_token, BASE_ID, TABLE_NAME)

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
	
	return userIdData.all()


# 동의서 작성

@app.route('/agree1', methods = ['POST'])
def agree1():
	responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "개인정보 수집 및 이용 동의서",
		  "description": "\'오늘 급식 뭐임\'(이하 \'서비스\')은 급식, 시간표, 학사 일정 확인 등을 위해 「개인정보 보호법」 제 15조 1항에 따라 보유 기간(25년 2월 28일)까지 사용자의 개인정보(사용자 ID, 학교, 학년, 반)를 수집 및 이용합니다. 사용자는 서비스 이용에 필요한 최소한의 개인정보 수집 및 이용에 동의하지 않을 수 있으나, 동의를 거부 할 경우 서비스 이용이 불가합니다.\n아래 동의 버튼 클릭 시 해당 내용에 동의한 것으로 간주됩니다.",
		"buttons": [
			{
			  "action": "block",
			  "label": "동의",
			  "blockId" : "65faa5ef091618695a7fee9c"
			}
		]
		}
		  
	  }
	]
  }
}
	return responesebody

@app.route('/agree2', methods = ['POST'])
def agree2():
	body = request.get_json()
	userID = body['userRequest']['user']['id']
	
	try:
		useridtable = userIdData.all(formula=match({"userID":userID}))
	except:
		Newdata = {'userID': userID, 'schoolcode': "E", 'gradecode': 0, 'gradecode': 0}
		userIdData.create(Newdata)
		print(Newdata)

	if useridtable == 0 or useridtable == "false" or useridtable == "" or useridtable == "NaN" or useridtable == []:
		Newdata = {'userID': userID, 'schoolcode': "E", 'gradecode': 0, 'gradecode': 0}
		userIdData.create(Newdata)
		print(Newdata)
	
	responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	{
		"basicCard": {
			"title": "학교를 입력해 주세요",
			"description": "현재 삼남중학교, 언양고등학교만 지원합니다. \n학교 추가를 바라신다면 상담직원 연결을 눌러주세요.",
			"thumbnail": {
				"imageUrl": "https://cdn.discordapp.com/attachments/1021364751541997659/1219962349981798431/253206e9ece97e04.png?ex=660d357a&is=65fac07a&hm=7849e04bb18f371d63d376a6b1f64f434683fe9b433dd5cd770167a8d5a58716&"
			}
		}
	}
	],
	"quickReplies": [
		{
			"label": "삼남중학교",
			"action": "block",
			"messageText": "삼남중학교",
			"blockId": "65faa603e8b2137164330ae3"
		},
		{
			"messageText": "언양고등학교",
			"action": "block",
			"label": "언양고등학교",
			"blockId": "65faa603e8b2137164330ae3"
		}
					]
	}
}
	return responesebody

@app.route('/school', methods = ['POST'])
def school():
	body = request.get_json()
	userschool = body['userRequest']['utterance']
	userID = body['userRequest']['user']['id']
	useridtable = userIdData.all(formula=match({"userID":userID}))
	id1 = useridtable[0]['id']
	for a in userIdData.all():
		if id1 == a['id']:
			if userschool == "삼남중학교":
				userIdData.update(id1, {"schoolcode": "S"})
			elif userschool == "언양고등학교":
				userIdData.update(id1, {"schoolcode": "E"})
			else:
				userIdData.update(id1, {"schoolcode": "0"})
	responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"basicCard": {
		  "title": "학년을 입력해 주세요",
		  "thumbnail": {
				"imageUrl": "https://cdn.discordapp.com/attachments/1021364751541997659/1219962349981798431/253206e9ece97e04.png?ex=660d357a&is=65fac07a&hm=7849e04bb18f371d63d376a6b1f64f434683fe9b433dd5cd770167a8d5a58716&"
}

		} 
	  }
	],
	"quickReplies": [
	  {
		"messageText": "1학년",
		"action": "block",
		"label": "1학년",
	"blockId": "65faa61da0a1dd2d9e02e80e"
	  },
	  {
		"messageText": "2학년",
		"action": "block",
		"label": "2학년",
		"blockId": "65faa61da0a1dd2d9e02e80e"
	  },
	{
		"messageText": "3학년",
		"action": "block",
		"label": "3학년",
		"blockId": "65faa61da0a1dd2d9e02e80e"
	  }
	]
  }
}
	return responesebody

@app.route('/grade', methods = ['POST'])
def grade():
	body = request.get_json()
	usergrade = body['userRequest']['utterance']
	userID = body['userRequest']['user']['id']
	useridtable = userIdData.all(formula=match({"userID":userID}))
	id1 = useridtable[0]['id']
	for a in userIdData.all():
		if id1 == a['id']:
			if usergrade == "1학년":
				userIdData.update(id1, {"gradecode": 1})
			elif userschool == "2학년":
				userIdData.update(id1, {"gradecode": 2})
			elif userschool == "3학년":
				userIdData.update(id1, {"gradecode": 3})
			else:
				userIdData.update(id1, {"gradecode": 0})
	responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"basicCard": {
		  "title": "반을 입력해 주세요",
"thumbnail": {
				"imageUrl": "https://cdn.discordapp.com/attachments/1021364751541997659/1219962349981798431/253206e9ece97e04.png?ex=660d357a&is=65fac07a&hm=7849e04bb18f371d63d376a6b1f64f434683fe9b433dd5cd770167a8d5a58716&"
		  }
		} 
	  }
	],
	"quickReplies": [
	  {
		"messageText": "1반",
		"action": "block",
		"label": "1반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "2반",
		"action": "block",
		"label": "2반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "3반",
		"action": "block",
		"label": "3반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "4반",
		"action": "block",
		"label": "4반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "5반",
		"action": "block",
		"label": "5반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "6반",
		"action": "block",
		"label": "6반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "7반",
		"action": "block",
		"label": "7반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "8반",
		"action": "block",
		"label": "8반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "9반",
		"action": "block",
		"label": "9반",
		"blockId": "65faa630d7cbb10c92facd52"
	  }
	  
	]
  }
}
	return responesebody

@app.route('/class1', methods = ['POST'])
def class1():
	body = request.get_json()
	userclass = body['userRequest']['utterance']
	userID = body['userRequest']['user']['id']
	useridtable = userIdData.all(formula=match({"userID":userID}))
	id1 = useridtable[0]['id']
	for a in userIdData.all():
		if id1 == a['id']:
			data = a['fields']
			uclass = userclass
			if userclass == "1반":
				userIdData.update(id1, {"classcode": 1})
			elif userclass == "2반":
				userIdData.update(id1, {"classcode": 2})
			elif userclass == "3반":
				userIdData.update(id1, {"classcode": 3})
			elif userclass == "4반":
				userIdData.update(id1, {"classcode": 4})
			elif userclass == "5반":
				userIdData.update(id1, {"classcode": 5})
			elif userclass == "6반":
				userIdData.update(id1, {"classcode": 6})
			elif userclass == "7반":
				userIdData.update(id1, {"classcode": 7})
			elif userclass == "8반":
				userIdData.update(id1, {"classcode": 8})
			elif userclass == "9반":
				userIdData.update(id1, {"classcode": 9})
			else:
				userIdData.update(id1, {"classcode": 0})

			if data['schoolcode'] == "S":
				uschool = "삼남중학교 "
			elif data['schoolcode'] == "E":
				uschool = "언양고등학교 "
			else:
				uschool = "지원하지 않는 학교 "
		
			if data['gradecode'] == "1":
				ugrade = "1학년 "
			elif data['gradecode'] == "2":
				ugrade = "2학년 "
			elif data['gradecode'] == "3":
				ugrade = "3학년 "
			else:
				ugrade = "지원하지 않는 학년 "
				
			description = str(uschool) + str(ugrade) + str(uclass)
			print(description)
	
			responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "입력한 정보가 맞는지 확인해 주세요",
		  "description": description,
		"buttons": [
			{
			  "action": "block",
			  "label": "맞아요!",
			  "blockId" : "65faaca1a64303558477aa63"
			},
			{
			  "action": "block",
			  "label": "아니에요",
			  "blockId" : "65faa5ef091618695a7fee9c"
			}
		]
		}
		  
	  }
	]
  }
}
			return responesebody
	

	except:
		responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "입력한 정보가 맞는지 확인해 주세요",
		  "description": "오류 발생, 아니에요 버튼을 눌러 다시 확인해 주세요",
		"buttons": [
			{
			  "action": "block",
			  "label": "맞아요!",
			  "blockId" : "65faaca1a64303558477aa63"
			},
			{
			  "action": "block",
			  "label": "아니에요",
			  "blockId" : "65faa5ef091618695a7fee9c"
			}
		]
		}
		  
	  }
	]
  }
}
	
	
		return responesebody

@app.route('/check', methods = ['POST'])
def check():
	responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "입력한 정보가 등록되었어요",
		"buttons": [
			{
			  "action": "message",
			  "label": "오늘 급식 뭐임?"
			},
			{
			  "action": "message",
			  "label": "오늘 시간표 뭐임?"
			}
		]
		}
		  
	  }
	]
  }
}
	return responesebody


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
			  "head": {
				"title": date + " 시간표" 
			  	},
			  	"itemList": [
				{
				"title": '1교시',
				"description": timetablelist[0] + ' | ' + teacherlist[0]
				},
				{
				"title": '2교시',
				"description": timetablelist[1] + ' | ' + teacherlist[1]
				},
				{
				"title": '3교시',
				"description": timetablelist[2] + ' | ' + teacherlist[2]
				},
				{
				"title": '4교시',
				"description": timetablelist[3] + ' | ' + teacherlist[3]
				},
				{
				"title": '5교시',
				"description": timetablelist[4] + ' | ' + teacherlist[4]
				},
				{
				"title": '6교시',
				"description": timetablelist[5] + ' | ' + teacherlist[5]
				},
				{
				"title": '7교시',
				"description": timetablelist[6] + ' | ' + teacherlist[6]
				}
			  ],
			  "itemListAlignment": "left"
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
