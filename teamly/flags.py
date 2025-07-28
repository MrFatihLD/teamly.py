



class BaseFlags:

    TEXT = (
        'view_channel',
        'manage_messages',
        'send_messages',
        'use_external_emojis',
        'manage_channel',
        'can_see_message_history'
    )

    VOICE = (
        'view_channel',
        'connect',
        'speak',
        'mute_members',
        'deafen_members',
        'move_members',
        'manage_channel',
        'disconnect'
    )

    TODO = (
        'view_channel',
        'manage_todos',
        'create_todos',
        'delete_todos',
        'edit_todos',
        'manage_channel'
    )

    WATCHSTREAM = (
        'view_channel',
        'manage_channel'
    )

    ANNOUNCEMENT = (
        'view_channel',
        'manage_channel',
        'create_announcements',
        'delete_announcements'
    )
