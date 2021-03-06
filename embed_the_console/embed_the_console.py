# DocuSign API Walkthrough 09 (PYTHON) - Embedded DocuSign
import sys, httplib2, json;

#enter your info:
username = "***";
password = "***";
integratorKey = "***";
templateId = "***";

authenticateStr = "<DocuSignCredentials>" \
                    "<Username>" + username + "</Username>" \
                    "<Password>" + password + "</Password>" \
                    "<IntegratorKey>" + integratorKey + "</IntegratorKey>" \
                    "</DocuSignCredentials>";
#
# STEP 1 - Login
#
url = 'https://demo.docusign.net/restapi/v2/login_information';   
headers = {'X-DocuSign-Authentication': authenticateStr, 'Accept': 'application/json'};
http = httplib2.Http();
response, content = http.request(url, 'GET', headers=headers);

status = response.get('status');
if (status != '200'): 
    print("Error calling webservice, status is: %s" % status); sys.exit();

# get the baseUrl and accountId from the response body
data = json.loads(content);
loginInfo = data.get('loginAccounts');
D = loginInfo[0];
baseUrl = D['baseUrl'];
accountId = D['accountId'];

#--- display results
print ("baseUrl = %s\naccountId = %s" % (baseUrl, accountId));

#
# STEP 2 - Get Console View
#

#construct the body of the request in JSON format.  In this case all we need is the accountId  
requestBody = "{\"accountId\": \"" + accountId + "\"}";

# append "/views/console" to the baseUrl and use in the request
url = baseUrl + "/views/console";
headers = {'X-DocuSign-Authentication': authenticateStr, 'Accept': 'application/json', 'Content-Length': str(len(requestBody))};
http = httplib2.Http();
response, content = http.request(url, 'POST', headers=headers, body=requestBody);
status = response.get('status');
if (status != '201'): 
    print("Error calling webservice, status is: %s" % status); sys.exit();
data = json.loads(content);
viewUrl = data.get('url');

#--- display results
print ("View URL = %s\n" % viewUrl)
