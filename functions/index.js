
// Firebase Functions — Daily cron 08:00 Europe/Paris
// Sends a daily digest email of open tasks (J-21/J-7/J-3) per store.
// Prereq:
//   firebase functions:config:set sendgrid.key="SG.xxxxx"
//   firebase functions:config:set email.from="alerts@smartexpiry.app"
// Optional per-store recipient in Firestore: stores/{storeId}.digestEmail
// Fallback recipient via: firebase functions:config:set email.to="timotonou@yahoo.com"

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const sgMail = require('@sendgrid/mail');

admin.initializeApp();
const db = admin.firestore();

const SENDGRID_KEY = functions.config().sendgrid && functions.config().sendgrid.key;
const EMAIL_FROM = (functions.config().email && functions.config().email.from) || 'alerts@smartexpiry.app';
const EMAIL_TO_FALLBACK = functions.config().email && functions.config().email.to;

if (!SENDGRID_KEY) {
  console.warn('⚠️ SendGrid API key not set. Use: firebase functions:config:set sendgrid.key="SG.XXXX"');
} else {
  sgMail.setApiKey(SENDGRID_KEY);
}

function stageLabel(stage) {
  return {
    'J-21': 'À 3 semaines — Planifier une promotion',
    'J-7':  'À 1 semaine — Mettre en avant / -20%',
    'J-3':  'À 3 jours — Action immédiate / -50%'
  }[stage] || stage;
}

function buildHtml(storeId, tasksByStage) {
  const sections = ['J-21','J-7','J-3'].map(stage => {
    const items = tasksByStage[stage] || [];
    if (!items.length) return '';
    const rows = items.map(t => `
      <tr style="border-bottom:1px solid #e5e7eb">
        <td style="padding:10px">${t.productId || ''}</td>
        <td style="padding:10px;font-weight:700">${t.lotNumber || ''}</td>
        <td style="padding:10px">${t.quantity || 0}</td>
        <td style="padding:10px">${t.expiryDate ? t.expiryDate.toDate().toLocaleDateString('fr-FR') : ''}</td>
        <td style="padding:10px">${t.daysLeft ?? ''}</td>
        <td style="padding:10px">${t.location || ''}</td>
      </tr>
    `).join('');
    return `
      <h3>${stageLabel(stage)}</h3>
      <table style="width:100%;border-collapse:collapse;border:1px solid #e5e7eb;border-radius:8px;overflow:hidden">
        <thead>
          <tr style="background:#f9fafb">
            <th style="padding:10px;text-align:left;font-size:12px;color:#6b7280">Produit</th>
            <th style="padding:10px;text-align:left;font-size:12px;color:#6b7280">Lot</th>
            <th style="padding:10px;text-align:left;font-size:12px;color:#6b7280">Qté</th>
            <th style="padding:10px;text-align:left;font-size:12px;color:#6b7280">DLC</th>
            <th style="padding:10px;text-align:left;font-size:12px;color:#6b7280">Jours</th>
            <th style="padding:10px;text-align:left;font-size:12px;color:#6b7280">Rayon</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table><br/>
    `;
  }).join('');

  const body = sections.trim() || '<p>Toutes les tâches sont à jour ✅</p>';

  return `<!doctype html><html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f3f4f6;margin:0;">
    <div style="max-width:640px;margin:0 auto;background:#fff;">
      <div style="background:linear-gradient(135deg,#3b82f6 0%,#6366f1 100%);padding:22px;color:#fff;border-radius:0;">
        <h2 style="margin:0">SmartExpiry Assistant — Digest quotidien</h2>
        <div style="opacity:.9">Magasin: ${storeId}</div>
      </div>
      <div style="padding:20px">${body}</div>
      <div style="background:#f9fafb;padding:14px;text-align:center;color:#6b7280;font-size:12px;border-top:1px solid #e5e7eb">
        SmartExpiry · Optimisation FEFO & marges
      </div>
    </div>
  </body></html>`;
}

exports.dailyDigest0800 = functions.pubsub
  .schedule('0 8 * * *')
  .timeZone('Europe/Paris')
  .onRun(async (context) => {
    console.log('⏰ CRON 08:00 — Daily digest start');
    if (!SENDGRID_KEY) { console.error('No SendGrid key. Abort.'); return null; }

    const storesSnap = await db.collection('stores').get();
    if (storesSnap.empty) { console.log('No stores.'); return null; }

    const todayStr = new Date().toISOString().slice(0,10);

    for (const storeDoc of storesSnap.docs) {
      const storeId = storeDoc.id;
      const storeData = storeDoc.data() || {};
      const toEmail = storeData.digestEmail || storeData.managerEmail || EMAIL_TO_FALLBACK;

      if (!toEmail) { console.warn(`No recipient for store ${storeId}`); continue; }

      // avoid duplicate per day
      const logId = `DIGEST_${storeId}_${todayStr}`;
      const logRef = db.collection('emailLogs').doc(logId);
      const logSnap = await logRef.get();
      if (logSnap.exists) { console.log(`Skip (already sent) ${logId}`); continue; }

      // open tasks by stage
      const tasksSnap = await db.collection('stores').doc(storeId).collection('tasks').get();
      const byStage = { 'J-21':[], 'J-7':[], 'J-3':[] };
      tasksSnap.forEach(d => {
        const t = d.data();
        if (t.status === 'open' && byStage[t.stage]) byStage[t.stage].push(t);
      });

      const totalOpen = byStage['J-21'].length + byStage['J-7'].length + byStage['J-3'].length;
      const html = buildHtml(storeId, byStage);

      try {
        await sgMail.send({ to: toEmail, from: EMAIL_FROM, subject: `SmartExpiry — Digest (${totalOpen} tâches ouvertes)`, html });
        await logRef.set({ storeId, date: todayStr, sentAt: admin.firestore.FieldValue.serverTimestamp(), status: 'sent', source: 'cron', to: toEmail });
        console.log(`✅ Sent digest to ${toEmail} for store ${storeId}`);
      } catch (e) {
        await logRef.set({ storeId, date: todayStr, sentAt: admin.firestore.FieldValue.serverTimestamp(), status: 'error', error: e.message, source: 'cron', to: toEmail });
        console.error(`❌ Send failed for ${storeId}:`, e.message);
      }
    }
    console.log('✅ CRON done');
    return null;
  });
