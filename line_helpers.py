import numpy as np

def get_slope(lines, eps=1e-7):
    '''
    @param lines is a numpy array with shape (n, 4)
    where n is the number of the lines and each line
    element has four attributes- x1, y1, x2, y2 in this order.
    Calculates the slope using eqn: (x2-x1)/(y2-y1)
    @param eps is for numerical stability. If None, takes machine epsilon
    '''
    if eps is None:
        eps = np.finfo(np.float32).eps
    xdiff = lines[:,2] - lines[:,0] + eps # x2 - x1 + eps[to avoid division by zero]
    return np.divide((lines[:,3] - lines[:,1]), xdiff, where= xdiff != 0)

def slope_mask(lines, _max=None, _min=None, eps=1e-7):
    '''
    @param lines is a numpy array with shape (n, 4)
    where n is the number of the lines and each line
    element has four attributes- x1, y1, x2, y2 in this order.
    '''
    mask = np.ones([lines.shape[0]]).astype(np.bool)
    m = get_slope(lines, eps=eps)
    if _max is not None:
        mask = np.logical_and(mask, m < _max)
    if _min is not None:
        mask = np.logical_and(mask, m > _min)
    return mask

def grouper(bool_mask):
    '''
    Returns the undirected graphs from a connection matrix.
    The connection matrix is represented as a boolean matrix in @param bool_mask.
    '''
    rr = bool_mask
    start = [x for x in range(0, rr.shape[0])]
    to_explore = []
    groups = []
    visited = []
    for i in start:
        if i in visited:
            # if i is already visited then skip the process
            continue
        visited.append(i)
        to_explore = []
        t = np.nonzero(rr[:, i])[0]
        if t.shape[0] != 0:
            to_explore.extend(list(t))
        for j in to_explore:
            if j in visited:
                continue
            visited.append(j)
            t = np.nonzero(rr[:, j])[0]
            if t.shape[0] != 0:
                to_explore.extend(list(t))
        to_explore.append(i)
        groups.append(set(to_explore))   
    return groups

def grp_endpoints(lines, radius=5):
    '''
    Groups line segments @param lines, if their end points are nearby within a @param radius(not inclusive).
    Returns the grouping in a boolean matrix
    '''
    # Circular grouping
    x_vec = np.hstack([lines[:, 0], lines[:,2]])
    y_vec = np.hstack([lines[:, 1], lines[:,3]])

    circ_x_mat = np.ones([x_vec.shape[0], x_vec.shape[0]]) * x_vec
    circ_y_mat = np.ones([y_vec.shape[0], y_vec.shape[0]]) * y_vec
    circ_x_mat = circ_x_mat - circ_x_mat.T
    circ_y_mat = circ_y_mat - circ_y_mat.T
    _circ_mask = circ_x_mat**2 + circ_y_mat**2 < radius ** 2 # eqn circle- (x - centerx)2 + (y - centery)2 < (radius)2

    _limit = x_vec.shape[0] //2
    circ_mask = _circ_mask[:_limit, :_limit] + _circ_mask[_limit:, :_limit] + _circ_mask[_limit:, _limit:]

    f_circ_mask = np.zeros_like(circ_mask, dtype=bool)
    f_circ_mask[np.tril_indices(circ_mask.shape[0], -1)] = (circ_mask + circ_mask.T)[np.tril_indices(circ_mask.shape[0], -1)]
    return f_circ_mask

def grp_angle_btwn(lines, angle_threshold=30, eps=1e-7):
    '''
    Group line segment, @param lines, by thresholding @param angle_threshold on the angles between them.
    @param angle_threshold is in degrees
    Eqn used is arctan((m1 - m2) / (1 - m1 * m2))
    '''
    orient_lm_rad = np.radians(angle_threshold)

    # Orientation grouping
    slope_vec = np.divide((lines[:,3] - lines[:,1]),(lines[:,2] - lines[:,0]) + eps)
    slope_mat = np.ones([slope_vec.shape[0], slope_vec.shape[0]]) * slope_vec
    orientation = np.arctan((slope_mat - slope_mat.T) / (1 - slope_mat * slope_mat.T))
    _orient = abs(orientation)

    orientation_mask = np.zeros_like(_orient)
    orientation_mask[np.tril_indices(orientation_mask.shape[0], -1)] = _orient[np.tril_indices(orientation_mask.shape[0], -1)] < orient_lm_rad
    orientation_mask = orientation_mask.astype(np.bool)
    return orientation_mask

def grp_filter_length(lines, groups, threshold, return_length_sum=False):
    '''
    Filter groups @param groups, of line segments @param lines by thresholding @param threshold
    on the sum of the length of lines segments in each group.
    If @param return_length_sum is True, returns the sum of squares of the length of line segments.
    '''
    _grps = np.array(groups)
    grp_sum = []
    for igrp in _grps:
        ll = lines[list(igrp)]
        length = np.square(ll[:,0] - ll[:,2]) + np.square(ll[:,1] - ll[:,3])
        grp_sum.append(np.sum(length))
    grp_sum = np.array(grp_sum)
    filtered_grp = list(_grps[grp_sum > threshold])
    if return_length_sum:
        return filtered_grp, grp_sum
    return filtered_grp

def grp_filter_count(groups, threshold):
    '''
    Filters the @param groups by thresholding @param threshold on the count of lines in each group.
    '''
    return list(filter(lambda x: len(x)>=threshold, groups))

def allcorrect():
    lines = [[200, 100, 300, 200], [200, 300, 200, 400], [200, 300, 400, 300]]
    slopes = [1, 100 / np.finfo(np.float32).eps, 0]
    lines = np.array(lines)
    slopes = np.array(slopes)
    assert np.allclose(get_slope(lines, eps=None), slopes)

    smask = np.array([True, False, False])
    assert np.allclose(slope_mask(lines, _max=3, _min=0, eps=None), smask)
    
    bool_mask = np.zeros([6,6]).astype(np.bool)    
    bool_mask[np.diag_indices(6)] = True    
    bool_mask[0, 1] = True
    bool_mask[1, 4] = True
    bool_mask[2, 3] = True
    bool_mask = np.logical_or(bool_mask, bool_mask.T)
    grps = np.array([{0, 1, 4}, {2, 3}, {5}])
    assert grouper(bool_mask), grps
    
    grp_endpoints_lines = np.array([[50, 50, 70, 70], [74, 75, 100, 100], [200, 200, 300, 300]])
    assert np.allclose(grp_endpoints(grp_endpoints_lines, radius=7),\
                       np.array([[False, False, False],\
                                 [ True, False, False],\
                                 [False, False, False]]))
    
    grp_angle_lines = np.array([[50, 50, 70, 70], [71, 75, 60, 60], [200, 200, 300, 300]])
    assert np.allclose(grp_angle_btwn(grp_angle_lines, angle_threshold=40),\
                       np.array([[False, False, False],\
                                 [ False, False, False],\
                                 [True, False, False]]))
    
    emap = grp_endpoints(grp_endpoints_lines, radius=7)
    assert grp_filter_length(lines=grp_endpoints_lines, groups=grouper(emap), threshold=10000, return_length_sum=False), [{2}]
    
    assert grp_filter_count(grouper(emap), 2), [{0, 1}]
    # print("All OK.")
    return True
