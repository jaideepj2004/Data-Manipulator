document.addEventListener("DOMContentLoaded", function() {
    var colors = ['#ff9999', '#99ff99', '#9999ff']; // Array of gradient colors
    var index = 0; // Index of the current color
    var body = document.querySelector('body'); // Select the body element

    setInterval(function() {
        body.style.backgroundColor = colors[index]; // Change the background color
        index = (index + 1) % colors.length; // Move to the next color in the array
    }, 5000); // Change color every 5 seconds (adjust as needed)
});
