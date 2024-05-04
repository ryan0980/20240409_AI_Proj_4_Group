import json

import requests
from pyasn1.compat.octets import null

# define all the GET Method in this class
headers = {
    'x-api-key': '3e39b9b8cab6cae613bc',
    'userId': '3631',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'PostmanRuntime/7.37.0',
    'Connection': 'keep-alive',
}


class GET:
    def __init__(self):
        self.url = "https://www.notexponential.com/aip2pgaming/api/rl/score.php"
        self.headers = headers  # Dictionary to store headers

    # Parameters: type=runs, teamId=$teamId, count=$count
    # Return Values: Your previous $count runs with score.  
    def getRuns(self, teamId: str, count: int) -> json:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/rl/score.php?type=runs&teamId=' + teamId + '&count=' + str(
            count)
        response = requests.request("GET", url=self.url, headers=self.headers)
        return json.loads(response.text)

    # Parameters: type=location, teamId=$teamId
    # Return Values: your current world and state in that world.  Think of this as your GPS, and confirm where you are.  If you are in world “-1”, that means you are in no world, and you can enter a world.   
    def getLocation(self, teamId: str) -> tuple:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/rl/gw.php?type=location&teamId=' + teamId
        response = requests.request("GET", url=self.url, headers=self.headers)
        
        if json.loads(response.text)["state"] == "" or null:
            return null, null
        x, y = map(int, json.loads(response.text)["state"].split(':'))
        world = json.loads(response.text)["world"]
        if not json.loads(response.text)["state"]:
            return world, null
        x, y = map(int, json.loads(response.text)["state"].split(':'))
        return world, (x, y)

    def resetWorld(self, teamId: str) -> None:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/rl/reset.php?teamId=' + teamId + '&otp=5712768807'

    def getScore(self, teamId: str) -> json:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/rl/score.php?type=score&teamId=' + teamId
        response = requests.request("GET", url=self.url, headers=self.headers)
        return json.loads(response.text)

class POST:
    def __init__(self):
        self.url = "https://www.notexponential.com/aip2pgaming/api/rl/gw.php"
        self.headers = headers
        self.payload = {}

    # Body: type=”enter”, worldId=$worldId, teamId=$teamId
    # Return Values: The new $runId started
    # Fails if you are already in a world.
    def enterWorld(self, worldId: str, teamid: str) -> None:
        self.payload = {'type': 'enter', 'worldId': worldId, 'teamId': teamid}
        response = requests.request("POST", url=self.url, headers=self.headers, data=self.payload)
        print("resText"+response.text)
        return json.loads(response.text)

    # Body: type=”move”, teamId=$teamId, move=”$move”, worldId=$worldId
    # Return Values: Reward, New State entered $runId started
    # Fails if you are not already in a world (in that case, enter a world first).
    def makeMove(self, teamid: str, move: str, worldId: str) -> json:
        self.payload = {'type': 'move', 'teamId': teamid, 'move': move, 'worldId': worldId}
        response = requests.request("POST", url=self.url, headers=self.headers, data=self.payload)
        print("resText"+response.text)
        return json.loads(response.text)


if __name__ == "__main__":
    # example
    get_test = GET()
    text = get_test.getScore('1399')
    print(text)

    # get_test = GET()
    # text = get_test.getRuns('1399',10000000)
    # print(text)
    # Count the records for each 'gworldId'
    # gworld_counts = {}
    # for run in text['runs']:
    #     # Get the 'gworldId'
    #     gworld_id = run.get('gworldId')
    #     # If the 'gworldId' is already in the dictionary, increment the count
    #     if gworld_id in gworld_counts:
    #         gworld_counts[gworld_id] += 1
    #     # If this is the first time we see the 'gworldId', initialize count to 1
    #     else:
    #         gworld_counts[gworld_id] = 1

    # Output the results
    # print(gworld_counts)
    post_test = POST()
    #  post_test.enterWorld('8', '1399')

    # getOp = GET()
    # getOp.resetWorld('1412')
    # response = requests.request("GET", url=getOp.url, headers=getOp.headers)
    # print(response.text)

    # W: -1,0   N: 0,+1  S: 0,-1  E:+1,0
    #  N: 1,0         E:0,1
    # N-1,0
    # moveInfo = post_test.makeMove('1399', 'N', '8')
    # print(moveInfo)

    get_test = GET()
    state = get_test.getLocation('1412')
    print(state)
