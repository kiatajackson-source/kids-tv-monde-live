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

 if(c.logo){
   const img=document.createElement("img");
   img.src=c.logo;
   img.alt="";
   img.loading="lazy";
   img.onerror=()=>{icon.textContent=icons[c.category]||"📺";};
   icon.appendChild(img);
 }else{
   icon.textContent=icons[c.category]||"📺";
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
     maxBufferLength:20
   });
   window.currentHls=hls;
   hls.loadSource(c.url);
   hls.attachMedia(video);
   hls.on(Hls.Events.MANIFEST_PARSED,()=>{
     loadPlayerTracks(hls);
     document.getElementById("message").textContent="Lecture : "+c.name;
     video.play().catch(()=> {
       document.getElementById("message").textContent="Appuie sur Lecture pour démarrer.";
     });
   });
   hls.on(Hls.Events.ERROR,(event,data)=>{
     if(data.fatal){
       document.getElementById("message").textContent="Lecture impossible. Vérifie Internet et le flux vidéo.";
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
