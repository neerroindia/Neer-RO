from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
INDEX_SOURCE = UPLOADS_DIR / "index.html"
ADMIN_SOURCE = UPLOADS_DIR / "admin.html"
HOST = "0.0.0.0"
PORT = 8000

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyD2zVKUFGJWlWJDW7eNzrLDJ69l8Evx-Ew",
    "authDomain": "neer-ro-india.firebaseapp.com",
    "databaseURL": "https://neer-ro-india-default-rtdb.firebaseio.com",
    "projectId": "neer-ro-india",
    "storageBucket": "neer-ro-india.firebasestorage.app",
    "messagingSenderId": "71113736436",
    "appId": "1:71113736436:web:53b1d83bb0e03ce1171ea1",
}

# Fixed single admin login requested by user.
ADMIN_LOGIN_EMAIL = "admin@mail.com"
ADMIN_LOGIN_PASSWORD = "n1m2a3828"
ADMIN_ALLOWLIST = [
    ADMIN_LOGIN_EMAIL,
]

DEFAULT_SETTINGS = {
    "logo": "",
    "brand": "NEER",
    "tag": "PREMIUM RO · NEERRO.IN",
    "headFont": "'Archivo Black',sans-serif",
    "bodyFont": "'Inter',sans-serif",
    "color1": "#22d3ee",
    "color2": "#0a0e1a",
}

DEFAULT_PRODUCTS = [
    {
        "id": 101,
        "nm": "Neer Classic",
        "name": "Neer Classic",
        "cat": "Entry Level",
        "category": "Entry Level",
        "pr": 5999,
        "price": 5999,
        "mrp": 8999,
        "img": "",
        "ft": ["16L Storage", "5-Stage", "TDS Controller", "1 Year Warranty"],
        "bdg": "Best Value",
        "badge": "Best Value",
        "desc": "Premium entry-level RO.",
        "warranty": "1 Year",
        "status": "active",
    },
    {
        "id": 102,
        "nm": "Neer Premium",
        "name": "Neer Premium",
        "cat": "Mid Range",
        "category": "Mid Range",
        "pr": 7999,
        "price": 7999,
        "mrp": 11999,
        "img": "",
        "ft": ["Copper+Alkaline", "Auto Flush", "16L Storage", "TDS Adjuster"],
        "bdg": "Popular",
        "badge": "Popular",
        "desc": "Copper purifier.",
        "warranty": "1 Year",
        "status": "active",
    },
    {
        "id": 103,
        "nm": "Neer Smart",
        "name": "Neer Smart",
        "cat": "Premium",
        "category": "Premium",
        "pr": 10999,
        "price": 10999,
        "mrp": 15999,
        "img": "",
        "ft": ["15L Tank", "LED TDS", "Auto TDS", "Smart Indicator"],
        "bdg": "Smart Choice",
        "badge": "Smart Choice",
        "desc": "Smart IoT purifier.",
        "warranty": "1 Year",
        "status": "active",
    },
]

DEFAULT_SPARES = [
    {"id": 201, "nm": "Spun Filter", "name": "Spun Filter", "pr": 99, "price": 99, "mrp": 199, "prTxt": "₹79–₹129", "img": "", "ic": "fa-filter", "desc": "PP spun filter.", "status": "active"},
    {"id": 202, "nm": "Bio Alkaline", "name": "Bio Alkaline", "pr": 399, "price": 399, "mrp": 599, "prTxt": "₹399", "img": "", "ic": "fa-leaf", "desc": "Alkaline filter.", "status": "active"},
    {"id": 203, "nm": "Pre Carbon", "name": "Pre Carbon", "pr": 399, "price": 399, "mrp": 599, "prTxt": "₹399", "img": "", "ic": "fa-fire", "desc": "Carbon filter.", "status": "active"},
    {"id": 204, "nm": "UV Filter", "name": "UV Filter", "pr": 499, "price": 499, "mrp": 799, "prTxt": "₹499", "img": "", "ic": "fa-sun", "desc": "UV sterilization.", "status": "active"},
    {"id": 205, "nm": "RO Membrane 100GPD", "name": "RO Membrane 100GPD", "pr": 799, "price": 799, "mrp": 1299, "prTxt": "₹799", "img": "", "ic": "fa-circle-notch", "desc": "100GPD membrane.", "status": "active"},
    {"id": 206, "nm": "TDS Controller", "name": "TDS Controller", "pr": 199, "price": 199, "mrp": 349, "prTxt": "₹199", "img": "", "ic": "fa-sliders-h", "desc": "TDS adjuster.", "status": "active"},
    {"id": 207, "nm": "Pump 100G", "name": "Pump 100G", "pr": 999, "price": 999, "mrp": 1599, "prTxt": "₹999", "img": "", "ic": "fa-tachometer-alt", "desc": "Booster pump.", "status": "active"},
]

DEFAULT_REVIEWS = [
    {"id": "r1", "nm": "Rajesh Kumar", "name": "Rajesh Kumar", "prod": "Neer Smart", "location": "Delhi NCR", "rating": 5, "text": "Amazing product!", "date": "20 Dec 2024", "status": "published"},
    {"id": "r2", "nm": "Priya Sharma", "name": "Priya Sharma", "prod": "Neer Premium", "location": "Mumbai", "rating": 5, "text": "Copper filter excellent.", "date": "18 Dec 2024", "status": "published"},
    {"id": "r3", "nm": "Arun Mehta", "name": "Arun Mehta", "prod": "Neer Classic", "location": "Bangalore", "rating": 4, "text": "Great value!", "date": "15 Dec 2024", "status": "published"},
]

DEFAULT_ANNOUNCEMENTS = [
    {"id": "a1", "icon": "fa-tag", "msg": "Book Above ₹5,999 → FREE Installation", "status": "active"},
    {"id": "a2", "icon": "fa-percent", "msg": "Coupon: NEER100 for ₹100 Off", "status": "active"},
    {"id": "a3", "icon": "fa-shield-alt", "msg": "1 Year Warranty + Free Service", "status": "active"},
]

DEFAULT_COUPONS = [
    {"id": "c1", "code": "NEER100", "type": "flat", "value": 100, "desc": "₹100 off above ₹5,999", "min": 5999, "maxUses": 100, "used": 42, "end": "2025-01-31", "status": "active"},
    {"id": "c2", "code": "WELCOME10", "type": "percent", "value": 10, "desc": "10% off first order", "min": 0, "maxUses": 500, "used": 128, "end": "2025-12-31", "status": "active"},
]

def _admin_rule_expr() -> str:
    emails = [email.strip().lower() for email in ADMIN_ALLOWLIST if email.strip()]
    if not emails:
        return "false"
    checks = " || ".join(f"auth.token.email === '{email}'" for email in emails)
    return f"auth != null && ({checks})"


ADMIN_RULE_EXPR = _admin_rule_expr()
ADMIN_ACCESS_EXPR = f"(root.child('meta/admins').child(auth.uid).val() === true || ({ADMIN_RULE_EXPR}))"

FIREBASE_RULES_HINT = {
    "rules": {
        ".read": True,
        "site": {
            ".read": True,
            ".write": ADMIN_ACCESS_EXPR,
        },
        "customers": {
            "$uid": {
                ".read": f"auth != null && (auth.uid === $uid || {ADMIN_ACCESS_EXPR})",
                ".write": f"auth != null && (auth.uid === $uid || {ADMIN_ACCESS_EXPR})",
            }
        },
        "orders": {
            "$orderId": {
                ".read": f"auth != null && (data.child('customer_uid').val() === auth.uid || data.child('customer_id').val() === auth.uid || {ADMIN_ACCESS_EXPR})",
                ".write": f"auth != null && (newData.child('customer_uid').val() === auth.uid || newData.child('customer_id').val() === auth.uid || {ADMIN_ACCESS_EXPR})",
            }
        },
        "notifications": {
            ".read": "auth != null",
            "$notificationId": {
                ".write": ADMIN_ACCESS_EXPR,
            },
        },
        "meta": {
            "admins": {
                ".read": ADMIN_ACCESS_EXPR,
                "$uid": {
                    ".write": f"auth != null && ((auth.uid === $uid && ({ADMIN_RULE_EXPR})) || {ADMIN_ACCESS_EXPR})",
                },
            }
        },
    }
}


