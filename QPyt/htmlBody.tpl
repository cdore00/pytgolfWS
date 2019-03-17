<body onload="listItems()">
  <div class="divCenter">
<h1>rec. GPS</h1>
<span id="mess"></span>

<form action="/start" method="GET">
  <div class="divLeft">
  <h2>Login</h2>
  <input type="text" size="20" maxlength="100" name="user" value="$defaultUser"></br>
  <input type="password" size="20" maxlength="100" name="passw"></br>

 <h3>Options</h3>
  <label for="tdelay">Loc.<input id="tdelay" type="text" size="2" maxlength="2" name="delay" value="%d"></label><label for="tfreq"> Freq.<input id="tfreq" type="text" size="3" maxlength="4" name="frequence" value="%d"></label> Second</br>
  <label for="minDist">Min:Dist.<input id="minDist" type="text" size="2" maxlength="2" name="minDist" value="%d"></label><label for="minAcc"> Acc.<input id="minAcc" type="text" size="3" maxlength="4" name="minAcc" value="%d"></label> Yard</br>
  
<label for="optToast"><input id="optToast" type="checkbox" name="optToast" %s value="toast">Show toast</input></label>
<label for="optNotify"><input id="optNotify" type="checkbox" name="optNotify" %s value="notify">Show notify</input></label>

  <h3>Server</h3>
  $optionList
<div class="divCenter">
    <input class="but" type="submit" name="save" value="Start"><input class="but" type="submit" name="cancel" onclick="close()" value="Cancel">
  </div>
  </div>
</form>

  </div>
</body>