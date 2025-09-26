import streamlit as st
import openai
import os
from dotenv import load_dotenv
import py3Dmol
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
import pandas as pd
import numpy as np
import json
import requests
import pubchempy as pcp
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import time
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="ChemViz - 3D Molecular Visualizer",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 25%, #2d2d2d 50%, #1a1a1a 75%, #0a0a0a 100%);
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #ffffff;
        min-height: 100vh;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hero Section - Dark Premium Style */
    .hero-section {
        text-align: center;
        padding: 4rem 0 3rem 0;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        margin-bottom: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .main-title {
        font-size: 4.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #a0a0a0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
    }
    
    .main-subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        color: #b0b0b0;
        margin-bottom: 2rem;
        letter-spacing: -0.01em;
    }
    
    .tagline {
        font-size: 1.1rem;
        color: #888888;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.5;
    }
    
    /* Input Section - Dark Premium Style */
    .input-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Custom input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0a84ff !important;
        box-shadow: 0 0 0 4px rgba(10, 132, 255, 0.3), 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        outline: none !important;
        background: rgba(255, 255, 255, 0.12) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888888 !important;
    }
    
    /* Premium Dark Button */
    .stButton > button {
        background: linear-gradient(135deg, #0a84ff 0%, #007aff 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: -0.01em;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 8px 24px rgba(10, 132, 255, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0056cc 0%, #0040a0 100%);
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(10, 132, 255, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(10, 132, 255, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* Content cards - Dark Glass morphism */
    .content-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Visualization container */
    .viz-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        text-align: center;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metrics styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.12);
    }
    
    /* Typography improvements */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    p {
        color: #b0b0b0;
        line-height: 1.6;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #0a84ff transparent transparent transparent;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(52, 199, 89, 0.15);
        border: 1px solid rgba(52, 199, 89, 0.4);
        border-radius: 12px;
        color: #34c759;
    }
    
    .stError {
        background: rgba(255, 59, 48, 0.15);
        border: 1px solid rgba(255, 59, 48, 0.4);
        border-radius: 12px;
        color: #ff3b30;
    }
    
    .stWarning {
        background: rgba(255, 149, 0, 0.15);
        border: 1px solid rgba(255, 149, 0, 0.4);
        border-radius: 12px;
        color: #ff9500;
    }
    
    /* Atom legend styling */
    .atom-legend {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 0 2rem 0;
        color: #888888;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 4rem;
    }
    
    .footer a {
        color: #0a84ff;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .footer a:hover {
        color: #40a0ff;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

class ChemVizService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.atom_colors = {
            'H': '#FFFFFF',   # White
            'C': '#909090',   # Gray
            'N': '#3050F8',   # Blue
            'O': '#FF0D0D',   # Red
            'F': '#90E050',   # Green
            'Cl': '#1FF01F',  # Bright Green
            'Br': '#A62929',  # Brown
            'I': '#940094',   # Purple
            'P': '#FF8000',   # Orange
            'S': '#FFFF30',   # Yellow
            'B': '#FFB5B5',   # Pink
            'Si': '#F0C8A0',  # Tan
            'default': '#FF1493'  # Hot Pink for unknown atoms
        }
    
    def parse_chemical_input(self, user_input):
        """Use OpenAI to parse and understand chemical input"""
        try:
            prompt = f"""
            You are a chemistry expert. Given the input: "{user_input}"
            
            Please provide a JSON response with the following information:
            1. "smiles": The SMILES notation for this molecule (if possible)
            2. "iupac_name": The IUPAC name of the compound
            3. "common_name": Common name(s) of the compound
            4. "molecular_formula": The molecular formula
            5. "description": A brief description of the molecule
            6. "pubchem_cid": PubChem CID if known (or null)
            
            If the input is unclear or not a valid chemical compound, set all fields to null except "description" which should explain the issue.
            
            Return ONLY valid JSON with no additional text, comments, or formatting.
            
            Example for aspirin:
            {{"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O", "iupac_name": "2-acetoxybenzoic acid", "common_name": "aspirin", "molecular_formula": "C9H8O4", "description": "A common pain reliever and anti-inflammatory drug", "pubchem_cid": 2244}}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Using available model instead of gpt-5-nano
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON if there's extra text
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            # Find JSON object in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return json.loads(content)
                
        except json.JSONDecodeError as e:
            st.error(f"Error parsing JSON response: {str(e)}")
            # Fallback: try to get basic info from PubChem
            return self.get_fallback_data(user_input)
        except Exception as e:
            st.error(f"Error with OpenAI API: {str(e)}")
            return self.get_fallback_data(user_input)
    
    def get_fallback_data(self, user_input):
        """Fallback method to get basic chemical data"""
        try:
            # Try PubChem first
            pubchem_data = self.get_molecule_from_pubchem(user_input)
            if pubchem_data:
                return {
                    'smiles': pubchem_data.get('smiles'),
                    'iupac_name': None,
                    'common_name': user_input,
                    'molecular_formula': pubchem_data.get('molecular_formula'),
                    'description': f"Chemical compound: {user_input}",
                    'pubchem_cid': pubchem_data.get('cid')
                }
            
            # If PubChem fails, try to parse as SMILES directly
            mol = Chem.MolFromSmiles(user_input)
            if mol:
                return {
                    'smiles': user_input,
                    'iupac_name': None,
                    'common_name': None,
                    'molecular_formula': rdMolDescriptors.CalcMolFormula(mol),
                    'description': f"SMILES notation: {user_input}",
                    'pubchem_cid': None
                }
            
            return None
        except:
            return None
    
    def get_molecule_from_pubchem(self, compound_name):
        """Get molecule data from PubChem"""
        try:
            compounds = pcp.get_compounds(compound_name, 'name')
            if compounds:
                compound = compounds[0]
                return {
                    'smiles': compound.canonical_smiles,
                    'molecular_formula': compound.molecular_formula,
                    'molecular_weight': compound.molecular_weight,
                    'cid': compound.cid
                }
        except:
            pass
        return None
    
    def create_molecule_from_smiles(self, smiles):
        """Create RDKit molecule from SMILES"""
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return None
            
            # Add hydrogens and generate 3D coordinates
            mol = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol, randomSeed=42)
            AllChem.MMFFOptimizeMolecule(mol)
            
            return mol
        except Exception as e:
            st.error(f"Error creating molecule: {str(e)}")
            return None
    
    def visualize_molecule_3d(self, mol, width=800, height=600):
        """Create 3D visualization using py3Dmol"""
        if mol is None:
            return None
        
        # Convert to mol block
        mol_block = Chem.MolToMolBlock(mol)
        
        # Create HTML for 3D viewer
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://3Dmol.csb.pitt.edu/build/3Dmol-min.js"></script>
            <style>
                #container {{
                    width: {width}px;
                    height: {height}px;
                    margin: 0 auto;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
            </style>
        </head>
        <body>
            <div id="container"></div>
            <script>
                let element = document.getElementById('container');
                let config = {{ backgroundColor: 'white' }};
                let viewer = $3Dmol.createViewer(element, config);
                
                let moldata = `{mol_block}`;
                viewer.addModel(moldata, "mol");
                
                // Set style with color-coded atoms
                viewer.setStyle({{}}, {{stick: {{radius: 0.15}}, sphere: {{scale: 0.25}}}});
                
                // Color atoms by element
                viewer.setStyle({{elem: 'C'}}, {{sphere: {{color: '#909090', scale: 0.4}}, stick: {{color: '#909090'}}}});
                viewer.setStyle({{elem: 'N'}}, {{sphere: {{color: '#3050F8', scale: 0.4}}, stick: {{color: '#3050F8'}}}});
                viewer.setStyle({{elem: 'O'}}, {{sphere: {{color: '#FF0D0D', scale: 0.4}}, stick: {{color: '#FF0D0D'}}}});
                viewer.setStyle({{elem: 'H'}}, {{sphere: {{color: '#FFFFFF', scale: 0.3}}, stick: {{color: '#FFFFFF'}}}});
                viewer.setStyle({{elem: 'S'}}, {{sphere: {{color: '#FFFF30', scale: 0.4}}, stick: {{color: '#FFFF30'}}}});
                viewer.setStyle({{elem: 'P'}}, {{sphere: {{color: '#FF8000', scale: 0.4}}, stick: {{color: '#FF8000'}}}});
                viewer.setStyle({{elem: 'F'}}, {{sphere: {{color: '#90E050', scale: 0.4}}, stick: {{color: '#90E050'}}}});
                viewer.setStyle({{elem: 'Cl'}}, {{sphere: {{color: '#1FF01F', scale: 0.4}}, stick: {{color: '#1FF01F'}}}});
                
                viewer.zoomTo();
                viewer.spin(true);
                viewer.render();
            </script>
        </body>
        </html>
        """
        
        return html_template
    
    def get_molecule_properties(self, mol):
        """Calculate molecular properties"""
        if mol is None:
            return {}
        
        return {
            'Molecular Weight': f"{Descriptors.MolWt(mol):.2f} g/mol",
            'LogP': f"{Descriptors.MolLogP(mol):.2f}",
            'TPSA': f"{Descriptors.TPSA(mol):.2f} Ų",
            'Rotatable Bonds': Descriptors.NumRotatableBonds(mol),
            'H-Bond Donors': Descriptors.NumHDonors(mol),
            'H-Bond Acceptors': Descriptors.NumHAcceptors(mol),
            'Heavy Atoms': mol.GetNumHeavyAtoms(),
            'Rings': Descriptors.RingCount(mol)
        }

def main():
    # Initialize service
    if 'chemviz_service' not in st.session_state:
        st.session_state.chemviz_service = ChemVizService()
    
    service = st.session_state.chemviz_service
    
    # Hero Section - Steve Jobs style
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">ChemViz</h1>
        <p class="main-subtitle">Molecular Visualization Reimagined</p>
        <p class="main-subtitle">Experience chemistry like never before. Enter any molecule and watch it come to life in stunning 3D.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Minimalist design
    with st.sidebar:
        st.markdown("""
        <div class="atom-legend">
            <h3 style="margin-bottom: 1rem; color: #ffffff; font-size: 1.2rem; font-weight: 600;">Atomic Elements</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Elegant atom legend
        elements = [
            ("🔴", "Oxygen", "#FF0D0D"),
            ("🔵", "Nitrogen", "#3050F8"), 
            ("⚫", "Carbon", "#909090"),
            ("⚪", "Hydrogen", "#FFFFFF"),
            ("🟡", "Sulfur", "#FFFF30"),
            ("🟠", "Phosphorus", "#FF8000"),
            ("🟢", "Fluorine", "#90E050"),
            ("🟣", "Iodine", "#940094")
        ]
        
        for emoji, name, color in elements:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 0.75rem; background: rgba(255,255,255,0.08); border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 2px 8px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);">
                <span style="margin-right: 0.75rem; font-size: 1.2rem;">{emoji}</span>
                <span style="color: #ffffff; font-weight: 500; font-size: 0.95rem;">{name}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1.25rem; background: rgba(255,255,255,0.08); border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 2px 8px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);">
            <p style="color: #b0b0b0; font-size: 0.9rem; margin: 0; line-height: 1.4;">
                💡 <strong style="color: #ffffff;">Pro Tip:</strong> Try entering "caffeine", "aspirin", or any SMILES notation for instant visualization.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main input section - Apple-inspired
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # Single column layout for cleaner look
    user_input = st.text_input(
        "Molecule Input",
        placeholder="Enter molecule name, formula, or SMILES notation...",
        help="Examples: caffeine, C8H10N4O2, CCO, c1ccccc1",
        label_visibility="collapsed"
    )
    
    # Center the button perfectly
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        visualize_btn = st.button("✨ Visualize Molecule", type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Processing and visualization
    if visualize_btn and user_input:
        with st.spinner("🔬 Analyzing chemical structure..."):
            # Parse input with OpenAI
            parsed_data = service.parse_chemical_input(user_input)
            
            if parsed_data and parsed_data.get('smiles'):
                # Display molecule information - Dark Premium style
                st.markdown("""
                <div class="content-card">
                    <h3 style="margin-bottom: 1.5rem; color: #ffffff; font-size: 1.5rem;">Molecular Profile</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Information cards
                col1, col2 = st.columns(2, gap="large")
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h4 style="color: #888888; font-size: 0.9rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">IUPAC Name</h4>
                        <p style="color: #ffffff; font-size: 1.1rem; font-weight: 500; margin: 0;">{parsed_data.get('iupac_name', 'Not available')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-container">
                        <h4 style="color: #888888; font-size: 0.9rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">Molecular Formula</h4>
                        <p style="color: #ffffff; font-size: 1.3rem; font-weight: 600; margin: 0; font-family: 'SF Mono', monospace;">{parsed_data.get('molecular_formula', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h4 style="color: #888888; font-size: 0.9rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">Common Name</h4>
                        <p style="color: #ffffff; font-size: 1.1rem; font-weight: 500; margin: 0;">{parsed_data.get('common_name', 'Not available')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if parsed_data.get('pubchem_cid'):
                        st.markdown(f"""
                        <div class="metric-container">
                            <h4 style="color: #888888; font-size: 0.9rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">PubChem ID</h4>
                            <p style="color: #0a84ff; font-size: 1.1rem; font-weight: 500; margin: 0;">{parsed_data.get('pubchem_cid')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                if parsed_data.get('description'):
                    st.markdown(f"""
                    <div class="content-card">
                        <h4 style="color: #888888; font-size: 0.9rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.5px;">About This Molecule</h4>
                        <p style="color: #b0b0b0; font-size: 1rem; line-height: 1.6; margin: 0;">{parsed_data.get('description')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # SMILES notation in a special code block
                st.markdown(f"""
                <div class="content-card">
                    <h4 style="color: #888888; font-size: 0.9rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.5px;">SMILES Notation</h4>
                    <div style="background: rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 1rem; font-family: 'SF Mono', monospace; font-size: 1rem; color: #ffffff; border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);">
                        {parsed_data.get('smiles', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Create molecule
                with st.spinner("🏗️ Building 3D structure..."):
                    mol = service.create_molecule_from_smiles(parsed_data['smiles'])
                    
                    if mol:
                        # 3D Visualization - Dark Premium style
                        st.markdown("""
                        <div class="viz-container">
                            <h3 style="margin-bottom: 2rem; color: #ffffff; font-size: 1.8rem; font-weight: 600;">3D Molecular Structure</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Create 3D visualization
                        html_viewer = service.visualize_molecule_3d(mol, width=900, height=600)
                        if html_viewer:
                            components.html(html_viewer, height=600, width=900)
                        
                        # Molecular properties - Apple metrics style
                        properties = service.get_molecule_properties(mol)
                        if properties:
                            st.markdown("""
                            <div class="content-card" style="margin-top: 3rem;">
                                <h3 style="margin-bottom: 2rem; color: #ffffff; font-size: 1.5rem;">Molecular Properties</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Create elegant property cards
                            prop_items = list(properties.items())
                            
                            # Split into rows of 4
                            for i in range(0, len(prop_items), 4):
                                cols = st.columns(4, gap="medium")
                                for j, (prop, value) in enumerate(prop_items[i:i+4]):
                                    with cols[j]:
                                        st.markdown(f"""
                                        <div class="metric-container">
                                            <h4 style="color: #888888; font-size: 0.8rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">{prop}</h4>
                                            <p style="color: #ffffff; font-size: 1.4rem; font-weight: 600; margin: 0;">{value}</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                    
                    else:
                        st.error("❌ Could not generate 3D structure for this molecule.")
            
            else:
                st.markdown("""
                <div class="content-card" style="border: 2px solid rgba(255, 59, 48, 0.3); background: rgba(255, 59, 48, 0.05);">
                    <h4 style="color: #ff3b30; margin-bottom: 1rem;">Unable to Process Molecule</h4>
                    <p style="color: #515154; margin: 0;">We couldn't parse your input. Please try:</p>
                    <ul style="color: #515154; margin: 1rem 0 0 1rem;">
                        <li>A different chemical name (e.g., "aspirin" instead of "acetylsalicylic acid")</li>
                        <li>The molecular formula (e.g., "C9H8O4")</li>
                        <li>SMILES notation (e.g., "CCO" for ethanol)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    
    elif visualize_btn and not user_input:
        st.markdown("""
        <div class="content-card" style="border: 2px solid rgba(255, 149, 0, 0.3); background: rgba(255, 149, 0, 0.05);">
            <h4 style="color: #ff9500; margin-bottom: 1rem;">Input Required</h4>
            <p style="color: #515154; margin: 0;">Please enter a chemical compound name, formula, or SMILES notation to begin visualization.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer - Apple style
    st.markdown("""
    <div class="footer">
        <p style="margin-bottom: 1rem;">
            <strong>ChemViz</strong> — Molecular visualization reimagined
        </p>
        <p style="margin-bottom: 1rem; font-size: 0.8rem;">
            Designed and developed by <strong>Prof. Shahab Anbarjafari</strong><br>
            <a href="https://3s-holding.com" target="_blank">3S Holding OÜ</a>
        </p>
        <p style="margin: 0; font-size: 0.8rem; opacity: 0.7;">
            Built with precision and passion
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
