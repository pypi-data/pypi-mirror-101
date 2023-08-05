from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
import nltk


class Swifter:
	"""docstring for Swifter"""
	def __init__(self, start_date,end_date, keyword):
		self._start_date = start_date
		self._end_date = end_date
		self._keyword = keyword
	def Collector(self):
		googlenews=GoogleNews(start = self._start_date, end = self._end_date)
		googlenews.search(self._keyword)
		result = googlenews.result()
		df = pd.DataFrame(result)
		df = df.drop(['datetime', 'link','img'], axis=1)
		return df





		