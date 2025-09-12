#!/usr/bin/env python3
import argparse
import logging
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import requests
import xml.dom.minidom as minidom

DEFAULT_CHANNELS_XML = "vodafone.pt.channels.xml"
DEFAULT_OUTPUT = "epg-vodafone-pt.xml"
SEGMENTS = ["00-06", "06-12", "12-18", "18-00"]
TZ = ZoneInfo("Europe/Lisbon")
HEADERS = {
    "User-Agent": "vodafone-epg-extractor/1.0 (+https://example.local)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

logger = logging.getLogger("vodafone_epg")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(fmt)
logger.addHandler(ch)

def parse_channels_xml(path: str):
    p = Path(path)
    if not p.exists():
        logger.error("Ficheiro de canais não encontrado: %s", path)
        raise FileNotFoundError(path)
    tree = ET.parse(p)
    root = tree.getroot()
    channels = []
    for chn in root.findall("channel"):
        site_id = chn.get("site_id") or chn.get("site") or chn.get("siteId") or chn.get("siteid")
        xmltv_id = chn.get("xmltv_id") or chn.get("xmltvid") or ""
        name = (chn.text or "").strip()
        if not xmltv_id:
            xmltv_id = f"vodafone.{site_id}"
        channels.append({"site_id": str(site_id), "name": name, "xmltv_id": xmltv_id})
    logger.info("Lidos %d canais do ficheiro %s", len(channels), path)
    return channels

def build_url(site_id: str, d: date, segment: str) -> str:
    return f"https://cdn.pt.vtv.vodafone.com/epg/{site_id}/{d.year:04d}/{d.month:02d}/{d.day:02d}/{segment}"

def parse_onair_datetime(val: str):
    if not val:
        return None
    for fmt in ("%d/%m/%Y %H:%M:%S", "%m/%d/%Y %H:%M:%S"):
        try:
            dt = datetime.strptime(val, fmt)
            return dt.replace(tzinfo=TZ)
        except Exception:
            continue
    try:
        dt = datetime.fromisoformat(val)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=TZ)
        return dt
    except Exception:
        logger.debug("Não foi possível parsear datetime: %s", val)
        return None

def program_to_xml(program: dict, channel_xmltv_id: str):
    metas = program.get("metas", {}) or {}
    start_raw = None
    end_raw = None
    try:
        if "onAir start time" in metas:
            start_raw = metas["onAir start time"].get("value")
        elif program.get("startDate"):
            ts = program.get("startDate")
            if ts:
                start_dt = datetime.fromtimestamp(int(ts), tz=TZ)
                start_raw = start_dt.strftime("%d/%m/%Y %H:%M:%S")
        if "onAir end time" in metas:
            end_raw = metas["onAir end time"].get("value")
        elif program.get("endDate"):
            ts = program.get("endDate")
            if ts:
                end_dt = datetime.fromtimestamp(int(ts), tz=TZ)
                end_raw = end_dt.strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        logger.debug("Erro a ler metas start/end para programa id=%s", program.get("id"))

    start_dt = parse_onair_datetime(start_raw) if start_raw else None
    end_dt = parse_onair_datetime(end_raw) if end_raw else None
    if not start_dt or not end_dt:
        try:
            if program.get("startDate") and program.get("endDate"):
                start_dt = datetime.fromtimestamp(int(program["startDate"]), tz=TZ)
                end_dt = datetime.fromtimestamp(int(program["endDate"]), tz=TZ)
        except Exception:
            pass

    if not start_dt or not end_dt:
        logger.warning("Ignorar programa sem horas válidas: %s (%s)", program.get("name"), program.get("id"))
        return None

    start_attr = f"{start_dt.strftime('%Y%m%d%H%M%S')} {start_dt.strftime('%z')}"
    stop_attr = f"{end_dt.strftime('%Y%m%d%H%M%S')} {end_dt.strftime('%z')}"
    prog = ET.Element("programme", {"start": start_attr, "stop": stop_attr, "channel": channel_xmltv_id})

    title = ET.SubElement(prog, "title")
    title.text = program.get("name") or ""

    desc_text = program.get("description") or ""
    desc = ET.SubElement(prog, "desc")
    desc.text = desc_text

    try:
        tags = program.get("tags") or {}
        genre = tags.get("genre")
        if genre and isinstance(genre, dict):
            objs = genre.get("objects") or []
            for g in objs:
                val = g.get("value")
                if val:
                    cat = ET.SubElement(prog, "category")
                    cat.text = val
    except Exception:
        pass

    try:
        imgs = program.get("images") or []
        if imgs and isinstance(imgs, list):
            url = None
            for im in imgs:
                if im.get("imageTypeName") == "cc":
                    url = im.get("url")
                    break
            if not url and imgs:
                url = imgs[0].get("url")
            if url:
                icon = ET.SubElement(prog, "icon")
                icon.set("src", url)
    except Exception:
        pass

    try:
        episode_name = metas.get("episode name", {}).get("value")
        if episode_name:
            en = ET.SubElement(prog, "episode-num", {"system": "onscreen"})
            en.text = episode_name
    except Exception:
        pass

    try:
        crid = program.get("crid") or program.get("epgId") or program.get("externalId")
        if crid:
            cr = ET.SubElement(prog, "crid")
            cr.text = str(crid)
    except Exception:
        pass

    return prog