def js(value) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


COMMON_FIREBASE_SDK = """
<script src=\"https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js\"></script>
<script src=\"https://www.gstatic.com/firebasejs/10.12.2/firebase-auth-compat.js\"></script>
<script src=\"https://www.gstatic.com/firebasejs/10.12.2/firebase-database-compat.js\"></script>
<script src=\"https://www.gstatic.com/firebasejs/10.12.2/firebase-storage-compat.js\"></script>
""".strip()

INDEX_SYNC_TEMPLATE = r"""
<!-- ===== FIREBASE SYNC ENGINE ===== -->
__COMMON_SDK__
<script>
(function(){
  const firebaseConfig = __FIREBASE_CONFIG__;
  const PUBLIC_APP_NAME = 'neer-public-app';
  let publicApp;
  try { publicApp = firebase.app(PUBLIC_APP_NAME); }
  catch (e) { publicApp = firebase.initializeApp(firebaseConfig, PUBLIC_APP_NAME); }
  const fbAuth = publicApp.auth();
  const fbDb = publicApp.database();
  const fbStorage = publicApp.storage();
  fbAuth.setPersistence(firebase.auth.Auth.Persistence.LOCAL).catch(function(err){ console.warn('Public auth persistence error', err); });
  window.__NEER_FB__ = { auth: fbAuth, db: fbDb, storage: fbStorage, app: publicApp };

  function clone(v){ return JSON.parse(JSON.stringify(v)); }
  function asArray(v){
    if(!v) return [];
    if(Array.isArray(v)) return v.filter(Boolean);
    return Object.keys(v).map(function(k){ return v[k]; }).filter(Boolean);
  }
  function sortByDate(list){
    return (list||[]).slice().sort(function(a,b){
      return new Date(b && (b.created_at || b.updated_at || b.date) || 0) - new Date(a && (a.created_at || a.updated_at || a.date) || 0);
    });
  }

  var DEF_SET = __DEF_SET__;
  var DEF_PROD = __DEF_PROD__;
  var DEF_SPARE = __DEF_SPARE__;
  var DEF_REV = __DEF_REV__;
  var DEF_ANN = __DEF_ANN__;
  var DEF_COUP = __DEF_COUP__;

  var __store = {
    settings: clone(DEF_SET),
    products: clone(DEF_PROD),
    spares: clone(DEF_SPARE),
    orders: [],
    customers: [],
    reviews: clone(DEF_REV),
    announcements: clone(DEF_ANN),
    notifications: [],
    coupons: clone(DEF_COUP)
  };

  window.DB = {
    save:function(k,d){ __store[k] = clone(d); return true; },
    load:function(k,def){ return __store[k] !== undefined ? clone(__store[k]) : def; }
  };

  var siteSettings = DB.load('settings', DEF_SET);
  var products = DB.load('products', DEF_PROD);
  var spares = DB.load('spares', DEF_SPARE);
  var orders = DB.load('orders', []);
  var customers = DB.load('customers', []);
  var reviews = DB.load('reviews', DEF_REV);
  var announcements = DB.load('announcements', DEF_ANN);
  var notifications = DB.load('notifications', []);
  var coupons = DB.load('coupons', DEF_COUP);

  window.siteSettings = siteSettings;
  window.products = products;
  window.spares = spares;
  window.orders = orders;
  window.customers = customers;
  window.reviews = reviews;
  window.announcements = announcements;
  window.notifications = notifications;
  window.coupons = coupons;

  function setGlobalStore(){
    window.siteSettings = siteSettings;
    window.products = products;
    window.spares = spares;
    window.orders = orders;
    window.customers = customers;
    window.reviews = reviews;
    window.announcements = announcements;
    window.notifications = notifications;
    window.coupons = coupons;
    __store.settings = clone(siteSettings);
    __store.products = clone(products);
    __store.spares = clone(spares);
    __store.orders = clone(orders);
    __store.customers = clone(customers);
    __store.reviews = clone(reviews);
    __store.announcements = clone(announcements);
    __store.notifications = clone(notifications);
    __store.coupons = clone(coupons);
  }

  window.compImg = function compImg(dataUrl, maxWidth, quality, callback){
    var img = new Image();
    img.onload = function(){
      var width = img.width;
      var height = img.height;
      if(width > maxWidth){
        height = Math.round(height * (maxWidth / width));
        width = maxWidth;
      }
      var canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      var ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, width, height);
      callback(canvas.toDataURL('image/jpeg', quality));
    };
    img.onerror = function(){ callback(dataUrl); };
    img.src = dataUrl;
  }

  window.applySettings = function(){
    var s = siteSettings || {};
    if(s.color1){
      document.documentElement.style.setProperty('--cyan', s.color1);
      document.documentElement.style.setProperty('--cyanD', s.color1);
    }
    if(s.headFont) document.documentElement.style.setProperty('--headFont', s.headFont);
    if(s.bodyFont){
      document.documentElement.style.setProperty('--bodyFont', s.bodyFont);
      document.body.style.fontFamily = s.bodyFont;
    }
    document.querySelectorAll('[data-logo]').forEach(function(el){
      if(s.logo && s.logo.length > 10){
        if(el.tagName === 'IMG'){ el.src = s.logo; el.style.display = 'block'; }
        else el.innerHTML = '<img src="'+s.logo+'" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">';
      }
    });
    document.querySelectorAll('[data-brand]').forEach(function(el){ if(s.brand) el.textContent = s.brand; });
    document.querySelectorAll('[data-tag]').forEach(function(el){ if(s.tag) el.textContent = s.tag; });
    if(s.brand) document.title = s.brand + ' RO — Pure Water, Pure Life';
  };

  window.renderBanner = function(){
    var active = (announcements || []).filter(function(a){ return a.status === 'active'; });
    var track = document.getElementById('bannerTrack');
    if(!track) return;
    if(!active.length){ track.innerHTML = ''; return; }
    var html = active.map(function(a){ return '<span><i class="fas '+a.icon+'"></i> '+a.msg+'</span>'; }).join('');
    track.innerHTML = html + html;
  };

  window.renderReviews = function(){
    var pub = (reviews || []).filter(function(r){ return r.status === 'published'; });
    var wrap = document.getElementById('revWrap');
    if(!wrap) return;
    if(!pub.length){
      wrap.innerHTML = '<div class="tc on"><p class="tc-t">No reviews yet.</p></div>';
      var emptyDots = document.getElementById('revDots');
      if(emptyDots) emptyDots.innerHTML = '';
      return;
    }
    wrap.innerHTML = pub.map(function(r,i){
      var stars = '';
      for(var s=0;s<(r.rating||5);s++) stars += '★';
      return '<div class="tc'+(i===0?' on':'')+'"><div class="tc-s">'+stars+'</div><p class="tc-t">'+(r.text||'')+'</p><div class="tc-a"><div class="tc-av">'+((r.nm||r.name||'U').charAt(0))+'</div><div class="tc-i"><h4>'+(r.nm||r.name||'User')+'</h4><p>'+(r.location||r.prod||'')+'</p></div></div></div>';
    }).join('');
    var dots = document.getElementById('revDots');
    if(dots) dots.innerHTML = pub.map(function(_,i){ return '<span class="'+(i===0?'on':'')+'" onclick="gT('+i+')"></span>'; }).join('');
  };

  function refreshPublicSiteData(site){
    site = site || {};
    siteSettings = site.settings || clone(DEF_SET);
    products = asArray(site.products);
    spares = asArray(site.spares);
    reviews = asArray(site.reviews);
    announcements = asArray(site.announcements);
    coupons = asArray(site.coupons);

    if(!products.length) products = clone(DEF_PROD);
    if(!spares.length) spares = clone(DEF_SPARE);
    if(!reviews.length) reviews = clone(DEF_REV);
    if(!announcements.length) announcements = clone(DEF_ANN);
    if(!coupons.length) coupons = clone(DEF_COUP);

    setGlobalStore();
    if(typeof applySettings === 'function') applySettings();
    if(typeof rP === 'function') rP();
    if(typeof initHero === 'function') initHero();
    if(typeof rS === 'function') rS();
    if(typeof renderBanner === 'function') renderBanner();
    if(typeof renderReviews === 'function') renderReviews();
    if(typeof populateReviewProducts === 'function') populateReviewProducts();
  }

  fbDb.ref('site').on('value', function(snap){
    refreshPublicSiteData(snap.val() || {});
  });

  fbDb.ref('notifications').on('value', function(snap){
    notifications = sortByDate(asArray(snap.val()));
    setGlobalStore();
    if(typeof updNotifBdg === 'function') updNotifBdg();
    if(typeof loadNotifs === 'function') loadNotifs();
  });

  applySettings();
  renderBanner();
  renderReviews();
})();
</script>
"""

