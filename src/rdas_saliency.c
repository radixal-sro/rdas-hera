/**
 * @file rdas_saliency.c
 * @brief Implementation of Fast Deterministic Saliency and Crater Extractor
 * @author radixal s.r.o.
 */

#include "rdas_saliency.h"

void rdas_saliency_compute_grid(rdas_saliency_state_t* state, const uint8* pImg) {
    uint32 gr, gc;
    uint32 step = RDAS_IMG_WIDTH / RDAS_GRID_SIZE; /* ~15 px step */
    uint32 sum = 0U;
    uint16 max_val = 0U;

    for (gr = 0U; gr < RDAS_GRID_SIZE; ++gr) {
        uint32 r_px = gr * step;
        for (gc = 0U; gc < RDAS_GRID_SIZE; ++gc) {
            uint32 c_px = gc * step;
            
            /* Fast 4-point cross-gradient */
            uint32 p_c = (uint32)pImg[(r_px * RDAS_IMG_WIDTH) + c_px];
            uint32 p_r = (c_px + 8U < RDAS_IMG_WIDTH) ? (uint32)pImg[(r_px * RDAS_IMG_WIDTH) + c_px + 8U] : p_c;
            uint32 p_d = (r_px + 8U < RDAS_IMG_HEIGHT) ? (uint32)pImg[((r_px + 8U) * RDAS_IMG_WIDTH) + c_px] : p_c;

            int32 gx = (int32)p_r - (int32)p_c;
            int32 gy = (int32)p_d - (int32)p_c;
            uint16 grad = (uint16)(((gx < 0 ? -gx : gx) + (gy < 0 ? -gy : gy)));

            state->grid[(gr * RDAS_GRID_SIZE) + gc] = grad;
            sum += grad;
            if (grad > max_val) {
                max_val = grad;
            }
        }
    }

    state->max_saliency = max_val;
    state->mean_saliency = (uint16)(sum / (RDAS_GRID_SIZE * RDAS_GRID_SIZE));
}

void rdas_saliency_extract_rois(rdas_saliency_state_t* state, uint16 threshold) {
    uint32 gr, gc;
    uint32 step = RDAS_IMG_WIDTH / RDAS_GRID_SIZE;
    state->num_rois_found = 0U;

    for (gr = 2U; gr < (RDAS_GRID_SIZE - 2U) && state->num_rois_found < RDAS_MAX_ROIS; ++gr) {
        for (gc = 2U; gc < (RDAS_GRID_SIZE - 2U) && state->num_rois_found < RDAS_MAX_ROIS; ++gc) {
            uint16 val = state->grid[(gr * RDAS_GRID_SIZE) + gc];
            if (val >= threshold) {
                /* Create ROI bounding box */
                rdas_roi_t* roi = &state->rois[state->num_rois_found];
                roi->x = (uint16)((gc - 2U) * step);
                roi->y = (uint16)((gr - 2U) * step);
                roi->width = (uint16)(step * 4U);
                roi->height = (uint16)(step * 4U);
                roi->saliency_score = val;
                roi->classification_class = 1U; /* Crater candidate */
                roi->confidence_pct = (uint8)((val * 100U) / (state->max_saliency > 0 ? state->max_saliency : 1U));
                roi->metric_diameter_m = 0;

                state->num_rois_found++;
                gc += 3U; /* Non-maximum suppression skip */
            }
        }
    }
}

void rdas_saliency_fuse_palt(rdas_roi_t* roi, float32 altitude_m) {
    /* Hera AFC Optical Specs: Focal length f = 106.6 mm, Pixel pitch p = 14 um, IFOV = 0.131 mrad/px */
    /* Metric diameter D = (pixel_width * pixel_pitch * altitude) / focal_length */
    /* D = pixel_width * altitude_m * (0.000014 / 0.1066) = pixel_width * altitude_m * 0.00013133 */
    if (altitude_m > 1.0f) {
        float32 diam_m = (float32)roi->width * altitude_m * 0.00013133f;
        roi->metric_diameter_m = (fixed32_t)(diam_m * 65536.0f);
    }
}
