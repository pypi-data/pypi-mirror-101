import pytest
from unittest import TestCase
import os
from acme_news.engines.aljazeera import AljazeeraEngine
from typing import List, Dict

class TestBrowser(TestCase):

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_news_contents(self):
        alj = AljazeeraEngine(search_query='iraq')
        results: List[Dict] = alj.parse_alj_contents()
        return self.assertEqual(10, len(results))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_video_links(self):
        alj = AljazeeraEngine(search_query='iraq', video=True, quantity=100, offset=4)
        results: List[Dict] = alj.parse_video_links()
        return self.assertEqual(100, len(results))
