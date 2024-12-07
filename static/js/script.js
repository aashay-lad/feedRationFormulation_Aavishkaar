document.getElementById('nutrition-form').addEventListener('submit', function(event) {
  event.preventDefault();
  
  const age = document.getElementById('age').value;
  const weight = document.getElementById('weight').value;
  const state = document.getElementById('state').value;

  fetch('/calculate', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ age, weight, state })
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById('nutrients').innerText = `Daily Nutrients: Protein: ${data.daily_nutrients.protein}gm, Fiber: ${data.daily_nutrients.fiber}gm`;
      document.getElementById('cost').innerText = `Minimum Cost: Rs.${data.minimum_cost}`;
      document.getElementById('results').style.display = 'block';
  })
  .catch(error => console.error('Error:', error));
});
