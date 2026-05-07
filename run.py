"""
WebStore Backend - Entry Point
Run with: python run.py
"""
from flask import Flask, jsonify
from flask_cors import CORS
import flask_app

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 WebStore Backend API")
    print("=" * 50)
    print("📍 API URL: http://localhost:5001")
    print("📍 Health Check: http://localhost:5001/api/health")
    print("=" * 50)
    flask_app.app.run(host='127.0.0.1', port=5001, debug=True)
