const POLL_MS = 4000;
let API_BASE = localStorage.getItem('devforge_api_url') || (window.location.protocol.startsWith('http') ? window.location.origin : '');
let currentJobId = null, pollTimer = null, elapsedTimer = null, elapsedSec = 0;
const $ = id => document.getElementById(id);

const STAGES = [
  {id:'ceo',icon:'&#129489;&#8205;&#128188;',name:'CEO<br>Agent'},
  {id:'analysis',icon:'&#128269;',name:'Analysis<br>Agent'},
  {id:'pm',icon:'&#128203;',name:'PM<br>Agent'},
  {id:'coding',icon:'&#9889;',name:'Coding<br>Agents'},
  {id:'qa',icon:'&#129514;',name:'QA<br>Agent'},
  {id:'integration',icon:'&#128279;',name:'Integration<br>Check'},
];

function buildPipeline() {
  const track = $('pipelineTrack'); track.innerHTML = '';
  STAGES.forEach((s,i) => {
    const el = document.createElement('div');
    el.className='stage'; el.id=`stage-${s.id}`;
    el.innerHTML=`<div class="stage-bubble">${s.icon}</div><div class="stage-name">${s.name}</div>`;
    track.appendChild(el);
    if (i < STAGES.length-1) {
      const c = document.createElement('div');
      c.className='stage-connector'; c.id=`conn-${i}`; track.appendChild(c);
    }
  });
}

function setSubtitle(text) {
  const el = $('pipelineSubtitle');
  if (el) el.innerHTML = text;
}

function updatePipeline(status, result) {
  STAGES.forEach(s => { const el = document.getElementById(`stage-${s.id}`); if(el) el.className='stage'; });
  for (let i=0;i<STAGES.length-1;i++) { const c=document.getElementById(`conn-${i}`); if(c) c.className='stage-connector'; }
  if (status==='pending') {
    setSubtitle('&#8987; Initializing multi-agent graph...');
    return;
  }
  let done = getDoneCount(result);
  if (status==='running' && !result) {
    if (elapsedSec < 38) done = 0;
    else if (elapsedSec < 75) done = 1;
    else if (elapsedSec < 220) done = 2;
    else if (elapsedSec < 420) done = 3;
    else if (elapsedSec < 500) done = 4;
    else done = 5;
  }
  for (let i=0;i<done;i++) {
    const el = document.getElementById(`stage-${STAGES[i].id}`);
    if (el) el.className='stage done';
    const c=document.getElementById(`conn-${i}`); if(c) c.className='stage-connector done';
  }
  if (status==='running' && done<STAGES.length) {
    const el = document.getElementById(`stage-${STAGES[done].id}`);
    if (el) el.className='stage active';
    const hints = [
      '&#129489;&#8205;&#128188; <strong>CEO Agent:</strong> Outlining project brief &amp; vision...',
      '&#128269; <strong>Analysis Agent:</strong> Extracting requirements &amp; tech stack...',
      '&#128203; <strong>PM Agent:</strong> Planning tasks, architecture &amp; API contracts...',
      '&#9889; <strong>Coding Agents:</strong> Generating database, backend &amp; frontend in parallel...',
      '&#129514; <strong>QA Agent:</strong> Validating code syntax, quality &amp; test coverage...',
      '&#128279; <strong>Integration Agent:</strong> Assembling codebase &amp; verifying structure...'
    ];
    setSubtitle(hints[done] || 'Agents collaborating in real-time...');
  }
  if (status==='done') {
    for (let i=0;i<STAGES.length;i++) {
      const el = document.getElementById(`stage-${STAGES[i].id}`);
      if (el) el.className='stage done';
      if (i<STAGES.length-1) { const c=document.getElementById(`conn-${i}`); if(c) c.className='stage-connector done'; }
    }
    setSubtitle('&#9989; <strong>All agents finished!</strong> Full codebase generated successfully.');
  }
  if (status==='failed') {
    const fi=Math.max(0,done);
    const el = document.getElementById(`stage-${STAGES[fi].id}`);
    if (el) el.className='stage failed';
    setSubtitle('&#10060; Pipeline execution encountered an error.');
  }
}

function getDoneCount(r) {
  if (!r) return 0;
  let n=0;
  if(r.brief)n=1; if(r.requirements)n=2; if(r.tasks)n=3;
  if(r.generated_code)n=4; if(r.qa_report)n=5; if(r.integration_report)n=6;
  return n;
}

