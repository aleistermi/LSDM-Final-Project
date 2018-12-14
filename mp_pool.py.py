import util
import multiprocessing as mp
import pandas as pd


zm_mex = pd.read_csv('zmmex.csv')[['CVE_MUN', 'MUN']]
crimes = ['homicidio', 'homicidios', 'muerto', 'muerte', 'muertos', 'muertes',  
          'asesinato', 'asesinatos', 'asesinados', 'asesinado',
          'ejecucion', 'ejecuciones', 'ejecutado', 'ejecutados',
          'secuestro', 'secuestros','secuestrado', 'secuestrada', 'secuestrados', 'secuestradas',
          'rapto', 'raptos', 'raptado', 'raptados', 'raptadas',
          'levanton', 'levantones',
          'feminicidio', 'feminicidios', 'asesinada', 'asesinadas', 'muerta','muertas']

cities = list(set(zm_mex['MUN']))

keywords_1 = util.build_keywords_list(cities[:200], crimes)
keywords_2 = util.build_keywords_list(cities[200:], crimes)

api_keys = ['a0849f217c5d4628a7350ce96868c85d', '7d337567864a45f19a5fe1a56d31c1bd']

url_requests_1 = [util.build_url(k, '2018-12-12T00:00:00', '2018-12-12T23:59:59', key= api_keys[0]) for k in keywords_1]
url_requests_2 = [util.build_url(k, '2018-12-12T00:00:00', '2018-12-12T23:59:59', key= api_keys[1]) for k in keywords_2]
url_requests = url_requests_1 + url_requests_2


def topics(url_request):
    response = util.get_news_json(url_request)
    if type(response) == str:
        return 'Maximun free news request exceded'
    articles_list = util.news_collection(response)
    if len(articles_list) == 0:
        return 'No topics found'
    articles_text = [util.get_content2(article) for article in articles_list if type(util.get_content2(article))==str]
    if len(articles_text) == 0:
        return 'No topics found'
    response_corpus = ' '.join(articles_text)
    topics = util.get_topics(response_corpus)
    print(topics)
    return topics



if __name__ == '__main__':
	p = mp.Pool(processes=3)

	r = p.map_async(topics, url_requests)

	p.close()
	p.join()
	
	results = r.get()

	#print(results)