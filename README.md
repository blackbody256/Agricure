# Agricure: AI-Powered Plant Disease Diagnosis and Recommendation System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![Accuracy](https://img.shields.io/badge/AI_Accuracy-97%25-brightgreen.svg)](https://tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Agricure is a cutting-edge agricultural technology platform that revolutionizes crop health management through advanced AI-powered plant disease diagnosis. The system combines deep learning computer vision with intelligent recommendation algorithms to provide farmers, agronomists, and agricultural administrators with comprehensive crop monitoring and disease management solutions.

## 🚀 System Overview

Agricure leverages a sophisticated **EfficientNet-based** deep learning model trained on over **30,000+ crop images** to achieve **97% accuracy** in plant disease detection. The platform integrates multiple data sources including real-time weather conditions, soil analysis, and environmental factors to generate personalized, actionable agricultural recommendations powered by Google's **Gemini AI**.

## 🌟 Key Features

### 🤖 Advanced AI Diagnosis Engine
-   **EfficientNet-based Deep Learning Model** - Pre-trained CNN achieving **97% accuracy** across multiple crop types
-   **Real-time Image Processing** - Upload or capture plant images with **~2.5 second** analysis time
-   **Multi-crop Support** - Comprehensive disease detection for:
    -   🌽 **Corn/Maize** (Common Rust, Northern Leaf Blight, Gray Leaf Spot)
    -   🍎 **Apple** (Apple Scab, Black Rot, Cedar Apple Rust)
    -   🍅 **Tomato** (Early/Late Blight, Bacterial Spot, Leaf Mold, Mosaic Virus)
    -   🥔 **Potato** (Early Blight, Late Blight)
    -   🌶️ **Pepper** (Bacterial Spot)
-   **Camera Integration** - Mobile-optimized field capture with live preview
-   **Confidence Scoring** - Transparent AI predictions with confidence percentages

### 🎯 Smart Recommendation System
-   **Gemini AI Integration** - Dynamic treatment recommendations based on diagnosis context
-   **Environmental Intelligence** - Weather-informed advice using OpenWeatherMap API
-   **Soil Analysis Integration** - ISDA soil data incorporation for comprehensive recommendations
-   **Treatment Protocols** - Step-by-step actionable guidance for disease management
-   **Prevention Strategies** - Proactive measures to prevent disease recurrence

### 👥 Multi-Role Platform Architecture
-   **🧑‍🌾 Farmer Dashboard:**
    -   Personal diagnosis history and crop health analytics
    -   Interactive charts showing disease patterns and trends
    -   Urgent alert system for critical crop conditions
    -   Recommendation tracking and feedback system
-   **🔬 Agronomist Portal:**
    -   Farmer data overview and monitoring capabilities
    -   Dataset upload and management tools
    -   Comprehensive reporting with email distribution
    -   Advanced analytics dashboard
-   **⚙️ Administrator Console:**
    -   System-wide analytics and user management
    -   Dataset administration and model management
    -   User role assignment and access control
    -   Platform monitoring and maintenance tools

### 📊 Advanced Analytics & Reporting
-   **Interactive Visualizations** - Plotly-powered charts and graphs
-   **Trend Analysis** - Monthly diagnosis patterns and disease prevalence
-   **Performance Metrics** - Model accuracy tracking and system statistics
-   **Export Capabilities** - CSV export for external analysis
-   **Email Reports** - Automated report generation and distribution

### 💬 Communication Features
-   **Real-time Chat System** - Direct farmer-agronomist communication
-   **File Sharing** - Document and image exchange capabilities
-   **Notification System** - Alert mechanisms for critical events
-   **Feedback Loop** - User feedback collection for continuous improvement

## 🛠️ Technology Stack

### Backend & Core Infrastructure
-   **Framework:** Django 5.2 with Python 3.9+
-   **Database:** PostgreSQL with advanced querying capabilities
-   **Authentication:** Multi-role user system with role-based access control
-   **File Storage:** Django media handling with organized upload directories

### AI & Machine Learning
-   **Deep Learning Framework:** TensorFlow 2.x & Keras
-   **Model Architecture:** EfficientNet-based transfer learning
-   **Image Processing:** PIL/Pillow with optimized preprocessing pipelines
-   **Training Dataset:** 30,000+ annotated crop disease images
-   **Model Performance:** 97% accuracy with ~2.5s inference time

