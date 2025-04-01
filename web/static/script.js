document.addEventListener('DOMContentLoaded', () => {
    let currentQuestion = parseInt(localStorage.getItem('questionIndex'), 10) || 1;
    let data = null;

    const textElement = document.querySelector('.text');
    const imgElement = document.querySelector('.display img');

    function showMessage(message, callback) {
        textElement.textContent = message;
        setTimeout(callback, 2000);
    }

    function showQuestion() {
        // Si la question n’existe pas => plus de questions
        if (!data || !data[currentQuestion]) {
            // Affiche un message
            textElement.textContent = 'Il n’y a plus de question.';
            imgElement.src = '';

            // Lance une requête fetch vers /end (méthode POST)
            fetch('/end', {
                method: 'POST'
            })
                .then(response => response.json())
                .then(resData => {
                    console.log('Réponse du serveur:', resData);
                    // Vous pouvez éventuellement rediriger l’utilisateur, etc.
                    // window.location.href = '/somewhere';
                })
                .catch(err => console.error('Erreur lors de l’appel à /end :', err));

            return; // On arrête la fonction ici
        }

        // Sinon on continue normalement
        textElement.textContent = data[currentQuestion].text;
        imgElement.src = data[currentQuestion].img;
    }

    fetch('/mise_en_place_d_une_API_a_l_aide_de_Flask')
        .then(response => response.json())
        .then(json => {
            data = json;
            showQuestion();
        })
        .catch(error => {
            textElement.textContent = 'Erreur de chargement !';
            console.error(error);
        });

    const form = document.querySelector('form');
    form.addEventListener('submit', event => {
        event.preventDefault();

        const userInput = document.querySelector('#search');
        const answer = userInput.value.trim();
        userInput.value = '';

        if (!data || !data[currentQuestion]) {
            textElement.textContent = 'Il n’y a plus de question.';
            return;
        }

        const correctAnswer = data[currentQuestion].answer.trim();

        if (answer.toLowerCase() === correctAnswer.toLowerCase()) {
            showMessage('Bonne réponse !', () => {
                currentQuestion++;
                localStorage.setItem('questionIndex', currentQuestion);
                showQuestion();
            });
        } else {
            showMessage('Mauvaise réponse, réessayez !', () => {
                showQuestion();
            });
        }
    });
});