async function apiFetch(path, opts) {
  const r = await fetch(API_BASE.replace(/\/$/,'')+path, {headers:{'Accept':'application/json'},...opts});
  if (!r.ok) { const t=await r.text(); throw new Error(`${r.status}: ${t}`); }
  return r.json();
}
const apiGet  = path => apiFetch(path);
const apiPost = (path,body) => apiFetch(path,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(body)});

async function checkApiStatus() {
  if (!API_BASE) { $('apiStatusBadge').innerHTML='&#9881;&#65039; Not Configured'; $('apiStatusBadge').style.color='var(--amber)'; return false; }
  try {
    await apiGet('/health');
    $('apiStatusBadge').innerHTML='<span class="api-dot"></span>API Connected'; $('apiStatusBadge').style.color='var(--green)'; return true;
  } catch { $('apiStatusBadge').innerHTML='&#9888;&#65039; Unreachable'; $('apiStatusBadge').style.color='var(--amber)'; return false; }
}

async function handleGenerate() {
  const prompt = $('promptInput').value.trim();
  if (!prompt) { showToast('Please describe your project first.','error'); return; }
  if (!API_BASE) { showToast('Configure the API URL first (&#9881;&#65039;)','error'); openSettings(); return; }
  const ok = await checkApiStatus();
  if (!ok) { showToast('Cannot reach the API. Check URL or tunnel.','error'); return; }
  $('generateBtn').disabled=true;
  const ico=$('btnIcon'); ico.style.animation='spin .8s linear infinite'; ico.style.display='inline-block'; ico.textContent='&#8987;';
  try {
    const data = await apiPost('/generate',{user_request:prompt});
    startTracking(data.job_id);
  } catch(e) {
    showToast(`Error: ${e.message}`,'error');
    $('generateBtn').disabled=false; ico.textContent='&#9889;'; ico.style.animation='';
  }
}

function startTracking(jobId) {
  currentJobId=jobId;
  $('heroSection').style.display='none'; $('pipelineSection').style.display='block';
  $('resultsSection').style.display='none'; $('newJobBtn').classList.add('visible');
  buildPipeline(); $('jobIdLabel').textContent=jobId.slice(0,8)+'...';
  updateStatusBadge('pending'); updatePipeline('pending',null);
  elapsedSec=0; $('elapsedLabel').textContent='0s';
  elapsedTimer=setInterval(()=>{
    elapsedSec++;
    $('elapsedLabel').textContent=elapsedSec<60?`${elapsedSec}s`:`${Math.floor(elapsedSec/60)}m ${elapsedSec%60}s`;
    if ($('pipelineSection').style.display !== 'none' && $('resultsSection').style.display === 'none') {
      updatePipeline('running', null);
    }
  },1000);
  $('pollBar').style.display='block'; poll(jobId);
}

async function poll(jobId) {
  try {
    const s=await apiGet(`/status/${jobId}`); updateStatusBadge(s.status);
    if (s.status==='pending'||s.status==='running') {
      try { const p=await apiGet(`/result/${jobId}`); updatePipeline(s.status,p); } catch { updatePipeline(s.status,null); }
      pollTimer=setTimeout(()=>poll(jobId),POLL_MS);
    } else if (s.status==='done') {
      clearInterval(elapsedTimer); $('pollBar').style.display='none';
      const r=await apiGet(`/result/${jobId}`); updatePipeline('done',r); showResults(r); loadHistory();
      showToast('&#127881; Project generated successfully!','success');
    } else if (s.status==='failed') {
      clearInterval(elapsedTimer); $('pollBar').style.display='none';
      try { const r=await apiGet(`/result/${jobId}`); updatePipeline('failed',r); showError(r.error||'Pipeline failed.'); } catch { showError('Pipeline failed.'); }
      showToast('Generation failed.','error');
    }
  } catch(e) { showToast(`Polling error: ${e.message}`,'error'); pollTimer=setTimeout(()=>poll(jobId),POLL_MS*2); }
}

function updateStatusBadge(status) {
  const labels={pending:'&#8987; Pending',running:'&#9889; Running',done:'&#9989; Done',failed:'&#10060; Failed'};
  $('statusBadge').className=`status-badge ${status}`; $('statusBadge').innerHTML=labels[status]||status;
}

function escHtml(s) { if(typeof s!=='string')s=String(s??''); return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function titleCase(s) { return s.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase()); }

