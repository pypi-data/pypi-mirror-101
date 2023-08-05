import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
from wizzi_utils import misc_tools as mt


def get_x_ticks_list(x_low, x_high, p=10):
    ten_percent_jump = (x_high - x_low) / p
    x_ticks = [x_low + i * ten_percent_jump for i in range(p + 1)]
    return x_ticks


def plot_2d_subplots_start(rows: int = 1, cols: int = 1, main_title: str = None):
    plt.close('all')

    fig, ax_item_or_tuple_or_arr = plt.subplots(nrows=rows, ncols=cols, sharex=False, sharey=False)
    if main_title is not None:
        fig.suptitle(main_title)
    return fig, ax_item_or_tuple_or_arr


def plot_2d_add_subplot(ax: Axes, points_groups: list, sub_title: str = None,
                        label_x: str = 'x', label_y: str = 'y', add_center: bool = False):
    """
    e.g:
    A = np.random.randint(low=-10, high=10, size=(10, 2))
    C = np.random.randint(low=-10, high=10, size=(5, 2))
    U = np.random.randint(low=-10, high=10, size=(5, 2))
    V = np.random.randint(low=-10, high=10, size=(5, 2))
    Q = np.random.randint(low=-10, high=10, size=(5, 2))

    g_A = (A, 'g', 'A')
    g_C = (C, 'r', 'C')
    g_U = (U, 'b', 'U')
    g_V = (V, 'aqua', 'V')
    g_Q = (Q, 'darkviolet', 'trainQ')

    # 1x1
    fig, ax = plot_2d_subplots_start(main_title='1x1')  # 1 row, 2 cols
    plot_2d_add_subplot(ax=ax, points_groups=[g_A, g_C, g_Q], sub_title='1', add_center=True)
    plot_2d_subplots_end(f=fig, zoomed=False)

    # 1x2
    fig, ax_tuple = plot_2d_subplots_start(cols=2, main_title='1x2')  # 1 row, 2 cols
    plot_2d_add_subplot(ax=ax_tuple[0], points_groups=[g_A, g_C], sub_title='1', add_center=True)
    plot_2d_add_subplot(ax=ax_tuple[1], points_groups=[g_A, g_C, g_U], sub_title='2', add_center=True)
    plot_2d_subplots_end(f=fig, zoomed=True)

    # 2x1
    fig, ax_tuple = plot_2d_subplots_start(rows=2, main_title='2x1')  # 2 rows, 1 col
    plot_2d_add_subplot(ax=ax_tuple[0], points_groups=[g_A, g_C], sub_title='1', add_center=True)
    plot_2d_add_subplot(ax=ax_tuple[1], points_groups=[g_A, g_C, g_U, g_V], sub_title='2', add_center=True)
    plot_2d_subplots_end(f=fig, zoomed=True)

    # 2x2
    fig, ax_arr = plot_2d_subplots_start(rows=2, cols=2, main_title='2x2')  # 2x2 subplots
    plot_2d_add_subplot(ax=ax_arr[0][0], points_groups=[g_A, g_U], sub_title='1', add_center=False)
    plot_2d_add_subplot(ax=ax_arr[0][1], points_groups=[g_A, g_U], sub_title='2', add_center=True)
    plot_2d_add_subplot(ax=ax_arr[1][0], points_groups=[g_A, g_V], sub_title='3', add_center=True)
    plot_2d_add_subplot(ax=ax_arr[1][1], points_groups=[g_A, g_C, g_U, g_V], sub_title='4', add_center=False)
    plot_2d_subplots_end(f=fig, zoomed=True)
    """
    assert points_groups is not None, 'need at least 1 group'

    # casting to numpy if torch and checking d==2
    if points_groups is not None:
        for i in range(len(points_groups)):
            A, color, lbl = points_groups[i]
            assert len(A.shape) > 1 and A.shape[1] == 2, 'A is not valid or d!=1. {}: A.shape={}'.format(lbl, A.shape)

    all_points = np.empty((0, 2), dtype=float)

    for point_group in points_groups:
        A, color, lbl = point_group
        X, y = mt.de_augment_numpy(A)
        ax.scatter(X, y, color=color, marker='.', label=lbl)
        all_points = np.concatenate((all_points, A), axis=0)

    if add_center:
        from wizzi_utils import algorithms as algs
        from scipy.spatial import distance
        centers = algs.find_centers(all_points, k=1)
        distance_mat = distance.cdist(centers, all_points, 'euclidean')
        rad = max(distance_mat[0])
        ax.scatter(centers[0][0], centers[0][1], color='orange', marker='o', label='center')
        circle_cover = plt.Circle(xy=(centers[0][0], centers[0][1]), radius=rad, color='orange', fill=False,
                                  linewidth=0.5)
        ax.add_artist(circle_cover)
    ax.grid()
    ax.legend(loc='upper right', ncol=1, fancybox=True, framealpha=0.5, edgecolor='black')
    if sub_title is not None:
        ax.set_title(sub_title)
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)

    all_points_x, all_points_y = mt.de_augment_numpy(all_points)
    min_x, max_x = min(all_points_x), max(all_points_x)
    min_y, max_y = min(all_points_y), max(all_points_y)
    ax.set_xticks(get_x_ticks_list(min_x, max_x, p=3))
    ax.set_yticks(get_x_ticks_list(min_y, max_y, p=3))
    ten_p_diff_x = (max_x - min_x) / 10
    ten_p_diff_y = (max_y - min_y) / 10
    ax.set_xlim(min_x - ten_p_diff_x, max_x + ten_p_diff_x)
    ax.set_ylim(min_y - ten_p_diff_y, max_y + ten_p_diff_y)
    ax.margins(0.1)
    return