def fetch_channel_segment(session: requests.Session, site_id: str, d: date, segment: str):
    url = build_url(site_id, d, segment)
    logger.debug("GET %s", url)
    try:
        r = session.get(url, headers=HEADERS, timeout=15)
    except Exception as e:
        logger.warning("Erro na request %s : %s", url, e)
        return None, site_id
    if r.status_code != 200:
        logger.warning("Resposta não-ok %s -> %s", url, r.status_code)
        return None, site_id
    try:
        j = r.json()
    except Exception as e:
        logger.warning("JSON inválido em %s : %s", url, e)
        return None, site_id
    return j, site_id

def generate_xmltv(channels: list, out_file: str, date_list: list, segments: list, workers: int = 6):
    logger.info("Iniciar geração XMLTV para %d datas", len(date_list))
    tv = ET.Element("tv", {"generator-info-name": "vodafone-epg-to-xmltv", "source-info-url": "https://cdn.pt.vtv.vodafone.com"})
    for ch in channels:
        cid = ch["xmltv_id"] or f"vodafone.{ch['site_id']}"
        c = ET.SubElement(tv, "channel", {"id": cid})
        dn = ET.SubElement(c, "display-name")
        dn.text = ch["name"] or cid

    session = requests.Session()
    futures = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for d in date_list:
            for ch in channels:
                site_id = ch["site_id"]
                for seg in segments:
                    futures.append(ex.submit(fetch_channel_segment, session, site_id, d, seg))
        for fut in as_completed(futures):
            res, site_id = fut.result()
            if not res:
                continue
            j = res.get("result") or {}
            objects = j.get("objects") or []
            for prog in objects:
                try:
                    epg_id = prog.get("epgChannelId")
                    channel_xmltv_id = None
                    if epg_id:
                        for ch in channels:
                            if ch["site_id"] and str(ch["site_id"]) == str(epg_id):
                                channel_xmltv_id = ch["xmltv_id"]
                                break
                    if not channel_xmltv_id:
                        for ch in channels:
                            if ch["site_id"] == str(site_id):
                                channel_xmltv_id = ch["xmltv_id"]
                                break
                    if not channel_xmltv_id:
                        channel_xmltv_id = f"vodafone.{epg_id}" if epg_id else f"vodafone.{site_id}"
                    pr = program_to_xml(prog, channel_xmltv_id)
                    if pr is not None:
                        tv.append(pr)
                except Exception:
                    logger.exception("Erro a processar programa: %s", prog.get("id"))

    raw = ET.tostring(tv, encoding="utf-8")
    reparsed = minidom.parseString(raw)
    pretty = reparsed.toprettyxml(indent="  ", encoding="utf-8")
    outp = Path(out_file)
    outp.write_bytes(pretty)
    logger.info("Escrito XMLTV em %s", out_file)

def main():
    ap = argparse.ArgumentParser(description="Extrai EPG Vodafone e gera XMLTV")
    ap.add_argument("-c", "--channels", default=DEFAULT_CHANNELS_XML, help="Ficheiro XML com a lista de canais")
    ap.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Ficheiro de saída XMLTV")
    ap.add_argument("-d", "--date", default=None, help="Data inicial (YYYY-MM-DD). Por defeito hoje.")
    ap.add_argument("-s", "--segments", default="all", help="Segmentos a pedir: all ou lista separada por vírgula")
    ap.add_argument("-w", "--workers", type=int, default=6, help="Workers concorrentes para pedidos HTTP")
    ap.add_argument("-v", "--verbose", action="store_true", help="Logs detalhados")
    ap.add_argument("-n", "--days", type=int, default=7, help="Número de dias a extrair (por defeito 7)")
    args = ap.parse_args()

    if args.verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    try:
        channels = parse_channels_xml(args.channels)
    except Exception as e:
        logger.error("Falha ao ler canais: %s", e)
        sys.exit(1)

    if args.date:
        try:
            start_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except Exception:
            logger.error("Formato de data inválido. Usa YYYY-MM-DD.")
            sys.exit(1)
    else:
        start_date = date.today()

    if args.segments.strip().lower() == "all":
        segments = SEGMENTS
    else:
        segments = [s.strip() for s in args.segments.split(",") if s.strip()]

    days = max(1, args.days)
    date_list = [start_date + timedelta(days=i) for i in range(days)]

    logger.info("Iniciar fetch EPG para %d canais, %d dias, segmentos %s", len(channels), days, segments)
    t0 = time.time()
    generate_xmltv(channels, args.output, date_list, segments, workers=args.workers)
    logger.info("Concluído em %.2f s", time.time() - t0)

if __name__ == "__main__":
    main()