function makeCard(title,bodyHtml) {
  const d=document.createElement('div'); d.className='result-card';
  d.innerHTML=`<div class="result-card-header" onclick="this.closest('.result-card').classList.toggle('collapsed')"><div class="result-card-title">${title}</div><span class="chevron">&#9660;</span></div><div class="result-card-body">${bodyHtml}</div>`;
  return d;
}

function showResults(r) {
  $('resultsSection').style.display='block'; $('resultGrid').innerHTML='';
  if(r.brief) $('resultGrid').appendChild(makeCard('&#128221; Project Brief',`<div class="brief-text">${escHtml(r.brief)}</div>`));
  if(r.requirements){
    const req=r.requirements,items=[];
    if(req.project_type)items.push(`Type: ${req.project_type}`);
    if(Array.isArray(req.features))req.features.forEach(f=>items.push(f));
    if(req.tech_stack)Object.entries(req.tech_stack).forEach(([k,v])=>{if(v)items.push(`${k}: ${Array.isArray(v)?v.join(', '):v}`);});
    $('resultGrid').appendChild(makeCard('&#128269; Requirements &amp; Tech Stack',`<div class="chips">${items.map(i=>`<span class="chip">${escHtml(i)}</span>`).join('')}</div>`));
  }
  if(r.generated_code){
    const code=r.generated_code,keys=Object.keys(code).filter(k=>code[k]);
    if(keys.length){
      const tabs=keys.map((k,i)=>`<button class="code-tab ${i===0?'active':''}" data-tab="${k}" onclick="switchTab(this)">${titleCase(k)}</button>`).join('');
      const panels=keys.map((k,i)=>{const content=typeof code[k]==='string'?code[k]:JSON.stringify(code[k],null,2);return `<div class="code-panel ${i===0?'active':''}" data-panel="${k}"><div class="code-block"><button class="copy-btn" onclick="copyCode(this)">Copy</button><code>${escHtml(content)}</code></div></div>`;}).join('');
      $('resultGrid').appendChild(makeCard('&#128187; Generated Code',`<div class="code-tabs">${tabs}</div>${panels}`));
    }
  }
  if(r.qa_report){
    let html='';
    Object.entries(r.qa_report).forEach(([agent,rep])=>{
      const pass=rep&&rep.passed!==false,body=typeof rep==='string'?rep:(rep?.feedback||JSON.stringify(rep));
      html+=`<div style="margin-bottom:14px"><span class="chip ${pass?'tag-pass':'tag-fail'}">${pass?'&#9989;':'&#10060;'} ${titleCase(agent)}</span><div style="font-size:13px;color:var(--text-dim);line-height:1.6;margin-top:8px">${escHtml(body)}</div></div>`;
    });
    $('resultGrid').appendChild(makeCard('&#129514; QA Report',html||'<div style="color:var(--text-muted)">No QA data.</div>'));
  }
  if(r.integration_report){
    const rep=typeof r.integration_report==='string'?r.integration_report:JSON.stringify(r.integration_report,null,2);
    $('resultGrid').appendChild(makeCard('&#128279; Integration Report',`<div class="brief-text">${escHtml(rep)}</div>`));
  }
  if(r.files_written&&r.files_written.length){
    const files=r.files_written.map(f=>`<div class="file-item"><span class="file-icon">&#128196;</span>${escHtml(f)}</div>`).join('');
    $('resultGrid').appendChild(makeCard(`&#128193; Files Written (${r.files_written.length})`,`<div style="margin-bottom:10px;font-size:12px;color:var(--text-muted)">Saved to: <code style="color:var(--cyan)">${escHtml(r.output_folder||'&mdash;')}</code></div><div class="files-list">${files}</div>`));
  }
  $('resultsSection').scrollIntoView({behavior:'smooth',block:'start'});
}

function showError(msg) { $('resultsSection').style.display='block'; $('resultGrid').innerHTML=`<div class="error-box"><strong>&#10060; Generation Failed</strong><br><br>${escHtml(msg)}</div>`; }

function switchTab(btn) {
  const body=btn.closest('.result-card-body');
  body.querySelectorAll('.code-tab').forEach(t=>t.classList.remove('active'));
  body.querySelectorAll('.code-panel').forEach(p=>p.classList.remove('active'));
  btn.classList.add('active'); body.querySelector(`[data-panel="${btn.dataset.tab}"]`)?.classList.add('active');
}
async function copyCode(btn) { try{await navigator.clipboard.writeText(btn.nextElementSibling.textContent);}catch{} btn.textContent='Copied!'; setTimeout(()=>btn.textContent='Copy',2000); }

