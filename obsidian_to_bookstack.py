#!/usr/bin/env python3
"""
Obsidian to BookStack Transfer Tool (Versión con configuración)

Este script transfiere contenido de una bóveda de Obsidian a una instancia de BookStack
a través de su API, usando un archivo de configuración JSON.

Autor: Miguel Navarro
Fecha: 2025
"""

import os
import json
import requests
import argparse
import re
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin
try:
    import frontmatter
except ImportError:
    frontmatter = None


class BookStackAPI:
    """Cliente para interactuar con la API de BookStack"""
    
    def __init__(self, base_url: str, token_id: str, token_secret: str):
        self.base_url = base_url.rstrip('/')
        self.api_url = urljoin(self.base_url, '/api/')
        self.headers = {
            'Authorization': f'Token {token_id}:{token_secret}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self, verbose: bool = False) -> bool:
        """Prueba la conexión con BookStack"""
        try:
            response = requests.get(f"{self.api_url}books", headers=self.headers, timeout=10)
            if verbose:
                return self._detailed_connection_test()
            return response.status_code == 200
        except Exception as e:
            if verbose:
                print(f"Error conectando con BookStack: {e}")
            return False
    
    def _detailed_connection_test(self) -> bool:
        """Realiza una prueba detallada de conexión con diagnósticos"""
        print(f"Probando conexión con: {self.base_url}")
        print(f"API URL: {self.api_url}")
        print("="*50)
        
        try:
            # Probar conexión básica
            print("1. Probando conexión básica...")
            response = requests.get(f"{self.api_url}books", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print("   ✅ Conexión exitosa")
            elif response.status_code == 401:
                print("   ❌ Error de autenticación - Verifica tus tokens")
                return False
            elif response.status_code == 403:
                print("   ❌ Sin permisos - Tu usuario no tiene acceso a la API")
                return False
            else:
                print(f"   ❌ Error HTTP {response.status_code}: {response.text}")
                return False
            
            # Obtener información de libros
            print("\n2. Obteniendo información de libros...")
            books_data = response.json()
            books = books_data.get('data', [])
            print(f"   📚 Libros existentes: {len(books)}")
            
            if books:
                print("   Primeros 5 libros:")
                for book in books[:5]:
                    print(f"     - {book.get('name', 'Sin nombre')} (ID: {book.get('id')})")
            
            # Probar creación de libro (simulado)
            print("\n3. Probando permisos de creación...")
            test_data = {
                'name': 'TEST_CONNECTION_BOOK_DELETE_ME',
                'description': 'Libro de prueba - puedes eliminarlo'
            }
            
            create_response = requests.post(f"{self.api_url}books", 
                                          headers=self.headers, 
                                          json=test_data,
                                          timeout=10)
            
            if create_response.status_code == 200:
                print("   ✅ Permisos de creación confirmados")
                
                # Intentar eliminar el libro de prueba
                test_book = create_response.json()
                book_id = test_book.get('id')
                if book_id:
                    delete_response = requests.delete(f"{self.api_url}books/{book_id}", 
                                                     headers=self.headers,
                                                     timeout=10)
                    if delete_response.status_code == 204:
                        print("   🗑️  Libro de prueba eliminado correctamente")
                    else:
                        print(f"   ⚠️  Libro de prueba creado pero no se pudo eliminar (ID: {book_id})")
                        print(f"      Puedes eliminarlo manualmente desde BookStack")
            else:
                print(f"   ❌ Sin permisos de creación: {create_response.status_code}")
                print(f"      {create_response.text}")
                return False
            
            # Probar creación de páginas
            print("\n4. Verificando API de páginas...")
            pages_response = requests.get(f"{self.api_url}pages", headers=self.headers, timeout=10)
            if pages_response.status_code == 200:
                pages_data = pages_response.json()
                pages = pages_data.get('data', [])
                print(f"   📄 Páginas existentes: {len(pages)}")
                print("   ✅ API de páginas accesible")
            else:
                print(f"   ❌ Error accediendo a páginas: {pages_response.status_code}")
            
            # Probar creación de capítulos
            print("\n5. Verificando API de capítulos...")
            chapters_response = requests.get(f"{self.api_url}chapters", headers=self.headers, timeout=10)
            if chapters_response.status_code == 200:
                chapters_data = chapters_response.json()
                chapters = chapters_data.get('data', [])
                print(f"   📖 Capítulos existentes: {len(chapters)}")
                print("   ✅ API de capítulos accesible")
            else:
                print(f"   ❌ Error accediendo a capítulos: {chapters_response.status_code}")
            
            print("\n" + "="*50)
            print("🎉 ¡Conexión exitosa! Tu configuración está lista para la transferencia.")
            return True
            
        except requests.exceptions.Timeout:
            print("   ❌ Timeout - El servidor no responde")
            return False
        except requests.exceptions.ConnectionError:
            print("   ❌ Error de conexión - Verifica la URL")
            return False
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error de request: {e}")
            return False
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
            return False
    
    def get_books(self) -> List[Dict]:
        """Obtiene la lista de libros existentes"""
        try:
            response = requests.get(f"{self.api_url}books", headers=self.headers)
            if response.status_code == 200:
                return response.json().get('data', [])
            return []
        except Exception as e:
            print(f"Error obteniendo libros: {e}")
            return []
    
    def create_book(self, name: str, description: str = "") -> Optional[Dict]:
        """Crea un nuevo libro en BookStack"""
        data = {
            'name': name,
            'description': description
        }
        try:
            response = requests.post(f"{self.api_url}books", 
                                   headers=self.headers, 
                                   json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creando libro: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en create_book: {e}")
            return None
    
    def create_chapter(self, book_id: int, name: str, description: str = "") -> Optional[Dict]:
        """Crea un nuevo capítulo en un libro"""
        data = {
            'book_id': book_id,
            'name': name,
            'description': description
        }
        try:
            response = requests.post(f"{self.api_url}chapters", 
                                   headers=self.headers, 
                                   json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creando capítulo: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en create_chapter: {e}")
            return None
    
    def create_page(self, book_id: int, name: str, markdown_content: str, 
                   chapter_id: Optional[int] = None) -> Optional[Dict]:
        """Crea una nueva página en BookStack"""
        data = {
            'book_id': book_id,
            'name': name,
            'markdown': markdown_content
        }
        if chapter_id:
            data['chapter_id'] = chapter_id
        
        try:
            response = requests.post(f"{self.api_url}pages", 
                                   headers=self.headers, 
                                   json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creando página: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en create_page: {e}")
            return None
    
    def get_shelves(self) -> List[Dict]:
        """Obtiene la lista de estantes existentes"""
        try:
            response = requests.get(f"{self.api_url}shelves", headers=self.headers)
            if response.status_code == 200:
                return response.json().get('data', [])
            return []
        except Exception as e:
            print(f"Error obteniendo estantes: {e}")
            return []
    
    def create_shelf(self, name: str, description: str = "") -> Optional[Dict]:
        """Crea un nuevo estante en BookStack"""
        data = {
            'name': name,
            'description': description
        }
        try:
            response = requests.post(f"{self.api_url}shelves", 
                                   headers=self.headers, 
                                   json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creando estante: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en create_shelf: {e}")
            return None
    
    def update_shelf(self, shelf_id: int, name: str = None, description: str = None, 
                    book_ids: List[int] = None) -> Optional[Dict]:
        """Actualiza un estante existente, incluyendo la asignación de libros"""
        data = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        if book_ids is not None:
            data['books'] = book_ids
        
        try:
            response = requests.put(f"{self.api_url}shelves/{shelf_id}", 
                                  headers=self.headers, 
                                  json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error actualizando estante: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en update_shelf: {e}")
            return None
    
    def upload_image(self, image_path: Path, page_id: int, name: str = None) -> Optional[Dict]:
        """Sube una imagen a BookStack y la asocia a una página"""
        try:
            if not image_path.exists():
                print(f"Archivo de imagen no encontrado: {image_path}")
                return None
            
            # Preparar headers sin Content-Type para multipart/form-data
            headers = {
                'Authorization': f'Token {self.headers["Authorization"].split(" ")[1]}'
            }
            
            # Preparar datos del formulario
            files = {
                'image': (image_path.name, open(image_path, 'rb'), f'image/{image_path.suffix[1:]}'),
                'name': (None, name or image_path.stem),
                'type': (None, 'gallery'),
                'uploaded_to': (None, str(page_id))
            }
            
            response = requests.post(
                f"{self.api_url}image-gallery",
                headers=headers,
                files=files
            )
            
            # Cerrar el archivo
            files['image'][1].close()
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error subiendo imagen {image_path.name}: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error subiendo imagen {image_path}: {e}")
            return None
    
    def upload_attachment(self, file_path: Path, page_id: int, name: str = None) -> Optional[Dict]:
        """Sube un adjunto a BookStack usando la API específica de attachments"""
        try:
            if not file_path.exists():
                print(f"Archivo adjunto no encontrado: {file_path}")
                return None
            
            # Preparar headers sin Content-Type para multipart/form-data
            headers = {
                'Authorization': f'Token {self.headers["Authorization"].split(" ")[1]}'
            }
            
            # Preparar datos del formulario para attachments
            with open(file_path, 'rb') as file:
                files = {
                    'file': (file_path.name, file, 'application/octet-stream')
                }
                data = {
                    'name': name or file_path.stem,
                    'uploaded_to': str(page_id)
                }
                
                response = requests.post(
                    f"{self.api_url}attachments",
                    headers=headers,
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error subiendo adjunto {file_path.name}: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error subiendo adjunto {file_path}: {e}")
            return None


class ObsidianParser:
    """Parser para archivos de Obsidian"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(f"La ruta de la bóveda no existe: {vault_path}")
    
    def get_folder_structure(self) -> Dict[str, List[Path]]:
        """Obtiene la estructura de carpetas con archivos markdown"""
        structure = {}
        
        for md_file in self.vault_path.rglob("*.md"):
            relative_path = md_file.relative_to(self.vault_path)
            folder = str(relative_path.parent) if relative_path.parent != Path('.') else 'root'
            
            if folder not in structure:
                structure[folder] = []
            structure[folder].append(md_file)
        
        return structure
    
    def get_hierarchical_structure(self) -> Dict[str, Dict[str, List[Path]]]:
        """Obtiene estructura jerárquica: primer nivel = libros, segundo nivel = capítulos"""
        structure = {}
        
        for md_file in self.vault_path.rglob("*.md"):
            relative_path = md_file.relative_to(self.vault_path)
            path_parts = relative_path.parts[:-1]  # Excluir el nombre del archivo
            
            if len(path_parts) == 0:
                # Archivo en la raíz
                book_name = 'root'
                chapter_name = 'root'
            elif len(path_parts) == 1:
                # Archivo en carpeta de primer nivel (libro sin capítulos)
                book_name = path_parts[0]
                chapter_name = 'root'
            else:
                # Archivo en carpeta de segundo nivel o más profundo
                book_name = path_parts[0]
                chapter_name = '/'.join(path_parts[1:])
            
            if book_name not in structure:
                structure[book_name] = {}
            if chapter_name not in structure[book_name]:
                structure[book_name][chapter_name] = []
            
            structure[book_name][chapter_name].append(md_file)
        
        return structure
    
    def get_markdown_files(self) -> List[Path]:
        """Obtiene todos los archivos markdown de la bóveda"""
        return list(self.vault_path.rglob("*.md"))
    

    
    def find_images_in_content(self, content: str, file_path: Path) -> List[Tuple[str, Path]]:
        """Encuentra todas las referencias a imágenes en el contenido markdown"""
        images = []
        
        # Patrones para encontrar imágenes en markdown
        # ![alt text](path/to/image.png)
        markdown_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        # [[image.png]]
        obsidian_pattern = r'!?\[\[([^\]]+\.(png|jpg|jpeg|gif|svg|webp))\]\]'
        
        # Buscar imágenes con sintaxis markdown
        for match in re.finditer(markdown_pattern, content, re.IGNORECASE):
            alt_text = match.group(1)
            image_path_str = match.group(2)
            
            # Resolver ruta de imagen relativa al archivo actual
            if not image_path_str.startswith(('http://', 'https://')):
                image_path = self._resolve_image_path(image_path_str, file_path)
                if image_path:
                    images.append((match.group(0), image_path))
        
        # Buscar imágenes con sintaxis Obsidian
        for match in re.finditer(obsidian_pattern, content, re.IGNORECASE):
            image_name = match.group(1)
            image_path = self._find_image_in_vault(image_name)
            if image_path:
                images.append((match.group(0), image_path))
        
        return images
    
    def find_attachments_in_content(self, content: str, file_path: Path) -> List[Tuple[str, Path]]:
        """Encuentra todas las referencias a adjuntos (archivos no imagen) en el contenido markdown"""
        attachments = []
        
        # Extensiones de archivos que se consideran adjuntos (no imágenes)
        attachment_extensions = {
            'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
            'txt', 'rtf', 'odt', 'ods', 'odp',
            'zip', 'rar', '7z', 'tar', 'gz',
            'mp3', 'wav', 'mp4', 'avi', 'mov', 'mkv',
            'csv', 'json', 'xml', 'yaml', 'yml',
            'py', 'js', 'html', 'css', 'sql'
        }
        
        # Patrón para enlaces markdown: [texto](archivo.ext)
        markdown_pattern = r'\[([^\]]*)\]\(([^\)]+\.(\w+))\)'
        # Patrón para enlaces Obsidian: [[archivo.ext]] o ![[archivo.ext]]
        obsidian_pattern = r'!?\[\[([^\]]+\.(\w+))\]\]'
        
        # Buscar adjuntos con sintaxis markdown
        for match in re.finditer(markdown_pattern, content, re.IGNORECASE):
            link_text = match.group(1)
            file_path_str = match.group(2)
            file_extension = match.group(3).lower()
            
            # Solo procesar si es una extensión de adjunto
            if file_extension in attachment_extensions:
                # Resolver ruta relativa al archivo actual
                if not file_path_str.startswith(('http://', 'https://')):
                    attachment_path = self._resolve_attachment_path(file_path_str, file_path)
                    if attachment_path:
                        attachments.append((match.group(0), attachment_path))
        
        # Buscar adjuntos con sintaxis Obsidian
        for match in re.finditer(obsidian_pattern, content, re.IGNORECASE):
            file_name = match.group(1)
            file_extension = match.group(2).lower()
            
            # Solo procesar si es una extensión de adjunto
            if file_extension in attachment_extensions:
                attachment_path = self._find_attachment_in_vault(file_name)
                if attachment_path:
                    attachments.append((match.group(0), attachment_path))
        
        return attachments
    
    def _resolve_image_path(self, image_path_str: str, file_path: Path) -> Optional[Path]:
        """Resuelve la ruta de una imagen relativa al archivo actual"""
        try:
            # Intentar ruta relativa al archivo
            relative_path = file_path.parent / image_path_str
            if relative_path.exists():
                return relative_path
            
            # Intentar ruta relativa al vault
            vault_relative_path = self.vault_path / image_path_str
            if vault_relative_path.exists():
                return vault_relative_path
            
            return None
        except Exception:
            return None
    
    def _find_image_in_vault(self, image_name: str) -> Optional[Path]:
        """Busca una imagen por nombre en todo el vault"""
        try:
            # Buscar en todo el vault
            for image_path in self.vault_path.rglob(image_name):
                if image_path.is_file():
                    return image_path
            return None
        except Exception:
            return None
    
    def _resolve_attachment_path(self, attachment_path_str: str, file_path: Path) -> Optional[Path]:
        """Resuelve la ruta de un adjunto relativa al archivo actual"""
        try:
            # Intentar ruta relativa al archivo
            relative_path = file_path.parent / attachment_path_str
            if relative_path.exists():
                return relative_path
            
            # Intentar ruta relativa al vault
            vault_relative_path = self.vault_path / attachment_path_str
            if vault_relative_path.exists():
                return vault_relative_path
            
            return None
        except Exception:
            return None
    
    def _find_attachment_in_vault(self, attachment_name: str) -> Optional[Path]:
        """Busca un adjunto por nombre en todo el vault"""
        try:
            # Buscar en todo el vault
            for attachment_path in self.vault_path.rglob(attachment_name):
                if attachment_path.is_file():
                    return attachment_path
            return None
        except Exception:
            return None
    
    def read_file(self, file_path: Path) -> Optional[Dict[str, str]]:
        """Lee un archivo markdown y extrae metadatos"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Usar python-frontmatter si está disponible
            if frontmatter:
                post = frontmatter.loads(content)
                title = post.metadata.get('title', file_path.stem)
                content = post.content
                metadata = post.metadata
            else:
                # Extraer frontmatter manualmente
                metadata = {}
                title = file_path.stem
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()
                        # Extraer título del frontmatter si existe
                        frontmatter_lines = parts[1].strip().split('\n')
                        for line in frontmatter_lines:
                            if line.strip().startswith('title:'):
                                title = line.split(':', 1)[1].strip().strip('"\'')
            
            # Encontrar imágenes y adjuntos en el contenido
            images = self.find_images_in_content(content, file_path)
            attachments = self.find_attachments_in_content(content, file_path)
            
            return {
                'title': title,
                'content': content,
                'markdown_content': content,
                'relative_path': str(file_path.relative_to(self.vault_path)),
                'metadata': metadata,
                'folder': str(file_path.parent.relative_to(self.vault_path)) if file_path.parent != self.vault_path else 'root',
                'images': images,
                'attachments': attachments
            }
        except Exception as e:
            print(f"Error leyendo archivo {file_path}: {e}")
            return None


class ObsidianToBookStackTransfer:
    """Clase principal para la transferencia"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.parser = ObsidianParser(config['obsidian']['vault_path'])
        self.bookstack = BookStackAPI(
            config['bookstack']['url'],
            config['bookstack']['token_id'],
            config['bookstack']['token_secret']
        )
        self.books = {}  # book_name -> book_id
        self.chapters = {}  # (book_id, chapter_name) -> chapter_id
        self.created_book_ids = []  # Lista de IDs de libros creados
        
        # Estadísticas de transferencia
        self.stats = {
            'images_uploaded': 0,
            'images_failed': 0,
            'attachments_uploaded': 0,
            'attachments_failed': 0,
            'pages_created': 0,
            'pages_failed': 0,
            'errors': []  # Lista de errores detallados
        }
    
    def _print_success(self, message: str):
        """Imprime mensaje de éxito en verde"""
        print(f"\033[92m{message}\033[0m")
    
    def _print_error(self, message: str):
        """Imprime mensaje de error en rojo"""
        print(f"\033[91m{message}\033[0m")
    
    def _print_warning(self, message: str):
        """Imprime mensaje de advertencia en amarillo"""
        print(f"\033[93m{message}\033[0m")
    
    def _add_error(self, error_type: str, item: str, error_msg: str):
        """Agrega un error a las estadísticas"""
        self.stats['errors'].append({
            'type': error_type,
            'item': item,
            'error': error_msg
        })
    
    def transfer(self) -> bool:
        """Ejecuta la transferencia completa"""
        print("Iniciando transferencia de Obsidian a BookStack...")
        
        # Probar conexión
        if not self.bookstack.test_connection():
            print("No se pudo conectar con BookStack")
            return False
        
        print("Conexión con BookStack exitosa")
        
        # Obtener estructura jerárquica
        hierarchical_structure = self.parser.get_hierarchical_structure()
        print(f"Encontrados {len(hierarchical_structure)} libros")
        
        success_count = 0
        total_files = sum(len(files) for book_chapters in hierarchical_structure.values() 
                         for files in book_chapters.values())
        
        # Procesar cada libro (carpeta de primer nivel)
        for book_name, chapters in hierarchical_structure.items():
            # Crear libro
            display_book_name = book_name if book_name != 'root' else 'Archivos Raíz'
            book = self.bookstack.create_book(
                display_book_name,
                f"Contenido transferido desde Obsidian - Carpeta: {book_name}"
            )
            
            if not book:
                print(f"✗ Error creando libro: {display_book_name}")
                continue
            
            book_id = book['id']
            self.books[book_name] = book_id
            self.created_book_ids.append(book_id)
            print(f"Libro creado: {display_book_name} (ID: {book_id})")
            
            # Procesar capítulos dentro del libro
            for chapter_name, files in chapters.items():
                chapter_id = None
                
                # Crear capítulo si no es 'root'
                if chapter_name != 'root':
                    display_chapter_name = chapter_name.replace('/', ' - ')
                    chapter = self.bookstack.create_chapter(
                        book_id,
                        display_chapter_name,
                        f"Capítulo para carpeta: {chapter_name}"
                    )
                    
                    if chapter:
                        chapter_id = chapter['id']
                        self.chapters[(book_id, chapter_name)] = chapter_id
                        print(f"  Capítulo creado: {display_chapter_name} (ID: {chapter_id})")
                    else:
                        print(f"  ✗ Error creando capítulo: {display_chapter_name}")
                        continue
                
                # Transferir archivos como páginas
                for md_file in files:
                    file_data = self.parser.read_file(md_file)
                    if file_data:
                        # Crear la página primero
                        page = self.bookstack.create_page(
                            book_id,
                            file_data['title'],
                            file_data['markdown_content'],
                            chapter_id
                        )
                        if page:
                            page_id = page['id']
                            
                            # Procesar imágenes y adjuntos si los hay
                            updated_content = file_data['markdown_content']
                            
                            # Procesar imágenes
                            if file_data.get('images'):
                                updated_content = self._process_images(
                                    file_data['images'], 
                                    updated_content, 
                                    page_id
                                )
                            
                            # Procesar adjuntos
                            if file_data.get('attachments'):
                                updated_content = self._process_attachments(
                                    file_data['attachments'], 
                                    updated_content, 
                                    page_id
                                )
                            
                            # Actualizar la página con el contenido modificado si cambió
                            if updated_content != file_data['markdown_content']:
                                self._update_page_content(page_id, updated_content)
                            
                            location = f"{display_book_name}"
                            if chapter_id:
                                location += f" → {display_chapter_name}"
                            
                            image_count = len(file_data.get('images', []))
                            attachment_count = len(file_data.get('attachments', []))
                            media_info = ""
                            if image_count > 0 or attachment_count > 0:
                                parts = []
                                if image_count > 0:
                                    parts.append(f"{image_count} imágenes")
                                if attachment_count > 0:
                                    parts.append(f"{attachment_count} adjuntos")
                                media_info = f" ({', '.join(parts)})"
                            
                            self._print_success(f"    ✓ Transferido: {file_data['title']} → {location}{media_info}")
                            self.stats['pages_created'] += 1
                            success_count += 1
                        else:
                            error_msg = f"Error transferiendo: {file_data['title']}"
                            self._print_error(f"    ✗ {error_msg}")
                            self._add_error('página', file_data['title'], error_msg)
                            self.stats['pages_failed'] += 1
        
        # Crear estante principal si se crearon libros
        if self.created_book_ids:
            shelf_name = self.config.get('transfer', {}).get('shelf_name', 'Contenido de Obsidian')
            shelf_description = f"Estante principal con {len(self.created_book_ids)} libros transferidos desde Obsidian"
            
            print(f"\nCreando estante principal: {shelf_name}")
            shelf = self.bookstack.create_shelf(shelf_name, shelf_description)
            
            if shelf:
                shelf_id = shelf['id']
                print(f"Estante creado: {shelf_name} (ID: {shelf_id})")
                
                # Agregar todos los libros al estante
                updated_shelf = self.bookstack.update_shelf(
                    shelf_id, 
                    book_ids=self.created_book_ids
                )
                
                if updated_shelf:
                    print(f"✓ {len(self.created_book_ids)} libros agregados al estante")
                else:
                    print("✗ Error agregando libros al estante")
            else:
                print("✗ Error creando estante principal")
        
        # Mostrar resumen final con estadísticas detalladas
        print("\n" + "="*60)
        print("RESUMEN DE TRANSFERENCIA")
        print("="*60)
        
        # Estadísticas de páginas
        print(f"📄 Páginas: {self.stats['pages_created']} creadas, {self.stats['pages_failed']} fallidas")
        
        # Estadísticas de imágenes
        total_images = self.stats['images_uploaded'] + self.stats['images_failed']
        if total_images > 0:
            print(f"🖼️  Imágenes: {self.stats['images_uploaded']} subidas, {self.stats['images_failed']} fallidas")
        
        # Estadísticas de adjuntos
        total_attachments = self.stats['attachments_uploaded'] + self.stats['attachments_failed']
        if total_attachments > 0:
            print(f"📎 Adjuntos: {self.stats['attachments_uploaded']} subidos, {self.stats['attachments_failed']} fallidos")
        
        print(f"📚 Libros creados: {len(self.created_book_ids)}")
        
        # Mostrar errores si los hay
        if self.stats['errors']:
            print(f"\n⚠️  ERRORES ENCONTRADOS ({len(self.stats['errors'])}):")            
            for error in self.stats['errors']:
                self._print_error(f"   • {error['type'].title()}: {error['item']} - {error['error']}")
        else:
            self._print_success("\n✅ Transferencia completada sin errores")
        
        print("="*60)
        return success_count > 0
    
    def _process_images(self, images: List[Tuple[str, Path]], content: str, page_id: int) -> str:
        """Procesa las imágenes encontradas en el contenido y las sube a BookStack"""
        updated_content = content
        
        for original_ref, image_path in images:
            try:
                # Subir imagen a BookStack
                uploaded_image = self.bookstack.upload_image(image_path, page_id)
                
                if uploaded_image:
                    # Obtener la URL de la imagen subida
                    image_url = uploaded_image.get('url', '')
                    
                    if image_url:
                        # Extraer alt text si existe
                        alt_text = self._extract_alt_text(original_ref)
                        
                        # Crear nueva referencia markdown
                        new_ref = f"![{alt_text}]({image_url})"
                        
                        # Reemplazar la referencia original
                        updated_content = updated_content.replace(original_ref, new_ref)
                        
                        self._print_success(f"      ✓ Imagen subida: {image_path.name} → {image_url}")
                        self.stats['images_uploaded'] += 1
                    else:
                        error_msg = f"No se obtuvo URL para {image_path.name}"
                        self._print_error(f"      ✗ Error: {error_msg}")
                        self._add_error('imagen', str(image_path.name), error_msg)
                        self.stats['images_failed'] += 1
                else:
                    error_msg = f"Error subiendo imagen: {image_path.name}"
                    self._print_error(f"      ✗ {error_msg}")
                    self._add_error('imagen', str(image_path.name), error_msg)
                    self.stats['images_failed'] += 1
                    
            except Exception as e:
                error_msg = f"Error procesando imagen {image_path}: {e}"
                self._print_error(f"      ✗ {error_msg}")
                self._add_error('imagen', str(image_path.name), str(e))
                self.stats['images_failed'] += 1
        
        return updated_content
    
    def _process_attachments(self, attachments: List[Tuple[str, Path]], content: str, page_id: int) -> str:
        """Procesa los adjuntos encontrados en el contenido y los sube a BookStack"""
        updated_content = content
        
        for original_ref, attachment_path in attachments:
            try:
                # Subir adjunto a BookStack
                uploaded_attachment = self.bookstack.upload_attachment(attachment_path, page_id)
                
                if uploaded_attachment:
                    # Construir la URL del adjunto usando el ID devuelto
                    attachment_id = uploaded_attachment.get('id')
                    
                    if attachment_id:
                        # Construir URL del adjunto
                        base_url = self.config['bookstack']['url'].rstrip('/')
                        attachment_url = f"{base_url}/attachments/{attachment_id}"
                        
                        # Extraer texto del enlace si existe
                        link_text = self._extract_link_text(original_ref)
                        
                        # Crear nueva referencia markdown
                        new_ref = f"[{link_text}]({attachment_url})"
                        
                        # Reemplazar la referencia original
                        updated_content = updated_content.replace(original_ref, new_ref)
                        
                        self._print_success(f"      ✓ Adjunto subido: {attachment_path.name} → {attachment_url}")
                        self.stats['attachments_uploaded'] += 1
                    else:
                        error_msg = f"No se obtuvo ID para {attachment_path.name}"
                        self._print_error(f"      ✗ Error: {error_msg}")
                        self._add_error('adjunto', str(attachment_path.name), error_msg)
                        self.stats['attachments_failed'] += 1
                else:
                    error_msg = f"Error subiendo adjunto: {attachment_path.name}"
                    self._print_error(f"      ✗ {error_msg}")
                    self._add_error('adjunto', str(attachment_path.name), error_msg)
                    self.stats['attachments_failed'] += 1
                    
            except Exception as e:
                error_msg = f"Error procesando adjunto {attachment_path}: {e}"
                self._print_error(f"      ✗ {error_msg}")
                self._add_error('adjunto', str(attachment_path.name), str(e))
                self.stats['attachments_failed'] += 1
        
        return updated_content
    
    def _extract_alt_text(self, image_ref: str) -> str:
        """Extrae el texto alternativo de una referencia de imagen"""
        # Para sintaxis markdown ![alt](url)
        markdown_match = re.match(r'!\[([^\]]*)\]\([^\)]+\)', image_ref)
        if markdown_match:
            return markdown_match.group(1)
        
        # Para sintaxis Obsidian [[image.png]]
        obsidian_match = re.match(r'!?\[\[([^\]]+)\]\]', image_ref)
        if obsidian_match:
            # Usar el nombre del archivo sin extensión como alt text
            filename = obsidian_match.group(1)
            return Path(filename).stem
        
        return ""
    
    def _extract_link_text(self, attachment_ref: str) -> str:
        """Extrae el texto del enlace de una referencia de adjunto"""
        # Para sintaxis markdown [texto](url)
        markdown_match = re.match(r'\[([^\]]*)\]\([^\)]+\)', attachment_ref)
        if markdown_match:
            return markdown_match.group(1)
        
        # Para sintaxis Obsidian [[archivo.ext]] o ![[archivo.ext]]
        obsidian_match = re.match(r'!?\[\[([^\]]+)\]\]', attachment_ref)
        if obsidian_match:
            # Usar el nombre del archivo sin extensión como texto del enlace
            filename = obsidian_match.group(1)
            return Path(filename).stem
        
        return ""
    
    def _update_page_content(self, page_id: int, new_content: str) -> bool:
        """Actualiza el contenido de una página existente"""
        try:
            data = {
                'markdown': new_content
            }
            
            response = requests.put(
                f"{self.bookstack.api_url}pages/{page_id}",
                headers=self.bookstack.headers,
                json=data
            )
            
            if response.status_code == 200:
                print(f"      ✓ Contenido de página actualizado (ID: {page_id})")
                return True
            else:
                print(f"      ✗ Error actualizando página {page_id}: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"      ✗ Error actualizando página {page_id}: {e}")
            return False

    
    def dry_run_transfer(self) -> None:
        """Simula la transferencia sin crear contenido real"""
        print("\n=== SIMULACIÓN DE TRANSFERENCIA ===")
        print(f"Configuración cargada desde: {self.config.get('_config_file', 'archivo de configuración')}")
        print(f"Vault de Obsidian: {self.config['obsidian']['vault_path']}")
        print(f"BookStack URL: {self.config['bookstack']['url']}")
        
        # Verificar conexión
        print("\n--- Verificando conexión ---")
        if self.bookstack.test_connection():
            print("✓ Conexión con BookStack exitosa")
        else:
            print("✗ No se pudo conectar con BookStack")
            return
        
        # Analizar archivos
        print("\n--- Analizando archivos de Obsidian ---")
        try:
            hierarchical_structure = self.parser.get_hierarchical_structure()
            print(f"Encontrados {len(hierarchical_structure)} libros")
            
            total_files = sum(len(files) for book_chapters in hierarchical_structure.values() 
                             for files in book_chapters.values())
            print(f"Total de archivos markdown: {total_files}")
            
            print("\n--- Estructura que se crearía ---")
            
            book_count = 0
            chapter_count = 0
            page_count = 0
            
            for book_name, chapters in hierarchical_structure.items():
                book_count += 1
                display_book_name = book_name if book_name != 'root' else 'Archivos Raíz'
                print(f"📖 Libro: {display_book_name}")
                
                for chapter_name, files in chapters.items():
                    if chapter_name != 'root':
                        chapter_count += 1
                        display_chapter_name = chapter_name.replace('/', ' - ')
                        print(f"  📂 Capítulo: {display_chapter_name}")
                        for md_file in files:
                            file_data = self.parser.read_file(md_file)
                            if file_data:
                                page_count += 1
                                # Mostrar información sobre imágenes y adjuntos
                                image_count = len(file_data.get('images', []))
                                attachment_count = len(file_data.get('attachments', []))
                                media_info = ""
                                if image_count > 0 or attachment_count > 0:
                                    parts = []
                                    if image_count > 0:
                                        parts.append(f"{image_count} imágenes")
                                    if attachment_count > 0:
                                        parts.append(f"{attachment_count} adjuntos")
                                    media_info = f" ({', '.join(parts)})"
                                print(f"    📄 Página: {file_data['title']}{media_info}")
                                
                                # Mostrar detalles de las imágenes encontradas
                                for original_ref, image_path in file_data.get('images', []):
                                    if image_path.exists():
                                        print(f"      🖼️  {image_path.name} ✓")
                                    else:
                                        print(f"      🖼️  {image_path.name} ✗ (no encontrada)")
                                
                                # Mostrar detalles de los adjuntos encontrados
                                for original_ref, attachment_path in file_data.get('attachments', []):
                                    if attachment_path.exists():
                                        print(f"      📎 {attachment_path.name} ✓")
                                    else:
                                        print(f"      📎 {attachment_path.name} ✗ (no encontrado)")
                    else:
                        # Páginas directas en el libro (sin capítulo)
                        for md_file in files:
                            file_data = self.parser.read_file(md_file)
                            if file_data:
                                page_count += 1
                                # Mostrar información sobre imágenes y adjuntos
                                image_count = len(file_data.get('images', []))
                                attachment_count = len(file_data.get('attachments', []))
                                media_info = ""
                                if image_count > 0 or attachment_count > 0:
                                    parts = []
                                    if image_count > 0:
                                        parts.append(f"{image_count} imágenes")
                                    if attachment_count > 0:
                                        parts.append(f"{attachment_count} adjuntos")
                                    media_info = f" ({', '.join(parts)})"
                                print(f"  📄 Página: {file_data['title']}{media_info}")
                                
                                # Mostrar detalles de las imágenes encontradas
                                for original_ref, image_path in file_data.get('images', []):
                                    if image_path.exists():
                                        print(f"    🖼️  {image_path.name} ✓")
                                    else:
                                        print(f"    🖼️  {image_path.name} ✗ (no encontrada)")
                                
                                # Mostrar detalles de los adjuntos encontrados
                                for original_ref, attachment_path in file_data.get('attachments', []):
                                    if attachment_path.exists():
                                        print(f"    📎 {attachment_path.name} ✓")
                                    else:
                                        print(f"    📎 {attachment_path.name} ✗ (no encontrado)")
            
            # Contar estadísticas de medios
            total_images = 0
            total_attachments = 0
            
            for book_name, chapters in hierarchical_structure.items():
                for chapter_name, files in chapters.items():
                    for md_file in files:
                        file_data = self.parser.read_file(md_file)
                        if file_data:
                            total_images += len(file_data.get('images', []))
                            total_attachments += len(file_data.get('attachments', []))
            
            print("\n--- Resumen ---")
            shelf_name = self.config.get('transfer', {}).get('shelf_name', 'Contenido de Obsidian')
            print(f"  • 1 estante principal: '{shelf_name}'")
            print(f"  • {book_count} libros")
            print(f"  • {chapter_count} capítulos")
            print(f"  • {page_count} páginas")
            if total_images > 0:
                print(f"  • {total_images} imágenes para transferir")
            if total_attachments > 0:
                print(f"  • {total_attachments} adjuntos para transferir")
            print(f"\n📚 Todos los libros se organizarán en el estante: '{shelf_name}'")
            if total_images > 0 or total_attachments > 0:
                print(f"📎 Se procesarán {total_images + total_attachments} archivos multimedia en total")
            print("\n⚠️  NOTA: Esta es una simulación. Ejecuta sin --dry-run para realizar la transferencia real.")
            
        except Exception as e:
            print(f"Error analizando archivos: {e}")
    



def load_config(config_path: str) -> Dict:
    """Carga la configuración desde un archivo JSON"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Error cargando configuración: {e}")


def main():
    parser = argparse.ArgumentParser(description='Transfiere contenido de Obsidian a BookStack usando configuración')
    parser.add_argument('config', help='Ruta al archivo de configuración JSON')
    parser.add_argument('--dry-run', action='store_true', help='Simula la transferencia sin crear contenido')
    parser.add_argument('--test-connection', action='store_true', help='Prueba la conexión con BookStack con diagnósticos detallados')
    
    args = parser.parse_args()
    
    try:
        config = load_config(args.config)
        
        if args.test_connection:
            # Solo probar conexión con diagnósticos detallados
            bookstack = BookStackAPI(
                config['bookstack']['url'],
                config['bookstack']['token_id'],
                config['bookstack']['token_secret']
            )
            success = bookstack.test_connection(verbose=True)
            if not success:
                print("\n❌ La prueba de conexión falló. Revisa tu configuración antes de continuar.")
                exit(1)
            return
        
        if args.dry_run:
            print("Modo simulación activado - no se creará contenido real")
            transfer = ObsidianToBookStackTransfer(config)
            transfer.dry_run_transfer()
            return
        
        transfer = ObsidianToBookStackTransfer(config)
        success = transfer.transfer()
        
        if success:
            print("\n¡Transferencia exitosa!")
        else:
            print("\nLa transferencia falló")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()