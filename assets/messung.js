import { MESSUNG, entscheideMessung, seitenaufruf } from './messung-logik.js';

/* Der Speicher hält nur einen Widerspruch fest (§ 25 Abs. 2 Nr. 2 TDDDG). */
const speicher = {
  lesen() {
    try { return localStorage.getItem(MESSUNG.storageKey); } catch { return null; }
  },
  schreiben(aus) {
    try {
      if (aus) localStorage.setItem(MESSUNG.storageKey, MESSUNG.aus);
      else localStorage.removeItem(MESSUNG.storageKey);
    } catch { /* ohne Speicher gilt die Wahl nur für diesen Aufruf */ }
  },
};

if (entscheideMessung({ gespeichert: speicher.lesen(), hostname: location.hostname })) {
  fetch(MESSUNG.collectUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(seitenaufruf(location, document.referrer)),
    keepalive: true,
    mode: 'cors',
    credentials: 'omit',
    cache: 'no-store',
  }).catch(() => { /* Messung darf die Seite nie stören */ });
}

const schalter = document.querySelector('[data-messung-schalter]');
if (schalter) {
  const status = document.querySelector('[data-messung-status]');
  const anzeigen = () => {
    const aus = speicher.lesen() === MESSUNG.aus;
    schalter.checked = !aus;
    status.textContent = aus ? 'Aus – dein Widerspruch ist gespeichert.' : 'An – Seitenaufrufe werden gezählt.';
  };
  schalter.addEventListener('change', () => { speicher.schreiben(!schalter.checked); anzeigen(); });
  anzeigen();
}
