from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

PORT = int(__import__("os").environ.get("PORT", "8766"))

HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KIDS TV MONDE LIVE</title>
<style>

*{box-sizing:border-box}
:root{
 --fond:#061326;
 --panneau:#0b2342;
 --carte:#102e52;
 --bleu:#08a9ff;
 --ciel:#8bdcff;
 --texte:#f4f9ff;
 --secondaire:#b6cce5;
}
html{scroll-behavior:smooth}
body{
 margin:0;
 background:radial-gradient(ellipse at top,#123c68 0%,#071a35 48%,#040c19 100%);
 color:var(--texte);
 font-family:Arial,Helvetica,sans-serif;
 min-height:100vh
}
header{
 background:linear-gradient(120deg,#0879cf,#08b7ef);
 padding:24px 16px;
 text-align:center;
 border-bottom:1px solid #72d8ff;
 box-shadow:0 8px 28px #0005
}
header h1{margin:0;font-size:clamp(22px,4vw,34px);letter-spacing:.5px}
header p{margin:9px 0 0;font-size:14px;color:#e5f8ff}
nav{
 display:flex;gap:9px;padding:13px;
 overflow-x:auto;background:#07182c;
 position:sticky;top:0;z-index:5;
 border-bottom:1px solid #21466b;
 scrollbar-width:thin
}
button,.tab{
 border:1px solid #2b5a82;border-radius:12px;
 padding:12px 16px;background:#123454;color:white;
 font-weight:bold;cursor:pointer;transition:background .2s,transform .2s;
 flex-shrink:0
}
button:hover,.tab:hover{background:#185080;transform:translateY(-1px)}
.tab.active{
 background:linear-gradient(135deg,#078fe8,#08baff);
 border-color:#79dcff;box-shadow:0 0 14px #08a9ff35
}
main{padding:18px;max-width:1250px;margin:auto}
h2{font-size:clamp(19px,3vw,25px);margin:18px 0}
.player{
 background:#000;border:1px solid #25517b;
 border-radius:18px;overflow:hidden;
 box-shadow:0 12px 36px #0007
}
video{width:100%;aspect-ratio:16/9;display:block;background:#000;max-height:72vh}
#message{padding:14px;font-size:14px;color:var(--ciel);background:#07182c}
.search{
 width:100%;padding:15px;border-radius:13px;
 border:1px solid #31658f;background:#0b2342;
 color:white;margin:14px 0;font-size:16px;outline:none
}
.search:focus{border-color:var(--bleu);box-shadow:0 0 0 3px #08a9ff25}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.channel{
 background:linear-gradient(145deg,#12375d,#0a203a);
 border:1px solid #244f77;border-radius:15px;padding:16px;
 text-align:left;color:white;min-height:105px;width:100%;
 overflow-wrap:anywhere
}
.channel:hover{border-color:#08baff;box-shadow:0 7px 22px #0004}

.channel-icon{
 display:flex;
 align-items:center;
 justify-content:center;
 width:54px;
 height:54px;
 margin-bottom:12px;
 border-radius:14px;
 background:linear-gradient(135deg,#0879cf,#08b7ef);
 color:white;
 font-size:29px;
 overflow:hidden;
 border:1px solid #72d8ff;
}
.channel-icon img{
 width:100%;
 height:100%;
 object-fit:contain;
 background:#fff;
}
\n.channel strong{display:block;font-size:15px;margin-bottom:10px;line-height:1.4}
.channel small{color:#b9d9f5;line-height:1.5}
.badge{color:#ffd06a;font-weight:bold;font-size:11px;margin-top:8px}
.panel{
 background:linear-gradient(145deg,#10375b,#0b2342);
 border:1px solid #28567d;padding:18px;border-radius:15px;margin-top:14px
}
footer{text-align:center;padding:28px 14px;color:#9fc7e5;font-size:12px}
input,select{max-width:100%}
@media(min-width:650px){
 main{padding:24px}
 .grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:15px}
}
@media(min-width:1000px){
 .grid{grid-template-columns:repeat(4,minmax(0,1fr))}
}
@media(max-width:400px){
 main{padding:10px}
 nav{padding:9px}
 .grid{gap:8px}
 .channel{padding:12px}
}


.player-tools {
  display:flex; flex-wrap:wrap; gap:10px;
  padding:12px; margin-top:10px;
  background:#102b48; border-radius:12px;
}
.player-tools label {
  display:flex; flex-direction:column; gap:5px;
  color:white; font-size:13px;
}
.player-tools select {
  max-width:190px; padding:8px; border-radius:8px;
}


/* === INTERFACE CINEMA STYLE STREAMING === */
body {
 background:#080808 !important;
 color:#fff;
}
header {
 text-align:left !important;
 padding:22px 5% !important;
 background:linear-gradient(90deg,#071b30,#101010 75%) !important;
 border-bottom:1px solid #263b50;
 box-shadow:none;
}
header h1 {
 color:#54c9ff;
 font-size:clamp(25px,4vw,38px);
}
header p {color:#ccc}
nav {
 background:#101010 !important;
 padding:14px 5% !important;
 border-bottom:1px solid #292929;
}
.tab {
 background:#222 !important;
 border:1px solid #444 !important;
 border-radius:7px !important;
}
.tab.active {
 background:#078fe8 !important;
 border-color:#54c9ff !important;
}
main {max-width:1500px;padding:20px 5%}
h2 {font-size:24px;color:#fff}
.player {
 border-radius:12px;
 border:1px solid #333;
}
.search {
 background:#181818;
 border:1px solid #444;
}
.grid {
 display:flex !important;
 gap:14px !important;
 overflow-x:auto;
 overflow-y:hidden;
 padding:12px 2px 22px;
 scroll-snap-type:x mandatory;
 scrollbar-width:thin;
}
.channel {
 flex:0 0 175px;
 width:175px;
 min-height:185px;
 border-radius:10px;
 background:#181818;
 border:1px solid #303030;
 padding:13px;
 scroll-snap-align:start;
 transition:transform .2s,border-color .2s;
}
.channel:hover {
 transform:scale(1.045);
 border-color:#36bfff;
 box-shadow:0 8px 25px #0009;
}
.channel-icon {
 width:100%;
 height:95px;
 border-radius:8px;
 background:linear-gradient(135deg,#073e69,#087fc2);
}
.channel strong {font-size:14px}
.channel small {font-size:12px}
.panel {
 background:#171717;
 border-color:#333;
}
.player-tools {background:#171717}
footer {background:#080808}
.netflix-hero {
 min-height:260px;
 margin:20px auto 28px;
 padding:30px;
 display:flex;
 flex-direction:column;
 justify-content:flex-end;
 align-items:flex-start;
 border-radius:15px;
 background:
 linear-gradient(90deg,#061629 0%,#061629dd 40%,#06162922 100%),
 linear-gradient(135deg,#07538b,#101010 75%);
 border:1px solid #245579;
 box-shadow:0 12px 35px #0008;
}
.netflix-hero .hero-label {
 color:#65d4ff;
 font-weight:bold;
 letter-spacing:2px;
 font-size:12px;
}
.netflix-hero h2 {
 font-size:clamp(27px,5vw,43px);
 margin:12px 0;
}
.netflix-hero p {color:#e0e0e0;max-width:550px}
.netflix-hero button {
 background:#078fe8;
 border:0;
 border-radius:7px;
 padding:13px 24px;
 font-size:15px;
}
@media(min-width:700px) {
 .channel {flex-basis:205px;width:205px}
 .channel-icon {height:115px}
 .netflix-hero {min-height:340px;padding:42px}
}

</style>
</head>
<body>
<header>
<h1>📺 KIDS TV MONDE LIVE</h1>
<p>Le monde des enfants, dans un seul espace !</p>
</header>
<nav>
<button class="tab active" onclick="showCategory('Kids',this)">🧒 Kids</button>
<button class="tab" onclick="showCategory('Éducation',this)">📚 Éducation</button>
<button class="tab" onclick="showCategory('Musique',this)">🎵 Musique</button>
<button class="tab" onclick="showCategory('Actualités',this)">🌍 Actualités</button>
<button class="tab" onclick="showCategory('Documentaires',this)">🌍 Documentaires</button>
<button class="tab" onclick="showCategory('Favoris',this)">⭐ Favoris</button>
<button class="tab" onclick="showCategory('Abonnement',this)">💳 Abonnement</button>
</nav>

<section class="netflix-hero">
 <span class="hero-label">JACKSON NGITUKA TV MONDE</span>
 <h2 id="heroTitle">Bienvenue dans votre télévision mondiale</h2>
 <p id="heroDescription">Découvrez vos chaînes préférées, les programmes éducatifs et les divertissements pour toute la famille.</p>
 <button onclick="playFeatured()">▶ Regarder maintenant</button>
</section>

<main>
<h2 id="heading">🧒 Chaînes pour enfants</h2>
<div class="player">
<video id="video" controls playsinline preload="metadata"></video>
<div class="player-tools">
  <label>Qualité :
    <select id="quality" onchange="changeQuality()">
      <option value="-1">Automatique</option>
    </select>
  </label>
  <label>Audio :
    <select id="audioTrack" onchange="changeAudio()">
      <option value="-1">Automatique</option>
    </select>
  </label>
  <label>Sous-titres :
    <select id="subtitleTrack" onchange="changeSubtitle()">
      <option value="-1">Désactivés / indisponibles</option>
    </select>
  </label>
  <label>Langue :
    <select id="interfaceLanguage" onchange="changeInterfaceLanguage()">
      <option value="fr">Français</option>
      <option value="en">English</option>
      <option value="es">Español</option>
      <option value="pt">Português</option>
    </select>
  </label>
</div>
<div id="message">Choisis une chaîne disposant d'un flux vidéo autorisé pour commencer.</div>
<div id="networkStatus" style="padding:10px 14px;background:#102b48;color:#8bdcff;font-size:13px">📶 Analyse de la connexion...</div>
</div>
<input id="search" class="search" placeholder="🔎 Rechercher une chaîne..." oninput="render()">
<div id="channels" class="grid"></div>
<div id="subscription" class="panel" hidden>
<h2>💳 Abonnement</h2>
<p>Tarif : <strong>2 000 FC pour 60 jours</strong>.</p>
<p>Les paiements Airtel Money, M-Pesa et Orange Money seront intégrés après obtention des accès marchands et de l'API officielle.</p>
<p>Ne communique jamais ton code PIN mobile money sur ce site.</p>
<p>Le paiement n'est pas encore activé. Aucun abonnement payant ne peut être confirmé ici.</p>
</div>
</main>
<footer>KIDS TV MONDE LIVE · Version de test locale</footer>
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<script>
let channels = [];

function updateFeatured(){
 const c = channels.find(x => x.url) || channels[0];
 if(!c) return;
 window.featuredChannel = c;
 document.getElementById("heroTitle").textContent = c.name;
 document.getElementById("heroDescription").textContent =
   "📺 " + c.country + " · " + c.category +
   " — Découvrez cette chaîne dans JACKSON NGITUKA TV MONDE.";
}
function playFeatured(){
 if(window.featuredChannel) play(window.featuredChannel);
 else document.getElementById("message").textContent =
   "Le catalogue est encore en cours de chargement.";
}


fetch("/chaines.json")
  .then(response => {
    if (!response.ok) throw new Error("Catalogue indisponible");
    return response.json();
  })
  .then(data => {
    channels = data.map(c => ({
      name: c.nom,
      country: c.pays,
      category: c.categorie,
      url: c.url || "",
      logo: c.logo || ""
    }));
    render();
    updateFeatured();
  })
  .catch(error => {
    document.getElementById("channels").textContent =
      "Impossible de charger le catalogue. Vérifie que le serveur fonctionne.";
    console.error(error);
  });

function changeQuality(){
  const h = window.currentHls;
  const select = document.getElementById("quality");
  if (!h || !select) return;

  const level = Number(select.value);
  h.currentLevel = level;

  document.getElementById("message").textContent =
    level === -1
      ? "Qualité automatique activée."
      : "Qualité sélectionnée : " +
        (h.levels[level]?.height || "résolution inconnue") + "p.";
}

function changeAudio(){
  const h = window.currentHls;
  const select = document.getElementById("audioTrack");
  if (h && select && h.audioTracks.length)
    h.audioTrack = Number(select.value);
}

function changeSubtitle(){
  const h = window.currentHls;
  const select = document.getElementById("subtitleTrack");
  if (h && select) {
    h.subtitleTrack = Number(select.value);
    h.subtitleDisplay = Number(select.value) !== -1;
  }
}

function loadPlayerTracks(h){
  const q = document.getElementById("quality");
  const a = document.getElementById("audioTrack");
  const st = document.getElementById("subtitleTrack");

  q.innerHTML = '<option value="-1">Automatique</option>';
  a.innerHTML = '<option value="-1">Automatique</option>';
  st.innerHTML = '<option value="-1">Désactivés / indisponibles</option>';

  const levels = h.levels || [];
  const seen = new Set();

  levels.forEach((level, i) => {
    const height = Number(level.height || 0);
    const bitrate = Number(level.bitrate || 0);
    const label = height
      ? height + "p" + (bitrate ? " — " + Math.round(bitrate / 1000) + " kb/s" : "")
      : "Qualité " + (i + 1);

    const option = document.createElement("option");
    option.value = String(i);
    option.textContent = label;
    q.appendChild(option);
    seen.add(height);
  });

  if (levels.length > 1) {
    const info = document.createElement("option");
    info.disabled = true;
    info.textContent = "Choisis une qualité disponible ci-dessus";
    q.appendChild(info);
  }

  (h.audioTracks || []).forEach((track, i) => {
    const option = document.createElement("option");
    option.value = String(i);
    option.textContent = track.name || track.lang || ("Audio " + (i + 1));
    a.appendChild(option);
  });

  (h.subtitleTracks || []).forEach((track, i) => {
    const option = document.createElement("option");
    option.value = String(i);
    option.textContent = track.name || track.lang || ("Sous-titre " + (i + 1));
    st.appendChild(option);
  });
}

function changeInterfaceLanguage(){
  const lang=document.getElementById("interfaceLanguage").value;
  localStorage.setItem("jack_language",lang);
  const messages={
    fr:"Choisis une chaîne pour commencer.",
    en:"Choose a channel to start.",
    es:"Elige un canal para comenzar.",
    pt:"Escolhe um canal para começar."
  };
  document.documentElement.lang=lang;
  document.getElementById("message").textContent=messages[lang];
}
function initPlayerLanguage(){
  const saved=localStorage.getItem("jack_language")||"fr";
  const select=document.getElementById("interfaceLanguage");
  if(select) select.value=saved;
  document.documentElement.lang=saved;
}

let current="Kids";
let favorites=JSON.parse(localStorage.getItem("jack_favorites")||"[]");
function showCategory(cat,button){
 current=cat;
 document.querySelectorAll(".tab").forEach(b=>b.classList.remove("active"));
 if(button)button.classList.add("active");
 document.getElementById("heading").textContent=cat==="Abonnement"?"💳 Mon abonnement":cat==="Favoris"?"⭐ Mes favoris":"📺 "+cat;
 document.getElementById("subscription").hidden=cat!=="Abonnement";
 document.getElementById("search").hidden=cat==="Abonnement";
 document.getElementById("channels").hidden=cat==="Abonnement";
 render();
}
function render(){
 const box=document.getElementById("channels");
 box.innerHTML="";
 const term=document.getElementById("search").value.toLowerCase();
 channels.filter(c=>(current==="Favoris"?favorites.includes(c.name):c.category===current)&&
 (c.name+" "+c.country).toLowerCase().includes(term)).forEach(c=>{
 const b=document.createElement("button");
 b.className="channel";
 const icon=document.createElement("div");
 icon.className="channel-icon";

 const icons={
   "Kids":"🧒",
   "Éducation":"📚",
   "Musique":"🎵",
   "Actualités":"📰",
   "Documentaires":"🌍"
 };

 const showFallbackLogo=()=>{
   icon.innerHTML="";
   const name=(c.name||"TV").trim();
   const words=name.split(/\\s+/).filter(Boolean);
   const initials=words.length>1
     ? words.slice(0,2).map(w=>w[0]).join("").toUpperCase()
     : name.slice(0,2).toUpperCase();

   let hash=0;
   for(let i=0;i<name.length;i++){
     hash=(hash*31+name.charCodeAt(i))>>>0;
   }

   const badge=document.createElement("div");
   badge.textContent=initials||"TV";
   badge.style.cssText=
     "width:100%;height:100%;display:flex;align-items:center;"+
     "justify-content:center;color:white;font-size:19px;"+
     "font-weight:900;border-radius:12px;text-shadow:0 2px 4px #000;"+
     "background:linear-gradient(135deg,hsl("+
     (hash%360)+",75%,42%),hsl("+((hash+65)%360)+",80%,25%))";
   icon.appendChild(badge);
 };

 if(c.logo){
   const img=document.createElement("img");
   img.src=c.logo;
   img.alt=c.name;
   img.loading="lazy";
   img.onerror=showFallbackLogo;
   icon.appendChild(img);
 }else{
   showFallbackLogo();
 }

 const title=document.createElement("strong");
 title.textContent=c.name;
 const country=document.createElement("small");
 country.textContent="🌍 "+c.country;
 const status=document.createElement("div");
 status.className="badge";
 status.textContent=c.url?"LIVE":"FLUX À CONFIGURER";
 b.append(icon,title,country,document.createElement("br"),status);
 b.onclick=()=>play(c);
 const fav=document.createElement("span");
 fav.textContent=favorites.includes(c.name)?" ★":" ☆";
 fav.style.float="right";
 fav.style.cursor="pointer";
 fav.onclick=e=>{
 e.stopPropagation();
 favorites=favorites.includes(c.name)?favorites.filter(n=>n!==c.name):[...favorites,c.name];
 localStorage.setItem("jack_favorites",JSON.stringify(favorites));
 render();
 };
 b.append(fav);
 box.appendChild(b);
 });
 if(!box.children.length&&current!=="Abonnement")box.textContent="Aucune chaîne dans cette catégorie pour le moment.";
}

// === GESTION INTELLIGENTE DU RESEAU ===

function networkProfile(){
 const c=navigator.connection ||
        navigator.mozConnection ||
        navigator.webkitConnection;

 if(!c) return {
   type:"inconnu",
   speed:0,
   save:false,
   maxHeight:720
 };

 const speed=Number(c.downlink||0);
 const effective=c.effectiveType||"";
 const save=!!c.saveData;
 const type=c.type||"inconnu";

 let maxHeight=1080;

 if(save || effective==="slow-2g" || effective==="2g" ||
    (speed>0 && speed<0.7)){
   maxHeight=360;
 }else if(effective==="3g" || (speed>0 && speed<1.5)){
   maxHeight=480;
 }else if(speed>0 && speed<3){
   maxHeight=720;
 }

 return {type,speed,save,maxHeight};
}

function showNetworkStatus(){
 const n=networkProfile();
 const box=document.getElementById("networkStatus");
 if(!box) return;

 let type="Connexion non identifiée";
 if(n.type==="wifi") type="Wi-Fi";
 if(n.type==="cellular") type="Réseau mobile";

 let speed=n.speed ? " · Débit estimé "+n.speed+" Mb/s" : "";
 box.textContent="📶 "+type+speed+
   " · Qualité maximale conseillée : "+n.maxHeight+"p"+
   " · VPN : non vérifiable";
}

function adaptPlayerNetwork(hls){
 if(!hls || !hls.levels || !hls.levels.length) return;

 const profile=networkProfile();
 const allowed=hls.levels
   .map((level,index)=>({index,height:Number(level.height||0)}))
   .filter(level=>!level.height || level.height<=profile.maxHeight);

 hls.autoLevelCapping=allowed.length
   ? allowed[allowed.length-1].index
   : 0;

 hls.startLevel=-1;
 hls.currentLevel=-1;

 showNetworkStatus();
}

function activateNetworkMonitor(){
 const c=navigator.connection ||
        navigator.mozConnection ||
        navigator.webkitConnection;

 showNetworkStatus();

 if(c){
   c.addEventListener("change",()=>{
     showNetworkStatus();
     if(window.currentHls){
       adaptPlayerNetwork(window.currentHls);
     }
   });
 }
}

window.addEventListener("online",()=>{
 const h=window.currentHls;
 if(h){
   h.startLoad();
   document.getElementById("message").textContent=
     "Connexion rétablie. Reprise du flux...";
 }
 showNetworkStatus();
});

window.addEventListener("offline",()=>{
 document.getElementById("message").textContent=
   "Connexion interrompue. En attente du retour d'Internet...";
});


function play(c){
 const video=document.getElementById("video");
 document.getElementById("message").textContent="Chargement : "+c.name;
 if(window.currentHls){
   window.currentHls.destroy();
   window.currentHls=null;
 }
 video.pause();
 video.removeAttribute("src");
 video.load();

 if(!c.url){
   document.getElementById("message").textContent="Le flux officiel de cette chaîne reste à configurer.";
   return;
 }

 if(window.Hls && Hls.isSupported()){
   const hls=new Hls({
     enableWorker:true,
     lowLatencyMode:false,

     // Tampon pour stabiliser la lecture
     maxBufferLength:35,
     maxMaxBufferLength:90,
     backBufferLength:30,
     maxBufferSize:60*1000*1000,

     // Reconnexion automatique
     manifestLoadingMaxRetry:5,
     manifestLoadingRetryDelay:1000,
     levelLoadingMaxRetry:6,
     levelLoadingRetryDelay:1000,
     fragLoadingMaxRetry:8,
     fragLoadingRetryDelay:1000,
     fragLoadingMaxRetryTimeout:64000,

     // Adaptation automatique
     startLevel:-1,
     capLevelToPlayerSize:true,
     abrEwmaDefaultEstimate:1000000
   });
   window.currentHls=hls;
   hls.loadSource(c.url);
   hls.attachMedia(video);
   hls.on(Hls.Events.MANIFEST_PARSED,()=>{
     adaptPlayerNetwork(hls);
     loadPlayerTracks(hls);
     document.getElementById("message").textContent="Lecture : "+c.name;
     video.play().catch(()=> {
       document.getElementById("message").textContent="Appuie sur Lecture pour démarrer.";
     });
   });
   let recoveries=0;
   hls.on(Hls.Events.FRAG_BUFFERED,()=>{
     recoveries=0;
   });
   hls.on(Hls.Events.ERROR,(event,data)=>{
     if(!data.fatal) return;

     if(data.type===Hls.ErrorTypes.NETWORK_ERROR && recoveries<8){
       recoveries++;
       document.getElementById("message").textContent=
         "Connexion instable. Nouvelle tentative "+recoveries+"/8...";
       setTimeout(()=>hls.startLoad(),1500);
     }else if(data.type===Hls.ErrorTypes.MEDIA_ERROR && recoveries<8){
       recoveries++;
       document.getElementById("message").textContent=
         "Réparation du lecteur vidéo...";
       hls.recoverMediaError();
     }else{
       document.getElementById("message").textContent=
         "Flux indisponible. Vérifie ta connexion ou essaie une autre chaîne.";
       hls.destroy();
       window.currentHls=null;
     }
   });
 }else if(video.canPlayType("application/vnd.apple.mpegurl")){
   video.src=c.url;
   video.play().catch(()=>{
     document.getElementById("message").textContent="Appuie sur Lecture pour démarrer.";
   });
 }else{
   document.getElementById("message").textContent="Ce navigateur ne prend pas en charge ce format.";
 }
}

initPlayerLanguage();
activateNetworkMonitor();
render();
</script>
</body>
</html>"""

class JacksonHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            body = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/chaines.json":
            try:
                with open("chaines.json", "rb") as fichier:
                    body = fichier.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except OSError:
                self.send_error(500, "Catalogue indisponible")
        elif path == "/health":
            body = json.dumps({"status": "ok", "app": "KIDS TV MONDE LIVE"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, "Page introuvable")

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), JacksonHandler)
    print("=" * 40)
    print(" KIDS TV MONDE LIVE")
    print("=" * 40)
    print("Ouvre Chrome sur : http://127.0.0.1:8766")
    print("Pour arrêter le serveur : CTRL+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServeur arrêté.")
        server.server_close()
