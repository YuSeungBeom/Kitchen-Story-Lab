from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def compress_image(uploaded_image, quality=70, max_size=(800, 800)):
    """
    이미지 압축 및 리사이징 유틸리티 함수
    
    주요 기능:
    - 이미지 크기 최적화
    - 압축률 조정
    - 포맷 변환 (필요시)
    
    매개변수:
    - uploaded_image: 원본 이미지 파일
    - quality: 압축 품질 (1-100)
    - max_size: 최대 이미지 크기 튜플
    
    반환값:
    압축 및 리사이징된 이미지 파일
    """
    try:
        img = Image.open(uploaded_image)
        
        # RGB 모드로 변환 (투명도 있는 PNG 처리)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 이미지 리사이징
        img.thumbnail(max_size, Image.LANCZOS)
        
        # 메모리 버퍼에 저장
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        
        # Django 파일 객체로 변환
        compressed_image = ContentFile(buffer.getvalue())
        compressed_image.name = uploaded_image.name.split('.')[0] + '.jpg'
        
        return compressed_image
    
    except Exception as e:
        # 이미지 처리 중 오류 발생 시 로깅 또는 기본 처리
        print(f"이미지 압축 중 오류 발생: {e}")
        return uploaded_image