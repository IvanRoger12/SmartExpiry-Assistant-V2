/**
 * SMARTEXPIRY — Firebase Cloud Functions
 * 
 * Daily CRON: 08:00 Europe/Paris
 * Sends digest emails for all stores with open tasks (J-21/J-7/J-3)
 * 
 * SETUP:
 *   1. firebase functions:config:set sendgrid.key="SG.xxxxx"
 *   2. firebase functions:config:set email.from="alerts@smartexpiry.app"
 *   3. firebase functions:config:set email.to="fallback@domain.com"
 *   4. npm install firebase-functions firebase-admin @sendgrid/mail
 *   5. firebase deploy --only functions
 * 
 * OPTIONAL:
 *   Set per-store digestEmail in stores/{storeId} doc
 */

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const sgMail = require('@sendgrid/mail');

// ═════════════════════════════════════════════════════════════════════════
// INIT
// ═════════════════════════════════════════════════════════════════════════

admin.initializeApp();
const db = admin.firestore();

// Config from Firebase environment
const SENDGRID_KEY = functions.config().sendgrid?.key;
const EMAIL_FROM = functions.config().email?.from || 'alerts@smartexpiry.app';
const EMAIL_TO_FALLBACK = functions.config().email?.to;

if (!SENDGRID_KEY) {
  console.warn('⚠️ SendGrid API key not configured.');
  console.warn('   Run: firebase functions:config:set sendgrid.key="SG.xxxxx"');
} else {
  sgMail.setApiKey(SENDGRID_KEY);
}

// ═════════════════════════════════════════════════════════════════════════
// HELPERS
// ═════════════════════════════════════════════════════════════════════════

/**
 * Maps stage key to French label
 */
function stageLabel(stage) {
  const labels = {
    'J-21': 'À 3 semaines — Planifier une promotion',
    'J-7': 'À 1 semaine — Mettre en avant / -20%',
    'J-3': 'À 3 jours — Action immédiate / -50%'
  };
  return labels[stage] || stage;
}

/**
 * Formats a date to DD/MM/YYYY
 */
function formatDate(timestamp) {
  if (!timestamp) return '';
  try {
    const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp);
    return date.toLocaleDateString('fr-FR');
  } catch {
    return '';
  }
}

/**
 * Builds HTML digest email
 */
function buildDigestHtml(storeId, tasksByStage) {
  const sections = ['J-21', 'J-7', 'J-3']
    .map(stage => {
      const items = tasksByStage[stage] || [];
      if (items.length === 0) return '';

      // Sort by DLC (earliest first — FEFO)
      items.sort((a, b) => {
        const dateA = a.expiryDate?.toDate?.() || new Date(a.expiryDate);
        const dateB = b.expiryDate?.toDate?.() || new Date(b.expiryDate);
        return dateA - dateB;
      });

      const rows = items
        .map(task => `
          <tr style="border-bottom:1px solid #e5e7eb;">
            <td style="padding:12px;font-size:0.875rem;">${task.productId || ''}</td>
            <td style="padding:12px;font-weight:700;color:#111827;">${task.lotNumber || ''}</td>
            <td style="padding:12px;">${task.quantity || 0}</td>
            <td style="padding:12px;">${formatDate(task.expiryDate)}</td>
            <td style="padding:12px;">${task.daysLeft ?? ''}</td>
            <td style="padding:12px;font-size:0.875rem;color:#6b7280;">${task.location || ''}</td>
          </tr>
        `)
        .join('');

      return `
        <h3 style="margin:20px 0 12px 0;color:#111827;font-size:1.125rem;font-weight:700;">
          ${stageLabel(stage)}
        </h3>
        <table style="width:100%;border-collapse:collapse;border:1px solid #e5e7eb;border-radius:8px;overflow:hidden;margin-bottom:24px;">
          <thead>
            <tr style="background:#f9fafb;">
              <th style="padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;">Produit</th>
              <th style="padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;">Lot</th>
              <th style="padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;">Qté</th>
              <th style="padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;">DLC</th>
              <th style="padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;">Jours</th>
              <th style="padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;">Rayon</th>
            </tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      `;
    })
    .join('');

  const body =
    sections.trim() ||
    '<p style="color:#6b7280;text-align:center;padding:20px;">✅ Toutes les tâches sont à jour</p>';

  const totalTasks = (tasksByStage['J-21'] || []).length +
    (tasksByStage['J-7'] || []).length +
    (tasksByStage['J-3'] || []).length;

  return `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
      </head>
      <body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f3f4f6;margin:0;padding:0;">
        <div style="max-width:680px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 10px 25px rgba(0,0,0,0.1);">
          <!-- HEADER -->
          <div style="background:linear-gradient(135deg,#3b82f6 0%,#6366f1 100%);padding:28px;color:#fff;">
            <h2 style="margin:0;font-size:24px;font-weight:900;">SmartExpiry Assistant</h2>
            <p style="margin:8px 0 0 0;opacity:0.9;font-size:14px;">Digest quotidien — ${totalTasks} tâche(s) ouverte(s)</p>
            <p style="margin:4px 0 0 0;opacity:0.8;font-size:12px;">Magasin: <strong>${storeId}</strong></p>
          </div>

          <!-- CONTENT -->
          <div style="padding:28px;color:#111827;">
            ${body}
            
            <div style="text-align:center;margin-top:32px;">
              <a href="#" style="display:inline-block;background:#2563eb;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:800;font-size:14px;transition:all 0.2s ease;">
                Ouvrir le dashboard →
              </a>
            </div>
          </div>

          <!-- FOOTER -->
          <div style="background:#f9fafb;padding:16px;text-align:center;color:#6b7280;font-size:12px;border-top:1px solid #e5e7eb;">
            <p style="margin:0;">SmartExpiry · Optimisation FEFO & Marges</p>
            <p style="margin:4px 0 0 0;opacity:0.7;">Envoyé le ${new Date().toLocaleDateString('fr-FR')} à ${new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</p>
          </div>
        </div>
      </body>
    </html>
  `;
}

