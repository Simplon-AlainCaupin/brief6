import subprocess
import time

var = 0
while var < 20:              
    bashcommand="curl -F 'vote=Dogs' https://brief6.westus.cloudapp.azure.com/"
    process = subprocess.run(bashcommand, shell=True, stderr=None, stdout=None)
    time.sleep(1)
    bashcommand2="curl -F 'vote=Cats' https://brief6.westus.cloudapp.azure.com/"
    process = subprocess.run(bashcommand2, shell=True, stderr=None, stdout=None)
    time.sleep(2)
    var = var +1
    if var == 20:
      break