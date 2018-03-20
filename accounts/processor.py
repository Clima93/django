import json
from common.models import Quote


def common(request):
	active_quotes = Quote.objects.filter(active=True)
	quotes = [{"author": x.author, "quote": x.text} for x in active_quotes]
	response = {'quotes': json.dumps(quotes)}

	return response