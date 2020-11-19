import requests, json

def implicature(query: str):
    ret = requests.post(url='http://server.seiker.kr:444', 
                        json={'query': query})
    ret = ret.json()
    
    if ret['predict'] is None:
        print(ret)
        raise ValueError('NLP module returned null.')

    print('[info] Implicature detected to {}'.format(ret['predict']))

    return ret['predict']