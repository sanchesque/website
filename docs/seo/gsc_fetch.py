#!/usr/bin/env python3
"""Consulta la API de Google Search Console para sanchesque.com y guarda
los JSON con fecha en docs/seo/gsc-AAAA-MM-DD/.

Subsesión «Sanchesque.com · SEO». Uso:

    ~/.venvs/gsc/bin/python website/docs/seo/gsc_fetch.py

La credencial NO es una API key suelta: Search Console exige OAuth2 o una
cuenta de servicio. Se lee de dos sitios, en este orden:

1. Variable de entorno GSC_SA_FILE: ruta a un JSON de cuenta de servicio
   (fuera del repo, p. ej. ~/.secrets/gsc-sa.json con chmod 600).
2. Llavero del Mac, item "gsc-service-account" (el contenido es el JSON):

       security add-generic-password -s gsc-service-account -a alex \
         -w "$(cat ~/Downloads/sa-sanchesque.json)"

La cuenta de servicio debe estar añadida como propietaria de la
propiedad https://sanchesque.com/ en Search Console (Ajustes › Usuarios y
permisos). La key nunca se imprime ni se guarda en disco desde aquí.

Solo lectura: scope webmasters.readonly. Librerías en ~/.venvs/gsc
(instaladas con el sí de Alex el 25-nov-2026).
"""
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

# Propiedad de dominio de Search Console (sc-domain:), no la URL prefijo
SITE = "sc-domain:sanchesque.com"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
OUT = Path(__file__).resolve().parent / f"gsc-{date.today().isoformat()}"
KEYCHAIN_ITEM = "gsc-service-account"


def load_credentials():
    from google.oauth2 import service_account
    env = os.environ.get("GSC_SA_FILE")
    if env and Path(env).exists():
        return service_account.Credentials.from_service_account_file(env, scopes=SCOPES)
    out = subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_ITEM, "-w"],
                         capture_output=True, text=True)
    if out.returncode == 0 and out.stdout.strip():
        info = json.loads(out.stdout)
        return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    sys.exit("sin credencial: define GSC_SA_FILE o crea el item de llavero "
             f"'{KEYCHAIN_ITEM}' con el JSON de la cuenta de servicio")


def main():
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    creds = load_credentials()
    service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    try:
        sitemaps = service.sitemaps().list(siteUrl=SITE).execute()
    except HttpError as e:
        if e.resp.status == 403:
            email = creds.service_account_email
            sys.exit(f"403: la cuenta de servicio {email} no tiene acceso a la "
                     f"propiedad {SITE}. Añádela como propietaria en Search Console "
                     "(Ajustes › Usuarios y permisos › Añadir usuario).")
        raise
    OUT.mkdir(exist_ok=True)

    sitemaps = service.sitemaps().list(siteUrl=SITE).execute()
    (OUT / "sitemaps.json").write_text(json.dumps(sitemaps, indent=2, ensure_ascii=False))

    rows = []
    request = {"startDate": "2026-11-01", "endDate": date.today().isoformat(),
               "dimensions": ["date"], "rowLimit": 25000}
    while True:
        resp = service.searchanalytics().query(siteUrl=SITE, body=request).execute()
        rows.extend(resp.get("rows", []))
        if "rows" not in resp:
            break
        request["startRow"] = len(rows)
    (OUT / "searchanalytics.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    insp = service.urlInspection().index().inspect(
        body={"inspectionUrl": "https://sanchesque.com/", "siteUrl": SITE}).execute()
    (OUT / "urlinspection-root.json").write_text(json.dumps(insp, indent=2, ensure_ascii=False))

    impr = sum(r.get("impressions", 0) for r in rows)
    clicks = sum(r.get("clicks", 0) for r in rows)
    print(f"guardado en {OUT}/: sitemaps={len(sitemaps.get('sitemap', []))}, "
          f"analytics filas={len(rows)} (impresiones={impr}, clics={clicks})")


if __name__ == "__main__":
    main()
