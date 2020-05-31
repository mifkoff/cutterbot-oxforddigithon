languages = ['ru', 'en', 'de', 'es', 'aa', 'ab', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az',
             'ba', 'bm', 'eu', 'be', 'bn', 'bh', 'bi', 'bo', 'bs', 'br', 'bg', 'my', 'ca', 'cs', 'ch', 'ce', 'zh', 'cu',
             'cy', 'cs', 'da', 'de', 'dv', 'nl', 'dz', 'el', 'eo', 'et', 'eu', 'ee', 'fo', 'fa', 'fj', 'fi', 'fr', 'cv',
             'fy', 'ff', 'Ga', 'gd', 'ga', 'gl', 'gv', 'el', 'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hr', 'kw',
             'hu', 'hy', 'ig', 'is', 'io', 'ii', 'iu', 'ie', 'ia', 'id', 'ik', 'is', 'it', 'jv', 'ja', 'kl', 'kn', 'ks',
             'ka', 'kr', 'kk', 'km', 'ki', 'rw', 'ky', 'kv', 'kg', 'ko', 'kj', 'ku', 'lo', 'la', 'lv', 'li', 'ln', 'lt',
             'lb', 'lu', 'lg', 'mk', 'mh', 'ml', 'mi', 'mr', 'ms', 'Mi', 'mk', 'mg', 'mt', 'mn', 'mi', 'ms', 'my', 'na',
             'nv', 'nr', 'nd', 'ng', 'ne', 'nl', 'nn', 'nb', 'no', 'oc', 'oj', 'or', 'om', 'os', 'pa', 'fa', 'pi', 'pl',
             'pt', 'ps', 'qu', 'rm', 'ro', 'ro', 'rn', 'sg', 'sa', 'si', 'sk', 'sk', 'sl', 'se', 'sm', 'sn', 'sd', 'kw',
             'so', 'st', 'es', 'sq', 'sc', 'sr', 'ss', 'su', 'sw', 'sv', 'ty', 'ta', 'tt', 'te', 'tg', 'tl', 'th', 'bo',
             'ti', 'to', 'tn', 'ts', 'tk', 'tr', 'tw', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'cy', 'wa', 'wo', 'xh',
             'yi', 'yo', 'za', 'zh', 'zu']
audio_file_name = 'article_t2s.mp3'
url_expression = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
emojies = '😄😇😍😌😎🤪🤩😏🤯🤬🥴🤤👊🤝🤞✊✌️🤘👌☝️🦄🙈⚡️🔥🎲🚀💡💰💣🔮🦠🎁🎉📚📝❤️💔💖☢️⛔️💯⚠️🍭🍺🌚🌝'
welcome_message = '''
Hi there! 👋

I am CutterBot but my target are articles and videos rather than people  😏
I think you know that every second a lot of new information is published which makes it impossible to read and watch everything.
I have a solution for you: send me a link for article or video, I will make summary and voice it so that it would be convinient for you to know information inside quickly.

As an example, you can send me an article on Forbes, for example https://www.forbes.ru/billionaire-school/401131-kodeks-obshchezhitiya-kak-osnovateli-skyeng-ne-slomalis-na-starte
'''
answer_for_message_no_links = '''
You message does not contain any URLs so that I cannot process it. 😔
Please, send your link again
'''
answer_for_message_with_links = '''
Got it! 🤪
Will come back when I am done processing
'''
already_in_progress = 'Your link is already in work. Wait a little bit!'
uploading_in_progress = 'Uploading your video 🔥'
already_in_bot = 'You are in bot already 🥴'
cannot_process = 'Sorry, I cannot process it. 😔'
