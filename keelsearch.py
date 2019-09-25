import keelback
import pylev

def search(query):
    manifest = keelback.inventory.keys()
    query = query.lower().replace('+', '-')

    if query in manifest:
        return query
    else:
        ratio_best = {'page': '', 'ratio': 0}
        for page in manifest:
            distance = pylev.levenshtein(query, page)
            ratio = 1 - distance / len(query + page)
            if ratio > ratio_best['ratio']:
                ratio_best['page'] = page
                ratio_best['ratio'] = ratio

        if ratio_best['ratio'] > 0.75:
            return ratio_best['page']
        else:
            print('KEELBACK: 404 encountered while searching for query: ' + str(query))
            return 'no-results'
