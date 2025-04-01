document.addEventListener('DOMContentLoaded', async () => {
    let data = null;
    let currentQuestion = 1;

    const textElement = document.querySelector('.text');
    const imgElement = document.querySelector('.display img');
    const userInput = document.querySelector('#search');
    const form = document.querySelector('form');

    // Récupère l'index du serveur
    async function loadIndex() {
        try {
            const response = await fetch('/get_index');
            const json = await response.json();
            currentQuestion = json.currentIndex || 1;
        } catch (err) {
            console.error('Erreur en récupérant l’index:', err);
        }
    }

    // Met à jour l'index côté serveur
    async function saveIndex(index) {
        try {
            await fetch('/set_index', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index })
            });
        } catch (err) {
            console.error('Erreur en sauvegardant l’index:', err);
        }
    }

    // Fonction « machine à écrire » pour animer lettre par lettre
    function typeText(element, text, speed = 40, callback) {
        let i = 0;
        element.textContent = ''; // On s'assure de vider le contenu avant l'animation

        const timer = setInterval(() => {
            element.textContent += text.charAt(i);
            i++;
            if (i >= text.length) {
                clearInterval(timer);
                if (callback) callback();
            }
        }, speed);
    }

    function showMessage(message, callback) {
        textElement.textContent = message;
        setTimeout(callback, 2000);
    }

    // -- NOUVELLE FONCTION --
    // Récupère la valeur FIDE_ELO depuis une route (ex. /get_fide_elo)
    // et remplace la réponse de la question "17" par cette valeur
    async function updateAnswer17WithFIDE() {
        try {
            const resp = await fetch('/get_fide_elo');
            // Cette route doit renvoyer un JSON du type { "fide_elo": "..." }
            const dataElo = await resp.json();

            // On vérifie si la question "17" existe
            if (data['17']) {
                data['17'].answer = dataElo.fide_elo;  // On met à jour la réponse
            }
        } catch (err) {
            console.error('Erreur en récupérant le FIDE_ELO :', err);
        }
    }

    // Affiche la question actuelle (ou signale la fin)
    function showQuestion() {
        if (!data || !data[currentQuestion]) {
            textElement.textContent = 'Il n’y a plus de question.';
            imgElement.src = '';

            // Appel au serveur pour signaler la fin
            fetch('/end', { method: 'POST' })
                .then(res => res.json())
                .then(resData => console.log('Réponse de /end :', resData))
                .catch(err => console.error('Erreur lors de l’appel à /end :', err));

            return;
        }

        const question = data[currentQuestion];
        imgElement.src = question.img;

        // Ajuster le placeholder : soit on attend une réponse, soit on attend la barre d'espace
        if (question.answer.trim() === '') {
            userInput.placeholder = '-- Press space --';
        } else {
            userInput.placeholder = 'Tapez votre réponse ici...';
        }

        // On anime le texte lettre par lettre
        typeText(textElement, question.text, 40);
    }

    // -- CHARGEMENT INITIAL DES DONNÉES --
    try {
        // 1) Charger l’index depuis le serveur
        await loadIndex();

        // 2) Charger toutes les questions
        const response = await fetch('/mise_en_place_d_une_API_a_l_aide_de_Flask');
        data = await response.json();

        // 3) Mettre à jour la question #17 avec FIDE_ELO
        //    (récupéré depuis /get_fide_elo qui appelle web/state.py)
        await updateAnswer17WithFIDE();

        // 4) Afficher la question
        showQuestion();

    } catch (err) {
        textElement.textContent = 'Erreur de chargement des questions !';
        console.error(err);
    }

    // Gère la soumission (si la question attend réellement une réponse)
    form.addEventListener('submit', event => {
        event.preventDefault();

        if (!data || !data[currentQuestion]) {
            textElement.textContent = 'Il n’y a plus de question.';
            return;
        }

        const answer = userInput.value.trim();
        userInput.value = '';

        const correctAnswer = data[currentQuestion].answer.trim();

        // Si la réponse attendue est vide => on ne fait rien sur submit
        if (correctAnswer === '') {
            return;
        }

        // Comparer la réponse
        if (answer.toLowerCase() === correctAnswer.toLowerCase()) {
            showMessage('Bonne réponse !', async () => {
                currentQuestion++;
                await saveIndex(currentQuestion);
                showQuestion();
            });
        } else {
            showMessage('Mauvaise réponse, réessayez !', () => {
                showQuestion();
            });
        }
    });

    // Gère l’appui sur la barre d’espace si la réponse attendue est vide
    document.addEventListener('keydown', async event => {
        if (event.code === 'Space' || event.key === ' ') {
            if (data && data[currentQuestion] && data[currentQuestion].answer.trim() === '') {
                event.preventDefault(); // Empêche le scroll
                currentQuestion++;
                await saveIndex(currentQuestion);
                showQuestion();
            }
        }
    });
});
