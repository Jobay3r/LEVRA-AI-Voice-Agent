from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf():
    """Create a simple test PDF for testing upload functionality."""
    
    content = """Test PDF Content for LEVRA Voice Assistant

This is a test document to verify PDF upload functionality.

Key Information:
- User Name: John Doe
- Role: Software Engineer  
- Company: Tech Innovations Inc.
- Skills: Python, JavaScript, React, Node.js
- Goals: Leadership development, communication skills

Training Focus Areas:
1. Public Speaking - Needs improvement in presenting to large groups
2. Team Leadership - Recently promoted to team lead position
3. Conflict Resolution - Dealing with difficult team dynamics
4. Strategic Thinking - Moving from technical to strategic role

Current Challenges:
- Managing a team of 8 developers
- Balancing technical work with management duties
- Preparing for quarterly business reviews
- Mentoring junior developers

This document should be used as context for personalized training 
recommendations and skill assessments."""

    # Create PDF
    filename = "test_document.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Split content into lines
    lines = content.split('\n')
    y_position = 750
    
    for line in lines:
        if y_position < 50:  # Start new page if needed
            c.showPage()
            y_position = 750
            
        c.drawString(50, y_position, line)
        y_position -= 20
    
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_test_pdf()
