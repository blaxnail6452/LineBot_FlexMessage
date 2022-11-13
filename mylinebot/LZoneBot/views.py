from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, FlexSendMessage
import json
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
return_message = ""
return_mode = ""
flexMessageJson = ""
alt_text = ""

@csrf_exempt
def callback(request):
    global return_message
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件


                #會動到的只有以下的if_else，如果想要再新增關鍵字，就從這邊加入
                #記得每個回答皆要設定return_mode的形式
                if event.message.text == "智能客服": #以Flex Message回復的範例
                    flexMessageJson = "test.json" #這個變數是填你要回答用的JSON檔名稱
                    return_mode = "flexmessage" #這個寫法代表是要用Flex Message回復
                else: #以純文字回復的範例
                    return_message = "抱歉，我無法回答><" #這個變數是填你純文字回復的內容
                    return_mode = "text" #這個寫法代表是要用純文字回復

                #會動到的只有這邊以上，其他地方都不動!




                if return_mode == "text": #以文字訊息回復
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=return_message)
                    )
                elif return_mode == "flexmessage": #以Flex Message回復
                    alt_text = event.message.text
                    FlexMessage = json.load(open(flexMessageJson,'r',encoding='utf-8'))
                    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text, FlexMessage))
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
