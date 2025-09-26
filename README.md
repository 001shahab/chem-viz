# ChemViz — Molecular Visualization Reimagined

*Designed and developed by **Prof. Shahab Anbarjafari** from **3S Holding OÜ***

A revolutionary molecular visualization platform that combines the power of artificial intelligence with stunning 3D graphics. Experience chemistry like never before with our Apple-inspired, minimalist interface that makes complex molecular structures accessible to everyone.

> *"Simplicity is the ultimate sophistication."* — Leonardo da Vinci

ChemViz embodies this philosophy, delivering professional-grade molecular visualization through an interface so intuitive, it feels magical.

## ✨ What Makes ChemViz Special

### 🎨 **Apple-Inspired Design**
- **Glass Morphism UI**: Translucent cards with backdrop blur effects
- **SF Pro Typography**: Clean, readable fonts that scale beautifully
- **Intuitive Interactions**: Every tap, click, and gesture feels natural
- **Minimalist Layout**: Focus on what matters — your molecules

### 🧠 **Intelligent Chemistry**
- **AI-Powered Parsing**: OpenAI GPT understands natural language chemistry
- **Smart Fallbacks**: Multiple data sources ensure reliability
- **Instant Recognition**: From "aspirin" to complex SMILES notation
- **Error Recovery**: Helpful suggestions when things don't work

### 🔬 **Professional Visualization**
- **Interactive 3D Models**: Rotate, zoom, and explore molecules
- **Color-Coded Elements**: Intuitive atomic color schemes
- **Real-Time Rendering**: Smooth animations and transitions
- **Publication Ready**: High-quality visuals for research and education

### 📊 **Comprehensive Analysis**
- **Molecular Properties**: Weight, LogP, TPSA, and more
- **Structural Insights**: Bond counts, rings, and descriptors
- **Chemical Intelligence**: IUPAC names, formulas, and identifiers

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd chem-viz
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** and navigate to `http://localhost:8501`

## 🎯 Usage

1. **Enter a chemical compound** in any of these formats:
   - Chemical name: `caffeine`, `aspirin`, `benzene`
   - Molecular formula: `C8H10N4O2`, `C6H6`
   - SMILES notation: `CCO`, `c1ccccc1`

2. **Click "Visualize"** to generate the 3D molecular structure

3. **Explore the molecule**:
   - Rotate, zoom, and pan the 3D model
   - View molecular properties and descriptors
   - See color-coded atoms and bonds

## 🎨 Atom Color Coding

- **🔴 Red**: Oxygen (O)
- **🔵 Blue**: Nitrogen (N)
- **⚫ Gray**: Carbon (C)
- **⚪ White**: Hydrogen (H)
- **🟡 Yellow**: Sulfur (S)
- **🟠 Orange**: Phosphorus (P)
- **🟢 Green**: Fluorine (F)
- **🟣 Purple**: Iodine (I)

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **AI**: OpenAI GPT for chemical parsing
- **Chemistry**: RDKit for molecular structure generation
- **Visualization**: py3Dmol for 3D rendering
- **Data**: PubChem integration for chemical data

## 📁 Project Structure

```
chem-viz/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── env.example        # Environment variables template
├── .env              # Your API keys (create from env.example)
├── myenv/            # Virtual environment
└── README.md         # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Customization

You can customize the application by modifying:

- **Atom colors**: Edit the `atom_colors` dictionary in `ChemVizService`
- **UI styling**: Modify the CSS in the `st.markdown()` sections
- **Molecular properties**: Add more descriptors in `get_molecule_properties()`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💼 About the Creator

**Prof. Shahab Anbarjafari** is a distinguished researcher and entrepreneur, leading innovation at **3S Holding OÜ**. With expertise spanning artificial intelligence, computer vision, and computational chemistry, Prof. Anbarjafari brings a unique perspective to molecular visualization.

### 🏢 3S Holding OÜ
A forward-thinking technology company focused on developing cutting-edge solutions that bridge the gap between complex scientific concepts and intuitive user experiences.

## 🎨 Design Philosophy

ChemViz follows Apple's design principles:

- **Simplicity**: Remove the unnecessary to highlight the essential
- **Clarity**: Every element serves a purpose and communicates clearly  
- **Deference**: The interface never competes with the content
- **Depth**: Visual layers create hierarchy and understanding
- **Consistency**: Familiar patterns reduce cognitive load

## 🙏 Acknowledgments

- **OpenAI** for the revolutionary GPT API
- **RDKit** for robust molecular informatics
- **Streamlit** for the elegant web framework
- **py3Dmol** for stunning 3D visualization
- **Apple** for design inspiration and SF Pro typography

## 🐛 Troubleshooting

### Common Issues

1. **NumPy compatibility error (`_ARRAY_API not found`)**:
   ```bash
   # The app requires NumPy < 2.0 for RDKit compatibility
   source myenv/bin/activate
   pip install --force-reinstall "numpy<2.0.0,>=1.24.0"
   ```

2. **RDKit installation issues**: 
   ```bash
   conda install -c conda-forge rdkit
   ```

3. **OpenAI API errors**: 
   - Check your API key in `.env` file
   - Verify billing status and API limits
   - The app includes fallback to PubChem if OpenAI fails

4. **JSON parsing errors**: 
   - The app now includes robust error handling
   - Falls back to PubChem and direct SMILES parsing

5. **Molecule not found**: Try different naming conventions or SMILES notation

6. **3D visualization not loading**: Ensure all dependencies are installed correctly

### Testing Your Installation

Run the test suite to verify everything is working:
```bash
source myenv/bin/activate
python test_app.py
```

Or run the app with automatic testing:
```bash
./run.sh --test
```

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.