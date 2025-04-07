#!/usr/bin/env python3
"""
Install certificates for Python on macOS.
This script installs the certificates for Python on macOS, which is necessary for SSL verification.
"""

import os
import ssl
import subprocess
import sys
import tempfile
import urllib.request
import urllib.error

def install_certificates():
    """
    Install certificates for Python on macOS.
    """
    print("Installing certificates for Python on macOS...")
    
    # Check if we're on macOS
    if sys.platform != "darwin":
        print("This script is only for macOS. Exiting.")
        return
    
    # Check if we're using Python from Python.org
    python_path = sys.executable
    if "Python.framework" not in python_path:
        print("This script is only for Python installed from Python.org. Exiting.")
        return
    
    # Get the path to the certificates
    cert_path = os.path.join(os.path.dirname(python_path), "..", "Resources", "Python.app", "Contents", "MacOS", "Install Certificates.command")
    
    if os.path.exists(cert_path):
        print(f"Found certificate installer at: {cert_path}")
        print("Running certificate installer...")
        
        # Run the certificate installer
        subprocess.run(["bash", cert_path], check=True)
        
        print("Certificate installation complete.")
    else:
        print(f"Certificate installer not found at: {cert_path}")
        print("Trying alternative method...")
        
        # Try to download the certificates manually
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as temp_cert:
                temp_cert_path = temp_cert.name
            
            # Download the certificates
            print("Downloading certificates...")
            urllib.request.urlretrieve("https://curl.se/ca/cacert.pem", temp_cert_path)
            
            # Set the SSL_CERT_FILE environment variable
            os.environ["SSL_CERT_FILE"] = temp_cert_path
            print(f"Set SSL_CERT_FILE to: {temp_cert_path}")
            
            print("Certificate installation complete.")
        except Exception as e:
            print(f"Failed to download certificates: {str(e)}")
            print("Please install certificates manually.")

if __name__ == "__main__":
    install_certificates() 