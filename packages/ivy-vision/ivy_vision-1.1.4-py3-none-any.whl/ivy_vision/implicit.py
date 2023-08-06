# global
import ivy
import math
import numpy as np


def sinusoid_positional_encoding(x, embedding_length=10):
    """
    Perform sinusoid positional encoding of the inputs.

    :param x: input array to encode *[batch_shape, dim]*
    :type x: array
    :param embedding_length: Length of the embedding. Default is 10.
    :type embedding_length: int, optional
    :return: The new positionally encoded array *[batch_shape, dim+dim*2*embedding_length]*
    """
    rets = [x]
    for i in range(embedding_length):
        for fn in [ivy.sin, ivy.cos]:
            rets.append(fn(2.**i * x))
    return ivy.concatenate(rets, -1)


# noinspection PyUnresolvedReferences
def sampled_volume_density_to_occupancy_probability(density, inter_sample_distance):
    """
    Compute probability of occupancy, given sampled volume densities and their associated inter-sample distances

    :param density: The sampled density values *[batch_shape]*
    :type density: array
    :param inter_sample_distance: The inter-sample distances *[batch_shape]*
    :type inter_sample_distance: array
    :return: The occupancy probabilities *[batch_shape]*
    """
    return 1 - ivy.exp(-density*inter_sample_distance)


def ray_termination_probabilities(density, inter_sample_distance):
    """
    Compute probability of occupancy, given sampled volume densities and their associated inter-sample distances

    :param density: The sampled density values *[batch_shape,num_samples_per_ray]*
    :type density: array
    :param inter_sample_distance: The inter-sample distances *[batch_shape,num_samples_per_ray]*
    :type inter_sample_distance: array
    :return: The occupancy probabilities *[batch_shape]*
    """

    # BS x NSPR
    occ_prob = sampled_volume_density_to_occupancy_probability(density, inter_sample_distance)
    return occ_prob * ivy.cumprod(1. - occ_prob + 1e-10, -1, exclusive=True)


# noinspection PyUnresolvedReferences
def stratified_sample(starts, ends, num_samples, batch_shape=None):
    """
    Perform stratified sampling, between start and end arrays. This operation divides the range into equidistant bins,
    and uniformly samples value within the ranges for each of these bins.

    :param starts: Start values *[batch_shape]*
    :type starts: array
    :param ends: End values *[batch_shape]*
    :type ends: array
    :param num_samples: The number of samples to generate between starts and ends
    :type num_samples: int
    :param batch_shape: Shape of batch, Inferred from inputs if None.
    :type batch_shape: sequence of ints, optional
    :return: The stratified samples, with each randomly placed in uniformly spaced bins *[batch_shape,num_samples]*
    """

    # shapes
    if batch_shape is None:
        batch_shape = starts.shape

    # shapes as lists
    batch_shape = list(batch_shape)

    # BS
    bin_sizes = (ends - starts)/num_samples

    # BS x NS
    linspace_vals = ivy.linspace(starts, ends - bin_sizes, num_samples)

    # BS x NS
    random_uniform = ivy.random_uniform(shape=batch_shape + [num_samples], dev_str=ivy.dev_str(starts))

    # BS x NS
    random_offsets = random_uniform * ivy.expand_dims(bin_sizes, -1)

    # BS x NS
    return linspace_vals + random_offsets


# noinspection PyUnresolvedReferences
def render_rays_via_termination_probabilities(ray_term_probs, features, render_variance=False):
    """
    Render features onto the image plane, given rays sampled at radial depths with readings of
    feature values and densities at these sample points.

    :param ray_term_probs: The ray termination probabilities *[batch_shape,num_samples_per_ray]*
    :type ray_term_probs: array
    :param features: Feature values at the sample points *[batch_shape,num_samples_per_ray,feat_dim]*
    :type features: array
    :param render_variance: Whether to also render the feature variance. Default is False.
    :type render_variance: bool, optional
    :return: The feature renderings along the rays, computed via the termination probabilities *[batch_shape,feat_dim]*
    """

    # BS x NSPR
    rendering = ivy.reduce_sum(ivy.expand_dims(ray_term_probs, -1) * features, -2)
    if not render_variance:
        return rendering
    var = ivy.reduce_sum(ray_term_probs*(ivy.expand_dims(rendering, -2) - features)**2, -2)
    return rendering, var


