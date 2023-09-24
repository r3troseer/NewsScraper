from newspaper import Article, build, fulltext


def vanguard_paper():
    urls = "https://leadership.ng/"
    vanguard_paper = build(urls,  memoize_articles=False)
    print(vanguard_paper.size())
    for article in vanguard_paper.articles:
        print(article.url)

    # for category in vanguard_paper.category_urls():
    #     print(category)



    # >>> vanguard_article = vanguard_paper.articles[0]
    urls = "https://www.vanguardngr.com/2023/09/breaking-explosion-at-benin-illegal-fuel-depot-kills-34/"
    article =Article(urls)
    article.download()
    article.parse()
    print(article.text)
vanguard_paper()