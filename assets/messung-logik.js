/* Reichweitenmessung mit dem selbst gehosteten Umami (analytics.tstieh.de).
   Bewusst nicht Umamis script.js, sondern ein Minimal-Sender: übertragen werden
   nur Pfad und Referrer, aus dem Endgerät wird nichts gelesen. Damit greift
   § 25 TDDDG nicht, ein Banner ist unnötig; Rechtsgrundlage Art. 6 Abs. 1 lit. f
   DSGVO. Logik ohne DOM und Netzwerk, damit sie testbar bleibt. */

export const MESSUNG = {
  collectUrl: 'https://analytics.tstieh.de/api/send',
  websiteId: 'c118e4e9-db39-482d-8efb-79386af1d73c',
  hosts: ['raindancer118.github.io'],
  storageKey: 'ludolph-messung',
  aus: 'off',
};

export function entscheideMessung({ gespeichert, hostname }) {
  if (!MESSUNG.hosts.includes(hostname)) return false;
  return gespeichert !== MESSUNG.aus;
}

export function seitenaufruf(ort, referrer) {
  return {
    type: 'event',
    payload: {
      website: MESSUNG.websiteId,
      hostname: ort.hostname,
      url: ort.pathname,
      referrer: referrer || '',
    },
  };
}