### APIs & External Services
-   **AI Recommendations:** Google Gemini API for intelligent content generation
-   **Weather Data:** OpenWeatherMap API for real-time environmental conditions
-   **Soil Analysis:** ISDA (International Soil Data Archive) integration
-   **Email Services:** Django email backend for notifications and reporting

### Frontend & User Experience
-   **Styling:** Bootstrap 5 with custom CSS animations
-   **JavaScript:** Vanilla JS with modern ES6+ features
-   **Charts & Visualization:** Plotly.js for interactive data visualization
-   **Responsive Design:** Mobile-first approach optimized for field use
-   **Camera Integration:** WebRTC for real-time image capture

### Data Analytics & Processing
-   **Data Analysis:** Pandas for advanced data manipulation
-   **Visualization:** Matplotlib integration for statistical analysis
-   **Export Formats:** CSV export capabilities for external analysis
-   **Real-time Processing:** Asynchronous task handling for AI operations

### DevOps & Deployment
-   **Environment Management:** Python-dotenv for configuration
-   **Static Files:** Django static file management
-   **Media Handling:** Organized file upload system
-   **Security:** CSRF protection, secure authentication, and data validation

## 🚀 Getting Started

Follow these instructions to get a copy of Agricure up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed on your system:
-   **Python 3.9+** (recommended: Python 3.11)
-   **PostgreSQL** (12.0 or higher)
-   **Git** for version control
-   **Virtual Environment** tools (venv or conda)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/blackbody256/Agricure.git
    cd Agricure/Agricure
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Using venv
    python -m venv agricure_env
    source agricure_env/bin/activate  # On Windows: agricure_env\Scripts\activate
    
    # Or using conda
    conda create -n agricure python=3.11
    conda activate agricure
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
    **Required packages include:**
    - `django` - Web framework
    - `tensorflow` - AI model inference
    - `numpy` & `pandas` - Data processing
    - `matplotlib` - Data visualization
    - `python-dotenv` - Environment management
    - `requests` - API communications
    - `Pillow` - Image processing

4.  **Set up environment variables:**
    
    Copy the example environment file and configure your settings:
    ```bash
    cp .env.example .env
    ```
    
    Edit the `.env` file with your configuration:
    ```env
    # Django Configuration
    SECRET_KEY='your-django-secret-key-here'
    DEBUG=True
    
    # Database Configuration (PostgreSQL)
    DB_ENGINE='django.db.backends.postgresql'
    DB_NAME='agricure_db'
    DB_USER='your_postgres_user'
    DB_PASSWORD='your_postgres_password'
    DB_HOST='localhost'
    DB_PORT='5432'
    
    # API Keys
    GEMINI_API_KEY='your-gemini-api-key'
    OPENWEATHER_API_KEY='your-openweathermap-api-key'
    
    # Email Configuration (Optional)
    EMAIL_HOST_USER='your-email@gmail.com'
    EMAIL_HOST_PASSWORD='your-gmail-app-password'
    ```

5.  **Set up the database:**
    ```bash
    # Create PostgreSQL database
    createdb agricure_db
    
    # Apply Django migrations
    python manage.py migrate
    ```

6.  **Create a superuser account:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Load the AI model:**
    
    Ensure the pre-trained model `newresult.h5` is present in the `diagnosis/model/` directory. The model file should be approximately 85MB.

8.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    
    The application will be available at `http://127.0.0.1:8000`

### Quick Start Guide

1. **Access the platform** at `http://127.0.0.1:8000`
2. **Sign up** as a farmer or login with your superuser account
3. **Upload a crop image** via the diagnosis interface
4. **View AI analysis results** with disease detection and confidence scores
5. **Get recommendations** based on your diagnosis and local conditions
6. **Explore dashboards** to track your crop health analytics

### Model Information

The system uses a custom **EfficientNet-based model** (`newresult.h5`) trained specifically for agricultural disease detection:
- **Input Size:** 224x224x3 RGB images
- **Output:** 21-class disease classification
- **Preprocessing:** EfficientNet-specific normalization
- **Accuracy:** 97% on validation dataset

