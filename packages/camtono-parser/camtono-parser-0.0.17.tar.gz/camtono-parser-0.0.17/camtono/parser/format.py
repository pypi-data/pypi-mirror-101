from .dialects import load_dialect_module
from .clean import strip_comments, unwrap_variables, ENCODING_CHARACTER
from moz_sql_parser.formatting import Formatter as MozFormatter, escape


def format_query(query_ast, sql_dialect) -> str:
    """

    :param query_ast:
    :param sql_dialect:
    :return:
    """
    dialect = load_dialect_module(dialect_name=sql_dialect)
    formatted_query = dialect.format_query(query_ast=query_ast)

    formatted_query = unwrap_variables(
        query=formatted_query, encoding_character=ENCODING_CHARACTER, skip_characters=len(ENCODING_CHARACTER)
    )
    formatted_query = unwrap_variables(
        query=formatted_query, encoding_character='"',
        skip_characters=len(ENCODING_CHARACTER)
    )
    return formatted_query


def get_allowed_dialects(query_ast):
    """

    :param query_ast:
    :return:
    """
    from .dialects import list_dialects

    allowed_dialects = []
    for dialect in list_dialects():
        try:
            format_query(query_ast=query_ast, sql_dialect=dialect)
        except Exception:
            pass
        else:
            allowed_dialects.append(dialect)
    return allowed_dialects


class BaseFormatter(MozFormatter):
    """"""

    def _union(self, json, wrap=True):
        return "(" + self.union(json) + ")"

    def _union_all(self, json, wrap=True):
        return "(" + self.union_all(json) + ")"

    def union_distinct(self, json):
        return " UNION DISTINCT ".join(self.query(query) for query in json)

    def _union_distinct(self, json):
        return "(" + self.union_distinct(json=json) + ')'

    def _interval(self, json):
        return 'INTERVAL {0} {1}'.format(*json)

    def _distinct(self, json):
        if isinstance(json, list):
            return "DISTINCT " + self.dispatch(json=json)
        else:
            return "DISTINCT(" + self.dispatch(json=json) + ')'

    def value(self, json):
        parts = [self.dispatch(json["value"])]
        if 'over' in json:
            parts.extend(['OVER', self.over(json=json['over'])])
        if "name" in json:
            parts.extend(["AS", self.dispatch(json["name"])])
        return " ".join(parts)

    def over(self, json):
        result = "(PARTITION BY " + self.dispatch(json=json['partitionby'])
        if json.get('orderby'):
            result += ' ' + self.orderby(json=json)
        return result + ')'

    def format(self, json):
        base = ""
        if "union" in json:
            base = self.union(json["union"])
        elif "union_all" in json:
            base =  self.union_all(json["union_all"])
        elif "union_distinct" in json:
            base = self.union_distinct(json["union_distinct"])
        if base:
            return (self.query(json) + " " + base).strip()
        else:
            return self.query(json)

    def _in(self, json):
        valid = self.dispatch(json[1])
        # `(10, 11, 12)` does not get parsed as literal, so it's formatted as
        # `10, 11, 12`. This fixes it.
        if not valid.startswith("("):
            valid = "({0})".format(valid)

        return "{0} IN {1}".format(self.dispatch(json[0]), valid)

    def _cast(self, json):
        _type = json[1]
        if isinstance(_type, dict):
            _type = list(_type.keys())[0]
        return "cast({0} AS {1})".format(json[0], _type)
