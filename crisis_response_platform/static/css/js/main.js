// Connect to Flask-SocketIO
const socket = io();

// Handle incoming mass notifications
socket.on('mass_notification', function(data) {
    showAlertPopup(data.message);
    playAlertSound();
});

// Handle new incidents reported live
socket.on('new_incident', function(data) {
    showIncidentPopup(data.description, data.location);
    playAlertSound();
});

// Play a notification sound
function playAlertSound() {
    const audio = new Audio('/static/sounds/alert.mp3'); // You need to add this sound file
    audio.play();
}

// Show a popup for mass notifications
function showAlertPopup(message) {
    const popup = document.createElement('div');
    popup.className = 'popup-alert';
    popup.innerHTML = `<strong>ALERT:</strong> ${message}`;
    document.body.appendChild(popup);
    
    setTimeout(() => {
        popup.remove();
    }, 5000); // Remove after 5 seconds
}

// Show a popup for incidents
function showIncidentPopup(description, location) {
    const popup = document.createElement('div');
    popup.className = 'popup-incident';
    popup.innerHTML = `<strong>New Incident:</strong> ${description} at ${location}`;
    document.body.appendChild(popup);
    
    setTimeout(() => {
        popup.remove();
    }, 5000); // Remove after 5 seconds
}
