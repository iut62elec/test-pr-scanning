package com.example.vulnerable;

import java.io.*;
import java.net.*;
import java.sql.*;
import javax.xml.parsers.*;
import org.xml.sax.InputSource;

/**
 * Data Access Layer - VULNERABLE CODE (intentional for testing).
 *
 * Contains common Java security vulnerabilities that a scanner should detect.
 */
public class DataAccessLayer {

    // VULNERABILITY: Hardcoded database credentials
    private static final String DB_URL = "jdbc:mysql://prod-server:3306/app";
    private static final String DB_USER = "root";
    private static final String DB_PASS = "r00t_pr0d_p@ss!";
    private static final String API_KEY = "java-api-key-prod-abc123xyz";

    private Connection connection;

    public DataAccessLayer() throws SQLException {
        this.connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
    }


    // VULNERABILITY: SQL Injection via string concatenation
    public ResultSet getUser(String userId) throws SQLException {
        Statement stmt = connection.createStatement();
        return stmt.executeQuery("SELECT * FROM users WHERE id = '" + userId + "'");
    }

    public ResultSet searchProducts(String keyword) throws SQLException {
        Statement stmt = connection.createStatement();
        return stmt.executeQuery(
            "SELECT * FROM products WHERE name LIKE '%" + keyword + "%'"
        );
    }

    public void deleteRecord(String table, String id) throws SQLException {
        Statement stmt = connection.createStatement();
        stmt.executeUpdate("DELETE FROM " + table + " WHERE id = " + id);
    }


    // VULNERABILITY: Command Injection
    public String runDiagnostic(String hostname) throws IOException {
        Runtime rt = Runtime.getRuntime();
        Process proc = rt.exec("ping -c 4 " + hostname);
        BufferedReader reader = new BufferedReader(
            new InputStreamReader(proc.getInputStream())
        );
        StringBuilder output = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }
        return output.toString();
    }

    public void generateReport(String reportName) throws IOException {
        Runtime.getRuntime().exec("bash -c report-gen " + reportName);
    }


    // VULNERABILITY: Path Traversal
    public byte[] readFile(String filename) throws IOException {
        File file = new File("/var/data/uploads/" + filename);
        FileInputStream fis = new FileInputStream(file);
        byte[] data = fis.readAllBytes();
        fis.close();
        return data;
    }


    // VULNERABILITY: XXE (XML External Entity)
    public String parseXml(String xmlInput) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        // Not disabling external entities = XXE vulnerability
        DocumentBuilder builder = factory.newDocumentBuilder();
        InputSource is = new InputSource(new StringReader(xmlInput));
        var doc = builder.parse(is);
        return doc.getDocumentElement().getTextContent();
    }


    // VULNERABILITY: SSRF
    public String fetchUrl(String targetUrl) throws IOException {
        URL url = new URL(targetUrl);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        BufferedReader reader = new BufferedReader(
            new InputStreamReader(conn.getInputStream())
        );
        StringBuilder response = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            response.append(line);
        }
        return response.toString();
    }


    // VULNERABILITY: Insecure Deserialization
    public Object deserialize(byte[] data) throws Exception {
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
        return ois.readObject();
    }


    // VULNERABILITY: Weak hashing
    public String hashData(String input) throws Exception {
        java.security.MessageDigest md = java.security.MessageDigest.getInstance("MD5");
        byte[] digest = md.digest(input.getBytes());
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}

