import requests
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
        self.headers =headers # Dictionary to store headers

    # Parameters: type=runs, teamId=$teamId, count=$count
    # Return Values: Your previous $count runs with score.  
    def getRuns(self, teamId: str, count: int) ->None:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/rl/score.php?type=runs&teamId='+ teamId +'&count='+ str(count)
    
    # Parameters: type=location, teamId=$teamId
    # Return Values: your current world and state in that world.  Think of this as your GPS, and confirm where you are.  If you are in world “-1”, that means you are in no world, and you can enter a world.   
    def getLocation(self, teamId: str) ->None:
         self.url ='https://www.notexponential.com/aip2pgaming/api/rl/gw.php?type=location&teamId=' + teamId

class POST:
    def __init__(self):
        self.url = "https://www.notexponential.com/aip2pgaming/api/rl/gw.php"
        self.headers = headers
        self.payload ={}

    # Body: type=”enter”, worldId=$worldId, teamId=$teamId
    # Return Values: The new $runId started
    # Fails if you are already in a world.
    def enterWorld(self, worldId :str, teamid :str) ->None:
         self.payload = {'type': 'enter', 'worldId': worldId, 'teamId': teamid}

    # Body: type=”move”, teamId=$teamId, move=”$move”, worldId=$worldId
    # Return Values: Reward, New State entered $runId started
    # Fails if you are not already in a world (in that case, enter a world first).
    def makeMove(self, teamid :str,  move : str, worldId :str) ->None:
        self.payload = {'type': 'move', 'teamId': teamid, 'move': move, 'worldId': worldId}



if __name__ == "__main__":
     # example
     get_test = GET()
     get_test.getRuns('1399', 10)
     response = requests.request("GET", url=get_test.url, headers=get_test.headers)
     print(response.text)

    #  post_test = POST()
    #  post_test.enterWorld('1', '1399')
    #  print(post_test.payload)
    #  response = requests.request("POST", url = post_test.url, headers=post_test.headers, data = post_test.payload)
    #  print(response.text)

    #  post_test = POST()
    #  post_test.makeMove('1399', 'N', '0')
    #  print(post_test.payload)
    #  response = requests.request("POST", url = post_test.url, headers=post_test.headers, data = post_test.payload)
    #  print(response.text)