def plot_2d_subplots_end(save_path: str = None, show_plot: bool = True, f: Figure = None, hspace: float = 0.3,
                         wspace: float = 0.3, dpi=200, zoomed: bool = False):
    if f is not None:
        f.subplots_adjust(hspace=hspace, wspace=wspace)
    if save_path is not None:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        print('\tsaved to {}.png'.format(save_path))
    if show_plot:
        if zoomed:
            wm = plt.get_current_fig_manager()
            wm.window.state('zoomed')
        plt.show()
    plt.cla()
    return


def plot_2d_scatter(groups: list, title: str = '', label_x: str = 'x', label_y: str = 'y', add_center: bool = False,
                    save_path: str = None, show_plot: bool = True, zoomed: bool = False):
    """
    np.random.seed(42)
    A = np.random.randint(low=-10, high=10, size=(10, 2))
    C = np.random.randint(low=-10, high=10, size=(5, 2))
    g_A = (A, 'g', 'A')
    g_C = (C, 'r', 'C')
    plot_2d_scatter(groups=[g_A, g_C], title='scatter', zoomed=True, add_center=True)
    """
    fig, ax = plot_2d_subplots_start(1, 1)
    plot_2d_add_subplot(ax=ax, points_groups=groups, sub_title=title, label_x=label_x,
                        label_y=label_y, add_center=add_center)
    plot_2d_subplots_end(save_path=save_path, show_plot=show_plot, zoomed=zoomed)
    return


