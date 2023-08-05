from pnplabs.utils.firestore import get_uid


def get_commands(db_client, api_key):
    teams_ids = [x.id for x in db_client.collection("teams").where("members", "array_contains", get_uid(api_key)).stream()]
    commands = [x.to_dict() for x in db_client.collection("commands").where(u"audience", u'in', [get_uid(api_key)] + teams_ids).stream()]
    return commands
