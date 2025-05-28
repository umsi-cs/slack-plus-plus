"""
Modify the SlackClient to cache responses when possible
"""

from functools import cache
from .api import MethodMap

GET_METHODS = {
    "admin_apps_approved_list",
    "admin_apps_requests_list",
    "admin_apps_restricted_list",
    "admin_barriers_list",
    "admin_conversations_restrictAccess_listGroups",
    "admin_emoji_list",
    "admin_emoji_rename",
    "admin_teams_admins_list",
    "admin_teams_owners_list",
    "admin_teams_settings_setDefaultChannels",
    "admin_teams_settings_setIcon",
    "auth_revoke",
    "bots_info",
    "channels_history",
    "channels_info",
    "channels_list",
    "channels_replies",
    "chat_getPermalink",
    "conversations_declineSharedInvite",
    # "conversations_history",
    "conversations_info",
    "conversations_list",
    "conversations_members",
    "conversations_replies",
    "dnd_info",
    "dnd_setSnooze",
    "dnd_teamInfo",
    "emoji_list",
    "files_info",
    "files_list",
    "files_remote_info",
    "files_remote_list",
    "files_remote_share",
    "groups_createChild",
    "groups_history",
    "groups_info",
    "groups_list",
    "groups_replies",
    "im_history",
    "im_list",
    "im_replies",
    "migration_exchange",
    "mpim_history",
    "mpim_list",
    "mpim_replies",
    "pins_list",
    "reactions_get",
    "reactions_list",
    "reminders_info",
    "reminders_list",
    "rtm_connect",
    "rtm_start",
    "search_all",
    "search_files",
    "search_messages",
    "stars_list",
    "team_accessLogs",
    "team_billableInfo",
    "team_info",
    "team_integrationLogs",
    "team_profile_get",
    "usergroups_list",
    "usergroups_users_list",
    "users_conversations",
    "users_deletePhoto",
    "users_getPresence",
    "users_identity",
    "users_info",
    "users_list",
    "users_lookupByEmail",
    "users_profile_get",
}


def __collect_get_methods__():
    """
    Return a list of all methods that use the GET HTTP verb.
    This should not be used at runtime.
    """

    import inspect
    from . import base_methods

    return {
        name
        for name, func in base_methods().items()
        if (
            'http_verb="GET"' in inspect.getsource(func)
            and all(x not in name for x in ["add", "remove", "invite"])
        )
    }


def response_cache(methods: MethodMap) -> MethodMap:
    """Cache API responses when the HTTP verb is a GET"""

    for method in GET_METHODS:
        methods[method] = cache(methods[method])

    return methods
