from django.http import HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json, requests,pywapi, re


PAGE_ACCESS_TOKEN="Access Token Here"
VERIFY_TOKEN = "Verify Token here"


class FbotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('hub.verify_token','435555343695') == VERIFY_TOKEN:
            return HttpResponse(self.request.GET.get('hub.challenge'))
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    # Assuming the sender only sends text.
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()

def post_facebook_message(fbid,recevied_message):
     responsetext = ''

     if re.search('weather', recevied_message, re.IGNORECASE):
         responsetext = mylocalweather()
     else:
         responsetext = "I didn't understand! Send 'Weather' for your current weather"

     post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+access_token
     response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":responsetext}})
     status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
     print(status.json())


def mylocalweather():
    '''get current weather update for New York'''
    weather = pywapi.get_weather_from_noaa('KJFK')
    current = 'It is ' + weather['weather'] + ' and ' + weather['temp_f'] + 'F right now in New York'
    return current
