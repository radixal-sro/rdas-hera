/**
 * @file rdas_saliency.h
 * @brief Fast Deterministic Saliency and Crater Feature Extractor
 * @author radixal s.r.o.
 */

#ifndef RDAS_SALIENCY_H
#define RDAS_SALIENCY_H

#include "rdas_types.h"

#define RDAS_GRID_SIZE 64U

typedef struct {
    uint16 grid[RDAS_GRID_SIZE * RDAS_GRID_SIZE];
    uint16 max_saliency;
    uint16 mean_saliency;
    uint32 num_rois_found;
    rdas_roi_t rois[RDAS_MAX_ROIS];
} rdas_saliency_state_t;

/**
 * @brief Computes coarse spatial saliency grid over 1020x1020 image without heap allocation.
 */
void rdas_saliency_compute_grid(rdas_saliency_state_t* state, const uint8* pImg);

/**
 * @brief Identifies top ROIs (Craters, Boulders, Ejecta boundaries).
 */
void rdas_saliency_extract_rois(rdas_saliency_state_t* state, uint16 threshold);

/**
 * @brief Fuses pixel crater bounding box with PALT laser altitude to compute metric crater diameter.
 */
void rdas_saliency_fuse_palt(rdas_roi_t* roi, float32 altitude_m);

#endif /* RDAS_SALIENCY_H */
