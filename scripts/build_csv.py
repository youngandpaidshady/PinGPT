import json, csv, os
from datetime import datetime, timedelta

urls_path = r'c:\Users\Administrator\Desktop\PinGPT\pinterest_urls.json'
csv_path = r'c:\Users\Administrator\Desktop\PinGPT\output\pinterest_bulk.csv'

with open(urls_path, 'r', encoding='utf-8') as f:
    urls = json.load(f)

pins = [
    # dl_1 - Toji ironsilence
    {'file': 'dl_1.png', 'title': '"one more." — the bar doesn\'t ask what happened', 'board': 'Jujutsu Kaisen Wallpapers',
     'desc': 'chalk dust. sodium light. 2am and the only thing that makes sense is the weight in his hands. some people journal. some people drink. he lifts until the noise stops. that wrap unraveling is the most honest thing about him right now. #tojifushiguro #jujutsukaisen #jjk #tojiaesthetic #ironsilence #2amgym #latenighttraining #darkaesthetic #animeboy #animewallpaper #gymmotivation #fightermanime #sigma #discipline #rawanime #literallyme #lockscreenwallpaper #animewarrior #gymlife'},
    # dl_2 - Yuta 4amvibes
    {'file': 'dl_2.png', 'title': '4:03am. still here.', 'board': 'Jujutsu Kaisen Wallpapers',
     'desc': 'cold coffee. one earbud in. the waitress stopped asking an hour ago. there\'s something about a 24hr diner at 4am that feels like the only honest place left. no performance. no audience. just you and the hum of the neon. #yutaokkotsu #jujutsukaisen #jjk #yutaaesthetic #4amvibes #latenightvibes #insomniaesthetic #midnightmood #darkaesthetic #animeboy #animewallpaper #lofivibes #moodyanime #nightowl #literallyme #lockscreenwallpaper'},
    # dl_3 - Jinwoo edgeofbed
    {'file': 'dl_3.png', 'title': 'all the power. none of the peace.', 'board': 'Anime Wallpapers',
     'desc': 'penthouse view. unmade bed. the shadow monarch can\'t sleep either. there\'s a version of winning where you lose everything soft about yourself. city lights don\'t keep you warm. they just remind you everyone else is asleep. #sungjinwoo #sololeveling #sololevelinganime #jinwooaesthetic #edgeofbed #darkaesthetic #animeboy #animewallpaper #midnightmood #shadowmonarch #sigma #lonewolf #lockscreenwallpaper #moodyanime'},
    # dl_4 - Denji grungeloner
    {'file': 'dl_4.png', 'title': 'the beautiful wreck.', 'board': 'Anime Wallpapers',
     'desc': 'beer can on his chest. posters peeling. one shoe off. this isn\'t a cry for help — this IS the help. the floor doesn\'t judge. the lamplight doesn\'t ask questions. he chose this and honestly? it looks like freedom. #denji #chainsawman #csm #denjiaesthetic #grungeloner #grunge #animeboy #darkaesthetic #animewallpaper #rebellion #aestheticmood #lockscreenwallpaper #literallyme #lonervibes #moodyanime'},
    # dl_5 - Nagi lofiden
    {'file': 'dl_5.png', 'title': 'effort is overrated.', 'board': 'Anime Wallpapers',
     'desc': 'controller died. he didn\'t move. dawn came anyway. there\'s genius in the laziness — or maybe laziness in the genius. the monitor glow is the only thing keeping time in this room. the world can wait. #nagiseishiro #bluelock #bluelockanime #nagiaesthetic #lofiden #lofi #lofiaesthetic #animeboy #animewallpaper #bedroomaesthetic #cozyroom #gamingaesthetic #lockscreenwallpaper #chillvibes #nightowl'},
    # dl_6 - Isagi skylineache
    {'file': 'dl_6.png', 'title': 'the bus left. he stayed.', 'board': 'Anime Wallpapers',
     'desc': 'golden hour. grass stains still on the joggers. a city that doesn\'t know his name yet but will. crouched at the edge, watching the skyline dissolve into purple. one day he\'ll be up there. tonight he just watches. #isagiyoichi #bluelock #bluelockanime #isagiaesthetic #skylineache #twilight #goldenhour #animeboy #darkaesthetic #animewallpaper #rooftopvibes #cityscape #lockscreenwallpaper #moodyanime #ambition #sigma'},
    # dl_7 - Killua dawnwalk
    {'file': 'dl_7.png', 'title': 'survived another one.', 'board': 'Anime Wallpapers',
     'desc': 'sneakers off. first light. silver hair and the only silence that doesn\'t hurt. there\'s something about dawn on a pier that feels like forgiveness. the water doesn\'t care what you did yesterday. maybe showing up is the whole thing. #killua #killuazoldyck #hunterxhunter #hxh #killuaaesthetic #dawnwalk #firstlight #sunrise #animeboy #animewallpaper #peacefulanime #goldenhour #lockscreenwallpaper #solitude'},
    # dl_8 - Rin jerseycore
    {'file': 'dl_8.png', 'title': 'everyone left. he didn\'t.', 'board': 'Anime Wallpapers',
     'desc': 'wet court. puddle under his fingertips. floodlights humming and nobody else for miles. this is what obsession looks like when the cameras are off. just him and the ball and the thing he can\'t name that won\'t let him stop. #rinitoshi #bluelock #bluelockanime #rinaesthetic #jerseycore #soccerboy #animesports #animeboy #darkaesthetic #animewallpaper #athleticaesthetic #sigma #discipline #lockscreenwallpaper #sportsanime'},
    # dl_9 - Loid darkacademia
    {'file': 'dl_9.png', 'title': 'the spy reads for himself now.', 'board': 'Anime Wallpapers',
     'desc': 'gloved finger on a page nobody ordered him to read. desk lamp. silence. there\'s something about a man in a vest with reading glasses that just hits different at midnight. for once he\'s not gathering intel — he\'s just here. #loidforger #spyxfamily #loidaesthetic #darkacademia #libraryaesthetic #animeboy #intellectualaesthetic #darkaesthetic #animewallpaper #moodyanime #literarycore #candlelitstudy #lockscreenwallpaper'},
    # dl_10 - Nagi lofiden v2
    {'file': 'dl_10.png', 'title': 'his controller died three hours ago.', 'board': 'Anime Wallpapers',
     'desc': 'headphones around his neck. chip bag empty. the monitor screensaver is doing more work than he has all day. that\'s the genius tax — everyone thinks you\'re lazy but really you just solved it already. the beanbag gets it. the beanbag doesn\'t judge. #nagiseishiro #bluelock #bluelockanime #nagiaesthetic #lofiden #lofi #gamingroom #animeboy #animewallpaper #cozyroom #bedroomaesthetic #chillvibes #gamingaesthetic #lockscreenwallpaper'},
    # dl_11 - Yuji burnoutdesk
    {'file': 'dl_11.png', 'title': 'he tried. that counts.', 'board': 'Jujutsu Kaisen Wallpapers',
     'desc': 'face on papers. pencil still in hand. the clock says 2:47 and the deadline doesn\'t know he\'s asleep. crumpled paper everywhere like tiny white flags of surrender. some people burn out quietly. he burned out mid-sentence. #yujiitadori #jujutsukaisen #jjk #yujiaesthetic #burnoutdesk #studyanime #animeboy #darkaesthetic #animewallpaper #academicburn #studyvibes #lockscreenwallpaper #literallyme #relatable #overachiever'},
    # dl_12 - Isagi skylineache v2
    {'file': 'dl_12.png', 'title': 'a city that doesn\'t know his name. yet.', 'board': 'Anime Wallpapers',
     'desc': 'team Z jersey. grass stains. that backpack with everything he owns. the sunset\'s doing its best work and he\'s just cataloguing every rooftop he\'ll stand on top of someday. ambition looks lonely from here. #isagiyoichi #bluelock #bluelockanime #isagiaesthetic #skylineache #rooftopvibes #twilight #goldenhour #animeboy #darkaesthetic #animewallpaper #cityscape #ambition #lockscreenwallpaper #dreamchaser #sigma #sportsanime'},
    # dl_13 - Killua dawnwalk v2
    {'file': 'dl_13.png', 'title': 'the boats don\'t ask where he came from.', 'board': 'Anime Wallpapers',
     'desc': 'one shoe on. one shoe off. harbor boats sleeping in the distance. the whole sky is doing that thing where it can\'t decide if it\'s night or morning. he ran away from everything and ended up somewhere this quiet. maybe the running was the destination. #killua #killuazoldyck #hunterxhunter #hxh #killuaaesthetic #dawnwalk #harborvibes #sunrise #animeboy #animewallpaper #peacefulanime #goldenhour #lockscreenwallpaper #freedom #solitude'},
    # dl_14 - Aqua sadboy
    {'file': 'dl_14.png', 'title': '"i\'ll be fine." — he wasn\'t.', 'board': 'Anime Wallpapers',
     'desc': 'rain-soaked blazer. headphones that aren\'t playing anything. the phone booth receiver hanging like he was mid-conversation with someone who left. there\'s a star in one eye that nobody noticed because they were too busy watching the performance. #aquahoshino #oshinoko #aquaaesthetic #sadboy #sadboyaesthetic #animeboy #darkaesthetic #rainaesthetic #animewallpaper #moodyanime #sadboyhours #literallyme #lockscreenwallpaper #animepfp #lonelyboy'},
]

start = datetime(2026, 4, 12, 14, 30, 0)
times = [(14, 30), (20, 30)]

rows = []
for i, pin in enumerate(pins):
    day_offset = i // 2
    time_idx = i % 2
    dt = start.replace(hour=times[time_idx][0], minute=times[time_idx][1]) + timedelta(days=day_offset)
    
    media_url = urls.get(pin['file'], {}).get('url', '')
    
    keywords = [t.replace('#','') for t in pin['desc'].split() if t.startswith('#')]
    desc = pin['desc']
    
    # Check if we need to remove the hashtags from the description to save space, or just keep them
    # For bulk CSV, we leave them in the description if requested, or keep the keyword list.
    
    rows.append({
        'Title': pin['title'],
        'Media URL': media_url,
        'Pinterest board': pin['board'],
        'Thumbnail': '',
        'Description': desc,
        'Link': '',
        'Publish date': dt.strftime('%Y-%m-%d %H:%M:%S'),
        'Keywords': ','.join(keywords)
    })

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Successfully wrote {len(rows)} pins to {csv_path}")
for r in rows:
    print(f"{r['Publish date']} - {r['Title']}")
