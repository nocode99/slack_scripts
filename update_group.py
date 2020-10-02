import os

from slack import WebClient

SLACK_TOKEN = os.environ["SLACK_TOKEN"]
ACTIVE_MEMBERS = []
# Set the session
CLIENT = WebClient(token=SLACK_TOKEN)

def get_usergroup_id(group_name):
    """
    Returns the unique id of a user group
    """
    response = CLIENT.usergroups_list()
    usergroups = response['usergroups']
    for usergroup in usergroups:
        if usergroup['handle'] == group_name:
            return usergroup['id']


def get_user_ids():
    """
    Appends to `ACTIVE_MEMBERS` of all active billed members ids
    """
    users = CLIENT.users_list()
    members = users['members']
    billing = CLIENT.team_billableInfo()
    billable_info = billing['billable_info']

    for member in members:
        # check that user is not a bot, deleted or a guest (single, multi-channel)
        if not member['deleted'] and not member['is_bot'] and not member['is_restricted'] and not member['is_ultra_restricted']:
            member_id = member['id']
            # print(member['name'])
            # check to see if the user is a billable user
            if member_id in billable_info:
                # verify they are an active billed user
                if billable_info[member_id]['billing_active']:
                    ACTIVE_MEMBERS.append(member['id'])

def main():
    get_user_ids()
    group_id = get_usergroup_id("*********ADD_ARG**********")
    CLIENT.usergroups_users_update(
        usergroup = group_id,
        users = ACTIVE_MEMBERS
    )

if __name__ == "__main__":
    main()