INDEX_PATCH_TEMPLATE = r"""
<script>
(function(){
  var fb = window.__NEER_FB__;
  if(!fb) return;
  var auth = fb.auth;
  var db = fb.db;
  var storage = fb.storage;
  var ordersRef = null;
  var ordersCb = null;
  var customerRef = null;
  var customerCb = null;
  var ADMIN_ALLOWLIST = __ADMIN_ALLOWLIST__.map(function(v){ return String(v).toLowerCase(); });

  function isAdminEmail(email){ return ADMIN_ALLOWLIST.indexOf(String(email || '').trim().toLowerCase()) > -1; }
  function isAdminUser(user){ return !!(user && isAdminEmail(user.email)); }
  function isoNow(){ return new Date().toISOString(); }
  function fmtDate(d){ return new Date(d).toLocaleDateString('en-IN',{day:'2-digit',month:'short',year:'numeric'}); }
  function asArray(v){
    if(!v) return [];
    if(Array.isArray(v)) return v.filter(Boolean);
    return Object.keys(v).map(function(k){ return v[k]; }).filter(Boolean);
  }
  function sortByDate(list){
    return (list||[]).slice().sort(function(a,b){
      return new Date(b && (b.created_at || b.updated_at || b.date) || 0) - new Date(a && (a.created_at || a.updated_at || a.date) || 0);
    });
  }
  function normalizeCustomer(id, data, fbUser){
    data = data || {};
    var photo = data.profile_photo_url || data.pic || (fbUser && fbUser.photoURL) || '';
    return {
      uid: id || data.id || '',
      id: id || data.id || '',
      name: data.name || data.nm || (fbUser && (fbUser.displayName || fbUser.email)) || 'User',
      nm: data.name || data.nm || (fbUser && (fbUser.displayName || fbUser.email)) || 'User',
      email: data.email || (fbUser && fbUser.email) || '',
      phone: data.phone || '',
      addr: data.address || data.addr || '',
      address: data.address || data.addr || '',
      pic: photo,
      profile_photo_url: photo,
      status: data.status || 'active',
      total_orders: data.total_orders || data.orders || 0,
      orders: data.total_orders || data.orders || 0
    };
  }
  function updateCheckoutFields(){
    var map = {
      cN: usr.name || '',
      cP: usr.phone || '',
      cE: usr.email || '',
      cA: usr.addr || ''
    };
    Object.keys(map).forEach(function(id){
      var el = document.getElementById(id);
      if(el && !el.value) el.value = map[id];
    });
  }

  window.getUserNotifs = function(em, ph, uid){
    return (notifications || []).filter(function(n){
      return n.forUser === 'all' || n.forUser === em || n.forUser === ph || n.forUserId === uid;
    });
  };

  window.updUI = function(){
    var l = document.getElementById('lBtn');
    var u = document.getElementById('uBtn');
    if(logd){
      l.style.display = 'none';
      u.classList.add('show');
      u.textContent = (usr.name || 'U').charAt(0).toUpperCase();
      u.style.backgroundImage = '';
      u.style.backgroundSize = 'cover';
      if(usr.pic){
        u.textContent = '';
        u.style.backgroundImage = 'url('+usr.pic+')';
      }
      var pav = document.getElementById('pAv');
      if(pav){
        if(usr.pic) pav.innerHTML = '<img src="'+usr.pic+'">';
        else pav.textContent = (usr.name || 'U').charAt(0).toUpperCase();
      }
      var pNm = document.getElementById('pNm');
      var pEm = document.getElementById('pEm');
      if(pNm) pNm.textContent = usr.name || 'User';
      if(pEm) pEm.textContent = usr.email || usr.phone || '—';
      var epN = document.getElementById('epN');
      var epE = document.getElementById('epE');
      var epP = document.getElementById('epP');
      if(epN) epN.value = usr.name || '';
      if(epE) epE.value = usr.email || '';
      if(epP) epP.value = usr.phone || '';
      updateCheckoutFields();
    }else{
      l.style.display = 'flex';
      u.classList.remove('show');
      u.style.backgroundImage = '';
      var pav2 = document.getElementById('pAv');
      if(pav2) pav2.textContent = 'U';
      var pNm2 = document.getElementById('pNm');
      var pEm2 = document.getElementById('pEm');
      if(pNm2) pNm2.textContent = 'User';
      if(pEm2) pEm2.textContent = '—';
    }
  };

  function detachOrderListener(){
    if(ordersRef && ordersCb){
      ordersRef.off('value', ordersCb);
      ordersRef = null;
      ordersCb = null;
    }
  }

  function detachCustomerListener(){
    if(customerRef && customerCb){
      customerRef.off('value', customerCb);
      customerRef = null;
      customerCb = null;
    }
  }

  async function refreshCustomerSession(fbUser){
    if(!fbUser || isAdminUser(fbUser)){
      detachOrderListener();
      detachCustomerListener();
      logd = false;
      usr = {name:'',email:'',phone:'',addr:'',pic:'',uid:'',isAdmin: !!fbUser};
      orders = [];
      updUI();
      updNotifBdg();
      return;
    }

    detachCustomerListener();
    customerRef = db.ref('customers/' + fbUser.uid);
    customerCb = function(customerSnap){
      var data = customerSnap.val() || {};
      usr = normalizeCustomer(fbUser.uid, data, fbUser);
      logd = true;
      window.usr = usr;
      updUI();
      updNotifBdg();
      if(typeof loadNotifs === 'function') loadNotifs();
    };
    customerRef.on('value', customerCb);

    detachOrderListener();
    ordersRef = db.ref('orders').orderByChild('customer_id').equalTo(fbUser.uid);
    ordersCb = function(orderSnap){
      orders = sortByDate(asArray(orderSnap.val()));
      if(typeof rendMyOrders === 'function') rendMyOrders();
    };
    ordersRef.on('value', ordersCb);
  }

  auth.onAuthStateChanged(function(fbUser){
    refreshCustomerSession(fbUser).catch(function(err){
      console.error(err);
      toast('Session sync failed', 'err');
    });
  });

  window.doLgn = async function(e){
    e.preventDefault();
    var form = document.getElementById('fL');
    var identifier = document.getElementById('lgIn').value.trim();
    var pw = form.querySelector('input[type="password"]').value;
    if(!identifier || !pw){ toast('Enter login details', 'err'); return; }
    try{
      var email = identifier;
      if(identifier.indexOf('@') < 0){
        var foundByPhone = await db.ref('customers').orderByChild('phone').equalTo(identifier).once('value');
        if(!foundByPhone.exists()) throw new Error('No account found for this phone number');
        var first = Object.values(foundByPhone.val())[0] || {};
        email = first.email || '';
        if(!email) throw new Error('This phone number has no email login');
      }
      if(isAdminEmail(email)) throw new Error('Admin account detected. Please login from /admin only.');
      await auth.signInWithEmailAndPassword(email, pw);
      toast('Welcome back! 👋', 'ok');
      clAuthF();
      form.reset();
    }catch(err){
      toast(err.message || 'Login failed', 'err');
    }
  };

  window.doSgn = async function(e){
    e.preventDefault();
    var nm = document.getElementById('sN').value.trim();
    var em = document.getElementById('sE').value.trim();
    var ph = document.getElementById('sP').value.trim();
    var ad = document.getElementById('sA').value.trim();
    var pw = document.querySelector('#fS input[type="password"]').value;
    if(!nm || !em || !ph || !ad || !pw){ toast('All fields required', 'err'); return; }
    if(ph.length < 10){ toast('Phone must be 10 digits', 'err'); return; }
    if(isAdminEmail(em)){ toast('That email is reserved for admin. Use /admin only.', 'err'); return; }
    try{
      var cred = await auth.createUserWithEmailAndPassword(em, pw);
      var payload = {
        id: cred.user.uid,
        uid: cred.user.uid,
        name: nm,
        nm: nm,
        email: em,
        phone: ph,
        address: ad,
        addr: ad,
        status: 'active',
        total_orders: 0,
        orders: 0,
        profile_photo_url: '',
        created_at: isoNow(),
        updated_at: isoNow()
      };
      await db.ref('customers/' + cred.user.uid).set(payload);
      toast('Welcome ' + nm + '! 🎉', 'ok');
      document.getElementById('fS').reset();
      clAuthF();
    }catch(err){
      toast(err.message || 'Signup failed', 'err');
    }
  };

  window.doLout = async function(){
    try{
      await auth.signOut();
      clProf();
      toast('Logged out', 'inf');
    }catch(err){
      toast(err.message || 'Logout failed', 'err');
    }
  };

  window.openProf = function(sec){
    if(!logd){ openAuth(); return; }
    oSB('ppan','ppOv');
    showPS(sec || 'Main');
  };

  window.updNotifBdg = function(){
    var el = document.getElementById('notifBdg');
    if(!el) return;
    if(!logd){ el.textContent = '0'; return; }
    el.textContent = String(getUserNotifs(usr.email, usr.phone, usr.uid).length);
  };

  window.loadNotifs = function(){
    var list = document.getElementById('custNotifList');
    if(!list) return;
    var my = logd ? getUserNotifs(usr.email, usr.phone, usr.uid) : [];
    if(!my.length){
      list.innerHTML = '<div class="sbe"><i class="fas fa-bell"></i><h4>No notifications</h4></div>';
      return;
    }
    list.innerHTML = my.slice().reverse().map(function(n){
      return '<div class="ocard"><p><strong>'+n.title+'</strong></p><p>'+n.msg+'</p><p style="font-size:.7rem;color:var(--muted);margin-top:4px">'+(n.date||'')+'</p></div>';
    }).join('');
  };

  window.rendMyOrders = function(){
    var list = document.getElementById('ordList');
    if(!list) return;
    var myOrders = sortByDate(orders || []);
    if(!myOrders.length){
      list.innerHTML = '<div class="sbe"><i class="fas fa-box"></i><h4>No orders yet</h4></div>';
      return;
    }
    list.innerHTML = myOrders.map(function(o){
      var stMap = {processing:'st-proc', shipped:'st-ship', delivered:'st-dlvr', cancelled:'st-cncl', out:'st-out'};
      var stCls = stMap[o.status] || 'st-proc';
      var acts = '';
      if(o.status === 'processing' || o.status === 'shipped') acts = '<button onclick="openDM(\''+o.id+'\')"><i class="fas fa-calendar-alt"></i> Change Date</button><button class="cbtn" onclick="cancelOrd(\''+o.id+'\')"><i class="fas fa-times"></i> Cancel</button>';
      else if(o.status === 'delivered') acts = '<button onclick="reorder(\''+o.id+'\')"><i class="fas fa-redo"></i> Reorder</button>';
      return '<div class="ocard"><div class="ocard-top"><h5>#'+o.id+'</h5><span class="'+stCls+'">'+o.status+'</span></div><p><strong>'+(o.prod || (o.product_details && o.product_details.name) || 'Product')+'</strong> — ₹'+((o.amount||0).toLocaleString())+'</p><p>'+(o.installDate || o.date || '')+'</p><div class="ocard-acts">'+acts+'</div></div>';
    }).join('');
  };

  window.cancelOrd = async function(id){
    if(!confirm('Cancel order?')) return;
    try{
      await db.ref('orders/' + id).update({ status:'cancelled', updated_at: isoNow() });
      toast('Cancelled', 'ok');
    }catch(err){
      toast(err.message || 'Cancel failed', 'err');
    }
  };

  window.openDM = function(id){
    curEditOrd = id;
    var o = (orders || []).find(function(x){ return x.id === id; });
    document.getElementById('dmOrdNm').textContent = o ? (o.prod || '') : '';
    document.getElementById('dmOv').classList.add('o');
  };

  window.svDM = async function(){
    var d = document.getElementById('dmDate').value;
    if(!d){ toast('Select a date', 'err'); return; }
    try{
      await db.ref('orders/' + curEditOrd).update({
        installDate: new Date(d).toLocaleDateString('en-IN',{day:'2-digit',month:'short',year:'numeric'}),
        updated_at: isoNow()
      });
      toast('Date updated!', 'ok');
      clDM();
    }catch(err){
      toast(err.message || 'Date update failed', 'err');
    }
  };

  window.chgPic = function(e){
    var file = e.target.files[0];
    if(!file || !auth.currentUser) return;
    var reader = new FileReader();
    reader.onload = function(ev){
      compImg(ev.target.result, 240, 0.78, async function(compacted){
        try{
          try{ await auth.currentUser.updateProfile({ photoURL: compacted }); }catch(profileErr){ console.warn('Profile photoURL update failed', profileErr); }
          await db.ref('customers/' + auth.currentUser.uid).update({
            profile_photo_url: compacted,
            pic: compacted,
            updated_at: isoNow()
          });
          usr.pic = compacted;
          usr.profile_photo_url = compacted;
          updUI();
          toast('Photo updated!', 'ok');
          e.target.value = '';
        }catch(err){
          toast(err.message || 'Photo upload failed', 'err');
        }
      });
    };
    reader.onerror = function(){ toast('Photo read failed', 'err'); };
    reader.readAsDataURL(file);
  };

  function collectCustomerBase(){
    return {
      name: document.getElementById('cN').value.trim(),
      phone: document.getElementById('cP').value.trim(),
      email: document.getElementById('cE').value.trim(),
      address: [
        document.getElementById('cA').value.trim(),
        document.getElementById('cCi').value.trim(),
        document.getElementById('cPn').value.trim()
      ].filter(Boolean).join(', ')
    };
  }

  async function findExistingCustomer(base){
    if(logd && auth.currentUser && !isAdminUser(auth.currentUser)) return auth.currentUser.uid;
    if(base.email){
      var byEmail = await db.ref('customers').orderByChild('email').equalTo(base.email).once('value');
      if(byEmail.exists()) return Object.keys(byEmail.val())[0];
    }
    if(base.phone){
      var byPhone = await db.ref('customers').orderByChild('phone').equalTo(base.phone).once('value');
      if(byPhone.exists()) return Object.keys(byPhone.val())[0];
    }
    return 'guest_' + Date.now();
  }

  async function upsertCustomerForOrder(base, customerId){
    var snap = await db.ref('customers/' + customerId).once('value');
    var existing = snap.val() || {};
    var orderCount = (existing.total_orders || existing.orders || 0) + 1;
    var payload = Object.assign({}, existing, {
      id: customerId,
      uid: auth.currentUser ? auth.currentUser.uid : (existing.uid || null),
      name: base.name,
      nm: base.name,
      email: base.email,
      phone: base.phone,
      address: base.address,
      addr: base.address,
      status: existing.status || 'active',
      total_orders: orderCount,
      orders: orderCount,
      created_at: existing.created_at || isoNow(),
      updated_at: isoNow()
    });
    await db.ref('customers/' + customerId).set(payload);
    return payload;
  }

  window.actuallyPlaceOrder = async function(){
    var base = collectCustomerBase();
    if(!base.name || !base.phone || !base.email){ toast('Fill shipping details', 'err'); goStp(1); return; }
    if(!cart.length){ toast('Cart empty!', 'err'); return; }
    try{
      var customerId = await findExistingCustomer(base);
      var customer = await upsertCustomerForOrder(base, customerId);
      var oid = 'NEER-' + new Date().getFullYear() + '-' + String(Math.floor(Math.random()*9000)+1000);
      var subtotal = cart.reduce(function(s,c){ return s + c.pr * c.qty; }, 0);
      var tax = Math.round(subtotal * .18);
      var install = new Date();
      install.setDate(install.getDate() + 5);
      var order = {
        id: oid,
        customer_id: customerId,
        customer_uid: auth.currentUser ? auth.currentUser.uid : null,
        cust: customer.name,
        customer_name: customer.name,
        phone: customer.phone,
        email: customer.email,
        address: customer.address,
        prod: cart.map(function(c){ return c.nm; }).join(', '),
        product_details: { name: cart[0] ? cart[0].nm : 'Product' },
        items: cart.map(function(c){ return { id:c.id, nm:c.nm, pr:c.pr, qty:c.qty, img:c.img || '' }; }),
        amount: subtotal,
        tax: tax,
        total: subtotal + tax,
        status: 'processing',
        payment: sPM,
        date: fmtDate(isoNow()),
        created_at: isoNow(),
        updated_at: isoNow(),
        installDate: fmtDate(install.toISOString())
      };
      await db.ref('orders/' + oid).set(order);
      var nid = 'n_' + Date.now();
      await db.ref('notifications/' + nid).set({
        id: nid,
        title: 'Order Confirmed! 🎉',
        msg: 'Order #' + oid + ' placed. Install: ' + order.installDate,
        forUser: customer.email || customer.phone,
        forUserId: customerId,
        date: fmtDate(isoNow()),
        created_at: isoNow()
      });
      document.getElementById('oId').textContent = 'Order #' + order.id;
      document.querySelectorAll('.csec').forEach(function(s){ s.classList.remove('on'); });
      document.getElementById('coSt').style.display = 'none';
      document.getElementById('coSc').classList.add('on');
      cart = [];
      uC();
      rP();
      rS();
      updNotifBdg();
      toast('Order placed! 🎉', 'ok');
    }catch(err){
      console.error(err);
      toast(err.message || 'Order failed', 'err');
    }
  };

  window.plcOrd = function(){
    if(!cart.length){ toast('Cart empty!', 'err'); return; }
    if(sPM === 'cod') actuallyPlaceOrder();
    else openRazorpay();
  };

  window.subFB = async function(e){
    e.preventDefault();
    if(!cSt){ toast('Please give a rating', 'err'); return; }
    var nm = document.getElementById('fbNm').value.trim();
    var prod = document.getElementById('fbProd').value;
    var loc = document.getElementById('fbLoc').value.trim();
    var txt = document.getElementById('fbTxt').value.trim();
    if(!nm || !prod || !loc || !txt){ toast('All review fields are required', 'err'); return; }
    var id = 'r_' + Date.now();
    var review = { id:id, nm:nm, name:nm, prod:prod, location:loc, rating:cSt, text:txt, date:fmtDate(isoNow()), status:'published', created_at: isoNow() };
    try{
      await db.ref('site/reviews/' + id).set(review);
      toast('Thanks for your review! ⭐', 'ok');
      e.target.reset();
      cSt = 0;
      document.querySelectorAll('#stI i').forEach(function(s){ s.className='far fa-star'; });
    }catch(err){
      toast(err.message || 'Review save failed', 'err');
    }
  };

  window.populateReviewProducts = function(){
    var sel = document.getElementById('fbProd');
    if(sel){
      var active = (products || []).filter(function(p){ return p.status === 'active'; });
      sel.innerHTML = '<option value="">Select product</option>' + active.map(function(p){ return '<option>' + (p.nm || p.name) + '</option>'; }).join('');
    }
  };

  var editForm = document.querySelector('#profEditProf form');
  if(editForm){
    editForm.onsubmit = async function(event){
      event.preventDefault();
      if(!auth.currentUser) return;
      try{
        var nextName = document.getElementById('epN').value.trim();
        var nextEmail = document.getElementById('epE').value.trim();
        var nextPhone = document.getElementById('epP').value.trim();
        await db.ref('customers/' + auth.currentUser.uid).update({
          name: nextName,
          nm: nextName,
          email: nextEmail,
          phone: nextPhone,
          address: usr.addr || '',
          addr: usr.addr || '',
          updated_at: isoNow()
        });
        usr.name = nextName;
        usr.email = nextEmail;
        usr.phone = nextPhone;
        updUI();
        toast('Updated!', 'ok');
        showPS('Main');
      }catch(err){
        toast(err.message || 'Profile update failed', 'err');
      }
    };
  }

  populateReviewProducts();
})();
</script>
"""

