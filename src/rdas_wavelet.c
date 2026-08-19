/**
 * @file rdas_wavelet.c
 * @brief Implementation of 2D Integer Lifting Wavelet Transform (CDF 5/3)
 * @author radixal s.r.o.
 */

#include "rdas_wavelet.h"

void rdas_dwt_forward_1d(int16* line, uint32 len) {
    uint32 i;
    uint32 half = len >> 1;
    int16 temp[RDAS_WAVELET_TILE_SIZE];

    if (len < 2U || len > RDAS_WAVELET_TILE_SIZE) {
        return;
    }

    /* Copy to temp buffer */
    for (i = 0U; i < len; ++i) {
        temp[i] = line[i];
    }

    /* 1. Predict Step: High-pass detail coefficients d[i] */
    for (i = 0U; i < half; ++i) {
        int32 left = (int32)temp[i << 1];
        int32 right = ((i + 1U) < half) ? (int32)temp[(i + 1U) << 1] : left;
        int32 odd = (int32)temp[(i << 1) + 1U];
        
        /* d[i] = x[2i+1] - floor((x[2i] + x[2i+2]) / 2) */
        line[half + i] = (int16)(odd - ((left + right) >> 1));
    }

    /* 2. Update Step: Low-pass approximation coefficients s[i] */
    for (i = 0U; i < half; ++i) {
        int32 left_d = (i > 0U) ? (int32)line[half + i - 1U] : (int32)line[half + i];
        int32 right_d = (int32)line[half + i];
        int32 even = (int32)temp[i << 1];

        /* s[i] = x[2i] + floor((d[i-1] + d[i] + 2) / 4) */
        line[i] = (int16)(even + ((left_d + right_d + 2) >> 2));
    }
}

void rdas_tile_load_raw(rdas_wavelet_tile_t* tile, const uint8* pImg, uint16 start_x, uint16 start_y, uint16 stride) {
    uint32 r, c;
    tile->width = RDAS_WAVELET_TILE_SIZE;
    tile->height = RDAS_WAVELET_TILE_SIZE;

    for (r = 0U; r < RDAS_WAVELET_TILE_SIZE; ++r) {
        uint32 img_row = (uint32)start_y + r;
        for (c = 0U; c < RDAS_WAVELET_TILE_SIZE; ++c) {
            uint32 img_col = (uint32)start_x + c;
            if (img_row < RDAS_IMG_HEIGHT && img_col < RDAS_IMG_WIDTH) {
                tile->buffer[(r * RDAS_WAVELET_TILE_SIZE) + c] = (int16)pImg[(img_row * (uint32)stride) + img_col];
            } else {
                tile->buffer[(r * RDAS_WAVELET_TILE_SIZE) + c] = 0;
            }
        }
    }
}

void rdas_dwt_forward_2d(rdas_wavelet_tile_t* tile, uint8 levels) {
    uint8 lvl;
    uint32 cur_w = RDAS_WAVELET_TILE_SIZE;
    uint32 cur_h = RDAS_WAVELET_TILE_SIZE;
    int16 line_buf[RDAS_WAVELET_TILE_SIZE];
    uint32 r, c;

    for (lvl = 0U; lvl < levels; ++lvl) {
        /* Transform Rows */
        for (r = 0U; r < cur_h; ++r) {
            for (c = 0U; c < cur_w; ++c) {
                line_buf[c] = tile->buffer[(r * RDAS_WAVELET_TILE_SIZE) + c];
            }
            rdas_dwt_forward_1d(line_buf, cur_w);
            for (c = 0U; c < cur_w; ++c) {
                tile->buffer[(r * RDAS_WAVELET_TILE_SIZE) + c] = line_buf[c];
            }
        }

        /* Transform Columns */
        for (c = 0U; c < cur_w; ++c) {
            for (r = 0U; r < cur_h; ++r) {
                line_buf[r] = tile->buffer[(r * RDAS_WAVELET_TILE_SIZE) + c];
            }
            rdas_dwt_forward_1d(line_buf, cur_h);
            for (r = 0U; r < cur_h; ++r) {
                tile->buffer[(r * RDAS_WAVELET_TILE_SIZE) + c] = line_buf[r];
            }
        }

        cur_w >>= 1;
        cur_h >>= 1;
    }
}

uint32 rdas_tile_encode_entropy(const rdas_wavelet_tile_t* tile, uint8* out_buf, uint32 max_out_len) {
    uint32 total_coeffs = RDAS_WAVELET_TILE_SIZE * RDAS_WAVELET_TILE_SIZE;
    uint32 i;
    uint32 out_idx = 0U;
    uint32 zero_run = 0U;

    /* Simple bit-exact run-length encoder on quantized high-frequency DWT coefficients */
    for (i = 0U; i < total_coeffs && out_idx < (max_out_len - 4U); ++i) {
        int16 coeff = tile->buffer[i];
        if (coeff == 0) {
            zero_run++;
            if (zero_run == 255U) {
                out_buf[out_idx++] = 0x00U;
                out_buf[out_idx++] = 0xFFU;
                zero_run = 0U;
            }
        } else {
            if (zero_run > 0U) {
                out_buf[out_idx++] = 0x00U;
                out_buf[out_idx++] = (uint8)zero_run;
                zero_run = 0U;
            }
            /* Emit non-zero coefficient (quantized 8-bit magnitude + sign) */
            uint8 sign = (coeff < 0) ? 0x80U : 0x00U;
            uint8 mag = (uint8)((coeff < 0) ? (-coeff) : coeff);
            out_buf[out_idx++] = sign | (mag & 0x7FU);
        }
    }

    if (zero_run > 0U && out_idx < (max_out_len - 2U)) {
        out_buf[out_idx++] = 0x00U;
        out_buf[out_idx++] = (uint8)zero_run;
    }

    return out_idx;
}
