/**
 * API Handler - VULNERABLE CODE (intentional for testing)
 * 
 * This file contains multiple security vulnerabilities that a
 * security scanner should detect.
 */
const { exec } = require("child_process");
const mysql = require("mysql");
const fs = require("fs");
const serialize = require("node-serialize");

// VULNERABILITY: Hardcoded secrets
const DB_PASSWORD = "mysql_pr0d_p@ssw0rd!";
const JWT_SECRET = "super-secret-jwt-key-never-commit";
const API_KEY = "api_key_prod_x9y8z7w6v5u4t3s2r1";
const WEBHOOK_SECRET = "whsec_prod_abc123def456ghi789";

const db = mysql.createConnection({
  host: "prod-db.company.com",
  user: "root",
  password: DB_PASSWORD,
  database: "app_production",
});


// VULNERABILITY: SQL Injection
function getUser(req, res) {
  const userId = req.params.id;
  // Direct string concatenation in SQL query
  db.query("SELECT * FROM users WHERE id = " + userId, (err, results) => {
    res.json(results);
  });
}

function searchUsers(req, res) {
  const name = req.query.name;
  // Template literal SQL injection
  db.query(`SELECT * FROM users WHERE name LIKE %%`, (err, results) => {
    res.json(results);
  });
}

function loginUser(req, res) {
  const { username, password } = req.body;
  // SQL injection in authentication
  const query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'";
  db.query(query, (err, results) => {
    if (results.length > 0) {
      res.json({ token: JWT_SECRET });
    }
  });
}


// VULNERABILITY: Command Injection
function convertImage(req, res) {
  const filename = req.body.filename;
  // Command injection via exec
  exec("convert /uploads/" + filename + " /outputs/thumb.png", (err) => {
    res.json({ status: "ok" });
  });
}

function pingHost(req, res) {
  const host = req.query.host;
  // Command injection
  exec(`ping -c 4 ${host}`, (err, stdout) => {
    res.send(stdout);
  });
}


// VULNERABILITY: Path Traversal
function downloadFile(req, res) {
  const filename = req.params.filename;
  // No path sanitization
  const filepath = "/var/data/files/" + filename;
  res.sendFile(filepath);
}

function readLog(req, res) {
  const logName = req.query.name;
  // Path traversal
  const content = fs.readFileSync(`/var/log/app/${logName}`, "utf8");
  res.send(content);
}


// VULNERABILITY: Insecure Deserialization
function processPayload(req, res) {
  const data = req.body.data;
  // Insecure deserialization
  const obj = serialize.unserialize(data);
  res.json(obj);
}


// VULNERABILITY: XSS (Reflected)
function renderPage(req, res) {
  const name = req.query.name;
  // Reflected XSS - user input directly in HTML
  res.send(`<html><body><h1>Hello ${name}</h1></body></html>`);
}

function renderError(req, res) {
  const error = req.query.message;
  // Reflected XSS
  res.send("<div class='error'>" + error + "</div>");
}


// VULNERABILITY: Missing authentication/authorization
function deleteUser(req, res) {
  // No auth check - any request can delete any user
  const userId = req.params.id;
  db.query(`DELETE FROM users WHERE id = ${userId}`, (err) => {
    res.json({ deleted: true });
  });
}

function adminPanel(req, res) {
  // No authentication check for admin endpoint
  db.query("SELECT * FROM users", (err, results) => {
    res.json(results);
  });
}


module.exports = {
  getUser, searchUsers, loginUser, convertImage, pingHost,
  downloadFile, readLog, processPayload, renderPage,
  renderError, deleteUser, adminPanel,
};

