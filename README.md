# CadxStudio AI Copilot for Fusion 360

An AI-powered Fusion 360 add-in that enables natural language 3D modeling. Create and modify 3D components using simple English commands powered by OpenAI's GPT models.

## 🚀 Features

### Core Capabilities
- **Natural Language Processing**: Describe what you want to create in plain English
- **Real-time AI Integration**: Powered by OpenAI GPT models for intelligent command interpretation
- **3D Modeling Actions**: Create boxes, cylinders, spheres, gears, holes, and more
- **Interactive Palette**: Modern glassmorphic UI integrated directly into Fusion 360
- **Mock Mode**: Test functionality without API keys using intelligent pattern matching

### Supported Commands
- **Basic Shapes**: "Create a 20mm cube", "Make a cylinder with radius 10mm and height 25mm"
- **Complex Geometry**: "Create a gear with 24 teeth and 6mm bore", "Make a sphere with radius 15mm"
- **Modifications**: "Create a hole with diameter 8mm and depth 15mm", "Extrude the selected face by 10mm"
- **Transformations**: "Move the selected body 15mm in the X direction"

## 📦 Installation Guide

### Prerequisites
- Autodesk Fusion 360 (latest version recommended)
- Windows or macOS
- OpenAI API key (optional - works in mock mode without it)

### Step 1: Download and Install
1. Download or clone this repository
2. Copy the entire `CadxStudio-AI-Copilot` folder to your Fusion 360 Add-ins directory:
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - **macOS**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`

### Step 2: Configure API Key (Optional)
1. Open `config.py` in the add-in folder
2. Set your OpenAI API key:
   ```python
   AI_API_KEY = "sk-your-openai-api-key-here"
   ```
3. Save the file

**Note**: The add-in works without an API key using intelligent mock responses for testing!

### Step 3: Enable the Add-in
1. Open Fusion 360
2. Go to **Tools** → **Add-ins**
3. Find "CadxStudio AI Copilot" in the list
4. Click **Run** (and optionally **Run on Startup** for automatic loading)

### Step 4: Launch the AI Copilot
1. Look for the **"CadxStudio AI Copilot"** button in the **Scripts and Add-ins** panel
2. Click it to open the AI interface palette
3. Start typing natural language commands!

## 🎯 Usage Examples

### Basic Shapes
```
Create a 30mm cube
Make a cylinder with radius 15mm and height 40mm
Create a sphere with radius 20mm
```

### Advanced Models
```
Create a gear with 24 teeth, module 2mm, and bore 6mm
Make a gear with 40 teeth and 8mm bore
Create a gear with 30 teeth, module 1.5mm, bore 8mm, and thickness 8mm
```

### Modifications (requires selection)
```
Create a hole with diameter 8mm and depth 15mm
Extrude the selected face by 10mm
Move the selected body 15mm in the X direction
```

## 🛠 Technical Architecture

### Components
- **Frontend**: Modern HTML/CSS/JavaScript palette with glassmorphic design
- **AI Service**: OpenAI GPT integration with intelligent fallback responses
- **Modeling Engine**: Direct Fusion 360 API integration for 3D operations
- **Communication Layer**: Seamless data flow between web interface and Python backend

### File Structure
```
CadxStudio-AI-Copilot/
├── config.py                 # Configuration and API settings
├── FusionGPT.py              # Main add-in entry point
├── commands/
│   └── paletteShow/          # AI Copilot palette command
├── lib/
│   ├── ai_service.py         # AI processing and OpenAI integration
│   ├── ai_modeling_actions.py # 3D modeling operations
│   └── fusionAddInUtils/     # Fusion 360 utilities
└── README.md
```

## 🔧 Development

### Adding New Commands
1. Update `SUPPORTED_AI_COMMANDS` in `config.py`
2. Add processing logic in `ai_service.py`
3. Implement the action in `ai_modeling_actions.py`
4. Test with both API and mock modes

### Customizing the UI
- Modify `commands/paletteShow/resources/html/index.html` for layout changes
- Update `commands/paletteShow/resources/html/static/palette.js` for functionality
- All styling is embedded CSS with glassmorphic design principles

### API Integration
- The system uses OpenAI's GPT models for natural language processing
- Fallback mock responses ensure functionality without API access
- Structured JSON responses enable reliable command parsing

## 🚨 Troubleshooting

### Common Issues
1. **Add-in not appearing**: Check that files are in the correct Add-ins directory
2. **Commands not working**: Ensure you have an active Fusion 360 design open
3. **API errors**: Verify your OpenAI API key is valid and has sufficient credits
4. **Selection required**: Some commands (holes, extrude, move) require selecting geometry first

### Debug Mode
- Set `DEBUG = True` in `config.py` for detailed logging
- Check the Fusion 360 Text Command window for error messages
- Use the browser developer tools for JavaScript debugging

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

For support, please open an issue on GitHub or contact the CadxStudio team.

---

**CadxStudio AI Copilot** - Bringing the future of AI-powered CAD to Fusion 360! 🚀