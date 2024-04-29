import json

import requests
from pyasn1.compat.octets import null

# define all the GET Method in this class
headers = {
    'x-api-key': 'ac4f3d3f5d3dff02d9bf',
    'userId': '3597',
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
        if not json.loads(response.text)["state"]:
            return null
        x, y = map(int, json.loads(response.text)["state"].split(':'))
        world = json.loads(response.text)["world"]
        return world, (x, y)

    def resetWorld(self, teamId: str) -> None:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/rl/reset.php?teamId=' + teamId + '&otp=5712768807'


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
    text = get_test.getRuns('1399', 2)
    print(text)

    post_test = POST()
    post_test.enterWorld('2', '1399')
    print(post_test.payload)
    response = requests.request("POST", url=post_test.url, headers=post_test.headers, data=post_test.payload)
    print(response.text)

    # getOp = GET()
    # getOp.resetWorld('1399')
    # response = requests.request("GET", url=getOp.url, headers=getOp.headers)
    # print(response.text)

    # W: -1,0   N: 0,+1  S: 0,-1  E:+1,0
    # moveInfo = post_test.makeMove('1399', 'E', '1')
    # print(moveInfo)

    get_test = GET()
    state = get_test.getLocation('1399')
    print(state)
