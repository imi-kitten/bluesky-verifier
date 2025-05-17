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


def get_redis():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    r.ping()
    return r


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

    while True:
        likes_resp = client.app.bsky.feed.get_likes({'uri': POST_URI})
        for like in likes_resp.likes:
            user_did = like.actor.did

            if user_did in verified_dids:
                continue

            try:
                handle = like.actor.handle
                display_name = like.actor.display_name or handle
                created_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

                # Create verification record for ATProto
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
                print(f"✅ Created verification record for {user_did}: {resp.uri}", flush=True)

                # Add to Redis set and log handle/display_name/created_at as a hash (no did)
                r.sadd(REDIS_SET_KEY, user_did)
                r.hset(f"{REDIS_HASH_PREFIX}{user_did}", mapping={
                    "handle": handle,
                    "display_name": display_name,
                    "created_at": created_at,
                })

                verified_dids.add(user_did)
            except Exception as e:
                print(f"❌ Failed to verify {user_did}: {e}", flush=True)

        time.sleep(60)


if __name__ == "__main__":
    main()
