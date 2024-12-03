from flask import Flask, request, send_file, jsonify, render_template
import subprocess
import os

app = Flask(__name__)
CA_KEY = "/app/ca/ca.key"
CA_CERT = "/app/ca/ca.crt"
CERT_DIR = "/app/certs"

# Crear la CA si no existe
if not os.path.exists(CA_KEY) or not os.path.exists(CA_CERT):
    subprocess.run([
        "openssl", "genrsa", "-out", CA_KEY, "4096"
    ])
    subprocess.run([
        "openssl", "req", "-x509", "-new", "-nodes", "-key", CA_KEY,
        "-sha256", "-days", "3650", "-out", CA_CERT,
        "-subj", "/C=ES/ST=Madrid/L=Madrid/O=Dominio Local/OU=IT Department/CN=Dominio Local CA/emailAddress=info@dominio.local"
    ])


@app.route('/')
def home():
    return render_template("index.html")


def sanitize_filename(domain):
    """Reemplaza los puntos en el dominio por guiones bajos"""
    return domain.replace('.', '_')

@app.route('/generate', methods=['POST'])
def generate_cert():
    domain = request.form.get('domain', 'example.local')
    sanitized_domain = sanitize_filename(domain)  # Reemplazar puntos
    private_key = f"{sanitized_domain}.key"
    csr_file = f"{sanitized_domain}.csr"
    cert_file = f"{sanitized_domain}.crt"
    
    # Ruta completa
    private_key_path = os.path.join(CERT_DIR, private_key)
    csr_path = os.path.join(CERT_DIR, csr_file)
    cert_path = os.path.join(CERT_DIR, cert_file)

    # Generar clave privada
    subprocess.run(["openssl", "genrsa", "-out", private_key_path, "2048"])
    # Generar CSR
    subprocess.run([
        "openssl", "req", "-new", "-key", private_key_path, "-out", csr_path,
        "-subj", f"/C=ES/ST=Madrid/L=Madrid/O=Dominio Local/OU=IT Department/CN={domain}/emailAddress=info@dominio.local"
    ])
    # Generar Certificado
    subprocess.run([
        "openssl", "x509", "-req", "-in", csr_path, "-CA", CA_CERT, "-CAkey", CA_KEY,
        "-CAcreateserial", "-out", cert_path, "-days", "3650", "-sha256"
    ])

    return render_template('download.html', 
                           domain=domain, 
                           private_key=f"/download/{private_key}",
                           certificate=f"/download/{cert_file}")


@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(CERT_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/ca', methods=['GET'])
def get_ca():
    return send_file(CA_CERT, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
