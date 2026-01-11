const tg = window.Telegram.WebApp;
tg.expand();
const API="https://dr-isroilov-miniapp.onrender.com";

function loadDates(){
 let today=new Date();
 let html="";
 for(let i=0;i<7;i++){
  let d=new Date(today); d.setDate(today.getDate()+i);
  let date=d.toISOString().slice(0,10);
  html+=`<button onclick="loadTimes('${date}')">${date}</button><br>`;
 }
 document.getElementById("content").innerHTML=html;
}

function loadTimes(date){
 fetch(API+"/times/"+date).then(r=>r.json()).then(times=>{
  let html="";
  times.forEach(t=>{ html+=`<button onclick="book('${date}','${t}')">${t}</button>`;});
  document.getElementById("content").innerHTML=html;
 });
}

function book(date,time){
 fetch(API+"/book",{method:"POST",headers:{"Content-Type":"application/json"},
 body:JSON.stringify({uid:tg.initDataUnsafe.user.id,name:tg.initDataUnsafe.user.first_name,date,time})})
 .then(()=>alert("Qabul olindi"));
}