from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Flowable

OUTPUT_PATH = "output/Image_Labels_Generator_Guide.pdf"

# ── Custom flowable: full-width colored banner ────────────────────────────────
class ColorBanner(Flowable):
    def __init__(self, text, bg, fg=colors.white, height=1.1*cm, font_size=13):
        super().__init__()
        self.text = text
        self.bg = bg
        self.fg = fg
        self.height = height
        self.font_size = font_size
        self.width = 0

    def wrap(self, available_width, available_height):
        self.width = available_width
        return available_width, self.height

    def draw(self):
        self.canv.setFillColor(self.bg)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        self.canv.setFillColor(self.fg)
        self.canv.setFont("Helvetica-Bold", self.font_size)
        self.canv.drawString(0.4*cm, 0.28*cm, self.text)


# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle("title",
            fontName="Helvetica-Bold", fontSize=28, textColor=colors.HexColor("#1a1a2e"),
            alignment=TA_CENTER, spaceAfter=6),

        "subtitle": ParagraphStyle("subtitle",
            fontName="Helvetica", fontSize=13, textColor=colors.HexColor("#4a4a6a"),
            alignment=TA_CENTER, spaceAfter=4),

        "tag": ParagraphStyle("tag",
            fontName="Helvetica-Bold", fontSize=10, textColor=colors.white,
            alignment=TA_CENTER),

        "h1": ParagraphStyle("h1",
            fontName="Helvetica-Bold", fontSize=16, textColor=colors.HexColor("#1a1a2e"),
            spaceBefore=18, spaceAfter=6),

        "h2": ParagraphStyle("h2",
            fontName="Helvetica-Bold", fontSize=12, textColor=colors.HexColor("#16213e"),
            spaceBefore=12, spaceAfter=4),

        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=10, textColor=colors.HexColor("#2d2d2d"),
            leading=15, spaceAfter=6, alignment=TA_JUSTIFY),

        "bullet": ParagraphStyle("bullet",
            fontName="Helvetica", fontSize=10, textColor=colors.HexColor("#2d2d2d"),
            leading=15, leftIndent=14, spaceAfter=3,
            bulletIndent=4, bulletText="•"),

        "code": ParagraphStyle("code",
            fontName="Courier", fontSize=9, textColor=colors.HexColor("#1e1e1e"),
            leading=13, spaceAfter=2, leftIndent=8),

        "note": ParagraphStyle("note",
            fontName="Helvetica-Oblique", fontSize=9.5,
            textColor=colors.HexColor("#555555"), leading=14, spaceAfter=4),

        "footer": ParagraphStyle("footer",
            fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#888888"),
            alignment=TA_CENTER),
    }
    return styles


# ── Helpers ───────────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#16213e")
ACCENT_BLUE = colors.HexColor("#0f3460")
LIGHT_GRAY  = colors.HexColor("#f0f2f5")
CODE_BG     = colors.HexColor("#1e1e1e")
CODE_FG     = colors.HexColor("#d4d4d4")
GREEN       = colors.HexColor("#2ecc71")
ORANGE      = colors.HexColor("#e67e22")

def hr(story):
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor("#cccccc"), spaceAfter=6))

def code_block(story, lines, s):
    data = [[Paragraph(line.replace(" ", "&nbsp;"), s["code"])] for line in lines]
    t = Table(data, colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_GRAY),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#cccccc")),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

def info_box(story, text, s, bg=colors.HexColor("#e8f4fd"), border=colors.HexColor("#3498db")):
    data = [[Paragraph(text, s["body"])]]
    t = Table(data, colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), bg),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("LINEBEFORE",   (0,0), (0,-1), 3, border),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))