## 📂 Project Architecture

Agricure follows a modular Django application structure designed for scalability and maintainability:

### Core Applications

#### `/users` - User Management & Authentication
-   **Custom User Model** with role-based permissions (Farmer, Agronomist, Admin)
-   **Multi-role Authentication** system with specialized dashboards
-   **Profile Management** with user-specific preferences and settings
-   **User Analytics** and activity tracking

#### `/diagnosis` - AI Disease Detection Engine
-   **Image Upload & Processing** with support for multiple formats
-   **Camera Integration** for real-time field capture
-   **EfficientNet Model Interface** for disease classification
-   **Diagnosis History** and result tracking
-   **Confidence Scoring** and prediction analysis

#### `/recommendations` - Intelligent Advisory System
-   **Gemini AI Integration** for generating contextual recommendations
-   **Weather API Client** for real-time environmental data
-   **Soil Analysis Module** using ISDA soil databases
-   **Treatment Protocol Generation** based on multiple data sources
-   **Feedback Collection** for recommendation effectiveness

#### `/analytics` - Data Visualization & Insights
-   **Plotly Integration** for interactive charts and graphs
-   **Statistical Analysis** of diagnosis patterns and trends
-   **Performance Metrics** tracking for AI model accuracy
-   **Export Functions** for data analysis and reporting

#### `/agronomist` - Professional Tools Suite
-   **Dataset Management** for training data uploads
-   **Report Generation** with automated email distribution
-   **Farmer Monitoring** tools and overview dashboards
-   **Data Export** capabilities for research and analysis

#### `/chat` - Communication Platform
-   **Real-time Messaging** between farmers and agronomists
-   **File Attachment** support for sharing images and documents
-   **Notification System** for important updates and alerts

#### `/administrator` - System Administration
-   **Dataset Upload** and management for model training
-   **User Management** with role assignment capabilities
-   **System Analytics** and performance monitoring
-   **Configuration Management** for platform settings

### Key System Files

```
Agricure/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── diagnosis/model/
│   ├── newresult.h5         # Pre-trained EfficientNet model (97% accuracy)
│   └── test.py              # Model testing and validation script
├── media/                   # User uploaded files
│   ├── diagnosis_images/    # Crop disease images
│   ├── datasets/           # Training datasets
│   └── chat_attachments/   # Communication files
└── static/                 # CSS, JavaScript, and static assets
```

### Database Schema Highlights

-   **User Model** - Extended Django user with agricultural roles
-   **Diagnosis Model** - Image analysis results with metadata
-   **Recommendation Model** - AI-generated advice with environmental context
-   **Feedback Model** - User feedback for continuous improvement
-   **AgronomistUpload Model** - Professional dataset management

### API Integration Points

-   **Google Gemini API** - Advanced natural language generation for recommendations
-   **OpenWeatherMap API** - Real-time weather data for contextual advice
-   **ISDA Soil Database** - Comprehensive soil analysis data integration

## 🎯 System Capabilities

### Disease Detection Accuracy
- **Overall Accuracy:** 97% across all supported crops
- **Processing Speed:** ~2.5 seconds per image analysis
- **Model Version:** v2.1 (July 2025) with enhanced training dataset
- **Supported Diseases:** 21 different disease classifications

### Supported Crop Types & Diseases

| Crop | Diseases Detected | Health Status |
|------|------------------|---------------|
| 🌽 **Corn/Maize** | Common Rust, Northern Leaf Blight, Gray Leaf Spot | ✅ Healthy detection |
| 🍎 **Apple** | Apple Scab, Black Rot, Cedar Apple Rust | ✅ Healthy detection |
| 🍅 **Tomato** | Early Blight, Late Blight, Bacterial Spot, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus | ✅ Healthy detection |
| 🥔 **Potato** | Early Blight, Late Blight | ✅ Healthy detection |
| 🌶️ **Bell Pepper** | Bacterial Spot | ✅ Healthy detection |

### Platform Statistics
- **Training Dataset:** 30,000+ annotated crop images
- **Active Users:** Farmers, Agronomists, and Administrators
- **Response Time:** Real-time analysis with immediate results
- **Mobile Optimization:** Fully responsive design for field use