def plot_x_y_std(data_x: np.array, groups: list, title: str = None, x_label: str = 'Size', y_label: str = 'Error',
                 save_path: str = None, show_plot: bool = True, with_shift: bool = False):
    """
    data_x: x values
    groups: list of groups s.t. each tuple(y values, y std, color, title)  y std could be None
    example:
        data_x = [10, 20, 30]
        C_errors = [5, 7, 1]
        C_errors_stds = [2, 1, 0.5]
        group_c = (C_errors, C_errors_stds, 'g', 'C')
        U_errors = [10, 8, 3]
        U_errors_vars = [4, 3, 1.5]
        group_u = (U_errors, U_errors_vars, 'r', 'U')
        groups = [group_c, group_u]
        title = 'bla'
        plot_x_y_std(data_x, groups, title)
    :return:
    """
    data_x_last = data_x  # in order to see all STDs, move a little on the x axis
    data_x_jump = 0.5
    data_x_offset = - int(len(groups) / 2) * data_x_jump
    line_style = {"linestyle": "-", "linewidth": 1, "markeredgewidth": 2, "elinewidth": 1, "capsize": 4}
    for i, group in enumerate(groups):
        data_y, std_y = group[0], group[1]  # std_y could be None
        color, label = group[2], group[3]
        if with_shift:  # move x data for each set a bit so you can see it clearly
            dx_shift = [x + i * data_x_jump + data_x_offset for x in data_x]
            data_x_last = dx_shift
        plt.errorbar(data_x_last, data_y, std_y, color=color, fmt='.', label=label, **line_style)

    plt.grid()
    plt.legend(loc='upper right', ncol=1, fancybox=True, framealpha=0.5)
    if title is not None:
        plt.title(title)
    plt.xticks(data_x)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if save_path is not None:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print('\tsaved to {}.png'.format(save_path))
    plt.pause(0.0001)
    if show_plot:
        plt.show(block=True)
    plt.cla()
    return


def histogram(values: np.array, title: str, save_path: str = None, show_hist: bool = True, bins_n: int = 50):
    """ plots a histogram """
    # print(sum(values), values.tolist())
    # plt.hist(values, bins=50, facecolor='green', alpha=0.75, range=(values.min(), values.max()))
    # count_in_each_bin, bins, patches = plt.hist(values, bins_n, density=False, facecolor='blue', alpha=0.75)
    plt.hist(values, bins_n, density=False, facecolor='blue', alpha=0.75)
    # print(count_in_each_bin, bins, patches[0])
    # print(list_1d_to_str(count_in_each_bin))

    plt.xlabel('Values')
    plt.ylabel('Bin Count')
    plt.title(title)
    plt.grid(True)
    if save_path is not None:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print('\tsaved to {}.png'.format(save_path))
    if show_hist:
        plt.show()
    plt.cla()
    return


def compare_images_sets(set_a, set_b, title: str = None):
    """
    build for images BEFORE transform:
    notice images should be in the format:
        gray scale mnist: [number of images, 28, 28]
        RGB  Cifar10    : [number of images, 32, 32, 3]

    :param set_a: array (nd\torch) of images
    :param set_b: array (nd\torch) of images
    :param title: plot title
    plot set a of images in row 1 and set b in row 2
    set_a and set_b can be ndarray or torch arrays
    example:
        from torchvision import datasets
        # choose data set - both work
        # data_root = path to the data else download
        data_root = '../../2019SGD/Datasets/'
        # dataset = datasets.MNIST(root=data_root, train=False, download=False)
        dataset = datasets.CIFAR10(root=data_root, train=False, download=False)
        set_a = dataset.data[:3]
        set_b = dataset.data[10:50]
        compare_images_sets(set_a, set_b)
        set_a = dataset.data[0:3]
        set_b = dataset.data[0:3]
        compare_images_sets(set_a, set_b)
    """
    n_cols = max(set_a.shape[0], set_b.shape[0])
    fig, axes = plt.subplots(nrows=2, ncols=n_cols, sharex='all', sharey='all', figsize=(15, 4))
    for images, row in zip([set_a, set_b], axes):
        for img, ax in zip(images, row):
            ax.imshow(np.squeeze(img), cmap='gray')
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
    if title is not None:
        plt.title(title)
    plt.show()
    return


