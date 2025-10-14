// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const goalInput = document.getElementById('goal-input');
    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');

    generateBtn.addEventListener('click', async () => {
        const goal = goalInput.value.trim();
        if (!goal) {
            alert('Please enter a goal.');
            return;
        }

        // Show loader and clear previous results
        loader.style.display = 'block';
        resultsContainer.innerHTML = '';

        try {
            // Call our backend API
            const response = await fetch('/create-plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ goal: goal }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Hide loader
            loader.style.display = 'none';

            // Display the results
            displayResults(data);

        } catch (error) {
            loader.style.display = 'none';
            resultsContainer.innerHTML = `<p style="color: red;">An error occurred: ${error.message}</p>`;
            console.error('Error:', error);
        }
    });

    function displayResults(data) {
        if (data.error) {
            resultsContainer.innerHTML = `<p style="color: red;">Error from server: ${data.error}</p>`;
            return;
        }

        // Add a title for the project
        const projectTitle = document.createElement('h2');
        projectTitle.textContent = data.project_name || 'Generated Plan';
        resultsContainer.appendChild(projectTitle);

        // Create a card for each task
        data.tasks.forEach(task => {
            const card = document.createElement('div');
            card.className = 'task-card';

            const title = document.createElement('h3');
            title.textContent = `${task.task_id}. ${task.task_name}`;

            const description = document.createElement('p');
            description.textContent = task.description;

            const meta = document.createElement('div');
            meta.className = 'meta';
            const timeline = `<strong>Timeline:</strong> ${task.timeline_days} days`;
            const dependencies = `<strong>Dependencies:</strong> ${task.dependencies.length > 0 ? task.dependencies.join(', ') : 'None'}`;
            meta.innerHTML = `${timeline} | ${dependencies}`;

            card.appendChild(title);
            card.appendChild(description);
            card.appendChild(meta);

            resultsContainer.appendChild(card);
        });
    }
});