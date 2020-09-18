import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def normalize(array: np.ndarray, axis):
    return array / np.linalg.norm(array, ord=2, axis=axis,
                                           keepdims=True)


def normalize_rows(array: np.ndarray):
    return normalize(array, 1)


def normalize_cols(array: np.ndarray):
    return normalize(array, 0)


def get_distances_matrix(position_array: np.ndarray):
    normalized_positions = normalize_rows(position_array)
    entries = position_array.shape[0]
    dimensions = position_array.shape[1]
    distance_matrix = np.zeros((entries, entries))
    for i in range(entries):
        coord_difference = normalized_positions - normalized_positions[i].reshape((1, dimensions))
        cart_distance = np.linalg.norm(coord_difference, ord=2, axis=1)
        distance_matrix[i] = 2 * np.arcsin(cart_distance / 2)
    return distance_matrix


def find_args_of_pot_cross_pts(distance_matrix: np.ndarray):
    sorted_matrix = np.argsort(distance_matrix, axis=0)
    sorted_matrix -= np.arange(sorted_matrix.shape[0])
    potential_cross_pts = np.where(abs(sorted_matrix[0:5]) > 3)[1]
    unique_potential_cross_pts = np.unique(potential_cross_pts)
    return unique_potential_cross_pts


def find_cross_pts(distance_matrix: np.ndarray):
    unq_cross_pt = find_args_of_pot_cross_pts(distance_matrix)
    pot_cross_pt_rows = distance_matrix[unq_cross_pt]
    sorted_pot_cross_pt = np.sort(pot_cross_pt_rows, axis=1)[:,0:5]
    sum_of_dist = np.sum(sorted_pot_cross_pt, axis=1)
    probable_cross_pts = unq_cross_pt[np.argsort(sum_of_dist)]

    return probable_cross_pts


def find_extrema(distance_matrix: np.ndarray, probable_cross_pts: np.ndarray):
    cross_point = probable_cross_pts[1]
    distances = distance_matrix[cross_point]
    distance_derivative = distances - np.roll(distances, -1)
    derivative_sign_change = distance_derivative * np.roll(distance_derivative, +1)
    arg_with_sign_change = np.where(derivative_sign_change < 0)
    excluded_pts = np.append(probable_cross_pts, [0, distance_matrix.shape[0]])
    arg_not_cross = ~np.isin(arg_with_sign_change, excluded_pts)[0]
    extrema_args = arg_with_sign_change[0][arg_not_cross]
    return extrema_args


def get_retardation(data):
    dis_mat = get_distances_matrix(data)
    probable_cross_pts = find_cross_pts(dis_mat)
    extrema_args = find_extrema(dis_mat, probable_cross_pts)

    data = normalize_rows(data)
    first_extremum_coords = data[extrema_args[0]]
    second_extremum_coords = data[extrema_args[1]]
    distance_between_extrema = np.linalg.norm(second_extremum_coords - first_extremum_coords,
                                              ord=2)

    retardation = np.arcsin(distance_between_extrema / 2) / (2 * np.pi)
    print("Retardation: {:.4f} or {:.4f} wave".format(retardation, 0.5 - retardation))
    return probable_cross_pts[0], extrema_args[0], extrema_args[1]


def stokes_from_power(data):
    stokes = np.zeros((data.shape[0], 3))
    stokes[:, 0] = (data[:, 1] - data[:, 0]) / (data[:, 1] + data[:, 0])
    stokes[:, 1] = (data[:, 3] - data[:, 2]) / (data[:, 3] + data[:, 2])
    stokes[:, 2] = -(data[:, 5] - data[:, 4]) / (data[:, 5] + data[:, 4])
    return stokes

# data = np.genfromtxt("test_data/qwp.tsv")
# get_retardation(data)
def temp(r):
    filename = "../output/2020-09-08/measurements/{}mm/qwpPowers1.tsv".format(r)
    powers = np.genfromtxt(filename)
    data = stokes_from_power(powers)
    print("Radius: {} mm".format(r))
    get_retardation(data)

def temp2(r):
    filename = "../output/old_stokes/{} mm/qwp1.tsv".format(r)
    powers = np.genfromtxt(filename)
    data = stokes_from_power(powers)
    print("Radius: {} mm".format(r))
    get_retardation(data)

print("Older results:")
temp2(13)
temp2(14)
print("Newer results:")
temp(14)
temp(14.25)
temp(14.5)
temp(14.75)
temp(15)
print("Older results:")
temp2(15)
temp2(16)


def fit_func(x: np.ndarray, a):
    return a / x

def make_plot():
    old_results = np.array([[13, 0.2798], [14, 0.2654], [15, 0.2387], [16, 0.2265]])
    new_results = np.array([[14, 0.2810], [14.25, 0.2579], [14.5, 0.2679], [14.75, 0.2458], [15, 0.2330]])
    all_results = np.append(old_results, new_results, axis=0)
    all_results = all_results[np.argsort(all_results[:, 0]).reshape(1, all_results.shape[0])]

    radii = all_results[0, :, 0]
    retardation = all_results[0:, :, 1][0]

    popt, pcov = curve_fit(fit_func, radii, retardation, p0=[4])
    radii_lin = np.linspace(radii.min(), radii.max(), 50)
    retardation_lin = fit_func(radii_lin, *popt)

    plt.figure(figsize=(4,3), dpi=300)
    plt.grid(alpha=0.2)
    plt.plot(radii_lin, retardation_lin, c="k", label="Model fit")
    plt.scatter(old_results[:, 0], old_results[:, 1], c="g", label="Crude step")
    plt.scatter(new_results[:, 0], new_results[:, 1], c="b", label="Fine step")
    plt.legend()
    plt.xlabel("Radius of the paddle [mm]")
    plt.ylabel("Retardation [waves]")
    plt.text(13, 0.24, "Fitted function:\na/x with \na = {:.2f}".format(*popt))
    plt.tight_layout()
    plt.savefig("retardation.png", dpi=300)
    print(popt)

make_plot()