ADMIN_SYNC_TEMPLATE = r"""
<!-- ===== FIREBASE ADMIN SYNC ENGINE ===== -->
__COMMON_SDK__
<script>
(function(){
  const firebaseConfig = __FIREBASE_CONFIG__;
  const ADMIN_APP_NAME = 'neer-admin-app';
  let adminApp;
  try { adminApp = firebase.app(ADMIN_APP_NAME); }
  catch (e) { adminApp = firebase.initializeApp(firebaseConfig, ADMIN_APP_NAME); }
  const fbAuth = adminApp.auth();
  const fbDb = adminApp.database();
  const fbStorage = adminApp.storage();
  fbAuth.setPersistence(firebase.auth.Auth.Persistence.LOCAL).catch(function(err){ console.warn('Admin auth persistence error', err); });
  const uploadedUrls = {};
  const ADMIN_ALLOWLIST = __ADMIN_ALLOWLIST__.map(function(v){ return String(v).toLowerCase(); });
  const ADMIN_LOGIN_EMAIL = String(__ADMIN_LOGIN_EMAIL__ || '').trim().toLowerCase();
  const ADMIN_LOGIN_PASSWORD = String(__ADMIN_LOGIN_PASSWORD__ || '');

  function isAllowedAdminEmail(email){ return ADMIN_ALLOWLIST.indexOf(String(email || '').trim().toLowerCase()) > -1; }
  function isFixedAdminCredentials(email, password){
    return String(email || '').trim().toLowerCase() === ADMIN_LOGIN_EMAIL && String(password || '') === ADMIN_LOGIN_PASSWORD;
  }
  function adminBlockedMessage(user){
    if(!user) return 'Admin login required';
    if(!isAllowedAdminEmail(user.email)) return 'This email is not allowed for admin access';
    return 'Admin access denied';
  }
  async function ensureAdminRecord(user){
    if(!user) return false;
    if(!isAllowedAdminEmail(user.email)) return false;
    var ref = fbDb.ref('meta/admins/' + user.uid);
    var snap = await ref.once('value');
    if(!snap.exists()){
      await ref.set({ uid:user.uid, email:user.email, role:'admin', granted_at:new Date().toISOString() });
    }
    return true;
  }

  function clone(v){ return JSON.parse(JSON.stringify(v)); }
  function asArray(v){
    if(!v) return [];
    if(Array.isArray(v)) return v.filter(Boolean);
    return Object.keys(v).map(function(k){ return v[k]; }).filter(Boolean);
  }
  function listToMap(v){
    if(!Array.isArray(v)) return v || {};
    var out = {};
    v.forEach(function(item){ if(item && item.id !== undefined) out[String(item.id)] = item; });
    return out;
  }
  function sortByField(list, field, ascending){
    return (list || []).slice().sort(function(a,b){
      var av = a && a[field] !== undefined ? a[field] : '';
      var bv = b && b[field] !== undefined ? b[field] : '';
      if(field && String(field).indexOf('created') > -1){
        av = new Date(av || 0).getTime();
        bv = new Date(bv || 0).getTime();
      }
      if(av < bv) return ascending ? -1 : 1;
      if(av > bv) return ascending ? 1 : -1;
      return 0;
    });
  }
  function sortByDate(list){
    return sortByField(list, 'created_at', false);
  }

  var DEF_SET = __DEF_SET__;
  var DEF_PROD = __DEF_PROD__;
  var DEF_SPARE = __DEF_SPARE__;
  var DEF_REV = __DEF_REV__;
  var DEF_ANN = __DEF_ANN__;
  var DEF_COUP = __DEF_COUP__;

  var __store = {
    settings: clone(DEF_SET),
    products: clone(DEF_PROD),
    spares: clone(DEF_SPARE),
    orders: [],
    customers: [],
    reviews: clone(DEF_REV),
    announcements: clone(DEF_ANN),
    coupons: clone(DEF_COUP),
    notifications: []
  };

  window.DB = {
    save:function(k,d){
      __store[k] = clone(d);
      var siteKeys = ['settings','products','spares','reviews','announcements','coupons'];
      if(siteKeys.indexOf(k) > -1){
        fbDb.ref('site/' + k).set(listToMap(d)).catch(function(err){ console.error(err); if(typeof toast==='function') toast(err.message,'err'); });
      }else if(k === 'notifications'){
        fbDb.ref('notifications').set(listToMap(d)).catch(function(err){ console.error(err); if(typeof toast==='function') toast(err.message,'err'); });
      }else if(k === 'customers'){
        fbDb.ref('customers').set(listToMap(d)).catch(function(err){ console.error(err); if(typeof toast==='function') toast(err.message,'err'); });
      }else if(k === 'orders'){
        fbDb.ref('orders').set(listToMap(d)).catch(function(err){ console.error(err); if(typeof toast==='function') toast(err.message,'err'); });
      }
      return true;
    },
    load:function(k,def){
      return __store[k] !== undefined ? clone(__store[k]) : def;
    }
  };

  var currentUser = null;
  var siteSettings = DB.load('settings',DEF_SET);
  var products = DB.load('products',DEF_PROD);
  var spares = DB.load('spares',DEF_SPARE);
  var orders = DB.load('orders',[]);
  var customers = DB.load('customers',[]);
  var reviews = DB.load('reviews',DEF_REV);
  var announcements = DB.load('announcements',DEF_ANN);
  var coupons = DB.load('coupons',DEF_COUP);
  var notifications = DB.load('notifications',[]);

  window.currentUser = currentUser;
  window.siteSettings = siteSettings;
  window.products = products;
  window.spares = spares;
  window.orders = orders;
  window.customers = customers;
  window.reviews = reviews;
  window.announcements = announcements;
  window.coupons = coupons;
  window.notifications = notifications;

  function syncGlobals(){
    window.currentUser = currentUser;
    window.siteSettings = siteSettings;
    window.products = products;
    window.spares = spares;
    window.orders = orders;
    window.customers = customers;
    window.reviews = reviews;
    window.announcements = announcements;
    window.coupons = coupons;
    window.notifications = notifications;
    __store.settings = clone(siteSettings);
    __store.products = clone(products);
    __store.spares = clone(spares);
    __store.orders = clone(orders);
    __store.customers = clone(customers);
    __store.reviews = clone(reviews);
    __store.announcements = clone(announcements);
    __store.coupons = clone(coupons);
    __store.notifications = clone(notifications);
  }

  window.compImg = function compImg(dataUrl, maxWidth, quality, callback){
    var img = new Image();
    img.onload = function(){
      var width = img.width;
      var height = img.height;
      if(width > maxWidth){
        height = Math.round(height * (maxWidth / width));
        width = maxWidth;
      }
      var canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      var ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, width, height);
      callback(canvas.toDataURL('image/jpeg', quality));
    };
    img.onerror = function(){ callback(dataUrl); };
    img.src = dataUrl;
  }

  window.applySettings = function(){
    var s = siteSettings; if(!s) return;
    if(s.color1) document.documentElement.style.setProperty('--cyan', s.color1);
    if(s.logo && s.logo.length > 10){
      document.querySelectorAll('[data-logo]').forEach(function(el){
        if(el.tagName === 'IMG'){ el.src = s.logo; el.style.display = 'block'; }
        else el.innerHTML = '<img src="'+s.logo+'" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">';
      });
    }
    document.querySelectorAll('[data-brand]').forEach(function(el){ if(s.brand) el.textContent = s.brand; });
    document.querySelectorAll('[data-tag]').forEach(function(el){ if(s.tag) el.textContent = s.tag; });
  };

  function normalizeSite(site){
    site = site || {};
    siteSettings = site.settings || clone(DEF_SET);
    products = asArray(site.products); if(!products.length) products = clone(DEF_PROD);
    spares = asArray(site.spares); if(!spares.length) spares = clone(DEF_SPARE);
    reviews = asArray(site.reviews); if(!reviews.length) reviews = clone(DEF_REV);
    announcements = asArray(site.announcements); if(!announcements.length) announcements = clone(DEF_ANN);
    coupons = asArray(site.coupons); if(!coupons.length) coupons = clone(DEF_COUP);
    syncGlobals();
    applySettings();
    if(typeof renderPage === 'function') renderPage(window.curPage || 'dashboard');
  }

  function normalizeCustomers(data){
    customers = sortByDate(asArray(data)).map(function(c){
      var photo = c.profile_photo_url || c.pic || '';
      return Object.assign({
        name:'', nm:'', email:'', phone:'', address:'', addr:'', status:'active', total_orders:0, orders:0, profile_photo_url:'', pic:''
      }, c, {
        name: c.name || c.nm || '',
        nm: c.name || c.nm || '',
        address: c.address || c.addr || '',
        addr: c.address || c.addr || '',
        profile_photo_url: photo,
        pic: photo,
        total_orders: c.total_orders || c.orders || 0,
        orders: c.total_orders || c.orders || 0
      });
    });
    syncGlobals();
  }

  function normalizeOrders(data){
    var customerMap = {};
    (customers || []).forEach(function(c){ customerMap[c.id || c.uid] = c; });
    orders = sortByDate(asArray(data)).map(function(o){
      var linked = customerMap[o.customer_id] || {};
      return Object.assign({}, o, {
        cust: o.cust || linked.name || linked.nm || 'Guest',
        product_details: o.product_details || { name: (o.prod || '').split(',')[0] || 'Product' }
      });
    });
    syncGlobals();
  }

  fbDb.ref('site').on('value', function(snap){ normalizeSite(snap.val() || {}); });
  fbDb.ref('customers').on('value', function(snap){ normalizeCustomers(snap.val() || {}); if(typeof renderPage === 'function') renderPage(window.curPage || 'dashboard'); });
  fbDb.ref('orders').on('value', function(snap){ normalizeOrders(snap.val() || {}); if(typeof renderPage === 'function') renderPage(window.curPage || 'dashboard'); });
  fbDb.ref('notifications').on('value', function(snap){ notifications = sortByDate(asArray(snap.val())); syncGlobals(); if(typeof loadNotifDropdown === 'function') loadNotifDropdown(); });

  function adminSession(user){
    if(!user) return null;
    return { user: { email: user.email, id: user.uid } };
  }
  async function isAdmin(uid){
    var user = fbAuth.currentUser;
    if(user && user.uid === uid) return await ensureAdminRecord(user);
    var snap = await fbDb.ref('meta/admins/' + uid).once('value');
    return !!snap.val();
  }

  class FirebaseTable {
    constructor(table){ this.table = table; }
    select(query){
      var self = this;
      return {
        order: async function(field, opts){
          try{
            var snap = await fbDb.ref(self.table).once('value');
            var data = asArray(snap.val());
            if(self.table === 'orders'){
              var byId = {};
              (customers || []).forEach(function(c){ byId[c.id || c.uid] = c; });
              data = data.map(function(o){
                var linked = byId[o.customer_id] || {};
                return Object.assign({}, o, {
                  customers: { name: linked.name || linked.nm || o.cust || 'Guest' },
                  product_details: o.product_details || { name: (o.prod || '').split(',')[0] || 'Product' }
                });
              });
            }
            if(self.table === 'customers'){
              data = data.map(function(c){ return Object.assign({}, c, { name:c.name || c.nm || '', total_orders: c.total_orders || c.orders || 0 }); });
            }
            var asc = !(opts && opts.ascending === false);
            data = sortByField(data, field || 'created_at', asc);
            return { data:data, error:null };
          }catch(err){
            return { data:null, error:{ message: err.message || 'Select failed' } };
          }
        }
      };
    }
    update(payload){
      var self = this;
      return {
        eq: async function(field, value){
          try{
            await fbDb.ref(self.table + '/' + value).update(Object.assign({}, payload, { updated_at: new Date().toISOString() }));
            return { data:null, error:null };
          }catch(err){
            return { data:null, error:{ message: err.message || 'Update failed' } };
          }
        }
      };
    }
    delete(){
      var self = this;
      return {
        eq: async function(field, value){
          try{
            await fbDb.ref(self.table + '/' + value).remove();
            return { data:null, error:null };
          }catch(err){
            return { data:null, error:{ message: err.message || 'Delete failed' } };
          }
        }
      };
    }
  }

  window._supabase = {
    auth: {
      async getSession(){
        var user = fbAuth.currentUser;
        if(user && !(await ensureAdminRecord(user))){
          await fbAuth.signOut();
          user = null;
        }
        return { data:{ session: adminSession(user) } };
      },
      onAuthStateChange(cb){
        return fbAuth.onAuthStateChanged(async function(user){
          if(user && !(await ensureAdminRecord(user))){
            await fbAuth.signOut();
            cb('SIGNED_OUT', null);
            return;
          }
          cb(user ? 'SIGNED_IN' : 'SIGNED_OUT', adminSession(user));
        });
      },
      async signInWithPassword(payload){
        try{
          var email = String(payload.email || '').trim().toLowerCase();
          var password = String(payload.password || '');
          if(!isFixedAdminCredentials(email, password)){
            return { data:null, error:{ message:'Use admin@mail.com / n1m2a3828 only' } };
          }
          var cred;
          try{
            cred = await fbAuth.signInWithEmailAndPassword(email, password);
          }catch(err){
            try{
              cred = await fbAuth.createUserWithEmailAndPassword(email, password);
            }catch(createErr){
              return { data:null, error:{ message: createErr.message || err.message || 'Admin login failed' } };
            }
          }
          if(!(await ensureAdminRecord(cred.user))){
            var msg = adminBlockedMessage(cred.user);
            await fbAuth.signOut();
            return { data:null, error:{ message: msg } };
          }
          return { data:{ user:{ email: cred.user.email, id: cred.user.uid } }, error:null };
        }catch(err){
          return { data:null, error:{ message: err.message || 'Login failed' } };
        }
      },
      async signUp(payload){
        return { data:null, error:{ message:'Signup disabled. Use admin@mail.com / n1m2a3828 only.' } };
      },
      async signOut(){
        try{ await fbAuth.signOut(); return { error:null }; }
        catch(err){ return { error:{ message: err.message || 'Logout failed' } }; }
      },
      async updateUser(payload){
        try{
          if(!fbAuth.currentUser) throw new Error('No admin logged in');
          await fbAuth.currentUser.updatePassword(payload.password);
          return { data:null, error:null };
        }catch(err){
          return { data:null, error:{ message: err.message || 'Password update failed' } };
        }
      }
    },
    from: function(table){ return new FirebaseTable(table); },
    channel: function(){ return { on:function(){ return this; }, subscribe:function(){ return this; } }; },
    storage: {
      from: function(){
        return {
          async upload(filePath, file){
            try{
              var snap = await fbStorage.ref().child(filePath).put(file);
              var url = await snap.ref.getDownloadURL();
              uploadedUrls[filePath] = url;
              return { data:{ path:filePath }, error:null };
            }catch(err){
              return { data:null, error:{ message: err.message || 'Upload failed' } };
            }
          },
          getPublicUrl(filePath){
            try{
              if(uploadedUrls[filePath]){
                return { data:{ publicUrl: uploadedUrls[filePath] } };
              }
              return { data:{ publicUrl: '' } };
            }catch(err){
              console.warn('Failed to get download URL:', err);
              return { data:{ publicUrl: '' } };
            }
          }
        };
      }
    }
  };

  window.addNotif = function(title,msg,forUser){
    var target = (customers || []).find(function(c){
      return forUser && (c.id === forUser || c.email === forUser || c.phone === forUser || c.name === forUser || c.nm === forUser);
    });
    var obj = {
      id: 'n_' + Date.now(),
      title: title,
      msg: msg,
      forUser: forUser || 'all',
      forUserId: target ? (target.id || target.uid) : (forUser === 'all' ? 'all' : ''),
      date: new Date().toLocaleDateString('en-IN',{day:'2-digit',month:'short',year:'numeric'}),
      created_at: new Date().toISOString()
    };
    notifications.unshift(obj);
    syncGlobals();
    fbDb.ref('notifications/' + obj.id).set(obj).catch(function(err){ console.error(err); if(typeof toast==='function') toast(err.message,'err'); });
  };

  window.loadDataFromSupabase = async function(){
    var custSnap = await fbDb.ref('customers').once('value');
    normalizeCustomers(custSnap.val() || {});
    var orderSnap = await fbDb.ref('orders').once('value');
    normalizeOrders(orderSnap.val() || {});
    if(typeof renderPage === 'function') renderPage(window.curPage || 'dashboard');
  };

  window.setupRealtime = function(){ return true; };
  window.toggleAuthMode = function(){
    var login = document.getElementById('login-form');
    var signup = document.getElementById('signup-form');
    if(login.style.display === 'none'){
      login.style.display = 'block';
      signup.style.display = 'none';
    }else{
      login.style.display = 'none';
      signup.style.display = 'block';
    }
  };

  window.handleLogin = async function(){
    var email = document.getElementById('auth-email').value;
    var password = document.getElementById('auth-password').value;
    if(!email || !password) return toast('Fill all fields','err');
    var result = await _supabase.auth.signInWithPassword({ email:email, password:password });
    if(result.error) toast(result.error.message,'err');
    else toast('Logged in successfully','ok');
  };

  window.handleSignup = async function(){
    var email = document.getElementById('reg-email').value;
    var password = document.getElementById('reg-password').value;
    var confirm = document.getElementById('reg-password-confirm').value;
    if(!email || !password) return toast('Fill all fields','err');
    if(password !== confirm) return toast('Passwords do not match','err');
    var result = await _supabase.auth.signUp({ email:email, password:password });
    if(result.error) toast(result.error.message,'err');
    else toast((result.message || 'Admin created. Verify email, then login.'),'ok');
  };

  window.handleLogout = async function(){
    await _supabase.auth.signOut();
    toast('Logged out','ok');
  };

  window.changeAdminPassword = async function(){
    var newPw = document.getElementById('new-admin-pw').value;
    if(!newPw || newPw.length < 6) return toast('Password too short','err');
    var result = await _supabase.auth.updateUser({ password: newPw });
    if(result.error) toast(result.error.message,'err');
    else {
      toast('Password updated!','ok');
      document.getElementById('new-admin-pw').value = '';
    }
  };

  window.initAuth = async function(){
    applySettings();
    var current = fbAuth.currentUser;
    if(current && await ensureAdminRecord(current)){
      currentUser = { email: current.email, id: current.uid };
      syncGlobals();
      document.getElementById('auth-overlay').classList.remove('active');
      document.getElementById('admin-email-display').textContent = current.email || 'admin';
      await loadDataFromSupabase();
    }else{
      document.getElementById('auth-overlay').classList.add('active');
    }

    _supabase.auth.onAuthStateChange(async function(_event, session){
      if(session && session.user){
        currentUser = session.user;
        syncGlobals();
        document.getElementById('auth-overlay').classList.remove('active');
        document.getElementById('admin-email-display').textContent = currentUser.email;
        await loadDataFromSupabase();
      }else{
        currentUser = null;
        syncGlobals();
        document.getElementById('auth-overlay').classList.add('active');
      }
    });
  };

  applySettings();
})();
</script>
"""

