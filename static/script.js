function showTab(id){
  document.querySelectorAll('.panel').forEach(x=>x.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  event.target.classList.add('active');
}
function money(n){return "₹"+Number(n).toLocaleString("en-IN",{maximumFractionDigits:2})}

async function checkLoan(){
  const r=await fetch("/api/check-loan",{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify({age:age.value,income:income.value,credit_score:creditScore.value,loan_amount:loanAmount.value,employment:employment.value})});
  const d=await r.json(); const box=document.getElementById("loanResult");
  box.className="result "+(d.eligible?"good":"warn");
  box.innerHTML=`<b>${d.eligible?"Likely Eligible":"Needs Review"}</b><br>Demo score: ${d.score}/100<br>${d.message}`;
}
async function calculateEMI(){
  const r=await fetch("/api/emi",{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify({amount:emiAmount.value,rate:emiRate.value,years:emiYears.value})});
  const d=await r.json(); const box=document.getElementById("emiResult");
  box.className="result"; box.innerHTML=`<b>Monthly EMI: ${money(d.emi)}</b><br>Total Payment: ${money(d.total)}<br>Total Interest: ${money(d.interest)}`;
}
async function analyzeCredit(){
  const r=await fetch("/api/credit/"+scoreInput.value); const d=await r.json();
  const box=document.getElementById("creditResult"); box.className="result";
  box.innerHTML=`<b>${d.category}</b> — Score ${d.score}/900<br>${d.tip}`;
}
async function getTips(){
  const r=await fetch("/api/ai-tips",{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify({question:question.value})});
  const d=await r.json(); const box=document.getElementById("aiResult");
  box.className="result"; box.textContent=d.answer;
}
