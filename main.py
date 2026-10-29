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
body{margin:0;background:#071a35;color:white;font-family:Arial,sans-serif}
header{background:#078fe8;padding:18px 14px;text-align:center}
header h1{margin:0;font-size:23px}
header p{margin:7px 0 0;font-size:13px}
nav{display:flex;gap:8px;padding:12px;overflow:auto;background:#0b294b}
button,.tab{border:0;border-radius:9px;padding:11px 14px;background:#123d65;color:white;font-weight:bold;cursor:pointer}
.tab.active{background:#08a5ff}
main{padding:14px;max-width:850px;margin:auto}
h2{font-size:19px}
.player{background:#000;border-radius:13px;overflow:hidden}
video{width:100%;aspect-ratio:16/9;display:block;background:#000}
#message{padding:12px;font-size:13px;color:#b9e5ff}
.search{width:100%;padding:13px;border-radius:9px;border:1px solid #28618d;background:#0d2d4e;color:white;margin:10px 0}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.channel{background:#10375b;border:1px solid #1b5783;border-radius:12px;padding:14px;text-align:left;color:white;min-height:90px}
.channel strong{display:block;font-size:15px;margin-bottom:8px}
.channel small{color:#b9e5ff}
.badge{color:#ff6262;font-weight:bold;font-size:11px}
footer{text-align:center;padding:25px;color:#9fc7e5;font-size:12px}
.panel{background:#10375b;padding:14px;border-radius:12px;margin-top:14px}
input,select{max-width:100%}
@media(min-width:600px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
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
<video id="video" controls playsinline preload="none"></video>
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
      url: c.url || ""
    }));
    render();
  })
  .catch(error => {
    document.getElementById("channels").textContent =
      "Impossible de charger le catalogue. Vérifie que le serveur fonctionne.";
    console.error(error);
  });
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
 const title=document.createElement("strong");
 title.textContent="📺 "+c.name;
 const country=document.createElement("small");
 country.textContent="🌍 "+c.country;
 const status=document.createElement("div");
 status.className="badge";
 status.textContent=c.url?"LIVE":"FLUX À CONFIGURER";
 b.append(title,country,document.createElement("br"),status);
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
