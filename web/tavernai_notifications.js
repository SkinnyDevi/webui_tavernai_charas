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

function dispatchNotifyCharaDownload(charaName) {
  window.dispatchEvent(
    new CustomEvent("notify_chara_download", { detail: { name: charaName } })
  );
}

const tavernscript = document.createElement("script");

tavernscript.innerHTML =
  notifyCharaDownload.toString() +
  dispatchNotifyCharaDownload.toString() +
  `window.addEventListener('notify_chara_download', (evt) => {
		notifyCharaDownload(evt.detail.name)
	})`;

document.head.appendChild(tavernscript);
