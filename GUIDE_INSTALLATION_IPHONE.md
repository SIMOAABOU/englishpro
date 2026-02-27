# 📱 Guide d'installation sur iPhone — EnglishPro

## Étapes simples en 15 minutes (GRATUIT)

---

## 🥇 ÉTAPE 1 : Mettre le code en ligne (GitHub)

**1.1** — Va sur https://github.com et crée un compte gratuit (si pas déjà fait)

**1.2** — Clique sur le bouton vert **"New"** pour créer un nouveau repository

**1.3** — Nom du repo : `englishpro` → Clique **"Create repository"**

**1.4** — Dans la page qui s'ouvre, clique sur **"uploading an existing file"**

**1.5** — Glisse-dépose TOUS les fichiers du dossier `english_app_pwa` :
```
📁 english_app_pwa/
  ├── app.py
  ├── index.html
  ├── requirements.txt
  ├── Procfile
  ├── data/
  │   ├── __init__.py
  │   ├── curriculum.py
  │   └── srs.py
  └── static/
      ├── manifest.json
      ├── sw.js
      ├── icon-192.png
      └── icon-512.png
```

**1.6** — Clique **"Commit changes"** (bouton vert en bas)

---

## 🥈 ÉTAPE 2 : Héberger sur Railway (GRATUIT)

**2.1** — Va sur https://railway.app

**2.2** — Clique **"Start a New Project"**

**2.3** — Choisis **"Deploy from GitHub repo"**

**2.4** — Connecte ton compte GitHub → Sélectionne `englishpro`

**2.5** — Railway détecte automatiquement Flask et déploie !

**2.6** — Va dans **Settings → Networking → Generate Domain**
→ Tu obtiens une URL comme : `englishpro-production.up.railway.app`

⏱️ Attends 2-3 minutes que ça se déploie.

---

## 🥉 ÉTAPE 3 : Installer sur ton iPhone comme une app

**3.1** — Sur ton iPhone, ouvre **Safari** (pas Chrome !)

**3.2** — Tape l'URL de ton app Railway : `https://englishpro-xxx.up.railway.app`

**3.3** — Appuie sur l'icône **Partager** (carré avec flèche vers le haut ↑) en bas

**3.4** — Fais défiler et appuie sur **"Sur l'écran d'accueil"**

**3.5** — Nom : `EnglishPro` → Appuie **"Ajouter"**

✅ L'app apparaît sur ton écran d'accueil comme une vraie app !

---

## 🎉 Résultat

- Icône sur l'écran d'accueil 📱
- S'ouvre en plein écran (pas de barre Safari)
- Fonctionne depuis n'importe où (WiFi ou 4G)
- Ta progression sauvegardée en ligne

---

## ❓ Questions fréquentes

**Q : C'est vraiment gratuit ?**
R : Oui ! Railway offre 500h/mois gratuitement, largement suffisant.

**Q : Mes données sont sécurisées ?**
R : L'app est juste pour toi — pas de compte, pas de données personnelles.

**Q : Je peux l'utiliser sans WiFi ?**
R : Une connexion est nécessaire, mais les pages sont très légères (chargement rapide en 4G).