// ═════════════════════════════════════════════════════════════════════════
// CLOUD FUNCTION — DAILY CRON
// ═════════════════════════════════════════════════════════════════════════

/**
 * Daily digest email scheduler (08:00 Europe/Paris)
 * 
 * Sends digest emails to all stores with:
 * - Open tasks in J-21, J-7, J-3 stages
 * - Anti-duplicate check (per day per store)
 * - Error logging in Firestore
 */
exports.dailyDigest0800 = functions.pubsub
  .schedule('0 8 * * *')
  .timeZone('Europe/Paris')
  .onRun(async context => {
    console.log('⏰ [CRON] Daily digest 08:00 Europe/Paris — START');

    // ─────────────────────────────────────────────────────────────────────
    // VALIDATION
    // ─────────────────────────────────────────────────────────────────────

    if (!SENDGRID_KEY) {
      console.error('❌ [ABORT] SendGrid API key not configured');
      return null;
    }

    if (!EMAIL_TO_FALLBACK && !db) {
      console.error('❌ [ABORT] No email configuration');
      return null;
    }

    // ─────────────────────────────────────────────────────────────────────
    // LOAD STORES
    // ─────────────────────────────────────────────────────────────────────

    let storesSnap;
    try {
      storesSnap = await db.collection('stores').get();
    } catch (e) {
      console.error('❌ [ERROR] Failed to load stores:', e.message);
      return null;
    }

    if (storesSnap.empty) {
      console.log('ℹ️  No stores found. Skipping.');
      return null;
    }

    console.log(`✓ Found ${storesSnap.size} store(s)`);

    // ─────────────────────────────────────────────────────────────────────
    // PROCESS EACH STORE
    // ─────────────────────────────────────────────────────────────────────

    const todayStr = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
    const results = { sent: 0, skipped: 0, errors: 0 };

    for (const storeDoc of storesSnap.docs) {
      const storeId = storeDoc.id;
      const storeData = storeDoc.data() || {};

      // Resolve recipient (priority: per-store > fallback)
      const toEmail = storeData.digestEmail || storeData.managerEmail || EMAIL_TO_FALLBACK;

      if (!toEmail) {
        console.warn(`⚠️  [${storeId}] No recipient configured. Skipping.`);
        results.skipped++;
        continue;
      }

      // ───────────────────────────────────────────────────────────────────
      // ANTI-DUPLICATE CHECK
      // ───────────────────────────────────────────────────────────────────

      const logId = `DIGEST_${storeId}_${todayStr}`;
      const logRef = db.collection('emailLogs').doc(logId);

      try {
        const logSnap = await logRef.get();
        if (logSnap.exists) {
          console.log(`⏭️  [${storeId}] Already sent today. Skipping.`);
          results.skipped++;
          continue;
        }
      } catch (e) {
        console.error(`❌ [${storeId}] Failed to check log:`, e.message);
        results.errors++;
        continue;
      }

      // ───────────────────────────────────────────────────────────────────
      // LOAD TASKS
      // ───────────────────────────────────────────────────────────────────

      let tasksSnap;
      try {
        tasksSnap = await db
          .collection('stores')
          .doc(storeId)
          .collection('tasks')
          .get();
      } catch (e) {
        console.error(`❌ [${storeId}] Failed to load tasks:`, e.message);
        results.errors++;
        continue;
      }

      // ───────────────────────────────────────────────────────────────────
      // GROUP BY STAGE & FILTER OPEN TASKS
      // ───────────────────────────────────────────────────────────────────

      const tasksByStage = {
        'J-21': [],
        'J-7': [],
        'J-3': []
      };

      tasksSnap.forEach(taskDoc => {
        const task = taskDoc.data();
        if (task.status === 'open' && tasksByStage[task.stage]) {
          tasksByStage[task.stage].push(task);
        }
      });

      const totalOpen =
        tasksByStage['J-21'].length +
        tasksByStage['J-7'].length +
        tasksByStage['J-3'].length;

      if (totalOpen === 0) {
        console.log(`ℹ️  [${storeId}] No open tasks. Logging as sent (no email).`);
        try {
          await logRef.set({
            storeId,
            date: todayStr,
            sentAt: admin.firestore.FieldValue.serverTimestamp(),
            status: 'sent',
            source: 'cron',
            to: toEmail,
            totalTasks: 0,
            reason: 'no_open_tasks'
          });
          results.sent++;
        } catch (e) {
          console.error(`❌ [${storeId}] Failed to log:`, e.message);
          results.errors++;
        }
        continue;
      }

      // ───────────────────────────────────────────────────────────────────
      // BUILD & SEND EMAIL
      // ───────────────────────────────────────────────────────────────────

      const html = buildDigestHtml(storeId, tasksByStage);
      const subject = `SmartExpiry — Digest quotidien (${totalOpen} tâche(s))`;

      try {
        await sgMail.send({
          to: toEmail,
          from: EMAIL_FROM,
          subject,
          html,
          replyTo: EMAIL_FROM
        });

        console.log(`✅ [${storeId}] Email sent to ${toEmail} (${totalOpen} tasks)`);

        // Log success
        await logRef.set({
          storeId,
          date: todayStr,
          sentAt: admin.firestore.FieldValue.serverTimestamp(),
          status: 'sent',
          source: 'cron',
          to: toEmail,
          totalTasks: totalOpen
        });

        results.sent++;
      } catch (e) {
        console.error(`❌ [${storeId}] Send failed:`, e.message);

        // Log error
        try {
          await logRef.set({
            storeId,
            date: todayStr,
            sentAt: admin.firestore.FieldValue.serverTimestamp(),
            status: 'error',
            source: 'cron',
            to: toEmail,
            error: e.message,
            totalTasks: totalOpen
          });
        } catch (logErr) {
          console.error(`❌ [${storeId}] Failed to log error:`, logErr.message);
        }

        results.errors++;
      }
    }

    // ─────────────────────────────────────────────────────────────────────
    // SUMMARY
    // ─────────────────────────────────────────────────────────────────────

    console.log('');
    console.log('═══════════════════════════════════════════════════════════');
    console.log('📊 CRON SUMMARY');
    console.log('═══════════════════════════════════════════════════════════');
    console.log(`✅ Sent: ${results.sent}`);
    console.log(`⏭️  Skipped: ${results.skipped}`);
    console.log(`❌ Errors: ${results.errors}`);
    console.log(`📅 Date: ${todayStr}`);
    console.log('═══════════════════════════════════════════════════════════');
    console.log('⏰ [CRON] Daily digest 08:00 — COMPLETE');

    return null;
  });