async function loadHistory() {
  if(!API_BASE) return;
  try {
    const jobs=await apiGet('/jobs'); if(!jobs.length) return;
    $('historySection').style.display='block';
    $('historyBody').innerHTML=jobs.reverse().slice(0,20).map(j=>`<tr>
      <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${escHtml(j.user_request)}">${escHtml(j.user_request.slice(0,80))}${j.user_request.length>80?'...':''}</td>
      <td><span class="status-badge ${j.status}">${j.status}</span></td>
      <td style="color:var(--text-muted);font-family:var(--mono);font-size:12px">${new Date(j.created_at).toLocaleTimeString()}</td>
      <td>${j.status==='done'?`<a class="view-link" onclick="viewJob('${j.job_id}')">View</a>`:''}</td>
    </tr>`).join('');
  } catch {}
}

async function viewJob(jobId) {
  currentJobId=jobId; $('heroSection').style.display='none'; $('pipelineSection').style.display='none';
  $('newJobBtn').classList.add('visible');
  try { const r=await apiGet(`/result/${jobId}`); $('resultsSection').style.display='block'; showResults(r); }
  catch { showToast('Could not load job.','error'); }
}

function openSettings() { $('apiUrlInput').value=API_BASE; $('settingsModal').classList.add('open'); }

async function saveSettings() {
  const url=$('apiUrlInput').value.trim().replace(/\/$/,'');
  if(!url){showToast('Please enter a valid URL.','error');return;}
  API_BASE=url; localStorage.setItem('devforge_api_url',API_BASE); $('settingsModal').classList.remove('open');
  const ok=await checkApiStatus();
  if(ok){showToast('&#9989; API connected!','success'); loadHistory();} else showToast('&#9888;&#65039; Saved but API unreachable.','error');
}

function resetToHome() {
  clearTimeout(pollTimer); clearInterval(elapsedTimer); currentJobId=null;
  $('heroSection').style.display='block'; $('pipelineSection').style.display='none';
  $('resultsSection').style.display='none'; $('newJobBtn').classList.remove('visible');
  $('generateBtn').disabled=false; $('btnIcon').textContent='&#9889;'; $('btnIcon').style.animation='';
  $('promptInput').value=''; $('charCount').textContent='0';
}

function showToast(msg,type='info') {
  const t=document.createElement('div'); t.className=`toast ${type}`; t.innerHTML=msg;
  $('toastContainer').appendChild(t); setTimeout(()=>t.remove(),4000);
}

$('promptInput').addEventListener('input',()=>$('charCount').textContent=$('promptInput').value.length);
$('promptInput').addEventListener('keydown',e=>{if(e.ctrlKey&&e.key==='Enter')handleGenerate();});
$('generateBtn').addEventListener('click',handleGenerate);
$('newJobBtn').addEventListener('click',resetToHome);
$('settingsBtn').addEventListener('click',openSettings);
$('saveSettingsBtn').addEventListener('click',saveSettings);
$('cancelSettingsBtn').addEventListener('click',()=>$('settingsModal').classList.remove('open'));
$('settingsModal').addEventListener('click',e=>{if(e.target===$('settingsModal'))$('settingsModal').classList.remove('open');});

(function(){
  const canvas=$('bgCanvas'),ctx=canvas.getContext('2d');let W,H,particles;
  function resize(){W=canvas.width=innerWidth;H=canvas.height=innerHeight;}
  function rp(){return{x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.5+.3,vx:(Math.random()-.5)*.25,vy:(Math.random()-.5)*.25,alpha:Math.random()*.5+.1,hue:Math.random()>.5?265:190};}
  function init(){resize();particles=Array.from({length:80},rp);}
  function draw(){
    ctx.clearRect(0,0,W,H);
    particles.forEach(p=>{
      p.x+=p.vx;p.y+=p.vy;
      if(p.x<0)p.x=W;if(p.x>W)p.x=0;if(p.y<0)p.y=H;if(p.y>H)p.y=0;
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=`hsla(${p.hue},70%,65%,${p.alpha})`;ctx.fill();
    });requestAnimationFrame(draw);
  }
  window.addEventListener('resize',resize);init();draw();
})();

(async function(){
  if(API_BASE){await checkApiStatus();loadHistory();}
  else{$('apiStatusBadge').innerHTML='&#9881;&#65039; Not Configured';$('apiStatusBadge').style.color='var(--amber)';setTimeout(openSettings,500);}
})();
