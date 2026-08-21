/**
 * @file rdas_shadow_gnc.h
 * @brief Shadow-Mode In-Situ 3D Mesh, Gravity Inversion, and Trajectory Benchmark Engine.
 * @author radixal s.r.o. (Brno, Czech Republic)
 * @date 2026-08-21
 *
 * Target: GR712RC Dual-Core LEON3 (SPARC V8 @ 50 MHz), Core 1 Bare-Metal.
 * Zero dynamic memory allocation (0 malloc), deterministic fixed-point math.
 */

#ifndef RDAS_SHADOW_GNC_H
#define RDAS_SHADOW_GNC_H

#include "rdas_types.h"

#ifdef __cplusplus
extern "C" {
#endif

#define RDAS_MAX_3D_LANDMARKS   64
#define RDAS_NOMINAL_GM_DIDYMOS 35400  /* 35.4 m^3/s^2 * 1000 fixed-point */

/**
 * @brief 3D Landmark Point in Asteroid-Fixed Frame.
 */
typedef struct {
    int32_t x_mm;          /**< X position in millimeters */
    int32_t y_mm;          /**< Y position in millimeters */
    int32_t z_mm;          /**< Z position in millimeters */
    uint16_t feature_id;   /**< Crater / Landmark feature ID */
    uint16_t observations; /**< Number of optical triangulation observations */
    uint16_t confidence;   /**< Confidence metric (0-100%) */
    uint16_t radius_m;     /**< Estimated feature radius in meters */
} RDas_Landmark3D_t;

/**
 * @brief Shadow-Mode Trajectory & Maneuver Recommendation Output.
 */
typedef struct {
    int32_t delta_vx_mms;      /**< Recommended delta-Vx in mm/s */
    int32_t delta_vy_mms;      /**< Recommended delta-Vy in mm/s */
    int32_t delta_vz_mms;      /**< Recommended delta-Vz in mm/s */
    uint32_t ignition_epoch_s; /**< Recommended ignition epoch (seconds from session start) */
    uint32_t target_crater_id; /**< Target landmark / DART crater ID */
    int32_t flyby_altitude_m;  /**< Target flyby closest approach altitude in meters */
    int32_t estimated_gm_m3s2; /**< In-situ estimated GM in m^3/s^2 (scaled x1000) */
    uint16_t gm_variance;      /**< Estimation variance (scaled) */
    uint16_t status_flags;     /**< Convergence and safety status flags */
} RDas_ShadowManeuver_t;

/**
 * @brief Initializes the Shadow-Mode GNC subsystem.
 */
void RDas_ShadowGNC_Init(void);

/**
 * @brief Ingests 2D optical craters and PALT altitude to triangulate 3D landmark mesh.
 * @param pCraters Array of detected 2D crater structures.
 * @param count Number of craters in array.
 * @param altitude_m Current PALT laser altitude in meters.
 * @param pAttQuat Pointer to 4-element spacecraft attitude quaternion.
 * @return Number of confirmed 3D landmarks updated.
 */
uint32_t RDas_ShadowGNC_Update3DMesh(const RDas_CraterFeature_t *pCraters, 
                                     uint32_t count, 
                                     uint32_t altitude_m, 
                                     const int32_t pAttQuat[4]);

/**
 * @brief Recursively estimates Didymos/Dimorphos gravitational parameter GM from passive orbital acceleration.
 * @param position_m Spacecraft radial distance from asteroid center in meters.
 * @param accel_mms2 Measured net gravitational acceleration in mm/s^2.
 * @return Current filtered GM estimate (scaled x1000 m^3/s^2).
 */
int32_t RDas_ShadowGNC_EstimateGravityGM(uint32_t position_m, int32_t accel_mms2);

/**
 * @brief Computes optimal impulsive delta-V maneuver recommendation to target DART crater flyby.
 * @param current_pos_m Current spacecraft position [X, Y, Z] in meters.
 * @param current_vel_mms Current spacecraft velocity [Vx, Vy, Vz] in mm/s.
 * @param target_crater_id Landmark ID of target scientific ROI / DART crater.
 * @param target_flyby_alt_m Desired closest approach altitude in meters.
 * @param pManeuverOut Pointer to output shadow maneuver structure.
 * @return 0 on success, negative error code on constraint violation.
 */
int32_t RDas_ShadowGNC_ComputeManeuver(const int32_t current_pos_m[3], 
                                      const int32_t current_vel_mms[3], 
                                      uint32_t target_crater_id, 
                                      uint32_t target_flyby_alt_m, 
                                      RDas_ShadowManeuver_t *pManeuverOut);

/**
 * @brief Serializes the Shadow-Mode GNC results into a 128-byte PUS Service 20 packet buffer.
 * @param pManeuver Pointer to computed maneuver structure.
 * @param pBuffer Destination buffer (minimum 128 bytes).
 * @return Number of serialized bytes.
 */
uint32_t RDas_ShadowGNC_SerializePUS20(const RDas_ShadowManeuver_t *pManeuver, uint8_t *pBuffer);

#ifdef __cplusplus
}
#endif

#endif /* RDAS_SHADOW_GNC_H */
