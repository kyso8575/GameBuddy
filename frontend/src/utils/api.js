/**
 * API utility functions
 */

// Base API URL
const API_BASE_URL = 'http://localhost:8000';

/**
 * Create a fetch request with authentication headers
 * @param {string} endpoint - API endpoint path (e.g. '/accounts/login/')
 * @param {Object} options - fetch options
 * @returns {Promise} - fetch response Promise
 */
export const fetchWithAuth = async (endpoint, options = {}) => {
  // Get token
  const token = localStorage.getItem('token');
  
  // Set default headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }
  
  // Execute fetch request
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
  
  // Handle 401 Unauthorized response
  if (response.status === 401) {
    // Token expired or invalid
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    // Redirect to login page if needed
    if (window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
  }
  
  return response;
};

/**
 * Create an API request without authentication
 * @param {string} endpoint - API endpoint path
 * @param {Object} options - fetch options
 * @returns {Promise} - fetch response Promise
 */
export const fetchWithoutAuth = async (endpoint, options = {}) => {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  return fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
};

/**
 * Send GET request
 */
export const get = (endpoint) => {
  return fetchWithAuth(endpoint, { method: 'GET' });
};

/**
 * Send POST request
 */
export const post = (endpoint, data) => {
  return fetchWithAuth(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

/**
 * Send POST request without authentication (for login, signup)
 */
export const postWithoutAuth = async (endpoint, data) => {
  console.log(`POST request: ${API_BASE_URL}${endpoint}`, data);
  
  try {
    const response = await fetchWithoutAuth(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
    
    console.log(`Response status: ${response.status}`);
    console.log(`Response headers:`, Object.fromEntries([...response.headers.entries()]));
    
    // Log response content (clone response to check)
    const responseClone = response.clone();
    try {
      const contentType = response.headers.get('content-type');
      console.log('Content-Type:', contentType);
      
      // Handle HTML response
      if (contentType && contentType.includes('text/html')) {
        const htmlText = await responseClone.text();
        console.log('HTML response:', htmlText.substring(0, 500) + '...'); // Show only first 500 chars
        
        // Try to extract error message from HTML
        let errorMessages = [];
        
        // 1. Extract error message from standard Django debug page
        const exceptionMatch = htmlText.match(/<pre class="exception_value">(.*?)<\/pre>/s);
        if (exceptionMatch && exceptionMatch[1]) {
          const rawError = exceptionMatch[1].trim();
          console.log('Extracted error message:', rawError);
          
          // Decode HTML entities (&#x27; -> ' etc.)
          const decodeHTMLEntities = (text) => {
            const textarea = document.createElement('textarea');
            textarea.innerHTML = text;
            return textarea.value;
          };
          
          const decodedError = decodeHTMLEntities(rawError);
          
          // Find errors in format ValidationError: ['This password is too common.']
          const validationMatch = decodedError.match(/ValidationError: \[(.*?)\]/);
          if (validationMatch && validationMatch[1]) {
            console.log('ValidationError content:', validationMatch[1]);
            
            // Split comma-separated error messages into an array
            errorMessages = validationMatch[1].split(',').map(item => 
              item.replace(/['"]/g, '').trim()
            );
          } else if (decodedError.includes('ValidationError')) {
            // Handle other ValidationError formats
            errorMessages = [decodedError.replace('ValidationError:', '').trim()];
          } else {
            // Other error messages
            errorMessages = [decodedError];
          }
        }
        
        // If error messages were extracted, convert to ValidationError
        if (errorMessages.length > 0) {
          const error = new Error('ValidationError');
          error.validationErrors = errorMessages;
          throw error;
        }
        
        throw new Error('Server returned an HTML response. Please check the API endpoint.');
      } else if (contentType && contentType.includes('application/json')) {
        const data = await responseClone.json();
        console.log('Response data:', data);
      } else {
        const text = await responseClone.text();
        console.log('Response text:', text);
      }
    } catch (error) {
      if (error.validationErrors) {
        throw error; // Re-throw if ValidationError extraction succeeded
      }
      console.error('Failed to log response content:', error);
    }
    
    return response;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

/**
 * PUT 요청 보내기
 */
export const put = (endpoint, data) => {
  return fetchWithAuth(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
};

/**
 * DELETE 요청 보내기
 */
export const del = (endpoint) => {
  return fetchWithAuth(endpoint, { method: 'DELETE' });
};

/**
 * Send logout request
 * @returns {Promise} - fetch response Promise
 */
export const logout = async () => {
  try {
    const response = await post('/accounts/logout/');
    if (!response.ok) {
      throw new Error('Logout failed');
    }
    
    // Remove token from local storage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    return true;
  } catch (error) {
    console.error('Logout error:', error);
    // Remove token from local storage even if error occurs
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    return false;
  }
};

export default {
  get,
  post,
  postWithoutAuth,
  put,
  delete: del,
  logout,
}; 