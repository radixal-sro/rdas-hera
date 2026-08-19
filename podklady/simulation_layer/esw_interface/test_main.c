#include "hera_interface.h"
#include "stub_utils.h"
#define APID_HERA       1500
#define TYPE_HERA       230
#define SUBTYPE_HERA    1
#define MAX_LINE_WIDTH  1020
#define MAX_LINES       1020
 
/**
* @brief Compresses an image line-by-line using smart RLE.
* * Logic:
* 1. Attempt to compress the line.
* 2. If compressed size < 1020 bytes, store the compressed data.
* 3. If compressed size >= 1020 bytes, store the original raw data.
* * @param img_data Pointer to the start of the raw image buffer.
* @param width Image width in pixels.
* @param height Image height in pixels.
*/
void compress_image(const uint8* img_data, int width, int height) {
    // Buffer size allocated for worst-case RLE expansion (2x)
    // We allocate this locally to avoid corrupting the source image.
    uint8 compressed_line[MAX_LINE_WIDTH * 2];
 
    for (int y = 0; y < height; y++) {
        // Pointer to the start of the current raw line in memory
        const uint8* raw_line = &img_data[y * width];

        int rle_index = 0;
        int x = 0;
        // --- Step 1: Attempt Compression ---
        while (x < width) {
            uint8 pixel_val = raw_line[x];
            uint8 run_length = 1;
            x++;
            // Count identical consecutive pixels (up to 255)
            while (x < width && raw_line[x] == pixel_val && run_length < 255) {
                run_length++;
                x++;
            }
            // Write the (Count, Value) pair to our temporary buffer
            compressed_line[rle_index++] = run_length;
            compressed_line[rle_index++] = pixel_val;
            // If the compressed version is already bigger than the original,
            // we can stop processing this line immediately to save CPU cycles.
            if (rle_index >= width) {
                break;
            }
        }
 
        // --- Step 2: Compare & Report ---
        if (rle_index < width) {
            // Success: The compressed version is smaller. Store it.
            Hera_Science_Report(APID_HERA, TYPE_HERA, SUBTYPE_HERA, (void*)compressed_line, (uint16)rle_index);
        } else {
            // The compressed version is larger or equal. Store the original raw line.
            Hera_Science_Report(APID_HERA, TYPE_HERA, SUBTYPE_HERA, (void*)raw_line, (uint16)width);
        }
    }
}
 
int main(void) {
    error_code_t status;
    uint32 exposure_time = 500;
    print_str("\n--- HERA RLE Test ---\n");
    // 1. Request Core0 to acquire an image from the camera
    print_str("Acquiring AFC...\n");
    status = Hera_AFC_AcquireSingleImage(exposure_time);

    if (status == HERA_OK) print_str(">> OK: Acquired.\n");
    else print_str(">> FAIL.\n");
    // 2. Retrieve the memory address of the new image
    uint8* pImg = Hera_AFC_GetImageBuffer();

    // 3. Run the compression and storage routine
    compress_image(pImg, MAX_LINE_WIDTH, MAX_LINES);
    // 4. Send a Housekeeping (HK) report with e.g. summary of results
    print_str("HK Report...\n");
    uint8 d[] = {0xCA, 0xFE};
    Hera_HK_Report(99, d, 2);
 
    print_str("--- TEST END ---\n");

    while(1);
    return 0;
}
