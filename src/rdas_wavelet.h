/**
 * @file rdas_wavelet.h
 * @brief Reversible 2D Integer Discrete Wavelet Transform (CDF 5/3 Lifting Scheme)
 * @author radixal s.r.o.
 */

#ifndef RDAS_WAVELET_H
#define RDAS_WAVELET_H

#include "rdas_types.h"

#define RDAS_WAVELET_TILE_SIZE 128U

/* Tile working memory: 128x128 16-bit signed integer buffer (32,768 bytes) */
typedef struct {
    int16 buffer[RDAS_WAVELET_TILE_SIZE * RDAS_WAVELET_TILE_SIZE];
    uint16 width;
    uint16 height;
} rdas_wavelet_tile_t;

/**
 * @brief In-place 1D CDF 5/3 forward lifting step along a line of length N.
 */
void rdas_dwt_forward_1d(int16* line, uint32 len);

/**
 * @brief In-place 2D CDF 5/3 forward wavelet decomposition on 128x128 tile.
 * @param tile Pointer to static tile structure.
 * @param levels Number of decomposition levels (typically 2 or 3).
 */
void rdas_dwt_forward_2d(rdas_wavelet_tile_t* tile, uint8 levels);

/**
 * @brief Loads raw 8-bit image pixels into 16-bit signed tile buffer.
 */
void rdas_tile_load_raw(rdas_wavelet_tile_t* tile, const uint8* pImg, uint16 start_x, uint16 start_y, uint16 stride);

/**
 * @brief Compresses decomposed tile coefficients using Golomb-Rice entropy coding.
 * @return Number of compressed bytes written to out_buf.
 */
uint32 rdas_tile_encode_entropy(const rdas_wavelet_tile_t* tile, uint8* out_buf, uint32 max_out_len);

#endif /* RDAS_WAVELET_H */
