#!/usr/bin/env python3
"""
Lightweight local CRM. Run: python crm.py
Then open http://localhost:5050
"""
import json
import os
from datetime import date
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

BASE = os.path.dirname(os.path.abspath(__file__))
KNOWN_FILE = os.path.join(BASE, "contacts", "known.json")
PROSPECTS_FILE = os.path.join(BASE, "contacts", "prospects.json")


def load(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        data = json.load(f)
    return [x for x in data if "_comment" not in x and "_example" not in x]


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CRM</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, sans-serif; background: #f5f5f0; color: #222; padding: 24px; }
  h1 { font-size: 1.4rem; margin-bottom: 24px; color: #111; }
  .tabs { display: flex; gap: 8px; margin-bottom: 24px; }
  .tab { padding: 8px 20px; border-radius: 6px; cursor: pointer; background: #e0e0da; border: none; font-size: 0.95rem; }
  .tab.active { background: #222; color: #fff; }
  .section { display: none; }
  .section.active { display: block; }
  .card { background: #fff; border-radius: 10px; padding: 20px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }
  .card h3 { font-size: 1rem; margin-bottom: 4px; }
  .card .meta { color: #666; font-size: 0.85rem; margin-bottom: 8px; }
  .card .notes { font-size: 0.9rem; color: #444; }
  .badge { display: inline-block; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; margin-left: 8px; }
  .badge.not_contacted { background: #fee; color: #c00; }
  .badge.in_progress { background: #ffd; color: #860; }
  .badge.done { background: #dfd; color: #060; }
  form { display: flex; flex-direction: column; gap: 14px; max-width: 580px; }
  label { font-size: 0.85rem; font-weight: 600; color: #555; margin-bottom: 4px; display: block; }
  input, textarea, select { width: 100%; padding: 9px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 0.95rem; font-family: inherit; background: #fafaf8; }
  textarea { min-height: 80px; resize: vertical; }
  button[type=submit] { padding: 10px 24px; background: #222; color: #fff; border: none; border-radius: 6px; font-size: 0.95rem; cursor: pointer; align-self: flex-start; }
  button[type=submit]:hover { background: #444; }
  .form-section { background: #fff; border-radius: 10px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }
  .form-section h2 { font-size: 1rem; margin-bottom: 18px; color: #333; }
  .list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
  .list-header h2 { font-size: 1rem; color: #333; }
  .count { font-size: 0.85rem; color: #888; }
  .empty { color: #aaa; font-size: 0.9rem; padding: 12px 0; }
  .toast { position: fixed; top: 20px; right: 20px; background: #222; color: #fff; padding: 12px 20px; border-radius: 8px; font-size: 0.9rem; display: none; }
  .delete-btn { float: right; background: none; border: none; color: #ccc; cursor: pointer; font-size: 1rem; }
  .delete-btn:hover { color: #c00; }
</style>
</head>
<body>
<h1>CRM</h1>
<div class="tabs">
  <button class="tab active" onclick="switchTab('known')">Known contacts</button>
  <button class="tab" onclick="switchTab('prospects')">Prospects</button>
</div>

<!-- KNOWN -->
<div id="tab-known" class="section active">
  <div class="form-section">
    <h2>Add known contact</h2>
    <form onsubmit="addKnown(event)">
      <div>
        <label>Name *</label>
        <input name="name" required placeholder="Jane Smith">
      </div>
      <div>
        <label>Handle / link</label>
        <input name="handle" placeholder="@janesmith or linkedin URL">
      </div>
      <div>
        <label>How do you know them? *</label>
        <input name="context" required placeholder="Met at NeurIPS, Twitter mutual, ...">
      </div>
      <div>
        <label>What do they do?</label>
        <input name="what_they_do" placeholder="PhD @ MIT, generative 3D models">
      </div>
      <div>
        <label>Notes (last talked about, anything worth noting)</label>
        <textarea name="notes" placeholder="Interested in the arena idea. Mentioned they're working on..."></textarea>
      </div>
      <div>
        <label>Public info (role, org, links — freeform)</label>
        <textarea name="public_info" placeholder="Autodesk Research, open-sourced XYZ dataset, website: ..."></textarea>
      </div>
      <button type="submit">Add contact</button>
    </form>
  </div>

  <div class="list-header">
    <h2>Known contacts</h2>
    <span class="count" id="known-count"></span>
  </div>
  <div id="known-list"></div>
</div>

<!-- PROSPECTS -->
<div id="tab-prospects" class="section">
  <div class="form-section">
    <h2>Add prospect</h2>
    <form onsubmit="addProspect(event)">
      <div>
        <label>Name *</label>
        <input name="name" required placeholder="Alex Chen">
      </div>
      <div>
        <label>Handle / link</label>
        <input name="handle" placeholder="@alexchen or linkedin URL">
      </div>
      <div>
        <label>Why relevant? *</label>
        <input name="why_relevant" required placeholder="Runs ML-for-manufacturing newsletter, potential distribution">
      </div>
      <div>
        <label>Role</label>
        <input name="role" placeholder="ML Engineer">
      </div>
      <div>
        <label>Org</label>
        <input name="org" placeholder="Autodesk Research">
      </div>
      <div>
        <label>Notable (what makes them interesting)</label>
        <textarea name="notable" placeholder="Open-sourced a CadQuery dataset, 5k Twitter followers in the space"></textarea>
      </div>
      <div>
        <label>Status</label>
        <select name="status">
          <option value="not_contacted">Not contacted</option>
          <option value="in_progress">In progress</option>
          <option value="done">Done</option>
        </select>
      </div>
      <button type="submit">Add prospect</button>
    </form>
  </div>

  <div class="list-header">
    <h2>Prospects</h2>
    <span class="count" id="prospects-count"></span>
  </div>
  <div id="prospects-list"></div>
</div>

<div class="toast" id="toast">Saved!</div>

<script>
function switchTab(name) {
  document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', ['known','prospects'][i] === name));
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
}

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.display = 'block';
  setTimeout(() => t.style.display = 'none', 2000);
}

async function loadKnown() {
  const res = await fetch('/api/known');
  const data = await res.json();
  const el = document.getElementById('known-list');
  document.getElementById('known-count').textContent = data.length + ' people';
  if (!data.length) { el.innerHTML = '<p class="empty">No contacts yet.</p>'; return; }
  el.innerHTML = data.map((c, i) => `
    <div class="card">
      <button class="delete-btn" onclick="deleteKnown(${i})">✕</button>
      <h3>${c.name} <span style="color:#888;font-weight:400;font-size:.85rem">${c.handle||''}</span></h3>
      <div class="meta">${c.context||''} · ${c.what_they_do||''}</div>
      ${c.notes ? `<div class="notes">${c.notes}</div>` : ''}
      ${c.public_info ? `<div class="notes" style="color:#888;margin-top:6px;font-size:.83rem">${c.public_info}</div>` : ''}
    </div>
  `).join('');
}

async function loadProspects() {
  const res = await fetch('/api/prospects');
  const data = await res.json();
  const el = document.getElementById('prospects-list');
  document.getElementById('prospects-count').textContent = data.length + ' people';
  if (!data.length) { el.innerHTML = '<p class="empty">No prospects yet.</p>'; return; }
  el.innerHTML = data.map((p, i) => `
    <div class="card">
      <button class="delete-btn" onclick="deleteProspect(${i})">✕</button>
      <h3>${p.name} <span style="color:#888;font-weight:400;font-size:.85rem">${p.handle||''}</span>
        <span class="badge ${p.status||'not_contacted'}">${(p.status||'not_contacted').replace('_',' ')}</span>
      </h3>
      <div class="meta">${p.public_info?.role||''} ${p.public_info?.org ? '@ '+p.public_info.org : ''}</div>
      <div class="notes">${p.why_relevant||''}</div>
      ${p.public_info?.notable ? `<div class="notes" style="color:#888;margin-top:6px;font-size:.83rem">${p.public_info.notable}</div>` : ''}
    </div>
  `).join('');
}

async function addKnown(e) {
  e.preventDefault();
  const fd = new FormData(e.target);
  const body = Object.fromEntries(fd);
  await fetch('/api/known', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) });
  e.target.reset();
  toast('Contact saved!');
  loadKnown();
}

async function addProspect(e) {
  e.preventDefault();
  const fd = new FormData(e.target);
  const body = Object.fromEntries(fd);
  await fetch('/api/prospects', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) });
  e.target.reset();
  toast('Prospect saved!');
  loadProspects();
}

async function deleteKnown(i) {
  await fetch('/api/known/' + i, { method: 'DELETE' });
  loadKnown();
}

async function deleteProspect(i) {
  await fetch('/api/prospects/' + i, { method: 'DELETE' });
  loadProspects();
}

loadKnown();
loadProspects();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/known", methods=["GET"])
def get_known():
    return jsonify(load(KNOWN_FILE))


@app.route("/api/known", methods=["POST"])
def add_known():
    d = request.json
    contacts = load(KNOWN_FILE)
    contacts.append({
        "name": d.get("name", ""),
        "handle": d.get("handle", ""),
        "context": d.get("context", ""),
        "what_they_do": d.get("what_they_do", ""),
        "notes": d.get("notes", ""),
        "public_info": d.get("public_info", ""),
        "added": date.today().isoformat(),
    })
    save(KNOWN_FILE, contacts)
    return jsonify({"ok": True})


@app.route("/api/known/<int:i>", methods=["DELETE"])
def delete_known(i):
    contacts = load(KNOWN_FILE)
    if 0 <= i < len(contacts):
        contacts.pop(i)
        save(KNOWN_FILE, contacts)
    return jsonify({"ok": True})


@app.route("/api/prospects", methods=["GET"])
def get_prospects():
    return jsonify(load(PROSPECTS_FILE))


@app.route("/api/prospects", methods=["POST"])
def add_prospect():
    d = request.json
    prospects = load(PROSPECTS_FILE)
    prospects.append({
        "name": d.get("name", ""),
        "handle": d.get("handle", ""),
        "why_relevant": d.get("why_relevant", ""),
        "public_info": {
            "role": d.get("role", ""),
            "org": d.get("org", ""),
            "notable": d.get("notable", ""),
        },
        "status": d.get("status", "not_contacted"),
        "added": date.today().isoformat(),
    })
    save(PROSPECTS_FILE, prospects)
    return jsonify({"ok": True})


@app.route("/api/prospects/<int:i>", methods=["DELETE"])
def delete_prospect(i):
    prospects = load(PROSPECTS_FILE)
    if 0 <= i < len(prospects):
        prospects.pop(i)
        save(PROSPECTS_FILE, prospects)
    return jsonify({"ok": True})


if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "contacts"), exist_ok=True)
    print("CRM running at http://localhost:5050")
    app.run(port=5050, debug=False)
