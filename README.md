# SlideForge
Transform your academic papers into customizable presentations effortlessly.

## Table of Contents
- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Why Now?](#why-now)
- [Solution](#solution)
- [Key Benefits](#key-benefits)
- [Competitive Landscape](#competitive-landscape)
- [How It Works](#how-it-works)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
SlideForge is an application designed by researchers for researchers. It enables professionals such as professors and graduate students in academia to convert their LaTeX-formatted papers into presentation slides with ease. Our goal is to help researchers build their community, save time, and enhance collaboration and reputation between academia and the public.

## Problem Statement
There is an extreme disconnect between the public and current areas of research since most people have to read complex papers to understand certain topics. PhD students and professors often have limited time to tailor their presentations for different groups or demographics, making it hard for others to understand. This creates a barrier between the public and academia that's hard to bridge, especially in the hard sciences.

## Why Now?
The world is moving at a much faster pace, and information is disseminating rapidly to younger audiences. There are now more expectations for researchers in this fast-moving world. The traditional "publish or perish" model hasn't addressed the need for researchers to craft their presentations for the public. There is a pressing need for better ways to engage with the field and make research more accessible.

## Solution
SlideForge provides a pipeline that takes LaTeX-formatted papers and translates them into LaTeX presentations that you can customize based on the audience, specialty, and focus areas. This optimizes presentations and expands the academic network, allowing engagement with people outside academia and enabling them to explore various ideas and topics.

## Key Benefits
- **Efficiency**: Save time by automating the conversion of papers to presentations.
- **Customization**: Tailor presentations to specific audiences and demographics.
- **Outreach**: Expand networks and grow outreach while focusing on publishing.
- **Accessibility**: Bridge the gap between academia and the public.

## Competitive Landscape
While there are tools that assist with presentation creation, few are tailored specifically for researchers needing to convert complex LaTeX documents into presentations. SlideForge stands out by focusing on high optimization for presentations and usability for researchers in academia.

_Note: A competitive landscape graph comparing SlideForge with other tools can be added here._

## How It Works
1. **Upload Your Files**: Provide your LaTeX source code and associated images.
2. **Processing**: SlideForge parses the LaTeX document, extracting sections, equations, and images.
3. **Conversion**: The backend uses OpenAI's API to optimize and convert content into presentation format.
4. **Customization**: Adjust the presentation based on your target audience.
5. **Generation**: Compile the presentation using pdflatex.
6. **Download**: Receive a downloadable PDF of your customized presentation.

## Features
- **Automatic Conversion**: Transform LaTeX papers into presentation slides seamlessly.
- **Image Handling**: Process images embedded in your LaTeX documents.
- **Customizable Output**: Generate presentations tailored to different audiences.
- **User-Friendly Interface**: Simple frontend application for easy interaction.
- **Backend Processing**: Robust backend server handling file uploads and processing.

## Tech Stack
- **Backend**:
  - Python 3.10
  - Flask
  - OpenAI API
- **Frontend**:
  - React.js
  - JavaScript
  - JSZip
- **Utilities**:
  - pdflatex for compiling LaTeX documents
  - openai Python library
- **Version Control**: Git and GitHub

## Architecture
The application consists of a frontend and a backend that communicate via RESTful APIs.

- **Frontend**: Built with React.js, allows users to upload files and initiate processing.
- **Backend**: Built with Flask, handles file uploads, interacts with the OpenAI API, and compiles LaTeX to PDF.

_An architecture diagram can be added here for visual representation._

## Getting Started

### Prerequisites

**Backend**:
- Python 3.10 or higher
- pip package manager
- Virtualenv
- pdflatex installed on your system
- OpenAI API key

**Frontend**:
- Node.js and npm

### Installation

#### Backend Setup
1. Clone the Repository:
   ```bash
   git clone https://github.com/Samuel-O-M/YHack-2024.git
   cd YHack-2024/backend
   ```
2. Create and Activate Virtual Environment:
    ```python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
    ```
3. Install Dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Install pdflatex:
    ```
    sudo apt-get install texlive-full  # On Ubuntu
    ```
#### Frontend Setup
1. Navigate to Frontend Directory:
    ```
    cd ../frontend
    ```
2. Install Dependencies:
    ```
    npm install
    ```

### Configuration
#### Backend Configuration
1. OpenAI API Key: Place your OpenAI API key in a file named openai_key in the backend directory.
    ```
    your-openai-api-key
    ```
2. Environment Variables: Set `FLASK_APP` to your main application file if necessary.

#### Frontend Configuration
Update API endpoints in `frontend/src/App.js` if the backend is not running on `localhost:5000`.

### Usage
#### Running the Backend Server
1. Activate Virtual Environment:
    ```
    cd backend
    source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
    ```
2. Run the Server:
    ```
    flask run
    ```
    The backend will start on `http://localhost:5000`.
#### Running the Frontend Application
1. Start the Frontend:
    ```
    cd frontend
    npm start
    ```
    The frontend will start on `http://localhost:3000`.

#### Using the Application
- Upload ZIP File: Click on "Select Zip File with Images" to upload your images.
- Upload LaTeX Code: Click on "Select LaTeX Code File (.txt)" to upload your LaTeX source code.
- Submit: Click on the "Submit" button to process your files.
- Download PDF: After processing, a PDF file will be downloaded automatically.

## API Endpoints
### POST /upload
Endpoint to receive images and a LaTeX text file.

**Parameters**:
- `images`: List of image files extracted from the uploaded ZIP.
- `textfile`: LaTeX code file (.txt format).

**Response**:
Returns the generated presentation PDF as a downloadable file.

**Example using curl**:
```bash
curl -X POST -F 'images=@images.zip' -F 'textfile=@latex_code.txt' http://localhost:5000/upload
```
## Testing

### Backend Testing
**Run Unit Tests**:
```bash
python -m unittest discover tests
```

Test LaTeX Compilation: Use the `/test_conversion` endpoint to test PDF generation with sample files.

### Frontend Testing
#### Run Tests:
```
npm test
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.