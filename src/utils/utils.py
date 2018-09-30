class utils:
    @staticmethod
    def read_config():
        print"read_config"


def split_by_sep(string='', separators=','):
    rst = [string]
    for sep in separators:
        tmp = []
        for r in rst:
            tmp.extend(map(lambda x: x.strip(), r.split(sep)))
        rst = tmp
    list_tmp = []
    [list_tmp.append(data) for data in rst if data != '']
    return reduce(lambda x, y: (y in x) and x or (x + [y]), ([[], ] + list_tmp) )

__all__ = ["utils"]