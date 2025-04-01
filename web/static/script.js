document.addEventListener('DOMContentLoaded', () => {
    // Retrieve the current question number from localStorage or default to 1.
    let currentQuestion = parseInt(localStorage.getItem('questionIndex'), 10) || 1;
    let data = null; // Will hold the questions from /apijson

    // Function to display the current question text in the .text element.
    function showQuestion() {
        const dialogText = document.querySelector('.text');
        if (data[currentQuestion]) {
            dialogText.textContent = data[currentQuestion].text;
        } else {
            dialogText.textContent = 'No more questions!';
        }
    }

    // Fetch the JSON containing all questions/answers.
    fetch('/mise_en_place_d_une_API_a_l_aide_de_Flask')
        .then(response => response.json())
        .then(json => {
            data = json;
            showQuestion();
        })
        .catch(err => {
            console.error('Error fetching JSON:', err);
            document.querySelector('.text').textContent = 'Error loading questions!';
        });

    // Handle form submission: compare typed answer, move to next question if correct.
    const form = document.querySelector('form');
    form.addEventListener('submit', event => {
        event.preventDefault();

        const userInput = document.querySelector('#search');
        const answer = userInput.value.trim();
        userInput.value = '';

        // If there's a question at currentQuestion, we check the answer.
        if (data && data[currentQuestion]) {
            const correctAnswer = data[currentQuestion].answer.trim();
            if (answer.toLowerCase() === correctAnswer.toLowerCase()) {
                // Advance to the next question if correct.
                currentQuestion++;
                localStorage.setItem('questionIndex', currentQuestion);
                showQuestion();
            } else {
                alert('Incorrect! Try again.');
            }
        } else {
            alert('No more questions!');
        }
    });
});
