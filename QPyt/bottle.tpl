<html>
<head> 
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
background: #ddd;
}
.but{
width: 5em;
margin: 10px;
}
#mess{
color: red;
}

h2{
margin-top: -1em;
}

input[type='radio']{
width: 50%;
transform: scale(2);
font-size: 1.5em;
}


</style>

<script type="text/javascript"> 
<!--
var dat = $action ;

function close(){
window.close();
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
}
// -->
</script>


</head>     

&HTMLbody

</html>