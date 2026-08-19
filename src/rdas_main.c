/**
 * @file rdas_main.c
 * @brief Main In-Flight Execution Entry Point for Radixal Deep-Space Autonomy Suite (R-DAS)
 * @author radixal s.r.o. (PI: Bc. Viktor Lostak, Engineering: Ing. Petr Slepicka)
 * @target GR712RC Dual-Core LEON3, Core 1 Bare-Metal Sandbox
 */

#include "rdas_types.h"
#include "rdas_saliency.h"
#include "rdas_wavelet.h"

/* Static Memory Pools (Strictly Zero Dynamic Allocation) */
static rdas_saliency_state_t g_saliency_state;
static rdas_wavelet_tile_t   g_wavelet_tile;
static uint8                 g_science_packet_payload[MAX_SCIENCE_SIZE];
static uint8                 g_hk_packet_payload[MAX_HK_SIZE];

/* In-Flight TMR Session Counter */
static tmr_uint32_t          g_session_frames_processed;

/**
 * @brief Core 1 Entry Point
 */
int main(void) {
    uint32 frame_idx = 0U;
    error_code_t err;
    uint8* pImageBuffer = (void*)0;

    /* Initialize SIFT TMR State */
    tmr_set_uint32(&g_session_frames_processed, 0U);

    /* 1. Send Boot Housekeeping Telemetry (PUS-3) */
    g_hk_packet_payload[0] = 0x01U; /* System Ready */
    g_hk_packet_payload[1] = 0x00U; /* Zero Errors */
    (void)Hera_HK_Report(0x0301U, g_hk_packet_payload, 2U);

    /* Main Operational Loop (Runs within 2-3 hour session window) */
    while (frame_idx < 10U) {
        /* Ingest Altimeter parameter from Mission Data Pool */
        float32 altitude_m = Hera_Read_Parameter_float32(0x1042U); /* PALT_ALTITUDE_VAL */

        /* Trigger Optical Acquisition */
        err = Hera_AFC_AcquireSingleImage(500U); /* 500 us exposure */
        if (err != HERA_OK) {
            (void)Hera_Event_Report(0x0501U, (void*)0, 0U); /* Warning Event */
            (void)Hera_Sleep(5U);
            continue;
        }

        pImageBuffer = Hera_AFC_GetImageBuffer();
        if (pImageBuffer == (void*)0) {
            continue;
        }

        /* STAGE 1: Spatial Saliency & Crater Feature Extraction */
        rdas_saliency_compute_grid(&g_saliency_state, pImageBuffer);
        rdas_saliency_extract_rois(&g_saliency_state, 45U);

        /* Fuse with PALT Laser Altimetry */
        if (g_saliency_state.num_rois_found > 0U) {
            uint32 r;
            for (r = 0U; r < g_saliency_state.num_rois_found; ++r) {
                rdas_saliency_fuse_palt(&g_saliency_state.rois[r], altitude_m);
            }
        }

        /* STAGE 2: Tile-based Wavelet Compression on High-Saliency Areas */
        rdas_tile_load_raw(&g_wavelet_tile, pImageBuffer, 0U, 0U, RDAS_IMG_WIDTH);
        rdas_dwt_forward_2d(&g_wavelet_tile, 2U);
        uint32 compressed_bytes = rdas_tile_encode_entropy(&g_wavelet_tile, g_science_packet_payload, MAX_SCIENCE_SIZE);

        /* STAGE 3: Emit PUS Science Telemetry (APID 0x480) */
        (void)Hera_Science_Report(0x0480U, 20U, 1U, g_science_packet_payload, (uint16)compressed_bytes);

        frame_idx++;
        tmr_set_uint32(&g_session_frames_processed, frame_idx);

        /* Power & Thermal Relaxation Cycle */
        (void)Hera_Sleep(10U);
    }

    /* Emit Final Session Summary HK */
    g_hk_packet_payload[0] = 0x02U; /* Session Completed */
    g_hk_packet_payload[1] = (uint8)tmr_vote_uint32(&g_session_frames_processed);
    (void)Hera_HK_Report(0x0302U, g_hk_packet_payload, 2U);

    return 0;
}
