from requests.tables import RequestTable


class RequestHomeTable(RequestTable):
    class Meta(RequestTable.Meta):
        exclude = ('assigned_to', 'priority', 'is_proceed', 'closed_on')
