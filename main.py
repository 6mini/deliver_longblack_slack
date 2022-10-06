from slack_sdk import WebClient
from bs4 import BeautifulSoup
import requests
import json

def main():
    token = "my-token"
    channel = "my-channel"
    
    message = []
    
    url = "https://www.longblack.co/"
            
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    get_today_href = soup.select_one("#today-note-img").get("href")

    soup2 = BeautifulSoup(requests.get(get_today_href).text, 'html.parser')

    content = soup2.select_one(".note-content").select("p")
    
    if "C" in content[0].text:
        link_text = "오늘의 롱블랙 노트, 읽으러 가보지 않으실래요?"
    elif "L" in content[0].text:
        link_text = "오늘의 롱블랙 노트, 읽으러 가보지 않을래?"
    else:
        link_text = "오늘의 롱블랙 노트, 함께 읽으러 가보시겠어요?"
    
    for i in content[1:]:
        try:
            strong = i.select_one("strong").text
            if strong == " ":
                pass
            elif '“' in strong:
                pass
            elif i.select_one("a"):
                pass
            else:
                break
        except:
            pass
        
        if i.get("style") == "margin-left: 40px;":
            text = i.text.replace(".**", ".\n ** ")
            text = text.replace(".*", ".\n * ")
            message.append({
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": text
                            }
                        })
    message.append({
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"<{get_today_href}|{link_text}>"
                            }
                        })


    client = WebClient(token=token)
    client.chat_postMessage(channel=channel, blocks=json.dumps(message))

if __name__ == '__main__':
    main()