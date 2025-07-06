import os
import sys
import webbrowser

# Get the target directory from drag-and-drop or default to current directory
if len(sys.argv) > 1:
    target_dir = sys.argv[1]
else:
    target_dir = os.getcwd()

# Define the output HTML file in the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
html_file = os.path.join(script_dir, "html_gallery.html")

# Overwrite the existing file
with open(html_file, "w") as f:
    f.write("""
    <html><head><style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #121212;
            margin: 0;
            height: 100vh;
            overflow: hidden;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-content: flex-start;
            height: 100vh;
            overflow-y: hidden;
            width: 100%;
        }
        img {
            width: auto;
            height: calc(100vh / var(--rows));
            display: block;
            cursor: pointer;
        }
        .controls {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 10;
        }
        button {
            margin: 5px;
            padding: 10px;
            font-size: 16px;
            cursor: pointer;
        }
        .fullscreen-image {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.9);
            justify-content: center;
            align-items: center;
        }
        .fullscreen-image img {
            width: 100vw;
            height: 100vh;
            object-fit: contain;
        }
    </style></head>
    <body>
    <div class='controls'>
        <button onclick="adjustZoom(1)">-</button>
        <button onclick="adjustZoom(-1)">+</button>
    </div>
    <div class='container' id='imageContainer'>
    """)

    # Walk through the target directory and add images
    for root, _, files in os.walk(target_dir):
        for name in files:
            if name.lower().endswith((".jpg", ".png", ".webp", ".jpeg")):
                filepath = os.path.join(root, name).replace("\\", "/")
                f.write(f"<img src='{filepath}' class='image' onclick='showFullscreenImage(\"{filepath}\")'>\n")
    
    # Add full-screen view container
    f.write("""
    </div>
    <div class='fullscreen-image' id='fullscreenContainer' onclick='hideFullscreenImage()'>
        <img id='fullscreenImg'>
    </div>
    <script>
        let container = document.getElementById('imageContainer');
        let fullscreenContainer = document.getElementById('fullscreenContainer');
        let fullscreenImg = document.getElementById('fullscreenImg');
        let rowCount = 1;
        let maxRows = 5;
        document.documentElement.style.setProperty('--rows', rowCount);

        function getRowHeight() {
            let images = document.querySelectorAll('.image');
            if (images.length > 0) {
                return images[0].getBoundingClientRect().height;
            }
            return 0;
        }

        function scrollRows(direction) {
            let rowHeight = getRowHeight();
            let scrollAmount = rowHeight * rowCount;
            if (direction === 'down') {
                container.scrollTop += scrollAmount;
            } else if (direction === 'up') {
                container.scrollTop -= scrollAmount;
            }
        }

        document.addEventListener('keydown', function(event) {
            if (event.key === 'ArrowDown') {
                scrollRows('down');
            } else if (event.key === 'ArrowUp') {
                scrollRows('up');
            }
        });

        document.addEventListener('wheel', function(event) {
            event.preventDefault(); // Disable default scrolling behavior
            if (event.deltaY > 0) {
                scrollRows('down');
            } else {
                scrollRows('up');
            }
        }, { passive: false });

        function showFullscreenImage(src) {
            fullscreenImg.src = src;
            fullscreenContainer.style.display = 'flex';
        }

        function hideFullscreenImage() {
            fullscreenContainer.style.display = 'none';
        }

        function adjustZoom(change) {
            rowCount = Math.max(1, Math.min(maxRows, rowCount + change));
            document.documentElement.style.setProperty('--rows', rowCount);
        }

        function initializeZoom() {
            adjustZoom(0);
        }

        window.addEventListener("load", initializeZoom);
    </script>
    </body></html>
    """)

# Open the HTML file automatically
webbrowser.open(html_file)
