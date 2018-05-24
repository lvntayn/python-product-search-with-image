import sys
from profind.crawler.hepsiburada import Hepsiburada
from profind.crawler.markafoni import Markafoni
from profind.crawler.trendyol import Trendyol
from profind.crawler.update import UpdateAll

site = sys.argv[1]
category = sys.argv[2]
page = sys.argv[3]

if site == 'hepsiburada':
    test = Hepsiburada()
    test.fetch(category, page)
elif site == 'trendyol':
    test = Trendyol()
    test.fetch(category, page)
elif site == 'markafoni':
    test = Markafoni()
    test.fetch(category, page)
elif site == 'update':
    test = UpdateAll()
    test.run()