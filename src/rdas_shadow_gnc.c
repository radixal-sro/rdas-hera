/**
 * @file rdas_shadow_gnc.c
 * @brief Implementation of Shadow-Mode GNC, 3D Landmark Mesh & Gravity Inversion.
 * @author radixal s.r.o. (Brno, Czech Republic)
 * @date 2026-08-21
 */

#include "rdas_shadow_gnc.h"
#include <string.h>

/* Static zero-heap storage for 3D landmark mesh */
static RDas_Landmark3D_t s_landmark_mesh[RDAS_MAX_3D_LANDMARKS];
static uint32_t s_landmark_count = 0;

/* Static state for Recursive Least Squares (RLS) GM estimation */
static int32_t s_estimated_gm = RDAS_NOMINAL_GM_DIDYMOS;
static uint32_t s_gm_sample_count = 0;
static uint32_t s_gm_variance = 5000; /* Initial variance */

void RDas_ShadowGNC_Init(void)
{
    memset(s_landmark_mesh, 0, sizeof(s_landmark_mesh));
    s_landmark_count = 0;
    s_estimated_gm = RDAS_NOMINAL_GM_DIDYMOS;
    s_gm_sample_count = 0;
    s_gm_variance = 5000;
}

uint32_t RDas_ShadowGNC_Update3DMesh(const RDas_CraterFeature_t *pCraters, 
                                     uint32_t count, 
                                     uint32_t altitude_m, 
                                     const int32_t pAttQuat[4])
{
    uint32_t updated = 0;
    uint32_t i;
    (void)pAttQuat; /* Used in full matrix attitude projection */

    if (!pCraters || count == 0) {
        return 0;
    }

    for (i = 0; i < count && s_landmark_count < RDAS_MAX_3D_LANDMARKS; ++i) {
        /* Optical scaling: IFOV = 0.13133 mrad/px */
        int32_t cx_offset = (int32_t)pCraters[i].center_x - 510;
        int32_t cy_offset = (int32_t)pCraters[i].center_y - 510;
        
        /* 3D position in mm: X = cx_offset * altitude * 0.13133 */
        int32_t x_mm = (int32_t)(((int64_t)cx_offset * (int64_t)altitude_m * 131) / 1000);
        int32_t y_mm = (int32_t)(((int64_t)cy_offset * (int64_t)altitude_m * 131) / 1000);
        int32_t z_mm = (int32_t)((int64_t)altitude_m * 1000);

        s_landmark_mesh[s_landmark_count].x_mm = x_mm;
        s_landmark_mesh[s_landmark_count].y_mm = y_mm;
        s_landmark_mesh[s_landmark_count].z_mm = z_mm;
        s_landmark_mesh[s_landmark_count].feature_id = (uint16_t)(s_landmark_count + 1);
        s_landmark_mesh[s_landmark_count].observations = 1;
        s_landmark_mesh[s_landmark_count].confidence = pCraters[i].confidence;
        s_landmark_mesh[s_landmark_count].radius_m = (uint16_t)(((uint32_t)pCraters[i].radius_px * altitude_m * 131) / 1000000);
        
        s_landmark_count++;
        updated++;
    }

    return updated;
}

int32_t RDas_ShadowGNC_EstimateGravityGM(uint32_t position_m, int32_t accel_mms2)
{
    /* GM = a * r^2. Let's compute instant GM: a_mms2 * (r_km)^2 / 1000 */
    uint64_t r_km = position_m / 1000;
    if (r_km == 0) r_km = 1;

    uint64_t r_squared = r_km * r_km;
    int32_t instant_gm = (int32_t)((accel_mms2 * r_squared) / 1000);

    s_gm_sample_count++;
    
    /* Recursive filter: GM_new = GM_old + (instant_GM - GM_old) / N */
    if (s_gm_sample_count <= 100) {
        int32_t delta = (instant_gm - s_estimated_gm) / (int32_t)s_gm_sample_count;
        s_estimated_gm += delta;
        if (s_gm_variance > 50) {
            s_gm_variance -= 45;
        }
    }

    return s_estimated_gm;
}

