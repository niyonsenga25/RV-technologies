"""
PDF Invoice Generator using reportlab
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

def generate_invoice(order, order_items, output_path):
    """Generate PDF invoice for an order"""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666')
    )
    
    # Title
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Company Info
    company_data = [
        ['E-Commerce Store', ''],
        ['Email: info@ecommerce.com', ''],
        ['Phone: +250 788 123 456', ''],
        ['Website: www.ecommerce.com', '']
    ]
    
    # Order Info
    order_data = [
        ['Order Number:', order['order_number']],
        ['Order Date:', order['created_at'].strftime('%B %d, %Y') if isinstance(order['created_at'], datetime) else str(order['created_at'])],
        ['Status:', order['status']],
        ['Payment Method:', order['payment_method']]
    ]
    
    # Customer Info
    customer_data = [
        ['Bill To:', ''],
        [order['shipping_name'], ''],
        [order['shipping_phone'], ''],
        [order['shipping_address'], '']
    ]
    
    # Create tables
    company_table = Table(company_data, colWidths=[4*inch, 2*inch])
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 14),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1a1a1a')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    order_table = Table(order_data, colWidths=[2*inch, 3*inch])
    order_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    customer_table = Table(customer_data, colWidths=[3*inch, 3*inch])
    customer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    # Combine info tables
    info_data = [[company_table, order_table, customer_table]]
    info_table = Table(info_data, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Order Items Table
    story.append(Paragraph("Order Items", heading_style))
    
    # Import Decimal early for use in calculations
    from decimal import Decimal
    
    items_data = [['Product', 'Quantity', 'Price', 'Total']]
    for item in order_items:
        quantity = Decimal(str(item['quantity']))
        price = Decimal(str(item['price']))
        total = quantity * price
        items_data.append([
            item['product_name'],
            str(item['quantity']),
            f"{price:,.0f} RWF",
            f"{total:,.0f} RWF"
        ])
    
    items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Total Section
    subtotal = sum(Decimal(str(item['quantity'])) * Decimal(str(item['price'])) for item in order_items)
    tax = subtotal * Decimal('0.18')  # 18% VAT
    total = subtotal + tax
    
    total_data = [
        ['Subtotal:', f"{subtotal:,.0f} RWF"],
        ['Tax (18%):', f"{tax:,.0f} RWF"],
        ['Total:', f"{total:,.0f} RWF"]
    ]
    
    total_table = Table(total_data, colWidths=[4*inch, 2*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -2), 11),
        ('FONTSIZE', (0, -1), (-1, -1), 14),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#1a1a1a')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(Paragraph("", normal_style))  # Spacer
    story.append(total_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = "Thank you for your purchase! For any inquiries, please contact us at info@ecommerce.com"
    story.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(story)
    return output_path



