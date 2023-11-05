
function isLoggedIn() {
    // Implement your authentication logic here. 
    // If the user is authenticated, return true; otherwise, return false.
    // You can replace this example logic with your actual authentication mechanism.
    // For example, you might check for a session or a stored token.
    
    // Example: If a user has a session, consider them logged in.
    return sessionStorage.getItem('userSession') !== null;
}

// Check if the user is logged in (you should use your own authentication logic here).
const userIsLoggedIn = isLoggedIn(); // Set to true if the user is logged in, otherwise false.

// Listen for the 'popstate' event (back/forward button clicked)
window.addEventListener('popstate', function(event) {
    if (isLoggedIn) {
        // If the user is logged in, go back to the home page.
        window.location.href = 'home/home.html';
    }
    console.log('JavaScript is working!');
});

function redirectToLoginPage() {
    // Redirect to the login page.
    window.location.href = '../../users/template/users/login.html';
}


