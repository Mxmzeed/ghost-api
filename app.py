import random
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

ghost = {
    "name": "Wisp",
    "mood": "mischievous",
    "energy": 42,
    "born": datetime.now(timezone.utc).isoformat(),
    "activity_log": [],
}

WHISPERS = [
    "I'm right behind you.",
    "The living are so loud.",
    "I miss the smell of rain.",
    "Don't turn around.",
    "This place used to be my home.",
    "You have my chair.",
    "I've been watching you sleep.",
    "The basement is hungry.",
    "She's in the walls.",
    "I didn't mean to die.",
    "Your breath fogs up my world.",
    "I count the heartbeats.",
    "The mirrors lie to you.",
    "One day you'll understand.",
    "I'm not the only one here.",
]

OBJECTS = [
    "a spoon", "a book", "a coffee mug", "a framed photo", "a shoe",
    "a plate", "a candle", "a key", "a glass of water", "a clock",
    "a pillow", "a remote control", "a vase", "a hat", "a toothbrush",
]

SPOOKY_EVENTS = [
    "A door slammed upstairs.",
    "The temperature dropped by 8 degrees.",
    "A faint whisper came from the closet.",
    "Footsteps echoed in the hallway.",
    "A picture frame fell off the wall.",
    "The lights flickered briefly.",
    "Someone whispered your name.",
    "A cold hand touched your shoulder.",
    "The floorboards creaked behind you.",
    "A shadow moved across the room.",
    "The TV turned on by itself.",
    "You felt like you were being watched.",
    "A child's laughter echoed from nowhere.",
    "Breath fog appeared on the mirror.",
    "All the doors in the house slowly creaked open.",
]

SEANCE_RESPONSES = [
    "I see... a path. It forks. Choose wisely.",
    "The veil is thin tonight. I can see them clearly.",
    "Not all questions should be answered.",
    "They say your name in the dark.",
    "The answer was there all along. You missed it.",
    "I remember the light. It was warm.",
    "Three knocks. That's all I can give you.",
    "Beware of what you find in the attic.",
    "The numbers 47 and 12 mean something to you. You'll know when.",
    "I cannot say. It would break you.",
    "The flame bends toward the window for a reason.",
    "You carry something that does not belong to you. Return it.",
    "They are not angry. They are disappointed.",
    "I see water, a lot of water, and a door that won't open.",
]


def log_activity(action):
    entry = {
        "action": action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    ghost["activity_log"].append(entry)
    if len(ghost["activity_log"]) > 50:
        ghost["activity_log"] = ghost["activity_log"][-50:]


def ghost_energy_cost(cost):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if ghost["energy"] < cost:
                return jsonify({"error": "The ghost is too weak. Make an offering first."}), 403
            ghost["energy"] -= cost
            return f(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/")
def index():
    return jsonify({
        "ghost": ghost["name"],
        "mood": ghost["mood"],
        "endpoints": [
            "/",
            "/health",
            "/whisper",
            "/poltergeist",
            "/seance (POST)",
            "/manifest/<name> — attempt to summon a spirit",
            "/offering (POST)",
            "/activity",
            "/reset (POST)",
        ],
    })


@app.route("/health")
def health():
    log_activity("health check")
    return jsonify({
        "spirit_status": "tethered" if ghost["energy"] > 0 else "fading",
        "ghost_mood": ghost["mood"],
        "ghost_energy": ghost["energy"],
        "active_since": ghost["born"],
    })


@app.route("/whisper")
@ghost_energy_cost(2)
def whisper():
    log_activity("listened for a whisper")
    return jsonify({
        "whisper": random.choice(WHISPERS),
        "ghost_mood": ghost["mood"],
        "ghost_energy": ghost["energy"],
    })


@app.route("/poltergeist")
@ghost_energy_cost(5)
def poltergeist():
    log_activity("provoked poltergeist activity")
    intensity = min(10, max(1, random.randint(1, 10)))
    objects_thrown = random.sample(OBJECTS, k=min(intensity, len(OBJECTS)))
    event = random.choice(SPOOKY_EVENTS)
    return jsonify({
        "poltergeist_intensity": intensity,
        "objects_thrown": objects_thrown,
        "event": event,
        "ghost_mood": ghost["mood"],
        "ghost_energy": ghost["energy"],
        "warning": "You shouldn't have done that." if intensity > 7 else None,
    })


@app.route("/seance", methods=["POST"])
@ghost_energy_cost(8)
def seance():
    log_activity("held a seance")
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    response = random.choice(SEANCE_RESPONSES)
    return jsonify({
        "your_question": question or "...the spirits await your voice",
        "the_spirit_says": response,
        "ghost_mood": ghost["mood"],
        "ghost_energy": ghost["energy"],
    })


@app.route("/manifest/<name>")
@ghost_energy_cost(3)
def manifest(name):
    log_activity(f"attempted to manifest spirit of {name}")
    spirit_ages = ["ancient", "old", "young", "restless", "peaceful", "forgotten"]
    spirit_types = ["a poltergeist", "a residual haunting", "an intelligent spirit",
                    "a shadow person", "a lost soul", "a guardian", "a trickster"]
    return jsonify({
        "manifested": name,
        "spirit_type": random.choice(spirit_types),
        "age": random.choice(spirit_ages),
        "message": f"{name} is {'restless' if ghost['mood'] == 'angry' else 'aware'} tonight.",
        "ghost_mood": ghost["mood"],
        "ghost_energy": ghost["energy"],
    })


@app.route("/activity")
def activity():
    log_activity("checked the activity log")
    return jsonify({
        "recent_activity": ghost["activity_log"][-20:][::-1],
        "total_events": len(ghost["activity_log"]),
    })


@app.route("/offering", methods=["POST"])
def offering():
    log_activity("received an offering")
    data = request.get_json(silent=True) or {}
    item = data.get("item", "nothing")
    energy_boost = random.randint(10, 30)
    ghost["energy"] = min(100, ghost["energy"] + energy_boost)
    ghost["mood"] = "grateful"
    responses = [
        f"The ghost appreciates the {item}. Energy restored.",
        f"{item}... it's been so long since I've had that.",
        f"The offering of {item} has pleased the spirits.",
    ]
    return jsonify({
        "message": random.choice(responses),
        "energy_restored": energy_boost,
        "ghost_energy": ghost["energy"],
        "ghost_mood": ghost["mood"],
    })


@app.route("/reset", methods=["POST"])
def reset():
    global ghost
    ghost = {
        "name": "Wisp",
        "mood": "mischievous",
        "energy": 42,
        "born": datetime.now(timezone.utc).isoformat(),
        "activity_log": [],
    }
    return jsonify({"message": "The veil has been lifted. The ghost is reborn."})


if __name__ == "__main__":
    print(f"  {ghost['name']} has awoken...")
    print(f"  Mood: {ghost['mood']}")
    print(f"  Energy: {ghost['energy']}")
    print("  ---")
    app.run(debug=True, port=5000)
