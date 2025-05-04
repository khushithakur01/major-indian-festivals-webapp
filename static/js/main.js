let totalSeconds = 300; // e.g., 5 minutes

function startTimer(duration, display) {
    let timer = duration;
    const interval = setInterval(function () {
        const minutes = String(Math.floor(timer / 60)).padStart(2, '0');
        const seconds = String(timer % 60).padStart(2, '0');
        display.textContent = `${minutes}:${seconds}`;

        if (--timer < 0) {
            clearInterval(interval);
            document.getElementById("quiz-form").submit(); // auto-submit
        }
    }, 1000);
}

window.onload = function () {
    const timeDisplay = document.querySelector('#timer');
    if (timeDisplay) {
        startTimer(totalSeconds, timeDisplay);
    }
};
