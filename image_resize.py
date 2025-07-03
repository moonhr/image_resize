#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import math
import shutil
import glob

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("이미지 리사이즈 프로그램")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # 현재 이미지 정보
        self.current_image = None
        self.current_image_path = None
        self.current_folder_path = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 모드 선택 프레임
        mode_frame = ttk.LabelFrame(main_frame, text="작업 모드", padding="10")
        mode_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # 모드 선택 버튼들
        button_frame = ttk.Frame(mode_frame)
        button_frame.grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="단일 이미지 파일 선택", 
                  command=self.select_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="폴더 선택 (WebP 변환)", 
                  command=self.select_folder).pack(side=tk.LEFT, padx=5)
        
        # 이미지 정보 표시 프레임
        info_frame = ttk.LabelFrame(main_frame, text="이미지 정보", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # 이미지 정보 레이블들
        self.info_labels = {}
        info_fields = ["파일명", "형식", "크기", "해상도", "파일 크기"]
        
        for i, field in enumerate(info_fields):
            ttk.Label(info_frame, text=f"{field}:").grid(row=i, column=0, sticky=tk.W, pady=2)
            self.info_labels[field] = ttk.Label(info_frame, text="선택된 파일이 없습니다")
            self.info_labels[field].grid(row=i, column=1, sticky=tk.W, padx=10, pady=2)
        
        # 폴더 정보 표시
        self.folder_info_label = ttk.Label(info_frame, text="")
        self.folder_info_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # 출력 설정 프레임
        output_frame = ttk.LabelFrame(main_frame, text="출력 설정", padding="10")
        output_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # 출력 형식 선택
        ttk.Label(output_frame, text="출력 형식:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.output_format = tk.StringVar(value="PNG")
        format_frame = ttk.Frame(output_frame)
        format_frame.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Radiobutton(format_frame, text="PNG", variable=self.output_format, 
                       value="PNG").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="JPEG", variable=self.output_format, 
                       value="JPEG").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="WebP", variable=self.output_format, 
                       value="WebP").pack(side=tk.LEFT, padx=5)
        
        # 품질 설정 (JPEG/WebP용)
        ttk.Label(output_frame, text="품질 (JPEG/WebP):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.IntVar(value=85)
        quality_frame = ttk.Frame(output_frame)
        quality_frame.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Scale(quality_frame, from_=10, to=100, orient=tk.HORIZONTAL, 
                 variable=self.quality_var, length=200).pack(side=tk.LEFT)
        ttk.Label(quality_frame, textvariable=self.quality_var).pack(side=tk.LEFT, padx=5)
        
        # 실행 버튼들
        button_frame2 = ttk.Frame(main_frame)
        button_frame2.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame2, text="단일 이미지 리사이즈", 
                  command=self.resize_and_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame2, text="폴더 전체 WebP 변환", 
                  command=self.convert_folder_to_webp).pack(side=tk.LEFT, padx=5)
        
        # 진행 상태 표시
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 상태 표시 레이블
        self.status_label = ttk.Label(main_frame, text="이미지 파일 또는 폴더를 선택해주세요.")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # 결과 표시 프레임
        result_frame = ttk.LabelFrame(main_frame, text="처리 결과", padding="10")
        result_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # 결과 리스트박스
        self.result_listbox = tk.Listbox(result_frame, height=8)
        self.result_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_listbox.config(yscrollcommand=scrollbar.set)
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
    
    def select_file(self):
        """이미지 파일 선택"""
        filetypes = [
            ("이미지 파일", "*.png *.jpg *.jpeg"),
            ("PNG 파일", "*.png"),
            ("JPEG 파일", "*.jpg *.jpeg"),
            ("모든 파일", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="이미지 파일 선택",
            filetypes=filetypes
        )
        
        if file_path:
            self.current_folder_path = None
            self.folder_info_label.config(text="")
            self.load_image(file_path)
    
    def select_folder(self):
        """폴더 선택"""
        folder_path = filedialog.askdirectory(
            title="이미지 폴더 선택"
        )
        
        if folder_path:
            self.current_folder_path = folder_path
            self.current_image = None
            self.current_image_path = None
            
            # 폴더 내 이미지 파일 개수 확인
            image_files = self.get_image_files(folder_path)
            
            # 이미지 정보 초기화
            for field in self.info_labels:
                self.info_labels[field].config(text="폴더 모드")
            
            # 폴더 정보 표시
            folder_name = os.path.basename(folder_path)
            self.folder_info_label.config(
                text=f"선택된 폴더: {folder_name} (이미지 파일: {len(image_files)}개)"
            )
            
            self.status_label.config(text=f"폴더가 선택되었습니다: {len(image_files)}개의 이미지 파일 발견")
    
    def get_image_files(self, folder_path):
        """폴더 내 이미지 파일 목록 가져오기"""
        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(folder_path, ext)))
        
        return image_files
    
    def load_image(self, file_path):
        """이미지 로드 및 정보 표시"""
        try:
            # 이미지 로드
            image = Image.open(file_path)
            self.current_image = image
            self.current_image_path = file_path
            
            # 파일 정보 가져오기
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # 이미지 정보 업데이트
            self.info_labels["파일명"].config(text=file_name)
            self.info_labels["형식"].config(text=image.format)
            self.info_labels["크기"].config(text=f"{image.size[0]} × {image.size[1]} 픽셀")
            self.info_labels["해상도"].config(text=f"{image.size[0]} × {image.size[1]}")
            self.info_labels["파일 크기"].config(text=f"{file_size_mb:.2f} MB ({file_size:,} bytes)")
            
            self.status_label.config(text="이미지가 성공적으로 로드되었습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"이미지를 로드할 수 없습니다:\n{str(e)}")
            self.status_label.config(text="이미지 로드 실패")
    
    def calculate_new_size(self, original_size, target_size_kb=300):
        """목표 파일 크기에 맞는 새로운 이미지 크기 계산"""
        width, height = original_size
        
        # 현재 이미지의 픽셀 수
        current_pixels = width * height
        
        # 목표 크기 (KB)를 바이트로 변환
        target_size_bytes = target_size_kb * 1024
        
        # 추정 압축률을 기반으로 필요한 픽셀 수 계산
        # 이 값은 경험적으로 조정된 값입니다
        if self.output_format.get() == "JPEG":
            compression_ratio = 0.1  # JPEG의 경우
        elif self.output_format.get() == "WebP":
            compression_ratio = 0.08  # WebP의 경우
        else:  # PNG
            compression_ratio = 0.3  # PNG의 경우 (무손실)
        
        target_pixels = target_size_bytes / (3 * compression_ratio)  # RGB 3바이트 가정
        
        if target_pixels >= current_pixels:
            return original_size  # 리사이즈 불필요
        
        # 비율 유지하면서 크기 조정
        ratio = math.sqrt(target_pixels / current_pixels)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        return (new_width, new_height)
    
    def generate_output_filename(self, input_path, output_format):
        """출력 파일명 자동 생성 (기존이름+resize)"""
        # 파일명과 확장자 분리
        file_name = os.path.basename(input_path)
        name_without_ext = os.path.splitext(file_name)[0]
        
        # 출력 형식에 따른 확장자 설정
        if output_format == "JPEG":
            ext = ".jpg"
        elif output_format == "WebP":
            ext = ".webp"
        else:  # PNG
            ext = ".png"
        
        # 새 파일명 생성
        new_filename = f"{name_without_ext}_resize{ext}"
        
        # 입력 파일과 같은 디렉토리에 저장
        output_path = os.path.join(os.path.dirname(input_path), new_filename)
        
        return output_path
    
    def resize_and_save(self):
        """단일 이미지 리사이즈 및 저장"""
        if self.current_image is None:
            messagebox.showwarning("경고", "먼저 이미지를 선택해주세요.")
            return
        
        try:
            # 자동 파일명 생성
            save_path = self.generate_output_filename(self.current_image_path, self.output_format.get())
            
            # 진행 상태 표시 시작
            self.progress.config(mode='indeterminate')
            self.progress.start()
            self.status_label.config(text="이미지 처리 중...")
            self.root.update()
            
            # 목표 크기 계산
            new_size = self.calculate_new_size(self.current_image.size)
            
            # 이미지 리사이즈
            resized_image = self.current_image.resize(new_size, Image.Resampling.LANCZOS)
            
            # 저장 옵션 설정
            save_kwargs = {}
            if self.output_format.get() in ["JPEG", "WebP"]:
                save_kwargs['quality'] = self.quality_var.get()
                save_kwargs['optimize'] = True
            
            if self.output_format.get() == "JPEG":
                # JPEG는 투명도를 지원하지 않으므로 RGB로 변환
                if resized_image.mode in ("RGBA", "P"):
                    background = Image.new("RGB", resized_image.size, (255, 255, 255))
                    background.paste(resized_image, mask=resized_image.split()[-1] if resized_image.mode == "RGBA" else None)
                    resized_image = background
            
            # 이미지 저장
            resized_image.save(save_path, format=self.output_format.get(), **save_kwargs)
            
            # 저장된 파일 크기 확인
            saved_size = os.path.getsize(save_path)
            saved_size_kb = saved_size / 1024
            
            # 300KB 초과 시 추가 리사이즈
            max_attempts = 5
            attempt = 0
            while saved_size_kb > 300 and attempt < max_attempts:
                attempt += 1
                # 크기를 더 줄임
                reduction_factor = math.sqrt(300 / saved_size_kb)
                new_width = int(new_size[0] * reduction_factor)
                new_height = int(new_size[1] * reduction_factor)
                new_size = (new_width, new_height)
                
                resized_image = self.current_image.resize(new_size, Image.Resampling.LANCZOS)
                
                if self.output_format.get() == "JPEG":
                    if resized_image.mode in ("RGBA", "P"):
                        background = Image.new("RGB", resized_image.size, (255, 255, 255))
                        background.paste(resized_image, mask=resized_image.split()[-1] if resized_image.mode == "RGBA" else None)
                        resized_image = background
                
                resized_image.save(save_path, format=self.output_format.get(), **save_kwargs)
                saved_size = os.path.getsize(save_path)
                saved_size_kb = saved_size / 1024
            
            # 진행 상태 표시 중지
            self.progress.stop()
            self.progress.config(mode='determinate')
            
            # 결과 메시지 표시
            message = f"이미지가 성공적으로 저장되었습니다!\n\n"
            message += f"저장 경로: {save_path}\n"
            message += f"새 크기: {new_size[0]} × {new_size[1]} 픽셀\n"
            message += f"파일 크기: {saved_size_kb:.2f} KB"
            
            if saved_size_kb > 300:
                message += f"\n\n경고: 파일 크기가 300KB를 초과합니다."
            
            messagebox.showinfo("완료", message)
            self.status_label.config(text="이미지 저장 완료")
            
            # 결과 리스트에 추가
            self.result_listbox.insert(tk.END, f"✓ {os.path.basename(save_path)} ({saved_size_kb:.1f}KB)")
            
        except Exception as e:
            self.progress.stop()
            self.progress.config(mode='determinate')
            messagebox.showerror("오류", f"이미지 저장 중 오류가 발생했습니다:\n{str(e)}")
            self.status_label.config(text="이미지 저장 실패")
    
    def convert_folder_to_webp(self):
        """폴더 내 모든 이미지를 WebP로 변환"""
        if self.current_folder_path is None:
            messagebox.showwarning("경고", "먼저 폴더를 선택해주세요.")
            return
        
        # 이미지 파일 목록 가져오기
        image_files = self.get_image_files(self.current_folder_path)
        
        if not image_files:
            messagebox.showwarning("경고", "선택한 폴더에 이미지 파일이 없습니다.")
            return
        
        # 출력 폴더 생성
        folder_name = os.path.basename(self.current_folder_path)
        output_folder = os.path.join(os.path.dirname(self.current_folder_path), f"{folder_name}_webp")
        
        try:
            # 출력 폴더가 있으면 삭제 후 재생성
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
            os.makedirs(output_folder)
            
            # 진행 상태 설정
            self.progress.config(mode='determinate', maximum=len(image_files))
            self.progress['value'] = 0
            
            # 결과 리스트 초기화
            self.result_listbox.delete(0, tk.END)
            
            success_count = 0
            error_count = 0
            
            for i, image_file in enumerate(image_files):
                try:
                    # 상태 업데이트
                    self.status_label.config(text=f"처리 중... ({i+1}/{len(image_files)})")
                    self.root.update()
                    
                    # 이미지 로드
                    image = Image.open(image_file)
                    
                    # 출력 파일명 생성
                    file_name = os.path.basename(image_file)
                    name_without_ext = os.path.splitext(file_name)[0]
                    output_file = os.path.join(output_folder, f"{name_without_ext}.webp")
                    
                    # WebP로 변환하여 저장
                    save_kwargs = {
                        'quality': self.quality_var.get(),
                        'optimize': True
                    }
                    
                    image.save(output_file, format='WebP', **save_kwargs)
                    
                    # 파일 크기 확인
                    output_size = os.path.getsize(output_file)
                    output_size_kb = output_size / 1024
                    
                    success_count += 1
                    self.result_listbox.insert(tk.END, f"✓ {name_without_ext}.webp ({output_size_kb:.1f}KB)")
                    
                except Exception as e:
                    error_count += 1
                    self.result_listbox.insert(tk.END, f"✗ {os.path.basename(image_file)} - 오류: {str(e)}")
                
                # 진행률 업데이트
                self.progress['value'] = i + 1
                self.root.update()
            
            # 완료 메시지
            message = f"폴더 변환이 완료되었습니다!\n\n"
            message += f"출력 폴더: {output_folder}\n"
            message += f"성공: {success_count}개\n"
            message += f"실패: {error_count}개"
            
            messagebox.showinfo("완료", message)
            self.status_label.config(text=f"폴더 변환 완료: {success_count}개 성공, {error_count}개 실패")
            
        except Exception as e:
            messagebox.showerror("오류", f"폴더 변환 중 오류가 발생했습니다:\n{str(e)}")
            self.status_label.config(text="폴더 변환 실패")
        
        finally:
            self.progress['value'] = 0

def main():
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 