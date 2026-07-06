#!/usr/bin/env node
/* Cifra calc-src.html → calc.html usando la plantilla wrapper.html.
   Uso: node tools/encrypt.js "<clave>"
   La clave NO queda en ningún archivo; se comparte por canal privado. */
const fs = require("fs");
const path = require("path");
const { webcrypto: crypto } = require("crypto");

(async () => {
  const pass = process.argv[2];
  if (!pass) { console.error('Uso: node tools/encrypt.js "<clave>"'); process.exit(1); }

  const root = path.join(__dirname, "..");
  const src = fs.readFileSync(path.join(root, "calc-src.html"), "utf8");
  const template = fs.readFileSync(path.join(__dirname, "wrapper.html"), "utf8");

  const enc = new TextEncoder();
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const iter = 600000;

  const km = await crypto.subtle.importKey("raw", enc.encode(pass), "PBKDF2", false, ["deriveKey"]);
  const key = await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: iter, hash: "SHA-256" },
    km, { name: "AES-GCM", length: 256 }, false, ["encrypt"]);
  const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, enc.encode(src)));

  const b64 = (u) => Buffer.from(u).toString("base64");
  const payload = JSON.stringify({ salt: b64(salt), iv: b64(iv), iter, ct: b64(ct) });

  const out = template.replace("__PAYLOAD__", payload);
  fs.writeFileSync(path.join(root, "calc.html"), out);
  console.log("OK → calc.html cifrado (" + ct.length + " bytes de contenido)");
})();