ADMIN_PATCH_TEMPLATE = r"""
<script>
(function(){
  var viewBtn = document.querySelector('.tb-btn[title="View Website"]');
  if(viewBtn){
    viewBtn.onclick = function(){ window.open('/index.html','_blank'); };
  }

  var loginEmail = document.getElementById('auth-email');
  var loginPassword = document.getElementById('auth-password');
  if(loginEmail) loginEmail.value = __ADMIN_LOGIN_EMAIL__;
  if(loginPassword) loginPassword.value = __ADMIN_LOGIN_PASSWORD__;

  var loginCard = document.getElementById('login-form');
  if(loginCard){
    var hints = loginCard.querySelectorAll('p');
    hints.forEach(function(el){
      el.textContent = 'Admin login only: ' + __ADMIN_LOGIN_EMAIL__ + ' / ' + __ADMIN_LOGIN_PASSWORD__;
      el.onclick = null;
      el.style.cursor = 'default';
    });
  }

  var signupCard = document.getElementById('signup-form');
  if(signupCard) signupCard.style.display = 'none';
})();
</script>
"""


def render_template(template: str) -> str:
    replacements = {
        "__COMMON_SDK__": COMMON_FIREBASE_SDK,
        "__FIREBASE_CONFIG__": js(FIREBASE_CONFIG),
        "__DEF_SET__": js(DEFAULT_SETTINGS),
        "__DEF_PROD__": js(DEFAULT_PRODUCTS),
        "__DEF_SPARE__": js(DEFAULT_SPARES),
        "__DEF_REV__": js(DEFAULT_REVIEWS),
        "__DEF_ANN__": js(DEFAULT_ANNOUNCEMENTS),
        "__DEF_COUP__": js(DEFAULT_COUPONS),
        "__ADMIN_ALLOWLIST__": js([email.lower() for email in ADMIN_ALLOWLIST]),
        "__ADMIN_LOGIN_EMAIL__": js(ADMIN_LOGIN_EMAIL),
        "__ADMIN_LOGIN_PASSWORD__": js(ADMIN_LOGIN_PASSWORD),
    }
    out = template
    for key, value in replacements.items():
        out = out.replace(key, value)
    return out