## 📱 Usage Examples

### For Farmers
1. **Capture/Upload** a crop image using your mobile device
2. **Receive instant AI diagnosis** with disease identification and confidence score
3. **Get personalized recommendations** based on your location's weather and soil conditions
4. **Track your crop health** over time with analytics dashboards
5. **Communicate directly** with agronomists for expert consultation

### For Agronomists
1. **Monitor farmer activities** and diagnosis patterns across your region
2. **Upload research datasets** to contribute to model improvements
3. **Generate comprehensive reports** with automated email distribution
4. **Analyze trends** in crop diseases and treatment effectiveness
5. **Provide expert guidance** through the integrated chat system

### For Administrators
1. **Manage system users** and assign appropriate roles
2. **Monitor platform performance** and AI model accuracy
3. **Oversee dataset management** for continuous model improvement
4. **Access system-wide analytics** for strategic decision making

## 🤝 Contributors
| Name | Registration Number | Student Number |
|------|-------------------|----------------|
| KARAGWA ANN TREASURE | 23/U/09034/PS | 2300709034 |
| AYAN MUSTAFA ABDIRAHMAN | 23/X/22948/EVE | 2300722948 |
| WANYANA SELINA MASEMBE | 23/U/1529 | 2300701529 |
| AMABE JUNIOR HUMPHREY | 23/U/05942/PS | 2300705942 |
| AKANGA ANDREW | 23/U/05555/PS | 2300705555 |


### Core Development Team

-   **sseluyindaeva** - Lead Developer & AI Specialist
    - Core system architecture and Django backend development
    - AI model integration and optimization
    - Database design and API development

-   **ayanhilwa** - Full-Stack Developer & UI/UX Specialist
    - Frontend development and responsive design
    - User interface optimization and user experience enhancement
    - Mobile optimization and cross-platform compatibility

### Project Recognition

Based on the comprehensive system analysis and the detailed project report, Agricure represents a significant advancement in agricultural technology, combining state-of-the-art AI with practical farming solutions.

### Contributing

We welcome contributions to enhance Agricure's capabilities! Here's how you can help:

1. **🐛 Bug Reports** - Report issues or unexpected behavior
2. **✨ Feature Requests** - Suggest new features or improvements
3. **📝 Documentation** - Help improve documentation and guides
4. **🧪 Testing** - Contribute to testing and quality assurance
5. **🔬 Research** - Share agricultural datasets or research insights

**Getting Started with Contributions:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Research Collaborations

Agricure is open to collaborations with:
- Agricultural research institutions
- Universities with agricultural or AI programs
- Farming cooperatives and agricultural organizations
- Technology companies focused on agricultural solutions

## 🔮 Future Roadmap

### Planned Enhancements
- **🌍 Multi-language Support** - Localization for global agricultural communities
- **🚜 IoT Integration** - Connection with farm sensors and equipment
- **📡 Satellite Imagery** - Integration with remote sensing data
- **🧬 Advanced Genomics** - Incorporation of plant genetic data
- **🌱 Precision Agriculture** - Enhanced precision farming recommendations

### Research Initiatives
- **Deep Learning Improvements** - Continuous model enhancement with new datasets
- **Climate Adaptation** - AI-driven climate change adaptation strategies
- **Sustainable Farming** - Environmentally conscious agricultural practices
- **Predictive Analytics** - Early warning systems for disease outbreaks

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**MIT License Summary:**
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❗ License and copyright notice required

## 📞 Support & Contact

### Technical Support
- **Email:** [support@agricure.com](mailto:sseluyindaeva@gmail.com)
- **Documentation:** [Wiki Documentation](https://github.com/blackbody256/Agricure/wiki)
- **Issues:** [GitHub Issues](https://github.com/blackbody256/Agricure/issues)

### Agricultural Expertise
For agricultural consulting and expert guidance, connect with our certified agronomists through the platform's chat system.

### Research Inquiries
For research collaborations and academic partnerships, please reach out through our institutional contact channels.

---

**🌱 Agricure - Cultivating the Future of Agriculture with AI** 

*Empowering farmers worldwide with intelligent crop health solutions*