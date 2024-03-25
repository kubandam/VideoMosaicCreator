import cv2
import sys
import numpy as np

def extract_frames(video_path, rows, cols):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # priadnie marginu aby nebol prvy a posledny obrazok cierny
    start_margin = int(frame_count * 0.01) 
    end_margin = int(frame_count * 0.99)  

    frames_to_extract = np.linspace(start_margin, end_margin, num=rows * cols, dtype=int)
    frames = []
    for i, frame_index in enumerate(frames_to_extract):
        print("\rProcessing.. %d%% complete"%(((i + 1) / len(frames_to_extract)) * 100), end="", flush=True)        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    cap.release()
    return frames

def create_mosaic(frames, rows, cols, width, height):
    tile_width = width // cols
    tile_height = height // rows
    
    resized_frames = [cv2.resize(frame, (tile_width, tile_height)) for frame in frames]
    
    mosaic = np.zeros((height, width, 3), dtype=np.uint8)
    for i, frame in enumerate(resized_frames):
        row = i // cols
        col = i % cols
        start_row = row * tile_height
        start_col = col * tile_width
        end_row = start_row + tile_height
        end_col = start_col + tile_width

        mosaic[start_row:end_row, start_col:end_col] = frame[:tile_height, :tile_width]

    return mosaic

def main():
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    width = int(sys.argv[3])
    height = int(sys.argv[4])
    video_path = sys.argv[5]
    output_path = sys.argv[6]

    frames = extract_frames(video_path, rows, cols)
    if len(frames) != rows * cols:
        sys.exit(1)

    mosaic_image = create_mosaic(frames, rows, cols, width, height)
    cv2.imwrite(output_path, mosaic_image)
    print(f"\nMosaic image saved as {output_path}")

if __name__ == "__main__":
    main()

#python mosaic.py 5 4 1280 1024 input.mkv output-1.jpg
#python mosaic.py 1 1 1280 1024 input.mkv output-2.jpg
#python mosaic.py 1 2 1280 1024 input.mkv output-3.jpg
#python mosaic.py 3 1 1280 1024 input.mkv output-4.jpg
#python mosaic.py 6 6 1280 1024 input.mkv output-5.jpg
#python mosaic.py 20 20 1920 1080 input.mkv output-6.jpg
#python mosaic.py 40 40 3840 2160 input.mkv output-7.jpg