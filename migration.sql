CREATE TABLE [IF NOT EXISTS] cogpreferences (
    serverid text,
    fun boolean,
    reddit boolean,
    games boolean,
    ai boolean,
    animals boolean,
    image boolean,
    tags boolean,
    text boolean,
    util boolean,
    smart boolean,
    memes boolean,
    misc boolean

)

CREATE TABLE [IF NOT EXISTS] prefixesandstuff (
    on_message_perm boolean,
    server_id text,
    command_prefix text
)

CREATE TABLE [IF NOT EXISTS] automeme (
    server_id bigint,
    webhook_url text,
    active boolean
)