def render_implicit_features_and_depth(network_fn, rays_o, rays_d, near, far, samples_per_ray, render_variance=False,
                                       batch_size_per_query=512*64, inter_feat_fn=None, v=None):
    """
    Render an rgb-d image, given an implicit rgb and density function conditioned on xyz data.

    :param network_fn: the implicit function.
    :type network_fn: callable
    :param rays_o: The camera center *[batch_shape,3]*
    :type rays_o: array
    :param rays_d: The rays in world space *[batch_shape,ray_batch_shape,3]*
    :type rays_d: array
    :param near: The near clipping plane values *[batch_shape,ray_batch_shape]*
    :type near: array
    :param far: The far clipping plane values *[batch_shape,ray_batch_shape]*
    :type far: array
    :param samples_per_ray: The number of stratified samples to use along each ray
    :type samples_per_ray: int
    :param render_variance: Whether to also render the feature variance. Default is False.
    :type render_variance: bool, optional
    :param batch_size_per_query: The maximum batch size for querying the implicit network. Default is 1024.
    :type batch_size_per_query: int, optional
    :param inter_feat_fn: Function to extract interpolated features from world-coords *[batch_shape,ray_batch_shape,3]*
    :type inter_feat_fn: callable, optional
    :param v: The container of trainable variables for the implicit model. default is to use internal variables.
    :type v: ivy Container of variables
    :return: The rendered feature *[batch_shape,ray_batch_shape,feat]* and depth *[batch_shape,ray_batch_shape,1]* values
    """

    # shapes
    batch_shape = list(near.shape)
    flat_batch_size = np.prod(batch_shape)
    num_sections = math.ceil(flat_batch_size*samples_per_ray/batch_size_per_query)

    # Compute 3D query points

    # BS x SPR x 1
    z_vals = ivy.expand_dims(stratified_sample(near, far, samples_per_ray), -1)

    # BS x 1 x 3
    rays_d = ivy.expand_dims(rays_d, -2)
    rays_o = ivy.broadcast_to(rays_o, rays_d.shape)

    # BS x SPR x 3
    pts = rays_o + rays_d * z_vals

    # (BSxSPR) x 3
    pts_flat = ivy.reshape(pts, (flat_batch_size*samples_per_ray, 3))

    # batch
    # ToDo: use a more general batchify function, from ivy core

    # num_sections size list of BSPQ x 3
    pts_split = [pts_flat[i*batch_size_per_query:min((i+1)*batch_size_per_query, flat_batch_size*samples_per_ray)]
                 for i in range(num_sections)]
    if inter_feat_fn is not None:
        # (BSxSPR) x IF
        features = ivy.reshape(inter_feat_fn(pts), (flat_batch_size*samples_per_ray, -1))
        # num_sections size list of BSPQ x IF
        feats_split =\
            [features[i * batch_size_per_query:min((i + 1) * batch_size_per_query, flat_batch_size*samples_per_ray)]
             for i in range(num_sections)]
    else:
        feats_split = [None]*num_sections

    # Run network

    # num_sections size list of tuple of (BSPQ x OF, BSPQ)
    feats_n_densities = [network_fn(pt, f) for pt, f in zip(pts_split, feats_split)]

    # BS x SPR x OF
    feat = ivy.reshape(ivy.concatenate([item[0] for item in feats_n_densities], 0),
                       batch_shape + [samples_per_ray, -1])

    # FBS x SPR
    densities = ivy.reshape(ivy.concatenate([item[1] for item in feats_n_densities], 0),
                            batch_shape + [samples_per_ray])

    # BS x (SPR+1)
    z_vals_w_terminal = ivy.concatenate((z_vals[..., 0], ivy.ones_like(z_vals[..., -1:, 0])*1e10), -1)

    # BS x SPR
    depth_diffs = z_vals_w_terminal[..., 1:] - z_vals_w_terminal[..., :-1]
    ray_term_probs = ray_termination_probabilities(densities, depth_diffs)

    # BS x OF
    feat = ivy.clip(render_rays_via_termination_probabilities(ray_term_probs, feat, render_variance), 0., 1.)

    # BS x 1
    depth = render_rays_via_termination_probabilities(ray_term_probs, z_vals, render_variance)
    if render_variance:
        # BS x OF, BS x OF, BS x 1, BS x 1
        return feat[0], feat[1], depth[0], depth[1]
    # BS x OF, BS x 1
    return feat, depth
