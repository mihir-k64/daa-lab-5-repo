import heapq
from collections import Counter
from docx import Document
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import os

# Define a class for Huffman Tree nodes
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Compare nodes based on frequency for heapq
    def __lt__(self, other):
        return self.freq < other.freq

# Build the Huffman Tree
def build_huffman_tree(text):
    if not text:
        raise ValueError("Text is empty, cannot build Huffman Tree.")
    
    # Filter out only letters from the text
    filtered_text = ''.join(filter(str.isalpha, text))
    freq = Counter(filtered_text)
    
    if not freq:  # Check if there are any letters
        raise ValueError("No letters found in text to build Huffman Tree.")
    
    heap = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    
    return heap[0]

# Generate Huffman Codes
def generate_codes(node, code, codes):
    if node is None:
        return
    
    if node.char is not None:
        codes[node.char] = code
    
    generate_codes(node.left, code + "0", codes)
    generate_codes(node.right, code + "1", codes)

# Compress the text using Huffman Coding
def compress(text):
    root = build_huffman_tree(text)
    codes = {}
    generate_codes(root, "", codes)
    compressed = ''.join([codes[char] for char in text if char in codes])  # Include only letters
    return compressed, codes

# Calculate the compression ratio
def calculate_compression_ratio(original_text, compressed_text):
    original_size = len(original_text) * 8  # Original text size in bits (1 char = 8 bits)
    compressed_size = len(compressed_text)  # Compressed text size (already in bits)
    return original_size, compressed_size

# Read DOCX file
def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return ' '.join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return ''

# Read PDF file
def extract_text_from_pdf(file_path):
    try:
        if not file_path.lower().endswith('.pdf'):
            print(f"Warning: The file '{file_path}' is not a PDF file since u have selected the option of pdf file but uploaded a docx file which is a mismatch between the format!")
            return ''
        
        reader = PdfReader(file_path)
        text = ''.join(page.extract_text() for page in reader.pages)
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ''

# Read HTML file
def extract_text_from_html(file_path):
    try:
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            return soup.get_text()
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return ''

# Read TXT file
def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return ''

# Process file depending on its type
def process_file(file_type, file_path):
    # Extract text based on the file type
    if file_type == 'html':
        text = extract_text_from_html(file_path)
    elif file_type == 'docx':
        text = extract_text_from_docx(file_path)
    elif file_type == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif file_type == 'txt':
        text = extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    if not text:
        print(f"No content extracted from {file_type} file. Since it does not include anything and it is blank, Huffman compression can't be done. To proceed, please enter some text.")
        return None, None

    # Additional check for file type mismatch
    if not file_path.lower().endswith(file_type):
        print(f"Warning: Selected file type is '{file_type}', but the file '{file_path}' does not match this type.")
    
    # Compress the extracted text
    compressed_text, huffman_codes = compress(text)
    original_size, compressed_size = calculate_compression_ratio(text, compressed_text)
    
    # Output the results
    print(f"File Type: {file_type}")
    print(f"Original text size (in bits): {original_size}")
    print(f"Compressed text size (in bits): {compressed_size}")
    print(f"Compression ratio: {compressed_size / original_size:.2f}")

    # Print Huffman codes for each letter
    print("Huffman Codes (for letters only):")
    for char, code in huffman_codes.items():
        if char.isalpha():  # Include only letters
            print(f"'{char}': {code}")

    return compressed_text, huffman_codes

# Example usage
process_file('pdf', 'intro.docx')  # This will trigger a warning about the file type mismatch.
