import os
from eventregistry import QueryArticlesIter, EventRegistry

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

er = EventRegistry(apiKey=NEWS_API_KEY)


def get_news(
    concept: str,
    category: str = "",
    sourceLocation: str = "",
    maxItems: int = 5,
):
    """
    gets news articles based on concept, category, and source location.

    Args:
    concept (str): The concept to search for in the news articles.
    category (str) [optional]: The category of news articles to search for.
    sourceLocation (str) [optional]: The source location of the news articles (e.g. New York). Use only state or country names.
    maxItems (int) [optional]: The maximum number of articles to return. Default is 5.
    """
    q = QueryArticlesIter(
        conceptUri=er.getConceptUri(concept),
        categoryUri=er.getCategoryUri(category) if category != "" else None,
        sourceLocationUri=er.getLocationUri(sourceLocation)
        if sourceLocation != ""
        else None,
    )

    response = q.execQuery(er, sortBy="socialScore", maxItems=maxItems)
    articles = [article for article in response]
    print(articles)

    return articles
