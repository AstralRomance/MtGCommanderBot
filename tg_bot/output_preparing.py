from collections import defaultdict

def prepare_data(response_cards):
    unacked_dict_list = {k:v for d in response_cards for k, v in d.items()}
    formatted = defaultdict(lambda: {})
    for name, cards in unacked_dict_list.items():
        for suffix in ('Foil',):
            if name.endswith(suffix):
                name = name.replace(suffix, '')
                suffix = 'Foil' if suffix == ' (Foil)' else suffix.strip(' -')
            else:
                suffix = 'C'
            formatted[name][suffix] = cards
    return formatted

def prepare_cards(cards):
    res = [f'\t\t\t\t{state}: {price}' for card in cards for state, price in card.items()]
    return res

def prepare_output(prepared_cards):
    lines = []
    for set_name, variants in prepared_cards.items():
        lines.append(f'<b>{set_name}</b>')
        for variant, cards in sorted(variants.items()):
            if variant != 'C':
                lines.append(f'{variant}: ')
            lines += prepare_cards(cards)
    return lines

def make_parser_header(card_name):
    price_parsing = {
                        'request':
                        {
                            'url':card_name,
                            'dont_filter':True
                        },
                       'spider_name':'starcitygames'
                    }
    return price_parsing