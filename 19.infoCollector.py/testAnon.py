from anonBrowser import *
ab = anonBrowser(proxies= [],\
    user_agents=[('User-agent','superSelectBroswer')])
for attempt in range(1, 5):
    ab.anonymize()
    print '[*] Fetching Page...'
    response = ab.open('http://kittenwar.com')
    for cookie in ab.cookie_jar:
        print cookie