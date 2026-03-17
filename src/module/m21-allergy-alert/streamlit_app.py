"""
Main Streamlit app for M21 Allergy Alert System
Optimized for Streamlit Cloud deployment with MongoDB Atlas
"""
import streamlit as st
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main app
from frontend.app import main

if __name__ == "__main__":
    main()