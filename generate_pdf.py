import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Register Korean Fonts
pdfmetrics.registerFont(TTFont('Malgun', 'C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('MalgunBold', 'C:/Windows/Fonts/malgunbd.ttf'))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Malgun", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 808, "신기한 입체도형 DIY 교구 학습 및 제작 가이드 | @moonshotkidz & anyhomepick 영상 기반")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 802, 559, 802)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 42, 559, 42)
        self.drawString(36, 30, "당기면 팝업되는 입체도형 전개도 학습 설명서 (초등 수학 공간감각 발달)")
        page_text = f"페이지 {self._pageNumber} / {page_count}"
        self.drawRightString(559, 30, page_text)
        self.restoreState()

def create_manual():
    pdf_path = r"c:\work123\입체도형_전개도_교구_설명서.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='MalgunBold',
        fontSize=18,
        leading=23,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='MalgunBold',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='MalgunBold',
        fontSize=12.5,
        leading=16.5,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='MalgunBold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Malgun',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Malgun',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#334155"),
        leftIndent=10,
        firstLineIndent=-10,
        spaceAfter=2.5
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Malgun',
        fontSize=7.5,
        leading=10,
        alignment=1, # Centered
        textColor=colors.HexColor("#475569")
    )

    caption_bold = ParagraphStyle(
        'Caption_Bold',
        parent=styles['Normal'],
        fontName='MalgunBold',
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#1E293B")
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Malgun',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )

    curated_dir = r"c:\work123\video_data\curated_frames_tight"
    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("【교구 활용 가이드】 당기면 팝업되는 신기한 입체도형 DIY", title_style))
    story.append(Paragraph("2D 평면 전개도에서 3D 입체도형으로! 초등 공간지각력 쑥쑥 키우는 매직 교구 설명서", subtitle_style))
    
    # Meta Box
    meta_data = [
        [
            Paragraph("<b>영상 출처:</b> 유튜브 쇼츠 (ID: BmUZ8yaFT3I)", body_style),
            Paragraph("<b>원작자/채널:</b> anyhomepick (@moonshotkidz)", body_style)
        ],
        [
            Paragraph("<b>핵심 키워드:</b> #입체도형DIY #초등수학 #공간감각 #아이교육 #전개도", body_style),
            Paragraph("<b>교육 대상:</b> 유아~초등 전 학년 (초등 3~6학년 도형단원 최적)", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[260, 263])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Section 1
    story.append(Paragraph("1. 영상 내용 개요 및 자막 나레이션 전문", h1_style))
    story.append(Paragraph(
        "본 영상은 초등학생 및 유아들이 가장 어려워하는 수학 개념인 <b>'평면 전개도와 입체도형의 상관관계'</b>를 "
        "실을 잡아당기는 직관적인 조작 놀이를 통해 한눈에 이해할 수 있도록 만든 혁신적인 핸즈온(Hands-on) 교구를 소개합니다. "
        "영상 속 자막과 해설 내용을 정리한 전문은 다음과 같습니다.", body_style
    ))

    script_box = [
        [
            Paragraph(
                "<b>💬 영상 나레이션 자막 전문:</b><br/>"
                "<i>\"아이한테 이거 정말 신기하더라고요. 평면이랑 입체도형을 아무리 설명해도 아이들은 이해하기 어렵잖아요. "
                "평평한 종이를 살짝 잡아당기면 눈앞에서 입체 도형으로 모양이 바뀌고 도형이 펼쳐지니까, "
                "단순히 보고 외우는 게 아니라 직접 만지고 움직이면서 이해할 수 있고 즐기다 보니 공간 감각까지 키울 수 있겠더라고요.\"</i>",
                callout_style
            )
        ]
    ]
    script_table = Table(script_box, colWidths=[523])
    script_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('LINELEFT', (0,0), (0,0), 3.5, colors.HexColor("#2563EB")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(script_table)
    story.append(Spacer(1, 8))

    # Section 2
    story.append(Paragraph("2. '당김 전개도 교구'가 수학 학습에 혁신적인 이유", h1_style))
    benefits = [
        ("① 추상적 기하학의 구체적 시각화", "교과서의 정적인 2D 그림만으로는 '접었을 때 어느 면과 면이 만나는지' 머릿속으로 시뮬레이션하기 힘듭니다. 실을 당기면 평면이 순식간에 3D로 솟아올라 직관적으로 파악됩니다."),
        ("② 능동적 촉각 학습 (Hands-on Manipulative)", "단순 암기식 주입이 아닌, 아이가 스스로 줄을 당기고 펴보는 양방향(Interactive) 신체 감각을 통해 뇌의 공간지각 회로가 강력하게 활성화됩니다."),
        ("③ 면(Face)과 모서리(Edge)의 일대일 대응 체득", "실이 지나가는 구멍들이 서로 가까워지면서 모서리가 맞닿는 물리적 과정을 통해 입체도형의 결합 원리를 자연스럽게 터득합니다."),
        ("④ 실패 없는 도형 탐구와 호기심 유발", "풀이나 접착제 없이 실 하나로 무한 반복 접기/펼치기가 가능하여 마술 같은 성취감과 수학에 대한 흥미를 높입니다.")
    ]
    for title, desc in benefits:
        story.append(Paragraph(f"• <b>{title}</b>: {desc}", bullet_style))
    
    story.append(Spacer(1, 6))

    intro_box = [
        [
            Paragraph(
                "<b>💡 교육학적 통찰:</b> 피아제(Piaget)의 인지발달이론에 따르면 초등 연령대 아동은 '구체적 조작기(Concrete Operational Stage)'에 해당합니다. "
                "이 시기에는 언어나 기호 설명보다 실물을 직접 손으로 만지고 변형시키는 구체적 조작 활동이 수학적 사고력 형성에 결정적인 역할을 합니다.",
                callout_style
            )
        ]
    ]
    intro_table = Table(intro_box, colWidths=[523])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BBF7D0")),
        ('LINELEFT', (0,0), (0,0), 3.5, colors.HexColor("#16A34A")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(intro_table)

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(Paragraph("3. 영상 속 4대 입체도형 메커니즘 상세 분석 (Part 1)", h1_style))
    story.append(Paragraph(
        "영상에서 시연된 4가지 대표 도형 중 기둥과 뿔의 기본형인 직육면체와 삼각뿔의 변환 과정을 분석합니다.",
        body_style
    ))

    # Shape 1: 직육면체
    story.append(Paragraph("도형 1: 직육면체 / 정육면체 (Cube & Rectangular Prism)", h2_style))
    story.append(Paragraph(
        "전개도의 네 면이 일렬로 배열되고 양옆에 날개 면이 달린 기본 전개도입니다. "
        "마주보는 면의 모서리에 펀치 구멍을 뚫고 실을 대칭으로 꿴 뒤 <b>'PULL'</b> 손잡이를 당기면 4개의 옆면과 2개의 밑면이 동시에 닫히며 직육면체 상자가 완성됩니다.",
        body_style
    ))

    # 3 images for cube: flat, pulling, 3d (tight crops)
    w3, h3 = 145, 185
    c1 = RLImage(os.path.join(curated_dir, "01_cube_flat.jpg"), width=w3, height=h3)
    c2 = RLImage(os.path.join(curated_dir, "02_cube_pulling.jpg"), width=w3, height=h3)
    c3 = RLImage(os.path.join(curated_dir, "03_cube_3d.jpg"), width=w3, height=h3)

    cube_table_data = [
        [c1, c2, c3],
        [
            Paragraph("<b>[1단계: 평면 전개도]</b><br/>실이 통과된 2D 전개도와 PULL 손잡이", caption_style),
            Paragraph("<b>[2단계: 당김 과정]</b><br/>줄을 당기자 면들이 각도를 이루며 기립", caption_style),
            Paragraph("<b>[3단계: 3D 직육면체 완성]</b><br/>완벽하게 닫힌 입체 상자 완성", caption_style)
        ]
    ]
    cube_table = Table(cube_table_data, colWidths=[174, 174, 174])
    cube_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 2),
        ('TOPPADDING', (0,1), (-1,1), 2),
    ]))
    story.append(cube_table)
    story.append(Spacer(1, 4))

    # Shape 2: 삼각뿔 / 정사면체
    story.append(Paragraph("도형 2: 삼각뿔 / 정사면체 (Triangular Pyramid & Tetrahedron)", h2_style))
    story.append(Paragraph(
        "정삼각형 4개로 이루어진 정사면체 전개도입니다. 바닥 중앙 정삼각형을 기준으로 세 변에 붙은 측면 삼각형 꼭짓점에 구멍을 뚫어 실을 통과시켰습니다. "
        "당기는 순간 3개의 꼭짓점이 허공의 한 점으로 모여 우뚝 솟은 피라미드가 됩니다.",
        body_style
    ))

    wp, hp = 145, 185
    p1 = RLImage(os.path.join(curated_dir, "04_pyramid_flat.jpg"), width=wp, height=hp)
    p2 = RLImage(os.path.join(curated_dir, "05_pyramid_3d.jpg"), width=wp, height=hp)
    
    pyr_note = Paragraph(
        "<b>📐 교육 핵심 포인트 (초등 6-1 각기둥과 각뿔):</b><br/>"
        "• <b>밑면:</b> 1개 (정삼각형)<br/>"
        "• <b>옆면:</b> 3개 (모두 정삼각형)<br/>"
        "• <b>꼭짓점:</b> 4개 (모이는 맨 위 꼭짓점 = '각뿔의 꼭짓점')<br/>"
        "• <b>모서리:</b> 6개 (접히면서 실에 의해 서로 맞닿는 변 확인)<br/>"
        "• <b>학습 지도법:</b> 전개도의 어떤 변들이 만나서 하나의 모서리가 되는지 색깔 스티커로 표시해보면 공간지각력이 크게 향상됩니다.",
        callout_style
    )

    pyr_table_data = [
        [p1, p2, pyr_note],
        [
            Paragraph("<b>[평면 전개도]</b> 펼쳐진 정삼각형 전개도", caption_style),
            Paragraph("<b>[입체 삼각뿔 완성]</b> 꼭짓점이 모여 피라미드 완성", caption_style),
            Paragraph("<b>[수학적 원리 및 지도 팁]</b>", caption_bold)
        ]
    ]
    pyr_table = Table(pyr_table_data, colWidths=[165, 165, 193])
    pyr_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#F0FDFA")),
        ('BOX', (2,0), (2,0), 1, colors.HexColor("#99F6E4")),
        ('LEFTPADDING', (2,0), (2,0), 8),
        ('RIGHTPADDING', (2,0), (2,0), 8),
        ('TOPPADDING', (2,0), (2,0), 6),
        ('BOTTOMPADDING', (0,0), (-1,0), 2),
        ('TOPPADDING', (0,1), (-1,1), 2),
    ]))
    story.append(pyr_table)

    # ================= PAGE 3 =================
    story.append(PageBreak())
    story.append(Paragraph("3. 영상 속 4대 입체도형 메커니즘 상세 분석 (Part 2)", h1_style))
    story.append(Paragraph(
        "곡면을 형성하는 원기둥과 다각형이 결합된 오각뿔의 정교한 팝업 메커니즘을 분석합니다.",
        body_style
    ))

    # Shape 3: 원기둥
    story.append(Paragraph("도형 3: 원기둥 (Cylinder - 곡면 팝업 메커니즘)", h2_style))
    story.append(Paragraph(
        "다각형뿐만 아니라 곡면을 가진 원기둥도 완벽하게 구현됩니다! "
        "전개도의 직사각형 옆면 양 끝에 펀칭을 하고 두 개의 원형 밑면과 실로 연결합니다. "
        "실을 당기면 평평했던 직사각형이 부드럽게 둥글게 말리면서 상하 원판이 뚜껑처럼 정확히 덮입니다.",
        body_style
    ))

    cy1 = RLImage(os.path.join(curated_dir, "06_cylinder_flat.jpg"), width=w3, height=h3)
    cy2 = RLImage(os.path.join(curated_dir, "08_cylinder_detail.jpg"), width=w3, height=h3)
    cy3 = RLImage(os.path.join(curated_dir, "07_cylinder_3d.jpg"), width=w3, height=h3)

    cyl_table_data = [
        [cy1, cy2, cy3],
        [
            Paragraph("<b>[전개도 상태]</b> 직사각형과 상하 원형 밑면", caption_style),
            Paragraph("<b>[실 통과 상세]</b> 곡면을 말아주는 타공 및 실 경로", caption_style),
            Paragraph("<b>[원기둥 완성]</b> 실을 당겨 둥근 기둥 완성", caption_style)
        ]
    ]
    cyl_table = Table(cyl_table_data, colWidths=[174, 174, 174])
    cyl_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 2),
        ('TOPPADDING', (0,1), (-1,1), 2),
    ]))
    story.append(cyl_table)
    story.append(Spacer(1, 4))

    # Shape 4: 오각뿔 (Star Net)
    story.append(Paragraph("도형 4: 오각뿔 / 별 모양 전개도 (Pentagonal Pyramid)", h2_style))
    story.append(Paragraph(
        "중앙의 정오각형을 밑면으로 하고 5개의 이등변삼각형이 별처럼 뻗은 전개도입니다. "
        "영상 후반부에 제작 과정이 디테일하게 등장하며, 별의 5개 꼭짓점에 펀치 구멍을 내고 실을 순서대로 꿴 뒤 위로 들어 올리면 웅장한 5각 텐트 모양이 완성됩니다.",
        body_style
    ))

    st1 = RLImage(os.path.join(curated_dir, "09_star_lacing.jpg"), width=w3, height=h3)
    st2 = RLImage(os.path.join(curated_dir, "10_star_flat.jpg"), width=w3, height=h3)
    st3 = RLImage(os.path.join(curated_dir, "11_star_3d.jpg"), width=w3, height=h3)

    star_table_data = [
        [st1, st2, st3],
        [
            Paragraph("<b>[실 꿰기 작업]</b> 꼭짓점 구멍에 실을 꿰는 손동작", caption_style),
            Paragraph("<b>[펼친 별 전개도]</b> 접는 선(점선)을 누른 평면 상태", caption_style),
            Paragraph("<b>[오각뿔 완성]</b> 줄을 위로 당겨 완성된 피라미드", caption_style)
        ]
    ]
    star_table = Table(star_table_data, colWidths=[174, 174, 174])
    star_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 2),
        ('TOPPADDING', (0,1), (-1,1), 2),
    ]))
    story.append(star_table)

    # ================= PAGE 4 =================
    story.append(PageBreak())
    story.append(Paragraph("4. 집에서 직접 만드는 '팝업 전개도 교구' DIY 가이드", h1_style))
    story.append(Paragraph(
        "아이와 함께 주변의 간단한 문구류로 손쉽게 만들 수 있습니다. 실패 없이 깔끔하게 접히도록 만드는 핵심 노하우를 공개합니다.",
        body_style
    ))

    # Materials Table
    mat_data = [
        [Paragraph("<b>준비물</b>", caption_bold), Paragraph("<b>추천 규격 및 선정 이유</b>", caption_bold), Paragraph("<b>활용 용도</b>", caption_bold)],
        [
            Paragraph("<b>도화지 / 색상지</b>", body_style),
            Paragraph("180g~250g/m² 백상지 또는 색도화지 (너무 얇으면 찌그러지고 너무 두꺼우면 뻑뻑함)", body_style),
            Paragraph("도형의 뼈대가 되는 전개도 본체", body_style)
        ],
        [
            Paragraph("<b>끈 (실)</b>", body_style),
            Paragraph("표면이 매끄러운 면끈, 트와인끈, 얇은 운동화끈 (마찰력이 적어야 부드럽게 작동)", body_style),
            Paragraph("도형을 세우고 펼치는 당김줄", body_style)
        ],
        [
            Paragraph("<b>1공 펀치 / 송곳</b>", body_style),
            Paragraph("지름 3~5mm 표준 1공 펀치 (아이 안전 고려)", body_style),
            Paragraph("꼭짓점 및 모서리에 실 통과 구멍 타공", body_style)
        ],
        [
            Paragraph("<b>자, 굳은 볼펜 / 철필</b>", body_style),
            Paragraph("선 긋기용 자, 잉크 안 나오는 볼펜 또는 칼등", body_style),
            Paragraph("<b>[핵심!]</b> 접는 선에 누름선(Score) 긋기", body_style)
        ],
        [
            Paragraph("<b>받침대 (스케치북)</b>", body_style),
            Paragraph("스프링 스케치북 또는 두꺼운 하드보드지", body_style),
            Paragraph("도형 밑면을 고정하여 팝업북 형태로 활용", body_style)
        ]
    ]
    mat_table = Table(mat_data, colWidths=[100, 260, 163])
    mat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(mat_table)
    story.append(Spacer(1, 6))

    # 5-Step Process
    story.append(Paragraph("📌 5단계 제작 프로세스 (Step-by-Step)", h2_style))
    steps = [
        ("Step 1. 전개도 도안 작도 또는 출력", "원하는 입체도형(직육면체, 삼각뿔, 원기둥 등)의 전개도를 200g 도화지에 자와 연필로 정확히 그립니다. (치수가 정확해야 입체로 조립되었을 때 빈틈이 생기지 않습니다.)"),
        ("Step 2. 누름선(Scoring) 작업 ★가장 중요★", "가위로 자르기 전, 모든 접히는 선(점선)을 자와 <b>굳은 볼펜(또는 칼등)</b>으로 꾹 눌러 그어줍니다. 종이 표면에 접힘 홈이 생겨 실을 당길 때 정확한 각도로 깔끔하게 접힙니다."),
        ("Step 3. 외곽선 오리기 및 타공(Punching)", "외곽 실선을 가위로 오려낸 뒤, 실이 지나갈 꼭짓점과 모서리 끝단(가장자리에서 약 3~5mm 안쪽)에 1공 펀치로 깔끔하게 구멍을 뚫습니다."),
        ("Step 4. 실 꿰기 (Lacing)", "도형의 마주보는 면들이 한곳으로 모이도록 실을 통과시킵니다. (오각뿔은 5개 꼭짓점을 순차적으로 꿰고, 직육면체는 양쪽 대칭으로 꿰어줍니다.)"),
        ("Step 5. 밑면 고정 및 'PULL' 손잡이 달기", "중앙 밑면을 스케치북이나 받침대 바닥에 풀로 고정합니다. 실 양쪽 끝을 모아 작은 종이 라벨('PULL')을 테이프로 감아 손잡이를 만들어 완성합니다.")
    ]
    for s_title, s_desc in steps:
        story.append(Paragraph(f"<b>{s_title}</b>: {s_desc}", bullet_style))
    
    story.append(Spacer(1, 6))

    # Section 5: Educational Application
    story.append(Paragraph("5. 초등 수학 교육과정 연계 및 200% 활용 지도 팁", h1_style))
    
    edu_box = [
        [
            Paragraph(
                "<b>📚 초등 수학 교과 연계 단원:</b><br/>"
                "• <b>초등 3학년 1학기 [평면도형]:</b> 삼각형, 사각형, 원의 기본 특성<br/>"
                "• <b>초등 5학년 2학기 [직육면체]:</b> 직육면체와 정육면체의 구성 요소(면, 모서리, 꼭짓점), 전개도 11가지 탐구<br/>"
                "• <b>초등 6학년 1학기 [각기둥과 각뿔]:</b> 각기둥과 각뿔의 이름 짓기, 밑면과 옆면의 관계, 겨냥도와 전개도<br/>"
                "• <b>초등 6학년 2학기 [원기둥, 원뿔, 구]:</b> 곡면의 성질, 원기둥 전개도에서 밑면의 둘레 = 옆면의 가로 길이<br/><br/>"
                "<b>💡 아이와 함께하는 즐거운 홈스쿨링 퀴즈 놀이:</b><br/>"
                "1. <b>'맞닿는 모서리 찾기' 퀴즈:</b> 실을 당기기 전, \"빨간색 변과 붙게 될 모서리는 어디일까?\" 예측해보고 직접 당겨 확인하기<br/>"
                "2. <b>'마주보는 면 찾기' 놀이:</b> 상자가 되었을 때 서로 평행하게 마주보는 면에 같은 색 스티커를 붙여 공간지각력 훈련하기<br/>"
                "3. <b>'나만의 팝업 수학책' 만들기:</b> 스케치북 한 권에 여러 입체도형을 페이지마다 만들어 붙이면 평생 간직하는 팝업북 완성!",
                callout_style
            )
        ]
    ]
    edu_table = Table(edu_box, colWidths=[523])
    edu_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FDE68A")),
        ('LINELEFT', (0,0), (0,0), 3.5, colors.HexColor("#D97706")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(edu_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {pdf_path}")

if __name__ == "__main__":
    create_manual()
