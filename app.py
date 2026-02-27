"""
Backend Flask - English Learning App
API REST pour toutes les fonctionnalités
"""

from flask import Flask, jsonify, request, send_from_directory
import os
import sys
import json

sys.path.insert(0, os.path.dirname(__file__))
from data.curriculum import get_day_data, CURRICULUM
from data.srs import (load_progress, save_progress, init_word_card, sm2_update,
                       get_due_words, get_stats, save_session_result, add_xp, get_word_key)

app = Flask(__name__, static_folder='static', static_url_path='/static')

# ==================== ROUTES FRONTEND ====================


@app.route('/static/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/static/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json', mimetype='application/manifest+json')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ==================== API PROGRESS ====================

@app.route('/api/progress', methods=['GET'])
def get_progress():
    progress = load_progress()
    stats = get_stats(progress)
    return jsonify({
        "user": progress["user"],
        "stats": stats,
        "recent_sessions": progress["sessions"][-5:] if progress["sessions"] else []
    })

@app.route('/api/progress/setup', methods=['POST'])
def setup_user():
    data = request.json
    progress = load_progress()
    progress["user"]["name"] = data.get("name", "Learner")
    save_progress(progress)
    return jsonify({"success": True, "user": progress["user"]})

# ==================== API CURRICULUM ====================

@app.route('/api/day/<int:day>', methods=['GET'])
def get_day(day):
    if day < 1 or day > 90:
        return jsonify({"error": "Day must be between 1 and 90"}), 400
    
    day_data = get_day_data(day)
    progress = load_progress()
    
    # Ajouter statut de chaque mot
    words_with_status = []
    for word in day_data["words"]:
        key = get_word_key(day, word["word"])
        card = progress["words"].get(key, None)
        word_status = {
            **word,
            "key": key,
            "seen": card is not None,
            "mastered": card["correct_count"] >= 3 if card else False,
            "correct_count": card["correct_count"] if card else 0
        }
        words_with_status.append(word_status)
    
    return jsonify({
        "day": day,
        "theme": day_data["theme"],
        "situation": day_data["situation"],
        "emoji": day_data["emoji"],
        "words": words_with_status,
        "total_words": len(words_with_status)
    })

# ==================== API SESSIONS ====================

@app.route('/api/session/start', methods=['POST'])
def start_session():
    """Démarrer une session d'apprentissage"""
    data = request.json
    day = data.get("day", 1)
    mode = data.get("mode", "flashcard")  # flashcard, quiz, pronunciation
    
    day_data = get_day_data(day)
    progress = load_progress()
    
    # Initialiser les cartes pour les nouveaux mots
    for word in day_data["words"]:
        key = get_word_key(day, word["word"])
        if key not in progress["words"]:
            progress["words"][key] = init_word_card(word)
    
    save_progress(progress)
    
    return jsonify({
        "session_started": True,
        "day": day,
        "mode": mode,
        "words": day_data["words"][:10]  # 10 mots par session
    })

@app.route('/api/session/answer', methods=['POST'])
def submit_answer():
    """Soumettre une réponse"""
    data = request.json
    word_key = data.get("word_key")
    quality = data.get("quality", 3)  # 0-5
    day = data.get("day", 1)
    mode = data.get("mode", "flashcard")
    
    progress = load_progress()
    
    if word_key in progress["words"]:
        progress["words"][word_key] = sm2_update(progress["words"][word_key], quality)
    
    save_progress(progress)
    
    # XP par réponse
    xp = 5 if quality >= 3 else 1
    progress = add_xp(progress, xp)
    save_progress(progress)
    
    return jsonify({
        "success": True,
        "xp_earned": xp,
        "level": progress["user"]["level"],
        "total_xp": progress["user"]["total_xp"]
    })

@app.route('/api/session/complete', methods=['POST'])
def complete_session():
    """Terminer une session"""
    data = request.json
    day = data.get("day", 1)
    score = data.get("score", 0)
    total = data.get("total", 10)
    mode = data.get("mode", "flashcard")
    
    progress = load_progress()
    progress = save_session_result(progress, day, score, total, mode)
    save_progress(progress)
    
    stats = get_stats(progress)
    
    return jsonify({
        "success": True,
        "percentage": round(score / total * 100) if total > 0 else 0,
        "stats": stats,
        "level": progress["user"]["level"],
        "streak": progress["user"]["streak"],
        "total_xp": progress["user"]["total_xp"]
    })

# ==================== API REVIEW (SRS) ====================

@app.route('/api/review', methods=['GET'])
def get_review_words():
    """Obtenir les mots dus pour révision"""
    progress = load_progress()
    due = get_due_words(progress, progress["user"]["current_day"])
    
    # Enrichir avec les données des mots
    review_words = []
    for item in due[:20]:  # Max 20 mots en révision
        key = item["key"]
        parts = key.split("_", 1)
        if len(parts) >= 2:
            day_str = parts[0].replace("d", "")
            try:
                day = int(day_str)
                day_data = get_day_data(day)
                word_name = item["card"]["word"]
                for w in day_data["words"]:
                    if w["word"] == word_name:
                        review_words.append({**w, "key": key, "card": item["card"]})
                        break
            except:
                pass
    
    return jsonify({
        "review_count": len(due),
        "words": review_words
    })

# ==================== API STATS ====================

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    progress = load_progress()
    stats = get_stats(progress)
    
    # Progression sur 7 jours
    from datetime import datetime, timedelta
    daily_data = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).date().isoformat()
        sessions = progress["daily_scores"].get(date, [])
        avg = sum(s["percentage"] for s in sessions) / len(sessions) if sessions else 0
        daily_data.append({"date": date, "score": round(avg), "sessions": len(sessions)})
    
    return jsonify({
        **stats,
        "daily_progress": daily_data,
        "level_details": get_level_details(progress["user"]["total_xp"])
    })

def get_level_details(xp: int) -> dict:
    levels = [
        ("A1", 0, 500),
        ("A2", 500, 1500),
        ("B1", 1500, 4000),
        ("B1+", 4000, 8000),
        ("B2", 8000, 15000),
        ("B2+", 15000, 25000),
        ("C1", 25000, 50000),
    ]
    
    for level, min_xp, max_xp in levels:
        if min_xp <= xp < max_xp:
            progress_pct = round((xp - min_xp) / (max_xp - min_xp) * 100)
            return {
                "current": level,
                "xp": xp,
                "min_xp": min_xp,
                "max_xp": max_xp,
                "progress_pct": progress_pct,
                "xp_to_next": max_xp - xp
            }
    
    return {"current": "C1", "xp": xp, "min_xp": 25000, "max_xp": 50000, "progress_pct": 100, "xp_to_next": 0}

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    print(f"🚀 English Learning App démarrée sur port {port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
