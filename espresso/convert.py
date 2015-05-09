def dataframe_to_list(df):
	"""returns df as a columns of data"""
	idx = list(df.index.values)
	values = list(df.values)
	z = zip(idx, values)
	return [(str(x[0]),float(x[1])) for x in z]

def aggregate_dataframe(df, interval='daily'):
	"""returns df aggregated to interval as columns of data"""
	return df.groupby(df['datetime'].map(lambda x: x.date())).sum()