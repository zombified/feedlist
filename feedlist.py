import feedparser

OUTPUT_PATH = "feeds.html"

FEEDS_TO_PULL = [
    ('fastmail', 'https://blog.fastmail.com/feed/', False),
    ('fortress of doors', 'http://www.fortressofdoors.com/rss/', False),
    ('gamedev treasure', 'http://www.gamedevtreasure.com/rss.xml', False),
    ('gurney journey', 'http://feeds.feedburner.com/blogspot/NVaYV?format=xml', False),
    ('joel kleier', 'https://joelkleier.com/rss.xml', False),
    ('lost decade games', 'http://www.lostdecadegames.com/rss.xml', False),
    ('nathan vangheem', 'https://www.nathanvangheem.com/feeds/posts/rss.xml', True),
    ('pollocks host file', 'http://someonewhocares.org/hosts/rss.xml', False),
    ('raspberry pi', 'https://www.raspberrypi.org/feed/', False),
    ('rocket.chat github tags', 'https://github.com/RocketChat/Rocket.Chat/tags.atom', True),
    ('rust lang', 'https://blog.rust-lang.org/', False),
    ('skial bainn', 'http://blog.skialbainn.com/rss', False),
    ('tested', 'http://www.tested.com/feeds/', False),
    ('wildcard corp', 'https://www.wildcardcorp.com/blog/rss.xml', True),
    ('nixos weekly', 'http://weekly.nixos.org/feeds/all.rss.xml', False),
    ('webupd8', 'http://feeds.feedburner.com/webupd8?format=xml', True),
]

STYLE = """
ul, li {
    list-style:none;
}
ul {
    margin:0;
    padding:0;
}
li {
    margin-left:10px;
    margin-bottom:10px;
    padding:0;
}


.itemdate,
.feedinfo {
    font-size:x-small;
    font-family:verdana,arial,sans;
    text-transform:lowercase;
}


.itemdate:before {
    content:"published on";
    padding-right:3px;
}
.itemdate:after {
    content:"by";
    padding-left:3px;
}


.feedinfo a,
.feedinfo a:link,
.feedinfo a:visited,
.feedinfo a:hover,
.feedinfo a:active {
    color: #336699;
}
.feedinfo a,
.feedinfo a:link,
.feedinfo a:visited,
.feedinfo a:active {
    text-decoration:none;
}
.feedinfo a:hover {
    text-decoration:underline;
}

.iteminfo {
    display:block;
}
.iteminfo a {
    font-size:medium;
    font-family:verdana,arial,sans;
    font-weight:normal;
}
.iteminfo a,
.iteminfo a:link,
.iteminfo a:visited,
.iteminfo a:hover,
.iteminfo a:active {
    text-decoration:none;
}
"""


def sortitem(val):
    return int("{:0>4d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}".format(val[4][0], val[4][1], val[4][2], val[4][3], val[4][4]))


def get_items():
    items = []
    for feed in FEEDS_TO_PULL:
        parsed = feedparser.parse(feed[1])
        try:
            if not feed[2]:
                feedtitle = parsed.feed.title
            else:
                feedtitle = feed[0]
        except:
            feedtitle = feed[0]

        try:
            feedlink = parsed.feed.link
        except:
            feedlink = feed[1]

        feeditems = []
        for item in parsed.entries:
            entrytitle = item.title
            entrylink = item.link
            try:
                entrydate = item.published_parsed
            except:
                entrydate = item.updated_parsed

            feeditems.append([feedtitle, feedlink, entrytitle, entrylink, entrydate])
        feeditems.sort(key=sortitem, reverse=True)
        items += feeditems[:15]
    return sorted(items, key=sortitem, reverse=True)


feeditems = get_items()
with open(OUTPUT_PATH, 'w') as feedout:
    feedout.write("<html><head><title>Feed List</title><style type='text/css'>{}</style></head><body><ul>".format(STYLE))
    for item in feeditems:
        feedout.write("<li><span class='iteminfo'><a href='{}'>{}</a></span> <span class='itemdate'>{}-{}-{}</span> <span class='feedinfo'><a href='{}'>{}</a></span></li>".format(
            item[3], item[2],
            item[4][0], item[4][1], item[4][2],
            item[1], item[0]))
    feedout.write("</ul></body></html>")

