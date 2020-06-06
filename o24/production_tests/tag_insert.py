import base64
import html
import uuid
from bs4 import BeautifulSoup
import traceback
 

html = '''
<!DOCTYPE html>
<html>
<head>
</head>
<body>
Hi Kirill <br /><br />My name is Kirill - I'm a blockchain developer and writer. Since early 2017 I’ve worked hard to become the top blockchain contributor for Hacker Noon - you can check my signature for published topics and my Linkedin and Hacker Noon profiles.<br /><br />I'm writing a Roundup <span style="color: #e74c3c;">topic for NewsBtc</span> that I’m planning to publish in the beginning of March.<br /><br /><br /><strong>The idea:</strong><br />Make a roundup with quotes from blockchain project founders, and ask them:<br /><span style="color: #e74c3c;"><em>What will be the share (in %) of crypto payments for online services at the end of 2020? Which services will be paid with crypto the most and why? (Excluding dark-net)</em></span><br /><br /><br />It's good PR for projects and interesting to the community at large:<br />- Quote from the founder<br />- Dofollow link from NewsBtc<br />The price to be mentioned: $50 (Small managing fee: proofreading, editing, distribution)<br /><br /><br />I've done such a Roundup recently and it got a lot of hype - you could find a link in a signature.<br /><br />Is this interesting to you?<br /><br /><br />P.S.<br />If you’re not interested, just let me know.<br />For a quicker response, message me on telegram: ksshilov<br /><br />Thanks,<br />Kirill Shilov,<br /><br />Telegram: @ksshilov<br />Linkedin: https://www.linkedin.com/in/kirill-shilov-25aa8630/
</body>
</html>
'''


tracking_link = 'https://via.smtps.com/ot/dsfadsfadsfa/open'

soup = BeautifulSoup(html, "html.parser")

tag = soup.new_tag('img', 
                    width="1", 
                    height="1", 
                    style="display: block;", 
                    alt="", 
                    src=tracking_link)
print(tag)
#soup.body.append(tag)

#soup.head.append(tag)
soup.html.append(tag)

print(str(soup))

