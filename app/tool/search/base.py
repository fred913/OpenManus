class WebSearchEngine(object):
    def perform_search(
        self, query: str, num_results: int = 10, *args, **kwargs
    ) -> list[dict | str]:
        """
        Perform a web search and return a list of URLs.

        Args:
            query (str): The search query to submit to the search engine.
            num_results (int, optional): The number of search results to return. Default is 10.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            list[dict | str]: A list of dict matching the search query.
        """
        raise NotImplementedError
