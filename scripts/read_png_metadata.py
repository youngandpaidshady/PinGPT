import os

def extract_png_metadata(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    idx = 0
    metadata = {}
    while idx < len(data):
        # find the next chunk
        # Chunk structure: length (4 bytes), type (4 bytes), data (length bytes), crc (4 bytes)
        chunk_type_idx = data.find(b'tEXt', idx)
        chunk_type_idx2 = data.find(b'iTXt', idx)
        
        found = []
        if chunk_type_idx != -1: found.append(('tEXt', chunk_type_idx))
        if chunk_type_idx2 != -1: found.append(('iTXt', chunk_type_idx2))
        
        if not found:
            break
            
        found.sort(key=lambda x: x[1])
        c_type, c_idx = found[0]
        
        try:
            # chunk length is 4 bytes before type
            length = int.from_bytes(data[c_idx-4:c_idx], 'big')
            chunk_data = data[c_idx+4:c_idx+4+length]
            print(f"[{filepath}] Found {c_type}:", chunk_data[:200]) # Print first 200 bytes
        except Exception as e:
            pass
            
        idx = c_idx + 4
        
if __name__ == "__main__":
    folder = r"c:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch"
    for file in os.listdir(folder):
        if file.endswith(".png"):
            extract_png_metadata(os.path.join(folder, file))