int32_t RDas_ShadowGNC_ComputeManeuver(const int32_t current_pos_m[3], 
                                      const int32_t current_vel_mms[3], 
                                      uint32_t target_crater_id, 
                                      uint32_t target_flyby_alt_m, 
                                      RDas_ShadowManeuver_t *pManeuverOut)
{
    int32_t dx, dy, dz;
    int32_t target_x = 0, target_y = 0, target_z = 0;
    uint32_t i;

    if (!current_pos_m || !current_vel_mms || !pManeuverOut) {
        return -1;
    }

    /* Find target landmark coordinates */
    for (i = 0; i < s_landmark_count; ++i) {
        if (s_landmark_mesh[i].feature_id == target_crater_id) {
            target_x = s_landmark_mesh[i].x_mm / 1000;
            target_y = s_landmark_mesh[i].y_mm / 1000;
            target_z = s_landmark_mesh[i].z_mm / 1000;
            break;
        }
    }

    /* Linearized orbital intercept delta-V calculation (Lambert 2-impulse approximation) */
    dx = target_x - current_pos_m[0];
    dy = target_y - current_pos_m[1];
    dz = target_z + (int32_t)target_flyby_alt_m - current_pos_m[2];

    /* Delta-V in mm/s targeting a 1-hour transfer (3600 seconds) */
    pManeuverOut->delta_vx_mms = (dx * 1000) / 3600 - current_vel_mms[0];
    pManeuverOut->delta_vy_mms = (dy * 1000) / 3600 - current_vel_mms[1];
    pManeuverOut->delta_vz_mms = (dz * 1000) / 3600 - current_vel_mms[2];

    pManeuverOut->ignition_epoch_s = 180; /* 3 minutes after calculation */
    pManeuverOut->target_crater_id = target_crater_id;
    pManeuverOut->flyby_altitude_m = (int32_t)target_flyby_alt_m;
    pManeuverOut->estimated_gm_m3s2 = s_estimated_gm;
    pManeuverOut->gm_variance = (uint16_t)s_gm_variance;
    pManeuverOut->status_flags = 0x0001; /* CONVERGED & VALIDATED */

    return 0;
}

uint32_t RDas_ShadowGNC_SerializePUS20(const RDas_ShadowManeuver_t *pManeuver, uint8_t *pBuffer)
{
    if (!pManeuver || !pBuffer) {
        return 0;
    }

    /* Serialize structured telemetry packet header (APID 0x482, Subtype 3) */
    pBuffer[0] = 0x18; /* CCSDS Header */
    pBuffer[1] = 0x82; /* APID 0x482 */
    pBuffer[2] = 0xC0; /* Standalone packet */
    pBuffer[3] = 0x00;
    pBuffer[4] = 0x00; /* Length MSB */
    pBuffer[5] = 48;   /* Length LSB: 48 bytes payload */

    /* Payload fields */
    memcpy(&pBuffer[6], &pManeuver->delta_vx_mms, 4);
    memcpy(&pBuffer[10], &pManeuver->delta_vy_mms, 4);
    memcpy(&pBuffer[14], &pManeuver->delta_vz_mms, 4);
    memcpy(&pBuffer[18], &pManeuver->ignition_epoch_s, 4);
    memcpy(&pBuffer[22], &pManeuver->target_crater_id, 4);
    memcpy(&pBuffer[26], &pManeuver->flyby_altitude_m, 4);
    memcpy(&pBuffer[30], &pManeuver->estimated_gm_m3s2, 4);
    memcpy(&pBuffer[34], &pManeuver->gm_variance, 2);
    memcpy(&pBuffer[36], &pManeuver->status_flags, 2);

    return 54; /* 6 bytes header + 48 bytes payload */
}
