import os
import time
from datetime import datetime, timezone

import redis
from atproto import Client, models

BSKY_HANDLE = os.getenv('BSKY_HANDLE')
BSKY_APP_PASSWORD = os.getenv('BSKY_APP_PASSWORD')
POST_URI = os.getenv('POST_URI')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DB = int(os.getenv('REDIS_DB', '0'))
REDIS_SET_KEY = "verified_dids"
REDIS_HASH_PREFIX = "verified_user:"

# Consistency check interval in seconds, default 1 hour (3600s)
CONSISTENCY_CHECK_INTERVAL = int(os.getenv('CONSISTENCY_CHECK_INTERVAL', '3600'))


def get_redis():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    r.ping()
    return r


def create_verification_record(client, user_did, handle, display_name):
    created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    record = models.AppBskyGraphVerification.Record(
        subject=user_did,
        handle=handle,
        displayName=display_name,
        createdAt=created_at,
    )
    resp = client.com.atproto.repo.create_record({
        'repo': BSKY_HANDLE,
        'collection': 'app.bsky.graph.verification',
        'record': record.model_dump(exclude_none=True),
    })
    print(f"✅ Created verification record for {user_did} ({handle}) at {created_at}: {resp.uri}", flush=True)
    return created_at


def check_likes(client, r, verified_dids):
    likes_resp = client.app.bsky.feed.get_likes({'uri': POST_URI})
    for like in likes_resp.likes:
        user_did = like.actor.did
        if user_did in verified_dids:
            continue

        handle = like.actor.handle
        display_name = like.actor.display_name or handle

        try:
            created_at = create_verification_record(client, user_did, handle, display_name)
            r.sadd(REDIS_SET_KEY, user_did)
            r.hset(f"{REDIS_HASH_PREFIX}{user_did}", mapping={
                "handle": handle,
                "display_name": display_name,
                "created_at": created_at,
            })
            verified_dids.add(user_did)
        except Exception as e:
            print(f"❌ Failed to verify {user_did}: {e}", flush=True)


def consistency_check(client, r, verified_dids):
    print("⏰ Performing consistency check (handle/display name)...", flush=True)
    for user_did in list(verified_dids):
        try:
            user_profile = client.com.atproto.identity.resolve_handle({'handle': user_did})
            new_handle = user_profile['handle']

            actor_profile = client.app.bsky.actor.get_profile({'actor': user_did})
            new_display_name = actor_profile.get('displayName') or new_handle

            hash_key = f"{REDIS_HASH_PREFIX}{user_did}"
            prev_data = r.hgetall(hash_key)
            prev_handle = prev_data.get("handle")
            prev_display_name = prev_data.get("display_name")

            if new_display_name != prev_display_name:
                r.hset(hash_key, "display_name", new_display_name)
                print(f"📝 Updated display_name for {user_did} to '{new_display_name}'", flush=True)

            if new_handle != prev_handle:
                created_at = create_verification_record(client, user_did, new_handle, new_display_name)
                r.hset(hash_key, mapping={
                    "handle": new_handle,
                    "display_name": new_display_name,
                    "created_at": created_at,
                })
                print(f"🔁 Handle for {user_did} changed: {prev_handle} → {new_handle}. Re-verified.", flush=True)

        except Exception as e:
            print(f"⚠️  Failed to check/update handle/display name for {user_did}: {e}", flush=True)


def main():
    print("🚀 Starting Bluesky Verifier Bot initialization...", flush=True)
    print(f"ℹ️  Logging in as '{BSKY_HANDLE}'...", flush=True)
    client = Client()
    client.login(BSKY_HANDLE, BSKY_APP_PASSWORD)
    print(f"✅ Successfully logged in as '{BSKY_HANDLE}'.", flush=True)
    print(f"👁️  Now watching for likes on post: {POST_URI}", flush=True)

    r = get_redis()
    verified_dids = set(r.smembers(REDIS_SET_KEY))
    print(f"ℹ️  Loaded {len(verified_dids)} previously verified DIDs from Redis.", flush=True)

    last_check = time.time()

    while True:
        check_likes(client, r, verified_dids)

        now = time.time()
        if now - last_check > CONSISTENCY_CHECK_INTERVAL:
            consistency_check(client, r, verified_dids)
            last_check = now

        time.sleep(60)


if __name__ == "__main__":
    main()
