import assert from 'node:assert/strict';
import test from 'node:test';
import { MESSUNG, entscheideMessung, seitenaufruf } from '../../assets/messung-logik.js';

const ctx = (over = {}) => ({ gespeichert: null, hostname: 'raindancer118.github.io', ...over });

test('ohne Widerspruch wird gemessen', () => {
  assert.equal(entscheideMessung(ctx()), true);
});

test('Widerspruch (Art. 21 DSGVO) schaltet die Messung ab', () => {
  assert.equal(entscheideMessung(ctx({ gespeichert: MESSUNG.aus })), false);
});

test('fremde Hosts (lokale Vorschau, Forks, Kopien) werden nie gemessen', () => {
  for (const hostname of ['localhost', '127.0.0.1', 'someone-else.github.io']) {
    assert.equal(entscheideMessung(ctx({ hostname })), false, hostname);
  }
});

test('nur "off" gilt als Widerspruch', () => {
  for (const wert of ['', 'on', 'irgendwas']) {
    assert.equal(entscheideMessung(ctx({ gespeichert: wert })), true, wert);
  }
});

test('Seitenaufruf enthaelt ausschliesslich Website, Host, Pfad und Referrer', () => {
  const ort = { hostname: 'raindancer118.github.io', pathname: '/dozenten-sprueche/', search: '?geheim=1', href: 'x' };
  const body = seitenaufruf(ort, 'https://example.com/');
  assert.deepEqual(body, {
    type: 'event',
    payload: {
      website: MESSUNG.websiteId,
      hostname: 'raindancer118.github.io',
      url: '/dozenten-sprueche/',
      referrer: 'https://example.com/',
    },
  });
});

test('fehlender Referrer wird zu leerem String', () => {
  const body = seitenaufruf({ hostname: 'raindancer118.github.io', pathname: '/' }, undefined);
  assert.equal(body.payload.referrer, '');
});
