const modal =
document.getElementById("logModal");

document.getElementById("openModal")
.addEventListener("click", () => {
modal.classList.add("show");
});

const logs = [];

function addLog(){

const username =
document.getElementById("userName").value;

const patientId =
document.getElementById("patientId").value;

const role =
document.getElementById("role").value;

const action =
document.getElementById("action").value;

if(username === "" || patientId === ""){
alert("Fill all fields");
return;
}

const newLog = {
id : Math.floor(Math.random()*10000),
username,
patientId,
role,
action,
status:"Authorized"
};

logs.push(newLog);

renderTable();

modal.classList.remove("show");
}

function renderTable(){

const table =
document.getElementById("logsTable");

table.innerHTML = "";

logs.forEach(log => {

table.innerHTML += `
<tr>
<td>${log.id}</td>
<td>${log.username}</td>
<td>${log.patientId}</td>
<td>${log.role}</td>
<td>${log.action}</td>
<td style="color:#22c55e">
${log.status}
</td>
</tr>
`;

});

}

const ctx =
document.getElementById("myChart");

new Chart(ctx,{

type:"line",

data:{
labels:[
"Mon","Tue","Wed",
"Thu","Fri","Sat","Sun"
],

datasets:[{

label:"Access Requests",

data:[
120,
190,
150,
220,
260,
300,
280
],

borderColor:"#38bdf8",

backgroundColor:
"rgba(56,189,248,.2)",

fill:true,

tension:.4

}]
},

options:{
responsive:true
}

});
function scrollToLogs() {
    const logSection = document.querySelector(".logSection");

    if(logSection){
        logSection.scrollIntoView({
            behavior: "smooth"
        });
    }
}
document.getElementById("logsBtn")
.addEventListener("click", function(){

    const logSection =
    document.querySelector(".logSection");

    if(logSection){
        logSection.scrollIntoView({
            behavior: "smooth"
        });
    }

});