def compare_images_multi_sets_squeezed(sets_dict: dict, title: str = None) -> str:
    """
    build for images AFTER transform:
    notice images should be in the format:
        gray scale mnist: [number of images, 1, 28, 28]
        RGB  Cifar10    : [number of images, 3, 32, 32]

    :param sets_dict: each entry in dict is title, set of images(np/tensor)
    :param title: for plot
    :return str with details which set in each row
    plot sets of images in rows
    example:
        import torch
        from torchvision import datasets
        import torchvision.transforms as transforms
        transform = transforms.Compose([transforms.ToTensor(), ])
        # choose data set - both work
        # data_root = path to the data else download
        data_root = '../../2019SGD/Datasets/'
        # dataset = datasets.MNIST(root=data_root, train=False, download=False, transform=transform)
        dataset = datasets.CIFAR10(root=data_root, train=False, download=False, transform=transform)
        data_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True, num_workers=2)
        images32, labels = iter(data_loader).next()

        images = images32[:16]  # imagine the first 16 are base images and predicted_images are the model output
        predicted_images = images32[16:32]
        d = {'original_data': images, 'predicted_data': predicted_images}
        print(compare_images_multi_sets_squeezed(d))
    """
    from wizzi_utils import torch_tools as tt
    from torchvision.utils import make_grid
    import torch
    for k, v in sets_dict.items():
        if isinstance(sets_dict[k], np.ndarray):
            sets_dict[k] = tt.numpy_to_torch(sets_dict[k])

    all_sets = None
    msg = ''
    set_len = 0
    msg_base = 'row {}: {}, '

    for i, (k, v) in enumerate(sets_dict.items()):
        all_sets = v if all_sets is None else torch.cat((all_sets, v), 0)
        msg += msg_base.format(i, k)
        set_len = v.shape[0]

    grid_images = make_grid(all_sets, nrow=set_len)
    if title is not None:
        plt.title(title)
    plt.axis('off')
    plt.imshow(np.transpose(tt.torch_to_numpy(grid_images), (1, 2, 0)))
    plt.show()
    return msg


def add_3d_subplot(ax: Axes, X: np.array, title: str = '3dplot', label: str = 'some label', marker: str = '.',
                   markersize: int = 50, color: str = 'red'):
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], color=color, marker=marker, s=markersize, alpha=1,
               label='{}({} blobs)'.format(label, X.shape[0]))

    ax.legend()
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    # noinspection PyUnresolvedReferences
    ax.set_zlabel('Z Label')
    ax.set_title(title)
    return


def plot3d_scatters(scatters: list, zoomed: bool = True, main_title: str = None) -> None:
    """
    dim_3d = 3

    sc1 = {
        'A': np.random.randint(low=-10, high=10, size=(20, dim_3d)),
        'title': 'P',
        'label': 'randomP',
        'color': 'r',
        'marker': 'o',
        'markersize': 50,
    }
    sc2 = {
        'A': np.random.randint(low=-10, high=10, size=(5, dim_3d)),
        'title': 'C',
        'label': 'randomC',
        'color': 'g',
        'marker': '.',
        'markersize': 50,
    }
    sc3 = {
        'A': np.random.randint(low=-10, high=10, size=(5, dim_3d)),
        'title': 'Q',
        'label': 'randomQ',
        'color': 'b',
        'marker': 'x',
        'markersize': 50,
    }

    scs = [sc1, sc2, sc3]
    plot3d_scatters(scs, zoomed=True, main_title='3d example')
    """

    fig = plt.figure()
    for i, sc in enumerate(scatters):
        ax = fig.add_subplot(1, len(scatters), i + 1, projection='3d')
        add_3d_subplot(ax, sc['A'], sc['title'], sc['label'], sc['marker'], sc['markersize'], sc['color'])
    if main_title is not None:
        fig.suptitle(main_title)
    if zoomed:
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')
    plt.show()
    return


def plot3d_scatter(X: np.array, title: str = '3dplot', label: str = 'some label', marker: str = '.',
                   markersize: int = 50, color: str = 'red'):
    """
    dim_3d = 3
    X = np.random.randint(low=-10, high=10, size=(20, dim_3d))  # must be 3d
    plot3d_scatter(X, title='3dplot', label='random', marker='o')
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    add_3d_subplot(ax, X, title, label, marker, markersize, color)
    plt.show()
    return


def main():
    return


if __name__ == '__main__':
    main()
