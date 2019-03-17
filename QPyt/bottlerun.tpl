<html>
<head> 
<meta charset="UTF-8">
<meta name="viewport" id="viewport"
 content="width=device-width, target-densitydpi=device-dpi,
 initial-scale=1.0, maximum-scale=2.0, minimum-scale=1.0"/>

<style>
.divCenter{
text-align: center;
display: block;
width:100%;
}
.divLeft{
text-align: left;
display: inline-block;
overflow-x: inherit
}
#mess{
color: red;
}
.viewCtl{
    width: 20px;
    border: buttonhighlight 2px outset;
    background: #eee;
    text-decoration: none;
    display: inline-block;
    text-align: center;
	margin-right: 10px;
}
#state{
height: 20px !important;
border: 0px !important;
margin-left: 5px;
margin-bottom: 15px;
}
#locState{
font-weight: bold;
font-size: larger;
}
.listitem {
    display: block;
    overflow: auto;
    padding: 0px 0px 2px 5px;
    border: 1px solid #333;
	padding-right: 10px;
	height: 1.3em;
	transition: height 0.4s ease-in-out;
	width: 100%;
}
#listData{
padding-left: 0px;
}
.mess{
color: red;
}
.but {
    width: 8em;
    margin: 10px;
}

</style>

<script type="text/javascript"> 
<!--
var dat = $action ;

//var dat = [1, [],[]]
//[{"run":1}, [{'bearing': 0, 'altitude': 118, 'provider': 'gps', 'sent':1, 'dist':122.5, 'longitude': -71.229320759999993, 'time': 1552279052000, 'latitude': 46.803383169999996, 'speed': 0, 'accuracy': 28.822999954223633}, {'bearing': 0, 'altitude': 106, 'provider': 'gps', 'longitude': -71.229327190000006, 'time': 1552279072000, 'latitude': 46.803414740000001, 'speed': 0, 'accuracy': 36.407997131347656}, {'bearing': 0, 'altitude': 105, 'provider': 'gps', 'longitude': -71.229333609999998, 'time': 1552279082000, 'latitude': 46.803432100000002, 'speed': 0, 'accuracy': 43.993000030517578}, {'bearing': 0, 'altitude': 106, 'provider': 'gps', 'longitude': -71.229337099999995, 'time': 1552279093000, 'latitude': 46.80343697, 'speed': 0, 'accuracy': 37.924999237060547}, {'bearing': 0, 'altitude': 104, 'provider': 'gps', 'longitude': -71.229331790000003, 'time': 1552279104000, 'latitude': 46.803439650000001, 'speed': 0, 'accuracy': 42.475997924804688}, {'bearing': 0, 'altitude': 104, 'provider': 'gps', 'longitude': -71.229335419999998, 'time': 1552279113000, 'latitude': 46.803443989999998, 'speed': 0, 'accuracy': 31.856998443603516}, {'bearing': 0, 'altitude': 105, 'provider': 'gps', 'longitude': -71.229342919999993, 'time': 1552279124000, 'latitude': 46.803447179999999, 'speed': 0, 'accuracy': 56.128997802734375}], ["Erreur1"]];

function showAll(oLi){
var x = document.getElementsByClassName("viewCtl");
if (oLi.innerHTML == "+"){
	oLi.innerHTML = "-";
}else{
	oLi.innerHTML = "+";
}
	for(var i = 0; i < x.length ; i++){
		if (x.id != "ctlAll")
			showdat(x[i]);
	}
}

function showdat(oLi){
if (oLi.innerHTML == "+"){
	oLi.innerHTML = "-";
	oLi.parentElement.style.height = "4em";
}else{
	oLi.innerHTML = "+";
	oLi.parentElement.style.height = "1.3em";
}
}

function listItems(){
//alert(dat[0].run)
var mess = document.getElementById('mess');
var message = ""
if (dat[2].length > 0)
	for(var i = dat[2].length - 1; i > -1 ; i--){
		message += dat[2][i] + '</br>'
		mess.innerHTML = message + '</br>';
	}
var locState = document.getElementById('locState');
if (dat[0].run == 1 && dat[1].length == 0){
	locState.innerHTML = "Start locating...";
	setTimeout(function(){ document.getElementById('butRefresh').click() }, 3000);
}else{
	if (dat[0].run == 0){
		locState.innerHTML = "Locating stopping...";
			setTimeout(function(){ document.getElementById('butRefresh').click() }, 3000);
	}
	if (dat[0].run == 1)
		locState.innerHTML = "Locating running...";
	if (dat[0].run == 2){
		locState.innerHTML = "Location stopped.";
			//setTimeout(function(){ document.getElementById('butRefresh').click() }, 2000);
    }
}
//locState.innerHTML += (message == "") ? "":" (ERROR!)"
var listData = document.getElementById('listData');
for(var i = dat[1].length - 1; i > -1 ; i--){
	strClass = 'listitem'
	if (dat[1][i].sent && dat[1][i].sent > 0)
		strClass += " mess"
	var liElem = document.createElement("li");
	liElem.setAttribute('class', strClass);
	liElem.innerHTML = '<a href="#" class="viewCtl" onclick="showdat(this)">+</a>' + (i+1) + '- ' + (new Date(dat[1][i].time)).toLocaleString("en-CA") 
		+ '</br>&#8239;&#8239;Alt.: ' + dat[1][i].altitude + '&#8239;&#8239;Acc.: ' + Math.round(dat[1][i].accuracy) 
		+ ((dat[1][i].dist) ? '&#8239;&#8239;Dist.: ' + Math.round(dat[1][i].dist) + '</br> ':'</br> ') + dat[1][i].latitude + ', ' + dat[1][i].longitude;
	listData.appendChild(liElem);
}
}
// -->
</script>

</head>     
<body onload="listItems()">
  <div class="divCenter">
<h1>Rec. GPS</h1>
<span id="mess" class="mess"></span>
<form action="/stop" method="GET">
    <input id="butStop" class="but" type="submit" name="stop" value="Stop location"></br>
	<input id="butView" class="but" type="submit" name="view" value="View locations"></br>
	<input id="butStart" class="but" type="submit" name="start" value="Start options"></br>
	<input id="butRefresh" class="but" type="submit" name="refresh" value="Refresh display"></br>
<div class="divLeft">

<div >
<ul id="listData">
<li id="state">
<a id="ctlAll" href="#" class="viewCtl" onclick="showAll(this)">+</a><span id="locState"></span>
</li>
</ul>
</div>

  </div>
</form>
  </div>
</body>
</html>