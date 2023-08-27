function notifyCharaDownload(charaName) {
  const notif = document.createElement("div");
  notif.classList.add("tavernai-notification");

  const title = document.createElement("h2");
  title.innerHTML = "TavernAI Characters";

  const card = document.createElement("p");
  card.innerHTML = "Downloaded: " + charaName;

  const timer = document.createElement("div");
  timer.classList.add("tavernai-notification-timer");

  notif.appendChild(title);
  notif.appendChild(card);
  notif.appendChild(timer);
  document.body.appendChild(notif);

  setTimeout(() => {
    document.body.removeChild(notif);
  }, 3000);
}

const tavernscript = document.createElement("script");

tavernscript.innerHTML = notifyCharaDownload.toString();

document.head.appendChild(tavernscript);