def build_index_html() -> str:
    html = INDEX_SOURCE.read_text(encoding="utf-8")
    sync_block = render_template(INDEX_SYNC_TEMPLATE)
    patch_block = render_template(INDEX_PATCH_TEMPLATE)
    html = re.sub(
        r"<!-- ===== SYNC ENGINE ===== -->\s*<script>.*?</script>\s*<!-- BANNER -->",
        sync_block + "\n\n<!-- BANNER -->",
        html,
        flags=re.S,
    )
    html = html.replace("</body>", patch_block + "\n</body>")
    return html


def build_admin_html() -> str:
    html = ADMIN_SOURCE.read_text(encoding="utf-8")
    sync_block = render_template(ADMIN_SYNC_TEMPLATE)
    patch_block = render_template(ADMIN_PATCH_TEMPLATE)
    html = html.replace(
        '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>',
        '',
    )
    html = re.sub(
        r"<script data-cfasync=\"false\" src=\"/cdn-cgi/scripts/.*?</script>",
        '',
        html,
        flags=re.S,
    )
    html = re.sub(
        r"<script>\(function\(\)\{function c\(\)\{var b=a.contentDocument.*?</script>",
        '',
        html,
        flags=re.S,
    )
    html = re.sub(
        r"<!-- ===== SAME SYNC ENGINE AS index.html ===== -->\s*<script>.*?</script>\s*<!-- SIDEBAR -->",
        sync_block + "\n\n<!-- SIDEBAR -->",
        html,
        flags=re.S,
    )
    html = html.replace("window.open('index.html','_blank')", "window.open('/index.html','_blank')")
    html = html.replace("</body>", patch_block + "\n</body>")
    return html


class AppHandler(BaseHTTPRequestHandler):
    def _send_text(self, status: int, body: str, content_type: str = "text/html; charset=utf-8") -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            if path in {"/", "/index.html"}:
                self._send_text(200, build_index_html())
                return
            if path in {"/admin", "/admin.html"}:
                self._send_text(200, build_admin_html())
                return
            if path == "/health":
                self._send_text(200, json.dumps({"ok": True}), "application/json; charset=utf-8")
                return
            if path == "/firebase-rules.json":
                self._send_text(200, json.dumps(FIREBASE_RULES_HINT, indent=2), "application/json; charset=utf-8")
                return
            self._send_text(404, "Not Found", "text/plain; charset=utf-8")
        except FileNotFoundError as exc:
            self._send_text(500, f"Missing source file: {exc}", "text/plain; charset=utf-8")
        except Exception as exc:  # pragma: no cover
            self._send_text(500, f"Server error: {exc}", "text/plain; charset=utf-8")

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        print("[%s] %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), AppHandler)
    print(f"Neer RO server running on http://{HOST}:{PORT}")
    print("Website: http://localhost:8000/")
    print("Admin:   http://localhost:8000/admin")
    print("Firebase rules hint: http://localhost:8000/firebase-rules.json")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close()