/**
 * API Handler - CLEAN CODE (secure implementation)
 *
 * This file demonstrates secure coding practices.
 * A security scanner should NOT flag any issues here.
 */
const crypto = require("crypto");
const path = require("path");
const { execFile } = require("child_process");


// Configuration from environment (not hardcoded)
const DB_CONFIG = {
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
};


/**
 * Get user by ID - uses parameterized query.
 */
function getUser(db, req, res) {
  const userId = parseInt(req.params.id, 10);
  if (isNaN(userId)) {
    return res.status(400).json({ error: "Invalid user ID" });
  }
  db.query("SELECT id, name, email FROM users WHERE id = ?", [userId], (err, results) => {
    if (err) return res.status(500).json({ error: "Database error" });
    res.json(results[0] || null);
  });
}


/**
 * Search users - parameterized LIKE query.
 */
function searchUsers(db, req, res) {
  const name = req.query.name || "";
  db.query(
    "SELECT id, name, email FROM users WHERE name LIKE ?",
    [`%${name}%`],
    (err, results) => {
      if (err) return res.status(500).json({ error: "Database error" });
      res.json(results);
    }
  );
}


/**
 * Safe file download with path validation.
 */
function downloadFile(req, res) {
  const filename = path.basename(req.params.filename); // Strip directory traversal
  const basePath = "/var/data/files";
  const fullPath = path.resolve(basePath, filename);

  // Ensure resolved path is within base directory
  if (!fullPath.startsWith(basePath)) {
    return res.status(403).json({ error: "Access denied" });
  }

  res.sendFile(fullPath);
}


/**
 * Render page with proper output encoding (no XSS).
 */
function renderPage(req, res) {
  const name = escapeHtml(req.query.name || "Guest");
  res.send(`<html><body><h1>Hello ${name}</h1></body></html>`);
}


/**
 * Verify webhook with HMAC signature.
 */
function verifyWebhook(payload, signature, secret) {
  const expected = crypto
    .createHmac("sha256", secret)
    .update(payload)
    .digest("hex");
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}


/**
 * Generate secure random token.
 */
function generateToken() {
  return crypto.randomBytes(32).toString("hex");
}


/**
 * Safe command execution using execFile (no shell).
 */
function convertImage(inputPath, outputPath, callback) {
  // execFile does NOT invoke a shell - safe from injection
  execFile("convert", [inputPath, outputPath], callback);
}


/**
 * HTML escaping utility.
 */
function escapeHtml(text) {
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#039;" };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}


/**
 * Simple math utilities - no security concerns.
 */
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function formatCurrency(amount) {
  return `$${amount.toFixed(2)}`;
}


module.exports = {
  getUser, searchUsers, downloadFile, renderPage,
  verifyWebhook, generateToken, convertImage,
  calculateTotal, formatCurrency,
};

