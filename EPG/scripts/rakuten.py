from lxml import etree
import requests
from datetime import datetime, timedelta, time, timezone
import pytz
import unicodedata
import time as times
import gzip

tz = pytz.timezone('Europe/London')


def remove_control_characters(s):
    return "".join(
        ch for ch in s
        if unicodedata.category(ch)[0] != "C"
    )


def get_days() -> list:
    # Hora actual em Europe/London, arredondada à hora
    now = datetime.now(tz).replace(
        minute=0,
        second=0,
        microsecond=0
    )

    # Meia-noite local
    today = datetime.now(tz).date()

    day_1 = tz.localize(
        datetime.combine(today, time(0, 0))
    ) + timedelta(days=1)

    day_2 = tz.localize(
        datetime.combine(today, time(0, 0))
    ) + timedelta(days=2)

    day_3 = tz.localize(
        datetime.combine(today, time(0, 0))
    ) + timedelta(days=3)

    return [now, day_1, day_2, day_3]


def build_xmltv(channels: list, programmes: list) -> bytes:
    dt_format = '%Y%m%d%H%M%S %z'

    data = etree.Element("tv")

    for ch in channels:
        channel = etree.SubElement(data, "channel")
        channel.set("id", str(ch.get("id")))

        name = etree.SubElement(channel, "display-name")
        name.set("lang", ch.get("language")[:-1].lower())
        name.text = remove_control_characters(ch.get("name"))

        if ch.get("icon") is not None:
            icon_src = etree.SubElement(channel, "icon")
            icon_src.set("src", ch.get("icon"))
            icon_src.text = ''

    for pr in programmes:
        programme = etree.SubElement(data, 'programme')

        start_time = datetime.fromtimestamp(
            pr.get('starts_at'),
            tz
        ).strftime(dt_format)

        end_time = datetime.fromtimestamp(
            pr.get('ends_at'),
            tz
        ).strftime(dt_format)

        programme.set("channel", str(pr.get('channel_id')))
        programme.set("start", start_time)
        programme.set("stop", end_time)

        title = etree.SubElement(programme, "title")
        title.set('lang', 'pt')
        title.text = remove_control_characters(pr.get("title"))

        if pr.get("subtitle") is not None:
            subtitle = etree.SubElement(programme, "sub-title")
            subtitle.set('lang', 'pt')
            subtitle.text = remove_control_characters(pr.get("subtitle"))

        if pr.get("description") is not None:
            description = etree.SubElement(programme, "desc")
            description.set('lang', 'pt')
            description.text = remove_control_characters(pr.get("description"))

        if pr.get('tags') is not None and len(pr.get('tags')) > 0:
            category = etree.SubElement(programme, "category")
            category.set('lang', 'pt')
            category.text = remove_control_characters(
                pr.get('tags')[0].get("name")
            )

        if pr.get("snapshot") is not None:
            icon = etree.SubElement(programme, "icon")
            icon.set("src", pr.get("snapshot"))

    return etree.tostring(
        data,
        pretty_print=True,
        encoding='utf-8'
    )


days = get_days()

# Converter para UTC para que o timestamp e o epg_*_at
# representem exactamente o mesmo instante.
epg_start_utc = days[0].astimezone(timezone.utc)
epg_end_utc = days[-1].astimezone(timezone.utc)

# A API usa segundos inteiros
epg_starts_timestamp = int(epg_start_utc.timestamp())
epg_ends_timestamp = int(epg_end_utc.timestamp())

url_string = (
    f"classification_id=64"
    f"&device_identifier=web"
    f"&device_stream_audio_quality=2.0"
    f"&device_stream_hdr_type=NONE"
    f"&device_stream_video_quality=FHD"
    f"&epg_duration_minutes=10080"
    f"&epg_ends_at={epg_end_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')}"
    f"&epg_ends_at_timestamp={epg_ends_timestamp}"
    f"&epg_starts_at={epg_start_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')}"
    f"&epg_starts_at_timestamp={epg_starts_timestamp}"
    f"&locale=pt"
    f"&market_code=pt"
    f"&per_page=70"
)

url = (
    "https://gizmo.rakuten.tv/v3/live_channels?"
    + url_string.replace(":", "%3A")
)

print(url)

times.sleep(4)

print("A buscar informações...")

res = requests.get(url)

if res.status_code != 200:
    print(url)
    print(res.text)
    raise ConnectionError(
        f"HTTP{res.status_code}: could not get info from server!"
    )

print("A carregar o JSON.")

json = res.json()['data']

print(f"\nRetribuídos {len(json)} canais:")

channels_data = []
programme_data = []

for channel in json:
    ch_name = channel['title']
    print(ch_name)

    ch_number = channel['channel_number']
    ch_id = channel['id']

    ch_icon = None

    if channel['images'] is not None:
        images = channel['images']

        if images.get('artwork_negative') is not None:
            ch_icon = images.get('artwork_negative')

        elif images.get('artwork') is not None:
            ch_icon = images.get('artwork')

    ch_language = None
    ch_tags = None

    if channel['labels'] is not None:
        labels = channel['labels']

        if labels.get('languages') is not None:
            ch_language = labels['languages'][0].get('id')

        if labels.get('tags') is not None:
            ch_tags = labels['tags']

    ch_age_rating = None

    if channel['classification'] is not None:
        ch_age_rating = channel['classification'].get('age')

    channels_data.append({
        "name": ch_name,
        "epg_number": ch_number,
        "id": ch_id,
        "icon": ch_icon,
        "language": ch_language,
        "tags": ch_tags
    })

    programmes_list = channel['live_programs']

    for item in programmes_list:
        title = item['title']
        subtitle = item['subtitle']
        description = item['description']

        start = datetime.strptime(
            item['starts_at'],
            '%Y-%m-%dT%H:%M:%S.000%z'
        ).timestamp()

        end = datetime.strptime(
            item['ends_at'][:-6],
            '%Y-%m-%dT%H:%M:%S.000'
        ).timestamp()

        snapshot = None

        if item.get('images') is not None:
            snapshot = item['images'].get('snapshot')

        programme_data.append({
            "title": title,
            "subtitle": subtitle,
            "description": description,
            "starts_at": start,
            "ends_at": end,
            "channel_id": ch_id,
            "language": ch_language,
            "tags": ch_tags,
            "snapshot": snapshot,
        })


channel_xml = build_xmltv(
    channels_data,
    programme_data
)

with gzip.open('../epg-rakuten-tv.xml.gz', 'wb') as f:
    f.write(channel_xml)