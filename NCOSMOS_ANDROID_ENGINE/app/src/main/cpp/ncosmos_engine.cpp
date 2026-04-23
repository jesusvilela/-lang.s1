#include <jni.h>
#include <vector>
#include <cmath>
#include <string>

// NCosmos Native Engine Core
// Implements Hamiltonian flow over Poincaré-hyperbolic n-manifold (n=8)

class NCosmosSection {
public:
    float q[8];
    float p[8];
    float salience;

    NCosmosSection() {
        for(int i=0; i<8; ++i) {
            q[i] = 0.0f;
            p[i] = 0.0f;
        }
        salience = 1.0f;
    }

    float norm() {
        float sum = 0;
        for(int i=0; i<8; ++i) sum += q[i] * q[i];
        return std::sqrt(sum);
    }

    float energy() {
        float sum_q = 0, sum_p = 0;
        for(int i=0; i<8; ++i) {
            sum_q += q[i] * q[i];
            sum_p += p[i] * p[i];
        }
        return 0.5f * sum_p + 0.5f * sum_q;
    }

    void evolve(float dt) {
        // Symplectic leapfrog step
        for(int i=0; i<8; ++i) {
            q[i] += p[i] * dt;
            p[i] -= q[i] * dt;
        }
    }

    void mobius_rho() {
        for(int i=0; i<8; ++i) {
            q[i] = -q[i];
            p[i] = -p[i];
        }
    }
};

extern "C" JNIEXPORT jfloatArray JNICALL
Java_com_topos_ncosmos_NCosmosRuntime_evolveSection(
        JNIEnv* env,
        jobject /* this */,
        jfloatArray current_q,
        jfloatArray current_p,
        jfloat dt) {
    
    jfloat* q_ptr = env->GetFloatArrayElements(current_q, 0);
    jfloat* p_ptr = env->GetFloatArrayElements(current_p, 0);

    NCosmosSection section;
    for(int i=0; i<8; ++i) {
        section.q[i] = q_ptr[i];
        section.p[i] = p_ptr[i];
    }

    section.evolve(dt);

    jfloatArray result = env->NewFloatArray(16);
    jfloat res[16];
    for(int i=0; i<8; ++i) {
        res[i] = section.q[i];
        res[i+8] = section.p[i];
    }
    env->SetFloatArrayRegion(result, 0, 16, res);

    env->ReleaseFloatArrayElements(current_q, q_ptr, 0);
    env->ReleaseFloatArrayElements(current_p, p_ptr, 0);

    return result;
}

extern "C" JNIEXPORT jboolean JNICALL
Java_com_topos_ncosmos_NCosmosRuntime_checkInteriority(
        JNIEnv* env,
        jobject /* this */,
        jfloatArray current_q) {
    
    jfloat* q_ptr = env->GetFloatArrayElements(current_q, 0);
    float sum = 0;
    for(int i=0; i<8; ++i) sum += q_ptr[i] * q_ptr[i];
    
    env->ReleaseFloatArrayElements(current_q, q_ptr, 0);
    return (std::sqrt(sum) < 0.999f) ? JNI_TRUE : JNI_FALSE;
}
