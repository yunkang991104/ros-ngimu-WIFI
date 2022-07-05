import numpy as np

def low_pass_filter(x_meas, x_esti):
    """Calculate average sonar using a low-pass filter."""
    alpha = 0.8
    x_esti = alpha * x_esti + (1 - alpha) * x_meas
    return x_esti

if __name__ == "__main__":

    x_esti = lpf.low_pass_filter(x_meas, x_esti)

    x_esti_list.append(x_esti)