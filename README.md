# bluesky-verifier bot

## Overview

feature overview:
- watches a post on bsky via at:// uri
- creates a verification record for each user who likes the post
- logs the user with their handle and display name to a redis db to both reduce api calls and to monitor for changes
-  if change is detected with display name or handle will send new verification record as changes will invalidate verification

## Quick Start

prereqs: need to have docker and a docker daemon installed

steps:
- take the [example.docker-compose.yml](example.docker-compose.yml)
- replace the env vars with your own values
- run `docker compose up -d` or `docker stack deploy -c docker-compose.yml`

## Docker Stuffs

### var descriptions

| env var                    | usage                                                                            |
|----------------------------|----------------------------------------------------------------------------------|
| BSKY_HANDLE                | the bsky handle you wish to authorize to                                         |
| BSKY_APP_PASSWORD          | generate an app password to use with this bot                                    |
| POST_URI                   | the at:// uri of the post you want to monitor                                    |
| CONSISTENCY_CHECK_INTERVAL | time in seconds between checks to check if handle and display name have changed  |

## Contribute

i mean if you want, i will accept issues and prs if you find something that should be updated, tho this is just a silly little project lol
