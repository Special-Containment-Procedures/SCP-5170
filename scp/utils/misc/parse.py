from ._keyboard import _KB  # noqa
from math import ceil


def paginate_modules(page_n, module_dict, prefix, chat=None):
    modules = sorted([
        _KB(
            x.__PLUGIN__,
            callback_data=f'{prefix}_module({chat},{x.__PLUGIN__.lower()})',
        )
        for x in module_dict.values()
    ]) if chat else sorted(
        [
            _KB(
                x.__PLUGIN__,
                callback_data=f'{prefix}_module({x.__PLUGIN__.lower()})',
            )
            for x in module_dict.values()
        ],
    )

    pairs = list(zip(modules[::2], modules[1::2]))
    c = 0
    for x in pairs:
        for _ in x:
            c += 1
    if len(modules) - c == 1:
        pairs.append((modules[-1],))
    elif len(modules) - c == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            ),
        )

    max_num_pages = ceil(len(pairs) / 4)
    modulo_page = page_n % max_num_pages

    # can only have a certain amount of buttons side by side
    if len(pairs) > 4:
        pairs = pairs[modulo_page * 4: 4 * (modulo_page + 1)] + [
            (
                _KB(
                    '<', callback_data=f'{prefix}_prev({modulo_page})',
                ),
                _KB(
                    '>', callback_data=f'{prefix}_next({modulo_page})',
                ),
            ),
        ]
    return pairs
