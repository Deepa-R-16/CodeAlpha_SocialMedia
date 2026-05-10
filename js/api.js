const BASE = 'http://127.0.0.1:8000/api';

async function apiCall(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('access_token');
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const options = { method, headers };

    if (body instanceof FormData) {
        options.body = body;
    } else if (body) {
        headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(body);
    }

    try {
        const res = await fetch(BASE + endpoint, options);

        if (res.status === 401) {
            localStorage.clear();
            window.location.href = '/frontend/pages/index.html';
            return null;
        }

        const data = await res.json();

        if (!res.ok) {
            return { __error: true, status: res.status, ...data };
        }

        return data;

    } catch (err) {
        console.error('Network error on', endpoint, ':', err.message);
        return {
            __error: true,
            __network: true,
            detail: 'Cannot connect to server. Make sure backend is running at ' + BASE
        };
    }
}

export const register          = d      => apiCall('/auth/register/', 'POST', d);
export const login             = d      => apiCall('/auth/login/', 'POST', d);
export const getMe             = ()     => apiCall('/auth/me/');
export const updateProfile     = d      => apiCall('/auth/profile/update/', 'PATCH', d);
export const followUser        = id     => apiCall(`/auth/follow/${id}/`, 'POST');
export const unfollowUser      = id     => apiCall(`/auth/follow/${id}/`, 'DELETE');
export const searchUsers       = q      => apiCall(`/auth/search/?q=${encodeURIComponent(q)}`);
export const getSuggestedUsers = ()     => apiCall('/auth/users/suggest/');
export const getUserById       = id     => apiCall(`/auth/users/${id}/`);
export const forgotPassword    = email  => apiCall('/auth/forgot-password/', 'POST', { email });
export const resetPassword     = d      => apiCall('/auth/reset-password/', 'POST', d);

export const getFeed           = (p=1)  => apiCall(`/posts/feed/?page=${p}`);
export const getExplore        = (p=1)  => apiCall(`/posts/?page=${p}`);
export const createPost        = d      => apiCall('/posts/create/', 'POST', d);
export const likePost          = id     => apiCall(`/posts/${id}/like/`, 'POST');
export const getComments       = id     => apiCall(`/posts/${id}/comments/`);
export const addComment        = (id,t) => apiCall(`/posts/${id}/comments/`, 'POST', {text: t});
export const getUserPosts      = uid    => apiCall(`/posts/user/${uid}/`);

export const getStories        = ()     => apiCall('/stories/');
export const createStory       = d      => apiCall('/stories/create/', 'POST', d);
export const viewStory         = id     => apiCall(`/stories/${id}/view/`, 'POST');
export const getUserStories    = uid    => apiCall(`/stories/user/${uid}/`);

export const getReels          = (p=1)  => apiCall(`/reels/?page=${p}`);