import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

DEFAULT_OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs", "milestone-1", "Relational_Model.pdf"
)

def build_pdf(filename=DEFAULT_OUT):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=12
    )

    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    card_header_style = ParagraphStyle(
        'CardHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0F172A')
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#F8FAFC'),
        backColor=colors.HexColor('#0F172A'),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    detail_style = ParagraphStyle(
        'DetailStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    notation_style = ParagraphStyle(
        'NotationStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1E293B')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.0,
        leading=12,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # Title Banner
    story.append(Paragraph("CSCE 2501 — Fundamentals of Database Systems", subtitle_style))
    story.append(Paragraph("Relational Model (Schema Mapping)", title_style))
    story.append(Paragraph("Resale Real Estate Database — Milestone I", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2563EB'), spaceAfter=10))

    # Notation Box
    notation_text = """
    <b>Notation & Conventions:</b><br/>
    • <u><b>Underlined</b></u> attributes denote <b>Primary Keys (PK)</b>.<br/>
    • <i><b>Italicized</b></i> attributes denote <b>Foreign Keys (FK)</b>.<br/>
    • All relation schemas are fully normalized to at least <b>3NF / BCNF</b>.
    """
    notation_table = Table(
        [[Paragraph(notation_text, notation_style)]],
        colWidths=[520]
    )
    notation_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINELEFT', (0,0), (0,-1), 3.5, colors.HexColor('#2563EB')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(notation_table)
    story.append(Spacer(1, 12))

    # Section 1: Relational Schemas
    story.append(Paragraph("1. Relational Schemas", section_style))

    schemas_data = [
        {
            "num": "1",
            "name": "Location",
            "type": "Independent Base Entity",
            "signature": "Location(<u>location_id</u>, city, district, area_name, compound_name)",
            "details": [
                "<b>PK:</b> <code>location_id</code>",
                "<b>FK:</b> None (Independent entity)"
            ]
        },
        {
            "num": "2",
            "name": "Developer",
            "type": "Independent Base Entity",
            "signature": "Developer(<u>developer_id</u>, developer_name, corporate_details, total_projects, total_properties_listed)",
            "details": [
                "<b>PK:</b> <code>developer_id</code>",
                "<b>UNIQUE:</b> <code>developer_name</code>",
                "<b>FK:</b> None (Independent entity)"
            ]
        },
        {
            "num": "3",
            "name": "Development",
            "type": "Dependent Entity",
            "signature": "Development(<u>development_id</u>, project_name, description, <i>developer_id</i>, <i>location_id</i>)",
            "details": [
                "<b>PK:</b> <code>development_id</code>",
                "<b>FK 1:</b> <code>developer_id</code> &rarr; Developer(developer_id) ON DELETE RESTRICT ON UPDATE CASCADE",
                "<b>FK 2:</b> <code>location_id</code> &rarr; Location(location_id) ON DELETE RESTRICT ON UPDATE CASCADE"
            ]
        },
        {
            "num": "4",
            "name": "Property",
            "type": "Dependent Entity",
            "signature": "Property(<u>property_id</u>, title, description, source_url, total_area_sqm, num_bedrooms, num_bathrooms, property_type, asking_price, price_per_sqm, payment_method, down_payment, contract_year, discount_over_market, gain_over_market, <i>development_id</i>, <i>location_id</i>)",
            "details": [
                "<b>PK:</b> <code>property_id</code>",
                "<b>FK 1:</b> <code>development_id</code> &rarr; Development(development_id) ON DELETE CASCADE ON UPDATE CASCADE",
                "<b>FK 2:</b> <code>location_id</code> &rarr; Location(location_id) ON DELETE RESTRICT ON UPDATE CASCADE",
                "<b>CHECK:</b> property_type IN ('apartment', 'villa', 'townhouse', 'duplex', 'chalet', 'penthouse', 'studio', 'other')",
                "<b>CHECK:</b> payment_method IN ('cash', 'installment')"
            ]
        },
        {
            "num": "5",
            "name": "Amenity",
            "type": "Independent Base Entity",
            "signature": "Amenity(<u>amenity_id</u>, amenity_name)",
            "details": [
                "<b>PK:</b> <code>amenity_id</code>",
                "<b>UNIQUE:</b> <code>amenity_name</code>",
                "<b>FK:</b> None (Lookup entity)"
            ]
        },
        {
            "num": "6",
            "name": "Property_Amenity",
            "type": "Junction Table (M:N)",
            "signature": "Property_Amenity(<u><i>property_id</i></u>, <u><i>amenity_id</i></u>)",
            "details": [
                "<b>COMPOSITE PK:</b> (property_id, amenity_id)",
                "<b>FK 1:</b> <code>property_id</code> &rarr; Property(property_id) ON DELETE CASCADE ON UPDATE CASCADE",
                "<b>FK 2:</b> <code>amenity_id</code> &rarr; Amenity(amenity_id) ON DELETE CASCADE ON UPDATE CASCADE"
            ]
        },
        {
            "num": "7",
            "name": "User",
            "type": "Independent Base Entity",
            "signature": "User(<u>user_id</u>, username, email, password_hash, gender, age, birthdate)",
            "details": [
                "<b>PK:</b> <code>user_id</code>",
                "<b>UNIQUE:</b> <code>username</code>, <code>email</code>",
                "<b>CHECK:</b> gender IN ('Male', 'Female')",
                "<b>CHECK:</b> age &gt;= 18"
            ]
        },
        {
            "num": "8",
            "name": "User_Focus_Area",
            "type": "Junction Table (M:N)",
            "signature": "User_Focus_Area(<u><i>user_id</i></u>, <u><i>location_id</i></u>)",
            "details": [
                "<b>COMPOSITE PK:</b> (user_id, location_id)",
                "<b>FK 1:</b> <code>user_id</code> &rarr; User(user_id) ON DELETE CASCADE ON UPDATE CASCADE",
                "<b>FK 2:</b> <code>location_id</code> &rarr; Location(location_id) ON DELETE CASCADE ON UPDATE CASCADE"
            ]
        },
        {
            "num": "9",
            "name": "Review",
            "type": "Dependent Entity",
            "signature": "Review(<u>review_id</u>, <i>user_id</i>, <i>development_id</i>, rating, review_comment, review_date)",
            "details": [
                "<b>PK:</b> <code>review_id</code>",
                "<b>FK 1:</b> <code>user_id</code> &rarr; User(user_id) ON DELETE CASCADE ON UPDATE CASCADE",
                "<b>FK 2:</b> <code>development_id</code> &rarr; Development(development_id) ON DELETE CASCADE ON UPDATE CASCADE",
                "<b>CHECK:</b> rating BETWEEN 1 AND 10",
                "<b>UNIQUE:</b> (user_id, development_id) — 1 review per user per project"
            ]
        }
    ]

    for item in schemas_data:
        card_content = []
        # Header row
        hdr = Paragraph(f"<b>{item['num']}. {item['name']}</b> &nbsp;&nbsp;<font color='#64748B'>[{item['type']}]</font>", card_header_style)
        card_content.append(hdr)
        card_content.append(Spacer(1, 3))
        
        # Signature
        sig = Paragraph(item['signature'], code_style)
        card_content.append(sig)
        card_content.append(Spacer(1, 3))
        
        # Details
        for d in item['details']:
            card_content.append(Paragraph(f"• {d}", detail_style))

        # Wrap in a nice Table card
        card_table = Table([[card_content]], colWidths=[520])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        
        story.append(KeepTogether([card_table, Spacer(1, 8)]))

    story.append(Spacer(1, 8))

    # Section 2: Normalization Verification
    story.append(Paragraph("2. Normalization Verification", section_style))

    norm_table_data = [
        [
            Paragraph("<b>Normal Form</b>", table_header_style),
            Paragraph("<b>Status</b>", table_header_style),
            Paragraph("<b>Justification</b>", table_header_style)
        ],
        [
            Paragraph("<b>1NF</b>", table_body_style),
            Paragraph("<font color='#16A34A'><b>✔ Satisfied</b></font>", table_body_style),
            Paragraph("All attributes are atomic values. Multi-valued attributes (amenities, focus areas) are resolved into dedicated junction relations.", table_body_style)
        ],
        [
            Paragraph("<b>2NF</b>", table_body_style),
            Paragraph("<font color='#16A34A'><b>✔ Satisfied</b></font>", table_body_style),
            Paragraph("No partial dependencies exist. All non-key attributes fully depend on the complete Primary Key in every relation.", table_body_style)
        ],
        [
            Paragraph("<b>3NF</b>", table_body_style),
            Paragraph("<font color='#16A34A'><b>✔ Satisfied</b></font>", table_body_style),
            Paragraph("No transitive dependencies exist. Every non-key attribute depends directly and solely on the primary key.", table_body_style)
        ],
        [
            Paragraph("<b>BCNF</b>", table_body_style),
            Paragraph("<font color='#16A34A'><b>✔ Satisfied</b></font>", table_body_style),
            Paragraph("Every functional dependency determinant is a candidate key in all relations.", table_body_style)
        ]
    ]

    norm_table = Table(norm_table_data, colWidths=[80, 80, 360])
    norm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')])
    ]))
    story.append(KeepTogether([norm_table, Spacer(1, 14)]))

    # Section 3: Dependency Tree
    story.append(Paragraph("3. Table Creation Order & Dependency Tree", section_style))

    dep_text = """
    <font color='#38BDF8'><b>Independent Base Tables (Create First):</b></font><br/>
    &nbsp;&nbsp;1. Location<br/>
    &nbsp;&nbsp;2. Developer<br/>
    &nbsp;&nbsp;3. User<br/>
    &nbsp;&nbsp;4. Amenity<br/><br/>
    <font color='#38BDF8'><b>Dependent & Junction Tables (Create After Parents):</b></font><br/>
    &nbsp;&nbsp;5. Development &nbsp;&nbsp;&nbsp;&mdash;&mdash;&gt; [depends on: Developer, Location]<br/>
    &nbsp;&nbsp;6. Property &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&mdash;&mdash;&gt; [depends on: Development, Location]<br/>
    &nbsp;&nbsp;7. Property_Amenity &mdash;&mdash;&gt; [depends on: Property, Amenity]<br/>
    &nbsp;&nbsp;8. User_Focus_Area &nbsp;&mdash;&mdash;&gt; [depends on: User, Location]<br/>
    &nbsp;&nbsp;9. Review &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&mdash;&mdash;&gt; [depends on: User, Development]
    """

    dep_style = ParagraphStyle(
        'DepStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9.0,
        leading=13,
        textColor=colors.HexColor('#E2E8F0')
    )

    dep_table = Table([[Paragraph(dep_text, dep_style)]], colWidths=[520])
    dep_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#1E293B')),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))

    story.append(KeepTogether([dep_table]))

    doc.build(story)
    print("PDF build successful:", filename)

if __name__ == "__main__":
    build_pdf()
