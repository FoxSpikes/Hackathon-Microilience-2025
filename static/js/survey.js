const questions = document.querySelectorAll('.question');
const nextBtn = document.getElementById('nextBtn');
const prevBtn = document.getElementById('prevBtn');
let current = 0;

function showQuestion(index) {
  questions.forEach((q, i) => q.classList.toggle('active', i === index));
  prevBtn.disabled = index === 0;
  nextBtn.disabled = index === questions.length - 1;
}

nextBtn.addEventListener('click', () => {
  if (current < questions.length - 1) {
    current++;
    showQuestion(current);
  }
});

prevBtn.addEventListener('click', () => {
  if (current > 0) {
    current--;
    showQuestion(current);
  }
});

function selectAnswer(answer) {
  alert("You selected: " + answer);
  if (current < questions.length - 1) {
    current++;
    showQuestion(current);
  }
}

// Initialize first question
showQuestion(current);
