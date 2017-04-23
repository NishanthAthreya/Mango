$(document).ready()
{
	
/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
	//addSelect('dropdown')
    document.getElementById("myDropdown").classList.toggle("show");
}
function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;          
}

function addSelect(n) {
   console.log(n);
   var newDiv=document.createElement('div');
   var json_obj = JSON.parse(Get('./courses?deptid="' + n + '"'));
   console.log(json_obj);
   var html = '<select>';
   for(i = 0;i < json_obj.length;i++){
	html += '<option value='+json_obj[i][0]+'>'+json_obj[i][1]+'</option>';
	}
   /*for(i = 0; i < dates.length; i++) {
       html += "<option value='"+dates[i]+"'>"+dates[i]+"</option>";
   }*/
   html += '</select>';
   newDiv.innerHTML= html;
   document.getElementById("drop").innerHTML = "";
   document.getElementById("drop").appendChild(newDiv);
   //document.getElementById("drop").classList.toggle("show");
   document.getElementById("drop").classList.add("show");
}

function getDepts() {
   var newDiv=document.createElement('div');
   var json_obj = JSON.parse(Get('./departments'));
   console.log(json_obj);
   var html = '<select onchange="addSelect(this.options[this.selectedIndex].value);">';
   for(i = 0;i < json_obj.length;i++){
	html += '<option value='+json_obj[i][0]+'>'+ json_obj[i][0] + ' '+ json_obj[i][1]+'</option>';
	}
   /*for(i = 0; i < dates.length; i++) {
       html += "<option value='"+dates[i]+"'>"+dates[i]+"</option>";
   }*/
   html += '</select>';
   newDiv.innerHTML= html;
   document.getElementById("depts").appendChild(newDiv);
   document.getElementById("depts").classList.toggle("show");
}


window.onload = getDepts;

function filterFunction() {
	addSelect("dropdown");
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}
}