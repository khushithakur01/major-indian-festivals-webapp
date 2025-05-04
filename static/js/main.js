let totalSeconds = 300; // 5 minutes
let current = 0; // Track the current question

const questions = document.querySelectorAll(".quiz-question");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const submitBtn = document.getElementById("submitBtn");
const progressBar = document.getElementById("progressBar");
const questionCounter = document.getElementById("questionCounter");
const questionSelector = document.getElementById("questionSelector");

// Timer function to update time every second
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

    // Show question with navigation buttons
    function showQuestion(index) {
        questions.forEach((q, i) => {
            q.classList.toggle("d-none", i !== index);
        });

        // Update question counter
        questionCounter.textContent = `Question ${index + 1} of ${questions.length}`;

        // Update progress bar
        const progress = Math.floor(((index + 1) / questions.length) * 100);
        progressBar.style.width = `${progress}%`;
        progressBar.textContent = `${progress}%`;

        // Enable/Disable buttons based on position
        prevBtn.disabled = index === 0;
        nextBtn.classList.toggle("d-none", index === questions.length - 1);
        submitBtn.classList.toggle("d-none", index !== questions.length - 1);

        // Update the dropdown to reflect the current question
        questionSelector.value = index;
    }

    // Check if a question is answered
    function isAnswered(index) {
        const inputs = questions[index].querySelectorAll("input[type='radio']");
        return Array.from(inputs).some(input => input.checked);
    }

    // Handle previous button click
    prevBtn.addEventListener("click", () => {
        if (current > 0) current--;
        showQuestion(current);
    });

    // Handle next button click
    nextBtn.addEventListener("click", () => {
        if (!isAnswered(current)) {
            const warning = questions[current].querySelector('.warning-message');
            if (warning) warning.classList.remove("d-none");
            return;
        }
        if (current < questions.length - 1) current++;
        showQuestion(current);
    });

    // Handle jump to specific question from dropdown
    questionSelector.addEventListener('change', function (e) {
        current = parseInt(e.target.value);
        showQuestion(current);
    });

    // Show the first question on load
    showQuestion(current);
};
