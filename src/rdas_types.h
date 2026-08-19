/**
 * @file rdas_types.h
 * @brief Radixal Deep-Space Autonomy Suite (R-DAS) - Common Types and SIFT Primitives
 * @author radixal s.r.o. (Lead Architect: Bc. Viktor Lostak, Engineering: Ing. Petr Slepicka)
 * @target GR712RC Dual-Core LEON3 (SPARC V8 @ 50 MHz), Core 1 Bare-Metal
 * @standard ECSS-E-ST-40C Category D / MISRA-C:2012 Deterministic Zero-Heap
 */

#ifndef RDAS_TYPES_H
#define RDAS_TYPES_H

#include "../specs/simulation_layer/esw_interface/hera_interface.h"

/* In-flight Memory Constants */
#define RDAS_STACK_BASE          0x40010000U
#define RDAS_CONFIG_BLOCK_ADDR   0x40001000U

/* Image and Tile Geometry */
#define RDAS_IMG_WIDTH           1020U
#define RDAS_IMG_HEIGHT          1020U
#define RDAS_TILE_SIZE           128U
#define RDAS_TILES_PER_ROW       8U
#define RDAS_TILES_PER_COL       8U
#define RDAS_TOTAL_TILES         64U

/* Saliency & Detection Limits */
#define RDAS_MAX_ROIS            16U
#define RDAS_MAX_CRATERS         32U

/* Fixed-Point Arithmetic Precision (Q16.16) */
typedef int32 fixed32_t;
#define FIXED_ONE                (1 << 16)
#define INT_TO_FIXED(x)          ((fixed32_t)((x) << 16))
#define FIXED_TO_INT(x)          ((int32)((x) >> 16))
#define FIXED_MUL(a, b)          ((fixed32_t)(((int64)(a) * (int64)(b)) >> 16))
#define FIXED_DIV(a, b)          ((fixed32_t)((((int64)(a)) << 16) / (b)))

/* Software-Implemented Fault Tolerance (SIFT) - Triple Modular Redundancy (TMR) */
typedef struct {
    uint32 val_a;
    uint32 val_b;
    uint32 val_c;
} tmr_uint32_t;

static inline uint32 tmr_vote_uint32(const tmr_uint32_t* tmr) {
    if (tmr->val_a == tmr->val_b) {
        return tmr->val_a;
    }
    if (tmr->val_a == tmr->val_c) {
        return tmr->val_a;
    }
    return tmr->val_b;
}

static inline void tmr_set_uint32(tmr_uint32_t* tmr, uint32 val) {
    tmr->val_a = val;
    tmr->val_b = val;
    tmr->val_c = val;
}

/* In-Flight Configurable Parameters (64 bytes aligned at 0x40001000) */
typedef struct {
    uint16 config_version;       /* Config format version */
    uint16 saliency_threshold;   /* Gradient threshold for ROI trigger (default: 45) */
    uint16 min_crater_radius_px; /* Min crater radius in px (default: 8) */
    uint16 max_crater_radius_px; /* Max crater radius in px (default: 120) */
    uint8  wavelet_levels;       /* Wavelet decomposition depth (default: 3) */
    uint8  compression_quality;  /* Bit-plane truncation mask (default: 0xFF) */
    uint16 max_telemetry_bytes;  /* Max science payload per session (default: 2048) */
    uint32 session_timeout_sec;  /* Guard timeout (default: 7200) */
    uint32 crc32_checksum;       /* Checksum of config block */
    uint8  reserved[40];         /* Padding to exact 64 bytes */
} __attribute__((packed, aligned(4))) rdas_config_t;

/* Extracted High-Saliency Region of Interest (ROI) */
typedef struct {
    uint16 x;                    /* Top-left X coordinate in AFC frame */
    uint16 y;                    /* Top-left Y coordinate in AFC frame */
    uint16 width;                /* ROI width (multiples of 16 px) */
    uint16 height;               /* ROI height (multiples of 16 px) */
    uint16 saliency_score;       /* Integrated saliency metric */
    uint8  classification_class; /* 1: Crater, 2: Boulder, 3: Regolith */
    uint8  confidence_pct;       /* 0–100% confidence */
    fixed32_t metric_diameter_m; /* Scaled diameter via PALT altimeter fusion */
} rdas_roi_t;

#endif /* RDAS_TYPES_H */
