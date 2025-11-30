"""
Gerchberg-Saxton phase-only hologram (angular spectrum propagation)
Save this file as gs_kinoform.py and run.
Requires: numpy, scipy, imageio, matplotlib
"""

import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift
import imageio
import matplotlib.pyplot as plt

# ---------------- user params ----------------
target_path = "picasso.png"   # path to your target monochrome image
wavelength = 633e-9       # meters (e.g., 633 nm)
pixel_pitch = 8e-6        # SLM pixel size in meters (8 um typical)
prop_dist = 0.2           # propagation distance in meters (tune)
n_iter = 10              # GS iterations
slm_amp = 1.0             # amplitude at SLM (phase-only)
quantize_bits = None      # set to e.g. 8 to quantize phase; or None
# ------------------------------------------------

# helper: load and prepare target intensity
def load_target(path, N):
    img = imageio.v2.imread(path, mode="F").astype(np.float32)
    # normalize to [0,1]
    img = img - img.min()
    if img.max() > 0:
        img /= img.max()
    # center-crop or pad to NxN
    h, w = img.shape
    if h != N or w != N:
        # simple resize by padding/cropping to center (not interpolation)
        out = np.zeros((N, N), dtype=img.dtype)
        sh = min(h, N); sw = min(w, N)
        r0 = (N - sh)//2; c0 = (N - sw)//2
        r1 = (h - sh)//2; c1 = (w - sw)//2
        out[r0:r0+sh, c0:c0+sw] = img[r1:r1+sh, c1:c1+sw]
        img = out
    return img

# angular spectrum propagator (square grid, same sampling both planes)
def angular_spectrum_prop(u_in, wavelength, z, dx):
    """
    u_in: NxN complex field
    wavelength: scalar
    z: propagation distance (m)
    dx: pixel sampling (m)
    returns: u_out (NxN complex)
    """
    N = u_in.shape[0]
    k = 2*np.pi / wavelength
    fx = np.fft.fftfreq(N, d=dx)  # cycles per meter
    FX, FY = np.meshgrid(fx, fx)
    H = np.exp(1j * z * 2*np.pi * np.sqrt((1/wavelength**2) - (FX**2 + FY**2)))
    U1 = fft2(u_in)
    U2 = U1 * H
    u_out = ifft2(U2)
    return u_out

# -------------- main GS routine ----------------
def gerchberg_saxton(target_I, N, wavelength, dx, z, n_iter=200, slm_amp=1.0, quantize_bits=None):
    # target_I in [0,1]
    target_amp = np.sqrt(target_I)
    # initialize field at SLM plane: uniform amplitude, random phase
    rng = np.random.default_rng(0)
    phi = rng.random((N, N)) * 2*np.pi
    u_slm = slm_amp * np.exp(1j * phi)

    for i in range(n_iter):        
        if (i+1) % 1 == 0 or i==0:
            recon_I = np.abs(angular_spectrum_prop(u_slm, wavelength, z, dx))**2
            # normalize recon for monitoring
            recon_I /= recon_I.max()


            plt.imshow(recon_I, cmap='gray')
            plt.show()


            rmse = np.sqrt(np.mean((recon_I - target_I)**2))
        
        print(f"iter {i+1}/{n_iter}  RMSE={rmse:.5f}")
        # forward propagate
        u_img = angular_spectrum_prop(u_slm, wavelength, z, dx)
        # replace amplitude with target amplitude (keep phase)
        phase_img = np.angle(u_img)
        u_img = target_amp * np.exp(1j * phase_img)
        # back-propagate
        u_back = angular_spectrum_prop(u_img, wavelength, -z, dx)
        # enforce SLM amplitude constraint (phase-only)
        phi = np.angle(u_back)
        u_slm = slm_amp * np.exp(1j * phi)
        # optional: quantize phase
        if quantize_bits is not None:
            levels = 2**quantize_bits
            q = np.round((phi % (2*np.pi)) / (2*np.pi) * (levels-1)) / (levels-1) * 2*np.pi
            u_slm = slm_amp * np.exp(1j * q)



    return u_slm, recon_I

# ---------------- run example ----------------
if __name__ == "__main__":
    # choose resolution
    N = 512
    target = load_target(target_path, N)
    u_slm, recon_I = gerchberg_saxton(target, N, wavelength, pixel_pitch, prop_dist, n_iter=n_iter, slm_amp=slm_amp, quantize_bits=quantize_bits)

    # save phase pattern (kinoform)
    phase = np.angle(u_slm)
    # normalize to 0..255 and save
    phase_img = ((phase % (2*np.pi)) / (2*np.pi) * 255).astype(np.uint8)
    imageio.v2.imwrite("kinoform_phase.png", phase_img)
    print("Saved kinoform_phase.png")

    # show results
    plt.figure(figsize=(10,4))
    plt.subplot(1,3,1); plt.title("Target (norm)"); plt.imshow(target, cmap='gray'); plt.axis('off')
    plt.subplot(1,3,2); plt.title("Reconstruction"); plt.imshow(np.abs(angular_spectrum_prop(np.exp(1j * phase), wavelength, prop_dist, pixel_pitch))**2, cmap='gray'); plt.axis('off')
    plt.subplot(1,3,3); plt.title("SLM phase"); plt.imshow(phase, cmap='gray'); plt.axis('off')
    plt.tight_layout()
    plt.show()

