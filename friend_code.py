from requests_html import HTMLSession
from bot_configs import BOT_LINK1, BOT_LINK2

session = HTMLSession()

page_config = [
    {
        'url': BOT_LINK1,
        'path': '.body-content .row div strong p',
    },  # expecting 20 codes max, chance for better players
    {
        'url': BOT_LINK2,
        'path': '#friends-list li div .comment-content strong',
    },  # expecting 30 codes max
]


def get_friend_codes(index=1):
    selected_config = page_config[index - 1]
    url = selected_config['url']
    r = session.get(url)
    items = r.html.find(selected_config['path'])
    return [item.text for item in items]