# ── Document builder ──────────────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm,  bottomMargin=2*cm,
        title="Image Labels Generator — Complete Guide",
        author="Image Labels Generator Project"
    )
    s = make_styles()
    story = []
    W = A4[0] - 4*cm   # usable width

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.5*cm))

    cover_banner_data = [[Paragraph("IMAGE LABELS GENERATOR", s["tag"])]]
    cb = Table(cover_banner_data, colWidths=[W])
    cb.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), DARK_BLUE),
        ("TOPPADDING",   (0,0), (-1,-1), 18),
        ("BOTTOMPADDING",(0,0), (-1,-1), 18),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(cb)
    story.append(Spacer(1, 0.8*cm))

    story.append(Paragraph("Complete Project Guide", s["title"]))
    story.append(Paragraph("Build a computer vision app using AWS S3 &amp; Amazon Rekognition", s["subtitle"]))
    story.append(Spacer(1, 0.6*cm))

    tags_data = [[
        Paragraph("Amazon S3", s["tag"]),
        Paragraph("Amazon Rekognition", s["tag"]),
        Paragraph("Python 3", s["tag"]),
        Paragraph("AWS Free Tier", s["tag"]),
    ]]
    tags_t = Table(tags_data, colWidths=[W/4]*4, hAlign="CENTER")
    tags_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,0), ACCENT_BLUE),
        ("BACKGROUND",   (1,0), (1,0), colors.HexColor("#c0392b")),
        ("BACKGROUND",   (2,0), (2,0), colors.HexColor("#27ae60")),
        ("BACKGROUND",   (3,0), (3,0), colors.HexColor("#8e44ad")),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("ROUNDEDCORNERS", [4]),
        ("LEFTPADDING",  (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(tags_t)
    story.append(Spacer(1, 1.2*cm))
    hr(story)

    summary_data = [[
        Table([[Paragraph("<b>~20 min</b>", s["body"])],
               [Paragraph("Build Time", s["note"])]], colWidths=[W/3]),
        Table([[Paragraph("<b>$0.00</b>", s["body"])],
               [Paragraph("Cost (Free Tier)", s["note"])]], colWidths=[W/3]),
        Table([[Paragraph("<b>Beginner</b>", s["body"])],
               [Paragraph("Difficulty Level", s["note"])]], colWidths=[W/3]),
    ]]
    st = Table(summary_data, colWidths=[W/3]*3)
    st.setStyle(TableStyle([
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
    ]))
    story.append(st)
    hr(story)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("What this project does", s["h1"]))
    story.append(Paragraph(
        "This project automatically analyzes any image using AWS artificial intelligence. "
        "You give it a photo and it tells you every object in the photo — such as 'Dog', 'Car', "
        "'Person', 'Tree' — along with how confident it is. It then draws colored bounding boxes "
        "around each detected object and saves an annotated version of your image.",
        s["body"]))
    story.append(Spacer(1, 0.3*cm))

    flow_data = [
        [Paragraph("1. Your Image", s["tag"]),
         Paragraph("→", s["body"]),
         Paragraph("2. Upload to S3", s["tag"]),
         Paragraph("→", s["body"]),
         Paragraph("3. Rekognition AI", s["tag"]),
         Paragraph("→", s["body"]),
         Paragraph("4. Labeled Output", s["tag"])],
    ]
    ft = Table(flow_data, colWidths=[2.5*cm, 0.5*cm, 2.5*cm, 0.5*cm, 2.5*cm, 0.5*cm, 2.5*cm])
    ft.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,0), colors.HexColor("#3498db")),
        ("BACKGROUND",   (2,0), (2,0), colors.HexColor("#e67e22")),
        ("BACKGROUND",   (4,0), (4,0), colors.HexColor("#c0392b")),
        ("BACKGROUND",   (6,0), (6,0), colors.HexColor("#27ae60")),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(ft)
    story.append(PageBreak())

    # ── PAGE 2: PREREQUISITES ─────────────────────────────────────────────────
    story.append(ColorBanner("SECTION 1 — PREREQUISITES & AWS SETUP", DARK_BLUE))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("What you need before you start", s["h1"]))
    prereqs = [
        ("A computer running Windows 10 or 11",
         "This guide is written for Windows. All commands are for PowerShell."),
        ("An internet connection",
         "Required to use AWS cloud services and download software."),
        ("An AWS Account (free to create)",
         "Amazon Web Services provides the AI and storage. No charge for this project."),
        ("About 20 minutes",
         "The full setup from scratch takes roughly 20 minutes."),
    ]
    for title, desc in prereqs:
        row = [[
            Paragraph(f"<b>{title}</b>", s["body"]),
            Paragraph(desc, s["note"]),
        ]]
        t = Table(row, colWidths=[7*cm, W - 7*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), LIGHT_GRAY),
            ("TOPPADDING",   (0,0), (-1,-1), 6),
            ("BOTTOMPADDING",(0,0), (-1,-1), 6),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("BOX",          (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ]))
        story.append(t)
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 0.4*cm))

    # AWS Services
    story.append(Paragraph("AWS Services Used", s["h1"]))
    services = [
        ("Amazon S3", "Simple Storage Service",
         "A cloud storage bucket. Your images are uploaded here before analysis.",
         colors.HexColor("#e67e22")),
        ("Amazon Rekognition", "Image Analysis AI",
         "AWS's deep learning service. It reads your image and returns a list of detected objects with confidence scores and coordinates.",
         colors.HexColor("#c0392b")),
        ("AWS IAM", "Identity & Access Management",
         "Controls who can access AWS services. You create a user here and get security keys for your Python script.",
         colors.HexColor("#8e44ad")),
        ("AWS CLI", "Command Line Interface",
         "A tool you install on your computer. Lets you connect your local machine to your AWS account using your security keys.",
         colors.HexColor("#27ae60")),
    ]
    for name, full_name, desc, color in services:
        row = [[
            Paragraph(f"<b>{name}</b><br/><font size=8>{full_name}</font>", s["body"]),
            Paragraph(desc, s["note"]),
        ]]
        t = Table(row, colWidths=[4*cm, W - 4*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), LIGHT_GRAY),
            ("TOPPADDING",   (0,0), (-1,-1), 7),
            ("BOTTOMPADDING",(0,0), (-1,-1), 7),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("LINEBEFORE",   (0,0), (0,-1), 4, color),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ── PAGE 3: FULL SETUP STEPS ──────────────────────────────────────────────
    story.append(ColorBanner("SECTION 2 — COMPLETE SETUP (STEP BY STEP)", DARK_BLUE))
    story.append(Spacer(1, 0.4*cm))

    # Step 1
    story.append(ColorBanner("STEP 1 — Create an AWS Account", ACCENT_BLUE, height=0.8*cm, font_size=11))
    story.append(Spacer(1, 0.2*cm))
    steps_1 = [
        "Go to https://aws.amazon.com and click Create an AWS Account.",
        "Enter your email address, a password, and an account name (anything you like).",
        "Enter your credit card when asked. You will NOT be charged — this project is 100% within the Free Tier.",
        "Choose Basic support — Free when asked.",
        "Sign in to the AWS Console at https://console.aws.amazon.com.",
    ]
    for i, step in enumerate(steps_1, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {step}", s["bullet"]))
    story.append(Spacer(1, 0.3*cm))

    # Step 2
    story.append(ColorBanner("STEP 2 — Create an S3 Bucket (Image Storage)", ACCENT_BLUE, height=0.8*cm, font_size=11))
    story.append(Spacer(1, 0.2*cm))
    steps_2 = [
        "In the AWS Console search bar at the top, type S3 and click on S3.",
        "Click the orange Create bucket button.",
        "Bucket name: image-labels-yourname  (replace 'yourname' with your actual name, no spaces).",
        "AWS Region: US East (N. Virginia)  us-east-1.",
        "Scroll down, leave everything else as default, click Create bucket.",
    ]
    for i, step in enumerate(steps_2, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {step}", s["bullet"]))
    info_box(story, "<b>Important:</b>  Bucket names must be globally unique across all AWS users. If your name is taken, add numbers — e.g. image-labels-amirtha-2024.", s,
             bg=colors.HexColor("#fff8e1"), border=ORANGE)

    # Step 3
    story.append(ColorBanner("STEP 3 — Create an IAM User (Security Keys)", ACCENT_BLUE, height=0.8*cm, font_size=11))
    story.append(Spacer(1, 0.2*cm))
    steps_3 = [
        "In the search bar, type IAM and click IAM.",
        "On the left menu, click Users, then click Create user.",
        "Username: rekognition-user  — click Next.",
        "Select Attach policies directly.",
        "Search for AmazonS3FullAccess — tick the checkbox.",
        "Search for AmazonRekognitionFullAccess — tick the checkbox.",
        "Click Next → Create user.",
        "Click on the user rekognition-user you just created.",
        "Click the Security credentials tab → scroll to Access keys → click Create access key.",
        "Select Command Line Interface (CLI) → tick the confirmation box → Next → Create access key.",
        "Click Download .csv file.  SAVE THIS FILE. You cannot view the secret key again.",
    ]
    for i, step in enumerate(steps_3, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {step}", s["bullet"]))
    info_box(story, "<b>Warning:</b>  The downloaded CSV file contains your Access Key ID and Secret Access Key. Keep this file safe and never share it publicly or upload it to GitHub.", s,
             bg=colors.HexColor("#fdecea"), border=colors.HexColor("#e74c3c"))

    story.append(PageBreak())

    # ── PAGE 4: LOCAL SETUP ───────────────────────────────────────────────────
    story.append(ColorBanner("SECTION 2 (CONTINUED) — LOCAL ENVIRONMENT SETUP", DARK_BLUE))
    story.append(Spacer(1, 0.4*cm))

    # Step 4
    story.append(ColorBanner("STEP 4 — Install Python", ACCENT_BLUE, height=0.8*cm, font_size=11))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("<b>1.</b>  Go to https://www.python.org/downloads and click the big yellow Download button.", s["bullet"]))
    story.append(Paragraph("<b>2.</b>  Run the installer. On the very first screen, tick the box that says:", s["bullet"]))
    info_box(story, "&#9745;  Add Python to PATH", s, bg=colors.HexColor("#e8f5e9"), border=GREEN)
    story.append(Paragraph("<b>3.</b>  Click Install Now and wait for it to finish.", s["bullet"]))
    story.append(Paragraph("<b>4.</b>  Open PowerShell (press Windows key, type powershell, press Enter) and verify:", s["bullet"]))
    code_block(story, ["python --version", "# Should show: Python 3.12.x  (or similar)"], s)

    # Step 5
    story.append(ColorBanner("STEP 5 — Install AWS CLI", ACCENT_BLUE, height=0.8*cm, font_size=11))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("<b>1.</b>  In PowerShell, run:", s["bullet"]))
    code_block(story, ["winget install Amazon.AWSCLI"], s)
    story.append(Paragraph("<b>2.</b>  Close PowerShell and open a new window, then verify:", s["bullet"]))
    code_block(story, ["aws --version", "# Should show: aws-cli/2.x.x"], s)

    # Step 6
    story.append(ColorBanner("STEP 6 — Connect AWS CLI to Your Account", ACCENT_BLUE, height=0.8*cm, font_size=11))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("<b>1.</b>  Open the CSV file you downloaded in Step 3. It has two values: Access key ID and Secret access key.", s["bullet"]))
    story.append(Paragraph("<b>2.</b>  In PowerShell, type:", s["bullet"]))
    code_block(story, ["aws configure"], s)
    story.append(Paragraph("<b>3.</b>  Answer each question:", s["bullet"]))
    code_block(story, [
        "AWS Access Key ID:      [paste your Access key ID]",
        "AWS Secret Access Key:  [paste your Secret access key]",
        "Default region name:    us-east-1",
        "Default output format:  json",
    ], s)
    story.append(Paragraph("<b>4.</b>  Verify the connection worked:", s["bullet"]))
    code_block(story, [
        "aws s3 ls",
        "# Should show your bucket name, e.g.:  image-labels-amirtha",
    ], s)

    # Step 7
    story.append(ColorBanner("STEP 7 — Set Up the Project Folder", ACCENT_BLUE, height=0.8*cm, font_size=11))
    story.append(Spacer(1, 0.2*cm))
    steps_7 = [
        ('Navigate to the project folder:', ["cd \"C:\\Image Labels Generator\""]),
        ('Create the input and output folders:', ["mkdir images", "mkdir output"]),
        ('Create a virtual environment (isolated Python workspace):', ["python -m venv venv"]),
        ('Activate the virtual environment:', [".\\venv\\Scripts\\Activate.ps1",
                                                "# You will see (venv) at the start of the prompt"]),
        ('Install required Python libraries:', ["pip install boto3 matplotlib pillow"]),
    ]
    for i, (desc, cmds) in enumerate(steps_7, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {desc}", s["bullet"]))
        code_block(story, cmds, s)

    story.append(PageBreak())

    # ── PAGE 5: PROJECT STRUCTURE & RUNNING ───────────────────────────────────
    story.append(ColorBanner("SECTION 3 — PROJECT STRUCTURE & HOW TO RUN", DARK_BLUE))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Project Folder Structure", s["h1"]))
    code_block(story, [
        "C:\\Image Labels Generator\\",
        "   images\\              ← Put your input images here",
        "   |   sample.jpg",
        "   output\\             ← Annotated images are saved here automatically",
        "   detect_labels.py    ← The main script that does everything",
        "   requirements.txt    ← List of Python libraries needed",
        "   generate_pdf.py     ← Script that generated this document",
        "   venv\\              ← Python virtual environment (auto-created)",
    ], s)

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Step 8 — Add Your Test Image", s["h1"]))
    story.append(Paragraph(
        "Copy any .jpg image from your computer into the images\\ folder. "
        "For example, a photo of your pet, a street scene, or any object. "
        "Rename it sample.jpg for the first test.",
        s["body"]))
    info_box(story, "<b>Tip:</b>  Images with clear, distinct objects work best (e.g. a single dog, a car, a person). Rekognition can detect up to 10 objects per call in our setup.", s)

    story.append(Paragraph("Step 9 — Open in VS Code", s["h1"]))
    story.append(Paragraph("In PowerShell (with venv active), open the project in Visual Studio Code:", s["body"]))
    code_block(story, ["code ."], s)
    story.append(Paragraph("If VS Code is not installed, download it free from https://code.visualstudio.com", s["note"]))

    story.append(Paragraph("Step 10 — Update Your Bucket Name in the Script", s["h1"]))
    story.append(Paragraph("Open detect_labels.py in VS Code. Find line 10:", s["body"]))
    code_block(story, [
        "BUCKET_NAME = \"YOUR-BUCKET-NAME-HERE\"",
        "",
        "# Change it to your actual bucket name, for example:",
        "BUCKET_NAME = \"image-labels-amirtha\"",
    ], s)
    story.append(Paragraph("Save the file with Ctrl + S.", s["body"]))

    story.append(Paragraph("Step 11 — Run the Script", s["h1"]))
    story.append(Paragraph("In PowerShell, make sure you see (venv) at the start of the line. Then run:", s["body"]))
    code_block(story, [
        "python detect_labels.py images/sample.jpg",
    ], s)

    story.append(Paragraph("Expected Terminal Output", s["h2"]))
    code_block(story, [
        "Uploading sample.jpg to S3...",
        "Upload complete.",
        "Analyzing image with Rekognition...",
        "",
        "Detected 7 labels:",
        "  - Dog (100.0%)",
        "  - Animal (100.0%)",
        "  - Mammal (100.0%)",
        "  - Pet (100.0%)",
        "  - Puppy (100.0%)",
        "  - Hound (80.8%)",
        "  Scene label: Animal (100.0%)",
        "Output saved to: output\\labeled_sample.jpg",
    ], s)

    story.append(Paragraph("Open the result:", s["h2"]))
    code_block(story, ["start output\\labeled_sample.jpg"], s)
    story.append(Paragraph(
        "Your image will open with colored bounding boxes drawn around every detected object, "
        "each labeled with its name and confidence percentage.",
        s["body"]))

    story.append(PageBreak())

    # ── PAGE 6: HOW IT WORKS + CODE EXPLAINED ────────────────────────────────
    story.append(ColorBanner("SECTION 4 — HOW THE CODE WORKS", DARK_BLUE))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("The Three Main Steps Inside detect_labels.py", s["h1"]))

    steps_code = [
        ("Step 1: Upload Image to S3",
         "The script uploads your local image file to your S3 bucket in the cloud. "
         "This gives Rekognition a place to read the image from.",
         ["s3_client.upload_file(local_path, BUCKET_NAME, filename)"]),
        ("Step 2: Call Rekognition API",
         "The script sends your image bytes directly to Amazon Rekognition. "
         "Rekognition uses deep learning to analyze the image and returns a list of detected labels.",
         [
             "with open(local_path, \"rb\") as f:",
             "    image_bytes = f.read()",
             "response = rekognition_client.detect_labels(",
             "    Image={\"Bytes\": image_bytes},",
             "    MaxLabels=10,",
             "    MinConfidence=75",
             ")",
         ]),
        ("Step 3: Draw Bounding Boxes",
         "For each detected label, if Rekognition provides coordinate data, the script uses "
         "matplotlib to draw a colored rectangle around the object on the image. "
         "Labels without coordinates (scene-level) are printed in the terminal only.",
         [
             "rect = patches.Rectangle(",
             "    (left, top), width, height,",
             "    linewidth=2, edgecolor=color, facecolor=\"none\"",
             ")",
             "ax.add_patch(rect)",
         ]),
    ]
    for title, desc, code in steps_code:
        story.append(KeepTogether([
            Paragraph(title, s["h2"]),
            Paragraph(desc, s["body"]),
            *[Paragraph(line.replace(" ", "&nbsp;").replace("<", "&lt;"), s["code"]) for line in code],
            Spacer(1, 8),
        ]))
        code_block(story, code, s)

    story.append(Paragraph("Understanding the Rekognition API Response", s["h1"]))
    story.append(Paragraph(
        "When Rekognition analyzes your image it returns a JSON object. "
        "There are two types of labels:",
        s["body"]))

    label_types = [
        ("Object Label", "Has a BoundingBox with coordinates. A box is drawn on the image.",
         "Dog, Car, Person, Bottle", GREEN),
        ("Scene Label", "No coordinates — describes the overall scene. Printed in terminal only.",
         "Outdoors, Nature, Urban", ORANGE),
    ]
    for name, desc, examples, color in label_types:
        row = [[
            Paragraph(f"<b>{name}</b>", s["body"]),
            Paragraph(desc, s["note"]),
            Paragraph(f"<i>e.g. {examples}</i>", s["note"]),
        ]]
        t = Table(row, colWidths=[3.5*cm, 7*cm, W - 10.5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), LIGHT_GRAY),
            ("TOPPADDING",   (0,0), (-1,-1), 7),
            ("BOTTOMPADDING",(0,0), (-1,-1), 7),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("LINEBEFORE",   (0,0), (0,-1), 4, color),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Bounding Box Coordinates Explained", s["h2"]))
    story.append(Paragraph(
        "Rekognition returns bounding box values as percentages between 0.0 and 1.0, "
        "not pixel values. To draw on the actual image you multiply by the image dimensions:",
        s["body"]))
    code_block(story, [
        "left   = box[\"Left\"]   * image_width    # e.g. 0.10 * 800px = 80px",
        "top    = box[\"Top\"]    * image_height   # e.g. 0.20 * 600px = 120px",
        "width  = box[\"Width\"]  * image_width    # e.g. 0.35 * 800px = 280px",
        "height = box[\"Height\"] * image_height   # e.g. 0.60 * 600px = 360px",
    ], s)

    story.append(PageBreak())

    # ── PAGE 7: TROUBLESHOOTING + USE CASES ──────────────────────────────────
    story.append(ColorBanner("SECTION 5 — TROUBLESHOOTING", DARK_BLUE))
    story.append(Spacer(1, 0.4*cm))

    errors = [
        (
            "botocore.errorfactory.InvalidS3ObjectException",
            "Region mismatch between S3 bucket and Rekognition, or wrong bucket name.",
            "Make sure BUCKET_NAME in the script matches exactly. The script sends image bytes directly so region mismatch should not apply. Double-check the bucket name has no typos."
        ),
        (
            "botocore.exceptions.NoCredentialsError",
            "AWS CLI is not configured, or credentials were not saved properly.",
            "Run aws configure again and re-enter your Access Key ID and Secret Access Key from the CSV file."
        ),
        (
            "FileNotFoundError: images/sample.jpg",
            "The image file does not exist at that path.",
            "Make sure you copied an image file into the images\\ folder and named it sample.jpg."
        ),
        (
            "(venv) not showing in PowerShell",
            "The virtual environment was not activated.",
            "Run: .\\venv\\Scripts\\Activate.ps1  from inside the C:\\Image Labels Generator folder."
        ),
        (
            "ModuleNotFoundError: No module named 'boto3'",
            "Libraries not installed in the active virtual environment.",
            "Activate venv first, then run: pip install boto3 matplotlib pillow"
        ),
        (
            "aws: command not found / not recognized",
            "AWS CLI was not installed or PATH was not updated.",
            "Reinstall AWS CLI with: winget install Amazon.AWSCLI  and then open a new PowerShell window."
        ),
    ]
    for error, cause, fix in errors:
        block = [
            [Paragraph(f"<b>Error:</b>  {error}", s["code"]),
             Paragraph(f"<b>Cause:</b>  {cause}", s["note"]),
             Paragraph(f"<b>Fix:</b>  {fix}", s["note"])],
        ]
        t = Table(block, colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#fdecea")),
            ("TOPPADDING",   (0,0), (-1,-1), 7),
            ("BOTTOMPADDING",(0,0), (-1,-1), 7),
            ("LEFTPADDING",  (0,0), (-1,-1), 10),
            ("LINEBEFORE",   (0,0), (0,-1), 4, colors.HexColor("#e74c3c")),
        ]))
        story.append(t)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 0.4*cm))
    story.append(ColorBanner("SECTION 6 — USE CASES & FREE TIER LIMITS", DARK_BLUE))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Real-World Use Cases", s["h1"]))
    use_cases = [
        ("Smart Surveillance", "Automatically tag and alert on detected objects in security camera footage — detect a person, vehicle, or animal entering a restricted area."),
        ("Retail Inventory Management", "Point a camera at a shelf and automatically detect which products are present, low in stock, or missing."),
        ("Accessibility for Visually Impaired", "Describe the contents of an image in real time to assist users who cannot see it."),
        ("Photo Organization", "Automatically sort thousands of photos by their content — separate dog photos, nature photos, and city photos automatically."),
        ("Content Moderation", "Automatically scan user-uploaded images for inappropriate content before publishing."),
    ]
    for title, desc in use_cases:
        row = [[Paragraph(f"<b>{title}</b>", s["body"]), Paragraph(desc, s["note"])]]
        t = Table(row, colWidths=[4.5*cm, W - 4.5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), LIGHT_GRAY),
            ("TOPPADDING",   (0,0), (-1,-1), 7),
            ("BOTTOMPADDING",(0,0), (-1,-1), 7),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("LINEBEFORE",   (0,0), (0,-1), 4, ACCENT_BLUE),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("AWS Free Tier Limits", s["h1"]))
    free_tier = [
        ["Service", "Free Tier Allowance", "After Free Tier"],
        ["Amazon S3", "5 GB storage\n20,000 GET requests/month\n2,000 PUT requests/month", "$0.023 per GB/month"],
        ["Amazon Rekognition", "5,000 images per month\n(first 12 months only)", "$0.001 per image"],
        ["AWS IAM", "Always free", "Always free"],
    ]
    ft_table = Table(free_tier, colWidths=[4*cm, 7*cm, W - 11*cm])
    ft_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK_BLUE),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("BACKGROUND",   (0,1), (-1,-1), LIGHT_GRAY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [LIGHT_GRAY, colors.white]),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(ft_table)

    # ── FINAL PAGE: QUICK REFERENCE ───────────────────────────────────────────
    story.append(PageBreak())
    story.append(ColorBanner("QUICK REFERENCE CHEAT SHEET", DARK_BLUE))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Commands You Will Use Every Time", s["h1"]))
    commands = [
        ("Open project folder",     "cd \"C:\\Image Labels Generator\""),
        ("Activate virtual env",    ".\\venv\\Scripts\\Activate.ps1"),
        ("Run the script",          "python detect_labels.py images/sample.jpg"),
        ("Run with a different image", "python detect_labels.py images/yourphoto.jpg"),
        ("Open output image",       "start output\\labeled_sample.jpg"),
        ("Deactivate virtual env",  "deactivate"),
        ("List S3 bucket contents", "aws s3 ls s3://your-bucket-name"),
    ]
    for desc, cmd in commands:
        row = [[Paragraph(desc, s["note"]), Paragraph(cmd, s["code"])]]
        t = Table(row, colWidths=[5.5*cm, W - 5.5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), LIGHT_GRAY),
            ("TOPPADDING",   (0,0), (-1,-1), 6),
            ("BOTTOMPADDING",(0,0), (-1,-1), 6),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ]))
        story.append(t)
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("File You Need to Edit", s["h1"]))
    code_block(story, [
        "detect_labels.py  —  Line 10:",
        "    BUCKET_NAME = \"image-labels-amirtha\"   ← change to YOUR bucket name",
    ], s)

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Workflow Summary", s["h1"]))
    workflow = [
        ["#", "Action", "Where"],
        ["1", "Put image in images\\ folder", "Windows File Explorer"],
        ["2", "Activate venv", "PowerShell"],
        ["3", "Run detect_labels.py", "PowerShell"],
        ["4", "Open labeled image in output\\", "Windows File Explorer"],
    ]
    wt = Table(workflow, colWidths=[1*cm, 9*cm, W - 10*cm])
    wt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), ACCENT_BLUE),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 10),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [LIGHT_GRAY, colors.white]),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("ALIGN",        (0,0), (0,-1), "CENTER"),
    ]))
    story.append(wt)

    story.append(Spacer(1, 0.8*cm))
    hr(story)
    story.append(Paragraph(
        "Image Labels Generator  |  Built with Python, boto3, matplotlib  |  Powered by AWS Rekognition &amp; S3",
        s["footer"]))

    doc.build(story)
    print(f"PDF saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
